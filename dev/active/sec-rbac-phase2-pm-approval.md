# SEC-RBAC Phase 2: PM Approval for Code Agent

**Date**: November 22, 2025, 10:45 AM
**From**: PM (via Lead Developer)
**To**: Code Agent
**Re**: Phase 2 Role-Based Permissions - Architectural Decisions

---

## Discovery Report Review: ✅ APPROVED

Excellent discovery work! Your 5 questions are exactly the right architectural decisions to clarify before implementation. Here are my answers:

---

## Question 1: JSONB Structure for Role Metadata

**Answer**: Option A - Upgrade to role metadata objects

**Approved Structure**:
```jsonb
shared_with: [
  {"user_id": "550e8400-e29b-41d4-a716-446655440000", "role": "viewer"},
  {"user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7", "role": "editor"},
  {"user_id": "9b2f5c44-3d1e-4f7a-b8c9-1e6d8a9f2b5c", "role": "admin"}
]
```

**Rationale**:
- ✅ Keeps permission data co-located with resource
- ✅ GIN index already optimized for JSONB containment queries
- ✅ No additional table joins needed
- ✅ Atomic updates with `jsonb_set`
- ❌ No need for separate roles table (adds complexity)
- ❌ No backward compatibility needed (alpha phase)

**Migration Strategy**: Simple upgrade migration (see Question 4)

---

## Question 2: Role Permission Matrix

**Answer**: Your proposed matrix is CORRECT - proceed with it

**Approved Permissions**:

### Viewer (Read-Only)
- ✅ Read list/todo details
- ✅ See list/todo in "shared-with-me" endpoint
- ❌ Modify content
- ❌ Delete
- ❌ Share with others
- ❌ Change roles

### Editor (Can Modify Content)
- ✅ Read list/todo details
- ✅ Modify content (name, description, items, status)
- ✅ Add/remove items from lists
- ✅ Mark todos complete/incomplete
- ❌ Delete list/todo (owner only)
- ❌ Share with others (owner only)
- ❌ Change roles (owner only)

### Admin (Can Share)
- ✅ Read list/todo details
- ✅ Modify content
- ✅ Share with others (add users to shared_with)
- ✅ Unshare (remove users from shared_with)
- ✅ Change other users' roles (viewer ↔ editor ↔ admin)
- ❌ Delete list/todo (owner only)
- ❌ Cannot remove owner or transfer ownership

**Owner Always Has**:
- All permissions above PLUS:
- ✅ Delete resource
- ✅ Transfer ownership (future Phase 3)
- ✅ Cannot be removed from shared_with (not applicable)

---

## Question 3: Default Role for Shared Access

**Answer**: Option B - Configurable per share action

**Approved API**:
```python
POST /api/v1/lists/{list_id}/share
Body: {
  "user_id": "uuid",
  "role": "viewer"  # Required parameter (viewer, editor, admin)
}
```

**Rationale**:
- ✅ Owner explicitly chooses permission level when sharing
- ✅ No ambiguity about what shared user can do
- ✅ More flexible than always-viewer default
- ❌ No two-step acceptance process (adds UX complexity)

**Default if Omitted**: If `role` parameter omitted from request → 400 Bad Request (explicit better than implicit)

---

## Question 4: Migration Strategy

**Answer**: Option A - Default all existing entries to "viewer"

**Approved Migration**:
```python
# Migration: 20251122_upgrade_shared_with_to_roles.py

def upgrade():
    # Convert all existing shared_with entries to viewer role
    op.execute("""
        UPDATE lists
        SET shared_with = (
            SELECT jsonb_agg(jsonb_build_object('user_id', elem, 'role', 'viewer'))
            FROM jsonb_array_elements_text(shared_with) AS elem
        )
        WHERE shared_with IS NOT NULL
        AND jsonb_typeof(shared_with) = 'array'
        AND jsonb_array_length(shared_with) > 0
        AND jsonb_typeof(shared_with->0) = 'string';  -- Only if old format
    """)

    # Same for todos
    op.execute("""
        UPDATE todos
        SET shared_with = (
            SELECT jsonb_agg(jsonb_build_object('user_id', elem, 'role', 'viewer'))
            FROM jsonb_array_elements_text(shared_with) AS elem
        )
        WHERE shared_with IS NOT NULL
        AND jsonb_typeof(shared_with) = 'array'
        AND jsonb_array_length(shared_with) > 0
        AND jsonb_typeof(shared_with->0) = 'string';
    """)
```

