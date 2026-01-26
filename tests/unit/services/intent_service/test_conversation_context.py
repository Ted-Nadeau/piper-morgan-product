"""
Tests for Conversation Context Manager (#427 MUX-IMPLEMENT-CONVERSE-MODEL)

Verifies:
- Turn-by-turn memory
- Follow-up detection
- Context-dependent resolution
- Temporal reference inheritance
"""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from services.intent_service.conversation_context import (
    FOLLOW_UP_PATTERNS,
    ConversationContext,
    ConversationTurn,
    FollowUpType,
    clear_context,
    detect_follow_up,
    extract_temporal_reference,
    extract_topic,
    get_or_create_context,
    resolve_follow_up,
)
from services.intent_service.intent_types import Intent, IntentCategory


class TestConversationTurn:
    """Tests for ConversationTurn dataclass."""

    def test_turn_has_unique_id(self):
        """Each turn should have a unique ID."""
        turn1 = ConversationTurn(message="Hello")
        turn2 = ConversationTurn(message="Hello")
        assert turn1.id != turn2.id

    def test_turn_has_timestamp(self):
        """Turn should have a timestamp."""
        turn = ConversationTurn(message="Hello")
        assert turn.timestamp is not None
        assert isinstance(turn.timestamp, datetime)

    def test_turn_age_seconds(self):
        """Turn should track age in seconds."""
        turn = ConversationTurn(message="Hello")
        assert turn.age_seconds >= 0
        assert turn.age_seconds < 1  # Should be very recent

    def test_turn_stores_intent(self):
        """Turn should store the classified intent."""
        intent = Intent(category=IntentCategory.QUERY, action="meeting_time")
        turn = ConversationTurn(message="What's on my calendar?", intent=intent)
        assert turn.intent == intent

    def test_turn_stores_temporal_reference(self):
        """Turn should store temporal reference."""
        turn = ConversationTurn(
            message="What's on tomorrow?",
            temporal_reference="tomorrow",
        )
        assert turn.temporal_reference == "tomorrow"


class TestConversationContext:
    """Tests for ConversationContext."""

    def test_context_starts_empty(self):
        """Context should start with no turns."""
        context = ConversationContext()
        assert len(context.turns) == 0

    def test_add_turn(self):
        """Should be able to add turns."""
        context = ConversationContext()
        turn = context.add_turn("Hello Piper!")
        assert len(context.turns) == 1
        assert turn.message == "Hello Piper!"

    def test_last_turn(self):
        """Should return the most recent turn."""
        context = ConversationContext()
        context.add_turn("First")
        context.add_turn("Second")
        context.add_turn("Third")
        assert context.last_turn.message == "Third"

    def test_last_intent(self):
        """Should return intent from last turn."""
        context = ConversationContext()
        intent = Intent(category=IntentCategory.QUERY, action="meeting_time")
        context.add_turn("What's tomorrow?", intent=intent)
        assert context.last_intent == intent

    def test_prunes_old_turns_by_count(self):
        """Should prune turns beyond max_turns."""
        context = ConversationContext(max_turns=3)
        for i in range(5):
            context.add_turn(f"Message {i}")
        assert len(context.turns) == 3
        assert context.turns[0].message == "Message 2"  # Oldest kept

    def test_is_active_when_recent(self):
        """Context should be active when turns are recent."""
        context = ConversationContext()
        context.add_turn("Hello")
        assert context.is_active is True

    def test_not_active_when_empty(self):
        """Context should not be active when empty."""
        context = ConversationContext()
        assert context.is_active is False

    def test_last_temporal_reference(self):
        """Should find the most recent temporal reference."""
        context = ConversationContext()
        context.add_turn("What's on today?", temporal_reference="today")
        context.add_turn("And tomorrow?", temporal_reference="tomorrow")
        assert context.last_temporal_reference == "tomorrow"

    def test_last_temporal_reference_skips_none(self):
        """Should skip turns without temporal reference."""
        context = ConversationContext()
        context.add_turn("What's on tomorrow?", temporal_reference="tomorrow")
        context.add_turn("Tell me more")  # No temporal
        assert context.last_temporal_reference == "tomorrow"


