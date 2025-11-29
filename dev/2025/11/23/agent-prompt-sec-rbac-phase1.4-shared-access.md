# Claude Code Prompt: SEC-RBAC Phase 1.4 - Shared Resource Access

## Your Identity

You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Mission: SEC-RBAC Phase 1.4 - Shared Resource Access

**GitHub Issue**: #357 - SEC-RBAC: Implement RBAC
**Current Phase**: Phase 1.4 - Shared Resource Access (Collaboration)
**Status**: Ready to implement (Prerequisites complete)
**Goal**: Enable users to share resources with other users while maintaining ownership

---

## Context: What's Already Done

### Phase 1.1 (Database Schema): ✅ COMPLETE (100%)

**Migration chain**: 100% complete (Issue #367 resolved!)
- 9 resource tables have owner_id columns
- All SEC-RBAC schema deployed
- JSON/JSONB indexes properly configured
- Database fully functional

**See**: `dev/2025/11/22/issue-367-completion.md`

### Phase 1.2 (Service Layer): ✅ COMPLETE

**7 services with 52+ methods secured**:
1. FileRepository (14 methods)
2. UniversalListRepository (11 methods)
3. TodoManagementService (7 methods)
4. FeedbackService (4 methods)
5. TodoListRepository (4 methods)
6. KnowledgeGraphService (12 methods)
7. ProjectRepository (7 methods)

**Pattern**: Optional owner_id parameter with conditional filtering

**See**: `dev/2025/11/21/sec-rbac-phase1.2-completion-summary.md`

### Phase 1.3 (Endpoint Protection): ✅ COMPLETE

**26 endpoints protected**:
- Lists API: 5 endpoints
- Todos API: 5 endpoints
- Projects API: 5 endpoints
- Feedback API: 3 endpoints
- Knowledge Graph API: 4 endpoints
- Files API: 4 endpoints

**Pattern**: JWT authentication + ownership validation + 404 for non-owned

**See**: `dev/2025/11/22/sec-rbac-phase1.3-completion-report.md`

---

## Your Mission: Shared Resource Access

**Goal**: Allow resource owners to grant access to other users (collaboration)

**Scope**: Lists and Todos only (most common sharing use cases)

**Out of Scope** (for Phase 1.4):
- Role-based permissions (viewer/editor/admin) → Phase 2
- Workspace/organization isolation → Phase 3
- Audit logging → Phase 4

---

## Phase 1: Schema Analysis (15 min) ⭐⭐⭐

**CRITICAL**: Before implementing, understand what already exists.

### Task 1.1: Check Existing Schema

The database already has sharing columns! Check the current schema:

```bash
# Check lists table
psql -U piper -d piper_morgan -c "\d lists"

# Check if shared_with column exists
psql -U piper -d piper_morgan -c "
  SELECT column_name, data_type
  FROM information_schema.columns
  WHERE table_name = 'lists' AND column_name = 'shared_with';
"

# Check todos table
psql -U piper -d piper_morgan -c "\d todos"
```

**Expected findings** (based on Issue #367 completion):
- `lists.shared_with` → JSONB column (with GIN index)
- `lists.tags` → JSONB column (with GIN index)
- `todos` table → may have similar sharing columns

### Task 1.2: Check Database Models

Read the SQLAlchemy models to understand the current schema:

```bash
# Find the lists/todos model definitions
grep -A 20 "class.*List.*DB" services/database/models.py
grep -A 20 "class.*Todo.*DB" services/database/models.py

# Or check if there's a separate models file
find services/ -name "models.py" -type f
```

**Document**:
- Does `shared_with` column exist?
- What's the JSONB structure? (e.g., `{"users": ["uuid1", "uuid2"]}`)
- Are there any existing sharing-related columns?

### Task 1.3: Check Domain Models

Read the Pydantic domain models:

```bash
# Check domain models for lists/todos
grep -A 30 "class.*List" services/domain/models.py
grep -A 30 "class.*Todo" services/domain/models.py
```

**Document**:
- Do domain models have `shared_with` field?
- What's the type? (List[UUID]? Dict? Custom model?)
- Any validation logic already present?

---

## Phase 2: Create STOP Report (10 min) ⚡

**MANDATORY STOP CONDITION**: Report findings before implementation.

**Create file**: `dev/2025/11/22/sec-rbac-phase1.4-schema-analysis.md`

**Template**:

```markdown
# SEC-RBAC Phase 1.4: Schema Analysis Report

**Date**: November 22, 2025
**Agent**: Claude Code

## Database Schema Findings

### Lists Table
- `shared_with` column: [EXISTS/MISSING]
- Data type: [JSONB/JSON/VARCHAR/etc.]
- Index type: [GIN/BTREE/NONE]
- Current structure: [describe JSONB schema if exists]

### Todos Table
- `shared_with` column: [EXISTS/MISSING]
- Similar findings...

## Database Models (SQLAlchemy)

**File**: `services/database/models.py` (or wherever found)

```python
# Paste relevant model definitions
class ListDB(Base):
    ...
    shared_with = Column(...)  # Or doesn't exist
```

## Domain Models (Pydantic)

**File**: `services/domain/models.py`

```python
# Paste relevant domain model definitions
class List(BaseModel):
    ...
    shared_with: Optional[...]  # Or doesn't exist
```

## Implementation Options

### Option A: Schema Already Exists
If `shared_with` columns exist:
1. Use existing JSONB structure
2. Add service layer methods for sharing
3. Add endpoint routes for share/unshare
4. Update ownership validation to include shared access

### Option B: Schema Needs Creation
If `shared_with` columns don't exist:
1. Create migration to add JSONB columns
2. Add GIN indexes for efficient querying
3. Implement service layer methods
4. Add endpoint routes

### Option C: Partial Schema
If some sharing infrastructure exists but incomplete:
1. Document what exists
2. Identify gaps
3. Propose minimal additions

## Recommended Approach

[Based on findings above, which option do you recommend?]

## Questions for PM

- [Any unclear decisions or patterns?]

## Ready to Implement?

- [ ] Database schema understood
- [ ] Model definitions found
- [ ] JSONB structure documented (if exists)
- [ ] Implementation option chosen

**STOP HERE - Report to PM before proceeding**
```

**Action**: Create this file, then **STOP and wait for PM approval** before implementing.

---

## Phase 3: Implementation (ONLY AFTER APPROVAL)

**DO NOT START THIS PHASE without PM approval of your schema analysis.**

### Implementation Path A: Use Existing Schema

**If `shared_with` JSONB columns already exist:**

#### Step 3.1: Update Repository Layer

**File**: `services/repositories/universal_list_repository.py`

Add sharing methods:

```python
async def share_list(
    self,
    list_id: UUID,
    owner_id: UUID,
    user_to_share_with: UUID
) -> Optional[UniversalList]:
    """Share a list with another user (owner only)"""
    # 1. Verify caller is owner
    list_obj = await self.get_list(list_id, owner_id=owner_id)
    if not list_obj:
        return None  # Not found or not owner

    # 2. Add user to shared_with JSONB
    stmt = update(ListDB).where(
        ListDB.id == list_id
    ).values(
        shared_with=func.jsonb_set(
            ListDB.shared_with,
            ['users'],
            func.jsonb_build_array(user_to_share_with),
            True  # Create path if not exists
        )
    )

    await self.session.execute(stmt)
    await self.session.commit()

    # 3. Return updated list
    return await self.get_list(list_id, owner_id=owner_id)

async def unshare_list(
    self,
    list_id: UUID,
    owner_id: UUID,
    user_to_unshare: UUID
) -> Optional[UniversalList]:
    """Remove sharing access (owner only)"""
    # Similar pattern - remove user from shared_with JSONB
    ...

async def get_lists_shared_with_me(
    self,
    user_id: UUID
) -> List[UniversalList]:
    """Get lists shared with this user (not owned by user)"""
    stmt = select(ListDB).where(
        and_(
            ListDB.owner_id != user_id,  # Not my lists
            ListDB.shared_with.op('@>')(
                func.jsonb_build_object('users', func.jsonb_build_array(user_id))
            )  # Shared with me
        )
    )

    result = await self.session.execute(stmt)
    return [self._map_to_domain(row) for row in result.scalars()]
```

#### Step 3.2: Update Ownership Validation

**Modify existing `get_list()` to check both ownership AND sharing**:

```python
async def get_list(
    self,
    list_id: UUID,
    user_id: Optional[UUID] = None
) -> Optional[UniversalList]:
    """Get list - supports ownership OR shared access"""
    filters = [ListDB.id == list_id]

    if user_id:
        # Allow access if EITHER:
        # 1. User is owner
        # 2. User is in shared_with array
        filters.append(
            or_(
                ListDB.owner_id == user_id,  # Owner
                ListDB.shared_with.op('@>')(
                    func.jsonb_build_object(
                        'users',
                        func.jsonb_build_array(user_id)
                    )
                )  # Shared with user
            )
        )

    stmt = select(ListDB).where(and_(*filters))
    result = await self.session.execute(stmt)
    row = result.scalar_one_or_none()

    return self._map_to_domain(row) if row else None
```

**Pattern**: Update all read methods (get_list, get_lists, etc.) to support shared access

#### Step 3.3: Add Sharing Endpoints

**File**: `web/api/routes/lists.py`

```python
@router.post("/{list_id}/share")
async def share_list(
    list_id: UUID,
    share_request: ShareListRequest,  # Pydantic model with user_id field
    current_user: JWTClaims = Depends(get_current_user),
    list_repo: UniversalListRepository = Depends(get_list_repository)
):
    """Share list with another user (owner only)"""
    result = await list_repo.share_list(
        list_id=list_id,
        owner_id=current_user.sub,
        user_to_share_with=share_request.user_id
    )

    if not result:
        raise HTTPException(404, "List not found or not owned by you")

    logger.info(
        "list_shared",
        list_id=str(list_id),
        owner_id=str(current_user.sub),
        shared_with=str(share_request.user_id)
    )

    return result

@router.delete("/{list_id}/share/{user_id}")
async def unshare_list(
    list_id: UUID,
    user_id: UUID,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo: UniversalListRepository = Depends(get_list_repository)
):
    """Remove sharing access (owner only)"""
    result = await list_repo.unshare_list(
        list_id=list_id,
        owner_id=current_user.sub,
        user_to_unshare=user_id
    )

    if not result:
        raise HTTPException(404, "List not found or not owned by you")

    logger.info(
        "list_unshared",
        list_id=str(list_id),
        owner_id=str(current_user.sub),
        unshared_from=str(user_id)
    )

    return {"status": "success"}

@router.get("/shared-with-me")
async def get_shared_lists(
    current_user: JWTClaims = Depends(get_current_user),
    list_repo: UniversalListRepository = Depends(get_list_repository)
):
    """Get all lists shared with current user"""
    lists = await list_repo.get_lists_shared_with_me(current_user.sub)

    logger.info(
        "shared_lists_retrieved",
        user_id=str(current_user.sub),
        count=len(lists)
    )

    return {"lists": lists, "count": len(lists)}
```

#### Step 3.4: Add Pydantic Models

**File**: `services/domain/models.py` (or appropriate location)

```python
class ShareListRequest(BaseModel):
    """Request to share a list with another user"""
    user_id: UUID

class ShareListResponse(BaseModel):
    """Response after sharing a list"""
    list_id: UUID
    owner_id: UUID
    shared_with: List[UUID]
```

---

### Implementation Path B: Create New Schema

**If `shared_with` columns DON'T exist:**

#### Step 3.1: Create Migration

**File**: `alembic/versions/[timestamp]_add_shared_access_to_lists_todos.py`

```python
def upgrade():
    # Add shared_with column to lists table
    op.execute("""
        ALTER TABLE lists
        ADD COLUMN IF NOT EXISTS shared_with JSONB DEFAULT '{}'::jsonb
    """)

    # Create GIN index for efficient shared access queries
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_lists_shared_with
        ON lists USING gin (shared_with)
    """)

    # Same for todos table
    op.execute("""
        ALTER TABLE todos
        ADD COLUMN IF NOT EXISTS shared_with JSONB DEFAULT '{}'::jsonb
    """)

    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_todos_shared_with
        ON todos USING gin (shared_with)
    """)

def downgrade():
    op.execute("DROP INDEX IF EXISTS idx_lists_shared_with")
    op.execute("ALTER TABLE lists DROP COLUMN IF EXISTS shared_with")

    op.execute("DROP INDEX IF EXISTS idx_todos_shared_with")
    op.execute("ALTER TABLE todos DROP COLUMN IF EXISTS shared_with")
```

**Then run**:
```bash
python -m alembic upgrade head
```

**Then proceed with Path A steps** (repository methods, endpoints, etc.)

---

## Phase 4: Testing (After Implementation)

### Task 4.1: Manual Sharing Test

**Create test script**: `tests/manual/manual_sec_rbac_phase1_4_sharing.py`

```python
"""Manual test for SEC-RBAC Phase 1.4 shared resource access"""
import httpx
import asyncio
from uuid import UUID

async def test_list_sharing():
    """Verify sharing works correctly"""

    async with httpx.AsyncClient() as client:
        # User 1 creates a list
        response = await client.post(
            "http://localhost:8001/api/auth/login",
            json={"username": "user1", "password": "test"}
        )
        user1_token = response.json()["access_token"]

        # Create list as user1
        response = await client.post(
            "http://localhost:8001/api/v1/lists",
            headers={"Authorization": f"Bearer {user1_token}"},
            json={"name": "Shared Shopping List", "description": "Groceries"}
        )
        list_id = response.json()["id"]

        # Authenticate as user2
        response = await client.post(
            "http://localhost:8001/api/auth/login",
            json={"username": "user2", "password": "test"}
        )
        user2_token = response.json()["access_token"]
        user2_id = response.json()["user_id"]

        # User2 can't access list (not shared yet)
        response = await client.get(
            f"http://localhost:8001/api/v1/lists/{list_id}",
            headers={"Authorization": f"Bearer {user2_token}"}
        )
        assert response.status_code == 404, "Should not access before sharing"
        print("✅ User2 cannot access unshared list")

        # User1 shares list with user2
        response = await client.post(
            f"http://localhost:8001/api/v1/lists/{list_id}/share",
            headers={"Authorization": f"Bearer {user1_token}"},
            json={"user_id": user2_id}
        )
        assert response.status_code == 200, "Sharing should succeed"
        print("✅ User1 shared list with User2")

        # User2 can now access shared list
        response = await client.get(
            f"http://localhost:8001/api/v1/lists/{list_id}",
            headers={"Authorization": f"Bearer {user2_token}"}
        )
        assert response.status_code == 200, "Should access after sharing"
        print("✅ User2 can access shared list")

        # User2 sees list in shared-with-me endpoint
        response = await client.get(
            "http://localhost:8001/api/v1/lists/shared-with-me",
            headers={"Authorization": f"Bearer {user2_token}"}
        )
        shared_lists = response.json()["lists"]
        assert len(shared_lists) > 0, "Should see shared list"
        assert any(l["id"] == list_id for l in shared_lists)
        print("✅ User2 sees list in shared-with-me")

        # User1 unshares list
        response = await client.delete(
            f"http://localhost:8001/api/v1/lists/{list_id}/share/{user2_id}",
            headers={"Authorization": f"Bearer {user1_token}"}
        )
        assert response.status_code == 200, "Unsharing should succeed"
        print("✅ User1 unshared list from User2")

        # User2 can no longer access
        response = await client.get(
            f"http://localhost:8001/api/v1/lists/{list_id}",
            headers={"Authorization": f"Bearer {user2_token}"}
        )
        assert response.status_code == 404, "Should not access after unsharing"
        print("✅ User2 cannot access after unsharing")

if __name__ == "__main__":
    asyncio.run(test_list_sharing())
```

### Task 4.2: Integration Tests

Create proper integration tests:

**File**: `tests/integration/test_sec_rbac_phase1_4_sharing.py`

```python
"""Integration tests for Phase 1.4 shared resource access"""
import pytest
from uuid import UUID, uuid4

class TestListSharing:
    """Test list sharing functionality"""

    async def test_owner_can_share_list(self, async_transaction):
        """Owner can share their list with another user"""
        # Test implementation
        ...

    async def test_shared_user_can_read_list(self, async_transaction):
        """User with shared access can read the list"""
        # Test implementation
        ...

    async def test_shared_user_cannot_share_further(self, async_transaction):
        """Shared user cannot re-share (only owner can)"""
        # Test implementation
        ...

    async def test_owner_can_unshare_list(self, async_transaction):
        """Owner can revoke sharing access"""
        # Test implementation
        ...

    async def test_unshared_user_loses_access(self, async_transaction):
        """After unsharing, user can no longer access"""
        # Test implementation
        ...

class TestTodoSharing:
    """Test todo sharing functionality"""
    # Similar tests for todos
    ...
```

---

## Phase 5: Documentation (After Testing)

**Create file**: `dev/2025/11/22/sec-rbac-phase1.4-completion-report.md`

**Template**:

```markdown
# SEC-RBAC Phase 1.4: Shared Resource Access - COMPLETION REPORT

**Date**: November 22, 2025
**Agent**: Claude Code
**Status**: ✅ COMPLETE

## Summary

Successfully implemented shared resource access for Lists and Todos, enabling collaboration while maintaining ownership security.

## Schema Implementation

[Document whether used existing schema or created new]

### Lists Table
- `shared_with`: JSONB column
- Index: GIN index on shared_with
- Structure: `{"users": ["uuid1", "uuid2"]}`

### Todos Table
- Similar structure...

## Repository Methods Added

### UniversalListRepository
- `share_list(list_id, owner_id, user_to_share_with)` ✅
- `unshare_list(list_id, owner_id, user_to_unshare)` ✅
- `get_lists_shared_with_me(user_id)` ✅
- Updated `get_list()` to support shared access ✅
- Updated `get_lists()` to support shared access ✅

[Similar for TodoRepository]

## Endpoints Added

### Lists API
- `POST /lists/{list_id}/share` - Share list with user ✅
- `DELETE /lists/{list_id}/share/{user_id}` - Unshare ✅
- `GET /lists/shared-with-me` - Get shared lists ✅

[Similar for Todos API]

## Security Model

**Ownership**: Only owner can share/unshare
**Shared Access**: Read-only (shared users cannot modify)
**Access Validation**: Both owned AND shared resources accessible
**Revocation**: Owner can revoke access anytime

## Testing Evidence

### Manual Testing
- Sharing works: ✅
- Shared access works: ✅
- Unsharing works: ✅
- Access revoked after unshare: ✅

### Integration Tests
- All tests passing: [X/X] ✅

## Commits

1. [hash] - Add shared_with schema (if new migration)
2. [hash] - Add repository sharing methods
3. [hash] - Add sharing endpoints
4. [hash] - Add integration tests

## Metrics

- **Resource Types**: 2 (Lists, Todos)
- **Repository Methods**: 6 (3 per resource type)
- **Endpoints Added**: 6 (3 per resource type)
- **Tests Added**: [X] integration tests

## Phase 1.4 COMPLETE ✅

Shared resource access now working for Lists and Todos.

**Next**: Phase 2 - Role-Based Permissions (viewer/editor/admin roles)

---

_Report created by: Claude Code_
```

---

## Success Criteria

**Phase 1.4 is complete when**:

- [ ] Schema analysis complete and approved
- [ ] Repository sharing methods implemented
- [ ] Ownership validation updated to include shared access
- [ ] Sharing endpoints added (share/unshare/shared-with-me)
- [ ] Manual sharing test passes
- [ ] Integration tests pass
- [ ] Completion report created with evidence

---

## What NOT to Do

**DO NOT**:
- Skip schema analysis (Phase 1 is mandatory)
- Implement before getting approval on approach
- Assume schema structure (verify with database queries)
- Add complex permissions (viewer/editor) - that's Phase 2
- Skip testing (manual + integration required)
- Allow shared users to modify resources (read-only for Phase 1.4)

**DO**:
- Follow phases in order (1 → 2 → 3 → 4 → 5)
- STOP after Phase 1 schema analysis
- Wait for PM approval
- Use existing JSONB infrastructure if available
- Test sharing, unsharing, and access revocation
- Provide evidence for all claims

---

## Timeline Estimate

- Phase 1 (Schema Analysis): 15 minutes
- Phase 2 (STOP report): 10 minutes
- **WAIT FOR APPROVAL**
- Phase 3 (Implementation): 45-60 minutes
- Phase 4 (Testing): 20 minutes
- Phase 5 (Documentation): 15 minutes

**Total**: ~2 hours (including approval wait)

---

**Remember**: Schema analysis first, implementation second. The database may already have sharing infrastructure from earlier work - discover and use it rather than recreating.

Good luck! 🚀

---

_Prompt created by: Lead Developer (Cursor)_
_Date: November 22, 2025, 9:10 AM_
_Session: SEC-RBAC Phase 1.4 Shared Resource Access_
_Prerequisites: Phases 1.1, 1.2, 1.3 complete_
