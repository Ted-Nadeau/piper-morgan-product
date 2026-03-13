# Gameplan: MUX-434 PHASE2-ENTITY

**Issue**: #434 MUX-TECH-PHASE2-ENTITY
**Created**: 2026-01-21
**Author**: Lead Developer (Claude Code Opus)
**Template Version**: 9.3

---

## Mission

Implement Piper as a first-class Entity with consciousness attributes, enabling self-expression and agency in the MUX system.

---

## Prerequisites

- [x] #433 PHASE1-GRAMMAR complete (domain model integration)
- [x] MUX module exists with 314 passing tests
- [x] EntityProtocol, Perception, PerceptionMode exist
- [x] "I notice" patterns established in lenses

---

## Phase Structure

| Phase | Name | Agent | Est Hours | Deliverables |
|-------|------|-------|-----------|--------------|
| 0-1 | Core Consciousness Foundation | Sonnet | 4h | Enums + ConsciousnessAttributes |
| 2 | PiperEntity Model | Sonnet | 4h | Full PiperEntity implementation |
| 3 | EntityContext System | Sonnet | 2h | EntityContext + role tracking |
| 4 | ConsciousnessExpression | Sonnet | 2h | Expression class with patterns |
| 5 | Domain Integration | Sonnet | 2h | Add consciousness to User/Stakeholder |
| Z | Verification | Default | 2h | Tests, docs, closure |

---

## Phase 0-1: Core Consciousness Foundation

### Context
Create the foundation enums and ConsciousnessAttributes dataclass that all other components depend on.

### Deliverables
1. Create `services/mux/consciousness.py` with:
   - AwarenessLevel enum (5 states)
   - EmotionalState enum (4 states)
   - EntityRole enum (4 roles)
   - ConsciousnessAttributes dataclass

### Code Specification

```python
# services/mux/consciousness.py
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
    SLEEPING = "sleeping"      # Inactive, not monitoring
    DROWSY = "drowsy"          # Low attention, passive monitoring
    ALERT = "alert"            # Active attention, normal operation
    FOCUSED = "focused"        # Deep attention, high engagement
    OVERWHELMED = "overwhelmed"  # Too much input, degraded function


class EmotionalState(Enum):
    """
    Emotional modes that color perception and expression.

    From PM vision: "I notice" vs "I'm concerned" shows emotional framing.
    """
    CURIOUS = "curious"        # Exploring, questioning
    CONCERNED = "concerned"    # Worried, flagging issues
    SATISFIED = "satisfied"    # Content, things are going well
    PUZZLED = "puzzled"        # Uncertain, needs clarification


class EntityRole(Enum):
    """
    Grammatical roles an entity can play in MUX grammar.

    Key insight: Same entity can be ACTOR in one moment, PLACE in another.
    A Team is both an actor (takes actions) and a place (where work happens).
    """
    ACTOR = "actor"            # Doing something (Entity substrate)
    PLACE = "place"            # Where something happens (Place substrate)
    OBSERVER = "observer"      # Watching something unfold
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
```

### Acceptance Criteria (P0-1)
- [ ] `services/mux/consciousness.py` exists
- [ ] AwarenessLevel has 5 states
- [ ] EmotionalState has 4 states
- [ ] EntityRole has 4 roles
- [ ] ConsciousnessAttributes has all specified fields
- [ ] Helper methods work (is_aware_of, trust_level, is_focused)
- [ ] MUX __init__.py exports new types
- [ ] 15+ unit tests for new types

### STOP Conditions
- If enum values differ from spec → STOP, clarify with PM
- If ConsciousnessAttributes fields unclear → STOP, check original issue
- If existing MUX tests break → STOP, investigate

---

## Phase 2: PiperEntity Model

### Context
Create the PiperEntity model as a first-class representation of Piper with identity, consciousness, agency, and boundaries.

### Deliverables
1. Add PiperEntity to `services/mux/consciousness.py` (or new `entity.py`)
2. Implement five orientation queries
3. Capability tracking system

### Code Specification

