# Group 2 Discovery Report: CORE-USER

**Date**: October 23, 2025, 9:57 AM PDT
**Agent**: Claude Code (prog-code)
**Sprint**: A7 (Polish & Buffer)
**Discovery Phase**: Group 2 (CORE-USER)

---

## Executive Summary

**Discovery Status**: COMPLETE ✅

**Key Findings**:
1. ✅ Database running (piper_morgan on PostgreSQL port 5433)
2. ✅ Users table exists with proper schema
3. ❌ alpha_users table does NOT exist (Issue #259 needs to create it)
4. ✅ xian user EXISTS in users table (created Oct 22, 2025)
5. ✅ Alembic migrations up-to-date (fcc1031179bb - audit logging)
6. ⚠️ Users table MISSING 'role' column (need to add for superuser support)
7. ✅ Legacy config exists (config/PIPER.user.md)
8. ⚠️ 85 users in database (many test users - need cleanup strategy)

**Ready to Proceed?**: YES, with clarifications needed

---

## Database Infrastructure

### Connection Details
- **Host**: localhost
- **Port**: 5433
- **Database**: piper_morgan (NOT "piper")
- **User**: piper (NOT "postgres")
- **Container**: piper-postgres (running, healthy)
- **Access Method**: `docker exec piper-postgres psql -U piper -d piper_morgan`

### Current Migration Status

**Alembic Version**: fcc1031179bb (head)

**Recent Migrations** (most recent first):
1. `fcc1031179bb` - add_audit_logging_issue_249 (Oct 22, 2025)
2. `8d46e93aabc3` - add_user_api_keys_table_issue_228 (Oct 22, 2025)
3. `68767106bfb6` - add_user_model_issue_228
4. `f3a951d71200` - add_token_blacklist_table_issue_227

**Migration for Issue #259**: Will be NEW migration (next after fcc1031179bb)

---

## Users Table Analysis

### Current Schema

```sql
Table "public.users"
Column          | Type                        | Nullable | Default
----------------+-----------------------------+----------+---------
id              | character varying(255)      | not null |
username        | character varying(255)      | not null |
email           | character varying(255)      | not null |
password_hash   | character varying(500)      |          |
is_active       | boolean                     | not null | true
is_verified     | boolean                     | not null | false
created_at      | timestamp without time zone | not null | now()
updated_at      | timestamp without time zone | not null | now()
last_login_at   | timestamp without time zone |          |

Indexes:
  "users_pkey" PRIMARY KEY, btree (id)
  "idx_users_active" btree (is_active)
  "idx_users_email" UNIQUE, btree (email)
  "idx_users_username" UNIQUE, btree (username)

Referenced by:
  audit_logs (user_id)
  feedback (user_id)
  personality_profiles (user_id)
  token_blacklist (user_id)
  user_api_keys (user_id)
```

### CRITICAL ISSUE: Missing 'role' Column

**Problem**: GitHub Issue #261 expects a 'role' column for superuser designation:
```python
role=\"superuser\"
```

**Current Reality**: No 'role' column exists

**Evidence**:
```
ERROR:  column "role" does not exist
LINE 1: SELECT id, username, email, role, created_at FROM users WHER...
```

**Decision Required**: Add 'role' column in Issue #259 migration OR create separate migration?

**Recommendation**: Add 'role' column in Issue #259 migration since Issue #261 depends on it.

---

## xian User Status

### Current State

**User Exists**: ✅ YES

```
id   | username | email            | is_active | created_at
-----+----------+------------------+-----------+----------------------------
xian | xian     | xian@example.com | t         | 2025-10-22 14:21:06.662986
```

**Analysis**:
- Created Oct 22, 2025 (yesterday)
- Email: xian@example.com (placeholder, need real email)
- Active and verified
- ID is VARCHAR "xian" (not UUID - inconsistency!)

**Issues for #261**:
1. User already exists (not a "migration" - just updates)
2. No 'role' column to mark as superuser
3. Email is placeholder (need real email from config?)
4. ID format inconsistent (VARCHAR vs UUID pattern in Issue #259)

---

## alpha_users Table Status

**Exists**: ❌ NO

**Evidence**:
```
Did not find any relation named "alpha_users".
```

**Action Required**: Issue #259 will create this table

---

## Database User Count

**Total Users**: 85

**Sample Users**:
```
id                        | username                   | email
--------------------------+---------------------------+---------------------------------------
warmth_user_0.3           | warmth_user_0.3           | warmth_user_0.3@example.com
perf_5                    | perf_5                    | perf_5@example.com
perf_test_user_5          | perf_test_user_5          | perf_test_user_5@example.com
concurrent_user_2         | concurrent_user_2         | concurrent_user_2@example.com
integration_test_analysis | integration_test_analysis | integration_test_analysis@example.com
xian                      | xian                      | xian@example.com
```

**Observation**: Many test users from integration tests. These are probably test artifacts.

**Question for PM**: Should we:
1. Clean up test users before creating alpha_users?
2. Leave test users (they're harmless)
3. Add cleanup as part of Issue #259?

---

## Legacy Configuration

### config/PIPER.user.md

**Exists**: ✅ YES

**Content Summary**:
- User: Christian (xian)
- Role: Product Manager & Developer
- Timezone: Pacific Time (PT)
- GitHub integration config
- Notion integration config (with database IDs)
- Calendar integration config
- Slack integration config
- Morning standup config
- Response personality config
- Plugin configuration

**Key Settings**:
```yaml
user_identity:
  user_id: "xian"
  display_name: "Christian"
  role: "Lead Developer"
  context: "working on Piper Morgan platform"
```

**Email**: Not explicitly stated in config (need to confirm with PM)

**Migration Strategy for #261**:
- Extract preferences from YAML
- Create proper user preferences JSON
- Archive legacy config (don't delete)

---

## All Database Tables (24 total)

```
action_humanizations
alembic_version
audit_logs            ← New from Issue #249
conversation_turns
conversations
features
feedback
intents
knowledge_edges
knowledge_nodes
list_items
lists
personality_profiles
products
project_integrations
projects
stakeholders
tasks
token_blacklist      ← New from Issue #227
uploaded_files
user_api_keys        ← New from Issue #228
users                ← Existing, need to extend
work_items
workflows
```

**Note**: No alpha_users table yet

---

## GitHub Issues Analysis

### Issue #259: CORE-USER-ALPHA-TABLE

**Objective**: Create alpha_users table for clean alpha/production separation

**Schema from Issue** (key fields):
```sql
CREATE TABLE alpha_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Alpha-specific
    alpha_wave INTEGER DEFAULT 2,
    test_start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    test_end_date TIMESTAMP,
    migrated_to_prod BOOLEAN DEFAULT FALSE,
    migration_date TIMESTAMP,
    prod_user_id UUID REFERENCES users(id),  ← ISSUE: users.id is VARCHAR!

    -- Preferences
    preferences JSONB DEFAULT '{}',
    learning_data JSONB DEFAULT '{}',

    -- Metadata
    notes TEXT,
    feedback_count INTEGER DEFAULT 0,
    last_active TIMESTAMP
);
```

**Schema Issues Discovered**:
1. **Foreign Key Problem**: `prod_user_id UUID REFERENCES users(id)`
   - Issue schema expects `users.id` to be UUID
   - Reality: `users.id` is VARCHAR(255)
   - **Solution**: Change FK to VARCHAR(255) OR migrate users.id to UUID

**Decision Required**: How to handle users.id type mismatch?

**Options**:
- **A**: Change alpha_users.prod_user_id to VARCHAR(255) (quick fix)
- **B**: Migrate users.id from VARCHAR to UUID (more work, cleaner)
- **C**: Add UUID field to users, keep VARCHAR id (dual keys)

**Recommendation**: Option A for now (minimal change), consider Option B for future

### Issue #260: CORE-USER-MIGRATION

**Objective**: CLI tool for alpha→production user migration

**Key Components**:
1. MigrationOptions dataclass (what to migrate)
2. AlphaMigrationService (execute migration)
3. CLI command: `piper migrate-user xian-alpha`
4. Backup/archive capability

**Dependencies**:
- Requires Issue #259 complete (alpha_users table exists)
- Requires Issue #261 complete (xian production user exists)

**Implementation Location**:
- Service: `services/user/alpha_migration_service.py` (NEW)
- CLI: Update `main.py` with new command

### Issue #261: CORE-USER-XIAN

**Objective**: Migrate xian from legacy to proper user structure

**Current Reality vs Issue Expectations**:

**Issue Expects**:
```python
xian_user = User(
    id=uuid.uuid4(),  # New proper UUID
    username="xian",
    email="xian@piper-morgan.com",
    role="superuser",  # ← Need to add role column!
    # ...
)
```

**Reality**:
- xian user ALREADY EXISTS in users table
- xian.id = "xian" (VARCHAR), not UUID
- No 'role' column in users table
- Email is placeholder: xian@example.com

**Issue Says**: "Migrate xian superuser to proper user structure"
**Reality**: xian is already in proper table, just needs enhancement

**Work Actually Needed**:
1. Add 'role' column to users table
2. Update xian user with role='superuser'
3. Update email from config (if different)
4. Migrate config/PIPER.user.md preferences to database
5. Archive legacy config

**NOT Needed**:
- Create new user (already exists)
- Migrate from different table (already in users)

---

## Discrepancies Between Issues and Reality

### 1. users.id Type Mismatch

**Issue #259 expects**: `users.id` is UUID
**Reality**: `users.id` is VARCHAR(255)

**Impact**: Foreign key `alpha_users.prod_user_id` needs type adjustment

### 2. xian User Already Exists

**Issue #261 expects**: Need to create xian user
**Reality**: xian user already exists, just needs enhancements

**Impact**: Issue #261 is more about "enhance" than "migrate"

### 3. Missing role Column

**Issue #261 expects**: `user.role` column for superuser
**Reality**: No role column in users table

**Impact**: Need to add role column (in Issue #259 or separate migration)

### 4. Test User Cleanup

**Issue #259 doesn't mention**: 85 existing users (many test users)
**Reality**: Database has test artifacts

**Impact**: May want cleanup before alpha users added

---

## Recommendations

### For Issue #259 (CORE-USER-ALPHA-TABLE)

**Changes to Schema**:
```sql
-- Adjust FK type to match users.id
prod_user_id VARCHAR(255) REFERENCES users(id),  -- Not UUID

-- Add role column to users table in same migration
ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'user';
CREATE INDEX idx_users_role ON users(role);
```

**Rationale**:
- Fixes FK type mismatch
- Adds role column needed by Issue #261
- Single migration handles both needs

### For Issue #260 (CORE-USER-MIGRATION)

**Proceed as planned** after Issue #259 complete

**Note**: Main.py already has Typer CLI infrastructure

### For Issue #261 (CORE-USER-XIAN)

**Revised Scope**:
1. ~~Create xian user~~ (already exists)
2. Update xian.role = 'superuser' (new)
3. Update xian.email from config (if needed)
4. Migrate preferences from config/PIPER.user.md
5. Archive legacy config

**SQL**:
```sql
-- After role column added by Issue #259
UPDATE users SET role = 'superuser' WHERE username = 'xian';
```

---

## Questions for PM

### Critical (Block Progress)
1. **users.id type**: Keep VARCHAR or migrate to UUID?
   - Option A: Keep VARCHAR (quick, works)
   - Option B: Migrate to UUID (cleaner, more work)

2. **role column**: Add in Issue #259 migration or separate?
   - Recommend: Add in Issue #259 (single migration)

### Important (Affect Scope)
3. **xian email**: What's the real email? (config doesn't specify)
   - Current: xian@example.com
   - Needed: Real email for Issue #261

4. **Test users**: Clean up 85 test users or leave them?
   - Recommend: Leave (not harmful, may be needed for tests)

### Nice to Have (Future)
5. **SQLAlchemy models**: Create models for alpha_users?
   - Recommend: Yes (consistency with other tables)

---

## Stop Conditions Met?

**NO BLOCKERS FOUND** ✅

**Proceed with**:
1. Issue #259 with schema adjustments (VARCHAR FK, add role column)
2. Issue #260 as planned
3. Issue #261 with revised scope (enhance, not create)

**Clarifications Needed**:
- Confirm users.id stays VARCHAR (not UUID)
- Confirm role column added in Issue #259
- Get real email for xian user

---

## Next Steps

**After PM Review**:
1. Begin Issue #259 implementation:
   - Create Alembic migration
   - Add role column to users
   - Create alpha_users table (with VARCHAR FK)
   - Apply migration
   - Create SQLAlchemy model

2. Test multi-user isolation

3. Proceed to Issue #260 (migration CLI)

4. Complete Issue #261 (enhance xian user)

---

**Discovery Complete**: October 23, 2025, 10:08 AM PDT
**Duration**: ~11 minutes
**Evidence**: All commands documented, full schema captured
**Thoroughness**: Complete with issue-by-issue analysis
