# Code Agent Prompt: CORE-ERROR-STANDARDS #215 - Phase 1

**Date**: October 15, 2025, 6:27 PM  
**Sprint**: A2 - Notion & Errors  
**Issue**: #215  
**Phase**: Phase 1 - Fix Intent Endpoint (Critical Path)  
**Duration**: 20-30 minutes  
**Agent**: Claude Code

---

## Mission

Fix the primary issue discovered in GREAT-5: The `/api/v1/intent` endpoint returns 200 with error JSON instead of proper HTTP status codes. Update it to use the new error utility functions from Phase 0.

**Context**: Phase 0 complete - error utility module tested and ready. Intent endpoint is the most critical endpoint (core functionality). Fix it first, validate thoroughly.

**Philosophy**: "Fix the most important thing first."

---

## Phase 0 Results (Foundation Ready!)

**Utility Module**: `web/utils/error_responses.py` ✅
- Functions: `validation_error()`, `bad_request_error()`, `internal_error()`, `not_found_error()`
- Tests: All 12 passing ✅
- Ready to use!

**Standards**: Pattern 034 documented ✅
- 200: Success only
- 400: Bad request (malformed syntax)
- 422: Validation error (semantic issues)
- 500: Internal error

---

## Step 1: Understand Current Intent Endpoint (5 min)

### Find the endpoint in web/app.py

```bash
# Find the intent endpoint
grep -n "@app.post.*intent" web/app.py -A 50

# Document current implementation
```

**Expected to find**:
- Line with `@app.post("/api/v1/intent")`
- Function definition: `async def process_intent(...)` or similar
- Error handling: `return {"status": "error", "error": str(e)}`

**Document in notes**: Current line numbers and structure

---

## Step 2: Update Intent Endpoint (10 min)

### Add import at top of web/app.py

**Find the imports section** (top of file):
```bash
head -30 web/app.py | grep -n "import"
```

**Add new import**:
```python
from web.utils.error_responses import validation_error, internal_error
```

**Location**: After other `from web.*` imports

### Update error handling in intent endpoint

**Current pattern** (example):
```python
@app.post("/api/v1/intent")
async def process_intent(request: dict):
    try:
        if not request.get("intent"):
            return {"status": "error", "error": "Intent required"}  # ❌ Returns 200!
        
        # ... process intent ...
        
    except Exception as e:
        return {"status": "error", "error": str(e)}  # ❌ Returns 200!
```

**New pattern**:
```python
@app.post("/api/v1/intent")
async def process_intent(request: dict):
    try:
        if not request.get("intent"):
            return validation_error(
                "Intent required",
                {"field": "intent", "issue": "Cannot be empty"}
            )  # ✅ Returns 422!
        
        # ... process intent ...
        
    except ValueError as e:
        # Known validation issues
        return validation_error(str(e))  # ✅ Returns 422!
    except Exception as e:
        # Unexpected errors
        logger.error(f"Unexpected error processing intent: {e}", exc_info=True)
        return internal_error()  # ✅ Returns 500!
```

**Key changes**:
1. ✅ Empty intent → `validation_error()` with field details
2. ✅ ValueError → `validation_error()` (semantic issues)
3. ✅ Unexpected Exception → `internal_error()` with logging
4. ✅ All return proper HTTP status codes

### Use str_replace for clean updates

```python
# Find exact old code
grep -n "def.*intent" web/app.py -A 30

# Use str_replace to update (if exact match found)
# Otherwise manually edit with care
```

---

## Step 3: Test Intent Endpoint Manually (5 min)

### Start the server

```bash
# Kill any existing server
pkill -f "python.*main.py" || true

# Start server
python main.py &

# Wait for startup
sleep 3

# Check it's running
curl http://localhost:8001/health
```

### Test invalid intent (should return 422)

```bash
# Test 1: Empty intent
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": ""}' \
  -w "\nHTTP Status: %{http_code}\n"

# Expected:
# HTTP Status: 422
# {"status":"error","code":"VALIDATION_ERROR",...}

# Test 2: Missing intent field
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"other": "data"}' \
  -w "\nHTTP Status: %{http_code}\n"

# Expected:
# HTTP Status: 422
# {"status":"error","code":"VALIDATION_ERROR",...}

# Test 3: Invalid JSON (should return 400)
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d 'invalid json' \
  -w "\nHTTP Status: %{http_code}\n"

# Expected:
# HTTP Status: 400 or 422
# {"status":"error",...}
```

**Document results** in `/tmp/intent-endpoint-test-results.txt`

### Test valid intent (should still work!)

```bash
# Test 4: Valid intent
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": "show me the standup"}' \
  -w "\nHTTP Status: %{http_code}\n"

# Expected:
# HTTP Status: 200
# Success response (functionality unchanged)
```

**CRITICAL**: Valid requests must still work! No regressions!

---

## Step 4: Update Intent Endpoint Tests (10 min)

### Find existing intent tests

```bash
# Find test files
find tests/ -name "*intent*" -type f

# If found, check for error assertions
grep -r "status_code.*200.*error\|assert.*error.*200" tests/ --include="*intent*"
```

**If tests exist**:

**Old test pattern**:
```python
def test_intent_validation_error():
    response = client.post("/api/v1/intent", json={})
    assert response.status_code == 200  # ❌ Wrong!
    assert response.json()["status"] == "error"
```

**New test pattern**:
```python
def test_intent_validation_error():
    response = client.post("/api/v1/intent", json={})
    assert response.status_code == 422  # ✅ Correct!
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == "VALIDATION_ERROR"
```

**Update ALL tests** checking error status codes

**If no tests exist**:
Create basic test file: `tests/web/test_intent_endpoint.py`