**Rationale**:
- ✅ Safe default: Read-only access preserved
- ✅ Owner can upgrade roles after migration if needed
- ✅ Idempotent: Only converts old format, leaves new format alone
- ✅ No data loss
- ❌ No backward compatibility needed (unreleased alpha)

**Downgrade**:
```python
def downgrade():
    # Simplify back to array of user IDs (loses role info)
    op.execute("""
        UPDATE lists
        SET shared_with = (
            SELECT jsonb_agg(elem->>'user_id')
            FROM jsonb_array_elements(shared_with) AS elem
        )
        WHERE shared_with IS NOT NULL;
    """)
```

---

## Question 5: Scope - Which Resources Get Roles?

**Answer**: Lists and Todos ONLY for Phase 2

**Approved Scope**:
- ✅ Lists (Universal Lists) - YES
- ✅ Todos - YES
- ❌ Projects - NO (Phase 3 or later)
- ❌ Files - NO (Phase 3 or later)
- ❌ Other resources - NO

**Rationale**:
- Lists and Todos are the core collaboration primitives
- Projects and Files can be added in future phases once we validate role-based permissions work
- Keep Phase 2 focused and testable

**Future Expansion** (Phase 3):
- Projects inherit roles from workspace/team
- Files inherit roles from parent list/project
- More complex hierarchy requires careful design

---

## Implementation Guidance

### JSONB Query Patterns

**Check if user has any access**:
```python
# User can access if: owner OR in shared_with array
ListDB.owner_id == user_id OR
ListDB.shared_with.op('@>')(
    func.jsonb_build_array(
        func.jsonb_build_object('user_id', user_id)
    )
)
```

**Check if user has specific role**:
```python
# User has editor or admin role
SELECT * FROM lists
WHERE owner_id = :user_id
OR EXISTS (
    SELECT 1
    FROM jsonb_array_elements(shared_with) AS share
    WHERE share->>'user_id' = :user_id
    AND share->>'role' IN ('editor', 'admin')
)
```

**Get user's role for resource**:
```python
def get_user_role(list_id: UUID, user_id: str) -> Optional[str]:
    """Returns: 'owner', 'admin', 'editor', 'viewer', or None"""
    if list.owner_id == user_id:
        return 'owner'

    for share in list.shared_with:
        if share['user_id'] == user_id:
            return share['role']

    return None
```

---

## Domain Model Updates

### Share Permission Model

```python
from enum import Enum
from dataclasses import dataclass

class ShareRole(str, Enum):
    """Role for shared resource access"""
    VIEWER = "viewer"    # Read-only
    EDITOR = "editor"    # Can modify content
    ADMIN = "admin"      # Can share with others

@dataclass
class SharePermission:
    """Permission entry for a shared resource"""
    user_id: str
    role: ShareRole

    def to_dict(self):
        return {"user_id": self.user_id, "role": self.role.value}
```

### Updated List Model

```python
@dataclass
class List:
    # Existing fields...
    owner_id: str
    shared_with: List[SharePermission] = field(default_factory=list)

    def get_user_role(self, user_id: str) -> Optional[ShareRole]:
        """Get user's role for this list"""
        if self.owner_id == user_id:
            return None  # Owner has all permissions

        for perm in self.shared_with:
            if perm.user_id == user_id:
                return perm.role

        return None

    def user_can_read(self, user_id: str) -> bool:
        """Any role can read"""
        return self.owner_id == user_id or self.get_user_role(user_id) is not None

    def user_can_write(self, user_id: str) -> bool:
        """Editor or Admin can write"""
        if self.owner_id == user_id:
            return True
        role = self.get_user_role(user_id)
        return role in (ShareRole.EDITOR, ShareRole.ADMIN)

    def user_can_share(self, user_id: str) -> bool:
        """Only Admin (and Owner) can share"""
        if self.owner_id == user_id:
            return True
        role = self.get_user_role(user_id)
        return role == ShareRole.ADMIN
```

