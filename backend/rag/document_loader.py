"""文档加载与分块：支持 PDF / TXT / DOCX / MD"""
import os
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_document(file_path: str, filename: str) -> List[Document]:
    """根据文件类型加载文档，返回 Document 列表"""
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        from langchain_community.document_loaders import PyPDFLoader
        loader = PyPDFLoader(file_path)
        docs = loader.load()
    elif ext in (".txt", ".md"):
        from langchain_community.document_loaders import TextLoader
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()
    elif ext == ".docx":
        from langchain_community.document_loaders import Docx2txtLoader
        loader = Docx2txtLoader(file_path)
        docs = loader.load()
    else:
        raise ValueError(f"不支持的文件类型: {ext}")

    # 给每个文档添加来源 metadata
    for doc in docs:
        doc.metadata["source"] = file_path
        doc.metadata["filename"] = filename

    return docs


def split_documents(docs: List[Document]) -> List[Document]:
    """将文档分块，适合中英文混合内容"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
        separators=["\n\n", "\n", "。", ".", "！", "？", "!", "?", " ", ""],
    )
    return splitter.split_documents(docs)


def load_and_split(file_path: str, filename: str) -> List[Document]:
    """加载并分块，返回可直接向量化的 chunks"""
    docs = load_document(file_path, filename)
    return split_documents(docs)
