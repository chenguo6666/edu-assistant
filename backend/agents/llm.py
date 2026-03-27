"""LLM 初始化：通过 DeepSeek OpenAI 兼容接口接入 deepseek-chat"""
from langchain_openai import ChatOpenAI
from config import settings


def get_llm(streaming: bool = True, lite: bool = False):
    """获取 LLM 实例

    Args:
        streaming: 是否启用流式输出
        lite: 参数保留兼容性，DeepSeek 目前统一使用 deepseek-chat
    """
    # 硅基流动（已停用，保留供回退参考）
    # from langchain_openai import ChatOpenAI
    # model = settings.SILICONFLOW_MODEL_LITE if lite else settings.SILICONFLOW_MODEL
    # return ChatOpenAI(
    #     model=model,
    #     openai_api_key=settings.SILICONFLOW_API_KEY,
    #     openai_api_base=settings.SILICONFLOW_BASE_URL,
    #     temperature=0.7,
    #     streaming=streaming,
    #     max_tokens=4096,
    # )

    return ChatOpenAI(
        model=settings.DEEPSEEK_MODEL,
        openai_api_key=settings.DEEPSEEK_API_KEY,
        openai_api_base=settings.DEEPSEEK_BASE_URL,
        temperature=0.7,
        streaming=streaming,
        max_tokens=4096,
    )
