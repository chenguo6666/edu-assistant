"""聊天相关的请求/响应模型"""
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """WebSocket 接收的用户消息"""
    type: str = "message"
    content: str
