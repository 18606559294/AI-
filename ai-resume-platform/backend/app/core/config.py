"""
应用配置模块
"""
from typing import Optional, List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用基础配置
    APP_NAME: str = "AI简历智能生成平台"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置
    # 开发环境使用SQLite，生产环境使用MySQL
    USE_SQLITE: bool = True  # 设为False使用MySQL
    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_resume.db"
    DATABASE_POOL_SIZE: int = 5  # SQLite不需要大连接池
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT配置
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # ========== AI模型配置 ==========

    # 默认AI提供商
    DEFAULT_AI_PROVIDER: str = "openai"  # openai/deepseek/xiaomi

    # OpenAI配置
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 4000
    OPENAI_TEMPERATURE: float = 0.7

    # DeepSeek配置（中国AI模型）
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MAX_TOKENS: int = 4000
    DEEPSEEK_TEMPERATURE: float = 0.7

    # 小米MiMo AI配置
    # 官方文档: https://platform.xiaomimimo.com/#/docs/quick-start/first-api-call
    XIAOMI_API_KEY: str = ""
    XIAOMI_MODEL: str = "MiMo-V2-Flash"  # 小米MiMo V2 Flash模型
    XIAOMI_BASE_URL: str = "https://api.xiaomimimo.com/v1"
    XIAOMI_MAX_TOKENS: int = 4000
    XIAOMI_TEMPERATURE: float = 0.7
    
    # 文件存储配置
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "doc", "docx", "png", "jpg", "jpeg"]
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "*"]
    
    # 邮件配置（可选）
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    # 微信登录配置（可选）
    WECHAT_APP_ID: Optional[str] = None
    WECHAT_APP_SECRET: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


settings = get_settings()
