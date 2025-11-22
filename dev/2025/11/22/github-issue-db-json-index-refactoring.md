# GitHub Issue: DB-JSON-INDEX - PostgreSQL JSON Index Schema Refactoring

**Title**: DB-JSON-INDEX: Refactor PostgreSQL JSON column indexes to use proper operators

**Labels**: `infrastructure`, `database`, `technical-debt`, `S1`

**Priority**: P1 (Blocks full migration chain)

**Assignee**: TBD (Chief Architect or Database Specialist)

---

## Summary

Remaining 30% of Alembic migration chain is blocked by improper JSON column indexing. PostgreSQL requires special operator classes (GIN for JSONB) for JSON column indexes, but multiple migrations attempt to create standard B-tree indexes on JSON columns.

**Discovered During**: SEC-RBAC Phase 1.1 database migration work (November 22, 2025)

**Impact**: Prevents `alembic upgrade head` from completing, blocks clean database recreation, blocks CI/CD pipeline validation

---

## Root Cause

PostgreSQL JSON columns require explicit operator classes for indexing:
- **JSONB columns**: Require GIN (Generalized Inverted Index) operator
- **JSON columns**: Cannot use standard B-tree indexes without explicit operator classes

**Current migrations** attempt to create indexes like:
```python
op.create_index('idx_lists_shared', 'lists', ['shared_with'])
```

**Problem**: `shared_with` is a JSON column, requires:
```python
op.create_index('idx_lists_shared', 'lists', ['shared_with'], postgresql_using='gin')
```

**Or convert to JSONB**:
```sql
ALTER TABLE lists ALTER COLUMN shared_with TYPE JSONB USING shared_with::jsonb;
CREATE INDEX idx_lists_shared ON lists USING gin (shared_with);
```

---

## Scope

**Affected Migrations**: ~30% of migration chain (final 8-10 migrations)

**Example Blocker** (first in sequence):
- Migration: `[hash]_add_lists_table.py` (or similar)
- Line: `op.create_index('idx_lists_shared', 'lists', ['shared_with'])`
- Column: `lists.shared_with` (JSON type)
- Error: `ERROR: data type json has no default operator class for access method "btree"`

**Likely Affected Tables** (based on typical JSON column usage):
- `lists` - `shared_with` column
- `conversation_turns` - `metadata` column (if indexed)
- `learned_patterns` - `pattern_data` column (if indexed)
- Any analytics tables with JSON columns

---

## Current State

**Migration Chain Status**:
- ✅ Migrations 1-20 (~70%): Apply successfully
- ❌ Migrations 21-28 (~30%): Blocked by JSON index issues
- 🔶 Database functional at 70% but not fully canonical

