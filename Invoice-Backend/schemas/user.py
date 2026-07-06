from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserCreate(BaseModel):
    username: str = Field(..., description="用户名", min_length=3, max_length=50)
    password: str = Field(..., description="密码", min_length=6)
    real_name: str = Field(..., description="真实姓名")
    role_id: Optional[int] = Field(default=None, description="角色ID")
    email: Optional[str] = Field(default=None, description="邮箱")
    phone: Optional[str] = Field(default=None, description="手机号")


class UserUpdate(BaseModel):
    real_name: Optional[str] = Field(default=None, description="真实姓名")
    role_id: Optional[int] = Field(default=None, description="角色ID")
    email: Optional[str] = Field(default=None, description="邮箱")
    phone: Optional[str] = Field(default=None, description="手机号")
    status: Optional[int] = Field(default=None, description="状态")


class UserResponse(BaseModel):
    id: int
    username: str
    real_name: str
    role_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    token: str
    user_info: UserResponse
