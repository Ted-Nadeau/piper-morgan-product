# Audit: #768 Issue - Systemic Timezone Investigation

**Date**: 2026-02-02
**Document**: GitHub Issue #768
**Type**: Technical Audit (not bug report - different template)

---

## Issue Quality Check

| Requirement | Status | Notes |
|-------------|--------|-------|
| Clear description | ✅ | Root cause pattern documented |
| Affected locations listed | ✅ | 10+ locations with file/line |
| Audit scope defined | ✅ | 4 clear objectives |
| Acceptance criteria | ✅ | 5 checkboxes |
| Priority assigned | ✅ | P1 |
| Related issues linked | ✅ | #757 referenced |
| Discovery method documented | ✅ | Grep commands shown |

---

## Issue Status: READY FOR AUDIT EXECUTION

The issue is well-structured for a systemic audit. No template gaps.

---

## Audit Execution Plan

For each of the 10+ locations, need to determine:

1. **Data Source**: Does the datetime come from the database, or is it created in-memory?
2. **If from DB**: Is the column `TIMESTAMP WITH TIME ZONE`?
3. **Impact**: What breaks if the age calculation is wrong?
4. **Test Coverage**: Is there a test that would catch this?
5. **Classification**: REAL BUG / FALSE POSITIVE / NEEDS INVESTIGATION

---

## Audit Matrix (COMPLETE)

| # | File | Line | Data Source | Column Type | Impact | Test Coverage | Classification |
|---|------|------|-------------|-------------|--------|---------------|----------------|
| 1 | file_resolver.py | 205 | DB (uploaded_files.upload_time) | TIMESTAMP WITH TZ | Recency score | test_file_scoring_weights | **REAL BUG** |
| 2 | file_resolver.py | 288 | DB (uploaded_files.last_referenced) | TIMESTAMP WITH TZ | Usage score | None | **REAL BUG** |
| 3 | context_tracker.py | 428 | DB (conversations) via get_conversation_context | TIMESTAMP WITH TZ | Conversation age | None | **REAL BUG** |
| 4 | portfolio_manager.py | 204 | In-memory dict (_sessions) | N/A | Session duration | None | FALSE POSITIVE |
| 5 | standup/conversation_manager.py | 203 | In-memory dict | N/A | Session duration | None | FALSE POSITIVE |
| 6 | preference_handler.py | 544 | In-memory dict (_SESSION_HINTS) | N/A | Preference age | None | FALSE POSITIVE |
| 7 | premonition.py | 209 | In-memory (no DB model) | N/A | Insight timing | None | FALSE POSITIVE |
| 8 | premonition.py | 271 | In-memory (no DB model) | N/A | Insight timing | None | FALSE POSITIVE |
| 9 | compost_bin.py | 358 | In-memory (no DB model) | N/A | Compost age | None | FALSE POSITIVE |
| 10 | compost_bin.py | 392 | In-memory (no DB model) | N/A | Compost age | None | FALSE POSITIVE |
| 11 | attention_model.py | 96 | In-memory (no DB model) | N/A | Attention age | None | FALSE POSITIVE |
| 12 | attention_model.py | 502 | In-memory (no DB model) | N/A | Response time | None | FALSE POSITIVE |

---

## Summary

**REAL BUGS: 3**
1. `file_resolver.py:205` - Recency scoring (exposed by #757 test)
2. `file_resolver.py:288` - Usage scoring (no test coverage)
3. `context_tracker.py:428` - Conversation age calculation (no test coverage)

**FALSE POSITIVES: 9**
All in-memory objects where both `created_at` and `datetime.now()` are naive local time created in the same process.

---

## SQL WHERE Clause Analysis (Additional)

These use naive `datetime.now()` in SQL WHERE clauses. PostgreSQL handles timezone conversion on the server side, so these may work correctly despite the inconsistency. However, they represent technical debt.

| File | Line(s) | Risk Level |
|------|---------|------------|
| file_repository.py | 114, 132, 151, 284 | LOW - PostgreSQL handles conversion |
| todo_repository.py | 533 | LOW - PostgreSQL handles conversion |
| session_persistence.py | 164, 250 | LOW - PostgreSQL handles conversion |

**Recommendation**: Low priority, but should be standardized for consistency.

---

## Recommended Fix Strategy

**Option B (Utility Function) is recommended**:

1. Create `services/utils/datetime_utils.py`:
   ```python
   from datetime import datetime, timezone

   def utc_now() -> datetime:
       """Return current UTC time as naive datetime for DB comparison."""
       return datetime.now(timezone.utc).replace(tzinfo=None)
   ```

2. Fix the 3 real bugs to use `utc_now()`

3. Optionally standardize the SQL WHERE clause locations for consistency

**Rationale**:
- Only 3 real bugs (not 10+)
- Utility function prevents future occurrences
- Clear naming makes intent obvious
- Minimal scope compared to original estimate

---

## Next Step

Create gameplan for the 3 confirmed bugs.
