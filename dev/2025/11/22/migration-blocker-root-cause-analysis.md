# Migration Blocker Root Cause Analysis

**Date**: November 22, 2025, 4:15 PM
**Issue**: Alembic migration af770c5854fe fails with "xian-alpha not found in alpha_users"
**Analysis Status**: ✅ ROOT CAUSE IDENTIFIED

---

## Executive Summary

The migration blocker is caused by a **username mismatch between two consecutive migrations**:

1. **Migration af770c5854fe** (Issue #259): Expects to migrate a user named `'xian-alpha'` FROM the users table TO the new alpha_users table
2. **Migration d8aeb665e878** (Issue #262): Later tries to migrate a user named `'xian'` FROM alpha_users BACK to users with an is_alpha flag

**The Problem**: These migrations assume different usernames for the same user:
- First migration looks for `'xian-alpha'` in users table
- Second migration looks for `'xian'` in alpha_users table
- **Since the database starts empty** (no migrations have run), the first migration cannot find `'xian-alpha'` and fails

---

## Migration Sequence and Timeline

### Migration History (Chronologically)

```
6d503d8783d2 (Oct 22, 7:20 AM)
├─ add_user_model_issue_228
├─ Creates users table
└─ Populates from existing user_id values

↓

af770c5854fe (Oct 23, 11:09 AM) ⚠️ BLOCKER
├─ create_alpha_users_add_role_migrate_xian_alpha_issue_259
├─ Part 1: Add role column to users table
├─ Part 2: Create alpha_users table
├─ Part 3: MIGRATE xian-alpha from users → alpha_users
│   └─ Executes: SELECT FROM users WHERE username = 'xian-alpha'
│   └─ Expected: Finds 1 user named 'xian-alpha'
│   └─ Actual: Finds 0 users (empty table at this point)
│   └─ Result: FAILS with "xian-alpha not found in alpha_users"
└─ Also renames users.xian-alpha → 'xian-alpha.migrated'

↓

d8aeb665e878 (Nov 9, 1:07 PM) ← Would run after af770c5854fe if it passed
├─ uuid_migration_issue_262_and_291
├─ Part 1: Drop FK constraints
├─ Part 2: Convert users.id to UUID
├─ Part 3: Add is_alpha flag to users
├─ Part 4: MIGRATE alpha_users data back to users
│   └─ Executes: SELECT FROM alpha_users WHERE username = 'xian'
│   └─ Expected: Finds 1 user named 'xian' (migrated from users as 'xian-alpha')
│   └─ Problem: If af770c5854fe uses username='xian-alpha', then is_alpha migration looks for 'xian'
├─ Part 5: Convert FK columns to UUID
└─ Part 6: Drop alpha_users table
```

---

## The Mismatch Details

### Migration af770c5854fe - Lines 130-131
```python
FROM users
WHERE username = 'xian-alpha'
```
Expects: A user with username `'xian-alpha'` in the users table

### Migration d8aeb665e878 - Lines 78
```python
WHERE username = 'xian'
```
Expects: A user with username `'xian'` in the alpha_users table

**The disconnect**: The first migration tries to find `'xian-alpha'`, but the second migration tries to find `'xian'`. These refer to the same user but with different usernames!

---

## Why This Matters (User Context)

Based on your explanation about the alpha account strategy:

1. **Original State**: You were the only user (xian). No user model existed.
2. **Phase 1 (Issue #228)**: User model created. Your data migrated to users table as a user_id.
3. **Phase 2 (Issue #259)**: Need to separate "development data" (accumulated test data) from "product data" (what alpha users see).
   - Created alpha_users table for separated data
   - Wanted to migrate your current account (xian-alpha) to alpha_users
   - Renamed it in users table to xian-alpha.migrated (marked inactive)
4. **Phase 3 (Issue #262)**: Consolidation and UUID migration.
   - Realized alpha_users table adds complexity
   - Decide to keep everything in users table with `is_alpha=True` flag
   - Merge alpha_users back to users
   - But... migration looks for username 'xian' not 'xian-alpha'

---

## The Root Cause

**There is no user data in the database yet** because we're setting up a fresh database. The migrations assume data was already migrated from a previous setup.

When running migrations sequentially on a fresh database:

1. af770c5854fe runs first → looks for users with username='xian-alpha' → **NONE EXIST** → fails

The second migration never gets a chance to run because the first one fails.

---

## Why The Mismatch Exists

**Most likely scenario** (based on code analysis):

The migrations were written at different times with different assumptions:

1. **af770c5854fe writer** assumed: "We'll migrate 'xian-alpha' to alpha_users table"
2. **d8aeb665e878 writer** assumed: "The alpha user in alpha_users is 'xian' (singular)"

This is a classic case where migration scripts were written independently without full alignment on the data model.

---

## Evidence

### Current Database State
```bash
$ docker exec piper-postgres psql -U piper -d piper_morgan -c "\dt"

 Schema |      Name       | Type  | Owner
--------+-----------------+-------+-------
 public | alembic_version | table | piper
(1 row)

# Only alembic_version table exists
# No users table yet (migrations not applied)
# No data to migrate
```

### Migration Dependency Chain
```
af770c5854fe → Revises: fcc1031179bb
d8aeb665e878 → Revises: 234aa8ec628c

They're in different dependency chains! The question is what comes between them.
```

---

## Solution Options

### Option 1: Skip the Problematic Migration (⚠️ WORKAROUND)
**For test environment only**:
```bash
# Run migrations but skip af770c5854fe
alembic upgrade fcc1031179bb    # Go up to the predecessor
# Then manually skip to d8aeb665e878
alembic upgrade d8aeb665e878
```

**Problem**: This breaks the migration sequence and leaves the database in an inconsistent state.

### Option 2: Fix the Migration (✅ RECOMMENDED - DATA-AWARE)
Make af770c5854fe not fail when the user doesn't exist (fresh database scenario):

```python
# In af770c5854fe, change the verification from:
if count == 0:
    raise Exception("Migration failed: xian-alpha not found in alpha_users")

# To:
if count == 0:
    # This is expected for fresh database setup - no data to migrate
    # Development data separation will be handled in next migration
    print("ℹ️ No xian-alpha user found to migrate (expected for fresh setup)")
```

### Option 3: Separate Fresh vs Existing Data (✅ BEST - ARCHITECTURAL)
Create a new migration sequence for fresh setups:
- Remove the data migration from af770c5854fe
- Add schema creation only
- Add a separate migration for data (only runs if data exists)

### Option 4: Inspect Real Production Database (⚠️ UNDERSTANDING)
If data actually exists in production:
```bash
# Check production database
docker exec piper-postgres-prod psql -U piper -d piper_morgan -c "SELECT username FROM users WHERE username LIKE 'xian%';"

# This would show if:
# - User 'xian-alpha' exists (first migration will work)
# - User 'xian' exists (second migration will work)
# - Both exist (inconsistent state)
# - Neither exist (data migration never happened)
```

---

## Recommendation

**For Issue #357 Test Database Setup**:

Implement **Option 2** - Make af770c5854fe tolerant of missing data on fresh database:

```python
# File: alembic/versions/af770c5854fe_create_alpha_users_add_role_migrate_.py
# Line 136-143: Change verification logic

# BEFORE (fails on fresh database):
if count == 0:
    raise Exception("Migration failed: xian-alpha not found in alpha_users")

# AFTER (tolerates fresh database):
if count == 0:
    # Expected for fresh database setup - no development data to migrate
    # This migration is primarily for schema changes (role column, alpha_users table)
    # Data migration is conditional (only if user exists)
    print("ℹ️ Info: No xian-alpha user found for migration (fresh database setup)")
else:
    print(f"✅ Migration successful: xian-alpha found in alpha_users (count={count})")
```

**This allows**:
1. ✅ Fresh database setup (no user data) → migrations proceed
2. ✅ Existing database (has xian-alpha) → data is migrated
3. ✅ Both test and production scenarios work

---

## Verification After Fix

```bash
# Test the fix
cd /Users/xian/Development/piper-morgan
alembic upgrade head

# Should see:
# - Schema creation (users table, alpha_users table, etc.)
# - "Info: No xian-alpha user found for migration (fresh database setup)"
# - Or "Migration successful: xian-alpha found in alpha_users" if user exists

# Verify all tables created
docker exec piper-postgres psql -U piper -d piper_morgan -c "\dt" | wc -l
# Should show 30+ tables (not just 1)
```

---

## Files to Update

- **alembic/versions/af770c5854fe_create_alpha_users_add_role_migrate_.py**
  - Lines 136-143: Change verification from Exception to warning/info
  - Also update line 145-158: Conditional rename only if user exists

---

## Impact Assessment

- ✅ Fixes test database initialization blocker
- ✅ Maintains forward compatibility with existing databases
- ✅ No breaking changes to schema
- ✅ Enables all 20 SEC-RBAC integration tests to run
- ⚠️ Doesn't resolve the username mismatch in d8aeb665e878 (but that's separate issue for later analysis)

---

## Next Steps

1. **Implement Option 2 fix** in af770c5854fe migration
2. **Run migrations**: `alembic upgrade head`
3. **Verify schema**: Check that 30+ tables are created
4. **Run integration tests**: `pytest tests/integration/test_cross_user_access.py -v`
5. **Document findings**: Update GitHub issue #357 with migration fix evidence

---

**Status**: Ready for implementation
**Blocking Issue**: #357 (SEC-RBAC: Implement RBAC)
**Side Quest**: Test database infrastructure setup
