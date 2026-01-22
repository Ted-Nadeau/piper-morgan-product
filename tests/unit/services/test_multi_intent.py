"""
Tests for Multi-Intent Detection and Handling (Issue #595).

This module tests the proper parsing and handling of messages containing
multiple intents, such as "Hi Piper! What's on my agenda?"

The multi-intent system supports:
- Detection of multiple intents in a single message
- "Handle all" strategy (process all detected intents)
- Proper priority ordering (substantive > conversational)
- Greeting acknowledgment when combined with substantive intents

This detection logic is designed to be reusable for #427
(Unified Conversation Model).
"""

import pytest

from services.domain.models import Intent
from services.intent_service.pre_classifier import MultiIntentResult, PreClassifier
from services.shared_types import IntentCategory


class TestMultiIntentResult:
    """Test the MultiIntentResult dataclass."""

    def test_empty_result(self):
        """Empty result has no intents and is not multi-intent."""
        result = MultiIntentResult()
        assert len(result.intents) == 0
        assert result.is_multi_intent is False
        assert result.primary_intent is None
        assert result.secondary_intents == []
        assert result.has_greeting is False
        assert result.has_substantive_intent is False

    def test_single_intent_result(self):
        """Single intent result is not multi-intent."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            confidence=1.0,
        )
        result = MultiIntentResult(
            intents=[intent],
            original_message="What's on my agenda?",
            is_multi_intent=False,
        )
        assert len(result.intents) == 1
        assert result.is_multi_intent is False
        assert result.primary_intent == intent
        assert result.secondary_intents == []

    def test_multi_intent_result(self):
        """Multiple intents properly detected."""
        greeting = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=1.0,
        )
        query = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            confidence=1.0,
        )
        result = MultiIntentResult(
            intents=[greeting, query],
            original_message="Hi Piper! What's on my agenda?",
            is_multi_intent=True,
        )
        assert len(result.intents) == 2
        assert result.is_multi_intent is True
        assert result.has_greeting is True
        assert result.has_substantive_intent is True

    def test_primary_intent_prefers_substantive(self):
        """Primary intent should be substantive over conversational."""
        greeting = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=1.0,
        )
        query = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            confidence=1.0,
        )
        # Order doesn't matter - substantive should be primary
        result = MultiIntentResult(
            intents=[greeting, query],
            original_message="Hi! What's on my agenda?",
            is_multi_intent=True,
        )
        assert result.primary_intent.category == IntentCategory.QUERY
        assert result.primary_intent.action == "meeting_time"

    def test_secondary_intents_excludes_primary(self):
        """Secondary intents should exclude the primary."""
        greeting = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=1.0,
        )
        query = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            confidence=1.0,
        )
        result = MultiIntentResult(
            intents=[greeting, query],
            original_message="Hi! What's on my agenda?",
            is_multi_intent=True,
        )
        secondary = result.secondary_intents
        assert len(secondary) == 1
        assert secondary[0].category == IntentCategory.CONVERSATION
        assert secondary[0].action == "greeting"

    def test_all_conversational_uses_first(self):
        """When all intents are conversational, use first as primary."""
        greeting = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=1.0,
        )
        thanks = Intent(
            category=IntentCategory.CONVERSATION,
            action="thanks",
            confidence=1.0,
        )
        result = MultiIntentResult(
            intents=[greeting, thanks],
            original_message="Hi! Thanks!",
            is_multi_intent=True,
        )
        assert result.primary_intent.action == "greeting"


class TestDetectMultipleIntents:
    """Test PreClassifier.detect_multiple_intents()."""

    def test_greeting_plus_agenda_query(self):
        """The canonical #595 bug case: 'Hi Piper! What's on my agenda?'"""
        result = PreClassifier.detect_multiple_intents("Hi Piper! What's on my agenda?")

        assert result.is_multi_intent is True
        assert result.has_greeting is True
        assert result.has_substantive_intent is True
        assert len(result.intents) >= 2

        # Primary should be the calendar query
        assert result.primary_intent.category == IntentCategory.QUERY
        assert result.primary_intent.action == "meeting_time"

    def test_hello_plus_calendar(self):
        """Greeting with calendar query variation."""
        result = PreClassifier.detect_multiple_intents("Hello! What's on my calendar today?")

        assert result.is_multi_intent is True
        assert result.has_greeting is True
        assert result.primary_intent.category == IntentCategory.QUERY

    def test_hey_plus_meetings(self):
        """Hey greeting with meetings query."""
        result = PreClassifier.detect_multiple_intents("Hey, do I have any meetings today?")

        assert result.is_multi_intent is True
        assert result.has_greeting is True
        assert result.primary_intent.action == "meeting_time"

    def test_greeting_plus_schedule(self):
        """Greeting with schedule query."""
        result = PreClassifier.detect_multiple_intents("Good morning! What's my schedule today?")

        assert result.is_multi_intent is True
        assert result.has_greeting is True
        assert result.primary_intent.category == IntentCategory.QUERY

    def test_greeting_plus_todos(self):
        """Greeting with todos query."""
        result = PreClassifier.detect_multiple_intents("Hi! Show my todos")

        assert result.is_multi_intent is True
        assert result.has_greeting is True
        assert result.primary_intent.category == IntentCategory.QUERY
        assert "todo" in result.primary_intent.action.lower()

    def test_greeting_plus_status(self):
        """Greeting with status query."""
        result = PreClassifier.detect_multiple_intents("Hello! What am I working on?")

        assert result.is_multi_intent is True
        assert result.has_greeting is True
        assert result.primary_intent.category == IntentCategory.STATUS

    def test_greeting_plus_priority(self):
        """Greeting with priority query."""
        result = PreClassifier.detect_multiple_intents("Hey Piper, what should I focus on today?")

        assert result.is_multi_intent is True
        assert result.has_greeting is True
        assert result.primary_intent.category == IntentCategory.PRIORITY

    def test_single_greeting_only(self):
        """Pure greeting should detect single intent."""
        result = PreClassifier.detect_multiple_intents("Hello!")

        assert len(result.intents) == 1
        assert result.is_multi_intent is False
        assert result.has_greeting is True
        assert result.has_substantive_intent is False

    def test_single_query_only(self):
        """Pure query without greeting."""
        result = PreClassifier.detect_multiple_intents("What's on my agenda?")

        # Should detect calendar query
        assert len(result.intents) >= 1
        assert result.has_substantive_intent is True

    def test_thanks_plus_query(self):
        """Thanks with query shouldn't be treated as greeting+substantive."""
        result = PreClassifier.detect_multiple_intents("Thanks! What's next?")

        # Should detect both
        assert len(result.intents) >= 1

    def test_no_intents_detected(self):
        """Message with no matching patterns."""
        result = PreClassifier.detect_multiple_intents("xyzzy plugh")

        assert len(result.intents) == 0
        assert result.is_multi_intent is False
        assert result.primary_intent is None


