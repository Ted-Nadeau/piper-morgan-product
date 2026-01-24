"""
Tests for CompostBin - staging area for objects awaiting decomposition.

Part of #666 COMPOSTING-BIN (child of #436 MUX-TECH-PHASE4-COMPOSTING).
"""

from dataclasses import dataclass
from datetime import datetime, timedelta

import pytest

from services.mux.compost_bin import (
    CompostBin,
    CompostBinEntry,
    determine_trigger,
    meets_composting_criteria,
    on_lifecycle_archived,
    on_lifecycle_deprecated,
)
from services.mux.composting_models import CompostingTrigger

# =============================================================================
# Test Fixtures
# =============================================================================


@dataclass
class MockObject:
    """Mock object for testing."""

    id: str
    name: str
    created_at: datetime = None
    is_contradicted: bool = False
    lifecycle_state: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


# =============================================================================
# CompostBinEntry Tests
# =============================================================================


class TestCompostBinEntry:
    """Tests for CompostBinEntry dataclass."""

    def test_basic_creation(self):
        """Test basic entry creation."""
        entry = CompostBinEntry(
            object_id="obj-123",
            object_type="Task",
            trigger=CompostingTrigger.AGE,
        )
        assert entry.object_id == "obj-123"
        assert entry.object_type == "Task"
        assert entry.trigger == CompostingTrigger.AGE
        assert entry.priority == 0

    def test_contradiction_gets_priority_boost(self):
        """Test that CONTRADICTION trigger gets automatic priority boost."""
        entry = CompostBinEntry(
            object_id="obj-123",
            object_type="Insight",
            trigger=CompostingTrigger.CONTRADICTION,
            priority=0,
        )
        assert entry.priority >= 10  # Auto-boosted

    def test_contradiction_preserves_higher_priority(self):
        """Test that contradiction doesn't lower existing high priority."""
        entry = CompostBinEntry(
            object_id="obj-123",
            object_type="Insight",
            trigger=CompostingTrigger.CONTRADICTION,
            priority=15,
        )
        assert entry.priority == 15  # Not lowered to 10

    def test_to_dict(self):
        """Test serialization to dictionary."""
        entry = CompostBinEntry(
            object_id="obj-456",
            object_type="Note",
            trigger=CompostingTrigger.MANUAL,
            priority=5,
        )
        d = entry.to_dict()
        assert d["object_id"] == "obj-456"
        assert d["object_type"] == "Note"
        assert d["trigger"] == "manual"
        assert d["priority"] == 5
        assert "added_at" in d

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "object_id": "obj-789",
            "object_type": "Document",
            "trigger": "scheduled",
            "priority": 3,
            "added_at": "2026-01-24T08:00:00",
        }
        entry = CompostBinEntry.from_dict(data)
        assert entry.object_id == "obj-789"
        assert entry.object_type == "Document"
        assert entry.trigger == CompostingTrigger.SCHEDULED
        assert entry.priority == 3

    def test_from_dict_with_defaults(self):
        """Test deserialization with missing fields."""
        data = {}
        entry = CompostBinEntry.from_dict(data)
        assert entry.object_id == ""
        assert entry.object_type == "unknown"
        assert entry.trigger == CompostingTrigger.MANUAL


# =============================================================================
# CompostBin Core Tests
# =============================================================================


class TestCompostBinBasics:
    """Tests for basic CompostBin operations."""

    def test_creation_empty(self):
        """Test creating an empty bin."""
        bin = CompostBin()
        assert bin.count == 0
        assert bin.pending == []
        assert bin.is_composting is False

    def test_add_by_object(self):
        """Test adding an object to the bin."""
        bin = CompostBin()
        obj = MockObject(id="task-1", name="Test Task")

        entry = bin.add(obj, CompostingTrigger.AGE)

        assert bin.count == 1
        assert entry.object_id == "task-1"
        assert entry.object_type == "MockObject"
        assert entry.trigger == CompostingTrigger.AGE

    def test_add_by_id(self):
        """Test adding by object ID string."""
        bin = CompostBin()

        entry = bin.add("task-123", CompostingTrigger.MANUAL, object_type="Task")

        assert bin.count == 1
        assert entry.object_id == "task-123"
        assert entry.object_type == "Task"

    def test_add_duplicate_returns_existing(self):
        """Test that adding duplicate ID returns existing entry."""
        bin = CompostBin()
        obj = MockObject(id="task-1", name="Test")

        entry1 = bin.add(obj, CompostingTrigger.AGE)
        entry2 = bin.add(obj, CompostingTrigger.MANUAL)

        assert bin.count == 1  # Still just one
        assert entry1 is entry2

    def test_add_duplicate_updates_priority(self):
        """Test that adding with higher priority updates existing."""
        bin = CompostBin()

        bin.add("task-1", CompostingTrigger.AGE, priority=3)
        bin.add("task-1", CompostingTrigger.AGE, priority=8)

        assert bin.count == 1
        entry = bin.get_entry("task-1")
        assert entry.priority == 8

    def test_remove_existing(self):
        """Test removing an existing entry."""
        bin = CompostBin()
        bin.add("task-1", CompostingTrigger.AGE)
        bin.add("task-2", CompostingTrigger.MANUAL)

        removed = bin.remove("task-1")

        assert bin.count == 1
        assert removed.object_id == "task-1"
        assert bin.get_entry("task-1") is None

    def test_remove_nonexistent(self):
        """Test removing nonexistent entry returns None."""
        bin = CompostBin()
        removed = bin.remove("nonexistent")
        assert removed is None

    def test_get_entry(self):
        """Test getting an entry without removing."""
        bin = CompostBin()
        bin.add("task-1", CompostingTrigger.AGE)

        entry = bin.get_entry("task-1")

        assert entry is not None
        assert entry.object_id == "task-1"
        assert bin.count == 1  # Still there

    def test_clear(self):
        """Test clearing all entries."""
        bin = CompostBin()
        bin.add("task-1", CompostingTrigger.AGE)
        bin.add("task-2", CompostingTrigger.MANUAL)
        bin.add("task-3", CompostingTrigger.SCHEDULED)

        cleared = bin.clear()

        assert cleared == 3
        assert bin.count == 0


