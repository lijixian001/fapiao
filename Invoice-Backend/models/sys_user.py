# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：models/sys_user.py
# 模块用途：用户数据模型，定义系统用户表结构
# 说明：
#   - 存储系统用户的基本信息、登录凭证和状态
#   - 通过role_id与角色表关联，实现基于角色的权限控制
#   - 密码使用bcrypt哈希存储，确保安全
# ================================================================================

# 从SQLAlchemy导入列、字符串、整数和外键类型
from sqlalchemy import Column, String, Integer, ForeignKey
# 从SQLAlchemy ORM导入关系映射
from sqlalchemy.orm import relationship
# 从基础模型导入BaseModel
from models.base import BaseModel

# 用户状态常量定义
# 使用常量提高代码可读性，避免魔法数字
# 启用状态：用户可以正常登录和使用系统
USER_STATUS_ENABLED = 1
# 禁用状态：用户无法登录系统
USER_STATUS_DISABLED = 0


class SysUser(BaseModel):
    """
    系统用户模型类
    对应数据库表 sys_user，存储系统用户信息

    表关联:
        - 与 sys_role 表是多对一关系（通过 role_id 外键）
        - 通过 role 属性访问关联的角色对象
        - 一个角色可以有多个用户

    字段说明:
        - id: 主键ID（继承自BaseModel）
        - username: 用户名，唯一登录标识
        - password: 密码哈希值
        - real_name: 真实姓名
        - role_id: 角色ID，外键关联sys_role表
        - email: 邮箱地址
        - phone: 手机号码
        - status: 用户状态（1=启用，0=禁用）
        - created_by: 创建人ID
        - created_at: 创建时间（继承自BaseModel）
        - updated_at: 更新时间（继承自BaseModel）
    """
    # 指定对应的数据库表名
    __tablename__ = "sys_user"

    # 用户名字段
    # 用户登录使用的账号，必须唯一
    # 长度限制50个字符
    username = Column(
        String(50),
        unique=True,
        nullable=False,
        comment="用户名"
    )

    # 密码字段
    # 存储的是bcrypt哈希后的密码，不是明文
    # 长度255以容纳足够长的哈希值
    password = Column(
        String(255),
        nullable=False,
        comment="密码"
    )

    # 真实姓名字段
    # 用户的真实姓名，用于显示和记录
    real_name = Column(
        String(100),
        nullable=False,
        comment="真实姓名"
    )

    # 角色ID字段
    # 外键关联到sys_role表的id字段
    # 用于确定用户的角色和权限
    # nullable=True表示可以没有角色
    role_id = Column(
        Integer,
        ForeignKey("sys_role.id"),
        nullable=True,
        comment="角色ID"
    )

    # 邮箱字段
    # 用户的电子邮箱地址，可用于找回密码、通知等
    email = Column(
        String(100),
        nullable=True,
        comment="邮箱"
    )

    # 手机号字段
    # 用户的手机号码，可用于验证、通知等
    phone = Column(
        String(20),
        nullable=True,
        comment="手机号"
    )

    # 用户状态字段
    # 1表示启用状态，可以正常登录
    # 0表示禁用状态，无法登录
    # 默认值为启用状态
    status = Column(
        Integer,
        default=USER_STATUS_ENABLED,
        nullable=False,
        comment="状态：1=启用，0=禁用"
    )

    # 创建人ID字段
    # 记录是谁创建了这个用户账号
    # 用于审计追踪
    created_by = Column(
        Integer,
        nullable=True,
        comment="创建人ID"
    )

    # 角色关系属性
    # 通过role_id外键关联到SysRole对象
    # backref="users"表示在SysRole侧会自动创建users属性，
    # 可以通过 role.users 访问该角色下的所有用户
    role = relationship("SysRole", backref="users")
