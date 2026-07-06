# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：models/sys_role.py
# 模块用途：角色模型
# ================================================================================

from sqlalchemy import Column, String
from models.base import BaseModel


class SysRole(BaseModel):
    __tablename__ = "sys_role"

    role_code = Column(
        String(50),
        unique=True,
        nullable=False,
        comment="角色编码"
    )

    role_name = Column(
        String(100),
        nullable=False,
        comment="角色名称"
    )

    description = Column(
        String(500),
        nullable=True,
        comment="角色描述"
    )
