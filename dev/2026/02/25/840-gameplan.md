# Gameplan: #840 — Conversation Not Appearing in History Sidebar

**Date**: 2026-02-25
**Issue**: #840
**Systemic Parent**: #854 (Cross-Turn State Continuity)

---

## Phase -1: Infrastructure Verification

**Infrastructure confirmed via investigation**:
- Web framework: FastAPI with Jinja2 templates
- Database: PostgreSQL (port 5433) with SQLAlchemy async
- Auth: JWT with 30-min access tokens, cookie-based for web UI
- Frontend: Vanilla JS in templates/home.html, web/static/js/chat.js
- Conversation model: `ConversationDB` in `services/database/models.py:697`
- Repository: `ConversationRepository` in `services/database/repositories.py`

**Current state confirmed**:
- Three conversation creation paths exist (explicit, auto-create, lazy ensure)
- History sidebar fetch missing credentials (always broken)
- `ensure_conversation_exists` falls back to `user_id="unknown"` (invisible conversations)
- 30-min token expiry with no refresh (silent auth loss)

**Worktree assessment**: SKIP — single agent, sequential fixes across 3-4 files, tightly coupled

**Proceed/Revise**: PROCEED

---

## Phase 0: GitHub Investigation

Issue #840 verified, rewritten with root cause analysis (Feb 25). Four root causes identified (A-D), plus structural underspec analysis.

No related PRs or existing partial fixes beyond the comment at repositories.py:1010-1011.

---

## Phase 0.5: Frontend-Backend Contract

This bug spans frontend AND backend. Current contract:

| Frontend Action | API Call | Auth Required? | Current Status |
|----------------|----------|---------------|----------------|
| Left sidebar load | GET `/api/v1/conversations` | Yes (cookie) | ✅ Sends credentials |
| History sidebar load | GET `/api/v1/conversations?...` | Yes (cookie) | ❌ Missing credentials |
| Send message | POST `/api/v1/intent` | Optional (cookie) | ⚠️ Works without auth |
| Create new chat | POST `/api/v1/conversations` | Yes (cookie) | ✅ Sends credentials |

**Contract gap**: The intent endpoint accepts unauthenticated requests and silently creates conversations with no owner. The frontend has no way to know this happened.

---

## Phase 0.6: Data Flow Verification

### Conversation Creation Flow (Current)

```
User types message → chat.js sends POST /api/v1/intent
  ├─ Auth cookie present + valid?
  │   ├─ YES → user_id extracted → auto-create conversation (intent.py:276-302)
  │   │         → conversation_created=true in response
  │   │         → frontend refreshes sidebar
  │   └─ NO → user_id=None → auto-create SKIPPED
  │            → turn saved → ensure_conversation_exists(user_id=None)
  │            → conversation created with user_id="unknown"
  │            → INVISIBLE to list_for_user()
  └─ Response sent to user (either way — user can't tell)
```

### Sidebar Fetch Flow (Current)

```
Page load → initSidebar() → loadConversations()
  ├─ fetch('/api/v1/conversations', {credentials: 'include'})
  ├─ API returns conversations WHERE user_id = current_user.sub
  └─ Renders in left sidebar

Page load → initHistorySidebar() → fetchHistoryConversations()
  ├─ fetch('/api/v1/conversations?...') ← NO CREDENTIALS
  ├─ API returns 401
  └─ Catch block → empty state shown
```

---

## Phase 0.7: Conversation Design

N/A — this is a persistence/display bug, not a conversational flow.

---

## Phase 0.9: Underspec Analysis

**Finding**: This feature was built across 11+ issues without a unifying specification. The conversation persistence pipeline has no documented invariants, no end-to-end contract, and no integration test that exercises the full path (message → persist → navigate → sidebar shows it).

**Recommendation**: After fixing the immediate bugs, file a follow-up issue to create a lightweight spec for conversation lifecycle. This would define:
- When conversations are created (and by which path)
- What user_id guarantee each path provides
- What happens when auth expires during a session
- What the sidebar refresh contract is

This is NOT blocking for the immediate fix but prevents recurrence.

---

## Phase 1: Fix A — History Sidebar Credentials (Frontend)

**Scope**: One-line fix, zero risk

**File**: `templates/home.html`
**Line**: 1898

