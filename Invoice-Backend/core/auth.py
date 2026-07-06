# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：core/auth.py
# 模块用途：认证模块，提供JWT令牌生成与验证、密码哈希、当前用户获取等认证相关功能
# 说明：
#   - 使用python-jose库处理JWT令牌的创建和验证
#   - 使用bcrypt算法进行密码哈希和验证，确保密码安全存储
#   - 提供get_current_user依赖函数，用于FastAPI路由的权限校验
# ================================================================================

# 导入datetime和timedelta用于处理令牌过期时间
from datetime import datetime, timedelta
# 导入Optional类型提示，表示可选参数
from typing import Optional

# 从python-jose库导入JWT异常类和JWT核心功能
from jose import JWTError, jwt
# 从FastAPI导入依赖注入、HTTP异常和状态码常量
from fastapi import Depends, HTTPException, status
# 从FastAPI安全模块导入Bearer认证方案和凭证类
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# 从SQLAlchemy ORM导入会话类型
from sqlalchemy.orm import Session
# 导入bcrypt库用于密码哈希和验证
import bcrypt

# 从配置模块导入JWT相关配置
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
# 从数据库模块导入数据库会话依赖
from core.database import get_db
# 从用户模型导入SysUser类
from models.sys_user import SysUser

# 创建HTTP Bearer认证方案实例
# security是FastAPI的安全依赖，用于从请求头中提取Bearer token
# 它会自动检查Authorization头的格式是否为 "Bearer <token>"
security = HTTPBearer()


def hash_password(password: str) -> str:
    """
    密码哈希函数
    使用bcrypt算法对明文密码进行哈希处理，生成安全的密码哈希值
    bcrypt是一种自适应哈希算法，包含随机盐值，能有效抵御彩虹表攻击

    参数:
        password (str): 用户输入的明文密码

    返回值:
        str: 经过bcrypt哈希后的密码字符串

    特点:
        - 每次哈希都会生成不同的盐值，相同密码也会得到不同的哈希值
        - 计算成本可调整，随着硬件性能提升可增加计算强度
    """
    # 生成随机盐值，默认使用12轮计算
    salt = bcrypt.gensalt()
    # 使用盐值对密码进行哈希处理，并将结果从bytes转换为str
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    密码验证函数
    将明文密码与存储的哈希密码进行比对，验证密码是否正确

    参数:
        plain_password (str): 用户输入的明文密码
        hashed_password (str): 数据库中存储的哈希密码

    返回值:
        bool: 密码验证结果，True表示验证通过，False表示验证失败

    原理:
        bcrypt会从哈希值中提取盐值，用相同的盐值哈希明文密码，
        然后将结果与存储的哈希值进行恒定时间比较，防止时序攻击
    """
    # 将明文密码和哈希密码都转换为bytes进行比对
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT访问令牌
    根据传入的数据和过期时间生成JWT令牌字符串

    参数:
        data (dict): 需要编码到令牌中的数据，通常包含用户ID、用户名、角色等
        expires_delta (Optional[timedelta]): 令牌有效期，可选参数
            如果为None，则使用配置文件中的默认过期时间

    返回值:
        str: 生成的JWT令牌字符串

    JWT结构:
        - Header: 包含令牌类型和签名算法
        - Payload: 包含用户数据和过期时间等声明
        - Signature: 使用密钥对前两部分签名，防止篡改
    """
    # 复制输入数据，避免修改原始字典
    to_encode = data.copy()
    # 计算令牌过期时间
    if expires_delta:
        # 如果指定了过期时间差，则从当前时间加上该时间段
        expire = datetime.utcnow() + expires_delta
    else:
        # 否则使用配置中的默认过期时间（分钟）
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 将过期时间添加到要编码的数据中
    # "exp"是JWT标准声明，表示过期时间
    to_encode.update({"exp": expire})
    # 使用密钥和算法对数据进行编码，生成JWT令牌
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> dict:
    """
    获取当前登录用户信息（依赖注入函数）
    从请求头中提取并验证JWT令牌，解析出用户信息
    作为FastAPI的依赖注入，用于需要登录才能访问的路由

    参数:
        credentials (HTTPAuthorizationCredentials): 从Authorization头解析出的Bearer凭证
            由security依赖自动注入，包含token字符串
        db (Session): 数据库会话，由get_db依赖注入

    返回值:
        dict: 当前用户信息字典，包含user_id、username、role_id

    异常:
        HTTPException: 认证失败时抛出401未授权异常

    使用方式:
        @app.get("/protected")
        def protected_route(current_user: dict = Depends(get_current_user)):
            return {"user": current_user}
    """
    # 定义认证异常，用于令牌无效或过期时返回
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 从凭证对象中提取token字符串
        token = credentials.credentials
        # 解码JWT令牌，验证签名和过期时间
        # SECRET_KEY用于验证签名，ALGORITHM指定允许的算法
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 从令牌负载中提取用户ID
        user_id: int = payload.get("user_id")
        # 从令牌负载中提取用户名
        username: str = payload.get("username")
        # 从令牌负载中提取角色ID
        role_id: int = payload.get("role_id")
        # 检查用户ID是否存在，如果不存在则认证失败
        if user_id is None:
            raise credentials_exception
        # 返回用户信息字典
        return {
            "user_id": user_id,
            "username": username,
            "role_id": role_id,
        }
    except JWTError:
        # 捕获所有JWT相关异常（签名错误、令牌过期、格式错误等）
        # 抛出认证失败异常
        raise credentials_exception
