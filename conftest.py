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
from unittest.mock import AsyncMock, Mock, patch

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
    """Python 3.11+ compatible database cleanup fixture"""

    def fin():
        # Simplified cleanup for Python 3.11+ compatibility
        # Let SQLAlchemy and asyncpg handle connection cleanup naturally
        # Don't try to manage event loops during teardown
        import warnings

        # Suppress asyncpg warnings during teardown
        warnings.filterwarnings("ignore", category=ResourceWarning, module="asyncpg")
        warnings.filterwarnings("ignore", message=".*Event loop is closed.*")

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
    """Provide isolated transaction session for tests with automatic rollback.

    This fixture ensures each test runs in an isolated transaction that
    gets rolled back after the test completes, preventing test state leakage.

    Usage:
        async def test_something(async_transaction):
            async with async_transaction as session:
                repo = FileRepository(session)
                ...

    TODO PM-058: ASYNCPG CONCURRENCY ISSUE
    This fixture causes "cannot perform operation: another operation is in progress"
    errors when multiple tests run in batch. The issue is AsyncPG connection pool
    contention - multiple async operations trying to use the same connection
    simultaneously. Individual tests pass, batch tests fail.

    Current workaround: Use async_session fixture instead for non-rollback tests.
    Proper fix requires architectural changes to connection pooling strategy.
    """
    from contextlib import asynccontextmanager

    from services.database.session_factory import AsyncSessionFactory

    @asynccontextmanager
    async def _transaction_rollback_scope():
        """Context manager that automatically rolls back transactions"""
        session = await AsyncSessionFactory.create_session()
        try:
            # Use session.begin() context manager for proper transaction handling
            async with session.begin() as transaction:
                yield session
                # Transaction automatically rolls back on context exit
        except Exception:
            # Ensure session is closed even if transaction fails
            try:
                await session.close()
            except Exception:
                # Ignore close errors during cleanup
                pass
            raise
        finally:
            # Ensure session is always closed
            try:
                await session.close()
            except Exception:
                # Ignore close errors during cleanup
                pass

    # Return the context manager generator, not the function
    return _transaction_rollback_scope()


@pytest.fixture
async def clean_database():
    """Clean database state for tests that need fresh data.

    This fixture truncates all test-related tables to ensure clean state.
    Use this for tests that need guaranteed clean data.

    NOTE: This fixture should be used before other fixtures that create sessions
    to avoid connection pool conflicts.

    TODO PM-058: ASYNCPG CONCURRENCY ISSUE
    This fixture can cause connection pool contention when used with async_transaction
    fixture. Both fixtures try to create database sessions simultaneously, leading
    to "another operation is in progress" errors. Consider using manual cleanup
    or redesigning the session management approach.
    """
    import asyncio

    from sqlalchemy import text

    from services.database.connection import db

    # List of tables that commonly cause state issues in tests
    tables_to_clean = [
        "uploaded_files",
        "workflows",
        "tasks",
        "intents",
    ]

    async def clean_tables():
        """Clean tables using direct connection to avoid session conflicts"""
        # Use a completely separate connection from the pool
        session = await db.get_session()
        try:
            # Clean tables in dependency order (reverse foreign key order)
            for table in tables_to_clean:
                await session.execute(text(f"DELETE FROM {table}"))
            await session.commit()
        except Exception as e:
            # If cleanup fails, just roll back and continue
            await session.rollback()
            # Don't raise - cleanup failures shouldn't break tests
        finally:
            # Ensure session is closed immediately
            await session.close()
            # Give connection time to return to pool
            await asyncio.sleep(0.01)

    # Clean before test - use separate connection
    await clean_tables()

    yield

    # Clean after test - use separate connection
    await clean_tables()


