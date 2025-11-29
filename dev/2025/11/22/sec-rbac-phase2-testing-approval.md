# SEC-RBAC Phase 2: Testing Approval

**Date**: November 22, 2025, 11:12 AM
**From**: PM (via Lead Developer)
**To**: Code Agent
**Re**: Phase 2 Testing - Approval to Proceed

---

## Implementation Review: ✅ EXCELLENT PROGRESS

You've completed Steps 1-5 ahead of schedule! Migration, domain models, repository methods, API endpoints, and access queries are all done. Great work following the PM approval guidance.

---

## Phase 4 Testing: ✅ APPROVED TO PROCEED

**Your Task**: Create comprehensive testing covering all role-based permission scenarios.

---

## Testing Strategy

### Part 1: Manual Test Script (Priority)

**File**: `tests/manual/manual_rbac_phase2_role_permissions.py`

**Purpose**: Exercise all 24 test cases from the access control matrix to verify role-based permissions work correctly.

**Test Coverage**:

```python
# Test matrix: 4 roles × 6 operations = 24 test cases

Roles to test:
- Owner (full permissions)
- Admin (can share, can't delete)
- Editor (can modify, can't share/delete)
- Viewer (read-only)

Operations to test:
1. Read resource (list/todo)
2. Update resource (modify content)
3. Delete resource
4. Share with new user
5. Unshare existing user
6. Change user's role
```

**Expected Results by Role**:

| Operation | Owner | Admin | Editor | Viewer |
|-----------|-------|-------|--------|--------|
| Read | ✅ 200 | ✅ 200 | ✅ 200 | ✅ 200 |
| Update | ✅ 200 | ✅ 200 | ✅ 200 | ❌ 404 |
| Delete | ✅ 200 | ❌ 404 | ❌ 404 | ❌ 404 |
| Share | ✅ 200 | ✅ 200 | ❌ 404 | ❌ 404 |
| Unshare | ✅ 200 | ✅ 200 | ❌ 404 | ❌ 404 |
| Change Role | ✅ 200 | ✅ 200 | ❌ 404 | ❌ 404 |

**Script Structure**:

```python
#!/usr/bin/env python3
"""
Manual test script for SEC-RBAC Phase 2 role-based permissions.

Tests all 24 role × operation combinations:
- Owner: Full permissions (all operations succeed)
- Admin: Can share but can't delete
- Editor: Can modify but can't share/delete
- Viewer: Read-only (can't modify/delete/share)

Run: python tests/manual/manual_rbac_phase2_role_permissions.py
"""

import asyncio
import httpx
from dotenv import load_dotenv
import os

BASE_URL = "http://localhost:8001"

async def test_role_permissions():
    """Test all role-based permission combinations"""

    load_dotenv()

    # Setup: Create 4 users (owner, admin, editor, viewer)
    owner_token = await create_test_user("owner@test.com")
    admin_token = await create_test_user("admin@test.com")
    editor_token = await create_test_user("editor@test.com")
    viewer_token = await create_test_user("viewer@test.com")

    # Create test list as owner
    list_id = await create_list_as_owner(owner_token)

    # Share with admin, editor, viewer at appropriate roles
    await share_list(owner_token, list_id, admin_user_id, "admin")
    await share_list(owner_token, list_id, editor_user_id, "editor")
    await share_list(owner_token, list_id, viewer_user_id, "viewer")

    # Test all 24 combinations
    results = []

    # Test Owner (should succeed on all)
    results.append(await test_read(owner_token, list_id, expected=200))
    results.append(await test_update(owner_token, list_id, expected=200))
    results.append(await test_delete(owner_token, list_id, expected=200))
    # ... etc

    # Test Admin (should succeed except delete)
    results.append(await test_read(admin_token, list_id, expected=200))
    results.append(await test_update(admin_token, list_id, expected=200))
    results.append(await test_delete(admin_token, list_id, expected=404))
    # ... etc

    # Test Editor (should succeed only read/update)
    results.append(await test_read(editor_token, list_id, expected=200))
    results.append(await test_update(editor_token, list_id, expected=200))
    results.append(await test_delete(editor_token, list_id, expected=404))
    results.append(await test_share(editor_token, list_id, expected=404))
    # ... etc

    # Test Viewer (should succeed only read)
    results.append(await test_read(viewer_token, list_id, expected=200))
    results.append(await test_update(viewer_token, list_id, expected=404))
    results.append(await test_delete(viewer_token, list_id, expected=404))
    # ... etc

    # Summary
    passed = sum(results)
    total = len(results)
    print(f"\n{'='*60}")
    print(f"RBAC Phase 2 Manual Test Results: {passed}/{total} passed")
    print(f"{'='*60}\n")

    if passed == total:
        print("✅ ALL TESTS PASSED - Role-based permissions working correctly!")
        return 0
    else:
        print(f"❌ {total - passed} TESTS FAILED - Review failures above")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(test_role_permissions())
    exit(exit_code)
```

