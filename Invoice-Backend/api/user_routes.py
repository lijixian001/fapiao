from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from core.database import get_db
from core.auth import get_current_user
from schemas.user import UserCreate, UserUpdate, UserResponse
from schemas.common import ResponseModel, PageResponse
from services.user_service import UserService

router = APIRouter(prefix="/api/user", tags=["用户管理"])


@router.get("", response_model=ResponseModel[PageResponse[UserResponse]])
def list_users(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    result = UserService.list_users(db, page=page, page_size=page_size, keyword=keyword)
    return ResponseModel(data=result)


@router.get("/{user_id}", response_model=ResponseModel[UserResponse])
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        return ResponseModel(code=404, message="用户不存在", data=None)
    return ResponseModel(data=user)


@router.post("", response_model=ResponseModel[UserResponse])
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user = UserService.create_user(db, user_data, created_by=current_user["user_id"])
    return ResponseModel(data=user, message="创建成功")


@router.put("/{user_id}", response_model=ResponseModel[UserResponse])
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user = UserService.update_user(db, user_id, user_data)
    return ResponseModel(data=user, message="更新成功")


@router.delete("/{user_id}", response_model=ResponseModel)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    UserService.delete_user(db, user_id)
    return ResponseModel(message="删除成功")
