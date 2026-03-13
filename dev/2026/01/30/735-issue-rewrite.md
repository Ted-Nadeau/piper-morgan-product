# FINISH-HISTORY-SIDEBAR - Mount and Wire History Sidebar Component

**Priority**: P2
**Labels**: `finish`, `MUX-IMPLEMENT`, `UX`
**Milestone**: Sprint P3-Extended
**Epic**: MUX-OBJECTS-VIEWS (#706)
**Related**: #425 (parent), #565 (left sidebar), PDR-002, #732 (trust gate)

---

## Problem Statement

### Current State

The History sidebar component (`history_sidebar.html`) was created in #425 (MUX-IMPLEMENT-MEMORY-SYNC) but **never mounted**. The component exists with full functionality (search, pagination, date grouping, privacy toggle, empty state), but:

1. `HistorySidebar.mount()` is never called
2. The navigation History button calls `toggle()` on an unmounted component → nothing happens
3. Command palette "Open History" commands call `open()` on an unmounted component → nothing happens

### Impact

- **Blocks**: Users cannot access Layer 2 User History (PDR-002) via UI
- **User Impact**: History button in navigation does nothing (confusing UX)
- **Technical Debt**: 56 unit tests exist for component that's not user-accessible

### Strategic Context

PDR-002 establishes **Three-Layer Context Persistence**:
1. Conversational Memory (24-hour window)
2. **User History (searchable archive)** ← This component
3. Composted Learning (patterns)

The History sidebar is the primary UI for Layer 2. Without it, users can't browse, search, or access past conversations.

---

## Goal

**Primary Objective**: Mount the History sidebar component and wire it to display user conversation history.

**Example User Experience**:
```
Before: User clicks History button → Nothing happens
After:  User clicks History button → Right sidebar slides in showing past conversations grouped by date
```

**Not In Scope** (explicitly):
- ❌ Showing non-conversation objects (WorkItems, Documents, etc.) - future MUX work
- ❌ Modifying the component's internal behavior - it's already tested and working
- ❌ Creating new API endpoints - use existing `/api/conversations`

---

## What Already Exists

### Infrastructure ✅

| Component | Location | Status |
|-----------|----------|--------|
| Sidebar component | `templates/components/history_sidebar.html` | ✅ Complete |
| `window.HistorySidebar` API | Same file | ✅ Complete (mount, toggle, update, etc.) |
| Navigation button | `templates/components/navigation.html:641` | ✅ Calls toggle() |
| Command palette | `templates/components/command_palette.html:464` | ✅ Calls open() |
| Empty state | Built into component | ✅ "No conversation history yet" |
| 56 unit tests | `tests/unit/templates/test_history_sidebar.py` | ✅ Passing |
| API endpoint | `GET /api/conversations` | ✅ Returns paginated list |

### What's Missing ❌

1. **Mount call** - `HistorySidebar.mount(document.body, options)` in home.html DOMContentLoaded
2. **Callback implementations** - onSelect, onSearch, onLoadMore, onPrivacyToggle
3. **API integration** - Fetch conversations and call `HistorySidebar.update(data)`

---

## Requirements

### Phase -1: Verification (5 min)

- [ ] Confirm component loads: `window.HistorySidebar` exists after page load
- [ ] Confirm API works: `curl /api/conversations` returns data
- [ ] Confirm button is wired: Navigation calls `window.HistorySidebar.toggle()`

### Phase 1: Mount Component (15 min)

**Objective**: Add mount call so sidebar DOM elements exist

**Tasks**:
- [ ] Add `HistorySidebar.mount(document.body, {})` to home.html DOMContentLoaded
- [ ] Verify sidebar appears when History button clicked (empty state OK)

**Deliverables**:
- Modified `templates/home.html`
- Screenshot showing sidebar opening

### Phase 2: Wire API Integration (45 min)

**Objective**: Populate sidebar with real conversation data

**Tasks**:
- [ ] Implement `fetchConversations()` calling `/api/conversations`
- [ ] Implement `onSearch` callback to filter conversations
- [ ] Implement `onLoadMore` callback for pagination
- [ ] Call `HistorySidebar.update(conversations, pagination)` with API response
- [ ] Load initial data on mount

**Deliverables**:
- Modified `templates/home.html` with fetch logic
- Screenshot showing conversations in sidebar

### Phase 3: Wire User Actions (30 min)

**Objective**: Handle user interactions with sidebar

**Tasks**:
- [ ] Implement `onSelect` callback to load selected conversation
- [ ] Implement `onPrivacyToggle` callback (or stub with TODO if privacy API not ready)
- [ ] Verify clicking conversation loads it in chat

**Deliverables**:
- Working conversation selection
- Evidence of load in chat area

### Phase 4: Testing & Polish (30 min)

**Objective**: Verify all functionality works end-to-end

**Tasks**:
- [ ] Test empty state (new user with no history)
- [ ] Test search functionality
- [ ] Test pagination (if enough conversations exist)
- [ ] Test keyboard navigation (Escape to close)
- [ ] Test mobile overlay

**Deliverables**:
- Manual testing checklist completed
- Any regression tests needed

### Phase Z: Completion & Handoff

- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] Documentation updated (if any)
- [ ] GitHub issue fully updated
- [ ] Session log completed

