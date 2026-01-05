"""
Unit test fixtures and configuration.

These tests use REAL database connections for repository tests with
transaction rollback for isolation. Tests verify actual database behavior
without mocking the database layer itself (though external services may be mocked).

Issue #349 - TEST-INFRA-FIXTURES: Fix async_transaction fixture pattern

NOTE: The async_transaction fixture depends on test database having required tables.
If tables don't exist, tests will fail with "relation does not exist" errors.
See: dev/2025/11/22/issue-349-analysis-and-fixture.md for more details.
"""

from datetime import datetime
from uuid import UUID

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.database.models import Base


@pytest.fixture(scope="session")
def unit_db_url():
    """Use test database for unit tests with real database fixtures"""
    return "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest_asyncio.fixture
async def async_transaction(unit_db_url):
    """
    Async transaction fixture for unit tests requiring real database access.

    Provides an AsyncSession context manager that:
    - Connects to real test database (PostgreSQL)
    - Runs in a transaction that's rolled back after the test
    - Ensures complete test isolation without manual cleanup
    - Compatible with async_with usage pattern

    IMPORTANT: Requires test database to have schema/tables.

    If you see "relation X does not exist" errors:
    1. Run: python -m alembic upgrade head (to create tables)
    2. Or ensure test database is properly initialized
    3. See dev/2025/11/22/issue-349-analysis-and-fixture.md

    Usage:
        async def test_something(async_transaction):
            async with async_transaction as session:
                repo = SomeRepository(session)
                result = await repo.operation()
                # Transaction automatically rolls back

    Architecture:
    - Uses nested transactions for isolation
    - No test pollution between tests
    - Natural fit with repository patterns
    - Matches integration_db fixture pattern

    Related: Issue #349 (TEST-INFRA-FIXTURES)
    """
    # Create engine for test database
    engine = create_async_engine(
        unit_db_url,
        echo=False,  # Set to True for SQL debugging
    )

    # Begin a connection and nested transaction for this test
    async with engine.begin() as conn:
        # Start a nested transaction that will be rolled back after test
        async with conn.begin_nested() as transaction:
            # Create session factory bound to this transaction
            async_session_factory = sessionmaker(
                conn,
                class_=AsyncSession,
                expire_on_commit=False,
            )

            # Create and yield a context manager that provides sessions
            class TransactionContextManager:
                """Context manager that yields AsyncSession in transaction"""

                async def __aenter__(self) -> AsyncSession:
                    """Enter transaction context"""
                    self.session = async_session_factory()
                    return self.session

                async def __aexit__(self, exc_type, exc_val, exc_tb):
                    """Exit transaction context and close session"""
                    try:
                        await self.session.close()
                    except Exception:
                        pass  # Ignore close errors during cleanup

            yield TransactionContextManager()

            # Rollback transaction (automatic test isolation)
            await transaction.rollback()

    await engine.dispose()


@pytest_asyncio.fixture
async def create_test_user():
    """
    Factory fixture to create test users in database for FK constraint satisfaction.

    Returns a callable that creates users with the given UUID.
    Usage:
        async def test_something(async_transaction, create_test_user):
            async with async_transaction as session:
                user_id = await create_test_user(session, str(uuid4()))
                # Now can create todos with that owner_id
    """

    async def _create_user(
        session: AsyncSession, user_id: str, username: str = None, email: str = None
    ) -> str:
        """Create a test user in the given session for FK constraints."""
        if username is None:
            username = f"test_user_{user_id[:8]}"
        if email is None:
            email = f"{username}@example.com"

        # Insert user directly - bypasses domain validation, ensures FK constraints work
        await session.execute(
            text(
                """
                INSERT INTO users (id, username, email, password_hash, is_active, is_verified,
                                   created_at, updated_at, role, is_alpha)
                VALUES (:id, :username, :email, '', true, false, :created_at, :updated_at, 'user', true)
                ON CONFLICT (id) DO NOTHING
            """
            ),
            {
                "id": user_id,
                "username": username,
                "email": email,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
        )
        await session.commit()
        return user_id

    return _create_user
