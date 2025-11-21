"""
conftest.py — Minimal test infrastructure for Piper Morgan
"""

import asyncio
import os
import sys
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# ============================================================================
# UUID Test Fixtures (Issue #262 - UUID Migration)
# ============================================================================
# Reusable UUIDs for tests - use these instead of hardcoded strings
TEST_USER_ID = UUID("11111111-1111-1111-1111-111111111111")
TEST_USER_ID_2 = UUID("22222222-2222-2222-2222-222222222222")
TEST_SESSION_ID = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
TEST_WORKFLOW_ID = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")

# For xian's actual UUID from migration
XIAN_USER_ID = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")


# Session-scoped event loop for async integration tests (Issue #290)
# This ensures all tests in a session share the same event loop, preventing
# "Task attached to different loop" errors when database connections are reused
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the entire test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# Basic fixtures that don't depend on services that may not exist
@pytest.fixture
def mock_session():
    """Provide a mock session for tests that need it"""
    return Mock()


@pytest.fixture(autouse=True)
def mock_token_blacklist(request):
    """
    Auto-mock TokenBlacklist for unit tests to prevent database session conflicts.

    Investigation (2025-11-20 SLACK-SPATIAL Phase 1.2):
    Confirmed this auto-mock serves its purpose without hiding bugs. All auth tests
    use @pytest.mark.integration and bypass this mock. See investigation report:
    dev/2025/11/20/token-blacklist-investigation-results.md

    WHY THIS EXISTS:
    Issue #281: TokenBlacklist.is_blacklisted() gets async context manager from
    overridden db.get_session() in tests, causing '_AsyncGeneratorContextManager'
    has no attribute 'execute' errors in unit tests that don't properly configure
    database session mocks.

    WHAT IT DOES:
    - Automatically mocks is_blacklisted() to return False for unit tests
    - Allows unit tests to run without complex database session setup
    - Does NOT affect integration tests (they bypass this mock)

    WHEN IT APPLIES:
    - Unit tests (no @pytest.mark.integration marker)
    - Tests that indirectly call TokenBlacklist through JWT validation

    WHEN IT DOESN'T APPLY:
    - Integration tests (marked with @pytest.mark.integration)
    - Tests in tests/unit/services/auth/ (all use integration marker)

    TO DISABLE FOR INVESTIGATION:
    Change autouse=True to autouse=False and run your tests. Remember to re-enable
    after investigation to maintain unit test stability.

    Related Issues: #281 (original issue), #292 (integration test behavior)
    Investigation: piper-morgan-otf (SLACK-SPATIAL Phase 1.2)
    """
    from unittest.mock import AsyncMock, patch

    # Skip mock for integration tests - they use real database
    if "integration" in request.keywords:
        yield
        return

    # Import the module first to ensure it exists before patching
    # This avoids "module has no attribute" errors during patch()
    try:
        from services.auth import token_blacklist  # noqa: F401
    except ImportError:
        # If module doesn't exist, skip the mock
        yield
        return

    # Patch the service class at its module definition location
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


@pytest_asyncio.fixture
async def initialized_container():
    """
    Initialize ServiceContainer with LLM service for tests that need container setup.

    This fixture provides a minimal container initialization for tests that directly
    instantiate IntentClassifier or LLMIntentClassifier without going through IntentService.

    Created to fix piper-morgan-8oz and piper-morgan-ss0 (container initialization bugs).

    Usage:
        @pytest.mark.asyncio
        async def test_classifier(initialized_container):
            classifier = IntentClassifier()  # Now works - container is initialized
            intent = await classifier.classify("message")
    """
    from services.container import ServiceContainer
    from services.domain.llm_domain_service import LLMDomainService

    # Initialize LLM domain service
    llm_domain_service = LLMDomainService()
    await llm_domain_service.initialize()

    # Get container instance and register LLM service
    container = ServiceContainer()
    container._registry.register("llm", llm_domain_service)
    container._initialized = True

    yield container

    # Cleanup: Reset container for next test
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
