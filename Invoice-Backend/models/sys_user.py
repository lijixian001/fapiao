# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：models/sys_user.py
# 模块用途：用户模型
# ================================================================================

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel

USER_STATUS_ENABLED = 1
USER_STATUS_DISABLED = 0


class SysUser(BaseModel):
    __tablename__ = "sys_user"

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        comment="用户名"
    )

    password = Column(
        String(255),
        nullable=False,
        comment="密码"
    )

    real_name = Column(
        String(100),
        nullable=False,
        comment="真实姓名"
    )

    role_id = Column(
        Integer,
        ForeignKey("sys_role.id"),
        nullable=True,
        comment="角色ID"
    )

    email = Column(
        String(100),
        nullable=True,
        comment="邮箱"
    )

    phone = Column(
        String(20),
        nullable=True,
        comment="手机号"
    )

    status = Column(
        Integer,
        default=USER_STATUS_ENABLED,
        nullable=False,
        comment="状态：1=启用，0=禁用"
    )

    created_by = Column(
        Integer,
        nullable=True,
        comment="创建人ID"
    )

    role = relationship("SysRole", backref="users")
