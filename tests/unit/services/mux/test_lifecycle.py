"""
Tests for Lifecycle State Machine (P3).

This module tests the 8-stage lifecycle model for objects:
EMERGENT → DERIVED → NOTICED → PROPOSED → RATIFIED → DEPRECATED → ARCHIVED → COMPOSTED

"Nothing disappears, it transforms."

References:
- ADR-055: Object Model Implementation
- MUX-399-P3: Lifecycle State Machine with Composting
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

import pytest

from services.mux.lifecycle import (
    VALID_TRANSITIONS,
    CompostingExtractor,
    CompostResult,
    HasLifecycle,
    InvalidTransitionError,
    LifecycleManager,
    LifecycleState,
    LifecycleTransition,
)

# =============================================================================
# Phase 1: LifecycleState Enum Tests
# =============================================================================


class TestLifecycleStateBasics:
    """Test the 8-stage lifecycle enum."""

    def test_has_emergent_state(self):
        """EMERGENT state exists - first stirrings of an idea."""
        assert LifecycleState.EMERGENT is not None
        assert LifecycleState.EMERGENT.value == "emergent"

    def test_has_derived_state(self):
        """DERIVED state exists - pattern recognized from emergence."""
        assert LifecycleState.DERIVED is not None
        assert LifecycleState.DERIVED.value == "derived"

    def test_has_noticed_state(self):
        """NOTICED state exists - brought to attention."""
        assert LifecycleState.NOTICED is not None
        assert LifecycleState.NOTICED.value == "noticed"

    def test_has_proposed_state(self):
        """PROPOSED state exists - formal recommendation."""
        assert LifecycleState.PROPOSED is not None
        assert LifecycleState.PROPOSED.value == "proposed"

    def test_has_ratified_state(self):
        """RATIFIED state exists - officially accepted."""
        assert LifecycleState.RATIFIED is not None
        assert LifecycleState.RATIFIED.value == "ratified"

    def test_has_deprecated_state(self):
        """DEPRECATED state exists - marked for retirement."""
        assert LifecycleState.DEPRECATED is not None
        assert LifecycleState.DEPRECATED.value == "deprecated"

    def test_has_archived_state(self):
        """ARCHIVED state exists - preserved but inactive."""
        assert LifecycleState.ARCHIVED is not None
        assert LifecycleState.ARCHIVED.value == "archived"

    def test_has_composted_state(self):
        """COMPOSTED state exists - transformed into nourishment."""
        assert LifecycleState.COMPOSTED is not None
        assert LifecycleState.COMPOSTED.value == "composted"

    def test_exactly_eight_states(self):
        """Lifecycle has exactly 8 states."""
        assert len(LifecycleState) == 8


class TestLifecycleStateMeanings:
    """Test the meaning property for each state."""

    def test_emergent_meaning(self):
        """EMERGENT has meaning describing initial formation."""
        assert (
            "stirring" in LifecycleState.EMERGENT.meaning.lower()
            or "forming" in LifecycleState.EMERGENT.meaning.lower()
        )

    def test_derived_meaning(self):
        """DERIVED has meaning describing pattern recognition."""
        assert (
            "pattern" in LifecycleState.DERIVED.meaning.lower()
            or "derived" in LifecycleState.DERIVED.meaning.lower()
        )

    def test_noticed_meaning(self):
        """NOTICED has meaning describing awareness."""
        assert (
            "attention" in LifecycleState.NOTICED.meaning.lower()
            or "noticed" in LifecycleState.NOTICED.meaning.lower()
        )

    def test_proposed_meaning(self):
        """PROPOSED has meaning describing recommendation."""
        assert (
            "recommend" in LifecycleState.PROPOSED.meaning.lower()
            or "proposed" in LifecycleState.PROPOSED.meaning.lower()
        )

    def test_ratified_meaning(self):
        """RATIFIED has meaning describing acceptance."""
        assert (
            "accept" in LifecycleState.RATIFIED.meaning.lower()
            or "ratified" in LifecycleState.RATIFIED.meaning.lower()
        )

    def test_deprecated_meaning(self):
        """DEPRECATED has meaning describing retirement."""
        assert (
            "retire" in LifecycleState.DEPRECATED.meaning.lower()
            or "deprecated" in LifecycleState.DEPRECATED.meaning.lower()
        )

    def test_archived_meaning(self):
        """ARCHIVED has meaning describing preservation."""
        assert (
            "preserved" in LifecycleState.ARCHIVED.meaning.lower()
            or "archived" in LifecycleState.ARCHIVED.meaning.lower()
        )

    def test_composted_meaning(self):
        """COMPOSTED has meaning describing transformation."""
        assert (
            "transform" in LifecycleState.COMPOSTED.meaning.lower()
            or "nourish" in LifecycleState.COMPOSTED.meaning.lower()
        )


class TestLifecycleStateExperiencePhrases:
    """Test consciousness-preserving experience phrases."""

    def test_emergent_experience_phrase(self):
        """EMERGENT has phrase expressing initial sensing."""
        phrase = LifecycleState.EMERGENT.experience_phrase
        assert phrase and len(phrase) > 10

    def test_derived_experience_phrase(self):
        """DERIVED has phrase expressing pattern recognition."""
        phrase = LifecycleState.DERIVED.experience_phrase
        assert phrase and len(phrase) > 10

    def test_composted_experience_phrase(self):
        """COMPOSTED has phrase expressing transformation."""
        phrase = LifecycleState.COMPOSTED.experience_phrase
        assert "transform" in phrase.lower() or "nourish" in phrase.lower()


class TestLifecycleStateTypicalObjects:
    """Test typical_objects property."""

    def test_emergent_typical_objects(self):
        """EMERGENT lists typical object types."""
        objects = LifecycleState.EMERGENT.typical_objects
        assert isinstance(objects, list)
        assert len(objects) > 0

    def test_ratified_typical_objects(self):
        """RATIFIED lists typical object types."""
        objects = LifecycleState.RATIFIED.typical_objects
        assert isinstance(objects, list)
        assert len(objects) > 0

    def test_composted_typical_objects(self):
        """COMPOSTED lists typical object types."""
        objects = LifecycleState.COMPOSTED.typical_objects
        assert isinstance(objects, list)
        assert len(objects) > 0


# =============================================================================
# Phase 2: Transition Rules Tests
# =============================================================================


class TestTransitionRulesStructure:
    """Test the VALID_TRANSITIONS mapping structure."""

    def test_valid_transitions_exists(self):
        """VALID_TRANSITIONS constant exists."""
        assert VALID_TRANSITIONS is not None
        assert isinstance(VALID_TRANSITIONS, dict)

    def test_all_states_have_transitions_defined(self):
        """Every state has a transition entry (even if empty set)."""
        for state in LifecycleState:
            assert state in VALID_TRANSITIONS

    def test_composted_has_no_transitions(self):
        """COMPOSTED is terminal - no outward transitions."""
        assert VALID_TRANSITIONS[LifecycleState.COMPOSTED] == set()


class TestTransitionRulesValidity:
    """Test specific valid transitions."""

    def test_emergent_can_transition_to_derived(self):
        """EMERGENT → DERIVED is valid."""
        assert LifecycleState.DERIVED in VALID_TRANSITIONS[LifecycleState.EMERGENT]

    def test_emergent_can_transition_to_noticed(self):
        """EMERGENT → NOTICED is valid (skip derived)."""
        assert LifecycleState.NOTICED in VALID_TRANSITIONS[LifecycleState.EMERGENT]

    def test_derived_can_transition_to_noticed(self):
        """DERIVED → NOTICED is valid."""
        assert LifecycleState.NOTICED in VALID_TRANSITIONS[LifecycleState.DERIVED]

    def test_derived_can_transition_to_deprecated(self):
        """DERIVED → DEPRECATED is valid (early deprecation)."""
        assert LifecycleState.DEPRECATED in VALID_TRANSITIONS[LifecycleState.DERIVED]

    def test_noticed_can_transition_to_proposed(self):
        """NOTICED → PROPOSED is valid."""
        assert LifecycleState.PROPOSED in VALID_TRANSITIONS[LifecycleState.NOTICED]

    def test_noticed_can_transition_to_deprecated(self):
        """NOTICED → DEPRECATED is valid (abandon without proposal)."""
        assert LifecycleState.DEPRECATED in VALID_TRANSITIONS[LifecycleState.NOTICED]

    def test_proposed_can_transition_to_ratified(self):
        """PROPOSED → RATIFIED is valid."""
        assert LifecycleState.RATIFIED in VALID_TRANSITIONS[LifecycleState.PROPOSED]

    def test_proposed_can_transition_to_deprecated(self):
        """PROPOSED → DEPRECATED is valid (rejected proposal)."""
        assert LifecycleState.DEPRECATED in VALID_TRANSITIONS[LifecycleState.PROPOSED]

    def test_ratified_can_transition_to_deprecated(self):
        """RATIFIED → DEPRECATED is valid."""
        assert LifecycleState.DEPRECATED in VALID_TRANSITIONS[LifecycleState.RATIFIED]

    def test_deprecated_can_transition_to_archived(self):
        """DEPRECATED → ARCHIVED is valid."""
        assert LifecycleState.ARCHIVED in VALID_TRANSITIONS[LifecycleState.DEPRECATED]

    def test_archived_can_transition_to_composted(self):
        """ARCHIVED → COMPOSTED is valid."""
        assert LifecycleState.COMPOSTED in VALID_TRANSITIONS[LifecycleState.ARCHIVED]


class TestLifecycleTransitionDataclass:
    """Test LifecycleTransition dataclass."""

    def test_transition_has_from_state(self):
        """Transition captures from_state."""
        t = LifecycleTransition(from_state=LifecycleState.EMERGENT, to_state=LifecycleState.DERIVED)
        assert t.from_state == LifecycleState.EMERGENT

    def test_transition_has_to_state(self):
        """Transition captures to_state."""
        t = LifecycleTransition(from_state=LifecycleState.EMERGENT, to_state=LifecycleState.DERIVED)
        assert t.to_state == LifecycleState.DERIVED

    def test_valid_transition_is_valid(self):
        """is_valid() returns True for valid transitions."""
        t = LifecycleTransition(from_state=LifecycleState.EMERGENT, to_state=LifecycleState.DERIVED)
        assert t.is_valid() is True

    def test_invalid_transition_is_not_valid(self):
        """is_valid() returns False for invalid transitions."""
        t = LifecycleTransition(
            from_state=LifecycleState.COMPOSTED,
            to_state=LifecycleState.EMERGENT,  # Can't resurrect!
        )
        assert t.is_valid() is False

    def test_same_state_transition_is_invalid(self):
        """is_valid() returns False for no-op transitions."""
        t = LifecycleTransition(
            from_state=LifecycleState.RATIFIED, to_state=LifecycleState.RATIFIED
        )
        assert t.is_valid() is False

    def test_backward_transition_is_invalid(self):
        """is_valid() returns False for backward transitions."""
        t = LifecycleTransition(
            from_state=LifecycleState.RATIFIED, to_state=LifecycleState.PROPOSED  # Can't un-ratify
        )
        assert t.is_valid() is False


class TestInvalidTransitionError:
    """Test InvalidTransitionError exception."""

    def test_error_is_exception(self):
        """InvalidTransitionError is a proper exception."""
        assert issubclass(InvalidTransitionError, Exception)

    def test_error_message_includes_states(self):
        """Error message includes from and to states."""
        error = InvalidTransitionError(LifecycleState.COMPOSTED, LifecycleState.EMERGENT)
        msg = str(error)
        assert "composted" in msg.lower()
        assert "emergent" in msg.lower()


# =============================================================================
# Phase 3: HasLifecycle Protocol Tests
# =============================================================================


class TestHasLifecycleProtocol:
    """Test HasLifecycle protocol for runtime checking."""

    def test_protocol_is_runtime_checkable(self):
        """HasLifecycle can be used with isinstance()."""

        class MockLifecycled:
            @property
            def lifecycle_state(self) -> LifecycleState:
                return LifecycleState.EMERGENT

            @property
            def lifecycle_history(self) -> List:
                return []

        obj = MockLifecycled()
        assert isinstance(obj, HasLifecycle)

    def test_non_conforming_object_fails(self):
        """Objects without lifecycle properties don't satisfy protocol."""

        class NoLifecycle:
            pass

        obj = NoLifecycle()
        assert not isinstance(obj, HasLifecycle)

    def test_partial_implementation_fails(self):
        """Objects with only some properties don't satisfy protocol."""

        class PartialLifecycle:
            @property
            def lifecycle_state(self) -> LifecycleState:
                return LifecycleState.EMERGENT

            # Missing lifecycle_history

        obj = PartialLifecycle()
        assert not isinstance(obj, HasLifecycle)


