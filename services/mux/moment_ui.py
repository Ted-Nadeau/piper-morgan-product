"""
Moment UI - How Moments appear in the interface.

Part of #418 MUX-INTERACT-MOMENT-UI.

This module provides:
- MomentType: 10 types from ADR-046
- RenderedMoment: UI representation of a Moment
- MomentLifecycle: State machine for Moment display
- Type-specific renderers for theatrical framing

Design Principle: Moments aren't notifications. They're scenes
in the user's workflow story. Each Moment offers context,
significance, and agency (actions the user can take).

References:
- ADR-046: Moment.type Agent Architecture
- ADR-055: Object Model Implementation
- consciousness-philosophy.md: Theatrical framing
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol

from .protocols import MomentProtocol

# =============================================================================
# MomentType Enum (ADR-046)
# =============================================================================


class MomentType(str, Enum):
    """
    10 Moment types from ADR-046.

    Each type represents a category of significant occurrence
    with specialized processing and presentation.
    """

    CAPABILITY = "capability"  # What Piper can do
    EPIC = "epic"  # Large goal/theme
    RULE = "rule"  # Constraint/guideline
    ASSERTION = "assertion"  # Piper's hypothesis
    QUESTION = "question"  # Clarification needed
    ISSUE = "issue"  # Problem detected
    PERMISSION = "permission"  # Authorization needed
    SCHEMA = "schema"  # Structure definition
    EVENT = "event"  # Something happened
    FUNCTION = "function"  # Action to execute


# =============================================================================
# Moment Lifecycle
# =============================================================================


class MomentLifecycle(str, Enum):
    """
    Lifecycle states for Moment display.

    Moments progress through states as users interact:
    EMERGING → PRESENT → (RESOLVED | DEFERRED)
    """

    EMERGING = "emerging"  # Moment appearing (animation)
    PRESENT = "present"  # User can interact
    RESOLVED = "resolved"  # User took action, Moment complete
    DEFERRED = "deferred"  # User saved for later
    DISMISSED = "dismissed"  # User dismissed without action


# =============================================================================
# Urgency and Visual Weight
# =============================================================================


class Urgency(str, Enum):
    """
    Urgency levels affect placement and visual treatment.

    - AMBIENT: Subtle, peripheral (sidebar, passive feed)
    - NOTABLE: Normal weight (inline in conversation)
    - URGENT: Prominent, interrupting (modal or banner)
    """

    AMBIENT = "ambient"
    NOTABLE = "notable"
    URGENT = "urgent"


class VisualWeight(str, Enum):
    """
    Visual weight affects styling intensity.
    """

    SUBTLE = "subtle"
    NORMAL = "normal"
    PROMINENT = "prominent"


# =============================================================================
# Action Model
# =============================================================================


@dataclass
class MomentAction:
    """
    An action the user can take on a Moment.

    Actions offer agency - they let users respond to Moments
    rather than just receiving information.
    """

    label: str  # Display text: "Answer", "Let's fix it"
    action_type: str  # Type: "reply", "engage", "defer", "dismiss", "expand"
    payload: Dict[str, Any] = field(default_factory=dict)

    # Optional metadata
    is_destructive: bool = False  # Red styling
    requires_confirmation: bool = False


# =============================================================================
# RenderedMoment
# =============================================================================


@dataclass
class RenderedMoment:
    """
    A Moment ready for UI display.

    Transforms internal Moment representation into
    something the UI can render with theatrical framing.

    Theatrical framing means:
    - Context: What situation is this about?
    - Significance: Why does this matter now?
    - Agency: What can the user do about it?
    """

    # Identity
    moment_id: str
    moment_type: MomentType
    lifecycle: MomentLifecycle = MomentLifecycle.EMERGING

    # Core content (theatrical framing)
    headline: str = ""  # "There's something happening..."
    context: str = ""  # Brief situational context
    significance: str = ""  # Why this matters now

    # Visual treatment
    urgency: Urgency = Urgency.NOTABLE
    visual_weight: VisualWeight = VisualWeight.NORMAL

    # Actions (agency)
    primary_action: Optional[MomentAction] = None
    secondary_actions: List[MomentAction] = field(default_factory=list)

    # Theatrical elements
    can_defer: bool = True  # Can user "save for later"?
    has_resolution: bool = True  # Does this Moment complete?

    # Timestamps
    emerged_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None

    def transition_to(self, new_state: MomentLifecycle) -> None:
        """
        Transition to a new lifecycle state.

        Valid transitions:
        - EMERGING → PRESENT
        - PRESENT → RESOLVED | DEFERRED | DISMISSED
        """
        valid_transitions = {
            MomentLifecycle.EMERGING: [MomentLifecycle.PRESENT],
            MomentLifecycle.PRESENT: [
                MomentLifecycle.RESOLVED,
                MomentLifecycle.DEFERRED,
                MomentLifecycle.DISMISSED,
            ],
        }

        if self.lifecycle in valid_transitions:
            if new_state in valid_transitions[self.lifecycle]:
                self.lifecycle = new_state
                if new_state in (
                    MomentLifecycle.RESOLVED,
                    MomentLifecycle.DISMISSED,
                ):
                    self.resolved_at = datetime.now()
                return

        raise ValueError(f"Invalid transition: {self.lifecycle.value} → {new_state.value}")

    @property
    def is_actionable(self) -> bool:
        """Check if user can interact with this Moment."""
        return self.lifecycle == MomentLifecycle.PRESENT

    @property
    def is_complete(self) -> bool:
        """Check if Moment has reached a terminal state."""
        return self.lifecycle in (
            MomentLifecycle.RESOLVED,
            MomentLifecycle.DISMISSED,
        )


# =============================================================================
# Moment Renderer Protocol
# =============================================================================


class MomentRenderer(Protocol):
    """
    Protocol for type-specific Moment renderers.

    Each MomentType has a specialized renderer that knows
    how to transform that type into a RenderedMoment.
    """

    def render(
        self,
        moment: MomentProtocol,
        context: Optional[Dict[str, Any]] = None,
    ) -> RenderedMoment:
        """
        Transform a Moment into its rendered representation.

        Args:
            moment: The Moment to render
            context: Optional context for rendering decisions

        Returns:
            RenderedMoment ready for UI display
        """
        ...


# =============================================================================
# Type-Specific Renderers
# =============================================================================


class CapabilityMomentRenderer:
    """Render Moment.type.capability - What Piper can do."""

    def render(
        self,
        moment: MomentProtocol,
        context: Optional[Dict[str, Any]] = None,
    ) -> RenderedMoment:
        ctx = context or {}
        captures = moment.captures() if hasattr(moment, "captures") else {}

        return RenderedMoment(
            moment_id=moment.id,
            moment_type=MomentType.CAPABILITY,
            headline="Something I can help with",
            context=captures.get("description", ""),
            significance="This might save you some time",
            urgency=Urgency.AMBIENT,
            visual_weight=VisualWeight.SUBTLE,
            primary_action=MomentAction(
                label="Tell me more",
                action_type="expand",
            ),
            secondary_actions=[
                MomentAction(label="Not now", action_type="dismiss"),
            ],
            can_defer=True,
            has_resolution=False,  # Capabilities don't "complete"
        )


class EpicMomentRenderer:
    """Render Moment.type.epic - Large goal/theme."""

    def render(
        self,
        moment: MomentProtocol,
        context: Optional[Dict[str, Any]] = None,
    ) -> RenderedMoment:
        ctx = context or {}
        captures = moment.captures() if hasattr(moment, "captures") else {}

        return RenderedMoment(
            moment_id=moment.id,
            moment_type=MomentType.EPIC,
            headline="A larger goal we're working toward",
            context=captures.get("description", ""),
            significance=captures.get("why_matters", "This frames our work"),
            urgency=Urgency.NOTABLE,
            visual_weight=VisualWeight.PROMINENT,
            primary_action=MomentAction(
                label="See the plan",
                action_type="expand",
            ),
            secondary_actions=[
                MomentAction(label="Update progress", action_type="engage"),
                MomentAction(label="Later", action_type="defer"),
            ],
            can_defer=True,
            has_resolution=True,
        )


class RuleMomentRenderer:
    """Render Moment.type.rule - Constraint/guideline."""

    def render(
        self,
        moment: MomentProtocol,
        context: Optional[Dict[str, Any]] = None,
    ) -> RenderedMoment:
        ctx = context or {}
        captures = moment.captures() if hasattr(moment, "captures") else {}

        return RenderedMoment(
            moment_id=moment.id,
            moment_type=MomentType.RULE,
            headline="Something to keep in mind",
            context=captures.get("description", ""),
            significance=captures.get("applies_when", "This is a guideline"),
            urgency=Urgency.AMBIENT,
            visual_weight=VisualWeight.SUBTLE,
            primary_action=MomentAction(
                label="Got it",
                action_type="acknowledge",
            ),
            secondary_actions=[
                MomentAction(label="Why?", action_type="expand"),
            ],
            can_defer=False,  # Rules are informational
            has_resolution=False,
        )


class AssertionMomentRenderer:
    """Render Moment.type.assertion - Piper's hypothesis."""

    def render(
        self,
        moment: MomentProtocol,
        context: Optional[Dict[str, Any]] = None,
    ) -> RenderedMoment:
        ctx = context or {}
        captures = moment.captures() if hasattr(moment, "captures") else {}

        return RenderedMoment(
            moment_id=moment.id,
            moment_type=MomentType.ASSERTION,
            headline="I think I've noticed something",
            context=captures.get("claim", ""),
            significance=captures.get("evidence", "Based on what I've observed"),
            urgency=Urgency.NOTABLE,
            visual_weight=VisualWeight.NORMAL,
            primary_action=MomentAction(
                label="That's right",
                action_type="confirm",
            ),
            secondary_actions=[
                MomentAction(label="Not quite", action_type="correct"),
                MomentAction(label="Tell me more", action_type="expand"),
            ],
            can_defer=True,
            has_resolution=True,  # User confirms or corrects
        )


