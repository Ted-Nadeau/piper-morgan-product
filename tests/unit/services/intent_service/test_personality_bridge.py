"""Tests for PersonalityBridge."""

import pytest

from services.domain.models import Intent
from services.intent_service.intent_types import IntentClassificationContext
from services.intent_service.personality_bridge import ACTION_NARRATIVES, PersonalityBridge
from services.shared_types import IntentCategory, PerceptionMode, PlaceType


class TestPersonalityBridge:
    """Test PersonalityBridge transformation."""

    @pytest.fixture
    def bridge(self):
        return PersonalityBridge()

    @pytest.fixture
    def basic_intent(self):
        return Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.9,
        )

    @pytest.fixture
    def basic_context(self):
        return IntentClassificationContext(
            message="add a todo",
            place=PlaceType.WEB_CHAT,
        )

    @pytest.fixture
    def casual_settings(self):
        return {"formality": "casual", "verbosity": "medium"}

    @pytest.fixture
    def professional_settings(self):
        return {"formality": "professional", "verbosity": "concise"}

    # --- Transform Tests ---

    def test_transform_creates_understanding(
        self, bridge, basic_intent, basic_context, casual_settings
    ):
        """Transform creates IntentUnderstanding."""
        understanding = bridge.transform(basic_intent, basic_context, casual_settings)
        assert understanding.intent == basic_intent
        assert understanding.perception_mode == PerceptionMode.NOTICING
        assert "understand" in understanding.understanding_narrative.lower()

    def test_experience_test_no_mechanical_language(
        self, bridge, basic_intent, basic_context, casual_settings
    ):
        """Understanding uses experiential, not mechanical language."""
        understanding = bridge.transform(basic_intent, basic_context, casual_settings)
        # These should NOT appear
        assert "Query" not in understanding.understanding_narrative
        assert "Classification" not in understanding.understanding_narrative
        assert "returned" not in understanding.understanding_narrative
        # These SHOULD appear
        assert "I" in understanding.understanding_narrative

    # --- Perception Mode Tests ---

    def test_noticing_is_default(self, bridge, basic_intent, basic_context, casual_settings):
        """Default perception mode is NOTICING."""
        understanding = bridge.transform(basic_intent, basic_context, casual_settings)
        assert understanding.perception_mode == PerceptionMode.NOTICING

    def test_remembering_for_repeated_patterns(self, basic_context, casual_settings):
        """Repeated patterns trigger REMEMBERING mode."""
        # Set up history showing repeated pattern
        bridge = PersonalityBridge(recent_intents={"user-1": ["create_item"] * 5})
        context = IntentClassificationContext(
            message="add another",
            user_id="user-1",
            place=PlaceType.WEB_CHAT,
        )
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.9,
        )
        understanding = bridge.transform(intent, context, casual_settings)
        assert understanding.perception_mode == PerceptionMode.REMEMBERING

    # --- Confidence Expression Tests ---

    def test_high_confidence_expression_casual(self, bridge, basic_context, casual_settings):
        """High confidence expressed casually."""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.95,
        )
        understanding = bridge.transform(intent, basic_context, casual_settings)
        assert understanding.confidence_expression == "Got it!"

    def test_high_confidence_expression_professional(
        self, bridge, basic_context, professional_settings
    ):
        """High confidence expressed professionally."""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.95,
        )
        understanding = bridge.transform(intent, basic_context, professional_settings)
        assert understanding.confidence_expression == "I understand."

    def test_low_confidence_expresses_uncertainty(self, bridge, basic_context, casual_settings):
        """Low confidence expressed as uncertainty."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_files",
            confidence=0.3,
        )
        understanding = bridge.transform(intent, basic_context, casual_settings)
        assert (
            "not" in understanding.confidence_expression.lower()
            or "sure" in understanding.confidence_expression.lower()
        )

    # --- Action Humanization Tests ---

    def test_action_humanization(self, bridge):
        """Technical actions become human-readable."""
        assert "new" in bridge._humanize_action("create_item")
        assert "find" in bridge._humanize_action("search_files")
        assert "list" in bridge._humanize_action("list_items")

    def test_unknown_action_readable(self, bridge):
        """Unknown actions still become readable."""
        result = bridge._humanize_action("weird_unknown_action")
        assert "_" not in result  # Underscores removed
        assert "weird unknown action" == result

    # --- Place Awareness Tests ---

    def test_slack_channel_notes_brevity(self, bridge, basic_intent, professional_settings):
        """Slack channel gets brevity note."""
        context = IntentClassificationContext(
            message="add a todo",
            place=PlaceType.SLACK_CHANNEL,
        )
        understanding = bridge.transform(basic_intent, context, professional_settings)
        assert "brief" in understanding.place_awareness.lower()

    def test_other_places_no_note(self, bridge, basic_intent, basic_context, casual_settings):
        """Other Places don't need explicit notes."""
        understanding = bridge.transform(basic_intent, basic_context, casual_settings)
        assert understanding.place_awareness == ""

    # --- Follow-up Suggestion Tests ---

    def test_low_confidence_suggests_clarification(self, bridge, basic_context, casual_settings):
        """Low confidence suggests clarification."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_files",
            confidence=0.3,
        )
        understanding = bridge.transform(intent, basic_context, casual_settings)
        assert understanding.follow_up_suggestion is not None
        assert "more" in understanding.follow_up_suggestion.lower()

    def test_high_confidence_no_follow_up(
        self, bridge, basic_intent, basic_context, casual_settings
    ):
        """High confidence usually needs no follow-up."""
        understanding = bridge.transform(basic_intent, basic_context, casual_settings)
        assert understanding.follow_up_suggestion is None


class TestActionNarratives:
    """Test ACTION_NARRATIVES completeness."""

    def test_common_actions_have_narratives(self):
        """Common actions have human-readable narratives."""
        common_actions = [
            "create_item",
            "search_files",
            "list_items",
            "clarification_needed",
        ]
        for action in common_actions:
            assert action in ACTION_NARRATIVES
            # Narrative should be human-readable
            narrative = ACTION_NARRATIVES[action]
            assert "_" not in narrative
            assert len(narrative) > 5
