"""用户相关的请求/响应模型"""
from typing import Optional, List
from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserProfile(BaseModel):
    """用户中心可编辑字段"""
    grade: Optional[str] = None
    major: Optional[str] = None
    subjects: Optional[List[str]] = None
    gpa: Optional[float] = None


class UserResponse(BaseModel):
    id: int
    username: str
    grade: Optional[str] = None
    major: Optional[str] = None
    subjects: Optional[List[str]] = None
    gpa: Optional[float] = None

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
