"""院校信息查询工具"""
from langchain_core.tools import tool


@tool
def query_school_info(query: str) -> str:
    """查询高校CS专业的保研信息，包括申请条件、考核方式、联系方式等。

    Args:
        query: 查询内容，如"清华大学CS保研条件"、"浙大计算机保研要求"
    """
    try:
        from rag.vector_store import get_vector_store
        from rag.retriever import retrieve_docs
        vector_store = get_vector_store("admission_knowledge")
        return retrieve_docs(vector_store, query, k=3)
    except Exception as e:
        return f"查询失败: {str(e)}"