**Key Test Scenarios**:

1. **Role Escalation Prevention**:
   - Admin cannot upgrade themselves to owner
   - Editor cannot upgrade themselves to admin
   - Viewer cannot upgrade themselves to editor

2. **Information Leakage Prevention**:
   - Non-shared users get 404 (not 403)
   - Viewer gets 404 when attempting operations (not "permission denied")

3. **Atomic Operations**:
   - Concurrent role changes don't corrupt JSONB
   - Unsharing user removes them completely

4. **Migration Verification**:
   - Old format `["uuid"]` converts to `[{"user_id": "uuid", "role": "viewer"}]`
   - New format `[{...}]` unchanged after migration

---

### Part 2: Integration Tests (Lower Priority)

**File**: `tests/integration/test_rbac_role_permissions.py`

**Purpose**: Automated tests that run in CI/CD pipeline.

**Test Coverage**:

```python
import pytest
from services.domain.models import ShareRole

@pytest.mark.asyncio
async def test_share_list_with_viewer_role(async_transaction):
    """Test sharing list with viewer role"""
    # Setup
    owner_id = "owner-uuid"
    viewer_id = "viewer-uuid"
    list_id = await create_test_list(owner_id)

    # Share with viewer role
    result = await list_repo.share_list(
        list_id, owner_id, viewer_id, ShareRole.VIEWER
    )

    # Verify
    assert result is not None
    assert viewer_id in [s["user_id"] for s in result.shared_with]
    assert result.shared_with[0]["role"] == "viewer"

@pytest.mark.asyncio
async def test_editor_cannot_delete(async_transaction):
    """Test that editor role cannot delete list"""
    # Setup: Create list, share with editor
    editor_id = "editor-uuid"
    list_id = await create_shared_list(editor_id, ShareRole.EDITOR)

    # Attempt delete as editor
    result = await list_repo.delete_list(list_id, editor_id)

    # Verify: Should fail (None returned)
    assert result is None

@pytest.mark.asyncio
async def test_admin_can_share(async_transaction):
    """Test that admin role can share with new users"""
    # Setup: Create list, share with admin
    admin_id = "admin-uuid"
    list_id = await create_shared_list(admin_id, ShareRole.ADMIN)

    # Admin shares with new user
    new_user_id = "new-user-uuid"
    result = await list_repo.share_list(
        list_id, admin_id, new_user_id, ShareRole.VIEWER
    )

    # Verify: Should succeed
    assert result is not None
    assert new_user_id in [s["user_id"] for s in result.shared_with]

@pytest.mark.asyncio
async def test_update_share_role_transition(async_transaction):
    """Test role transitions (viewer → editor → admin)"""
    # Setup
    user_id = "user-uuid"
    list_id = await create_shared_list(user_id, ShareRole.VIEWER)

    # Upgrade viewer → editor
    result = await list_repo.update_share_role(
        list_id, owner_id, user_id, ShareRole.EDITOR
    )
    assert result is True

    # Verify role changed
    role = await list_repo.get_user_role(list_id, user_id)
    assert role == "editor"

    # Upgrade editor → admin
    result = await list_repo.update_share_role(
        list_id, owner_id, user_id, ShareRole.ADMIN
    )
    assert result is True

    # Verify role changed
    role = await list_repo.get_user_role(list_id, user_id)
    assert role == "admin"

@pytest.mark.asyncio
async def test_migration_converts_old_format(async_transaction):
    """Test migration converts old shared_with format correctly"""
    # Setup: Insert old format directly
    await db.execute("""
        INSERT INTO lists (id, owner_id, shared_with)
        VALUES ('test-id', 'owner-id', '["user1", "user2"]'::jsonb)
    """)

    # Run migration (or migration function)
    await run_shared_with_migration()

    # Verify conversion
    result = await db.fetch_one(
        "SELECT shared_with FROM lists WHERE id = 'test-id'"
    )

    shared_with = result["shared_with"]
    assert len(shared_with) == 2
    assert shared_with[0] == {"user_id": "user1", "role": "viewer"}
    assert shared_with[1] == {"user_id": "user2", "role": "viewer"}
```

**Test Priority**:
1. Share with each role type (viewer, editor, admin)
2. Access control enforcement per role
3. Role transitions (upgrade/downgrade)
4. Migration correctness
5. JSONB query performance (optional)

---

## Testing Workflow

### Step 1: Manual Test Script
```bash
# Create the manual test script
# File: tests/manual/manual_rbac_phase2_role_permissions.py

# Run it
python tests/manual/manual_rbac_phase2_role_permissions.py
```

