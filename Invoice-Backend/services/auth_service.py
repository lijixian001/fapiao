from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.sys_user import SysUser, USER_STATUS_ENABLED
from models.sys_role import SysRole
from schemas.user import UserCreate, UserUpdate
from core.auth import hash_password, verify_password, create_token
from datetime import timedelta
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES


class AuthService:
    @staticmethod
    def login(db: Session, username: str, password: str) -> dict:
        user = db.query(SysUser).filter(SysUser.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        if user.status != USER_STATUS_ENABLED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户已被禁用"
            )
        
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_token(
            data={"user_id": user.id, "username": user.username, "role_id": user.role_id},
            expires_delta=access_token_expires
        )
        
        return {
            "token": token,
            "user_info": user
        }

    @staticmethod
    def get_user_info(db: Session, user_id: int) -> SysUser:
        user = db.query(SysUser).filter(SysUser.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        return user
