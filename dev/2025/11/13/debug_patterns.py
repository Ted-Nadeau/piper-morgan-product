#!/usr/bin/env python3
"""Debug script to check database connectivity"""

import asyncio
from uuid import UUID

from sqlalchemy import select

from services.database.models import LearnedPattern
from services.database.session_factory import AsyncSessionFactory

TEST_USER_ID = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")


async def test_query():
    """Test querying patterns"""
    print(f"Querying patterns for user {TEST_USER_ID}...")

    async with AsyncSessionFactory.session_scope() as session:
        result = await session.execute(
            select(LearnedPattern)
            .where(LearnedPattern.user_id == TEST_USER_ID)
            .order_by(LearnedPattern.last_used_at.desc())
        )
        patterns = result.scalars().all()

        print(f"Found {len(patterns)} patterns")
        for p in patterns:
            print(f"  - {p.id}: {p.pattern_type.value}, enabled={p.enabled}")

        return patterns


if __name__ == "__main__":
    asyncio.run(test_query())
