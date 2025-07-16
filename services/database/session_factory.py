"""
Async Session Factory
Provides standardized session management with automatic resource cleanup
"""

from contextlib import asynccontextmanager
from typing import AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from .connection import db


class AsyncSessionFactory:
    """Factory for creating async database sessions with automatic resource management"""

    @staticmethod
    async def create_session() -> AsyncSession:
        """Create a new async session

        Returns:
            AsyncSession: New database session

        Note:
            Caller is responsible for closing the session.
            Prefer using session_scope() context manager for automatic cleanup.
        """
        return await db.get_session()

    @staticmethod
    @asynccontextmanager
    async def session_scope() -> AsyncContextManager[AsyncSession]:
        """Context manager for automatic session lifecycle management

        Yields:
            AsyncSession: Database session with automatic cleanup

        Example:
            async with AsyncSessionFactory.session_scope() as session:
                repo = ExampleRepository(session)
                result = await repo.operation()
                # Automatic commit and cleanup
        """
        session = await AsyncSessionFactory.create_session()
        try:
            yield session
        except Exception:
            try:
                await session.rollback()
            except Exception:
                # Ignore rollback errors during cleanup
                pass
            raise
        finally:
            try:
                await session.close()
            except Exception:
                # Ignore close errors during cleanup
                pass

    @staticmethod
    @asynccontextmanager
    async def transaction_scope() -> AsyncContextManager[AsyncSession]:
        """Context manager for explicit transaction management

        Yields:
            AsyncSession: Database session within transaction context

        Example:
            async with AsyncSessionFactory.transaction_scope() as session:
                repo = ExampleRepository(session)
                await repo.operation()
                # Explicit transaction commit on success, rollback on exception
        """
        session = await AsyncSessionFactory.create_session()
        try:
            async with session.begin():
                yield session
        finally:
            try:
                await session.close()
            except Exception:
                # Ignore close errors during cleanup
                pass
