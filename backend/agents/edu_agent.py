"""通用教育助手 Agent"""
from typing import Optional, Dict
from agents.base_agent import BaseAgent
from agents.tools.summarize import summarize
from agents.tools.quiz_generator import generate_quiz
from agents.tools.knowledge_extractor import extract_knowledge
from agents.tools.study_plan import generate_study_plan
from agents.tools.web_search import web_search

EDU_SYSTEM_PROMPT = """你是一个专业的教育助手 AI，专注于帮助学生高效学习。

你拥有以下工具能力：
1. **文本总结** (summarize)：对学习材料进行总结归纳
2. **习题生成** (generate_quiz)：根据内容生成选择题、填空题、简答题
3. **知识点提取** (extract_knowledge)：从文本中提取核心知识点
4. **学习计划生成** (generate_study_plan)：制定个性化学习计划
5. **联网搜索** (web_search)：搜索互联网获取最新信息
6. **知识库检索** (search_knowledge_base)：从用户上传的文档中检索相关内容

工作原则：
- 当用户提出复合任务时（如"总结课文并生成习题"），你应该拆解任务，依次调用对应工具完成
- 先理解用户意图，选择最合适的工具
- 如果用户询问其上传的文档内容，优先使用 search_knowledge_base 工具
- 如果用户的问题不需要使用工具，直接用你的知识回答即可
- 回答始终使用中文，内容准确、简洁、有条理
- 对于生成的习题，确保答案正确"""


def create_edu_agent(user_id: Optional[int] = None, user_profile: Optional[Dict] = None) -> BaseAgent:
    """创建通用教育助手 Agent

    Args:
        user_id: 用户 ID，用于创建知识库检索工具
        user_profile: 用户画像，用于个性化回答
    """
    tools = [summarize, generate_quiz, extract_knowledge, generate_study_plan, web_search]

    # 如果有用户 ID，动态注入知识库检索工具
    if user_id is not None:
        from agents.tools.knowledge_search import make_knowledge_search_tool
        tools.append(make_knowledge_search_tool(user_id))

    return BaseAgent(
        system_prompt=EDU_SYSTEM_PROMPT,
        tools=tools,
        user_profile=user_profile,
    )
