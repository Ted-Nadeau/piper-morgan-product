# Claude Code Prompt: SEC-RBAC Phase 1.3 - Endpoint Protection

## Your Identity

You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Mission: SEC-RBAC Phase 1.3 - Endpoint Authorization

**GitHub Issue**: #357 - SEC-RBAC: Implement RBAC
**Current Phase**: Phase 1.3 - Endpoint Protection
**Status**: Ready to implement (Prerequisites complete)
**Goal**: Add owner_id validation to FastAPI endpoints

---

## Context: What's Already Done

### Phase 1.2 (Service Layer): ✅ COMPLETE

**7 services with 52+ methods secured**:
1. FileRepository (14 methods) - Commit: 1a41237e, 263ae02f
2. UniversalListRepository (11 methods) - Commit: d214ac83
3. TodoManagementService (7 methods) - Already secure
4. FeedbackService (4 methods) - Commit: 241f1629
5. TodoListRepository (4 methods) - Commit: 58825174
6. KnowledgeGraphService (12 methods) - Commit: 720d39ce
7. ProjectRepository (7 methods) - Commit: fd245dbc

**Plus Learning Services (via delegation)**:
- CrossFeatureKnowledgeService → Delegates to KnowledgeGraphService
- PatternRecognitionService → Part of knowledge graph

**See**: `dev/2025/11/21/sec-rbac-phase1.2-completion-summary.md`

### Phase 1.1 (Database Schema): ✅ SUFFICIENT (70%)

**Migration 4d1e2c3b5f7a applied successfully**:
- 9 resource tables have owner_id columns
- All SEC-RBAC schema deployed in applied migrations
- Knowledge graph tables exist

**See**: `dev/2025/11/22/sec-rbac-phase1.1-completion-report.md`

---

## Your Mission: Endpoint Protection Layer

**Goal**: Connect FastAPI endpoints → service layer with user ownership validation

**Pattern**: Extract user_id from request context, pass to secured service methods

### Endpoint Categories to Secure

Based on Phase 1.2 services, you need to secure endpoints for:

1. **File Endpoints** (`web/routes/files.py` or similar)
   - Upload file
   - Get file
   - List files
   - Delete file

2. **List Endpoints** (`web/routes/lists.py` or similar)
   - Create list
   - Get list
   - Update list
   - Delete list

3. **Todo Endpoints** (`web/routes/todos.py` or similar)
   - Create todo
   - Get todo
   - Update todo
   - Delete todo

4. **Feedback Endpoints** (`web/routes/feedback.py` or similar)
   - Submit feedback
   - Get feedback
   - List feedback

5. **Knowledge Graph Endpoints** (`web/routes/knowledge.py` or similar)
   - Create node
   - Get node
   - Create edge
   - Query graph

6. **Project Endpoints** (`web/routes/projects.py` or similar)
   - Create project
   - Get project
   - Update project
   - Delete project

---

## Phase 1: Infrastructure Discovery (15 min) ⭐⭐⭐

**CRITICAL**: Before implementing, understand the existing infrastructure.

### Task 1.1: Find Endpoint Files

```bash
# Where are FastAPI routes defined?
find web/ -name "*.py" -type f | grep -E "(route|endpoint|api)"
ls -la web/routes/ 2>/dev/null || echo "No routes/ directory"
ls -la web/api/ 2>/dev/null || echo "No api/ directory"

# Check main app structure
cat web/app.py | grep -E "(router|include_router|APIRouter)"
```

**Document**: Where are routes actually defined in this codebase?

### Task 1.2: Find Authentication Pattern

```bash
# How is user context currently extracted?
grep -r "current_user" web/ --include="*.py"
grep -r "get_user" web/ --include="*.py"
grep -r "user_id" web/ --include="*.py" | head -20

# Check for existing auth dependencies
grep -r "Depends" web/ --include="*.py" | grep -i "user"
```

**Document**: How do we currently get user_id in endpoints?

### Task 1.3: Examine Existing Endpoint Pattern

```bash
# Look at a representative endpoint
grep -A 20 "async def.*file" web/ --include="*.py" | head -50
grep -A 20 "@router" web/ --include="*.py" | head -50
```

**Expected patterns**:
- `async def endpoint(user_id: UUID, ...)`
- `async def endpoint(current_user: User = Depends(get_current_user), ...)`
- `async def endpoint(request: Request, ...)`

**Document**: What's the current pattern?

### Task 1.4: Check Service Layer Signatures

Verify Phase 1.2 service methods accept owner_id/user_id parameters:

```bash
# FileRepository
grep -A 5 "async def get_file" services/repositories/file_repository.py

# UniversalListRepository
grep -A 5 "async def get_list" services/repositories/universal_list_repository.py

# KnowledgeGraphService
grep -A 5 "async def get_node" services/knowledge_graph_service.py
```

**Verify**: All service methods have `owner_id: Optional[UUID] = None` or `user_id: Optional[UUID] = None`

---

