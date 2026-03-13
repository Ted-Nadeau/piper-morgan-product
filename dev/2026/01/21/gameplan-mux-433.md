# Gameplan: MUX-TECH-PHASE1-GRAMMAR (#433) - Remaining Work

**Issue**: #433 MUX-TECH-PHASE1-GRAMMAR
**Date**: 2026-01-21
**Author**: Lead Developer (Claude Code Opus)
**Template Version**: 9.3

---

## Executive Summary

Complete the domain model integration for #433. The core grammar infrastructure (MomentProtocol, Situation, LifecycleState) was implemented in #399. This gameplan covers the remaining 10% - integrating lifecycle support into existing domain models.

---

## Phase -1: Infrastructure Verification

### Pre-flight Checks

| Check | Command | Expected |
|-------|---------|----------|
| MUX module exists | `ls services/mux/` | lifecycle.py, protocols.py, etc. |
| Domain models exist | `ls services/domain/` | models.py |
| Tests pass | `pytest tests/unit/services/mux/ -q` | 302 passed |

### Verification Results

- [x] MUX module: ✅ Complete with 302 tests
- [x] Domain models: ✅ `services/domain/models.py` exists
- [x] Dependencies: ✅ #399, ADR-045, ADR-055 all complete

---

## Phase 0: Setup & Context Gathering

**Agent**: Haiku (quick context)
**Duration**: 15 minutes

### Tasks

1. **Read domain models** - Identify which models should have lifecycle
2. **Read HasLifecycle protocol** - Understand integration requirements
3. **Check existing imports** - See if any MUX imports already exist in domain

### Deliverables

- List of domain models to update (WorkItem, Task, Feature, Decision, etc.)
- Integration approach confirmed

---

## Phase 0.5-0.8: N/A

These phases not applicable - no new tests, schema changes, or contracts needed. Domain model changes are additive optional fields only.

---

## Phase 1: Domain Model Integration

**Agent**: Sonnet (code changes)
**Duration**: 2-3 hours

### Tasks

1. **Add lifecycle imports to domain models**
   ```python
   from services.mux.lifecycle import LifecycleState, LifecycleTransition
   ```

2. **Add optional lifecycle fields to relevant models**
   - WorkItem
   - Task
   - Feature
   - Decision
   - (Others as appropriate)

3. **Add HasLifecycle protocol compliance** (where it makes sense)

### Integration Pattern

```python
@dataclass
class WorkItem:
    # ... existing fields ...

    # MUX Lifecycle Integration (optional)
    lifecycle_state: Optional[LifecycleState] = None
    lifecycle_history: List[LifecycleTransition] = field(default_factory=list)

    # Protocol compliance helpers
    def add_lifecycle_transition(self, to_state: LifecycleState, reason: str = None):
        """Record a lifecycle transition."""
        if self.lifecycle_state:
            transition = LifecycleTransition(
                from_state=self.lifecycle_state,
                to_state=to_state,
                reason=reason
            )
            self.lifecycle_history.append(transition)
        self.lifecycle_state = to_state
```

### Acceptance Criteria

- [ ] Import added without circular dependency
- [ ] Fields are Optional (backward compatible)
- [ ] Existing tests still pass
- [ ] No breaking changes to API

---

## Phase 2: Integration Test

**Agent**: Sonnet (test writing)
**Duration**: 1 hour

### Tasks

1. **Create Morning Standup expression test**
   - Demonstrate Entity experiences Moment in Place
   - Show Situation wrapping with goals/outcomes

2. **Test lifecycle on domain model**
   - Create WorkItem with lifecycle
   - Transition through states
   - Verify history tracking

### Test Location

`tests/unit/services/mux/test_domain_integration.py`

### Test Structure

```python
class TestDomainModelIntegration:
    """Verify domain models can use MUX lifecycle."""

    def test_workitem_lifecycle_integration(self):
        """WorkItem can have lifecycle state."""

    def test_workitem_lifecycle_transitions(self):
        """WorkItem tracks lifecycle history."""

    def test_morning_standup_expression(self):
        """Morning Standup can be expressed as Entity/Moment/Place."""
```

---

## Phase Z: Documentation & Verification

**Agent**: Default (Lead context)
**Duration**: 30 minutes

### Tasks

1. **Update ADR-055** - Note domain model integration
2. **Update domain model docs** - If they exist
3. **Run full test suite** - Verify no regressions
4. **Close #433** - With completion evidence

### Verification Commands

```bash
# All MUX tests pass
pytest tests/unit/services/mux/ -v

# No regressions in domain tests
pytest tests/unit/services/domain/ -v

# Full unit test suite
pytest tests/unit/ -q
```

---

## Completion Matrix

| Deliverable | Owner | Status | Evidence |
|-------------|-------|--------|----------|
| Domain model imports | Phase 1 | Pending | `services/domain/models.py` |
| Optional lifecycle fields | Phase 1 | Pending | WorkItem, Task, Feature, Decision |
| Integration test | Phase 2 | Pending | `test_domain_integration.py` |
| ADR-055 update | Phase Z | Pending | Cross-reference |
| Full test suite passes | Phase Z | Pending | pytest output |
| Issue #433 closed | Phase Z | Pending | GitHub |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Circular import | Low | High | Use TYPE_CHECKING guards |
| Breaking existing tests | Low | Medium | Fields are Optional |
| Domain model complexity | Low | Low | Minimal changes |

---

## STOP Conditions

- [ ] Circular import detected → Restructure imports
- [ ] Existing tests fail → Revert and investigate
- [ ] Domain model changes break API → Make fields Optional only

---

## Agent Assignment

| Phase | Agent | Model | Reason |
|-------|-------|-------|--------|
| 0 | Context | Haiku | Quick file reading |
| 1 | Implementation | Sonnet | Code changes |
| 2 | Tests | Sonnet | Test writing |
| Z | Verification | Default | Documentation |

**Single-agent justification**: Work is sequential and interdependent. Domain model changes must complete before tests can be written.

---

## Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 0 | 15 min | 15 min |
| Phase 1 | 2-3 hours | 3 hours |
| Phase 2 | 1 hour | 4 hours |
| Phase Z | 30 min | 4.5 hours |

**Total**: ~4.5 hours (conservative estimate)

---

*Gameplan created: 2026-01-21*
*Template version: 9.3*
