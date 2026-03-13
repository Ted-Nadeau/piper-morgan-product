# Gameplan: Issue #468 - API Contract Mismatch Fix
**Version**: 1.0
**Created**: 2025-12-04 17:40
**Methodology**: Strict TDD with Subagent Separation

---

## Executive Summary

All three entity create endpoints (Lists, Todos, Projects) expect query parameters but frontends send JSON body. This causes 422 errors surfacing as "Unknown error" to users.

**Approach**: TDD with subagent separation to avoid build/test incentive conflicts.

---

## Phase -1: Infrastructure Verification

### Verified ✅
- [x] `lists` table exists in PostgreSQL
- [x] `ListDB` model maps to `lists` table
- [x] `UniversalListRepository` has `create_list`, `get_lists_by_owner` methods
- [x] Frontend sends JSON body (verified in templates)
- [x] Backend expects query params (verified in route signatures)
- [x] Server is running and healthy

### Worktree Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [x] Multiple agents will work in parallel (Test Agent + Fix Agent)
- [x] Task duration >30 minutes
- [ ] Multi-component work
- [ ] Exploratory/risky changes

Worktrees ADD overhead when:
- [ ] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits

**Assessment**: SKIP WORKTREE
Rationale: While parallel agents involved, the test and fix are tightly coupled - test must run against fix. Sequential execution is cleaner.

---

## Phase 0: Bookending

### GitHub Issue
- Created: #468 - P0: API Contract Mismatch
- Labels: bug, api, tdd, systematic-fix

### Scope Definition

**In Scope**:
- E2E tests for Lists, Todos, Projects create workflows
- Backend Pydantic request models for JSON body
- Verification on dev and alpha laptops