```python
@dataclass
class Capability:
    """Something Piper can do."""
    name: str
    description: str
    requires: List[str] = field(default_factory=list)  # Dependencies
    blocked_by: Optional[str] = None  # Why it can't be used


class TrustLevel(Enum):
    """Trust levels for user relationships."""
    UNKNOWN = "unknown"
    CAUTIOUS = "cautious"
    STANDARD = "standard"
    TRUSTED = "trusted"
    FULL = "full"


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
    version: str = "0.8.3"

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
    ethical_boundaries: List[str] = field(default_factory=lambda: [
        "Never deceive users about AI nature",
        "Acknowledge uncertainty rather than guess",
        "Respect user privacy and data boundaries",
        "Escalate when unsure rather than proceed"
    ])
    knowledge_boundaries: Dict[str, bool] = field(default_factory=dict)

    # Five Orientation Queries
    identity_awareness: str = "I am Piper Morgan, an AI PM assistant"
    temporal_awareness: str = ""  # Set by context
    spatial_awareness: str = ""   # Set by context
    capability_awareness: str = ""  # Set by context
    predictive_awareness: str = ""  # Set by context

    # Relationships
    primary_user: Optional[str] = None
    known_entities: List[str] = field(default_factory=list)
    active_situations: List[str] = field(default_factory=list)

    # Five Orientation Query Methods
    def who_am_i(self) -> str:
        """Identity awareness - self-concept."""
        return self.identity_awareness

    def when_am_i(self) -> str:
        """Temporal awareness - not clock time but rhythm/deadline awareness."""
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

    def update_temporal_context(self, context: str) -> None:
        """Update temporal awareness from situation."""
        self.temporal_awareness = context

    def update_spatial_context(self, context: str) -> None:
        """Update spatial awareness from situation."""
        self.spatial_awareness = context

    def set_attention(self, *focuses: str) -> None:
        """Set what Piper is attending to."""
        self.attention_focus = list(focuses)

    def is_overwhelmed(self) -> bool:
        """Check if Piper is overwhelmed."""
        return self.awareness_level == AwarenessLevel.OVERWHELMED
```

### Acceptance Criteria (P2)
- [ ] PiperEntity exists with all identity fields
- [ ] Five orientation query methods work
- [ ] Capability tracking (available/active/blocked) works
- [ ] Boundaries (trust, ethical, knowledge) exist
- [ ] Default ethical boundaries are meaningful
- [ ] 15+ unit tests for PiperEntity

### STOP Conditions
- If orientation queries don't match PM spec → STOP, verify
- If ethical boundaries seem wrong → STOP, discuss with PM

---

## Phase 3: EntityContext System

### Context
Create tracking for entity's current grammatical role - the same entity can be ACTOR in one moment and PLACE in another.

### Deliverables
1. EntityContext dataclass
2. Role tracking and switching

### Code Specification

```python
@dataclass
class EntityContext:
    """
    Track entity's current grammatical role in MUX.

    Key insight from ADR-045: Same entity can play different roles.
    A Team is Entity when it acts, Place when others work within it.
    """
    entity_id: str
    current_role: EntityRole = EntityRole.ACTOR
    in_moment: Optional[str] = None  # Moment.id if in a moment
    in_place: Optional[str] = None   # Place.id if in a place
    as_entity: bool = True   # Currently acting as Entity
    as_place: bool = False   # Currently serving as Place

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

    def is_participating_in(self, moment_id: str) -> bool:
        """Check if entity is in a specific moment."""
        return self.in_moment == moment_id
```

### Acceptance Criteria (P3)
- [ ] EntityContext tracks current role
- [ ] Role switching methods work
- [ ] in_moment/in_place tracking works
- [ ] 8+ unit tests for EntityContext

---

## Phase 4: ConsciousnessExpression

### Context
Formalize the "I notice" patterns from lenses into a reusable class that generates first-person expressions from consciousness state.

### Deliverables
1. ConsciousnessExpression class
2. Pattern-based expression generation

### Code Specification

