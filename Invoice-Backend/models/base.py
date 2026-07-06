# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：models/base.py
# 模块用途：基础模型，定义所有模型的公共字段
# ================================================================================

from sqlalchemy import Column, Integer, DateTime, func
from core.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="主键ID"
    )

    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
        comment="创建时间"
    )

    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="更新时间"
    )
