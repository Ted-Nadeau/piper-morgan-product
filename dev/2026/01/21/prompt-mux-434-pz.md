# Agent Prompt: MUX-434 Phase Z - Verification and Closure

## Mission

Verify all #434 acceptance criteria are met, update documentation, and close the issue with evidence.

---

## Context

- **Issue**: #434 MUX-TECH-PHASE2-ENTITY
- **Phase**: Z (Verification)
- **Agent**: Default
- **Estimated Time**: 2 hours
- **Dependency**: All previous phases (0-1, 2, 3, 4, 5) complete
- **Session Log**: `dev/2026/01/21/2026-01-21-0639-lead-code-opus-log.md`

---

## Prerequisites

Verify all phases complete:
```bash
python -m pytest tests/unit/services/mux/test_consciousness.py -v
python -m pytest tests/unit/services/mux/test_piper_entity.py -v
python -m pytest tests/unit/services/mux/test_entity_context.py -v
python -m pytest tests/unit/services/mux/test_consciousness_expression.py -v
python -m pytest tests/unit/services/mux/test_domain_consciousness.py -v
```

---

## Tasks

### Task 1: Run Full Test Suite

```bash
# All MUX tests
python -m pytest tests/unit/services/mux/ -v --tb=short

# Full unit test suite (verify no regressions)
python -m pytest tests/unit/ -v --tb=no | tail -20
```

Expected: All tests pass, MUX test count should be ~364 (314 original + ~50 new)

### Task 2: Verify Issue Acceptance Criteria

Check each criterion from the issue:

| Criterion | Test Command | Expected |
|-----------|--------------|----------|
| AwarenessLevel enum (5 states) | `python -c "from services.mux.consciousness import AwarenessLevel; print(len(AwarenessLevel))"` | 5 |
| EmotionalState enum (4 states) | `python -c "from services.mux.consciousness import EmotionalState; print(len(EmotionalState))"` | 4 |
| EntityRole enum (4 roles) | `python -c "from services.mux.consciousness import EntityRole; print(len(EntityRole))"` | 4 |
| ConsciousnessAttributes dataclass | Import test | Success |
| PiperEntity with five queries | Method check | 5 methods |
| EntityContext tracks role | Import test | Success |
| ConsciousnessExpression generates | Pattern test | Generates output |
| Domain models have consciousness | Field check | Optional field exists |

### Task 3: Consciousness Test

Run the verification test from the spec:

```python
# tests/verification/test_consciousness_verification.py (or run inline)
from services.mux.consciousness import (
    PiperEntity,
    EmotionalState,
    ConsciousnessExpression,
)

# Can Piper express: "I'm concerned that the sprint seems overloaded"?
piper = PiperEntity(
    emotional_state=EmotionalState.CONCERNED,
    attention_focus=["sprint_planning"]
)

result = ConsciousnessExpression.express(
    piper, "the sprint seems overloaded", "issue"
)

assert "concerned" in result.lower()
print(f"Consciousness Test PASSED: {result}")
```

### Task 4: Anti-Flattening Test

Verify the anti-flattening criteria:

```python
from services.mux.consciousness import PiperEntity, ConsciousnessAttributes

# 1. Does Piper have identity or just functions?
piper = PiperEntity()
assert piper.name == "Piper Morgan"  # Has identity
assert piper.who_am_i()  # Can self-reflect

# 2. Do entities have wants/fears or just properties?
attrs = ConsciousnessAttributes(
    wants=["ship features"],
    fears=["missing deadlines"]
)
assert len(attrs.wants) > 0  # Has drives

# 3. Can entities play multiple roles?
from services.mux.consciousness import EntityContext, EntityRole
ctx = EntityContext(entity_id="team-1")
ctx.switch_to_place()
assert ctx.current_role == EntityRole.PLACE
ctx.switch_to_actor()
assert ctx.current_role == EntityRole.ACTOR  # Role fluidity

print("Anti-Flattening Test PASSED")
```

### Task 5: Update ADR-055

