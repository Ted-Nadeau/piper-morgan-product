# Programmer Subagent B Prompt: #849 Calendar Router User-ID Threading (Category A)

## Your Identity

You are a Programmer Agent (prog-B) working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims. You report back to the Lead Developer.

## Session Log

Create a session log at: `dev/2026/02/25/2026-02-25-prog-b-code-opus-log.md`
Update it throughout your work with timestamped entries.

## GitHub Issue

**Issue**: #849 — SEC-KEYCHAIN: Comprehensive audit and fix of all non-scoped keychain retrieval paths

## Mission

Thread `user_id` through all CalendarIntegrationRouter instantiation sites that currently lack it. This is Category A from the issue — 5 sites where CalendarIntegrationRouter is created without user_id, meaning calendar operations use global keychain keys instead of user-scoped keys.

**Scope**: ONLY Category A (calendar router threading). Do NOT touch route-level keychain calls, OAuth handlers, or connection test endpoints.

## Critical Context: Why user_id Matters

CalendarIntegrationRouter.__init__ accepts `user_id: Optional[str] = None`. When user_id is provided, it passes it to the GoogleCalendarMCPAdapter, which uses it to construct user-scoped keychain key names like `f"google_calendar_{user_id}"`. Without user_id, global keys are used — which means in a multi-user deployment, calendar data would leak across users.

The CalendarIntegrationRouter constructor (from `services/integrations/calendar/calendar_integration_router.py`):

```python
def __init__(
    self,
    config_service: Optional[CalendarConfigService] = None,
    user_id: Optional[str] = None,
):
    # ...
    self._user_id = user_id
    # ...
    self.spatial_calendar = GoogleCalendarMCPAdapter(self.config_service, user_id=user_id)
```

