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


def add_documents_batch(
    collection_name: str, 
    documents: List[Document], 
    batch_size: int = 100
):
    """批量添加文档，避免一次性加载过多"""
    store = get_vector_store(collection_name)
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        store.add_documents(batch)
        logger.info(f"已添加 {min(i+batch_size, len(documents))}/{len(documents)} 个文档")
    
    return store


def delete_documents_by_source(collection_name: str, source: str):
    """按来源文件路径删除向量（删除单个文档时）"""
    try:
        store = get_vector_store(collection_name)
        # 先检查是否存在
        results = store.get(where={"source": source})
        if results and results.get("ids"):
            store.delete(ids=results["ids"])
            logger.info(f"已删除 {len(results['ids'])} 个文档块，来源: {source}")
            return True
        return False
    except Exception as e:
        logger.error(f"删除失败 {source}: {str(e)}")
        return False