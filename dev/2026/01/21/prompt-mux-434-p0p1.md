# Agent Prompt: MUX-434 Phase 0-1 - Core Consciousness Foundation

## Mission

Create the foundation consciousness types (enums and ConsciousnessAttributes dataclass) in `services/mux/consciousness.py`.

---

## Context

- **Issue**: #434 MUX-TECH-PHASE2-ENTITY
- **Phase**: 0-1 (Core Foundation)
- **Agent**: Sonnet
- **Estimated Time**: 4 hours
- **Session Log**: `dev/2026/01/21/2026-01-21-0639-lead-code-opus-log.md`

---

## Prerequisites

Read these files first:
1. `services/mux/protocols.py` - Understand EntityProtocol
2. `services/mux/perception.py` - See PerceptionMode as enum pattern
3. `dev/2026/01/21/gameplan-mux-434.md` - Full gameplan with code specs

---

## Tasks

### Task 1: Create consciousness.py

Create `services/mux/consciousness.py` with:

```python
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
    trusts: Dict[str, float] = field(default_factory=dict)
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

### Task 2: Update MUX __init__.py

Add exports to `services/mux/__init__.py`:

```python
# Consciousness types (#434)
from .consciousness import (
    AwarenessLevel,
    EmotionalState,
    EntityRole,
    ConsciousnessAttributes,
)
```

### Task 3: Create Unit Tests

Create `tests/unit/services/mux/test_consciousness.py`:

```python
"""
Tests for MUX consciousness types.

Part of #434 MUX-TECH-PHASE2-ENTITY.
"""

import pytest
from services.mux.consciousness import (
    AwarenessLevel,
    EmotionalState,
    EntityRole,
    ConsciousnessAttributes,
)


class TestAwarenessLevel:
    """Tests for AwarenessLevel enum."""

    def test_has_five_levels(self):
        """AwarenessLevel has exactly 5 states."""
        assert len(AwarenessLevel) == 5

    def test_sleeping_is_lowest(self):
        """SLEEPING represents inactive state."""
        assert AwarenessLevel.SLEEPING.value == "sleeping"

    def test_overwhelmed_is_degraded(self):
        """OVERWHELMED represents too much input."""
        assert AwarenessLevel.OVERWHELMED.value == "overwhelmed"

    def test_all_values_are_lowercase_strings(self):
        """All enum values are lowercase strings."""
        for level in AwarenessLevel:
            assert level.value == level.value.lower()
            assert isinstance(level.value, str)


class TestEmotionalState:
    """Tests for EmotionalState enum."""

    def test_has_four_states(self):
        """EmotionalState has exactly 4 states."""
        assert len(EmotionalState) == 4

    def test_curious_is_default_exploration(self):
        """CURIOUS represents exploring mode."""
        assert EmotionalState.CURIOUS.value == "curious"

    def test_concerned_for_issues(self):
        """CONCERNED represents worry about issues."""
        assert EmotionalState.CONCERNED.value == "concerned"

    def test_puzzled_for_uncertainty(self):
        """PUZZLED represents needing clarification."""
        assert EmotionalState.PUZZLED.value == "puzzled"


class TestEntityRole:
    """Tests for EntityRole enum."""

    def test_has_four_roles(self):
        """EntityRole has exactly 4 roles."""
        assert len(EntityRole) == 4

    def test_actor_for_doing(self):
        """ACTOR is for entities doing things."""
        assert EntityRole.ACTOR.value == "actor"

    def test_place_for_context(self):
        """PLACE is for context where things happen."""
        assert EntityRole.PLACE.value == "place"


class TestConsciousnessAttributes:
    """Tests for ConsciousnessAttributes dataclass."""

    def test_empty_defaults(self):
        """ConsciousnessAttributes defaults to empty collections."""
        attrs = ConsciousnessAttributes()
        assert attrs.wants == []
        assert attrs.fears == []
        assert attrs.capabilities == []
        assert attrs.knows_about == []
        assert attrs.attention_on is None
        assert attrs.emotional_state is None
        assert attrs.trusts == {}
        assert attrs.depends_on == []
        assert attrs.influences == []

    def test_with_values(self):
        """ConsciousnessAttributes accepts values."""
        attrs = ConsciousnessAttributes(
            wants=["ship features"],
            fears=["missing deadlines"],
            capabilities=["planning", "tracking"],
            emotional_state=EmotionalState.CURIOUS
        )
        assert "ship features" in attrs.wants
        assert attrs.emotional_state == EmotionalState.CURIOUS

    def test_is_aware_of_known_topic(self):
        """is_aware_of returns True for known topics."""
        attrs = ConsciousnessAttributes(knows_about=["sprint", "backlog"])
        assert attrs.is_aware_of("sprint") is True
        assert attrs.is_aware_of("unknown") is False

    def test_trust_level_default(self):
        """trust_level returns 0.5 for unknown entities."""
        attrs = ConsciousnessAttributes()
        assert attrs.trust_level("unknown-entity") == 0.5

    def test_trust_level_known(self):
        """trust_level returns stored value for known entities."""
        attrs = ConsciousnessAttributes(trusts={"user-1": 0.9})
        assert attrs.trust_level("user-1") == 0.9

    def test_is_focused_when_attention_set(self):
        """is_focused returns True when attention_on is set."""
        attrs = ConsciousnessAttributes(attention_on="sprint planning")
        assert attrs.is_focused() is True

    def test_not_focused_when_attention_none(self):
        """is_focused returns False when attention_on is None."""
        attrs = ConsciousnessAttributes()
        assert attrs.is_focused() is False
```

### Task 4: Verify Tests Pass

```bash
# Run new tests
python -m pytest tests/unit/services/mux/test_consciousness.py -v

# Run all MUX tests to verify no regressions
python -m pytest tests/unit/services/mux/ -v --tb=short
```

---

## Acceptance Criteria

- [ ] `services/mux/consciousness.py` exists
- [ ] AwarenessLevel has 5 states (sleeping, drowsy, alert, focused, overwhelmed)
- [ ] EmotionalState has 4 states (curious, concerned, satisfied, puzzled)
- [ ] EntityRole has 4 roles (actor, place, observer, participant)
- [ ] ConsciousnessAttributes has all 9 fields
- [ ] Helper methods work (is_aware_of, trust_level, is_focused)
- [ ] MUX __init__.py exports new types
- [ ] 15+ unit tests pass

---

## STOP Conditions

- If enum values differ from spec → STOP, clarify with PM
- If ConsciousnessAttributes fields unclear → STOP, check gameplan
- If existing MUX tests break → STOP, investigate immediately

---

## Output Format

When complete, report:

```markdown
## Phase 0-1 Complete

### Files Created/Modified
- `services/mux/consciousness.py` - Created (X lines)
- `services/mux/__init__.py` - Modified (added exports)
- `tests/unit/services/mux/test_consciousness.py` - Created (X tests)

### Test Results
```
[paste pytest output]
```

### Acceptance Criteria
- [x] criterion 1
- [x] criterion 2
...

### Notes
[Any issues or observations]
```

---

## Session Log Reminder

Update the session log at `dev/2026/01/21/2026-01-21-0639-lead-code-opus-log.md` with your progress.
