"""
认证路由
"""
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt
import httpx
from app.core.database import get_db
from app.core.security import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token, decode_token,
    get_current_user
)
from app.core.config import settings
from app.core.rate_limit import limiter, RateLimit
from app.models.user import User
from app.schemas.user import (
    UserCreate, UserLogin, UserResponse,
    TokenResponse, TokenRefresh, PasswordChange,
    PasswordResetRequest, PasswordResetVerify,
    WechatLoginRequest, WechatUserInfo
)
from app.services.email_service import email_service
from app.schemas.common import Response

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=None)
@limiter.limit(RateLimit.AUTH_REGISTER)
async def register(
    user_data: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """用户注册 - 注册成功后自动登录返回token"""
    # 检查邮箱是否已存在
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )

    # 检查手机号是否已存在
    if user_data.phone:
        result = await db.execute(select(User).where(User.phone == user_data.phone))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该手机号已被注册"
            )

    # 创建用户
    user = User(
        email=user_data.email,
        phone=user_data.phone,
        username=user_data.username,
        password_hash=get_password_hash(user_data.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # 注册成功后自动生成token，实现自动登录
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return Response(
        data={
            "user": UserResponse.model_validate(user),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        },
        message="注册成功"
    )


@router.post("/login", response_model=None)
@limiter.limit(RateLimit.AUTH_LOGIN)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """用户登录 - OAuth2 表单格式"""
    # 查找用户
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password_hash):
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

    # 生成令牌
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return Response(
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
        message="登录成功"
    )


@router.post("/login/json")
async def login_json(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """用户登录 - JSON格式"""
    # 查找用户
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(login_data.password, user.password_hash):
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

    # 生成令牌
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return Response(
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
        message="登录成功"
    )


@router.post("/refresh", response_model=None)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """刷新令牌"""
    payload = decode_token(token_data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )
    
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已被禁用"
        )
    
    # 生成新令牌
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return Response(
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
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
        email_service.save_reset_code(request_data.email, reset_code, expire_minutes=15)

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
    if not email_service.verify_reset_code(reset_data.email, reset_data.code):
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


# ==================== 微信登录 ====================

async def _get_wechat_access_token(code: str) -> dict:
    """
    通过微信授权码获取access_token
    文档: https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login.html
    """
    appid = getattr(settings, 'WECHAT_APP_ID', '')
    secret = getattr(settings, 'WECHAT_APP_SECRET', '')

    if not appid or not secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="微信登录未配置，请联系管理员"
        )

    async with httpx.AsyncClient() as client:
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": appid,
            "secret": secret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        response = await client.get(url, params=params)
        data = response.json()

        if "errcode" in data and data["errcode"] != 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"微信授权失败: {data.get('errmsg', '未知错误')}"
            )

        return data


@router.post("/wechat/login", response_model=None)
async def wechat_login(
    request: WechatLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    微信小程序登录

    流程:
    1. 小程序调用 wx.login 获取 code
    2. 前端将 code 发送到后端
    3. 后端通过 code 向微信服务器获取 session_key 和 openid
    4. 根据 openid 查找或创建用户
    5. 返回 JWT token
    """
    # 获取微信用户信息
    wechat_data = await _get_wechat_access_token(request.code)
    openid = wechat_data.get("openid")
    session_key = wechat_data.get("session_key")
    unionid = wechat_data.get("unionid")  # 只有开放平台绑定的账号才有

    if not openid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="获取微信用户信息失败"
        )

    # 查找是否已有该openid的用户
    result = await db.execute(select(User).where(User.wechat_openid == openid))
    user = result.scalar_one_or_none()

    if user:
        # 用户已存在，更新登录时间
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账户已被禁用"
            )
        user.last_login_at = datetime.now(timezone.utc)
        await db.commit()
    else:
        # 新用户，创建账号
        # 使用一个临时邮箱（基于openid生成）
        temp_email = f"wx_{openid}@wechat.local"

        # 检查邮箱是否已被占用（理论上不太可能）
        existing = await db.execute(select(User).where(User.email == temp_email))
        if existing.scalar_one_or_none():
            # 极端情况，使用随机数
            import random
            temp_email = f"wx_{random.randint(1000000, 9999999)}@wechat.local"

        user = User(
            email=temp_email,
            username=f"微信用户_{openid[:8]}",
            password_hash=get_password_hash(str(openid)),  # 临时密码
            wechat_openid=openid,
            wechat_unionid=unionid,
            is_verified=True,  # 微信用户默认已验证
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # 生成令牌
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return Response(
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
        message="微信登录成功"
    )


@router.post("/wechat/bind", response_model=None)
async def wechat_bind_account(
    code: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    绑定微信账号到当前用户
    """
    # 获取微信用户信息
    wechat_data = await _get_wechat_access_token(code)
    openid = wechat_data.get("openid")
    unionid = wechat_data.get("unionid")

    if not openid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="获取微信用户信息失败"
        )

    # 检查该openid是否已被其他用户绑定
    existing = await db.execute(
        select(User).where(User.wechat_openid == openid).where(User.id != current_user.id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该微信账号已被其他用户绑定"
        )

    # 绑定微信信息到当前用户
    current_user.wechat_openid = openid
    current_user.wechat_unionid = unionid
    await db.commit()

    return Response(
        data=UserResponse.model_validate(current_user),
        message="微信账号绑定成功"
    )


@router.post("/wechat/unbind")
async def wechat_unbind_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    解绑微信账号
    """
    if not current_user.wechat_openid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="未绑定微信账号"
        )

    current_user.wechat_openid = None
    current_user.wechat_unionid = None
    await db.commit()

    return Response(message="微信账号解绑成功")
