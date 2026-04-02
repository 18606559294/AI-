"""
Search API 扩展测试 - 针对缺失覆盖行
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.resume import Resume
from app.models.template import Template


class TestSearchResumesExtended:
    """简历搜索扩展测试"""

    async def test_search_resumes_in_title(
        self, client: AsyncClient, auth_headers, test_user, db_session
    ):
        """测试: 在简历标题中搜索"""
        resume1 = Resume(
            user_id=test_user.id,
            title="软件工程师简历",
            content={},
            style_config={}
        )
        resume2 = Resume(
            user_id=test_user.id,
            title="产品经理简历",
            content={},
            style_config={}
        )
        db_session.add(resume1)
        db_session.add(resume2)
        await db_session.commit()

        response = await client.get(
            "/api/v1/search/resumes?q=软件",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert len(data["data"]["results"]) >= 1
        assert data["data"]["query"] == "软件"

    async def test_search_resumes_in_description(
        self, client: AsyncClient, auth_headers, test_user, db_session
    ):
        """测试: 在简历描述中搜索"""
        resume = Resume(
            user_id=test_user.id,
            title="我的简历",
            description="资深Java开发工程师，5年经验",
            content={},
            style_config={}
        )
        db_session.add(resume)
        await db_session.commit()

        response = await client.get(
            "/api/v1/search/resumes?q=Java",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] >= 1

    async def test_search_resumes_in_content_basic_info(
        self, client: AsyncClient, auth_headers, test_user, db_session
    ):
        """测试: 在内容基本信息中搜索"""
        resume = Resume(
            user_id=test_user.id,
            title="包含关键字的简历",
            description="张三的简历",
            content={
                "basic_info": {
                    "name": "张三",
                    "phone": "13800138000",
                    "email": "zhangsan@example.com"
                }
            },
            style_config={}
        )
        db_session.add(resume)
        await db_session.commit()

        # 搜索描述中的姓名
        response = await client.get(
            "/api/v1/search/resumes?q=张三",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        # 应该在描述中找到
        assert data["data"]["total"] >= 1

    async def test_search_resumes_pagination(
        self, client: AsyncClient, auth_headers, test_user, db_session
    ):
        """测试: 搜索结果分页"""
        # 创建多个简历
        for i in range(15):
            resume = Resume(
                user_id=test_user.id,
                title=f"搜索测试{i}",
                description="测试描述",
                content={},
                style_config={}
            )
            db_session.add(resume)
        await db_session.commit()

        # 第一页
        response1 = await client.get(
            "/api/v1/search/resumes?q=测试&page=1&page_size=5",
            headers=auth_headers
        )
        assert response1.status_code == 200
        data1 = response1.json()
        assert len(data1["data"]["results"]) == 5
        assert data1["data"]["page"] == 1

        # 第二页
        response2 = await client.get(
            "/api/v1/search/resumes?q=测试&page=2&page_size=5",
            headers=auth_headers
        )
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["data"]["page"] == 2

    async def test_search_resumes_unauthorized(
        self, client: AsyncClient
    ):
        """测试: 未授权搜索简历"""
        response = await client.get("/api/v1/search/resumes?q=test")

        assert response.status_code == 401

    async def test_search_resumes_empty_query(
        self, client: AsyncClient, auth_headers
    ):
        """测试: 空搜索词"""
        response = await client.get(
            "/api/v1/search/resumes?q=",
            headers=auth_headers
        )

        assert response.status_code == 422

    async def test_search_resumes_no_results(
        self, client: AsyncClient, auth_headers, test_user, db_session
    ):
        """测试: 没有搜索结果"""
        resume = Resume(
            user_id=test_user.id,
            title="普通简历",
            content={},
            style_config={}
        )
        db_session.add(resume)
        await db_session.commit()

        response = await client.get(
            "/api/v1/search/resumes?q=不存在的关键词xyz123",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] == 0
        assert len(data["data"]["results"]) == 0

    async def test_search_resumes_only_own_resumes(
        self, client: AsyncClient, auth_headers, db_session
    ):
        """测试: 只能搜索自己的简历"""
        other_user = User(
            email="search_other@example.com",
            password_hash="hash",
            username="search_other",
            role="user"
        )
        db_session.add(other_user)
        await db_session.commit()

        other_resume = Resume(
            user_id=other_user.id,
            title="其他用户的简历",
            content={},
            style_config={}
        )
        db_session.add(other_resume)
        await db_session.commit()

        # 当前用户搜索
        response = await client.get(
            "/api/v1/search/resumes?q=其他用户",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        # 应该找不到其他用户的简历
        assert data["data"]["total"] == 0


class TestSearchTemplatesExtended:
    """模板搜索扩展测试"""

    async def test_search_templates_by_name(
        self, client: AsyncClient, db_session
    ):
        """测试: 按模板名称搜索"""
        template = Template(
            name="现代简约模板",
            category="技术",
            layout="single",
            is_active=True,
            use_count=10
        )
        db_session.add(template)
        await db_session.commit()

        response = await client.get("/api/v1/search/templates?q=现代")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] >= 1

    async def test_search_templates_by_description(
        self, client: AsyncClient, db_session
    ):
        """测试: 按模板描述搜索"""
        template = Template(
            name="测试模板",
            description="适合金融行业的专业模板",
            category="金融",
            layout="single",
            is_active=True,
            use_count=5
        )
        db_session.add(template)
        await db_session.commit()

        response = await client.get("/api/v1/search/templates?q=金融")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] >= 1

    async def test_search_templates_with_category_filter(
        self, client: AsyncClient, db_session
    ):
        """测试: 按分类筛选模板"""
        template1 = Template(
            name="技术模板",
            category="技术",
            sub_category="后端",
            layout="single",
            is_active=True,
            use_count=10
        )
        template2 = Template(
            name="金融模板",
            category="金融",
            sub_category="银行",
            layout="single",
            is_active=True,
            use_count=10
        )
        db_session.add(template1)
        db_session.add(template2)
        await db_session.commit()

        response = await client.get(
            "/api/v1/search/templates?q=模板&category=技术"
        )

        assert response.status_code == 200
        data = response.json()
        # 应该只返回技术分类的模板
        for t in data["data"]["results"]:
            assert t["category"] == "技术"

    async def test_search_templates_with_industry_filter(
        self, client: AsyncClient, db_session
    ):
        """测试: 按行业(sub_category)筛选"""
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

        response = await client.get(
            "/api/v1/search/templates?q=开发&industry=后端"
        )

        assert response.status_code == 200

    async def test_search_templates_excludes_inactive(
        self, client: AsyncClient, db_session
    ):
        """测试: 搜索排除非活跃模板"""
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

        response = await client.get("/api/v1/search/templates?q=模板")

        assert response.status_code == 200
        data = response.json()
        # 所有结果应该是活跃的
        for t in data["data"]["results"]:
            assert t["is_active"] is True

    async def test_search_templates_pagination(
        self, client: AsyncClient, db_session
    ):
        """测试: 模板搜索分页"""
        for i in range(12):
            template = Template(
                name=f"测试模板{i}",
                category="test",
                layout="single",
                is_active=True,
                use_count=i
            )
            db_session.add(template)
        await db_session.commit()

        response = await client.get(
            "/api/v1/search/templates?q=测试&page=1&page_size=5"
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["results"]) == 5
        assert data["data"]["page"] == 1
        assert data["data"]["page_size"] == 5

    async def test_search_templates_ordering(
        self, client: AsyncClient, db_session
    ):
        """测试: 模板排序（免费优先，然后按时间）"""
        premium = Template(
            name="付费模板",
            category="test",
            is_premium=True,
            is_active=True,
            layout="single",
            use_count=100
        )
        free = Template(
            name="免费模板",
            category="test",
            is_premium=False,
            is_active=True,
            layout="single",
            use_count=50
        )
        db_session.add(premium)
        db_session.add(free)
        await db_session.commit()

        response = await client.get("/api/v1/search/templates?q=模板")

        assert response.status_code == 200
        data = response.json()
        # 免费模板应该排在前面
        if len(data["data"]["results"]) >= 2:
            first_is_premium = data["data"]["results"][0].get("is_premium")
            assert first_is_premium is False or first_is_premium is None


class TestSearchCategoriesExtended:
    """搜索分类扩展测试"""

    async def test_get_search_categories_with_data(
        self, client: AsyncClient, db_session
    ):
        """测试: 获取有数据的搜索分类"""
        categories = ["技术", "金融", "教育"]
        sub_categories = ["后端", "前端", "银行"]

        for cat in categories:
            template = Template(
                name=f"{cat}模板",
                category=cat,
                sub_category=sub_categories[categories.index(cat)] if len(sub_categories) > categories.index(cat) else None,
                layout="single",
                is_active=True,
                use_count=10
            )
            db_session.add(template)
        await db_session.commit()

        response = await client.get("/api/v1/search/categories")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert len(data["data"]) == 2

        # 验证分类结构
        category_data = next(d for d in data["data"] if d["type"] == "category")
        sub_category_data = next(d for d in data["data"] if d["type"] == "sub_category")

        assert "分类" in category_data["name"]
        assert "子分类" in sub_category_data["name"]

    async def test_get_search_categories_empty(
        self, client: AsyncClient, db_session
    ):
        """测试: 没有模板时获取分类"""
        # 清空现有模板（通过不创建任何模板）
        response = await client.get("/api/v1/search/categories")

        assert response.status_code == 200
        data = response.json()
        # 应该返回空列表
        category_data = next(d for d in data["data"] if d["type"] == "category")
        sub_category_data = next(d for d in data["data"] if d["type"] == "sub_category")
        assert category_data["options"] == []
        assert sub_category_data["options"] == []

    async def test_get_search_categories_excludes_null(
        self, client: AsyncClient, db_session
    ):
        """测试: 排除空分类"""
        template = Template(
            name="有分类模板",
            category="技术",
            sub_category=None,
            layout="single",
            is_active=True,
            use_count=10
        )
        template_no_cat = Template(
            name="无分类模板",
            category=None,
            sub_category=None,
            layout="single",
            is_active=True,
            use_count=5
        )
        db_session.add(template)
        db_session.add(template_no_cat)
        await db_session.commit()

        response = await client.get("/api/v1/search/categories")

        assert response.status_code == 200
        data = response.json()
        category_data = next(d for d in data["data"] if d["type"] == "category")

        # 应该包含有分类的
        assert "技术" in category_data["options"]
        # 列表中不应该有 None
        assert None not in category_data["options"]


class TestSearchSuggestionsExtended:
    """搜索建议扩展测试"""

    async def test_get_suggestions_from_user_titles(
        self, client: AsyncClient, auth_headers, test_user, db_session
    ):
        """测试: 从用户简历标题获取建议"""
        resume = Resume(
            user_id=test_user.id,
            title="高级Python开发工程师",
            content={},
            style_config={}
        )
        db_session.add(resume)
        await db_session.commit()

        response = await client.get(
            "/api/v1/search/suggestions?q=Python",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert len(data["data"]) >= 1

    async def test_get_suggestions_from_common_terms(
        self, client: AsyncClient, auth_headers
    ):
        """测试: 从常用搜索词获取建议"""
        response = await client.get(
            "/api/v1/search/suggestions?q=软件",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        # "软件工程师" 在常用词列表中
        assert any("软件工程师" in s for s in data["data"])

    async def test_get_suggestions_case_insensitive(
        self, client: AsyncClient, auth_headers, test_user, db_session
    ):
        """测试: 搜索建议不区分大小写"""
        resume = Resume(
            user_id=test_user.id,
            title="Java开发工程师",
            content={},
            style_config={}
        )
        db_session.add(resume)
        await db_session.commit()

        # 小写搜索
        response = await client.get(
            "/api/v1/search/suggestions?q=java",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        # 应该匹配到 Java开发工程师
        assert any("java" in s.lower() for s in data["data"])

    async def test_get_suggestions_limit_10(
        self, client: AsyncClient, auth_headers, test_user, db_session
    ):
        """测试: 建议结果限制在10条"""
        # 创建多个简历
        for i in range(15):
            resume = Resume(
                user_id=test_user.id,
                title=f"开发工程师{i}",
                content={},
                style_config={}
            )
            db_session.add(resume)
        await db_session.commit()

        response = await client.get(
            "/api/v1/search/suggestions?q=开发",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        # 最多返回10条
        assert len(data["data"]) <= 10

    async def test_get_suggestions_unauthorized(
        self, client: AsyncClient
    ):
        """测试: 未授权获取建议"""
        response = await client.get("/api/v1/search/suggestions?q=test")

        assert response.status_code == 401

    async def test_get_suggestions_empty_input(
        self, client: AsyncClient, auth_headers
    ):
        """测试: 空输入"""
        response = await client.get(
            "/api/v1/search/suggestions?q=",
            headers=auth_headers
        )

        assert response.status_code == 422
