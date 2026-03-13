# Audit: #757 Issue against bug_report_alpha.md template

**Date**: 2026-02-02
**Document**: GitHub Issue #757
**Template**: `.github/ISSUE_TEMPLATE/bug_report_alpha.md`

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Bug Description | ✅ | "Pre-existing test failure discovered during #747 validation" |
| Steps to Reproduce | ❌ | Missing - no steps provided |
| Expected Behavior | ⚠️ | Implied (score in range 0.4-0.7) but not explicit |
| Actual Behavior | ✅ | Score 0.72 shown |
| Environment | ❌ | Missing |
| Screenshots/Logs | ✅ | Error message included |
| Severity | ❌ | Missing checkboxes |
| Additional Context | ⚠️ | Analysis section covers this partially |

---

## Summary

- ✅ Present: 3
- ⚠️ Partial: 2
- ❌ Missing: 3

---

## Investigation Results

### Root Cause Analysis

**Test**: `test_scoring_weight_distribution`

The test creates files with specific upload times (5min, 30min, 120min ago) and expects scores in specific ranges. The test fails because `partial_match.pdf` gets score 0.72 instead of expected (0.4, 0.7).

### Five Whys

1. **Why does the test fail?**
   - `partial_match.pdf` score is 0.72 but expected range is (0.4, 0.7)

2. **Why is the score 0.72?**
   - All files get recency_score = 1.0 (max), contributing 0.30 to the total

3. **Why is recency_score 1.0 for a 30-minute-old file?**
   - The age calculation shows NEGATIVE time (-1 day, 16:30:00)
   - Files appear to be "from the future" so age < 5 minutes check passes

4. **Why is the age negative?**
   - When saving to PostgreSQL, naive datetime gets interpreted as UTC
   - Local time 11:17 → stored as 19:17 (UTC, +8 hours)
   - When retrieved and compared with local `datetime.now()`, it appears to be in the future

5. **Why does this timezone mismatch occur?**
   - Domain model uses naive `datetime.now()` (local time)
   - Database column is `DateTime(timezone=True)` with default `datetime.now(timezone.utc)`
   - PostgreSQL converts naive datetime to UTC on insert
   - Retrieved datetime is naive but shifted to UTC value
   - `_calculate_recency_score()` compares with naive `datetime.now()` (local time)

### Decision: This is a CODE BUG, not a test bug

**The scoring algorithm has a timezone handling bug:**
- Files created with naive local datetime get shifted by UTC offset when stored
- Recency calculation uses naive `datetime.now()` which is local time
- This causes all files to appear "from the future" (negative age)
- Negative age passes the `age <= timedelta(minutes=5)` check → recency = 1.0

**Impact:**
- ALL files get maximum recency score (1.0)
- Recency-based scoring is completely broken
- This affects file resolution in production

### Options

**Option A: Fix the timezone handling in FileResolver (Recommended)**
Update `_calculate_recency_score()` to handle timezone-aware datetimes properly.

**Option B: Fix the domain model**
Make domain model use UTC-aware datetimes consistently.

**Option C: Fix the database layer**
Store datetimes as naive (no timezone) to avoid conversion.

**Option D: Update test expectations (NOT recommended)**
This would mask a real production bug.

**Recommendation**: Option A - Fix timezone handling, but this is SYSTEMIC.

---

## SYSTEMIC ANALYSIS

**This bug affects multiple locations in the codebase.**

### Definitely Affected (Python-side comparison with DB values):

| File | Line | Pattern | Impact |
|------|------|---------|--------|
| `services/file_context/file_resolver.py` | 205 | `now - upload_time` | **Current test failure** |
| `services/file_context/file_resolver.py` | 288 | `now - file.last_referenced` | Usage score broken |
| `services/conversation/context_tracker.py` | 428 | `now - conv_state.created_at` | Conversation age wrong |
| `services/onboarding/portfolio_manager.py` | 204 | `now - session.created_at` | Duration calculation wrong |
| `services/standup/conversation_manager.py` | 203 | `now - conversation.created_at` | Duration calculation wrong |
| `services/intent_service/preference_handler.py` | 544 | `now - stored_at` | Preference age wrong |
| `services/mux/premonition.py` | 209, 271 | `now - last_similar_surfaced`, `now - created_at` | Insight timing wrong |
| `services/mux/compost_bin.py` | 358, 392 | `now - created_at` | Compost age wrong |
| `services/integrations/slack/attention_model.py` | 96, 502 | `now - created_at` | Attention age wrong |

### Possibly Affected (SQL WHERE clause with naive cutoff):

| File | Line | Pattern | Risk |
|------|------|---------|------|
| `services/repositories/file_repository.py` | 114, 132, 151, 284 | `cutoff = now - timedelta; WHERE upload_time > cutoff` | PostgreSQL may handle conversion |
| `services/repositories/todo_repository.py` | 533 | `cutoff = now - timedelta; WHERE ...` | PostgreSQL may handle conversion |
| `services/orchestration/session_persistence.py` | 164, 250 | `cutoff = now - timedelta; WHERE ...` | PostgreSQL may handle conversion |

### Recommended Fix Strategy:

1. **Immediate**: Fix FileResolver (fixes #757)
2. **Follow-up Issue**: Create tracking issue for systemic timezone audit
3. **Long-term**: Consider adding a utility function `utc_now()` that all code should use

---

## Required Fixes to Issue

### 1. Add Steps to Reproduce

```markdown
## Steps to Reproduce

1. Run `pytest tests/unit/services/test_file_scoring_weights.py::test_scoring_weight_distribution -xvs`
2. Test creates 3 files with different upload times (5min, 30min, 120min ago)
3. Test scores each file using FileResolver._calculate_score()
4. partial_match.pdf gets score 0.72 instead of expected (0.4, 0.7)
```

### 2. Add Environment

```markdown
## Environment

- Test framework: pytest
- Python: 3.12
- Database: PostgreSQL (async via asyncpg)
- Timezone: Local system timezone (PST/PDT, UTC-8/UTC-7)
```

### 3. Add Severity Checkbox

```markdown
## Severity

- [ ] Blocker
- [x] Major - Recency scoring is completely broken in production
- [ ] Minor
- [ ] Enhancement
```

### 4. Update Analysis with Root Cause

```markdown
## Root Cause

**This is a CODE BUG in timezone handling, not a test bug.**

When files are saved to PostgreSQL:
1. Domain model creates naive datetime (local time)
2. PostgreSQL `TIMESTAMP WITH TIME ZONE` interprets naive as UTC
3. Local time 11:17 → stored as 19:17 UTC (+8 hours shift)
4. Retrieved datetime is naive but contains UTC value
5. `_calculate_recency_score()` compares with naive `datetime.now()` (local)
6. Files appear "from the future" (negative age)
7. All files get recency_score = 1.0

**Impact**: Recency-based file scoring is broken in production.
```

---

## Status: READY FOR GAMEPLAN

Issue needs update, then gameplan for code fix.
