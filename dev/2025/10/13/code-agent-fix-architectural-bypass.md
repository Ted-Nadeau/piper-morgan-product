# Code Agent Prompt: Fix Architectural Bypass in test_issues_integration.py

**Date**: October 13, 2025, 5:47 PM
**Task**: Refactor CLI test to use proper intent classification
**Duration**: 15-20 minutes
**Priority**: HIGH (architectural violation)
**Agent**: Code Agent

---

## Mission

Fix the architectural bypass in `test_issues_integration.py` by refactoring it to use proper intent classification flow instead of directly calling backend services.

**This is a real architectural issue, not a test configuration problem.** The bypass prevention test correctly identified this violation.

---

## The Problem

**File**: `tests/cli/test_issues_integration.py` (or similar location in CLI tests)
**Issue**: Test bypasses intent classification and directly calls backend services

**Violation Detected By**: `test_no_cli_bypasses.py`
**Error Message**: "test_issues_integration.py does not use intent classification (bypasses the intent system)"

**Current Pattern** (WRONG ❌):
```
User Input → Backend Service (BYPASS!)
```

**Should Be** (CORRECT ✅):
```
User Input → Intent Classification → Handler → Backend Service
```

---

## Why This Matters

**From GREAT-4E Architecture**:
1. **Security**: Intent classification validates and sanitizes input
2. **Consistency**: All requests get same treatment
3. **Monitoring**: Can track/log all requests
4. **Quality**: Intent handlers provide canonical responses

**This pattern is enforced across**:
- Web interface (test_no_web_bypasses.py)
- CLI interface (test_no_cli_bypasses.py)
- Slack interface (test_no_slack_bypasses.py)

---

## Investigation Phase (5 minutes)

### Step 1: Locate the Test File

Find `test_issues_integration.py`:
```bash
# It's in the CLI tests
find tests/cli/ -name "*issues*" -type f
```

### Step 2: Examine Current Implementation

Look at how it's currently structured:
```python
# What does it import?
# What does it test?
# How does it call services?
```

### Step 3: Find a Good Example

Look at other CLI tests that DO use intent classification:
```bash
# Find similar CLI integration tests
ls tests/cli/test_*integration*.py

# Check how they import and use IntentService
```

**Example Pattern** (from other tests):
```python
from services.intent_service.intent_service import IntentService

async def test_something(intent_service):
    # Use the service
    result = await intent_service.process_intent(
        query="create github issue for bug",
        user_id="test_user",
        session_id="test_session"
    )

    # Verify the result
    assert result.status == "success"
```

---

## Refactoring Phase (10 minutes)

### Step 1: Update Imports

**Remove direct service imports** (examples of what to remove):
```python
# REMOVE these (or similar):
from services.github.github_service import GitHubService
from services.issues.issue_tracker import IssueTracker
# etc.
```

**Add intent service import**:
```python
# ADD this:
from services.intent_service.intent_service import IntentService
```

### Step 2: Update Fixtures

If the test has fixtures that directly instantiate services, replace them:

**Before** (WRONG ❌):
```python
@pytest.fixture
def github_service():
    return GitHubService()
```

**After** (CORRECT ✅):
```python
@pytest.fixture
def intent_service():
    # Use the existing IntentService fixture
    # Or import it if needed
    return IntentService()
```

### Step 3: Refactor Test Cases

For each test in the file, refactor to use intent classification:

**Before** (WRONG ❌):
```python
async def test_create_issue(github_service):
    # Direct service call
    result = await github_service.create_issue(
        title="Bug found",
        description="Something broke"
    )
    assert result.success
```

**After** (CORRECT ✅):
```python
async def test_create_issue(intent_service):
    # Through intent classification
    result = await intent_service.process_intent(
        query="create github issue: Bug found - Something broke",
        user_id="test_user",
        session_id="test_session"
    )

    # Verify canonical response structure
    assert result.status == "success"
    assert result.intent_category == "ACTION"  # or whatever is appropriate
    assert "issue" in result.response.lower()
```

### Key Points for Refactoring

1. **Query Format**: Natural language queries, not direct parameters
   - Bad: `create_issue(title="Bug", desc="...")`
   - Good: `"create github issue: Bug - ..."`

2. **Response Structure**: Canonical handler responses
   - Will have: status, intent_category, response, etc.
   - Not: Direct service return values

3. **Assertions**: Verify the canonical response
   - Check status/intent_category
   - Verify response content makes sense
   - Don't check internal service details

---

## Verification Phase (5 minutes)

### Step 1: Run the Test Locally

```bash
# Run the refactored test
pytest tests/cli/test_issues_integration.py -v
```

**Expected**: All tests pass ✅

### Step 2: Run Bypass Prevention Test

