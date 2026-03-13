# Gameplan: #685 MUX-LIFECYCLE-OBJECTS

**Issue**: #685 - Wire lifecycle tracking for object types
**Date**: 2026-01-26
**Author**: Lead Developer

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Backend lifecycle: `services/mux/lifecycle.py` (LifecycleState enum, LifecycleManager, 53 tests)
- [x] Integration helpers: `services/mux/lifecycle_integration.py` (describe_with_lifecycle, has_lifecycle, 20 tests)
- [x] Domain models: Feature & WorkItem have `lifecycle_state` and `lifecycle_history` fields
- [x] UI components: `lifecycle_indicator.html`, `lifecycle_detail.html`, `lifecycle_notification.html` (82 tests)
- [x] Command palette: 5 lifecycle filter commands exist

**My understanding of the task**:
- Wire initialization so new objects get lifecycle_state set
- Wire transitions so status changes update lifecycle_state
- Wire UI so lifecycle_indicator appears on object displays
- Wire notifications for Stage 3+ users

### Part A.2: Work Characteristics Assessment

**Worktree Assessment**:
- [ ] Multiple agents in parallel - NO (single agent)
- [ ] Task duration >30 min - MAYBE (medium complexity)
- [ ] Multi-component work - YES (backend + templates)
- [ ] Exploratory/risky changes - NO (wiring existing code)

**Assessment**: ☑️ **SKIP WORKTREE** - Single agent, wiring existing components, low risk

### Part B: PM Verification

**What actually exists**:
```bash
ls services/mux/lifecycle*.py
# lifecycle.py (LifecycleState, LifecycleManager, transitions)
# lifecycle_integration.py (helpers)

ls templates/components/lifecycle*.html
# lifecycle_indicator.html, lifecycle_detail.html, lifecycle_notification.html

grep "lifecycle_state" services/domain/models.py
# Feature and WorkItem both have the field
```

**Task type**:
- [x] Wire existing functionality together

### Part C: Decision

- [x] **PROCEED** - Infrastructure verified, task is clear wiring work

---

## Phase 0: Investigation

### GitHub Issue Verification
- [x] Issue #685 exists and is properly formatted (rewritten today)
- [x] Parent issues #408, #423 are CLOSED (infrastructure complete)
- [x] ADR-055 and lifecycle-experience-guide.md available

### Current State Verification
- [x] `LifecycleManager.transition()` exists and works
- [x] UI components render correctly (82 tests prove this)
- [x] Domain model fields exist but are never set

---

## Phase 0.5-0.8: N/A

These phases do not apply:
- Phase 0.5 (Frontend-Backend Contract): UI components already exist and tested
- Phase 0.6 (Data Flow): No new data flows, wiring existing
- Phase 0.7 (Conversation Design): No conversational feature
- Phase 0.8 (Post-Completion): No complex state to manage

---

## Phase 1: Lifecycle Initialization

**Objective**: Set lifecycle_state when objects are created

**Tasks**:
1. [ ] Create `_get_lifecycle_for_status()` mapping function in lifecycle_integration.py
2. [ ] Create `initialize_lifecycle(obj)` function
3. [ ] Identify WorkItem creation paths and add initialization
4. [ ] Identify Feature creation paths and add initialization
5. [ ] Add unit tests (5+)

**Status-to-Lifecycle Mapping**:

```python
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
```

**Deliverables**:
- `_get_lifecycle_for_status()` function
- `initialize_lifecycle()` function
- 5+ unit tests

---

## Phase 2: Automatic Transitions

**Objective**: Transition lifecycle_state when status changes

**Tasks**:
1. [ ] Create `sync_lifecycle_to_status(obj)` function
2. [ ] Handle invalid transition paths gracefully (log, don't crash)
3. [ ] Add to WorkItem status update hooks
4. [ ] Add to Feature status update hooks
5. [ ] Add unit tests (10+)

**Transition Logic**:
```python
def sync_lifecycle_to_status(obj):
    """Sync lifecycle_state to match current status."""
    target_state = _get_lifecycle_for_status(obj)
    if target_state and obj.lifecycle_state != target_state:
        try:
            manager = LifecycleManager()
            manager.transition(obj, target_state)
        except InvalidTransitionError as e:
            logger.warning(f"Lifecycle transition skipped: {e.user_message}")
```

**Deliverables**:
- `sync_lifecycle_to_status()` function
- Graceful error handling
- 10+ unit tests

---

## Phase 3: UI Integration

**Objective**: Show lifecycle indicator on object displays

**Tasks**:
1. [ ] Identify templates that display WorkItems
2. [ ] Identify templates that display Features
3. [ ] Add `{% include 'components/lifecycle_indicator.html' %}` with context
4. [ ] Wire click handler to show lifecycle_detail
5. [ ] Add template tests (10+)

**Integration Pattern**:
```html
{% if item.lifecycle_state %}
  {% include 'components/lifecycle_indicator.html' with stage=item.lifecycle_state.value %}
{% endif %}
```

**Deliverables**:
- Lifecycle indicator in WorkItem templates
- Lifecycle indicator in Feature templates
- Journey view accessible via click
- 10+ template tests

---

## Phase 4: Transition Notifications

**Objective**: Notify users when objects transition (Stage 3+ trust)

**Tasks**:
1. [ ] Wire notification trigger in `sync_lifecycle_to_status()`
2. [ ] Pass transition explanation to notification component
3. [ ] Verify trust-gating works (Stage 3+ only)
4. [ ] Add tests (5+)

**Deliverables**:
- Notifications appear on transition
- Trust-gated appropriately
- 5+ tests

---

## Verification Gates

- [ ] Phase 1 complete: New objects get lifecycle_state
- [ ] Phase 2 complete: Status changes trigger transitions
- [ ] Phase 3 complete: UI shows lifecycle indicators
- [ ] Phase 4 complete: Notifications work for Stage 3+
- [ ] Evidence: Test output showing all 30+ new tests pass

---

## Phase Z: Completion

**Tasks**:
1. [ ] Update #685 completion matrix
2. [ ] Add evidence (test output, screenshots)
3. [ ] Verify existing 135 lifecycle tests still pass
4. [ ] Update session log
5. [ ] Request PM review

---

## Agent Deployment

**Agent Type**: Opus (medium complexity, multiple integration points)
**Estimated Effort**: Medium
**Supervision**: Normal - clear requirements, existing patterns

---

## STOP Conditions

- Existing lifecycle tests fail
- Status-to-lifecycle mapping creates invalid transitions
- UI components don't render as expected
- Experience phrases don't match lifecycle-experience-guide.md
- Can't find object creation/update paths

---

## Success Criteria

- [ ] New WorkItems get lifecycle_state set
- [ ] New Features get lifecycle_state set
- [ ] Status changes trigger lifecycle transitions
- [ ] Lifecycle indicator visible on object displays
- [ ] Experience phrases shown (not technical labels)
- [ ] 30+ new tests pass
- [ ] Existing 135 lifecycle tests still pass
- [ ] Session log updated

---

*Gameplan ready for audit against template.*
