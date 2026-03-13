# Agent Prompt: Test Execution Verification

## Mission
After Code fixes dependencies, verify tests ACTUALLY RUN and report real pass/fail status. No theoretical success.

## Context
Code has fixed:
- `tests.mocks` module (restored or created)
- `services.database.async_session_factory` (fixed location or created)

Your job: Prove tests execute and report honest results.

## Verification Tasks

### 1. Integration Tests - Full Execution
```bash
# Run integration test suite
cd /Users/xian/Development/piper-morgan
PYTHONPATH=. python -m pytest tests/integration/ -v

# Capture FULL output including:
# - "collected X items" line
# - Each test with PASSED/FAILED status
# - Final summary (X passed, Y failed, Z errors)
```

### 2. Performance Tests - Full Suite
```bash
# Run all performance tests (not just QueryRouter one)
PYTHONPATH=. python -m pytest tests/performance/ -v

# Check for:
# - Collection errors (should be GONE)
# - Pass/fail status
# - Any performance threshold violations
```

### 3. E2E GitHub Test - Specific Execution
```bash
# Run the specific E2E test
PYTHONPATH=. python -m pytest tests/integration/test_github_integration_e2e.py -v

# Look for:
# - Does it collect?
# - Does it execute?
# - Does it pass?
```

## Evidence Requirements

### Format for Each Test Category

**Integration Tests**:
```
Terminal Output:
[paste complete pytest output]

Status: [ALL_PASSING | SOME_FAILING | COLLECTION_ERRORS]
Count: X passed, Y failed, Z errors
Concerns: [any warnings, weird behavior, or quality issues]
```

**Performance Tests**:
```
Terminal Output:
[paste complete pytest output]

Status: [ALL_PASSING | SOME_FAILING | COLLECTION_ERRORS]
Performance: [all <500ms | some violations | unclear]
Concerns: [any issues]
```

**E2E Tests**:
```
Terminal Output:
[paste complete pytest output]

Status: [PASSING | FAILING | CANNOT_RUN]
GitHub Integration: [works | fails | cannot verify]
Concerns: [any issues]
```

## Critical Standards

### What Counts as PASSING
- ✅ Test collects without errors
- ✅ Test executes completely
- ✅ Test assertions all pass
- ✅ No warnings about missing features
- ✅ Terminal shows "PASSED" status

### What Counts as FAILING
- ❌ Collection errors (even if Code "fixed" them)
- ❌ Test runs but assertions fail
- ❌ Test passes but doesn't actually test anything (check assertions!)
- ❌ Warnings about mock behavior or missing implementations

### The Honesty Rule
**Report what you see, not what we hope for.**

If a test "passes" but has concerning warnings, report both:
- Status: PASSING (with concerns)
- Concerns: [specific warnings about mocks, etc.]

## Success Criteria
- Every test category has clear PASS or FAIL status
- No "would pass if..." or "mostly working" claims
- Evidence = terminal output showing execution
- Honest assessment of test quality

## STOP Conditions
- If tests pass but clearly don't test anything real (mock everything)
- If tests pass but have architectural issues (e.g., hardcoded values)
- If Code's "fixes" created new problems

Report findings with brutal honesty. We need truth, not optimism.
