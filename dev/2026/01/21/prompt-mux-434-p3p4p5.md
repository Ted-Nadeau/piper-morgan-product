# Agent Prompt: MUX-434 Phases 3-4-5 - EntityContext, Expression, Integration

## Mission

Complete remaining #434 components: EntityContext tracking, ConsciousnessExpression class, and domain model integration.

---

## Context

- **Issue**: #434 MUX-TECH-PHASE2-ENTITY
- **Phases**: 3 (EntityContext), 4 (Expression), 5 (Integration)
- **Agent**: Sonnet
- **Estimated Time**: 6 hours total
- **Dependency**: Phases 0-1 and 2 must be complete
- **Session Log**: `dev/2026/01/21/2026-01-21-0639-lead-code-opus-log.md`

---

## Prerequisites

Verify Phases 0-1 and 2 are complete:
```bash
python -m pytest tests/unit/services/mux/test_consciousness.py -v
python -m pytest tests/unit/services/mux/test_piper_entity.py -v
```

Read:
1. `services/mux/consciousness.py` - Current implementation
2. `services/domain/models.py` - Domain models for Phase 5
3. `dev/2026/01/21/gameplan-mux-434.md` - Full specs

---

## Phase 3: EntityContext System (2h)

### Task 3.1: Add EntityContext to consciousness.py

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
    in_moment: Optional[str] = None  # Moment.id if participating in a moment
    in_place: Optional[str] = None   # Place.id if located in a place
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
```

### Task 3.2: Create EntityContext Tests

Add to `tests/unit/services/mux/test_entity_context.py`:

```python
"""
Tests for EntityContext role tracking.

Part of #434 MUX-TECH-PHASE2-ENTITY.
"""

import pytest
from services.mux.consciousness import EntityContext, EntityRole


class TestEntityContextDefaults:
    """Tests for EntityContext default state."""

    def test_default_is_actor(self):
        """EntityContext defaults to ACTOR role."""
        ctx = EntityContext(entity_id="team-1")
        assert ctx.current_role == EntityRole.ACTOR
        assert ctx.as_entity is True
        assert ctx.as_place is False

    def test_no_moment_or_place_by_default(self):
        """EntityContext has no moment or place by default."""
        ctx = EntityContext(entity_id="team-1")
        assert ctx.in_moment is None
        assert ctx.in_place is None


class TestEntityContextRoleSwitching:
    """Tests for role switching."""

    def test_switch_to_place(self):
        """switch_to_place changes role to PLACE."""
        ctx = EntityContext(entity_id="team-1")
        ctx.switch_to_place()
        assert ctx.current_role == EntityRole.PLACE
        assert ctx.as_entity is False
        assert ctx.as_place is True

    def test_switch_to_actor_with_moment(self):
        """switch_to_actor can set moment."""
        ctx = EntityContext(entity_id="team-1")
        ctx.switch_to_actor(moment_id="standup-1")
        assert ctx.current_role == EntityRole.ACTOR
        assert ctx.in_moment == "standup-1"

    def test_switch_to_observer(self):
        """switch_to_observer sets observer role with moment."""
        ctx = EntityContext(entity_id="user-1")
        ctx.switch_to_observer(moment_id="meeting-1")
        assert ctx.current_role == EntityRole.OBSERVER
        assert ctx.in_moment == "meeting-1"

    def test_switch_to_participant(self):
        """switch_to_participant sets participant role."""
        ctx = EntityContext(entity_id="user-1")
        ctx.switch_to_participant(moment_id="standup-1", place_id="channel-1")
        assert ctx.current_role == EntityRole.PARTICIPANT
        assert ctx.in_moment == "standup-1"
        assert ctx.in_place == "channel-1"


class TestEntityContextQueries:
    """Tests for context queries."""

    def test_is_participating_in(self):
        """is_participating_in checks moment participation."""
        ctx = EntityContext(entity_id="user-1", in_moment="meeting-1")
        assert ctx.is_participating_in("meeting-1") is True
        assert ctx.is_participating_in("other-meeting") is False

    def test_is_located_in(self):
        """is_located_in checks place location."""
        ctx = EntityContext(entity_id="user-1", in_place="channel-1")
        assert ctx.is_located_in("channel-1") is True
        assert ctx.is_located_in("other-channel") is False
