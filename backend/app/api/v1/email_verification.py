"""
邮箱验证路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.services.email_service import email_service

router = APIRouter(prefix="/email", tags=["邮箱验证"])


class SendCodeRequest(BaseModel):
    """发送验证码请求"""
    email: EmailStr


class VerifyCodeRequest(BaseModel):
    """验证验证码请求"""
    email: EmailStr
    code: str


@router.post("/send-code", response_model=dict)
async def send_verification_code(request: SendCodeRequest):
    """发送验证码"""
    try:
        # 生成验证码
        code = email_service.generate_code(length=6)

        # 保存验证码（5分钟有效期）
        email_service.save_code(request.email, code, expire_minutes=5)

        # 发送邮件
        success = await email_service.send_verification_email(
            email=request.email,
            code=code
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="发送验证码失败，请稍后重试"
            )

        return {
            "code": 200,
            "message": "验证码已发送到您的邮箱，请查收",
            "data": {
                "expire_in": 300  # 5分钟，单位秒
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发送验证码失败: {str(e)}"
        )


@router.post("/verify-code", response_model=dict)
async def verify_code(request: VerifyCodeRequest):
    """验证验证码"""
    try:
        is_valid = email_service.verify_code(request.email, request.code)

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误或已过期"
            )

        return {
            "code": 200,
            "message": "验证成功",
            "data": {
                "verified": True
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"验证失败: {str(e)}"
        )
