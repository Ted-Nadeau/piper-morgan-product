"""
conftest.py — Test infrastructure for Piper Morgan

## Session Management Pattern (2025-07-14)

**IMPORTANT:**
- Do NOT reuse a single AsyncSession for multiple DB operations in a loop or across awaits.
- This causes asyncpg/SQLAlchemy errors: 'cannot perform operation: another operation is in progress'.
- Instead, use the new `db_session_factory` fixture to get a fresh session for each operation.

### Example usage:
    @pytest.mark.asyncio
    async def test_something(db_session_factory):
        for item in items:
            async with await db_session_factory() as session:
                repo = FileRepository(session)
                await repo.save_file_metadata(file)

This pattern prevents concurrent session usage errors and aligns with DDD/test best practices.
"""

import os
import sys
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient

from main import app
from services.database.connection import db
from services.database.session_factory import AsyncSessionFactory
from services.knowledge_graph.document_service import DocumentService
from services.knowledge_graph.ingestion import DocumentIngester
from services.queries.conversation_queries import ConversationQueryService
from services.queries.file_queries import FileQueryService
from services.queries.project_queries import ProjectQueryService
from services.queries.query_router import QueryRouter

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture(scope="session", autouse=True)
def close_db_event_loop(request):
    def fin():
        import asyncio

        try:
            # Try to get existing event loop
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                # Create new event loop if closed
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Close database connections
            loop.run_until_complete(db.close())

        except RuntimeError:
            # If no event loop exists, create one for cleanup
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(db.close())
            finally:
                loop.close()

    request.addfinalizer(fin)


@pytest.fixture(scope="session")
def test_client():
    """Create a test client with properly initialized app state"""
    # Create mock repository for testing
    mock_repo = Mock()
    mock_repo.list_active_projects = AsyncMock(return_value=[])
    mock_repo.get_by_id = AsyncMock(return_value=None)
    mock_repo.get_default_project = AsyncMock(return_value=None)
    mock_repo.find_by_name = AsyncMock(return_value=None)
    mock_repo.count_active_projects = AsyncMock(return_value=0)

    # Create mock file repository for testing
    mock_file_repo = Mock()
    mock_file_repo.get_by_id = AsyncMock(return_value=None)
    mock_file_repo.search_by_name = AsyncMock(return_value=[])

    # Initialize app state for tests (similar to lifespan function)
    app.state.query_router = QueryRouter(
        project_query_service=ProjectQueryService(mock_repo),
        conversation_query_service=ConversationQueryService(),
        file_query_service=FileQueryService(mock_file_repo),
    )
    app.state.document_service = DocumentService()
    app.state.ingester = DocumentIngester()

    return TestClient(app)


@pytest.fixture
async def db_session():
    """Yield a fresh async database session for each test, and close it after use.

    DEPRECATED: Use async_session fixture instead for new tests.
    This fixture is maintained for backward compatibility.
    """
    async with AsyncSessionFactory.session_scope() as session:
        yield session


@pytest.fixture
async def db_session_factory():
    """Provide a factory that creates fresh async sessions for each operation.

    Usage:
        async with await db_session_factory() as session:
            repo = FileRepository(session)
            ...
    """
    from services.database.connection import db

    async def _create_session():
        session = await db.get_session()
        return session

    return _create_session


@pytest.fixture
async def async_session():
    """Provide AsyncSessionFactory.session_scope() for production-pattern tests.

    Usage:
        async def test_something(async_session):
            async with async_session as session:
                repo = FileRepository(session)
                ...
    """
    return AsyncSessionFactory.session_scope()


@pytest.fixture
async def async_transaction():
    """Provide AsyncSessionFactory.transaction_scope() for explicit transaction tests.

    Usage:
        async def test_something(async_transaction):
            async with async_transaction as session:
                repo = FileRepository(session)
                ...
    """
    return AsyncSessionFactory.transaction_scope()


@pytest.fixture(scope="function", autouse=True)
async def cleanup_sessions():
    """Ensure proper cleanup after each test function"""
    yield
    # Allow some time for any pending async operations to complete
    import asyncio

    await asyncio.sleep(0.1)  # Increased delay for more thorough cleanup
