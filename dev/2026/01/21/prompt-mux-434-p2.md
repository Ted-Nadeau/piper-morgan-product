# Agent Prompt: MUX-434 Phase 2 - PiperEntity Model

## Mission

Implement the PiperEntity model as a first-class representation of Piper with identity, consciousness, agency, and boundaries.

---

## Context

- **Issue**: #434 MUX-TECH-PHASE2-ENTITY
- **Phase**: 2 (PiperEntity Model)
- **Agent**: Sonnet
- **Estimated Time**: 4 hours
- **Dependency**: Phase 0-1 must be complete
- **Session Log**: `dev/2026/01/21/2026-01-21-0639-lead-code-opus-log.md`

---

## Prerequisites

Read these files first:
1. `services/mux/consciousness.py` - Foundation types from Phase 0-1
2. `services/mux/protocols.py` - EntityProtocol for reference
3. `dev/2026/01/21/gameplan-mux-434.md` - Full PiperEntity spec

Verify Phase 0-1 is complete:
```bash
python -m pytest tests/unit/services/mux/test_consciousness.py -v
```

---

## Tasks

### Task 1: Add Support Types to consciousness.py

Add these types to `services/mux/consciousness.py`:

```python
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
    UNKNOWN = "unknown"      # No history, cautious
    CAUTIOUS = "cautious"    # Some concern
    STANDARD = "standard"    # Normal trust
    TRUSTED = "trusted"      # High trust
    FULL = "full"            # Complete trust
```

### Task 2: Create PiperEntity Class

Add to `services/mux/consciousness.py`:

```python
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
```

### Task 3: Update MUX __init__.py

Add exports:

```python
from .consciousness import (
    # ... existing exports ...
    Capability,
    TrustLevel,
    PiperEntity,
)
```

### Task 4: Create Unit Tests

Create/update `tests/unit/services/mux/test_piper_entity.py`:

