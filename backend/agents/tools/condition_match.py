"""条件匹配推荐工具"""
from langchain_core.tools import tool


@tool
def match_schools(conditions: str) -> str:
    """根据学生的具体条件，从知识库检索并推荐合适的高校。

    Args:
        conditions: 学生的条件描述，如"GPA3.5，专业排名15%，有一篇会议论文，想去北京或上海"
    """
    try:
        from rag.vector_store import get_vector_store
        from rag.retriever import retrieve_docs
        vector_store = get_vector_store("admission_knowledge")
        # 用条件作为查询，检索匹配的院校
        query = f"CS保研申请条件 {conditions}"
        return retrieve_docs(vector_store, query, k=4)
    except Exception as e:
        return f"匹配失败: {str(e)}"
