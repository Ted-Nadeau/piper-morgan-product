# Gameplan: #773 Schema Drift Validator False Positive

**Issue**: #773 - Schema drift validator false positive: DateTime vs timestamptz
**Date**: 2026-02-05

## Problem Statement

Schema drift validator reports 72 false positives for DateTime columns after the timestamptz migration because the TYPE_MAPPING doesn't include `"timestamptz"` (the PostgreSQL `udt_name` for timezone-aware timestamps).

## Five Whys Summary

Root cause: TYPE_MAPPING uses `data_type` naming ("timestamp with time zone") but validator compares against `udt_name` ("timestamptz").

## Files to Modify

| File | Change |
|------|--------|
| `services/infrastructure/schema_validator.py` | Add "timestamptz" to DateTime mapping |

## Solution Approach

This is a one-line fix: add `"timestamptz"` to the DateTime compatible types list in TYPE_MAPPING.

---

## Phase 1: Fix TYPE_MAPPING

**File**: `services/infrastructure/schema_validator.py`
**Line**: 89

```python
# Before:
"DateTime": ["timestamp without time zone", "timestamp with time zone", "timestamp"],

# After:
"DateTime": ["timestamp without time zone", "timestamp with time zone", "timestamp", "timestamptz"],
```

---

## Phase Z: Verification

### Success Criteria

- [ ] Schema validator passes with 0 mismatches for DateTime columns
- [ ] Server starts without schema drift warnings
- [ ] Existing unit tests pass

### Test Plan

1. Run validator directly: `python -c "from services.infrastructure.schema_validator import SchemaValidator; import asyncio; v = SchemaValidator(); asyncio.run(v.validate()); print(v.get_report())"`
2. Start server and check logs for schema drift warnings
3. Run unit tests: `pytest tests/unit/services/infrastructure/test_schema_validator.py -v`

### Rollback Plan

Revert single line change in `services/infrastructure/schema_validator.py`.

---

## Out of Scope

- Adding other missing udt_name mappings (only DateTime has this issue currently)
- Refactoring validator to use data_type instead of udt_name

---

## Work Characteristics

- **Scope**: Single-line fix in one file
- **Risk**: Low - additive change to type mapping
- **Duration**: < 15 minutes
- **Worktree**: Skip (trivial fix)
