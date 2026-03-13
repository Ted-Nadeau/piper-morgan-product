# Code Agent Prompt: Phase 3 - Update Tests for New Error Codes

**Date**: October 16, 2025, 1:40 PM
**Sprint**: A2 - Notion & Errors (Day 2)
**Issue**: CORE-ERROR-STANDARDS #215
**Phase**: Phase 3 - Test Updates
**Duration**: 45-60 minutes (likely faster!)
**Agent**: Claude Code

---

## Mission

Update all tests to expect proper HTTP status codes (422, 404, 500) instead of 200 for errors. With Phase 2 complete, endpoints now return REST-compliant codes - tests need to match!

**Context**: Phase 2 updated all endpoints to Pattern 034. Tests still expect old behavior (200 with error body). Need to update expectations to match new reality.

**Philosophy**: "Tests validate reality, not old assumptions."

---

## What We've Accomplished

### Phase 2 ✅ (Just Completed!)
- All 15+ endpoints now REST-compliant
- Validation errors → 422
- Not found → 404
- Internal errors → 500
- Valid requests → 200

### Phase 3 ← **WE ARE HERE**
- Update test expectations
- Validate error response format
- Ensure 100% test pass rate

---

## Step 1: Find Tests Needing Updates (10 min)

### Search for old patterns

**Use Serena to find**:
```bash
# Pattern 1: Tests checking status_code == 200 with errors
# Pattern 2: Tests checking error responses without status validation
# Pattern 3: Tests for specific endpoints we updated
```

**Search patterns**:
```python
# Old pattern 1: Expects 200 with error
assert response.status_code == 200
assert "error" in response.json()

# Old pattern 2: Expects 200, checks error status
assert response.status_code == 200
assert response.json()["status"] == "error"

# Old pattern 3: No status code check at all
result = client.post(...)
assert result.json()["status"] == "error"
```

### Create audit report

**File**: `dev/active/phase-3-test-audit.md`

```markdown
# Phase 3 - Test Audit

**Date**: October 16, 2025, 1:45 PM
**Purpose**: Find all tests expecting old error behavior

---

## Summary

**Test Files Found**: [count]
**Tests Needing Updates**: [count]
**Test Categories**:
- Intent endpoint tests
- Workflow endpoint tests
- Personality endpoint tests
- Admin endpoint tests
- Integration tests

---

## Tests by File

### tests/web/test_intent_endpoint.py
**Line [X]**: test_intent_empty
```python
assert response.status_code == 200  # ❌ Should be 422
assert response.json()["status"] == "error"
```

**Line [Y]**: test_intent_missing
```python
assert response.status_code == 200  # ❌ Should be 422
```

---

### tests/web/test_workflow_endpoints.py
[Repeat for each test file]

---

## Migration Priority

### High Priority (Blocking CI)
1. Intent endpoint tests
2. Workflow endpoint tests
3. [Tests that run in CI]

### Medium Priority
[Tests that exist but may not be in CI]

### Low Priority
[Deprecated or example tests]

---

**Total Tests to Update**: [count]
```

---

## Step 2: Update Intent Endpoint Tests (15 min)

### Find intent tests

**Likely location**: `tests/web/test_intent_endpoint.py` or similar

### Old pattern

```python
def test_intent_endpoint_empty_intent():
    """Test that empty intent returns error."""
    response = client.post("/api/v1/intent", json={"intent": ""})

    assert response.status_code == 200  # ❌ Old behavior
    data = response.json()
    assert data["status"] == "error"
    assert "intent" in data["error"].lower()
```

### New pattern

```python
def test_intent_endpoint_empty_intent():
    """Test that empty intent returns 422 validation error."""
    response = client.post("/api/v1/intent", json={"intent": ""})

    # Expect 422 Validation Error
    assert response.status_code == 422  # ✅ REST-compliant

    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == "VALIDATION_ERROR"
    assert "intent" in data["message"].lower() or (
        "details" in data and "intent" in str(data["details"]).lower()
    )
```

### Additional test patterns

**Test for 404 Not Found**:
```python
def test_workflow_not_found():
    """Test that nonexistent workflow returns 404."""
    response = client.get("/api/v1/workflows/nonexistent-id")

    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == "NOT_FOUND"
```

