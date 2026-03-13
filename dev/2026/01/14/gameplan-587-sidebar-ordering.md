# Gameplan: Issue #587 - Sidebar Ordering Bug

**Issue**: [#587](https://github.com/mediajunkie/piper-morgan-product/issues/587)
**Type**: Bug Fix (P2)
**Template Version**: v9.3

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Chief Architect's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Frontend: Jinja2 templates + vanilla JavaScript
- [x] Database: PostgreSQL with SQLAlchemy
- [x] Conversation model has `last_activity_at` field (indexed)
- [x] Repository sorts by `created_at.desc()` (line 1013 of repositories.py)

**Root Cause Identified**:
- Repository method `list_for_user()` sorts by `created_at.desc()`
- Should sort by `last_activity_at.desc()` (or `COALESCE(last_activity_at, created_at)`)
- Date grouping in frontend uses `updated_at || created_at` but data arrives in wrong order

**My understanding of the task**:
- Change sort order in repository from `created_at` to `last_activity_at`
- Ensure conversations with recent activity appear at top regardless of creation date

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

- [x] Single agent, sequential work
- [x] Small fixes (<15 min estimated)
- [x] Single file modification likely

**Assessment**:
- [x] **SKIP WORKTREE** - Single file fix, focused scope

### Part B: PM Verification Required

**PM, please confirm**:

1. **Sort behavior preference**:
   - [x] Sort by `last_activity_at` (most recently active first)
   - [ ] Sort by `created_at` (newest created first)
   - [ ] Other: ____________

2. **Null handling for `last_activity_at`**:
   - [x] Use `COALESCE(last_activity_at, created_at)` for conversations with no activity yet
   - [ ] Always require `last_activity_at` to be set

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Root cause identified, fix is straightforward

---

## Phase 0: Investigation Complete

### Root Cause

**File**: `services/database/repositories.py` line 1013

```python
.order_by(ConversationDB.created_at.desc())  # BUG: Should be last_activity_at
```

### Why This Causes the Bug

1. User creates conversation Monday → `created_at = Monday`
2. User sends message Wednesday → `last_activity_at = Wednesday`
3. API returns conversations sorted by `created_at` (Monday first)
4. Frontend groups by `updated_at` (Wednesday = Today)
5. Result: Wednesday's conversation appears in "Today" group but BELOW Monday's conversation

### Evidence Chain

| Layer | What It Does | Correct? |
|-------|--------------|----------|
| Repository | Sorts by `created_at.desc()` | ❌ Wrong |
| API | Passes through | ✅ OK |
| Frontend grouping | Groups by `updated_at || created_at` | ✅ OK |
| Frontend rendering | Renders in received order | ✅ OK |

**Single point of failure**: Repository sort order

---

## Phase 1: Implementation

### Fix

**File**: `services/database/repositories.py`
**Line**: 1013
**Change**: Sort by `last_activity_at` with fallback to `created_at`

```python
# Before
.order_by(ConversationDB.created_at.desc())

# After (Issue #587)
.order_by(
    func.coalesce(ConversationDB.last_activity_at, ConversationDB.created_at).desc()
)
```

**Import needed**: `from sqlalchemy import func` (likely already imported)

### Files to Modify

| File | Change |
|------|--------|
| `services/database/repositories.py` | Change sort order in `list_for_user()` |

---

## Phase 2: Testing

### Unit Tests
- [ ] Verify `list_for_user()` returns conversations in `last_activity_at` order
- [ ] Verify conversations with NULL `last_activity_at` use `created_at` as fallback

### Manual Verification
- [ ] Create new conversation → appears at top
- [ ] Send message in old conversation → moves to top
- [ ] Date groupings show correct labels
- [ ] Page refresh maintains correct order

### Regression
- [ ] Existing conversation list functionality unaffected
- [ ] Pagination still works correctly

---

## Phase Z: Completion

### Acceptance Criteria (from #587)

- [ ] New conversations appear at TOP of sidebar (most recent first)
- [ ] Date groupings show correct labels ("Today", "Yesterday", "This Week", etc.)
- [ ] Conversations sorted by most recent activity (updated_at descending)
- [ ] After sending a message, conversation moves to top of list
- [ ] Timezone handling is correct for date group boundaries

### Evidence Required

1. **Before/after**: Screenshot or description of ordering behavior
2. **Test output**: Any unit tests modified/added

---

## STOP Conditions

- [ ] `func` import not available → check SQLAlchemy imports
- [ ] `last_activity_at` not being updated on new messages → separate bug
- [ ] Performance concerns with COALESCE → discuss with PM

---

## Multi-Agent Deployment

**Recommendation**: Single agent sufficient

**Rationale**:
- Single file, single line fix
- Clear root cause identified
- <15 min estimated

---

## Estimated Effort

| Phase | Estimate |
|-------|----------|
| Phase -1 | 2 min (PM confirmation) |
| Phase 0 | Done (investigation complete) |
| Phase 1 | 5 min (implementation) |
| Phase 2 | 10 min (testing) |
| Phase Z | 5 min (documentation) |
| **Total** | **~20 min** |

---

*Gameplan created: 2026-01-14*
*Template: v9.3*