```python
"""Tests for intent endpoint error handling."""

from fastapi.testclient import TestClient
from web.app import app

client = TestClient(app)


def test_intent_endpoint_empty_intent():
    """Test that empty intent returns 422."""
    response = client.post("/api/v1/intent", json={"intent": ""})
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == "VALIDATION_ERROR"


def test_intent_endpoint_missing_intent():
    """Test that missing intent returns 422."""
    response = client.post("/api/v1/intent", json={"other": "data"})
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"


def test_intent_endpoint_valid_intent():
    """Test that valid intent still works (no regression)."""
    response = client.post(
        "/api/v1/intent",
        json={"intent": "show me the standup"}
    )
    # Should be 200 (or whatever success code is)
    assert response.status_code in [200, 201, 202]
    # Should not be an error
    data = response.json()
    assert data.get("status") != "error"
```

### Run tests

```bash
# Run intent tests specifically
pytest tests/ -k "intent" -v

# Or run all tests
pytest tests/ -v

# Expected: All tests pass
```

**Document**: Test results in session log

---

## Step 5: Verify No Regressions (5 min)

### Quick health check

```bash
# Health endpoint should still work
curl http://localhost:8001/health

# Check other endpoints still work
curl http://localhost:8001/

# Stop test server
pkill -f "python.*main.py"
```

### Run full test suite

```bash
# Run all tests to ensure no breakage
pytest tests/ --tb=short

# Expected: Same pass rate as before (or better)
```

**Document**: Any test failures or regressions

---

## Step 6: Commit Changes (5 min)

### Use the new commit script!

```bash
# The improved pre-commit routine from today!
./scripts/commit.sh "feat(api): fix intent endpoint to return proper HTTP status codes

Changes:
- Import error utility functions
- Update empty/missing intent to return 422 (not 200)
- Add proper exception handling with 500 for unexpected errors
- Update tests to expect correct status codes
- Validate with manual curl tests

Before: Invalid intent returned 200 with error JSON (not REST-compliant)
After: Invalid intent returns 422 with validation error (REST-compliant)

Part of: CORE-ERROR-STANDARDS #215, Phase 1
Sprint: A2"
```

**Or if script doesn't work**:
```bash
./scripts/fix-newlines.sh
git add -u
git commit -m "feat(api): fix intent endpoint to return proper HTTP status codes"
git push origin main
```

---

## Step 7: Update Session Log (3 min)

Add to your session log:

```markdown
## Phase 1: Fix Intent Endpoint - COMPLETE

**Duration**: [actual time]  
**Started**: 6:30 PM  
**Completed**: [time]

### What Changed

**File**: `web/app.py`
- Added import: `from web.utils.error_responses import validation_error, internal_error`
- Updated intent endpoint error handling
- Empty intent → 422 validation error
- Unexpected errors → 500 internal error with logging

### Testing

**Manual Tests**:
- ✅ Empty intent: Returns 422
- ✅ Missing intent: Returns 422
- ✅ Valid intent: Returns 200 (no regression)

**Automated Tests**:
- Tests updated: [count]
- Tests passing: [count]/[count]
- No regressions detected

### Evidence

**curl test results**: /tmp/intent-endpoint-test-results.txt
**pytest output**: [pass/fail counts]

### Impact

**Before**: Intent endpoint returned 200 with error JSON (not REST-compliant)
**After**: Intent endpoint returns 422 for validation errors (REST-compliant)

**Breaking Change**: Yes - clients must check status_code
**Backward Compatible**: Error response format unchanged

### Next Steps

**Tomorrow - Phase 2**: Update remaining 19 endpoints
**Tomorrow - Phase 3**: Update all endpoint tests
**Tomorrow - Phase 4**: Complete documentation

---

**Phase 1 Status**: ✅ COMPLETE
```

---

## Deliverables Phase 1

When complete, you should have:

- [ ] Intent endpoint updated in `web/app.py`
- [ ] Error utilities imported
- [ ] Manual tests documented (422 for errors, 200 for success)
- [ ] Automated tests updated/created
- [ ] All tests passing
- [ ] Changes committed
- [ ] Session log updated

---

## Success Criteria

**Phase 1 is complete when**:
- ✅ Intent endpoint returns 422 for validation errors (not 200)
- ✅ Intent endpoint returns 500 for unexpected errors (not 200)
- ✅ Valid intents still work (no regression)
- ✅ Tests updated and passing
- ✅ Changes committed

---

## Time Budget

**Target**: 20-30 minutes

- Understand current: 5 min
- Update endpoint: 10 min
- Manual testing: 5 min
- Update tests: 10 min (if exist)
- Verify no regressions: 5 min
- Commit: 5 min
- Session log: 3 min

**Total**: ~33 minutes (realistic)

---

## What NOT to Do

- ❌ Don't update other endpoints yet (that's Phase 2)
- ❌ Don't update all tests yet (just intent tests)
- ❌ Don't write documentation yet (that's Phase 4)
- ❌ Don't break valid intent functionality

## What TO Do

- ✅ Focus ONLY on intent endpoint
- ✅ Use the error utilities from Phase 0
- ✅ Test thoroughly (manual + automated)
- ✅ Verify no regressions
- ✅ Use the new commit script!

---

## STOP Conditions

Stop and escalate if:

- Intent endpoint functionality breaks
- Valid intents stop working
- Tests fail catastrophically
- Server won't start

---

**Phase 1 Start**: 6:30 PM  
**Expected Done**: ~7:00 PM (30 minutes)  
**Status**: Ready to fix the critical path!

**GO MAKE INTENT ENDPOINT REST-COMPLIANT!** ⚡

---

*"Fix the most important thing first, then iterate."*  
*- Phase 1 Philosophy*
