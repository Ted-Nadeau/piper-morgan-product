# Task 6: Comprehensive Testing - Standup API

**Agent**: Claude Code (Programmer)
**Issue**: #162 (CORE-STAND-MODES-API)
**Task**: 6 of 7 - Comprehensive Testing
**Sprint**: A4 "Standup Epic"
**Date**: October 19, 2025, 6:57 PM
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

**Bash + JSON = Python. Always.** This is the lesson from Task 5.

---

## Mission

Create a comprehensive pytest unit test suite for all standup API endpoints, achieving high test coverage, testing all success and error paths, and ensuring the API is production-ready and maintainable.

**Scope**:
- Create pytest test suite (tests/api/test_standup_api.py)
- Test all endpoints thoroughly
- Test all modes (5)
- Test all formats (4)
- Test all error scenarios
- Achieve >80% code coverage
- Verify with pytest run

**NOT in scope**:
- Integration testing (Task 7)
- Performance testing
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
  - ❓ Comprehensive tests needed
- **Target State**:
  - Complete pytest test suite
  - All endpoints tested
  - All scenarios covered
  - High code coverage
  - CI/CD ready
- **Dependencies**:
  - pytest framework
  - pytest-asyncio for async tests
  - Working API endpoints
- **User Data Risk**: None - testing only
- **Infrastructure Verified**: Yes - pytest configured

---

## STOP Conditions (EXPANDED TO 17)

If ANY of these occur, STOP and escalate to PM immediately:

1. **Infrastructure doesn't match gameplan** - pytest not configured properly
2. **Method implementation <100% complete** - All test scenarios must be written
3. **Pattern already exists in catalog** - Check existing test patterns
4. **Tests fail for any reason** - ALL tests must pass before claiming done
5. **Configuration assumptions needed** - Don't guess pytest setup
6. **GitHub issue missing or unassigned** - Verify #162 still assigned
7. **Can't provide verification evidence** - Must show test results
8. **ADR conflicts with approach** - Check for testing ADRs
9. **Resource not found after searching** - Test files must exist
10. **User data at risk** - N/A for testing
11. **Completion bias detected** - Tests must actually pass
12. **Rationalizing gaps as "minor"** - All scenarios critical
13. **GitHub tracking not working** - Issue updates must work
14. **Single agent seems sufficient** - This IS single agent task
15. **Git operations failing** - All commits must work
16. **Server state unexpected** - API must be running for tests
17. **Bash + JSON not working** - Switch to Python immediately

**Remember**: STOP means STOP. Don't try to work around it. Ask PM.

---

## Evidence Requirements (CRITICAL - EXPANDED)

### For EVERY Claim You Make:

- **"Tests pass"** → Show pytest output with all passing
- **"Coverage X%"** → Show coverage report
- **"Scenario X tested"** → Show test function for that scenario
- **"All modes tested"** → Show 5 test functions or parameterized test
- **"All formats tested"** → Show 4 test functions or parameterized test
- **"Error handling tested"** → Show error scenario tests

### Completion Bias Prevention (CRITICAL):

- **Never guess! Always verify first!**
- **NO "tests should pass"** - only "here's pytest output showing all passed"
- **NO "probably covered"** - only "here's the test function"
- **NO assumptions** - only verified facts with pytest output
- **NO rushing to claim done** - all tests passing, then claim done

### Working Files Location (CRITICAL):

**NEVER use /tmp for important files**:
- ❌ /tmp - Can be lost between sessions
- ✅ dev/active/ - For working files, evidence
- ✅ tests/api/ - For test files
- ✅ outputs/ - For final reports

**Save pytest output to**: dev/active/pytest-output-task6.txt

### Testing Approach (CRITICAL):

**When testing API with JSON**:
- ✅ Use Python + requests library
- ✅ Use pytest framework
- ✅ Use pytest fixtures for setup
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

