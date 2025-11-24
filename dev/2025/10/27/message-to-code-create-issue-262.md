# Code: Please Create GitHub Issue #262

**Task**: Write GitHub issue for pre-existing bug discovered during #257

---

## Bug Discovery

You discovered a pre-existing bug while working on Issue #257:

**Bug**: `adaptive_boundaries.get_adaptive_patterns()` returns `List[str]` but code expects `Dict`

**Location**: `services/ethics/boundary_enforcer.py:282`

**Impact**: NOT blocking #257 (your changes used different methods), but causes test failure in ethics layer

---

## Request

Please create a new GitHub issue **#262** for this bug using the information from your Checkpoint 1 report.

### Issue Template

Use this structure:

```markdown
# Issue #262: Fix adaptive_boundaries Type Mismatch

**Labels**: `bug`, `ethics`, `boundary-enforcement`, `alpha`
**Milestone**: Alpha (or Sprint A8)
**Priority**: Medium
**Discovered During**: Issue #257 (CORE-KNOW-BOUNDARY-COMPLETE)

---

## Summary

The `adaptive_boundaries.get_adaptive_patterns()` method returns `List[str]` but calling code expects `Dict`, causing an AttributeError.

## Error

```
AttributeError: 'list' object has no attribute 'get'
```

## Location

**File**: `services/ethics/boundary_enforcer.py`
**Line**: 282

## Root Cause

[Paste your analysis from Checkpoint 1 report]

**Code**:
```python
# Line 133: adaptive_boundaries.get_adaptive_patterns() returns List[str]
adaptive_enhancement = await adaptive_boundaries.get_adaptive_patterns(
    boundary_type or "none"
)

# Line 282: Code expects Dict, but receives List
adaptive_adjustment = adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)
```

**Source of bug**:
```python
# services/ethics/adaptive_boundaries.py:151
async def get_adaptive_patterns(self, boundary_type: str) -> List[str]:
    """Get learned patterns for a boundary type"""
    patterns = []
    # ... returns List[str], not Dict
    return patterns
```

## Impact

- **Severity**: Medium (not currently blocking)
- **Test Failure**: `tests/ethics/test_boundary_enforcer_integration.py::TestBoundaryEnforcer::test_enforce_boundaries_no_violation`
- **Workaround**: Use content-based methods instead of Request-based enforcement

## Where Used

- `services/ethics/boundary_enforcer.py:133` (active version)
- `services/ethics/boundary_enforcer_refactored.py:181` (has comment about this bug)

## Proposed Fix

**Option A**: Change return type to Dict
```python
async def get_adaptive_patterns(self, boundary_type: str) -> Dict[str, Any]:
    """Get learned patterns for a boundary type"""
    patterns = {
        "patterns": [],
        "adaptive_confidence_adjustment": 0.0,
        # ... other fields
    }
    return patterns
```

**Option B**: Change calling code to handle List
```python
# Line 282 in boundary_enforcer.py
adaptive_adjustment = 0.0  # Default since patterns is a List
if isinstance(adaptive_enhancement, dict):
    adaptive_adjustment = adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)
```

## Acceptance Criteria

- [ ] Type mismatch resolved (either fix return type or calling code)
- [ ] Test passes: `test_enforce_boundaries_no_violation`
- [ ] Both instances updated (boundary_enforcer.py and boundary_enforcer_refactored.py)
- [ ] No regressions in other ethics tests

## Testing

```bash
# Verify fix
pytest tests/ethics/test_boundary_enforcer_integration.py::TestBoundaryEnforcer::test_enforce_boundaries_no_violation -v

# Full ethics suite
pytest tests/ethics/ -v
```

---

**Discovered by**: Claude Code (prog-code)
**Date**: October 23, 2025, 8:15 AM
**Related Issue**: #257 (CORE-KNOW-BOUNDARY-COMPLETE)
```

---

## Instructions

1. **Create the issue file**: `dev/active/adaptive-boundaries-type-mismatch-issue.md`
2. **Use your Checkpoint 1 report** as the source of truth
3. **Include all evidence** (error messages, code snippets, locations)
4. **Recommend a fix** (Option A or B, your choice)
5. **Link to #257** (discovered during that work)

---

## Questions?

If you need any clarification or want to discuss the recommended fix approach, just ask!

---

**Priority**: Low urgency (can be tackled in Sprint A8 or later)
**Estimated Effort**: Small (1-2 hours to fix + test)
