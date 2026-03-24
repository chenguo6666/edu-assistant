"""用户数据模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    grade = Column(String(20), nullable=True)          # 年级
    major = Column(String(100), nullable=True)          # 专业
    subjects = Column(Text, nullable=True)              # 感兴趣学科（JSON 数组）
    gpa = Column(Float, nullable=True)                  # GPA
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
