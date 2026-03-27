"""Embedding 模型初始化：通过硅基流动 OpenAI 兼容接口"""
from langchain_openai import OpenAIEmbeddings
from config import settings

# Embedding 模型使用 BAAI/bge-m3（1024 维，中英文效果好）
_embeddings = None


def get_embeddings():
    """获取 Embedding 实例（单例）"""
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(
            model="BAAI/bge-m3",
            openai_api_key=settings.SILICONFLOW_API_KEY,
            openai_api_base=settings.SILICONFLOW_BASE_URL,
        )
    return _embeddings
