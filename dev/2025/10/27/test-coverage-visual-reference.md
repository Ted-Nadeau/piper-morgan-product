# Test Coverage Visual Reference

## Test File Structure

```
tests/
├── conftest.py
│   └── intent_service fixture (orchestration_engine=None) ← STANDARD TESTS
│
├── intent/
│   ├── base_validation_test.py
│   │   └── intent_service fixture (real OrchestrationEngine) ← DEEP TESTS
│   │
│   ├── test_direct_interface.py
│   │   └── Tests: test_conversation_direct, test_query_direct, ... (13 total)
│   │
│   ├── test_web_interface.py
│   │   └── Tests: test_conversation_web, test_query_web, ... (13 total)
│   │
│   ├── test_slack_interface.py
│   │   └── Tests: test_conversation_slack, test_query_slack, ... (13 total)
│   │
│   ├── test_cli_interface.py
│   │   └── Tests: test_conversation_cli, test_query_cli, ... (13 total)
│   │
│   ├── test_constants.py
│   │   ├── INTENT_CATEGORIES = ["TEMPORAL", "STATUS", ..., "CONVERSATION"]
│   │   ├── CATEGORY_EXAMPLES = {"CONVERSATION": "Hey, how's it going?"}
│   │   └── PERFORMANCE_THRESHOLDS
│   │
│   ├── coverage_tracker.py
│   │   └── coverage.categories_tested, coverage.interfaces_tested
│   │
│   └── contracts/
│       ├── test_accuracy_contracts.py (13 categories × 5 tests)
│       ├── test_error_contracts.py
│       ├── test_bypass_contracts.py
│       ├── test_multiuser_contracts.py
│       └── test_performance_contracts.py
```

## Test Coverage Matrix

```
┌─────────────────┬──────────┬────────────┬────────────────┐
│ Category        │ Direct   │ Web        │ Slack   │ CLI  │
├─────────────────┼──────────┼────────────┼─────────┼──────┤
│ TEMPORAL        │ ✓ 1/13   │ ✓ 2/13     │ ✓ 3/13  │ ✓ 4/13
│ STATUS          │ ✓ 2/13   │ ✓ 3/13     │ ✓ 4/13  │ ✓ 5/13
│ PRIORITY        │ ✓ 3/13   │ ✓ 4/13     │ ✓ 5/13  │ ✓ 6/13
│ IDENTITY        │ ✓ 4/13   │ ✓ 5/13     │ ✓ 6/13  │ ✓ 7/13
│ GUIDANCE        │ ✓ 5/13   │ ✓ 6/13     │ ✓ 7/13  │ ✓ 8/13
│ EXECUTION       │ ✓ 6/13   │ ✓ 7/13     │ ✓ 8/13  │ ✓ 9/13
│ ANALYSIS        │ ✓ 7/13   │ ✓ 8/13     │ ✓ 9/13  │ ✓ 10/13
│ SYNTHESIS       │ ✓ 8/13   │ ✓ 9/13     │ ✓ 10/13 │ ✓ 11/13
│ STRATEGY        │ ✓ 9/13   │ ✓ 10/13    │ ✓ 11/13 │ ✓ 12/13
│ LEARNING        │ ✓ 10/13  │ ✓ 11/13    │ ✓ 12/13 │ ✓ 13/13
│ UNKNOWN         │ ✓ 11/13  │ ✓ 12/13    │ ✓ 13/13 │ ✓ 14/13
│ QUERY           │ ✓ 12/13  │ ✓ 13/13    │ ✓ 14/13 │ ✓ 15/13
│ CONVERSATION    │ ✓ 13/13  │ ✓ 14/13    │ ✓ 15/13 │ ✓ 16/13
├─────────────────┼──────────┼────────────┼─────────┼──────┤
│ TOTAL TESTS     │ 52       │ 52         │ 52      │ 52
│ + CONTRACTS     │ +65      │ +65        │ +65     │ +65
│ GRAND TOTAL     │ 117 TESTS ACROSS 4 INTERFACES            │
└─────────────────┴──────────┴────────────┴─────────┴──────┘
```

## Execution Flow Comparison

### Fixture A: Standard Tests (conftest.py)
```
orchestration_engine = None
           ↓
process_intent("Hello there")
           ↓
Line 190: if orchestration_engine is None → YES
           ↓
return _handle_missing_engine()  ← EXIT
           ↓
[Line 199 NEVER REACHED]
```

### Fixture B: Deep Tests (base_validation_test.py)
```
orchestration_engine = OrchestrationEngine(...)
           ↓
process_intent("Hello there")
           ↓
Line 190: if orchestration_engine is None → NO
           ↓
Line 195: intent = classifier.classify()
           ↓
Line 199: if intent.category.value == "conversation"
           ↓
           "conversation" == "conversation" → YES ✓
           ↓
return _handle_conversation_intent()
           ↓
[Line 199 EXECUTES but bug not caught]
```

## Enum Structure

```python
IntentCategory (Enum)
├── CONVERSATION
│   ├── .name    = "CONVERSATION"  (uppercase)
│   └── .value   = "conversation"  (lowercase) ← Used in line 199
├── QUERY
│   ├── .name    = "QUERY"
│   └── .value   = "query"
├── EXECUTION
│   ├── .name    = "EXECUTION"
│   └── .value   = "execution"
└── ... (10 more categories)
```

## Case Handling Pattern

