# Issue #735 MUX Research

**Date**: 2026-01-30
**Issue**: #735 - Finish: Mount History sidebar component (#425)

---

## Key Clarifications from PM (6:02 PM)

1. **The right sidebar (HistorySidebar) is NOT for conversations** - it's for "other objects that will appear over time"
2. **Left sidebar** (#565) - simple conversation list for current chat context
3. **Right sidebar** (#425) - Layer 2 User History per PDR-002 design
4. **Empty state needed** - new users won't have history yet
5. **Must research MUX docs** to ensure consistent design

---

## What the Component Was Designed For

From #425 (MUX-IMPLEMENT-MEMORY-SYNC) and PDR-002:

### Layer 2: User History

PDR-002 defines three layers of context persistence:
1. **Layer 1: Conversational Memory** (24-hour window) - Natural continuity
2. **Layer 2: User History** (all time) - Searchable archive ← **This is what HistorySidebar displays**
3. **Layer 3: Composted Learning** (patterns) - Informs behavior

### Component Features (from history_sidebar.html)

| Feature | Status | Notes |
|---------|--------|-------|
| Date grouping (today, yesterday, this week, older) | ✅ Implemented | Works |
| Search functionality | ✅ Implemented | Debounced input |
| Click to view/continue | ✅ Implemented | Callback-based |
| Private conversation indicator | ✅ Implemented | 🔒 icon |
| Pagination | ✅ Implemented | Load more button |
| Privacy mode toggle | ✅ Implemented | Start/end private session |
| Empty state | ✅ Implemented | "No conversation history yet" |
| Keyboard accessibility | ✅ Implemented | Enter/Space to select |

### Component API

```javascript
HistorySidebar.mount(container, {
  onSelect: (conversation) => { /* Load/continue conversation */ },
  onSearch: (query) => { /* Fetch filtered results */ },
  onLoadMore: (page) => { /* Fetch next page */ },
  onPrivacyToggle: (isPrivate) => { /* Toggle privacy mode */ }
});

HistorySidebar.update(conversations, { page, totalPages });
HistorySidebar.open();
HistorySidebar.close();
HistorySidebar.toggle();
HistorySidebar.setPrivacyState(isPrivate);
```

---

## The Gap: What's Missing

### 1. Mount Call (The Bug)

Component is included but never mounted:

```html
<!-- templates/home.html:1012 -->
{% include 'components/history_sidebar.html' %}
```

Missing initialization:
```javascript
// Need to add to DOMContentLoaded
if (window.HistorySidebar) {
  HistorySidebar.mount(document.body, {
    onSelect: handleConversationSelect,
    onSearch: handleHistorySearch,
    onLoadMore: handleLoadMore,
    onPrivacyToggle: handlePrivacyToggle
  });
}
```

### 2. Backend API Wiring

The sidebar needs data. Options:

| Option | Endpoint | Exists? |
|--------|----------|---------|
| Conversations | `GET /api/conversations` | ✅ Yes (`list_conversations`) |
| User History | `UserHistoryService.get_history()` | ✅ Yes (not exposed via API) |

**Decision needed**: Use existing `/api/conversations` or create dedicated history API?

### 3. Callback Implementations

Need to implement:
- `handleConversationSelect(conv)` → Load conversation in chat
- `handleHistorySearch(query)` → Fetch filtered results
- `handleLoadMore(page)` → Fetch next page
- `handlePrivacyToggle(isPrivate)` → Toggle privacy mode

### 4. Empty State Content

Current empty state is generic:
```
"No conversation history yet"
"No conversations match your search"
```

**Question**: Is this sufficient, or should empty state guide users on what to do?

---

## Design Questions to Resolve (Phase -1)

### Q1: What objects does the sidebar show?

PM said "other objects that will appear over time" - but the current implementation only handles conversations.

**Current**: Conversations only
**Future per views-objects-roadmap.md**: Possibly WorkItems, Documents, Lists (all have lifecycle)

**Recommendation**: Mount as-is for conversations. Object expansion is future scope.

### Q2: What API should the sidebar call?

| Option | Pros | Cons |
|--------|------|------|
| **A) `/api/conversations`** | Already exists, tested | May not have all history fields |
| **B) New `/api/history`** | Clean separation | More work |
| **C) Use UserHistoryService** | Has search, pagination | Needs API endpoint |

**Recommendation**: Use existing `/api/conversations` for MVP. Create `/api/history` if needed.

### Q3: Trust gating for history access?

Per PDR-002 Trust Gradient and #732:
- Stage 2+ for work references
- Stage 3+ for history commands

**Question**: Should History button be trust-gated?

**Recommendation**: No trust gate for viewing own history (it's your data). Trust gate is for proactive surfacing.

### Q4: Empty state for new users?

Options:
- A) Generic "No history yet" ← Current
- B) Helpful "You haven't had any conversations yet" with action
- C) Hide sidebar until there's content

**Recommendation**: Keep current empty state. It's clear and functional.

---

## Related MUX Work

| Issue | Title | Relevance |
|-------|-------|-----------|
| #425 | MUX-IMPLEMENT-MEMORY-SYNC | Parent issue (CLOSED - component created) |
| #565 | Left conversation sidebar | Different sidebar, works |
| #706 | MUX-OBJECTS-VIEWS | Future: History shows objects with lifecycle |
| #715 | MUX-HOME-CONVERSATIONS-LIFECYCLE | Wire lifecycle to Home/Conversations |
| #732 | History trust gate fix | Trust gate for history access |

---

## Implementation Summary

### What Exists ✅
- `history_sidebar.html` - Full component with styling, templates, JS
- `window.HistorySidebar` object with mount/update/toggle API
- Navigation button wired to call `toggle()`
- Command palette commands wired to call `open()`
- Empty state rendering
- 56 unit tests for the component

### What's Missing ❌
1. `HistorySidebar.mount()` call in home.html DOMContentLoaded
2. Callback implementations (onSelect, onSearch, onLoadMore, onPrivacyToggle)
3. API integration to fetch conversation history

### Effort Estimate

| Task | Effort |
|------|--------|
| Add mount() call | 5 min |
| Implement callbacks | 30 min |
| Wire to existing API | 30 min |
| Testing | 30 min |
| **Total** | ~2 hours |

---

## Recommendation

**Proceed with Option A from original issue** - mount the sidebar with minimal callbacks, wired to existing `/api/conversations` endpoint.

The component is 95% complete. Only the "last mile" wiring is missing.
