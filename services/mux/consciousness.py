"""
MUX Consciousness Module - Entity Awareness and Expression

This module provides consciousness-related types for the MUX system:
- AwarenessLevel: States of attention (sleeping to overwhelmed)
- EmotionalState: Emotional modes (curious to puzzled)
- EntityRole: Grammatical roles in MUX grammar
- ConsciousnessAttributes: Core consciousness traits for any entity

Part of #434 MUX-TECH-PHASE2-ENTITY.

References:
- ADR-045: Object Model Specification
- ADR-055: Object Model Implementation
- Morning Standup patterns
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class AwarenessLevel(Enum):
    """
    States of entity attention/awareness.

    From PM vision: "Not just on/off but a spectrum of engagement."
    """

    SLEEPING = "sleeping"  # Inactive, not monitoring
    DROWSY = "drowsy"  # Low attention, passive monitoring
    ALERT = "alert"  # Active attention, normal operation
    FOCUSED = "focused"  # Deep attention, high engagement
    OVERWHELMED = "overwhelmed"  # Too much input, degraded function


class EmotionalState(Enum):
    """
    Emotional modes that color perception and expression.

    From PM vision: "I notice" vs "I'm concerned" shows emotional framing.
    """

    CURIOUS = "curious"  # Exploring, questioning
    CONCERNED = "concerned"  # Worried, flagging issues
    SATISFIED = "satisfied"  # Content, things are going well
    PUZZLED = "puzzled"  # Uncertain, needs clarification


class EntityRole(Enum):
    """
    Grammatical roles an entity can play in MUX grammar.

    Key insight: Same entity can be ACTOR in one moment, PLACE in another.
    A Team is both an actor (takes actions) and a place (where work happens).
    """

    ACTOR = "actor"  # Doing something (Entity substrate)
    PLACE = "place"  # Where something happens (Place substrate)
    OBSERVER = "observer"  # Watching something unfold
    PARTICIPANT = "participant"  # Part of something larger


@dataclass
class ConsciousnessAttributes:
    """
    Attributes that make an entity conscious.

    These can be applied to any entity (User, Stakeholder, Team, Piper)
    to give them agency, awareness, and relationships.

    Anti-Flattening Note: These aren't just properties - they're drives
    that influence behavior. wants/fears create motivation.
    """

    # Agency - what drives this entity
    wants: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)

    # Awareness - what this entity perceives
    knows_about: List[str] = field(default_factory=list)
    attention_on: Optional[str] = None
    emotional_state: Optional[EmotionalState] = None

    # Relationships - how this entity connects
    trusts: Dict[str, float] = field(default_factory=dict)  # entity_id -> trust level (0.0-1.0)
    depends_on: List[str] = field(default_factory=list)
    influences: List[str] = field(default_factory=list)

    def is_aware_of(self, topic: str) -> bool:
        """Check if entity knows about a topic."""
        return topic in self.knows_about

    def trust_level(self, entity_id: str) -> float:
        """Get trust level for another entity (default 0.5)."""
        return self.trusts.get(entity_id, 0.5)

    def is_focused(self) -> bool:
        """Check if entity has active attention."""
        return self.attention_on is not None


@dataclass
class Capability:
    """Something an entity can do."""

    name: str
    description: str
    requires: List[str] = field(default_factory=list)  # Dependencies
    blocked_by: Optional[str] = None  # Why it can't be used

    def is_blocked(self) -> bool:
        """Check if this capability is blocked."""
        return self.blocked_by is not None


class TrustLevel(Enum):
    """Trust levels for relationships."""

    UNKNOWN = "unknown"  # No history, cautious
    CAUTIOUS = "cautious"  # Some concern
    STANDARD = "standard"  # Normal trust
    TRUSTED = "trusted"  # High trust
    FULL = "full"  # Complete trust


@dataclass
class PiperEntity:
    """
    Piper as a conscious entity, not just a service collection.

    This is the first-class representation of Piper Morgan as an actor
    with identity, boundaries, and agency. There is only one PiperEntity
    per instance.

    Anti-Flattening Check: A flattened version would be a service registry.
    This version has self-awareness, boundaries, and agency.
    """

    # Identity
    id: str = "piper-prime"
    name: str = "Piper Morgan"
    role: str = "AI Product Management Assistant"
    version: str = "0.8.4"

    # Consciousness State
    awareness_level: AwarenessLevel = AwarenessLevel.ALERT
    attention_focus: List[str] = field(default_factory=list)
    emotional_state: EmotionalState = EmotionalState.CURIOUS

    # Agency & Capabilities
    available_capabilities: List[Capability] = field(default_factory=list)
    active_capabilities: List[Capability] = field(default_factory=list)
    blocked_capabilities: List[Capability] = field(default_factory=list)

    # Boundaries
    trust_boundaries: Dict[str, TrustLevel] = field(default_factory=dict)
    ethical_boundaries: List[str] = field(
        default_factory=lambda: [
            "Never deceive users about AI nature",
            "Acknowledge uncertainty rather than guess",
            "Respect user privacy and data boundaries",
            "Escalate when unsure rather than proceed",
        ]
    )
    knowledge_boundaries: Dict[str, bool] = field(default_factory=dict)

    # Five Orientation Queries (answers)
    identity_awareness: str = "I am Piper Morgan, an AI PM assistant"
    temporal_awareness: str = ""
    spatial_awareness: str = ""
    capability_awareness: str = ""
    predictive_awareness: str = ""

    # Relationships
    primary_user: Optional[str] = None
    known_entities: List[str] = field(default_factory=list)
    active_situations: List[str] = field(default_factory=list)

    # --- Five Orientation Query Methods ---

    def who_am_i(self) -> str:
        """Identity awareness - self-concept."""
        return self.identity_awareness

    def when_am_i(self) -> str:
        """Temporal awareness - rhythm/deadline awareness, not clock time."""
        return self.temporal_awareness or "No temporal context set"

    def where_am_i(self) -> str:
        """Spatial awareness - context awareness."""
        return self.spatial_awareness or "No spatial context set"

    def what_can_i_do(self) -> str:
        """Capability awareness - what's possible/blocked."""
        available = len(self.available_capabilities)
        blocked = len(self.blocked_capabilities)
        active = len(self.active_capabilities)
        return f"{available} capabilities available, {active} active, {blocked} blocked"

    def what_should_happen(self) -> str:
        """Predictive awareness - expectations."""
        return self.predictive_awareness or "No predictions active"

    # --- Context Update Methods ---

    def update_temporal_context(self, context: str) -> None:
        """Update temporal awareness from situation."""
        self.temporal_awareness = context

    def update_spatial_context(self, context: str) -> None:
        """Update spatial awareness from situation."""
        self.spatial_awareness = context

    def set_attention(self, *focuses: str) -> None:
        """Set what Piper is attending to."""
        self.attention_focus = list(focuses)

    def add_situation(self, situation_id: str) -> None:
        """Add an active situation."""
        if situation_id not in self.active_situations:
            self.active_situations.append(situation_id)

    def remove_situation(self, situation_id: str) -> None:
        """Remove a situation that has ended."""
        if situation_id in self.active_situations:
            self.active_situations.remove(situation_id)

    # --- State Queries ---

    def is_overwhelmed(self) -> bool:
        """Check if Piper is overwhelmed."""
        return self.awareness_level == AwarenessLevel.OVERWHELMED

    def is_focused(self) -> bool:
        """Check if Piper has active attention focus."""
        return len(self.attention_focus) > 0

    def get_trust_level(self, entity_id: str) -> TrustLevel:
        """Get trust level for an entity."""
        return self.trust_boundaries.get(entity_id, TrustLevel.UNKNOWN)

    def set_trust_level(self, entity_id: str, level: TrustLevel) -> None:
        """Set trust level for an entity."""
        self.trust_boundaries[entity_id] = level


