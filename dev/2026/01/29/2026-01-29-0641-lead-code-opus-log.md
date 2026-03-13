# Session Log: 2026-01-29-0641-lead-code-opus

**Role**: Lead Developer
**Model**: Claude Code (Opus)
**Date**: Thursday, January 29, 2026
**Start Time**: 6:41 AM

## Session Objectives

Continue alpha testing bug triage from yesterday's session.

## PM Alpha Testing Feedback (6:41 AM)

**Confirmed Fixed:**
- ✅ Username display (shows "alfamux" not email prefix)
- ✅ Design/styling issues (interface "notably crisper and better looking")

**Still Broken:**
1. **Projects not saving** - #728 fix didn't work. Piper claims to save but Projects page empty
2. **Conversation not persisting** - Conversation disappears on refresh
3. **Sidebar shows "No conversations yet"** - Even during active conversation
4. **History button** - Still not wired up (need to verify #729 fix)
5. **Onboarding flow bug** - After saying "Yes" to save, Piper asks again instead of saving

**Key Observations from Screenshots:**
- Screenshot 1: Active conversation visible, but sidebar shows "No conversations yet"
- Screenshot 2: Projects page shows "No projects set up yet" after Piper claimed to save them
- Screenshot 3: After refresh, conversation gone, sidebar still empty
- Screenshot 4: New chat via "+ New Chat" button DOES appear in sidebar ("New conversation 6:47 AM")

**Critical Insight:** Starting chat via text box vs "+ New Chat" button may create different session states.

## Investigation Plan

1. Trace why #728 fix (captured_projects in context) isn't resulting in database writes
2. Investigate conversation persistence - why isn't the initial conversation being saved?
3. Verify sidebar population logic
4. Check if History button include is working

---

## Work Log

### 6:45 AM - Investigation Start

**Root Cause Found: Conversations Not Being Created**

When user types directly in the chat input (without clicking "+ New Chat"):
1. `chat.js` generates a random `sessionId` via `crypto.randomUUID()` stored in localStorage
2. Messages sent to `/api/v1/intent` with this sessionId
3. BUT no conversation is created in the database
4. On refresh, sidebar loads from `/api/v1/conversations` - finds nothing
5. All history is only in localStorage, not database

The `+ New Chat` button works because it POSTs to `/api/v1/conversations` first, creating a DB record.

**Root Cause #2: Projects May Not Be Persisting**

The onboarding persistence relies on:
1. `OnboardingProcessAdapter.handle_message()` returns `captured_projects` in context ✓ (fixed yesterday)
2. `IntentService._check_active_guided_process()` checks for `state == "complete"` and `captured_projects`
3. Calls `_persist_onboarding_projects(user_id, captured_projects)`

Possible issues:
- If `user_id` is not passed correctly, projects won't be owned by user
- Need to verify logging to confirm this code path is reached

---

### 7:00 AM - Fixes Applied

**Fix #1: Conversation Auto-Creation (Issue #731)**

Fixed `web/api/routes/intent.py` to auto-create conversations when users type directly in chat:
- Before processing intent, check if conversation exists for the session_id
- If not, create one using the session_id as its ID
- Ensures frontend localStorage session_id matches database record

The original code had incorrect parameters (`conversation_id=`, `owner_id=`) that didn't match the model. Fixed to use ConversationDB directly with correct fields.

**Fix #2: Project Persistence Debug Logging**

Added debug prints to trace the onboarding flow:
- `services/onboarding/portfolio_handler.py` - trace `_handle_confirming` execution
- `services/intent/intent_service.py` - trace persistence check

The code path SHOULD work:
1. `OnboardingProcessAdapter.handle_message()` returns `captured_projects` in context ✓
2. `IntentService._check_active_guided_process()` checks `state == "complete"` ✓
3. Calls `_persist_onboarding_projects(user_id, captured_projects)`

**Investigation Finding: Onboarding Flow Bug**

PM reported: "After saying 'Yes' to save, Piper asks again instead of saving"

Possible causes:
1. Session state not transitioning to CONFIRMING before user says "Yes"
2. CONFIRM_PATTERN not matching (unlikely - "yes" clearly matches `\b(yes|...)\b`)
3. Session lookup failing between requests

The singletons ARE set up correctly:
- `_get_onboarding_components()` returns the same manager/handler
- Session stored in `manager._sessions` dict
- State machine allows CONFIRMING → COMPLETE transition

**Next Step: Manual Testing Required**

The debug logging will show:
```
[OnboardingHandler] _handle_confirming called, message='Yes'
[OnboardingHandler] Session state=confirming, captured_projects=1
[OnboardingHandler] CONFIRM_PATTERNS match=True
[OnboardingHandler] CONFIRM MATCHED! Transitioning to COMPLETE...
[IntentService] PERSISTENCE TRIGGERED! captured_projects=[{...}], user_id=xxx
```

If these don't appear in server output, we can trace where the flow is failing.

---

### Tests Passing

- 5253 unit tests passed
- 191 onboarding tests passed
- 14 adapter tests passed

---

### History Button Verification (#729)

Verified that History button IS properly wired up:
1. Button element exists: `templates/components/navigation.html:547-553`
   - `id="nav-history-trigger"`
   - Trust-gated at stage 2: `data-min-trust-stage="2"`
2. Click handler wired: `templates/components/navigation.html:636-656`
   - Calls `window.HistorySidebar.toggle()`
3. History sidebar included: `templates/home.html:1012`
   - `{% include 'components/history_sidebar.html' %}`
4. `window.HistorySidebar` exported: `templates/components/history_sidebar.html:694-704`

If the button isn't working in testing, possible causes:
- User trust stage < 2 (button may be hidden)
- Browser console errors preventing script execution
- Need to clear browser cache

---

### Files Modified

1. `web/api/routes/intent.py` - Auto-create conversation before processing intent
2. `services/onboarding/portfolio_handler.py` - Debug logging for confirming flow
3. `services/intent/intent_service.py` - Debug logging for persistence check

---

## Summary for PM

**Fix Applied: Conversation Auto-Creation**

When users type directly in the chat input (without clicking "+ New Chat"), conversations were not being created in the database. Fixed by auto-creating the conversation record in `/api/v1/intent` before processing.

**Debug Logging Added for Onboarding**

Added debug prints to trace the exact flow when user says "Yes" to save projects. Terminal output will show:
- Which handler method is called
- Session state at time of message
- Whether CONFIRM_PATTERN matched
- Whether persistence was triggered

**History Button Verified**

The History button is properly wired up. If it's not working:
1. Check if trust stage is set (button is trust-gated at stage 2)
2. Check browser console for errors
3. Try clearing browser cache

**Action Needed: Manual Testing**

Please retest the onboarding flow and watch the terminal output for debug messages. This will help identify exactly where the flow is breaking.

---

### 8:06 AM - History Button Trust Gate Fix

PM feedback: "Why does a new user need to be trusted to see their own history?" - Valid point.

**Fix Applied:** Lowered History button trust gate from stage 2 to stage 1 in `templates/components/navigation.html`.

---

### ~8:15 AM - GitHub Issues Created

Created tracking issues for all work done this session:

1. **#731** - Fix: Conversations not persisting when typing directly in chat
2. **#732** - Fix: History button trust-gated at wrong level
3. **#733** - Debug: Projects not saving during onboarding

PM noted: "please continue to make bug issues and update them as you go to track any work we do, so it will be legible to future developers"

---

## Current Status

**PM Re-test at 8:19 AM:**

### Verified Working
- ✅ **Conversation persistence (#731)** - "old chat now appears in sidebar"

### Still Broken
- ❌ **History button (#732)** - Trust gate fix insufficient. Real issue: `HistorySidebar.mount()` never called
- ❌ **Project onboarding** - "Piper is still struggling to set up my projects, semantically"

### CRITICAL NEW BUG FOUND
- 🚨 **#734** - Calendar data leaking between users. alfamux sees previous user's calendar events despite not connecting calendar. This is a multi-tenancy failure - integration tokens stored globally without user scoping.

---

### 8:30 AM - Investigation: Calendar Data Leak

**Root Cause:** All integration tokens (calendar, GitHub, Slack, LLM keys) are stored globally in keychain without user_id prefix.

**Evidence:**
- `keychain.store_api_key("google_calendar", tokens.refresh_token)` - No username parameter
- `keychain.get_api_key("google_calendar")` - No username parameter

**The Correct Pattern Exists:**
`UserAPIKeyService.store_user_key()` properly uses `username=user_id` but routes bypass it and call keychain directly.

**Fix requires:** Threading user_id through ALL storage AND retrieval calls for:
- Google Calendar tokens
- GitHub tokens
- Slack tokens
- OpenAI/Anthropic keys

Created issue #734 with detailed fix plan.

---

### 8:35 AM - History Button Root Cause

Trust gate fix was necessary but insufficient. The real issue:

```
HistorySidebar.mount() is never called
```

The component is included in the page (`home.html:1012`) and creates `window.HistorySidebar`, but `mount()` is never called so the DOM element doesn't exist.

Updated #732 with this finding.

**PM Question:** "what is its purpose? the tab for opening and closing the chat history sidebar works just fine"

There are TWO sidebar features:
1. **Left sidebar** - conversation list - WORKS
2. **Right History sidebar** (#425) - search, date grouping - NEVER MOUNTED

May be duplicate functionality - need PM decision.

---

### 8:28 AM - PM Testing Feedback & Terminal Log Analysis

**PM Re-test confirmed:**
- ✅ #731 conversation persistence WORKING
- ❌ History button still broken (needs mount call)
- ❌ Project onboarding "still struggling semantically"
- 🚨 Calendar data leaking between users (multi-tenancy bug)

**Issues Created:**
- **#734** - Calendar tokens not user-scoped (multi-tenancy)
- **#735** - History sidebar never mounted

**Terminal Log Analysis (from PM's 8:17-8:25 AM test):**

Root cause findings from logs:

1. **First message "Can you help me set up my projects?" → NOT onboarding**
   - Classified as GUIDANCE intent
   - Returns static help message pointing to Settings → Projects
   - Onboarding only triggers on GREETING intent (when user says "hi")

2. **When user said "hi piper" → onboarding DID trigger correctly**
   - `first_meeting_detection should_trigger=True`
   - `portfolio_onboarding_triggered`
   - Projects WERE captured (4 projects)

3. **Persistence FAILED with database constraint error:**
   ```
   duplicate key value violates unique constraint "projects_name_key"
   DETAIL: Key (name)=(Decision Reviews) already exists.
   ```
   - Project "Decision Reviews" existed from PREVIOUS USER
   - **BUG: Unique constraint on `name` is GLOBAL, not per-user**
   - Should be composite: `(owner_id, name)`

4. **Session lookup returned empty:**
   ```
   [PortfolioManager] Current sessions: []
   [PortfolioManager] No active session found
   ```
   - Investigating: Session was created but not found on subsequent message
   - May be instance mismatch in singleton pattern

---

### 8:36 AM - PM Feedback: Debugging Monofocus

PM correctly noted I was in deep debugging without updating log or following plan.

**Action items:**
- Create issues for distinct bugs found
- Consider parallel investigation with Sonnet agents
- Keep session log updated

---

## Current Status

### Fixes Applied
- [x] Conversation auto-creation (#731) - ✅ VERIFIED WORKING

### Issues Identified This Session
- #734 - Calendar tokens not user-scoped (created, awaiting triage)
- #735 - History sidebar never mounted (created, awaiting triage)
- **NEW** - Projects table unique constraint wrong (global, should be per-user) - NEEDS ISSUE
- **NEW** - Onboarding only triggers on GREETING, not "help set up projects" - NEEDS INVESTIGATION

### Investigation In Progress
- [ ] Project persistence (#733) - ROOT CAUSE FOUND: global unique constraint on `name`
- [ ] Onboarding session not found on subsequent messages - may be singleton instance issue

### Files Modified This Session
1. `web/api/routes/intent.py` - Auto-create conversation before processing intent
2. `services/onboarding/portfolio_handler.py` - Debug logging for confirming flow
3. `services/intent/intent_service.py` - Debug logging for persistence check
4. `templates/components/navigation.html` - Lowered History trust gate from 2 to 1

---

### 8:37 AM - Parallel Agent Work Launched

PM heading to meetings. Three agents launched:

1. **Agent: Fix #736** - Creating migration for composite unique constraint `(owner_id, name)`
2. **Agent: Session singleton investigation** - Finding why onboarding sessions disappear between messages
3. **Agent: Terminal log analysis** (Haiku) - Reviewing warnings/errors for additional issues

---

### 8:45 AM - Agent Results Consolidated

#### Agent 1: Fix #736 - ✅ COMPLETE

**Migration created and tested:**
- File: `alembic/versions/3c85fd899ece_fix_projects_unique_constraint_736.py`
- Model: `services/database/models.py` updated with `__table_args__` composite constraint
- Constraint changed: `name` (global unique) → `(owner_id, name)` (per-user unique)
- Upgrade tested: ✅
- Downgrade tested: ✅
- 196 project-related tests: ✅ All passing
- Database now at: `3c85fd899ece (head)`

**Impact:** Different users can now have projects with the same name.

#### Agent 2: Session Singleton Investigation - Hypothesis Ready

**Finding:** Code appears correct but needs runtime verification.

- Both paths use `_get_onboarding_components()` singleton correctly
- Missing: manager `id()` in lookup debug output (only in creation)
- Dead code found: `IntentService._check_active_onboarding` (never called)
- **Hypothesis:** Two manager instances OR module reloading resetting singleton

**Recommended fix:** Add `manager id=` to `get_session_by_user` debug output, then test again to compare IDs.

#### Agent 3: Terminal Log Analysis - ✅ COMPLETE

**Key findings:**
- **Schema drift warning** - NOT a bug. Expected graceful error handling in `schema_validator.py`
- **All significant errors already tracked** in issues #731-#736
- **No new issues needed**
- Root cause chain confirmed: #736 (constraint) → #733 (projects not saving)

---

## Current Status (8:45 AM)

### ✅ FIXED THIS SESSION
- **#731** - Conversation persistence - VERIFIED WORKING
- **#736** - Projects unique constraint - MIGRATION APPLIED

### ⏳ AWAITING RE-TEST
- **#733** - Projects not saving - Root cause (#736) now fixed, needs re-test

### 📋 AWAITING TRIAGE
- **#734** - Calendar tokens multi-tenancy
- **#735** - History sidebar never mounted

### 🔍 NEEDS MORE DEBUG
- Session singleton issue - Add manager ID to lookup debug, re-test
