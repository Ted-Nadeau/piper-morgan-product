# Claude Code Prompt: SEC-RBAC Phase 1.1 Database Schema - Completion

## Your Identity

You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Mission: Complete SEC-RBAC Phase 1.1 Database Schema

**GitHub Issue**: #357 - SEC-RBAC: Implement RBAC
**Current Phase**: Phase 1.1 - Database Schema (owner_id columns)
**Status**: Nearly complete but blocked by migration issues
**Goal**: Fix migrations, clean database, deploy schema

---

## Context: What's Already Done

### Phase 1.2 (Service Layer): ✅ COMPLETE

- 7 services with 52 methods secured
- Learning Services complete via delegation
- Architectural pattern established
- See: `dev/2025/11/21/sec-rbac-phase1.2-completion-summary.md`

### Phase 1.1 (Database Schema): 🔶 IN PROGRESS

**Migration Created**: `4d1e2c3b5f7a_add_owner_id_to_resource_tables_sec_rbac_357.py`

- Adds owner_id columns to 9 resource tables ✅
- Data mapping logic needs alpha fix ⚠️
- Can't apply due to broken migration chain ❌

### Related Work: ✅ READY

- **Issue #356** (PERF-INDEX): 6 performance indexes + 450-line test suite
- **Issue #532** (PERF-ANALYTICS): 2 analytics indexes
- Both migrations ready, waiting for clean database

---

## The Problem You're Solving

### Three Interconnected Issues

**Issue 1: Broken Foundation Migration**

- File: `alembic/versions/31937a4b9327_add_uploaded_files_table_and_fix_task_.py`
- Line 46 tries to alter `tasks` table that doesn't exist
- Tasks were refactored into lists system
- Blocks: `alembic upgrade head` fails on first migration

**Issue 2: SEC-RBAC Data Mapping**

- File: `alembic/versions/4d1e2c3b5f7a_add_owner_id_to_resource_tables_sec_rbac_357.py`
- Current logic tries to map session_id → user UUID (format mismatch)
- Alpha reality: All 542 test files belong to xian (alpha tester)
- Solution: Assign all files to xian's account

**Issue 3: Missing Conversations Tables**

- Migration `a9ee08bbdf8c` was skipped somehow
- Current database missing conversations/conversation_turns
- Leaves database in inconsistent state

### PM's Decisions (Final)

1. ✅ **No backward compatibility needed** - Unreleased application
2. ✅ **Assign test data to xian** - All data created before distinct users existed
3. ✅ **Wipe & recreate database NOW** - Perfect timing before other human users
4. ✅ **Add migration CI/CD testing** - Prevent this from happening again

---

## Your Tasks (20 minutes total)

### Task 1: Apply SEC-RBAC Alpha Fix (5 min) ⭐

**File**: `alembic/versions/4d1e2c3b5f7a_add_owner_id_to_resource_tables_sec_rbac_357.py`

**Current Code** (lines 55-62):

```python
op.execute("""
    UPDATE uploaded_files
    SET owner_id = (
        SELECT u.id FROM users u WHERE u.id::text = uploaded_files.session_id
    )
    WHERE session_id IS NOT NULL
""")
```

**Change To** (alpha solution):

```python
# Alpha: Assign all test files to xian (created before distinct user accounts)
op.execute("""
    UPDATE uploaded_files
    SET owner_id = '3f4593ae-5bc9-468d-b08d-8c4c02a5b963'
    WHERE owner_id IS NULL
""")
```

**Commit Message**:

```
fix(SEC-RBAC Phase 1.1): Alpha data ownership - assign test files to xian

All 542 uploaded_files are test data created before distinct user accounts
existed. Assigning to xian (3f4593ae-5bc9-468d-b08d-8c4c02a5b963) as the
alpha tester and logical owner of all pre-user-account test resources.

This is the correct model for alpha - test data belongs to the alpha tester.
When real users are added, their data will have proper ownership from creation.

Related: #357 SEC-RBAC Phase 1.1

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### Task 2: Fix Broken Foundation Migration (2 min) ⭐

**File**: `alembic/versions/31937a4b9327_add_uploaded_files_table_and_fix_task_.py`

**Current Code** (line 46):

```python
op.add_column("tasks", sa.Column("updated_at", sa.DateTime(), nullable=True))
```

**Action**: **DELETE THIS LINE ENTIRELY**

**Rationale**:

- Tasks table doesn't exist (was refactored into lists system)
- Line is obsolete and breaks migration chain
- uploaded_files table creation (earlier in migration) is still valid

**Commit Message**:

```
fix(migrations): Remove obsolete tasks table reference from foundation migration

