"""习题生成工具"""
from langchain_core.tools import tool
from agents.llm import get_llm


@tool
def generate_quiz(text: str, quiz_type: str = "choice", count: int = 5) -> str:
    """根据学习材料生成练习题。

    Args:
        text: 需要生成习题的学习材料内容
        quiz_type: 题型，可选 choice（选择题）、fill（填空题）、short_answer（简答题）
        count: 生成题目数量，默认5题
    """
    type_map = {
        "choice": "选择题（每题4个选项A/B/C/D，标注正确答案）",
        "fill": "填空题（用____标注需要填写的位置）",
        "short_answer": "简答题",
    }
    type_desc = type_map.get(quiz_type, type_map["choice"])

    llm = get_llm(streaming=False, lite=True)
    prompt = f"""请根据以下学习材料生成{count}道{type_desc}：

{text[:3000]}

要求：
1. 题目应紧扣材料内容
2. 难度适中，覆盖不同知识点
3. 每道题后附上参考答案
4. 使用中文出题"""
    response = llm.invoke(prompt)
    return response.content
