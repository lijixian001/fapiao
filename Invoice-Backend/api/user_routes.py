"""
用户管理相关API路由模块

本模块提供用户管理相关的接口，包括用户列表查询、用户详情获取、
用户创建、用户更新和用户删除等功能。所有接口都需要登录认证。
"""

# 导入FastAPI框架相关组件：APIRouter用于创建路由，Depends用于依赖注入，
# Query用于查询参数解析和验证
from fastapi import APIRouter, Depends, Query
# 导入SQLAlchemy的Session类，用于数据库会话管理
from sqlalchemy.orm import Session
# 导入typing模块的Optional类型，用于表示可选参数
from typing import Optional

# 导入数据库会话获取函数，用于依赖注入获取数据库连接
from core.database import get_db
# 导入当前用户获取函数，用于依赖注入获取当前登录用户信息
from core.auth import get_current_user
# 导入用户相关的Pydantic数据模型：创建模型、更新模型、响应模型
from schemas.user import UserCreate, UserUpdate, UserResponse
# 导入通用响应模型，包括统一响应格式和分页响应格式
from schemas.common import ResponseModel, PageResponse
# 导入用户服务类，封装了用户管理相关的业务逻辑
from services.user_service import UserService

# 创建用户管理路由实例，前缀为/api/user，在API文档中归类为"用户管理"标签
router = APIRouter(prefix="/api/user", tags=["用户管理"])


@router.get("", response_model=ResponseModel[PageResponse[UserResponse]])
def list_users(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取用户列表接口

    分页查询用户列表，支持按关键词搜索。

    请求方式: GET
    请求路径: /api/user

    参数:
        page (int): 页码，默认为1
        page_size (int): 每页数量，默认为10
        keyword (Optional[str]): 搜索关键词，可选，用于模糊匹配用户名等
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取

    返回值:
        ResponseModel[PageResponse[UserResponse]]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 分页数据
                - total: 总记录数
                - page: 当前页码
                - page_size: 每页数量
                - items: 用户列表

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用用户服务获取分页用户列表
    result = UserService.list_users(db, page=page, page_size=page_size, keyword=keyword)
    # 返回统一格式的成功响应
    return ResponseModel(data=result)


@router.get("/{user_id}", response_model=ResponseModel[UserResponse])
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取用户详情接口

    根据用户ID获取用户的详细信息。

    请求方式: GET
    请求路径: /api/user/{user_id}

    参数:
        user_id (int): 用户ID，路径参数
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取

    返回值:
        ResponseModel[UserResponse]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 用户详细信息（用户不存在时为None）

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用用户服务根据ID获取用户信息
    user = UserService.get_user_by_id(db, user_id)
    # 判断用户是否存在，不存在则返回404错误
    if not user:
        return ResponseModel(code=404, message="用户不存在", data=None)
    # 用户存在，返回用户信息
    return ResponseModel(data=user)


@router.post("", response_model=ResponseModel[UserResponse])
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    创建用户接口

    创建一个新的用户账户。

    请求方式: POST
    请求路径: /api/user

    参数:
        user_data (UserCreate): 用户创建请求体，包含用户信息
            - username: 用户名
            - password: 密码
            - 其他用户属性
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取
            - user_id: 创建人用户ID

    返回值:
        ResponseModel[UserResponse]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 新创建的用户信息

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用用户服务创建新用户，传入当前用户ID作为创建人
    user = UserService.create_user(db, user_data, created_by=current_user["user_id"])
    # 返回创建成功的响应
    return ResponseModel(data=user, message="创建成功")


@router.put("/{user_id}", response_model=ResponseModel[UserResponse])
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    更新用户信息接口

    根据用户ID更新用户的信息。

    请求方式: PUT
    请求路径: /api/user/{user_id}

    参数:
        user_id (int): 用户ID，路径参数
        user_data (UserUpdate): 用户更新请求体，包含要更新的字段
            - 可选的用户属性字段
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取

    返回值:
        ResponseModel[UserResponse]: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息
            - data: 更新后的用户信息

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用用户服务更新用户信息
    user = UserService.update_user(db, user_id, user_data)
    # 返回更新成功的响应
    return ResponseModel(data=user, message="更新成功")


@router.delete("/{user_id}", response_model=ResponseModel)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    删除用户接口

    根据用户ID删除指定用户。

    请求方式: DELETE
    请求路径: /api/user/{user_id}

    参数:
        user_id (int): 用户ID，路径参数
        db (Session): 数据库会话，通过依赖注入自动获取
        current_user (dict): 当前登录用户信息，通过依赖注入自动获取

    返回值:
        ResponseModel: 统一响应格式，包含：
            - code: 响应状态码
            - message: 响应消息

    权限要求: 需要登录（需在请求头中携带有效令牌）
    """
    # 调用用户服务删除用户
    UserService.delete_user(db, user_id)
    # 返回删除成功的响应
    return ResponseModel(message="删除成功")
