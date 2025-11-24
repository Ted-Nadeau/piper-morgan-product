# CORE-BOUNDARIES-MISMATCH: Fix adaptive_boundaries Type Mismatch

**Issue #263**
**Labels**: `bug`, `ethics`, `boundary-enforcement`, `alpha`, `tech-debt`
**Milestone**: Alpha
**Priority**: Medium
**Discovered During**: Issue #257 (CORE-KNOW-BOUNDARY-COMPLETE)
**Sprint**: A8 or later (low urgency)

---

## Summary

The `adaptive_boundaries.get_adaptive_patterns()` method returns `List[str]` but calling code in `boundary_enforcer.py` expects `Dict[str, Any]`, causing an AttributeError when trying to access dictionary keys on a list object.

This is a **pre-existing bug** discovered during Issue #257 work. It does NOT block Issue #257 completion because the knowledge graph integration uses different boundary enforcement methods (content-based checking).

---

## Error

```
AttributeError: 'list' object has no attribute 'get'
```

**Test Failure**:
```bash
tests/ethics/test_boundary_enforcer_integration.py::TestBoundaryEnforcer::test_enforce_boundaries_no_violation
FAILED - AttributeError: 'list' object has no attribute 'get'
```

---

## Location

**File**: `services/ethics/boundary_enforcer.py`
**Lines**: 133 (call site), 282 (error site)

---

## Root Cause Analysis

### The Type Mismatch

**Line 133** - `adaptive_boundaries.get_adaptive_patterns()` is called and returns `List[str]`:
```python
# services/ethics/boundary_enforcer.py:133
adaptive_enhancement = await adaptive_boundaries.get_adaptive_patterns(
    boundary_type or "none"
)
```

**Line 282** - Code expects `Dict` but receives `List`:
```python
# services/ethics/boundary_enforcer.py:282
adaptive_adjustment = adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)
# ❌ Error: 'list' object has no attribute 'get'
```

### The Source of the Bug

**Method Definition**:
```python
# services/ethics/adaptive_boundaries.py:151
async def get_adaptive_patterns(self, boundary_type: str) -> List[str]:
    """Get learned patterns for a boundary type"""
    patterns = []
    # ... builds list of pattern strings
    return patterns  # Returns List[str], NOT Dict
```

**Type Signature**: `-> List[str]` (explicitly typed as list)

---

## Where Used

This bug exists in **two locations**:

1. **`services/ethics/boundary_enforcer.py:133`** (active version)
   - Currently in production use
   - Causes test failure

2. **`services/ethics/boundary_enforcer_refactored.py:181`** (has comment about bug)
   - Refactored version with TODO comment acknowledging issue
   - Not currently active

---

## Impact

- **Severity**: Medium (not currently blocking)
- **Blocking**: NO - Issue #257 knowledge graph integration uses different methods
- **Test Impact**: 1 test failure in ethics layer (not knowledge layer)
- **Workaround**: Use content-based methods (`check_harassment_patterns`, `check_inappropriate_content`) instead of Request-based enforcement

### Why NOT Blocking Issue #257

Issue #257 implementation used:
- ✅ `boundary_enforcer.check_harassment_patterns(content)` (works)
- ✅ `boundary_enforcer.check_inappropriate_content(content)` (works)

Did NOT use:
- ❌ `adaptive_boundaries.get_adaptive_patterns()` (has bug)

---

## Proposed Fix

### Option A: Change Return Type to Dict (RECOMMENDED)

**Rationale**: Calling code expects dictionary with adaptive learning metadata

```python
# services/ethics/adaptive_boundaries.py:151
async def get_adaptive_patterns(self, boundary_type: str) -> Dict[str, Any]:
    """Get learned patterns for a boundary type with adaptive metadata"""
    patterns_list = []
    # ... build patterns list

    return {
        "patterns": patterns_list,  # List[str] of pattern strings
        "adaptive_confidence_adjustment": 0.0,  # Float for confidence tuning
        "boundary_type": boundary_type,  # String for context
        "pattern_count": len(patterns_list),  # Int for stats
        # ... other adaptive learning fields
    }
```

**Pros**:
- Matches caller expectations
- Allows future adaptive learning metadata
- More extensible design

**Cons**:
- Breaking change (need to update all callers)
- More complex return type

### Option B: Change Calling Code to Handle List

**Rationale**: Maintain current return type, fix caller defensively

