"""
导出路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import io
from urllib.parse import quote
from app.core.database import get_db
from app.core.security import get_current_user
from app.core.rate_limit import limiter, RateLimit
from app.models.user import User
from app.models.resume import Resume
from app.models.template import Template
from app.services.export.export_service import ExportService
from app.schemas.common import Response

router = APIRouter(prefix="/export", tags=["导出"])
export_service = ExportService()


@router.get("/{resume_id}/pdf")
@limiter.limit(RateLimit.RESUME_EXPORT)
async def export_to_pdf(
    request: Request,
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """导出简历为PDF"""
    # 获取简历
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    )
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="简历不存在"
        )
    
    # 获取模板HTML（如果有）
    template_html = None
    if resume.template_id:
        result = await db.execute(
            select(Template).where(Template.id == resume.template_id)
        )
        template = result.scalar_one_or_none()
        if template and template.html_content:
            template_html = template.html_content
    
    try:
        pdf_bytes = await export_service.to_pdf(
            resume_content=resume.content or {},
            style_config=resume.style_config,
            template_html=template_html
        )

        filename = f"{resume.title}.pdf"
        encoded_filename = quote(filename.encode('utf-8'))
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{resume_id}/word")
@limiter.limit(RateLimit.RESUME_EXPORT)
async def export_to_word(
    request: Request,
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """导出简历为Word文档"""
    # 获取简历
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    )
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="简历不存在"
        )
    
    word_bytes = await export_service.to_word(
        resume_content=resume.content or {},
        style_config=resume.style_config
    )

    filename = f"{resume.title}.docx"
    encoded_filename = quote(filename.encode('utf-8'))
    return StreamingResponse(
        io.BytesIO(word_bytes),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        }
    )


@router.get("/{resume_id}/html")
async def export_to_html(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """导出简历为HTML"""
    # 获取简历
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    )
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="简历不存在"
        )
    
    # 获取模板HTML（如果有）
    template_html = None
    if resume.template_id:
        result = await db.execute(
            select(Template).where(Template.id == resume.template_id)
        )
        template = result.scalar_one_or_none()
        if template and template.html_content:
            template_html = template.html_content
    
    html_content = await export_service.to_html(
        resume_content=resume.content or {},
        style_config=resume.style_config,
        template_html=template_html
    )

    filename = f"{resume.title}.html"
    encoded_filename = quote(filename.encode('utf-8'))
    return StreamingResponse(
        io.BytesIO(html_content.encode('utf-8')),
        media_type="text/html; charset=utf-8",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        }
    )


@router.get("/{resume_id}/preview")
async def preview_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """预览简历HTML"""
    # 获取简历
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    )
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="简历不存在"
        )
    
    # 获取模板HTML（如果有）
    template_html = None
    if resume.template_id:
        result = await db.execute(
            select(Template).where(Template.id == resume.template_id)
        )
        template = result.scalar_one_or_none()
        if template and template.html_content:
            template_html = template.html_content
    
    html_content = await export_service.to_html(
        resume_content=resume.content or {},
        style_config=resume.style_config,
        template_html=template_html
    )
    
    return StreamingResponse(
        io.BytesIO(html_content.encode('utf-8')),
        media_type="text/html; charset=utf-8"
    )