class TestFollowUpDetection:
    """Tests for follow-up detection."""

    @pytest.fixture
    def active_context(self):
        """Create an active context with a previous turn."""
        context = ConversationContext()
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"temporal_reference": "tomorrow"},
        )
        context.add_turn(
            "What's on my calendar tomorrow?",
            intent=intent,
            temporal_reference="tomorrow",
        )
        return context

    def test_detect_temporal_shift_how_about(self, active_context):
        """Should detect 'How about today?'."""
        result = detect_follow_up("How about today?", active_context)
        assert result is not None
        follow_up_type, data = result
        assert follow_up_type == FollowUpType.TEMPORAL_SHIFT
        assert data["new_temporal"] == "today"

    def test_detect_temporal_shift_what_about(self, active_context):
        """Should detect 'What about tomorrow?'."""
        result = detect_follow_up("What about tomorrow?", active_context)
        assert result is not None
        follow_up_type, data = result
        assert follow_up_type == FollowUpType.TEMPORAL_SHIFT
        assert data["new_temporal"] == "tomorrow"

    def test_detect_temporal_shift_and(self, active_context):
        """Should detect 'And today?'."""
        result = detect_follow_up("And today?", active_context)
        assert result is not None
        follow_up_type, _ = result
        assert follow_up_type == FollowUpType.TEMPORAL_SHIFT

    def test_detect_temporal_shift_single_word(self, active_context):
        """Should detect single word temporal like 'Today?'."""
        result = detect_follow_up("Today?", active_context)
        assert result is not None
        follow_up_type, _ = result
        assert follow_up_type == FollowUpType.TEMPORAL_SHIFT

    def test_detect_confirmation_yes(self, active_context):
        """Should detect 'Yes'."""
        result = detect_follow_up("Yes", active_context)
        assert result is not None
        follow_up_type, _ = result
        assert follow_up_type == FollowUpType.CONFIRMATION

    def test_detect_confirmation_okay(self, active_context):
        """Should detect 'Okay'."""
        result = detect_follow_up("Okay", active_context)
        assert result is not None
        follow_up_type, _ = result
        assert follow_up_type == FollowUpType.CONFIRMATION

    def test_detect_continuation_and(self, active_context):
        """Should detect 'And?'."""
        result = detect_follow_up("And?", active_context)
        assert result is not None
        follow_up_type, _ = result
        assert follow_up_type == FollowUpType.CONTINUATION

    def test_detect_continuation_what_else(self, active_context):
        """Should detect 'What else?'."""
        result = detect_follow_up("What else?", active_context)
        assert result is not None
        follow_up_type, _ = result
        assert follow_up_type == FollowUpType.CONTINUATION

    def test_no_follow_up_without_context(self):
        """Should not detect follow-up without active context."""
        empty_context = ConversationContext()
        result = detect_follow_up("How about today?", empty_context)
        assert result is None

    def test_no_follow_up_for_new_query(self, active_context):
        """Should not detect follow-up for new queries."""
        result = detect_follow_up("What projects am I working on?", active_context)
        assert result is None


class TestFollowUpResolution:
    """Tests for resolving follow-ups into intents."""

    @pytest.fixture
    def context_with_calendar(self):
        """Context with a calendar query."""
        context = ConversationContext()
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"temporal_reference": "tomorrow"},
        )
        context.add_turn(
            "What's on my calendar tomorrow?",
            intent=intent,
            temporal_reference="tomorrow",
        )
        return context

    def test_resolve_temporal_shift(self, context_with_calendar):
        """Should resolve temporal shift to inherited intent."""
        extracted = {"new_temporal": "today"}
        resolved = resolve_follow_up(
            FollowUpType.TEMPORAL_SHIFT,
            extracted,
            context_with_calendar,
        )
        assert resolved is not None
        assert resolved.category == IntentCategory.QUERY
        assert resolved.action == "meeting_time"
        assert resolved.context["temporal_reference"] == "today"

    def test_resolve_confirmation(self, context_with_calendar):
        """Should resolve confirmation to confirmation intent."""
        resolved = resolve_follow_up(
            FollowUpType.CONFIRMATION,
            {},
            context_with_calendar,
        )
        assert resolved is not None
        assert resolved.category == IntentCategory.CONVERSATION
        assert resolved.action == "confirmation"

    def test_resolve_continuation(self, context_with_calendar):
        """Should resolve continuation to continue_previous."""
        resolved = resolve_follow_up(
            FollowUpType.CONTINUATION,
            {},
            context_with_calendar,
        )
        assert resolved is not None
        assert resolved.action == "continue_previous"

    def test_resolve_without_last_intent(self):
        """Should return None when no last intent."""
        context = ConversationContext()
        context.add_turn("Hello")  # No intent
        resolved = resolve_follow_up(
            FollowUpType.TEMPORAL_SHIFT,
            {"new_temporal": "today"},
            context,
        )
        assert resolved is None


