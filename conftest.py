import os
import sys
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient

from main import app
from services.database.connection import db
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

        loop = asyncio.get_event_loop()
        loop.run_until_complete(db.close())

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
    """Yield a fresh async database session for each test, and close it after use."""
    from services.database.connection import db

    session = await db.get_session()
    try:
        yield session
    finally:
        await session.close()
