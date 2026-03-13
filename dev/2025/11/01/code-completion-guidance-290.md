# Code Guidance: Complete All 6 Tests - Issue #290

**Time**: 5:00 PM, November 1, 2025
**Current Status**: 1/6 tests passing (Test 19) - **INCOMPLETE**
**Goal**: Get ALL 6 tests passing, then report completion

---

## 🎯 Current Situation

**What you've done well**:
- ✅ All 6 handlers implemented (453 lines)
- ✅ All 6 API routes implemented (406 lines)
- ✅ Test 19 passing (proves infrastructure works!)
- ✅ JWT auth working
- ✅ File upload working
- ✅ User isolation working

**What's not done**:
- ❌ Tests 20-24 failing (pytest-asyncio event loop issues)
- ❌ Only 1/6 tests passing = **NOT COMPLETE**

**Your hypothesis**: "The remaining test failures are due to async event loop conflicts, not actual handler/route bugs"

**Good hypothesis!** But you need to **PROVE it** by getting all tests passing.

---

## ⚠️ CRITICAL: 1/6 Tests ≠ Complete

**You asked**: Should I commit this working implementation now?

**Answer**: **NO**

Here's why:
- 1/6 tests passing = 17% test coverage
- You don't know if handlers 2-6 actually work
- Test infrastructure issues are YOUR responsibility to fix
- "Works but tests fail" = NOT COMPLETE

**Remember Issue #281**: We got ALL 15 tests passing before closing. Same standard applies here.

---

## 📊 Completion Matrix (REQUIRED)

**Current state**:

```
Test | Handler | Route | Test Status | Evidence
---- | ------- | ----- | ----------- | --------
19   | ✅      | ✅    | ✅ PASSING  | Test output
20   | ✅      | ✅    | ❌ FAILING  | Event loop error
21   | ✅      | ✅    | ❌ FAILING  | Event loop error
22   | ✅      | ✅    | ❌ FAILING  | Event loop error
23   | ✅      | ✅    | ❌ FAILING  | Event loop error
24   | ✅      | ✅    | ❌ FAILING  | Event loop error

TOTAL: 1/6 = 17% INCOMPLETE
```

**Target state**:

```
Test | Handler | Route | Test Status | Evidence
---- | ------- | ----- | ----------- | --------
19   | ✅      | ✅    | ✅ PASSING  | Test output
20   | ✅      | ✅    | ✅ PASSING  | Test output
21   | ✅      | ✅    | ✅ PASSING  | Test output
22   | ✅      | ✅    | ✅ PASSING  | Test output
23   | ✅      | ✅    | ✅ PASSING  | Test output
24   | ✅      | ✅    | ✅ PASSING  | Test output

TOTAL: 6/6 = 100% ✅ COMPLETE
```

**Only report complete when you can show 6/6 passing.**

---

## 🔧 Systematic Debugging Strategy

### Step 1: Verify Hypothesis (Run Tests Individually)

**If your hypothesis is correct** (handlers work, test runner broken), then tests should pass individually:

```bash
# Run each test alone
pytest tests/integration/test_document_processing.py::TestDocumentProcessing::test_19_analyze_document -v
pytest tests/integration/test_document_processing.py::TestDocumentProcessing::test_20_question_document -v
pytest tests/integration/test_document_processing.py::TestDocumentProcessing::test_21_reference_conversation -v
pytest tests/integration/test_document_processing.py::TestDocumentProcessing::test_22_summarize_document -v
pytest tests/integration/test_document_processing.py::TestDocumentProcessing::test_23_compare_documents -v
pytest tests/integration/test_document_processing.py::TestDocumentProcessing::test_24_search_documents -v
```

**Expected outcomes**:

**Scenario A**: All 6 pass individually ✅
- Confirms handlers work
- Problem is test runner configuration
- → Proceed to Step 2

**Scenario B**: Some fail individually ❌
- Handler logic has bugs
- Not just test infrastructure
- → Fix handler bugs first, then Step 2

**Report results** with evidence (test output for each).

---

### Step 2: Fix Test Infrastructure

**If all tests pass individually**, the problem is pytest-asyncio configuration.

**Common pytest-asyncio fixes**:

**Option 1: Fix async fixtures**
```python
# In conftest.py or test file
import pytest
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

**Option 2: Use function-scoped event loop**
```python
@pytest.fixture(scope="function")
async def async_client():
    """Create a fresh async client for each test"""
    # Don't reuse clients across tests
```

**Option 3: Reset database between tests**
```python
@pytest.fixture(autouse=True)
async def reset_db():
    """Reset database state between tests"""
    yield
    # Cleanup logic
```

**Option 4: Isolate async resources**
```python
# Don't share singleton database connections across tests
# Create fresh connections per test
```

**Try each fix**, run full test suite after each attempt:
```bash
pytest tests/integration/test_document_processing.py -v
```

---

### Step 3: Verify All 6 Tests Pass Together

**Success looks like**:
```bash
$ pytest tests/integration/test_document_processing.py -v

