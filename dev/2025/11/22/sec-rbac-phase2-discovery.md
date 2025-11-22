# SEC-RBAC Phase 2 Discovery - Role-Based Permissions

**Date**: November 22, 2025, 10:37 AM
**Status**: 🔍 DISCOVERY - AWAITING PM APPROVAL
**Session**: Continuing from Phase 1.4 (Complete)

---

## Context from Phase 1.4

Phase 1.4 established the foundation:
- Simple `shared_with` array of user IDs
- Read-only access for all shared users
- No permission differentiation in JSONB structure

Phase 2 will extend this with **role-based permissions**.

---

## Phase 2 Vision (from PM Approval)

```
Phase 2 Objectives:
- Add roles: viewer (read-only), editor (can modify), admin (can share)
- Phase 1.4 lays foundation for these roles
```

---

## Critical Questions for PM

Before proceeding with Phase 2 implementation, I need clarification on:

### Question 1: JSONB Structure for Role Metadata

**Current Structure** (Phase 1.4):
```jsonb
shared_with: ["uuid1", "uuid2", "uuid3"]
```

**Option A**: Upgrade to role metadata
```jsonb
shared_with: [
  {"user_id": "uuid1", "role": "viewer"},
  {"user_id": "uuid2", "role": "editor"},
  {"user_id": "uuid3", "role": "admin"}
]
```

**Option B**: Keep simple array, add separate roles table
```jsonb
shared_with: ["uuid1", "uuid2", "uuid3"]

-- New table: share_permissions(list_id, user_id, role)
```

**Option C**: Use JSONB with both formats (backward compatible)
```jsonb
shared_with: ["uuid1", {"user_id": "uuid2", "role": "editor"}]
-- Mixed simple and complex entries
```

**Which approach do you prefer?**

---

### Question 2: Role Permission Matrix

Which operations should each role allow?

**Viewer** (read-only):
- ✅ Read list/todo details
- ❌ Modify content
- ❌ Delete
- ❌ Share with others

**Editor** (can modify):
- ✅ Read list/todo details
- ✅ Modify content (name, description, etc.)
- ❌ Delete
- ❌ Share with others (only owner can share)

**Admin** (can share):
- ✅ Read list/todo details
- ✅ Modify content
- ✅ Share with others (but not delete)
- ❌ Delete (only owner can delete)

**Is this correct, or should permissions differ?**

---

### Question 3: Default Role for Shared Access

When Owner shares a resource with a user, what role should they get by default?

**Option A**: Always "viewer" (safest)
- Explicit action needed to upgrade to "editor" or "admin"
- More secure by default

**Option B**: Configurable per share action
- Owner specifies role when sharing: `POST /share?role=editor`
- Requires user to choose role

**Option C**: Two-step process
- Share → creates pending share
- Recipient accepts with chosen role
- More UX overhead

**Your preference?**

---

### Question 4: Migration Strategy

Currently, Phase 1.4 has users in `shared_with` array with no role information.

How should we handle the migration?

**Option A**: Default all existing entries to "viewer"
```python
# During migration, convert:
shared_with: ["uuid1", "uuid2"]
# To:
shared_with: [
  {"user_id": "uuid1", "role": "viewer"},
  {"user_id": "uuid2", "role": "viewer"}
]
```

**Option B**: Add migration as separate step
- Backward compatibility: Support both formats initially
- Later deprecate simple array format

**Your preference?**

---

### Question 5: Scope - Lists and Todos Only?

Should Phase 2 add roles for:
- ✅ Lists (Universal Lists) - YES
- ✅ TodoLists - YES
- ❓ Other resources (Projects, Files, etc.) - YES or NO?

**Which resources need role-based permissions?**

---

## Phase 2 Scope (Preliminary)

Assuming answers to above questions, Phase 2 will include:

### Implementation Steps

1. **Schema Upgrade**
   - Modify JSONB structure to include role metadata
   - OR create new share_permissions table
   - Migration for Phase 1.4 data

2. **Domain Models**
   - Add `SharePermission` or similar class
   - Add role enum: Viewer, Editor, Admin

3. **Repository Methods**
   - Update `share_list()` to accept role parameter
   - Add `get_shared_with_roles()` to retrieve full permission set
   - Update `get_list_for_read()` to check specific roles

4. **API Endpoints**
   - Modify `POST /share` to accept role in request body
   - Add `GET /shares` to list all shared access with roles
   - Add `PUT /share/{user_id}` to change user's role (owner only)

5. **Access Control**
   - Update repository layer to check role, not just presence in array
   - Implement role-based permission checking
   - Ensure owner always has all permissions

6. **Testing**
   - Test each role's capabilities
   - Test role transitions (viewer → editor)
   - Test editor cannot delete, cannot share

---

## Estimated Work Breakdown

| Task | Estimate | Notes |
|------|----------|-------|
| Schema decision & migration | 30 min | Depends on PM answer |
| Domain models + enums | 20 min | Straightforward |
| Repository method updates | 45 min | Complex queries with roles |
| API endpoint updates | 45 min | Additional validation |
| Access control refactor | 45 min | Significant change |
| Testing & documentation | 45 min | Comprehensive test matrix |
| **TOTAL** | **210 min** | ~3.5 hours |

---

## Risk Assessment

### High Risk Areas

1. **Migration Complexity**: Converting Phase 1.4 data to role format
2. **Backward Compatibility**: Supporting both old and new formats
3. **Access Control Logic**: Complex role-based decision tree

### Mitigation Strategies

- Atomic database operations for migration
- Comprehensive test coverage for each role
- Clear audit logging for permission changes

---

## Recommendation

I recommend we:

1. **Get PM approval** on the 5 questions above
2. **Create Phase 2 Gameplan** document with detailed implementation steps
3. **Execute Phase 2** once gameplan is approved

---

## Next Steps

**Awaiting PM Response** to the 5 critical questions above before proceeding.

Once approved:
1. ✅ Create detailed Phase 2 gameplan
2. ✅ Implement schema changes
3. ✅ Update repository layer
4. ✅ Add/modify API endpoints
5. ✅ Comprehensive testing
6. ✅ Documentation

---

_Discovery Report: SEC-RBAC Phase 2_
_Date: November 22, 2025, 10:37 AM_
_Status: ⏸️ AWAITING PM DECISIONS_
