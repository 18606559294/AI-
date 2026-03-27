#!/usr/bin/env python3
"""
OAuth 字段数据库迁移脚本

添加 Google 和 GitHub OAuth 相关字段到 users 表
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.config import settings


async def get_existing_columns(conn):
    """获取 users 表现有的列"""
    result = await conn.execute(text("PRAGMA table_info(users)"))
    rows = result.fetchall()
    return {row[1] for row in rows}


async def migrate():
    """执行数据库迁移"""
    print(f"Using database: {settings.DATABASE_URL}")
    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        # 获取现有列
        existing_columns = await get_existing_columns(conn)
        print(f"Existing columns: {sorted(existing_columns)}")

        # 定义要添加的列
        new_columns = {
            "google_id": "VARCHAR(100)",
            "google_email": "VARCHAR(255)",
            "google_verified_email": "BOOLEAN DEFAULT 0",
            "github_id": "INTEGER",
            "github_login": "VARCHAR(100)",
            "github_email": "VARCHAR(255)",
        }

        # 定义需要创建唯一索引的列
        unique_indexes = {
            "google_id": "ix_users_google_id",
            "github_id": "ix_users_github_id",
        }

        # 添加不存在的列
        for col_name, col_def in new_columns.items():
            if col_name not in existing_columns:
                try:
                    await conn.execute(text(
                        f"ALTER TABLE users ADD COLUMN {col_name} {col_def}"
                    ))
                    print(f"✓ Added column: {col_name}")
                except Exception as e:
                    print(f"✗ Failed to add column {col_name}: {e}")
            else:
                print(f"⊙ Column already exists: {col_name}")

        # 创建唯一索引
        for col_name, index_name in unique_indexes.items():
            # 检查索引是否存在
            result = await conn.execute(text(
                f"SELECT name FROM sqlite_master WHERE type='index' AND name='{index_name}'"
            ))
            if not result.fetchone():
                try:
                    await conn.execute(text(
                        f"CREATE UNIQUE INDEX {index_name} ON users ({col_name})"
                    ))
                    print(f"✓ Created unique index: {index_name}")
                except Exception as e:
                    print(f"✗ Failed to create index {index_name}: {e}")
            else:
                print(f"⊙ Index already exists: {index_name}")

    await engine.dispose()
    print("\n✅ Migration completed successfully!")


if __name__ == "__main__":
    asyncio.run(migrate())
