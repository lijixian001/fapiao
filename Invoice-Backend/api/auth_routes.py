from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.auth import get_current_user
from schemas.user import UserLogin, LoginResponse, UserResponse
from schemas.common import ResponseModel
from services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login", response_model=ResponseModel[LoginResponse])
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    result = AuthService.login(db, user_data.username, user_data.password)
    return ResponseModel(data=result, message="登录成功")


@router.post("/logout", response_model=ResponseModel)
def logout(current_user: dict = Depends(get_current_user)):
    return ResponseModel(message="登出成功")


@router.get("/userinfo", response_model=ResponseModel[UserResponse])
def get_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = AuthService.get_user_info(db, current_user["user_id"])
    return ResponseModel(data=user)
