# SEC-RBAC Phase 1.4: Schema Analysis Report

**Date**: November 22, 2025, 9:07 AM
**Agent**: Claude Code
**Status**: ✅ ANALYSIS COMPLETE - AWAITING PM APPROVAL

---

## 🔍 Database Schema Findings

### Lists Table

**Column**: `shared_with`
- **Exists**: ✅ YES
- **Data Type**: `jsonb` (PostgreSQL JSON binary)
- **Nullable**: YES (default is empty list)
- **Index Type**: GIN index (`idx_lists_shared`)
- **Current Structure**: Array of user IDs (matches Phase 1.4 requirements)

**All Relevant Columns**:
```
id                 - varchar (PRIMARY KEY)
name               - varchar
description        - text
owner_id           - varchar  ← Ownership field
shared_with        - jsonb    ← SHARING FIELD ✅
tags               - jsonb
created_at         - timestamp
updated_at         - timestamp
item_count         - integer
completed_count    - integer
```

**Schema Status**: ✅ **FULLY READY** - No migration needed

---

### TodoLists Table

**Column**: `shared_with`
- **Exists**: ✅ YES
- **Data Type**: `jsonb` (PostgreSQL JSON binary)
- **Nullable**: YES (default is empty list)
- **Index Type**: GIN index
- **Current Structure**: Array of user IDs

**All Relevant Columns**:
```
id                 - varchar (PRIMARY KEY)
name               - varchar
description        - text
owner_id           - varchar  ← Ownership field
shared_with        - jsonb    ← SHARING FIELD ✅
tags               - jsonb
created_at         - timestamp
updated_at         - timestamp
todo_count         - integer
completed_count    - integer
```

**Schema Status**: ✅ **FULLY READY** - No migration needed

---

### TodoItems Table

**Column**: `shared_with`
- **Exists**: ❌ NO
- **Note**: Individual todo items may not need sharing (shared at list level)
- **Recommendation**: Focus on list-level sharing, not item-level

**Conclusion**: For Phase 1.4, **todolist-level sharing is sufficient**

---

## 📋 Database Models (SQLAlchemy)

**File**: `services/database/models.py`

### ListDB Model

```python
class ListDB(Base):
    __tablename__ = "lists"

    # ... other fields ...

    # Ownership and sharing
    owner_id = Column(String, nullable=False)
    shared_with = Column(postgresql.JSONB, default=list)  # Array of user IDs

    # Strategic indexes for performance
    __table_args__ = (
        Index("idx_lists_owner_type", "owner_id", "item_type"),
        Index("idx_lists_owner_list_type", "owner_id", "list_type"),
        Index("idx_lists_owner_archived", "owner_id", "is_archived"),
        Index("idx_lists_shared", "shared_with", postgresql_using="gin"),
        ...
    )
```

**Status**: ✅ **READY TO USE** - `shared_with` column exists and indexed

---

### TodoListDB Model (referenced as `TodoList`)

```python
# Similar structure to ListDB
class TodoListDB(Base):
    __tablename__ = "todo_lists"

    owner_id = Column(String, nullable=False)
    shared_with = Column(postgresql.JSONB, default=list)  # Array of user IDs

    # GIN index for efficient querying
    Index("idx_todo_lists_shared", "shared_with", postgresql_using="gin")
```

**Status**: ✅ **READY TO USE** - `shared_with` column exists and indexed

---

## 🏗️ Domain Models (Pydantic)

**File**: `services/domain/models.py`

### List Domain Model

```python
@dataclass
class List:
    """Universal List model for ANY item type"""
    id: str
    name: str
    description: str
    item_type: str  # todo, feature, bug, attendee
    list_type: str  # personal, shared, project
    # ... other fields ...
    created_at: datetime
    updated_at: datetime
```

**Observation**: Domain model **DOES NOT** have `shared_with` or `owner_id` fields
**Status**: ⚠️ **NEEDS UPDATE** - Must add these fields to domain model

### Todo Domain Model

