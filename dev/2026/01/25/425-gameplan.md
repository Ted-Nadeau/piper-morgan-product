# Gameplan: #425 MUX-IMPLEMENT-MEMORY-SYNC

**Issue**: #425 MUX-IMPLEMENT-MEMORY-SYNC: Memory sync between touchpoints
**Date**: 2026-01-25
**Author**: Lead Developer (Claude Code Opus)

---

## Phase -1: Infrastructure Verification

### Part A: Chief Architect's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] CLI structure: N/A for this issue
- [x] Database: PostgreSQL
- [x] Testing framework: pytest
- [x] Existing endpoints: `/` (home), `/documents`, `/insights`
- [x] Missing features: `/history` endpoint, greeting context UI, privacy toggle

**My understanding of the task**:
- Backend memory services are COMPLETE (ConversationalMemoryService, UserHistoryService, GreetingContextService, PrivacyModeService)
- UI layer needs to be created to expose these services
- 5 phases per issue: (1) Greeting UI, (2) History Sidebar, (3) Privacy Mode UI, (4) Cross-Channel Indicator, (5) Navigation Integration

### Part A.2: Work Characteristics Assessment

**Assessment**: SKIP WORKTREE
- Single agent, sequential work
- UI components build on each other (sidebar → privacy → nav integration)
- Estimate 2-3 hours of focused work

### Part B: PM Verification

**Verified earlier this session**:
- Backend services at `services/memory/` all exist and work
- GreetingContextService has 7 conditions defined
- UserHistoryService has pagination, search, mark_private
- PrivacyModeService has start/end session, retroactive marking

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Backend infrastructure verified, issue well-specified

---

## Phase 0: Initial Bookending

### GitHub Issue Verification
```bash
gh issue view 425  # Verified - has full specification
```

### Codebase Investigation

**Backend services verified**:
| Service | Location | Methods |
|---------|----------|---------|
| GreetingContextService | services/memory/greeting_context.py:102-243 | get_greeting_context() |
| UserHistoryService | services/memory/user_history.py:285-442 | get_history(), search_history(), mark_private() |
| PrivacyModeService | services/memory/privacy_mode.py:75-267 | start_private_session(), end_private_session(), get_privacy_state() |

**Greeting conditions from ADR-054**:
- SAME_DAY_RECENT (< 8 hours)
- NEXT_DAY_ACTIVE (< 36 hours)
- WEEK_GAP (< 168 hours)
- MONTH_GAP (>= 168 hours)
- PREVIOUS_TRIVIAL
- PREVIOUS_NEGATIVE
- FIRST_SESSION

---

## Phase 0.5: Frontend-Backend Contract Verification

### API Endpoints Needed

| Phase | Endpoint | Backend Service | Route File |
|-------|----------|-----------------|------------|
| 1 | GET /api/greeting-context | GreetingContextService | NEW: greeting.py |
| 2 | GET /api/history | UserHistoryService | NEW: history.py |
| 2 | GET /api/history/search | UserHistoryService | NEW: history.py |
| 3 | POST /api/privacy/start | PrivacyModeService | NEW: privacy.py |
| 3 | POST /api/privacy/end | PrivacyModeService | NEW: privacy.py |
| 3 | GET /api/privacy/state | PrivacyModeService | NEW: privacy.py |

### Note on Backend API Routes

Decision: Create UI components first with JavaScript that will call backend APIs. Backend routes can be created as a follow-up or in parallel. The primary focus of this issue is the UI components per the MUX-IMPLEMENT epic scope.

For Phase 1-4, we'll create frontend templates that expect API endpoints. Phase 5 wires into existing navigation.

---

## Phase 0.6: Data Flow & Integration Verification

### User Context Propagation

| Layer | Needs user_id? | Needs session_id? | Source |
|-------|----------------|-------------------|--------|
| UI Template | Yes (for API calls) | Yes (for privacy state) | session/cookies |
| API Route | Yes | Yes | get_current_user dependency |
| Service | Yes | Yes | parameters from route |

### State Persistence

- Conversation history: Database (UserHistoryRepository)
- Privacy mode: In-memory per session (PrivacyModeService._session_privacy)
- Greeting context: Computed on demand (no persistence)

---

## Phase 0.7: Conversation Design

**N/A** - This issue creates read-only UI, not conversational features. Greeting context displays but doesn't gather input beyond "Continue" / "Start fresh" buttons.

---

## Phase 0.8: Post-Completion Integration

**When complete**:
- History sidebar visible when user clicks History nav item
- Privacy mode toggle available
- Greeting shows context-aware message on home

**Downstream changes**: None - these are display features that read from existing services.

---

## Phase 1: Context-Aware Greeting UI

**Scope**: Create greeting component that shows condition-specific welcome message

