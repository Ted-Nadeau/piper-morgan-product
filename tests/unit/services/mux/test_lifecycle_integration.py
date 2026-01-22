"""
Tests for Lifecycle Integration Helpers.

These tests verify that lifecycle-aware language can be integrated
into intent handler responses.
"""

from dataclasses import dataclass
from typing import Optional

import pytest

from services.mux.lifecycle import LifecycleState
from services.mux.lifecycle_integration import (
    describe_with_lifecycle,
    explain_transition,
    format_lifecycle_context,
    get_lifecycle_state,
    has_lifecycle,
)


@dataclass
class MockFeature:
    """Mock feature with lifecycle state."""

    name: str
    lifecycle_state: Optional[LifecycleState] = None


@dataclass
class MockTodo:
    """Mock todo without lifecycle state (like current todos)."""

    title: str
    completed: bool = False


class TestDescribeWithLifecycle:
    """Test describe_with_lifecycle helper."""

    def test_object_with_lifecycle_gets_prefix(self):
        """Objects with lifecycle state get experience phrase prefix."""
        feature = MockFeature(name="Auth", lifecycle_state=LifecycleState.EMERGENT)
        result = describe_with_lifecycle(feature, "the auth feature")
        assert "I just noticed" in result
        assert "the auth feature" in result

    def test_object_without_lifecycle_unchanged(self):
        """Objects without lifecycle return base description."""
        todo = MockTodo(title="Review PR")
        result = describe_with_lifecycle(todo, "the review task")
        assert result == "the review task"

    def test_none_lifecycle_unchanged(self):
        """Objects with None lifecycle return base description."""
        feature = MockFeature(name="Auth", lifecycle_state=None)
        result = describe_with_lifecycle(feature, "the auth feature")
        assert result == "the auth feature"

    def test_include_phrase_prefix_false(self):
        """Can disable phrase prefix even with lifecycle."""
        feature = MockFeature(name="Auth", lifecycle_state=LifecycleState.PROPOSED)
        result = describe_with_lifecycle(feature, "the proposal", include_phrase_prefix=False)
        assert result == "the proposal"

    def test_different_lifecycle_states(self):
        """Each lifecycle state produces different prefix."""
        for state in LifecycleState:
            feature = MockFeature(name="Test", lifecycle_state=state)
            result = describe_with_lifecycle(feature, "item")
            # Should contain the experience phrase for that state
            assert state.experience_phrase in result


class TestFormatLifecycleContext:
    """Test format_lifecycle_context helper."""

    def test_returns_none_for_no_lifecycle(self):
        """Returns None if object has no lifecycle."""
        todo = MockTodo(title="Test")
        result = format_lifecycle_context(todo)
        assert result is None

    def test_returns_experience_phrase(self):
        """Returns experience phrase for lifecycle objects."""
        feature = MockFeature(name="Test", lifecycle_state=LifecycleState.RATIFIED)
        result = format_lifecycle_context(feature)
        assert "We're doing" in result

    def test_with_meaning(self):
        """Can include meaning in context."""
        feature = MockFeature(name="Test", lifecycle_state=LifecycleState.DERIVED)
        result = format_lifecycle_context(feature, include_meaning=True)
        assert "I figured out from" in result
        assert "(" in result  # Meaning in parentheses


class TestExplainTransition:
    """Test explain_transition helper."""

    def test_valid_transition_explanation(self):
        """Valid transitions get friendly explanations."""
        result = explain_transition(
            LifecycleState.PROPOSED,
            LifecycleState.RATIFIED,
            "Sprint 42 plan",
        )
        assert "Sprint 42 plan" in result
        assert "agreed" in result.lower() or "proceed" in result.lower()

    def test_explanation_with_reason(self):
        """Explanations can include reason."""
        result = explain_transition(
            LifecycleState.NOTICED,
            LifecycleState.DEPRECATED,
            "old task",
            reason="priorities changed",
        )
        assert "old task" in result
        assert "priorities changed" in result


class TestHasLifecycle:
    """Test has_lifecycle helper."""

    def test_object_with_state_returns_true(self):
        """Objects with lifecycle state return True."""
        feature = MockFeature(name="Test", lifecycle_state=LifecycleState.EMERGENT)
        assert has_lifecycle(feature) is True

    def test_object_without_state_returns_false(self):
        """Objects without lifecycle state return False."""
        todo = MockTodo(title="Test")
        assert has_lifecycle(todo) is False

    def test_object_with_none_state_returns_false(self):
        """Objects with None lifecycle state return False."""
        feature = MockFeature(name="Test", lifecycle_state=None)
        assert has_lifecycle(feature) is False


class TestGetLifecycleState:
    """Test get_lifecycle_state helper."""

    def test_returns_state_when_present(self):
        """Returns state when object has one."""
        feature = MockFeature(name="Test", lifecycle_state=LifecycleState.COMPOSTED)
        assert get_lifecycle_state(feature) == LifecycleState.COMPOSTED

    def test_returns_none_when_no_attribute(self):
        """Returns None when object lacks lifecycle_state attribute."""
        todo = MockTodo(title="Test")
        assert get_lifecycle_state(todo) is None

    def test_returns_none_when_none(self):
        """Returns None when lifecycle_state is explicitly None."""
        feature = MockFeature(name="Test", lifecycle_state=None)
        assert get_lifecycle_state(feature) is None


class TestWiringFromHandlers:
    """Test that lifecycle module is importable from handler context."""

    def test_lifecycle_state_importable(self):
        """LifecycleState can be imported (wiring test)."""
        from services.mux.lifecycle import LifecycleState

        assert hasattr(LifecycleState.EMERGENT, "experience_phrase")

    def test_transition_explanation_callable(self):
        """transition_explanation is callable (wiring test)."""
        from services.mux.lifecycle import transition_explanation

        assert callable(transition_explanation)

    def test_composting_narrative_callable(self):
        """get_composting_narrative is callable (wiring test)."""
        from services.mux.lifecycle import get_composting_narrative

        assert callable(get_composting_narrative)

    def test_integration_helpers_importable(self):
        """Integration helpers are importable (wiring test)."""
        from services.mux.lifecycle_integration import describe_with_lifecycle, has_lifecycle

        assert callable(describe_with_lifecycle)
        assert callable(has_lifecycle)
