# Issue #262: Fix adaptive_boundaries Type Mismatch

**Labels**: `bug`, `ethics`, `boundary-enforcement`, `alpha`
**Milestone**: Alpha (Sprint A8 or later)
**Priority**: Medium
**Discovered During**: Issue #257 (CORE-KNOW-BOUNDARY-COMPLETE)
**Discovered By**: Claude Code (prog-code)
**Date**: October 23, 2025, 8:15 AM PDT

---

## Summary

The `adaptive_boundaries.get_adaptive_patterns()` method returns `List[str]` but calling code in `boundary_enforcer.py` expects `Dict[str, Any]`, causing an AttributeError when trying to access dictionary keys.

## Error

```
AttributeError: 'list' object has no attribute 'get'
```

**Stack Trace**:
```
tests/ethics/test_boundary_enforcer_integration.py:46: in test_enforce_boundaries_no_violation
    decision = await boundary_enforcer.enforce_boundaries(mock_request)
services/ethics/boundary_enforcer.py:140: in enforce_boundaries
    harassment_result = await self._enhanced_harassment_check(content, adaptive_enhancement)
services/ethics/boundary_enforcer.py:282: in _enhanced_harassment_check
    adaptive_adjustment = adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)
E   AttributeError: 'list' object has no attribute 'get'
```

## Location

**Primary File**: `services/ethics/boundary_enforcer.py`
**Problem Lines**: 133 (call site), 282 (usage site)

## Root Cause

### The Bug

**Line 133** calls `get_adaptive_patterns()` and expects a Dict:
```python
# services/ethics/boundary_enforcer.py:133
adaptive_enhancement = await adaptive_boundaries.get_adaptive_patterns(
    boundary_type or "none"
)
```

**Line 282** tries to use it as a Dict:
```python
# services/ethics/boundary_enforcer.py:282
async def _enhanced_harassment_check(
    self, content: str, adaptive_enhancement: Dict[str, Any]  # ← Type hint says Dict
) -> Dict[str, Any]:
    # ...
    adaptive_adjustment = adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)
    # ↑ Tries to call .get() on what is actually a List[str]
```

**Lines 306-331** also expect Dict:
```python
# Line 306: _enhanced_professional_check
if adaptive_enhancement.get("recommendation") == "extra_caution":
    # ...

# Line 328: _enhanced_inappropriate_content_check
contextual_factor = adaptive_enhancement.get("contextual_risk_factor", 1.0)
```

### The Source

**Line 151** in `adaptive_boundaries.py` returns `List[str]`, not `Dict`:
```python
# services/ethics/adaptive_boundaries.py:151
async def get_adaptive_patterns(self, boundary_type: str) -> List[str]:
    """Get learned patterns for a boundary type"""
    patterns = []

    for pattern_hash, metadata in self.learned_patterns.items():
        if (
            metadata.boundary_type == boundary_type
            and metadata.confidence_score >= self.confidence_threshold
            and metadata.frequency >= self.min_frequency_threshold
        ):
            patterns.append(pattern_hash)  # ← Appending strings to list

    return patterns  # ← Returns List[str], not Dict
```

## Impact

**Severity**: Medium (pre-existing, not currently blocking)

**Test Failure**:
- `tests/ethics/test_boundary_enforcer_integration.py::TestBoundaryEnforcer::test_enforce_boundaries_no_violation` ❌ FAILS

**Workaround**:
- Issue #257 worked around this by using content-based methods (`check_harassment_patterns`, `check_inappropriate_content`) instead of Request-based `enforce_boundaries`
- The content-based methods don't use adaptive_boundaries, so #257 is not blocked