# =============================================================================
# CompostBin Priority Ordering Tests
# =============================================================================


class TestCompostBinPriority:
    """Tests for priority ordering in get_ready()."""

    def test_get_ready_orders_by_priority(self):
        """Test that get_ready returns high priority first."""
        bin = CompostBin()
        bin.add("low", CompostingTrigger.AGE, priority=1)
        bin.add("high", CompostingTrigger.AGE, priority=10)
        bin.add("medium", CompostingTrigger.AGE, priority=5)

        ready = bin.get_ready(limit=3)

        assert [e.object_id for e in ready] == ["high", "medium", "low"]

    def test_get_ready_fifo_within_priority(self):
        """Test FIFO ordering within same priority level."""
        bin = CompostBin()

        # Add with same priority, at different times
        entry1 = bin.add("first", CompostingTrigger.AGE, priority=5)
        entry1.added_at = datetime(2026, 1, 24, 8, 0, 0)

        entry2 = bin.add("second", CompostingTrigger.AGE, priority=5)
        entry2.added_at = datetime(2026, 1, 24, 9, 0, 0)

        entry3 = bin.add("third", CompostingTrigger.AGE, priority=5)
        entry3.added_at = datetime(2026, 1, 24, 10, 0, 0)

        ready = bin.get_ready(limit=3)

        assert [e.object_id for e in ready] == ["first", "second", "third"]

    def test_get_ready_respects_limit(self):
        """Test that get_ready respects the limit parameter."""
        bin = CompostBin()
        for i in range(10):
            bin.add(f"task-{i}", CompostingTrigger.AGE)

        ready = bin.get_ready(limit=3)

        assert len(ready) == 3

    def test_get_ready_uses_default_batch_size(self):
        """Test that get_ready uses batch_size as default limit."""
        bin = CompostBin(batch_size=5)
        for i in range(10):
            bin.add(f"task-{i}", CompostingTrigger.AGE)

        ready = bin.get_ready()  # No limit specified

        assert len(ready) == 5


# =============================================================================
# CompostBin Processing Logic Tests
# =============================================================================


class TestCompostBinShouldProcess:
    """Tests for should_process_now() logic."""

    def test_empty_bin_never_processes(self):
        """Test that empty bin returns False."""
        bin = CompostBin()
        assert bin.should_process_now() is False

    def test_already_composting_returns_false(self):
        """Test that is_composting=True prevents new processing."""
        bin = CompostBin()
        bin.add("task-1", CompostingTrigger.AGE)
        bin.is_composting = True

        assert bin.should_process_now() is False

    def test_max_pending_triggers_processing(self):
        """Test that exceeding max_pending triggers processing."""
        bin = CompostBin(max_pending=5)
        for i in range(5):
            bin.add(f"task-{i}", CompostingTrigger.AGE)

        assert bin.should_process_now() is True

    def test_high_priority_triggers_processing(self):
        """Test that high priority items trigger processing."""
        bin = CompostBin()
        bin.add("urgent", CompostingTrigger.CONTRADICTION, priority=10)

        # Even with just one item, high priority triggers processing
        assert bin.should_process_now() is True

    def test_quiet_hours_triggers_processing(self):
        """Test that quiet hours (2-5 AM) triggers processing."""
        bin = CompostBin()
        bin.add("task-1", CompostingTrigger.AGE)

        # At 3 AM (quiet hours)
        at_3am = datetime(2026, 1, 24, 3, 0, 0)
        assert bin.should_process_now(current_time=at_3am) is True

    def test_outside_quiet_hours_no_auto_trigger(self):
        """Test that outside quiet hours, low priority doesn't trigger."""
        bin = CompostBin()
        bin.add("task-1", CompostingTrigger.AGE, priority=0)

        # At 10 AM (not quiet hours), low priority
        at_10am = datetime(2026, 1, 24, 10, 0, 0)
        assert bin.should_process_now(current_time=at_10am) is False

    def test_has_urgent_property(self):
        """Test has_urgent property."""
        bin = CompostBin()
        assert bin.has_urgent is False

        bin.add("normal", CompostingTrigger.AGE, priority=5)
        assert bin.has_urgent is False

        bin.add("urgent", CompostingTrigger.CONTRADICTION, priority=10)
        assert bin.has_urgent is True


