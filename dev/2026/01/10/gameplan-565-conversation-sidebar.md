# Gameplan: Issue #565 - CONV-PERSIST-3: Conversation History Sidebar (MVP)

**Date**: 2026-01-10
**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/565
**Parent**: #314 (CONV-UX-PERSIST)
**Priority**: P2 (Medium)
**Dependencies**: #563 ✅, #566 ✅ (both complete)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Frontend: Jinja2 templates with vanilla JavaScript
- [x] Home page: `templates/home.html` with sidebar placeholder from #566
- [x] Backend: `ConversationDB` and `ConversationRepository` exist
- [x] API routes: `web/api/routes/conversations.py` created in #563

**My understanding of the task**:
This is a **frontend + API** feature with these components:
1. Sidebar UI component (HTML/CSS/JS)
2. API endpoints for conversation CRUD (verify/extend existing)
3. Frontend state management for active conversation
4. Conversation switching logic

### Part A.2: Work Characteristics Assessment

**Worktree Assessment:**
- [ ] Multiple agents will work in parallel - NO
- [x] Task duration >30 minutes - YES
- [x] Frontend + backend changes
- [x] Moderate complexity (state management)

**Assessment: SKIP WORKTREE** - Single agent, sequential phases.

### Part B: PM Verification (Infrastructure Investigation)

**Verification commands** (to run at start of Phase 0):
```bash
# Check existing conversation routes
cat web/api/routes/conversations.py

# Check ConversationRepository methods
grep -n "def " services/database/repositories.py | grep -i conversation

# Check sidebar placeholder from #566
grep -n "sidebar" templates/home.html
```

**Expected infrastructure**:
- `web/api/routes/conversations.py` - Created in #563, has `/latest` endpoint
- `services/database/repositories.py` - Has ConversationRepository
- `templates/home.html` - Has `.sidebar` placeholder (hidden)

**Note**: Actual verification happens at Phase 0 start. If reality differs, STOP and revise.

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Dependencies complete, infrastructure exists

---

## Phase 0.5: Frontend-Backend Contract Verification

### Endpoints Needed

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/api/v1/conversations` | GET | List user's conversations | VERIFY |
| `/api/v1/conversations` | POST | Create new conversation | VERIFY |
| `/api/v1/conversations/{id}` | GET | Get conversation with turns | VERIFY |
| `/api/v1/conversations/{id}/turns` | GET | Get turns for conversation | EXISTS (#563) |
| `/api/v1/conversations/latest` | GET | Get latest conversation | EXISTS (#563) |

### API Response Contracts

**GET /api/v1/conversations** (list):
```json
{
  "conversations": [
    {
      "id": "uuid",
      "title": "Sprint planning discussion",
      "created_at": "2026-01-10T14:30:00Z",
      "updated_at": "2026-01-10T15:45:00Z",
      "turn_count": 5
    }
  ],
  "has_more": false
}
```

**POST /api/v1/conversations** (create):
```json
// Request: {} or { "title": "optional" }
// Response:
{
  "id": "uuid",
  "title": null,
  "created_at": "2026-01-10T16:00:00Z"
}
```

---

## Phase 0.6: Data Flow & Integration Verification

### User Context Propagation

| Layer | Needs user_id? | Source |
|-------|----------------|--------|
| Route handler | ✅ | `get_current_user` dependency |
| Repository | ✅ | Parameter from route |

### State Management

- **Where stored**: Frontend JavaScript (active conversation ID)
- **Key for lookup**: `conversation_id` from sidebar click
- **Persistence**: URL query param or localStorage

---

## Phase 0.7-0.8: Skipped Phases

**Phase 0.7 (Conversation Design)**: SKIP - Not a multi-turn conversational feature itself.

**Phase 0.8 (Post-Completion Integration)**: SKIP - No new database state changes beyond existing conversation model.

---

## Phase 0: Initial Bookending & API Verification

### Required Actions

```bash
# 1. Verify issue exists
gh issue view 565

