# Gameplan: #474 MUX-TECH-LISTS - Enable Full List Management

**Issue**: #474
**Epic**: #629 MUX-LISTS
**Sprint**: L1
**Created**: 2026-01-22

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Database: PostgreSQL on 5433 (confirmed)
- [x] Testing framework: pytest (confirmed)
- [x] Existing endpoints: `/api/v1/lists` CRUD for Lists (confirmed)
- [x] Missing endpoints: `/api/v1/lists/{id}/items` CRUD for Items

**My understanding of the task**:
- Repository layer is complete (`UniversalListItemRepository` has all CRUD methods)
- Need to create API routes to expose item operations
- Need to create/update UI for item management
- Need to fix "Coming soon" edit list functionality

### Part A.2: Work Characteristics Assessment

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [x] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment**:
- [x] **SKIP WORKTREE** - Single agent, tightly coupled API+UI work

### Part B: PM Verification Required

**What actually exists in the filesystem?**
```
✅ web/api/routes/lists.py - List CRUD only, no item endpoints
✅ services/repositories/universal_list_repository.py - Has UniversalListItemRepository
✅ services/domain/primitives.py - Item model (lines 19-68)
✅ services/database/models.py - ItemDB (line 1447)
✅ templates/lists.html - Shows "Coming soon" for edit (line 266)
```

**Actual task needed?**
- [x] Add to existing application (extend lists.py with item endpoints)
- [x] Fix broken functionality (edit list shows "Coming soon")

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding is correct, gameplan appropriate

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 474
   ```
   ✅ Issue exists, updated with complete structure

2. **Codebase Investigation** (completed in audit)
   - Repository: `UniversalListItemRepository` has all needed methods
   - Routes: `lists.py` needs item endpoints added
   - UI: `lists.html` needs item management + edit fix

3. **Update GitHub Issue**
   ```bash
   gh issue edit 474 --body "## Status: Implementation Started..."
   ```

---

## Phase 0.5: Frontend-Backend Contract Verification

### Endpoint Design

| Endpoint | Route Path | Mount Prefix | Full Path |
|----------|------------|--------------|-----------|
| Add item | `POST /{list_id}/items` | `/api/v1/lists` | `/api/v1/lists/{list_id}/items` |
| Get items | `GET /{list_id}/items` | `/api/v1/lists` | `/api/v1/lists/{list_id}/items` |
| Edit item | `PUT /{list_id}/items/{item_id}` | `/api/v1/lists` | `/api/v1/lists/{list_id}/items/{item_id}` |
| Delete item | `DELETE /{list_id}/items/{item_id}` | `/api/v1/lists` | `/api/v1/lists/{list_id}/items/{item_id}` |

### Verification Commands (after Phase 1)
```bash
curl -s http://localhost:8001/api/v1/lists/{list_id}/items
# Must NOT return {"detail":"Not Found"}
```

---

## Phase 1: Backend - Item API Endpoints

### 1.1 Add Item Endpoints to lists.py

**File**: `web/api/routes/lists.py`

Add after existing List CRUD endpoints:

```python
# === Item Management Endpoints ===

class CreateItemRequest(BaseModel):
    """Request model for creating an item in a list"""
    text: str

class UpdateItemRequest(BaseModel):
    """Request model for updating an item"""
    text: str

@router.post("/{list_id}/items")
async def add_item_to_list(
    list_id: str,
    request: CreateItemRequest,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
    item_repo=Depends(get_item_repository),  # Need to add dependency
) -> dict:
    """Add item to list with ownership validation"""
    # Verify list ownership
    # Create item via item_repo.create_item()
    # Return item data

@router.get("/{list_id}/items")
async def get_items_in_list(...) -> dict:
    """Get all items in a list"""

@router.put("/{list_id}/items/{item_id}")
async def update_item(...) -> dict:
    """Update item text"""

@router.delete("/{list_id}/items/{item_id}")
async def delete_item(...) -> dict:
    """Delete item from list"""
```

### 1.2 Add Dependency Injection

**File**: `web/api/dependencies.py`

```python
def get_item_repository():
    """Dependency for item repository"""
    from services.repositories.universal_list_repository import UniversalListItemRepository
    return UniversalListItemRepository(get_db_session())
```

### 1.3 Test Endpoints

```bash
# Start server
python main.py

# Test add item
curl -X POST http://localhost:8001/api/v1/lists/{list_id}/items \
  -H "Content-Type: application/json" \
  -d '{"text": "Test item"}' \
  --cookie "session=..."

# Test get items
curl http://localhost:8001/api/v1/lists/{list_id}/items \
  --cookie "session=..."