```python
"""
Tests for PiperEntity model.

Part of #434 MUX-TECH-PHASE2-ENTITY.
"""

import pytest
from services.mux.consciousness import (
    AwarenessLevel,
    EmotionalState,
    Capability,
    TrustLevel,
    PiperEntity,
)


class TestCapability:
    """Tests for Capability dataclass."""

    def test_basic_capability(self):
        """Capability can be created with name and description."""
        cap = Capability(name="planning", description="Create project plans")
        assert cap.name == "planning"
        assert cap.is_blocked() is False

    def test_blocked_capability(self):
        """Capability can be blocked with reason."""
        cap = Capability(
            name="external_api",
            description="Call external APIs",
            blocked_by="No API key configured"
        )
        assert cap.is_blocked() is True


class TestTrustLevel:
    """Tests for TrustLevel enum."""

    def test_has_five_levels(self):
        """TrustLevel has 5 levels."""
        assert len(TrustLevel) == 5

    def test_unknown_is_default(self):
        """UNKNOWN is the cautious default."""
        assert TrustLevel.UNKNOWN.value == "unknown"


class TestPiperEntityIdentity:
    """Tests for PiperEntity identity."""

    def test_default_identity(self):
        """PiperEntity has default identity values."""
        piper = PiperEntity()
        assert piper.id == "piper-prime"
        assert piper.name == "Piper Morgan"
        assert piper.role == "AI Product Management Assistant"

    def test_who_am_i(self):
        """who_am_i returns identity awareness."""
        piper = PiperEntity()
        assert "Piper Morgan" in piper.who_am_i()


class TestPiperEntityConsciousness:
    """Tests for PiperEntity consciousness state."""

    def test_default_consciousness(self):
        """PiperEntity defaults to alert and curious."""
        piper = PiperEntity()
        assert piper.awareness_level == AwarenessLevel.ALERT
        assert piper.emotional_state == EmotionalState.CURIOUS

    def test_is_overwhelmed(self):
        """is_overwhelmed detects overwhelmed state."""
        piper = PiperEntity(awareness_level=AwarenessLevel.OVERWHELMED)
        assert piper.is_overwhelmed() is True

        piper2 = PiperEntity()
        assert piper2.is_overwhelmed() is False

    def test_set_attention(self):
        """set_attention updates attention focus."""
        piper = PiperEntity()
        piper.set_attention("sprint planning", "backlog review")
        assert "sprint planning" in piper.attention_focus
        assert len(piper.attention_focus) == 2

    def test_is_focused(self):
        """is_focused detects when attention is set."""
        piper = PiperEntity()
        assert piper.is_focused() is False

        piper.set_attention("task")
        assert piper.is_focused() is True


class TestPiperEntityOrientationQueries:
    """Tests for the five orientation queries."""

    def test_when_am_i_default(self):
        """when_am_i returns default when not set."""
        piper = PiperEntity()
        assert "No temporal context" in piper.when_am_i()

    def test_when_am_i_with_context(self):
        """when_am_i returns context when set."""
        piper = PiperEntity()
        piper.update_temporal_context("End of sprint, 2 days to deadline")
        assert "2 days to deadline" in piper.when_am_i()

    def test_where_am_i_default(self):
        """where_am_i returns default when not set."""
        piper = PiperEntity()
        assert "No spatial context" in piper.where_am_i()

    def test_where_am_i_with_context(self):
        """where_am_i returns context when set."""
        piper = PiperEntity()
        piper.update_spatial_context("In #platform-standup channel")
        assert "#platform-standup" in piper.where_am_i()

    def test_what_can_i_do(self):
        """what_can_i_do summarizes capabilities."""
        piper = PiperEntity(
            available_capabilities=[Capability("a", "desc"), Capability("b", "desc")],
            blocked_capabilities=[Capability("c", "desc", blocked_by="reason")]
        )
        result = piper.what_can_i_do()
        assert "2 capabilities available" in result
        assert "1 blocked" in result

    def test_what_should_happen_default(self):
        """what_should_happen returns default when not set."""
        piper = PiperEntity()
        assert "No predictions" in piper.what_should_happen()


class TestPiperEntityBoundaries:
    """Tests for PiperEntity boundaries."""

    def test_default_ethical_boundaries(self):
        """PiperEntity has default ethical boundaries."""
        piper = PiperEntity()
        assert len(piper.ethical_boundaries) == 4
        assert any("deceive" in b.lower() for b in piper.ethical_boundaries)

    def test_trust_boundaries(self):
        """Trust boundaries track per-entity trust."""
        piper = PiperEntity()
        assert piper.get_trust_level("user-1") == TrustLevel.UNKNOWN

        piper.set_trust_level("user-1", TrustLevel.TRUSTED)
        assert piper.get_trust_level("user-1") == TrustLevel.TRUSTED


class TestPiperEntitySituations:
    """Tests for situation management."""

    def test_add_situation(self):
        """add_situation adds unique situation."""
        piper = PiperEntity()
        piper.add_situation("standup-2026-01-21")
        assert "standup-2026-01-21" in piper.active_situations

        # Adding again should not duplicate
        piper.add_situation("standup-2026-01-21")
        assert len(piper.active_situations) == 1

    def test_remove_situation(self):
        """remove_situation removes existing situation."""
        piper = PiperEntity()
        piper.add_situation("standup-2026-01-21")
        piper.remove_situation("standup-2026-01-21")
        assert "standup-2026-01-21" not in piper.active_situations
```

### Task 5: Verify Tests Pass

```bash
# Run PiperEntity tests
python -m pytest tests/unit/services/mux/test_piper_entity.py -v

# Run all MUX tests
python -m pytest tests/unit/services/mux/ -v --tb=short
```

---

## Acceptance Criteria

- [ ] Capability dataclass exists with is_blocked() method
- [ ] TrustLevel enum has 5 levels
- [ ] PiperEntity exists with all identity fields
- [ ] Five orientation query methods work (who/when/where/what can/what should)
- [ ] Capability tracking (available/active/blocked) works
- [ ] Boundaries (trust, ethical, knowledge) exist
- [ ] Default ethical boundaries are meaningful (4 items)
- [ ] 15+ unit tests pass

---

## STOP Conditions

- If Phase 0-1 tests fail → STOP, Phase 0-1 must be complete
- If orientation queries don't match PM spec → STOP, verify with gameplan
- If ethical boundaries seem wrong → STOP, discuss with PM

---

## Output Format

When complete, report:

```markdown
## Phase 2 Complete

### Files Modified
- `services/mux/consciousness.py` - Added Capability, TrustLevel, PiperEntity
- `services/mux/__init__.py` - Added exports
- `tests/unit/services/mux/test_piper_entity.py` - Created (X tests)

### Test Results
```
[paste pytest output]
```

### Acceptance Criteria
- [x] criterion 1
...

### Notes
[Any issues or observations]
```

---

## Session Log Reminder

Update the session log at `dev/2026/01/21/2026-01-21-0639-lead-code-opus-log.md` with your progress.
