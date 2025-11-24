# Claude Code Prompt: SEC-RBAC Phase 2 - Role-Based Permissions

## Your Identity

You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Mission: SEC-RBAC Phase 2 - Role-Based Permissions

**GitHub Issue**: #357 - SEC-RBAC: Implement RBAC
**Current Phase**: Phase 2 - Role-Based Permissions System
**Status**: Ready to implement (Phase 1 complete)
**Goal**: Implement roles, permissions, and permission checking for granular access control

---

## Context: What's Already Done (Phase 1)

### Phase 1.1: Database Schema ✅
- owner_id columns on 9 resource tables
- shared_with JSONB columns (Lists, TodoLists)
- GIN indexes for efficient queries
- 100% migration chain complete

### Phase 1.2: Service Layer ✅
- 52+ methods with ownership validation
- Optional owner_id parameter pattern
- Defense-in-depth validation

### Phase 1.3: Endpoint Protection ✅
- 26 endpoints with ownership enforcement
- JWT authentication + ownership validation
- 404 response strategy (no info leakage)

### Phase 1.4: Shared Resource Access ✅
- Read-only sharing for Lists and TodoLists
- share/unshare endpoints (owner only)
- Atomic JSONB operations
- shared-with-me endpoint

**Current State**: Users are isolated with read-only sharing. Now we add granular permissions.

---

## Your Mission: Role-Based Permission System

**Goal**: Enhance shared access with permission levels (viewer/editor/admin)

**What Phase 2 Adds**:
- Roles table (viewer, editor, admin)
- Permissions table (read, write, delete per resource type)
- Role-permission mappings
- Permission checking decorators
- Share-with-role endpoints

**What Phase 2 Does NOT Add** (future phases):
- Workspace/organization isolation → Phase 3
- Audit logging expansion → Phase 4
- Fine-grained permissions (field-level) → Future

---

## Phase 1: Database Schema Design (30 min) ⭐⭐⭐

**CRITICAL**: Before implementing, design the schema and get PM approval.

### Task 1.1: Design Roles Table

**Purpose**: Define available permission levels for shared resources

**Proposed Schema**:
```sql
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,  -- 'viewer', 'editor', 'admin'
    description TEXT,
    is_system BOOLEAN DEFAULT false,    -- System roles can't be deleted
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Initial Roles**:
- **viewer**: Read-only access (current Phase 1.4 behavior)
- **editor**: Read + write access (can modify shared resources)
- **admin**: Read + write + share access (can re-share resources)

**Questions for PM**:
- Should we support custom user-defined roles? (Recommend: NO for Phase 2, YES for future)
- Should roles be resource-type specific? (e.g., "list-editor" vs just "editor")

### Task 1.2: Design Permissions Table

**Purpose**: Define specific actions allowed per role

**Proposed Schema**:
```sql
CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    resource_type VARCHAR(50) NOT NULL,  -- 'list', 'todo', 'file', etc.
    action VARCHAR(50) NOT NULL,          -- 'read', 'write', 'delete', 'share'
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(role_id, resource_type, action)
);
```

**Permission Matrix** (proposed):

| Role | Resource | Read | Write | Delete | Share |
|------|----------|------|-------|--------|-------|
| viewer | list/todo | ✅ | ❌ | ❌ | ❌ |
| editor | list/todo | ✅ | ✅ | ❌ | ❌ |
| admin | list/todo | ✅ | ✅ | ✅ | ✅ |

**Questions for PM**:
- Should editor role allow delete? (Recommend: NO - admin only)
- Should we track permission grants per-resource or per-role? (Recommend: per-role for Phase 2)

### Task 1.3: Update shared_with Schema

**Current** (Phase 1.4):
```jsonb
shared_with: ["user-uuid-1", "user-uuid-2"]  # Array of user IDs
```

**Proposed** (Phase 2):
```jsonb
shared_with: [
  {"user_id": "uuid-1", "role": "viewer"},
  {"user_id": "uuid-2", "role": "editor"},
  {"user_id": "uuid-3", "role": "admin"}
]
```

**Alternative** (simpler - recommended):
```jsonb
shared_with: {
  "viewer": ["uuid-1", "uuid-2"],
  "editor": ["uuid-3"],
  "admin": ["uuid-4"]
}
```

**Questions for PM**:
- Which JSONB structure? (Array of objects vs grouped by role)
- Should we migrate existing shared_with data? (Array → new structure)

---

## Phase 2: Create STOP Report (10 min) ⚡

**MANDATORY STOP CONDITION**: Report schema design before implementation.

**Create file**: `dev/2025/11/22/sec-rbac-phase2-schema-design.md`

**Template**:

```markdown
# SEC-RBAC Phase 2: Schema Design Report

