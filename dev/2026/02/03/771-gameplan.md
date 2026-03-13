# Gameplan: #771 - Schema Drift Fix (timestamp → timestamptz)

**Issue**: #771 - AUDIT: Schema drift - DateTime(timezone=True) models vs timestamp without time zone columns
**Date**: 2026-02-03
**Prepared By**: Lead Developer

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Database: PostgreSQL (port 5433, docker container `piper-postgres`)
- [x] ORM: SQLAlchemy with asyncpg
- [x] Migrations: Alembic
- [x] Testing framework: pytest

**My understanding of the task**:
- Convert all `timestamp without time zone` columns to `timestamp with time zone` (timestamptz)
- This fixes the mismatch between SQLAlchemy models (`DateTime(timezone=True)`) and actual DB schema
- After migration, code can use `utc_now()` consistently instead of `utc_now_naive()` workarounds

### Part A.2: Work Characteristics Assessment

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [x] Small fixes (<2 hours)
- [x] Tightly coupled files requiring atomic commits

**Assessment**:
- [x] **SKIP WORKTREE** - Single agent, ~2 hours, tightly coupled migration + code changes

**Rationale**: This is a focused infrastructure fix. Migration must be atomic with code changes. No parallel work needed.

### Part B: PM Verification Required

**PM, please confirm**:
- [x] PostgreSQL container is `piper-postgres` with user `piper`, database `piper_morgan`
- [x] Alpha data is disposable (can wipe if needed)
- [x] No other agents working on database-related changes
- [x] Proceed with Option A (fix database, not code)

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - PM confirmed Option A approach during discussion

---

## Phase 0: Initial Bookending

### GitHub Issue Verification
- Issue #771 exists and has been updated with full template sections
- Related issues: #768, #769, #770 (all FIXED with workarounds)

### Codebase Investigation

**Affected columns query**:
```sql
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE data_type = 'timestamp without time zone'
  AND table_schema = 'public'
ORDER BY table_name, column_name;
```

**SQLAlchemy models using DateTime(timezone=True)**:
```bash
grep -n "DateTime(timezone=True)" services/database/models.py
```

---

## Phase 0.5: Frontend-Backend Contract Verification

**N/A** - This is a backend-only database migration. No UI changes.

---

## Phase 0.6: Data Flow & Integration Verification

**N/A** - This is an infrastructure fix, not a multi-layer feature.

---

## Phase 0.7: Conversation Design

**N/A** - No conversational features involved.

---

## Phase 0.8: Post-Completion Integration

### Completion Side-Effects

When migration completes:

| Side Effect | Verification |
|-------------|--------------|
| All timestamp columns are timestamptz | SQL query confirms |
| Existing data preserved (interpreted as UTC) | Spot-check existing records |
| Code uses `utc_now()` consistently | No `utc_now_naive()` in DB operations |

### Downstream Behavior Changes

| Feature | Before | After |
|---------|--------|-------|
| Token blacklist | Uses `utc_now_naive()` workaround | Uses `utc_now()` |
| Setup completion | Uses `utc_now_naive()` workaround | Uses `utc_now()` |
| File resolver | Uses `utc_now_naive()` for comparisons | Uses `utc_now()` |

---

## Phase 1: Audit & Inventory

**Objective**: Identify all columns requiring migration

### Tasks
- [ ] Run SQL query to list all `timestamp without time zone` columns
- [ ] Cross-reference with SQLAlchemy models
- [ ] Document complete list

### Deliverables
- Complete list of columns to migrate

---

## Phase 2: Alembic Migration

**Objective**: Create and run migration to convert columns

### Tasks
- [ ] Create migration file: `alembic revision -m "convert_timestamps_to_timestamptz"`
- [ ] Write upgrade(): Convert each column with `USING column_name AT TIME ZONE 'UTC'`
- [ ] Write downgrade(): Convert back to timestamp (for safety)
- [ ] Test migration locally: `alembic upgrade head`
- [ ] Verify columns converted: Re-run audit query

### Migration Template
```python
def upgrade():
    # For each table/column:
    op.execute("""
        ALTER TABLE table_name
        ALTER COLUMN column_name TYPE TIMESTAMPTZ
        USING column_name AT TIME ZONE 'UTC'
    """)

def downgrade():
    # For each table/column:
    op.execute("""
        ALTER TABLE table_name
        ALTER COLUMN column_name TYPE TIMESTAMP
        USING column_name AT TIME ZONE 'UTC'
    """)
```

### Deliverables
- Migration file in `alembic/versions/`
- Evidence of successful migration

---

## Phase 3: Code Cleanup

**Objective**: Remove workarounds, use `utc_now()` consistently

### Tasks
- [ ] Replace `utc_now_naive()` with `utc_now()` in:
  - `services/auth/token_blacklist.py`
  - `web/api/routes/setup.py`
  - `services/file_context/file_resolver.py`
  - `services/conversation/context_tracker.py`
- [ ] Replace `ensure_utc_naive()` with `ensure_utc()` where used for DB operations
- [ ] Verify no remaining `datetime.now()` without timezone in DB operations

### Deliverables
- Clean code using timezone-aware datetimes

---

## Phase Z: Verification & Handoff

### Acceptance Criteria Verification

**Functionality**:
- [ ] All datetime columns in PostgreSQL are `timestamptz`
- [ ] Setup wizard completes without timezone errors
- [ ] Login/logout works without token rejection
- [ ] File resolver scoring works correctly

**Testing**:
```bash
pytest tests/unit/services/auth/test_token_blacklist.py -v
pytest tests/unit/services/test_file_scoring_weights.py -v
pytest tests/unit/services/test_file_resolver_edge_cases.py -v
```

**Manual Verification**:
1. [ ] Fresh database, run migrations
2. [ ] Start server
3. [ ] Complete setup wizard - no 500 errors
4. [ ] Login/logout cycle - no token rejection

### Evidence Required
- SQL query showing all columns are `timestamptz`
- Test output showing all tests pass
- Screenshot or log showing successful setup/login

---

## Multi-Agent Deployment

**Single Agent Justified**:
- Migration is atomic - cannot be split
- Code changes depend on migration completing
- Total scope ~2 hours
- No parallelization benefit

---

## STOP Conditions

- Migration fails or corrupts data
- Existing tests fail after migration
- Performance degrades noticeably
- Any timezone errors persist after fix

---

## Effort Estimate

| Phase | Estimate |
|-------|----------|
| Phase 1: Audit | 15 min |
| Phase 2: Migration | 30 min |
| Phase 3: Code cleanup | 30 min |
| Phase Z: Verification | 30 min |
| Buffer | 15 min |
| **Total** | **~2 hours** |

---

## Files to Modify

| File | Change |
|------|--------|
| `alembic/versions/xxx_convert_timestamps_to_timestamptz.py` | NEW - Migration |
| `services/auth/token_blacklist.py` | Replace utc_now_naive → utc_now |
| `web/api/routes/setup.py` | Replace utc_now_naive → utc_now |
| `services/file_context/file_resolver.py` | Replace utc_now_naive → utc_now |
| `services/conversation/context_tracker.py` | Replace utc_now_naive → utc_now |

---

**Status**: Ready for PM Approval
