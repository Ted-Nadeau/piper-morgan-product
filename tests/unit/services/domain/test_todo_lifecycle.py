"""
Unit tests for Todo lifecycle integration (#708 MUX-LIFECYCLE-UI-TODOS).

Tests verify:
- Todo.to_dict() includes lifecycle_state when present
- Todo.to_dict() excludes lifecycle_state when None
- Todo model accepts lifecycle_state field

Follows "Lifecycle Optionality" principle: simple status + optional lifecycle_state.
"""

import pytest

from services.domain.models import Todo
from services.mux.lifecycle import LifecycleState


class TestTodoLifecycleField:
    """Test Todo model accepts lifecycle_state field."""

    def test_todo_accepts_lifecycle_state(self):
        """Todo can be created with lifecycle_state."""
        todo = Todo(
            text="Review quarterly report",
            lifecycle_state=LifecycleState.RATIFIED,
        )
        assert todo.lifecycle_state == LifecycleState.RATIFIED

    def test_todo_defaults_lifecycle_to_none(self):
        """Todo defaults lifecycle_state to None (simple status mode)."""
        todo = Todo(text="Simple task")
        assert todo.lifecycle_state is None


class TestTodoToDictLifecycle:
    """Test Todo.to_dict() lifecycle inclusion."""

    def test_to_dict_includes_lifecycle_when_present(self):
        """to_dict includes lifecycle_state when it's set."""
        todo = Todo(
            text="Review PR",
            lifecycle_state=LifecycleState.NOTICED,
        )
        result = todo.to_dict()
        assert "lifecycle_state" in result
        assert result["lifecycle_state"] == "noticed"

    def test_to_dict_excludes_lifecycle_when_none(self):
        """to_dict excludes lifecycle_state when it's None."""
        todo = Todo(text="Simple task")
        result = todo.to_dict()
        assert "lifecycle_state" not in result

    def test_to_dict_lifecycle_all_states(self):
        """to_dict includes correct value for all lifecycle states."""
        for state in LifecycleState:
            todo = Todo(
                text="Test task",
                lifecycle_state=state,
            )
            result = todo.to_dict()
            assert result["lifecycle_state"] == state.value

    def test_to_dict_preserves_other_fields(self):
        """to_dict still includes all standard fields with lifecycle."""
        todo = Todo(
            text="Test task",
            description="A test description",
            status="pending",
            priority="high",
            lifecycle_state=LifecycleState.RATIFIED,
        )
        result = todo.to_dict()

        # Check lifecycle
        assert result["lifecycle_state"] == "ratified"

        # Check standard fields still present
        assert result["text"] == "Test task"
        assert result["description"] == "A test description"
        assert result["status"] == "pending"
        assert result["priority"] == "high"
        assert "id" in result
        assert "created_at" in result


class TestTodoHybridModel:
    """Test the hybrid model: simple status + optional lifecycle."""

    def test_status_and_lifecycle_coexist(self):
        """Todo can have both status and lifecycle_state."""
        todo = Todo(
            text="Complete quarterly review",
            status="pending",  # Simple status
            lifecycle_state=LifecycleState.RATIFIED,  # Optional lifecycle
        )
        result = todo.to_dict()

        # Both should be present
        assert result["status"] == "pending"
        assert result["lifecycle_state"] == "ratified"

    def test_completed_todo_with_lifecycle(self):
        """Completed todo can still have lifecycle (e.g., ARCHIVED or COMPOSTED)."""
        todo = Todo(
            text="Old project task",
            status="completed",
            completed=True,
            lifecycle_state=LifecycleState.COMPOSTED,
        )
        result = todo.to_dict()

        assert result["status"] == "completed"
        assert result["completed"] is True
        assert result["lifecycle_state"] == "composted"