**Current Status**:
- Ethics boundary enforcement via `enforce_boundaries()` broken
- Content-based boundary checks work fine
- Knowledge graph integration (Issue #257) complete using workaround

## Where Used

### Primary Instance (Active)
- **File**: `services/ethics/boundary_enforcer.py:133`
- **Status**: ❌ Broken (test failing)
- **Usage**: Request-based boundary enforcement with adaptive learning

### Secondary Instance (Has Comment About Bug)
- **File**: `services/ethics/boundary_enforcer_refactored.py:181`
- **Status**: ✅ Has comment acknowledging issue
- **Comment**: `"# FIXED (Phase 2B): Handle type mismatch - get_adaptive_patterns returns List[str], not Dict"`
- **Code**: Uses workaround

```python
# services/ethics/boundary_enforcer_refactored.py:181-183
# FIXED (Phase 2B): Handle type mismatch - get_adaptive_patterns returns List[str], not Dict
# Use patterns for enhanced detection, not as a dictionary
adaptive_patterns = await adaptive_boundaries.get_adaptive_patterns(boundary_type or "none")
```

## Proposed Fix

### Option A: Change Return Type to Dict (RECOMMENDED)

Update `adaptive_boundaries.py` to return a structured Dict with all expected fields:

```python
# services/ethics/adaptive_boundaries.py:151
async def get_adaptive_patterns(self, boundary_type: str) -> Dict[str, Any]:
    """
    Get adaptive enhancement data for a boundary type.

    Returns:
        Dict with:
        - patterns: List[str] of learned pattern hashes
        - adaptive_confidence_adjustment: float confidence delta
        - temporal_risk_factor: float temporal risk multiplier
        - contextual_risk_factor: float contextual risk multiplier
        - recommendation: str ("proceed", "extra_caution", "proceed_with_confidence")
        - learned_patterns_matched: int count of patterns matched
    """
    patterns = []

    for pattern_hash, metadata in self.learned_patterns.items():
        if (
            metadata.boundary_type == boundary_type
            and metadata.confidence_score >= self.confidence_threshold
            and metadata.frequency >= self.min_frequency_threshold
        ):
            patterns.append(pattern_hash)

    # Calculate adaptive enhancements
    confidence_adjustment = len(patterns) * 0.05  # +5% per pattern
    risk_factor = 1.0 + (len(patterns) * 0.1)  # 10% increase per pattern

    return {
        "patterns": patterns,
        "adaptive_confidence_adjustment": min(0.3, confidence_adjustment),  # Cap at +30%
        "temporal_risk_factor": 1.0,  # Could be time-based
        "contextual_risk_factor": risk_factor,
        "recommendation": "proceed_with_confidence" if len(patterns) > 3 else "proceed",
        "learned_patterns_matched": len(patterns)
    }
```

**Pros**:
- ✅ Matches caller expectations
- ✅ Provides all expected fields
- ✅ Backward compatible if callers check for Dict
- ✅ Clean API

**Cons**:
- ⚠️ Requires understanding expected fields (documented above)

### Option B: Change Calling Code to Handle List

Update `boundary_enforcer.py` to handle List return type:

```python
# services/ethics/boundary_enforcer.py:282
async def _enhanced_harassment_check(
    self, content: str, adaptive_enhancement: Union[List[str], Dict[str, Any]]
) -> Dict[str, Any]:
    """Enhanced harassment detection with confidence scoring"""
    content_lower = content.lower()
    base_confidence = 0.0
    matched_patterns = []

    # Check base patterns
    for pattern in self.harassment_patterns:
        if pattern in content_lower:
            matched_patterns.append(pattern)
            base_confidence += 0.3

    # Apply adaptive enhancement (handle both List and Dict)
    adaptive_adjustment = 0.0
    if isinstance(adaptive_enhancement, dict):
        adaptive_adjustment = adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)
    elif isinstance(adaptive_enhancement, list):
        # If it's a list of patterns, use pattern count to adjust confidence
        adaptive_adjustment = len(adaptive_enhancement) * 0.05  # +5% per learned pattern

    final_confidence = min(1.0, base_confidence + adaptive_adjustment)

    # ... rest of method
```

**Pros**:
- ✅ Backward compatible
- ✅ Handles both return types

**Cons**:
- ❌ Duplicates logic (confidence calculation in two places)
- ❌ Unclear API contract
- ❌ Need to update multiple call sites (lines 306, 328, etc.)

### Recommendation

**Choose Option A** - Fix the return type to Dict.

**Reasoning**:
1. Clearer API contract (one source of truth)
2. Method name `get_adaptive_patterns` is misleading if it returns more than patterns
3. All callers expect Dict, so fix the source
4. Centralizes adaptive enhancement logic

## Implementation Plan

1. **Update `adaptive_boundaries.py:151`**:
   - Change return type to `Dict[str, Any]`
   - Return structured dict with all expected fields
   - Update docstring

2. **Update type hints in `boundary_enforcer.py`**:
   - Line 282: Already correct (`Dict[str, Any]`)
   - Verify other methods also expect Dict

3. **Update `boundary_enforcer_refactored.py`**:
   - Remove workaround comment
   - Update to use Dict return type

4. **Add tests**:
   - Test `get_adaptive_patterns` returns correct Dict structure
   - Test all expected fields present
   - Test boundary checks use adaptive data correctly

## Acceptance Criteria

- [ ] `adaptive_boundaries.get_adaptive_patterns()` returns `Dict[str, Any]`
- [ ] Dict contains all expected fields:
  - `patterns`: List[str]
  - `adaptive_confidence_adjustment`: float
  - `temporal_risk_factor`: float
  - `contextual_risk_factor`: float
  - `recommendation`: str
  - `learned_patterns_matched`: int
- [ ] Test passes: `tests/ethics/test_boundary_enforcer_integration.py::TestBoundaryEnforcer::test_enforce_boundaries_no_violation`
- [ ] Both instances updated:
  - `services/ethics/boundary_enforcer.py:133`
  - `services/ethics/boundary_enforcer_refactored.py:181`
- [ ] No regressions in ethics test suite
- [ ] Type hints updated throughout

## Testing

### Verify Fix
```bash
# Run failing test
pytest tests/ethics/test_boundary_enforcer_integration.py::TestBoundaryEnforcer::test_enforce_boundaries_no_violation -v

# Should PASS after fix
```

### Full Ethics Suite
```bash
# Run all ethics tests
pytest tests/ethics/ -v

# Should show improved pass rate
```

### Verify Type Contract
```python
# Test the return type
from services.ethics.adaptive_boundaries import adaptive_boundaries
result = await adaptive_boundaries.get_adaptive_patterns("harassment")
assert isinstance(result, dict), "Should return Dict"
assert "patterns" in result, "Should have patterns field"
assert "adaptive_confidence_adjustment" in result, "Should have confidence field"
```

## Related Issues

- **#257 (CORE-KNOW-BOUNDARY-COMPLETE)**: Where this bug was discovered
  - Note: #257 complete using content-based methods (workaround)
  - Knowledge graph integration not affected by this bug

## Notes

- **Not Blocking**: Issue #257 complete without this fix
- **Pre-existing**: Bug existed before Sprint A7
- **Low Priority**: Can be addressed in Sprint A8 or later
- **Estimated Effort**: Small (1-2 hours to implement + test)

---

**Status**: Open
**Assignee**: TBD
**Sprint**: A8 or later
**Created**: October 23, 2025, 10:10 AM PDT
