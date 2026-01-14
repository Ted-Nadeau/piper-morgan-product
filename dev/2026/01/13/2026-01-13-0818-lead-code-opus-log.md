# Lead Developer Session Log

**Date**: 2026-01-13
**Started**: 08:18
**Role**: Lead Developer (Claude Code Opus)
**Focus**: Alpha Testing Sprint A20 - End-to-End Bug Fixes

---

## Session Context

Starting new alpha testing sprint (A20) focused on end-to-end bug fixes discovered during v0.8.4 testing. The philosophy: "finishing is better than skipping stuff" - we'll stay on bug fixes until the system is solid before moving to MUX super-epics.

Yesterday (2026-01-12) was a full day:
- Morning: Released v0.8.4, updated release runbook, processed alpha feedback
- Evening: Fixed Issue #582 (standup/portfolio integration bug)

---

## 08:18 - Session Start

### Yesterday's Tail Review

From `dev/2026/01/12/2026-01-12-0830-lead-code-opus-log.md`:

**Issue #582 Fix** (completed):
- Root cause: Portfolio onboarding stored projects in `projects` table, but standup/status read from `User.preferences` or `PIPER.md`
- Fix: `UserContextService` now queries database directly via `ProjectRepository.list_active_projects()`
- Commit: `c7d58927 fix(#582): Connect UserContextService to database projects`

**New Issues Filed**:
- **#583**: Chat persistence regression (messages not showing on refresh)
- **#584**: Tech debt - Document user_id vs session_id patterns
- **#585**: Standup routing - `/standup` routes to STATUS handler instead of interactive standup flow

**Key Insight**: The "75% pattern" struck again - portfolio onboarding worked, but output wasn't connected to consuming features.

---

## Immediate Backlog (Sprint A20)

### Open Issues from Yesterday

| Issue | Title | Priority | Status |
|-------|-------|----------|--------|
| #583 | Chat persistence regression | P1 | Open |
| #584 | Tech debt: user_id vs session_id docs | P2 | Open |
| #585 | Standup routing to interactive flow | P1 | Open |

### Beads Status

✅ All beads are closed - clean slate for Sprint A20.

---

## Sprint A20 Scope

### Immediate Priority (Yesterday's Bugs)

| Issue | Title | Priority | Notes |
|-------|-------|----------|-------|
| **#583** | Chat persistence regression | **P1** | Piper's replies not showing on refresh |
| **#585** | Standup routing broken | **P1** | `/standup` → STATUS handler, not interactive flow |
| **#584** | user_id vs session_id docs | P2 | Tech debt - prevent future confusion |

### Related Open Issues (May Surface During Testing)

| Issue | Title | Notes |
|-------|-------|-------|
| #561 | Portfolio onboarding flow design | May be related to #585 |
| #558 | LLM preference extraction | Post-standup enhancement |
| #557 | WebSocket infrastructure | Could fix #583 properly |

### MUX Issues (Deferred Until A20 Complete)

#531-534 (Gates 1-4), #488, #551, #567-569 - all waiting for stable foundation.

---

## Work Log

### 08:18 - Session Start

Reviewed yesterday's log, checked beads (all closed), checked GitHub issues.

Sprint A20 focus: Fix #583 and #585 to complete the standup/portfolio end-to-end flow.

---

### 08:23 - PM Established Rigorous 6-Step Process for #583

PM approved a systematic approach with template compliance audits at each stage:
1. Audit GitHub issue against feature.md template
2. Write gameplan with five-whys investigation
3. Audit gameplan against gameplan-template v9.3
4. Write subagent prompts with TDD cross-check approach
5. Audit prompts against agent-prompt-template v10.2
6. Execute with cross-checking agents (sequential with gate approvals)

### 08:44 - Steps 1-5 Completed

- Step 1: Audited #583 (Grade D → A after updates)
- Step 2: Created `dev/2026/01/13/gameplan-583-chat-persistence.md`
- Step 3: Audited gameplan (PM-approved skip of Phase 0.7)
- Step 4: Created `dev/2026/01/13/prompts-583-chat-persistence.md` (4 agent prompts)
- Step 5: Audited prompts (100% compliance)

