"""
数据库测试
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.resume import Resume, ResumeVersion
from app.core.security import get_password_hash
from loguru import logger


@pytest.mark.asyncio
class TestDatabase:
    """数据库测试"""

    async def test_create_user(self, db: AsyncSession):
        """测试创建用户"""
        user = User(
            email="test_db@example.com",
            username="db_tester",
            hashed_password=get_password_hash("Test123!")
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        assert user.id is not None
        assert user.email == "test_db@example.com"
        logger.success("✅ 创建用户测试通过")

    async def test_user_resume_relationship(self, db: AsyncSession):
        """测试用户-简历关系"""
        # 创建用户
        user = User(
            email="test_rel@example.com",
            username="rel_tester",
            hashed_password=get_password_hash("Test123!")
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        # 创建简历
        resume = Resume(
            user_id=user.id,
            title="测试简历",
            content={"basic_info": {"name": "测试用户"}}
        )
        db.add(resume)
        await db.commit()
        await db.refresh(resume)

        # 查询验证
        query = select(Resume).where(Resume.user_id == user.id)
        result = await db.execute(query)
        resumes = result.scalars().all()

        assert len(resumes) == 1
        assert resumes[0].title == "测试简历"
        logger.success("✅ 用户-简历关系测试通过")

    async def test_resume_version(self, db: AsyncSession):
        """测试简历版本控制"""
        # 创建用户和简历
        user = User(
            email="test_ver@example.com",
            username="ver_tester",
            hashed_password=get_password_hash("Test123!")
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        resume = Resume(
            user_id=user.id,
            title="版本测试简历",
            content={"basic_info": {"name": "测试用户"}}
        )
        db.add(resume)
        await db.commit()
        await db.refresh(resume)

        # 创建版本
        version = ResumeVersion(
            resume_id=resume.id,
            version_number=1,
            content={"basic_info": {"name": "测试用户 v1"}},
            change_reason="初始版本"
        )
        db.add(version)
        await db.commit()
        await db.refresh(version)

        # 创建第二个版本
        version2 = ResumeVersion(
            resume_id=resume.id,
            version_number=2,
            content={"basic_info": {"name": "测试用户 v2"}},
            change_reason="更新内容"
        )
        db.add(version2)
        await db.commit()
        await db.refresh(version2)

        # 查询验证
        query = select(ResumeVersion).where(ResumeVersion.resume_id == resume.id)
        result = await db.execute(query)
        versions = result.scalars().all()

        assert len(versions) == 2
        assert versions[0].version_number == 1
        assert versions[1].version_number == 2
        logger.success("✅ 简历版本控制测试通过")

    async def test_transaction_rollback(self, db: AsyncSession):
        """测试事务回滚"""
        from sqlalchemy.exc import IntegrityError

        # 尝试创建重复用户（应该失败）
        user1 = User(
            email="test_dup@example.com",
            username="dup_tester",
            hashed_password=get_password_hash("Test123!")
        )
        db.add(user1)
        await db.commit()

        # 尝试创建重复邮箱的用户
        user2 = User(
            email="test_dup@example.com",  # 重复邮箱
            username="dup_tester2",
            hashed_password=get_password_hash("Test123!")
        )
        db.add(user2)

        try:
            await db.commit()
            assert False, "应该抛出 IntegrityError"
        except IntegrityError:
            await db.rollback()
            logger.success("✅ 事务回滚测试通过")

    async def test_query_filtering(self, db: AsyncSession):
        """测试查询过滤"""
        # 创建多个用户
        users = [
            User(
                email=f"test{i}@example.com",
                username=f"tester{i}",
                hashed_password=get_password_hash("Test123!")
            )
            for i in range(3)
        ]
        for user in users:
            db.add(user)
        await db.commit()

        # 查询过滤
        query = select(User).where(User.username.like("tester%"))
        result = await db.execute(query)
        filtered_users = result.scalars().all()

        assert len(filtered_users) == 3
        logger.success("✅ 查询过滤测试通过")


@pytest.fixture
async def db():
    """返回数据库会话"""
    from app.core.database import get_db

    async for session in get_db():
        yield session
        break


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
