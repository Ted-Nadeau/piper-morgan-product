# Agent Prompt: Verify LLM Classifier Fix

## Mission
After Code fixes the constructor bug, verify LLM classifier tests and reassess Testing Phase checkbox status.

## Context
Code fixed constructor parameter bug in `services/intent_service/llm_classifier.py`:
- Changed: `message=original_message` → `original_message=original_message`
- Should eliminate TypeError and allow tests to execute

## Verification Tasks

### 1. Run Complete LLM Test Suite
```bash
cd /Users/xian/Development/piper-morgan

# Full LLM classifier test suite
PYTHONPATH=. python -m pytest tests/unit/services/intent_service/test_llm_intent_classifier.py -v

# Capture complete output
```

### 2. Run Performance Benchmark
```bash
# LLM performance test that was failing
PYTHONPATH=. python -m pytest tests/performance/test_llm_classifier_benchmarks.py -v

# Check if <500ms requirement met
```

### 3. Run Integration Tests Again
```bash
# Re-run integration suite to see impact
PYTHONPATH=. python -m pytest tests/integration/ -v --tb=short

# Check if LLM-dependent integration tests now pass
```

### 4. Run Complete Testing Phase Suite
```bash
# All performance tests
PYTHONPATH=. python -m pytest tests/performance/ -v

# Error scenario tests
PYTHONPATH=. python -m pytest tests/ -k "error" -v

# E2E GitHub test (should still pass)
PYTHONPATH=. python -m pytest tests/integration/test_github_integration_e2e.py -v
```

## Evidence Requirements

### For Each Test Category

**LLM Classifier Tests**:
```
Terminal Output:
[paste complete pytest output]

Status: [ALL_PASSING | SOME_FAILING | STILL_BROKEN]
Count: X passed, Y failed
Constructor Bug: [FIXED | STILL_PRESENT]
New Issues Found: [list any remaining failures]
```

**Performance Tests**:
```
Terminal Output:
[paste complete pytest output]

Status: [ALL_PASSING | SOME_FAILING]
Count: X passed, Y failed
<500ms Requirement: [MET | VIOLATED | UNCLEAR]
```

**Integration Tests**:
```
Terminal Output:
[paste pytest output - first 50 lines and summary]

Status: [IMPROVED | SAME | WORSE]
Count: X passed, Y failed
```

## Testing Phase Checkbox Assessment

Based on test results, provide honest assessment:

**Checkbox 1: Unit tests for QueryRouter initialization**
- Status: [CAN_CHECK ✅ | CANNOT_CHECK ❌]
- Evidence: [test output or issue]

**Checkbox 2: Integration tests for orchestration pipeline**
- Status: [CAN_CHECK ✅ | CANNOT_CHECK ❌]
- Evidence: [test output or issue]

**Checkbox 3: Performance tests validating <500ms**
- Status: [CAN_CHECK ✅ | CANNOT_CHECK ❌]
- Evidence: [test output or issue]

**Checkbox 4: Error scenario tests with meaningful messages**
- Status: [CAN_CHECK ✅ | CANNOT_CHECK ❌]
- Evidence: [test output or issue]

**Checkbox 5: End-to-end test: GitHub issue creation**
- Status: [CAN_CHECK ✅ | CANNOT_CHECK ❌]
- Evidence: [test output or issue]

## Critical Standards

**CAN_CHECK means**:
- ✅ Tests collect without errors
- ✅ Tests execute completely
- ✅ Tests pass all assertions
- ✅ Evidence provided (terminal output)

**CANNOT_CHECK means**:
- ❌ Tests fail (even if collect/execute)
- ❌ Missing functionality
- ❌ Requires additional work

## Success Criteria
- Complete test execution results for all Testing Phase categories
- Honest assessment of what can be checked vs what needs more work
- Clear evidence for PM to validate checkboxes
- Identification of any remaining blockers

Report with brutal honesty - we need truth for checkbox validation.
