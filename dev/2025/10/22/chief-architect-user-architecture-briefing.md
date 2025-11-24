# Chief Architect Briefing: User Architecture & Migration Strategy

**To**: Chief Architect (Cursor/Opus)
**From**: Lead Developer (Sonnet)
**Date**: Tuesday, October 22, 2025, 5:13 PM
**Subject**: Architectural Guidance Required for Sprint A7 CORE-USER Issues

---

## Executive Summary

Sprint A7 includes three CORE-USER issues (#259-261) that require architectural decisions around user table structure, data migration strategy, and superuser/role implementation. These decisions impact the migration of legacy "xian in the cracks" data to proper user structure while preserving all knowledge graph associations and maintaining multi-tenant architecture principles.

**Critical Path**: These decisions block implementation of CORE-USER group (3 of 12 Sprint A7 issues). Need architectural guidance before proceeding with Sprint A7 execution.

**Context**: Roadmap v10.0 and Current State updated by Code (October 22, 3:30 PM). Sprint A6 complete, A7 in progress (12 issues), A8 planned for Alpha prep.

---

## Context: The "xian in the cracks" Problem

### Historical Evolution

**Phase 1: Pre-User Era (May-August 2025)**
- Piper Morgan started as hobby project
- PM (Christian) was inventor + only user
- No user table existed
- No boundaries or multi-user concept
- Real project data created (PM's actual projects, knowledge, workflows)
- **Status**: "xian living in the cracks" - god mode by default, no structure

**Phase 2: Alpha Test Account Creation (September 2025)**
- User table implemented (Sprint A6, #227-229)
- Created `xian-alpha` as first proper alpha test account
- Separate from PM's "real" account
- Purpose: Safe experimentation without affecting real data
- **Status**: Dummy account, working fine

**Phase 3: Current State (October 2025)**
- Sprint A6 complete: Multi-user infrastructure operational
- xian-alpha exists as proper test user
- Legacy "xian in the cracks" data still unstructured
- Need to create production "xian" superuser account
- **Status**: Migration needed from Phase 1 → Phase 3

### The Three xian Identities

**1. Legacy xian (Pre-User Era)**
- No formal user record
- All early project/knowledge data
- God mode by default (no boundaries)
- **Needs**: Migration to proper structure

**2. xian-alpha (Test Account)**
- Proper user record in database
- Test/dummy data only
- Can experiment safely
- **Status**: Keep as-is, working fine

**3. Production xian (Superuser - Not Yet Created)**
- Needs to be created via migration
- Inherits all legacy data from #1
- Has superuser powers (structured god mode)
- Distinct from xian-alpha and future users
- **Status**: Sprint A7 deliverable (#261)

### Key Requirements from PM

PM (Christian) explicitly stated:

> "But the real information about my real projects etc. that we added when I was the only user now needs to migrate from that old pre-user-table existence to a new forward-compatible xian account. At least in my own instance this user should also be able to have superuser powers (whereas if I later onboard my colleague from Kind they will not be sysadmins or god power users for the whole instance or platform."

**Translation**:
1. ✅ Superuser concept must exist after migration
2. ✅ Different from admin (Kind colleague = admin, not superuser)
3. ✅ Superuser can do anything, including platform-level operations
4. ✅ Admin can manage users, but bounded by system rules
5. ✅ Cannot "live in the cracks" anymore - must be proper structure

---

## Sprint A7 CORE-USER Issues

### Issue #259: CORE-USER-ALPHA-TABLE
**Create Alpha Users Table**

**Objective**: Separate alpha testers from production users with clean migration path

**Current Uncertainty**:
- Should this be separate table or flag on users table?
- What fields needed for migration tracking?
- How to handle relationships (API keys, conversations, knowledge)?

**Estimated**: 1-2 hours → Likely 20 min (if pattern holds)

---

### Issue #260: CORE-USER-MIGRATION
**Alpha→Production Migration Tool**

**Objective**: CLI tool for migrating alpha accounts to production when ready

**Current Uncertainty**:
- What data to migrate (all? selective? user choice)?
- How to preserve relationships (knowledge graph, conversations)?
- Preview before commit?
- Rollback capability?

**Estimated**: 2-3 hours → Likely 20 min (if pattern holds)

---

### Issue #261: CORE-USER-XIAN
**Migrate xian Superuser to Proper User Structure**

**Objective**: Create production xian account with superuser powers, migrate all legacy data

**Current Uncertainty**:
- How to identify legacy data (no user_id on old records)?
- Retroactive user_id assignment vs separate legacy container?
- Preserve audit trail that data was created pre-user-table?
- Superuser implementation (role, flag, permission set)?

**Estimated**: 1-2 hours → Likely 20 min (if pattern holds)

---

## Decision Point 1: User Table Architecture

### Context

Need to separate alpha users from production users while supporting clean migration path. Two approaches possible:

### Option A: Separate Table (`alpha_users`)

**Schema**:
```sql
-- Alpha users table
CREATE TABLE alpha_users (
  id UUID PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  email TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  migration_status TEXT DEFAULT 'active',  -- 'active', 'migrated', 'declined'
  migration_date TIMESTAMP NULL,
  migrated_to_user_id UUID REFERENCES users(id) NULL,
  ...
);

-- Production users table (unchanged)
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  email TEXT,
  role TEXT DEFAULT 'user',  -- 'superuser', 'admin', 'user'
  created_at TIMESTAMP DEFAULT NOW(),
  ...
);

-- All relationships reference either table
CREATE TABLE api_keys (
  user_id UUID,  -- Could reference alpha_users OR users
  ...
);
```

**Pros**:
- ✅ Clean separation (easy to identify alpha users)
- ✅ Easy cleanup post-alpha (drop table when done)
- ✅ No alpha cruft in production schema long-term
- ✅ Clear migration status tracking

**Cons**:
- ❌ Duplicate schema (maintain two user tables)
- ❌ Complex relationships (foreign keys can point to either table)
- ❌ Migration requires moving data between tables
- ❌ Query complexity (JOIN across both tables in some cases)

---

### Option B: Single Table with Flags

**Schema**:
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  email TEXT,
  role TEXT DEFAULT 'user',  -- 'superuser', 'admin', 'user'
  user_type TEXT DEFAULT 'production',  -- 'alpha', 'production'
  alpha_start_date TIMESTAMP NULL,
  alpha_end_date TIMESTAMP NULL,
  migration_status TEXT NULL,  -- NULL for production, status for alpha
  created_at TIMESTAMP DEFAULT NOW(),
  ...
);

-- All relationships reference single table
CREATE TABLE api_keys (
  user_id UUID REFERENCES users(id),
  ...
);
```

**Pros**:
- ✅ Single source of truth (one user table)
- ✅ Simpler relationships (all foreign keys to users)
- ✅ "Migration" is just flag update (user_type: alpha → production)
- ✅ Easier to query (no JOIN complexity)

**Cons**:
- ❌ Alpha fields in production schema forever
- ❌ Harder to identify alpha users (requires WHERE clause)
- ❌ No hard separation (alpha and production mixed)
- ❌ Cleanup requires archiving flags, not dropping table

---

### PM's Input

From conversation:
> "I will ask the chief architect re schema vs. flag"

**Question for Chief Architect**: Which approach aligns better with Piper Morgan's multi-tenant future and clean separation principles?

---

## Decision Point 2: Migration Data Scope

### Context

Migration tool needs to handle all user-associated data. PM intuition: "User just needs to migrate to new table and retain all associations."

### Data Categories to Migrate

**Core User Data** (Obvious):
- ✅ User record (username, email, preferences)
- ✅ API keys (encrypted, OS keychain)
- ✅ Audit logs (security trail)
- ✅ Session history

**Relationship Data** (Important):
- ✅ Conversations/messages (chat history)
- ✅ Project associations (PM's real projects)
- ✅ Task/workflow history (PM work)
- ✅ Integration connections (GitHub, Notion, Slack)

**Knowledge Graph Data** (Critical!):
PM explicitly asked: "any and all data (knowledge graph too, yes?)"

**Answer**: YES, knowledge graph must migrate!

- ✅ **Nodes**: All nodes created by/for user
- ✅ **Edges**: All relationships involving user's nodes
- ✅ **Embeddings**: Vector representations for user's knowledge
- ✅ **Metadata**: Tags, categories, timestamps
- ✅ **Boundary rules**: User-specific boundary enforcement

**System Data** (Unclear):
- ⚠️ Learning/feedback events
- ⚠️ Performance metrics
- ⚠️ Feature usage analytics

### Migration Strategy Options

**Option A: All-or-Nothing**
```python
# Migrate everything
migrate_user(alpha_user_id, target_role='user'):
    # Move user record
    # Move all API keys
    # Move all conversations
    # Move all knowledge graph nodes/edges
    # Move all audit logs
    # Update all foreign key references
    return new_user_id
```

**Pros**: Simple, no data loss, complete migration
**Cons**: No user choice, can't exclude unwanted data

**Option B: Selective with Defaults**
```python
# Migrate with options
migrate_user(alpha_user_id,
             include_conversations=True,
             include_knowledge=True,
             include_audit_logs=True,
             preview=False):
    if preview:
        show_migration_preview()
        return

    # Migrate selected data
    ...
```

**Pros**: User control, can exclude test data
**Cons**: More complex, risk of partial migration

**Option C: Lift and Shift (PM's Intuition)**
```python
# User migrates to new table, all associations follow
if Option A (separate tables):
    move_user_record(alpha_users → users)
    # All FKs automatically reference new user_id

if Option B (single table):
    update_user_type(alpha → production)
    # No data movement, just flag change
```

**Pros**: Matches PM's intuition, preserves relationships
**Cons**: Assumes all data wanted (no cleanup of test data)

### PM's Input

From conversation:
> "I would think any and all data (knowledge graph too, yes?) ... it may be that the user just needs to migrate to the new table and retain all associations? we can also get advice from the chief re this too"

**Questions for Chief Architect**:
1. Should migration be all-or-nothing or selective?
2. Do we preserve timestamps (created_at) from alpha phase?
3. How do we handle shared knowledge (if multiple alpha users reference same node)?
4. Should user be able to preview what will migrate before committing?

---

## Decision Point 3: Superuser vs Admin vs User Roles

### Context

Three distinct permission levels needed after migration. PM explicitly stated superuser ≠ admin.

### PM's Requirements

From conversation:
> "At least in my own instance this user should also be able to have superuser powers (whereas if I later onboard my colleague from Kind they will not be sysadmins or god power users for the whole instance or platform."

**Interpretation**:
- ✅ PM (xian) = superuser (god mode, structured)
- ✅ Kind colleague = admin (user management, not god mode)
- ✅ Alpha testers = user (standard boundaries)

### Proposed Role Hierarchy

**Superuser** (Platform Owner):
- **Who**: PM (Christian), future platform maintainers
- **Powers**:
  - Platform-level configuration
  - Can access any user's data (for support/debugging)
  - Can modify system code/architecture
  - Can bypass normal boundaries
  - Can promote/demote admins
- **Use Cases**: Debugging, support, system maintenance

**Admin** (Instance Manager):
- **Who**: Kind colleague, future customer admins
- **Powers**:
  - User management (create, disable, reset passwords)
  - Instance configuration (non-platform)
  - View aggregate metrics/logs
  - Manage integrations (API keys for instance)
- **Boundaries**:
  - Cannot access other users' private data
  - Cannot modify platform code
  - Cannot bypass system rules
- **Use Cases**: Onboarding users, managing instance

**User** (Standard):
- **Who**: xian-alpha, future alpha testers, production users
- **Powers**:
  - Own data only
  - Standard CRUD operations
  - Personal integrations (own API keys)
- **Boundaries**:
  - Cannot see other users
  - Cannot access system configuration
  - Full boundary enforcement
- **Use Cases**: Normal Piper Morgan usage

### Implementation Options

**Option A: Role Field**
```sql
CREATE TABLE users (
  role TEXT DEFAULT 'user',  -- 'superuser' | 'admin' | 'user'
  ...
);
```

**Pros**: Simple, single field
**Cons**: Hard to extend (what if need more roles?)

**Option B: Permission Flags**
```sql
CREATE TABLE users (
  is_superuser BOOLEAN DEFAULT FALSE,
  is_admin BOOLEAN DEFAULT FALSE,
  ...
);
```

**Pros**: Flexible (user can be both admin and superuser)
**Cons**: More fields, potential confusion

**Option C: Permission Table**
```sql
CREATE TABLE user_permissions (
  user_id UUID REFERENCES users(id),
  permission TEXT,  -- 'superuser', 'admin', 'manage_users', ...
  granted_at TIMESTAMP,
  granted_by UUID REFERENCES users(id),
  ...
);
```

**Pros**: Most flexible, auditable
**Cons**: Complex, overkill for Alpha

### Questions for Chief Architect

1. **Implementation**: Role field, permission flags, or permission table?
2. **Multiplicity**: Can user be both superuser and admin, or mutually exclusive?
3. **Audit**: How do we audit superuser actions (since they bypass boundaries)?
4. **Activation**: Should superuser mode require explicit activation (like sudo), or always active?

---

## Decision Point 4: Legacy "xian in the cracks" Migration

### Context

Pre-user-table data exists without proper user association. Need to migrate to production xian account.

### Current State of Legacy Data

**What Exists**:
- Knowledge graph nodes/edges (no `user_id` field existed!)
- Conversations (stored where? need to verify)
- API keys (in PIPER.user.md, not database)
- Projects/tasks (need to identify storage)

**What Doesn't Exist**:
- User record for legacy xian
- Foreign key associations (user_id)
- Audit trail (who created what when)

### Migration Strategy Options

**Option A: Retroactive Association**
```sql
-- Step 1: Create production xian superuser
INSERT INTO users (id, username, role)
VALUES ('xian-uuid', 'xian', 'superuser');

-- Step 2: Associate all orphaned knowledge
UPDATE knowledge_nodes
SET user_id = 'xian-uuid'
WHERE user_id IS NULL;

UPDATE knowledge_edges
SET user_id = 'xian-uuid'
WHERE user_id IS NULL;

-- Step 3: Associate all orphaned conversations
UPDATE conversations
SET user_id = 'xian-uuid'
WHERE user_id IS NULL;

-- Step 4: Migrate API keys from PIPER.user.md → database
-- (manual step or script)
```

**Pros**: Clean, everything associated with proper user
**Cons**: Loses audit trail that data was created pre-user-table

---

**Option B: Legacy Data Container**
```sql
-- Keep legacy data separate but accessible
CREATE TABLE legacy_data (
  id UUID PRIMARY KEY,
  data_type TEXT,  -- 'knowledge_node', 'conversation', etc.
  data_id UUID,
  original_created_at TIMESTAMP,
  migrated_to_user_id UUID REFERENCES users(id),
  migration_date TIMESTAMP,
  ...
);

-- Legacy nodes remain in knowledge_nodes but flagged
ALTER TABLE knowledge_nodes ADD COLUMN is_legacy BOOLEAN DEFAULT FALSE;
```

**Pros**: Preserves audit trail, visible that data is legacy
**Cons**: Complex queries, legacy flag in schema forever

---

**Option C: Hybrid Approach**
```sql
-- Retroactively assign user_id but track migration
UPDATE knowledge_nodes
SET
  user_id = 'xian-uuid',
  metadata = metadata || '{"migrated_from": "pre_user_era", "migration_date": "2025-10-23"}'
WHERE user_id IS NULL;
```

**Pros**: Clean schema, audit trail in metadata
**Cons**: Metadata query complexity

### Questions for Chief Architect

1. **Association**: Retroactive user_id assignment, legacy container, or hybrid?
2. **Audit Trail**: How to preserve history that data was created pre-user-table?
3. **Read-Only**: Should legacy data be read-only until migration, or fully accessible?
4. **Multiple Claims**: Can multiple users claim legacy knowledge, or exclusive to xian?

---

## Sprint A7 Context & Timeline

### Current Sprint Status

**Sprint A7: Polish & Buffer** (12 issues total)
- **Group 1: CORE-UX** (4 issues, ~1h actual)
- **Group 2: CORE-KEYS** (3 issues, ~1.5h actual)
- **Group 3: CORE-USER** (3 issues, ~1h actual) ← **BLOCKED ON THESE DECISIONS**
- **Group 4: CORE-PREF** (1 issue, ~45min actual)
- **Group 5: Critical Fixes** (2 issues, ~45min actual)

**Execution Plan** (from gameplan):
- **Day 1 (Wed Oct 23)**: Groups 1, 2, 4, 5 (not blocked) - ~4h actual
- **Day 2 (Thu Oct 24)**: Group 3 (CORE-USER) - ~1h actual
- **Day 3 (Fri Oct 25)**: Buffer/polish if needed

### Why Architectural Decisions Block Progress

**Without decisions**:
- Cannot design alpha_users schema (don't know if separate table or flag)
- Cannot implement migration tool (don't know data scope)
- Cannot create xian superuser (don't know role implementation)

**With decisions**:
- Clear schema design
- Defined migration scope
- Structured superuser implementation
- Estimated ~1 hour total for all 3 issues

**Impact of Delay**:
- Groups 1, 2, 4, 5 can proceed (9 of 12 issues)
- Group 3 waits for architectural guidance
- Minimal sprint delay if decisions by Wednesday morning

---

## Recommended Decision Process

### Option 1: Full Huddle (1-2 hours)

**When**: Tomorrow (Wed Oct 23) morning
**Participants**: PM + Chief Architect
**Outcome**: Decisions on all 4 questions
**Timeline**: CORE-USER implementation starts afternoon

### Option 2: Async Architectural Brief (30 min)

**When**: Tonight/tomorrow morning
**Process**: Chief Architect reviews this briefing, provides recommendations
**Outcome**: Documented decisions for Lead Developer
**Timeline**: CORE-USER implementation starts Wed/Thu

### Option 3: Serena Deep Dive (45 min)

**When**: Tomorrow morning
**Process**: Use Serena to analyze existing architecture patterns, recommend approach
**Outcome**: Architecture-consistent decisions
**Timeline**: CORE-USER implementation starts afternoon

---

## My Recommendations (Lead Developer)

### Question 1: User Architecture

**Recommendation**: **Option B** (Single Table with Flags)

**Reasoning**:
- Simpler relationships (all FKs to users)
- "Migration" is just flag update (minimal data movement)
- Aligns with PM's intuition ("user just migrates to new table and retains associations")
- Alpha fields are small (2-3 columns), acceptable cruft
- Easier to implement (20 min vs 1h for separate tables)

### Question 2: Migration Data Scope

**Recommendation**: **Option C** (Lift and Shift with Preview)

**Reasoning**:
- Matches PM's intuition ("any and all data")
- Include knowledge graph (PM explicitly confirmed)
- Preserve all relationships automatically
- Add preview capability (show what will migrate)
- Add optional rollback (in case of mistakes)

### Question 3: Superuser vs Admin

**Recommendation**: **Option A** (Role Field) for Alpha

**Reasoning**:
- Simple (`role TEXT` with 3 values)
- Sufficient for Alpha (only need 3 roles)
- Easy to extend later (add permission table if needed)
- Clear hierarchy (superuser > admin > user)
- PM's superuser = explicit activation (audit trail)

### Question 4: Legacy xian Migration

**Recommendation**: **Option C** (Hybrid Approach)

**Reasoning**:
- Retroactive user_id assignment (clean schema)
- Track migration in metadata (audit trail preserved)
- Fully accessible (not read-only)
- Exclusive to xian (no multiple claims)
- Simple to implement

---

## Summary of Recommendations

If Chief Architect agrees with Lead Developer recommendations:

**Schema Design**:
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  email TEXT,
  role TEXT DEFAULT 'user',  -- 'superuser' | 'admin' | 'user'
  user_type TEXT DEFAULT 'production',  -- 'alpha' | 'production'
  alpha_start_date TIMESTAMP NULL,
  alpha_end_date TIMESTAMP NULL,
  migration_status TEXT NULL,  -- NULL for production, status for alpha
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Migration Tool**:
- Lift and shift all data (knowledge graph included)
- Preview before commit
- Preserve timestamps
- Track migration in metadata

**Superuser Implementation**:
- Role field with 3 values
- Explicit activation (audit all superuser actions)
- Clear separation from admin

**Legacy xian Migration**:
- Create xian superuser (role='superuser')
- Retroactively assign user_id to all orphaned data
- Track migration date in metadata
- Full access (not read-only)

**Implementation Time**: ~1 hour total (if recommendations accepted)

---

## Next Steps

### If Architectural Decisions Made Tonight/Tomorrow AM

**Wednesday (Oct 23)**:
- Morning: Execute Groups 1, 2, 4, 5 (9 issues, ~4h actual)
- Afternoon: Execute Group 3 (CORE-USER, 3 issues, ~1h actual)
- **Result**: Sprint A7 complete in 1 day!

### If Architectural Decisions Need Discussion

**Wednesday (Oct 23)**:
- Morning: Huddle with Chief Architect (1-2h)
- Afternoon: Execute Groups 1, 2, 4, 5 (9 issues, ~4h actual)

**Thursday (Oct 24)**:
- Morning: Execute Group 3 (CORE-USER, 3 issues, ~1h actual)
- Afternoon: Integration testing
- **Result**: Sprint A7 complete in 2 days

---

## Appendix: Relevant Sprint A6 Infrastructure

### What Sprint A6 Delivered (Relevant to CORE-USER)

**User Model** (#227):
```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    api_keys = relationship("UserAPIKey", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
```

**UserAPIKeyService** (#228):
- Store/retrieve API keys per user
- OS keychain integration
- Zero-downtime rotation

**AsyncSessionFactory** (#229):
- Database session management
- Connection pooling

**AuditLog Model** (#249):
- Complete audit trail
- User-associated events

**Infrastructure Ready**:
- Alembic migrations system
- PostgreSQL with SSL/TLS
- Multi-user isolation working

---

## Request for Architectural Guidance

**Chief Architect**: Please review the four decision points and provide guidance on:

1. **User Architecture**: Separate table or single table with flags?
2. **Migration Scope**: All-or-nothing, selective, or lift-and-shift?
3. **Role Implementation**: Role field, permission flags, or permission table?
4. **Legacy Migration**: Retroactive association, legacy container, or hybrid?

**If you agree with Lead Developer recommendations**: We can proceed with implementation immediately.

**If you have different recommendations**: Please provide architectural reasoning and we'll adjust gameplan.

**Timeline Impact**: Decisions needed by Wednesday morning for 1-day sprint completion.

---

**Briefing Complete**: Tuesday, October 22, 2025, 5:15 PM

**Prepared by**: Lead Developer (Sonnet)
**For**: Chief Architect (Cursor/Opus)
**Purpose**: Unblock Sprint A7 CORE-USER implementation
**Urgency**: Medium (9 of 12 issues not blocked, 3 await architectural decisions)
