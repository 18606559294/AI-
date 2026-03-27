"""
认证路由 - 基础认证功能
"""
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token,
    get_current_user
)
from app.core.config import settings
from app.core.rate_limit import limiter, RateLimit
from app.models.user import User
from app.schemas.user import (
    UserCreate, UserLogin, UserResponse,
    TokenResponse, TokenRefresh, PasswordChange,
    PasswordResetRequest, PasswordResetVerify
)
from app.services.email_service import email_service
from app.schemas.common import Response

router = APIRouter(prefix="/auth", tags=["认证"])


async def _authenticate_user(email: str, password: str, db: AsyncSession) -> User:
    """
    用户认证共享函数

    Args:
        email: 用户邮箱
        password: 密码
        db: 数据库会话

    Returns:
        认证成功的用户对象

    Raises:
        HTTPException: 认证失败
    """
    # 查找用户
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被禁用"
        )

    # 更新最后登录时间
    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()

    return user


def _create_token_response(user: User) -> TokenResponse:
    """
    创建令牌响应

    Args:
        user: 用户对象

    Returns:
        令牌响应
    """
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/register", response_model=None)
@limiter.limit(RateLimit.AUTH_REGISTER)
async def register(
    user_data: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """用户注册"""
    # 检查邮箱是否已存在
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )

    # 创建用户
    user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=get_password_hash(user_data.password),
        is_verified=False,  # 需要邮箱验证
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # 生成并发送验证码
    verification_code = email_service.generate_code()
    await email_service.save_code(user_data.email, verification_code, expire_minutes=5)
    await email_service.send_verification_email(user_data.email, verification_code)

    return Response(
        data={
            "user": UserResponse.model_validate(user),
            "require_verification": True
        },
        message="注册成功，验证码已发送到您的邮箱"
    )


@router.post("/login", response_model=None)
@limiter.limit(RateLimit.AUTH_LOGIN)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """用户登录 - OAuth2 表单格式"""
    user = await _authenticate_user(form_data.username, form_data.password, db)
    return Response(data=_create_token_response(user), message="登录成功")


@router.post("/login/json")
async def login_json(
    login_data: UserLogin,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """用户登录 - JSON格式"""
    user = await _authenticate_user(login_data.email, login_data.password, db)
    return Response(data=_create_token_response(user), message="登录成功")


@router.post("/refresh", response_model=None)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """刷新令牌"""
    # 验证 refresh token
    payload = decode_token(token_data.refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌格式"
        )

    # 查找用户
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已被禁用"
        )

    return Response(
        data=_create_token_response(user),
        message="令牌刷新成功"
    )


@router.get("/me", response_model=None)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    return Response(
        data=UserResponse.model_validate(current_user),
        message="获取成功"
    )


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """修改密码"""
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="原密码错误"
        )

    current_user.password_hash = get_password_hash(password_data.new_password)
    await db.commit()

    return Response(message="密码修改成功")


@router.post("/password-reset/request")
@limiter.limit(RateLimit.AUTH_PASSWORD_RESET)
async def request_password_reset(
    request: Request,
    request_data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    """请求密码重置"""
    # 检查邮箱是否存在
    result = await db.execute(
        select(User).where(User.email == request_data.email)
    )
    user = result.scalar_one_or_none()

    # 无论用户是否存在都返回成功（防止邮箱枚举攻击）
    if user:
        # 生成重置码
        reset_code = email_service.generate_code()
        await email_service.save_reset_code(request_data.email, reset_code, expire_minutes=15)

        # 发送重置邮件
        await email_service.send_password_reset_email(request_data.email, reset_code)

    return Response(message="如果该邮箱已注册，重置验证码已发送到您的邮箱")


@router.post("/password-reset/verify")
async def verify_password_reset(
    reset_data: PasswordResetVerify,
    db: AsyncSession = Depends(get_db)
):
    """验证密码重置码并重置密码"""
    # 验证重置码
    if not await email_service.verify_reset_code(reset_data.email, reset_data.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码无效或已过期"
        )

    # 查找用户
    result = await db.execute(
        select(User).where(User.email == reset_data.email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 更新密码
    user.password_hash = get_password_hash(reset_data.new_password)
    await db.commit()

    return Response(message="密码重置成功，请使用新密码登录")
