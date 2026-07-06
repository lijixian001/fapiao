# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：main.py
# 模块用途：FastAPI应用入口文件，负责创建应用实例、配置中间件、注册路由和启动初始化
# 说明：
#   - 使用FastAPI框架构建RESTful API服务
#   - 配置CORS跨域支持，允许前端应用访问
#   - 应用启动时自动初始化数据库表和默认数据
#   - 支持热重载（开发模式）
# ================================================================================

# 导入sys模块用于修改Python模块搜索路径
import sys
# 导入os模块用于文件路径操作
import os

# 将当前脚本所在目录添加到Python模块搜索路径的最前面
# 确保项目内部的模块（如core、models等）可以正确导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 从FastAPI框架导入FastAPI应用类
from fastapi import FastAPI
# 从FastAPI中间件导入CORS跨域资源共享中间件
from fastapi.middleware.cors import CORSMiddleware

# 从配置模块导入应用相关配置
from core.config import APP_NAME, APP_VERSION, DEBUG
# 从数据库模块导入初始化函数、引擎和会话工厂
from core.database import init_db, engine, SessionLocal
# 从用户模型导入SysUser类
from models.sys_user import SysUser
# 从角色模型导入SysRole类
from models.sys_role import SysRole
# 从认证模块导入密码哈希函数
from core.auth import hash_password


def create_app() -> FastAPI:
    """
    创建并配置FastAPI应用实例
    工厂模式创建应用，便于测试和不同环境配置

    返回值:
        FastAPI: 配置完成的FastAPI应用实例

    配置内容:
        1. 设置应用基本信息（名称、版本、调试模式）
        2. 配置CORS跨域中间件
        3. 注册所有API路由
        4. 添加健康检查和根路径接口
    """
    # 创建FastAPI应用实例
    # title: API文档标题
    # version: API版本号
    # debug: 是否开启调试模式
    app = FastAPI(
        title=APP_NAME,
        version=APP_VERSION,
        debug=DEBUG
    )

    # 添加CORS（跨域资源共享）中间件
    # 允许前端应用从不同域名/端口访问后端API
    # 注意：生产环境应限制allow_origins为具体域名，不要使用"*"
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],           # 允许所有来源的请求（开发环境用）
        allow_credentials=True,        # 允许携带认证凭证（如Cookie、Authorization头）
        allow_methods=["*"],           # 允许所有HTTP方法（GET, POST, PUT, DELETE等）
        allow_headers=["*"],           # 允许所有请求头
    )

    # 导入各路由模块
    # 使用局部导入避免循环依赖问题
    from api.auth_routes import router as auth_router
    from api.user_routes import router as user_router
    from api.invoice_routes import router as invoice_router

    # 注册认证相关路由（登录、登出、用户信息）
    app.include_router(auth_router)
    # 注册用户管理相关路由（用户CRUD）
    app.include_router(user_router)
    # 注册发票管理相关路由（发票CRUD、审核、归档）
    app.include_router(invoice_router)

    # 根路径接口 - 用于服务状态检查
    @app.get("/")
    def root():
        """
        根路径接口
        返回应用基本信息，用于快速验证服务是否正常运行

        返回值:
            dict: 包含应用名称、版本和运行状态的字典
        """
        return {
            "app": APP_NAME,
            "version": APP_VERSION,
            "status": "running"
        }

    # 健康检查接口 - 用于监控和负载均衡
    @app.get("/health")
    def health_check():
        """
        健康检查接口
        简单的健康检查端点，返回服务健康状态
        可用于Kubernetes liveness/readiness探针或其他监控系统

        返回值:
            dict: 健康状态信息
        """
        return {"status": "healthy"}

    # 返回配置好的应用实例
    return app


def init_data():
    """
    初始化默认数据
    在应用启动时检查并创建必要的初始数据，如：
    - 超级管理员角色
    - 默认管理员用户

    注意事项:
        - 使用独立的数据库会话，不与请求共享
        - 数据已存在则跳过，保证幂等性
        - 任何异常都会回滚，防止部分数据写入
    """
    # 创建一个新的数据库会话
    db = SessionLocal()
    try:
        # 检查是否已存在超级管理员角色
        # 通过角色编码admin查询
        admin_role = db.query(SysRole).filter(SysRole.role_code == "admin").first()
        # 如果不存在，则创建超级管理员角色
        if not admin_role:
            admin_role = SysRole(
                role_code="admin",                  # 角色编码，唯一标识
                role_name="超级管理员",               # 角色显示名称
                description="拥有所有权限"            # 角色描述
            )
            # 将角色对象添加到会话
            db.add(admin_role)
            # 刷新到数据库以获取生成的ID
            # flush会立即发送SQL到数据库，但不提交事务
            db.flush()

        # 检查是否已存在管理员用户
        # 优先查找用户名为"123"的管理员用户
        admin_user = db.query(SysUser).filter(SysUser.username == "123").first()
        # 如果不存在"123"用户，再尝试查找旧的"admin"用户
        if not admin_user:
            old_admin = db.query(SysUser).filter(SysUser.username == "admin").first()
            if old_admin:
                # 将旧的admin用户更改为123用户
                old_admin.username = "123"
                old_admin.password = hash_password("123")
                old_admin.real_name = "超级管理员"
                old_admin.email = "123@example.com"
                db.commit()
                db.refresh(old_admin)
                admin_user = old_admin
            else:
                # 如果都不存在，则创建默认管理员用户（用户名和密码都是123）
                hashed_password = hash_password("123")
                admin_user = SysUser(
                    username="123",                     # 用户名
                    password=hashed_password,           # 哈希后的密码
                    real_name="超级管理员",               # 真实姓名
                    role_id=admin_role.id,              # 关联角色ID
                    email="123@example.com",            # 邮箱
                    phone="13800138000",                # 手机号
                    status=1                            # 状态：1=启用
                )
                # 将用户对象添加到会话
                db.add(admin_user)
        else:
            # 如果用户已存在，确保密码是最新的（每次启动都重置为默认密码123，方便开发调试）
            admin_user.password = hash_password("123")

        # 提交事务，将所有更改持久化到数据库
        db.commit()
        # 输出初始化成功信息
        print("数据初始化完成")
    except Exception as e:
        # 发生异常时回滚事务，确保数据一致性
        db.rollback()
        # 输出错误信息
        print(f"数据初始化失败: {e}")
    finally:
        # 无论成功或失败，最终都关闭数据库会话
        db.close()


# 创建全局应用实例
# 这是uvicorn等ASGI服务器加载的入口点
app = create_app()


@app.on_event("startup")
async def startup_event():
    """
    应用启动事件处理函数
    在FastAPI应用启动完成前执行，用于初始化工作

    功能:
        1. 调用init_db()创建所有数据库表
        2. 调用init_data()初始化默认数据

    注意: startup事件已被标记为deprecated，
         新版本推荐使用lifespan事件处理
    """
    # 初始化数据库表结构
    init_db()
    # 初始化默认数据（角色、管理员用户等）
    init_data()


# 当直接运行此脚本时（如 python main.py），启动uvicorn服务器
if __name__ == "__main__":
    # 导入uvicorn ASGI服务器
    import uvicorn
    # 启动uvicorn服务器
    # "main:app" 指定模块和应用对象
    # host="0.0.0.0" 监听所有网络接口，允许外部访问
    # port=8000 服务端口
    # reload=DEBUG 开发模式下开启热重载，代码修改后自动重启
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG
    )
