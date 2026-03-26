"""文本总结工具"""
from langchain_core.tools import tool
from agents.llm import get_llm


@tool
def summarize(text: str) -> str:
    """对输入的学习材料或课文进行总结归纳，提取核心内容。输入为需要总结的文本内容。"""
    llm = get_llm(streaming=False, lite=False)
    prompt = f"""请对以下内容进行简洁、准确的总结归纳，提取核心要点：

{text[:3000]}

要求：
1. 用清晰的条目列出主要内容
2. 保留关键信息，去除冗余
3. 使用中文回答"""
    response = llm.invoke(prompt)
    return response.content
