# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：core/database.py
# 模块用途：数据库配置模块，负责数据库连接、会话管理和基础模型类定义
# 说明：
#   - 使用SQLAlchemy作为ORM框架，提供数据库操作的抽象层
#   - 支持SQLite数据库，check_same_thread=False解决多线程访问问题
#   - 提供get_db依赖注入函数和init_db初始化函数
# ================================================================================

# 从SQLAlchemy导入数据库引擎创建函数
from sqlalchemy import create_engine
# 从SQLAlchemy扩展模块导入声明式基类工厂函数
from sqlalchemy.ext.declarative import declarative_base
# 从SQLAlchemy ORM模块导入会话工厂函数
from sqlalchemy.orm import sessionmaker

# 从配置模块导入数据库连接URL
from core.config import DATABASE_URL

# 创建数据库引擎
# engine是SQLAlchemy的核心组件，负责管理数据库连接池和SQL执行
# connect_args参数是SQLite特有的配置
# check_same_thread=False允许在不同线程中使用同一个连接
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 创建会话工厂
# SessionLocal是一个会话类，用于创建与数据库的交互会话
# autocommit=False：关闭自动提交，需要手动commit才能持久化变更
# autoflush=False：关闭自动刷新，避免不必要的数据库同步操作
# bind=engine：将会话绑定到指定的数据库引擎
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建声明式基类
# Base是所有ORM模型类的基类，提供了表映射、关系定义等ORM功能
# 所有数据模型都需要继承自这个Base类
Base = declarative_base()


def get_db():
    """
    数据库会话依赖注入函数
    用于FastAPI的Depends依赖注入，为每个请求创建一个独立的数据库会话
    使用生成器模式确保会话在请求结束后正确关闭

    返回值:
        Generator[Session, None, None]: 数据库会话生成器

    用法:
        @app.get("/")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    # 创建一个新的数据库会话
    db = SessionLocal()
    try:
        # yield将会话返回给调用方，暂停在此处等待调用完成
        yield db
    finally:
        # 无论请求成功还是失败，最终都会关闭数据库会话
        # 防止连接泄漏，保证资源正确释放
        db.close()


def init_db():
    """
    初始化数据库表结构
    根据已定义的ORM模型自动创建对应的数据库表
    注意：此函数需要在所有模型导入后调用，否则无法创建对应表

    功能说明：
        1. 导入所有模型类（确保模型已注册到Base.metadata）
        2. 调用create_all根据元数据创建所有不存在的表
        3. 已存在的表不会被修改或重建（不会影响现有数据）
    """
    # 导入所有模型，使它们注册到Base的元数据中
    # 这些导入是必要的，否则Base不知道有哪些表需要创建
    from models import sys_user, sys_role, sys_operate_log, invoice_main, invoice_item
    # 根据元数据创建所有表，如果表已存在则跳过
    # bind=engine指定使用哪个数据库连接执行创建操作
    Base.metadata.create_all(bind=engine)