```

---

## Phase 4: ConsciousnessExpression (2h)

### Task 4.1: Add ConsciousnessExpression to consciousness.py

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

        # Default: use first pattern with its placeholder
        first_pattern = patterns[0]
        # Extract placeholder name from pattern
        import re
        match = re.search(r'\{(\w+)\}', first_pattern)
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
```

### Task 4.2: Create Expression Tests

Add to `tests/unit/services/mux/test_consciousness_expression.py`:

```python
"""
Tests for ConsciousnessExpression class.

Part of #434 MUX-TECH-PHASE2-ENTITY.
"""

import pytest
from services.mux.consciousness import (
    EmotionalState,
    PiperEntity,
    ConsciousnessExpression,
)


class TestConsciousnessExpressionPatterns:
    """Tests for expression pattern constants."""

    def test_patterns_for_all_emotions(self):
        """FIRST_PERSON_PATTERNS has entries for all emotions."""
        for state in EmotionalState:
            assert state in ConsciousnessExpression.FIRST_PERSON_PATTERNS
            assert len(ConsciousnessExpression.FIRST_PERSON_PATTERNS[state]) >= 2


class TestConsciousnessExpressionGeneration:
    """Tests for expression generation."""

    def test_curious_generates_i_notice(self):
        """Curious entity generates 'I notice' style."""
        piper = PiperEntity(emotional_state=EmotionalState.CURIOUS)
        result = ConsciousnessExpression.express_awareness(piper, "3 tasks overdue")
        assert "I notice" in result or "I'm seeing" in result

    def test_concerned_generates_concern(self):
        """Concerned entity generates concern language."""
        piper = PiperEntity(emotional_state=EmotionalState.CONCERNED)
        result = ConsciousnessExpression.express(piper, "the sprint is overloaded", "issue")
        assert "concerned" in result.lower() or "issue" in result.lower()

    def test_puzzled_generates_uncertainty(self):
        """Puzzled entity generates uncertainty language."""
        piper = PiperEntity(emotional_state=EmotionalState.PUZZLED)
        result = ConsciousnessExpression.express(piper, "the requirements", "uncertainty")
        assert "not sure" in result.lower() or "unclear" in result.lower()

    def test_satisfied_generates_positive(self):
        """Satisfied entity generates positive language."""
        piper = PiperEntity(emotional_state=EmotionalState.SATISFIED)
        result = ConsciousnessExpression.express(piper, "sprint completion", "topic")
        assert "going well" in result.lower() or "notice" in result.lower()


class TestConvenienceMethods:
    """Tests for convenience expression methods."""

    def test_express_awareness(self):
        """express_awareness works for any entity."""
        piper = PiperEntity()
        result = ConsciousnessExpression.express_awareness(piper, "a pattern")
        assert "pattern" in result

    def test_express_concern_always_concerned(self):
        """express_concern always uses concerned pattern."""
        piper = PiperEntity(emotional_state=EmotionalState.CURIOUS)  # Not concerned
        result = ConsciousnessExpression.express_concern(piper, "deadline risk")
        assert "concerned" in result.lower()

    def test_express_uncertainty(self):
        """express_uncertainty uses puzzled pattern."""
        piper = PiperEntity()
        result = ConsciousnessExpression.express_uncertainty(piper, "the scope")
        assert "not sure" in result.lower()


class TestConsciousnessTest:
    """The consciousness test from the issue spec."""

    def test_sprint_overloaded_concern(self):
        """
        Can Piper express: "I'm concerned that the sprint seems overloaded"?

        This is the key test from the issue specification.
        """
        piper = PiperEntity(
            emotional_state=EmotionalState.CONCERNED,
            attention_focus=["sprint_planning"]
        )

        result = ConsciousnessExpression.express(
            piper, "the sprint seems overloaded", "issue"
        )

        assert "concerned" in result.lower()
        assert "sprint" in result.lower() or "overloaded" in result.lower()
```

---

## Phase 5: Domain Integration (2h)

### Task 5.1: Add Consciousness to Domain Models

Edit `services/domain/models.py`:

1. Add import at top (near other MUX imports):
```python
# MUX Consciousness Integration (#434)
from services.mux.consciousness import ConsciousnessAttributes
```

2. Add to Stakeholder class (around line 206):
```python
    # MUX Consciousness Integration (#434) - optional, backward compatible
    consciousness: Optional[ConsciousnessAttributes] = None
```

3. If User class exists, add the same field.

### Task 5.2: Create Domain Integration Tests

