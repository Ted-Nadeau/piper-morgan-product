# Issue #7 Investigation: Create New Todo Button Fails

**Date**: November 23, 2025
**Investigator**: Code Agent
**Duration**: 8 minutes
**Status**: Complete

---

## Summary

The "Create New Todo" button frontend UI is fully built and functional, but the API call to create the todo is commented out (TODO). The button opens a dialog and collects data, but never sends it to the backend because the backend POST /api/v1/todos endpoint does not exist. This is identical to Issue #6, following the same Option B pattern.

**Type B: Missing Piece** - requires implementing the backend API endpoint and uncommenting the JavaScript.

---

## Frontend Analysis

**Button Location**: `templates/todos.html:44`

```html
<button class="create-resource-btn" onclick="createNewTodo()">
  + Create New Todo
</button>
```

**JavaScript Handler**: `templates/todos.html:171-211`

**Function Name**: `createNewTodo()`

**Status**: ✅ Exists and wired correctly

### Function Details

The `createNewTodo()` function:
1. ✅ Opens a Dialog (from dialog.js)
2. ✅ Collects inputs: todo text, due date
3. ✅ Validates required fields
4. ✅ Displays Toast notifications
5. ✅ Sharing modal fully implemented (lines 245-369)
6. ❌ API call is commented out (lines 194-199)

### Code Snippet

```javascript
async function createNewTodo() {
  Dialog.show({
    title: 'Create New Todo',
    content: `
      <div class="form-group">
        <label>Todo Text</label>
        <input type="text" id="new-todo-text" placeholder="What do you need to do?">
      </div>
      <div class="form-group">
        <label>Due Date (optional)</label>
        <input type="date" id="new-todo-due-date">
      </div>
    `,
    onConfirm: async () => {
      const text = document.getElementById('new-todo-text').value;
      const dueDate = document.getElementById('new-todo-due-date').value;

      if (!text) {
        Toast.error('Todo text is required');
        return false;
      }

      try {
        // TODO: Call API to create todo
        // const response = await fetch('/api/v1/todos', {
        //   method: 'POST',
        //   headers: {'Content-Type': 'application/json'},
        //   body: JSON.stringify({ text, due_date: dueDate })
        // });

        Toast.success('Todo created successfully'); // Shows even though no API call!
        await loadTodos();
        return true;
      } catch (error) {
        console.error('Error creating todo:', error);
        Toast.error('Failed to create todo');
        return false;
      }
    }
  });
}
```

**Problem**: Lines 194-199 show the API call is **commented out** with a TODO. The function always shows "success" even though no API call is made.

---

## Backend Analysis

**Route**: web/app.py:1040-1047

```python
@app.get("/todos", response_class=HTMLResponse)
async def todos_ui(request: Request):
    """Todos management page with permission-aware UI (Issue #376)"""
    user_context = _extract_user_context(request)
    todos_data = []
    return templates.TemplateResponse(
        "todos.html", {"request": request, "user": user_context, "todos": todos_data}
    )
```

**Status**: ❌ GET route exists, but NO POST route exists

### What's Missing

- **POST /api/v1/todos** - Does not exist in web/app.py
- **GET /api/v1/todos/{resourceId}/shares** - Does not exist (called from sharing modal line 249)
- **POST /api/v1/todos/{resourceId}/share** - Does not exist (called from sharing modal line 328)
- **DELETE /api/v1/todos/{resourceId}/share/{userId}** - Does not exist (called from sharing modal line 354)

### Backend Service

- ❌ No TodoRepository visible in services/
- ❌ No create_todo method
- ❌ No shared_with JSONB handling for todos

---

## Git History

**Last Modified**: `cf552824` - November 23, 2025, 11:06 AM

**Commit Message**: `feat(#376): Frontend RBAC Option B - Permission-aware resource pages with sharing`

**Author**: Claude (Code Agent)

**Context**: This was built TODAY as part of Option B work. The UI pages were created with placeholder/stub implementations, and the API calls were intentionally left as TODO.

