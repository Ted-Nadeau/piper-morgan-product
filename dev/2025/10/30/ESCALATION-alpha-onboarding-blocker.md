# ESCALATION: Alpha User Onboarding Blocked

**Date**: 2025-10-30
**Time Invested**: 3+ hours
**Status**: ❌ BLOCKED - Database schema/migration mismatch
**Requester**: Alpha Tester (xian/alpha-one)
**Escalating To**: Chief Architect

---

## Executive Summary

Alpha user onboarding is blocked by cascading database architecture issues. After 3+ hours and 15+ bug fixes, the system still cannot complete a single alpha user setup due to:

1. **Database schema out of sync** between dev and test environments
2. **Alembic migration history mismatch** with actual schema state
3. **Foreign key architecture** not designed for dual user tables (alpha_users + users)
4. **No test coverage** for end-to-end onboarding flow

**Recommendation**: Stop reactive bugfixing. Need architectural design session for alpha user infrastructure.

---

## Environment Details

### Test Environment (alpha-one laptop)

- **Path**: `~/piper-morgan-workspace/piper-morgan-product`
- **Database**: PostgreSQL 5433, database `piper_dev`
- **State**: Schema partially created, migrations out of sync
- **Issue**: Alembic trying to create tables that already exist (`uploaded_files`)

### Dev Environment (xian laptop)

- **Path**: `/Users/xian/Development/piper-morgan`
- **Database**: PostgreSQL 5433, different credentials
- **State**: Migrations applied successfully
- **Issue**: Not being tested for onboarding flow

---

## Technical Root Cause

### Issue #259: Alpha/Production Data Separation

**Original Design** (incomplete implementation):

- `users` table for production users (String IDs)
- `alpha_users` table for alpha testers (UUID IDs)
- Alpha users can optionally migrate to production

**What Wasn't Considered**:

1. All existing tables have FK constraints to `users.id`
2. Audit logging, API keys, feedback, etc. all reference `users` table
3. SQLAlchemy relationships depend on FK constraints
4. Multiple environments need synchronized migrations

### Attempted Fixes (All Incomplete)

1. **Setup wizard** - Updated to create AlphaUser records
2. **Preferences script** - Updated to query alpha_users table
3. **Status script** - Updated to support alpha_users
4. **API key validator** - Disabled format validation (security issue)
5. **Audit log FK** - Removed constraint via migration (worked in dev, failed in test)
6. **Audit log relationships** - Commented out ORM relationships
7. **Migration sync** - Failed due to schema mismatch

---

## Current Blockers

### Blocker 1: Schema/Migration Mismatch (CRITICAL)

**Symptom**:

```
psycopg2.errors.DuplicateTable: relation "uploaded_files" already exists
```

**Analysis**:

- Alembic thinks it's at migration 0 (empty database)
- Actual database has many tables already created
- No `alembic_version` table tracking or it's out of sync

**Impact**: Cannot run any migrations to fix FK constraint issue

### Blocker 2: Foreign Key Constraint (CRITICAL)

**Symptom**:

```
asyncpg.exceptions.ForeignKeyViolationError:
insert or update on table "audit_logs" violates foreign key constraint "audit_logs_user_id_fkey"
Key (user_id)=(ecbf12eb-a20e-4344-8a4a-acfb78659e28) is not present in table "users".
```

**Analysis**:

- FK constraint `audit_logs_user_id_fkey` still exists in test database
- Migration to remove it can't run due to Blocker 1
- Alpha user IDs (UUID) can't satisfy FK to users.id (String)

**Impact**: Transaction rollback on API key storage, user account deleted

### Blocker 3: No End-to-End Test Coverage

**Issue**: No automated test for:

- Complete onboarding flow (wizard → preferences → status)
- Multi-environment migration sync
- Alpha user creation → API key storage → audit logging

**Impact**: Every fix requires manual testing, 10+ minute feedback loop

---

## Files Modified (Session)

1. `scripts/setup_wizard.py` - Alpha user creation (3 edits)
2. `scripts/preferences_questionnaire.py` - Alpha user queries (2 edits)
3. `scripts/status_checker.py` - Alpha user support (1 edit)
4. `services/database/models.py` - FK removal, relationship disable (2 edits)
5. `services/security/provider_key_validator.py` - Relaxed OpenAI validation (1 edit)
6. `services/security/user_api_key_service.py` - Disabled validation (1 edit)
7. `alembic/versions/648730a3238d_*.py` - FK removal migration (1 new)