1. **Verifying infrastructure FIRST** (no wrong assumptions)
2. **Ensuring 100% completeness** (no 80% pattern)
3. **Checking what exists NEXT** (test file may already exist)
4. **Preserving user data ALWAYS** (N/A for testing)
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

**Incomplete tests = unreliable API. Evidence is mandatory.**

---

## Task Requirements

### 1. Review Existing Test Infrastructure

**Check pytest configuration**:

```bash
# Check pytest.ini exists
cat pytest.ini

# Check test directory structure
ls -la tests/
ls -la tests/api/

# Check if test file exists
ls -la tests/api/test_standup_api.py

# Check dependencies
grep pytest requirements.txt
```

**If not configured**: STOP (condition #1)

**If test file exists**: Review it first, don't overwrite

---

### 2. Design Test Suite Structure

**Test organization**:

```python
# tests/api/test_standup_api.py

import pytest
from fastapi.testclient import TestClient
# Or for async:
# import pytest_asyncio
# from httpx import AsyncClient

# Test structure:
# 1. Fixtures (setup/teardown)
# 2. Authentication tests
# 3. Endpoint tests (success paths)
# 4. Error handling tests
# 5. Mode-specific tests
# 6. Format-specific tests
# 7. Edge cases
```

**Use fixtures for**:
- Test client setup
- Token generation
- Database state (if applicable)
- Mock services (if needed)

---

### 3. Test All Endpoints

**Endpoint enumeration**:

| Endpoint | Method | Test Count | Status |
|----------|--------|------------|--------|
| /api/v1/standup/generate | POST | ~20 tests | ☐ |
| /api/v1/standup/health | GET | ~2 tests | ☐ |
| /api/v1/standup/modes | GET | ~2 tests | ☐ |
| /api/v1/standup/formats | GET | ~2 tests | ☐ |

**Total**: ~26 tests minimum

---

### 4. Test All Standup Modes

**Mode testing** (5 modes):

```python
@pytest.mark.parametrize("mode", [
    "standard",
    "issues",
    "documents",
    "calendar",
    "trifecta"
])
def test_standup_generation_mode(client, auth_token, mode):
    """Test standup generation for each mode"""
    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": mode, "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "standup" in data
    assert "metadata" in data
```

**Each mode should**:
- Return 200 with auth
- Include standup content
- Include metadata
- Have appropriate structure

---

### 5. Test All Output Formats

**Format testing** (4 formats):

```python
@pytest.mark.parametrize("format_type", [
    "json",
    "slack",
    "markdown",
    "text"
])
def test_standup_generation_format(client, auth_token, format_type):
    """Test standup generation for each format"""
    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard", "format": format_type},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    # Format-specific assertions
```

**Each format should**:
- Return 200 with auth
- Have format-appropriate structure
- Be valid for that format type

---

### 6. Test Authentication Flows

**Auth test scenarios**:

```python
def test_generate_no_auth(client):
    """Test generation without authentication"""
    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard"}
    )
    assert response.status_code == 401
    assert "Authentication required" in response.json()["detail"]

def test_generate_invalid_token(client):
    """Test generation with invalid token"""
    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard"},
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert "Invalid or expired token" in response.json()["detail"]

def test_generate_valid_token(client, auth_token):
    """Test generation with valid token"""
    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
```

---

### 7. Test Error Scenarios

**Validation error tests**:

```python
def test_generate_invalid_mode(client, auth_token):
    """Test generation with invalid mode"""
    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "invalid_mode"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422
    # Pydantic validation error format

def test_generate_invalid_format(client, auth_token):
    """Test generation with invalid format"""
    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard", "format": "invalid"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422
```

---

### 8. Test Public Endpoints

**Health, modes, formats**:

```python
def test_health_endpoint(client):
    """Test health endpoint (public)"""
    response = client.get("/api/v1/standup/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_modes_endpoint(client):
    """Test modes listing (public)"""
    response = client.get("/api/v1/standup/modes")
    assert response.status_code == 200
    data = response.json()
    assert len(data["modes"]) == 5

def test_formats_endpoint(client):
    """Test formats listing (public)"""
    response = client.get("/api/v1/standup/formats")
    assert response.status_code == 200
    data = response.json()
    assert len(data["formats"]) == 4
```

---

### 9. Create Test Fixtures

**Essential fixtures**:

```python
import pytest
from fastapi.testclient import TestClient
from services.auth.jwt_service import JWTService

@pytest.fixture
def client():
    """Create test client"""
    from main import app
    return TestClient(app)

@pytest.fixture
def jwt_service():
    """Create JWT service"""
    return JWTService()

@pytest.fixture
def auth_token(jwt_service):
    """Generate valid auth token"""
    return jwt_service.create_token({"sub": "test_user"})

@pytest.fixture
def test_user_id():
    """Test user ID"""
    return "test_user"
```

---

### 10. Run Tests and Generate Coverage

**Run pytest**:

```bash
# Run all tests with verbose output
pytest tests/api/test_standup_api.py -v > dev/active/pytest-output-task6.txt 2>&1

# Show summary
tail -20 dev/active/pytest-output-task6.txt

# Run with coverage
pytest tests/api/test_standup_api.py --cov=web.api --cov-report=term-missing

# Save coverage report
pytest tests/api/test_standup_api.py --cov=web.api --cov-report=term > dev/active/coverage-report-task6.txt
```

**Expected**:
- All tests passing (100%)
- Coverage >80%
- No failures or errors

**If tests fail**: STOP (condition #4) - Fix before continuing

---

## Verification Steps

### Step 1: Run Full Test Suite

```bash
# Activate environment if needed
# source venv/bin/activate

# Run all standup API tests
pytest tests/api/test_standup_api.py -v --tb=short

# Should see:
# - All tests passing (green)
# - No failures (red)
# - No errors
```

**Evidence Required**: Complete pytest output

---

### Step 2: Verify Coverage

```bash
# Generate coverage report
pytest tests/api/test_standup_api.py \
  --cov=web.api.routes.standup \
  --cov=web.api.routes \
  --cov-report=term-missing

# Target: >80% coverage
```

**Evidence Required**: Coverage percentage and report

---

### Step 3: Test Enumeration

**Create completeness table**:

| Test Category | Count | Status |
|--------------|-------|--------|
| Auth tests | 3 | ✅ |
| Mode tests | 5 | ✅ |
| Format tests | 4 | ✅ |
| Error tests | 6 | ✅ |
| Public endpoints | 3 | ✅ |
| Edge cases | X | ✅ |
| **Total** | **X** | **100%** |

**Target**: All categories complete

---

### Step 4: Verify Test Quality

**Check each test has**:
- Clear docstring
- Appropriate assertions
- Error case coverage
- Edge case handling

**Run with extra strictness**:
```bash
# Run with warnings
pytest tests/api/test_standup_api.py -W error::pytest.PytestUnraisableExceptionWarning

# Check for deprecation warnings
pytest tests/api/test_standup_api.py -W default
```

---

## Success Criteria

Task 6 is complete when:

- [ ] Pytest test suite created (tests/api/test_standup_api.py)
- [ ] All endpoints tested (4 endpoints)
- [ ] All modes tested (5 modes)
- [ ] All formats tested (4 formats)
- [ ] All auth scenarios tested (3 scenarios)
- [ ] All error scenarios tested (6+ scenarios)
- [ ] All public endpoints tested (3 endpoints)
- [ ] Test fixtures properly configured
- [ ] All tests passing (100% pass rate)
- [ ] Coverage >80% achieved
- [ ] Pytest output saved to dev/active/ (not /tmp!)
- [ ] Coverage report saved to dev/active/
- [ ] Test enumeration complete (X/X = 100%)
- [ ] Code committed with git log shown
- [ ] Session log updated in .md format

---

## Self-Check Before Claiming Complete

### Ask Yourself:

1. **Do all tests actually pass?** (Not just "should pass")
2. **Did I test all 5 modes?** (Not just some)
3. **Did I test all 4 formats?** (Not just JSON)
4. **Did I test all auth scenarios?** (No auth, bad auth, good auth)
5. **Did I test all error cases?** (Invalid input, validation errors)
6. **Is coverage >80%?** (Verified with coverage report)
7. **Did I use Python for testing?** (Not bash/curl)
8. **Did I save evidence to dev/active/?** (Not /tmp!)
9. **Do I have pytest output showing all pass?** (Actual evidence)
10. **Is there a gap between claims and reality?** (Evidence matches)
11. **Am I rationalizing any missing tests?** (No "probably covered")
12. **Did I verify git commits?** (Shown log output)
13. **Am I guessing or do I have evidence?** (Evidence for everything)

### If Uncertain About Anything:

- Run the tests again
- Show actual pytest output
- Count the test functions
- Check coverage report
- Ask for help if stuck
- **Never assume tests pass - run them!**

---

## Files to Create/Modify

### Primary Files

- `tests/api/test_standup_api.py` - Main test suite

### Evidence Files (save to dev/active/)

- `pytest-output-task6.txt` - Complete pytest run output
- `coverage-report-task6.txt` - Coverage report

### Session Log

- `dev/2025/10/19/HHMM-prog-code-log.md` - Your session log

---

## Deliverables

### 1. Test Suite File

**Location**: tests/api/test_standup_api.py

**Should include**:
- Fixtures for setup
- Auth tests (3+)
- Mode tests (5)
- Format tests (4)
- Error tests (6+)
- Public endpoint tests (3)
- Edge case tests
- Clear docstrings
- Proper assertions

---

### 2. Test Results

**Evidence**: dev/active/pytest-output-task6.txt

**Should show**:
```
============================= test session starts ==============================
...
tests/api/test_standup_api.py::test_health_endpoint PASSED           [  4%]
tests/api/test_standup_api.py::test_modes_endpoint PASSED            [  8%]
...
tests/api/test_standup_api.py::test_mode_standard PASSED             [ 52%]
tests/api/test_standup_api.py::test_mode_issues PASSED               [ 56%]
...
============================== X passed in X.XXs ===============================
```

**Target**: 100% pass rate (all green)

---

### 3. Coverage Report

**Evidence**: dev/active/coverage-report-task6.txt

**Should show**:
```
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
web/api/routes/standup.py            150     20    87%   45-50, 78-82
-----------------------------------------------------------------
TOTAL                                150     20    87%
```

**Target**: >80% coverage

---

### 4. Test Enumeration

**Table**:

| Category | Tests | Pass | Coverage |
|----------|-------|------|----------|
| Authentication | 3 | 3/3 | 100% |
| Modes (5) | 5 | 5/5 | 100% |
| Formats (4) | 4 | 4/4 | 100% |
| Errors | 6 | 6/6 | 100% |
| Public endpoints | 3 | 3/3 | 100% |
| Edge cases | X | X/X | 100% |
| **Total** | **X** | **X/X** | **100%** |

---

### 5. Session Log

**In dev/2025/10/19/HHMM-prog-code-log.md**:
- Test suite design
- Fixtures created
- Test categories implemented
- Pytest run results
- Coverage analysis
- Any challenges and solutions
- Time spent

---

## Remember

- **Use Python + pytest** - Not bash/curl
- **Test ALL scenarios** - Not just happy paths
- **All tests must pass** - Before claiming done
- **Save to dev/active/** - Not /tmp!
- **Evidence for everything** - pytest output, coverage report
- **100% means 100%** - All modes, formats, errors tested

**Comprehensive tests = confidence in production!** 🧪

---

*Template Version: 8.0*
*Based on: agent-prompt-template.md*
*All methodology sections included*
*Post-compaction protocol added*
*Working files location guidance added*
*Bash + JSON = Python guidance added*
*STOP early when stuck emphasized*
*Task-specific sections customized*
*Ready for deployment*
