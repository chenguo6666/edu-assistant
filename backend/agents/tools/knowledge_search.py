"""知识库检索工具：从用户上传的文档中检索相关内容"""
from langchain_core.tools import tool


def make_knowledge_search_tool(user_id: int):
    """为特定用户创建知识库检索工具（工厂函数）"""
    from rag.vector_store import get_vector_store, get_user_collection_name
    from rag.retriever import retrieve_docs

    @tool
    def search_knowledge_base(query: str) -> str:
        """从用户上传的文档知识库中检索相关内容。当需要基于用户提供的文档资料回答问题时使用此工具。

        Args:
            query: 检索查询词
        """
        try:
            collection_name = get_user_collection_name(user_id)
            vector_store = get_vector_store(collection_name)
            return retrieve_docs(vector_store, query)
        except Exception as e:
            return f"知识库检索失败: {str(e)}"

    return search_knowledge_base