```bash
# Run the bypass detection
pytest tests/intent/test_no_cli_bypasses.py -v
```

**Expected**: Should pass now (no bypass detected) ✅

### Step 3: Run Full CLI Test Suite

```bash
# Make sure we didn't break anything
pytest tests/cli/ -v
```

**Expected**: All CLI tests pass ✅

---

## Commit Strategy

### Create Descriptive Commit

```bash
# Stage the changes
git add tests/cli/test_issues_integration.py

# Commit with clear message
git commit -m "fix(tests): Refactor test_issues_integration to use intent classification

The test was bypassing the intent classification system and directly
calling backend services. This violated the architectural pattern that
ALL user input must go through intent classification first.

Changes:
- Updated imports to use IntentService
- Refactored test cases to use process_intent()
- Tests now follow canonical handler response pattern
- Fixes bypass prevention test failure

This ensures:
- Security: Input validation/sanitization
- Consistency: Same flow for all interfaces
- Monitoring: All requests are logged
- Quality: Canonical responses maintained

Detected by: test_no_cli_bypasses.py
Architectural Pattern: User Input → Intent → Handler → Service"

# Push
git push origin main
```

---

## Documentation

### Update CI Fixes Results

Add to `dev/2025/10/13/ci-fixes-results.md`:

```markdown
### Architectural Fix: test_issues_integration.py

**Date**: October 13, 2025, 5:47 PM
**Duration**: [X] minutes

**Problem Detected**:
- Bypass prevention test found architectural violation
- test_issues_integration.py bypassed intent classification
- Directly called backend services (security/consistency issue)

**Fix Applied**:
- Refactored to use IntentService.process_intent()
- Updated imports and test structure
- Now follows proper architectural pattern

**Pattern Enforced**:
✅ User Input → Intent Classification → Handler → Service
❌ User Input → Service (BYPASSED)

**Tests Passing**:
- [x] test_issues_integration.py
- [x] test_no_cli_bypasses.py
- [x] Full CLI test suite

**Impact**:
- Architectural integrity maintained
- Security pattern enforced
- Consistency across all interfaces

**Time**: [X] minutes
**Status**: ✅ Complete
```

---

## Success Criteria

### Refactoring Complete ✅
- [ ] Imports updated to use IntentService
- [ ] All test cases refactored to use process_intent()
- [ ] Tests verify canonical handler responses
- [ ] No direct service calls remaining

### Tests Passing ✅
- [ ] test_issues_integration.py passes locally
- [ ] test_no_cli_bypasses.py passes (no violation)
- [ ] Full CLI suite passes
- [ ] No new failures introduced

### Committed and Pushed ✅
- [ ] Changes staged
- [ ] Descriptive commit message
- [ ] Pushed to main branch
- [ ] CI triggered

### Documentation ✅
- [ ] CI fixes results updated
- [ ] Architectural pattern documented
- [ ] Ready for final CI verification

---

## Time Budget

- **Investigation**: 5 minutes (locate, examine, find examples)
- **Refactoring**: 10 minutes (update imports, fixtures, test cases)
- **Verification**: 5 minutes (run tests, check bypass prevention)
- **Commit & Push**: 3 minutes
- **Documentation**: 2 minutes
- **Total**: 25 minutes (with buffer)

**Target Completion**: 6:12 PM

---

## What NOT to Do

- ❌ Don't change the test's purpose/coverage
- ❌ Don't add new functionality
- ❌ Don't fix other issues found
- ❌ Don't modify bypass prevention tests
- ❌ Don't skip running bypass test to verify

## What TO Do

- ✅ Keep test coverage equivalent
- ✅ Use same patterns as other CLI tests
- ✅ Follow canonical response structure
- ✅ Verify bypass prevention passes
- ✅ Document the architectural pattern

---

## Context

**PM Quote**: "I'm up for it! we closed GAP today. Anything beyond that is gravy! :D"

**Why This Fix Matters**:
- Real architectural violation (not technical debt)
- Security pattern enforcement
- Maintains consistency across all interfaces
- Validates our bypass prevention system works!

**What This Demonstrates**:
- Quality gates catching real issues ✅
- Architectural patterns being enforced ✅
- Test-driven quality working ✅
- "Push to 100%" philosophy validated ✅

**What Comes After**:
- CI should be 13/14 or 14/14 passing
- Ready for PROOF documentation work
- Clean baseline for rest of PROOF epic

---

**Fix Start Time**: 5:47 PM
**Expected Completion**: ~6:12 PM (25 minutes)
**Status**: Ready for Code Agent execution

**LET'S ENFORCE ARCHITECTURAL INTEGRITY! 🏗️**

---

*"Architecture patterns aren't suggestions. They're requirements. And tests that enforce them are heroes."*
*- Bypass Prevention Philosophy*
