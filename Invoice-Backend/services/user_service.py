from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional

from models.sys_user import SysUser
from schemas.user import UserCreate, UserUpdate
from core.auth import hash_password


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[SysUser]:
        return db.query(SysUser).filter(SysUser.id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[SysUser]:
        return db.query(SysUser).filter(SysUser.username == username).first()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate, created_by: int = None) -> SysUser:
        existing_user = UserService.get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        hashed_password = hash_password(user_data.password)
        db_user = SysUser(
            username=user_data.username,
            password=hashed_password,
            real_name=user_data.real_name,
            role_id=user_data.role_id,
            email=user_data.email,
            phone=user_data.phone,
            created_by=created_by
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> SysUser:
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        db.delete(user)
        db.commit()
        return True

    @staticmethod
    def list_users(
        db: Session,
        page: int = 1,
        page_size: int = 10,
        keyword: Optional[str] = None
    ) -> dict:
        query = db.query(SysUser)
        
        if keyword:
            query = query.filter(
                (SysUser.username.like(f"%{keyword}%")) |
                (SysUser.real_name.like(f"%{keyword}%"))
            )
        
        total = query.count()
        users = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "list": users
        }
