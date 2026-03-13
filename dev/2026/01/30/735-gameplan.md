# Gameplan: Issue #735 - Mount and Wire History Sidebar

**Issue**: #735 FINISH-HISTORY-SIDEBAR
**Date**: 2026-01-30
**Author**: Lead Developer (Claude Code)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Templates: Jinja2 (confirmed)
- [x] Component exists: `templates/components/history_sidebar.html` (confirmed)
- [x] API exists: `GET /api/conversations` (confirmed via grep)
- [x] Tests exist: 56 tests in `tests/unit/templates/test_history_sidebar.py` (confirmed)

**My understanding of the task**:
- Component is 95% complete - only mount() call missing
- Need to add mount call + wire callbacks
- Small scope, ~2 hours work

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes ← Borderline (~2 hours, but simple)
- [ ] Multi-component work
- [ ] Exploratory/risky changes

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work

**Assessment**: **SKIP WORKTREE** - Single agent, simple wiring work, tightly scoped

### Part B: PM Verification

**PM confirmed (6:02 PM)**:
1. Option A selected - mount the right sidebar
2. Right sidebar is for "other objects over time" (conversations for now)
3. Empty state already exists in component
4. Research MUX docs to ensure consistent design ✅ Done

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding is correct, gameplan appropriate

---

## Phase 0: Initial Bookending

### 0.1 GitHub Issue Status

- [x] Issue #735 exists and assigned
- [x] Issue description rewritten using feature template
- [x] Labels updated (`UX` not `bug`)

### 0.2 Codebase Verification

```bash
# Confirm component exists
ls templates/components/history_sidebar.html
# ✅ Exists

# Confirm window.HistorySidebar is exported
grep "window.HistorySidebar" templates/components/history_sidebar.html
# ✅ Line 694

# Confirm API endpoint exists
grep "list_conversations" web/api/routes/conversations.py
# ✅ Line 247
```

### 0.3 Current State

| Check | Status |
|-------|--------|
| Component included in home.html | ✅ Line 1012 |
| mount() called | ❌ **Missing** |
| Navigation button wired | ✅ Calls toggle() |
| API endpoint functional | ✅ /api/conversations |

### STOP Conditions Check

- [ ] Issue doesn't exist → NO
- [ ] Feature already implemented → NO (mount() not called)
- [ ] Different problem → NO

**Proceed to Phase 1.**

---

## Phase 0.5: Frontend-Backend Contract Verification

### When to Apply

- ✅ Creating new API endpoints + UI → **NO** (using existing)
- ❌ Backend-only changes → NO
- ❌ Frontend-only styling → NO
- ✅ Adding JavaScript that makes fetch() calls → **YES**

### Endpoint Verification

| Endpoint | Route Path | Mount Prefix | Full Path | Verified |
|----------|------------|--------------|-----------|----------|
| list_conversations | /conversations | /api | /api/conversations | ✅ |

### API Response Format

Need to confirm `/api/conversations` response matches component expectations:

Component expects:
```javascript
{
  conversations: [{
    id, topic_summary, summary, timestamp, is_private, channel
  }],
  pagination: { page, totalPages }
}
```

API returns (from routes/conversations.py):
```python
class ConversationListResponse:
    conversations: List[ConversationSummary]
    has_more: bool
```

**⚠️ Potential gap**: Component expects `pagination: {page, totalPages}` but API returns `has_more: bool`.

**Resolution**: Transform response in JavaScript, OR use simpler "Load More" without page numbers.

---

## Phase 0.6: Data Flow Verification

### N/A Declaration

This phase is for multi-layer service features. #735 is frontend wiring only.

- [ ] Skip Phase 0.6 - Not applicable (PM may validate)

---

## Phase 0.7: Conversation Design

### N/A Declaration

This phase is for conversational features. #735 is UI component, not conversation.

- [ ] Skip Phase 0.7 - Not applicable (PM may validate)

---

## Phase 0.8: Post-Completion Integration

### N/A Declaration

This phase is for features that change user state. #735 just displays existing data.

- [ ] Skip Phase 0.8 - Not applicable (PM may validate)

---

## Phase 1: Mount Component

### Objective

