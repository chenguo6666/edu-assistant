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
    llm = get_llm(streaming=False, lite=False)
    prompt = f"""请根据以下学习材料生成{count}道单选题，每题4个选项（A/B/C/D）。

{text[:3000]}

输出格式要求（严格按此格式，每道题独立完整）：
1. 题目内容（）
A. 选项内容
B. 选项内容
C. 选项内容
D. 选项内容
答案：X
解析：简要说明正确答案的理由

2. 题目内容（）
A. ...
（依此类推）

其他要求：
- 题目紧扣材料内容，难度适中，覆盖不同知识点
- 每道题生成完后立即附上答案和解析，不要先列完所有题目再统一给答案
- 只输出题目内容，不要有其他说明文字
- 使用中文出题"""
    response = llm.invoke(prompt)
    return response.content