Add Phase 2 Entity implementation section to `docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md`:

```markdown
## Phase 2: Entity Implementation (Jan 21, 2026)

### Consciousness Types Created

**Core Enums** (`services/mux/consciousness.py`):
- `AwarenessLevel`: 5 states (sleeping → overwhelmed)
- `EmotionalState`: 4 states (curious, concerned, satisfied, puzzled)
- `EntityRole`: 4 roles (actor, place, observer, participant)
- `TrustLevel`: 5 levels (unknown → full)

**Core Dataclasses**:
- `ConsciousnessAttributes`: Agency, awareness, and relationship traits
- `Capability`: Something an entity can do
- `PiperEntity`: First-class Piper representation with identity, consciousness, boundaries
- `EntityContext`: Role tracking for grammar participation

**Expression System**:
- `ConsciousnessExpression`: First-person expression generation from emotional state
- Patterns: "I notice", "I'm concerned", "I should mention", etc.

### Domain Model Integration

- `Stakeholder`: Added `consciousness: Optional[ConsciousnessAttributes]`
- Backward compatible (None default)

### Five Orientation Queries

PiperEntity implements the PM vision's five orientation queries:
1. `who_am_i()` - Identity awareness
2. `when_am_i()` - Temporal/rhythm awareness
3. `where_am_i()` - Context/spatial awareness
4. `what_can_i_do()` - Capability boundaries
5. `what_should_happen()` - Predictive modeling

### Test Coverage

- ~50 new tests for consciousness types
- Total MUX tests: ~364
```

### Task 6: Close Issue with Evidence

Add comment and close:

```bash
gh issue comment 434 --body "## Phase Z Verification Complete

### Implementation Evidence

**Files Created/Modified:**
- \`services/mux/consciousness.py\` - Core consciousness types
- \`services/mux/__init__.py\` - Updated exports
- \`services/domain/models.py\` - Stakeholder consciousness integration
- \`tests/unit/services/mux/test_consciousness.py\`
- \`tests/unit/services/mux/test_piper_entity.py\`
- \`tests/unit/services/mux/test_entity_context.py\`
- \`tests/unit/services/mux/test_consciousness_expression.py\`
- \`tests/unit/services/mux/test_domain_consciousness.py\`

### Test Coverage
- New tests: ~50
- Total MUX tests: ~364
- All passing

### Acceptance Criteria Met
- [x] AwarenessLevel enum (5 states)
- [x] EmotionalState enum (4 states)
- [x] EntityRole enum (4 roles)
- [x] ConsciousnessAttributes dataclass
- [x] PiperEntity with identity, consciousness, agency, boundaries
- [x] Five orientation queries have model support
- [x] EntityContext tracks role
- [x] ConsciousnessExpression generates first-person
- [x] Domain models can have consciousness
- [x] All MUX tests pass
- [x] New unit tests added

### Verification Tests Passed
1. **Consciousness Test**: Piper can express \"I'm concerned that the sprint seems overloaded\"
2. **Anti-Flattening Test**: Piper has identity, entities have drives, roles are fluid

🤖 Verified by Lead Developer (Claude Code Opus) - 2026-01-21"

gh issue close 434 --comment "Closed - All acceptance criteria verified."
```

---

## Acceptance Criteria (Phase Z)

- [ ] All 11 issue acceptance criteria verified
- [ ] All MUX tests pass (~364 total)
- [ ] Consciousness test passes
- [ ] Anti-flattening test passes
- [ ] ADR-055 updated with Phase 2 section
- [ ] Issue #434 closed with evidence

---

## Output Format

```markdown
## Phase Z Complete - #434 CLOSED

### Test Results
```
[MUX test output summary]
```

### Verification Evidence
- Consciousness Test: [output]
- Anti-Flattening Test: [output]

### Documentation Updated
- ADR-055: Phase 2 section added

### Issue Closed
- GitHub comment: [link]
- All 11 acceptance criteria met
```

---

## Session Log Reminder

Update the session log with final #434 completion status.