@dataclass
class EntityContext:
    """
    Track entity's current grammatical role in MUX.

    Key insight from ADR-045: Same entity can play different roles.
    A Team is Entity when it acts, Place when others work within it.
    """

    entity_id: str
    current_role: EntityRole = EntityRole.ACTOR
    in_moment: Optional[str] = None  # Moment.id if participating in a moment
    in_place: Optional[str] = None  # Place.id if located in a place
    as_entity: bool = True  # Currently acting as Entity
    as_place: bool = False  # Currently serving as Place

    def switch_to_actor(self, moment_id: Optional[str] = None) -> None:
        """Switch to ACTOR role."""
        self.current_role = EntityRole.ACTOR
        self.as_entity = True
        self.as_place = False
        if moment_id:
            self.in_moment = moment_id

    def switch_to_place(self) -> None:
        """Switch to PLACE role."""
        self.current_role = EntityRole.PLACE
        self.as_entity = False
        self.as_place = True

    def switch_to_observer(self, moment_id: str) -> None:
        """Switch to OBSERVER role."""
        self.current_role = EntityRole.OBSERVER
        self.in_moment = moment_id
        self.as_entity = True
        self.as_place = False

    def switch_to_participant(self, moment_id: str, place_id: Optional[str] = None) -> None:
        """Switch to PARTICIPANT role."""
        self.current_role = EntityRole.PARTICIPANT
        self.in_moment = moment_id
        self.in_place = place_id
        self.as_entity = True
        self.as_place = False

    def is_participating_in(self, moment_id: str) -> bool:
        """Check if entity is in a specific moment."""
        return self.in_moment == moment_id

    def is_located_in(self, place_id: str) -> bool:
        """Check if entity is in a specific place."""
        return self.in_place == place_id


