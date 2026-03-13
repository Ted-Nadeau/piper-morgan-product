# Agent Prompt: #685 MUX-LIFECYCLE-OBJECTS

## Your Identity
You are a Claude Code agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

---

## Mission
Wire lifecycle tracking for Feature and WorkItem objects. Connect existing infrastructure (backend, helpers, UI components) so users see lifecycle states with experience phrases.

**Scope Boundaries**:
- This prompt covers: Wiring initialization, transitions, and UI integration
- NOT in scope: Adding lifecycle to new object types, database persistence, composting pipeline
- All infrastructure exists: You are WIRING, not creating

---

## Context
- **GitHub Issue**: #685 - MUX-LIFECYCLE-OBJECTS
- **Current State**: Backend, helpers, domain fields, and UI all exist but aren't connected
- **Target State**: Objects get lifecycle_state set and displayed in UI
- **Dependencies**: #408 (CLOSED), #423 (CLOSED) - infrastructure complete
- **User Data Risk**: None (adding optional fields)
- **Infrastructure Verified**: Yes

---

## Key Files (READ THESE FIRST)

**Backend**:
- `services/mux/lifecycle.py` - LifecycleState enum, LifecycleManager, VALID_TRANSITIONS
- `services/mux/lifecycle_integration.py` - describe_with_lifecycle(), has_lifecycle()

**Domain Models**:
- `services/domain/models.py` - Feature and WorkItem with lifecycle_state fields

**UI Components**:
- `templates/components/lifecycle_indicator.html`
- `templates/components/lifecycle_detail.html`
- `templates/components/lifecycle_notification.html`

**Documentation**:
- `docs/internal/architecture/current/lifecycle-experience-guide.md`

---

## Phase 0: Verification

```bash
# Verify infrastructure exists
ls services/mux/lifecycle*.py
ls templates/components/lifecycle*.html
grep "lifecycle_state" services/domain/models.py

# Run existing lifecycle tests (must pass before changes)
PYTHONPATH=. pytest tests/unit/services/mux/test_lifecycle*.py -v
```

**STOP if**:
- [ ] Any lifecycle files missing
- [ ] Existing lifecycle tests fail
- [ ] Domain models don't have lifecycle_state field

---

## Phase 1: Lifecycle Initialization

### Tasks

1. **Add status-to-lifecycle mapping** to `services/mux/lifecycle_integration.py`:

```python
from services.mux.lifecycle import LifecycleState

WORKITEM_STATUS_TO_LIFECYCLE = {
    "open": LifecycleState.NOTICED,
    "in_progress": LifecycleState.RATIFIED,
    "done": LifecycleState.DEPRECATED,
    "closed": LifecycleState.ARCHIVED,
}

FEATURE_STATUS_TO_LIFECYCLE = {
    "draft": LifecycleState.EMERGENT,
    "proposed": LifecycleState.PROPOSED,
    "approved": LifecycleState.RATIFIED,
    "shipped": LifecycleState.DEPRECATED,
    "archived": LifecycleState.ARCHIVED,
}

def get_lifecycle_for_status(obj) -> Optional[LifecycleState]:
    """Get appropriate lifecycle state for object's current status."""
    if hasattr(obj, 'status'):
        if obj.__class__.__name__ == 'WorkItem':
            return WORKITEM_STATUS_TO_LIFECYCLE.get(obj.status)
        elif obj.__class__.__name__ == 'Feature':
            return FEATURE_STATUS_TO_LIFECYCLE.get(obj.status)
    return None

def initialize_lifecycle(obj) -> None:
    """Set initial lifecycle_state based on object's status."""
    if hasattr(obj, 'lifecycle_state') and obj.lifecycle_state is None:
        lifecycle = get_lifecycle_for_status(obj)
        if lifecycle:
            obj.lifecycle_state = lifecycle
```

2. **Add tests** in `tests/unit/services/mux/test_lifecycle_integration.py`:

```python
def test_workitem_open_maps_to_noticed():
    item = WorkItem(status="open")
    initialize_lifecycle(item)
    assert item.lifecycle_state == LifecycleState.NOTICED

def test_feature_draft_maps_to_emergent():
    feature = Feature(status="draft")
    initialize_lifecycle(feature)
    assert feature.lifecycle_state == LifecycleState.EMERGENT
```

### Validation
```bash
PYTHONPATH=. pytest tests/unit/services/mux/test_lifecycle_integration.py -v
```

---

## Phase 2: Automatic Transitions

### Tasks

1. **Add sync function** to `services/mux/lifecycle_integration.py`:

