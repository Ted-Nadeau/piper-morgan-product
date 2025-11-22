# SEC-RBAC Phase -1: Clarification Research (COMPLETED)

**Date**: 2025-11-21 (4:27 PM)
**Research Depth**: ADRs, domain models, migrations, roadmap
**Status**: ✅ All clarifications answered with evidence

---

## Clarification 1: UUID vs String Pattern - Architecture Direction

### ANSWER: Move toward UUID for NEW owner_id fields

**Evidence**:

**1. User Model Migration - Issue #262 (COMPLETED)**
- Status: ✅ Done (November 2025)
- Migration: d8aeb665e878
- User.id: Converted from VARCHAR(255) → UUID
- Rationale: Industry standard, security, federation-ready

**2. Intentional Pattern Separation (ADR-041)**
- Domain models (Item, List): String IDs (preserved for stability)
- User model: UUID (migrated for MVP)
- **Deliberate Choice**: Different ID types for different entity categories
  - **User IDs**: UUID (stable, high-value, federation)
  - **Resource IDs**: String (polymorphic inheritance pattern)

**3. Type Consistency Pattern**
```
Current Implementation:
├─ User table: id = UUID
├─ User relationships: user_id = UUID (FK to users)
├─ Resource tables: id = String (polymorphic)
└─ Future: owner_id = ??? (decision point)
```

**4. Strategic Direction**
- Issue #262: Establishes UUID as industry standard for identity
- No roadmap item for bulk String→UUID conversion of resources
- New infrastructure (token_blacklist, etc) uses UUID for user references
- **Clear signal**: UUID for identity/ownership, String for resources

### RECOMMENDATION: ✅ Use UUID for owner_id

**Reasoning**:
1. **Matches User.id type** - Direct FK relationship (User owns resource)
2. **Industry standard** - Consistent with Issue #262 decision
3. **Federation-ready** - Supports future multi-tenant/federation (ADR-021)
4. **Non-breaking** - New tables only, doesn't affect existing resource IDs
5. **Type safety** - FK constraint will enforce UUID type matching

**Implementation Pattern**:
```python
# Resource table (new) - uses UUID owner_id
class ProjectDB(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)  # Resource stays String
    owner_id = Column(postgresql.UUID(as_uuid=True),
                     ForeignKey("users.id"),
                     nullable=False)  # FK to User
```

---

## Clarification 2: All 12 Tables in Scope for Alpha

### ANSWER: ✅ YES - All 12 tables confirmed in scope

**Decision Confirmation**: Use all 12 tables identified in Phase -1:

**Already Have owner_id** (3):
1. todo_lists - TodoListDB
2. lists - ListDB
3. todo_items - TodoDB

**Need owner_id Added** (9):
4. projects - ProjectDB
5. project_integrations - ProjectIntegrationDB
6. uploaded_files - UploadedFileDB
7. knowledge_nodes - KnowledgeNodeDB
8. knowledge_edges - KnowledgeEdgeDB
9. list_memberships - ListMembershipDB
10. list_items - ListItemDB
11. feedback - FeedbackDB
12. personality_profiles - PersonalityProfileModel

**Why all 12 for alpha**:
- All contain user-owned or user-specific data
- All require authorization checks (user shouldn't see other user's data)
- Complete coverage needed to pass security audit
- Partial implementation leaves exploitable gaps

---

## Clarification 3: Data Backfill Strategy - Deep Dive

### ANSWER: Three options with tradeoffs

**Current State Analysis**:
- 3 tables (todo_lists, lists, todo_items) already have owner_id populated
- 9 tables have existing data with NO owner_id value
- Need strategy to assign ownership to existing records

### Option A: Assign to Admin User ✅ RECOMMENDED

**Approach**:
1. Find first admin user (or create system admin)
2. Set all existing records' owner_id = admin_user.id
3. Admin must then re-assign or share appropriately

**Advantages**:
- ✅ Simple to implement
- ✅ No data loss
- ✅ No null values (all records owned)
- ✅ Admin has audit trail of what was inherited
- ✅ Works regardless of record creation history

**Disadvantages**:
- ❌ Admin temporarily owns all data
- ❌ Requires admin to re-share/reassign
- ❌ Doesn't match original creator if unknown

**Example**:
```sql
-- Find first admin
SELECT id FROM users WHERE role = 'admin' ORDER BY created_at LIMIT 1;
-- Result: admin_user_id = UUID(...)

-- Backfill projects
UPDATE projects
SET owner_id = UUID('...')
WHERE owner_id IS NULL;
```

**When to use**: Default choice for most tables

---

### Option B: Mark as Orphaned (Null with Manual Review)

**Approach**:
1. Keep owner_id NULL for records where creator unknown
2. Require admin review before data accessible
3. Flag in UI: "This record is orphaned, needs ownership assignment"

**Advantages**:
- ✅ Doesn't force false ownership
- ✅ Explicit audit trail
- ✅ Preserves original intent