class TestMultiIntentEdgeCases:
    """Test edge cases in multi-intent detection."""

    def test_emoji_in_greeting(self):
        """Greeting with emoji should still detect multiple intents."""
        result = PreClassifier.detect_multiple_intents("Hi! 👋 What's my schedule?")

        assert result.has_greeting is True
        assert result.has_substantive_intent is True

    def test_multiple_substantive_intents(self):
        """Multiple substantive intents in one message."""
        result = PreClassifier.detect_multiple_intents("What's on my calendar and show my todos")

        # Should detect both calendar and todo queries
        assert len(result.intents) >= 1  # At least one substantive

    def test_case_insensitive_detection(self):
        """Detection should be case insensitive."""
        result = PreClassifier.detect_multiple_intents("HI PIPER! WHAT'S ON MY AGENDA?")

        assert result.is_multi_intent is True
        assert result.has_greeting is True

    def test_extra_whitespace_handling(self):
        """Extra whitespace should be handled."""
        result = PreClassifier.detect_multiple_intents("  Hi!   What's on my agenda?  ")

        assert result.is_multi_intent is True
        assert result.has_greeting is True

    def test_exclamation_points(self):
        """Multiple exclamation points should be handled."""
        result = PreClassifier.detect_multiple_intents("Hello!!! What's on my calendar???")

        assert result.is_multi_intent is True
        assert result.has_greeting is True


class TestCalendarActionRefinement:
    """Test calendar action refinement in multi-intent context."""

    def test_agenda_today_is_meeting_time(self):
        """'What's on my agenda' should map to meeting_time."""
        result = PreClassifier.detect_multiple_intents("Hi! What's on my agenda?")

        primary = result.primary_intent
        assert primary.action == "meeting_time"

    def test_week_calendar_is_week_calendar(self):
        """'What's my week look like' should map to week_calendar."""
        result = PreClassifier.detect_multiple_intents("Hi! What's my week look like?")

        primary = result.primary_intent
        assert primary.action == "week_calendar"

    def test_recurring_meetings_is_recurring(self):
        """'Show recurring meetings' should map to recurring_meetings."""
        result = PreClassifier.detect_multiple_intents("Hi! Show my recurring meetings")

        primary = result.primary_intent
        assert primary.action == "recurring_meetings"


class TestMultiIntentContextMarking:
    """Test that multi-intent context is properly marked."""

    def test_context_includes_multi_intent_flag(self):
        """Detected intents should have multi_intent_detection context."""
        result = PreClassifier.detect_multiple_intents("Hi! What's on my agenda?")

        for intent in result.intents:
            assert intent.context.get("multi_intent_detection") is True

    def test_context_includes_original_message(self):
        """Detected intents should have original_message in context."""
        message = "Hi Piper! What's on my agenda?"
        result = PreClassifier.detect_multiple_intents(message)

        for intent in result.intents:
            assert intent.context.get("original_message") == message
