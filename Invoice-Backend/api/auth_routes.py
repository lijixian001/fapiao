"""
认证相关API路由模块

本模块提供用户认证相关的接口，包括登录、登出和获取当前用户信息。
所有接口都遵循统一的响应格式 ResponseModel。
"""

# 导入FastAPI框架相关组件：APIRouter用于创建路由，Depends用于依赖注入，
# HTTPException用于抛出HTTP异常，status提供HTTP状态码常量
from fastapi import APIRouter, Depends, HTTPException, status
# 导入SQLAlchemy的Session类，用于数据库会话管理
from sqlalchemy.orm import Session

# 导入数据库会话获取函数，用于依赖注入获取数据库连接
from core.database import get_db
# 导入当前用户获取函数，用于依赖注入获取当前登录用户信息
from core.auth import get_current_user
# 导入用户相关的Pydantic数据模型：登录请求模型、登录响应模型、用户响应模型
from schemas.user import UserLogin, LoginResponse, UserResponse
# 导入通用响应模型，用于统一API响应格式
from schemas.common import ResponseModel
# 导入认证服务类，封装了认证相关的业务逻辑
from services.auth_service import AuthService

# 创建认证路由实例，前缀为/api/auth，在API文档中归类为"认证"标签
router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login", response_model=ResponseModel[LoginResponse])
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录接口

    接收用户的用户名和密码，验证通过后返回访问令牌和用户信息。

    请求方式: POST
    请求路径: /api/auth/login

    参数:
        user_data (UserLogin): 登录请求体，包含用户名和密码
            - username: 用户名
            - password: 密码
        db (Session): 数据库会话，通过依赖注入自动获取

    返回值:
        ResponseModel[LoginResponse]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 登录响应数据
                - token: 访问令牌
                - user: 用户信息

    权限要求: 无需登录（公开接口）
    """
    # 调用认证服务的登录方法，验证用户名和密码并生成令牌
    result = AuthService.login(db, user_data.username, user_data.password)
    # 返回统一格式的成功响应
    return ResponseModel(data=result, message="登录成功")


@router.post("/logout", response_model=ResponseModel)
def logout(current_user: dict = Depends(get_current_user)):
    """
    用户登出接口

    用户退出登录，使当前访问令牌失效。

    请求方式: POST
    请求路径: /api/auth/logout

    参数:
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取
            - user_id: 用户ID
            - 其他用户相关信息

    返回值:
        ResponseModel: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 返回登出成功响应（实际令牌失效逻辑可在服务层或中间件处理）
    return ResponseModel(message="登出成功")


@router.get("/userinfo", response_model=ResponseModel[UserResponse])
def get_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户信息接口

    根据当前登录用户的令牌，返回用户的详细信息。

    请求方式: GET
    请求路径: /api/auth/userinfo

    参数:
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取
            - user_id: 用户ID
        db (Session): 数据库会话，通过依赖注入自动获取

    返回值:
        ResponseModel[UserResponse]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 用户详细信息

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用认证服务获取用户详细信息
    user = AuthService.get_user_info(db, current_user["user_id"])
    # 返回统一格式的成功响应，包含用户信息
    return ResponseModel(data=user)
