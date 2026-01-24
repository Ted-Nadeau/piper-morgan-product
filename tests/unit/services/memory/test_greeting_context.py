"""
Tests for greeting context service.

Part of #662 MEM-ADR054-P2.

Tests cover:
- GreetingCondition enum values
- GreetingContext dataclass
- GreetingContextService condition detection
- Time-based condition boundaries
- Sentiment override behavior
- can_reference_work and offer_fresh_start flags
- Integration with ConversationalMemoryService
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.memory.conversational_memory import (
    ConversationalMemoryEntry,
    ConversationalMemoryWindow,
)
from services.memory.greeting_context import (
    GREETING_APPROACHES,
    GreetingCondition,
    GreetingContext,
    GreetingContextService,
)

# =============================================================================
# Test Fixtures
# =============================================================================


def make_entry(
    topic: str = "Discussed project roadmap",
    hours_ago: float = 0,
    sentiment: str = None,
    entities: list = None,
    outcome: str = None,
) -> ConversationalMemoryEntry:
    """Helper to create test memory entries."""
    return ConversationalMemoryEntry(
        conversation_id="conv-123",
        timestamp=datetime.now(timezone.utc) - timedelta(hours=hours_ago),
        topic_summary=topic,
        entities_mentioned=entities or [],
        outcome=outcome,
        user_sentiment=sentiment,
    )


def make_window(entries: list = None, user_id: str = "user-1") -> ConversationalMemoryWindow:
    """Helper to create test memory windows."""
    return ConversationalMemoryWindow(
        user_id=user_id,
        entries=entries or [],
    )


@pytest.fixture
def mock_memory_service():
    """Mock memory service for testing."""
    return AsyncMock()


@pytest.fixture
def service(mock_memory_service):
    """Greeting context service with mocked memory."""
    return GreetingContextService(memory_service=mock_memory_service)


# =============================================================================
# Test: GreetingCondition Enum
# =============================================================================


class TestGreetingCondition:
    """Tests for the GreetingCondition enum."""

    def test_has_same_day_recent(self):
        """SAME_DAY_RECENT condition exists."""
        assert GreetingCondition.SAME_DAY_RECENT.value == "same_day_recent"

    def test_has_next_day_active(self):
        """NEXT_DAY_ACTIVE condition exists."""
        assert GreetingCondition.NEXT_DAY_ACTIVE.value == "next_day_active"

    def test_has_week_gap(self):
        """WEEK_GAP condition exists."""
        assert GreetingCondition.WEEK_GAP.value == "week_gap"

    def test_has_month_gap(self):
        """MONTH_GAP condition exists."""
        assert GreetingCondition.MONTH_GAP.value == "month_gap"

    def test_has_previous_trivial(self):
        """PREVIOUS_TRIVIAL condition exists."""
        assert GreetingCondition.PREVIOUS_TRIVIAL.value == "previous_trivial"

    def test_has_previous_negative(self):
        """PREVIOUS_NEGATIVE condition exists."""
        assert GreetingCondition.PREVIOUS_NEGATIVE.value == "previous_negative"

    def test_has_first_session(self):
        """FIRST_SESSION condition exists."""
        assert GreetingCondition.FIRST_SESSION.value == "first_session"

    def test_all_conditions_have_approaches(self):
        """All conditions have greeting approaches defined."""
        for condition in GreetingCondition:
            assert condition in GREETING_APPROACHES


# =============================================================================
# Test: GreetingContext Dataclass
# =============================================================================


class TestGreetingContext:
    """Tests for the GreetingContext dataclass."""

    def test_creates_with_all_fields(self):
        """GreetingContext can be created with all fields."""
        entry = make_entry()
        ctx = GreetingContext(
            condition=GreetingCondition.SAME_DAY_RECENT,
            last_session=entry,
            time_since_last=timedelta(hours=2),
            suggested_greeting_approach="Back already!",
            can_reference_work=True,
            offer_fresh_start=False,
            topic_reference="project roadmap",
            entity_references=["api-project"],
        )

        assert ctx.condition == GreetingCondition.SAME_DAY_RECENT
        assert ctx.can_reference_work is True
        assert ctx.offer_fresh_start is False
        assert ctx.topic_reference == "project roadmap"

    def test_defaults_for_optional_fields(self):
        """Optional fields have sensible defaults."""
        ctx = GreetingContext(
            condition=GreetingCondition.FIRST_SESSION,
            last_session=None,
            time_since_last=None,
            suggested_greeting_approach="Welcome!",
            can_reference_work=False,
            offer_fresh_start=False,
        )

        assert ctx.topic_reference is None
        assert ctx.entity_references == []


# =============================================================================
# Test: Condition Detection - Time-Based
# =============================================================================


class TestConditionDetectionTimeBased:
    """Tests for time-based condition detection."""

    @pytest.mark.asyncio
    async def test_first_session_when_no_entries(self, service, mock_memory_service):
        """First session detected when user has no history."""
        mock_memory_service.get_memory_window.return_value = make_window(entries=[])

        ctx = await service.get_greeting_context("new-user")

        assert ctx.condition == GreetingCondition.FIRST_SESSION
        assert ctx.last_session is None
        assert ctx.time_since_last is None

    @pytest.mark.asyncio
    async def test_same_day_recent_within_8_hours(self, service, mock_memory_service):
        """Same day recent detected within 8 hours."""
        entry = make_entry(hours_ago=4)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.SAME_DAY_RECENT

    @pytest.mark.asyncio
    async def test_same_day_recent_boundary(self, service, mock_memory_service):
        """Just under 8 hours is still same day recent."""
        entry = make_entry(hours_ago=7.9)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.SAME_DAY_RECENT

    @pytest.mark.asyncio
    async def test_next_day_active_8_to_36_hours(self, service, mock_memory_service):
        """Next day active detected between 8-36 hours."""
        entry = make_entry(hours_ago=20)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.NEXT_DAY_ACTIVE

    @pytest.mark.asyncio
    async def test_next_day_active_at_8_hours(self, service, mock_memory_service):
        """Exactly 8 hours triggers next day active."""
        entry = make_entry(hours_ago=8)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.NEXT_DAY_ACTIVE

    @pytest.mark.asyncio
    async def test_week_gap_36_hours_to_week(self, service, mock_memory_service):
        """Week gap detected between 36 hours and 1 week."""
        entry = make_entry(hours_ago=72)  # 3 days
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.WEEK_GAP

    @pytest.mark.asyncio
    async def test_week_gap_at_36_hours(self, service, mock_memory_service):
        """Exactly 36 hours triggers week gap."""
        entry = make_entry(hours_ago=36)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.WEEK_GAP

    @pytest.mark.asyncio
    async def test_month_gap_over_week(self, service, mock_memory_service):
        """Month gap detected after 1 week."""
        entry = make_entry(hours_ago=200)  # ~8 days
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.MONTH_GAP

    @pytest.mark.asyncio
    async def test_month_gap_at_168_hours(self, service, mock_memory_service):
        """Exactly 168 hours (1 week) triggers month gap."""
        entry = make_entry(hours_ago=168)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.MONTH_GAP


# =============================================================================
# Test: Condition Detection - Sentiment Override
# =============================================================================


class TestConditionDetectionSentimentOverride:
    """Tests for sentiment-based condition override."""

    @pytest.mark.asyncio
    async def test_negative_sentiment_overrides_same_day(self, service, mock_memory_service):
        """Negative sentiment overrides time-based condition."""
        # Recent session (would be SAME_DAY_RECENT) but negative
        entry = make_entry(hours_ago=2, sentiment="negative")
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.PREVIOUS_NEGATIVE

    @pytest.mark.asyncio
    async def test_negative_sentiment_overrides_next_day(self, service, mock_memory_service):
        """Negative sentiment overrides next day condition."""
        entry = make_entry(hours_ago=20, sentiment="negative")
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.PREVIOUS_NEGATIVE

    @pytest.mark.asyncio
    async def test_positive_sentiment_no_override(self, service, mock_memory_service):
        """Positive sentiment doesn't override time-based condition."""
        entry = make_entry(hours_ago=2, sentiment="positive")
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.SAME_DAY_RECENT

    @pytest.mark.asyncio
    async def test_neutral_sentiment_no_override(self, service, mock_memory_service):
        """Neutral sentiment doesn't override time-based condition."""
        entry = make_entry(hours_ago=2, sentiment="neutral")
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.SAME_DAY_RECENT


