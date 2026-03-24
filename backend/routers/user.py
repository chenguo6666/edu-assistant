"""用户中心路由：更新个人资料"""
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserProfile, UserResponse
from services.auth_service import get_current_user

router = APIRouter(prefix="/api/user", tags=["用户"])


@router.put("/profile", response_model=UserResponse)
def update_profile(
    data: UserProfile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新用户个人资料"""
    if data.grade is not None:
        current_user.grade = data.grade
    if data.major is not None:
        current_user.major = data.major
    if data.subjects is not None:
        current_user.subjects = json.dumps(data.subjects, ensure_ascii=False)
    if data.gpa is not None:
        current_user.gpa = data.gpa

    db.commit()
    db.refresh(current_user)

    subjects = None
    if current_user.subjects:
        try:
            subjects = json.loads(current_user.subjects)
        except json.JSONDecodeError:
            subjects = None

    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        grade=current_user.grade,
        major=current_user.major,
        subjects=subjects,
        gpa=current_user.gpa,
    )