**Total**: 11 files, 15+ commits, 0 successful end-to-end completions

---

## Proposed Solutions

### Option 1: Nuclear Reset (30 minutes)

**Steps**:

1. Drop and recreate test database
2. Run all migrations from scratch
3. Verify FK constraint is removed
4. Test onboarding flow

**Pros**: Clean slate, known state
**Cons**: Doesn't fix underlying architecture issues
**Risk**: Medium - might hit different issues

### Option 2: Manual Schema Fix (60 minutes)

**Steps**:

1. Manually stamp Alembic to current revision
2. Manually drop FK constraint via SQL
3. Skip broken migrations
4. Test onboarding flow

**Pros**: Preserves existing data
**Cons**: Fragile, hard to reproduce
**Risk**: High - manual SQL on production

### Option 3: Architectural Redesign (4-8 hours)

**Steps**:

1. Design proper dual-user-table architecture
2. Create polymorphic FK strategy or separate audit tables
3. Build migration path from current state to target state
4. Add E2E test coverage for onboarding
5. Document multi-environment deployment process

**Pros**: Fixes root causes, sustainable long-term
**Cons**: Delays alpha testing by days
**Risk**: Low - proper design prevents future issues

### Option 4: Temporary Workaround (15 minutes)

**Steps**:

1. Disable audit logging entirely for alpha phase
2. Remove all FK constraints manually
3. Let users onboard without audit trail
4. Fix properly post-alpha

**Pros**: Fastest unblock
**Cons**: Security gap, technical debt
**Risk**: Medium - no audit trail during alpha

---

## Recommendation

**Immediate** (Today): Option 1 (Nuclear Reset)

- Get alpha tester unblocked TODAY
- Document exact reproduction steps
- Capture current schema state for analysis

**Short-term** (This Week): Option 3 (Architectural Redesign)

- Schedule 4-hour design session with chief architect
- Design proper alpha user infrastructure
- Build test coverage for onboarding flow

**Long-term** (Next Sprint): Database Architecture Review

- Review all FK constraints for multi-tenant support
- Design migration strategy for multiple environments
- Create deployment runbook for schema changes

---

## Questions for Chief Architect

1. **User Model Strategy**: Should we:

   - Keep dual tables (alpha_users + users)?
   - Merge into single users table with type discriminator?
   - Use separate databases entirely?

2. **Audit Logging**: Should we:

   - Make audit_logs.user_id polymorphic (support both tables)?
   - Create separate alpha_audit_logs table?
   - Disable audit logging for alpha phase?

3. **Migration Management**: How should we:

   - Handle schema drift between environments?
   - Validate migration state before applying?
   - Test migrations before deploying?

4. **Foreign Key Strategy**: Should we:

   - Remove all FK constraints for alpha phase?
   - Use soft references (no DB-level FKs)?
   - Design for polymorphic references from start?

5. **Testing Strategy**: How do we:
   - Test multi-environment deployments?
   - Validate end-to-end onboarding flows?
   - Catch these issues before they block users?

---

## Success Criteria

**Minimum** (Onboarding works):

- Alpha user can complete setup wizard
- API keys stored successfully
- Preferences saved correctly
- System status shows configured state

**Optimal** (Sustainable):

- Automated E2E test for onboarding
- Migration strategy documented
- Multi-environment deployment tested
- No disabled security features (audit logging, validation)

---

## Session Log

Full debugging history: `dev/active/2025/10/30/session-log-alpha-onboarding.md`

**Key Stats**:

- Time: 3+ hours
- Bugs fixed: 15+
- Commits: 15+
- Successful onboardings: 0
- Environments tested: 2 (neither working)

---

## Next Steps

**Awaiting Decision**:

1. Which solution option to pursue?
2. Who will lead architectural redesign?
3. Timeline for alpha testing start?

**Blocked On**:

- Database schema synchronization
- FK constraint removal in test environment
- Architectural guidance on dual-user-table design

**Ready To Provide**:

- Complete code history
- Database schema dumps
- Error logs and stack traces
- Reproduction steps

---

**Status**: ⏸️ PAUSED - Awaiting architectural guidance
**Priority**: 🔴 CRITICAL - Blocking alpha testing program
**Estimated Fix Time**: 30 min (reset) to 8 hours (proper design)
