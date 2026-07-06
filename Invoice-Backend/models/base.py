# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：models/base.py
# 模块用途：基础模型类，定义所有数据模型的公共字段和行为
# 说明：
#   - 所有业务模型都继承自BaseModel，实现代码复用
#   - 包含主键ID、创建时间、更新时间等通用字段
#   - 继承自database中的Base，是SQLAlchemy的声明式基类
# ================================================================================

# 从SQLAlchemy导入列、整数、日期时间和函数模块
from sqlalchemy import Column, Integer, DateTime, func
# 从数据库模块导入声明式基类Base
from core.database import Base


class BaseModel(Base):
    """
    基础模型抽象类
    所有业务数据模型的基类，提供统一的通用字段定义

    包含的通用字段:
        - id: 主键ID，自增整数
        - created_at: 创建时间，默认为当前时间
        - updated_at: 更新时间，创建时为当前时间，更新时自动更新

    注意:
        - __abstract__ = True 表示这是一个抽象基类，不会创建对应的数据库表
        - 所有继承的子类会自动获得这些字段
    """
    # 标记为抽象基类，SQLAlchemy不会为其创建数据库表
    __abstract__ = True

    # 主键ID字段
    # Integer: 整数类型
    # primary_key=True: 主键约束
    # autoincrement=True: 自动递增
    # nullable=False: 不允许为空
    # comment: 字段注释说明
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="主键ID"
    )

    # 记录创建时间字段
    # DateTime: 日期时间类型
    # default=func.now(): 默认值为数据库服务器当前时间
    # func.now()是SQLAlchemy的跨平台当前时间函数
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
        comment="创建时间"
    )

    # 记录更新时间字段
    # onupdate=func.now(): 记录更新时自动更新为当前时间
    # 每次修改记录时该字段会自动刷新
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="更新时间"
    )
