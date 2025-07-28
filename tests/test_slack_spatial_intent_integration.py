"""
Test Slack Spatial Intelligence to Intent Classification Integration
Verifies PM-078 implementation - spatial context flows through intent classification
"""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.domain.models import Intent
from services.integrations.slack.event_handler import EventProcessingResult
from services.integrations.slack.slack_workflow_factory import (
    SlackWorkflowFactory,
    SpatialWorkflowContext,
)
from services.integrations.slack.spatial_agent import NavigationDecision, NavigationIntent
from services.integrations.slack.spatial_types import (
    AttentionLevel,
    EmotionalValence,
    SpatialCoordinates,
    SpatialEvent,
)
from services.intent_service.classifier import IntentClassifier
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import IntentCategory, WorkflowType


@pytest.mark.asyncio
async def test_spatial_event_uses_enhanced_intent_classifier():
    """Test that spatial events flow through the enhanced IntentClassifier"""
    # Setup
    workflow_factory = Mock(spec=WorkflowFactory)
    intent_classifier = AsyncMock(spec=IntentClassifier)
    slack_workflow_factory = SlackWorkflowFactory(workflow_factory, intent_classifier)

    # Create test spatial event
    spatial_event = SpatialEvent(
        event_id="evt123",
        event_type="attention_attracted",
        coordinates=SpatialCoordinates(
            room_id="C123456",
            territory_id="T789012",
            path_id="thread456",
            object_position=1,
        ),
        event_time=datetime.now(),
    )

    # Create event result with @mention message
    event_result = EventProcessingResult(
        success=True,
        spatial_event=spatial_event,
        attention_level=AttentionLevel.DIRECT,
    )

    # Create navigation decision
    navigation_decision = NavigationDecision(
        intent=NavigationIntent.RESPOND,
        target_room="C123456",
        confidence=0.9,
        reasoning="Direct mention requires response",
        urgency=0.8,
    )

    # Create spatial context
    spatial_context = SpatialWorkflowContext(
        room_id="C123456",
        territory_id="T789012",
        spatial_event_type="attention_attracted",
        attention_level="direct",
        emotional_valence="neutral",
        navigation_intent="respond",
        spatial_coordinates={"path_id": "thread456"},
        user_context={"user_id": "U123456", "username": "test_user"},
    )

    # Mock the classify response
    expected_intent = Intent(
        category=IntentCategory.QUERY,
        action="get_status",
        confidence=0.9,
        context={
            "original_message": "Spatial event: attention_attracted",
            "spatial_context": {
                "room_id": "C123456",
                "territory_id": "T789012",
                "path_id": "thread456",
                "spatial_event_type": "attention_attracted",
                "navigation_intent": "respond",
            },
            "response_target": {
                "channel_id": "C123456",
                "thread_ts": "thread456",
                "workspace_id": "T789012",
            },
        },
    )
    intent_classifier.classify.return_value = expected_intent

    # Execute
    await slack_workflow_factory.create_workflow_from_spatial_event(
        event_result, navigation_decision, spatial_context
    )

    # Verify IntentClassifier was called with spatial context
    intent_classifier.classify.assert_called_once()
    call_args = intent_classifier.classify.call_args

    # Check message - could be positional or keyword arg
    if call_args.args:
        assert call_args.args[0] == "Spatial event: attention_attracted"
    else:
        assert call_args.kwargs.get("message") == "Spatial event: attention_attracted"

    # Check spatial context was passed
    spatial_context_arg = call_args.kwargs.get("spatial_context")
    assert spatial_context_arg is not None
    assert spatial_context_arg["room_id"] == "C123456"
    assert spatial_context_arg["territory_id"] == "T789012"
    assert spatial_context_arg["navigation_intent"] == "respond"
    # Check spatial coordinates sub-dict contains path_id and object_position
    assert "spatial_coordinates" in spatial_context_arg
    coords = spatial_context_arg["spatial_coordinates"]
    assert coords["path_id"] == "thread456"
    assert coords["object_position"] == 1
    assert coords["room_id"] == "C123456"
    assert coords["territory_id"] == "T789012"


@pytest.mark.asyncio
async def test_intent_includes_response_targeting():
    """Test that classified intent includes response targeting information"""
    # Setup
    workflow_factory = Mock(spec=WorkflowFactory)
    intent_classifier = IntentClassifier()
    slack_workflow_factory = SlackWorkflowFactory(workflow_factory, intent_classifier)

    # Mock LLM response
    with patch.object(intent_classifier.llm, "complete") as mock_llm:
        mock_llm.return_value = """{
            "category": "query",
            "action": "get_status",
            "confidence": 0.9,
            "reasoning": "User asking for project status in Slack channel",
            "helpful_knowledge_domains": ["project_management"],
            "ambiguity_notes": [],
            "knowledge_used": []
        }"""

        # Create spatial context
        spatial_context_dict = {
            "room_id": "C123456",
            "territory_id": "T789012",
            "path_id": "thread789",
            "attention_level": "high",
            "spatial_event_type": "attention_attracted",
        }

        # Classify with spatial context
        intent = await intent_classifier.classify(
            message="@piper what's the status?",
            context={"user": "test_user"},
            spatial_context=spatial_context_dict,
        )

        # Verify intent has response targeting
        assert intent.category == IntentCategory.QUERY
        assert intent.action == "get_status"
        assert "response_target" in intent.context
        assert intent.context["response_target"]["channel_id"] == "C123456"
        assert intent.context["response_target"]["thread_ts"] == "thread789"
        assert intent.context["response_target"]["workspace_id"] == "T789012"


@pytest.mark.asyncio
async def test_spatial_context_influences_classification():
    """Test that spatial context influences intent classification"""
    intent_classifier = IntentClassifier()

    # Mock LLM to return different results based on spatial context
    with patch.object(intent_classifier.llm, "complete") as mock_llm:

        async def llm_response(task_type, prompt, context):
            # Check if spatial context indicates high urgency
            if "High attention" in prompt and "urgent" in prompt.lower():
                return """{
                    "category": "execution",
                    "action": "create_urgent_task",
                    "confidence": 0.95,
                    "reasoning": "High attention mention indicates urgent task creation needed",
                    "helpful_knowledge_domains": ["task_management"],
                    "ambiguity_notes": [],
                    "knowledge_used": []
                }"""
            else:
                return """{
                    "category": "query",
                    "action": "list_items",
                    "confidence": 0.7,
                    "reasoning": "General query about items",
                    "helpful_knowledge_domains": ["general"],
                    "ambiguity_notes": [],
                    "knowledge_used": []
                }"""

        mock_llm.side_effect = llm_response

        # Test with high attention spatial context
        spatial_context_high = {
            "room_id": "C123456",
            "attention_level": "high",
            "spatial_event_type": "attention_attracted",
            "navigation_intent": "respond",
        }

        intent_high = await intent_classifier.classify(
            message="need this urgently",
            spatial_context=spatial_context_high,
        )

        assert intent_high.category == IntentCategory.EXECUTION
        assert intent_high.action == "create_urgent_task"
        assert intent_high.confidence == 0.95

        # Test without spatial context
        intent_low = await intent_classifier.classify(
            message="need this urgently",
            spatial_context=None,
        )

        assert intent_low.category == IntentCategory.QUERY
        assert intent_low.action == "list_items"
        assert intent_low.confidence == 0.7


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
