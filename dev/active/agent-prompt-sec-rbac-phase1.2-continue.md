# Claude Code Prompt: SEC-RBAC Phase 1.2 Service Layer Ownership Checks (Continuation)

## Your Identity

You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## CRITICAL: Post-Compaction Context Recovery

You just compacted and received this continuation prompt. Here's where you left off:

**Last Completed Work**:

- ✅ P0 CRITICAL FIX (commit 263ae02f) - Fixed cross-user file access in FileRepository
- ✅ Phase 1.1 Database Schema (commit 5d92d212) - Added owner_id to 9 resource tables
- ✅ Phase 1.2 FileRepository (commit 1a41237e) - Added owner_id validation to 3 CRUD methods
- ✅ Documentation (commit 512c760d) - Phase 0 and 1 reports
- ✅ Test Skip Fix (just completed) - Unblocked git push

**Current Position**: Resume Phase 1.2 Service Layer Ownership Checks

---

## Mission

**Continue Phase 1.2 Service Layer Ownership Checks** for SEC-RBAC Issue #357.

Add owner_id validation to all remaining service layer CRUD methods (40+ methods across 8+ services) to prevent cross-user resource access at the service layer (defense-in-depth).

**This prompt covers ONLY**: UniversalListRepository owner_id validation
**NOT in scope**: Other repositories (separate continuation prompts will follow)
**Next after this**: TodoManagementService, Learning services, Knowledge services, etc.

---

## Context

- **GitHub Issue**: #357 - SEC-RBAC: Implement Role-Based Access Control
- **Current Phase**: Phase 1.2 - Service Layer Ownership Checks
- **Current State**: FileRepository ✅ complete (3 methods updated)
- **Target State**: UniversalListRepository 100% complete (4 methods need updates)
- **Dependencies**:
  - Database migration complete (owner_id columns exist)
  - FileRepository pattern established (optional owner_id parameter with conditional filtering)
- **User Data Risk**: LOW - This is adding authorization checks, not modifying data
- **Infrastructure Verified**: YES - All required tables and columns exist

---

## Lead Developer's Analysis (Already Completed)

**UniversalListRepository Location**: `services/repositories/universal_list_repository.py`

**Methods Analysis**:

### ✅ ALREADY HAVE owner_id Validation:

- `get_lists_by_owner(owner_id, ...)` - Line 53
- `get_default_list(owner_id, ...)` - Line 75
- `search_lists_by_name(owner_id, ...)` - Line 158

### 🔧 NEED owner_id Validation Added (4 methods):

1. **`get_list_by_id(list_id)`** (Lines 39-43)

   - Currently: No owner_id check
   - Need: Add `owner_id: UUID` parameter, add `ListDB.owner_id == owner_id` to WHERE clause

2. **`update_list(list_id, updates)`** (Lines 102-110)

   - Currently: No owner_id check
   - Need: Add `owner_id: UUID` parameter, add `ListDB.owner_id == owner_id` to WHERE clause

3. **`delete_list(list_id)`** (Lines 142-150)

   - Currently: No owner_id check
   - Need: Add `owner_id: UUID` parameter, add `ListDB.owner_id == owner_id` to WHERE clause

4. **`update_item_counts(list_id)`** (Lines 112-140)
   - Currently: Calls `get_list_by_id` internally (will inherit fix automatically)
   - Need: Add `owner_id: UUID` parameter, pass to `get_list_by_id` call

---

## Implementation Pattern (Established in FileRepository)

**Pattern to follow** (from commit 1a41237e):

```python
# BEFORE (vulnerable):
async def get_resource(self, resource_id: str) -> Optional[domain.Resource]:
    result = await self.session.execute(
        select(ResourceDB).where(ResourceDB.id == resource_id)
    )
    return result.scalar_one_or_none()

# AFTER (secure):
async def get_resource(self, resource_id: str, owner_id: UUID) -> Optional[domain.Resource]:
    """Get resource - verify ownership."""
    result = await self.session.execute(
        select(ResourceDB).where(
            ResourceDB.id == resource_id,
            ResourceDB.owner_id == owner_id  # ✅ ADD THIS
        )
    )
    db_resource = result.scalar_one_or_none()
    return db_resource.to_domain() if db_resource else None
```