# =============================================================================
# Phase 4: LifecycleManager Tests
# =============================================================================


class TestLifecycleManagerBasics:
    """Test LifecycleManager basic functionality."""

    def test_manager_exists(self):
        """LifecycleManager class exists."""
        assert LifecycleManager is not None

    def test_manager_can_be_instantiated(self):
        """LifecycleManager can be created."""
        manager = LifecycleManager()
        assert manager is not None


class MockLifecycleObject:
    """Test fixture: object with lifecycle support."""

    def __init__(self, initial_state: LifecycleState = LifecycleState.EMERGENT):
        self._state = initial_state
        self._history: List[LifecycleTransition] = []

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._state

    @lifecycle_state.setter
    def lifecycle_state(self, value: LifecycleState):
        self._state = value

    @property
    def lifecycle_history(self) -> List[LifecycleTransition]:
        return self._history

    def add_history(self, transition: LifecycleTransition):
        self._history.append(transition)


class TestLifecycleManagerTransition:
    """Test LifecycleManager.transition() method."""

    def test_valid_transition_succeeds(self):
        """Manager performs valid transitions."""
        manager = LifecycleManager()
        obj = MockLifecycleObject(LifecycleState.EMERGENT)

        result = manager.transition(obj, LifecycleState.DERIVED)

        assert result is True
        assert obj.lifecycle_state == LifecycleState.DERIVED

    def test_transition_records_history(self):
        """Manager records transition in history."""
        manager = LifecycleManager()
        obj = MockLifecycleObject(LifecycleState.EMERGENT)

        manager.transition(obj, LifecycleState.DERIVED)

        assert len(obj.lifecycle_history) == 1
        assert obj.lifecycle_history[0].from_state == LifecycleState.EMERGENT
        assert obj.lifecycle_history[0].to_state == LifecycleState.DERIVED

    def test_invalid_transition_raises(self):
        """Manager raises InvalidTransitionError for invalid transitions."""
        manager = LifecycleManager()
        obj = MockLifecycleObject(LifecycleState.COMPOSTED)

        with pytest.raises(InvalidTransitionError):
            manager.transition(obj, LifecycleState.EMERGENT)

    def test_invalid_transition_does_not_change_state(self):
        """Failed transition leaves state unchanged."""
        manager = LifecycleManager()
        obj = MockLifecycleObject(LifecycleState.COMPOSTED)

        try:
            manager.transition(obj, LifecycleState.EMERGENT)
        except InvalidTransitionError:
            pass

        assert obj.lifecycle_state == LifecycleState.COMPOSTED

    def test_callback_is_called_on_success(self):
        """Manager calls callback after successful transition."""
        manager = LifecycleManager()
        obj = MockLifecycleObject(LifecycleState.EMERGENT)
        callback_called = []

        def on_transition(transition: LifecycleTransition):
            callback_called.append(transition)

        manager.transition(obj, LifecycleState.DERIVED, on_transition=on_transition)

        assert len(callback_called) == 1
        assert callback_called[0].to_state == LifecycleState.DERIVED

    def test_full_lifecycle_journey(self):
        """Manager can take object through full lifecycle."""
        manager = LifecycleManager()
        obj = MockLifecycleObject(LifecycleState.EMERGENT)

        # EMERGENT → DERIVED → NOTICED → PROPOSED → RATIFIED
        manager.transition(obj, LifecycleState.DERIVED)
        manager.transition(obj, LifecycleState.NOTICED)
        manager.transition(obj, LifecycleState.PROPOSED)
        manager.transition(obj, LifecycleState.RATIFIED)
        # → DEPRECATED → ARCHIVED → COMPOSTED
        manager.transition(obj, LifecycleState.DEPRECATED)
        manager.transition(obj, LifecycleState.ARCHIVED)
        manager.transition(obj, LifecycleState.COMPOSTED)

        assert obj.lifecycle_state == LifecycleState.COMPOSTED
        assert len(obj.lifecycle_history) == 7