class QuestionMomentRenderer:
    """Render Moment.type.question - Clarification needed."""

    def render(
        self,
        moment: MomentProtocol,
        context: Optional[Dict[str, Any]] = None,
    ) -> RenderedMoment:
        ctx = context or {}
        captures = moment.captures() if hasattr(moment, "captures") else {}

        return RenderedMoment(
            moment_id=moment.id,
            moment_type=MomentType.QUESTION,
            headline="I need your input",
            context=captures.get("question", ""),
            significance="This will help me help you better",
            urgency=Urgency.NOTABLE,
            visual_weight=VisualWeight.NORMAL,
            primary_action=MomentAction(
                label="Answer",
                action_type="reply",
            ),
            secondary_actions=[
                MomentAction(label="Skip for now", action_type="defer"),
                MomentAction(label="Not relevant", action_type="dismiss"),
            ],
            can_defer=True,
            has_resolution=True,
        )


class IssueMomentRenderer:
    """Render Moment.type.issue - Problem detected."""

    def render(
        self,
        moment: MomentProtocol,
        context: Optional[Dict[str, Any]] = None,
    ) -> RenderedMoment:
        ctx = context or {}
        captures = moment.captures() if hasattr(moment, "captures") else {}
        is_blocking = captures.get("blocking", False)

        return RenderedMoment(
            moment_id=moment.id,
            moment_type=MomentType.ISSUE,
            headline="Something needs attention",
            context=captures.get("description", ""),
            significance=captures.get("impact", "This could affect our work"),
            urgency=Urgency.URGENT if is_blocking else Urgency.NOTABLE,
            visual_weight=VisualWeight.PROMINENT,
            primary_action=MomentAction(
                label="Let's fix it",
                action_type="engage",
            ),
            secondary_actions=[
                MomentAction(label="Tell me more", action_type="expand"),
                MomentAction(label="I'll handle it", action_type="acknowledge"),
            ],
            can_defer=not is_blocking,
            has_resolution=True,
        )


