# Gameplan: Issue #603 - Fix tests/load/test_cache_effectiveness.py Error

**Issue**: #603 TEST-INFRA: Fix tests/load/test_cache_effectiveness.py error
**Priority**: P2
**Type**: Test Infrastructure
**Estimated Effort**: 10 minutes

---

## Root Cause Analysis

### The Error
```
ModuleNotFoundError: No module named 'setup_real_system'
```

### Why It Happens
1. `tests/load/test_cache_effectiveness.py` imports: `from setup_real_system import ...`
2. This is a **bare import** (not relative like `from .setup_real_system`)
3. Works when running directly: `cd tests/load && python test_cache_effectiveness.py`
4. Fails with pytest because pytest uses the package import system
5. `tests/load/` has no `__init__.py`, so Python doesn't treat it as a package

### Files Affected
All load tests have the same issue:
- `tests/load/test_cache_effectiveness.py` - imports `setup_real_system`
- `tests/load/test_concurrent_load.py` - likely same issue
- `tests/load/test_error_recovery.py` - likely same issue
- `tests/load/test_memory_stability.py` - likely same issue
- `tests/load/test_sequential_load.py` - likely same issue

---

## Phase 0: Verification

```bash
# Verify the error
python -m pytest tests/load/test_cache_effectiveness.py --collect-only

# Check all load tests for same issue
grep -n "from setup_real_system" tests/load/*.py
```

---

## Phase 1: Fix Implementation

### Option A: Add `__init__.py` + Relative Imports (Recommended)

1. Create `tests/load/__init__.py`:
```python
# Load tests package
```

2. Change imports in all test files from:
```python
from setup_real_system import setup_real_intent_service, validate_real_system
```
To:
```python
from .setup_real_system import setup_real_intent_service, validate_real_system
```

### Option B: Mark as Manual Tests Only

If these are meant to be run manually (not via pytest), add pytest skip:
```python
import pytest
pytestmark = pytest.mark.skip(reason="Load tests run manually, not via pytest collection")
```

### Recommendation

**Use Option A** - These appear to be legitimate tests that should work with pytest.

---

## Phase 2: Verification

```bash
# Verify collection works
python -m pytest tests/load/ --collect-only

# Verify smoke tests work without --ignore
python -m pytest tests/ -m smoke -x --collect-only

# Run the load test (optional, may take time)
python -m pytest tests/load/test_cache_effectiveness.py -v
```

---

## Acceptance Criteria

- [ ] `python -m pytest tests/ -m smoke` works without `--ignore=tests/load/`
- [ ] `python -m pytest tests/load/ --collect-only` shows tests collected (no import errors)
- [ ] Existing unit/integration tests still pass

---

## Implementation Notes

This is a simple fix - add `__init__.py` and update 5 import statements. The load tests were written to be run directly (`python test_*.py`) but should also work with pytest.