Add `HistorySidebar.mount()` call so the sidebar DOM elements exist.

### Tasks

1. **Locate DOMContentLoaded handler in home.html**
   - Find existing `document.addEventListener('DOMContentLoaded', ...)`

2. **Add mount call**
   ```javascript
   // Mount History sidebar (Issue #735)
   if (window.HistorySidebar) {
     HistorySidebar.mount(document.body, {
       onSelect: handleHistorySelect,
       onSearch: handleHistorySearch,
       onLoadMore: handleHistoryLoadMore,
       onPrivacyToggle: handleHistoryPrivacyToggle
     });
   }
   ```

3. **Add stub callbacks** (to be implemented in Phase 2-3)
   ```javascript
   function handleHistorySelect(conversation) {
     console.log('Selected:', conversation);
     // TODO: Load conversation in chat
   }

   function handleHistorySearch(query) {
     console.log('Search:', query);
     // TODO: Fetch filtered results
   }

   function handleHistoryLoadMore(page) {
     console.log('Load more:', page);
     // TODO: Fetch next page
   }

   function handleHistoryPrivacyToggle(isPrivate) {
     console.log('Privacy:', isPrivate);
     // TODO: Toggle privacy mode
   }
   ```

### Verification

- [ ] Browser shows sidebar when History button clicked
- [ ] Empty state displays (no API call yet)
- [ ] Console logs show callback invocations

### Deliverables

- Modified `templates/home.html`
- Screenshot of sidebar opening

### Progressive Bookending

After phase completion:
```bash
gh issue comment 735 -b "✓ Phase 1 complete: Mount call added, sidebar opens"
```

---

## Phase 2: Wire API Integration

### Objective

Fetch conversation history from API and display in sidebar.

### Tasks

1. **Implement fetchConversations()**
   ```javascript
   async function fetchConversations(query = '', page = 1) {
     const params = new URLSearchParams();
     if (query) params.set('q', query);
     params.set('page', page);

     const response = await fetch(`/api/conversations?${params}`);
     const data = await response.json();

     // Transform to component format
     return {
       conversations: data.conversations.map(c => ({
         id: c.id,
         topic_summary: c.title || c.topic_summary || 'Untitled',
         summary: c.summary || '',
         timestamp: c.last_activity_at || c.created_at,
         is_private: c.is_private || false,
         channel: c.channel || 'web'
       })),
       pagination: {
         page: page,
         totalPages: data.has_more ? page + 1 : page
       }
     };
   }
   ```

2. **Update mount to load initial data**
   ```javascript
   if (window.HistorySidebar) {
     HistorySidebar.mount(document.body, { ... });
     // Load initial data
     loadHistoryData();
   }

   async function loadHistoryData(query = '', page = 1) {
     try {
       const data = await fetchConversations(query, page);
       HistorySidebar.update(data.conversations, data.pagination);
     } catch (error) {
       console.error('Failed to load history:', error);
     }
   }
   ```

3. **Implement onSearch callback**
   ```javascript
   function handleHistorySearch(query) {
     loadHistoryData(query, 1);
   }
   ```

4. **Implement onLoadMore callback**
   ```javascript
   let currentHistoryPage = 1;
   let currentHistoryQuery = '';

   function handleHistoryLoadMore(page) {
     currentHistoryPage = page;
     loadHistoryData(currentHistoryQuery, page);
   }
   ```

### Verification

- [ ] Sidebar shows real conversations from API
- [ ] Conversations grouped by date (Today, Yesterday, etc.)
- [ ] Search filters results
- [ ] Load More fetches next page

### Deliverables

- Working API integration
- Screenshot showing real conversations

---

## Phase 3: Wire User Actions

### Objective

Handle user interactions - selecting conversations and privacy toggle.

### Tasks

1. **Implement onSelect callback**
   ```javascript
   function handleHistorySelect(conversation) {
     // Load selected conversation in chat
     const chatContainer = document.getElementById('chat-container');
     if (chatContainer && window.loadConversation) {
       window.loadConversation(conversation.id);
     } else {
       // Fallback: navigate to conversation
       window.location.href = `/chat?conversation=${conversation.id}`;
     }
   }
   ```

