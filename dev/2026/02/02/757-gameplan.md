# Gameplan: #757 - Fix timezone handling in FileResolver recency scoring

**Issue**: #757
**Date**: 2026-02-02
**Type**: Code Bug Fix (Timezone handling)

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Task**: Fix `_calculate_recency_score()` to handle timezone-aware datetimes from database.

**Infrastructure**:
- Code file: `services/file_context/file_resolver.py`
- Test file: `tests/unit/services/test_file_scoring_weights.py`
- Related: Database layer stores datetimes as UTC-aware, domain model uses naive local time

**Root Cause**:
- Database returns UTC-aware datetimes (or naive UTC values)
- `_calculate_recency_score()` compares with naive `datetime.now()` (local time)
- This causes 8-hour offset on PST systems, making files appear "from the future"

**Worktree Assessment**: SKIP WORKTREE - Single method fix, < 30 min

### Part B: PM Verification

- [ ] PM confirms this is a code bug (not test bug)
- [ ] PM confirms Option A (fix recency calculation) over other options

### Part C: Decision

- [ ] PROCEED with gameplan
- [ ] REVISE based on PM feedback

---

## Phase 0: Investigation (Complete)

See `dev/2026/02/02/757-issue-audit.md` for full analysis.

**Key Finding**: PostgreSQL timezone handling causes all files to appear "from the future", giving max recency score to all files.

---

## Phase 0.5-0.8: N/A

- 0.5: N/A - No frontend
- 0.6: N/A - Single-layer fix
- 0.7: N/A - Not conversational
- 0.8: N/A - No new state

---

## SYSTEMIC DISCOVERY

**This is not an isolated bug.** Investigation found 10+ locations with the same pattern.

See `757-issue-audit.md` for full list.