**Out of Scope**:
- CSS/styling issues (#462 already addressed)
- Toast API mismatch (#466 separate issue)
- Other endpoints (GET, PUT, DELETE work correctly)

### Files to Modify

| File | Change |
|------|--------|
| `tests/integration/test_create_entity_e2e.py` | NEW - E2E tests |
| `web/api/routes/lists.py` | Add Pydantic request model |
| `web/api/routes/todos.py` | Add Pydantic request model |
| `web/api/routes/projects.py` | Add Pydantic request model |

---

## Phase 0.5: Frontend-Backend Contract Definition

### Expected Contract (Standard REST)

**Request**:
```http
POST /api/v1/lists HTTP/1.1
Content-Type: application/json
Cookie: auth_token=<jwt>

{
  "name": "My List",
  "description": "Optional description"
}
```

**Response (Success)**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "uuid",
  "name": "My List",
  "description": "Optional description",
  "owner_id": "user-uuid",
  "created_at": "2025-12-04T17:00:00Z"
}
```

**Response (Validation Error)**:
```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Phase 1: E2E Tests (RED) - Test Subagent

### Objective
Write E2E tests that:
1. Authenticate as test user
2. Call POST with JSON body (same as frontend)
3. Assert 200 response
4. Assert entity created with correct data
5. Cleanup

### Test File Structure

```python
# tests/integration/test_create_entity_e2e.py
"""
E2E Tests for Entity Create Workflows (Issue #468)

These tests verify the frontend→backend contract for create operations.
They use the same JSON body format as the frontend templates.

TDD: These tests are written FIRST and MUST FAIL against current code.
"""

import pytest
from httpx import AsyncClient

@pytest.mark.integration
@pytest.mark.asyncio
class TestListCreateE2E:
    """E2E tests for POST /api/v1/lists with JSON body"""

    async def test_create_list_with_json_body(self, authenticated_client):
        """Frontend sends JSON body - backend must accept it"""
        response = await authenticated_client.post(
            "/api/v1/lists",
            json={"name": "Test List", "description": "Test Description"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test List"
        assert "id" in data

    async def test_create_list_name_required(self, authenticated_client):
        """Empty name should return 422 with clear error"""
        response = await authenticated_client.post(
            "/api/v1/lists",
            json={"description": "No name provided"}
        )
        assert response.status_code == 422
        # Or 400 if we prefer - but must be clear error

    async def test_create_list_appears_in_list(self, authenticated_client):
        """Created list must appear in GET /api/v1/lists"""
        # Create
        create_resp = await authenticated_client.post(
            "/api/v1/lists",
            json={"name": "Visibility Test"}
        )
        assert create_resp.status_code == 200
        list_id = create_resp.json()["id"]

        # Verify in list
        list_resp = await authenticated_client.get("/api/v1/lists")
        assert list_resp.status_code == 200
        lists = list_resp.json()["lists"]
        assert any(l["id"] == list_id for l in lists)

# Similar classes for TestTodoCreateE2E, TestProjectCreateE2E
```

### Expected Result
All tests MUST FAIL with current code (proving the bug exists).

### Stop Condition
If tests pass → STOP. Either:
1. Bug was already fixed (verify manually)
2. Test is wrong (not using JSON body)

---

## Phase 2: Backend Fix (GREEN) - Fix Subagent

### Objective
Modify endpoints to accept JSON body via Pydantic models.

### Implementation Pattern

**Before** (Query Params):
```python
@router.post("")
async def create_list(
    name: str,
    description: Optional[str] = None,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
```

**After** (JSON Body):
```python
class CreateListRequest(BaseModel):
    """Request model for creating a list"""
    name: str
    description: Optional[str] = None

@router.post("")
async def create_list(
    request: CreateListRequest,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    # Use request.name, request.description instead
```

### Files to Modify

1. **web/api/routes/lists.py**
   - Add `CreateListRequest` Pydantic model
   - Modify `create_list()` signature
   - Update function body to use `request.name`, `request.description`

2. **web/api/routes/todos.py**
   - Add `CreateTodoRequest` Pydantic model
   - Modify `create_todo()` signature
   - Update function body

3. **web/api/routes/projects.py**
   - Add `CreateProjectRequest` Pydantic model
   - Modify `create_project()` signature
   - Update function body

### Expected Result
E2E tests from Phase 1 now pass.

---

## Phase 3: Verification (REFACTOR)

### Automated Verification
```bash
# Run E2E tests
python -m pytest tests/integration/test_create_entity_e2e.py -xvs

# Run all integration tests (no regressions)
python -m pytest tests/integration/ -v

# Run unit tests (no regressions)
python -m pytest tests/unit/ -v
```

### Manual Verification - Dev Laptop

1. Start server: `python main.py`
2. Login as test user
3. Navigate to Lists → Click "+ Create New List"
4. Fill in name and description
5. Click "Create"
6. **Expected**: List appears in list, success toast

Repeat for Todos and Projects.

### Manual Verification - Alpha Laptop

Same steps as dev laptop.

---

## Completion Matrix

| Phase | Task | Status | Evidence |
|-------|------|--------|----------|
| **Phase 1: E2E Tests (RED)** ||||
| | Create test file | [ ] | File exists |
| | TestListCreateE2E.test_create_list_with_json_body | [ ] | Test fails |
| | TestListCreateE2E.test_create_list_appears_in_list | [ ] | Test fails |
| | TestTodoCreateE2E tests | [ ] | Tests fail |
| | TestProjectCreateE2E tests | [ ] | Tests fail |
| **Phase 2: Backend Fix (GREEN)** ||||
| | Add CreateListRequest model | [ ] | grep shows class |
| | Modify create_list() | [ ] | Signature updated |
| | Add CreateTodoRequest model | [ ] | grep shows class |
| | Modify create_todo() | [ ] | Signature updated |
| | Add CreateProjectRequest model | [ ] | grep shows class |
| | Modify create_project() | [ ] | Signature updated |
| | All E2E tests pass | [ ] | pytest output |
| **Phase 3: Verification** ||||
| | Integration tests pass | [ ] | pytest output |
| | Unit tests pass | [ ] | pytest output |
| | Manual: Create list works | [ ] | PM visual |
| | Manual: Create todo works | [ ] | PM visual |
| | Manual: Create project works | [ ] | PM visual |
| | Alpha laptop verified | [ ] | PM visual |

---

## Subagent Deployment

### Subagent 1: Test Writer (Phase 1)
**Role**: Write E2E tests ONLY. Do not fix code.
**Objective**: Create failing tests that prove the bug exists.
**Deliverable**: `tests/integration/test_create_entity_e2e.py`
**Stop Condition**: If tests pass, STOP and report (bug may be fixed).

### Subagent 2: Backend Fixer (Phase 2)
**Role**: Fix backend ONLY after tests fail.
**Objective**: Make tests pass by adding Pydantic request models.
**Deliverable**: Modified route files.
**Stop Condition**: Tests pass.

### Separation Rationale
TDD discipline requires separation of concerns:
- Test writer has incentive to write thorough tests
- Fixer has incentive to make tests pass correctly
- Neither has incentive to cheat (skip tests, weaken assertions)

---

## Stop Conditions

1. **E2E tests pass before fix** → STOP, verify bug status manually
2. **Existing tests fail after fix** → STOP, regression introduced
3. **Manual verification fails** → STOP, additional issues exist
4. **Any 500 errors in logs** → STOP, server error

---

## Risk Assessment

**Low Risk**:
- Pydantic models are additive
- Function body changes are minimal (request.name vs name)
- FastAPI handles JSON parsing automatically

**Medium Risk**:
- Existing tests may call endpoints with query params
- May need to update test fixtures

**Mitigation**:
- Run full test suite before and after
- Keep query param support temporarily if needed (not recommended)

---

## Post-Fix Follow-Up

1. Update API documentation (if exists)
2. Consider adding OpenAPI schema validation
3. Review other POST endpoints for same pattern
4. Add pre-commit hook to enforce Pydantic models for POST

---

*Gameplan follows v9.2 template with TDD emphasis per PM direction*