**SEC-RBAC Impact**:
- ✅ Phase 1.1 owner_id columns deployed (in applied 70%)
- ✅ Phase 1.2 service layer complete
- ✅ Phase 1.3 can proceed (doesn't depend on blocked migrations)
- ❌ Full migration validation incomplete

**Performance Index Impact**:
- Issue #356 (PERF-INDEX): 6 indexes deployed in applied migrations
- Issue #532 (PERF-ANALYTICS): 2 indexes blocked in final 30%

---

## Architectural Decisions Required

### Decision 1: JSON vs JSONB

**Option A: Convert to JSONB** (Recommended)
- **Pros**: Better performance, supports GIN indexing, standard PostgreSQL practice
- **Cons**: Requires data migration (JSON → JSONB), potentially breaks existing queries
- **Recommendation**: Use JSONB for any columns requiring indexing

**Option B: Keep JSON, add explicit operators**
- **Pros**: No data migration needed
- **Cons**: Limited indexing options, worse performance
- **Recommendation**: Only if backward compatibility critical

### Decision 2: Migration Strategy

**Option A: Fix migrations in place**
- Add `postgresql_using='gin'` to existing index creation
- Convert column types from JSON to JSONB in same migration
- **Risk**: May break if migrations already partially applied

**Option B: Create new migration**
- Leave existing migrations as-is
- Add new migration: "Convert JSON columns to JSONB and add proper indexes"
- **Benefit**: Safer for databases in intermediate states

**Option C: Hybrid approach**
- Fix migrations not yet applied
- Add conversion migration for any databases stuck at 70%

---

## Implementation Plan (Recommended)

### Phase 1: Audit (1 hour)

1. **Identify all JSON columns with indexes**:
```bash
grep -r "create_index" alembic/versions/ | grep -v ".pyc"
# For each index, check if column is JSON type
```

2. **Categorize by migration status**:
   - Migrations before 70% mark: Already applied, leave as-is
   - Migrations after 70% mark: Not yet applied, can fix directly

3. **Document findings**: List all affected migrations and columns

### Phase 2: Fix Migrations (2-3 hours)

For each affected migration after 70% mark:

1. **Convert column to JSONB** (if not already):
```python
# In upgrade():
op.execute("ALTER TABLE table_name ALTER COLUMN column_name TYPE JSONB USING column_name::jsonb")

# In downgrade():
op.execute("ALTER TABLE table_name ALTER COLUMN column_name TYPE JSON")
```

2. **Add GIN index**:
```python
# Instead of:
op.create_index('idx_name', 'table', ['json_column'])

# Use:
op.create_index('idx_name', 'table', ['json_column'], postgresql_using='gin')
```

3. **Make idempotent** (like enum pattern from Phase 1.1):
```python
# Check if index exists before creating
op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_indexes WHERE indexname = 'idx_name'
        ) THEN
            CREATE INDEX idx_name ON table_name USING gin (json_column);
        END IF;
    END
    $$;
""")
```

### Phase 3: Test (1 hour)

1. **Wipe and recreate test database**:
```bash
docker exec -it piper-postgres psql -U piper -d postgres -c "DROP DATABASE IF EXISTS piper_morgan_test;"
docker exec -it piper-postgres psql -U piper -d postgres -c "CREATE DATABASE piper_morgan_test OWNER piper;"
```

2. **Run full migration chain**:
```bash
PIPER_DB_NAME=piper_morgan_test python -m alembic upgrade head
```

3. **Verify 100% success**:
```bash
# Should complete without errors
# Check all tables exist
# Check all indexes created
```

### Phase 4: Deploy (30 min)

1. **For development/alpha databases stuck at 70%**:
   - Option A: Wipe and recreate (clean slate)
   - Option B: Run conversion migration to bring to 100%

2. **Update CI/CD**:
   - Add migration validation to test pipeline
   - Ensure fresh database creation tested regularly

---

## Acceptance Criteria

- [ ] All JSON columns requiring indexes converted to JSONB
- [ ] All JSONB indexes use `postgresql_using='gin'`
- [ ] Migration chain applies 100% from base → head
- [ ] All tables from original design exist
- [ ] Issue #532 analytics indexes deployed
- [ ] CI/CD pipeline validates fresh database creation
- [ ] No regressions in existing 70% of migrations

---

## Dependencies

**Blocks**:
- Full migration chain validation
- Issue #532 completion (analytics indexes)
- CI/CD migration testing
- New developer onboarding (fresh DB setup)

**Depends On**:
- None (can start immediately)

**Related**:
- Issue #357 (SEC-RBAC): Phase 1.1 complete at 70%, sufficient for Phase 1.3
- Issue #356 (PERF-INDEX): Deployed in applied migrations
- Issue #532 (PERF-ANALYTICS): Blocked by this issue

---

## Estimated Effort

- **Audit**: 1 hour
- **Implementation**: 2-3 hours
- **Testing**: 1 hour
- **Documentation**: 30 minutes

**Total**: 4-6 hours (half day for database specialist)

---

## Notes

**Discovered By**: Claude Code agent during SEC-RBAC Phase 1.1 execution (November 22, 2025, 6:45-7:45 AM)

**Escalation**: Code agent correctly identified this as architectural issue beyond Phase 1.1 scope and escalated rather than attempting quick fixes

**Current Workaround**: Database functional at 70% - sufficient for SEC-RBAC Phase 1.3 work to proceed

**Files**:
- Discovery: `dev/2025/11/22/sec-rbac-phase1.1-completion-report.md`
- Analysis: See "Architectural Issues Discovered" section

---

## References

**PostgreSQL JSON Indexing Documentation**:
- https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING
- https://www.postgresql.org/docs/current/gin.html

**Related Patterns** (from Phase 1.1 fixes):
- Idempotent enum creation (see commits 9057d017, 9a2ced8c)
- Migration chain validation (see completion report)

---

_Issue drafted by: Lead Developer (Claude Code session)_
_Date: November 22, 2025, 7:05 AM_
_Sprint: S1 (Infrastructure)_
_Priority: P1 (blocks full migration chain)_