# =============================================================================
# Test: Condition Detection - Trivial Session
# =============================================================================


class TestConditionDetectionTrivialSession:
    """Tests for trivial session detection."""

    @pytest.mark.asyncio
    async def test_trivial_session_short_topic_no_entities(self, service, mock_memory_service):
        """Trivial session detected for short topic with no entities."""
        entry = make_entry(
            topic="Hi",  # Very short
            hours_ago=2,
            entities=[],
            outcome=None,
        )
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.PREVIOUS_TRIVIAL

    @pytest.mark.asyncio
    async def test_not_trivial_with_entities(self, service, mock_memory_service):
        """Session with entities is not trivial."""
        entry = make_entry(
            topic="Brief",
            hours_ago=2,
            entities=["project-x"],
            outcome=None,
        )
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        # Should be time-based, not trivial
        assert ctx.condition == GreetingCondition.SAME_DAY_RECENT

    @pytest.mark.asyncio
    async def test_not_trivial_with_outcome(self, service, mock_memory_service):
        """Session with outcome is not trivial."""
        entry = make_entry(
            topic="Brief",
            hours_ago=2,
            entities=[],
            outcome="Completed task",
        )
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.SAME_DAY_RECENT

    @pytest.mark.asyncio
    async def test_not_trivial_with_long_topic(self, service, mock_memory_service):
        """Session with substantive topic is not trivial."""
        entry = make_entry(
            topic="Discussed the project architecture and deployment plan",
            hours_ago=2,
            entities=[],
            outcome=None,
        )
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.condition == GreetingCondition.SAME_DAY_RECENT


