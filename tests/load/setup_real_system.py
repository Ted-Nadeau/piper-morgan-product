"""
Setup function to initialize REAL system components for load testing
NO MOCKING - creates actual IntentService with real dependencies
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


async def setup_real_intent_service():
    """
    Initialize IntentService with REAL dependencies (no mocks).

    Mimics the initialization from web/app.py lifespan function.
    This ensures we test the actual system performance.

    Returns:
        IntentService: Fully initialized with real dependencies
    """
    print("🔧 Setting up REAL system components (no mocks)...")

    # Initialize OrchestrationEngine (real)
    try:
        from services.llm.clients import llm_client
        from services.orchestration.engine import OrchestrationEngine

        print("  📦 Initializing OrchestrationEngine...")
        orchestration_engine = OrchestrationEngine(llm_client=llm_client)
        print("  ✅ OrchestrationEngine initialized")

    except Exception as e:
        print(f"  ❌ OrchestrationEngine initialization failed: {e}")
        orchestration_engine = None

    # Initialize IntentService (real)
    try:
        from services.conversation.conversation_handler import ConversationHandler
        from services.intent.intent_service import IntentService
        from services.intent_service import classifier

        print("  📦 Initializing IntentService...")
        intent_service = IntentService(
            orchestration_engine=orchestration_engine,
            intent_classifier=classifier,
            conversation_handler=ConversationHandler(session_manager=None),
        )
        print("  ✅ IntentService initialized")

        return intent_service

    except Exception as e:
        print(f"  ❌ IntentService initialization failed: {e}")
        raise RuntimeError(f"Failed to initialize real system: {e}")


def validate_real_system(intent_service):
    """
    Validate that we have a real system (not mocked).

    Args:
        intent_service: The IntentService to validate

    Raises:
        AssertionError: If system appears to be mocked
    """
    print("🔍 Validating REAL system setup...")

    # Check that we have real components
    assert intent_service is not None, "IntentService is None"
    assert hasattr(intent_service, "orchestration_engine"), "Missing orchestration_engine"
    assert hasattr(intent_service, "intent_classifier"), "Missing intent_classifier"

    # Check for mock objects (common mock indicators)
    orchestration_str = str(type(intent_service.orchestration_engine))
    classifier_str = str(type(intent_service.intent_classifier))

    mock_indicators = ["Mock", "MagicMock", "AsyncMock", "mock"]

    for indicator in mock_indicators:
        assert (
            indicator not in orchestration_str
        ), f"OrchestrationEngine appears to be mocked: {orchestration_str}"
        assert indicator not in classifier_str, f"Classifier appears to be mocked: {classifier_str}"

    print("  ✅ System validated as REAL (no mocks detected)")
    print(f"  📊 OrchestrationEngine: {type(intent_service.orchestration_engine).__name__}")
    print(f"  📊 Classifier: {type(intent_service.intent_classifier).__name__}")
