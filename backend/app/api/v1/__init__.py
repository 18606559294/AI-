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
from app.api.v1.search import router as search_router

router = APIRouter()

# 注册各模块路由
router.include_router(auth_router)
router.include_router(resume_router)
router.include_router(template_router)
router.include_router(export_router)
router.include_router(advanced_router)
router.include_router(compliance_router)
router.include_router(email_verification_router)
router.include_router(ai_config_router)
router.include_router(search_router)