---

## API Endpoints to Add/Modify

### Modified Endpoints (Phase 1.4 → Phase 2)

```python
# 1. Share endpoint now requires role
POST /api/v1/lists/{list_id}/share
Body: {
    "user_id": "uuid",
    "role": "viewer"  # Required: viewer, editor, admin
}
Auth: Must be owner OR admin
Returns: Updated list with new shared_with entry

# 2. Unshare endpoint (unchanged)
DELETE /api/v1/lists/{list_id}/share/{user_id}
Auth: Must be owner OR admin
Returns: Success status

# 3. Shared-with-me endpoint (unchanged behavior)
GET /api/v1/lists/shared-with-me
Auth: Any authenticated user
Returns: Lists shared with current user (any role)
```

### New Endpoints (Phase 2 only)

```python
# 4. Get all shares for a list
GET /api/v1/lists/{list_id}/shares
Auth: Must be owner OR admin
Returns: [
    {"user_id": "uuid1", "role": "viewer"},
    {"user_id": "uuid2", "role": "editor"}
]

# 5. Update user's role
PUT /api/v1/lists/{list_id}/share/{user_id}
Body: {"role": "editor"}  # New role
Auth: Must be owner OR admin
Returns: Success status

# 6. Get my role for a list
GET /api/v1/lists/{list_id}/my-role
Auth: Any authenticated user
Returns: {"role": "viewer"}  # or "editor", "admin", "owner"
         404 if no access
```

**Same 6 endpoints for todos** (`/api/v1/todos/{todo_id}/...`)

---

## Repository Method Updates

### UniversalListRepository

```python
async def share_list(
    self,
    list_id: UUID,
    owner_id: str,
    user_to_share_with: str,
    role: ShareRole
) -> Optional[UniversalList]:
    """Share list with user at specified role (owner or admin only)"""
    # Verify caller is owner or admin
    # Add {user_id, role} to shared_with JSONB array
    # Return updated list

async def update_share_role(
    self,
    list_id: UUID,
    requesting_user_id: str,
    target_user_id: str,
    new_role: ShareRole
) -> bool:
    """Update a user's role (owner or admin only)"""
    # Verify caller is owner or admin
    # Update role in shared_with array
    # Return success status

async def get_user_role(
    self,
    list_id: UUID,
    user_id: str
) -> Optional[str]:
    """Get user's role for list: 'owner', 'admin', 'editor', 'viewer', or None"""
    # Check owner_id first
    # Search shared_with array
    # Return role string or None
```

---

## Access Control Matrix

| Operation | Owner | Admin | Editor | Viewer | None |
|-----------|-------|-------|--------|--------|------|
| Read list | ✅ | ✅ | ✅ | ✅ | ❌ |
| Update list | ✅ | ✅ | ✅ | ❌ | ❌ |
| Delete list | ✅ | ❌ | ❌ | ❌ | ❌ |
| Share with user | ✅ | ✅ | ❌ | ❌ | ❌ |
| Unshare user | ✅ | ✅ | ❌ | ❌ | ❌ |
| Change role | ✅ | ✅ | ❌ | ❌ | ❌ |
| View shares | ✅ | ✅ | ❌ | ❌ | ❌ |

---

## Testing Requirements

### Manual Testing Must Verify

1. **Viewer Role**:
   - ✅ Can read shared list
   - ❌ Cannot modify shared list (403)
   - ❌ Cannot delete shared list (404)
   - ❌ Cannot share with others (403)

2. **Editor Role**:
   - ✅ Can read shared list
   - ✅ Can modify shared list (name, description)
   - ❌ Cannot delete shared list (404)
   - ❌ Cannot share with others (403)

