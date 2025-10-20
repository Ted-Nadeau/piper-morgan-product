# Task 7: Integration Testing - Standup API

**Agent**: Claude Code (Programmer)
**Issue**: #162 (CORE-STAND-MODES-API)
**Task**: 7 of 7 - Integration Testing
**Sprint**: A4 "Standup Epic"
**Date**: October 20, 2025, 6:57 AM
**Estimated Effort**: Medium (60-90 minutes)

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

**DO NOT**:
- ❌ Read old context files to self-direct
- ❌ Assume you should continue
- ❌ Start working on next task without authorization

**This is critical**. After compaction, get your bearings first.

---

## CRITICAL: Testing Approach

**For API testing with JSON payloads**:

- ✅ **USE PYTHON** - requests library, pytest framework
- ❌ **NOT BASH** - JSON escaping is genuinely hard

**If you find yourself fighting bash/curl**:
- 🛑 STOP after 2 failed attempts
- 🐍 Switch to Python immediately
- 💬 Ask if unclear: "Should I use Python for this?"

**Bash + JSON = Python. Always.** (Lesson from Tasks 5 & 6)

---

## Mission

Create comprehensive integration tests that verify end-to-end workflows across multiple components, ensuring the standup API works correctly in realistic scenarios with real integrations, authentication, and data flow.

**Scope**:
- Create integration test suite (tests/integration/test_standup_integration.py)
- Test end-to-end workflows (request → response)
- Test with real API server (not mocked)
- Test authentication flow
- Test all 5 modes in integration
- Test all 4 formats in integration
- Test error handling end-to-end
- Verify actual integrations work

**NOT in scope**:
- Unit testing (Task 6 completed)
- Performance benchmarking
- Load testing
- UI testing

---

## Context

- **GitHub Issue**: #162 (CORE-STAND-MODES-API) - Multi-modal API
- **Current State**:
  - ✅ REST API endpoints created (Task 1)
  - ✅ Service integration complete (Task 2)
  - ✅ Authentication working (Task 3)
  - ✅ OpenAPI docs verified (Task 4)
  - ✅ Error handling verified (Task 5)
  - ✅ Unit tests passing (Task 6: 20/20 tests)
  - ✅ Architecture verified DDD-compliant
  - ❓ Integration tests needed
- **Target State**:
  - Complete integration test suite
  - All end-to-end workflows verified
  - Real integrations tested
  - Production-ready confidence
- **Dependencies**:
  - Running API server (port 8001)
  - pytest framework
  - Real integrations (GitHub, etc.)
- **User Data Risk**: Low - using test data
- **Infrastructure Verified**: Yes - API server operational

---

## STOP Conditions (EXPANDED TO 17)

If ANY of these occur, STOP and escalate to PM immediately:

1. **Infrastructure doesn't match gameplan** - API server not running on 8001
2. **Method implementation <100% complete** - All integration scenarios must work
3. **Pattern already exists in catalog** - Check existing integration test patterns
4. **Tests fail for any reason** - ALL tests must pass before claiming done
5. **Configuration assumptions needed** - Don't guess integration setup
6. **GitHub issue missing or unassigned** - Verify #162 still assigned
7. **Can't provide verification evidence** - Must show test results
8. **ADR conflicts with approach** - Check for testing ADRs
9. **Resource not found after searching** - Test files must be accessible
10. **User data at risk** - Ensure using test data only
11. **Completion bias detected** - Tests must actually pass
12. **Rationalizing gaps as "minor"** - All scenarios critical
13. **GitHub tracking not working** - Issue updates must work
14. **Single agent seems sufficient** - This IS single agent task
15. **Git operations failing** - All commits must work
16. **Server state unexpected** - API must be running and responsive
17. **Bash + JSON not working** - Switch to Python immediately

**Remember**: STOP means STOP. Don't try to work around it. Ask PM.

---

## Evidence Requirements (CRITICAL - EXPANDED)

### For EVERY Claim You Make:

- **"Integration tests pass"** → Show pytest output with all passing
- **"End-to-end workflow works"** → Show complete request/response cycle
- **"Mode X tested"** → Show integration test for that mode
- **"Format X tested"** → Show integration test for that format
- **"Authentication works"** → Show test with real JWT token
- **"Error handling works"** → Show integration error scenario tests

### Completion Bias Prevention (CRITICAL):

- **Never guess! Always verify first!**
- **NO "tests should pass"** - only "here's pytest output showing all passed"
- **NO "probably works"** - only "here's the integration test proving it"
- **NO assumptions** - only verified facts with pytest output
- **NO rushing to claim done** - all integration tests passing, then claim done

