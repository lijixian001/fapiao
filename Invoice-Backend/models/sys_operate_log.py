# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：models/sys_operate_log.py
# 模块用途：操作日志模型
# ================================================================================

from sqlalchemy import Column, String, Integer, Text
from models.base import BaseModel


class SysOperateLog(BaseModel):
    __tablename__ = "sys_operate_log"

    user_id = Column(
        Integer,
        nullable=True,
        comment="操作用户ID"
    )

    username = Column(
        String(50),
        nullable=True,
        comment="操作用户名"
    )

    operation = Column(
        String(100),
        nullable=False,
        comment="操作类型"
    )

    method = Column(
        String(20),
        nullable=True,
        comment="请求方法"
    )

    url = Column(
        String(500),
        nullable=True,
        comment="请求URL"
    )

    ip = Column(
        String(50),
        nullable=True,
        comment="IP地址"
    )

    params = Column(
        Text,
        nullable=True,
        comment="请求参数"
    )

    result = Column(
        Text,
        nullable=True,
        comment="返回结果"
    )

    status = Column(
        Integer,
        default=1,
        nullable=False,
        comment="状态：1=成功，0=失败"
    )

    error_msg = Column(
        Text,
        nullable=True,
        comment="错误信息"
    )
