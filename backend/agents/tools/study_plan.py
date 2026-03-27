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
    llm = get_llm(streaming=False, lite=True)
    goal_text = f"，学习目标为：{goal}" if goal else ""
    prompt = f"""请为学生制定一份{subject}的{duration}学习计划{goal_text}。

要求：
1. 按天/周合理分配学习内容
2. 包含具体的学习任务和建议学习时长
3. 穿插复习和自测环节
4. 给出学习方法建议
5. 使用中文回答"""
    response = llm.invoke(prompt)
    return response.content
