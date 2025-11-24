from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent, IntentCategory
from services.intent_service.classifier import IntentClassifier


@pytest.fixture
def classifier():
    """Fixture to create an IntentClassifier with a mocked LLM client."""
    # Inject mocked LLM through constructor (llm is a read-only property)
    mock_llm = AsyncMock()
    mock_knowledge_graph = MagicMock()
    ingester_mock = MagicMock()
    ingester_mock.search_with_context = AsyncMock(return_value=[])
    mock_knowledge_graph.get_ingester = MagicMock(return_value=ingester_mock)

    classifier_instance = IntentClassifier(
        llm_service=mock_llm, knowledge_graph_service=mock_knowledge_graph
    )

    return classifier_instance


@pytest.mark.asyncio
async def test_classify_user_complaint_as_create_ticket(classifier):
    """
    Tests that a common user complaint is correctly classified as an
    EXECUTION intent with the 'create_ticket' action.
    """
    # Arrange
    user_message = "Users are complaining the login page is slow"

    # This is the expected JSON response from the LLM based on the improved prompt
    mock_llm_response = """
    {
        "category": "EXECUTION",
        "action": "create_ticket",
        "confidence": 0.9,
        "reasoning": "The user is reporting a problem that needs to be tracked and resolved, which maps to creating a ticket.",
        "knowledge_domains": ["bug_tracking", "user_support"],
        "ambiguity_notes": [],
        "knowledge_used": ["The prompt example for user complaints guided this classification."]
    }
    """

    classifier.llm.complete.return_value = mock_llm_response

    # Act
    result_intent = await classifier.classify(user_message)

    # Assert
    assert isinstance(result_intent, Intent)
    assert result_intent.category == IntentCategory.EXECUTION
    assert result_intent.action == "create_ticket"
    assert result_intent.confidence >= 0.7

    # Verify that the LLM was called correctly
    classifier.llm.complete.assert_called_once()
    call_args = classifier.llm.complete.call_args
    prompt = call_args.kwargs.get("prompt")
    assert user_message in prompt