```python
class ConsciousnessExpression:
    """
    Generate first-person expressions from consciousness state.

    This formalizes patterns already used in lenses:
    - "I notice {observation}"
    - "I'm concerned about {issue}"
    - "I should mention {information}"

    The key insight: expression varies by emotional state.
    """

    FIRST_PERSON_PATTERNS = {
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
        content_type: str = "observation"
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
        patterns = cls.FIRST_PERSON_PATTERNS.get(
            entity.emotional_state,
            cls.FIRST_PERSON_PATTERNS[EmotionalState.CURIOUS]
        )

        # Find pattern with matching placeholder
        for pattern in patterns:
            if f"{{{content_type}}}" in pattern:
                return pattern.format(**{content_type: content})

        # Default to first pattern
        placeholder = pattern.split("{")[1].split("}")[0] if "{" in patterns[0] else "observation"
        return patterns[0].format(**{placeholder: content})

    @classmethod
    def express_awareness(cls, entity: "PiperEntity", observation: str) -> str:
        """Convenience method for observations."""
        return cls.express(entity, observation, "observation")

    @classmethod
    def express_concern(cls, entity: "PiperEntity", issue: str) -> str:
        """Convenience method for concerns."""
        # Temporarily switch to concerned for this expression
        original = entity.emotional_state
        result = cls.FIRST_PERSON_PATTERNS[EmotionalState.CONCERNED][0].format(issue=issue)
        return result
```

### Acceptance Criteria (P4)
- [ ] ConsciousnessExpression class exists
- [ ] FIRST_PERSON_PATTERNS constant has patterns for all 4 emotions
- [ ] express() generates based on emotional state
- [ ] Convenience methods work
- [ ] 10+ unit tests for expression generation

---

## Phase 5: Domain Integration

### Context
Add optional consciousness attributes to existing domain models (User, Stakeholder).

### Deliverables
1. Add `consciousness: Optional[ConsciousnessAttributes]` to domain models
2. Maintain backward compatibility

### Code Specification

```python
# In services/domain/models.py

# Add import at top:
from services.mux.consciousness import ConsciousnessAttributes

# Add to User class (if exists) or Stakeholder:
@dataclass
class Stakeholder:
    # ... existing fields ...

    # MUX Consciousness Integration (#434) - optional, backward compatible
    consciousness: Optional[ConsciousnessAttributes] = None
```

### Acceptance Criteria (P5)
- [ ] User model has `consciousness: Optional[ConsciousnessAttributes]`
- [ ] Stakeholder model has `consciousness: Optional[ConsciousnessAttributes]`
- [ ] Backward compatibility maintained (None defaults)
- [ ] All existing tests pass
- [ ] 4+ integration tests for domain models with consciousness

---

## Phase Z: Verification

### Context
Run all tests, verify acceptance criteria, document, close issue.

### Tasks
1. Run full MUX test suite
2. Run integration tests
3. Update ADR-055 with Phase 2 implementation
4. Update `services/mux/__init__.py` exports
5. Close issue with evidence

### Verification Commands
```bash
# MUX tests
python -m pytest tests/unit/services/mux/ -v

# Full unit tests
python -m pytest tests/unit/ -v

# Specific consciousness tests
python -m pytest tests/unit/services/mux/test_consciousness.py -v
```

### Acceptance Criteria (PZ)
- [ ] All 11 issue acceptance criteria met
- [ ] All MUX tests pass (target: 344+ total)
- [ ] ADR-055 updated
- [ ] Issue #434 closed with evidence

---

## Completion Matrix

| Phase | Acceptance Criteria | Test Count | Evidence |
|-------|---------------------|------------|----------|
| P0-1 | 8/8 | 15+ | `test_consciousness.py` |
| P2 | 6/6 | 15+ | `test_piper_entity.py` |
| P3 | 4/4 | 8+ | `test_entity_context.py` |
| P4 | 5/5 | 10+ | `test_consciousness_expression.py` |
| P5 | 5/5 | 4+ | `test_domain_consciousness.py` |
| PZ | 4/4 | - | Issue comment |
| **Total** | **32/32** | **52+** | |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Over-engineering PiperEntity | Medium | Medium | Stick to spec fields |
| Breaking existing lenses | Low | High | Add only, don't modify |
| Scope creep in expression | Medium | Low | Formalize existing patterns only |
| Domain model conflicts | Low | Medium | Optional fields, None defaults |

---

## Dependencies

```
P0-1 ──→ P2 ──→ P4
   └──→ P3
   └──→ P5
         └──→ PZ (all)
```

P0-1 (enums) must complete first.
P2, P3, P5 can run in parallel after P0-1.
P4 needs P2.
PZ needs all.

---

*Gameplan created: 2026-01-21*
*Template version: 9.3*