class PermissionMomentRenderer:
    """Render Moment.type.permission - Authorization needed."""

    def render(
        self,
        moment: MomentProtocol,
        context: Optional[Dict[str, Any]] = None,
    ) -> RenderedMoment:
        ctx = context or {}
        captures = moment.captures() if hasattr(moment, "captures") else {}

        return RenderedMoment(
            moment_id=moment.id,
            moment_type=MomentType.PERMISSION,
            headline="I need your permission",
            context=captures.get("action", ""),
            significance=captures.get("why_needed", "To proceed, I need authorization"),
            urgency=Urgency.NOTABLE,
            visual_weight=VisualWeight.NORMAL,
            primary_action=MomentAction(
                label="Allow",
                action_type="authorize",
            ),
            secondary_actions=[
                MomentAction(label="Deny", action_type="deny"),
                MomentAction(label="Why?", action_type="expand"),
            ],
            can_defer=True,
            has_resolution=True,
        )


class SchemaMomentRenderer:
    """Render Moment.type.schema - Structure definition."""

    def render(
        self,
        moment: MomentProtocol,
        context: Optional[Dict[str, Any]] = None,
    ) -> RenderedMoment:
        ctx = context or {}
        captures = moment.captures() if hasattr(moment, "captures") else {}

        return RenderedMoment(
            moment_id=moment.id,
            moment_type=MomentType.SCHEMA,
            headline="A structure we're working with",
            context=captures.get("description", ""),
            significance=captures.get("purpose", "This defines how data is organized"),
            urgency=Urgency.AMBIENT,
            visual_weight=VisualWeight.SUBTLE,
            primary_action=MomentAction(
                label="View details",
                action_type="expand",
            ),
            secondary_actions=[
                MomentAction(label="Modify", action_type="engage"),
            ],
            can_defer=True,
            has_resolution=False,  # Schemas don't "complete"
        )


