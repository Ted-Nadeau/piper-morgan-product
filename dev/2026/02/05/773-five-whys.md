# Five Whys Analysis: #773 Schema Drift Validator False Positive

**Date**: 2026-02-05
**Issue**: #773 - Schema drift validator false positive: DateTime vs timestamptz

## The Problem

Schema drift validator reports 72 mismatches for DateTime columns after timestamptz migration, even though the schema is correct.

## Five Whys

### 1. Why does the validator report DateTime vs timestamptz as a mismatch?
Because `timestamptz` is not in the list of compatible types for `DateTime` in TYPE_MAPPING.

### 2. Why isn't `timestamptz` in the compatible types list?
The TYPE_MAPPING at line 89 lists: `["timestamp without time zone", "timestamp with time zone", "timestamp"]` - these are `data_type` values, not `udt_name` values.

### 3. Why does this matter?
The validator uses `udt_name` (line 264: `schema_type = schema_col["udt_name"]`) for comparison, not `data_type`. PostgreSQL stores:
- `data_type` = "timestamp with time zone"
- `udt_name` = "timestamptz"

### 4. Why wasn't this caught before?
Before Issue #771's migration (`d73b3722eb03_convert_timestamps_to_timestamptz.py`), columns were `timestamp without time zone` which has `udt_name` = "timestamp" - that WAS in the list.

### 5. Why did the original mapping use data_type values?
Likely a misunderstanding of PostgreSQL's information_schema. The validator was written to query `udt_name` but the mapping was populated with `data_type` values. For most types these overlap, but timestamps are different:

| SQLAlchemy | data_type | udt_name |
|------------|-----------|----------|
| DateTime | timestamp without time zone | timestamp |
| DateTime(timezone=True) | timestamp with time zone | timestamptz |

## Root Cause

**TYPE_MAPPING mismatch**: The DateTime entry uses `data_type` naming convention while the comparison uses `udt_name`. Adding `"timestamptz"` to the DateTime compatible types list will fix this.

## Evidence

```sql
SELECT column_name, data_type, udt_name
FROM information_schema.columns
WHERE table_name = 'users' AND column_name LIKE '%_at';

-- Result:
-- created_at | timestamp with time zone | timestamptz
-- updated_at | timestamp with time zone | timestamptz
```

## Fix

**One-line fix**: Add `"timestamptz"` to the DateTime compatible types in TYPE_MAPPING:

```python
# Before (line 89):
"DateTime": ["timestamp without time zone", "timestamp with time zone", "timestamp"],

# After:
"DateTime": ["timestamp without time zone", "timestamp with time zone", "timestamp", "timestamptz"],
```

## Verification

After fix, running the validator should show 0 mismatches for DateTime/timestamptz columns.
