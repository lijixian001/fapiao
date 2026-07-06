"""
项目名称：Invoice-Backend（发票管理系统后端）
模块名称：user.py
模块用途：定义用户相关的Pydantic数据模型（Schema）
模块说明：本文件包含用户登录、用户创建、用户更新、用户响应和登录响应等数据模型，
         用于API请求参数验证和响应数据格式化。
"""

# 导入Optional类型，用于声明可选字段
from typing import Optional
# 导入datetime类型，用于处理日期时间字段
from datetime import datetime
# 导入Pydantic的BaseModel基类和Field字段验证器
# BaseModel：所有Pydantic模型的基类，提供数据验证、序列化等功能
# Field：用于定义字段的额外验证规则和描述信息
from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    """
    用户登录数据模型

    用途：用于用户登录接口的请求参数验证
    字段说明：
        - username: 用户名（必填）
        - password: 密码（必填）
    使用场景：用户登录时，前端提交的登录表单数据通过此模型进行验证
    """
    username: str = Field(..., description="用户名")  # 用户名，必填字段，字符串类型
    password: str = Field(..., description="密码")    # 密码，必填字段，字符串类型


class UserCreate(BaseModel):
    """
    用户创建数据模型

    用途：用于创建新用户时的请求参数验证
    字段说明：
        - username: 用户名（必填，长度3-50个字符）
        - password: 密码（必填，最少6个字符）
        - real_name: 真实姓名（必填）
        - role_id: 角色ID（可选）
        - email: 邮箱（可选）
        - phone: 手机号（可选）
    使用场景：管理员创建新用户时，通过此模型验证提交的用户信息
    """
    username: str = Field(..., description="用户名", min_length=3, max_length=50)  # 用户名，必填，长度限制3-50个字符
    password: str = Field(..., description="密码", min_length=6)                   # 密码，必填，最少6个字符
    real_name: str = Field(..., description="真实姓名")                             # 真实姓名，必填字段
    role_id: Optional[int] = Field(default=None, description="角色ID")             # 角色ID，可选，默认为None
    email: Optional[str] = Field(default=None, description="邮箱")                 # 邮箱地址，可选，默认为None
    phone: Optional[str] = Field(default=None, description="手机号")               # 手机号码，可选，默认为None


class UserUpdate(BaseModel):
    """
    用户更新数据模型

    用途：用于更新用户信息时的请求参数验证
    字段说明：
        - real_name: 真实姓名（可选）
        - role_id: 角色ID（可选）
        - email: 邮箱（可选）
        - phone: 手机号（可选）
        - status: 状态（可选）
    使用场景：管理员或用户更新个人信息时，通过此模型验证需要更新的字段
    说明：所有字段均为可选，只更新传入的字段值
    """
    real_name: Optional[str] = Field(default=None, description="真实姓名")  # 真实姓名，可选
    role_id: Optional[int] = Field(default=None, description="角色ID")     # 角色ID，可选
    email: Optional[str] = Field(default=None, description="邮箱")         # 邮箱地址，可选
    phone: Optional[str] = Field(default=None, description="手机号")       # 手机号码，可选
    status: Optional[int] = Field(default=None, description="状态")        # 用户状态，可选（如：1=启用，0=禁用）


class UserResponse(BaseModel):
    """
    用户响应数据模型

    用途：用于用户信息查询接口的响应数据格式化
    字段说明：
        - id: 用户ID
        - username: 用户名
        - real_name: 真实姓名
        - role_id: 角色ID（可选）
        - email: 邮箱（可选）
        - phone: 手机号（可选）
        - status: 状态
        - created_at: 创建时间
        - updated_at: 更新时间
    使用场景：返回用户信息给前端时，通过此模型进行数据序列化
    说明：from_attributes = True 表示可以从ORM对象（如SQLAlchemy模型）直接转换
    """
    id: int                    # 用户唯一标识ID
    username: str              # 用户名
    real_name: str             # 真实姓名
    role_id: Optional[int] = None  # 角色ID，可选，默认为None
    email: Optional[str] = None    # 邮箱地址，可选，默认为None
    phone: Optional[str] = None    # 手机号码，可选，默认为None
    status: int                # 用户状态（如：1=启用，0=禁用）
    created_at: datetime       # 用户创建时间
    updated_at: datetime       # 用户信息最后更新时间

    class Config:
        """Pydantic模型配置类"""
        # 启用ORM模式，允许从ORM对象（如SQLAlchemy模型实例）直接创建Pydantic模型
        from_attributes = True


class LoginResponse(BaseModel):
    """
    登录响应数据模型

    用途：用于用户登录成功后的响应数据格式化
    字段说明：
        - token: 访问令牌（JWT Token）
        - user_info: 用户详细信息
    使用场景：用户登录成功后，返回访问令牌和用户信息给前端
    """
    token: str                 # 访问令牌（JWT Token），用于后续接口的身份验证
    user_info: UserResponse    # 用户详细信息，包含用户的基本信息