class TestTemporalExtraction:
    """Tests for temporal reference extraction."""

    def test_extract_today(self):
        """Should extract 'today'."""
        assert extract_temporal_reference("What's on today?") == "today"

    def test_extract_tomorrow(self):
        """Should extract 'tomorrow'."""
        assert extract_temporal_reference("Show me tomorrow's meetings") == "tomorrow"

    def test_extract_yesterday(self):
        """Should extract 'yesterday'."""
        assert extract_temporal_reference("What happened yesterday?") == "yesterday"

    def test_extract_this_week(self):
        """Should extract 'this week'."""
        assert extract_temporal_reference("What's on this week?") == "this_week"

    def test_extract_day_name(self):
        """Should extract day names."""
        assert extract_temporal_reference("What about Monday?") == "monday"

    def test_no_temporal(self):
        """Should return None when no temporal reference."""
        assert extract_temporal_reference("What projects am I on?") is None


class TestTopicExtraction:
    """Tests for topic extraction."""

    def test_extract_topic_from_action(self):
        """Should use intent action as topic."""
        intent = Intent(category=IntentCategory.QUERY, action="meeting_time")
        topic = extract_topic("What's on my calendar?", intent)
        assert topic == "meeting_time"

    def test_extract_topic_from_category(self):
        """Should fall back to category-based topic."""
        intent = Intent(category=IntentCategory.STATUS, action="get")
        topic = extract_topic("Status?", intent)
        assert topic == "status"

    def test_extract_topic_no_intent(self):
        """Should return None without intent."""
        topic = extract_topic("Hello")
        assert topic is None


class TestSessionManagement:
    """Tests for session context management."""

    def test_get_or_create_new(self):
        """Should create new context for new session."""
        session_id = str(uuid4())
        context = get_or_create_context(session_id)
        assert context is not None
        assert len(context.turns) == 0

    def test_get_or_create_existing(self):
        """Should return existing context."""
        session_id = str(uuid4())
        context1 = get_or_create_context(session_id)
        context1.add_turn("Hello")
        context2 = get_or_create_context(session_id)
        assert len(context2.turns) == 1

    def test_clear_context(self):
        """Should clear context for session."""
        session_id = str(uuid4())
        context = get_or_create_context(session_id)
        context.add_turn("Hello")
        clear_context(session_id)
        new_context = get_or_create_context(session_id)
        assert len(new_context.turns) == 0


class TestFollowUpPatterns:
    """Tests for follow-up pattern coverage."""

    def test_temporal_shift_patterns_exist(self):
        """Should have temporal shift patterns."""
        assert FollowUpType.TEMPORAL_SHIFT in FOLLOW_UP_PATTERNS
        assert len(FOLLOW_UP_PATTERNS[FollowUpType.TEMPORAL_SHIFT]) > 0

    def test_confirmation_patterns_exist(self):
        """Should have confirmation patterns."""
        assert FollowUpType.CONFIRMATION in FOLLOW_UP_PATTERNS

    def test_continuation_patterns_exist(self):
        """Should have continuation patterns."""
        assert FollowUpType.CONTINUATION in FOLLOW_UP_PATTERNS

    def test_all_follow_up_types_have_patterns(self):
        """All follow-up types should have patterns."""
        for follow_up_type in FollowUpType:
            assert follow_up_type in FOLLOW_UP_PATTERNS


class TestContextWindowBehavior:
    """Tests for the 10-turn context window (PM-034)."""

    def test_default_max_turns_is_10(self):
        """Default max turns should be 10 per PM-034."""
        context = ConversationContext()
        assert context.max_turns == 10

    def test_maintains_10_turn_window(self):
        """Should maintain exactly 10 turns when more are added."""
        context = ConversationContext()
        for i in range(15):
            context.add_turn(f"Message {i}")
        assert len(context.turns) == 10
        # Should have messages 5-14 (the last 10)
        assert context.turns[0].message == "Message 5"
        assert context.turns[-1].message == "Message 14"

    def test_30_minute_max_age(self):
        """Default max age should be 30 minutes."""
        context = ConversationContext()
        assert context.max_age_minutes == 30