**Disadvantages**:
- ❌ Creates NULL values (breaks NOT NULL constraint)
- ❌ Records become inaccessible until reviewed
- ❌ Additional admin work
- ❌ May break existing queries

**When to use**: Not recommended - violates constraint design

---

### Option C: Create System User (Synthetic Owner)

**Approach**:
1. Create special "system" or "migrated" user
2. Assign all unattributed records to system user
3. Flag in UI which records are system-owned
4. Admin can re-assign later

**Advantages**:
- ✅ Maintains NOT NULL constraint
- ✅ Clear audit trail (system user)
- ✅ All records accessible
- ✅ Explicit distinction from real users

**Disadvantages**:
- ❌ Extra user account needed
- ❌ More complex to implement
- ❌ May confuse users seeing "system" as owner

**When to use**: Tables where attribution is important

---

### Recommended Strategy (Mixed Approach)

**For most tables (projects, files, documents)**:
- **Use Option A** (assign to admin)
- Rationale: PM created/owns these records
- Audit trail: Admin → current owner via sharing/delegation

**For user-centric tables (personality_profiles, feedback)**:
- **Use Option C** (system user)
- Rationale: These are system-generated from user actions
- Audit trail: system user shows it's from migration

**For knowledge graph (knowledge_nodes, edges)**:
- **Use Option A** (assign to admin)
- Rationale: Part of shared knowledge base
- Audit trail: Admin maintains it

---

## Clarification 4: Shared Resources Model Architecture

### ANSWER: Domain model documented with three relationships

**Core Principle**: All resources have owner. Some are shareable.

### Domain Model (Proposed)

```python
@dataclass
class Resource:
    """Base for all ownable resources"""
    id: UUID
    owner_id: UUID  # Required - all resources have owner
    is_shareable: bool = True  # Can this type be shared?
    created_at: datetime = field(default_factory=datetime.now)

    # Relationships
    owner: User  # Who owns this
    shared_with: List[ResourceShare] = field(default_factory=list)

    def can_access(self, user_id: UUID, action: str) -> bool:
        """Check if user can perform action on this resource"""
        # Owner can do anything
        if user_id == self.owner_id:
            return True

        # Check if shared with this user
        share = next(
            (s for s in self.shared_with if s.shared_with_id == user_id),
            None
        )
        if share:
            return action in share.permissions

        return False

@dataclass
class ResourceShare:
    """Sharing relationship - 'is shared with' permission link"""
    resource_id: UUID
    shared_with_id: UUID  # User who has access
    permissions: List[str] = field(default_factory=list)  # ['view', 'edit', 'comment']
    shared_by_id: UUID = None  # Who initiated the share?
    shared_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None  # Optional expiration

    # Relationships
    resource: Resource
    shared_with_user: User
    shared_by_user: Optional[User] = None
```

### Relationships Diagram

```
User (owner)
    ↓ (owns)
Resource (project, file, list, etc)
    ├─ owned_by: User ← Required always
    └─ shared_with: List[ResourceShare] ← Optional if shareable
        └─ ResourceShare entries
            ├─ shared_with_id: UUID (which user)
            ├─ permissions: ['view', 'edit', 'comment', ...]
            └─ shared_by_id: UUID (who created the share)
```

### Database Schema

```sql
-- Core table (for all resource types)
CREATE TABLE resource_shares (
    id UUID PRIMARY KEY,
    resource_type VARCHAR(50) NOT NULL,  -- 'project', 'file', 'list', etc
    resource_id UUID NOT NULL,           -- Reference to specific resource
    shared_with_id UUID NOT NULL,        -- User who has access
    permissions JSONB NOT NULL DEFAULT '["view"]',  -- ['view', 'edit', 'comment']
    shared_by_id UUID,                   -- Who shared it (audit)
    shared_at TIMESTAMP DEFAULT now(),
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT now(),

    -- Foreign keys
    FOREIGN KEY (shared_with_id) REFERENCES users(id),
    FOREIGN KEY (shared_by_id) REFERENCES users(id),

    -- Constraints
    UNIQUE (resource_type, resource_id, shared_with_id),  -- Can't share same resource twice

    -- Indexes
    INDEX idx_shares_resource (resource_type, resource_id),
    INDEX idx_shares_shared_with (shared_with_id),
    INDEX idx_shares_expires (expires_at)  -- For cleanup jobs
);

-- Per-resource tables (existing, NEED owner_id added)
ALTER TABLE projects ADD COLUMN owner_id UUID NOT NULL;
ALTER TABLE files ADD COLUMN owner_id UUID NOT NULL;
ALTER TABLE lists ADD COLUMN owner_id UUID NOT NULL;
-- ... repeat for all 12 tables

-- Indexes for authorization checks
CREATE INDEX idx_projects_owner ON projects(owner_id);
CREATE INDEX idx_files_owner ON files(owner_id);
-- ... etc
```

