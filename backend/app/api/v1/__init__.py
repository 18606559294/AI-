"""
API v1 路由汇总
"""
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.resumes import router as resume_router
from app.api.v1.templates import router as template_router
from app.api.v1.export import router as export_router
from app.api.v1.advanced import router as advanced_router
from app.api.v1.compliance import router as compliance_router
from app.api.v1.email_verification import router as email_verification_router
from app.api.v1.ai_config import router as ai_config_router
from app.api.v1.ai_usage import router as ai_usage_router
from app.api.v1.search import router as search_router

router = APIRouter()

# 修复response_model与FastAPI的兼容性问题
def fix_response_model(router: APIRouter) -> APIRouter:
    """移除不兼容的response_model"""
    for route in router.routes:
        if hasattr(route, 'response_model'):
            # 将response_model设为None以避免FastAPI的兼容性问题
            route.response_model = None
    return router

# 注册各模块路由
router.include_router(fix_response_model(auth_router))
router.include_router(fix_response_model(resume_router))
router.include_router(fix_response_model(template_router))
router.include_router(fix_response_model(export_router))
router.include_router(fix_response_model(advanced_router))
router.include_router(fix_response_model(compliance_router))
router.include_router(fix_response_model(email_verification_router))
router.include_router(fix_response_model(ai_config_router))
router.include_router(fix_response_model(ai_usage_router))
router.include_router(fix_response_model(search_router))