**Date**: November 22, 2025
**Agent**: Claude Code

## Proposed Database Schema

### Roles Table
[Schema from Task 1.1]

**Initial Seed Data**:
- viewer (is_system=true)
- editor (is_system=true)
- admin (is_system=true)

### Permissions Table
[Schema from Task 1.2]

**Permission Matrix**:
[Table from Task 1.2]

### shared_with JSONB Structure

**Current** (Phase 1.4):
```jsonb
shared_with: ["uuid-1", "uuid-2"]
```

**Proposed** (Phase 2):
[Structure from Task 1.3]

## Migration Strategy

**Option A: New Tables + Migrate shared_with**
1. Create roles table
2. Create permissions table
3. Seed initial roles/permissions
4. Migrate shared_with JSONB (array → role-grouped structure)

**Option B: New Tables Only (No Migration)**
1. Create roles/permissions tables
2. Keep existing shared_with as "viewer" role
3. New shares use role-based structure

**Recommended**: Option A (clean migration now avoids tech debt)

## Questions for PM

1. **JSONB Structure**: Array of objects vs grouped by role?
2. **Migration**: Migrate existing shares or treat as viewer-only?
3. **Custom Roles**: Support in Phase 2 or defer to future?
4. **Delete Permission**: Should editors be able to delete?

## Implementation Options

### Option A: Full Role System
- Roles + Permissions tables
- Role-based JSONB structure
- Migration of existing data
- Permission checking decorators

### Option B: Simplified Roles
- Roles table only (no permissions table)
- Hardcoded permission checks per role
- Simpler but less flexible

**Recommended**: Option A (proper foundation for future expansion)

## Ready to Implement?

- [ ] Schema design reviewed
- [ ] JSONB structure chosen
- [ ] Migration strategy approved
- [ ] Permission matrix confirmed

**STOP HERE - Report to PM before proceeding**
```

**Action**: Create this file, then **STOP and wait for PM approval** before implementing.

---

## Phase 3: Implementation (ONLY AFTER APPROVAL)

**DO NOT START THIS PHASE without PM approval of schema design.**

### Task 3.1: Create Alembic Migration

**File**: `alembic/versions/[timestamp]_add_rbac_roles_permissions.py`

```python
"""Add RBAC roles and permissions tables

Revision ID: [auto-generated]
Revises: [previous migration]
Create Date: 2025-11-22
"""

def upgrade():
    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', postgresql.UUID(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_system', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', postgresql.UUID(), nullable=False),
        sa.Column('role_id', postgresql.UUID(), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=False),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('role_id', 'resource_type', 'action')
    )

    # Seed initial roles
    roles_table = sa.table('roles',
        sa.column('id', postgresql.UUID()),
        sa.column('name', sa.String()),
        sa.column('description', sa.Text()),
        sa.column('is_system', sa.Boolean())
    )

    viewer_id = uuid.uuid4()
    editor_id = uuid.uuid4()
    admin_id = uuid.uuid4()

    op.bulk_insert(roles_table, [
        {'id': viewer_id, 'name': 'viewer', 'description': 'Read-only access', 'is_system': True},
        {'id': editor_id, 'name': 'editor', 'description': 'Read and write access', 'is_system': True},
        {'id': admin_id, 'name': 'admin', 'description': 'Full access including sharing', 'is_system': True}
    ])

    # Seed permissions
    permissions_table = sa.table('permissions',
        sa.column('id', postgresql.UUID()),
        sa.column('role_id', postgresql.UUID()),
        sa.column('resource_type', sa.String()),
        sa.column('action', sa.String())
    )

    permissions_data = []
    for resource_type in ['list', 'todo']:
        # Viewer: read only
        permissions_data.append({
            'id': uuid.uuid4(),
            'role_id': viewer_id,
            'resource_type': resource_type,
            'action': 'read'
        })

        # Editor: read + write
        for action in ['read', 'write']:
            permissions_data.append({
                'id': uuid.uuid4(),
                'role_id': editor_id,
                'resource_type': resource_type,
                'action': action
            })

        # Admin: read + write + delete + share
        for action in ['read', 'write', 'delete', 'share']:
            permissions_data.append({
                'id': uuid.uuid4(),
                'role_id': admin_id,
                'resource_type': resource_type,
                'action': action
            })

    op.bulk_insert(permissions_table, permissions_data)

def downgrade():
    op.drop_table('permissions')
    op.drop_table('roles')