### Permission Model - Progressive Enhancement

**Phase 1 (Alpha)** - Basic permissions:
```python
PERMISSIONS = {
    "view": "Can read this resource",
    "edit": "Can modify this resource",
    "delete": "Can delete this resource",
    "share": "Can share with others",
    "comment": "Can add comments (future)"
}

# Stored as JSON in resource_shares.permissions
resource_share.permissions = ["view", "edit", "comment"]
```

**Phase 2 (Post-Alpha)** - Role-based permissions:
```python
ROLE_PERMISSIONS = {
    "editor": ["view", "edit", "comment"],
    "viewer": ["view", "comment"],
    "commenter": ["view", "comment"],
    "owner": ["view", "edit", "delete", "share", "comment"]
}

# Upgrade resource_shares schema
ALTER TABLE resource_shares ADD COLUMN role_id UUID;
```

**Phase 3 (Enterprise)** - Fine-grained control:
```python
# Custom permissions per share
# Example: User A gets view-only on project B
resource_share.role_id = None  # Not role-based
resource_share.permissions = ["view"]  # Explicit permissions

# OR: User C gets editor role on project D
resource_share.role_id = UUID("editor-role-id")
resource_share.permissions = None  # Derive from role
```

### Authorization Logic

```python
class AuthorizationService:
    def can_access(
        self,
        user_id: UUID,
        resource_type: str,
        resource_id: UUID,
        action: str
    ) -> bool:
        """
        Check if user can perform action on resource

        Returns True if:
        1. User owns the resource, OR
        2. User is admin, OR
        3. Resource is shared with user AND permission granted
        """
        # Admin bypass
        if self.is_admin(user_id):
            return True

        # Get resource
        resource = self.get_resource(resource_type, resource_id)

        # Owner check
        if resource.owner_id == user_id:
            return True

        # Shared check
        share = self.db.query(ResourceShare).filter(
            ResourceShare.resource_type == resource_type,
            ResourceShare.resource_id == resource_id,
            ResourceShare.shared_with_id == user_id
        ).first()

        if share and action in share.permissions:
            # Also check expiration
            if share.expires_at and share.expires_at < datetime.now():
                return False
            return True

        return False
```

### API Examples

**Check access to file**:
```python
@app.get("/files/{file_id}")
async def get_file(file_id: UUID, user_id: UUID = Depends(get_current_user)):
    # Authorization check
    if not auth_service.can_access(user_id, "file", file_id, "view"):
        raise HTTPException(403, "Not authorized")

    return file_service.get_file(file_id)
```

**Share resource with user**:
```python
@app.post("/files/{file_id}/share")
async def share_file(
    file_id: UUID,
    share_request: ShareRequest,  # {shared_with_id, permissions}
    user_id: UUID = Depends(get_current_user)
):
    # Only owner or admin can share
    if not auth_service.can_access(user_id, "file", file_id, "share"):
        raise HTTPException(403, "Only owner can share")

    # Create share
    resource_share = ResourceShare(
        resource_type="file",
        resource_id=file_id,
        shared_with_id=share_request.shared_with_id,
        permissions=share_request.permissions,
        shared_by_id=user_id
    )
    return share_service.create_share(resource_share)
```

### Implementation Phases

**Phase 1 (Alpha - NOW)**:
- ✅ Add owner_id to all 12 tables
- ✅ Implement AuthorizationService (ownership checks)
- ✅ Protect all endpoints with ownership checks
- ⏳ ResourceShare table NOT required yet (single-user testing)

**Phase 2 (Post-Alpha)**:
- Add ResourceShare table
- Implement sharing endpoints
- Add permission checks
- Basic sharing UI

**Phase 3 (Enterprise)**:
- Role-based permissions
- Fine-grained access control
- Audit logging
- Admin management UI

---

## Summary: All Clarifications Answered

| Clarification | Answer | Confidence |
|---------------|--------|-----------|
| 1. UUID vs String | Use UUID for owner_id (new tables) | High - ADR-041 + Issue #262 evidence |
| 2. All 12 tables | ✅ Confirmed in scope for alpha | High - Complete authorization required |
| 3. Backfill strategy | Option A (admin) + Option C (system) mixed | High - Practical, audit-friendly |
| 4. Shared resources | Domain model documented with 3 relationships | High - Extensible, progressive enhancement |

---

## Recommended Next Steps

1. **Confirm owner_id type**: UUID (recommended) vs String
2. **Confirm backfill approach**: Admin user + system user (recommended)
3. **Confirm sharing scope**: Phase 1 (ownership only) vs Phase 2 (add sharing)
4. **Proceed to Phase 0**: Security Audit with complete infrastructure verified

**Ready to proceed to Phase 0 (Security Audit)** ✅

---

**Researched By**: Claude Code (Programmer Agent)
**Method**: ADR analysis + domain model inspection + roadmap review + migration documentation
**Confidence Level**: High - All claims backed by codebase evidence
