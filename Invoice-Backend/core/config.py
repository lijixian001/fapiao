# ================================================================================
# 项目名称：企业发票管理业务系统后端
# 模块名称：core/config.py
# 模块用途：全局配置管理，集中管理数据库连接、JWT认证、应用信息等配置项
# 说明：
#   - 所有配置项在此文件统一定义，便于维护和环境切换
#   - 生产环境应使用环境变量或配置文件管理敏感信息，避免硬编码
# ================================================================================

# 数据库配置 - SQLite数据库文件路径，相对路径相对于项目根目录
# SQLite是轻量级嵌入式数据库，适合中小规模应用
DATABASE_URL = "sqlite:///./data/fapiao.db"

# JWT（JSON Web Token）认证配置
# SECRET_KEY：JWT签名密钥，用于生成和验证token，生产环境必须更换为强随机字符串
SECRET_KEY = "your-secret-key-change-in-production-2024"
# ALGORITHM：JWT签名算法，HS256是HMAC-SHA256对称加密算法
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES：访问令牌有效期，单位为分钟，1440分钟等于24小时
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24小时

# 应用基础配置
# APP_NAME：应用名称，用于API文档标题、页面标题等展示
APP_NAME = "企业发票管理业务系统"
# APP_VERSION：应用版本号，用于版本追踪
APP_VERSION = "1.0.0"
# DEBUG：调试模式开关，生产环境应设置为False
# 开启后会输出详细错误信息和自动重载
DEBUG = True
