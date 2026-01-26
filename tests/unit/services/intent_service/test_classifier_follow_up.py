"""
Tests for conversational follow-up detection in classify_conscious (#427 MUX-IMPLEMENT-CONVERSE-MODEL)

Verifies:
- Follow-up detection integration
- Context inheritance for temporal shifts
- Conversation context tracking
- Session-based context isolation
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent_service.classifier import IntentClassifier
from services.intent_service.conversation_context import (
    ConversationContext,
    clear_context,
    get_or_create_context,
)
from services.intent_service.intent_types import IntentCategory, IntentUnderstanding


@pytest.fixture
def classifier():
    """Create a classifier with mocked LLM."""
    with patch("services.intent_service.classifier.get_ingester"):
        return IntentClassifier(llm_service=None)


@pytest.fixture
def session_id():
    """Generate a unique session ID for test isolation."""
    return str(uuid4())


@pytest.fixture(autouse=True)
def clear_session_contexts(session_id):
    """Clear conversation context before and after each test."""
    clear_context(session_id)
    yield
    clear_context(session_id)


class TestFollowUpIntegration:
    """Tests for follow-up detection integration in classify_conscious."""

    @pytest.mark.asyncio
    async def test_temporal_shift_inherits_intent(self, classifier, session_id):
        """'How about today?' should inherit calendar intent from previous turn."""
        # Set up previous turn with calendar query
        context = get_or_create_context(session_id)
        previous_intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"temporal_reference": "tomorrow"},
        )
        context.add_turn(
            message="What's on my calendar tomorrow?",
            intent=previous_intent,
            temporal_reference="tomorrow",
        )

        # Now ask follow-up
        with patch.object(classifier, "classify", new_callable=AsyncMock) as mock_classify:
            mock_classify.return_value = Intent(
                category=IntentCategory.CONVERSATION,
                action="unknown",
                confidence=0.3,
            )

            result = await classifier.classify_conscious(
                message="How about today?",
                context={"session_id": session_id},
            )

            # Should NOT call classify - follow-up should be resolved directly
            mock_classify.assert_not_called()

            # Result should inherit from previous intent
            assert result.intent is not None
            assert result.intent.category == IntentCategory.QUERY
            assert result.intent.action == "meeting_time"
            assert result.intent.context.get("temporal_reference") == "today"

    @pytest.mark.asyncio
    async def test_confirmation_detected(self, classifier, session_id):
        """'Yes' should be detected as confirmation."""
        # Set up previous turn
        context = get_or_create_context(session_id)
        previous_intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
        )
        context.add_turn(
            message="What's on my calendar?",
            intent=previous_intent,
        )

        with patch.object(classifier, "classify", new_callable=AsyncMock) as mock_classify:
            result = await classifier.classify_conscious(
                message="Yes",
                context={"session_id": session_id},
            )

            # Follow-up resolved without LLM
            mock_classify.assert_not_called()
            assert result.intent.action == "confirmation"

    @pytest.mark.asyncio
    async def test_continuation_detected(self, classifier, session_id):
        """'What else?' should be detected as continuation."""
        # Set up previous turn
        context = get_or_create_context(session_id)
        previous_intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
        )
        context.add_turn(
            message="What's on my calendar?",
            intent=previous_intent,
        )

        with patch.object(classifier, "classify", new_callable=AsyncMock) as mock_classify:
            result = await classifier.classify_conscious(
                message="What else?",
                context={"session_id": session_id},
            )

            mock_classify.assert_not_called()
            assert result.intent.action == "continue_previous"

    @pytest.mark.asyncio
    async def test_new_query_not_detected_as_follow_up(self, classifier, session_id):
        """New queries should not be detected as follow-ups."""
        # Set up previous turn
        context = get_or_create_context(session_id)
        previous_intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
        )
        context.add_turn(
            message="What's on my calendar?",
            intent=previous_intent,
        )

        with patch.object(classifier, "classify", new_callable=AsyncMock) as mock_classify:
            new_intent = Intent(
                category=IntentCategory.QUERY,
                action="list_projects",
                confidence=0.9,
            )
            mock_classify.return_value = new_intent

            result = await classifier.classify_conscious(
                message="What projects am I working on?",
                context={"session_id": session_id},
            )

            # Should call classify for new query
            mock_classify.assert_called_once()
            assert result.intent.action == "list_projects"

    @pytest.mark.asyncio
    async def test_no_context_uses_classify(self, classifier, session_id):
        """Without active context, should fall through to classify."""
        # Empty context (no previous turns)
        with patch.object(classifier, "classify", new_callable=AsyncMock) as mock_classify:
            mock_classify.return_value = Intent(
                category=IntentCategory.TEMPORAL,
                action="agenda_query",
                confidence=0.9,
            )

            result = await classifier.classify_conscious(
                message="How about today?",
                context={"session_id": session_id},
            )

            # Should call classify since no active context
            mock_classify.assert_called_once()
            assert result.intent.action == "agenda_query"


class TestConversationContextTracking:
    """Tests for conversation context tracking in classify_conscious."""

    @pytest.mark.asyncio
    async def test_turn_added_after_classification(self, classifier, session_id):
        """Each classification should add a turn to context."""
        with patch.object(classifier, "classify", new_callable=AsyncMock) as mock_classify:
            mock_classify.return_value = Intent(
                category=IntentCategory.QUERY,
                action="meeting_time",
                confidence=0.9,
            )

            await classifier.classify_conscious(
                message="What's on my calendar tomorrow?",
                context={"session_id": session_id},
            )

            context = get_or_create_context(session_id)
            assert len(context.turns) == 1
            assert context.turns[0].message == "What's on my calendar tomorrow?"
            assert context.turns[0].temporal_reference == "tomorrow"
            assert context.turns[0].intent.action == "meeting_time"

    @pytest.mark.asyncio
    async def test_context_attached_to_classification_context(self, classifier, session_id):
        """ConversationContext should be attached to IntentClassificationContext."""
        with patch.object(classifier, "classify", new_callable=AsyncMock) as mock_classify:
            mock_classify.return_value = Intent(
                category=IntentCategory.QUERY,
                action="test",
                confidence=0.9,
            )

            # The transform method receives classification_context with conversation_context
            with patch.object(classifier.personality_bridge, "transform") as mock_transform:
                mock_transform.return_value = MagicMock(spec=IntentUnderstanding)

                await classifier.classify_conscious(
                    message="Hello",
                    context={"session_id": session_id},
                )

                # Verify conversation_context was attached
                call_kwargs = mock_transform.call_args
                classification_context = call_kwargs.kwargs.get("context") or call_kwargs.args[1]
                assert classification_context.conversation_context is not None

    @pytest.mark.asyncio
    async def test_session_isolation(self, classifier):
        """Different sessions should have isolated conversation contexts."""
        session_1 = str(uuid4())
        session_2 = str(uuid4())

        with patch.object(classifier, "classify", new_callable=AsyncMock) as mock_classify:
            mock_classify.return_value = Intent(
                category=IntentCategory.QUERY,
                action="test",
                confidence=0.9,
            )

            # Add turn to session 1
            await classifier.classify_conscious(
                message="Hello from session 1",
                context={"session_id": session_1},
            )

            # Add turn to session 2
            await classifier.classify_conscious(
                message="Hello from session 2",
                context={"session_id": session_2},
            )

            # Verify isolation
            context_1 = get_or_create_context(session_1)
            context_2 = get_or_create_context(session_2)

            assert len(context_1.turns) == 1
            assert len(context_2.turns) == 1
            assert context_1.turns[0].message == "Hello from session 1"
            assert context_2.turns[0].message == "Hello from session 2"

        # Cleanup
        clear_context(session_1)
        clear_context(session_2)


class TestTemporalReferenceTracking:
    """Tests for temporal reference extraction and inheritance."""

    @pytest.mark.asyncio
    async def test_extracts_temporal_reference(self, classifier, session_id):
        """Should extract temporal reference from message."""
        with patch.object(classifier, "classify", new_callable=AsyncMock) as mock_classify:
            mock_classify.return_value = Intent(
                category=IntentCategory.QUERY,
                action="meeting_time",
                confidence=0.9,
            )

            await classifier.classify_conscious(
                message="What's happening this week?",
                context={"session_id": session_id},
            )

            context = get_or_create_context(session_id)
            assert context.turns[0].temporal_reference == "this_week"

    @pytest.mark.asyncio
    async def test_inherits_temporal_with_shift(self, classifier, session_id):
        """'What about Monday?' should inherit intent with new temporal."""
        context = get_or_create_context(session_id)
        context.add_turn(
            message="What's on my calendar tomorrow?",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="meeting_time",
                context={"temporal_reference": "tomorrow"},
            ),
            temporal_reference="tomorrow",
        )

        with patch.object(classifier, "classify", new_callable=AsyncMock) as mock_classify:
            result = await classifier.classify_conscious(
                message="What about Monday?",
                context={"session_id": session_id},
            )

            mock_classify.assert_not_called()
            assert result.intent.context.get("temporal_reference") == "monday"


class TestFollowUpWithoutPreviousIntent:
    """Tests for follow-up handling when previous turn has no intent."""

    @pytest.mark.asyncio
    async def test_falls_back_to_classify_without_previous_intent(self, classifier, session_id):
        """If previous turn has no intent, should fall through to classify."""
        context = get_or_create_context(session_id)
        # Add turn without intent
        context.add_turn(message="Hello")

        with patch.object(classifier, "classify", new_callable=AsyncMock) as mock_classify:
            mock_classify.return_value = Intent(
                category=IntentCategory.TEMPORAL,
                action="agenda_query",
                confidence=0.9,
            )

            result = await classifier.classify_conscious(
                message="How about today?",
                context={"session_id": session_id},
            )

            # resolve_follow_up returns None without previous intent
            # So should fall through to classify
            mock_classify.assert_called_once()


class TestTopicExtraction:
    """Tests for topic extraction during classification."""

    @pytest.mark.asyncio
    async def test_extracts_topic_from_intent_action(self, classifier, session_id):
        """Should extract topic from intent action."""
        with patch.object(classifier, "classify", new_callable=AsyncMock) as mock_classify:
            mock_classify.return_value = Intent(
                category=IntentCategory.QUERY,
                action="meeting_time",
                confidence=0.9,
            )

            await classifier.classify_conscious(
                message="What meetings do I have?",
                context={"session_id": session_id},
            )

            context = get_or_create_context(session_id)
            assert context.turns[0].topic == "meeting_time"
