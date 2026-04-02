"""
Auth API 扩展测试 - 针对缺失覆盖行
"""
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.security import create_access_token, create_refresh_token


class TestAuthRegisterExtended:
    """注册扩展测试"""

    async def test_register_sends_verification_email(
        self, client: AsyncClient, db_session
    ):
        """测试: 注册发送验证邮件"""
        mock_email_service = AsyncMock()
        mock_email_service.generate_code.return_value = "123456"
        mock_email_service.save_code = AsyncMock()
        mock_email_service.send_verification_email = AsyncMock()

        with patch("app.api.v1.auth.email_service", mock_email_service):
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "verify@example.com",
                    "username": "verifyuser",
                    "password": "VerifyPass123!"
                }
            )

            assert response.status_code == 200
            # 验证邮件服务被调用
            mock_email_service.generate_code.assert_called_once()
            mock_email_service.save_code.assert_called_once()
            mock_email_service.send_verification_email.assert_called_once()

    async def test_register_inactive_user(
        self, client: AsyncClient, db_session
    ):
        """测试: 注册后用户未验证状态"""
        mock_email_service = AsyncMock()
        mock_email_service.generate_code.return_value = "654321"
        mock_email_service.save_code = AsyncMock()
        mock_email_service.send_verification_email = AsyncMock()

        with patch("app.api.v1.auth.email_service", mock_email_service):
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "inactive@example.com",
                    "username": "inactive",
                    "password": "Inactive123!"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["data"]["require_verification"] is True

            # 验证用户创建为未验证状态
            result = await db_session.execute(
                select(User).where(User.email == "inactive@example.com")
            )
            user = result.scalar_one_or_none()
            assert user is not None
            assert user.is_verified is False

    async def test_register_with_minimal_data(
        self, client: AsyncClient, db_session
    ):
        """测试: 最小数据注册"""
        mock_email_service = AsyncMock()
        mock_email_service.generate_code.return_value = "111111"
        mock_email_service.save_code = AsyncMock()
        mock_email_service.send_verification_email = AsyncMock()

        with patch("app.api.v1.auth.email_service", mock_email_service):
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "minimal@example.com",
                    "username": "minimal",
                    "password": "Minimal123!"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["data"]["user"]["email"] == "minimal@example.com"


class TestAuthLoginExtended:
    """登录扩展测试"""

    async def test_login_updates_last_login_time(
        self, client: AsyncClient, test_user, db_session
    ):
        """测试: 登录更新最后登录时间"""
        # 获取原始登录时间
        await db_session.refresh(test_user)
        original_last_login = test_user.last_login_at

        response = await client.post(
            "/api/v1/auth/login/json",
            json={
                "email": test_user.email,
                "password": "TestPassword123!"
            }
        )

        assert response.status_code == 200

        # 验证最后登录时间已更新
        await db_session.refresh(test_user)
        assert test_user.last_login_at is not None
        if original_last_login:
            assert test_user.last_login_at > original_last_login

    async def test_login_inactive_account(
        self, client: AsyncClient, test_user, db_session
    ):
        """测试: 登录已禁用账户"""
        # 禁用用户
        test_user.is_active = False
        await db_session.commit()

        response = await client.post(
            "/api/v1/auth/login/json",
            json={
                "email": test_user.email,
                "password": "TestPassword123!"
            }
        )

        assert response.status_code == 403
        data = response.json()
        assert "已被禁用" in data["detail"]


class TestRefreshTokenExtended:
    """刷新令牌扩展测试"""

    async def test_refresh_token_inactive_user(
        self, client: AsyncClient, auth_headers, test_user, db_session
    ):
        """测试: 刷新令牌时用户已禁用"""
        # 先登录获取 refresh_token
        login_response = await client.post(
            "/api/v1/auth/login/json",
            json={
                "email": test_user.email,
                "password": "TestPassword123!"
            }
        )
        login_data = login_response.json()
        refresh_token = login_data["data"]["refresh_token"]

        # 禁用用户
        test_user.is_active = False
        await db_session.commit()

        # 尝试刷新令牌
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )

        assert response.status_code == 401

    async def test_refresh_token_without_sub(
        self, client: AsyncClient
    ):
        """测试: refresh token 没有 sub 字段"""
        # 创建一个没有 sub 的假 token
        from jose import jwt
        from app.core.config import settings

        fake_token = jwt.encode(
            {"user_id": "123"},  # 没有 sub
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": fake_token}
        )

        assert response.status_code == 401


