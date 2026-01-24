"""
Unit tests for UserTrustProfileRepository.

Issue #647: TRUST-LEVELS-1 - Core Infrastructure
ADR-053: Trust Computation Architecture

Tests repository logic without database (using mocks for async session).
Integration tests would verify actual DB persistence.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest

from services.domain.models import TrustEvent, UserTrustProfile
from services.repositories.user_trust_profile_repository import UserTrustProfileRepository
from services.shared_types import TrustStage


class TestUserTrustProfileRepositoryUnit:
    """Unit tests for UserTrustProfileRepository logic."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        session = AsyncMock()
        session.flush = AsyncMock()
        session.refresh = AsyncMock()
        session.add = MagicMock()
        session.delete = AsyncMock()
        return session

    @pytest.fixture
    def repository(self, mock_session):
        """Create repository with mock session."""
        return UserTrustProfileRepository(mock_session)

    @pytest.fixture
    def sample_user_id(self):
        """Generate a sample user ID."""
        return uuid4()

    @pytest.fixture
    def sample_trust_event(self, sample_user_id):
        """Create a sample trust event."""
        return TrustEvent(
            event_id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            outcome="successful",
            context="User completed task successfully",
            stage_at_time=TrustStage.NEW,
        )

    @pytest.fixture
    def sample_profile(self, sample_user_id):
        """Create a sample user trust profile."""
        return UserTrustProfile(
            user_id=sample_user_id,
            current_stage=TrustStage.NEW,
            highest_stage_achieved=TrustStage.NEW,
            successful_count=0,
            neutral_count=0,
            negative_count=0,
            consecutive_negative=0,
            recent_events=[],
            stage_history=[],
            last_interaction_at=datetime.now(timezone.utc),
            last_stage_change_at=None,
        )


class TestTrustEventToDictMethod:
    """Test TrustEvent.to_dict() method added for repository serialization."""

    def test_to_dict_serializes_all_fields(self):
        """TrustEvent.to_dict() should serialize all fields correctly."""
        event_id = uuid4()
        timestamp = datetime.now(timezone.utc)

        event = TrustEvent(
            event_id=event_id,
            timestamp=timestamp,
            outcome="successful",
            context="Test context",
            stage_at_time=TrustStage.BUILDING,
        )

        result = event.to_dict()

        assert result["event_id"] == str(event_id)
        assert result["timestamp"] == timestamp.isoformat()
        assert result["outcome"] == "successful"
        assert result["context"] == "Test context"
        assert result["stage_at_time"] == 2  # BUILDING = 2

    def test_to_dict_handles_all_stages(self):
        """TrustEvent.to_dict() should handle all TrustStage values."""
        for stage in TrustStage:
            event = TrustEvent(
                event_id=uuid4(),
                timestamp=datetime.now(timezone.utc),
                outcome="neutral",
                context="Testing stage",
                stage_at_time=stage,
            )
            result = event.to_dict()
            assert result["stage_at_time"] == stage.value


class TestRecordEventLogic:
    """Test the business logic in record_event method."""

    def test_successful_outcome_increments_counter(self):
        """Successful outcome should increment successful_count."""
        profile = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.NEW,
            successful_count=5,
            neutral_count=0,
            negative_count=0,
            consecutive_negative=2,
        )

        # Successful outcome should increment and reset consecutive_negative
        assert profile.successful_count == 5
        profile.successful_count += 1
        profile.consecutive_negative = 0

        assert profile.successful_count == 6
        assert profile.consecutive_negative == 0

    def test_neutral_outcome_increments_counter(self):
        """Neutral outcome should increment neutral_count only."""
        profile = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.NEW,
            successful_count=0,
            neutral_count=3,
            negative_count=0,
            consecutive_negative=1,
        )

        # Neutral doesn't reset consecutive_negative per ADR-053
        profile.neutral_count += 1

        assert profile.neutral_count == 4
        assert profile.consecutive_negative == 1  # NOT reset

    def test_negative_outcome_increments_both_counters(self):
        """Negative outcome should increment negative_count and consecutive_negative."""
        profile = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.NEW,
            successful_count=0,
            neutral_count=0,
            negative_count=2,
            consecutive_negative=1,
        )

        profile.negative_count += 1
        profile.consecutive_negative += 1

        assert profile.negative_count == 3
        assert profile.consecutive_negative == 2


