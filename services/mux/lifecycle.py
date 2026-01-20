"""
Lifecycle State Machine with Composting.

This module implements the 8-stage lifecycle for objects in the MUX-VISION model:
EMERGENT → DERIVED → NOTICED → PROPOSED → RATIFIED → DEPRECATED → ARCHIVED → COMPOSTED

"Nothing disappears, it transforms."

The lifecycle represents how ideas, tasks, and decisions mature through a system:
- Objects begin as EMERGENT (first stirrings)
- Progress through recognition and formalization
- Eventually decompose into COMPOSTED nourishment for new ideas

References:
- ADR-055: Object Model Implementation
- MUX-399-P3: Lifecycle State Machine
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol, Set, runtime_checkable


class LifecycleState(Enum):
    """
    The 8 stages of an object's lifecycle.

    Each state represents a phase of consciousness:
    - EMERGENT: First stirrings, not yet formed
    - DERIVED: Pattern recognized from emergence
    - NOTICED: Brought to attention, considered
    - PROPOSED: Formally recommended for adoption
    - RATIFIED: Officially accepted and active
    - DEPRECATED: Marked for retirement
    - ARCHIVED: Preserved but inactive
    - COMPOSTED: Transformed into nourishment for new growth
    """

    EMERGENT = "emergent"
    DERIVED = "derived"
    NOTICED = "noticed"
    PROPOSED = "proposed"
    RATIFIED = "ratified"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    COMPOSTED = "composted"

    @property
    def meaning(self) -> str:
        """What this state means in the lifecycle journey."""
        meanings = {
            LifecycleState.EMERGENT: (
                "First stirrings of formation - an idea is forming in the collective consciousness"
            ),
            LifecycleState.DERIVED: (
                "Pattern derived from emergence - recognized as a distinct entity"
            ),
            LifecycleState.NOTICED: (
                "Brought to attention - someone or something has noticed this matters"
            ),
            LifecycleState.PROPOSED: (
                "Formally proposed for consideration - a recommendation has been made"
            ),
            LifecycleState.RATIFIED: (
                "Officially ratified and accepted - now part of the active system"
            ),
            LifecycleState.DEPRECATED: ("Marked as deprecated - scheduled for retirement"),
            LifecycleState.ARCHIVED: ("Preserved in the archive - inactive but not forgotten"),
            LifecycleState.COMPOSTED: (
                "Transformed into nourishment - wisdom extracted for future growth"
            ),
        }
        return meanings[self]

    @property
    def experience_phrase(self) -> str:
        """How Piper expresses experiencing objects in this state."""
        phrases = {
            LifecycleState.EMERGENT: (
                "I sense something forming, though its shape is not yet clear"
            ),
            LifecycleState.DERIVED: ("I recognize a pattern emerging from the noise"),
            LifecycleState.NOTICED: ("This has caught my attention - it seems significant"),
            LifecycleState.PROPOSED: ("I am considering this proposal for its merits"),
            LifecycleState.RATIFIED: ("This is now part of our established reality"),
            LifecycleState.DEPRECATED: ("This served us well, but its time is passing"),
            LifecycleState.ARCHIVED: ("This rests in memory, preserved though no longer active"),
            LifecycleState.COMPOSTED: ("This has transformed into nourishment for future growth"),
        }
        return phrases[self]

    @property
    def typical_objects(self) -> List[str]:
        """Types of objects typically found in this state."""
        objects = {
            LifecycleState.EMERGENT: [
                "draft ideas",
                "fleeting thoughts",
                "unstructured notes",
                "initial signals",
            ],
            LifecycleState.DERIVED: [
                "recognized patterns",
                "extracted themes",
                "identified trends",
                "synthesized insights",
            ],
            LifecycleState.NOTICED: [
                "flagged items",
                "attention requests",
                "prioritized concerns",
                "acknowledged issues",
            ],
            LifecycleState.PROPOSED: [
                "feature requests",
                "RFC documents",
                "decision proposals",
                "change requests",
            ],
            LifecycleState.RATIFIED: [
                "active policies",
                "approved features",
                "accepted standards",
                "official decisions",
            ],
            LifecycleState.DEPRECATED: [
                "legacy features",
                "sunset APIs",
                "retiring processes",
                "phasing-out practices",
            ],
            LifecycleState.ARCHIVED: [
                "historical records",
                "past decisions",
                "completed projects",
                "reference documents",
            ],
            LifecycleState.COMPOSTED: [
                "lessons learned",
                "extracted wisdom",
                "pattern insights",
                "retrospective findings",
            ],
        }
        return objects[self]


# =============================================================================
# Transition Rules
# =============================================================================

VALID_TRANSITIONS: Dict[LifecycleState, Set[LifecycleState]] = {
    LifecycleState.EMERGENT: {LifecycleState.DERIVED, LifecycleState.NOTICED},
    LifecycleState.DERIVED: {LifecycleState.NOTICED, LifecycleState.DEPRECATED},
    LifecycleState.NOTICED: {LifecycleState.PROPOSED, LifecycleState.DEPRECATED},
    LifecycleState.PROPOSED: {LifecycleState.RATIFIED, LifecycleState.DEPRECATED},
    LifecycleState.RATIFIED: {LifecycleState.DEPRECATED},
    LifecycleState.DEPRECATED: {LifecycleState.ARCHIVED},
    LifecycleState.ARCHIVED: {LifecycleState.COMPOSTED},
    LifecycleState.COMPOSTED: set(),  # Terminal state - nothing beyond compost
}


class InvalidTransitionError(Exception):
    """
    Raised when an invalid lifecycle transition is attempted.

    Objects follow a forward-only lifecycle. You cannot:
    - Go backward (e.g., RATIFIED → PROPOSED)
    - Skip stages without valid paths
    - Resurrect from COMPOSTED
    """

    def __init__(self, from_state: LifecycleState, to_state: LifecycleState):
        self.from_state = from_state
        self.to_state = to_state
        super().__init__(
            f"Invalid transition: {from_state.value} → {to_state.value}. "
            f"Valid transitions from {from_state.value}: "
            f"{[s.value for s in VALID_TRANSITIONS[from_state]]}"
        )


@dataclass(frozen=True)
class LifecycleTransition:
    """
    Represents a transition between lifecycle states.

    Captures:
    - from_state: The state being left
    - to_state: The state being entered
    - reason: Why the transition occurred (optional)
    - timestamp: When the transition occurred (auto-set)

    Example:
        transition = LifecycleTransition(
            from_state=LifecycleState.PROPOSED,
            to_state=LifecycleState.RATIFIED,
            reason="Approved by architecture review"
        )
    """

    from_state: LifecycleState
    to_state: LifecycleState
    reason: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def is_valid(self) -> bool:
        """Check if this transition follows valid lifecycle rules."""
        # Same state is not a valid transition
        if self.from_state == self.to_state:
            return False

        # Check against valid transitions
        return self.to_state in VALID_TRANSITIONS[self.from_state]


# =============================================================================
# HasLifecycle Protocol
# =============================================================================


@runtime_checkable
class HasLifecycle(Protocol):
    """
    Protocol for objects with lifecycle awareness.

    Any object can satisfy this protocol by providing:
    - lifecycle_state: Current state in the lifecycle
    - lifecycle_history: Record of past transitions

    Example:
        class MyTask:
            @property
            def lifecycle_state(self) -> LifecycleState:
                return self._state

            @property
            def lifecycle_history(self) -> List[LifecycleTransition]:
                return self._history

        task = MyTask()
        assert isinstance(task, HasLifecycle)  # True
    """

    @property
    def lifecycle_state(self) -> LifecycleState:
        """The current lifecycle state of this object."""
        ...

    @property
    def lifecycle_history(self) -> List[LifecycleTransition]:
        """The history of lifecycle transitions for this object."""
        ...


# =============================================================================
# LifecycleManager
# =============================================================================


class LifecycleManager:
    """
    Manages lifecycle transitions for objects.

    The manager:
    - Validates transitions against rules
    - Updates object state on valid transitions
    - Records transition history
    - Optionally calls event callbacks

    Example:
        manager = LifecycleManager()
        obj = MyLifecycleObject(state=LifecycleState.EMERGENT)

        manager.transition(obj, LifecycleState.DERIVED)
        assert obj.lifecycle_state == LifecycleState.DERIVED
    """

    def transition(
        self,
        obj: Any,
        to_state: LifecycleState,
        reason: Optional[str] = None,
        on_transition: Optional[Callable[[LifecycleTransition], None]] = None,
    ) -> bool:
        """
        Transition an object to a new lifecycle state.

        Args:
            obj: Object implementing HasLifecycle-like interface
            to_state: The target state
            reason: Why the transition is happening (optional)
            on_transition: Callback after successful transition (optional)

        Returns:
            True if transition succeeded

        Raises:
            InvalidTransitionError: If the transition is not valid
        """
        from_state = obj.lifecycle_state

        # Create transition record
        transition = LifecycleTransition(
            from_state=from_state,
            to_state=to_state,
            reason=reason,
        )

        # Validate
        if not transition.is_valid():
            raise InvalidTransitionError(from_state, to_state)

        # Execute transition
        obj.lifecycle_state = to_state

        # Record history
        if hasattr(obj, "add_history"):
            obj.add_history(transition)
        elif hasattr(obj, "_history"):
            obj._history.append(transition)

        # Call callback if provided
        if on_transition:
            on_transition(transition)

        return True


# =============================================================================
# Composting Integration
# =============================================================================


@dataclass
class CompostResult:
    """
    The result of composting an object.

    "Nothing disappears, it transforms."

    Contains:
    - object_summary: Key attributes preserved from the original
    - journey: The lifecycle states traversed
    - lessons: Wisdom extracted from the object's existence
    - composted_at: When the composting occurred
    """

    object_summary: Dict[str, Any]
    journey: List[LifecycleState]
    lessons: List[str]
    composted_at: datetime


class CompostingExtractor:
    """
    Extracts wisdom from objects entering the COMPOSTED state.

    The extractor:
    - Captures key object attributes as summary
    - Records the lifecycle journey taken
    - Generates lessons learned from the object's existence
    - Timestamps the transformation

    This enables:
    - Learning from completed/failed work
    - Pattern recognition across composted objects
    - Feeding insights back into new emergent ideas

    Example:
        extractor = CompostingExtractor()
        result = extractor.extract(old_feature)
        for lesson in result.lessons:
            print(f"Learned: {lesson}")
    """

    # Attributes to look for when summarizing objects
    SUMMARY_ATTRIBUTES = [
        "id",
        "title",
        "name",
        "description",
        "type",
        "category",
        "created_at",
        "updated_at",
        "owner",
        "status",
    ]

    def extract(self, obj: Any) -> CompostResult:
        """
        Extract wisdom from an object for composting.

        Args:
            obj: Object to compost (should implement HasLifecycle)

        Returns:
            CompostResult containing preserved wisdom
        """
        object_summary = self._extract_summary(obj)
        journey = self._extract_journey(obj)
        lessons = self._generate_lessons(obj, journey)

        return CompostResult(
            object_summary=object_summary,
            journey=journey,
            lessons=lessons,
            composted_at=datetime.now(),
        )

    def _extract_summary(self, obj: Any) -> Dict[str, Any]:
        """Extract key attributes from the object."""
        summary = {}

        for attr in self.SUMMARY_ATTRIBUTES:
            if hasattr(obj, attr):
                value = getattr(obj, attr)
                # Convert datetime to string for serialization
                if isinstance(value, datetime):
                    value = value.isoformat()
                summary[attr] = value

        return summary

    def _extract_journey(self, obj: Any) -> List[LifecycleState]:
        """Extract the lifecycle journey from history."""
        if not hasattr(obj, "lifecycle_history"):
            return [obj.lifecycle_state] if hasattr(obj, "lifecycle_state") else []

        history = obj.lifecycle_history
        if not history:
            return [obj.lifecycle_state] if hasattr(obj, "lifecycle_state") else []

        # Build journey from history
        journey = [history[0].from_state]
        for transition in history:
            journey.append(transition.to_state)

        return journey

    def _generate_lessons(self, obj: Any, journey: List[LifecycleState]) -> List[str]:
        """Generate lessons learned from the object's lifecycle."""
        lessons = []

        # Lesson from journey length
        if len(journey) >= 7:
            lessons.append("This object completed a full lifecycle - patterns are worth studying")
        elif len(journey) <= 2:
            lessons.append("Short lifecycle - consider what caused early deprecation")

        # Lesson from reaching ratified
        if LifecycleState.RATIFIED in journey:
            lessons.append("Successfully ratified - this approach was validated")

        # Lesson from skipping states
        if (
            LifecycleState.EMERGENT in journey
            and LifecycleState.NOTICED in journey
            and LifecycleState.DERIVED not in journey
        ):
            lessons.append("Skipped derivation - sometimes direct noticing is efficient")

        # Ensure at least one lesson
        if not lessons:
            lessons.append("Every object teaches something through its existence")

        return lessons