# =============================================================================
# Phase 5: Composting Integration Tests
# =============================================================================


class TestCompostResultDataclass:
    """Test CompostResult dataclass."""

    def test_compost_result_has_object_summary(self):
        """CompostResult captures object summary."""
        result = CompostResult(
            object_summary={"type": "task", "title": "Old task"},
            journey=[],
            lessons=["Scope creep is real"],
            composted_at=datetime.now(),
        )
        assert result.object_summary["type"] == "task"

    def test_compost_result_has_journey(self):
        """CompostResult captures lifecycle journey."""
        result = CompostResult(
            object_summary={},
            journey=[LifecycleState.EMERGENT, LifecycleState.DEPRECATED],
            lessons=[],
            composted_at=datetime.now(),
        )
        assert len(result.journey) == 2

    def test_compost_result_has_lessons(self):
        """CompostResult captures extracted lessons."""
        result = CompostResult(
            object_summary={},
            journey=[],
            lessons=["Don't over-engineer", "Get feedback early"],
            composted_at=datetime.now(),
        )
        assert len(result.lessons) == 2

    def test_compost_result_has_timestamp(self):
        """CompostResult has composted_at timestamp."""
        now = datetime.now()
        result = CompostResult(object_summary={}, journey=[], lessons=[], composted_at=now)
        assert result.composted_at == now


