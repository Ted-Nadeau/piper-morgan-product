"""
conftest.py — Minimal test infrastructure for Piper Morgan
"""

import os
import sys
from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


# Basic fixtures that don't depend on services that may not exist
@pytest.fixture
def mock_session():
    """Provide a mock session for tests that need it"""
    return Mock()


@pytest.fixture(autouse=True)
def mock_token_blacklist():
    """
    Auto-mock TokenBlacklist for all tests to prevent database session conflicts.

    Issue #281: TokenBlacklist.is_blacklisted() gets async context manager from
    overridden db.get_session() in tests, causing '_AsyncGeneratorContextManager'
    has no attribute 'execute' errors.

    Solution: Mock is_blacklisted to return False (token not blacklisted) for all tests.
    Individual tests can override this if they need to test blacklist behavior.
    """
    from unittest.mock import AsyncMock, patch

    with patch(
        "services.auth.token_blacklist.TokenBlacklist.is_blacklisted",
        new=AsyncMock(return_value=False),
    ):
        yield


@pytest.fixture
def mock_async_session():
    """Provide a mock async session for tests that need it"""
    return AsyncMock()


# GREAT-5 Phase 1.5: IntentService test fixtures
# Updated in #212 Phase 0 to add ServiceRegistry initialization (required after #217 refactoring)
@pytest.fixture
async def intent_service():
    """
    Provide properly initialized IntentService for testing.

    This fixture ensures IntentService is available with all required dependencies:
    - ServiceRegistry with LLM service (#217 refactoring requirement)
    - OrchestrationEngine (None for tests)
    - Intent classifier
    - Conversation handler

    Created in GREAT-5 Phase 1.5 to fix initialization issues revealed by
    stricter test assertions in Phase 1.
    Updated in #212 Phase 0 for #217 ServiceRegistry pattern.
    """
    import sys

    from services.container import ServiceContainer
    from services.container.service_registry import ServiceRegistry
    from services.conversation.conversation_handler import ConversationHandler
    from services.domain.llm_domain_service import LLMDomainService
    from services.intent.intent_service import IntentService
    from services.intent_service import classifier

    print("[FIXTURE DEBUG] Starting fixture setup", file=sys.stderr)

    # Initialize ServiceRegistry with LLM domain service (Phase 1.6: Updated to use container pattern)
    llm_domain_service = LLMDomainService()
    await llm_domain_service.initialize()  # Must initialize before use

    # Get container instance and access internal registry for test setup
    container = ServiceContainer()
    print(
        f"[FIXTURE DEBUG] Before register. Registry: {list(container._registry._services.keys())}",
        file=sys.stderr,
    )
    container._registry.register("llm", llm_domain_service)
    container._initialized = True  # Mark as initialized for tests
    print(
        f"[FIXTURE DEBUG] After register. Registry: {list(container._registry._services.keys())}",
        file=sys.stderr,
    )

    # Initialize IntentService with test configuration
    service = IntentService(
        orchestration_engine=None,  # Tests don't need real orchestration
        intent_classifier=classifier,
        conversation_handler=ConversationHandler(session_manager=None),
    )

    yield service

    # Cleanup: Reset classifier's cached LLM and ServiceContainer (Phase 1.6)
    # The classifier singleton caches the LLM reference, which becomes stale
    # when we clear the container. Must reset it for next test.
    classifier._llm = None
    ServiceContainer.reset()


@pytest.fixture
def client_with_intent():
    """
    FastAPI TestClient with IntentService properly initialized in app.state.

    This ensures tests using the web API have access to a working IntentService,
    preventing "IntentService not available - initialization failed" errors.

    Created in GREAT-5 Phase 1.5.
    """
    from fastapi.testclient import TestClient

    from services.conversation.conversation_handler import ConversationHandler
    from services.intent.intent_service import IntentService
    from services.intent_service import classifier
    from web.app import app

    # Ensure IntentService is initialized in app.state
    if not hasattr(app.state, "intent_service") or app.state.intent_service is None:
        app.state.intent_service = IntentService(
            orchestration_engine=None,
            intent_classifier=classifier,
            conversation_handler=ConversationHandler(session_manager=None),
        )

    client = TestClient(app)
    return client


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    """
    Create fresh async database engine per test.

    Using function scope ensures each test gets a new engine in a fresh event loop,
    avoiding "Future attached to different loop" errors when tests run together.

    Issue #281: Fix async test isolation
    """
    from services.database.connection import db

    # Initialize global db connection if not already done
    if not db._initialized:
        await db.initialize()

    # Build database URL (same as db.initialize() does)
    db_url = db._build_database_url()

    # Create fresh engine for this test
    engine = create_async_engine(
        db_url,
        echo=False,  # Reduce log noise in tests
        pool_pre_ping=True,  # Verify connections are alive
        pool_recycle=3600,
    )

    yield engine

    # Proper cleanup: dispose engine and its connection pool
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    """
    Create fresh async database session per test.

    Each test gets a new session from a new engine, ensuring proper event loop isolation.
    The session is automatically cleaned up by the context manager.

    Issue #281: Fix async test isolation
    """
    # Create fresh sessionmaker for this test
    async_session_factory = async_sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False,  # Allow access to objects after commit
    )

    # Create session and yield it
    async with async_session_factory() as session:
        yield session
        # Session cleanup happens automatically via context manager
