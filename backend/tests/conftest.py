"""
测试配置和 Fixtures
"""
import asyncio
import os
import tempfile
import pytest
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.core.database import get_db, Base
from app.core.config import settings
from app.models.user import User
from app.models.resume import Resume, ResumeVersion
from app.models.export_task import ExportTask, ExportFormat, ExportStatus


# 测试数据库 - 使用内存 SQLite
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 创建测试引擎
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

# 创建测试会话
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """创建测试数据库会话"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """创建测试客户端"""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """创建测试用户"""
    from app.core.security import get_password_hash

    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=get_password_hash("TestPassword123!"),
        is_verified=True,
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def auth_headers(client: AsyncClient, test_user: User) -> dict:
    """获取认证头"""
    from app.core.security import create_access_token

    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def test_resume(db_session: AsyncSession, test_user: User) -> Resume:
    """创建测试简历"""
    resume = Resume(
        user_id=test_user.id,
        title="测试简历",
        description="这是一个测试简历",
        template_id=None,  # TODO: 关联到实际模板表
        content={
            "basic_info": {
                "name": "张三",
                "email": "zhangsan@example.com",
                "phone": "13800138000"
            },
            "education": [],
            "work_experience": [],
            "skills": []
        },
        style_config={
            "theme": "blue",
            "font": "default"
        }
    )
    db_session.add(resume)
    await db_session.commit()
    await db_session.refresh(resume)
    return resume


@pytest.fixture
async def test_export_task(db_session: AsyncSession, test_user: User, test_resume: Resume) -> ExportTask:
    """创建测试导出任务"""
    export_task = ExportTask(
        user_id=test_user.id,
        resume_ids=[test_resume.id],
        export_format=ExportFormat.PDF,
        status=ExportStatus.PENDING,
        progress=0.0,
        options={}
    )
    db_session.add(export_task)
    await db_session.commit()
    await db_session.refresh(export_task)
    return export_task