```

### Task 3.2: Create Database Models

**File**: `services/database/models.py` (add to existing file)

```python
class RoleDB(Base):
    """Role definition for RBAC"""
    __tablename__ = "roles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_system = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    permissions = relationship("PermissionDB", back_populates="role", cascade="all, delete-orphan")


class PermissionDB(Base):
    """Permission for a role on a resource type"""
    __tablename__ = "permissions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    role_id = Column(String, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    resource_type = Column(String(50), nullable=False)  # 'list', 'todo', etc.
    action = Column(String(50), nullable=False)  # 'read', 'write', 'delete', 'share'
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    role = relationship("RoleDB", back_populates="permissions")

    __table_args__ = (
        UniqueConstraint('role_id', 'resource_type', 'action'),
    )
```

### Task 3.3: Create Domain Models

**File**: `services/domain/models.py` (add to existing)

```python
@dataclass
class Role:
    """Role domain model"""
    id: str
    name: str  # 'viewer', 'editor', 'admin'
    description: Optional[str] = None
    is_system: bool = False
    created_at: Optional[datetime] = None


@dataclass
class Permission:
    """Permission domain model"""
    id: str
    role_id: str
    resource_type: str  # 'list', 'todo'
    action: str  # 'read', 'write', 'delete', 'share'
    created_at: Optional[datetime] = None
```

### Task 3.4: Create Permission Service

**File**: `services/rbac/permission_service.py` (new file)

```python
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from services.database.models import RoleDB, PermissionDB
from services.domain.models import Role, Permission