3. **Admin Role**:
   - ✅ Can read shared list
   - ✅ Can modify shared list
   - ✅ Can share with new users
   - ✅ Can change other users' roles (viewer ↔ editor ↔ admin)
   - ❌ Cannot delete shared list (404)
   - ❌ Cannot remove owner

4. **Owner**:
   - ✅ All of the above PLUS delete

5. **Role Transitions**:
   - ✅ Upgrade viewer → editor → works
   - ✅ Downgrade editor → viewer → works
   - ✅ Revoke access entirely → 404

### Integration Tests Must Cover

- `share_list()` with each role type
- `update_share_role()` transitions
- `get_user_role()` accuracy
- Access control enforcement per role
- Migration converts old format correctly
- JSONB query patterns work at scale

---

## Security Considerations

**Role Escalation Prevention**:
- Only owner can grant admin role
- Admin cannot upgrade themselves to owner
- Admin cannot remove owner from shared_with
- Role changes are logged (future: audit trail)

**Information Leakage Prevention**:
- Return 404 (not 403) for resources user can't access
- Don't reveal resource exists if no permission
- GET /shares endpoint requires admin or owner

**Validation**:
- Verify role enum values (viewer, editor, admin only)
- Prevent self-sharing (owner sharing with themselves)
- Atomic JSONB operations (no read-modify-write race conditions)

---

## Migration Plan

### Step 1: Create Migration File
**File**: `alembic/versions/20251122_upgrade_shared_with_to_roles.py`

### Step 2: Test on Fresh Database
```bash
python -m alembic upgrade head
# Verify shared_with structure upgraded
```

### Step 3: Test on Database with Existing Shares
```bash
# Create test data with old format
INSERT INTO lists (shared_with) VALUES ('["uuid1", "uuid2"]');

# Run migration
python -m alembic upgrade head

# Verify conversion
SELECT shared_with FROM lists;
-- Should show: [{"user_id": "uuid1", "role": "viewer"}, ...]
```

---

## Estimated Timeline

| Phase | Task | Estimate |
|-------|------|----------|
| **Schema** | Migration file creation | 20 min |
| **Schema** | Migration testing | 10 min |
| **Domain** | ShareRole enum + SharePermission model | 15 min |
| **Domain** | Update List/Todo models | 15 min |
| **Repository** | Update share_list() to accept role | 20 min |
| **Repository** | Add update_share_role() | 20 min |
| **Repository** | Add get_user_role() | 15 min |
| **Repository** | Update access control queries | 30 min |
| **API** | Modify POST /share endpoint | 15 min |
| **API** | Add PUT /share/{user_id} endpoint | 15 min |
| **API** | Add GET /shares endpoint | 15 min |
| **API** | Add GET /my-role endpoint | 10 min |
| **API** | Update access control middleware | 20 min |
| **Testing** | Manual testing (4 roles × 6 operations) | 30 min |
| **Testing** | Integration tests | 30 min |
| **Docs** | Update API documentation | 15 min |
| **Total** | | **275 min (~4.6 hours)** |

---

## Approval Summary

✅ **Approved to proceed with Phase 2 implementation**

**Scope**:
- Role-based permissions for Lists and Todos
- Three roles: Viewer (read), Editor (write), Admin (share)
- Owner always has full permissions including delete

**Approach**:
- JSONB upgrade: `[user_ids]` → `[{user_id, role}]`
- Migration defaults existing shares to "viewer"
- New share endpoint requires explicit role parameter

**Prerequisites**:
- ✅ Phase 1 complete (all 4 sub-phases)
- ✅ Database schema with shared_with JSONB columns
- ✅ GIN indexes deployed

---

## Authorization

**Approved by**: PM (xian)
**Date**: November 22, 2025, 10:45 AM
**Authority**: Product Management approval for Phase 2 implementation

**You are cleared to proceed with Phase 2 implementation.**

Follow the 5-phase approach in your prompt:
1. ✅ Schema design (this document)
2. Migration file creation
3. Domain model updates
4. Repository layer updates
5. API endpoint implementation

Good luck! 🚀

---

_Approval provided by: PM (xian)_
_Via: Lead Developer (Cursor session)_
_Time: 10:45 AM, November 22, 2025_
