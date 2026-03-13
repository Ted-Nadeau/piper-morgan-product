# Agent Prompt: MUX-433 Phase Z - Verification & Closure

## Mission

Verify all #433 work is complete and close the issue with evidence.

## Context

- **Issue**: #433 MUX-TECH-PHASE1-GRAMMAR
- **Phase**: Z (Final verification)
- **Agent**: Default (Lead context)
- **Time Budget**: 30 minutes
- **Depends On**: Phases 0-1 and 2 complete

---

## Task 1: Run Full Test Suite

### Commands

```bash
# MUX tests (should be 302+ now with new integration tests)
pytest tests/unit/services/mux/ -v --tb=short

# Domain tests (if they exist)
pytest tests/unit/services/domain/ -v --tb=short 2>/dev/null || echo "No domain tests"

# Full unit test suite (verify no regressions)
pytest tests/unit/ -q
```

### Expected Results

- All MUX tests pass
- No regressions in other tests

---

## Task 2: Update ADR-055

Add a note about domain model integration in `docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md`.

### Section to Add

Under "Implementation Status" or appropriate section:

```markdown
### Domain Model Integration (Jan 2026)

The following domain models now support optional MUX lifecycle:
- WorkItem: lifecycle_state, lifecycle_history
- [other models if added]

This enables domain objects to participate in the 8-stage lifecycle
(EMERGENT → COMPOSTED) while maintaining backward compatibility.

See: #433 MUX-TECH-PHASE1-GRAMMAR
```

---

## Task 3: Verify Acceptance Criteria

### Original #433 Acceptance Criteria

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Moment model expresses bounded occurrences | ✅ | MomentProtocol in #399 |
| Situation containers organize Moments | ✅ | Situation class in #399 |
| Lifecycle includes composting | ✅ | LifecycleState in #399 |
| "Noticed" in lifecycle | ✅ | LifecycleState.NOTICED |
| Morning Standup expressible | ? | Check integration test |
| Domain model integration | ? | Check models.py |

### Remaining Criteria Check

```bash
# Verify domain model has lifecycle
grep -n "lifecycle_state" services/domain/models.py

# Verify integration test exists
ls tests/unit/services/mux/test_domain_integration.py

# Run the specific test
pytest tests/unit/services/mux/test_domain_integration.py -v
```

---

## Task 4: Close Issue #433

### Closing Comment Template

```markdown
## #433 MUX-TECH-PHASE1-GRAMMAR Complete

### Implementation Status: 100%

All acceptance criteria met:
- [x] Moment model expresses bounded occurrences (MomentProtocol)
- [x] Situation containers organize Moments narratively
- [x] Lifecycle includes composting (8 stages)
- [x] "Noticed" appears in lifecycle
- [x] Morning Standup can be expressed (integration test)
- [x] Domain models have lifecycle support

### Evidence

**Core Implementation** (from #399):
- `services/mux/protocols.py` - MomentProtocol
- `services/mux/situation.py` - Situation class
- `services/mux/lifecycle.py` - LifecycleState, LifecycleManager

**Domain Integration** (this sprint):
- `services/domain/models.py` - Added lifecycle fields
- `tests/unit/services/mux/test_domain_integration.py` - Integration tests

### Test Results
```
pytest tests/unit/services/mux/ -q
[X] tests passed
```

### References
- ADR-045: Object Model Specification
- ADR-055: Implementation (updated)
- #399: Core implementation

---

*Completed: 2026-01-21*
```

---

## Task 5: Update Session Log

Add Phase Z completion to the session log:

```markdown
## [TIME] - #433 Phase Z Complete

### Test Results
- MUX tests: [X] passed
- Full suite: [Y] passed
- No regressions

### Documentation Updated
- ADR-055: Domain integration note added

### Issue Closed
- #433: Closed with evidence

### Files Modified This Sprint
- `services/domain/models.py` - Lifecycle fields
- `tests/unit/services/mux/test_domain_integration.py` - New tests
- `docs/.../adr-055-object-model-implementation.md` - Updated
```

---

## Acceptance Criteria

- [ ] All tests pass (no regressions)
- [ ] ADR-055 updated with domain integration note
- [ ] All #433 acceptance criteria verified
- [ ] Issue closed with completion evidence
- [ ] Session log updated

---

## STOP Conditions

🛑 **STOP and escalate if**:
- Tests failing (do not close issue)
- Acceptance criteria not met
- Can't verify integration test exists

---

*Prompt created: 2026-01-21*
*Template version: 10.2*
