"""
Templates API 扩展测试 - 针对缺失覆盖行
"""
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.template import Template, Favorite
from app.core.config import settings


class TestListTemplatesExtended:
    """模板列表扩展测试"""

    async def test_list_templates_default_pagination(
        self, client: AsyncClient, db_session
    ):
        """测试: 默认分页参数"""
        for i in range(5):
            template = Template(
                name=f"模板{i}",
                category="test",
                layout="single",
                is_active=True,
                use_count=i
            )
            db_session.add(template)
        await db_session.commit()

        # 不指定分页参数
        response = await client.get("/api/v1/templates")

        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 20

    async def test_list_templates_with_level_senior(
        self, client: AsyncClient, db_session
    ):
        """测试: 按高级职级筛选"""
        template = Template(
            name="高级模板",
            category="技术",
            level="senior",
            layout="single",
            is_active=True,
            use_count=10
        )
        db_session.add(template)
        await db_session.commit()

        response = await client.get("/api/v1/templates?level=senior")

        assert response.status_code == 200
        data = response.json()
        for t in data["data"]:
            assert t["level"] == "senior"

    async def test_list_templates_with_sub_category(
        self, client: AsyncClient, db_session
    ):
        """测试: 按子分类筛选"""
        template = Template(
            name="后端开发模板",
            category="技术",
            sub_category="后端",
            layout="single",
            is_active=True,
            use_count=10
        )
        db_session.add(template)
        await db_session.commit()

        response = await client.get("/api/v1/templates?sub_category=后端")

        assert response.status_code == 200

    async def test_list_templates_active_only(
        self, client: AsyncClient, db_session
    ):
        """测试: 只返回活跃模板"""
        active = Template(
            name="活跃模板",
            category="test",
            layout="single",
            is_active=True,
            use_count=10
        )
        inactive = Template(
            name="非活跃模板",
            category="test",
            layout="single",
            is_active=False,
            use_count=5
        )
        db_session.add(active)
        db_session.add(inactive)
        await db_session.commit()

        response = await client.get("/api/v1/templates")

        assert response.status_code == 200
        data = response.json()
        # 应该只包含活跃模板
        for t in data["data"]:
            assert t["id"] != inactive.id


class TestGetTemplateExtended:
    """获取模板详情扩展测试"""

    async def test_get_template_inactive_returns_404(
        self, client: AsyncClient, db_session
    ):
        """测试: 非活跃模板返回 404"""
        template = Template(
            name="非活跃",
            category="test",
            layout="single",
            is_active=False,
            use_count=0
        )
        db_session.add(template)
        await db_session.commit()

        response = await client.get(f"/api/v1/templates/{template.id}")

        assert response.status_code == 404


class TestUseTemplateExtended:
    """使用模板扩展测试"""

    async def test_use_free_template_as_free_user(
        self, client: AsyncClient, auth_headers, db_session
    ):
        """测试: 免费用户使用免费模板"""
        template = Template(
            name="免费模板",
            category="test",
            is_premium=False,
            layout="single",
            is_active=True,
            use_count=10
        )
        db_session.add(template)
        await db_session.commit()

        response = await client.post(
            f"/api/v1/templates/{template.id}/use",
            headers=auth_headers
        )

        assert response.status_code == 200

    async def test_use_premium_template_as_free_user_forbidden(
        self, client: AsyncClient, auth_headers, db_session
    ):
        """测试: 免费用户使用付费模板被拒绝"""
        template = Template(
            name="付费模板",
            category="test",
            is_premium=True,
            layout="single",
            is_active=True,
            use_count=10
        )
        db_session.add(template)
        await db_session.commit()

        response = await client.post(
            f"/api/v1/templates/{template.id}/use",
            headers=auth_headers
        )

        assert response.status_code == 403
        data = response.json()
        assert "高级会员" in data["detail"]

    async def test_use_template_increments_count(
        self, client: AsyncClient, auth_headers, test_user, db_session
    ):
        """测试: 使用模板增加计数"""
        template = Template(
            name="计数测试",
            category="test",
            is_premium=False,
            layout="single",
            is_active=True,
            use_count=100
        )
        db_session.add(template)
        await db_session.commit()

        initial_count = template.use_count

        await client.post(
            f"/api/v1/templates/{template.id}/use",
            headers=auth_headers
        )

        # 刷新并验证计数增加
        await db_session.refresh(template)
        assert template.use_count == initial_count + 1