**Expected Output**:
```
Testing Owner Role (6 operations)...
  ✅ Read: 200 OK
  ✅ Update: 200 OK
  ✅ Delete: 200 OK
  ✅ Share: 200 OK
  ✅ Unshare: 200 OK
  ✅ Change Role: 200 OK

Testing Admin Role (6 operations)...
  ✅ Read: 200 OK
  ✅ Update: 200 OK
  ❌ Delete: 404 Not Found (expected)
  ✅ Share: 200 OK
  ✅ Unshare: 200 OK
  ✅ Change Role: 200 OK

Testing Editor Role (6 operations)...
  ✅ Read: 200 OK
  ✅ Update: 200 OK
  ❌ Delete: 404 Not Found (expected)
  ❌ Share: 404 Not Found (expected)
  ❌ Unshare: 404 Not Found (expected)
  ❌ Change Role: 404 Not Found (expected)

Testing Viewer Role (6 operations)...
  ✅ Read: 200 OK
  ❌ Update: 404 Not Found (expected)
  ❌ Delete: 404 Not Found (expected)
  ❌ Share: 404 Not Found (expected)
  ❌ Unshare: 404 Not Found (expected)
  ❌ Change Role: 404 Not Found (expected)

============================================================
RBAC Phase 2 Manual Test Results: 24/24 passed
============================================================

✅ ALL TESTS PASSED - Role-based permissions working correctly!
```

### Step 2: Integration Tests (Optional)
```bash
# Create integration tests (if time permits)
# File: tests/integration/test_rbac_role_permissions.py

# Run them
pytest tests/integration/test_rbac_role_permissions.py -v
```

### Step 3: Full Test Suite
```bash
# Run all tests to ensure no regressions
pytest tests/ -v

# Should show:
# - All existing tests still passing
# - New RBAC tests passing
# - No unexpected failures
```

---

## Acceptance Criteria

**Manual Testing**:
- ✅ Manual test script created
- ✅ All 24 role × operation combinations tested
- ✅ Script output shows expected results
- ✅ Owner has full permissions
- ✅ Admin can share but not delete
- ✅ Editor can modify but not share/delete
- ✅ Viewer can only read

**Integration Testing** (optional but recommended):
- ✅ Share with each role type works
- ✅ Role transitions work (viewer → editor → admin)
- ✅ Access control enforced per role
- ✅ Migration converts old format correctly

**Regression Testing**:
- ✅ All existing tests still pass
- ✅ No new test failures introduced

---

## What to Do If Tests Fail

**If Manual Tests Fail**:
1. Document exact failure (which role, which operation, actual vs expected)
2. Check repository method implementation
3. Check API endpoint access control logic
4. Check JSONB query patterns
5. Fix issue
6. Re-run manual tests
7. Document fix in completion report

**If Integration Tests Fail**:
1. Same debugging process as manual tests
2. May need to adjust test setup (async_transaction fixture, etc.)
3. Verify database state after each test

**If Existing Tests Fail**:
1. STOP immediately
2. Identify which test broke
3. Determine if Phase 2 changes caused regression
4. Fix regression OR document as known issue
5. Do NOT proceed to Phase 5 until resolved

---

## Timeline Guidance

**Manual Test Script**: 30-45 minutes
- 15 min: Script structure and setup
- 15 min: Implement 24 test cases
- 10 min: Run and verify results

**Integration Tests**: 30-45 minutes (if creating them)
- 15 min: Test file setup
- 20 min: Implement 5-7 key test cases
- 10 min: Run and verify

**Total Testing Phase**: 1-1.5 hours

---

## After Testing Complete

Once testing is done:

1. **Create Phase 2 Completion Report**
   - File: `dev/2025/11/22/sec-rbac-phase2-completion-report.md`
   - Include: Test results, files changed, acceptance criteria met
   - Evidence: Manual test output, pytest output

2. **Update Session Log**
   - Document testing results
   - Note any issues found and fixed
   - Confirm Phase 2 complete

3. **Signal Completion**
   - Report back to PM/Lead Dev
   - Ready for Phase 3 (if any) or mark SEC-RBAC complete

---

## Approval Summary

✅ **Approved to proceed with Phase 2 Testing (Phase 4)**

**Priority**:
1. **HIGH**: Manual test script (required)
2. **MEDIUM**: Integration tests (recommended)
3. **LOW**: Additional edge case tests (nice-to-have)

**Success Criteria**:
- Manual test script runs successfully
- All 24 test cases pass with expected results
- No regressions in existing test suite

**Estimated Time**: 1-1.5 hours

---

## Authorization

**Approved by**: PM (xian) via Lead Developer
**Date**: November 22, 2025, 11:12 AM
**Authority**: Testing phase approval for Phase 2

**You are cleared to proceed with testing.**

Good luck! 🧪

---

_Testing approval provided by: Lead Developer (Claude Sonnet)_
_Time: 11:12 AM, November 22, 2025_