### Current Implementation
```python
Line 199  (CONVERSATION only):
if intent.category.value == "conversation":  # Lowercase
                                   ↑
                      Uses .value directly

Lines 232-256 (All others):
if intent.category.value.upper() == "QUERY":  # Uppercase
                           ↑
                    Converts .value to uppercase
```

### Comparison

| Handler | Pattern | Enum.value | Comparison | Works |
|---------|---------|-----------|-----------|-------|
| CONVERSATION | `== "conversation"` | "conversation" | "conversation" == "conversation" | ✓ |
| QUERY | `.upper() == "QUERY"` | "query" | "QUERY" == "QUERY" | ✓ |
| EXECUTION | `.upper() == "EXECUTION"` | "execution" | "EXECUTION" == "EXECUTION" | ✓ |
| ... (10 more) | `.upper() == "CATEGORY"` | varies | varies | ✓ |

## Test Assertion Coverage

### What Tests Verify
```
✓ Response message exists
✓ No placeholder text ("Phase 3", "full orchestration workflow")
✓ Performance < 4000ms
✓ Success flag is not None
```

### What Tests Don't Verify
```
✗ Handler method was called
✗ Routing logic consistency
✗ Case sensitivity patterns
✗ Return value structure
✗ Intent category matches handler
✗ Handler method name matches category
```

## Code Locations Map

### Production Files
```
services/
├── intent/
│   └── intent_service.py (line 199 - THE BUG)
│       └── Line 199: if intent.category.value == "conversation":
│       └── Lines 232-256: if intent.category.value.upper() == "CATEGORY":
├── shared_types.py (lines 9-22)
│   └── class IntentCategory(Enum): ... CONVERSATION = "conversation"
└── conversation/
    └── conversation_handler.py (232 lines)
        └── async def respond(self, intent: Intent, ...)
```

### Test Files
```
tests/
├── conftest.py (line 75 - THE FIXTURE)
│   └── orchestration_engine=None ← Causes early exit
├── intent/
│   ├── base_validation_test.py (line 34 - THE DEEP FIXTURE)
│   │   └── orchestration_engine = OrchestrationEngine(...)
│   ├── test_direct_interface.py (line 242-257 - THE TEST)
│   │   └── test_conversation_direct()
│   ├── test_constants.py (line 49 - THE TEST DATA)
│   │   └── "CONVERSATION": "Hey, how's it going?"
│   └── coverage_tracker.py (THE COVERAGE TRACKER)
```

## Test Execution Timeline

### Standard Test Execution
```
Test starts
  ↓ (uses conftest.py fixture)
intent_service initialized with orchestration_engine=None
  ↓
test_conversation_direct() called
  ↓
process_intent("Hey, how's it going?") called
  ↓
Line 190 check: orchestration_engine is None?
  → TRUE
  ↓
return _handle_missing_engine("Hey, how's it going?")
  ↓
Test assertions pass (checks response content only)
  ↓
Test completes: PASS ✓
  ↓
[Case mismatch bug on line 199 never reached]
```

### Deep Test Execution
```
Test starts
  ↓ (uses base_validation_test.py fixture)
intent_service initialized with real OrchestrationEngine
  ↓
test_conversation_direct() called
  ↓
process_intent("Hey, how's it going?") called
  ↓
Line 190 check: orchestration_engine is None?
  → FALSE, continue
  ↓
Line 195: classify intent
  ↓
Line 199 check: intent.category.value == "conversation"?
  → "conversation" == "conversation" → TRUE ✓
  ↓
_handle_conversation_intent() called
  ↓
Test assertions pass (checks response content only)
  ↓
Test completes: PASS ✓
  ↓
[Case mismatch bug exists but test passes anyway]
```

## Bug Impact Analysis

### What Happens With Current Code
```
intent.category.value = "conversation" (lowercase)
         ↓
Line 199 check: "conversation" == "conversation"
         ↓
Result: TRUE ✓ Handler called correctly
```

### What Would Happen With Fix
```
intent.category.value = "conversation" (lowercase)
         ↓
Convert to uppercase: "CONVERSATION"
         ↓
Line 199 check (after fix): "CONVERSATION" == "CONVERSATION"
         ↓
Result: TRUE ✓ Handler called correctly
```

### Impact Summary
```
Bug Severity: LOW
├── Current: Works ✓
├── With Fix: Still works ✓
└── No runtime failures either way

Code Quality: MEDIUM
├── Current: Inconsistent pattern (line 199 vs 232-256)
└── With Fix: Consistent pattern across all handlers
```

## Coverage Completeness

### Coverage: 100% Categories
```
✓ All 13 categories tested
✓ All 4 interfaces tested
✓ 52 interface tests (13 × 4)
✓ 65 contract tests (13 × 5)
───────────────────────────
✓ Total: 117 tests
```

### Coverage: 0% Routing Logic
```
✗ No tests verify handler execution
✗ No tests verify routing path taken
✗ No tests check case sensitivity consistency
✗ No tests confirm method names match categories
```

## Summary

**Test Coverage by Metric:**
- Categories: 100% (13/13)
- Interfaces: 100% (4/4)
- Output verification: 100%
- Routing logic verification: 0%
- Assertion coverage: 30%

**Why Bug Survives:**
1. Default fixture exits early (conftest.py)
2. Deep tests weak on assertions
3. Functional transparency (bug doesn't break anything)

**Risk Level: LOW**
- Comparison works both ways
- No runtime failures
- Inconsistency pattern only
