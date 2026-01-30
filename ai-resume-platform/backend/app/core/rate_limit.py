"""
API限流配置
使用slowapi实现请求频率限制,防止恶意刷接口
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from app.core.config import settings


def get_user_id(request: Request) -> str:
    """
    获取用户ID用于限流
    优先使用认证用户ID,否则使用IP地址
    """
    # 尝试从请求中获取用户ID
    try:
        # 检查是否有认证用户
        if hasattr(request.state, 'user') and request.state.user:
            return f"user:{request.state.user.id}"
    except:
        pass

    # 降级到IP地址限流
    return get_remote_address(request)


# 创建限流器实例
limiter = Limiter(
    key_func=get_user_id,
    default_limits=["200/hour"],  # 默认限制:每小时200次
    storage_uri="memory://",      # 使用内存存储(生产环境应使用Redis)
    headers_enabled=True,         # 在响应头中包含限流信息
    strategy="fixed-window"       # 使用固定窗口策略
)


# 限流策略定义
class RateLimit:
    """限流策略类"""

    # 认证相关 - 严格限制
    AUTH_REGISTER = "5/hour"      # 注册:每小时5次
    AUTH_LOGIN = "20/minute"      # 登录:每分钟20次
    AUTH_PASSWORD_RESET = "3/hour" # 密码重置:每小时3次
    AUTH_CODE_SEND = "10/hour"    # 验证码发送:每小时10次

    # 简历操作 - 中等限制
    RESUME_CREATE = "30/hour"     # 创建简历:每小时30次
    RESUME_UPDATE = "100/hour"    # 更新简历:每小时100次
    RESUME_DELETE = "20/hour"     # 删除简历:每小时20次
    RESUME_EXPORT = "50/hour"     # 导出简历:每小时50次

    # AI功能 - 严格限制(消耗资源)
    AI_GENERATE = "20/hour"       # AI生成:每小时20次
    AI_OPTIMIZE = "50/hour"       # AI优化:每小时50次
    AI_ANALYZE = "30/hour"        # AI分析:每小时30次

    # 通用查询 - 宽松限制
    GENERAL_GET = "300/hour"      # GET请求:每小时300次
    GENERAL_SEARCH = "100/hour"   # 搜索:每小时100次


# 自定义错误处理
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """自定义限流错误响应"""
    from fastapi import JSONResponse
    from app.schemas.common import Response

    return JSONResponse(
        status_code=429,
        content={
            "code": 429,
            "message": "请求过于频繁,请稍后再试",
            "detail": f"限流规则: {exc.detail}",
            "data": None
        }
    )