### 08:58 - Phase 0: Investigation Began

PM approved: "yes, please proceed!"

### 09:15 - Root Cause Identified

**Phase 0 Investigation Complete**

#### Five Whys Analysis

**Why #1**: Are assistant messages being saved to the database?
- **YES** - Verified via direct SQL query:
  ```sql
  SELECT turn_number, user_message, assistant_response FROM conversation_turns
  WHERE conversation_id = '5d0f273d-e87e-4b06-a24a-9e812357635f';
  ```
  Result: 10 turns, all with both `user_message` and `assistant_response` populated ✅

**Why #2**: Does the API return assistant messages?
- **YES** - `GET /api/v1/conversations/{id}/turns` returns `ConversationTurnResponse` with both fields
- Location: `web/api/routes/conversations.py:179-188` ✅

**Why #3**: Does frontend code render assistant messages?
- **YES** - `templates/home.html:1481-1482` calls `appendMessage()` for both:
  ```javascript
  ChatWidget.appendMessage(turn.user_message, true, false, timestamp);
  ChatWidget.appendMessage(turn.assistant_response, false, false, timestamp);
  ```
  ✅

**Why #4**: Is the rendering function called on page refresh?
- **NO** - `switchConversation()` is only called when URL has `?conversation=xxx` parameter
- On plain refresh, `conversationId = params.get('conversation')` returns `null`
- Location: `templates/home.html:1553-1574` ❌

**Why #5**: What runs instead on page refresh?
- `chat.js:restoreChatHistory()` loads from **localStorage** (stale, max 50 messages)
- Database turns are never fetched

#### ROOT CAUSE

**File**: `templates/home.html`
**Lines**: 1550-1574 (`initSidebar` function)

```javascript
function initSidebar() {
  const params = new URLSearchParams(window.location.search);
  const conversationId = params.get('conversation');  // NULL on plain refresh
  // ...
  loadConversations();

  if (conversationId) {       // <-- SKIPPED when null
    switchConversation(conversationId);
  }
}
```

**The bug**: On page refresh without URL parameter, no conversation is auto-loaded from database. Only stale localStorage history is shown.