class TestFavoriteTemplateExtended:
    """收藏模板扩展测试"""

    async def test_favorite_inactive_template_forbidden(
        self, client: AsyncClient, auth_headers, db_session
    ):
        """测试: 不能收藏非活跃模板"""
        template = Template(
            name="非活跃模板",
            category="test",
            layout="single",
            is_active=False,
            use_count=0
        )
        db_session.add(template)
        await db_session.commit()

        response = await client.post(
            f"/api/v1/templates/{template.id}/favorite",
            headers=auth_headers
        )

        assert response.status_code == 404

    async def test_favorite_duplicate_fails(
        self, client: AsyncClient, auth_headers, db_session
    ):
        """测试: 重复收藏失败"""
        template = Template(
            name="重复收藏测试",
            category="test",
            layout="single",
            is_active=True,
            use_count=10
        )
        db_session.add(template)
        await db_session.commit()

        # 第一次收藏
        response1 = await client.post(
            f"/api/v1/templates/{template.id}/favorite",
            headers=auth_headers
        )
        assert response1.status_code == 200

        # 第二次收藏
        response2 = await client.post(
            f"/api/v1/templates/{template.id}/favorite",
            headers=auth_headers
        )
        assert response2.status_code == 400

    async def test_unfavorite_removes_from_list(
        self, client: AsyncClient, auth_headers, db_session
    ):
        """测试: 取消收藏后从列表移除"""
        template = Template(
            name="取消收藏测试",
            category="test",
            layout="single",
            is_active=True,
            use_count=10
        )
        db_session.add(template)
        await db_session.commit()

        # 收藏
        await client.post(
            f"/api/v1/templates/{template.id}/favorite",
            headers=auth_headers
        )

        # 取消收藏
        await client.delete(
            f"/api/v1/templates/{template.id}/favorite",
            headers=auth_headers
        )

        # 验证不在收藏列表中
        response = await client.get(
            "/api/v1/templates/favorites/list",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        template_ids = [t["id"] for t in data["data"]]
        assert template.id not in template_ids


class TestGetFavoriteTemplatesExtended:
    """获取收藏列表扩展测试"""

    async def test_get_favorites_excludes_inactive(
        self, client: AsyncClient, auth_headers, db_session
    ):
        """测试: 收藏列表排除非活跃模板"""
        template = Template(
            name="活跃变非活跃",
            category="test",
            layout="single",
            is_active=True,
            use_count=10
        )
        db_session.add(template)
        await db_session.commit()

        # 收藏模板
        await client.post(
            f"/api/v1/templates/{template.id}/favorite",
            headers=auth_headers
        )

        # 设为非活跃
        template.is_active = False
        await db_session.commit()

        # 获取收藏列表
        response = await client.get(
            "/api/v1/templates/favorites/list",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        # 应该不包含非活跃模板
        template_ids = [t["id"] for t in data["data"]]
        assert template.id not in template_ids


class TestGetCategoriesExtended:
    """获取分类扩展测试"""

    async def test_get_categories_returns_distinct(
        self, client: AsyncClient, db_session
    ):
        """测试: 返回不同的分类"""
        categories = ["技术", "金融", "技术", "金融", "教育"]
        for cat in categories:
            template = Template(
                name=f"{cat}模板",
                category=cat,
                layout="single",
                is_active=True,
                use_count=10
            )
            db_session.add(template)
        await db_session.commit()

        response = await client.get("/api/v1/templates/categories")

        assert response.status_code == 200
        data = response.json()
        # 应该去重
        assert len(data["data"]) == len(set(data["data"]))

    async def test_get_categories_active_only(
        self, client: AsyncClient, db_session
    ):
        """测试: 只返回活跃模板的分类"""
        # 添加活跃和非活跃模板
        active = Template(
            name="活跃",
            category="active_category",
            layout="single",
            is_active=True,
            use_count=10
        )
        inactive = Template(
            name="非活跃",
            category="inactive_category",
            layout="single",
            is_active=False,
            use_count=10
        )
        db_session.add(active)
        db_session.add(inactive)
        await db_session.commit()

        response = await client.get("/api/v1/templates/categories")

        assert response.status_code == 200
        data = response.json()
        # 应该包含活跃分类
        assert "active_category" in data["data"]
        # 不应该包含非活跃分类
        assert "inactive_category" not in data["data"]

    async def test_get_categories_empty(
        self, client: AsyncClient, db_session
    ):
        """测试: 没有模板时返回空列表"""
        response = await client.get("/api/v1/templates/categories")

        assert response.status_code == 200
        data = response.json()
        assert data["data"] == []

    async def test_get_categories_excludes_null(
        self, client: AsyncClient, db_session
    ):
        """测试: 排除空分类"""
        # 添加有分类和无分类的模板
        with_cat = Template(
            name="有分类",
            category="有分类",
            layout="single",
            is_active=True,
            use_count=10
        )
        no_cat = Template(
            name="无分类",
            category=None,
            layout="single",
            is_active=True,
            use_count=10
        )
        db_session.add(with_cat)
        db_session.add(no_cat)
        await db_session.commit()

        response = await client.get("/api/v1/templates/categories")

        assert response.status_code == 200
        data = response.json()
        # 应该包含有分类的
        assert "有分类" in data["data"]
        # 列表中不应该有 None
        assert None not in data["data"]
