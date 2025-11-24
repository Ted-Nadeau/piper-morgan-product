# Code Agent Prompt: Frontend RBAC Option B - Resource Pages

**Date**: November 23, 2025, 10:15 AM
**From**: Lead Developer (PM)
**To**: Code Agent
**Priority**: P0 (Alpha blocking - Michelle arrives tomorrow)
**Type**: Implementation Task
**Estimated Duration**: 6-7 hours

---

## Mission

Build rudimentary resource management pages (Lists, Todos, Projects) with permission-aware UI using existing Jinja2 + vanilla JavaScript patterns. Enable sharing functionality and prevent confusing 403 errors.

**Architecture**: Jinja2 server-side rendering + Vanilla JavaScript (proven in Issues #307, #310)

**No frameworks needed**: Follow existing patterns from navigation (#307) and quick wins (#310)

---

## Context You Have

### From Issue #307 (Navigation & User Context)
- ✅ User context system working: `window.currentUser` with `username` and `user_id`
- ✅ `_extract_user_context()` function in `web/app.py` (line 136)
- ✅ All 9 templates inject user context in `<script>` tags
- ✅ Pattern proven and working

### From Investigation (This Morning)
- ❌ Lists/Todos/Projects pages don't exist yet (you're building from scratch)
- ⚠️ Missing `is_admin` flag in user context (Phase 1 fix)
- ✅ Utility modules available: `dialog.js`, `toast.js`, `loading.js`
- ✅ Design system in place: CSS spacing, colors, components

### From SEC-RBAC Backend (Issue #357)
- ✅ Backend RBAC complete and enforced
- ✅ Sharing endpoints exist: `/api/v1/lists/{id}/share` (and similar for todos/projects)
- ✅ Permission model: Owner, Admin, Editor (can edit), Viewer (read-only)
- ✅ `shared_with` JSONB column on lists/todos/projects tables

---

## Phase-by-Phase Execution

### Phase 1: Extend User Context (15 minutes)

**Objective**: Add `is_admin` flag to existing user context

**File to Edit**: `web/app.py`

**Task 1.1**: Update `_extract_user_context()` function (line 136)

**Current code**:
```python
def _extract_user_context(request: Request) -> dict:
    user_id = getattr(request.state, 'user_id', 'user')
    username = user_id
    user_claims = getattr(request.state, 'user_claims', None)
    if user_claims and hasattr(user_claims, 'username'):
        username = user_claims.username
    elif user_claims and isinstance(user_claims, dict) and 'username' in user_claims:
        username = user_claims['username']

    return {
        'user_id': user_id,
        'username': username
    }
```

**Add this logic** before the return statement:
```python
    # Extract is_admin flag from user claims
    is_admin = False
    if user_claims:
        is_admin = getattr(user_claims, 'is_admin', False) or \
                   (isinstance(user_claims, dict) and user_claims.get('is_admin', False))
```

**Update return dict** to include `is_admin`:
```python
    return {
        'user_id': user_id,
        'username': username,
        'is_admin': is_admin  # NEW
    }
```

**Task 1.2**: Update all 9 templates to include `is_admin` in window.currentUser

**Files to edit**:
- templates/home.html
- templates/standup.html
- templates/learning-dashboard.html
- templates/personality-preferences.html
- templates/settings-index.html
- templates/account.html
- templates/files.html
- templates/privacy-settings.html
- templates/advanced-settings.html

**Find this pattern** in each template:
```javascript
window.currentUser = {
  username: "{{ user.username }}",
  user_id: "{{ user.user_id }}"
};
```

**Add one line**:
```javascript
window.currentUser = {
  username: "{{ user.username }}",
  user_id: "{{ user.user_id }}",
  is_admin: {{ 'true' if user.is_admin else 'false' }}  // NEW
};
```

**Verification**:
```bash
# Test that is_admin appears in all templates
grep -c "is_admin" templates/*.html
# Should show 9 files with at least 1 match each
```

**Acceptance Criteria**:
- [ ] `_extract_user_context()` returns `is_admin` boolean
- [ ] All 9 templates inject `window.currentUser.is_admin`
- [ ] No syntax errors in templates (they still render)

---

### Phase 2: Permission Helper Utilities (30 minutes)

**Objective**: Create reusable JavaScript permission functions

**Task 2.1**: Create `web/static/js/permissions.js`

**Full file content**:
```javascript
/**
 * Permission helper utilities for RBAC
 * Checks permissions based on window.currentUser and resource metadata
 */

// Check if current user can edit a resource
function canEdit(resource) {
  if (!window.currentUser) return false;
  if (window.currentUser.is_admin) return true;
  if (resource.owner_id === window.currentUser.user_id) return true;

  // Check shared_with for EDITOR or ADMIN role
  if (!resource.shared_with) return false;
  const share = resource.shared_with.find(s => s.user_id === window.currentUser.user_id);
  return share && (share.role === 'EDITOR' || share.role === 'ADMIN');
}

// Check if current user can delete a resource
function canDelete(resource) {
  if (!window.currentUser) return false;
  if (window.currentUser.is_admin) return true;
  if (resource.owner_id === window.currentUser.user_id) return true;

  // Only resource-level ADMIN role can delete
  if (!resource.shared_with) return false;
  const share = resource.shared_with.find(s => s.user_id === window.currentUser.user_id);
  return share && share.role === 'ADMIN';
}

// Check if current user can share a resource
function canShare(resource) {
  if (!window.currentUser) return false;
  if (window.currentUser.is_admin) return true;
  return resource.owner_id === window.currentUser.user_id;
}

// Check if current user is owner
function isOwner(resource) {
  if (!window.currentUser) return false;
  return resource.owner_id === window.currentUser.user_id;
}

// Get current user's role for a resource
function getUserRole(resource) {
  if (!window.currentUser) return 'NONE';
  if (window.currentUser.is_admin) return 'ADMIN';
  if (resource.owner_id === window.currentUser.user_id) return 'OWNER';

  if (!resource.shared_with) return 'NONE';
  const share = resource.shared_with.find(s => s.user_id === window.currentUser.user_id);
  return share ? share.role : 'NONE';
}

// Format role for display
function formatRole(role) {
  const roleLabels = {
    'OWNER': 'Owner',
    'ADMIN': 'Admin',
    'EDITOR': 'Editor',
    'VIEWER': 'Viewer',
    'NONE': 'No Access'
  };
  return roleLabels[role] || role;
}

// Get role badge CSS class
function getRoleBadgeClass(role) {
  return `permission-badge ${role.toLowerCase()}`;
}
```

**Task 2.2**: Create `web/static/css/permissions.css`

**Full file content**:
```css
/* Permission-aware UI styles */

.permission-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.85em;
  font-weight: 500;
  margin-left: 8px;
}

.permission-badge.owner {
  background: #667eea;
  color: white;
}

.permission-badge.admin {
  background: #f59e0b;
  color: white;
}

.permission-badge.editor {
  background: #10b981;
  color: white;
}

.permission-badge.viewer {
  background: #6b7280;
  color: white;
}

.shared-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9em;
  color: #6b7280;
  margin-top: 4px;
}

.shared-indicator svg {
  width: 16px;
  height: 16px;
}

/* Resource list styles */
.resource-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.resource-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  transition: box-shadow 0.2s;
}

.resource-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.resource-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.resource-title {
  font-size: 1.1em;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.resource-actions {
  display: flex;
  gap: 8px;
}

.resource-actions button {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  font-size: 0.9em;
  cursor: pointer;
  transition: all 0.2s;
}

.resource-actions button.edit-btn {
  background: #3b82f6;
  color: white;
}

.resource-actions button.edit-btn:hover {
  background: #2563eb;
}

.resource-actions button.delete-btn {
  background: #ef4444;
  color: white;
}

.resource-actions button.delete-btn:hover {
  background: #dc2626;
}

.resource-actions button.share-btn {
  background: #8b5cf6;
  color: white;
}

.resource-actions button.share-btn:hover {
  background: #7c3aed;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6b7280;
}

.empty-state h3 {
  font-size: 1.3em;
  margin-bottom: 8px;
}

.empty-state p {
  margin-bottom: 20px;
}

/* Create button */
.create-resource-btn {
  background: #10b981;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 20px;
}

.create-resource-btn:hover {
  background: #059669;
}

/* Responsive */
@media (max-width: 480px) {
  .resource-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .resource-actions {
    width: 100%;
    flex-direction: column;
  }

  .resource-actions button {
    width: 100%;
  }
}
```

**Acceptance Criteria**:
- [ ] `permissions.js` created with all 7 functions
- [ ] `permissions.css` created with all styles
- [ ] Files accessible (no 404 when linked in HTML)

---

### Phase 3: Build Lists Page (90 minutes)

**Objective**: Create `/lists` page with permission-aware UI

**Task 3.1**: Add route handler in `web/app.py` (15 min)

**Add this route** (find similar routes like `/standup` and add nearby):
```python
@app.get("/lists", response_class=HTMLResponse)
async def lists_ui(request: Request):
    """Lists management page with permission-aware UI"""
    user_context = _extract_user_context(request)

    # TODO: Fetch lists from backend API
    # For now, pass empty list (will implement API call)
    lists_data = []

    return templates.TemplateResponse("lists.html", {
        "request": request,
        "user": user_context,
        "lists": lists_data
    })
```

**Task 3.2**: Create `templates/lists.html` (60 min)

**Template structure** (use existing templates as reference):
```html
<!DOCTYPE html>
<html>
<head>
  <title>My Lists - Piper Morgan</title>
  <link rel="icon" type="image/x-icon" href="/assets/favicon.ico" />
  <link rel="stylesheet" href="/static/css/toast.css" />
  <link rel="stylesheet" href="/static/css/dialog.css" />
  <link rel="stylesheet" href="/static/css/permissions.css" />
  <link rel="stylesheet" href="/static/css/spacing.css" />
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      margin: 0;
      padding: 20px;
      background: #f5f5f5;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: white;
      border-radius: 10px;
      padding: 30px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .page-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
    }
    .page-header h1 {
      color: #2c3e50;
      margin: 0;
    }
  </style>
</head>
<body>
  <!-- Include navigation component -->
  {% include 'components/navigation.html' %}

  <div class="container">
    <div class="page-header">
      <h1>My Lists</h1>
      <button class="create-resource-btn" onclick="createNewList()">
        + Create New List
      </button>
    </div>

    <!-- Lists will be rendered here by JavaScript -->
    <div id="lists-container" class="resource-list">
      <div class="empty-state">
        <h3>No lists yet</h3>
        <p>Create your first list to get started</p>
      </div>
    </div>
  </div>

  <!-- JavaScript -->
  <script src="/static/js/toast.js"></script>
  <script src="/static/js/dialog.js"></script>
  <script src="/static/js/permissions.js"></script>
  <script>
    // Inject user context from server
    {% if user %}
    window.currentUser = {
      username: "{{ user.username }}",
      user_id: "{{ user.user_id }}",
      is_admin: {{ 'true' if user.is_admin else 'false' }}
    };
    {% else %}
    window.currentUser = null;
    {% endif %}

    // Fetch and render lists on page load
    document.addEventListener('DOMContentLoaded', async () => {
      await loadLists();
    });

    // Load lists from API
    async function loadLists() {
      try {
        // TODO: Call backend API
        // const response = await fetch('/api/v1/lists');
        // const lists = await response.json();

        // For now, use empty array
        const lists = [];

        renderLists(lists);
      } catch (error) {
        console.error('Error loading lists:', error);
        Toast.error('Failed to load lists');
      }
    }

    // Render lists with permission-aware UI
    function renderLists(lists) {
      const container = document.getElementById('lists-container');

      if (lists.length === 0) {
        container.innerHTML = `
          <div class="empty-state">
            <h3>No lists yet</h3>
            <p>Create your first list to get started</p>
          </div>
        `;
        return;
      }

      container.innerHTML = lists.map(list => {
        const role = getUserRole(list);
        const roleDisplay = formatRole(role);

        // Build action buttons based on permissions
        let actionButtons = '';

        if (canEdit(list)) {
          actionButtons += `
            <button class="edit-btn" onclick="editList('${list.id}')">
              Edit
            </button>
          `;
        }

        if (canDelete(list)) {
          actionButtons += `
            <button class="delete-btn" onclick="deleteList('${list.id}')">
              Delete
            </button>
          `;
        }

        if (canShare(list)) {
          actionButtons += `
            <button class="share-btn" onclick="shareList('${list.id}', '${list.name}')">
              Share
            </button>
          `;
        }

        // Build owner indicator
        const ownerIndicator = !isOwner(list) ?
          `<div class="shared-indicator">
             Owned by: ${list.owner_username || list.owner_id}
           </div>` : '';

        return `
          <div class="resource-item">
            <div class="resource-header">
              <div>
                <h3 class="resource-title">
                  ${list.name}
                  <span class="${getRoleBadgeClass(role)}">
                    ${roleDisplay}
                  </span>
                </h3>
                ${ownerIndicator}
              </div>
              <div class="resource-actions">
                ${actionButtons}
              </div>
            </div>
            <p>${list.description || 'No description'}</p>
            <small>Items: ${list.item_count || 0}</small>
          </div>
        `;
      }).join('');
    }

    // Create new list
    function createNewList() {
      Dialog.show({
        title: 'Create New List',
        content: `
          <div class="form-group">
            <label>List Name</label>
            <input type="text" id="new-list-name" placeholder="My List">
          </div>
          <div class="form-group">
            <label>Description (optional)</label>
            <textarea id="new-list-description"
                      placeholder="What's this list for?"
                      rows="3"></textarea>
          </div>
        `,
        onConfirm: async () => {
          const name = document.getElementById('new-list-name').value;
          const description = document.getElementById('new-list-description').value;

          if (!name) {
            Toast.error('List name is required');
            return false; // Keep dialog open
          }

          try {
            // TODO: Call API to create list
            // const response = await fetch('/api/v1/lists', {
            //   method: 'POST',
            //   headers: {'Content-Type': 'application/json'},
            //   body: JSON.stringify({ name, description })
            // });

            Toast.success('List created successfully');
            await loadLists(); // Refresh list
            return true; // Close dialog
          } catch (error) {
            console.error('Error creating list:', error);
            Toast.error('Failed to create list');
            return false;
          }
        }
      });
    }

    // Edit list
    function editList(listId) {
      // TODO: Implement edit functionality
      Toast.info('Edit functionality coming soon');
    }

    // Delete list
    function deleteList(listId) {
      Dialog.confirm({
        title: 'Delete List',
        message: 'Are you sure you want to delete this list? This cannot be undone.',
        onConfirm: async () => {
          try {
            // TODO: Call API to delete
            // await fetch(`/api/v1/lists/${listId}`, { method: 'DELETE' });

            Toast.success('List deleted successfully');
            await loadLists();
          } catch (error) {
            console.error('Error deleting list:', error);
            Toast.error('Failed to delete list');
          }
        }
      });
    }

    // Share list
    function shareList(listId, listName) {
      // TODO: Implement sharing modal (Phase 6)
      Toast.info('Sharing functionality coming soon');
    }
  </script>
</body>
</html>
```

**Task 3.3**: Add navigation link (5 min)

**Edit**: `templates/components/navigation.html`

**Find the nav menu** and add:
```html
<li><a href="/lists">Lists</a></li>
```

**Acceptance Criteria**:
- [ ] `/lists` route accessible
- [ ] Page renders without errors
- [ ] Empty state shows when no lists
- [ ] Create button present
- [ ] Navigation link works
- [ ] User context injected correctly

---

### Phase 4 & 5: Todos and Projects Pages (3 hours total)

**Follow exact same pattern as Phase 3 for**:
- `/todos` route + `templates/todos.html`
- `/projects` route + `templates/projects.html`

**Differences**:
- Todos: Use `/api/v1/todos` endpoints
- Projects: Use `/api/v1/projects` endpoints
- Adjust field names (todos have due_date, projects have start/end dates)

**Copy-paste approach**:
1. Copy lists.html → todos.html
2. Find/replace "list" → "todo", "List" → "Todo"
3. Adjust fields for todo-specific data
4. Repeat for projects

**Acceptance Criteria** (each page):
- [ ] Route accessible
- [ ] Page renders
- [ ] Permission-aware buttons
- [ ] Empty state
- [ ] Navigation link

---

### Phase 6: Sharing Modal (60 minutes)

**Objective**: Make sharing functional across all resource types

**Task 6.1**: Create sharing modal function (30 min)

**Add to each template's JavaScript** (lists.html, todos.html, projects.html):

```javascript
// Replace stub shareList/shareTodo/shareProject function with:

function shareList(listId, listName) {
  openShareModal('lists', listId, listName);
}

// Generic sharing modal
async function openShareModal(resourceType, resourceId, resourceName) {
  // Fetch current shares
  let currentShares = [];
  try {
    const response = await fetch(`/api/v1/${resourceType}/${resourceId}/shares`);
    if (response.ok) {
      currentShares = await response.json();
    }
  } catch (error) {
    console.error('Error fetching shares:', error);
  }

  Dialog.show({
    title: `Share ${resourceName}`,
    width: '500px',
    content: `
      <div class="share-modal-content">
        <div class="form-group">
          <label>Email or User ID</label>
          <input type="text" id="share-user-input"
                 placeholder="user@example.com or user-id">
        </div>

        <div class="form-group">
          <label>Role</label>
          <select id="share-role-select">
            <option value="VIEWER">Viewer (Read only)</option>
            <option value="EDITOR">Editor (Can edit)</option>
            <option value="ADMIN">Admin (Can manage shares)</option>
          </select>
        </div>

        <button onclick="addShare('${resourceType}', '${resourceId}')"
                class="create-resource-btn"
                style="width: 100%; margin-top: 12px;">
          Add Share
        </button>

        <div class="current-shares" style="margin-top: 24px;">
          <h4>Currently Shared With</h4>
          <div id="current-shares-list">
            ${renderCurrentShares(currentShares, resourceType, resourceId)}
          </div>
        </div>
      </div>
    `,
    hideFooter: true // Custom buttons in content
  });
}

// Render current shares list
function renderCurrentShares(shares, resourceType, resourceId) {
  if (shares.length === 0) {
    return '<p style="color: #6b7280;">Not shared with anyone yet</p>';
  }

  return shares.map(share => `
    <div style="display: flex; justify-content: space-between; align-items: center;
                padding: 12px; border: 1px solid #e5e7eb; border-radius: 6px; margin-bottom: 8px;">
      <div>
        <strong>${share.user_email || share.user_id}</strong>
        <span class="${getRoleBadgeClass(share.role)}">${formatRole(share.role)}</span>
      </div>
      <button onclick="removeShare('${resourceType}', '${resourceId}', '${share.user_id}')"
              style="background: #ef4444; color: white; padding: 6px 12px;
                     border: none; border-radius: 4px; cursor: pointer;">
        Remove
      </button>
    </div>
  `).join('');
}

// Add share
async function addShare(resourceType, resourceId) {
  const userInput = document.getElementById('share-user-input').value;
  const role = document.getElementById('share-role-select').value;

  if (!userInput) {
    Toast.error('Please enter a user email or ID');
    return;
  }

  try {
    const response = await fetch(`/api/v1/${resourceType}/${resourceId}/share`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        user_to_share_with: userInput,
        role: role
      })
    });

    if (response.ok) {
      Toast.success('Shared successfully');
      // Close and reopen modal to refresh
      Dialog.close();
      // Reload resource to get updated shares
      await loadLists(); // or loadTodos/loadProjects depending on page
    } else {
      const error = await response.json();
      Toast.error(error.message || 'Failed to share');
    }
  } catch (error) {
    console.error('Error sharing:', error);
    Toast.error('Failed to share');
  }
}

// Remove share
async function removeShare(resourceType, resourceId, userId) {
  try {
    const response = await fetch(
      `/api/v1/${resourceType}/${resourceId}/share/${userId}`,
      { method: 'DELETE' }
    );

    if (response.ok) {
      Toast.success('Share removed');
      Dialog.close();
      await loadLists(); // or loadTodos/loadProjects
    } else {
      Toast.error('Failed to remove share');
    }
  } catch (error) {
    console.error('Error removing share:', error);
    Toast.error('Failed to remove share');
  }
}
```

**Task 6.2**: Test sharing flow (20 min)

Manual test:
1. Open sharing modal
2. Verify current shares display
3. Add new share
4. Verify API call made
5. Verify toast notification
6. Remove share
7. Verify removal works

**Task 6.3**: Error handling (10 min)

Add try/catch blocks and user-friendly error messages for:
- User not found
- Already shared
- Permission denied
- Network errors

**Acceptance Criteria**:
- [ ] Sharing modal opens
- [ ] Current shares display
- [ ] Can add new share
- [ ] Can remove share
- [ ] Toast notifications work
- [ ] Error handling present

---

## STOP Conditions

**YOU MUST STOP and report if**:

1. ❌ Backend API endpoints don't exist
   - **Check**: Try calling `/api/v1/lists` - does it return 404?
   - **Action**: Report missing endpoints, wait for guidance

2. ❌ User claims don't include `is_admin` flag
   - **Check**: After Phase 1, test `window.currentUser.is_admin`
   - **Action**: Report missing claim, check JWT structure

3. ❌ Sharing API endpoints missing
   - **Check**: `/api/v1/lists/{id}/share` exists?
   - **Action**: Report, may need to skip sharing features

4. ❌ Tests fail after changes
   - **Action**: Report failures, don't proceed

5. ❌ Templates don't render (Jinja2 errors)
   - **Action**: Fix syntax errors, verify template variables

**DO NOT rationalize these as minor issues. STOP and report.**

---

## Success Criteria

**When ALL complete**:
- [ ] `is_admin` flag in user context
- [ ] Permission utility functions working
- [ ] 3 resource pages created (Lists, Todos, Projects)
- [ ] Permission-aware buttons (hidden when no permission)
- [ ] Sharing modal functional
- [ ] No JavaScript console errors
- [ ] No 403 errors during normal use
- [ ] Mobile responsive
- [ ] All pages accessible via navigation

---

## Testing Checklist

**After completing all phases**, manually test:

**As Owner**:
- [ ] Can see owned resources
- [ ] Can create new resources
- [ ] Can edit owned resources
- [ ] Can delete owned resources
- [ ] Can share owned resources

**As Editor** (if you have test shared resources):
- [ ] Can see shared resources
- [ ] Can edit shared resources
- [ ] Cannot delete (button hidden)
- [ ] Cannot share (button hidden)

**As Viewer** (if you have test shared resources):
- [ ] Can see shared resources
- [ ] Cannot edit (button hidden)
- [ ] Cannot delete (button hidden)
- [ ] Cannot share (button hidden)

**Responsive**:
- [ ] Mobile (<480px) buttons stack vertically
- [ ] Desktop layout works

---

## Deliverables

When complete, provide:

1. **List of files changed**:
   - web/app.py (routes added)
   - templates/ (pages created)
   - web/static/ (JS/CSS added)

2. **Screenshots** (if possible):
   - Empty state
   - Lists page with resources
   - Permission badges
   - Sharing modal

3. **Evidence of testing**:
   - Console logs showing permission checks
   - No JavaScript errors
   - Routes accessible

4. **Completion report** in:
   `dev/2025/11/23/frontend-rbac-option-b-completion.md`

---

## Time Tracking

Document actual time spent on each phase:

| Phase | Estimated | Actual |
|-------|-----------|--------|
| 1 | 15 min | ___ min |
| 2 | 30 min | ___ min |
| 3 | 90 min | ___ min |
| 4 | 90 min | ___ min |
| 5 | 90 min | ___ min |
| 6 | 60 min | ___ min |
| Testing | 30 min | ___ min |

---

## Remember

- Follow existing patterns from templates/home.html and templates/standup.html
- Reuse utility modules (dialog.js, toast.js)
- Don't over-engineer - simple vanilla JS is perfect
- Permission checks happen client-side for UI, backend enforces actual security
- Mobile-first responsive design
- ARIA labels for accessibility

---

**Authorization**: Execute immediately
**Expected Completion**: 6-7 hours
**Target**: Complete today for Michelle tomorrow

Good luck! Build systematically, test as you go, and stop if you hit any blockers.