**Key Points**:

- Add `owner_id: UUID` as required parameter
- Add `ResourceDB.owner_id == owner_id` to WHERE clause using `and_()` if needed
- Update docstring to mention ownership verification
- For `update()` statements, add to `.where()` clause
- For `delete()`, verify ownership before deletion

---

## Implementation Approach

### Step 1: Update `get_list_by_id` Method

**File**: `services/repositories/universal_list_repository.py` (Line 39)

**Changes**:

1. Add `owner_id: UUID` parameter to signature
2. Add `ListDB.owner_id == owner_id` to WHERE clause
3. Update docstring: "Get universal list by ID - verify ownership"

**Expected outcome**: Method signature includes `owner_id`, query filters by both `id` and `owner_id`

**Validation**:

```bash
# Verify signature change
grep -A 5 "async def get_list_by_id" services/repositories/universal_list_repository.py
```

**Evidence**: Show the updated method signature and WHERE clause

---

### Step 2: Update `update_list` Method

**File**: `services/repositories/universal_list_repository.py` (Line 102)

**Changes**:

1. Add `owner_id: UUID` parameter to signature
2. Add `ListDB.owner_id == owner_id` to WHERE clause (use `and_()` with existing condition)
3. Update docstring: "Update universal list - verify ownership"

**Expected outcome**: Update only succeeds if list belongs to owner

**Validation**:

```bash
# Verify signature change
grep -A 8 "async def update_list" services/repositories/universal_list_repository.py
```

**Evidence**: Show the updated WHERE clause with both conditions

---

### Step 3: Update `delete_list` Method

**File**: `services/repositories/universal_list_repository.py` (Line 142)

**Changes**:

1. Add `owner_id: UUID` parameter to signature
2. Add `ListDB.owner_id == owner_id` to WHERE clause in SELECT
3. Update docstring: "Delete a list - verify ownership (cascades to items)"

**Expected outcome**: Delete only succeeds if list belongs to owner

**Validation**:

```bash
# Verify signature change
grep -A 8 "async def delete_list" services/repositories/universal_list_repository.py
```

**Evidence**: Show the updated WHERE clause with ownership check

---

### Step 4: Update `update_item_counts` Method

**File**: `services/repositories/universal_list_repository.py` (Line 112)

**Changes**:

1. Add `owner_id: UUID` parameter to signature
2. Update call to `self.get_list_by_id(list_id, owner_id)` (pass owner_id)
3. Update docstring: "Update cached item counts - verify ownership"

**Expected outcome**: Item counts only updated if list belongs to owner

**Validation**:

```bash
# Verify signature change and call update
grep -A 15 "async def update_item_counts" services/repositories/universal_list_repository.py
```

**Evidence**: Show the updated method call with owner_id parameter

---

### Step 5: Find and Update All Callers

**CRITICAL**: All callers of these 4 methods must be updated to pass `owner_id`.

**Find callers**:

```bash
# Search for calls to these methods
grep -r "\.get_list_by_id(" services/ --include="*.py"
grep -r "\.update_list(" services/ --include="*.py"
grep -r "\.delete_list(" services/ --include="*.py"
grep -r "\.update_item_counts(" services/ --include="*.py"
```

**For each caller**:

1. Identify where `user_id` or `owner_id` is available in context
2. Update call to pass `owner_id` parameter
3. If `user_id` not available in caller, add it to caller's signature (cascade upward)

**Expected outcome**: All calls include `owner_id` parameter

**Validation**: Re-run grep searches, verify all calls have correct number of parameters

**Evidence**: Show grep results before/after, list all updated callers

---

### Step 6: Run Tests

**Verify no regressions**:

```bash
# Run universal list tests
pytest tests/unit/services/repositories/test_universal_list_repository.py -xvs

# Run broader service tests
pytest tests/unit/services/ -k "list" -x
```

**Expected outcome**: All tests pass (or failures are pre-existing and skipped)