**Change**: Add `credentials: 'include'` to `fetchHistoryConversations()` fetch call.

**Verification**: History sidebar loads conversations for authenticated users.

**Test**: No automated test possible for this (it's a fetch option in browser JS). Manual verification during CXO re-test.

---

## Phase 2: Fix B — Refuse Unknown user_id (Backend)

**Scope**: Small change, moderate risk (need to handle the "what do we do instead" question)

**File**: `services/database/repositories.py`
**Method**: `ensure_conversation_exists()` (lines 989-1028)

**Change**: Instead of falling back to `user_id="unknown"`, either:
- **Option 1**: Skip conversation creation entirely (log warning, don't create). Turns won't be saved (FK constraint), but this is better than invisible conversations.
- **Option 2**: Propagate the error upward so the caller can handle it.

**Recommended**: Option 1 — skip creation, log prominently. The user is effectively unauthenticated; creating an ownerless conversation helps nobody.

**Also**: Clean up the misleading comment at line 1010-1011 that acknowledges the bug but doesn't fix it.

**Test**: Unit test in `test_conversation_repository.py` — verify `ensure_conversation_exists(conv_id, user_id=None)` does NOT create a conversation.

---

## Phase 3: Fix C — Auth Expiry Handling (Frontend + Backend)

**Scope**: Moderate change, addresses the structural gap

**Options**:

| Approach | Complexity | User Experience | Risk |
|----------|-----------|----------------|------|
| **C1: 401 detection + redirect** | Low | User sees login page, re-authenticates | May lose unsent message |
| **C2: Token refresh** | High | Seamless, user never notices | Complex, needs refresh endpoint |
| **C3: Pre-flight auth check** | Medium | Warning toast before message fails | Extra API call per message |

**Recommended**: C1 (401 detection + redirect) for M0. This is the minimum viable fix:
- In `chat.js`, after the intent fetch: if response is 200 but `result.session_id` exists and `conversation_created` is false AND the conversation should have been created → show a warning.
- Actually simpler: In `get_current_user_optional`, when token is expired, instead of silently returning None, set a response header like `X-Auth-Expired: true`. Frontend checks this header and shows a re-login prompt.

**Alternative minimal approach**: Make the intent endpoint REQUIRE authentication (switch from `get_current_user_optional` to `get_current_user`). If the token is expired, the user gets a 401 and knows to re-login. This is the most honest fix but changes the API contract.

**PM Decision needed**: Which approach for auth expiry? C1 (redirect on 401) is recommended for M0 scope.

---

## Phase 4: Fix D — Error Visibility (Backend, optional for M0)

**Scope**: Small improvements across multiple files

**Changes**:
- `intent.py:303-305`: Log at ERROR level (not warning) when auto-create fails
- `intent_service.py:296-302`: Include conversation_id in warning for debugging
- Consider: return a `persistence_warning` field in the intent response when conversation save fails

**This phase is OPTIONAL for M0** — Fixes A+B+C resolve the user-visible bug. Fix D is defensive improvement.

---

## Phase 5: Cross-Validation

After all fixes:
- `grep -n "credentials.*include" templates/home.html` — verify ALL fetch calls include credentials
- `grep -n "unknown" services/database/repositories.py` — verify no "unknown" user_id fallback
- `grep -n "get_current_user_optional" web/api/routes/` — verify auth handling is appropriate per endpoint

---

## Phase 6: Test Suite

- Run existing conversation tests: `pytest tests/unit/web/api/routes/test_conversations.py -v`
- Run integration tests if DB available: `pytest tests/integration/services/test_conversation_repository.py -v`
- New test for Phase 2: `ensure_conversation_exists` with None user_id
- Manual test plan for CXO: login → chat → navigate away → verify sidebar

---

## Phase Z: Closure

- Update #840 description with checked acceptance criteria
- Add closing comment with evidence
- Close #840
- Update #854 (systemic parent) with progress
- File follow-up issue for conversation lifecycle spec (underspec finding)
- Update session log

---

## STOP Conditions

1. Auth changes break login flow — STOP, revert
2. Conversation creation changes cause FK constraint errors — STOP, investigate
3. Frontend changes break left sidebar (which currently works) — STOP, revert
4. PM disagrees with auth expiry approach — STOP, discuss