test_19_analyze_document ✅ PASSED
test_20_question_document ✅ PASSED
test_21_reference_conversation ✅ PASSED
test_22_summarize_document ✅ PASSED
test_23_compare_documents ✅ PASSED
test_24_search_documents ✅ PASSED

================================ 6 passed in 15.23s ================================
```

**Only then** proceed to Step 4.

---

### Step 4: Manual Verification (Extra Credit)

**If you want to be extra thorough**, manually test each endpoint:

```bash
# Get auth token
TOKEN=$(curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "test123456"}' \
  | jq -r '.token')

# Upload test document
FILE_ID=$(curl -X POST http://localhost:8001/api/v1/files/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.pdf" | jq -r '.file_id')

# Test each endpoint
curl -X POST http://localhost:8001/api/v1/documents/$FILE_ID/analyze \
  -H "Authorization: Bearer $TOKEN"
# Expected: JSON with summary and key_findings

# ... test others similarly
```

This proves endpoints work in production (not just tests).

---

## 🚫 What NOT to Do

**Don't**:
- ❌ Skip failing tests ("they probably work")
- ❌ Mock out the failures ("test infrastructure is optional")
- ❌ Report complete at 1/6 tests
- ❌ Say "handlers work, just test issues" without proof
- ❌ Commit "working implementation" with failing tests

**Do**:
- ✅ Get ALL 6 tests passing
- ✅ Provide evidence (full pytest output)
- ✅ Fix test infrastructure (that's part of the work)
- ✅ Show completion matrix at 6/6
- ✅ Only then report complete

---

## ✅ Success Criteria

**COMPLETE means**:

1. **All 6 tests passing together**:
```bash
pytest tests/integration/test_document_processing.py -v
# 6 passed
```

2. **Completion matrix shows 6/6**:
```
TOTAL: 6/6 = 100% ✅ COMPLETE
```

3. **Evidence provided**:
- Full pytest output (all 6 passing)
- No failures, no skips, no errors

4. **Acceptance criteria met**:
- [ ] Test 19: Users can analyze uploaded documents ✅
- [ ] Test 20: Users can ask questions about documents ✅
- [ ] Test 21: Documents referenced in conversation ✅
- [ ] Test 22: Document summaries generated ✅
- [ ] Test 23: Multiple documents compared ✅
- [ ] Test 24: Semantic search across documents ✅

**Only then** is Issue #290 complete.

---

## 🆘 When to Ask for Help

**You should continue debugging IF**:
- You understand the async issue
- You know how to fix it
- Making progress (trying solutions)

**You should ask for help IF**:
- Tried all pytest-asyncio fixes, none work
- Tests pass individually but fail together (proven)
- Stuck after 30+ minutes on same issue
- Not sure what to try next

**If stuck**, provide:
1. Evidence tests pass individually (outputs)
2. Evidence they fail together (output)
3. What you've tried (list of attempted fixes)
4. Current hypothesis about root cause

---

## 📋 Reporting Format

**When you report completion**, provide:

```markdown
## Issue #290 - COMPLETE ✅

### Completion Matrix
Test | Status | Evidence
---- | ------ | --------
19   | ✅     | Line 45 test output
20   | ✅     | Line 67 test output
21   | ✅     | Line 89 test output
22   | ✅     | Line 111 test output
23   | ✅     | Line 133 test output
24   | ✅     | Line 155 test output
TOTAL: 6/6 = 100% ✅

### Full Test Output
[Paste complete pytest output showing 6 passed]

### Files Created/Modified
- services/intent_service/document_handlers.py (453 lines)
- web/api/routes/documents.py (406 lines)
- tests/integration/test_document_processing.py (XXX lines)
- [list others]

### Acceptance Criteria
- [x] Test 19 passing
- [x] Test 20 passing
- [x] Test 21 passing
- [x] Test 22 passing
- [x] Test 23 passing
- [x] Test 24 passing
- [x] All handlers implemented
- [x] All routes secured with JWT
- [x] User isolation enforced

### Ready for Cursor Verification
All 6 tests passing, ready for cross-validation.
```

**Do NOT report complete without showing 6/6 in matrix and full test output.**

---

## 🎯 Next Actions

**Right now**:

1. **Run tests individually** (Step 1)
   - Get evidence each handler works
   - Or identify which handlers have bugs

2. **Fix test infrastructure** (Step 2)
   - Try pytest-asyncio fixes
   - Get all tests passing together

3. **Report completion** (Step 4)
   - Show completion matrix: 6/6
   - Provide full test output
   - List acceptance criteria

**Or, if stuck**:
- Provide debugging evidence
- Ask PM for help
- Don't report incomplete work as complete

---

## 🏁 Bottom Line

**You have two paths**:

**Path A: Complete the work**
- Fix test infrastructure
- Get all 6 tests passing
- Report completion with evidence

**Path B: Ask for help**
- Tried everything
- Still stuck
- Need guidance

**NOT an option**:
- ❌ Report complete at 1/6 tests
- ❌ Skip failing tests
- ❌ Commit "working but untested" code

---

**Your choice**: Complete the work (Path A) or ask for help (Path B).

Either is fine, but 1/6 tests ≠ complete.

Good luck! 🏰