# 2. Update issue status
gh issue comment 565 -b "## Status: Implementation Started
- [ ] Phase 0: API verification
- [ ] Phase 1: Sidebar container
- [ ] Phase 2: Conversation list
- [ ] Phase 3: Conversation switching
- [ ] Phase 4: New Chat button"
```

### API Verification Tasks

1. Read `web/api/routes/conversations.py` - check existing endpoints
2. Check `ConversationRepository` for required methods:
   - `list_for_user(user_id, limit, offset)`
   - `create(user_id, title=None)`
   - `get_by_id(conversation_id)`
3. Add missing endpoints/methods as needed

---

## Phase 1: Sidebar Container (Enable #566 Placeholder)

### Approach

The sidebar HTML structure already exists from #566. We need to:
1. Enable it (remove `display: none`)
2. Add toggle button
3. Add internal structure

### Implementation Steps

**Step 1**: Update sidebar visibility in CSS
```css
.sidebar {
  display: block; /* Was: none */
}
```

**Step 2**: Add toggle button and internal structure:
```html
<aside class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <button class="new-chat-btn" onclick="createNewConversation()">
      + New Chat
    </button>
    <button class="sidebar-toggle" onclick="toggleSidebar()" aria-label="Toggle sidebar">
      ◀
    </button>
  </div>
  <div class="conversation-list" id="conversation-list">
    <!-- Populated by JavaScript -->
  </div>
</aside>
```

**Step 3**: Add collapse/expand JavaScript and CSS

### Acceptance Criteria - Phase 1

- [ ] Sidebar visible on left side
- [ ] Toggle button collapses/expands
- [ ] Main content resizes appropriately
- [ ] "New Chat" button visible

---

## Phase 2: Conversation List

### Implementation Steps

**Step 1**: Create fetch function
```javascript
async function loadConversations() {
  const response = await fetch('/api/v1/conversations', {
    credentials: 'include'
  });
  const data = await response.json();
  renderConversationList(data.conversations);
}
```

**Step 2**: Create render function
```javascript
function renderConversationList(conversations) {
  const list = document.getElementById('conversation-list');
  list.innerHTML = conversations.map(conv => `
    <div class="conversation-item ${conv.id === activeConversationId ? 'active' : ''}"
         onclick="switchConversation('${conv.id}')"
         data-id="${conv.id}">
      <div class="conversation-title">${conv.title || 'New conversation'}</div>
      <div class="conversation-date">${formatRelativeDate(conv.updated_at)}</div>
    </div>
  `).join('');
}
```

**Step 3**: Add date grouping (Today, Yesterday, Earlier)

### Acceptance Criteria - Phase 2

- [ ] Conversations load from API
- [ ] List displays with titles and dates
- [ ] Newest first ordering
- [ ] Active conversation highlighted
- [ ] Date groups (Today/Yesterday/Earlier)

---

## Phase 3: Conversation Switching

### Implementation Steps

**Step 1**: Track active conversation
```javascript
let activeConversationId = null;