```python
# services/ethics/boundary_enforcer.py:282
# Defensive handling of List vs Dict
adaptive_adjustment = 0.0  # Default value
if isinstance(adaptive_enhancement, dict):
    adaptive_adjustment = adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)
elif isinstance(adaptive_enhancement, list):
    # List of patterns - no adjustment value available
    adaptive_adjustment = 0.0
```

**Pros**:
- Minimal change
- Backward compatible
- Quick fix

**Cons**:
- Loses adaptive learning metadata
- Band-aid solution
- Doesn't fix underlying design issue

### Recommendation: Option A

**Why**: The calling code clearly expects adaptive learning metadata (confidence adjustments), which requires a dictionary return type. Option A aligns the implementation with the intended design.

---

## Acceptance Criteria

- [ ] Type mismatch resolved (return type OR calling code fixed)
- [ ] Test passes: `test_enforce_boundaries_no_violation`
- [ ] Both instances updated:
  - [ ] `boundary_enforcer.py:133,282`
  - [ ] `boundary_enforcer_refactored.py:181` (if still active)
- [ ] No regressions in other ethics tests
- [ ] Type hints updated to match implementation
- [ ] Documentation updated (docstrings)

---

## Testing

### Verify Fix
```bash
# Test the specific failing test
pytest tests/ethics/test_boundary_enforcer_integration.py::TestBoundaryEnforcer::test_enforce_boundaries_no_violation -xvs

# Verify type consistency
python -c "
from services.ethics.adaptive_boundaries import AdaptiveBoundaries
import asyncio
ab = AdaptiveBoundaries()
result = asyncio.run(ab.get_adaptive_patterns('test'))
print(f'Type: {type(result).__name__}')
print(f'Value: {result}')
"
```

### Full Ethics Suite
```bash
# Run all boundary enforcer tests
pytest tests/ethics/ -v

# Check for regressions
pytest tests/ethics/test_boundary_enforcer_framework.py -v
pytest tests/ethics/test_boundary_enforcer_integration.py -v
```

---

## Implementation Estimate

**Effort**: Small (1-2 hours)

**Breakdown**:
- Fix implementation: 15 min
- Update both files: 10 min
- Test verification: 20 min
- Regression testing: 15 min

**Low urgency** - can be tackled in Sprint A8 or later

---

## Related Context

### Discovery Timeline

**Discovered by**: Claude Code (prog-code)
**Date**: October 23, 2025, 8:15 AM PDT
**During**: Issue #257 implementation (Sprint A7 Group 1)

**Context**: While implementing boundary enforcement for knowledge graph operations, discovered pre-existing type mismatch in ethics layer. Did NOT block #257 because knowledge graph uses different boundary methods.

### Related Issues

- **Issue #257**: CORE-KNOW-BOUNDARY-COMPLETE (where bug was discovered)
- **Sprint A7**: Groups 1-2 (Critical Fixes + CORE-USER)

### Related Files

**Source Files**:
- `services/ethics/adaptive_boundaries.py` (method definition)
- `services/ethics/boundary_enforcer.py` (bug location)
- `services/ethics/boundary_enforcer_refactored.py` (has comment about bug)

**Test Files**:
- `tests/ethics/test_boundary_enforcer_integration.py` (failing test)
- `tests/ethics/test_boundary_enforcer_framework.py` (regression check)

---

## Code References

### Current Implementation (Buggy)

**Method Definition** (services/ethics/adaptive_boundaries.py:151):
```python
async def get_adaptive_patterns(self, boundary_type: str) -> List[str]:
    """Get learned patterns for a boundary type"""
    patterns = []
    # ... implementation
    return patterns
```

**Caller** (services/ethics/boundary_enforcer.py:133,282):
```python
# Line 133: Call site
adaptive_enhancement = await adaptive_boundaries.get_adaptive_patterns(
    boundary_type or "none"
)

# Line 282: Error site
adaptive_adjustment = adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)
# ❌ AttributeError: 'list' object has no attribute 'get'
```

---

## Notes

- This is **tech debt** from adaptive learning implementation
- Pre-existing before Issue #257
- Not blocking current sprint work
- Good candidate for A8 polish sprint

---

**Issue Created**: October 23, 2025, 11:41 AM PDT
**Created By**: Claude Code (prog-code)
**File**: `dev/active/CORE-BOUNDARIES-MISMATCH-issue-263.md`
