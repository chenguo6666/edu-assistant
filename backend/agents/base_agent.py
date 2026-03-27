"""Agent 基类：封装 LLM、工具注册、Prompt 模板、AgentExecutor"""
from typing import List, Optional, Dict
from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor
from agents.llm import get_llm


class BaseAgent:
    """Agent 基类，教育 Agent 和保研 Agent 继承此类"""

    def __init__(
        self,
        system_prompt: str,
        tools: List[BaseTool],
        user_profile: Optional[Dict] = None,
    ):
        self.llm = get_llm(streaming=True)
        self.tools = tools
        self.system_prompt = self._build_prompt(system_prompt, user_profile)
        self.agent = self._create_agent()
        self.executor = self._create_executor()

    def _build_prompt(self, base_prompt: str, user_profile: Optional[Dict]) -> str:
        """将用户画像信息注入 system prompt"""
        prompt = base_prompt
        if user_profile:
            profile_parts = []
            if user_profile.get("grade"):
                profile_parts.append(f"年级：{user_profile['grade']}")
            if user_profile.get("major"):
                profile_parts.append(f"专业：{user_profile['major']}")
            if user_profile.get("subjects"):
                profile_parts.append(f"感兴趣学科：{', '.join(user_profile['subjects'])}")
            if user_profile.get("gpa"):
                profile_parts.append(f"GPA：{user_profile['gpa']}")
            if profile_parts:
                prompt += f"\n\n当前用户信息：\n" + "\n".join(profile_parts)
        return prompt

    def _create_agent(self):
        """创建 Agent 实例"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ])
        return create_openai_tools_agent(self.llm, self.tools, prompt)

    def _create_executor(self) -> AgentExecutor:
        """创建 AgentExecutor"""
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=10,
            return_intermediate_steps=True,
            handle_parsing_errors=True,
        )

    async def arun(self, user_input: str, chat_history: list = None, callbacks: list = None):
        """异步执行 Agent"""
        return await self.executor.ainvoke(
            {
                "input": user_input,
                "chat_history": chat_history or [],
            },
            config={"callbacks": callbacks or []},
        )