Migration 31937a4b9327 tried to alter tasks table that doesn't exist.
Tasks were refactored into the lists system.

Removing obsolete line to unblock migration chain. uploaded_files table
creation (primary purpose of this migration) remains intact.

This fix enables clean database recreation from alembic upgrade head.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### Task 3: Database Wipe & Recreate (5-7 min) ⭐⭐⭐

**CRITICAL**: This is the most important task. Clean migration history matters for production.

**Step 1: Backup Current Database** (defensive measure)

```bash
docker exec piper-postgres pg_dump -U piper piper_morgan > /tmp/backup_before_wipe_$(date +%Y%m%d_%H%M%S).sql
```

**Step 2: Drop and Recreate Database**

```bash
# Connect to postgres database (not piper_morgan)
docker exec -it piper-postgres psql -U piper -d postgres

# In psql:
DROP DATABASE IF EXISTS piper_morgan;
CREATE DATABASE piper_morgan OWNER piper;
\q
```

**Step 3: Run All Migrations From Scratch**

```bash
# This should now work with your fixes
python -m alembic upgrade head
```

**Expected Output**:

- All 28+ migrations apply cleanly
- No errors
- Ends with: "Running upgrade ... -> b8e4f3c9a2d7, add analytics indexes"

**If Any Migration Fails**:

- **STOP immediately**
- Document which migration failed and why
- Report to Lead Developer
- Do NOT try to patch around it

---

### Task 4: Verify Migration Chain (3 min)

**Step 1: Check All Expected Tables Exist**

```bash
docker exec piper-postgres psql -U piper -d piper_morgan -c "\dt" | tee /tmp/tables_after_migration.txt
```

**Expected Tables** (28+ total):

- ✅ conversations
- ✅ conversation_turns
- ✅ uploaded_files (with owner_id column)
- ✅ projects (with owner_id column)
- ✅ feedback (with owner_id column)
- ✅ lists (with owner_id column)
- ✅ list_items (with owner_id column)
- ✅ list_memberships (with owner_id column)
- ✅ knowledge_nodes (with owner_id column)
- ✅ knowledge_edges (with owner_id column)
- ✅ learned_patterns (with owner_id column)
- And 17+ others...

**Step 2: Verify SEC-RBAC Schema**

```bash
# Check owner_id columns exist in resource tables
docker exec piper-postgres psql -U piper -d piper_morgan -c "
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE column_name = 'owner_id'
ORDER BY table_name;
" | tee /tmp/owner_id_columns.txt
```

**Expected**: 9 tables with owner_id columns (UUID type, NOT NULL except uploaded_files)

**Step 3: Verify Performance Indexes**

```bash
# Check #356 and #532 indexes exist
docker exec piper-postgres psql -U piper -d piper_morgan -c "
SELECT indexname, tablename
FROM pg_indexes
WHERE schemaname = 'public'
AND indexname LIKE 'idx_%'
ORDER BY tablename, indexname;
" | tee /tmp/performance_indexes.txt
```

