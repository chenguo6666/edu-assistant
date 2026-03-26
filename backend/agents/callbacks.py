"""自定义 Callback：通过 WebSocket 推送 Agent 中间步骤给前端"""
import json
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.outputs import LLMResult


class WebSocketCallbackHandler(AsyncCallbackHandler):
    """将 Agent 执行过程中的事件通过 WebSocket 推送给前端"""

    def __init__(self, websocket):
        self.websocket = websocket
        self.step_count = 0

    async def _send(self, data: dict):
        """发送 JSON 消息到 WebSocket"""
        try:
            await self.websocket.send_json(data)
        except Exception:
            pass

    async def on_chat_model_start(self, serialized, messages, **kwargs) -> None:
        """Chat 模型开始调用时触发（新版 LangChain 要求实现）"""
        pass

    async def on_agent_action(self, action: AgentAction, **kwargs) -> None:
        """Agent 决定调用工具时触发"""
        self.step_count += 1
        await self._send({
            "type": "tool_call",
            "data": {
                "step_number": self.step_count,
                "tool_name": action.tool,
                "input": str(action.tool_input),
                "status": "running",
            },
        })

    async def on_tool_end(self, output: str, **kwargs) -> None:
        """工具执行完成时触发"""
        # 截断过长的输出
        display_output = output[:500] + "..." if len(output) > 500 else output
        await self._send({
            "type": "tool_result",
            "data": {
                "step_number": self.step_count,
                "output": display_output,
                "status": "done",
            },
        })

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        """LLM 生成新 token 时触发（流式输出）"""
        if token:
            await self._send({"type": "token", "content": token})

    async def on_agent_finish(self, finish: AgentFinish, **kwargs) -> None:
        """Agent 执行结束时触发"""
        pass

    async def on_llm_error(self, error: BaseException, **kwargs) -> None:
        """LLM 调用出错时触发"""
        await self._send({"type": "error", "content": f"LLM 调用失败: {str(error)}"})

    async def on_tool_error(self, error: BaseException, **kwargs) -> None:
        """工具执行出错时触发"""
        await self._send({
            "type": "tool_result",
            "data": {
                "step_number": self.step_count,
                "output": f"工具执行失败: {str(error)}",
                "status": "error",
            },
        })
