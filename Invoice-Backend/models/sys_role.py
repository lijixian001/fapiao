# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：models/sys_role.py
# 模块用途：角色数据模型，定义系统角色表结构
# 说明：
#   - 角色用于权限控制，不同角色拥有不同的操作权限
#   - 通过role_code唯一标识角色，便于程序中引用
#   - 与用户表是一对多关系（一个角色可以有多个用户）
# ================================================================================

# 从SQLAlchemy导入列和字符串类型
from sqlalchemy import Column, String
# 从基础模型导入BaseModel
from models.base import BaseModel


class SysRole(BaseModel):
    """
    系统角色模型类
    对应数据库表 sys_role，存储系统角色信息

    表关联:
        - 与 sys_user 表是一对多关系（通过 users 反向引用）
        - 一个角色可以被多个用户拥有

    字段说明:
        - id: 主键ID（继承自BaseModel）
        - role_code: 角色编码，唯一标识
        - role_name: 角色名称，用于展示
        - description: 角色描述信息
        - created_at: 创建时间（继承自BaseModel）
        - updated_at: 更新时间（继承自BaseModel）
    """
    # 指定对应的数据库表名
    __tablename__ = "sys_role"

    # 角色编码字段
    # 角色的唯一标识符，用于程序中判断角色类型
    # 例如：admin(超级管理员), user(普通用户)等
    # unique=True: 唯一约束，不允许重复
    # nullable=False: 必填字段
    role_code = Column(
        String(50),
        unique=True,
        nullable=False,
        comment="角色编码"
    )

    # 角色名称字段
    # 角色的显示名称，用于前端界面展示
    # 例如：超级管理员、普通用户、财务人员等
    role_name = Column(
        String(100),
        nullable=False,
        comment="角色名称"
    )

    # 角色描述字段
    # 存储角色的详细描述信息，说明角色的权限范围和用途
    # nullable=True: 可选字段，可以为空
    description = Column(
        String(500),
        nullable=True,
        comment="角色描述"
    )