**Expected**: 8 indexes total (6 from #356 + 2 from #532)

---

### Task 5: Close Issues #356 and #532 (2 min)

**Once verification passes**:

1. Update issue #356 description with deployment evidence
2. Update issue #532 description with deployment evidence
3. Close both issues with comment: "Deployed in clean database migration"

---

## Success Criteria (ALL Must Pass)

- [ ] Migration 31937a4b9327 fixed (tasks line removed)
- [ ] Migration 4d1e2c3b5f7a fixed (alpha data ownership)
- [ ] Both migrations committed with clear explanations
- [ ] Database wiped and recreated successfully
- [ ] `alembic upgrade head` completes without errors
- [ ] All expected tables exist (verified with \dt)
- [ ] All 9 owner_id columns present (verified with query)
- [ ] All 8 performance indexes exist (verified with pg_indexes)
- [ ] Issues #356 and #532 closed
- [ ] Evidence documented in session log

---

## Evidence Required

Create file: `dev/2025/11/22/sec-rbac-phase1.1-completion-report.md`

**Contents**:

```markdown
# SEC-RBAC Phase 1.1: Database Schema Completion Report

**Date**: November 22, 2025
**Agent**: Claude Code
**Status**: ✅ COMPLETE

## Summary

Successfully completed SEC-RBAC Phase 1.1 by:

1. Fixing migration chain blockers (2 migrations)
2. Wiping and recreating database with clean migration history
3. Deploying SEC-RBAC schema (9 owner_id columns)
4. Deploying performance indexes (#356, #532)

## Migration Fixes

### Fix 1: SEC-RBAC Alpha Data Ownership

**File**: 4d1e2c3b5f7a_add_owner_id_to_resource_tables_sec_rbac_357.py
**Change**: Replaced session_id mapping with direct assignment to xian
**Rationale**: All 542 test files created before distinct user accounts
**Commit**: [hash]

### Fix 2: Foundation Migration Tasks Table

**File**: 31937a4b9327*add_uploaded_files_table_and_fix_task*.py
**Change**: Removed obsolete tasks table reference (line 46)
**Rationale**: Tasks refactored into lists system
**Commit**: [hash]

## Database Recreation

**Backup Created**: /tmp/backup*before_wipe*[timestamp].sql (274KB)
**Database Dropped**: piper_morgan
**Database Recreated**: piper_morgan (clean)
**Migrations Applied**: 28 migrations from base → head
**Result**: All migrations applied cleanly ✅

## Verification Results

### Tables Created: [X] total

[Paste output of \dt command]

### Owner_id Columns: 9 confirmed

[Paste output of owner_id query]

### Performance Indexes: 8 confirmed

[Paste output of pg_indexes query]

## Issues Closed

- ✅ #356 (PERF-INDEX) - 6 composite indexes deployed
- ✅ #532 (PERF-ANALYTICS) - 2 analytics indexes deployed

## Phase 1.1 Status: ✅ COMPLETE

All database schema work complete:

- owner_id columns in all resource tables
- NOT NULL constraints properly applied
- Data migration strategy implemented (alpha ownership)
- Migration chain validated from scratch
- Foundation ready for Phase 1.3 (Endpoint Protection)

---

_Report created by: Claude Code_
_Next Phase: Phase 1.3 - Endpoint Authorization_
```

---

## What NOT to Do

**DO NOT**:

- Patch the database without wiping (we want clean migration history)
- Skip the backup (defensive measure)
- Try to preserve test data (PM approved wipe)
- Continue if migrations fail (STOP and report)
- Close issues without verification evidence

**DO**:

- Follow tasks in order (1 → 2 → 3 → 4 → 5)
- Provide evidence for each step
- Document exactly what you did
- Report any unexpected issues immediately
- Celebrate when all migrations apply cleanly!

---

## Migration Chain Should Look Like This After Fixes

```
Base (empty database)
    ↓
31937a4b9327 ✅ FIXED (uploaded_files creation, tasks line removed)
    ↓
... 26 migrations (all apply cleanly) ...
    ↓
a9ee08bbdf8c ✅ (conversations + conversation_turns created)
    ↓
... more migrations ...
    ↓
4d1e2c3b5f7a ✅ FIXED (SEC-RBAC schema + alpha data ownership)
    ↓
a7c3f9e2b1d4 ✅ (Issue #356 - 6 performance indexes)
    ↓
b8e4f3c9a2d7 ✅ (Issue #532 - 2 analytics indexes)
    ↓
HEAD (clean canonical state)
```

---

## Timeline Estimate

- Task 1 (SEC-RBAC fix): 5 minutes
- Task 2 (Foundation fix): 2 minutes
- Task 3 (Database wipe): 5-7 minutes
- Task 4 (Verification): 3 minutes
- Task 5 (Close issues): 2 minutes
- Documentation: 3 minutes

**Total**: ~20 minutes

---

## When You're Done

**Report to Lead Developer**:

- Phase 1.1 COMPLETE
- Migration chain validated
- Ready for Phase 1.3 (Endpoint Protection)
- Evidence provided in completion report

---

**Remember**: This is infrastructure work. Take your time, verify each step, provide evidence. Clean migration history is critical for production readiness.

Good luck! 🚀

---

_Prompt created by: Lead Developer (Cursor)_
_Date: November 22, 2025, 6:45 AM_
_Session: SEC-RBAC Phase 1.1 Completion_
_Authority: PM approved all decisions (6:38 AM)_