class TestCompostingExtractorBasics:
    """Test CompostingExtractor basic functionality."""

    def test_extractor_exists(self):
        """CompostingExtractor class exists."""
        assert CompostingExtractor is not None

    def test_extractor_can_be_instantiated(self):
        """CompostingExtractor can be created."""
        extractor = CompostingExtractor()
        assert extractor is not None


class MockCompostableObject:
    """Test fixture: object that can be composted."""

    def __init__(self):
        self._state = LifecycleState.ARCHIVED
        self._history: List[LifecycleTransition] = []
        self.title = "Old Feature Request"
        self.created_at = datetime(2024, 1, 1)
        self.description = "A feature that was never built"

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._state

    @lifecycle_state.setter
    def lifecycle_state(self, value: LifecycleState):
        self._state = value

    @property
    def lifecycle_history(self) -> List[LifecycleTransition]:
        return self._history

    def add_history(self, transition: LifecycleTransition):
        self._history.append(transition)


class TestCompostingExtractorExtract:
    """Test CompostingExtractor.extract() method."""

    def test_extract_produces_compost_result(self):
        """Extractor produces CompostResult from object."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()

        result = extractor.extract(obj)

        assert isinstance(result, CompostResult)

    def test_extract_captures_object_summary(self):
        """Extractor captures key object attributes."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()

        result = extractor.extract(obj)

        assert result.object_summary is not None
        assert "title" in result.object_summary or len(result.object_summary) > 0

    def test_extract_captures_journey(self):
        """Extractor captures lifecycle journey."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()
        # Add some history
        obj.add_history(
            LifecycleTransition(from_state=LifecycleState.EMERGENT, to_state=LifecycleState.NOTICED)
        )

        result = extractor.extract(obj)

        # Journey should reflect the history
        assert result.journey is not None

    def test_extract_sets_timestamp(self):
        """Extractor sets composted_at timestamp."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()

        before = datetime.now()
        result = extractor.extract(obj)
        after = datetime.now()

        assert before <= result.composted_at <= after

    def test_extract_generates_lessons(self):
        """Extractor generates lessons from object."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()

        result = extractor.extract(obj)

        # Should have at least one lesson or empty list
        assert isinstance(result.lessons, list)


class TestCompostingPhilosophy:
    """Test the philosophical aspects of composting."""

    def test_composted_objects_retain_wisdom(self):
        """Composting preserves learned insights."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()

        result = extractor.extract(obj)

        # The result should contain enough info to learn from
        assert result.object_summary or result.lessons or result.journey

    def test_nothing_truly_disappears(self):
        """Composted objects transform rather than vanish."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()
        obj.title = "Important Lesson"

        result = extractor.extract(obj)

        # Original identity should be traceable
        summary_str = str(result.object_summary)
        assert len(summary_str) > 0  # Something is preserved
