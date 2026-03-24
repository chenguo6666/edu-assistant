"""LLM 初始化：通过硅基流动 OpenAI 兼容接口接入通义千问"""
from langchain_openai import ChatOpenAI
from config import settings


def get_llm(streaming: bool = True, lite: bool = False):
    """获取 LLM 实例

    Args:
        streaming: 是否启用流式输出
        lite: 是否使用轻量模型（122B）
    """
    model = settings.SILICONFLOW_MODEL_LITE if lite else settings.SILICONFLOW_MODEL
    return ChatOpenAI(
        model=model,
        openai_api_key=settings.SILICONFLOW_API_KEY,
        openai_api_base=settings.SILICONFLOW_BASE_URL,
        temperature=0.7,
        streaming=streaming,
        max_tokens=4096,
    )
