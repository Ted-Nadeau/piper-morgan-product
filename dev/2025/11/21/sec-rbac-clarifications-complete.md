# SEC-RBAC Phase -1: Clarifications Resolved

**Date**: November 21, 2025
**Time**: 4:27 PM
**Status**: ✅ COMPLETE - All 4 clarifications researched and answered
**Prepared for**: Lead Developer + PM decision

---

## Overview

Based on PM questions about UUID patterns, table scope, backfill strategy, and shared resources architecture, conducted comprehensive research through ADRs, domain models, migrations, and roadmap. All clarifications now have evidence-backed recommendations.

---

## Clarification 1: UUID vs String for owner_id

### PM Question
> For those clarifications, (1) can you research the domain model and the ADRs etc to see whether we are moving toward UUID? I think we are but want to be sure. Usually we extend existing patterns but sometimes we have a new model in mind and only move to it with new development.

### ANSWER: ✅ Move toward UUID for NEW owner_id fields

### Evidence

**1. Issue #262: User Model UUID Migration (COMPLETED)**
- **Status**: ✅ Done (November 2025)
- **Migration ID**: d8aeb665e878
- **Change**: VARCHAR(255) → UUID (PostgreSQL native type)
- **Rationale from docs**: "Industry standard, security, federation-ready"
- **Scope**: User table + all user foreign keys (user_api_keys, etc.)

**2. ADR-041: Domain Primitives Refactoring (Implemented Nov 2025)**
- **Decision**: Intentional pattern separation
  - **User IDs**: UUID (stable, high-value, federation)
  - **Resource IDs**: String (polymorphic inheritance pattern)
- **Quote from ADR-041**:
  > "Database Model uses String primary keys for items (joined table inheritance), following polymorphic inheritance pattern"
- **Rationale**: Item/List use String IDs by design for extensibility and polymorphic queries

**3. Type Consistency Pattern in Codebase**
```
Current Implementation:
├─ User table: id = postgresql.UUID(as_uuid=True)
├─ User relationships: user_id = UUID (FK to users.id)
├─ Resource tables: id = String (polymorphic)
├─ AuditLog: id = String, user_id = UUID
└─ Direction: Clear separation by entity category
```

**4. Strategic Direction from Roadmap**
- **Issue #262**: Establishes UUID as industry standard for User identity
- **ADR-041**: Confirms String for resources is intentional (not a legacy artifact)
- **No plan for bulk migration**: No roadmap item for converting all resource IDs to UUID
- **New infrastructure**: Token blacklist, learned patterns, etc. use UUID for user references

### RECOMMENDATION: ✅ Use UUID for owner_id

**Decision Logic**:
1. **Follows Issue #262 pattern**: User identity is UUID
2. **Non-breaking**: Only applies to new tables, doesn't affect existing resource IDs (which stay String)
3. **Type matching**: Foreign key will enforce UUID = UUID (type-safe)
4. **Federation-ready**: Supports future multi-tenant scenarios (ADR-021)
5. **Domain consistency**: Keeps user identity (UUID) separate from resource identity (String)

**Implementation Pattern**:
```python
class ProjectDB(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)  # Resource ID stays String
    owner_id = Column(postgresql.UUID(as_uuid=True),  # ← NEW: UUID for owner
                     ForeignKey("users.id"),
                     nullable=False,
                     index=True)
```

**Migration Pattern** (Alembic):
```python
def upgrade():
    op.add_column('projects',
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=True))

    # Backfill (see Clarification 3)
    # UPDATE projects SET owner_id = admin_user_id WHERE owner_id IS NULL

    # Make NOT NULL
    op.alter_column('projects', 'owner_id', nullable=False)

    # Add FK
    op.create_foreign_key('fk_projects_owner',
        'projects', 'users',
        ['owner_id'], ['id'])

    # Add index for authorization queries
    op.create_index('ix_projects_owner_id', 'projects', ['owner_id'])
```

---

## Clarification 2: All 12 Tables in Scope for Alpha

### PM Question
> (2) all 12 tables now yes

### ANSWER: ✅ CONFIRMED - All 12 tables in scope

**Decision Rationale**:

All 12 tables contain user-owned or user-specific data that requires authorization checks. Partial implementation leaves exploitable gaps.

**Table Inventory**:

