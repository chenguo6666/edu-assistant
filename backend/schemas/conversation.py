"""对话相关的请求/响应模型"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class ConversationCreate(BaseModel):
    mode: str = "edu"  # edu / admission


class ConversationUpdate(BaseModel):
    title: Optional[str] = None


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    agent_steps: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationResponse(BaseModel):
    id: int
    title: str
    mode: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConversationDetail(ConversationResponse):
    messages: List[MessageResponse] = []