# MCP Infrastructure Test Fixtures (PM-015 Group 2)
@pytest.fixture(scope="function", autouse=True)
async def mcp_infrastructure_reset():
    """
    Autouse fixture to reset MCP singletons and clean environment for every test.

    Addresses PM-015 Group 2 issues:
    - MCPConnectionPool singleton state leakage
    - Environment variable contamination
    - Mock setup inconsistencies

    This fixture ensures clean state between all tests that might use MCP.
    """
    import asyncio
    import logging
    import os

    # Store original environment variables
    original_env = {}
    mcp_env_vars = ["ENABLE_MCP_FILE_SEARCH", "USE_MCP_POOL", "MCP_SERVER_URL", "MCP_TIMEOUT"]

    for env_var in mcp_env_vars:
        if env_var in os.environ:
            original_env[env_var] = os.environ[env_var]

    # Don't reset singletons before test - let tests control their initial state
    # The autouse fixture only handles cleanup to prevent state leakage

    yield

    # Clean up after test with aggressive timeout to prevent hanging
    try:
        # Only try to reset MCP if the module exists and can be imported
        try:
            from services.infrastructure.mcp.connection_pool import MCPConnectionPool
        except ImportError:
            # MCP modules not available, skip cleanup
            pass
        else:
            # Disable logging during shutdown to prevent I/O errors
            original_level = logging.getLogger().level
            logging.getLogger().setLevel(logging.ERROR)

            try:
                pool = MCPConnectionPool.get_instance()

                # Use very short timeout to prevent hanging
                try:
                    await asyncio.wait_for(pool.shutdown(), timeout=0.1)
                except asyncio.TimeoutError:
                    # Force shutdown immediately if timeout occurs
                    pool._is_shutdown = True
                    pool._all_connections.clear()
                    pool._available_connections.clear()
                    pool._pool_lock = None

                MCPConnectionPool._reset_instance()
            except Exception:
                # Ignore any errors during MCP cleanup
                pass
            finally:
                # Restore logging level
                logging.getLogger().setLevel(original_level)

    except Exception:
        # Handle any other cleanup errors gracefully
        pass

    # Restore original environment variables
    for env_var in mcp_env_vars:
        if env_var in original_env:
            os.environ[env_var] = original_env[env_var]
        elif env_var in os.environ:
            del os.environ[env_var]


@pytest.fixture
async def mcp_disabled_env():
    """Fixture to disable MCP for tests that need it explicitly disabled."""
    import os

    with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "false", "USE_MCP_POOL": "false"}):
        yield


@pytest.fixture
async def mcp_enabled_env():
    """Fixture to enable MCP for tests that need it explicitly enabled."""
    import os

    with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "true", "USE_MCP_POOL": "true"}):
        yield


@pytest.fixture
async def mcp_connection_pool():
    """
    Provide a clean MCPConnectionPool instance for tests.

    Ensures proper initialization and cleanup of the connection pool
    without singleton state leakage between tests.
    """
    from services.infrastructure.mcp.connection_pool import MCPConnectionPool

    # Reset before creating instance
    MCPConnectionPool._reset_instance()
    pool = MCPConnectionPool.get_instance()

    yield pool

    # Clean shutdown after test
    try:
        await pool.shutdown()
    except Exception:
        pass  # Ignore shutdown errors
    finally:
        MCPConnectionPool._reset_instance()


@pytest.fixture
async def mcp_resource_manager():
    """
    Provide a clean MCPResourceManager instance for tests.

    Ensures proper initialization and cleanup without singleton issues.
    """
    from services.mcp.resources import MCPResourceManager

    manager = MCPResourceManager()

    yield manager

    # Clean up manager resources
    try:
        await manager.cleanup()
    except Exception:
        pass  # Ignore cleanup errors


@pytest.fixture
def mock_mcp_client():
    """
    Provide a mock MCP client for tests that need to avoid real MCP connections.

    This fixture handles all the common mocking patterns to avoid repetition
    in individual tests.
    """
    from unittest.mock import AsyncMock, Mock

    mock_client = AsyncMock()
    mock_client.connect.return_value = True
    mock_client.is_connected.return_value = True
    mock_client.disconnect = AsyncMock()
    mock_client.list_resources.return_value = []
    mock_client.get_resource.return_value = None
    mock_client.search_content.return_value = []

    return mock_client


@pytest.fixture(scope="function", autouse=True)
async def cleanup_sessions():
    """Clean up database sessions and engine after each test"""
    yield

    # Dispose of database engine to clean up connection pool
    try:
        from services.database.connection import db

        if db.engine:
            await db.engine.dispose()
    except Exception:
        pass  # Ignore disposal errors during cleanup
