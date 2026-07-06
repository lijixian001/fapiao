"""
认证服务模块

本模块提供用户认证相关的业务逻辑处理，包括用户登录验证和获取用户信息等功能。
主要负责用户身份认证、密码校验、Token生成等核心认证流程。
"""

# SQLAlchemy 数据库会话对象，用于数据库操作
from sqlalchemy.orm import Session
# FastAPI HTTP异常类和状态码常量，用于返回标准化的HTTP错误响应
from fastapi import HTTPException, status

# 系统用户模型及启用状态常量
from models.sys_user import SysUser, USER_STATUS_ENABLED
# 系统角色模型
from models.sys_role import SysRole
# 用户创建和更新的数据验证模式
from schemas.user import UserCreate, UserUpdate
# 认证核心工具：密码哈希、密码验证、Token生成
from core.auth import hash_password, verify_password, create_token
# 时间间隔类，用于设置Token过期时间
from datetime import timedelta
# 访问令牌过期时间配置（分钟）
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES


class AuthService:
    """
    认证服务类

    提供用户认证相关的静态方法，封装了登录验证和用户信息查询等业务逻辑。
    所有方法均为静态方法，可直接通过类名调用，无需实例化。
    """

    @staticmethod
    def login(db: Session, username: str, password: str) -> dict:
        """
        用户登录验证

        根据用户名和密码进行身份验证，验证成功后生成访问令牌并返回用户信息。

        参数:
            db (Session): 数据库会话对象，用于执行数据库查询操作
            username (str): 用户登录名
            password (str): 用户登录密码（明文）

        返回:
            dict: 登录成功后返回包含以下字段的字典：
                - token (str): 生成的JWT访问令牌
                - user_info (SysUser): 用户信息对象

        异常:
            HTTPException: 
                - 401 Unauthorized: 用户名不存在或密码错误
                - 401 Unauthorized: 用户账号已被禁用

        业务逻辑说明:
            1. 根据用户名查询数据库中的用户记录
            2. 校验用户是否存在，不存在则抛出异常
            3. 校验用户状态是否为启用状态，禁用则抛出异常
            4. 验证密码是否正确，错误则抛出异常
            5. 计算Token过期时间，生成JWT访问令牌
            6. 返回Token和用户信息
        """
        # 根据用户名查询用户记录
        user = db.query(SysUser).filter(SysUser.username == username).first()
        # 用户不存在，抛出401未授权异常
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        # 校验用户状态，非启用状态则抛出401未授权异常
        if user.status != USER_STATUS_ENABLED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户已被禁用"
            )
        
        # 验证密码是否匹配，不匹配则抛出401未授权异常
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        # 计算访问令牌的过期时间间隔
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # 生成JWT访问令牌，包含用户ID、用户名和角色ID信息
        token = create_token(
            data={"user_id": user.id, "username": user.username, "role_id": user.role_id},
            expires_delta=access_token_expires
        )
        
        # 返回访问令牌和用户信息
        return {
            "token": token,
            "user_info": user
        }

    @staticmethod
    def get_user_info(db: Session, user_id: int) -> SysUser:
        """
        获取用户详细信息

        根据用户ID查询用户的详细信息。

        参数:
            db (Session): 数据库会话对象，用于执行数据库查询操作
            user_id (int): 用户唯一标识ID

        返回:
            SysUser: 用户信息对象

        异常:
            HTTPException: 
                - 404 Not Found: 用户不存在

        业务逻辑说明:
            1. 根据用户ID查询数据库中的用户记录
            2. 校验用户是否存在，不存在则抛出404异常
            3. 返回用户信息对象
        """
        # 根据用户ID查询用户记录
        user = db.query(SysUser).filter(SysUser.id == user_id).first()
        # 用户不存在，抛出404资源未找到异常
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        # 返回用户信息
        return user