### Deliverables
1. `templates/components/greeting_context.html` - Greeting component
2. `tests/unit/templates/test_greeting_context.py` - Unit tests

### Implementation
- Display condition-specific message per ADR-054 table
- "Continue" and "Start fresh" buttons
- Topic/entity references when available (SAME_DAY_RECENT, NEXT_DAY_ACTIVE)
- Clean slate for PREVIOUS_NEGATIVE
- Trust-gated (Stage 2+ for work references)

### Acceptance Criteria
- [ ] All 7 greeting conditions render correctly
- [ ] Continue/Start fresh buttons functional
- [ ] Topic references displayed naturally
- [ ] PREVIOUS_NEGATIVE shows no prior reference
- [ ] Tests: ~25 tests

---

## Phase 2: Conversation History Sidebar

**Scope**: Create history panel component for viewing past conversations

### Deliverables
1. `templates/components/history_sidebar.html` - History sidebar
2. `tests/unit/templates/test_history_sidebar.py` - Unit tests

### Implementation
- Paginated history display
- Date grouping (today, yesterday, this week, older)
- Search input
- Click to view conversation detail
- Visual indicator for private conversations (lock icon)

### Acceptance Criteria
- [ ] History panel renders
- [ ] Date grouping works
- [ ] Search input present
- [ ] Private conversation indicator
- [ ] Tests: ~30 tests

---

## Phase 3: Privacy Mode UI

**Scope**: Create privacy mode controls

### Deliverables
1. `templates/components/privacy_mode.html` - Privacy controls
2. `tests/unit/templates/test_privacy_mode.py` - Unit tests

### Implementation
- "Start private session" button with confirmation
- Visual indicator during private session (banner)
- "Mark as private" for existing conversations (in history)
- Privacy mode respects D2 patterns (clear, no guilt)

### Acceptance Criteria
- [ ] Start private session action
- [ ] Visual indicator during private session
- [ ] Mark existing as private action
- [ ] Private conversations hidden by default
- [ ] Tests: ~25 tests

---

## Phase 4: Cross-Channel Continuity Indicator

**Scope**: Create indicator when user switches channels

### Deliverables
1. `templates/components/channel_continuity.html` - Continuity indicator
2. `tests/unit/templates/test_channel_continuity.py` - Unit tests

### Implementation
- Detect recent activity in other channels
- Display at session start: "You were just working on..."
- Offer continuity or fresh start
- No surveillance language ("I saw you in Slack" → "You were working on...")

### Acceptance Criteria
- [ ] Channel detection indicator
- [ ] Continue/fresh start options
- [ ] No surveillance language
- [ ] Tests: ~20 tests

---

## Phase 5: Navigation Integration

**Scope**: Add History to navigation and command palette

### Deliverables
1. Update `templates/components/navigation.html`
2. Update `templates/components/command_palette.html`
3. `tests/unit/templates/test_navigation.py` - Update tests

### Implementation
- Add "History" nav item
- Command palette: "Search conversations", "Start private session"
- Link to history sidebar toggle

### Acceptance Criteria
- [ ] Nav item for history
- [ ] Command palette commands
- [ ] Tests updated

---

## Phase Z: Final Bookending

### Evidence Collection
- All phase tests passing
- Full test suite passing
- GitHub issue updated with completion matrix

### Success Criteria
- [ ] ~100+ new tests for #425
- [ ] All 5 phases complete
- [ ] Navigation integrated
- [ ] No surveillance language
- [ ] No regressions

---

## Test Strategy

### Unit Tests
- Greeting component: All 7 conditions
- History sidebar: Pagination, search, date grouping
- Privacy mode: Toggle state, visual indicator
- Channel continuity: Detection, language

### D2/D3 Compliance Tests
- No surveillance language checks
- Privacy mode respects user choice
- Greeting offers choice (not force continuity)

---

## STOP Conditions

**STOP immediately and escalate if**:
- Backend memory services unavailable
- Greeting conditions don't match ADR-054
- Privacy mode leaks to history
- Cross-channel feels surveillance-like
- Tests fail for any reason

---

## Anti-Patterns to Avoid (from issue)

1. ❌ "I've been tracking your conversations"
2. ❌ Force continuity without user choice
3. ❌ Memory dump (show all history at once)
4. ❌ Privacy theater (must truly be private)
5. ❌ "I saw you in Slack" → ✅ "You were just working on..."

---

## Effort Estimate

| Phase | Estimate |
|-------|----------|
| Phase 1 (Greeting) | 20 min |
| Phase 2 (History) | 30 min |
| Phase 3 (Privacy) | 25 min |
| Phase 4 (Cross-Channel) | 20 min |
| Phase 5 (Navigation) | 15 min |
| **Total** | ~2 hours |

---

*Gameplan created: 2026-01-25 7:45 PM*