**Test for 500 Internal Error**:
```python
def test_internal_error(mocker):
    """Test that unexpected errors return 500."""
    # Mock to raise exception
    mocker.patch('services.some_service.method', side_effect=Exception("Boom"))

    response = client.post("/api/v1/intent", json={"intent": "test"})

    assert response.status_code == 500
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == "INTERNAL_ERROR"
    # Should NOT expose internal details
    assert "Boom" not in data.get("message", "")
```

**Test for 200 Success**:
```python
def test_intent_success():
    """Test that valid intent returns 200."""
    response = client.post(
        "/api/v1/intent",
        json={"intent": "show me the standup"}
    )

    # Valid request should succeed
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"  # or similar success indicator
```

---

## Step 3: Update Workflow Tests (10 min)

### Find workflow tests

**Search for**: Tests of workflow endpoints

### Apply same patterns

**For each test**:
1. Empty/invalid input → expect 422
2. Not found → expect 404
3. Internal error → expect 500
4. Valid request → expect 200

### Example updates

```python
# Test validation error
def test_workflow_missing_id():
    response = client.get("/api/v1/workflows/")
    assert response.status_code == 404  # or 422, depending on implementation

# Test not found
def test_workflow_invalid_id():
    response = client.get("/api/v1/workflows/invalid")
    assert response.status_code == 404

# Test success
def test_workflow_valid_id():
    response = client.get("/api/v1/workflows/test-123")
    assert response.status_code in [200, 404]  # Depends on if exists
```

---

## Step 4: Update Personality Tests (10 min)

### Find personality tests

**Search for**: Tests of personality endpoints

### Apply same patterns

**Example**:
```python
def test_personality_profile_missing_user():
    response = client.get("/api/personality/profile/")
    assert response.status_code in [404, 422]

def test_personality_profile_invalid_user():
    response = client.get("/api/personality/profile/invalid")
    assert response.status_code == 404

def test_personality_enhance_empty():
    response = client.post("/api/personality/enhance", json={})
    assert response.status_code == 422
    data = response.json()
    assert data["code"] == "VALIDATION_ERROR"
```

---

## Step 5: Update Integration Tests (10 min)

### Find integration tests

**Look for**: Tests that test multiple endpoints or full flows

### Update expectations

**Example**:
```python
def test_full_intent_flow():
    """Test complete intent processing flow."""

    # 1. Invalid intent should fail with 422
    response = client.post("/api/v1/intent", json={"intent": ""})
    assert response.status_code == 422

    # 2. Valid intent should succeed with 200
    response = client.post(
        "/api/v1/intent",
        json={"intent": "show standup"}
    )
    assert response.status_code == 200
```

---

## Step 6: Run Test Suite (5 min)

### Run all tests

```bash
# Run full test suite
pytest tests/ -v

# Check for failures
pytest tests/ --tb=short -q

# Run with coverage (optional)
pytest tests/ --cov=web --cov=services --cov-report=term-missing
```

### Expected outcome

**Before updates**: Some tests failing (expecting 200, getting 422/404/500)
**After updates**: All tests passing ✅

### If tests fail

**Common issues**:
1. Test still expects 200
2. Test doesn't check error code field
3. Test checks wrong error format

**Fix systematically**:
- One test file at a time
- Run tests after each fix
- Document any issues

---

## Step 7: Document Test Updates (5 min)

### Create test update report

**File**: `dev/active/phase-3-test-updates.md`

