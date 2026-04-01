# Issue: ARCH-LAZY-WORKFLOW — Defer workflow creation to async handlers

**Type**: Technical Debt / Architecture
**Priority**: Low (P3)
**Sprint**: M1 or Backlog
**Effort**: 2-3 hours
**Labels**: `architecture`, `technical-debt`, `intent-service`

---

## Context

During M0 CXO testing (March 1-2), we discovered that `process_intent()` creates a `Workflow` database row for **every** intent before routing to handlers. The `workflow_id` is passed to all 27+ handlers.

**Problem**: Only 1 of 27 handlers (`_handle_generic_query`) actually starts async work via the orchestration engine. The other 26 are fully synchronous.

**Tactical fix shipped** (commit `fix(intent): Restore 200 OK for business errors, strip spurious workflow_id`):
- Added `async_work_started: bool = False` to `IntentProcessingResult`
- Route layer strips `workflow_id` from responses unless `async_work_started=True`

This resolves the user-facing issue (60-second polling timeout) but leaves architectural debt.

---

## Problem Statement

Current architecture:
- Creates workflow row for every intent (27 workflows per 27 intents)
- 26 of those workflows are never used
- Unused workflows accumulate in "pending" state forever
- "Workflow" object now means two things (tracking vs. orchestration)

---

## Solution: Lazy Workflow Creation

Defer `Workflow` creation to handlers that actually need it.

### Before (current)
```python
workflow = workflow_service.create(intent_id=...)
result = handler(workflow_id=workflow.id, ...)
```

### After (proposed)
```python
def create_workflow_if_needed() -> str:
    return workflow_service.create(intent_id=...).id

result = handler(create_workflow=create_workflow_if_needed, ...)
# Handler calls create_workflow() only if starting async work
```

---

## Acceptance Criteria

- [ ] `process_intent()` no longer pre-creates Workflow objects
- [ ] Handlers receive `create_workflow` factory function instead of `workflow_id`
- [ ] `_handle_generic_query` (and future async handlers) call `create_workflow()` when starting async work
- [ ] Synchronous handlers never call `create_workflow()`
- [ ] No telemetry or logging regressions (verify call sites)
- [ ] Tests updated for new signature
- [ ] One-time migration to clean up orphaned workflow rows (optional, can defer)

---

## Implementation Phases

### Phase 1: Add factory parameter (30 min)
- Add `create_workflow: Callable[[], str]` to handler signature
- Update `_handle_generic_query` to call it
- Keep old `workflow_id` parameter temporarily for compatibility

### Phase 2: Remove pre-creation (1 hour)
- Remove `workflow_service.create()` from `process_intent()`
- Update all handler call sites
- Run full test suite

### Phase 3: Cleanup (30 min)
- Remove deprecated `workflow_id` parameter
- Verify no telemetry/logging breaks
- Update documentation

### Phase 4: Data migration (optional, 30 min)
- One-time script to delete orphaned workflows in "pending" state
- Or: leave them and let natural cleanup handle over time

---

## Risks

| Risk | Mitigation |
|------|------------|
| Telemetry depends on workflow existence | Audit call sites before removing pre-creation |
| Handler signature change breaks tests | Phase 1 maintains backward compatibility |
| Orphaned workflows cause issues | Phase 4 cleanup or natural expiration |

---

## Why Now (or Soon)

Async orchestration is coming in M1/M2:
- Multi-step planning
- Long-running analysis
- Background jobs

Better to have clean workflow semantics before adding more async use cases.

---

## References

- Lead Developer memo: `2026-03-03-async-workflow-architecture-decision.md`
- Related issues: #878, #876
- Tactical fix commit: `fix(intent): Restore 200 OK for business errors, strip spurious workflow_id`

---

*Drafted by Chief Architect, March 8, 2026*
