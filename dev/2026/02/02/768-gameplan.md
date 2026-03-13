# Gameplan: #768 - Fix Systemic Timezone Handling (3 Bugs)

**Issue**: #768
**Date**: 2026-02-02
**Type**: Code Bug Fix (Timezone handling)

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Task**: Fix 3 timezone bugs by creating utility function and updating affected code.

**Infrastructure**:
- New file: `services/utils/datetime_utils.py` (to be created)
- Bug 1: `services/file_context/file_resolver.py:205`
- Bug 2: `services/file_context/file_resolver.py:288`
- Bug 3: `services/conversation/context_tracker.py:428`

**Worktree Assessment**: SKIP WORKTREE - 4 files, ~30 min, single agent

### Part B: PM Verification

- [x] PM confirms audit results (3 real bugs, 9 false positives)
- [x] PM confirms Option B (utility function approach)

### Part C: Decision

- [x] PROCEED with gameplan

---

## Phase 0: Investigation (Complete)

See `dev/2026/02/02/768-issue-audit.md` for full audit results.

---

## Phase 0.5-0.8: N/A

- 0.5: N/A - No frontend
- 0.6: N/A - Single utility function, simple data flow
- 0.7: N/A - Not conversational
- 0.8: N/A - No new state

---

## Phase 1: Create Utility Function

### New File: `services/utils/datetime_utils.py`

```python
"""
Datetime utilities for consistent timezone handling.

Issue #768: Systemic timezone bug where naive datetime.now() (local time)
was compared with database values (UTC), causing incorrect age calculations.

Usage:
    from services.utils.datetime_utils import utc_now

    age = utc_now() - record.created_at  # Both are naive UTC
"""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """
    Return current UTC time as naive datetime.

    Use this instead of datetime.now() when comparing with database timestamps,
    which are stored as UTC in PostgreSQL TIMESTAMP WITH TIME ZONE columns.

    Returns:
        Naive datetime representing current UTC time.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


def ensure_utc_naive(dt: datetime) -> datetime:
    """
    Convert a datetime to naive UTC.

    If the datetime is timezone-aware, converts to UTC and strips tzinfo.
    If already naive, assumes it's UTC (as returned by our database).

    Args:
        dt: A datetime that may or may not have timezone info.

    Returns:
        Naive datetime in UTC.
    """
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt
```

---

## Phase 2: Fix Bug #1 - file_resolver.py:205 (_calculate_recency_score)

### Current Code (Broken)

```python
def _calculate_recency_score(self, upload_time: datetime) -> float:
    """Calculate recency score (0.0 to 1.0)"""
    if not upload_time:
        return 0.0

    now = datetime.now()  # <-- BUG: naive local time
    age = now - upload_time
```

### Fixed Code

```python
def _calculate_recency_score(self, upload_time: datetime) -> float:
    """Calculate recency score (0.0 to 1.0)"""
    if not upload_time:
        return 0.0

    from services.utils.datetime_utils import utc_now, ensure_utc_naive

    now = utc_now()
    upload_utc = ensure_utc_naive(upload_time)
    age = now - upload_utc
```

---

## Phase 3: Fix Bug #2 - file_resolver.py:288 (_calculate_usage_score)

### Current Code (Broken)

```python
if file.last_referenced:
    age = datetime.now() - file.last_referenced  # <-- BUG
```

### Fixed Code

```python
if file.last_referenced:
    from services.utils.datetime_utils import utc_now, ensure_utc_naive
    now = utc_now()
    last_ref_utc = ensure_utc_naive(file.last_referenced)
    age = now - last_ref_utc
```

---

## Phase 4: Fix Bug #3 - context_tracker.py:428

### Current Code (Broken)

```python
"conversation_age": (datetime.now() - conv_state.created_at).total_seconds(),
```

### Fixed Code

```python
from services.utils.datetime_utils import utc_now, ensure_utc_naive
# ... in the method:
"conversation_age": (utc_now() - ensure_utc_naive(conv_state.created_at)).total_seconds(),
```

---

## Phase Z: Verification

### Acceptance Criteria

- [ ] `services/utils/datetime_utils.py` created with `utc_now()` and `ensure_utc_naive()`
- [ ] `file_resolver.py:_calculate_recency_score` uses utility functions
- [ ] `file_resolver.py:_calculate_usage_score` uses utility functions
- [ ] `context_tracker.py` uses utility functions
- [ ] `test_file_scoring_weights` passes (verifies bug #1 fix)
- [ ] All file_resolver tests pass
- [ ] No import errors

### STOP Conditions

- If utility function import fails → check path
- If other tests break → evaluate impact

### Test Verification

```bash
# Verify #757 test now passes
pytest tests/unit/services/test_file_scoring_weights.py::test_scoring_weight_distribution -xvs

# Verify all file resolver tests pass
pytest tests/unit/services/test_file_resolver_edge_cases.py -xvs
pytest tests/unit/services/test_file_scoring_weights.py -xvs

# Verify no import errors
python -c "from services.utils.datetime_utils import utc_now, ensure_utc_naive; print('OK')"
```

### Evidence Required

- [ ] Test output showing test_file_scoring_weights passes
- [ ] Debug output showing correct age calculation (positive, not negative)

---

## Files to Modify

| File | Changes |
|------|---------|
| `services/utils/datetime_utils.py` | CREATE - New utility module |
| `services/file_context/file_resolver.py` | UPDATE - Lines 205 and 288 |
| `services/conversation/context_tracker.py` | UPDATE - Line 428 |

---

## Multi-Agent Deployment

**Single agent** - 4 files, simple changes, ~30 min

---

## Estimated Scope

- Phase 1: 5 min (create utility)
- Phase 2: 5 min (fix recency score)
- Phase 3: 5 min (fix usage score)
- Phase 4: 5 min (fix context tracker)
- Phase Z: 10 min (verify all tests)

**Total**: ~30 min