function setActiveConversation(id) {
  activeConversationId = id;
  // Update URL for bookmarkability
  history.replaceState(null, '', `/?conversation=${id}`);
  // Update highlight
  document.querySelectorAll('.conversation-item').forEach(el => {
    el.classList.toggle('active', el.dataset.id === id);
  });
}
```

**Step 2**: Load conversation turns
```javascript
async function switchConversation(conversationId) {
  setActiveConversation(conversationId);

  const response = await fetch(`/api/v1/conversations/${conversationId}/turns`, {
    credentials: 'include'
  });
  const data = await response.json();

  // Clear and repopulate chat
  clearChat();
  data.turns.forEach(turn => {
    appendMessage(turn.user_message, true, false, new Date(turn.created_at).getTime());
    appendMessage(turn.assistant_response, false, false, new Date(turn.created_at).getTime());
  });
}
```

**Step 3**: Handle initial load (check URL for conversation param)

### Acceptance Criteria - Phase 3

- [ ] Click conversation item loads that conversation
- [ ] Messages display correctly
- [ ] Timestamps preserved
- [ ] Active indicator updates
- [ ] URL updates for bookmarking

---

## Phase 4: New Chat Button

### Implementation Steps

**Step 1**: Create new conversation
```javascript
async function createNewConversation() {
  const response = await fetch('/api/v1/conversations', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({})
  });
  const newConv = await response.json();

  // Clear chat
  clearChat();

  // Set as active
  setActiveConversation(newConv.id);

  // Refresh list
  await loadConversations();

  // Focus input
  document.querySelector('.chat-input').focus();
}
```

**Step 2**: Clear chat helper
```javascript
function clearChat() {
  const chatWindow = document.getElementById('chat-window');
  chatWindow.innerHTML = '';
  lastMessageTimestamp = null;
}
```

### Acceptance Criteria - Phase 4

- [ ] "New Chat" button creates new conversation
- [ ] Chat area clears
- [ ] New conversation appears in list
- [ ] New conversation is active/highlighted

---

## Agent Deployment

**Single Agent Assignment**: Frontend + backend with sequential dependencies.

| Phase | Agent | Evidence Required |
|-------|-------|-------------------|
| 0 | Claude Code | API verification, endpoint docs |
| 1-4 | Claude Code | Screenshots, working functionality |
| Z | Claude Code | Manual verification, PM approval |

---

## Verification Gates

### Test Scope Requirements

- [ ] **Unit tests**: API endpoints (list, create, get)
- [ ] **Integration tests**: NOT REQUIRED for MVP
- [ ] **Manual testing**: REQUIRED - full flow verification

### Verification Checkpoints

| Gate | Criteria | Method |
|------|----------|--------|
| Phase 0 | APIs exist/created | curl tests |
| Phase 1 | Sidebar visible, toggle works | Visual check |
| Phase 2 | Conversations list | Visual check |
| Phase 3 | Switch works | Click test |
| Phase 4 | New Chat works | Click test |

---

## Phase Z: Final Verification

### Manual Testing Checklist

- [ ] Sidebar visible on page load
- [ ] Toggle collapses/expands sidebar
- [ ] Main content resizes appropriately
- [ ] Conversations list populates
- [ ] Date grouping works (Today/Yesterday/Earlier)
- [ ] Click conversation loads messages
- [ ] Active conversation highlighted
- [ ] "New Chat" clears and creates new
- [ ] New conversation appears in list
- [ ] Timestamps work with #564 formatting
- [ ] No console errors

### Evidence Required

```bash
# API tests
curl -s http://localhost:8001/api/v1/conversations (with auth)

# Screenshots
# - Sidebar expanded
# - Sidebar collapsed
# - Conversation list with grouping
# - Active conversation highlighted
```

### Files Modified/Created

| File | Action |
|------|--------|
| `web/api/routes/conversations.py` | MODIFY (add endpoints) |
| `templates/home.html` | MODIFY (sidebar content) |
| `web/static/js/sidebar.js` | CREATE |
| `web/static/css/sidebar.css` | CREATE (or add to existing) |

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| API endpoints verified/created | ❌ | |
| Sidebar container visible | ❌ | |
| Toggle collapse/expand | ❌ | |
| Conversation list loads | ❌ | |
| Date grouping | ❌ | |
| Conversation switching | ❌ | |
| New Chat button | ❌ | |
| Manual testing | ❌ | |

---

## STOP Conditions

- API endpoints can't be created (missing repository methods)
- Sidebar layout breaks main content
- Performance unacceptable (>1s list load)
- State management conflicts with existing chat.js
- URL parameter handling conflicts with other features

---

## Success Criteria (Issue Completion Requires)

- [ ] All acceptance criteria met (Phases 1-4)
- [ ] Evidence provided (screenshots + curl output)
- [ ] Manual testing complete
- [ ] No regressions to existing chat functionality
- [ ] GitHub issue #565 fully updated with evidence
- [ ] PM approval received

---

## PM Approval Request Template

```markdown
@PM - Issue #565 complete and ready for review:
- Sidebar visible and toggleable ✓
- Conversation list with date grouping ✓
- Switch conversations works ✓
- New Chat creates fresh conversation ✓
- Screenshots in issue ✓

Please review and close if satisfied.
```

---

## Notes

- Leverage existing `appendMessage()` from chat.js for loading turns
- Use `TimestampUtils` from #564 for date formatting consistency
- Sidebar state (collapsed/expanded) could persist to localStorage
- Consider keyboard shortcut Ctrl+N for new chat (stretch goal)
- Auto-generate title from first user message (stretch goal)