**Evidence**: Show full pytest output with pass counts

**If tests fail**: STOP and report (do NOT rationalize as "minor" or "not critical")

---

### Step 7: Commit Changes

**After all changes and tests pass**:

```bash
./scripts/fix-newlines.sh
git add services/repositories/universal_list_repository.py
git add [any caller files]
git commit -m "feat(SEC-RBAC Phase 1.2): Add owner_id validation to UniversalListRepository

Added ownership verification to 4 methods:
- get_list_by_id: Added owner_id parameter and WHERE filter
- update_list: Added owner_id parameter and WHERE filter
- delete_list: Added owner_id parameter and WHERE filter
- update_item_counts: Added owner_id parameter, pass to get_list_by_id

Updated [N] callers to pass owner_id parameter.

Defense-in-depth: Service layer now prevents cross-user list access.

Part of SEC-RBAC #357 Phase 1.2 Service Layer Ownership Checks.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Evidence**: Show `git log --oneline -1` and `git diff HEAD~1` output

---

## Success Criteria (With Evidence)

- [ ] All 4 methods updated with owner_id validation (show grep results)
- [ ] All callers updated to pass owner_id (show grep results showing no missing params)
- [ ] All tests pass (show pytest output)
- [ ] Changes committed (show `git log --oneline -1`)
- [ ] No user data lost (not applicable - authorization only)
- [ ] Evidence provided for each step (terminal outputs below)

---

## Deliverables

1. **Code Changes**: `services/repositories/universal_list_repository.py` + caller files
2. **Completeness**: 4/4 methods = 100% of UniversalListRepository CRUD methods secured
3. **Test Evidence**: Pytest output showing passes
4. **Caller Update Evidence**: Grep results showing all callers updated
5. **Git Commit**: Clean commit with descriptive message
6. **Report to Lead Dev**: Summary of work completed for session log

---

## STOP Conditions

If ANY of these occur, STOP and report to Lead Dev (PM will relay):

- [ ] Tests fail for any reason
- [ ] Can't find where user_id/owner_id is available in caller context
- [ ] Caller signature changes would break endpoint contracts
- [ ] Database query patterns don't match FileRepository example
- [ ] Git operations fail
- [ ] Any uncertainty about implementation approach

---

## Evidence Report Template

When complete, provide this evidence:

```markdown
## SEC-RBAC Phase 1.2: UniversalListRepository Complete

### Methods Updated (4/4 = 100%)

1. ✅ get_list_by_id - owner_id validation added
2. ✅ update_list - owner_id validation added
3. ✅ delete_list - owner_id validation added
4. ✅ update_item_counts - owner_id parameter added

### Signature Changes

[paste grep results showing new signatures]

### Callers Updated ([N] total)

[list each caller file and what was changed]

### Test Results

[paste pytest output]

### Git Commit

[paste git log output]

### Ready for Next Repository

UniversalListRepository Phase 1.2 work complete.
Next target: TodoManagementService (verify existing user_id checks).
```

---

## Related Context

- **Gameplan**: `dev/active/gameplan-sec-rbac-implementation.md`
- **Progress Checkpoint**: `dev/2025/11/21/sec-rbac-phase-1-progress-checkpoint.md`
- **Previous Commits**:
  - 263ae02f (P0 fix)
  - 5d92d212 (Phase 1.1 migration)
  - 1a41237e (Phase 1.2 FileRepository - PATTERN ESTABLISHED HERE)
  - 512c760d (documentation)

---

## REMINDER: You're Continuing Ongoing Work

This is a continuation prompt after compaction. You have:

- ✅ Established the pattern (FileRepository commit 1a41237e)
- ✅ Working database schema (migration applied)
- ✅ Test suite health verified (95.6% pass rate)

Just apply the pattern to UniversalListRepository, then report completion.

Lead Developer is monitoring your progress and will provide the next continuation prompt.

---

_Prompt created by: Lead Developer (Cursor)_
_Date: November 21, 2025, 8:34 PM_
_For: Claude Code terminal agent_
_Session: SEC-RBAC Phase 1.2 Continuation_