Several methods in the codebase already correctly pass user_id (fixed by Issues #586, #843):
- `canonical_handlers.py:863` — `CalendarIntegrationRouter(user_id=user_id)` ✅
- `intent_service.py:3005, 3130, 3227` — `CalendarIntegrationRouter(user_id=user_id)` ✅
- `morning_standup.py:425, 569` — `CalendarIntegrationRouter(user_id=user_id)` ✅

The following 5 sites do NOT pass user_id.

## Multi-Agent Coordination

Subagent A is working in parallel on Categories B+C+D+E (route-level keychain fixes).
Your scope is Category A only. Do NOT modify:
- `web/api/routes/settings_integrations.py`
- `web/api/routes/integrations.py`
- `services/integrations/slack/oauth_handler.py`

## Pre-Flight Verification (MANDATORY FIRST ACTION)

Before making any changes:
1. Confirm each file listed below exists at the expected path
2. Confirm the line numbers are approximately correct (code may have shifted)
3. Confirm user_id availability in each caller chain as specified
4. Run existing tests BEFORE changes to establish a baseline:
   ```bash
   pytest tests/unit/ -v -k "calendar" 2>&1 | tail -30
   pytest tests/integration/test_calendar_integration.py -v 2>&1 | tail -30
   ```

If reality doesn't match this prompt, STOP and report the mismatch.

## Exact Changes Required

### Site A1: ConversationHandler._get_calendar_summary() — DEEP THREADING

**File**: `services/conversation/conversation_handler.py`

**Call chain** (innermost → outermost):
1. `_get_calendar_summary(self)` at line 130 — creates `CalendarIntegrationRouter()` without user_id
2. Called by `_respond_to_greeting(self, intent, session_id=None)` at line 162
3. Called by `respond(self, intent, session_id=None)` at line 106
4. Called by `CanonicalHandlers._handle_conversation_query(intent, session_id)` at line 4905 in `canonical_handlers.py`

**Required changes**:
1. Add `user_id: Optional[str] = None` parameter to `_get_calendar_summary(self, user_id=None)`
2. Change line 130 to: `calendar_router = CalendarIntegrationRouter(user_id=user_id)`
3. Add `user_id: Optional[str] = None` parameter to `_respond_to_greeting(self, intent, session_id=None, user_id=None)`
4. Update line 162 call: `calendar_summary = await self._get_calendar_summary(user_id=user_id)`
5. Add `user_id: Optional[str] = None` parameter to `respond(self, intent, session_id=None, user_id=None)`
6. Update line 106 call: `return await self._respond_to_greeting(intent, session_id, user_id=user_id)`
7. In `canonical_handlers.py`, update the call at line 4905: `result = await conversation_handler.respond(intent, session_id, user_id=user_id)`
8. **STOP CHECK**: Verify `_handle_conversation_query` has or can receive `user_id`. If it does NOT have `user_id`, you need to also add it to that method's signature and update its caller. Check before proceeding.

**Add comment at each changed site**: `# Issue #849: Thread user_id for user-scoped calendar auth`

### Site A2: IntentService._handle_attention_query() — SIMPLE

**File**: `services/intent/intent_service.py`

**Call chain**:
1. `_handle_attention_query(self, intent, workflow_id, session_id)` at line 3823 — creates `CalendarIntegrationRouter()` without user_id
2. Called by `_handle_query_intent(self, intent, workflow, session_id, user_id=None)` at line 1548

**Required changes**:
1. Add `user_id: Optional[str] = None` to `_handle_attention_query` signature
2. Change line 3823 to: `calendar_router = CalendarIntegrationRouter(user_id=user_id)`
3. Update caller at line 1548: `return await self._handle_attention_query(intent, workflow.id, session_id, user_id=user_id)`

### Site A3: CanonicalHandlers._get_calendar_context() — TWO CALLERS

**File**: `services/intent_service/canonical_handlers.py`

**The method** at line 1906: `calendar_router = CalendarIntegrationRouter()` — no user_id

**Caller 1** — `_handle_guidance_query(self, intent, session_id, user_id=None)` at line 4126:
- Already has `user_id` parameter. Just pass it through.

**Caller 2** — `_handle_agenda_query(self, intent, session_id)` at line 2922:
- Does NOT have `user_id`. Called by `_handle_temporal_query(self, intent, session_id, user_id=None)` at line 812.
- `_handle_temporal_query` HAS `user_id` — needs to be threaded through.

**Required changes**:
1. Add `user_id: Optional[str] = None` to `_get_calendar_context(self, user_id=None)`
2. Change line 1906 to: `calendar_router = CalendarIntegrationRouter(user_id=user_id)`
3. Update guidance caller at line 4126: `calendar_context = await self._get_calendar_context(user_id=user_id)`
4. Add `user_id: Optional[str] = None` to `_handle_agenda_query(self, intent, session_id, user_id=None)`
5. Update agenda's call at line 2922: `calendar_context = await self._get_calendar_context(user_id=user_id)`
6. Update temporal's call to agenda at line 812: `return await self._handle_agenda_query(intent, session_id, user_id=user_id)`

### Site A4: CalendarPlugin.__init__() — ARCHITECTURAL NOTE (LOW RISK)

**File**: `services/integrations/calendar/calendar_plugin.py`

**Current** at line 28: `self.integration_router = CalendarIntegrationRouter(self.config_service)` — no user_id

**Analysis**: CalendarPlugin is a **singleton** initialized at module level (`_calendar_plugin = CalendarPlugin()`). There is no user context available at initialization time. The `is_configured()` method already returns `False` unconditionally (Issue #784 fix) because it acknowledges this limitation. The plugin's integration_router is used only for feature flag checks (`use_spatial`, `allow_legacy`) and status metadata — NOT for authenticated calendar data access.

**Required change**: Add a comment explaining the architectural limitation:
```python
# Issue #849: CalendarPlugin is a singleton initialized without user context.
# This router is used for feature flags and status only, not authenticated data access.
# User-scoped calendar operations use ad-hoc CalendarIntegrationRouter(user_id=...) instances.
self.integration_router = CalendarIntegrationRouter(self.config_service)
```

**Do NOT attempt to refactor CalendarPlugin to accept user_id** — that would require architectural changes to the plugin system that are out of scope.

### Site A5: create_calendar_integration() Factory Function

**File**: `services/integrations/calendar/calendar_integration_router.py`

**Current** at line 474-481:
```python
def create_calendar_integration() -> CalendarIntegrationRouter:
    return CalendarIntegrationRouter()
```

**Required changes**:
```python
def create_calendar_integration(user_id: Optional[str] = None) -> CalendarIntegrationRouter:
    """
    Factory function to create CalendarIntegrationRouter instance.

    Args:
        user_id: Optional user ID for user-scoped keychain authentication

    Returns:
        CalendarIntegrationRouter: Configured router instance
    """
    return CalendarIntegrationRouter(user_id=user_id)
```

This function has no current production callers but should accept user_id for future-proofing.

## Method Signature Change Safety

When you modify method signatures, you MUST:
1. Keep `user_id` as an **optional keyword argument with default None** — this ensures backward compatibility
2. Search for ALL callers of each modified method (use `find_referencing_symbols` or grep)
3. Verify you haven't broken any callers that don't pass user_id — they should still work with the default None

## Testing Requirements

### Unit Tests to Write

1. **CalendarIntegrationRouter user_id propagation test**: Create router with user_id → verify `_user_id` is set and passed to adapter
2. **_get_calendar_summary with user_id**: Mock CalendarIntegrationRouter, call `_get_calendar_summary(user_id="test_user")`, verify router was created with `user_id="test_user"`
3. **_handle_attention_query with user_id**: Verify user_id flows from `_handle_query_intent` → `_handle_attention_query` → CalendarIntegrationRouter
4. **_get_calendar_context with user_id**: Verify both caller paths (guidance and agenda) propagate user_id to CalendarIntegrationRouter

### Run Existing Tests

After all changes, run:
```bash
pytest tests/unit/ -v -k "calendar"
pytest tests/integration/test_calendar_integration.py -v
pytest tests/integration/test_intent_wiring_integration.py -v
pytest tests/unit/services/ -v -k "canonical or intent_service or conversation"
```

Report ALL test output, not just "tests pass."

## STOP Conditions

- If `_handle_conversation_query` does NOT have user_id and its caller chain doesn't either → STOP and report (the threading depth may be too deep)
- If any method you need to modify has more than 5 callers → STOP and report (blast radius too large)
- If any existing test fails after your changes → STOP and report (do NOT decide if it's critical — the Lead Developer decides)
- If you find additional CalendarIntegrationRouter() sites not listed above → note them and continue with your assigned scope
- If CalendarPlugin's integration_router is used for authenticated operations → STOP and report

**When tests fail**: STOP immediately. Report the exact error output. Do NOT decide if the failure is "critical" or "pre-existing" — the Lead Developer decides. Report: which tests fail, exact error messages, and whether the failure existed in your baseline run.

## Self-Check Before Claiming Complete

- [ ] Every site listed in my scope (A1-A5) has been addressed
- [ ] Every modified method's callers have been verified (no broken call sites)
- [ ] All `user_id` parameters are optional with default None (backward-compatible)
- [ ] Tests run and FULL output captured (not "tests pass" but actual output)
- [ ] Session log updated with all changes
- [ ] No changes outside my assigned scope (no route-level files)
- [ ] STOP conditions checked — none triggered

## Evidence Requirements

Before reporting back, you MUST provide:
1. List of all files modified with exact paths
2. Full `pytest -v` output for all test runs (not just pass counts)
3. Any tests that were failing BEFORE your changes (baseline run output)
4. For each method signature change: confirmation that ALL callers were updated
5. Your session log location
6. **Cross-validation markers**: For each CalendarIntegrationRouter() site, the before/after grep so Lead can verify:
   - Example: `grep -n "CalendarIntegrationRouter()" services/conversation/conversation_handler.py` should return 0 matches after fix
   - Example: `grep -n "user_id=user_id" services/conversation/conversation_handler.py` should show the new pattern

## Handoff Format

```
## Issue #849 Subagent B Completion Report
**Status**: Complete/Partial/Blocked

**Category A Sites Fixed**:
- A1 (ConversationHandler._get_calendar_summary): [status]
- A2 (IntentService._handle_attention_query): [status]
- A3 (CanonicalHandlers._get_calendar_context): [status]
- A4 (CalendarPlugin.__init__): [status]
- A5 (create_calendar_integration): [status]

**Method Signatures Changed**:
- [method] in [file] — callers updated: [list]

**Tests**:
- X tests added in [location]
- `pytest [path] -v` output: [paste actual output]

**Files Modified**:
- [file1.py] (lines changed)
- [file2.py] (lines changed)

**Session Log**: dev/2026/02/25/2026-02-25-prog-b-code-opus-log.md

**Blockers** (if any):
- [description]
```
