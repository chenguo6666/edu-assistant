"""知识库文档管理路由：上传、列表、删除"""
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime
from database import get_db
from models.user import User
from models.conversation import Document
from services.auth_service import get_current_user
from rag.document_loader import load_and_split
from rag.vector_store import get_vector_store, get_user_collection_name, delete_documents_by_source

router = APIRouter(prefix="/api/knowledge", tags=["知识库"])

# 上传目录
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    chunk_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """上传文档并向量化入库"""
    # 验证文件类型
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型，仅支持: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # 读取并检查文件大小
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件大小超过限制（10MB）",
        )

    # 保存文件到 uploads 目录
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    safe_name = f"{current_user.id}_{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, safe_name)
    with open(file_path, "wb") as f:
        f.write(content)

    try:
        # 加载、分块、向量化
        chunks = load_and_split(file_path, file.filename)
        collection_name = get_user_collection_name(current_user.id)
        vector_store = get_vector_store(collection_name)
        vector_store.add_documents(chunks)

        # 记录到数据库
        doc = Document(
            user_id=current_user.id,
            filename=file.filename,
            file_path=file_path,
            file_type=ext.lstrip("."),
            chunk_count=len(chunks),
            collection_name=collection_name,
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc

    except Exception as e:
        # 出错时清理已上传的文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文档处理失败: {str(e)}",
        )


@router.get("/documents", response_model=List[DocumentResponse])
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取当前用户已上传的文档列表"""
    return (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .order_by(Document.created_at.desc())
        .all()
    )


@router.delete("/documents/{doc_id}")
def delete_document(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除文档及其向量索引"""
    doc = (
        db.query(Document)
        .filter(Document.id == doc_id, Document.user_id == current_user.id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文档不存在")

    # 从向量库删除（失败不影响数据库删除）
    try:
        delete_documents_by_source(doc.collection_name, doc.file_path)
    except Exception:
        pass

    # 删除文件（失败不影响数据库删除）
    try:
        if os.path.exists(doc.file_path):
            os.remove(doc.file_path)
    except Exception:
        pass

    # 删除数据库记录（核心操作）
    db.delete(doc)
    db.commit()
    return {"detail": "文档已删除"}