class TestPasswordResetExtended:
    """密码重置扩展测试"""

    async def test_password_reset_sends_email(
        self, client: AsyncClient, test_user
    ):
        """测试: 密码重置发送邮件"""
        mock_email_service = AsyncMock()
        mock_email_service.generate_code.return_value = "888999"
        mock_email_service.save_reset_code = AsyncMock()
        mock_email_service.send_password_reset_email = AsyncMock()

        with patch("app.api.v1.auth.email_service", mock_email_service):
            response = await client.post(
                "/api/v1/auth/password-reset/request",
                json={"email": test_user.email}
            )

            assert response.status_code == 200
            # 验证邮件服务被调用
            mock_email_service.generate_code.assert_called_once()
            mock_email_service.save_reset_code.assert_called_once()
            mock_email_service.send_password_reset_email.assert_called_once()

    async def test_password_reset_verify_success(
        self, client: AsyncClient, test_user, db_session
    ):
        """测试: 验证重置码并重置密码"""
        mock_email_service = AsyncMock()
        mock_email_service.verify_reset_code = AsyncMock(return_value=True)

        with patch("app.api.v1.auth.email_service", mock_email_service):
            response = await client.post(
                "/api/v1/auth/password-reset/verify",
                json={
                    "email": test_user.email,
                    "code": "123456",
                    "new_password": "NewResetPass123!"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "重置成功" in data["message"]

    async def test_password_reset_verify_invalid_code(
        self, client: AsyncClient, test_user
    ):
        """测试: 无效的重置码"""
        mock_email_service = AsyncMock()
        mock_email_service.verify_reset_code = AsyncMock(return_value=False)

        with patch("app.api.v1.auth.email_service", mock_email_service):
            response = await client.post(
                "/api/v1/auth/password-reset/verify",
                json={
                    "email": test_user.email,
                    "code": "000000",
                    "new_password": "NewPass123!"
                }
            )

            assert response.status_code == 400

    async def test_password_reset_verify_nonexistent_user(
        self, client: AsyncClient
    ):
        """测试: 重置不存在的用户密码"""
        mock_email_service = AsyncMock()
        # 即使验证码正确，用户也不存在
        mock_email_service.verify_reset_code = AsyncMock(return_value=True)

        with patch("app.api.v1.auth.email_service", mock_email_service):
            response = await client.post(
                "/api/v1/auth/password-reset/verify",
                json={
                    "email": "nonexistent@example.com",
                    "code": "123456",
                    "new_password": "NewPass123!"
                }
            )

            assert response.status_code == 404


class TestChangePasswordExtended:
    """修改密码扩展测试"""

    async def test_change_password_updates_hash(
        self, client: AsyncClient, auth_headers, test_user, db_session
    ):
        """测试: 修改密码更新哈希"""
        original_hash = test_user.password_hash

        response = await client.post(
            "/api/v1/auth/change-password",
            headers=auth_headers,
            json={
                "old_password": "TestPassword123!",
                "new_password": "CompletelyNew123!"
            }
        )

        assert response.status_code == 200

        # 验证密码哈希已更新
        await db_session.refresh(test_user)
        assert test_user.password_hash != original_hash

    async def test_change_password_same_password(
        self, client: AsyncClient, auth_headers, test_user, db_session
    ):
        """测试: 修改为相同密码（技术上允许）"""
        original_hash = test_user.password_hash

        response = await client.post(
            "/api/v1/auth/change-password",
            headers=auth_headers,
            json={
                "old_password": "TestPassword123!",
                "new_password": "TestPassword123!"
            }
        )

        assert response.status_code == 200

        # 哈希仍然应该更新（因为重新哈希）
        await db_session.refresh(test_user)
        # 由于是相同密码，哈希值可能会相同（取决于实现）

    async def test_change_password_unauthorized(
        self, client: AsyncClient, test_user
    ):
        """测试: 未认证修改密码"""
        response = await client.post(
            "/api/v1/auth/change-password",
            json={
                "old_password": "TestPassword123!",
                "new_password": "NewPass123!"
            }
        )

        assert response.status_code == 401


class TestTokenCreation:
    """令牌创建测试"""

    async def test_access_token_contains_sub(
        self, client: AsyncClient, test_user
    ):
        """测试: access token 包含用户 ID"""
        response = await client.post(
            "/api/v1/auth/login/json",
            json={
                "email": test_user.email,
                "password": "TestPassword123!"
            }
        )

        assert response.status_code == 200
        data = response.json()
        access_token = data["data"]["access_token"]

        # 验证 token 可以解码
        from app.core.security import decode_token
        payload = decode_token(access_token)
        assert payload is not None
        assert "sub" in payload
        assert payload["sub"] == str(test_user.id)

    async def test_refresh_token_contains_sub(
        self, client: AsyncClient, test_user
    ):
        """测试: refresh token 包含用户 ID"""
        response = await client.post(
            "/api/v1/auth/login/json",
            json={
                "email": test_user.email,
                "password": "TestPassword123!"
            }
        )

        assert response.status_code == 200
        data = response.json()
        refresh_token = data["data"]["refresh_token"]

        # 验证 token 可以解码
        from app.core.security import decode_token
        payload = decode_token(refresh_token)
        assert payload is not None
        assert "sub" in payload

    async def test_token_expires_in_present(
        self, client: AsyncClient, test_user
    ):
        """测试: 响应包含 expires_in"""
        response = await client.post(
            "/api/v1/auth/login/json",
            json={
                "email": test_user.email,
                "password": "TestPassword123!"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "expires_in" in data["data"]
        assert isinstance(data["data"]["expires_in"], int)