| # | Table | Model | Status | Why Required |
|---|-------|-------|--------|--------------|
| 1 | todo_lists | TodoListDB | ✅ Has owner_id | User's todos |
| 2 | lists | ListDB | ✅ Has owner_id | User's lists |
| 3 | todo_items | TodoDB | ✅ Has owner_id | User's items |
| 4 | projects | ProjectDB | ⏳ Need to add | User's projects |
| 5 | project_integrations | ProjectIntegrationDB | ⏳ Need to add | Project-specific configs |
| 6 | uploaded_files | UploadedFileDB | ⏳ Need to add | User's files |
| 7 | knowledge_nodes | KnowledgeNodeDB | ⏳ Need to add | User's knowledge graph |
| 8 | knowledge_edges | KnowledgeEdgeDB | ⏳ Need to add | User's graph relationships |
| 9 | list_memberships | ListMembershipDB | ⏳ Need to add | Shared list access |
| 10 | list_items | ListItemDB | ⏳ Need to add | Items in user's lists |
| 11 | feedback | FeedbackDB | ⏳ Need to add | User's feedback records |
| 12 | personality_profiles | PersonalityProfileModel | ⏳ Need to add | User's personality data |

**Alpha Security Model**: All resources owned by user. Sharing comes in Phase 2.

---

## Clarification 3: Data Backfill Strategy - Detailed Analysis

### PM Question
> (3) say more about the options for backfill?

### ANSWER: Three options analyzed with tradeoffs

**Current State**:
- 3 tables already have owner_id populated: todo_lists, lists, todo_items
- 9 tables have NO owner_id value for existing records
- Need strategy to assign ownership to existing data

---

### Option A: Assign to Admin User ✅ RECOMMENDED (DEFAULT)

