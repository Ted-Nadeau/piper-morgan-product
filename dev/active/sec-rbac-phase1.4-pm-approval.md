# SEC-RBAC Phase 1.4: PM Approval for Code Agent

**Date**: November 22, 2025, 9:15 AM
**From**: PM (via Lead Developer)
**To**: Code Agent
**Re**: Phase 1.4 Schema Analysis - Approval to Proceed

---

## Schema Analysis Review: ✅ APPROVED

Excellent work on the schema analysis! Your findings are accurate and the Option A approach is exactly right.

---

## Answers to Your Questions

### Question 1: Shared Access Permissions

**Answer**: Read-only access for Phase 1.4

**Details**:
- Shared users can READ lists/todos
- Shared users CANNOT edit or delete
- Only owner can share/unshare
- Only owner can modify or delete

**Rationale**: Edit permissions belong in Phase 2 (Role-Based Permissions: viewer/editor/admin)

---

### Question 2: Sharing Scope Confirmation

**Answer**: Lists and TodoLists only (not individual items)

**Confirmed**:
- ✅ Lists (Universal Lists) - YES
- ✅ TodoLists - YES
- ❌ Individual TodoItems - NO (list-level sharing is sufficient)

**Rationale**: List-level sharing covers the collaboration use case without over-complicating permissions

---

### Question 3: Implementation Path

**Answer**: Option A is perfect - use existing schema, no migration needed

**Approval**:
- ✅ Use existing `shared_with` JSONB columns
- ✅ Use existing GIN indexes
- ✅ No database migration required
- ✅ Proceed directly to domain models + repository methods + endpoints

---

## Implementation Guidance

### Sharing Semantics

**Owner Capabilities**:
- Create, read, update, delete their own resources
- Share with any user (add to shared_with array)
- Unshare from any user (remove from shared_with array)
- Cannot share resources they don't own

**Shared User Capabilities** (Phase 1.4):
- Read shared resources (lists, todos)
- See shared resources in "shared-with-me" endpoint
- CANNOT modify shared resources
- CANNOT share resources further (no re-sharing)
- CANNOT delete shared resources

**Future** (Phase 2):
- Add roles: viewer (read-only), editor (can modify), admin (can share)
- Phase 1.4 lays foundation for these roles

---

## Recommended Access Pattern

Update `get_list()` and similar methods to check BOTH:

```python
# User can access if EITHER:
# 1. User is owner
# 2. User is in shared_with array

filters.append(
    or_(
        ListDB.owner_id == user_id,  # Owner
        ListDB.shared_with.op('@>')(
            func.jsonb_build_array(user_id)
        )  # Shared with user
    )
)
```

**For updates/deletes**: Only check ownership (shared users can't modify)

```python
# Updates/deletes require ownership
filters.append(ListDB.owner_id == user_id)  # Owner only
```

---

## JSONB Structure

Use simple array structure (already in database):

```jsonb
shared_with: []  # No sharing

shared_with: ["550e8400-e29b-41d4-a716-446655440000"]  # Shared with 1 user

shared_with: [
  "550e8400-e29b-41d4-a716-446655440000",
  "7c9e6679-7425-40de-944b-e07fc1f90ae7"
]  # Shared with 2 users
```

**Do NOT use**:
- Complex nested structures
- Permission levels in JSONB (that's Phase 2)
- User metadata in shared_with (just UUIDs)

---

## Domain Model Updates

### List Domain Model

```python
@dataclass
class List:
    # Existing fields...
    owner_id: str  # ADD THIS
    shared_with: List[str] = field(default_factory=list)  # ADD THIS
```

### Todo Domain Model

```python
@dataclass
class Todo(Item):
    # Existing fields...
    # owner_id already exists ✅
    shared_with: List[str] = field(default_factory=list)  # ADD THIS
```

---

## Endpoints to Add

### Lists API (web/api/routes/lists.py)

```python
POST   /api/v1/lists/{list_id}/share
       Body: {"user_id": "uuid"}
       Auth: Must be owner
       Returns: Updated list with shared_with array

DELETE /api/v1/lists/{list_id}/share/{user_id}
       Auth: Must be owner
       Returns: Success status

GET    /api/v1/lists/shared-with-me
       Auth: Any authenticated user
       Returns: Lists shared with current user
```

### Todos API (web/api/routes/todos.py)

Same 3 endpoints for todos.

---

## Testing Requirements

### Manual Test Must Verify

1. Owner can share list → User B gains read access ✅
2. Shared user (User B) can read list ✅
3. Shared user CANNOT modify list ❌ (404 or 403)
4. Shared user CANNOT delete list ❌ (404 or 403)
5. Shared user CANNOT share list further ❌ (404 or 403)
6. Owner can unshare → User B loses access ✅
7. Unshared user gets 404 when accessing ✅

### Integration Tests Must Cover

- share_list() adds user to array
- unshare_list() removes user from array
- get_lists_shared_with_me() returns correct lists
- get_list() allows BOTH owner and shared users
- update_list() allows ONLY owner
- delete_list() allows ONLY owner

---

## Security Considerations

**Information Leakage Prevention**:
- Return 404 (not 403) for non-owned/non-shared resources
- Don't reveal whether resource exists if user lacks access
- Log all sharing operations (who shared what with whom)

**Validation**:
- Verify owner_id before allowing share/unshare
- Verify user_to_share_with exists (optional but nice)
- Prevent owner from sharing with themselves (no-op or error)

**Race Conditions**:
- Use atomic JSONB operations (jsonb_set, array operations)
- Don't read-modify-write shared_with array

---

## Approval Summary

✅ **Approved to proceed with Phase 1.4 implementation**

**Scope**:
- Read-only shared access for Lists and TodoLists
- Owner-only sharing/unsharing
- No edit permissions for shared users (Phase 2)

**Approach**:
- Option A (use existing schema)
- No migration needed
- Estimated 110 minutes

**Prerequisites**:
- All Phase 1.3 work complete ✅
- Database schema ready ✅
- GIN indexes deployed ✅

---

## Authorization

**Approved by**: PM (xian)
**Date**: November 22, 2025, 9:15 AM
**Authority**: Product Management approval for Phase 1.4 implementation

**You are cleared to proceed with Phase 3 implementation.**

Good luck! 🚀

---

_Approval provided by: PM (xian)_
_Via: Lead Developer (Cursor session)_
_Time: 9:15 AM, November 22, 2025_