```
cf552824 feat(#376): Frontend RBAC Option B
8c3b079c docs: Complete Phase Z verification
ce9aa5e9 docs: Rename session log
8c3b079c docs: Complete Phase Z verification
cf38ccf7 fix(SEC-RBAC Phase 1): Resolve domain/ORM model mismatches
```

---

## Root Cause

**Classification**: **Type B: Missing Piece**

**Exact Issue**:
The `createNewTodo()` function in templates/todos.html has the API call commented out (lines 194-199). Additionally, the backend does not have POST endpoint for `/api/v1/todos` or the sharing endpoints (GET/POST/DELETE for shares).

This is an identical pattern to Issue #6 - appears to be a conscious design decision from Option B implementation: build the UI shell with placeholder functions and TODO comments for API integration. The function structure is correct, it just needs:
1. Uncomment the API call in the JavaScript
2. Implement the POST `/api/v1/todos` endpoint in web/app.py
3. Implement TodoRepository.create_todo() in services/
4. Implement sharing endpoints for todos (GET/POST/DELETE)

**Why This Happened**:
Option B was designed as a "rudimentary resource management pages" implementation. The focus was on:
- ✅ UI pages with permission-aware buttons
- ✅ Permission checking logic
- ✅ Sharing modal structure
- ⏳ API integration (intentionally deferred)

The 75% pattern: Frontend UI 100% complete, backend API 0% complete.

---

## Fix Estimate

**Effort**: 45-60 minutes

**What Needs to Happen**:

1. **Backend (30-40 minutes)**:
   - Implement `POST /api/v1/todos` endpoint in web/app.py
   - Create TodoRepository.create_todo() method
   - Handle RBAC checks (owner_id, shared_with initialization)
   - Implement sharing endpoints: GET/POST/DELETE for shares
   - Return created todo JSON

2. **Frontend (10-15 minutes)**:
   - Uncomment the API call in createNewTodo() (lines 194-199)
   - Wire up the token/auth headers
   - Handle response properly

3. **Testing (5 minutes)**:
   - Click button, create todo, verify appears in list

**Complexity**: Medium (requires backend API implementation, identical to Issue #6)

---

## Recommendation

**Action**: **Fix This Issue** (Type B - Medium effort, high priority)

**Reasoning**:
1. The issue is clearly defined and well-understood
2. Frontend is 100% complete, just needs API wiring
3. Only missing piece is POST endpoint which is standard REST
4. This is blocking core functionality (can't create todos)
5. Effort is reasonable (45-60 minutes)
6. Option B explicitly intended this to be incomplete, needing completion today
7. **PATTERN DISCOVERED**: Identical pattern to Issue #6 - suggests Issue #14 may follow same pattern too

**If Proceeding with Fix**:
1. Create POST /api/v1/todos endpoint (copy pattern from Issue #6 fix)
2. Implement TodoRepository.create_todo()
3. Implement sharing endpoints for todos
4. Uncomment and test the JavaScript
5. Test full flow: Button → Dialog → API → Todo appears

**Suggested Priority**: FIX NOW (blocks basic functionality, same as Issue #6)

**Efficiency Note**: Once Issue #6 is fixed (if approved), the same API pattern can be applied to Issue #7, reducing implementation time.

---

## Evidence

**Frontend Button**: templates/todos.html:44
**Function Code**: templates/todos.html:171-211
**Commented API Call**: templates/todos.html:194-199
**GET Route Exists**: web/app.py:1040-1047
**Sharing Modal**: templates/todos.html:245-369
**No POST Route**: Confirmed via file inspection - no @app.post routes for /api/v1/todos
**No Sharing Endpoints**: Confirmed - sharing modal calls non-existent endpoints

---

## Next Steps

This issue is identical to Issue #6. Once #6 is fixed, apply the same solution to #7. Both should follow the same implementation pattern.

Also: This pattern suggests Investigation Issue #14 (Login/Logout) may also have similar gaps.