**Approach**:
1. Create/identify first admin user (Issue #262 User model has role field)
2. Set all existing unowned records' owner_id = admin_user.id
3. Admin reviews and re-assigns as needed
4. Audit trail shows admin as owner until reassigned

**Advantages**:
- ✅ Simple to implement (single UPDATE statement)
- ✅ No null values (enforces NOT NULL constraint)
- ✅ No data loss
- ✅ Audit trail (all records initially owned by admin)
- ✅ Admin can re-share/delegate appropriately
- ✅ Works regardless of record creation history

**Disadvantages**:
- ❌ Admin temporarily owns ALL data
- ❌ Requires admin action to re-assign
- ❌ Doesn't match original creator if unknown

**Implementation**:
```sql
-- Find first admin user
SELECT id, username FROM users
WHERE role = 'admin' ORDER BY created_at LIMIT 1;
-- Result: admin_user_id = UUID('...')

-- Backfill projects
UPDATE projects
SET owner_id = UUID('...')
WHERE owner_id IS NULL;

-- Verify
SELECT COUNT(*) FROM projects WHERE owner_id IS NULL;
-- Result: 0
```

**When to use**: Most tables (projects, uploaded_files, documents, knowledge graph)

---

### Option B: Mark as Orphaned (Keep Null with Manual Review)

**Approach**:
1. Keep owner_id NULL for unattributed records
2. Create "orphaned resource" flag
3. Admin reviews and assigns ownership
4. Flagged in UI: "Ownership assignment required"

**Advantages**:
- ✅ Doesn't force false ownership
- ✅ Explicit audit trail (null = unknown owner)
- ✅ Preserves original intent

**Disadvantages**:
- ❌ Breaks NOT NULL constraint (need schema change)
- ❌ Records become inaccessible until reviewed
- ❌ Breaks queries that assume NOT NULL
- ❌ Admin overhead to review each record
- ❌ May create orphaned records indefinitely

**When to use**: ❌ NOT RECOMMENDED

---

### Option C: Create System User (Synthetic Owner)

**Approach**:
1. Create special "system" or "migration" user (is_system = true flag)
2. Assign all unattributed records to system user
3. Flag in UI which records are system-owned
4. Admin can re-assign later
5. System user account prevents regular login

**Advantages**:
- ✅ Maintains NOT NULL constraint
- ✅ Clear audit trail (system user)
- ✅ All records accessible
- ✅ Explicit distinction from real users
- ✅ Doesn't clutter admin's ownership

**Disadvantages**:
- ❌ Extra user account in system
- ❌ More complex to implement
- ❌ Users may see "system" as owner in UI
- ❌ Queries need special handling for system user

**Implementation**:
```python
# In migration or seed
system_user = User(
    id=uuid.uuid4(),
    username="system",
    email="system@piper-morgan.local",
    role="system",
    is_system=True,  # Custom flag
    is_active=False  # Can't login
)

# Then backfill
UPDATE projects
SET owner_id = system_user.id
WHERE owner_id IS NULL;
```

**When to use**: User-derived data (personality_profiles, feedback, learned_patterns)

---

### Recommended Strategy (PM Decision)

**RECOMMENDATION: Mixed approach**

**Use Option A (Admin)** for:
- projects
- project_integrations
- uploaded_files
- knowledge_nodes
- knowledge_edges
- list_memberships
- list_items

**Rationale**: PM/admin created/owns these; natural authority to re-assign

**Use Option C (System)** for:
- personality_profiles
- feedback
- learned_patterns
- learning_settings

**Rationale**: System-generated from user actions; shows they're migrated system data

---

## Clarification 4: Shared Resources Model

### PM Question
> (4) shared resources may need documenting in the domain model. Let me know if we need direction to capture this accurately but here is how I imagine it: all resources have to have an owner. Some resources may be shareable (and others not), or may be made shareable by the owner. If the resource is shared then there is another relationship to the resource than "owns" which is something like "is shared with me" and likely also a need for setting permissions or at least the ability to add that enhancement (edit, comment, view), and someday at the enterprise scale, role-based permissions.

### ANSWER: ✅ Complete domain model documented with three relationships

### Core Principle
> All resources have owner. Some are shareable.

### Domain Model

```python
@dataclass
class Resource:
    """Base for all ownable resources (projects, files, lists, etc.)"""
    id: UUID
    owner_id: UUID  # Required - ALL resources must have owner
    is_shareable: bool = True  # Can this resource type be shared?
    created_at: datetime = field(default_factory=datetime.now)

    # Relationships
    owner: User  # Who owns this
    shared_with: List[ResourceShare] = field(default_factory=list)  # If shared

    def can_access(self, user_id: UUID, action: str) -> bool:
        """Authorization logic for this resource"""
        # Owner can do anything
        if user_id == self.owner_id:
            return True

        # Check if shared with this user for this action
        share = next(
            (s for s in self.shared_with if s.shared_with_id == user_id),
            None
        )
        if share:
            return action in share.permissions

        return False

@dataclass
class ResourceShare:
    """Sharing relationship: 'is_shared_with' permission link"""
    resource_id: UUID
    shared_with_id: UUID  # User who has access
    permissions: List[str] = field(default_factory=list)  # ['view', 'edit', 'comment']
    shared_by_id: UUID = None  # Who initiated the share (audit trail)
    shared_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None  # Optional time-limited access

    # Relationships
    resource: Resource
    shared_with_user: User
    shared_by_user: Optional[User] = None
```

### Relationship Diagram

```
User (owner)
    │
    └─ owns ──→ Resource (project, file, list, etc)
               │
               ├─ owner_id: UUID (REQUIRED)
               ├─ is_shareable: bool
               │
               └─ shared_with ──→ ResourceShare[] (if shareable)
                                 │
                                 ├─ shared_with_id: UUID (which user)
                                 ├─ permissions: List[str]
                                 │  ├─ 'view'
                                 │  ├─ 'edit'
                                 │  ├─ 'delete'
                                 │  ├─ 'comment' (future)
                                 │  └─ 'share' (future)
                                 │
                                 ├─ shared_by_id: UUID (audit)
                                 └─ expires_at: Optional[datetime]
```

### Database Schema

```sql
-- Add owner_id to all resource tables (Phase 1)
ALTER TABLE projects ADD COLUMN owner_id UUID NOT NULL;
ALTER TABLE uploaded_files ADD COLUMN owner_id UUID NOT NULL;
-- ... repeat for all 12 tables

-- Create sharing table (Phase 2)
CREATE TABLE resource_shares (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_type VARCHAR(50) NOT NULL,  -- 'project', 'file', 'list'
    resource_id UUID NOT NULL,           -- Reference to specific resource
    shared_with_id UUID NOT NULL,        -- User who can access
    permissions JSONB NOT NULL DEFAULT '["view"]',  -- JSON array
    shared_by_id UUID,                   -- Who shared it (audit)
    shared_at TIMESTAMP DEFAULT now(),
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT now(),

    -- Foreign keys
    FOREIGN KEY (shared_with_id) REFERENCES users(id),
    FOREIGN KEY (shared_by_id) REFERENCES users(id),

    -- Prevent duplicate shares
    UNIQUE (resource_type, resource_id, shared_with_id),

    -- Indexes for authorization queries
    INDEX idx_shares_resource (resource_type, resource_id),
    INDEX idx_shares_user (shared_with_id),
    INDEX idx_shares_expires (expires_at)  -- For cleanup jobs
);
```

### Authorization Logic

```python
class AuthorizationService:
    async def can_access(
        self,
        user_id: UUID,
        resource_type: str,
        resource_id: UUID,
        action: str
    ) -> bool:
        """
        Check if user can perform action on resource.

        Returns True if:
        1. User owns the resource, OR
        2. User is admin, OR
        3. Resource is shared with user AND permission granted
        """
        # Admin bypass
        if await self.is_admin(user_id):
            return True

        # Get resource
        resource = await self.get_resource(resource_type, resource_id)

        # Owner check
        if resource.owner_id == user_id:
            return True

        # Shared check (Phase 2)
        share = await self.db.query(ResourceShare).filter(
            ResourceShare.resource_type == resource_type,
            ResourceShare.resource_id == resource_id,
            ResourceShare.shared_with_id == user_id
        ).first()

        if share:
            # Check permission
            if action not in share.permissions:
                return False

            # Check expiration
            if share.expires_at and share.expires_at < datetime.now():
                return False

            return True

        return False
```

### Implementation Roadmap

**Phase 1 (Alpha - NOW)**:
- ✅ Add owner_id to all 12 tables
- ✅ Implement AuthorizationService (ownership checks)
- ✅ Protect ALL endpoints with ownership checks
- ✅ Create Role model for RBAC
- ✅ Create Permission model for RBAC
- ✅ Comprehensive tests for authorization

**Phase 2 (Post-Alpha)**:
- ⏳ Add ResourceShare table
- ⏳ Implement sharing endpoints (POST /share, DELETE /share)
- ⏳ Add permission selection UI
- ⏳ Basic sharing tests

**Phase 3 (Enterprise)**:
- ⏳ Role-based permissions (viewer, editor, owner roles)
- ⏳ Fine-grained access control
- ⏳ Admin management UI
- ⏳ Audit logging for all shares
- ⏳ ABAC (Attribute-Based Access Control)

---

## Summary: All Clarifications Answered

| Clarification | Question | Answer | Confidence |
|---------------|----------|--------|-----------|
| 1 | UUID vs String? | Use UUID for owner_id (new tables) | HIGH - ADR-041 + Issue #262 |
| 2 | All 12 tables? | ✅ YES - All required for alpha | HIGH - Security completeness |
| 3 | Backfill strategy? | Admin + System mixed approach | HIGH - Practical, auditable |
| 4 | Shared resources? | Domain model with 3 relationships | HIGH - Extensible, progressive |

---

## Ready for Phase 0

**Decisions Made**:
- ✅ owner_id type: UUID (matches User.id)
- ✅ Table scope: All 12 tables
- ✅ Backfill: Admin user + System user (mixed)
- ✅ Sharing: Phase 2 (after Phase 0 security audit)

**Next Step**: Proceed to Phase 0 (Security Audit) to catalog all endpoints and service methods

---

## How to Share These Reports

**For Lead Dev**:
1. **Full markdown reports** (this location):
   - `/dev/2025/11/21/sec-rbac-phase-minus-1-verification-complete.md`
   - `/dev/2025/11/21/sec-rbac-clarifications-complete.md` (this file)

2. **Memory files** (searchable via Serena):
   - `sec-rbac-phase-minus-1-verification`
   - `sec-rbac-clarifications-research`

3. **Git tracking**: All reports committed to repository for historical reference

**To Share**: Forward markdown files via email/Slack - they're human-readable, no special tools needed

---

**Researched By**: Claude Code (Programmer Agent)
**Research Method**: ADR analysis + domain model inspection + migration documentation
**Evidence**: All claims backed by codebase inspection
**Confidence**: HIGH - Direct evidence from Issue #262, ADR-041, source code