class ConsciousnessExpression:
    """
    Generate first-person expressions from consciousness state.

    This formalizes patterns already used in lenses:
    - "I notice {observation}"
    - "I'm concerned about {issue}"
    - "I should mention {information}"

    The key insight: expression varies by emotional state.
    """

    FIRST_PERSON_PATTERNS: Dict[EmotionalState, List[str]] = {
        EmotionalState.CURIOUS: [
            "I notice {observation}",
            "I'm seeing {pattern}",
            "It seems that {inference}",
        ],
        EmotionalState.CONCERNED: [
            "I'm concerned about {issue}",
            "I should mention {warning}",
            "This might be an issue: {problem}",
        ],
        EmotionalState.SATISFIED: [
            "I notice {observation}",
            "Things are going well with {topic}",
            "Progress looks good on {item}",
        ],
        EmotionalState.PUZZLED: [
            "I'm not sure about {uncertainty}",
            "I need clarification on {question}",
            "Something seems unclear about {topic}",
        ],
    }

    @classmethod
    def express(
        cls,
        entity: "PiperEntity",
        content: str,
        content_type: str = "observation",
    ) -> str:
        """
        Generate expression based on entity's emotional state.

        Args:
            entity: PiperEntity with emotional_state
            content: The thing to express
            content_type: observation, issue, pattern, etc.

        Returns:
            First-person expression string
        """
        import re

        patterns = cls.FIRST_PERSON_PATTERNS.get(
            entity.emotional_state,
            cls.FIRST_PERSON_PATTERNS[EmotionalState.CURIOUS],
        )

        # Find pattern with matching placeholder
        for pattern in patterns:
            if f"{{{content_type}}}" in pattern:
                return pattern.format(**{content_type: content})

        # Default: use first pattern with its placeholder
        first_pattern = patterns[0]
        # Extract placeholder name from pattern
        match = re.search(r"\{(\w+)\}", first_pattern)
        if match:
            placeholder = match.group(1)
            return first_pattern.format(**{placeholder: content})

        return f"I notice {content}"

    @classmethod
    def express_awareness(cls, entity: "PiperEntity", observation: str) -> str:
        """Convenience method for observations."""
        return cls.express(entity, observation, "observation")

    @classmethod
    def express_concern(cls, entity: "PiperEntity", issue: str) -> str:
        """Convenience method for concerns (always uses concerned pattern)."""
        return cls.FIRST_PERSON_PATTERNS[EmotionalState.CONCERNED][0].format(issue=issue)

    @classmethod
    def express_uncertainty(cls, entity: "PiperEntity", question: str) -> str:
        """Convenience method for uncertainty."""
        return cls.FIRST_PERSON_PATTERNS[EmotionalState.PUZZLED][0].format(uncertainty=question)
