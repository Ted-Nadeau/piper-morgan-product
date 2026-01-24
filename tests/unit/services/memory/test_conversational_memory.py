"""
Tests for ConversationalMemoryService.

Part of #657 MEM-ADR054-P1.

Tests cover:
- ConversationalMemoryEntry dataclass
- ConversationalMemoryWindow dataclass and helper methods
- ConversationalMemoryService methods
- 24-hour window boundary behavior
- Pruning behavior
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest

from services.memory.conversational_memory import (
    ConversationalMemoryEntry,
    ConversationalMemoryService,
    ConversationalMemoryWindow,
)

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def mock_repository():
    """Mock repository for testing."""
    return AsyncMock()


@pytest.fixture
def service(mock_repository):
    """Service with mocked repository."""
    return ConversationalMemoryService(repository=mock_repository)


def make_entry(
    conversation_id: str = "conv-123",
    topic: str = "Test topic",
    hours_ago: float = 0,
    entities: list = None,
    outcome: str = None,
    sentiment: str = None,
) -> ConversationalMemoryEntry:
    """Helper to create test entries."""
    return ConversationalMemoryEntry(
        conversation_id=conversation_id,
        timestamp=datetime.now(timezone.utc) - timedelta(hours=hours_ago),
        topic_summary=topic,
        entities_mentioned=entities or [],
        outcome=outcome,
        user_sentiment=sentiment,
    )


# =============================================================================
# Test: ConversationalMemoryEntry
# =============================================================================


class TestConversationalMemoryEntry:
    """Tests for the ConversationalMemoryEntry dataclass."""

    def test_creates_with_required_fields(self):
        """Entry can be created with required fields only."""
        entry = ConversationalMemoryEntry(
            conversation_id="conv-1",
            timestamp=datetime.now(timezone.utc),
            topic_summary="Discussed project roadmap",
        )
        assert entry.conversation_id == "conv-1"
        assert entry.topic_summary == "Discussed project roadmap"
        assert entry.entities_mentioned == []
        assert entry.outcome is None
        assert entry.user_sentiment is None

    def test_creates_with_all_fields(self):
        """Entry can be created with all fields."""
        entry = ConversationalMemoryEntry(
            conversation_id="conv-2",
            timestamp=datetime.now(timezone.utc),
            topic_summary="Fixed authentication bug",
            entities_mentioned=["auth-service", "user-api"],
            outcome="Bug resolved",
            user_sentiment="positive",
        )
        assert entry.entities_mentioned == ["auth-service", "user-api"]
        assert entry.outcome == "Bug resolved"
        assert entry.user_sentiment == "positive"

    def test_timestamp_is_stored_correctly(self):
        """Timestamp is preserved accurately."""
        now = datetime.now(timezone.utc)
        entry = ConversationalMemoryEntry(
            conversation_id="conv-1",
            timestamp=now,
            topic_summary="Test",
        )
        assert entry.timestamp == now


# =============================================================================
# Test: ConversationalMemoryWindow
# =============================================================================


class TestConversationalMemoryWindow:
    """Tests for the ConversationalMemoryWindow dataclass."""

    def test_empty_window(self):
        """Empty window has no entries."""
        window = ConversationalMemoryWindow(user_id="user-1")
        assert window.is_empty()
        assert window.get_most_recent() is None
        assert window.get_active_topics() == []
        assert window.get_active_entities() == []

    def test_get_most_recent(self):
        """Returns first entry (most recent)."""
        entries = [
            make_entry(topic="Recent", hours_ago=1),
            make_entry(topic="Older", hours_ago=5),
        ]
        window = ConversationalMemoryWindow(user_id="user-1", entries=entries)
        assert window.get_most_recent().topic_summary == "Recent"

    def test_get_active_topics_deduplicates(self):
        """Topics are deduplicated."""
        entries = [
            make_entry(topic="Topic A"),
            make_entry(topic="Topic B"),
            make_entry(topic="Topic A"),  # Duplicate
        ]
        window = ConversationalMemoryWindow(user_id="user-1", entries=entries)
        topics = window.get_active_topics()
        assert len(topics) == 2
        assert "Topic A" in topics
        assert "Topic B" in topics

    def test_get_active_entities_deduplicates(self):
        """Entities are deduplicated across entries."""
        entries = [
            make_entry(entities=["project-A", "user-X"]),
            make_entry(entities=["project-B", "user-X"]),  # user-X is duplicate
        ]
        window = ConversationalMemoryWindow(user_id="user-1", entries=entries)
        entities = window.get_active_entities()
        assert len(entities) == 3
        assert "project-A" in entities
        assert "project-B" in entities
        assert "user-X" in entities

    def test_is_empty_false_with_entries(self):
        """is_empty returns False when entries exist."""
        entries = [make_entry()]
        window = ConversationalMemoryWindow(user_id="user-1", entries=entries)
        assert not window.is_empty()

    def test_empty_topic_filtered(self):
        """Empty topic strings are filtered out."""
        entries = [
            make_entry(topic="Valid topic"),
            make_entry(topic=""),  # Empty
        ]
        window = ConversationalMemoryWindow(user_id="user-1", entries=entries)
        topics = window.get_active_topics()
        assert len(topics) == 1
        assert "Valid topic" in topics


# =============================================================================
# Test: ConversationalMemoryService.record_conversation_end
# =============================================================================


class TestRecordConversationEnd:
    """Tests for recording conversation summaries."""

    @pytest.mark.asyncio
    async def test_saves_entry_with_required_fields(self, service, mock_repository):
        """Records entry with required fields."""
        mock_repository.save_entry = AsyncMock()
        mock_repository.delete_entries_before = AsyncMock(return_value=0)

        await service.record_conversation_end(
            user_id="user-1",
            conversation_id="conv-1",
            summary="Discussed sprint planning",
        )

        mock_repository.save_entry.assert_called_once()
        call_args = mock_repository.save_entry.call_args
        assert call_args[0][0] == "user-1"  # user_id
        entry = call_args[0][1]
        assert entry.conversation_id == "conv-1"
        assert entry.topic_summary == "Discussed sprint planning"

    @pytest.mark.asyncio
    async def test_saves_entry_with_all_fields(self, service, mock_repository):
        """Records entry with all optional fields."""
        mock_repository.save_entry = AsyncMock()
        mock_repository.delete_entries_before = AsyncMock(return_value=0)

        await service.record_conversation_end(
            user_id="user-1",
            conversation_id="conv-2",
            summary="Fixed critical bug",
            entities=["auth-service", "api-gateway"],
            outcome="Deployed fix to production",
            sentiment="positive",
        )

        entry = mock_repository.save_entry.call_args[0][1]
        assert entry.entities_mentioned == ["auth-service", "api-gateway"]
        assert entry.outcome == "Deployed fix to production"
        assert entry.user_sentiment == "positive"

    @pytest.mark.asyncio
    async def test_prunes_old_entries_after_save(self, service, mock_repository):
        """Prunes old entries after saving new one."""
        mock_repository.save_entry = AsyncMock()
        mock_repository.delete_entries_before = AsyncMock(return_value=3)

        await service.record_conversation_end(
            user_id="user-1",
            conversation_id="conv-1",
            summary="Test",
        )

        mock_repository.delete_entries_before.assert_called_once()
        call_args = mock_repository.delete_entries_before.call_args
        assert call_args[0][0] == "user-1"

    @pytest.mark.asyncio
    async def test_timestamp_is_set_automatically(self, service, mock_repository):
        """Entry timestamp is set to current time."""
        mock_repository.save_entry = AsyncMock()
        mock_repository.delete_entries_before = AsyncMock(return_value=0)

        before = datetime.now(timezone.utc)
        await service.record_conversation_end(
            user_id="user-1",
            conversation_id="conv-1",
            summary="Test",
        )
        after = datetime.now(timezone.utc)

        entry = mock_repository.save_entry.call_args[0][1]
        assert before <= entry.timestamp <= after


# =============================================================================
# Test: ConversationalMemoryService.get_memory_window
# =============================================================================


class TestGetMemoryWindow:
    """Tests for retrieving memory window."""

    @pytest.mark.asyncio
    async def test_returns_window_with_entries(self, service, mock_repository):
        """Returns window with entries from repository."""
        entries = [make_entry(topic="Topic 1"), make_entry(topic="Topic 2")]
        mock_repository.get_entries_since = AsyncMock(return_value=entries)

        window = await service.get_memory_window("user-1")

        assert window.user_id == "user-1"
        assert len(window.entries) == 2
        assert not window.is_empty()

    @pytest.mark.asyncio
    async def test_returns_empty_window_for_new_user(self, service, mock_repository):
        """Returns empty window for user with no history."""
        mock_repository.get_entries_since = AsyncMock(return_value=[])

        window = await service.get_memory_window("new-user")

        assert window.user_id == "new-user"
        assert window.is_empty()

    @pytest.mark.asyncio
    async def test_window_uses_24_hour_range(self, service, mock_repository):
        """Window queries for 24-hour range."""
        mock_repository.get_entries_since = AsyncMock(return_value=[])

        await service.get_memory_window("user-1")

        call_args = mock_repository.get_entries_since.call_args
        since_arg = call_args[0][1]

        # Should be approximately 24 hours ago
        now = datetime.now(timezone.utc)
        hours_ago = (now - since_arg).total_seconds() / 3600
        assert 23.9 < hours_ago < 24.1  # Allow small variance


# =============================================================================
# Test: Window Boundary Behavior
# =============================================================================


class TestWindowBoundary:
    """Tests for 24-hour window boundary behavior."""

    def test_window_start_is_24_hours_ago(self):
        """Window start is 24 hours before window end."""
        window = ConversationalMemoryWindow(user_id="user-1")
        duration = window.window_end - window.window_start
        assert 23.9 < duration.total_seconds() / 3600 < 24.1

    @pytest.mark.asyncio
    async def test_23_hour_old_entry_in_window(self, service, mock_repository):
        """Entry 23 hours old should be included."""
        entry = make_entry(hours_ago=23)
        mock_repository.get_entries_since = AsyncMock(return_value=[entry])

        window = await service.get_memory_window("user-1")

        assert len(window.entries) == 1

    @pytest.mark.asyncio
    async def test_25_hour_old_entry_excluded(self, service, mock_repository):
        """Entry 25 hours old should NOT be returned by repository."""
        # Repository filtering handles this - test documents expected behavior
        mock_repository.get_entries_since = AsyncMock(return_value=[])

        window = await service.get_memory_window("user-1")

        assert window.is_empty()


# =============================================================================
# Test: Pruning Behavior
# =============================================================================


class TestPruning:
    """Tests for old entry pruning."""

    @pytest.mark.asyncio
    async def test_prune_deletes_old_entries(self, service, mock_repository):
        """Pruning removes entries older than 24 hours."""
        mock_repository.delete_entries_before = AsyncMock(return_value=5)

        await service._prune_old_entries("user-1")

        mock_repository.delete_entries_before.assert_called_once()
        call_args = mock_repository.delete_entries_before.call_args
        assert call_args[0][0] == "user-1"

        # Cutoff should be ~24 hours ago
        cutoff = call_args[0][1]
        now = datetime.now(timezone.utc)
        hours_ago = (now - cutoff).total_seconds() / 3600
        assert 23.9 < hours_ago < 24.1

    @pytest.mark.asyncio
    async def test_prune_with_no_entries_to_delete(self, service, mock_repository):
        """Pruning handles case where nothing is deleted."""
        mock_repository.delete_entries_before = AsyncMock(return_value=0)

        # Should not raise
        await service._prune_old_entries("user-1")

        mock_repository.delete_entries_before.assert_called_once()


# =============================================================================
# Test: Service Configuration
# =============================================================================


class TestServiceConfiguration:
    """Tests for service configuration."""

    def test_window_hours_is_24(self):
        """Service uses 24-hour window."""
        assert ConversationalMemoryService.WINDOW_HOURS == 24
