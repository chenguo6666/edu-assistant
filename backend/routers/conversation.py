"""对话管理路由：对话的增删查改"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.conversation import Conversation, Message
from schemas.conversation import (
    ConversationCreate, ConversationUpdate, ConversationResponse,
    ConversationDetail, MessageResponse,
)
from services.auth_service import get_current_user

router = APIRouter(prefix="/api/conversations", tags=["对话"])


@router.get("", response_model=list[ConversationResponse])
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取当前用户的对话列表，按更新时间倒序"""
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )


@router.post("", response_model=ConversationResponse)
def create_conversation(
    data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """创建新对话"""
    conv = Conversation(user_id=current_user.id, mode=data.mode)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


@router.get("/{conversation_id}", response_model=ConversationDetail)
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取对话详情（含消息历史）"""
    conv = _get_user_conversation(db, conversation_id, current_user.id)
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conv.id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return ConversationDetail(
        id=conv.id,
        title=conv.title,
        mode=conv.mode,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        messages=[MessageResponse.model_validate(m) for m in messages],
    )


@router.put("/{conversation_id}", response_model=ConversationResponse)
def update_conversation(
    conversation_id: int,
    data: ConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新对话标题"""
    conv = _get_user_conversation(db, conversation_id, current_user.id)
    if data.title is not None:
        conv.title = data.title
    conv.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conv)
    return conv


@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除对话及其所有消息"""
    conv = _get_user_conversation(db, conversation_id, current_user.id)
    db.query(Message).filter(Message.conversation_id == conv.id).delete()
    db.delete(conv)
    db.commit()
    return {"detail": "对话已删除"}


def _get_user_conversation(db: Session, conversation_id: int, user_id: int) -> Conversation:
    """获取属于当前用户的对话，不存在则 404"""
    conv = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
        .first()
    )
    if not conv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="对话不存在")
    return conv
