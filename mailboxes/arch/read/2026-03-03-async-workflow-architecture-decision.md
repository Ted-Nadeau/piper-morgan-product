# Memo: Async Workflow Architecture Decision Needed

**From**: Lead Developer
**Date**: 2026-03-03
**Priority**: Low (no user-facing urgency)
**Related issues**: #878, #876

## Context

During M0 CXO testing (March 1-2), we discovered that `process_intent()` creates a workflow object for **every** intent before routing to handlers. The `workflow_id` is passed to all 27+ handlers. The frontend polls any non-null `workflow_id` for status, expecting async work to complete.

**Problem**: Only 1 of 27 handlers (`_handle_generic_query`) actually starts async work via the orchestration engine. The other 26 are fully synchronous — they call a service, get a result, and return it immediately. The leaked `workflow_id` caused the frontend to poll for 60 seconds then show a timeout error after every successful response.

## What We Did (Tactical Fix)

Added `async_work_started: bool = False` to `IntentProcessingResult`. The route layer strips `workflow_id` from responses unless `async_work_started=True`. This is explicit, forward-compatible, and requires ~0 effort for new handlers (default is False; async handlers opt in).

Commit: `fix(intent): Restore 200 OK for business errors, strip spurious workflow_id (#875, #878)`

## Decision Needed

The current architecture creates a workflow row in the database for every intent, even ones that never use it. This is:
- Wasted DB writes (27 workflows created per 27 intents, 26 never used)
- Confusing (workflow objects exist in "pending" state forever)
- Architectural debt (workflow was designed for orchestration, not tracking)

### Options for the future

**Option A: Lazy workflow creation**
Defer `Workflow` creation to handlers that need it. Pass a `create_workflow()` factory function instead of a pre-created `workflow_id`. Only `_handle_generic_query` (and future async handlers) call it.
- Pro: Eliminates wasted DB writes, cleaner semantics
- Con: Moderate refactor (~2-3 hours), need to verify telemetry/logging isn't depending on workflow existence

**Option B: Keep current architecture, use async_work_started as permanent flag**
Accept that workflows are created for tracking/telemetry. The `async_work_started` flag already solves the frontend polling issue.
- Pro: Zero additional work
- Con: DB accumulates unused workflow rows; "workflow" means two different things

**Option C: Replace workflows with a lighter telemetry mechanism**
If workflows are only used for tracking (not orchestration), replace with a simpler intent log table.
- Pro: Right-sized for actual needs
- Con: Larger refactor, needs design

### Recommendation

Option A is the cleanest if async orchestration is coming soon (e.g., for long-running analysis, multi-step planning). Option B is fine if workflows remain unused for the foreseeable future.

Please advise which direction to take so we can log it as a tracked issue and triage it appropriately.
