"""RAG 检索器：从向量库中检索相关文档"""
from langchain_core.vectorstores import VectorStore


def get_retriever(vector_store: VectorStore, k: int = 4):
    """获取相似度检索器，返回 top-k 相关文档"""
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )


def retrieve_docs(vector_store: VectorStore, query: str, k: int = 4) -> str:
    """直接检索并返回格式化的文档内容（供工具调用）"""
    retriever = get_retriever(vector_store, k)
    docs = retriever.invoke(query)

    if not docs:
        return "知识库中未找到相关内容。"

    result_parts = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("filename", "未知来源")
        result_parts.append(f"[片段 {i}]（来自：{source}）\n{doc.page_content}")

    return "\n\n".join(result_parts)