### Working Files Location (CRITICAL):

**NEVER use /tmp for important files**:
- ❌ /tmp - Can be lost between sessions
- ✅ dev/active/ - For working files, evidence
- ✅ tests/integration/ - For integration test files
- ✅ outputs/ - For final reports

**Save pytest output to**: dev/active/pytest-integration-output-task7.txt

### Testing Approach (CRITICAL):

**When testing API with JSON**:
- ✅ Use Python + requests library
- ✅ Use pytest framework
- ✅ Use real API server (not mocked)
- ❌ Do NOT use bash/curl scripts

**If stuck with testing approach**:
- 🛑 STOP and ask for help
- Don't spend >30 minutes on one approach
- Switch to different approach if not working

---

## Related Documentation

- **resource-map.md** - ALWAYS CHECK FIRST for test file locations
- **stop-conditions.md** - When to stop and ask for help
- **anti-80-pattern.md** - Understanding completion bias prevention
- **pytest docs** - https://docs.pytest.org/

---

## REMINDER: Methodology Cascade

This prompt carries our methodology forward. You are responsible for:

1. **Verifying infrastructure FIRST** (API server running on 8001)
2. **Ensuring 100% completeness** (no 80% pattern)
3. **Checking what exists NEXT** (integration tests may exist)
4. **Preserving user data ALWAYS** (use test data only)
5. **Checking resource-map.md FIRST** (for test locations)
6. **Following ALL verification requirements**
7. **Providing evidence for EVERY claim**
8. **Creating test scenario enumeration** (all scenarios tested)
9. **Stopping when assumptions are needed**
10. **Maintaining architectural integrity**
11. **Updating GitHub with progress** (in descriptions!)
12. **Creating session logs in .md format**
13. **Verifying git commits with log output**
14. **Using Python for API testing** (not bash!)
15. **Saving evidence to dev/active/** (not /tmp!)
16. **Never guessing - always verifying first!**
17. **Never rationalizing incompleteness!**

**Incomplete integration tests = unreliable API. Evidence is mandatory.**

---

## Task Requirements

### 1. Verify API Server Running

**Before starting integration tests**:

```bash
# Check if API server is running
curl -s http://localhost:8001/api/v1/standup/health

# Should return:
# {"status":"healthy","timestamp":"..."}

# If not running, start it:
# Terminal 1:
uvicorn main:app --reload --port 8001
```

**If server not running**: STOP (condition #1)

**If server on wrong port**: STOP (condition #1)

---

### 2. Review Existing Integration Tests

**Check if integration tests exist**:

```bash
# Check test directory
ls -la tests/integration/

# Check for standup integration tests
ls -la tests/integration/test_standup_integration.py
```

**If tests exist**: Review them first, don't overwrite

**If tests don't exist**: Create new file

---

### 3. Design Integration Test Structure

**Integration test organization**:

```python
# tests/integration/test_standup_integration.py

import pytest
import requests
import time
from services.auth.jwt_service import JWTService

# Integration tests use REAL API server
BASE_URL = "http://localhost:8001"

# Test structure:
# 1. Setup fixtures (API client, auth tokens)
# 2. End-to-end workflow tests
# 3. Multi-mode integration tests
# 4. Multi-format integration tests
# 5. Authentication integration tests
# 6. Error handling integration tests
# 7. Performance baseline tests
```

**Use real HTTP requests** to actual API server

---

### 4. Create Test Fixtures

**Essential fixtures**:

```python
import pytest
import requests
from services.auth.jwt_service import JWTService

@pytest.fixture(scope="module")
def base_url():
    """Base URL for API server"""
    return "http://localhost:8001"

@pytest.fixture(scope="module")
def api_client(base_url):
    """HTTP client for API requests"""
    # Verify server is running
    try:
        response = requests.get(f"{base_url}/api/v1/standup/health", timeout=5)
        assert response.status_code == 200
    except requests.exceptions.RequestException:
        pytest.skip("API server not running on port 8001")

    return requests.Session()

@pytest.fixture(scope="module")
def jwt_service():
    """JWT service for creating auth tokens"""
    return JWTService()

@pytest.fixture(scope="module")
def auth_token(jwt_service):
    """Valid authentication token"""
    return jwt_service.create_token({"sub": "test_user"})

@pytest.fixture(scope="module")
def auth_headers(auth_token):
    """Headers with authentication"""
    return {"Authorization": f"Bearer {auth_token}"}
```

---

### 5. Test End-to-End Workflows

**Complete request/response cycle tests**:

```python
def test_complete_standup_generation_workflow(api_client, base_url, auth_headers):
    """Test complete standup generation workflow end-to-end"""
    # 1. Generate standup
    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": "standard", "format": "json"},
        headers=auth_headers
    )

    # 2. Verify success
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "standup" in data
    assert "metadata" in data

    # 3. Verify standup structure
    standup = data["standup"]
    assert "yesterday" in standup or "accomplishments" in standup
    assert "today" in standup or "priorities" in standup
    assert "blockers" in standup

    # 4. Verify metadata
    metadata = data["metadata"]
    assert "mode" in metadata
    assert metadata["mode"] == "standard"
    assert "format" in metadata
    assert "generated_at" in metadata

    # 5. Verify performance (target <2s)
    assert metadata.get("generation_time_ms", 0) < 2000

def test_multi_step_workflow(api_client, base_url, auth_headers):
    """Test workflow with multiple API calls"""
    # 1. Check health
    health_response = api_client.get(f"{base_url}/api/v1/standup/health")
    assert health_response.status_code == 200

    # 2. Get available modes
    modes_response = api_client.get(f"{base_url}/api/v1/standup/modes")
    assert modes_response.status_code == 200
    modes = modes_response.json()["modes"]

    # 3. Generate standup for each mode
    for mode in ["standard", "issues", "documents"]:
        response = api_client.post(
            f"{base_url}/api/v1/standup/generate",
            json={"mode": mode, "format": "json"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
```

---

### 6. Test All Modes in Integration

**Integration tests for each mode**:

```python
@pytest.mark.parametrize("mode", [
    "standard",
    "issues",
    "documents",
    "calendar",
    "trifecta"
])
def test_mode_integration(api_client, base_url, auth_headers, mode):
    """Test each mode works end-to-end with real integrations"""
    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": mode, "format": "json"},
        headers=auth_headers,
        timeout=30  # Some modes may take longer
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["standup"]["mode"] == mode

    # Mode-specific assertions
    standup = data["standup"]
    if mode == "issues":
        # Should include GitHub issues
        assert "issues" in standup or "github" in str(standup).lower()
    elif mode == "documents":
        # Should include document analysis
        assert "documents" in standup or "analysis" in str(standup).lower()
    elif mode == "calendar":
        # Should include calendar events
        assert "events" in standup or "calendar" in str(standup).lower()
    elif mode == "trifecta":
        # Should include all three
        assert len(standup.keys()) >= 3
```

---

### 7. Test All Formats in Integration

**Integration tests for each format**:

```python
@pytest.mark.parametrize("format_type", [
    "json",
    "slack",
    "markdown",
    "text"
])
def test_format_integration(api_client, base_url, auth_headers, format_type):
    """Test each format works end-to-end"""
    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": "standard", "format": format_type},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    # Format-specific assertions
    if format_type == "json":
        assert isinstance(data["standup"], dict)
    elif format_type == "slack":
        # Slack format should have blocks or text
        standup = data["standup"]
        assert "blocks" in standup or "text" in standup
    elif format_type == "markdown":
        # Markdown should have markdown syntax
        standup_text = str(data["standup"])
        assert "#" in standup_text or "**" in standup_text or "*" in standup_text
    elif format_type == "text":
        # Plain text format
        standup_text = str(data["standup"])
        assert len(standup_text) > 0
```

---

### 8. Test Authentication Integration

**End-to-end auth flow tests**:

```python
def test_authentication_flow_integration(api_client, base_url, jwt_service):
    """Test complete authentication flow end-to-end"""
    # 1. Request without auth should fail
    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": "standard"}
    )
    assert response.status_code == 401

    # 2. Request with invalid token should fail
    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": "standard"},
        headers={"Authorization": "Bearer invalid_token_123"}
    )
    assert response.status_code == 401

    # 3. Generate valid token
    token = jwt_service.create_token({"sub": "test_user"})

    # 4. Request with valid token should succeed
    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": "standard"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_token_expiration_integration(api_client, base_url, jwt_service):
    """Test token expiration behavior"""
    # Create token that expires in 1 second
    token = jwt_service.create_token(
        {"sub": "test_user"},
        expires_delta=1  # 1 second
    )

    # Should work immediately
    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": "standard"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # Wait for expiration
    time.sleep(2)

    # Should fail after expiration
    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": "standard"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
```

---

### 9. Test Error Handling Integration

**End-to-end error scenarios**:

```python
def test_invalid_input_integration(api_client, base_url, auth_headers):
    """Test error handling for invalid inputs"""
    # Invalid mode
    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": "invalid_mode", "format": "json"},
        headers=auth_headers
    )
    assert response.status_code == 422

    # Invalid format
    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": "standard", "format": "invalid_format"},
        headers=auth_headers
    )
    assert response.status_code == 422

def test_server_error_handling_integration(api_client, base_url, auth_headers):
    """Test error handling when integrations fail"""
    # This tests graceful degradation
    # Even if some integrations fail, API should return partial results
    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": "trifecta", "format": "json"},
        headers=auth_headers,
        timeout=30
    )

    # Should either succeed or fail gracefully
    assert response.status_code in [200, 500, 503]

    if response.status_code == 200:
        # Success - verify structure
        data = response.json()
        assert "standup" in data or "error" in data
```

---

### 10. Test Performance Baseline

**Basic performance checks**:

```python
import time

def test_response_time_baseline(api_client, base_url, auth_headers):
    """Test that API responds within acceptable time"""
    start_time = time.time()

    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": "standard", "format": "json"},
        headers=auth_headers
    )

    end_time = time.time()
    response_time = end_time - start_time

    assert response.status_code == 200
    # Target: <2 seconds for standard mode
    assert response_time < 2.0, f"Response took {response_time:.2f}s (target <2s)"

def test_concurrent_requests_baseline(api_client, base_url, auth_headers):
    """Test handling multiple concurrent requests"""
    import concurrent.futures

    def make_request():
        return api_client.post(
            f"{base_url}/api/v1/standup/generate",
            json={"mode": "standard", "format": "json"},
            headers=auth_headers
        )

    # Test with 3 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(make_request) for _ in range(3)]
        responses = [f.result() for f in futures]

    # All should succeed
    assert all(r.status_code == 200 for r in responses)
    assert all(r.json()["success"] is True for r in responses)
```

---

## Verification Steps

### Step 1: Run Full Integration Test Suite

```bash
# Ensure API server is running in Terminal 1:
uvicorn main:app --reload --port 8001

# Terminal 2: Run integration tests
pytest tests/integration/test_standup_integration.py -v --tb=short

# Save output
pytest tests/integration/test_standup_integration.py -v > dev/active/pytest-integration-output-task7.txt 2>&1
```

**Expected**: All integration tests passing

---

### Step 2: Verify End-to-End Workflows

**Manual verification** (optional but recommended):

```bash
# 1. Health check
curl http://localhost:8001/api/v1/standup/health

# 2. Get token (via Python)
python3 -c "
from services.auth.jwt_service import JWTService
jwt = JWTService()
token = jwt.create_token({'sub': 'test_user'})
print(f'TOKEN={token}')
"

# 3. Test standup generation
curl -X POST http://localhost:8001/api/v1/standup/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"mode":"standard","format":"json"}'
```

---

### Step 3: Test Enumeration

**Create completeness table**:

| Test Category | Count | Status |
|--------------|-------|--------|
| End-to-end workflows | 2+ | ☐ |
| Mode integration (5) | 5 | ☐ |
| Format integration (4) | 4 | ☐ |
| Auth integration | 2+ | ☐ |
| Error handling integration | 2+ | ☐ |
| Performance baseline | 2+ | ☐ |
| **Total** | **17+** | **☐** |

**Target**: All categories complete, all tests passing

---

### Step 4: Verify Real Integrations

**Check that real services are being called**:

```python
def test_github_integration_real(api_client, base_url, auth_headers):
    """Verify GitHub integration is actually called"""
    response = api_client.post(
        f"{base_url}/api/v1/standup/generate",
        json={"mode": "issues", "format": "json"},
        headers=auth_headers,
        timeout=30
    )

    assert response.status_code == 200
    data = response.json()

    # Should have called GitHub (check metadata or content)
    metadata = data.get("metadata", {})
    # Verify GitHub was actually contacted (not mocked)
```

---

## Success Criteria

Task 7 is complete when:

- [ ] Integration test suite created (tests/integration/test_standup_integration.py)
- [ ] API server verified running on port 8001
- [ ] End-to-end workflow tests passing (2+)
- [ ] All modes tested in integration (5)
- [ ] All formats tested in integration (4)
- [ ] Authentication flow tested end-to-end (2+)
- [ ] Error handling tested in integration (2+)
- [ ] Performance baseline tests passing (2+)
- [ ] All integration tests passing (17+ tests, 100% pass rate)
- [ ] Real integrations verified (not mocked)
- [ ] Integration test output saved to dev/active/
- [ ] Test enumeration complete (X/X = 100%)
- [ ] Code committed with git log shown
- [ ] Session log updated in .md format

---

## Self-Check Before Claiming Complete

### Ask Yourself:

1. **Do all integration tests actually pass?** (Not just "should pass")
2. **Did I test with real API server?** (Not mocked)
3. **Did I test all 5 modes in integration?** (Not just unit tests)
4. **Did I test all 4 formats in integration?** (Not just JSON)
5. **Did I test complete auth flow?** (No token → invalid → valid)
6. **Did I test error handling end-to-end?** (Invalid inputs, server errors)
7. **Did I verify real integrations?** (GitHub actually called)
8. **Is API server actually running?** (Verified on port 8001)
9. **Did I save evidence to dev/active/?** (Not /tmp!)
10. **Do I have integration test output?** (Actual pytest results)
11. **Is there a gap between claims and reality?** (Evidence matches)
12. **Am I rationalizing any missing tests?** (No "probably works")
13. **Did I verify git commits?** (Shown log output)
14. **Am I guessing or do I have evidence?** (Evidence for everything)

### If Uncertain About Anything:

- Run the integration tests again with API server
- Show actual pytest output
- Count the test functions
- Verify server is running
- Ask for help if stuck
- **Never assume integration tests pass - run them with real server!**

---

## Files to Create/Modify

### Primary Files

- `tests/integration/test_standup_integration.py` - Integration test suite

### Evidence Files (save to dev/active/)

- `pytest-integration-output-task7.txt` - Complete pytest run output

### Session Log

- `dev/2025/10/20/HHMM-prog-code-log.md` - Your session log

---

## Deliverables

### 1. Integration Test Suite File

**Location**: tests/integration/test_standup_integration.py

**Should include**:
- Fixtures for API client, auth tokens
- End-to-end workflow tests (2+)
- Mode integration tests (5)
- Format integration tests (4)
- Auth flow integration tests (2+)
- Error handling integration tests (2+)
- Performance baseline tests (2+)
- Clear docstrings
- Real HTTP requests

---

### 2. Integration Test Results

**Evidence**: dev/active/pytest-integration-output-task7.txt

**Should show**:
```
============================= test session starts ==============================
...
tests/integration/test_standup_integration.py::test_complete_workflow PASSED [ 5%]
tests/integration/test_standup_integration.py::test_mode_standard PASSED    [10%]
tests/integration/test_standup_integration.py::test_mode_issues PASSED      [15%]
...
============================== X passed in X.XXs ===============================
```

**Target**: 100% pass rate (all green), 17+ tests

---

### 3. Test Enumeration

**Table**:

| Category | Tests | Pass | Coverage |
|----------|-------|------|----------|
| End-to-end workflows | 2+ | X/X | 100% |
| Mode integration (5) | 5 | 5/5 | 100% |
| Format integration (4) | 4 | 4/4 | 100% |
| Auth flow | 2+ | X/X | 100% |
| Error handling | 2+ | X/X | 100% |
| Performance | 2+ | X/X | 100% |
| **Total** | **17+** | **X/X** | **100%** |

---

### 4. Session Log

**In dev/2025/10/20/HHMM-prog-code-log.md**:
- Integration test suite design
- API server verification
- Test categories implemented
- Pytest run results
- Any challenges and solutions
- Time spent

---

## Remember

- **Use Python + pytest** - Not bash/curl for integration
- **Test with real API server** - Running on port 8001
- **Test ALL scenarios** - All modes, formats, auth, errors
- **All tests must pass** - Before claiming done
- **Save to dev/active/** - Not /tmp!
- **Evidence for everything** - pytest output required
- **100% means 100%** - All integration tests passing

**Integration tests = production confidence!** 🚀

---

## Issue #162 Context

**This is the FINAL task** before closing Issue #162!

**After Task 7**:
- ✅ All 7 tasks complete
- ✅ Multi-modal API fully tested
- ✅ Ready for Task Z (commit & close)
- ✅ Ready for Phase 3 (#161)

**Make this count** - thorough integration testing ensures production readiness!

---

*Template Version: 9.0*
*Based on: agent-prompt-template.md*
*All methodology sections included*
*Post-compaction protocol prominent*
*Python testing approach emphasized*
*Integration testing focus*
*Task-specific sections customized*
*Ready for deployment*