Add to `tests/unit/services/mux/test_domain_consciousness.py`:

```python
"""
Tests for domain model consciousness integration.

Part of #434 MUX-TECH-PHASE2-ENTITY.
"""

import pytest
from services.domain.models import Stakeholder
from services.mux.consciousness import ConsciousnessAttributes, EmotionalState


class TestStakeholderConsciousness:
    """Tests for Stakeholder consciousness integration."""

    def test_stakeholder_consciousness_defaults_to_none(self):
        """Stakeholder consciousness is None by default (backward compatible)."""
        stakeholder = Stakeholder(id="sh-1", name="Test Stakeholder")
        assert stakeholder.consciousness is None

    def test_stakeholder_can_have_consciousness(self):
        """Stakeholder can have consciousness attributes."""
        attrs = ConsciousnessAttributes(
            wants=["project success"],
            fears=["budget overrun"],
            emotional_state=EmotionalState.CONCERNED
        )
        stakeholder = Stakeholder(
            id="sh-2",
            name="PM Stakeholder",
            consciousness=attrs
        )
        assert stakeholder.consciousness is not None
        assert "project success" in stakeholder.consciousness.wants

    def test_stakeholder_consciousness_awareness(self):
        """Stakeholder consciousness can track awareness."""
        attrs = ConsciousnessAttributes(
            knows_about=["sprint status", "budget"],
            attention_on="deadline"
        )
        stakeholder = Stakeholder(
            id="sh-3",
            name="Aware Stakeholder",
            consciousness=attrs
        )
        assert stakeholder.consciousness.is_aware_of("sprint status")
        assert stakeholder.consciousness.is_focused()
```

### Task 5.3: Update MUX __init__.py Exports

Ensure all new types are exported:

```python
from .consciousness import (
    AwarenessLevel,
    EmotionalState,
    EntityRole,
    ConsciousnessAttributes,
    Capability,
    TrustLevel,
    PiperEntity,
    EntityContext,
    ConsciousnessExpression,
)
```

### Task 5.4: Verify All Tests Pass

```bash
# All Phase 3-4-5 tests
python -m pytest tests/unit/services/mux/test_entity_context.py -v
python -m pytest tests/unit/services/mux/test_consciousness_expression.py -v
python -m pytest tests/unit/services/mux/test_domain_consciousness.py -v

# All MUX tests
python -m pytest tests/unit/services/mux/ -v --tb=short
```

---

## Acceptance Criteria

### Phase 3 (EntityContext)
- [ ] EntityContext dataclass exists with all fields
- [ ] Role switching methods work (actor, place, observer, participant)
- [ ] is_participating_in and is_located_in queries work
- [ ] 8+ tests pass

### Phase 4 (ConsciousnessExpression)
- [ ] ConsciousnessExpression class exists
- [ ] FIRST_PERSON_PATTERNS has patterns for all 4 emotions
- [ ] express() generates based on emotional state
- [ ] Convenience methods work
- [ ] Consciousness test passes ("sprint overloaded" expression)
- [ ] 10+ tests pass

### Phase 5 (Domain Integration)
- [ ] Stakeholder has `consciousness: Optional[ConsciousnessAttributes]`
- [ ] Backward compatibility maintained
- [ ] 4+ integration tests pass
- [ ] All existing domain tests pass

---

## STOP Conditions

- If Phases 0-1 or 2 tests fail → STOP, those must be complete
- If domain model modification breaks existing tests → STOP, investigate
- If expression patterns don't match existing lens patterns → verify consistency

---

## Output Format

When complete, report:

```markdown
## Phases 3-4-5 Complete

### Files Modified
- `services/mux/consciousness.py` - Added EntityContext, ConsciousnessExpression
- `services/mux/__init__.py` - Updated exports
- `services/domain/models.py` - Added consciousness to Stakeholder
- `tests/unit/services/mux/test_entity_context.py` - Created
- `tests/unit/services/mux/test_consciousness_expression.py` - Created
- `tests/unit/services/mux/test_domain_consciousness.py` - Created

### Test Results
```
[paste pytest output for all tests]
```

### Acceptance Criteria
Phase 3:
- [x] ...

Phase 4:
- [x] ...

Phase 5:
- [x] ...

### Notes
[Any issues or observations]
```

---

## Session Log Reminder

Update the session log at `dev/2026/01/21/2026-01-21-0639-lead-code-opus-log.md` with your progress.
