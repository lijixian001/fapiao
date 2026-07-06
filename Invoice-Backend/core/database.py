# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：core/database.py
# 模块用途：数据库配置模块，创建数据库连接、会话和基类
# ================================================================================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from models import sys_user, sys_role, sys_operate_log, invoice_main, invoice_item
    Base.metadata.create_all(bind=engine)
