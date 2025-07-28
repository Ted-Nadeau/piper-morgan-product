"""
Test Spatial Intent Integration
Tests the integration between spatial events and the enhanced IntentClassifier system.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent, IntentCategory
from services.integrations.slack.response_flow_integration import (
    ResponseContent,
    ResponseFlowIntegration,
    ResponseTarget,
)
from services.integrations.slack.spatial_types import SpatialCoordinates, SpatialEvent
from services.intent_service.classifier import IntentClassifier
from services.intent_service.spatial_intent_classifier import (
    SpatialIntentClassifier,
    SpatialIntentContext,
)


class TestSpatialIntentClassifier:
    """Test spatial intent classifier functionality"""

    def test_create_spatial_context_from_event(self):
        """Test creating spatial context from spatial event"""
        # Arrange
        classifier = SpatialIntentClassifier()
        coords = SpatialCoordinates(
            territory_id="T123456",
            room_id="C789012",
            path_id="1234567890.123456",
            object_id="1234567890.123457",
        )
        spatial_event = SpatialEvent(
            event_id="test_event",
            event_type="attention_attracted",
            coordinates=coords,
            actor_id="U123456",
        )
        navigation_intent = "respond"
        user_context = {"user_id": "U123456"}

        # Act
        spatial_context = classifier.create_spatial_context_from_event(
            spatial_event, navigation_intent, user_context
        )

        # Assert
        assert isinstance(spatial_context, SpatialIntentContext)
        assert spatial_context.room_id == "C789012"
        assert spatial_context.territory_id == "T123456"
        assert spatial_context.attention_level == "high"
        assert spatial_context.navigation_intent == "respond"
        assert spatial_context.user_context == user_context

    def test_create_intent_from_spatial_event(self):
        """Test creating intent from spatial event"""
        # Arrange
        classifier = SpatialIntentClassifier()
        coords = SpatialCoordinates(
            territory_id="T123456",
            room_id="C789012",
            path_id="1234567890.123456",
            object_id="1234567890.123457",
        )
        spatial_event = SpatialEvent(
            event_id="test_event",
            event_type="attention_attracted",
            coordinates=coords,
            actor_id="U123456",
            significance_level="significant",
        )
        navigation_intent = "respond"
        user_context = {"user_id": "U123456"}

        # Act
        intent = classifier.create_intent_from_spatial_event(
            spatial_event, navigation_intent, user_context
        )

        # Assert
        assert isinstance(intent, Intent)
        assert intent.category == IntentCategory.EXECUTION
        assert intent.action == "respond_to_mention"
        assert intent.confidence == 0.8  # significant level
        assert "spatial_context" in intent.context
        assert "response_target" in intent.context
        assert intent.context["response_target"]["channel_id"] == "C789012"
        assert intent.context["response_target"]["thread_ts"] == "1234567890.123456"

    def test_convert_spatial_context_to_dict(self):
        """Test converting spatial context to dictionary"""
        # Arrange
        classifier = SpatialIntentClassifier()
        spatial_context = SpatialIntentContext(
            room_id="C789012",
            territory_id="T123456",
            attention_level="high",
            emotional_valence="positive",
            navigation_intent="respond",
            spatial_coordinates={
                "territory_id": "T123456",
                "room_id": "C789012",
                "path_id": "1234567890.123456",
            },
            user_context={"user_id": "U123456"},
        )

        # Act
        context_dict = classifier.convert_spatial_context_to_dict(spatial_context)

        # Assert
        assert isinstance(context_dict, dict)
        assert context_dict["room_id"] == "C789012"
        assert context_dict["territory_id"] == "T123456"
        assert context_dict["attention_level"] == "high"
        assert context_dict["emotional_valence"] == "positive"
        assert context_dict["navigation_intent"] == "respond"


class TestEnhancedIntentClassifier:
    """Test enhanced IntentClassifier with spatial context"""

    @pytest.mark.asyncio
    async def test_classify_with_spatial_context(self):
        """Test IntentClassifier with spatial context"""
        # Arrange
        classifier = IntentClassifier()
        message = "Spatial event: attention_attracted"
        spatial_context = {
            "room_id": "C789012",
            "territory_id": "T123456",
            "attention_level": "high",
            "emotional_valence": "positive",
            "navigation_intent": "respond",
            "spatial_coordinates": {
                "territory_id": "T123456",
                "room_id": "C789012",
                "path_id": "1234567890.123456",
            },
        }

        # Mock LLM response
        mock_response = """{
            "category": "execution",
            "action": "respond_to_mention",
            "confidence": 0.9,
            "reasoning": "High attention spatial event requires immediate response",
            "helpful_knowledge_domains": ["spatial_context"],
            "ambiguity_notes": [],
            "knowledge_used": []
        }"""

        with patch.object(classifier.llm, "complete", return_value=mock_response):
            # Act
            intent = await classifier.classify(
                message=message,
                spatial_context=spatial_context,
            )

            # Assert
            assert isinstance(intent, Intent)
            assert intent.category == IntentCategory.EXECUTION
            assert intent.action == "respond_to_mention"
            assert intent.confidence == 0.9
            assert "spatial_context" in intent.context
            assert "response_target" in intent.context
            assert intent.context["response_target"]["channel_id"] == "C789012"


class TestResponseFlowIntegration:
    """Test response flow integration"""

    @pytest.mark.asyncio
    async def test_extract_response_target_from_spatial_context(self):
        """Test extracting response target from spatial context"""
        # Arrange
        config_service = MagicMock()
        response_flow = ResponseFlowIntegration(config_service)

        workflow = MagicMock()
        workflow.context = {
            "spatial_context": {
                "room_id": "C789012",
                "territory_id": "T123456",
                "spatial_coordinates": {
                    "path_id": "1234567890.123456",
                },
            },
        }

        # Act
        response_target = response_flow._extract_response_target(workflow)

        # Assert
        assert isinstance(response_target, ResponseTarget)
        assert response_target.channel_id == "C789012"
        assert response_target.thread_ts == "1234567890.123456"
        assert response_target.workspace_id == "T123456"

    @pytest.mark.asyncio
    async def test_generate_response_content_success(self):
        """Test generating response content for successful workflow"""
        # Arrange
        config_service = MagicMock()
        response_flow = ResponseFlowIntegration(config_service)

        workflow = MagicMock()
        workflow.context = {
            "spatial_context": {
                "attention_level": "high",
            },
        }

        workflow_result = MagicMock()
        workflow_result.success = True
        workflow_result.data = {
            "message": "Workflow completed successfully",
            "workflow_details": "Test workflow details",
            "task_results": [
                {"name": "Task 1", "status": "completed"},
                {"name": "Task 2", "status": "completed"},
            ],
        }
        workflow_result.error = None

        # Act
        response_content = response_flow._generate_response_content(workflow, workflow_result)

        # Assert
        assert isinstance(response_content, ResponseContent)
        assert "🔔" in response_content.text  # High attention indicator
        assert "Workflow completed successfully" in response_content.text
        assert "Task Summary:" in response_content.text
        assert "✅ Task 1" in response_content.text
        assert "✅ Task 2" in response_content.text

    @pytest.mark.asyncio
    async def test_generate_response_content_error(self):
        """Test generating response content for failed workflow"""
        # Arrange
        config_service = MagicMock()
        response_flow = ResponseFlowIntegration(config_service)

        workflow = MagicMock()
        workflow.context = {}

        workflow_result = MagicMock()
        workflow_result.success = False
        workflow_result.error = "Test error"
        workflow_result.data = {
            "recovery_suggestion": "Try again later",
        }

        # Act
        response_content = response_flow._generate_response_content(workflow, workflow_result)

        # Assert
        assert isinstance(response_content, ResponseContent)
        assert "❌" in response_content.text
        assert "Test error" in response_content.text
        assert "Try again later" in response_content.text


class TestSpatialWorkflowFactoryIntegration:
    """Test integration between spatial workflow factory and enhanced classifier"""

    @pytest.mark.asyncio
    async def test_workflow_creation_with_enhanced_classifier(self):
        """Test workflow creation using enhanced IntentClassifier"""
        # Arrange
        from services.integrations.slack.event_handler import EventProcessingResult
        from services.integrations.slack.slack_workflow_factory import SlackWorkflowFactory
        from services.integrations.slack.spatial_agent import NavigationDecision, NavigationIntent
        from services.orchestration.workflow_factory import WorkflowFactory

        workflow_factory = WorkflowFactory()
        intent_classifier = IntentClassifier()
        slack_workflow_factory = SlackWorkflowFactory(workflow_factory, intent_classifier)

        # Create mock spatial event
        coords = SpatialCoordinates(
            territory_id="T123456",
            room_id="C789012",
            path_id="1234567890.123456",
            object_id="1234567890.123457",
        )
        spatial_event = SpatialEvent(
            event_id="test_event",
            event_type="attention_attracted",
            coordinates=coords,
            actor_id="U123456",
            significance_level="significant",
        )

        event_result = EventProcessingResult(
            success=True,
            spatial_event=spatial_event,
            attention_level=MagicMock(value="high"),
            emotional_valence=MagicMock(value="positive"),
        )

        navigation_decision = NavigationDecision(
            intent=NavigationIntent.RESPOND,
            target_room="C789012",
            confidence=0.9,
            reasoning="High attention event",
        )

        spatial_context = MagicMock()
        spatial_context.room_id = "C789012"
        spatial_context.territory_id = "T123456"
        spatial_context.user_context = {"user_id": "U123456"}

        # Mock LLM response
        mock_response = """{
            "category": "execution",
            "action": "respond_to_mention",
            "confidence": 0.9,
            "reasoning": "High attention spatial event requires immediate response",
            "helpful_knowledge_domains": ["spatial_context"],
            "ambiguity_notes": [],
            "knowledge_used": []
        }"""

        with patch.object(intent_classifier.llm, "complete", return_value=mock_response):
            # Act
            workflow = await slack_workflow_factory.create_workflow_from_spatial_event(
                event_result, navigation_decision, spatial_context
            )

            # Assert
            assert workflow is not None
            assert "spatial_context" in workflow.context
            assert workflow.context["spatial_context"]["room_id"] == "C789012"
            assert workflow.context["spatial_context"]["attention_level"] == "high"