**The 75% Pattern**: Database persistence was implemented (#563), but the "restore on page load" logic was incomplete.

#### Proposed Fix Options

**Option A**: Auto-select most recent conversation on page load
- Modify `initSidebar()` to call `switchConversation()` with first conversation from list

**Option B**: Persist active conversation ID in localStorage
- Store `activeConversationId` when user switches conversations
- Restore from localStorage on page load

**Option C**: Add conversation ID to URL on navigation
- Update `switchConversation()` to update URL (history.pushState)
- On refresh, URL already contains the conversation ID

**Recommendation**: Option A or B (simplest). Option C is more robust but higher effort.

---

## Gate 0→1: PM Approved (9:24)

**Root cause identified with evidence. PM approved proceeding to Phase 1.**

---

### Phase 1: TDD Test Writer (9:29)

**Mission**: Write tests that verify the backend works correctly (proving the bug is frontend-only).

**Tests Written**:
- `tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_returns_both_user_message_and_assistant_response_issue_583` - Verifies API returns both fields
- `tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_returns_empty_list_for_new_conversation_no_turns_issue_583` - Empty list for new conversation
- `tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_response_model_includes_required_fields_issue_583` - Response model validation
- `tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_returns_empty_for_unauthorized_conversation_issue_583` - Security test
- `tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_returns_empty_for_nonexistent_conversation_issue_583` - Security test
- `tests/unit/web/api/routes/test_conversations.py::TestConversationTurnResponseModel::test_model_has_both_message_fields` - Model contract test
- `tests/unit/web/api/routes/test_conversations.py::TestConversationTurnResponseModel::test_model_validates_required_fields` - Model validation

**Test Results (ALL PASS - Backend Works)**:
```
============================= test session starts ==============================
platform darwin -- Python 3.12.10, pytest-7.4.3, pluggy-1.6.0
collected 7 items

tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_returns_both_user_message_and_assistant_response_issue_583 PASSED
tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_returns_empty_list_for_new_conversation_no_turns_issue_583 PASSED
tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_response_model_includes_required_fields_issue_583 PASSED
tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_returns_empty_for_unauthorized_conversation_issue_583 PASSED
tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_returns_empty_for_nonexistent_conversation_issue_583 PASSED
tests/unit/web/api/routes/test_conversations.py::TestConversationTurnResponseModel::test_model_has_both_message_fields PASSED
tests/unit/web/api/routes/test_conversations.py::TestConversationTurnResponseModel::test_model_validates_required_fields PASSED

======================== 7 passed, 6 warnings in 0.31s =========================
```

**Existing Integration Test Also Passes**:
```
tests/integration/services/test_conversation_repository.py::TestConversationRepositoryRoundTrip::test_both_user_and_assistant_messages_persist PASSED
```

**Frontend Fix Requirement**:

The fix must ensure that on page refresh (without URL parameter), the most recent or previously active conversation is automatically loaded from the database. The `initSidebar()` function at `templates/home.html:1550-1574` currently only calls `switchConversation()` when `?conversation=xxx` is in URL.

**Recommended Fix Approaches**:

1. **Store activeConversationId in localStorage, restore on load**:
   - When `setActiveConversation(id)` is called, also save to `localStorage.setItem('lastConversationId', id)`
   - In `initSidebar()`, if no URL param, check `localStorage.getItem('lastConversationId')`
   - Call `switchConversation()` with that ID

2. **Auto-select first conversation from list**:
   - After `loadConversations()` completes, if no URL param and no localStorage ID
   - Auto-call `switchConversation()` with the first conversation in the list

**Critical Note**: The backend (repository + API) works correctly. This is 100% a frontend JavaScript bug in `initSidebar()`.

**Phase 1 Complete** - Ready for Phase 2 (Implementer Agent)

---

## Gate 1→2: PM Approved (9:41)

**PM Feedback**: Prompts could have been better researched - I assumed a `role` column schema but actual schema uses paired `user_message`/`assistant_response` columns.

**Methodology Improvement**: Add to prompt-writing process: "Verify actual schema/infrastructure before writing test templates." A quick `\d conversation_turns` before Step 4 would have caught this.

**Process Question (for CIO review)**: How do we ensure infrastructure verification happens when appropriate?

*Current gap*: Step 4 (Write Prompts) came after Step 3 (Audit Gameplan) but before any actual code reading. The prompts included test code templates based on assumed schema rather than verified schema.

*Proposed guardrail*: Add to prompt-writing checklist:
- [ ] **Schema verified?** If prompts reference database tables, run `\d tablename` first
- [ ] **API contracts verified?** If prompts reference endpoints, read the actual route handler
- [ ] **Code patterns verified?** If prompts assume patterns, grep for actual implementations

*Why this matters*: Prompts guide subagents. Wrong assumptions in prompts propagate to subagent work, requiring rework. The Test Writer agent had to adapt on the fly because my prompts assumed `role` column but reality was `user_message`/`assistant_response` paired columns.

*Broader principle*: "Verify before you specify" - any specification (gameplan, prompt, test template) that references infrastructure should verify that infrastructure first. This is analogous to the "VERIFY FIRST, CREATE SECOND" rule in CLAUDE.md but applied to planning artifacts, not just code.

**Fix Approach Approved**: Option B - Store `activeConversationId` in localStorage, restore on load.

---

### Phase 2: Implementer Agent (9:41)

**Implementation Complete**

**Files Modified**:
- `templates/home.html` - Added localStorage persistence for activeConversationId

**Changes**:

1. **`setActiveConversation()` (lines 1436-1441)** - Now saves ID to localStorage:
   ```javascript
   // Issue #583: Persist to localStorage for refresh recovery
   if (id) {
     localStorage.setItem('piper_active_conversation_id', id);
   } else {
     localStorage.removeItem('piper_active_conversation_id');
   }
   ```

2. **`initSidebar()` (lines 1561-1566)** - Now checks localStorage if no URL parameter:
   ```javascript
   let conversationId = params.get('conversation');

   // Issue #583: If no URL param, try localStorage for refresh recovery
   if (!conversationId) {
     conversationId = localStorage.getItem('piper_active_conversation_id');
   }
   ```

**Test Results**:

```
============================= test session starts ==============================
tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_returns_both_user_message_and_assistant_response_issue_583 PASSED
tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_returns_empty_list_for_new_conversation_no_turns_issue_583 PASSED
tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_response_model_includes_required_fields_issue_583 PASSED
tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_returns_empty_for_unauthorized_conversation_issue_583 PASSED
tests/unit/web/api/routes/test_conversations.py::TestGetConversationTurns::test_returns_empty_for_nonexistent_conversation_issue_583 PASSED
tests/unit/web/api/routes/test_conversations.py::TestConversationTurnResponseModel::test_model_has_both_message_fields PASSED
tests/unit/web/api/routes/test_conversations.py::TestConversationTurnResponseModel::test_model_validates_required_fields PASSED

======================== 7 passed, 6 warnings in 0.21s =========================
```

**Smoke Tests**: 614 passed, 1 skipped (clean)

**Edge Case Handling**: If localStorage has an ID for a deleted conversation, `switchConversation()` will fail gracefully (existing error handling via Toast.error) and the user will simply see an empty chat with the conversation list available.

---

## Gate 2→3: PM Approved (10:21)

**Phase 2 Complete**. Proceeding to Phase 3 (Auditor/Cross-validation).

---

### Methodology Note: The "Last Mile" Gap Pattern

**Observation from #583**: The database persistence (#563) was implemented correctly, but screen refresh behavior was not considered. This is a "last mile" gap - the core feature works, but the user experience loop isn't closed.

**Pattern Recognition**: When implementing persistence/state features, ask:
1. **Save path**: Does data get saved? ✅ (usually tested)
2. **Retrieve path**: Can data be retrieved? ✅ (usually tested)
3. **Restore path**: Does the UI **automatically restore** on page load/refresh? ❌ (often missed)

**Why it's missed**: The restore path requires "remembering" to think about it. If something requires remembering, it's not yet internalized in the mental model.

**Proposed Guardrail**: Add to feature completion checklist:
- [ ] **Persistence Loop Complete?** If this feature saves state, verify:
  - Save works (unit test)
  - Retrieve works (unit test)
  - **Auto-restore on page load works** (integration test)
  - **Auto-restore after refresh works** (E2E test)

**Action Item**: Consider adding this to `docs/internal/development/checklists/` or the feature.md template as a mandatory section for state/persistence features.

---

### Phase 3: Auditor Agent - Cross-Validation (10:23)

**Mission**: Independent verification of Issue #583 fix. Did NOT write the tests or implementation.

---

## Issue #583 Audit Report

### Code Review

| Check | Result | Evidence |
|-------|--------|----------|
| Changes address root cause | **PASS** | localStorage persistence fills the gap where URL param was missing on refresh |
| localStorage used correctly | **PASS** | Key `piper_active_conversation_id` used consistently at lines 1438, 1440, 1565 |
| Save logic correct | **PASS** | `setActiveConversation()` saves when ID truthy, removes when falsy |
| Restore logic correct | **PASS** | `initSidebar()` checks URL first, then localStorage as fallback |
| Edge cases handled | **PARTIAL** | See "Minor Issue" below |

### Implementation Logic Verification

**Save path** (`setActiveConversation()` at lines 1436-1441):
```javascript
// Issue #583: Persist to localStorage for refresh recovery
if (id) {
  localStorage.setItem('piper_active_conversation_id', id);
} else {
  localStorage.removeItem('piper_active_conversation_id');
}
```
**Verdict**: Correct - saves ID when set, clears when cleared.

**Restore path** (`initSidebar()` at lines 1558-1587):
```javascript
let conversationId = params.get('conversation');

// Issue #583: If no URL param, try localStorage for refresh recovery
if (!conversationId) {
  conversationId = localStorage.getItem('piper_active_conversation_id');
}
// ...
if (conversationId) {
  switchConversation(conversationId);
}
```
**Verdict**: Correct - URL param takes precedence, localStorage is fallback, then loads via `switchConversation()`.

### Test Results

| Test Suite | Result | Count |
|------------|--------|-------|
| Issue #583 specific tests | **PASS** | 7 passed |
| Conversation unit tests | **PASS** | 149 passed, 4 skipped |
| Smoke tests | **PASS** | 614 passed, 1 skipped |

Full test output available in audit run.

### Edge Case Analysis

| Scenario | Expected | Actual | Status |
|----------|----------|--------|--------|
| First-time user (no localStorage, no conversations) | No auto-load | No auto-load | **PASS** |
| User with localStorage ID but conversation deleted | Show error, allow manual recovery | Toast error shown, **but localStorage not cleared** | **MINOR ISSUE** |
| User clears localStorage | Fall back to no auto-load | Falls back correctly | **PASS** |
| Multiple browser tabs | Last active conversation wins | Shared localStorage | **ACCEPTABLE** |

### Minor Issue Found

**Issue**: When a user has a conversation ID saved in localStorage but that conversation has been deleted (e.g., via database cleanup or another session), the following happens:

1. `initSidebar()` retrieves the stale ID from localStorage
2. `switchConversation(staleId)` is called
3. Fetch returns 404
4. Error toast shown to user
5. **localStorage is NOT cleared**
6. On next refresh, same error occurs

**Severity**: Low - User can recover by clicking any conversation in the list, which will update localStorage. The error doesn't prevent app usage.

**Recommended Follow-up** (not blocking sign-off):
```javascript
// In switchConversation catch block:
} catch (error) {
  console.error('Failed to load conversation:', error);
  Toast.error('Failed to load conversation', error.message);
  // Clear stale localStorage to prevent repeat failures
  if (error.message.includes('404')) {
    localStorage.removeItem('piper_active_conversation_id');
  }
}
```

### Manual Verification Steps

Server confirmed running (received 401 at `http://localhost:8001/` - auth required but server responding).

**Steps for PM to verify manually**:
1. Open browser, navigate to `http://localhost:8001/` and log in
2. Send a message, get a response from Piper
3. Note which conversation is active in sidebar
4. Refresh the page (F5)
5. **Expected**: Same conversation loads with all messages visible
6. **Verify**: Check browser console - should see `[DEBUG #574] Fetching turns for: <conversation-id>`

### Security Check

- No sensitive data stored in localStorage (only conversation UUID)
- localStorage is per-origin, no cross-site concerns
- No security regressions identified

---

## Sign-Off

**APPROVED** - The fix correctly addresses the root cause (Issue #583).

**Conditions**:
- All tests pass (770+ tests verified)
- Code changes are minimal and focused
- Logic flow is correct
- Minor edge case (deleted conversation) is low-severity and doesn't block functionality

**Recommended**: File follow-up issue for the "stale localStorage ID on deleted conversation" edge case cleanup. Not blocking for Issue #583 closure.

---

**Auditor**: Claude Code Opus (Auditor Agent)
**Timestamp**: 2026-01-13 10:28

---

## Gate 3→Z: Awaiting Final PM Approval

**Audit Result**: APPROVED

**Summary**:
- Root cause identified ✅
- Tests written (7 unit tests) ✅
- Fix implemented (localStorage persistence) ✅
- Cross-validation passed ✅
- All tests pass (770+) ✅

**Minor Issue**: ~~Stale localStorage ID on deleted conversation causes repeat error on refresh.~~ **FIXED** (10:35) - Added `localStorage.removeItem()` in catch block at line 1502.

**Additional Fix** (10:43): PM correctly identified that Option B alone was insufficient - new sessions with no localStorage wouldn't auto-load any conversation. Added Option A (auto-select most recent) to work in combination:

**Final Implementation** (3-tier fallback):
1. URL parameter `?conversation=xxx` (explicit link)
2. localStorage `piper_active_conversation_id` (refresh recovery)
3. Most recent conversation from API (default for new sessions)

**Changes**:
- `loadConversations()` now returns first conversation ID
- `initSidebar()` now async, uses `targetConversationId = conversationId || firstConversationId`

---

## Gate 3→Z: PM Verified (10:50)

**Manual Testing**: PM confirmed all scenarios work:
- Fresh session (no localStorage) → auto-loads most recent conversation ✅
- Page refresh → restores previous conversation ✅
- Deleted conversation in localStorage → graceful error, clears stale ID ✅

**Ready for**:
1. Issue #583 closure
2. Commit to main branch

---

## Evening Session: 7:00 PM - 10:31 PM PT

### Session Focus
Continuation session focused on completing calendar timezone fix (#586) verification and discovering/fixing the root cause of calendar queries not working (#589).

---

### #586 - Calendar Timezone-Aware Queries
**Status**: ✅ Closed with evidence

- Resumed from earlier session where implementation was complete
- Ran manual verification - discovered calendar adapter WORKS (returns 7 events)
- Root cause of "no meetings" was NOT the adapter - it was intent routing
- Closed with evidence showing adapter returns real calendar data

### #589 - Intent Classifier Routes Calendar to TEMPORAL
**Status**: ✅ Closed with evidence

**Root Cause**: `PreClassifier` in `services/intent_service/pre_classifier.py` had calendar patterns ("what's on my calendar") in `TEMPORAL_PATTERNS` instead of `CALENDAR_QUERY_PATTERNS`.

**Fix Applied**:
1. Added calendar patterns to `CALENDAR_QUERY_PATTERNS`
2. Updated action mapping to `meeting_time` (matches IntentService handler)
3. Calendar patterns checked BEFORE temporal patterns

**Evidence**:
```bash
curl -X POST http://localhost:8001/api/v1/intent \
  -d '{"message": "What is on my calendar today?"}'
# Response: category=query, action=meeting_time, 7 meetings returned
```

**Tests**: 1730 unit tests pass, 16 new tests added

### Issue Audit (6:43 PM)
**Status**: ✅ Complete

- Audited all closed issues from 01/13 (#581-585)
- Fixed #581, #582, #583 with proper completion evidence
- Audited 01/12 issues - all OK

### New Issues Filed

| Issue | Description | Status |
|-------|-------------|--------|
| #587 | Sidebar ordering bug - new conversations below old | Open |
| #588 | "Tomorrow" intent not understood | Open |
| #589 | Calendar → TEMPORAL routing | ✅ Closed |
| #590 | Missing test_client fixture | Open |
| #591 | CICD spatial test assertion failure | Open |

### Files Modified (Evening Session)

| File | Change |
|------|--------|
| `services/intent_service/pre_classifier.py` | Added calendar patterns to CALENDAR_QUERY_PATTERNS |
| `services/queries/query_router.py` | Added backup calendar patterns |
| `tests/unit/services/queries/test_query_router_calendar.py` | New - 10 unit tests |
| `tests/integration/services/intent/test_calendar_intent_routing.py` | New - 6 routing integration tests |
| `tests/unit/services/intent_service/test_calendar_query_handlers.py` | Updated action names |

### Gameplans Created

- `gameplan-589-calendar-intent-routing.md` - Audited against template v9.3

### Key Learnings

1. **Two classifiers exist**: `PreClassifier` (rule-based, checked first) and `QueryRouter._rule_based_classification()` (different code path). The PreClassifier was the culprit.

2. **Cache can hide fixes**: After code changes, stale intent cache can return old classifications. Server restart clears cache.

3. **Pattern order matters**: Calendar patterns MUST be checked before temporal patterns because "what's on my calendar today" contains "today" which could match temporal.

### Test Results

```
1730 unit tests pass
16 new tests (10 unit + 6 integration)
Pre-existing integration test failures filed as #590, #591
```

### End State

- Calendar feature **working end-to-end**
- "What's on my calendar today?" returns 7 actual meetings
- "What time is it?" still works (regression verified)
- PM to verify in UI tomorrow morning

---

## Daily Summary

**Total Session Time**: ~8 hours (08:18 - 10:50, 19:00 - 22:31)

**Issues Closed**: #583, #586, #589
**Issues Filed**: #587, #588, #590, #591

**Major Accomplishments**:
1. Chat persistence fixed and verified (#583)
2. Calendar timezone fix verified working (#586)
3. Calendar intent routing fixed - queries now return real events (#589)

**Tomorrow**:
- PM to verify calendar feature in UI
- Address sidebar ordering (#587) and "tomorrow" intent (#588)

---

_Session log complete: 2026-01-13_