## Phase 2: Create STOP Report (5 min) ⚡

**MANDATORY STOP CONDITION**: Before implementing, report your findings.

**Create file**: `dev/2025/11/22/sec-rbac-phase1.3-infrastructure-discovery.md`

**Template**:

```markdown
# SEC-RBAC Phase 1.3: Infrastructure Discovery Report

**Date**: November 22, 2025
**Agent**: Claude Code

## Endpoint File Locations

[Where are routes defined? List files found]

## Current Authentication Pattern

[How is user_id currently extracted? Show code examples]

## Service Layer Verification

- FileRepository.get_file: [signature]
- UniversalListRepository.get_list: [signature]
- KnowledgeGraphService.get_node: [signature]
- (etc.)

## Recommended Implementation Pattern

[Based on discovery, what pattern should we use?]

### Option A: Dependency Injection
```python
@router.get("/files/{file_id}")
async def get_file(
    file_id: UUID,
    current_user: User = Depends(get_current_user),
    file_repo: FileRepository = Depends(get_file_repository)
):
    return await file_repo.get_file(file_id, owner_id=current_user.id)
```

### Option B: Request Context
```python
@router.get("/files/{file_id}")
async def get_file(file_id: UUID, request: Request):
    user_id = request.state.user_id
    file_repo = FileRepository(request.state.db)
    return await file_repo.get_file(file_id, owner_id=user_id)
```

### Option C: [Whatever pattern you discover]

## Questions for Lead Developer

- [Any unclear patterns or decisions needed]

## Ready to Implement?

- [ ] Found all endpoint files
- [ ] Identified auth pattern
- [ ] Verified service signatures
- [ ] Chosen implementation pattern

**STOP HERE - Report to Lead Developer before proceeding**
```

**Action**: Create this file, then **STOP and wait for Lead Developer approval** before implementing.

---

## Phase 3: Implementation (ONLY AFTER APPROVAL)

**DO NOT START THIS PHASE without Lead Developer approval of your discovery report.**

### Task 3.1: Implement File Endpoints

**File**: [wherever you found file endpoints in Phase 1]

**Pattern**: [pattern approved by Lead Developer]

**Example** (adjust based on actual pattern):

```python
@router.get("/files/{file_id}")
async def get_file(
    file_id: UUID,
    current_user: User = Depends(get_current_user),
    file_repo: FileRepository = Depends(get_file_repository)
):
    """Get file - validates ownership"""
    file = await file_repo.get_file(file_id, owner_id=current_user.id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file
```

**Endpoints to secure**:
- GET /files/{file_id}
- GET /files (list)
- POST /files (upload)
- DELETE /files/{file_id}

### Task 3.2: Implement List Endpoints

**File**: [wherever you found list endpoints]

**Pattern**: [same as approved pattern]

**Endpoints to secure**:
- GET /lists/{list_id}
- GET /lists
- POST /lists
- PUT /lists/{list_id}
- DELETE /lists/{list_id}

### Task 3.3: Implement Todo Endpoints

**File**: [wherever you found todo endpoints]

**Endpoints to secure**:
- GET /todos/{todo_id}
- GET /todos
- POST /todos
- PUT /todos/{todo_id}
- DELETE /todos/{todo_id}

### Task 3.4: Implement Knowledge Graph Endpoints

**File**: [wherever you found knowledge endpoints]

**Endpoints to secure**:
- POST /knowledge/nodes
- GET /knowledge/nodes/{node_id}
- POST /knowledge/edges
- GET /knowledge/query

### Task 3.5: Implement Project Endpoints

**File**: [wherever you found project endpoints]

**Endpoints to secure**:
- GET /projects/{project_id}
- GET /projects
- POST /projects
- PUT /projects/{project_id}
- DELETE /projects/{project_id}

### Task 3.6: Implement Feedback Endpoints

**File**: [wherever you found feedback endpoints]

**Endpoints to secure**:
- POST /feedback
- GET /feedback/{feedback_id}
- GET /feedback

---

## Phase 4: Testing (After Implementation)

### Task 4.1: Manual Endpoint Testing

**Create test script**: `tests/manual/manual_sec_rbac_endpoint_test.py`

```python
"""Manual test for SEC-RBAC Phase 1.3 endpoint protection"""
import httpx
import asyncio
from uuid import UUID

async def test_cross_user_access():
    """Verify users cannot access each other's resources"""

    # User 1 creates a file
    async with httpx.AsyncClient() as client:
        # Authenticate as user1
        response = await client.post(
            "http://localhost:8001/api/auth/login",
            json={"username": "user1", "password": "test"}
        )
        user1_token = response.json()["access_token"]

        # Create file as user1
        response = await client.post(
            "http://localhost:8001/api/files",
            headers={"Authorization": f"Bearer {user1_token}"},
            files={"file": ("test.txt", b"content")}
        )
        file_id = response.json()["id"]

        # Authenticate as user2
        response = await client.post(
            "http://localhost:8001/api/auth/login",
            json={"username": "user2", "password": "test"}
        )
        user2_token = response.json()["access_token"]

        # Try to access user1's file as user2
        response = await client.get(
            f"http://localhost:8001/api/files/{file_id}",
            headers={"Authorization": f"Bearer {user2_token}"}
        )

        # Should return 404 (not found) or 403 (forbidden)
        assert response.status_code in [403, 404], \
            f"Expected 403/404, got {response.status_code}"

        print("✅ Cross-user access blocked successfully")

if __name__ == "__main__":
    asyncio.run(test_cross_user_access())
```