class PermissionService:
    """Service for checking permissions"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_role_by_name(self, role_name: str) -> Optional[Role]:
        """Get role by name"""
        stmt = select(RoleDB).where(RoleDB.name == role_name)
        result = await self.session.execute(stmt)
        role_db = result.scalar_one_or_none()

        if not role_db:
            return None

        return Role(
            id=role_db.id,
            name=role_db.name,
            description=role_db.description,
            is_system=role_db.is_system,
            created_at=role_db.created_at
        )

    async def has_permission(
        self,
        role_name: str,
        resource_type: str,
        action: str
    ) -> bool:
        """Check if role has permission for action on resource type"""
        stmt = select(PermissionDB).join(RoleDB).where(
            and_(
                RoleDB.name == role_name,
                PermissionDB.resource_type == resource_type,
                PermissionDB.action == action
            )
        )

        result = await self.session.execute(stmt)
        permission = result.scalar_one_or_none()

        return permission is not None

    async def get_role_permissions(
        self,
        role_name: str,
        resource_type: Optional[str] = None
    ) -> List[Permission]:
        """Get all permissions for a role, optionally filtered by resource type"""
        stmt = select(PermissionDB).join(RoleDB).where(RoleDB.name == role_name)

        if resource_type:
            stmt = stmt.where(PermissionDB.resource_type == resource_type)

        result = await self.session.execute(stmt)
        permissions_db = result.scalars().all()

        return [
            Permission(
                id=p.id,
                role_id=p.role_id,
                resource_type=p.resource_type,
                action=p.action,
                created_at=p.created_at
            )
            for p in permissions_db
        ]
```

### Task 3.5: Update shared_with JSONB Structure

**Update**: `services/repositories/universal_list_repository.py`

**Change share_list method** to accept role parameter:

```python
async def share_list(
    self,
    list_id: UUID,
    owner_id: UUID,
    user_to_share_with: UUID,
    role: str = "viewer"  # NEW: Default to viewer
) -> Optional[UniversalList]:
    """Share list with user at specified permission level"""

    # Validate role exists
    permission_service = PermissionService(self.session)
    role_obj = await permission_service.get_role_by_name(role)
    if not role_obj:
        raise ValueError(f"Invalid role: {role}")

    # 1. Verify caller is owner
    list_obj = await self.get_list(list_id, owner_id=owner_id)
    if not list_obj:
        return None

    # 2. Update shared_with JSONB with role-based structure
    # Using grouped-by-role structure (per PM approval)
    stmt = update(ListDB).where(
        ListDB.id == list_id
    ).values(
        shared_with=func.jsonb_set(
            coalesce(ListDB.shared_with, cast('{}', JSONB)),
            [role],  # Path: role name as key
            func.jsonb_build_array(user_to_share_with) +
            coalesce(
                func.jsonb_extract_path(ListDB.shared_with, role),
                cast('[]', JSONB)
            ),
            True
        )
    )

    await self.session.execute(stmt)
    await self.session.commit()

    return await self.get_list(list_id, owner_id=owner_id)
```

### Task 3.6: Add Permission Checking to Repository Methods

**Update**: `services/repositories/universal_list_repository.py`

**Add permission check for updates**:

```python
async def update_list(
    self,
    list_id: UUID,
    user_id: UUID,
    updates: dict
) -> Optional[UniversalList]:
    """Update list - requires owner OR editor/admin role"""

    # Get list with shared access
    list_obj = await self.get_list(list_id, user_id=user_id)
    if not list_obj:
        return None

    # Check if user is owner
    if list_obj.owner_id == str(user_id):
        # Owner can always update
        pass
    else:
        # Shared user - check permission
        user_role = await self._get_user_role_for_list(list_id, user_id)
        if user_role not in ['editor', 'admin']:
            # Viewer cannot update
            return None

    # Proceed with update
    stmt = update(ListDB).where(ListDB.id == list_id).values(**updates)
    await self.session.execute(stmt)
    await self.session.commit()

    return await self.get_list(list_id, user_id=user_id)


async def _get_user_role_for_list(
    self,
    list_id: UUID,
    user_id: UUID
) -> Optional[str]:
    """Get role of user for this list (if shared)"""
    stmt = select(ListDB.shared_with).where(ListDB.id == list_id)
    result = await self.session.execute(stmt)
    shared_with = result.scalar_one_or_none()

    if not shared_with:
        return None

    # Check each role's user list
    for role in ['admin', 'editor', 'viewer']:
        if role in shared_with and str(user_id) in shared_with[role]:
            return role

    return None
```

---

## Phase 4: Testing (After Implementation)

### Task 4.1: Manual Permission Testing

**Create test script**: `tests/manual/manual_rbac_permissions_test.py`

```python
"""Manual test for SEC-RBAC Phase 2 permission levels"""
import httpx
import asyncio

async def test_permission_levels():
    """Test viewer/editor/admin permission levels"""

    async with httpx.AsyncClient() as client:
        # Owner creates list
        response = await client.post(
            "http://localhost:8001/api/auth/login",
            json={"username": "owner", "password": "test"}
        )
        owner_token = response.json()["access_token"]

        # Create list
        response = await client.post(
            "http://localhost:8001/api/v1/lists",
            headers={"Authorization": f"Bearer {owner_token}"},
            json={"name": "Shared Todo List", "description": "Groceries"}
        )
        list_id = response.json()["id"]

        # User 1: Viewer role
        response = await client.post(
            f"http://localhost:8001/api/v1/lists/{list_id}/share",
            headers={"Authorization": f"Bearer {owner_token}"},
            json={"user_id": "viewer-user-id", "role": "viewer"}
        )
        assert response.status_code == 200
        print("✅ Shared with viewer")

        # Viewer can read
        # Viewer CANNOT modify
        # Verify...

        # User 2: Editor role
        # Editor can read AND modify
        # Editor CANNOT delete
        # Verify...

        # User 3: Admin role
        # Admin can read, modify, AND re-share
        # Verify...

if __name__ == "__main__":
    asyncio.run(test_permission_levels())
```

---

## Phase 5: Documentation (After Testing)

**Create file**: `dev/2025/11/22/sec-rbac-phase2-completion-report.md`

[Standard completion report format with Phase 2 specifics]

---

## Success Criteria

**Phase 2 is complete when**:

- [ ] Schema design approved by PM
- [ ] Migration creates roles and permissions tables
- [ ] Initial roles seeded (viewer, editor, admin)
- [ ] Permissions seeded (read/write/delete/share matrix)
- [ ] shared_with JSONB migrated to role-based structure
- [ ] PermissionService implements permission checking
- [ ] share_list() accepts role parameter
- [ ] update_list() checks permissions for shared users
- [ ] Manual permission test passes (viewer/editor/admin behaviors)
- [ ] Completion report created with evidence

---

## Timeline Estimate

- Phase 1 (Schema Design): 30 minutes
- Phase 2 (STOP report): 10 minutes
- **WAIT FOR APPROVAL**
- Phase 3 (Implementation): 2-3 hours
- Phase 4 (Testing): 30 minutes
- Phase 5 (Documentation): 20 minutes

**Total**: ~4 hours (including approval wait)

---

**Remember**: Schema design and STOP report first. The JSONB structure and migration strategy require PM approval before implementing.

Good luck! 🚀

---

_Prompt created by: Lead Developer (Cursor)_
_Date: November 22, 2025, 10:15 AM_
_Session: SEC-RBAC Phase 2 - Role-Based Permissions_
_Prerequisites: Phases 1.1, 1.2, 1.3, 1.4 complete_