**Recommended Approach**:
1. Fix FileResolver immediately (fixes #757 test)
2. Create tracking issue #761 for systemic timezone audit
3. Add utility function to prevent future occurrences

---

## Phase 1: Fix the Recency Calculation

### Current Code (Broken)

```python
def _calculate_recency_score(self, upload_time: datetime) -> float:
    """Calculate recency score (0.0 to 1.0)"""
    if not upload_time:
        return 0.0

    now = datetime.now()  # <-- NAIVE, local time
    age = now - upload_time  # <-- Fails if upload_time is UTC or timezone-aware

    # Last 5 minutes: full score
    if age <= timedelta(minutes=5):
        return 1.0

    # Decay over 1 hour
    if age <= timedelta(hours=1):
        minutes_old = age.total_seconds() / 60
        return max(0.0, 1.0 - (minutes_old / 60))

    # Very old files get minimal score
    return 0.1
```

### Fixed Code

```python
def _calculate_recency_score(self, upload_time: datetime) -> float:
    """Calculate recency score (0.0 to 1.0)"""
    if not upload_time:
        return 0.0

    # Handle timezone-aware datetimes from database
    # Convert both to naive UTC for comparison
    from datetime import timezone

    if upload_time.tzinfo is not None:
        # upload_time is timezone-aware, convert to naive UTC
        upload_utc = upload_time.astimezone(timezone.utc).replace(tzinfo=None)
    else:
        # upload_time is naive - assume it's already in UTC (from database)
        # or local time. For safety, treat as-is since PostgreSQL may have
        # stripped the timezone but the value is in UTC.
        # Actually, based on investigation: naive datetime from DB IS in UTC
        upload_utc = upload_time

    # Use UTC now for comparison
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    age = now_utc - upload_utc

    # Last 5 minutes: full score
    if age <= timedelta(minutes=5):
        return 1.0

    # Decay over 1 hour
    if age <= timedelta(hours=1):
        minutes_old = age.total_seconds() / 60
        return max(0.0, 1.0 - (minutes_old / 60))

    # Very old files get minimal score
    return 0.1
```

Wait - the investigation showed the DB returns naive datetimes that contain UTC values. So the fix is simpler: use UTC `datetime.now()` instead of local.

### Simpler Fixed Code

```python
def _calculate_recency_score(self, upload_time: datetime) -> float:
    """Calculate recency score (0.0 to 1.0)"""
    if not upload_time:
        return 0.0

    # Use UTC for comparison since database stores times in UTC
    # (even if returned as naive datetime, the value is UTC)
    from datetime import timezone

    # Get current time in UTC, as naive datetime
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)

    # If upload_time has timezone info, convert to naive UTC
    if upload_time.tzinfo is not None:
        upload_utc = upload_time.astimezone(timezone.utc).replace(tzinfo=None)
    else:
        # Assume naive datetime is already UTC (from database)
        upload_utc = upload_time

    age = now_utc - upload_utc

    # Last 5 minutes: full score
    if age <= timedelta(minutes=5):
        return 1.0

    # Decay over 1 hour
    if age <= timedelta(hours=1):
        minutes_old = age.total_seconds() / 60
        return max(0.0, 1.0 - (minutes_old / 60))

    # Very old files get minimal score
    return 0.1
```

---

## Phase 2: Update Test Setup (if needed)

The test creates files with naive local time:
```python
upload_time=datetime.now() - timedelta(minutes=age_minutes)
```

After the fix, this should work correctly because:
1. Test creates file with local naive datetime
2. DB stores it as UTC (adds timezone offset)
3. Retrieved as naive UTC
4. Recency score now correctly compares UTC to UTC

If tests still fail, we may need to update test to create UTC times:
```python
from datetime import timezone
upload_time=datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=age_minutes)
```

---

## Phase 1.5: Fix Usage Score (Same Bug)

The `_calculate_usage_score` method has the same bug at line 288:

### Current Code (Broken)

```python
if file.last_referenced:
    age = datetime.now() - file.last_referenced  # <-- SAME BUG
    if age <= timedelta(hours=1):
        recency_bonus = 0.3
```

### Fixed Code

```python
if file.last_referenced:
    # Use UTC for comparison since database stores times in UTC
    from datetime import timezone
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    if file.last_referenced.tzinfo is not None:
        last_ref_utc = file.last_referenced.astimezone(timezone.utc).replace(tzinfo=None)
    else:
        last_ref_utc = file.last_referenced
    age = now_utc - last_ref_utc
    if age <= timedelta(hours=1):
        recency_bonus = 0.3
```

---

## Phase 2: Create Systemic Tracking Issue

Create issue #761 to track the systemic timezone audit:

- 10+ locations with same pattern
- Need consistent approach across codebase
- Consider adding `utc_now()` utility function

---

## Phase Z: Verification

### Acceptance Criteria

- [ ] `_calculate_recency_score()` handles timezone-aware and naive datetimes
- [ ] Files from 30 minutes ago have recency score ≈ 0.5 (not 1.0)
- [ ] Files from 120 minutes ago have recency score ≈ 0.1 (not 1.0)
- [ ] `test_scoring_weight_distribution` passes
- [ ] All other tests in file pass
- [ ] `test_file_resolver_edge_cases.py` tests still pass

### STOP Conditions

- If fix causes other file resolver tests to fail → evaluate impact
- If fix requires changes to database layer → escalate to PM

### Test Verification

- Run failing test to confirm current failure
- Apply fix
- Run test in isolation to confirm pass
- Run related tests to confirm no regression

### Evidence Required

- [ ] Debug output showing correct age calculation after fix
- [ ] Test output showing all tests pass
- [ ] Grep showing no other methods have similar timezone issues

---

## Files to Modify

| File | Changes |
|------|---------|
| `services/file_context/file_resolver.py` | Fix `_calculate_recency_score()` timezone handling |

---

## Multi-Agent Deployment

**Single agent** - Single method fix, < 30 min

---

## Estimated Scope

- Phase 1: 15 min (fix code)
- Phase 2: 5 min (verify test setup, update if needed)
- Phase Z: 10 min (verify all tests)

**Total**: ~30 min