### Task 4.2: Run Integration Tests

```bash
# Run existing integration tests to ensure no regressions
pytest tests/integration/ -xvs

# Should all still pass
```

---

## Phase 5: Documentation (After Testing)

**Create file**: `dev/2025/11/22/sec-rbac-phase1.3-completion-report.md`

**Template**:

```markdown
# SEC-RBAC Phase 1.3: Endpoint Protection - COMPLETION REPORT

**Date**: November 22, 2025
**Agent**: Claude Code
**Status**: ✅ COMPLETE

## Summary

Successfully implemented owner_id validation across [X] FastAPI endpoints, completing the endpoint protection layer for SEC-RBAC Phase 1.

## Endpoints Secured

### File Endpoints ([X] endpoints)
- GET /files/{file_id} ✅
- GET /files ✅
- POST /files ✅
- DELETE /files/{file_id} ✅

[Continue for all categories]

## Implementation Pattern

[Document the pattern you used]

Example:
```python
@router.get("/files/{file_id}")
async def get_file(
    file_id: UUID,
    current_user: User = Depends(get_current_user),
    file_repo: FileRepository = Depends(get_file_repository)
):
    """Get file - validates ownership"""
    return await file_repo.get_file(file_id, owner_id=current_user.id)
```

## Testing Evidence

### Manual Testing
- Cross-user access blocked: ✅
- Same-user access allowed: ✅
- Error handling correct: ✅

### Integration Tests
- All tests passing: [X/X] ✅

## Commits

1. [hash] - Secure file endpoints (4 endpoints)
2. [hash] - Secure list endpoints (5 endpoints)
3. [hash] - Secure todo endpoints (5 endpoints)
4. [hash] - Secure knowledge graph endpoints (4 endpoints)
5. [hash] - Secure project endpoints (5 endpoints)
6. [hash] - Secure feedback endpoints (3 endpoints)

## Metrics

- **Endpoints Secured**: [X] total
- **Files Modified**: [X]
- **Lines Added**: ~[X]
- **Tests Passing**: [X/X]

## Phase 1 SEC-RBAC: COMPLETE ✅

All three phases complete:

1. ✅ Phase 1.1 - Database Schema (owner_id columns)
2. ✅ Phase 1.2 - Service Layer (52 methods secured)
3. ✅ Phase 1.3 - Endpoint Protection ([X] endpoints secured)

**Next**: Phase 2 - Role-Based Access Control (roles & permissions)

---

_Report created by: Claude Code_
_Next Phase: SEC-RBAC Phase 2 - RBAC Implementation_
```

---

## Success Criteria

**Phase 1.3 is complete when**:

- [ ] Infrastructure discovery report created and approved
- [ ] All file endpoints secured
- [ ] All list endpoints secured
- [ ] All todo endpoints secured
- [ ] All knowledge graph endpoints secured
- [ ] All project endpoints secured
- [ ] All feedback endpoints secured
- [ ] Cross-user access test passes
- [ ] Integration tests pass (no regressions)
- [ ] Completion report created with evidence

---

## What NOT to Do

**DO NOT**:
- Skip infrastructure discovery (Phase 1 is mandatory)
- Implement before getting approval on pattern
- Guess at endpoint locations (use grep/find to verify)
- Assume auth pattern (discover what exists)
- Skip testing (manual + integration required)
- Create new auth infrastructure (use what exists)

**DO**:
- Follow phases in order (1 → 2 → 3 → 4 → 5)
- STOP after Phase 1 discovery report
- Wait for Lead Developer approval
- Use existing patterns consistently
- Provide evidence for all claims
- Test cross-user access blocking

---

## Timeline Estimate

- Phase 1 (Discovery): 15 minutes
- Phase 2 (STOP report): 5 minutes
- **WAIT FOR APPROVAL**
- Phase 3 (Implementation): 30-40 minutes
- Phase 4 (Testing): 15 minutes
- Phase 5 (Documentation): 10 minutes

**Total**: ~80 minutes (including approval wait)

---

**Remember**: Discovery first, implementation second. The existing infrastructure will guide the pattern. Don't invent - discover and apply.

Good luck! 🚀

---

_Prompt created by: Lead Developer (Cursor)_
_Date: November 22, 2025, 7:04 AM_
_Session: SEC-RBAC Phase 1.3 Endpoint Protection_
_Authority: PM approved Phase 1.3 start (7:01 AM)_
