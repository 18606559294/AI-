"""
数据模型汇总
"""
from app.models.user import User, UserRole
from app.models.resume import Resume, ResumeVersion, ResumeStatus
from app.models.template import Template, Favorite, OperationLog

__all__ = [
    "User",
    "UserRole",
    "Resume",
    "ResumeVersion",
    "ResumeStatus",
    "Template",
    "Favorite",
    "OperationLog",
]
