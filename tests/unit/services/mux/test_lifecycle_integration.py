"""
Tests for Lifecycle Integration Helpers.

These tests verify that lifecycle-aware language can be integrated
into intent handler responses.
"""

from dataclasses import dataclass
from typing import Optional

import pytest

from services.mux.lifecycle import LifecycleState, LifecycleTransition
from services.mux.lifecycle_integration import (
    FEATURE_STATUS_TO_LIFECYCLE,
    WORKITEM_STATUS_TO_LIFECYCLE,
    describe_with_lifecycle,
    explain_transition,
    format_lifecycle_context,
    get_lifecycle_for_status,
    get_lifecycle_state,
    has_lifecycle,
    initialize_lifecycle,
    sync_lifecycle_to_status,
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


@dataclass
class MockWorkItem:
    """Mock WorkItem with status and lifecycle state for testing status-to-lifecycle mapping."""

    title: str
    status: str = "open"
    lifecycle_state: Optional[LifecycleState] = None

    # Make class name match what get_lifecycle_for_status expects
    @property
    def __class_name__(self):
        return "WorkItem"


# Override __class__.__name__ for MockWorkItem to return "WorkItem"
MockWorkItem.__name__ = "WorkItem"


@dataclass
class MockFeatureWithStatus:
    """Mock Feature with status and lifecycle state for testing status-to-lifecycle mapping."""

    name: str
    status: str = "draft"
    lifecycle_state: Optional[LifecycleState] = None


# Override __class__.__name__ for MockFeatureWithStatus to return "Feature"
MockFeatureWithStatus.__name__ = "Feature"


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


class TestStatusToLifecycleMappings:
    """Test status-to-lifecycle mapping dictionaries."""

    def test_workitem_status_mapping_has_all_statuses(self):
        """WorkItem mapping covers common statuses."""
        assert "open" in WORKITEM_STATUS_TO_LIFECYCLE
        assert "in_progress" in WORKITEM_STATUS_TO_LIFECYCLE
        assert "done" in WORKITEM_STATUS_TO_LIFECYCLE
        assert "closed" in WORKITEM_STATUS_TO_LIFECYCLE

    def test_workitem_open_maps_to_noticed(self):
        """Open WorkItems map to NOTICED state."""
        assert WORKITEM_STATUS_TO_LIFECYCLE["open"] == LifecycleState.NOTICED

    def test_workitem_in_progress_maps_to_ratified(self):
        """In-progress WorkItems map to RATIFIED state."""
        assert WORKITEM_STATUS_TO_LIFECYCLE["in_progress"] == LifecycleState.RATIFIED

    def test_workitem_done_maps_to_deprecated(self):
        """Done WorkItems map to DEPRECATED state."""
        assert WORKITEM_STATUS_TO_LIFECYCLE["done"] == LifecycleState.DEPRECATED

    def test_workitem_closed_maps_to_archived(self):
        """Closed WorkItems map to ARCHIVED state."""
        assert WORKITEM_STATUS_TO_LIFECYCLE["closed"] == LifecycleState.ARCHIVED

    def test_feature_status_mapping_has_all_statuses(self):
        """Feature mapping covers common statuses."""
        assert "draft" in FEATURE_STATUS_TO_LIFECYCLE
        assert "proposed" in FEATURE_STATUS_TO_LIFECYCLE
        assert "approved" in FEATURE_STATUS_TO_LIFECYCLE
        assert "shipped" in FEATURE_STATUS_TO_LIFECYCLE
        assert "archived" in FEATURE_STATUS_TO_LIFECYCLE

    def test_feature_draft_maps_to_emergent(self):
        """Draft Features map to EMERGENT state."""
        assert FEATURE_STATUS_TO_LIFECYCLE["draft"] == LifecycleState.EMERGENT

    def test_feature_proposed_maps_to_proposed(self):
        """Proposed Features map to PROPOSED state."""
        assert FEATURE_STATUS_TO_LIFECYCLE["proposed"] == LifecycleState.PROPOSED

    def test_feature_approved_maps_to_ratified(self):
        """Approved Features map to RATIFIED state."""
        assert FEATURE_STATUS_TO_LIFECYCLE["approved"] == LifecycleState.RATIFIED

    def test_feature_shipped_maps_to_deprecated(self):
        """Shipped Features map to DEPRECATED state."""
        assert FEATURE_STATUS_TO_LIFECYCLE["shipped"] == LifecycleState.DEPRECATED

    def test_feature_archived_maps_to_archived(self):
        """Archived Features map to ARCHIVED state."""
        assert FEATURE_STATUS_TO_LIFECYCLE["archived"] == LifecycleState.ARCHIVED


class TestGetLifecycleForStatus:
    """Test get_lifecycle_for_status helper."""

    def test_workitem_returns_correct_lifecycle(self):
        """WorkItem with status returns appropriate lifecycle."""

        # Create a real-enough mock that class name check works
        @dataclass
        class WorkItem:
            status: str

        item = WorkItem(status="open")
        result = get_lifecycle_for_status(item)
        assert result == LifecycleState.NOTICED

    def test_feature_returns_correct_lifecycle(self):
        """Feature with status returns appropriate lifecycle."""

        @dataclass
        class Feature:
            status: str

        feature = Feature(status="draft")
        result = get_lifecycle_for_status(feature)
        assert result == LifecycleState.EMERGENT

    def test_unknown_status_returns_none(self):
        """Unknown status returns None."""

        @dataclass
        class WorkItem:
            status: str

        item = WorkItem(status="unknown_status")
        result = get_lifecycle_for_status(item)
        assert result is None

    def test_object_without_status_returns_none(self):
        """Object without status attribute returns None."""
        todo = MockTodo(title="Test")
        result = get_lifecycle_for_status(todo)
        assert result is None

    def test_unknown_class_returns_none(self):
        """Unknown class type returns None."""

        @dataclass
        class UnknownType:
            status: str

        obj = UnknownType(status="open")
        result = get_lifecycle_for_status(obj)
        assert result is None


class TestInitializeLifecycle:
    """Test initialize_lifecycle helper."""

    def test_workitem_open_initialized_to_noticed(self):
        """Open WorkItem gets initialized to NOTICED."""

        @dataclass
        class WorkItem:
            status: str
            lifecycle_state: Optional[LifecycleState] = None

        item = WorkItem(status="open")
        result = initialize_lifecycle(item)
        assert result is True
        assert item.lifecycle_state == LifecycleState.NOTICED

    def test_feature_draft_initialized_to_emergent(self):
        """Draft Feature gets initialized to EMERGENT."""

        @dataclass
        class Feature:
            status: str
            lifecycle_state: Optional[LifecycleState] = None

        feature = Feature(status="draft")
        result = initialize_lifecycle(feature)
        assert result is True
        assert feature.lifecycle_state == LifecycleState.EMERGENT

    def test_does_not_overwrite_existing_state(self):
        """Does not overwrite existing lifecycle state."""

        @dataclass
        class WorkItem:
            status: str
            lifecycle_state: Optional[LifecycleState] = None

        item = WorkItem(status="open", lifecycle_state=LifecycleState.RATIFIED)
        result = initialize_lifecycle(item)
        assert result is False
        assert item.lifecycle_state == LifecycleState.RATIFIED  # Unchanged

    def test_returns_false_if_no_lifecycle_attribute(self):
        """Returns False if object has no lifecycle_state attribute."""
        todo = MockTodo(title="Test")
        result = initialize_lifecycle(todo)
        assert result is False

    def test_returns_false_for_unknown_status(self):
        """Returns False if status doesn't map to lifecycle."""

        @dataclass
        class WorkItem:
            status: str
            lifecycle_state: Optional[LifecycleState] = None

        item = WorkItem(status="weird_status")
        result = initialize_lifecycle(item)
        assert result is False
        assert item.lifecycle_state is None


class TestSyncLifecycleToStatus:
    """Test sync_lifecycle_to_status helper."""

    def test_sync_from_none_to_noticed(self):
        """Syncing from None state just sets the state."""

        @dataclass
        class WorkItem:
            status: str
            lifecycle_state: Optional[LifecycleState] = None

        item = WorkItem(status="open")
        result = sync_lifecycle_to_status(item)
        assert result is True
        assert item.lifecycle_state == LifecycleState.NOTICED

    def test_sync_already_correct_returns_false(self):
        """Returns False if already in correct state."""

        @dataclass
        class WorkItem:
            status: str
            lifecycle_state: Optional[LifecycleState] = None

        item = WorkItem(status="open", lifecycle_state=LifecycleState.NOTICED)
        result = sync_lifecycle_to_status(item)
        assert result is False
        assert item.lifecycle_state == LifecycleState.NOTICED

    def test_sync_valid_forward_transition(self):
        """Valid forward transition updates state."""

        @dataclass
        class WorkItem:
            status: str
            lifecycle_state: Optional[LifecycleState] = None

        # NOTICED -> DEPRECATED is valid (when status changes to done)
        item = WorkItem(status="done", lifecycle_state=LifecycleState.NOTICED)
        result = sync_lifecycle_to_status(item)
        assert result is True
        assert item.lifecycle_state == LifecycleState.DEPRECATED

    def test_sync_feature_proposed_to_ratified(self):
        """Feature PROPOSED -> RATIFIED is valid transition."""

        @dataclass
        class Feature:
            status: str
            lifecycle_state: Optional[LifecycleState] = None

        # PROPOSED -> RATIFIED is valid (when feature is approved)
        feature = Feature(status="approved", lifecycle_state=LifecycleState.PROPOSED)
        result = sync_lifecycle_to_status(feature)
        assert result is True
        assert feature.lifecycle_state == LifecycleState.RATIFIED

    def test_sync_skip_requires_intermediate_states(self):
        """Some status changes require intermediate lifecycle states (by design)."""

        @dataclass
        class WorkItem:
            status: str
            lifecycle_state: Optional[LifecycleState] = None

        # NOTICED -> RATIFIED is NOT a valid direct transition
        # (would need to go through PROPOSED first)
        # This is handled gracefully - logged and returns False
        item = WorkItem(status="in_progress", lifecycle_state=LifecycleState.NOTICED)
        result = sync_lifecycle_to_status(item)
        assert result is False  # Transition skipped (not a valid hop)
        assert item.lifecycle_state == LifecycleState.NOTICED  # Unchanged

    def test_sync_invalid_transition_returns_false(self):
        """Invalid transition returns False without crashing."""

        @dataclass
        class WorkItem:
            status: str
            lifecycle_state: Optional[LifecycleState] = None

        # ARCHIVED -> NOTICED would be backward (invalid)
        item = WorkItem(status="open", lifecycle_state=LifecycleState.ARCHIVED)
        result = sync_lifecycle_to_status(item)
        assert result is False
        # State unchanged (invalid transition skipped)
        assert item.lifecycle_state == LifecycleState.ARCHIVED

    def test_sync_unknown_status_returns_false(self):
        """Unknown status returns False."""

        @dataclass
        class WorkItem:
            status: str
            lifecycle_state: Optional[LifecycleState] = None

        item = WorkItem(status="weird", lifecycle_state=LifecycleState.NOTICED)
        result = sync_lifecycle_to_status(item)
        assert result is False

    def test_sync_object_without_status_returns_false(self):
        """Object without status returns False."""
        feature = MockFeature(name="Test", lifecycle_state=LifecycleState.EMERGENT)
        result = sync_lifecycle_to_status(feature)
        assert result is False
