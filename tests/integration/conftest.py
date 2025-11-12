"""
Integration test fixtures and configuration.

These tests use REAL database connections with transaction rollback
for isolation. No mocking - tests verify actual system behavior.

Issue #292 - CORE-ALPHA-AUTH-INTEGRATION-TESTS
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Mark all tests in integration/ as integration tests
pytestmark = pytest.mark.integration


@pytest.fixture(scope="session")
def integration_db_url():
    """Use test database for integration tests"""
    return "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def integration_db(integration_db_url):
    """
    Database connection with transaction rollback.

    Each test runs in a transaction that's rolled back after completion,
    ensuring complete test isolation without manual cleanup.

    Architecture Decision: Transaction rollback strategy
    - Fast and deterministic
    - No test pollution
    - Natural fit with FastAPI TestClient
    """
    engine = create_async_engine(integration_db_url)

    async with engine.begin() as conn:
        # Start a nested transaction
        async with conn.begin_nested() as transaction:
            # Create session factory
            async_session_factory = sessionmaker(conn, class_=AsyncSession, expire_on_commit=False)

            async with async_session_factory() as session:
                yield session

            # Rollback transaction (automatic cleanup)
            await transaction.rollback()

    await engine.dispose()


@pytest.fixture
async def real_client(integration_db):
    """
    HTTP client using real database.

    This client uses the actual application with real database connections,
    not mocked dependencies. Perfect for integration testing.

    Architecture Decision: Real sessions via database connection override
    - Overrides db.get_session() to use integration_db
    - Maintains transaction isolation
    - Tests actual production code paths
    """
    from services.database.connection import db
    from web.app import app

    # Store original get_session method
    original_get_session = db.get_session

    # Override db.get_session to return integration_db
    async def override_get_session():
        return integration_db

    db.get_session = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    # Restore original method after test
    db.get_session = original_get_session
