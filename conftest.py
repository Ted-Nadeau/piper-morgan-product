"""Root-level pytest configuration

PM-058 FIX: ASYNCPG CONCURRENCY ISSUE RESOLVED
Provides async_transaction fixture for test isolation with dedicated connections.
"""

from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture(scope="function")
async def async_transaction(db_engine):
    """PM-058 FIX: ASYNCPG CONCURRENCY ISSUE RESOLVED

    Provides isolated transaction context for tests.

    Features:
    - Dedicated connection (prevents connection pool exhaustion)
    - Transaction with rollback (ensures test isolation)
    - Auto-cleanup on exception

    Usage:
        async def test_something(async_transaction):
            async with async_transaction as session:
                repo = Repository(session)
                await repo.do_something()

    Args:
        db_engine: Database engine fixture (creates fresh engine per test)

    Returns:
        Async context manager yielding AsyncSession
    """
    # Create dedicated connection from engine
    connection = await db_engine.connect()

    try:
        # Start transaction
        transaction = await connection.begin()

        try:
            # Bind session to connection for isolation
            session = AsyncSession(bind=connection, expire_on_commit=False)

            @asynccontextmanager
            async def _transaction():
                """Inner context manager for session lifecycle"""
                try:
                    yield session
                finally:
                    await session.close()

            # Yield the context manager
            yield _transaction()

        finally:
            # Rollback for test isolation
            await transaction.rollback()

    finally:
        # Connection cleanup
        await connection.close()