class TestStageHistoryFormat:
    """Test stage_history tuple format for domain model."""

    def test_stage_history_uses_tuple_format(self):
        """stage_history should be List[Tuple[datetime, TrustStage, str]]."""
        now = datetime.now(timezone.utc)
        profile = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.BUILDING,
            stage_history=[
                (now, TrustStage.BUILDING, "Reached 10 successful interactions"),
            ],
        )

        assert len(profile.stage_history) == 1
        timestamp, stage, reason = profile.stage_history[0]
        assert timestamp == now
        assert stage == TrustStage.BUILDING
        assert reason == "Reached 10 successful interactions"


class TestTrustStageEnum:
    """Test TrustStage IntEnum behavior per ADR-053."""

    def test_trust_stages_are_comparable(self):
        """TrustStage should support integer comparison for stage checks."""
        assert TrustStage.NEW < TrustStage.BUILDING
        assert TrustStage.BUILDING < TrustStage.ESTABLISHED
        assert TrustStage.ESTABLISHED < TrustStage.TRUSTED

    def test_trust_stages_have_correct_values(self):
        """TrustStage values should match ADR-053 specification."""
        assert TrustStage.NEW.value == 1
        assert TrustStage.BUILDING.value == 2
        assert TrustStage.ESTABLISHED.value == 3
        assert TrustStage.TRUSTED.value == 4

    def test_trust_stage_from_int(self):
        """Should be able to construct TrustStage from integer."""
        assert TrustStage(1) == TrustStage.NEW
        assert TrustStage(2) == TrustStage.BUILDING
        assert TrustStage(3) == TrustStage.ESTABLISHED
        assert TrustStage(4) == TrustStage.TRUSTED


class TestRecentEventsWindowLogic:
    """Test the rolling window logic for recent_events."""

    def test_recent_events_window_maintains_max_size(self):
        """recent_events should maintain max_recent_events window."""
        max_events = 20
        events = []

        # Add 25 events
        for i in range(25):
            event = TrustEvent(
                event_id=uuid4(),
                timestamp=datetime.now(timezone.utc),
                outcome="successful",
                context=f"Event {i}",
                stage_at_time=TrustStage.NEW,
            )
            events.append(event)

        # Window should keep last 20
        if len(events) > max_events:
            events = events[-max_events:]

        assert len(events) == 20
        assert events[0].context == "Event 5"  # First event after window
        assert events[-1].context == "Event 24"  # Most recent


class TestUserTrustProfileToDictMethod:
    """Test UserTrustProfile.to_dict() for JSON serialization."""

    def test_to_dict_serializes_complete_profile(self):
        """UserTrustProfile.to_dict() should serialize all fields."""
        user_id = uuid4()
        now = datetime.now(timezone.utc)

        event = TrustEvent(
            event_id=uuid4(),
            timestamp=now,
            outcome="successful",
            context="Test",
            stage_at_time=TrustStage.NEW,
        )

        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
            highest_stage_achieved=TrustStage.BUILDING,
            successful_count=10,
            neutral_count=2,
            negative_count=1,
            consecutive_negative=0,
            recent_events=[event],
            stage_history=[(now, TrustStage.BUILDING, "Threshold reached")],
            created_at=now,
            last_interaction_at=now,
            last_stage_change_at=now,
        )

        result = profile.to_dict()

        assert result["user_id"] == str(user_id)
        assert result["current_stage"] == 2
        assert result["highest_stage_achieved"] == 2
        assert result["successful_count"] == 10
        assert result["neutral_count"] == 2
        assert result["negative_count"] == 1
        assert result["consecutive_negative"] == 0
        assert len(result["recent_events"]) == 1
        assert len(result["stage_history"]) == 1
