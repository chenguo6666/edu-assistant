"""对话与消息数据模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), default="新对话")
    mode = Column(String(20), default="edu")            # edu / admission
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, index=True)
    role = Column(String(10), nullable=False)            # user / assistant
    content = Column(Text, nullable=False)
    agent_steps = Column(Text, nullable=True)            # Agent 中间步骤（JSON）
    created_at = Column(DateTime, default=datetime.utcnow)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(20), nullable=False)
    chunk_count = Column(Integer, default=0)
    collection_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
