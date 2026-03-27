"""认证路由：注册、登录、获取当前用户"""
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from services.auth_service import hash_password, verify_password, create_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")

    user = User(username=data.username, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(user.id)
    return TokenResponse(
        access_token=token,
        user=_build_user_response(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    token = create_token(user.id)
    return TokenResponse(
        access_token=token,
        user=_build_user_response(user),
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return _build_user_response(current_user)


def _build_user_response(user: User) -> UserResponse:
    """构建用户响应，处理 subjects JSON 反序列化"""
    subjects = None
    if user.subjects:
        try:
            subjects = json.loads(user.subjects)
        except json.JSONDecodeError:
            subjects = None

    return UserResponse(
        id=user.id,
        username=user.username,
        grade=user.grade,
        major=user.major,
        subjects=subjects,
        gpa=user.gpa,
    )
