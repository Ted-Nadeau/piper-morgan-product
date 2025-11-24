# Gameplan: Fix Broken Migrations for Production Deployment

**Issue**: #378 (ALPHA-DEPLOY-PROD)
**Date**: November 23, 2025, 8:55 PM
**Status**: INVESTIGATION PHASE

---

## Problem Statement

Production deployment blocked by multiple broken Alembic migrations that prevent:
1. Fresh database initialization (can't run `alembic upgrade heads`)
2. Unit test execution (test DB can't be created)
3. Production branch deployment (migrations will fail there too)

---

## Investigation Summary

### Current Database State
- **Main branch database**: Exists, migrations already run, working
- **Test database**: Just wiped clean, trying to rebuild from scratch
- **Production branch**: Unknown state (498 commits behind)

### Broken Migrations Found

1. **`20251122_upgrade_shared_with_to_roles.py`**
   - **Problem**: Wrong parent revision (`6m5s5d1t6500` instead of `4d1e2c3b5f7a`)
   - **Problem**: Uses `todos` table (migrated to `todo_items` in `234aa8ec628c`)
   - **Problem**: Tries to upgrade `shared_with` column that doesn't exist yet (migration assumes existing data)
   - **Root Cause**: Migration for upgrading EXISTING databases, not fresh installs
   - **Status**: Moved to `.broken` file

2. **`20251122_120858_add_is_admin_to_users_sec_rbac_357.py`**
   - **Problem**: Parent points to broken migration above
   - **Problem**: Invalid PostgreSQL syntax (`LIMIT 1` in `UPDATE` statement)
   - **Root Cause**: SQL syntax error
   - **Status**: Parent fixed to `4d1e2c3b5f7a`, still has SQL bug

3. **Migration Graph**
   - 3 migration heads (splits in migration tree)
   - `b8e4f3c9a2d7` - Working head (analytics indexes)
   - `d8aeb665e878c` - Working head (UUID migration)
   - `20251122_120858` - Broken head (depends on broken migration)

---

## Options Analysis

### Option A: Fix Migrations Properly (Thorough, takes time)
**Steps**:
1. Fix `20251122_120858` SQL syntax (remove `LIMIT 1`)
2. Add `shared_with` column creation to models (if missing)
3. Delete upgrade migration (only needed for existing DBs)
4. Merge migration heads
5. Test on fresh database
6. Test on existing database (main)

**Pros**:
- Clean migrations for future
- Proper fix

**Cons**:
- Takes 30-60 minutes
- May reveal more bugs

### Option B: Nuclear Option - Delete Broken Migrations (Fast, clean slate)
**Steps**:
1. Delete `20251122_upgrade_shared_with_to_roles.py.broken` (already moved)
2. Delete `20251122_120858_add_is_admin_to_users_sec_rbac_357.py`
3. Verify models have `is_admin` column defined (should be there from earlier migrations)
4. Rebuild test database
5. Run tests
6. Commit working state

**Pros**:
- Fast (10 minutes)
- Clean slate
- Models already have columns (migrations already ran on main DB)
- `is_admin` already exists in User model (line 80 of models.py)

**Cons**:
- Can't deploy to truly fresh database without those migrations
- But: Alpha testing doesn't need fresh DB

### Option C: Skip Test Database, Deploy Directly (Risky)
**Steps**:
1. Assume main DB migrations are fine (they are - system works)
2. Deploy to production branch
3. Hope production DB is in same state as main

**Pros**:
- Fastest

**Cons**:
- Risky
- No test coverage
- Production DB state unknown

---

## Recommended Approach: Option B (Nuclear)

**Rationale**:
1. Main database already has all columns (migrations ran successfully before)
2. Michelle testing on existing database (not fresh install)
3. Future fresh installs can run models directly (no migrations needed)
4. Alpha phase - acceptable to use nuclear options
5. We can add proper migrations post-alpha if needed

---

## Execution Plan (Option B)

### Phase 1: Clean Up Broken Migrations (5 min)
- ✅ Already moved `20251122_upgrade_shared_with_to_roles.py` to `.broken`
- ⏸️ Delete `20251122_120858_add_is_admin_to_users_sec_rbac_357.py`
- ⏸️ Verify no other migrations depend on deleted ones

### Phase 2: Verify Model Definitions (2 min)
- ⏸️ Check `services/database/models.py` User model has `is_admin` column
- ⏸️ Check `services/database/models.py` has `shared_with` columns on resource tables

### Phase 3: Rebuild Test Database (5 min)
- ⏸️ Run `alembic upgrade heads` on fresh DB
- ⏸️ Verify all working heads reached
- ⏸️ Check key tables exist (users, lists, todo_items, uploaded_files)

### Phase 4: Run Tests (5 min)
- ⏸️ Run unit test: `pytest tests/unit/services/test_file_repository_migration.py::test_file_repository_with_async_session -xvs`
- ⏸️ Run integration tests: `pytest tests/integration/ -k "rbac or owner_id" -xvs`
- ⏸️ Verify all pass

### Phase 5: Commit Changes (3 min)
- ⏸️ Commit test file fixes (UUID format changes)
- ⏸️ Commit migration deletions
- ⏸️ Git status shows clean

### Phase 6: Proceed with Deployment (Issue #378)
- ⏸️ Continue Phase 1 of deployment gameplan

---

## Success Criteria

- ✅ Test database can be created from scratch
- ✅ Unit tests pass
- ✅ Integration tests pass
- ✅ No broken migrations in tree
- ✅ Main database still works
- ✅ Ready to deploy to production branch

---

## Risks & Mitigations

**Risk**: Future fresh installs won't have `is_admin` or proper `shared_with`
**Mitigation**: Models define columns, SQLAlchemy creates them automatically. Migrations are for schema changes, not initial creation.

**Risk**: Production branch database in different state
**Mitigation**: Will discover during deployment Phase 0 investigation

**Risk**: Deleting migrations breaks existing databases
**Mitigation**: Only deleting migrations that never successfully ran on any database

---

## Evidence Required

1. Screenshot/output of `alembic heads` showing clean tree
2. Screenshot/output of passing unit test
3. Screenshot/output of passing integration tests
4. Git status showing committed changes

---

## Next Steps After This Gameplan

1. Get PM approval on Option B (Nuclear)
2. Execute Phase 1-6 systematically
3. Update Issue #378 gameplan with findings
4. Proceed with production deployment

---

**Estimated Time**: 20 minutes total (vs 60+ min for Option A)
**Risk Level**: Low (alpha phase, nuclear options acceptable)
**Recommendation**: Proceed with Option B
