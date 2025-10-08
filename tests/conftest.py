"""
conftest.py — Minimal test infrastructure for Piper Morgan
"""

import os
import sys
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


# Basic fixtures that don't depend on services that may not exist
@pytest.fixture
def mock_session():
    """Provide a mock session for tests that need it"""
    return Mock()


@pytest.fixture
def mock_async_session():
    """Provide a mock async session for tests that need it"""
    return AsyncMock()


# GREAT-5 Phase 1.5: IntentService test fixtures
@pytest.fixture
async def intent_service():
    """
    Provide properly initialized IntentService for testing.

    This fixture ensures IntentService is available with all required dependencies:
    - OrchestrationEngine (None for tests)
    - Intent classifier
    - Conversation handler

    Created in GREAT-5 Phase 1.5 to fix initialization issues revealed by
    stricter test assertions in Phase 1.
    """
    from services.conversation.conversation_handler import ConversationHandler
    from services.intent.intent_service import IntentService
    from services.intent_service import classifier

    # Initialize IntentService with test configuration
    service = IntentService(
        orchestration_engine=None,  # Tests don't need real orchestration
        intent_classifier=classifier,
        conversation_handler=ConversationHandler(session_manager=None),
    )

    yield service

    # Cleanup if needed
    # await service.cleanup() if service has cleanup method


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
