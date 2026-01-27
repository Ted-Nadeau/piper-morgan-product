"""
Tests for grammar-conscious intent types.

Issue #619: GRAMMAR-TRANSFORM: Intent Classification
Phase 1: Foundation dataclasses
"""

from datetime import datetime

import pytest

from services.domain.models import Intent
from services.intent_service.intent_types import IntentClassificationContext, IntentUnderstanding
from services.shared_types import IntentCategory, InteractionSpace, PerceptionMode


class TestInteractionSpace:
    """Test InteractionSpace enum."""

    def test_all_spaces_defined(self):
        """All expected InteractionSpace types exist."""
        assert InteractionSpace.SLACK_DM == "slack_dm"
        assert InteractionSpace.SLACK_CHANNEL == "slack_channel"
        assert InteractionSpace.WEB_CHAT == "web_chat"
        assert InteractionSpace.CLI == "cli"
        assert InteractionSpace.API == "api"
        assert InteractionSpace.UNKNOWN == "unknown"

    def test_is_string_enum(self):
        """InteractionSpace is a string enum for easy serialization."""
        assert isinstance(InteractionSpace.SLACK_DM, str)
        assert InteractionSpace.SLACK_DM == "slack_dm"


class TestPerceptionMode:
    """Test PerceptionMode enum."""

    def test_all_modes_defined(self):
        """All perception modes exist."""
        assert PerceptionMode.NOTICING == "noticing"
        assert PerceptionMode.REMEMBERING == "remembering"
        assert PerceptionMode.ANTICIPATING == "anticipating"

    def test_is_string_enum(self):
        """PerceptionMode is a string enum."""
        assert isinstance(PerceptionMode.NOTICING, str)


class TestIntentClassificationContext:
    """Test IntentClassificationContext dataclass."""

    def test_basic_creation(self):
        """Can create with just a message."""
        ctx = IntentClassificationContext(message="add a todo")
        assert ctx.message == "add a todo"
        assert ctx.place == InteractionSpace.UNKNOWN
        assert ctx.user_id is None

    def test_full_creation(self):
        """Can create with all fields."""
        ctx = IntentClassificationContext(
            message="add a todo",
            user_id="user-123",
            session_id="session-456",
            place=InteractionSpace.SLACK_DM,
            spatial_context={"channel": "D123"},
            conversation_history=["hello", "hi there"],
            user_preferences={"brevity": "concise"},
        )
        assert ctx.user_id == "user-123"
        assert ctx.place == InteractionSpace.SLACK_DM
        assert len(ctx.conversation_history) == 2
        assert ctx.user_preferences["brevity"] == "concise"

    def test_timestamp_defaults_to_now(self):
        """Timestamp defaults to current time."""
        before = datetime.now()
        ctx = IntentClassificationContext(message="test")
        after = datetime.now()
        assert before <= ctx.timestamp <= after

    def test_from_classify_args_basic(self):
        """Factory method builds from minimal args."""
        ctx = IntentClassificationContext.from_classify_args(
            message="find documents",
        )
        assert ctx.message == "find documents"
        assert ctx.place == InteractionSpace.UNKNOWN
        assert ctx.user_id is None

    def test_from_classify_args_with_context(self):
        """Factory method extracts from context dict."""
        ctx = IntentClassificationContext.from_classify_args(
            message="find documents",
            context={"user_id": "u1", "session_id": "s1"},
            spatial_context={"channel": "C123"},
            place=InteractionSpace.SLACK_CHANNEL,
        )
        assert ctx.message == "find documents"
        assert ctx.user_id == "u1"
        assert ctx.session_id == "s1"
        assert ctx.place == InteractionSpace.SLACK_CHANNEL
        assert ctx.spatial_context == {"channel": "C123"}

    def test_from_classify_args_handles_none_context(self):
        """Factory method handles None context gracefully."""
        ctx = IntentClassificationContext.from_classify_args(
            message="test",
            context=None,
            spatial_context=None,
        )
        assert ctx.user_id is None
        assert ctx.session_id is None


class TestIntentUnderstanding:
    """Test IntentUnderstanding dataclass."""

    @pytest.fixture
    def basic_intent(self):
        """Create a basic Intent for testing."""
        return Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.9,
        )

    def test_wraps_intent(self, basic_intent):
        """IntentUnderstanding wraps raw Intent."""
        understanding = IntentUnderstanding(
            intent=basic_intent,
            understanding_narrative="I understand you want to create something",
            confidence_expression="Got it!",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
        )
        assert understanding.intent == basic_intent
        assert understanding.perception_mode == PerceptionMode.NOTICING

    def test_proxy_properties_category(self, basic_intent):
        """Category proxy property works."""
        understanding = IntentUnderstanding(
            intent=basic_intent,
            understanding_narrative="test",
            confidence_expression="test",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
        )
        assert understanding.category == IntentCategory.EXECUTION
        assert understanding.category == basic_intent.category

    def test_proxy_properties_action(self, basic_intent):
        """Action proxy property works."""
        understanding = IntentUnderstanding(
            intent=basic_intent,
            understanding_narrative="test",
            confidence_expression="test",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
        )
        assert understanding.action == "create_item"
        assert understanding.action == basic_intent.action

    def test_proxy_properties_confidence(self, basic_intent):
        """Confidence proxy property works."""
        understanding = IntentUnderstanding(
            intent=basic_intent,
            understanding_narrative="test",
            confidence_expression="test",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
        )
        assert understanding.confidence == 0.9
        assert understanding.confidence == basic_intent.confidence

    def test_proxy_properties_id(self, basic_intent):
        """ID proxy property works."""
        understanding = IntentUnderstanding(
            intent=basic_intent,
            understanding_narrative="test",
            confidence_expression="test",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
        )
        assert understanding.id == basic_intent.id

    def test_follow_up_optional(self, basic_intent):
        """Follow-up suggestion is optional."""
        understanding = IntentUnderstanding(
            intent=basic_intent,
            understanding_narrative="test",
            confidence_expression="test",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
        )
        assert understanding.follow_up_suggestion is None

        understanding_with_followup = IntentUnderstanding(
            intent=basic_intent,
            understanding_narrative="test",
            confidence_expression="test",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
            follow_up_suggestion="Is that what you meant?",
        )
        assert understanding_with_followup.follow_up_suggestion == "Is that what you meant?"

    def test_experience_test_no_mechanical_language(self, basic_intent):
        """Understanding uses experiential, not mechanical language."""
        understanding = IntentUnderstanding(
            intent=basic_intent,
            understanding_narrative="I understand you want to create something",
            confidence_expression="Got it!",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
        )
        # Experience test: no mechanical language
        assert "Query returned" not in understanding.understanding_narrative
        assert "Classification" not in understanding.understanding_narrative
        assert "processed" not in understanding.understanding_narrative.lower()
        # Should have personal language
        assert "I" in understanding.understanding_narrative


class TestBackwardCompatibility:
    """Ensure IntentUnderstanding works as drop-in where Intent is used."""

    def test_can_access_all_intent_fields(self):
        """All commonly used Intent fields accessible via proxy."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_files",
            confidence=0.75,
            context={"search_query": "project plans"},
        )
        understanding = IntentUnderstanding(
            intent=intent,
            understanding_narrative="I think you want to search",
            confidence_expression="I believe I understand",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
        )

        # All these should work as if accessing Intent directly
        assert understanding.category == IntentCategory.QUERY
        assert understanding.action == "search_files"
        assert understanding.confidence == 0.75
        assert understanding.context == {"search_query": "project plans"}
        assert understanding.id is not None  # UUID generated
