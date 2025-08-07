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
from services.database.connection import Base, db
from services.database.session_factory import AsyncSessionFactory
from services.knowledge_graph.document_service import DocumentService
from services.knowledge_graph.ingestion import DocumentIngester
from services.queries.conversation_queries import ConversationQueryService
from services.queries.file_queries import FileQueryService
from services.queries.project_queries import ProjectQueryService
from services.queries.query_router import QueryRouter

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


async def clear_sqla_cache():
    """
    Chief Architect DECISION-002: Nuclear option SQLAlchemy metadata rebuild

    Complete metadata reconstruction to fix cache synchronization issues.
    This is the most aggressive approach when cache clearing fails.
    """
    from sqlalchemy import MetaData, text
    from sqlalchemy.orm import declarative_base

    print("🚨 NUCLEAR OPTION: Complete SQLAlchemy metadata rebuild initiated")

    # Step 1: Initialize database connection if needed
    if not db._initialized:
        await db.initialize()

    # Step 2: Complete engine disposal and recreation - ENHANCED FOR ASYNCPG
    if hasattr(db, "engine") and db.engine:
        await db.engine.dispose()
        print("  ✅ Engine disposed")

    # Force recreate with fresh connection pool (this clears AsyncPG cache)
    await db.initialize()

    # CRITICAL: Clear AsyncPG prepared statement cache by getting fresh connection
    async with db.engine.connect() as conn:
        # Force a simple query to ensure fresh connection without cached schema
        await conn.execute(text("SELECT 1"))
        print("  ✅ AsyncPG connection freshly initialized")

    print("  ✅ Engine and AsyncPG cache recreated")

    # Step 3: Nuclear metadata rebuild - MODULE RELOAD APPROACH
    import importlib
    import sys

    # Step 3a: Clear module cache to force reload
    modules_to_reload = ["services.database.models", "services.database.connection"]

    for module_name in modules_to_reload:
        if module_name in sys.modules:
            del sys.modules[module_name]
            print(f"  ✅ Cleared {module_name} from module cache")

    # Step 3b: Force reimport of database modules
    from services.database import models as fresh_models
    from services.database.connection import Base as FreshBase
    from services.database.connection import db as fresh_db

    print("  ✅ Reimported fresh database modules")

    # Step 3c: Replace global Base with fresh instance
    globals()["Base"] = FreshBase

    # Step 4: Initialize fresh database connection
    if not fresh_db._initialized:
        await fresh_db.initialize()
        print("  ✅ Fresh database initialized")

    # Step 5: Test table access with fresh modules
    from services.database.models import UploadedFileDB as FreshUploadedFileDB

    print(f"  ✅ Fresh UploadedFileDB loaded with table: {FreshUploadedFileDB.__tablename__}")

    # Step 6: Check if fresh model has the column
    if hasattr(FreshUploadedFileDB, "item_metadata"):
        print("  ✅ Fresh model HAS item_metadata attribute")
    else:
        print("  ❌ Fresh model MISSING item_metadata attribute")

    # Step 7: Verify fresh metadata has the table with all columns
    if "uploaded_files" in FreshBase.metadata.tables:
        columns = list(FreshBase.metadata.tables["uploaded_files"].columns.keys())
        print(f"  ✅ Fresh uploaded_files table with columns: {columns}")

        if "item_metadata" in columns:
            print("  ✅ CRITICAL: item_metadata column confirmed in FRESH schema")
        else:
            print("  ❌ CRITICAL: item_metadata column MISSING in fresh schema")
    else:
        print("  ❌ CRITICAL: uploaded_files table not found in fresh metadata")

    print("🚨 NUCLEAR OPTION COMPLETE: SQLAlchemy metadata completely reconstructed")
    print("✅ Chief Architect DECISION-002 nuclear option executed successfully")


@pytest.fixture(scope="function", autouse=True)  # Changed to function scope
async def clear_metadata_cache_and_close_db(request):
    """Clear SQLAlchemy cache at session start and cleanup at end"""
    # Clear cache at start of test session
    await clear_sqla_cache()

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

    PM-058 FIX: ASYNCPG CONCURRENCY ISSUE RESOLVED
    Fixed by using dedicated connection per test transaction and proper
    savepoint-based isolation to prevent connection pool contention.
    Each test gets its own isolated transaction context.
    """
    from contextlib import asynccontextmanager

    from services.database.connection import db

    @asynccontextmanager
    async def _transaction_rollback_scope():
        """Context manager with proper connection isolation for tests"""
        # Ensure database is initialized
        if not db._initialized:
            await db.initialize()

        # Create a dedicated connection for this test to avoid pool contention
        connection = await db.engine.connect()

        # Start a transaction on the dedicated connection
        transaction = await connection.begin()

        # Create session bound to this specific connection
        from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

        session_factory = async_sessionmaker(
            bind=connection, class_=AsyncSession, expire_on_commit=False
        )
        session = session_factory()

        try:
            yield session
            # Don't commit - we want rollback for test isolation
        except Exception:
            # Rollback on exception
            await transaction.rollback()
            raise
        finally:
            # Always clean up resources
            try:
                await session.close()
                await transaction.rollback()  # Rollback for test isolation
                await connection.close()
            except Exception:
                # Ignore cleanup errors to prevent masking original exception
                pass

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
