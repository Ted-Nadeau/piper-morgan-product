# Issue: ARCH-LAZY-WORKFLOW — Defer Workflow Creation to Async Handlers

## Summary

Currently, `process_intent` creates a workflow for ALL intents, but only one handler (`_handle_generic_query`) actually starts async work. This causes semantic confusion: 75 code paths return `workflow_id` without any async work occurring. Refactor to create workflows only when async work actually begins.

## Context

- **Discovered in M0**: #878 audit cascade found 75 code paths returning `workflow_id` with `error=None` but no async work
- **M0 fix**: Added `async_work_started` flag as tactical solution (commit `6042b7f9`)
- **Technical debt**: The flag is a workaround; proper fix is lazy workflow creation
- **Why now**: More async work is coming (WebSocket in M2, etc.). Semantic confusion will compound if not addressed.

## Current Behavior

```
User sends message
  → process_intent() creates workflow immediately
  → Handler runs (27 of 28 do NOT start async work)
  → Response includes workflow_id even though nothing is async
  → Frontend polls for status on work that doesn't exist
```

## Desired Behavior

```
User sends message
  → process_intent() runs handler
  → Handler that needs async work creates workflow at that point
  → Response includes workflow_id ONLY if async work started
  → Frontend polls only when meaningful
```

## Acceptance Criteria

- [ ] Workflow creation moved from `process_intent()` to individual handlers that need it
- [ ] Only `_handle_generic_query` (and future async handlers) create workflows
- [ ] `async_work_started` flag removed (no longer needed)
- [ ] Frontend polling unchanged (still uses `workflow_id` presence as signal)
- [ ] All existing tests pass
- [ ] No user-facing behavior change

## Technical Notes

From Architect memo (March 10, 2026):
> "Semantic confusion compounds; async work coming. 2-3 hour effort."

Files likely affected:
- `services/intent_service.py` — workflow creation logic
- `_handle_generic_query()` — receives workflow creation responsibility
- Integration tests for workflow polling

## Effort Estimate

- **Estimate**: 2-3 hours
- **Risk**: Low — refactoring existing pattern, not new functionality

## Sprint

M1 — Architecture track

## Labels

`architecture`, `tech-debt`, `m1-sprint`

---

*Issue drafted by PPM, March 11, 2026*
*Source: Chief Architect memo, M0 #878 audit cascade findings*
