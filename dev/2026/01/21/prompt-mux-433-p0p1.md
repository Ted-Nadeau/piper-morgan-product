# Agent Prompt: MUX-433 Phases 0-1 - Domain Model Integration

## Mission

Add MUX lifecycle support to existing domain models in `services/domain/models.py`.

## Context

- **Issue**: #433 MUX-TECH-PHASE1-GRAMMAR
- **Phase**: 0-1 (Context + Implementation)
- **Agent**: Sonnet
- **Time Budget**: 2-3 hours

### What Already Exists

The MUX lifecycle infrastructure is complete in `services/mux/`:
- `lifecycle.py`: LifecycleState enum (8 stages), LifecycleTransition, LifecycleManager
- `protocols.py`: HasLifecycle protocol

### What You're Building

Add optional lifecycle fields to domain models so they can participate in the MUX lifecycle system.

---

## Phase 0: Context Gathering

### Read These Files First

1. `services/mux/lifecycle.py` - Understand LifecycleState, LifecycleTransition
2. `services/domain/models.py` - Identify models to update
3. `tests/unit/services/mux/test_lifecycle.py` - See usage patterns

### Identify Target Models

Domain models that should have lifecycle support:
- WorkItem (tasks evolve through lifecycle)
- Task (if separate from WorkItem)
- Feature (features have lifecycle)
- Decision (decisions move from proposed → ratified)
- Any other models with natural lifecycle progression

---

## Phase 1: Implementation

### Step 1: Add Import

At the top of `services/domain/models.py`, add:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.mux.lifecycle import LifecycleState, LifecycleTransition
else:
    # Runtime import to avoid circular dependency if needed
    from services.mux.lifecycle import LifecycleState, LifecycleTransition
```

If circular import occurs, use TYPE_CHECKING guard only:
```python
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from services.mux.lifecycle import LifecycleState, LifecycleTransition
```

### Step 2: Add Lifecycle Fields

For each identified model, add optional lifecycle fields:

```python
@dataclass
class WorkItem:
    # ... existing fields ...

    # MUX Lifecycle Integration (optional, backward compatible)
    lifecycle_state: Optional["LifecycleState"] = None
    lifecycle_history: List["LifecycleTransition"] = field(default_factory=list)
```

### Step 3: Add Helper Method (Optional)

If the model is a dataclass, consider adding a helper:

```python
def transition_lifecycle(self, to_state: "LifecycleState", reason: str = None) -> None:
    """Transition to a new lifecycle state, recording history."""
    from services.mux.lifecycle import LifecycleTransition

    if self.lifecycle_state is not None:
        transition = LifecycleTransition(
            from_state=self.lifecycle_state,
            to_state=to_state,
            reason=reason
        )
        self.lifecycle_history.append(transition)
    self.lifecycle_state = to_state
```

---

## Acceptance Criteria

- [ ] Import added without circular dependency errors
- [ ] Lifecycle fields are Optional (existing code unaffected)
- [ ] At least WorkItem has lifecycle support
- [ ] `pytest tests/unit/services/domain/ -v` passes (if tests exist)
- [ ] `pytest tests/unit/services/mux/ -v` still passes (302 tests)

---

## STOP Conditions

🛑 **STOP and escalate if**:
- Circular import that can't be resolved with TYPE_CHECKING
- Domain model file structure is different than expected
- Existing tests fail after changes
- Uncertainty about which models should have lifecycle

---

## Output Format

When complete, report:

```markdown
## Phase 0-1 Complete

### Files Modified
- `services/domain/models.py`: Added lifecycle to [list models]

### Import Strategy
[How circular imports were handled]

### Models Updated
| Model | Fields Added | Helper Method |
|-------|--------------|---------------|
| WorkItem | lifecycle_state, lifecycle_history | Yes/No |
| ... | ... | ... |

### Test Results
- Domain tests: [X passed / Y failed]
- MUX tests: 302 passed

### Issues Encountered
[Any issues and how they were resolved]
```

---

## Session Log Reminder

Update the session log at `/Users/xian/Development/piper-morgan/dev/2026/01/21/2026-01-21-0639-lead-code-opus-log.md` with your progress.

---

*Prompt created: 2026-01-21*
*Template version: 10.2*
