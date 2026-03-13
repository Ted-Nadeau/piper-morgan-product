# Session Log: 2026-03-02-0709-lead-code-opus

**Role**: Lead Developer
**Branch**: `claude/m0-conversational-glue`
**Resumed from**: 2026-03-01 session (same context window)

## Session Start — 7:09 AM

### Carry-over from March 1

**Uncommitted work on branch** (pending PM smoke test):
- **#871**: Header cleanup — removed legacy POC header, collapsed greeting to compact line, moved subtext to chat placeholder
- **#875**: Fixed intent route error regression — restored 200 OK for business errors (was accidentally changed to 422 during Nov 2025 refactor)
  - `intent.py`: Replace `validation_error()` with 200 response + error metadata
  - `chat.js`: Guard workflow polling on `!result.error`
  - `test_api_degradation_integration.py`: Updated 3 tests, added 1 contract test
  - Design decision documented in intent.py module docstring

**Issues filed yesterday**:
- #871 — Remove legacy POC header area
- #872 — Planning workflow raw error (child of #875)
- #873 — Workflow timeout surfaces to user (child of #875)
- #874 — API error on issue query (child of #875)
- #875 — SYSTEMIC: Nov 2025 refactor broke error response contract
- #876 — TECH-DEBT: 56 raw error messages in intent_service.py

**Pending**: PM smoke test of #875 fix, then close #872/#873/#874/#875

## 7:09 AM — PM smoke test instructions provided, audit cascade on #876 started

## ~7:30 AM — Session resumed after compaction

### #876 Audit Cascade Results (completed in background)

**Scope**: All raw error messages in `services/intent/intent_service.py`

**Findings**: 54+ error messages across 30+ handler methods, categorized:

| Category | Count | Description | Fix Approach |
|----------|-------|-------------|--------------|
| **A: Raw exception leaks** | 27 | `f"Failed to X: {str(e)}"` — exposes Python internals | `safe_intent_handler` decorator |
| **B: Technical validation** | 17 | Comprehensible but not conversational | Validation helper library |
| **C: Infrastructure/timeout** | 4 | Already caught by Pattern-007 degradation | Already handled |
| **D: Already conversational** | 8+ | Good messages, no change needed | None |

**Key finding**: 27 Category A messages all follow the identical anti-pattern:
```python
except Exception as e:
    return IntentProcessingResult(success=False, message=f"Failed to X: {str(e)}")
```

**Recommended fix**: Single `safe_intent_handler` decorator wrapping handler exceptions → conversational fallback. Plus a validation helper library for Category B.

**Estimated effort**: ~9 hours total

Awaiting PM response to smoke test + these findings.

## 7:49-8:00 AM — PM smoke test results + investigation

### Smoke test findings from PM:
- **Test 1**: Partial success — reply is natural but (a) extraneous workflow triggered, (b) generic message loses capability context
- **Test 3**: "An API error occurred" — red error box instead of conversational

### Investigation results:

**Test 3 root cause: Server not restarted**
- Server PID 41689 started Sun Mar 1 3:59 PM — BEFORE our fix was applied (~8 PM)
- Running old code with `validation_error()` → 422 → "An API error occurred"
- **Fixed**: Killed old process, restarted server. Now returns 200 with error in body. ✅

**Extraneous workflow (#878 filed)**
- Unhandled action fallback returns `workflow_id=workflow.id` but `error=None`
- `!result.error` guard doesn't catch because error is None

**Classification non-determinism**
- LLM classifier has no `temperature=0` → same message routes differently each call
- "Q3 planning" can be STRATEGY (informative) or EXECUTION (generic fallback)

**GitHubIntegrationRouter.create_issue() (#879 filed)**
- Domain service passes `assignees` but router doesn't accept it → TypeError
- Pre-existing bug blocking all issue creation via intent handler

### Issues filed:
- #878 — Extraneous workflow polling on unhandled action fallbacks
- #879 — GitHubIntegrationRouter.create_issue() missing assignees parameter
- #880 — Calendar credential setup fails with 401 Unauthorized

## 5:19-6:30 PM — PM re-test results + #878 fix

### PM re-test:
- **Test 1**: STRATEGY → strategic_planning → "Cannot create plan: planning type not specified" (raw #876)
- **Test 3**: Pass ✅ — error displays in chat, not red box
- **Test 4**: Pass ✅ — compact greeting

### #878 Audit Cascade Results:
- **75 code paths** return workflow_id with error=None (not just 2)
- 14 fallback/unhandled + 22 validation failures + 37 "legitimate" handlers
- Root cause: architectural — process_intent creates workflow for ALL intents, passes through to all handlers
- No handler actually starts async work — workflow_id is tracking-only

### #878 Fix (4 changes):
1. `intent_service.py:4468` — unhandled EXECUTION: `workflow_id=None`
2. `intent_service.py:7224` — generic STRATEGY: `workflow_id=None`
3. `intent.py:345-346` — route filter: strip workflow_id when `not result.success or result.error or result.requires_clarification`
4. `chat.js:458` — safety net: added `&& !result.requires_clarification` to polling guard

### Verification:
- 11 integration tests: all pass
- curl test (planning query): `workflow_id: null` ✅
- curl test (bug report): `workflow_id: null, error: set` ✅

## ~6:30 PM — Issues closed, session wrap-up

### Issues closed with evidence:
- **#875** ✅ — SYSTEMIC: Nov 2025 refactor broke error response contract
- **#872** ✅ — Planning workflow raw error (child of #875)
- **#873** ✅ — Workflow timeout surfaces to user (child of #875 + #878)
- **#874** ✅ — API error on issue query (child of #875)
- **#878** ✅ — Extraneous workflow polling on unhandled action fallbacks

### Issues filed today:
- #878 — Extraneous workflow polling → fixed and closed
- #879 — GitHubIntegrationRouter.create_issue() missing assignees param → open
- #880 — Calendar credential setup fails with 401 → open (PM to triage)

### Uncommitted work on `claude/m0-conversational-glue`:
- **#871**: Header cleanup (templates/home.html, templates/components/chat-inline.html)
- **#875**: Error response fix (intent.py, chat.js, test_api_degradation_integration.py)
- **#878**: Workflow polling fix (intent_service.py ×2, intent.py, chat.js)

### Open items for tomorrow:
1. **Commit all uncommitted work** (#871, #875, #878)
2. **#876**: Raw error message humanization (~9 hours)
   - Category A: 27 raw exception leaks → `safe_intent_handler` decorator
   - Category B: 17 technical validation msgs → conversational helpers
3. **#879**: GitHubIntegrationRouter.create_issue() signature fix (quick)
4. **#878 remaining**: 37 success-path handlers still pass workflow_id (strip unconditionally?)
5. **Start/stop scripts**: Update to match current architecture; add restart script
6. **Classifier determinism**: Pre-classifier rule for planning + temperature=0

### Session end: ~6:30 PM