```

### Evidence Required
- [ ] All 4 endpoints return 200/201 (not 404)
- [ ] curl output for each endpoint
- [ ] Unit tests pass

---

## Phase 2: Backend - Unit Tests

### 2.1 Create Test File

**File**: `tests/unit/web/api/routes/test_lists_items.py`

```python
"""Unit tests for list item endpoints (Issue #474)"""

class TestListItemEndpoints:
    @pytest.mark.asyncio
    async def test_add_item_to_list(self):
        """POST /lists/{id}/items creates item"""

    @pytest.mark.asyncio
    async def test_get_items_in_list(self):
        """GET /lists/{id}/items returns items"""

    @pytest.mark.asyncio
    async def test_update_item(self):
        """PUT /lists/{id}/items/{item_id} updates item"""

    @pytest.mark.asyncio
    async def test_delete_item(self):
        """DELETE /lists/{id}/items/{item_id} removes item"""

    @pytest.mark.asyncio
    async def test_item_ownership_validation(self):
        """Items only accessible by list owner"""
```

### Evidence Required
- [ ] `pytest tests/unit/web/api/routes/test_lists_items.py -v` all pass
- [ ] Test output in session log

---

## Phase 3: Frontend - Item Management UI

### 3.1 Update lists.html for Item Display

When clicking a list, show its items with add/edit/delete controls.

**Approved Pattern**: Inline expansion (PM approved 2026-01-22)
- Click list row → expands accordion-style to show items below
- Matches existing Piper patterns (settings panels)
- No new routes needed (pure JS)
- Future upgrade path to detail page if needed

### 3.2 Add Item Input

```javascript
// Add item form at top of expanded list
<div class="add-item-form">
  <input type="text" placeholder="Add an item..." id="new-item-${listId}">
  <button onclick="addItem('${listId}')">Add</button>
</div>
```

### 3.3 Fix Edit List

Replace "Coming soon" at line 266:

```javascript
function editList(listId) {
  Dialog.show({
    mode: 'form',
    title: 'Edit List',
    confirmText: 'Save',
    content: `
      <div class="form-group">
        <label>List Name</label>
        <input type="text" id="edit-list-name" value="${currentList.name}">
      </div>
      <div class="form-group">
        <label>Description</label>
        <textarea id="edit-list-description">${currentList.description || ''}</textarea>
      </div>
    `,
    onConfirm: async () => {
      // Call PUT /api/v1/lists/{listId}
    }
  });
}
```

### Evidence Required
- [ ] Screenshot: Add item UI
- [ ] Screenshot: Edit item UI
- [ ] Screenshot: Delete item with confirmation
- [ ] Screenshot: Edit list dialog (not "Coming soon")

---

## Phase 4: Integration Testing

### 4.1 E2E Flow Test

Manual verification:
1. Create a list
2. Add 3 items
3. Edit one item
4. Delete one item
5. Edit list name
6. Verify all persisted after refresh

### Evidence Required
- [ ] Screenshot sequence or screen recording
- [ ] Database query showing items exist

---

## Phase Z: Final Bookending & Handoff

### GitHub Final Update
```bash
gh issue edit 474 --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] All API endpoints working
- [x] All UI functionality working
- [x] Tests passing: [output]
- [x] No regressions

### Ready for PM Review
"
```

### Documentation Updates
- [ ] Update NAVIGATION.md if new patterns
- [ ] No ADR needed (extends existing pattern)

---

## Completion Matrix

| Phase | Criterion | Evidence | Status |
|-------|-----------|----------|--------|
| 1 | POST /items works | curl output | ⬜ |
| 1 | GET /items works | curl output | ⬜ |
| 1 | PUT /items works | curl output | ⬜ |
| 1 | DELETE /items works | curl output | ⬜ |
| 2 | Unit tests pass | pytest output | ⬜ |
| 3 | Add item UI | Screenshot | ⬜ |
| 3 | Edit item UI | Screenshot | ⬜ |
| 3 | Delete item UI | Screenshot | ⬜ |
| 3 | Edit list UI | Screenshot | ⬜ |
| 4 | E2E flow works | Screenshot | ⬜ |

---

## STOP Conditions

- If `UniversalListItemRepository` methods have different signatures than expected
- If ownership validation pattern differs from list CRUD
- If session/auth handling blocks API calls
- If frontend JS patterns differ from documented approach

---

## Effort Estimate

| Phase | Estimate |
|-------|----------|
| Phase 1: API endpoints | Medium |
| Phase 2: Unit tests | Small |
| Phase 3: Frontend UI | Medium |
| Phase 4: Integration | Small |
| **Total** | **Medium** |
