"""知识点提取工具"""
from langchain_core.tools import tool
from agents.llm import get_llm


@tool
def extract_knowledge(text: str) -> str:
    """从学习材料中提取核心知识点，形成结构化的知识点列表。输入为需要提取知识点的文本内容。"""
    llm = get_llm(streaming=False, lite=True)
    prompt = f"""请从以下学习材料中提取核心知识点：

{text[:3000]}

要求：
1. 按重要程度排列知识点
2. 每个知识点用一句话概括
3. 标注知识点之间的关联关系（如有）
4. 使用中文回答"""
    response = llm.invoke(prompt)
    return response.content