```markdown
# Phase 3 - Test Updates Report

**Date**: October 16, 2025
**Time**: [completion time]
**Duration**: [actual time]

---

## Summary

**Test Files Updated**: [count]
**Tests Updated**: [count]
**Test Suite Status**: ✅ All Passing / ❌ [X] Failing

---

## Tests Updated by Category

### Intent Endpoint Tests
**File**: tests/web/test_intent_endpoint.py
**Tests Updated**: [count]
- test_intent_empty: 200 → 422
- test_intent_missing: 200 → 422
- test_intent_success: Verified 200
- [others]

### Workflow Tests
**File**: tests/web/test_workflow_endpoints.py
**Tests Updated**: [count]
- test_workflow_not_found: 200 → 404
- test_workflow_invalid: 200 → 422
- [others]

### Personality Tests
**File**: tests/web/test_personality_endpoints.py
**Tests Updated**: [count]
- [list tests]

### Integration Tests
**File**: tests/integration/test_api_integration.py
**Tests Updated**: [count]
- [list tests]

---

## Test Results

```bash
$ pytest tests/ -v
```

[Paste results]

**Total Tests**: [X]
**Passed**: [X]
**Failed**: [X]
**Skipped**: [X]

---

## Changes Made

### Pattern 1: Validation Errors
**Before**:
```python
assert response.status_code == 200
assert response.json()["status"] == "error"
```

**After**:
```python
assert response.status_code == 422
assert response.json()["code"] == "VALIDATION_ERROR"
```

### Pattern 2: Not Found
**Before**:
```python
assert response.status_code == 200
assert "not found" in response.json()["error"]
```

**After**:
```python
assert response.status_code == 404
assert response.json()["code"] == "NOT_FOUND"
```

### Pattern 3: Internal Errors
**Added**:
```python
assert response.status_code == 500
assert response.json()["code"] == "INTERNAL_ERROR"
assert "error_id" in response.json()["details"]
```

---

## Backward Compatibility

**Response Format**: Unchanged ✅
- Still returns `{"status": "error", ...}`
- Added `"code"` field
- Breaking change: HTTP status codes

**Impact on Clients**:
- Must check `response.status_code`
- Can still check `response.json()["status"]`
- Better: Use standard HTTP status handling

---

**Phase 3 Complete**: [time]
**Ready for Phase 4**: ✅ YES
```

---

## Step 8: Commit Changes (5 min)

### Commit test updates

```bash
./scripts/commit.sh "test(#215): Phase 3 - update tests for REST-compliant error codes

Updated test expectations to match Phase 2 endpoint changes:

Changed Expectations:
- Validation errors: 200 → 422
- Not found: 200 → 404
- Internal errors: 200 → 500
- Success: Still 200

Tests Updated:
- Intent endpoint tests: [count]
- Workflow endpoint tests: [count]
- Personality endpoint tests: [count]
- Integration tests: [count]

Test Results:
- Total: [X] tests
- Passing: [X] / [X]
- Status: ✅ All passing

Response Format:
- Backward compatible (still has 'status' field)
- Added 'code' field (VALIDATION_ERROR, NOT_FOUND, etc.)
- Breaking: HTTP status codes now correct

Part of: #215 Phase 3, Sprint A2
Duration: [actual time]"
```

---

## Deliverables Phase 3

When complete, you should have:

- [ ] Test audit completed (found all tests needing updates)
- [ ] Intent tests updated
- [ ] Workflow tests updated
- [ ] Personality tests updated
- [ ] Integration tests updated
- [ ] All tests passing (100%)
- [ ] Test update report documented
- [ ] Changes committed

---

## Success Criteria

**Phase 3 is complete when**:

- ✅ All tests expect correct HTTP status codes
- ✅ Tests validate error response format
- ✅ All tests passing (100%)
- ✅ No false positives (tests actually testing something)
- ✅ Documentation complete
- ✅ Changes committed

---

## Time Budget

**Target**: 45-60 minutes

- Test audit: 10 min
- Intent tests: 15 min
- Workflow tests: 10 min
- Personality tests: 10 min
- Integration tests: 10 min
- Run tests: 5 min
- Documentation: 5 min
- Commit: 5 min

**Total**: ~70 minutes (with buffer)

**Expected with current velocity**: 30-40 minutes! ⚡

---

## What NOT to Do

- ❌ Don't change test behavior (just expectations)
- ❌ Don't skip running tests
- ❌ Don't leave failing tests
- ❌ Don't create false positives

## What TO Do

- ✅ Update status code expectations
- ✅ Add error code validation
- ✅ Ensure all tests pass
- ✅ Document changes
- ✅ Run full test suite

---

## STOP Conditions

Stop and escalate if:

- Many tests failing unexpectedly
- Tests reveal actual bugs in endpoints
- Can't determine correct expectations
- Test coverage dropping significantly

---

**Phase 3 Start**: 1:45 PM
**Expected Done**: ~2:30 PM (45 min)
**With velocity**: ~2:15 PM (30 min)!
**Status**: Ready to align tests with reality!

**LET'S UPDATE THOSE TESTS!** 🧪

---

*"Tests should validate reality, not preserve old assumptions."*
*- Phase 3 Philosophy*