```python
from services.mux.lifecycle import LifecycleManager, InvalidTransitionError
import logging

logger = logging.getLogger(__name__)

def sync_lifecycle_to_status(obj) -> bool:
    """Sync lifecycle_state to match current status. Returns True if transitioned."""
    target_state = get_lifecycle_for_status(obj)
    if not target_state:
        return False

    if obj.lifecycle_state == target_state:
        return False  # Already correct

    if obj.lifecycle_state is None:
        # Initial set, not a transition
        obj.lifecycle_state = target_state
        return True

    try:
        manager = LifecycleManager()
        manager.transition(obj, target_state)
        return True
    except InvalidTransitionError as e:
        logger.warning(f"Lifecycle transition skipped for {obj}: {e.user_message}")
        return False
```

2. **Add tests** (10+):

```python
def test_sync_open_to_in_progress():
    item = WorkItem(status="open", lifecycle_state=LifecycleState.NOTICED)
    item.status = "in_progress"
    result = sync_lifecycle_to_status(item)
    assert result is True
    assert item.lifecycle_state == LifecycleState.RATIFIED

def test_sync_invalid_transition_handled():
    """Invalid transitions should log warning, not crash."""
    item = WorkItem(status="done", lifecycle_state=LifecycleState.ARCHIVED)
    item.status = "open"  # Would be backward transition
    result = sync_lifecycle_to_status(item)
    assert result is False  # Gracefully skipped
```

### Validation
```bash
PYTHONPATH=. pytest tests/unit/services/mux/test_lifecycle_integration.py -v
```

---

## Phase 3: UI Integration

### Tasks

1. **Find templates that display objects**:
```bash
grep -r "WorkItem\|work_item\|item\." templates/ --include="*.html"
grep -r "Feature\|feature\." templates/ --include="*.html"
```

2. **Add lifecycle indicator** where objects are displayed:

```html
{% if item.lifecycle_state %}
<div class="lifecycle-wrapper">
  {% include 'components/lifecycle_indicator.html' with stage=item.lifecycle_state.value expanded=false %}
</div>
{% endif %}
```

3. **Add template tests** in `tests/unit/templates/test_lifecycle_integration.py`:

```python
def test_workitem_display_includes_lifecycle_indicator():
    """WorkItem display should include lifecycle indicator when state set."""
    # Test that template includes lifecycle_indicator.html when lifecycle_state present

def test_lifecycle_indicator_shows_experience_phrase():
    """Indicator should show experience phrase, not technical label."""
```

### Validation
```bash
PYTHONPATH=. pytest tests/unit/templates/test_lifecycle*.py -v
```

---

## Phase 4: Transition Notifications

### Tasks

1. **Trigger notification on transition** in `sync_lifecycle_to_status()`:

```python
def sync_lifecycle_to_status(obj, notify: bool = True) -> bool:
    # ... existing transition logic ...

    if transitioned and notify:
        # Get transition explanation
        explanation = transition_explanation(
            old_state, target_state, str(obj)
        )
        # Notification will be trust-gated by the component
        _queue_lifecycle_notification(obj, explanation)
```

2. **Add tests**:

```python
def test_transition_queues_notification():
    """Successful transitions should queue notification."""
```

### Validation
```bash
PYTHONPATH=. pytest tests/unit/services/mux/test_lifecycle_integration.py -v
```

---

## Success Criteria

- [ ] New WorkItems get lifecycle_state based on status
- [ ] New Features get lifecycle_state based on status
- [ ] Status changes trigger lifecycle transitions
- [ ] Invalid transitions handled gracefully (logged, not crashed)
- [ ] Lifecycle indicator visible on object displays
- [ ] Experience phrases shown (not technical labels)
- [ ] 30+ new tests pass
- [ ] Existing 135 lifecycle tests still pass

---

## Evidence Requirements

Provide in your completion report:
1. `pytest tests/unit/services/mux/test_lifecycle*.py -v` output
2. `pytest tests/unit/templates/test_lifecycle*.py -v` output
3. Total test count confirmation (existing 135 + new 30+)
4. git diff showing changes

---

## Handoff Format

```
## Issue #685 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X new tests added
- pytest output: [paste]

**Files Modified**:
- [file] (+X/-Y lines)

**Verification**:
- Existing tests: [pass/fail count]
- New tests: [pass/fail count]

**Blockers** (if any):
- [description]
```

---

## STOP Conditions

- Existing lifecycle tests fail after changes
- Invalid transition mapping (backward movement)
- Experience phrases don't match lifecycle-experience-guide.md
- Can't locate object display templates
- UI components don't render

---

*Prompt Version: 1.0*
*Task: Integration/wiring (not new code)*
*Estimated Effort: Medium*
