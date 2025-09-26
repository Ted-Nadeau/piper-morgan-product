# Agent Prompt: Fix LLM Classifier Constructor Bug

## Mission
Fix the constructor parameter mismatch in LLM classifier that's blocking test execution.

## The Bug (Found in Investigation)
**File**: `services/intent_service/llm_classifier.py`
**Line**: 364
**Problem**: Using wrong parameter name for Intent constructor

**Current (WRONG)**:
```python
intent = Intent(
    message=original_message,  # ❌ Intent doesn't have 'message' parameter
    category=IntentCategory(classification_result["category"].lower()),
    action=classification_result["action"],
    confidence=confidence,
    # ...
)
```

**Should be**:
```python
intent = Intent(
    original_message=original_message,  # ✅ Correct parameter name
    category=IntentCategory(classification_result["category"].lower()),
    action=classification_result["action"],
    confidence=confidence,
    # ...
)
```

## Implementation

### 1. Verify Current State
```bash
cd /Users/xian/Development/piper-morgan

# Show the current bug
grep -n "message=original_message" services/intent_service/llm_classifier.py
```

### 2. Apply Fix
Change line 364 from:
```python
message=original_message,
```

to:
```python
original_message=original_message,
```

### 3. Verify Fix Applied
```bash
# Confirm the change
grep -n "original_message=original_message" services/intent_service/llm_classifier.py

# Verify no more message= usage in Intent constructor
grep -A 5 "intent = Intent(" services/intent_service/llm_classifier.py | grep "message="
```

### 4. Run Tests to Verify
```bash
# Run the specific failing test
PYTHONPATH=. python -m pytest tests/unit/services/intent_service/test_llm_intent_classifier.py::TestLLMIntentClassifier::test_successful_classification_with_high_confidence -v

# Run full LLM classifier test suite
PYTHONPATH=. python -m pytest tests/unit/services/intent_service/test_llm_intent_classifier.py -v

# Run LLM performance benchmark that was failing
PYTHONPATH=. python -m pytest tests/performance/test_llm_classifier_benchmarks.py -v
```

## Evidence Requirements

### Fix Application
```
Before:
Line 364: message=original_message,

After:
Line 364: original_message=original_message,

Verification:
[paste grep output showing change]
```

### Test Results
```
LLM Classifier Tests:
[paste pytest output]

Status: [ALL_PASSING | SOME_FAILING]
Count: X passed, Y failed

Performance Benchmark:
[paste pytest output]

Status: [PASSING | FAILING]
Performance: [<500ms | violation | N/A]
```

## Success Criteria
- ✅ Constructor parameter corrected
- ✅ TypeError: unexpected keyword 'message' GONE
- ✅ LLM classifier tests execute (may have other failures, but constructor works)
- ✅ Can assess if JSON parsing issues remain

## Expected Outcome

This fix should:
1. Eliminate the TypeError
2. Allow tests to execute past constructor
3. Reveal if there are additional issues (JSON parsing, confidence scores, etc.)

Report findings with before/after evidence and test execution results.
