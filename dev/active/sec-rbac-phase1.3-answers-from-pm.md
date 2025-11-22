# SEC-RBAC Phase 1.3: PM Answers to Code Agent Questions

**Date**: November 22, 2025, 7:25 AM
**From**: PM (via Lead Developer)
**To**: Code Agent
**Re**: Phase 1.3 Infrastructure Discovery Questions

---

## Answer 1: Database State After Phase 1.1

**Short Answer**: YES - Proceed assuming owner_id columns exist

**Details**:
- Phase 1.1 achieved 70% migration completion
- Migration `4d1e2c3b5f7a` (SEC-RBAC schema) was successfully applied
- All 9 resource tables have owner_id columns in the applied portion
- Database is in "sufficient" state for Phase 1.3 work

**Action**: Assume owner_id columns exist. If you encounter issues during implementation, report them.

---

## Answer 2: FileRepository.session_id vs owner_id

**Short Answer**: Code needs updating - use owner_id, not session_id

**Details**:
- The database schema was migrated to owner_id (Phase 1.1)
- The code still references session_id (old pattern)
- Phase 1.2 service layer updates may have been incomplete for FileRepository

**Action**:
1. Update FileRepository code to use `owner_id` instead of `session_id`
2. Pattern: `filters.append(UploadedFileDB.owner_id == owner_id)`
3. This is part of Phase 1.3 work - fix it as you go

**Evidence**: Migration 4d1e2c3b5f7a added owner_id columns to uploaded_files table

---

## Answer 3: Endpoint Dependency Injection

**Short Answer**: Some providers exist, create others as needed

**Details**:

**Existing DI Providers** (found in web/api/routes/):
- ✅ `get_jwt_service` (auth.py)
- ✅ `get_user_api_key_service` (api_keys.py)
- ✅ `get_standup_service` (standup.py)
- ✅ `get_cross_feature_service_instance` (learning.py)

**Need to Create**:
- ❌ get_file_repository
- ❌ get_list_repository
- ❌ get_knowledge_service
- ❌ get_todo_repo
- ❌ get_project_repo
- ❌ get_feedback_service

**Action**:
1. Follow the existing pattern from auth.py / api_keys.py
2. Create DI providers as needed for each endpoint category
3. Pattern example:

```python
async def get_file_repository(request: Request) -> FileRepository:
    """Dependency injection for FileRepository"""
    return FileRepository(request.state.db)
```

---

## Answer 4: Database Session Injection

**Short Answer**: AsyncSession is stored in `request.state.db`

**Pattern** (based on existing codebase):

```python
# In endpoint:
@router.get("/files/{file_id}")
async def get_file(
    file_id: UUID,
    request: Request,
    current_user: JWTClaims = Depends(get_current_user)
):
    # Access database session from request state
    db = request.state.db

    # Instantiate repository
    file_repo = FileRepository(db)

    # Call with owner_id
    file = await file_repo.get_file(file_id, owner_id=current_user.user_id)
    ...
```

**Or with DI**:

```python
@router.get("/files/{file_id}")
async def get_file(
    file_id: UUID,
    current_user: JWTClaims = Depends(get_current_user),
    file_repo: FileRepository = Depends(get_file_repository)
):
    # Repository already has session injected via DI
    file = await file_repo.get_file(file_id, owner_id=current_user.user_id)
    ...
```

**Evidence**: Check `web/api/routes/auth.py` or `web/api/routes/api_keys.py` for existing patterns

---

## Implementation Guidance

### Recommended Pattern (Option A - With DI)

1. **Create DI providers** (one per service/repository):

```python
# Add to each route file or create web/api/dependencies.py
async def get_file_repository(request: Request) -> FileRepository:
    return FileRepository(request.state.db)

async def get_list_repository(request: Request) -> UniversalListRepository:
    return UniversalListRepository(request.state.db)

# etc...
```

2. **Use in endpoints**:

```python
@router.get("/files/{file_id}")
async def get_file(
    file_id: UUID,
    current_user: JWTClaims = Depends(get_current_user),
    file_repo: FileRepository = Depends(get_file_repository)
):
    """Get file - validates ownership"""
    file = await file_repo.get_file(file_id, owner_id=current_user.user_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file
```

### Alternative Pattern (Option B - Manual Instantiation)

```python
@router.get("/files/{file_id}")
async def get_file(
    file_id: UUID,
    request: Request,
    current_user: JWTClaims = Depends(get_current_user)
):
    """Get file - validates ownership"""
    file_repo = FileRepository(request.state.db)
    file = await file_repo.get_file(file_id, owner_id=current_user.user_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file
```

**Recommendation**: Use Option A (DI) for consistency with existing codebase patterns

---

## Special Note: FileRepository session_id Issue

**Problem**: FileRepository code references session_id but database has owner_id

**Fix Required** (as part of Phase 1.3):

```python
# In services/repositories/file_repository.py
# BEFORE:
if owner_id:
    filters.append(UploadedFileDB.session_id == owner_id)  # WRONG

# AFTER:
if owner_id:
    filters.append(UploadedFileDB.owner_id == owner_id)  # CORRECT
```

**Action**: Fix this when implementing file endpoints

---

## Authorization

**All questions answered**. You are approved to proceed with Phase 1.3 implementation:

1. ✅ Database state is sufficient (70% with owner_id columns)
2. ✅ Fix FileRepository to use owner_id (part of Phase 1.3 work)
3. ✅ Create DI providers as needed (follow existing pattern)
4. ✅ Use request.state.db for database session access

**Next Steps**:
1. Create DI providers for repositories/services
2. Fix FileRepository session_id → owner_id references
3. Implement endpoint protection using approved pattern (Option A - DI)
4. Test cross-user access blocking
5. Create completion report with evidence

Good luck! 🚀

---

_Answers provided by: PM (xian)_
_Via: Lead Developer (Cursor session)_
_Time: 7:25 AM, November 22, 2025_
_Authority: PM approval for Phase 1.3 implementation_
