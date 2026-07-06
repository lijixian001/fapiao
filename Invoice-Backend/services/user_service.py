"""
用户服务模块

本模块提供系统用户管理相关的业务逻辑处理，包括用户的增删改查、
用户信息查询、用户列表分页等核心用户管理功能。
"""

# SQLAlchemy 数据库会话对象，用于数据库操作
from sqlalchemy.orm import Session
# FastAPI HTTP异常类和状态码常量，用于返回标准化的HTTP错误响应
from fastapi import HTTPException, status
# 可选类型注解，用于标识参数或返回值可以为None
from typing import Optional

# 系统用户模型
from models.sys_user import SysUser
# 用户创建和更新的数据验证模式
from schemas.user import UserCreate, UserUpdate
# 认证核心工具：密码哈希函数
from core.auth import hash_password


class UserService:
    """
    用户服务类

    提供系统用户管理相关的静态方法，封装了用户的增删改查等业务逻辑。
    所有方法均为静态方法，可直接通过类名调用，无需实例化。
    """

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[SysUser]:
        """
        根据用户ID查询用户信息

        参数:
            db (Session): 数据库会话对象，用于执行数据库查询操作
            user_id (int): 用户唯一标识ID

        返回:
            Optional[SysUser]: 用户信息对象，若不存在则返回None
        """
        # 根据用户ID查询用户记录，返回第一条匹配结果或None
        return db.query(SysUser).filter(SysUser.id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[SysUser]:
        """
        根据用户名查询用户信息

        参数:
            db (Session): 数据库会话对象，用于执行数据库查询操作
            username (str): 用户登录名

        返回:
            Optional[SysUser]: 用户信息对象，若不存在则返回None
        """
        # 根据用户名查询用户记录，返回第一条匹配结果或None
        return db.query(SysUser).filter(SysUser.username == username).first()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate, created_by: int = None) -> SysUser:
        """
        创建新用户

        在数据库中创建一条新的用户记录，包含用户名、密码、真实姓名等信息。

        参数:
            db (Session): 数据库会话对象，用于执行数据库操作
            user_data (UserCreate): 用户创建数据，包含用户名、密码、真实姓名等字段
            created_by (int, optional): 创建该用户的操作人ID，默认为None

        返回:
            SysUser: 创建成功后的用户信息对象

        异常:
            HTTPException: 
                - 400 Bad Request: 用户名已存在

        业务逻辑说明:
            1. 检查用户名是否已存在，存在则抛出异常
            2. 对用户密码进行哈希加密处理
            3. 创建用户实体对象并设置各项属性
            4. 将用户对象添加到数据库会话
            5. 提交事务到数据库
            6. 刷新用户对象以获取数据库生成的字段（如ID、创建时间等）
            7. 返回用户信息
        """
        # 检查用户名是否已存在
        existing_user = UserService.get_user_by_username(db, user_data.username)
        # 用户名已存在，抛出400请求错误异常
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 对密码进行哈希加密处理
        hashed_password = hash_password(user_data.password)
        # 创建用户实体对象，设置各项用户属性
        db_user = SysUser(
            username=user_data.username,
            password=hashed_password,
            real_name=user_data.real_name,
            role_id=user_data.role_id,
            email=user_data.email,
            phone=user_data.phone,
            created_by=created_by
        )
        # 将用户对象添加到数据库会话
        db.add(db_user)
        # 提交事务，将数据持久化到数据库
        db.commit()
        # 刷新用户对象，获取数据库自动生成的字段值
        db.refresh(db_user)
        # 返回创建成功的用户信息
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> SysUser:
        """
        更新用户信息

        根据用户ID更新用户的相关信息，支持部分字段更新。

        参数:
            db (Session): 数据库会话对象，用于执行数据库操作
            user_id (int): 用户唯一标识ID
            user_data (UserUpdate): 用户更新数据，仅包含需要更新的字段

        返回:
            SysUser: 更新成功后的用户信息对象

        异常:
            HTTPException: 
                - 404 Not Found: 用户不存在

        业务逻辑说明:
            1. 根据用户ID查询用户记录
            2. 校验用户是否存在，不存在则抛出404异常
            3. 提取用户数据中已设置的字段（排除未设置的字段）
            4. 遍历更新数据，动态设置用户对象的属性
            5. 提交事务到数据库
            6. 刷新用户对象以获取最新数据
            7. 返回更新后的用户信息
        """
        # 根据用户ID查询用户记录
        user = UserService.get_user_by_id(db, user_id)
        # 用户不存在，抛出404资源未找到异常
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 提取用户数据中已显式设置的字段（排除未设置的字段，实现部分更新）
        update_data = user_data.model_dump(exclude_unset=True)
        # 遍历更新数据，使用setattr动态设置用户对象的属性
        for key, value in update_data.items():
            setattr(user, key, value)
        
        # 提交事务，将更新后的数据持久化到数据库
        db.commit()
        # 刷新用户对象，获取数据库中的最新数据
        db.refresh(user)
        # 返回更新后的用户信息
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        删除用户

        根据用户ID删除指定的用户记录。

        参数:
            db (Session): 数据库会话对象，用于执行数据库操作
            user_id (int): 用户唯一标识ID

        返回:
            bool: 删除成功返回True

        异常:
            HTTPException: 
                - 404 Not Found: 用户不存在

        业务逻辑说明:
            1. 根据用户ID查询用户记录
            2. 校验用户是否存在，不存在则抛出404异常
            3. 从数据库中删除该用户记录
            4. 提交事务
            5. 返回删除成功标识
        """
        # 根据用户ID查询用户记录
        user = UserService.get_user_by_id(db, user_id)
        # 用户不存在，抛出404资源未找到异常
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 从数据库会话中删除用户对象
        db.delete(user)
        # 提交事务，执行删除操作
        db.commit()
        # 返回删除成功
        return True

    @staticmethod
    def list_users(
        db: Session,
        page: int = 1,
        page_size: int = 10,
        keyword: Optional[str] = None
    ) -> dict:
        """
        分页查询用户列表

        支持按关键字模糊搜索用户，支持分页功能。

        参数:
            db (Session): 数据库会话对象，用于执行数据库查询操作
            page (int, optional): 页码，默认为1
            page_size (int, optional): 每页数据条数，默认为10
            keyword (Optional[str], optional): 搜索关键字，支持用户名和真实姓名模糊匹配，默认为None

        返回:
            dict: 分页查询结果，包含以下字段：
                - total (int): 总记录数
                - page (int): 当前页码
                - page_size (int): 每页数据条数
                - list (List[SysUser]): 用户数据列表

        业务逻辑说明:
            1. 构建用户查询对象
            2. 若有关键字，则添加用户名和真实姓名的模糊搜索条件（OR关系）
            3. 查询符合条件的总记录数
            4. 计算分页偏移量，查询当前页的用户数据
            5. 返回分页结果字典
        """
        # 构建用户查询对象
        query = db.query(SysUser)
        
        # 若有关键字，则添加模糊搜索条件（用户名或真实姓名匹配）
        if keyword:
            query = query.filter(
                (SysUser.username.like(f"%{keyword}%")) |
                (SysUser.real_name.like(f"%{keyword}%"))
            )
        
        # 查询符合条件的总记录数
        total = query.count()
        # 计算分页偏移量，查询当前页的用户数据列表
        users = query.offset((page - 1) * page_size).limit(page_size).all()
        
        # 返回分页结果字典
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "list": users
        }