# =============================================================================
# CompostBin Stats Tests
# =============================================================================


class TestCompostBinStats:
    """Tests for get_stats()."""

    def test_stats_empty_bin(self):
        """Test stats for empty bin."""
        bin = CompostBin()
        stats = bin.get_stats()

        assert stats["total"] == 0
        assert stats["by_trigger"] == {}
        assert stats["avg_priority"] == 0

    def test_stats_with_entries(self):
        """Test stats with multiple entries."""
        bin = CompostBin()
        bin.add("task-1", CompostingTrigger.AGE, priority=5)
        bin.add("task-2", CompostingTrigger.AGE, priority=10)
        bin.add("task-3", CompostingTrigger.MANUAL, priority=0)

        stats = bin.get_stats()

        assert stats["total"] == 3
        assert stats["by_trigger"]["age"] == 2
        assert stats["by_trigger"]["manual"] == 1
        assert stats["avg_priority"] == 5.0  # (5+10+0)/3


# =============================================================================
# Integration Hook Tests
# =============================================================================


class TestMeetsCompostingCriteria:
    """Tests for meets_composting_criteria()."""

    def test_old_object_meets_criteria(self):
        """Test that old objects meet criteria."""
        old_obj = MockObject(
            id="old-1",
            name="Old Thing",
            created_at=datetime.now() - timedelta(days=40),
        )

        assert meets_composting_criteria(old_obj, min_age_days=30) is True

    def test_new_object_fails_criteria(self):
        """Test that new objects don't meet criteria."""
        new_obj = MockObject(
            id="new-1",
            name="New Thing",
            created_at=datetime.now() - timedelta(days=5),
        )

        assert meets_composting_criteria(new_obj, min_age_days=30) is False

    def test_relevance_callback(self):
        """Test custom relevance callback."""
        obj = MockObject(id="test", name="Test")

        # Object is still relevant
        assert meets_composting_criteria(obj, check_relevance=lambda o: True) is False

        # Object is not relevant
        assert meets_composting_criteria(obj, check_relevance=lambda o: False) is True


class TestDetermineTrigger:
    """Tests for determine_trigger()."""

    def test_contradiction_detected(self):
        """Test that contradicted objects get CONTRADICTION trigger."""
        obj = MockObject(id="test", name="Test", is_contradicted=True)
        assert determine_trigger(obj) == CompostingTrigger.CONTRADICTION

    def test_age_detected(self):
        """Test that old objects get AGE trigger."""
        obj = MockObject(
            id="test",
            name="Test",
            created_at=datetime.now() - timedelta(days=45),
        )
        assert determine_trigger(obj) == CompostingTrigger.AGE

    def test_default_to_manual(self):
        """Test that unknown cases default to MANUAL."""
        obj = MockObject(id="test", name="Test")
        assert determine_trigger(obj) == CompostingTrigger.MANUAL


class TestLifecycleHooks:
    """Tests for lifecycle integration hooks."""

    @pytest.mark.asyncio
    async def test_on_lifecycle_deprecated_with_old_object(self):
        """Test deprecated hook adds old objects."""
        bin = CompostBin()
        old_obj = MockObject(
            id="old-1",
            name="Old",
            created_at=datetime.now() - timedelta(days=40),
        )

        entry = await on_lifecycle_deprecated(old_obj, bin)

        assert entry is not None
        assert bin.count == 1

    @pytest.mark.asyncio
    async def test_on_lifecycle_deprecated_with_new_object(self):
        """Test deprecated hook skips new objects."""
        bin = CompostBin()
        new_obj = MockObject(id="new-1", name="New")

        entry = await on_lifecycle_deprecated(new_obj, bin)

        assert entry is None
        assert bin.count == 0

    @pytest.mark.asyncio
    async def test_on_lifecycle_deprecated_force(self):
        """Test deprecated hook with force=True."""
        bin = CompostBin()
        new_obj = MockObject(id="new-1", name="New")

        entry = await on_lifecycle_deprecated(new_obj, bin, force=True)

        assert entry is not None
        assert bin.count == 1

    @pytest.mark.asyncio
    async def test_on_lifecycle_archived_always_adds(self):
        """Test archived hook always adds to bin."""
        bin = CompostBin()
        obj = MockObject(id="archived-1", name="Archived")

        entry = await on_lifecycle_archived(obj, bin)

        assert entry is not None
        assert bin.count == 1
