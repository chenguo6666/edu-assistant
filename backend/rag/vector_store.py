"""向量存储管理：ChromaDB 本地持久化"""
import os
from langchain_chroma import Chroma
from rag.embeddings import get_embeddings

# ChromaDB 持久化目录
CHROMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")


def get_vector_store(collection_name: str) -> Chroma:
    """获取指定 Collection 的向量存储"""
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DIR,
    )


def get_user_collection_name(user_id: int) -> str:
    """用户文档 Collection 名"""
    return f"user_{user_id}_docs"


def delete_collection(collection_name: str):
    """删除整个 Collection（用户删除文档时）"""
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass


def delete_documents_by_source(collection_name: str, source: str):
    """按来源文件路径删除向量（删除单个文档时）"""
    store = get_vector_store(collection_name)
    # ChromaDB 支持按 metadata 过滤删除
    results = store.get(where={"source": source})
    if results and results.get("ids"):
        store.delete(ids=results["ids"])
