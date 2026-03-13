# Test Infrastructure Cleanup - Issue Catalog
## Date: November 19, 2025
## Session: test-restructure-fixes

---

## Executive Summary

**Before Restructure**: 0 tests collected from `tests/services/` (shadow package blocked collection)
**After Fixes**: 299 tests collected from `tests/unit/services/`
**Remaining Collection Errors**: 1

---

## Issues Fixed (8 files)

### 1. test_attention_scenarios_validation.py ✅
- **Issue**: Unused NavigationIntent import from wrong module
- **Fix**: Removed unused import
- **Commit**: 009712a2

### 2. test_spatial_integration.py ✅
- **Issue**: 5 test functions missing `async` keyword
- **Fix**: Added `async def` to all functions using `await`
- **Functions Fixed**:
  - test_process_unsupported_event
  - test_process_spatial_event_no_event
  - test_process_high_attention_event
  - test_process_emotional_event
  - test_process_new_room_event
- **Commit**: 009712a2

### 3. test_token_blacklist.py ✅
- **Issue**: Syntax errors - trailing comma in comment (5 occurrences)
- **Pattern**: `user_id=uuid4()  # Issue #262,` (comma after comment)
- **Fix**: Moved comma before comment: `user_id=uuid4(),  # Issue #262`
- **Lines Fixed**: 192, 212, 231, 249, 325
- **Commit**: 460937c9

### 4. test_spatial_system_integration.py ✅
- **Issue**: Malformed UUID import
- **Was**: `from attention_model import UUID, from, import, uuid, uuid4`
- **Now**: `from uuid import UUID, uuid4`
- **Commit**: d62c7d18

### 5. test_workflow_pipeline_integration.py ✅
- **Issue**: Malformed UUID import
- **Was**: `from spatial_types import UUID, from, import, uuid, uuid4`
- **Now**: `from uuid import UUID, uuid4`
- **Commit**: d62c7d18

### 6. test_api_key_validator.py ✅
- **Issue**: ValidationError imported from wrong module
- **Was**: `from api_key_validator import ValidationError`
- **Now**: `from services.api.errors import ValidationError`
- **Commit**: d62c7d18

### 7. Venv pandas corruption ✅
- **Issue**: pandas 2.3.1 had circular import error
- **Fix**: Reinstalled pandas (2.3.1 → 2.3.3)
- **Method**: `pip install --force-reinstall --no-cache-dir pandas`

---

## Remaining Collection Errors (1 file)

### 1. test_event_spatial_mapping.py 🔴 IN PROGRESS
- **Issue**: Missing `async` keywords on functions using `await`
- **Await statements found**: 13
- **Lines with await**: 63, 86, 108, 128, 151, 171, 193, 208, 245, 267, 285, 306, 325
- **Status**: Bead created (piper-morgan-dut)
- **Next**: Identify functions needing async, apply fixes

---

## Test Collection Statistics

### Before Shadow Package Fix
```
tests/services/: 0 tests collected (shadow package blocked pytest)
```

### After Restructure + Fixes
```
tests/unit/services/: 299 tests collected, 1 error
```

### Breakdown by Status
- ✅ **Collectible**: 299 tests
- 🔴 **Blocked**: ~10-15 tests (in test_event_spatial_mapping.py)
- 📊 **Total Potential**: ~310-315 tests

---

## Next Steps

1. **Fix test_event_spatial_mapping.py** (missing async keywords)
2. **Run full test suite** to identify test failures vs collection errors
3. **Catalog test failures** by category:
   - Mock/fixture issues
   - Import errors
   - Logic errors
   - Database issues
4. **Document for PM's e2e testing**

---

## Impact on E2E Testing

**For PM's parallel alpha testing**:
- Test infrastructure now matches production codebase
- 299 tests discoverable (was 0)
- Can accurately assess technical debt
- Test failures will reveal real issues vs collection problems

**Beads Closed**:
- piper-morgan-p4o: test_spatial_integration.py async fixes
- piper-morgan-4s4: test_token_blacklist.py syntax fixes
- piper-morgan-an1: UUID import fixes (2 files)
- piper-morgan-252: ValidationError import fix

**Beads Open**:
- piper-morgan-dut: test_event_spatial_mapping.py (in progress)
- piper-morgan-iu0: Full catalog (this document)

---

**Generated**: 2025-11-19 09:55 AM
**Agent**: Claude Code (Sonnet 4.5)
**Session**: 2025-11-19-0836-prog-code-log
