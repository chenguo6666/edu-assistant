"""保研时间线查询工具"""
from langchain_core.tools import tool


@tool
def query_admission_timeline(query: str) -> str:
    """查询CS专业预推免的时间安排、流程和注意事项。

    Args:
        query: 查询内容，如"保研什么时候报名"、"预推免流程"、"推免系统什么时候开放"
    """
    try:
        from rag.vector_store import get_vector_store
        from rag.retriever import retrieve_docs
        vector_store = get_vector_store("admission_knowledge")
        return retrieve_docs(vector_store, query, k=3)
    except Exception as e:
        return f"查询失败: {str(e)}"