class EventMomentRenderer:
    """Render Moment.type.event - Something happened."""

    def render(
        self,
        moment: MomentProtocol,
        context: Optional[Dict[str, Any]] = None,
    ) -> RenderedMoment:
        ctx = context or {}
        captures = moment.captures() if hasattr(moment, "captures") else {}
        requires_action = captures.get("requires_action", False)

        return RenderedMoment(
            moment_id=moment.id,
            moment_type=MomentType.EVENT,
            headline="Something happened",
            context=captures.get("description", ""),
            significance=captures.get("why_matters", "You might want to know about this"),
            urgency=Urgency.NOTABLE if requires_action else Urgency.AMBIENT,
            visual_weight=VisualWeight.NORMAL if requires_action else VisualWeight.SUBTLE,
            primary_action=(
                MomentAction(
                    label="See details",
                    action_type="expand",
                )
                if requires_action
                else None
            ),
            secondary_actions=[
                MomentAction(label="Acknowledge", action_type="acknowledge"),
            ],
            can_defer=True,
            has_resolution=requires_action,
        )


class FunctionMomentRenderer:
    """Render Moment.type.function - Action to execute."""

    def render(
        self,
        moment: MomentProtocol,
        context: Optional[Dict[str, Any]] = None,
    ) -> RenderedMoment:
        ctx = context or {}
        captures = moment.captures() if hasattr(moment, "captures") else {}

        return RenderedMoment(
            moment_id=moment.id,
            moment_type=MomentType.FUNCTION,
            headline="An action I can take",
            context=captures.get("description", ""),
            significance=captures.get("effect", "This will make something happen"),
            urgency=Urgency.NOTABLE,
            visual_weight=VisualWeight.NORMAL,
            primary_action=MomentAction(
                label="Run it",
                action_type="execute",
            ),
            secondary_actions=[
                MomentAction(label="Preview", action_type="expand"),
                MomentAction(label="Cancel", action_type="dismiss"),
            ],
            can_defer=True,
            has_resolution=True,
        )


# =============================================================================
# Renderer Registry
# =============================================================================


MOMENT_RENDERERS: Dict[MomentType, MomentRenderer] = {
    MomentType.CAPABILITY: CapabilityMomentRenderer(),
    MomentType.EPIC: EpicMomentRenderer(),
    MomentType.RULE: RuleMomentRenderer(),
    MomentType.ASSERTION: AssertionMomentRenderer(),
    MomentType.QUESTION: QuestionMomentRenderer(),
    MomentType.ISSUE: IssueMomentRenderer(),
    MomentType.PERMISSION: PermissionMomentRenderer(),
    MomentType.SCHEMA: SchemaMomentRenderer(),
    MomentType.EVENT: EventMomentRenderer(),
    MomentType.FUNCTION: FunctionMomentRenderer(),
}


def render_moment(
    moment: MomentProtocol,
    moment_type: MomentType,
    context: Optional[Dict[str, Any]] = None,
) -> RenderedMoment:
    """
    Transform an internal Moment to UI representation.

    Uses the appropriate type-specific renderer.

    Args:
        moment: The Moment to render
        moment_type: The type of Moment (determines renderer)
        context: Optional context for rendering decisions

    Returns:
        RenderedMoment ready for UI display
    """
    renderer = MOMENT_RENDERERS.get(moment_type)
    if renderer is None:
        raise ValueError(f"No renderer for MomentType: {moment_type}")

    return renderer.render(moment, context)


# =============================================================================
# Situation Rendering (Grouped Moments)
# =============================================================================


@dataclass
class RenderedSituation:
    """
    Multiple related Moments rendered as a coherent scene.

    Situations can collapse/expand, showing Moments as a group.

    Example: "Morning orientation"
    ├── Your calendar today (event)
    ├── Standup in 30 min (event)
    ├── PR needs review (issue)
    └── What's your focus? (question)
    """

    situation_id: str
    title: str  # "Morning orientation"
    description: str = ""
    moments: List[RenderedMoment] = field(default_factory=list)

    # Collapse state
    is_collapsed: bool = False

    # Aggregate urgency (highest of children)
    @property
    def urgency(self) -> Urgency:
        """Return highest urgency among moments."""
        if not self.moments:
            return Urgency.AMBIENT

        urgency_order = [Urgency.AMBIENT, Urgency.NOTABLE, Urgency.URGENT]
        max_index = 0
        for m in self.moments:
            try:
                idx = urgency_order.index(m.urgency)
                max_index = max(max_index, idx)
            except ValueError:
                pass
        return urgency_order[max_index]

    @property
    def pending_count(self) -> int:
        """Count moments awaiting action."""
        return sum(1 for m in self.moments if m.is_actionable)

    @property
    def has_urgent(self) -> bool:
        """Check if any moment is urgent."""
        return any(m.urgency == Urgency.URGENT for m in self.moments)
