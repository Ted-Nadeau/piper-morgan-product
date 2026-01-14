# Gameplan: Issue #581 - Chat Input / Sidebar Integration

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/581
**Type**: Feature Completion (Integration Gap)
**Template Version**: v9.3
**Created**: 2026-01-12 16:01
**Last Updated**: 2026-01-12 16:25
**Status**: Awaiting PM Approval

---

## Problem Statement

When sending a message while viewing a conversation selected via the sidebar, the message goes to a different conversation (the one stored in `chat.js`'s localStorage) instead of the selected one.

**Evidence**: PM sent message while viewing conversation `5d0f273d...` (Today), but network payload showed `session_id: 6d3b5ffa...` (Sunday's conversation).

**Root Cause**: `chat.js` maintains its own `sessionId` from localStorage, completely independent of the sidebar's `activeConversationId`. When user selects a conversation in sidebar, chat.js is never notified.

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (backend) + Jinja2 + vanilla JS (frontend)
- [x] Sidebar code: `templates/home.html` - manages `activeConversationId`
- [x] Chat code: `web/static/js/chat.js` - manages `sessionId` in localStorage
- [x] Chat exports: `window.ChatWidget` object with various methods
- [x] Message submission: `chat.js:429` sends `session_id: sessionId`
- [x] No existing sync mechanism between sidebar and chat.js

**My understanding of the task**:
- Need to sync `activeConversationId` (sidebar) with `sessionId` (chat.js)
- When user clicks conversation in sidebar, chat.js should use that conversation
- Must not break: new conversation creation, localStorage persistence, existing chat functionality
- This is COMPLETING an incomplete feature, not just fixing a bug

**Related incomplete patterns to investigate**:
- URL param handling (`?conversation=X`)
- "New Chat" button flow
- Page refresh persistence
- Browser back/forward navigation

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [x] Small fix (< 60 min expected)
- [x] Tightly coupled files (2 files, atomic change)

**Assessment**: [x] **SKIP WORKTREE** - Single agent, focused integration fix

**Multi-Agent Assessment**:
- [ ] Multi-agent - Separate frontend/backend work → N/A (same files)
- [x] Single-agent - Tightly coupled JS state management

**Justification**: Both changes (chat.js + home.html) are JavaScript state management in the same execution context. Separating would create coordination overhead without benefit.

### Part B: PM Verification Required

**PM, please confirm**:

1. **Intended behavior when clicking sidebar conversation**:
   - [x] Future messages should go to the selected conversation
   - [ ] Only viewing, not changing where messages go

2. **Edge cases to consider**:
   - What happens when user clicks "New Chat"? (Should create new conversation)
   - What happens on page load with URL param `?conversation=X`?
   - Should localStorage be updated when switching? (Persistence across refresh)
   - What about browser back/forward navigation?

3. **Scope of "completing the feature"**:
   - [ ] Minimum: Just sync sessionId on sidebar click
   - [ ] Standard: + URL param handling + refresh persistence
   - [ ] Complete: + back/forward navigation + error recovery

4. **Critical context I'm missing?**
   - ____________

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** - Understanding is correct
- [ ] **REVISE** - Need different approach
- [ ] **CLARIFY** - Need more context

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 581
   ```

2. **Related Issues Investigation**
   ```bash
   # Find related conversation/sidebar issues
   gh issue list --search "sidebar OR conversation OR session" --state all

   # Check if similar issues were filed before
   gh issue list --search "chat session" --state closed
   ```

3. **Codebase Investigation**
   ```bash
   # Find ALL places that set/use sessionId
   grep -rn "sessionId\|session_id" web/static/js/ templates/ --include="*.js" --include="*.html"

   # Find ALL places that use activeConversationId
   grep -rn "activeConversationId" templates/

   # Check what else uses localStorage
   grep -rn "localStorage" web/static/js/ templates/

   # Check URL param handling
   grep -rn "URLSearchParams\|conversation=" templates/
   ```

4. **Update GitHub Issue**
   ```bash
   gh issue edit 581 --body "
   ## Status: Investigation Started
   - [ ] Phase 0: Codebase investigation
   - [ ] Phase 0.5: State flow documented
   - [ ] Phase 0.6: Data flow verified
   - [ ] Phase 1: Implementation
   - [ ] Phase 2: Testing
   - [ ] Phase Z: Completion
   "
   ```

### STOP Conditions
- If multiple systems independently manage conversation state → architectural review
- If backend doesn't validate conversation ownership → security issue first
- If localStorage has conflicting keys → cleanup before fix

---

## Phase 0.5: Frontend-Backend Contract Verification

### Purpose
Verify all paths where session_id flows between frontend and backend

### Required Actions

#### 1. Document All session_id Touchpoints

| Component | Uses session_id? | Source | Sets session_id? |
|-----------|------------------|--------|------------------|
| chat.js handleSubmit | Yes | localStorage | No |
| chat.js init | Yes | localStorage | Yes (on first load) |
| home.html sidebar click | No | - | Should it? |
| home.html New Chat | ? | ? | ? |
| home.html URL param | ? | ? | ? |
| Backend /intent | Yes | request body | No |
| Backend /conversations | Yes | URL path | No |

#### 2. Verify Backend Endpoints Accept session_id

```bash
# Check /intent endpoint
grep -n "session_id" web/api/routes/intent.py

# Check conversation creation
grep -n "session_id\|conversation" web/api/routes/conversations.py
```

#### 3. Static File Verification

```bash
# Verify chat.js location
ls -la web/static/js/chat.js

# Verify it's loaded in home.html
grep -n "chat.js" templates/home.html
```

### STOP Conditions
- Backend expects session_id from different source than we're setting
- Multiple conflicting session_id sources

---

## Phase 0.6: Data Flow & Integration Verification

### Purpose
This is a STATE SYNCHRONIZATION feature with multiple state holders. Must verify data flow.

### Part A: State Flow Requirements

| State Holder | Current Value Source | Needs Sync From? | Needs Sync To? |
|-------------|---------------------|------------------|----------------|
| `activeConversationId` (home.html) | Sidebar click / URL param | - | chat.js |
| `sessionId` (chat.js) | localStorage | sidebar | localStorage |
| `localStorage.sessionId` | chat.js init | sidebar (indirect) | - |
| `?conversation=X` URL | Manual / bookmark | - | sidebar + chat.js |

### Part B: State Synchronization Points

Verify each transition is handled:

| Event | Current Behavior | Expected Behavior | Implemented? |
|-------|------------------|-------------------|--------------|
| Sidebar click | Sets `activeConversationId`, loads turns | + Sets chat.js `sessionId` | ❌ No |
| New Chat button | Creates conversation, adds to sidebar | + Sets chat.js `sessionId` to new ID | ? |
| Page load (no URL) | chat.js loads from localStorage | Should match sidebar selection | ? |
| Page load (URL param) | ? | Set sidebar + chat.js to URL value | ? |
| Send message | Uses chat.js `sessionId` | Should match sidebar | ❌ No |
| Page refresh | Reloads from localStorage | Should persist selection | ? |

### Part C: Integration Points Checklist

| Caller | Callee | Method Exists? | Parameters Correct? |
|--------|--------|----------------|---------------------|
| home.html setActiveConversation | ChatWidget.setSessionId | ❌ No (to add) | N/A |
| home.html createNewConversation | ChatWidget.setSessionId | ❌ No (to add) | N/A |
| home.html (URL param handler) | ChatWidget.setSessionId | ❌ No (to add) | N/A |

### STOP Conditions
- If URL param handling doesn't exist → add to scope
- If New Chat doesn't sync → add to scope
- If page refresh loses state → add to scope

---

## Phase 0.8: Post-Completion Integration

### Purpose
Ensure the fix integrates properly with rest of system

### Completion Side-Effects Checklist

When user switches conversation:

| Side Effect | Location | Value | Verified? |
|-------------|----------|-------|-----------|
| sessionId updated | chat.js variable | selected conversation ID | [ ] |
| localStorage updated | browser storage | selected conversation ID | [ ] |
| URL updated | address bar | `?conversation=X` | [ ] |
| Sidebar highlight updated | DOM | .active class on selected | [ ] (already works) |

### Downstream Behavior Changes

| Feature | Before Fix | After Fix |
|---------|-----------|-----------|
| Send message | Goes to localStorage session | Goes to selected conversation |
| Page refresh | Loads localStorage session | Loads URL param or last selection |
| New Chat | Creates but doesn't switch | Creates AND switches to new |

---

## Phase 1: Implementation

### 1.1 Add `setSessionId` to chat.js

**File**: `web/static/js/chat.js`

**Location**: In the `window.ChatWidget` export object (around line 475)

```javascript
window.ChatWidget = {
  appendMessage,
  setExample,
  pollWorkflowStatus,
  handleDirectResponse,
  handleErrorResponse,
  clearHistory: clearChatHistory,
  getSessionId: () => sessionId,
  setSessionId: (id) => {           // NEW
    sessionId = id;
    // Persist to localStorage for refresh
    if (storageAvailable && id) {
      localStorage.setItem(STORAGE_KEYS.SESSION_ID, id);
    }
    console.log('[ChatWidget] sessionId set to:', id);
  },
  init: initChat
};
```

### 1.2 Call `setSessionId` from sidebar click

**File**: `templates/home.html`

**Location**: In `setActiveConversation()` function

```javascript
function setActiveConversation(id) {
  activeConversationId = id;

  // Sync with chat.js so messages go to this conversation
  if (window.ChatWidget && window.ChatWidget.setSessionId) {
    ChatWidget.setSessionId(id);
  }

  // Update URL for bookmarking/refresh
  if (id) {
    history.replaceState(null, '', `/?conversation=${id}`);
  } else {
    history.replaceState(null, '', '/');
  }

  // Update visual highlight
  document.querySelectorAll('.conversation-item').forEach(el => {
    el.classList.toggle('active', el.dataset.id === id);
  });
}
```

### 1.3 Handle URL param on page load

**File**: `templates/home.html`

**Investigation needed**: Check if URL param handling exists

```bash
grep -n "URLSearchParams\|getURLParameter\|conversation=" templates/home.html
```

If missing, add:
```javascript
// On page load, check for URL param
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const conversationId = urlParams.get('conversation');

  if (conversationId) {
    // Set sidebar selection
    setActiveConversation(conversationId);
    // Load the conversation
    switchConversation(conversationId);
  }
});
```

### 1.4 Handle "New Chat" button

**File**: `templates/home.html`

**Location**: In `createNewConversation()` function

**Investigation needed**: Verify current behavior
```bash
grep -n "createNewConversation" templates/home.html
```

After creating conversation, ensure `setActiveConversation(newId)` is called (which will now sync to chat.js).

---

## Phase 2: Testing

### 2.1 Manual Test Scenarios

| # | Scenario | Steps | Expected | Status |
|---|----------|-------|----------|--------|
| 1 | Send to selected conversation | Select conv A, send message | Message goes to conv A | [ ] |
| 2 | Switch and send | Select A, switch to B, send | Message goes to conv B | [ ] |
| 3 | New chat button | Click New Chat, send message | New conversation created with message | [ ] |
| 4 | Page refresh persistence | Select A, refresh, send | Message goes to conv A | [ ] |
| 5 | Rapid switching | Click A, B, A quickly, send | Message goes to final selection (A) | [ ] |
| 6 | URL param load | Load `/?conversation=X`, send | Message goes to X | [ ] |
| 7 | Browser back button | Select A, select B, click Back | Returns to A, chat.js synced | [ ] |
| 8 | New tab with URL | Open new tab with `/?conversation=X` | Both sidebar and chat.js set to X | [ ] |

### 2.2 Regression Checks

| Check | How | Status |
|-------|-----|--------|
| Existing conversations still load | Click each conversation | [ ] |
| New conversations can be created | Click New Chat | [ ] |
| Messages still display correctly | Send and receive message | [ ] |
| LocalStorage not corrupted | Check DevTools Application tab | [ ] |
| Chat input still functions | Type and submit message | [ ] |

### 2.3 Wiring Integration Tests

**Required per template v9.3**:

```javascript
// Test 1: Verify ChatWidget.setSessionId exists and works
console.assert(typeof ChatWidget.setSessionId === 'function', 'setSessionId should be a function');

