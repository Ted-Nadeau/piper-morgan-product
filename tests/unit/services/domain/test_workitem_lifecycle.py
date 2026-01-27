"""
Unit tests for WorkItem lifecycle integration (#685 MUX-LIFECYCLE-OBJECTS).

Tests verify:
- WorkItem.to_dict() includes lifecycle_state when present
- WorkItem.to_dict() excludes lifecycle_state when None
"""

import pytest

from services.domain.models import WorkItem
from services.mux.lifecycle import LifecycleState


class TestWorkItemToDictLifecycle:
    """Test WorkItem.to_dict() lifecycle inclusion."""

    def test_to_dict_includes_lifecycle_when_present(self):
        """to_dict includes lifecycle_state when it's set."""
        item = WorkItem(
            title="Test task",
            status="open",
            lifecycle_state=LifecycleState.NOTICED,
        )
        result = item.to_dict()
        assert "lifecycle_state" in result
        assert result["lifecycle_state"] == "noticed"

    def test_to_dict_excludes_lifecycle_when_none(self):
        """to_dict excludes lifecycle_state when it's None."""
        item = WorkItem(title="Test task", status="open")
        result = item.to_dict()
        assert "lifecycle_state" not in result

    def test_to_dict_lifecycle_all_states(self):
        """to_dict includes correct value for all lifecycle states."""
        for state in LifecycleState:
            item = WorkItem(
                title="Test task",
                status="open",
                lifecycle_state=state,
            )
            result = item.to_dict()
            assert result["lifecycle_state"] == state.value

    def test_to_dict_preserves_other_fields(self):
        """to_dict still includes all standard fields with lifecycle."""
        item = WorkItem(
            title="Test task",
            description="A test",
            status="in_progress",
            priority="high",
            lifecycle_state=LifecycleState.RATIFIED,
        )
        result = item.to_dict()

        # Check lifecycle
        assert result["lifecycle_state"] == "ratified"

        # Check standard fields still present
        assert result["title"] == "Test task"
        assert result["description"] == "A test"
        assert result["status"] == "in_progress"
        assert result["priority"] == "high"
        assert "id" in result
        assert "created_at" in result
