"""学习计划生成工具"""
from langchain_core.tools import tool
from agents.llm import get_llm


@tool
def generate_study_plan(subject: str, duration: str = "1周", goal: str = "") -> str:
    """为学生生成个性化学习计划。

    Args:
        subject: 学习科目或主题
        duration: 学习周期，如"1周"、"1个月"
        goal: 学习目标，如"期末考试复习"、"掌握基础概念"
    """
    llm = get_llm(streaming=False, lite=False)
    goal_text = f"，学习目标为：{goal}" if goal else ""
    prompt = f"""请为学生制定一份{subject}的{duration}学习计划{goal_text}。

要求：
1. 按天分配学习内容，每天不超过2行描述
2. 仅列出最核心的学习任务，不展开细节
3. 末尾一句话给出学习方法建议
4. 总字数控制在300字以内，使用中文回答"""
    response = llm.invoke(prompt)
    return response.content