# =============================================================================
# Test: Context Flags
# =============================================================================


class TestContextFlags:
    """Tests for can_reference_work and offer_fresh_start flags."""

    @pytest.mark.asyncio
    async def test_can_reference_work_for_same_day_recent(self, service, mock_memory_service):
        """can_reference_work is True for same day recent."""
        entry = make_entry(hours_ago=2)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.can_reference_work is True

    @pytest.mark.asyncio
    async def test_can_reference_work_for_next_day_active(self, service, mock_memory_service):
        """can_reference_work is True for next day active."""
        entry = make_entry(hours_ago=20)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.can_reference_work is True

    @pytest.mark.asyncio
    async def test_cannot_reference_work_for_week_gap(self, service, mock_memory_service):
        """can_reference_work is False for week gap."""
        entry = make_entry(hours_ago=72)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.can_reference_work is False

    @pytest.mark.asyncio
    async def test_cannot_reference_work_for_month_gap(self, service, mock_memory_service):
        """can_reference_work is False for month gap."""
        entry = make_entry(hours_ago=200)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.can_reference_work is False

    @pytest.mark.asyncio
    async def test_offer_fresh_start_for_week_gap(self, service, mock_memory_service):
        """offer_fresh_start is True for week gap."""
        entry = make_entry(hours_ago=72)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.offer_fresh_start is True

    @pytest.mark.asyncio
    async def test_offer_fresh_start_for_month_gap(self, service, mock_memory_service):
        """offer_fresh_start is True for month gap."""
        entry = make_entry(hours_ago=200)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.offer_fresh_start is True

    @pytest.mark.asyncio
    async def test_offer_fresh_start_for_negative(self, service, mock_memory_service):
        """offer_fresh_start is True for negative sentiment."""
        entry = make_entry(hours_ago=2, sentiment="negative")
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.offer_fresh_start is True

    @pytest.mark.asyncio
    async def test_no_fresh_start_for_same_day_recent(self, service, mock_memory_service):
        """offer_fresh_start is False for same day recent."""
        entry = make_entry(hours_ago=2)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.offer_fresh_start is False