---

## Acceptance Criteria

### Functionality
- [ ] History button in navigation opens right sidebar
- [ ] Sidebar shows user's past conversations grouped by date
- [ ] Search input filters displayed conversations
- [ ] Clicking conversation loads it in chat area
- [ ] Empty state displays for users with no history
- [ ] Sidebar closes on X button, overlay click, or Escape key

### Testing
- [ ] Existing 56 unit tests still passing
- [ ] Manual testing scenarios verified (see below)
- [ ] No console errors during operation

### Quality
- [ ] No regressions to left sidebar (#565)
- [ ] No regressions to navigation functionality
- [ ] Keyboard accessible (Tab, Enter, Escape)

### Documentation
- [ ] Session log completed with evidence
- [ ] Issue description updated with completion matrix

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Mount call added | ⏸️ | |
| API fetch working | ⏸️ | |
| onSearch callback | ⏸️ | |
| onLoadMore callback | ⏸️ | |
| onSelect callback | ⏸️ | |
| onPrivacyToggle callback | ⏸️ | |
| Empty state verified | ⏸️ | |
| Existing tests passing | ⏸️ | |

---

## Testing Strategy

### Unit Tests
- Existing 56 tests in `tests/unit/templates/test_history_sidebar.py` cover component
- No new unit tests needed (component unchanged)

### Integration Tests
- Verify mount + API integration works together
- Verify conversation selection updates chat

### Manual Testing Checklist

**Scenario 1: First-Time User**
1. [ ] Log in as new user with no conversations
2. [ ] Click History button
3. [ ] Verify empty state displays: "No conversation history yet"
4. [ ] Verify sidebar closes on X or Escape

**Scenario 2: Returning User**
1. [ ] Log in as user with existing conversations
2. [ ] Click History button
3. [ ] Verify conversations appear grouped by date
4. [ ] Click a conversation
5. [ ] Verify it loads in chat area

**Scenario 3: Search**
1. [ ] Open History sidebar
2. [ ] Type in search box
3. [ ] Verify results filter after 300ms debounce
4. [ ] Clear search
5. [ ] Verify full list returns

---

## Success Metrics

### Quantitative
- All 56 existing tests passing
- No new console errors
- Sidebar opens in <100ms

### Qualitative
- History button "just works"
- Conversation selection feels natural
- Empty state is helpful, not confusing

---

## STOP Conditions

**STOP immediately and escalate if**:
- API endpoint `/api/conversations` doesn't exist or returns errors
- Component template `history_sidebar.html` is missing or corrupted
- Left sidebar (#565) breaks after changes
- Navigation button wiring is more complex than expected
- Privacy API not available (stub and document)

---

## Effort Estimate

**Overall Size**: Small

**Breakdown by Phase**:
- Phase -1: 5 min (verification)
- Phase 1: 15 min (mount call)
- Phase 2: 45 min (API wiring)
- Phase 3: 30 min (user actions)
- Phase 4: 30 min (testing)
- **Total**: ~2 hours

**Complexity Notes**: Low complexity - component exists and works. This is wiring, not creation.

---

## Dependencies

### Required (Must be complete first)
- [x] #425 - History sidebar component (CLOSED - complete)
- [x] `/api/conversations` endpoint operational

### Optional (Nice to have)
- [ ] Privacy mode API (can stub if not ready)

---

## Related Documentation

- **Product**: PDR-002 (Conversational Glue) - Three-Layer Context Persistence
- **Architecture**: ADR-054 (Cross-Session Memory)
- **Implementation**: #425 MUX-IMPLEMENT-MEMORY-SYNC (parent issue)
- **Research**: `dev/2026/01/30/735-mux-research.md`

---

## Notes for Implementation

**PM Clarification (6:02 PM)**:
> The history right sidebar is not for conversations but for other objects that will appear over time.

For this issue, mount as-is with conversations. Object expansion (WorkItems, Documents, etc.) is future scope per #706 MUX-OBJECTS-VIEWS roadmap.

**API Response Format** (expected by component):
```javascript
{
  conversations: [
    {
      id: "uuid",
      topic_summary: "Project planning discussion",
      summary: "We discussed...",
      timestamp: "2026-01-30T10:00:00Z",
      is_private: false,
      channel: "web"
    }
  ],
  pagination: { page: 1, totalPages: 3 }
}
```

---

## Evidence Section

[This section is filled in during/after implementation]

### Implementation Evidence
```bash
[Terminal output showing tests passing]
[Commit hashes with descriptions]
```

---

## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met ✅
- [ ] Completion matrix 100% ✅
- [ ] Evidence provided for each criterion ✅
- [ ] Tests passing with output ✅
- [ ] No regressions confirmed ✅
- [ ] STOP conditions all clear ✅
- [ ] Session log complete ✅

**Status**: In Progress

---

_Issue rewritten: 2026-01-30_
_Source: #735 original + MUX research_