// Test 2: Verify setSessionId updates internal state
ChatWidget.setSessionId('test-123');
console.assert(ChatWidget.getSessionId() === 'test-123', 'getSessionId should return set value');

// Test 3: Verify setSessionId updates localStorage
console.assert(localStorage.getItem('piper_session_id') === 'test-123', 'localStorage should be updated');

// Test 4: Verify setActiveConversation calls setSessionId
// (Manual: set breakpoint in setSessionId, click sidebar item)
```

### 2.4 Network Verification

After each test, verify in Network tab:
- `intent` request payload contains correct `session_id`
- `session_id` matches `activeConversationId`

---

## Phase 3: Evidence Collection

### 3.1 Before/After Comparison

**Before Fix**:
- Selected: `5d0f273d...` (Today)
- Sent to: `6d3b5ffa...` (Sunday) ❌

**After Fix**:
- Selected: `[conversation_id]`
- Sent to: `[same conversation_id]` ✅

### 3.2 Evidence Required

- [ ] Console log showing `[ChatWidget] sessionId set to: X` on sidebar click
- [ ] Network payload showing correct `session_id` matches selected conversation
- [ ] URL updated to `?conversation=X` after selection
- [ ] Conversation loads correctly after page refresh with URL param

---

## Phase Z: Final Bookending

### Commit Message

```
fix(#581): Sync chat input with sidebar conversation selection

Root cause: chat.js used its own sessionId from localStorage, ignoring
the activeConversationId from the sidebar when sending messages.

Fix:
- Added ChatWidget.setSessionId() method to chat.js
- Called from setActiveConversation() when user clicks sidebar item
- URL param now persists selection for refresh/bookmarking
- New Chat button properly syncs to new conversation

Testing: 8 manual test scenarios verified
Closes #581

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Issue Update

- Update Evidence section with fix verification
- Check all Investigation Status boxes
- Add before/after network payload comparison
- Close issue

---

## Verification Gates

- [ ] Phase 0: GitHub investigation complete
- [ ] Phase 0.5: Frontend-backend contract verified
- [ ] Phase 0.6: All state sync points identified
- [ ] Phase 1: Implementation complete
- [ ] Phase 2: All 8 test scenarios pass
- [ ] Phase 2: All 4 regression checks pass
- [ ] Phase 2: Wiring tests pass
- [ ] Phase Z: Evidence compiled
- [ ] Phase Z: PM approval

---

## Completion Matrix

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Phase -1 infrastructure verified | [ ] | PM approval |
| Phase 0 investigation complete | [ ] | grep results |
| All state sync points handled | [ ] | Phase 0.6 table |
| setSessionId added to chat.js | [ ] | Code change |
| setActiveConversation syncs | [ ] | Code change |
| URL param handling works | [ ] | Test #6, #8 |
| New Chat syncs correctly | [ ] | Test #3 |
| Page refresh persists | [ ] | Test #4 |
| Manual tests pass (8 scenarios) | [ ] | Test results |
| Regression checks pass | [ ] | Test results |
| Wiring tests pass | [ ] | Console output |
| Network payload verified | [ ] | Screenshot |
| Issue updated with evidence | [ ] | GitHub link |
| PM approval received | [ ] | Issue closed |

---

## STOP Conditions

- Multiple systems independently manage session state → Need architecture review
- Backend doesn't validate conversation ownership on message submit → Security issue first
- URL param handling requires backend changes → Scope expansion
- New Chat button doesn't call setActiveConversation → Additional fix needed
- Browser history API conflicts with existing code → Need PM decision

---

## Risk Analysis: Deeper Problems Check

### What Could This Fix Mask?

| Potential Deeper Issue | How to Check | Status |
|------------------------|--------------|--------|
| Multiple session IDs in system | `grep -rn "session_id\|sessionId"` | [ ] |
| Backend creating duplicate conversations | Check conversation creation logic | [ ] |
| localStorage/cookie conflicts | Check what else uses localStorage | [ ] |
| Race conditions on rapid switching | Manual test with fast clicks | [ ] |
| No validation of conversation ownership | Check backend message handler | [ ] |

### Investigation Commands

```bash
# Find all session_id references
grep -rn "session_id\|sessionId" web/static/js/ templates/ --include="*.js" --include="*.html"

# Find all localStorage usage
grep -rn "localStorage" web/static/js/ templates/

# Find conversation creation endpoints
grep -rn "create.*conversation\|POST.*conversation" web/api/routes/

# Check if backend validates ownership on message send
grep -n "session_id\|conversation" services/intent/intent_service.py
```

---

## Effort Estimate

| Phase | Estimate |
|-------|----------|
| Phase -1: Verification | 5 min |
| Phase 0: Investigation | 15 min |
| Phase 0.5: Contract verification | 10 min |
| Phase 0.6: Data flow verification | 10 min |
| Phase 1: Implementation | 15 min |
| Phase 2: Testing | 20 min |
| Phase 3: Evidence | 10 min |
| Phase Z: Bookending | 5 min |
| **Total** | ~90 min |

---

_Gameplan created: 2026-01-12 16:01_
_Gameplan updated: 2026-01-12 16:25 (Template v9.3 compliance)_