2. **Implement onPrivacyToggle callback**
   ```javascript
   async function handleHistoryPrivacyToggle(isPrivate) {
     // TODO: Call privacy API when available
     console.log('Privacy mode:', isPrivate ? 'enabled' : 'disabled');
     // For now, just update local state
     // Future: POST /api/privacy/toggle
   }
   ```

3. **Wire to existing chat loading logic**
   - Check if `loadConversation()` exists in home.html
   - If yes, use it
   - If no, implement minimal version

### Verification

- [ ] Clicking conversation loads it in chat
- [ ] Privacy toggle logs to console (stub OK for now)
- [ ] Sidebar closes after selection

### Deliverables

- Working conversation selection
- Evidence of chat loading

---

## Phase 4: Testing & Polish

### Objective

Verify all functionality and handle edge cases.

### Manual Testing Checklist

**Scenario 1: First-Time User**
- [ ] Log in as new user with no conversations
- [ ] Click History button
- [ ] Verify empty state displays
- [ ] Verify sidebar closes on X or Escape

**Scenario 2: Returning User**
- [ ] Log in as user with existing conversations
- [ ] Click History button
- [ ] Verify conversations appear grouped by date
- [ ] Click a conversation
- [ ] Verify it loads in chat area

**Scenario 3: Search**
- [ ] Open History sidebar
- [ ] Type in search box
- [ ] Verify results filter after debounce
- [ ] Clear search
- [ ] Verify full list returns

**Scenario 4: Keyboard Navigation**
- [ ] Open sidebar with Ctrl/Cmd+H (command palette)
- [ ] Press Escape to close
- [ ] Tab through items
- [ ] Press Enter to select

### Unit Test Verification

```bash
pytest tests/unit/templates/test_history_sidebar.py -v
# Expected: 56 tests passing
```

### Regression Check

- [ ] Left sidebar (#565) still works
- [ ] Navigation buttons still work
- [ ] Command palette still works

---

## Phase Z: Final Bookending & Handoff

### GitHub Issue Update

Update issue #735 with:
- [x] All phase checkboxes checked
- [ ] Completion matrix 100%
- [ ] Evidence links for each component
- [ ] Test output showing 56 tests pass

### Evidence Compilation

```bash
# Test output
pytest tests/unit/templates/test_history_sidebar.py -v

# Modified files
git diff --name-only
# Expected: templates/home.html

# Commit
git add templates/home.html
git commit -m "feat(#735): Mount and wire History sidebar component"
```

### Completion Checklist

- [ ] All acceptance criteria met
- [ ] 56 existing tests passing
- [ ] No console errors
- [ ] No regressions to left sidebar
- [ ] Session log updated

---

## Multi-Agent Coordination Plan

### Agent Deployment

| Phase | Agent Type | Evidence Required |
|-------|------------|------------------|
| All | Lead Dev (direct) | Test output, screenshots |

**Single agent work** - no subagents needed for this scope.

### Verification Gates

- [ ] Phase 1: Sidebar opens (empty state OK)
- [ ] Phase 2: Conversations display from API
- [ ] Phase 3: Selection works
- [ ] Phase 4: All manual tests pass

---

## STOP Conditions (Apply Throughout)

Stop immediately and escalate if:
- API endpoint doesn't exist or returns errors
- Component template is missing or corrupted
- Left sidebar breaks after changes
- Navigation wiring is more complex than expected
- loadConversation() doesn't exist and fallback fails

---

## Success Criteria

| Criterion | Verification |
|-----------|--------------|
| History button works | Manual test |
| Conversations display | Screenshot |
| Search filters | Manual test |
| Selection loads chat | Manual test |
| Empty state works | Manual test with new user |
| 56 tests pass | pytest output |
| No regressions | Manual test left sidebar |

---

## Effort Estimate

| Phase | Estimate |
|-------|----------|
| Phase -1 | 5 min (already done) |
| Phase 0 | 5 min (already done) |
| Phase 1 | 15 min |
| Phase 2 | 45 min |
| Phase 3 | 30 min |
| Phase 4 | 30 min |
| Phase Z | 15 min |
| **Total** | ~2.5 hours |

---

_Gameplan created: 2026-01-30_
_Issue: #735_