# =============================================================================
# Test: Topic and Entity References
# =============================================================================


class TestTopicAndEntityReferences:
    """Tests for topic and entity reference extraction."""

    @pytest.mark.asyncio
    async def test_extracts_topic_reference(self, service, mock_memory_service):
        """Topic reference is extracted from last session."""
        entry = make_entry(topic="API refactoring project")
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.topic_reference == "API refactoring project"

    @pytest.mark.asyncio
    async def test_extracts_entity_references(self, service, mock_memory_service):
        """Entity references are extracted from last session."""
        entry = make_entry(entities=["user-service", "auth-module"])
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert "user-service" in ctx.entity_references
        assert "auth-module" in ctx.entity_references

    @pytest.mark.asyncio
    async def test_no_references_for_first_session(self, service, mock_memory_service):
        """No references for first session."""
        mock_memory_service.get_memory_window.return_value = make_window(entries=[])

        ctx = await service.get_greeting_context("new-user")

        assert ctx.topic_reference is None
        assert ctx.entity_references == []


# =============================================================================
# Test: Suggested Greeting Approaches
# =============================================================================


class TestSuggestedGreetingApproaches:
    """Tests for suggested greeting approach templates."""

    @pytest.mark.asyncio
    async def test_same_day_approach_mentions_topic(self, service, mock_memory_service):
        """Same day approach template includes topic placeholder."""
        entry = make_entry(hours_ago=2)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert (
            "{topic}" in ctx.suggested_greeting_approach
            or "working on" in ctx.suggested_greeting_approach
        )

    @pytest.mark.asyncio
    async def test_first_session_welcome(self, service, mock_memory_service):
        """First session has welcome message."""
        mock_memory_service.get_memory_window.return_value = make_window(entries=[])

        ctx = await service.get_greeting_context("new-user")

        assert (
            "Welcome" in ctx.suggested_greeting_approach
            or "welcome" in ctx.suggested_greeting_approach.lower()
        )

    @pytest.mark.asyncio
    async def test_negative_has_clean_approach(self, service, mock_memory_service):
        """Negative sentiment has clean/neutral approach."""
        entry = make_entry(hours_ago=2, sentiment="negative")
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        # Should not reference previous topic
        assert "{topic}" not in ctx.suggested_greeting_approach


# =============================================================================
# Test: Time Since Last
# =============================================================================


class TestTimeSinceLast:
    """Tests for time_since_last calculation."""

    @pytest.mark.asyncio
    async def test_time_since_last_is_timedelta(self, service, mock_memory_service):
        """time_since_last is a timedelta."""
        entry = make_entry(hours_ago=5)
        mock_memory_service.get_memory_window.return_value = make_window(entries=[entry])

        ctx = await service.get_greeting_context("user-1")

        assert ctx.time_since_last is not None
        # Should be approximately 5 hours
        hours = ctx.time_since_last.total_seconds() / 3600
        assert 4.9 < hours < 5.1

    @pytest.mark.asyncio
    async def test_time_since_last_none_for_first_session(self, service, mock_memory_service):
        """time_since_last is None for first session."""
        mock_memory_service.get_memory_window.return_value = make_window(entries=[])

        ctx = await service.get_greeting_context("new-user")

        assert ctx.time_since_last is None