```python
@dataclass
class Todo(Item):
    # ... inherited from Item ...
    description: str
    priority: str
    status: str
    completed: bool
    # ... other fields ...
    owner_id: Optional[str] = None  ← Has owner_id ✅
    assigned_to: Optional[str] = None
```

**Observation**: Todo model **HAS** `owner_id` but **NO** `shared_with`
**Status**: ⚠️ **NEEDS UPDATE** - Must add `shared_with` field

---

## 📊 Current State Summary

| Component | Lists | TodoLists | TodoItems |
|-----------|-------|-----------|-----------|
| **DB shared_with** | ✅ YES | ✅ YES | ❌ NO |
| **DB GIN Index** | ✅ YES | ✅ YES | ❌ N/A |
| **SQLAlchemy Model** | ✅ YES | ✅ YES | ❌ N/A |
| **Domain Model owner_id** | ❌ NO | ❌ NO | ✅ YES |
| **Domain Model shared_with** | ❌ NO | ❌ NO | ❌ NO |
| **Migration Needed** | ❌ NO | ❌ NO | ❌ N/A |

---

## 🎯 Implementation Options Analysis

### **RECOMMENDED: Option A (Use Existing Schema)**

✅ **Schema already exists!** The `shared_with` JSONB columns were created in Phase 1.1 (Issue #367)

**Path**:
1. Update domain models to include `owner_id` and `shared_with` fields
2. Add service layer methods for sharing (repository layer)
3. Add endpoint routes for share/unshare/shared-with-me
4. Update ownership validation to include shared access

**Advantages**:
- ✅ No database migration needed
- ✅ GIN indexes already exist (performance optimized)
- ✅ JSONB structure proven in Phase 1.1
- ✅ Minimal code changes required
- ✅ Fast implementation (no data migration risk)

**Timeline**: ~90 minutes total

---

### Why NOT Option B (Create New Schema)?

❌ **Not needed** - Schema already exists! Creating a new migration would be:
- Redundant (same columns would conflict)
- Risky (data migration not needed)
- Slower (deployment overhead)
- Wasteful (code already written)

---

## 🔍 JSONB Structure Analysis

**Expected structure** (based on database):
```jsonb
shared_with: []                           # Empty array initially
shared_with: ["uuid1", "uuid2"]           # Array of user UUIDs
shared_with: ["550e8400-e29b-41d4-a716-446655440000", "...]  # Real UUIDs
```

**PostgreSQL Operators for Queries**:
- `@>` (contains) - Check if user is in array
- `jsonb_set()` - Add/update values
- `jsonb_build_array()` - Create arrays
- GIN index supports all these operations efficiently

---

## 📋 Domain Model Updates Needed

### List Domain Model - ADD

```python
@dataclass
class List:
    # ... existing fields ...
    owner_id: str              # NEW
    shared_with: List[str] = field(default_factory=list)  # NEW
```

### Todo Domain Model - ADD

```python
@dataclass
class Todo(Item):
    # ... existing fields ...
    # owner_id already exists ✅
    shared_with: List[str] = field(default_factory=list)  # NEW
```

---

## 🏗️ Repository Methods Needed

### UniversalListRepository - ADD

```python
async def share_list(
    self,
    list_id: UUID,
    owner_id: UUID,
    user_to_share_with: UUID
) -> Optional[UniversalList]:
    """Share a list with another user (owner only)"""

async def unshare_list(
    self,
    list_id: UUID,
    owner_id: UUID,
    user_to_unshare: UUID
) -> Optional[UniversalList]:
    """Remove sharing access (owner only)"""

async def get_lists_shared_with_me(
    self,
    user_id: UUID
) -> List[UniversalList]:
    """Get lists shared with this user"""
```

### Modify existing methods:

```python
async def get_list(
    self,
    list_id: UUID,
    user_id: Optional[UUID] = None
) -> Optional[UniversalList]:
    """
    Get list - NOW supports BOTH:
    1. Ownership access (owner_id == user_id)
    2. Shared access (user_id in shared_with array)
    """
```

---

## 🔗 Endpoints Needed

### Lists API - ADD

```
POST   /api/v1/lists/{list_id}/share
DELETE /api/v1/lists/{list_id}/share/{user_id}
GET    /api/v1/lists/shared-with-me
```

### Todos API - ADD (same pattern)

```
POST   /api/v1/todos/{todo_id}/share
DELETE /api/v1/todos/{todo_id}/share/{user_id}
GET    /api/v1/todos/shared-with-me
```

---

## 🚦 Recommended Implementation Sequence

### Phase 1: ✅ ANALYSIS COMPLETE (THIS REPORT)

**Finding**: Schema fully exists, no migration needed

### Phase 2: (PENDING PM APPROVAL)

**Option**: Use existing JSONB infrastructure

### Phase 3: Implementation (AFTER APPROVAL)

**Sequence**:
1. Update domain models (List, Todo)
2. Add repository sharing methods (UniversalListRepository, TodoListRepository)
3. Update ownership validation in get_list(), get_todo()
4. Add sharing endpoints (lists.py, todos.py)
5. Add Pydantic request/response models

### Phase 4: Testing

1. Manual sharing test
2. Integration tests
3. Unsharing tests
4. Access revocation tests

### Phase 5: Documentation

- Completion report
- Commit summary
- Evidence of sharing working

---

## ✅ Verification Checklist

- [x] Database schema checked (both lists and todo_lists)
- [x] `shared_with` JSONB column exists on both tables
- [x] GIN indexes exist for efficient querying
- [x] SQLAlchemy models have the columns
- [x] JSONB structure documented
- [x] Domain models reviewed
- [x] Domain models updated recommendations provided
- [x] Migration NOT needed (reusing existing schema)
- [x] Implementation path identified (Option A)

---

## 🎯 Questions for PM

1. **Shared Access Permissions**: Should shared users have:
   - Read-only access? (YES, recommended for Phase 1.4)
   - Edit access? (NO, defer to Phase 2 - Role-Based Permissions)
   - Delete access? (NO, only owner can delete)

2. **Sharing Scope Confirmation**: Are we implementing for:
   - Lists? (YES)
   - TodoLists? (YES)
   - Individual TodoItems? (NO, unnecessary - list-level sufficient)

3. **Feedback on Implementation Path**: Does Option A (use existing schema, no migration) work for you?

---

## 🚀 Ready to Implement?

- [x] Database schema understood
- [x] Model definitions found
- [x] JSONB structure documented
- [x] Implementation option chosen (Option A)
- [x] Migration needs identified (NONE)
- [x] Domain model updates identified

---

## 📌 CRITICAL HANDOFF NOTES

**For implementation phase**:

1. **Schema is ready** - The `shared_with` JSONB columns and GIN indexes from Issue #367 are immediately usable
2. **No migration required** - Save time, use existing infrastructure
3. **Two places to update**:
   - Domain models (add `shared_with` field)
   - Repository layer (add sharing methods)
4. **Four endpoints to add**:
   - Two share/unshare endpoints
   - Two shared-with-me endpoints (one per resource type)
5. **Access pattern**: Check BOTH ownership AND shared_with array

---

## 📊 Expected Implementation Work Breakdown

| Task | Estimate | Status |
|------|----------|--------|
| Update domain models | 10 min | Pending |
| Add repository methods | 20 min | Pending |
| Update get_list() for shared access | 15 min | Pending |
| Add sharing endpoints | 20 min | Pending |
| Add Pydantic models | 10 min | Pending |
| Integration tests | 20 min | Pending |
| Documentation | 15 min | Pending |
| **TOTAL** | **110 min** | **Pending PM Approval** |

---

## ⏹️ STOP - AWAITING PM APPROVAL

**This analysis is complete.**

**Next steps**: PM reviews findings and approves implementation approach (Option A).

**Do NOT proceed to Phase 3 implementation without PM approval.**

---

_Report created by: Claude Code_
_Date: November 22, 2025, 9:07 AM_
_Session: SEC-RBAC Phase 1.4 - Shared Resource Access_
_Issue: #357_
