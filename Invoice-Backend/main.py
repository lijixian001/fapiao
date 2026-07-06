import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import APP_NAME, APP_VERSION, DEBUG
from core.database import init_db, engine, SessionLocal
from models.sys_user import SysUser
from models.sys_role import SysRole
from core.auth import hash_password


def create_app() -> FastAPI:
    app = FastAPI(
        title=APP_NAME,
        version=APP_VERSION,
        debug=DEBUG
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from api.auth_routes import router as auth_router
    from api.user_routes import router as user_router
    from api.invoice_routes import router as invoice_router

    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(invoice_router)

    @app.get("/")
    def root():
        return {
            "app": APP_NAME,
            "version": APP_VERSION,
            "status": "running"
        }

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    return app


def init_data():
    db = SessionLocal()
    try:
        admin_role = db.query(SysRole).filter(SysRole.role_code == "admin").first()
        if not admin_role:
            admin_role = SysRole(
                role_code="admin",
                role_name="超级管理员",
                description="拥有所有权限"
            )
            db.add(admin_role)
            db.flush()

        admin_user = db.query(SysUser).filter(SysUser.username == "admin").first()
        if not admin_user:
            hashed_password = hash_password("admin123")
            admin_user = SysUser(
                username="admin",
                password=hashed_password,
                real_name="超级管理员",
                role_id=admin_role.id,
                email="admin@example.com",
                phone="13800138000",
                status=1
            )
            db.add(admin_user)

        db.commit()
        print("数据初始化完成")
    except Exception as e:
        db.rollback()
        print(f"数据初始化失败: {e}")
    finally:
        db.close()


app = create_app()


@app.on_event("startup")
async def startup_event():
    init_db()
    init_data()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG
    )
