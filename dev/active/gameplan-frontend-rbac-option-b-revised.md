# Gameplan: Frontend RBAC - Option B (Rudimentary Resource Pages)
**Issue**: #376 FRONTEND-RBAC-AWARENESS
**Date**: November 23, 2025, 10:05 AM
**Decision**: Option B - Build rudimentary Lists/Todos/Projects pages
**Estimated Duration**: 4-6 hours
**Target**: Complete today for Michelle tomorrow

---

## Mission Statement

Build lightweight resource management pages (Lists, Todos, Projects) with permission-aware UI following existing Jinja2 + vanilla JavaScript patterns. Enable sharing functionality and prevent 403 errors by hiding inappropriate actions.

**Architecture Decision**: ✅ Jinja2 + Vanilla JavaScript (proven in Issues #307, #310)

---

## Phase 0: Investigation - ✅ COMPLETE

**Findings Documented**: `dev/2025/11/23/phase-0-investigation-complete-findings.md`

**Key Discoveries**:
- ✅ User context system working (`window.currentUser`)
- ❌ Lists/Todos/Projects UI pages don't exist yet
- ✅ Jinja2 + vanilla JS is correct architecture
- ⚠️ Missing `is_admin` flag in user context

**Decision**: Build rudimentary resource pages from scratch

---

## Phase 1: Extend User Context (15 minutes)

### Objective
Add `is_admin` flag to existing user context system

### Tasks

**1.1 Update `_extract_user_context()` in web/app.py** (10 min)
```python
# Location: web/app.py line 136
def _extract_user_context(request: Request) -> dict:
    user_id = getattr(request.state, 'user_id', 'user')
    username = user_id
    user_claims = getattr(request.state, 'user_claims', None)

    # Extract username
    if user_claims and hasattr(user_claims, 'username'):
        username = user_claims.username
    elif user_claims and isinstance(user_claims, dict) and 'username' in user_claims:
        username = user_claims['username']

    # Extract is_admin flag (NEW)
    is_admin = False
    if user_claims:
        is_admin = getattr(user_claims, 'is_admin', False) or \
                   (isinstance(user_claims, dict) and user_claims.get('is_admin', False))

    return {
        'user_id': user_id,
        'username': username,
        'is_admin': is_admin  # NEW
    }
```

**1.2 Update all template user context injection** (5 min)

Add to script tags in all templates:
```javascript
window.currentUser = {
  username: "{{ user.username }}",
  user_id: "{{ user.user_id }}",
  is_admin: {{ 'true' if user.is_admin else 'false' }}  // NEW
};
```

**Templates to update**:
- templates/home.html
- templates/standup.html
- templates/learning-dashboard.html
- templates/personality-preferences.html
- templates/settings-index.html
- templates/account.html
- templates/files.html
- templates/privacy-settings.html
- templates/advanced-settings.html

**Acceptance Criteria**:
- [ ] `_extract_user_context()` returns `is_admin` boolean
- [ ] All 9 templates inject `window.currentUser.is_admin`
- [ ] Console shows correct admin status for test users

---

## Phase 2: Permission Helper Utilities (30 minutes)

### Objective
Create reusable JavaScript permission check functions

### Tasks

**2.1 Create `web/static/js/permissions.js`** (20 min)
```javascript
/**
 * Permission helper utilities for RBAC
 * Uses window.currentUser and resource metadata
 */

// Check if current user can edit a resource
function canEdit(resource) {
  if (!window.currentUser) return false;
  if (window.currentUser.is_admin) return true;
  if (resource.owner_id === window.currentUser.user_id) return true;

  // Check shared_with for EDITOR or ADMIN role
  const share = resource.shared_with?.find(s => s.user_id === window.currentUser.user_id);
  return share && (share.role === 'EDITOR' || share.role === 'ADMIN');
}

// Check if current user can delete a resource
function canDelete(resource) {
  if (!window.currentUser) return false;
  if (window.currentUser.is_admin) return true;
  if (resource.owner_id === window.currentUser.user_id) return true;

  // Only ADMIN share role can delete
  const share = resource.shared_with?.find(s => s.user_id === window.currentUser.user_id);
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
  if (!window.currentUser) return null;
  if (window.currentUser.is_admin) return 'ADMIN';
  if (resource.owner_id === window.currentUser.user_id) return 'OWNER';

  const share = resource.shared_with?.find(s => s.user_id === window.currentUser.user_id);
  return share?.role || 'NONE';
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
```

**2.2 Add permission CSS** (10 min)

Create `web/static/css/permissions.css`:
```css
/* Permission-aware UI styles */

.permission-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.85em;
  font-weight: 500;
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

/* Hide elements based on permissions (fallback for JS) */
[data-requires-edit]:not([data-can-edit="true"]) {
  display: none !important;
}

[data-requires-delete]:not([data-can-delete="true"]) {
  display: none !important;
}

[data-requires-share]:not([data-can-share="true"]) {
  display: none !important;
}
```

**Acceptance Criteria**:
- [ ] `permissions.js` file created with all 6 helper functions
- [ ] `permissions.css` file created with badge styles
- [ ] Functions accessible globally (no module imports needed)

---

## Phase 3: Build Lists Page (90 minutes)

### Objective
Create `/lists` page with permission-aware UI

### Tasks

**3.1 Create backend route** (15 min)

Add to `web/app.py`:
```python
@app.get("/lists", response_class=HTMLResponse)
async def lists_ui(request: Request):
    """Lists management page with permission awareness"""
    user_context = _extract_user_context(request)

    # Fetch user's lists from backend API
    # Include owned lists + shared lists
    lists_data = []
    try:
        # TODO: Call backend API to get lists
        # For now, return empty (will implement API call)
        pass
    except Exception as e:
        logger.error(f"Error fetching lists: {e}")

    return templates.TemplateResponse("lists.html", {
        "request": request,
        "user": user_context,
        "lists": lists_data
    })
```

**3.2 Create `templates/lists.html`** (60 min)

Structure:
- Header with "My Lists" title
- "Create New List" button
- List of lists with permission-aware actions
- Sharing modal component
- Permission indicators

Key features:
- Show owner name if not current user
- Hide Edit/Delete for viewers
- Hide Delete for editors
- Hide Share for non-owners
- Visual role badges

**3.3 Add API integration JavaScript** (15 min)

Functions for:
- Fetching lists from backend
- Creating new list
- Editing list
- Deleting list
- Opening share modal

**Acceptance Criteria**:
- [ ] `/lists` route returns lists page
- [ ] Page shows owned + shared lists
- [ ] Permission-aware buttons render correctly
- [ ] Empty state shown if no lists
- [ ] Mobile responsive

---

## Phase 4: Build Todos Page (90 minutes)

### Objective
Create `/todos` page (similar pattern to Lists)

### Tasks

**4.1 Create backend route** (15 min)
**4.2 Create `templates/todos.html`** (60 min)
**4.3 Add API integration JavaScript** (15 min)

**Reuse from Phase 3**:
- Permission helper functions
- CSS styles
- Sharing modal pattern
- API integration pattern

**Acceptance Criteria**:
- [ ] `/todos` route returns todos page
- [ ] Permission-aware UI working
- [ ] Sharing functionality present
- [ ] Consistent with Lists page UX

---

## Phase 5: Build Projects Page (90 minutes)

### Objective
Create `/projects` page (similar pattern to Lists/Todos)

### Tasks

**5.1 Create backend route** (15 min)
**5.2 Create `templates/projects.html`** (60 min)
**5.3 Add API integration JavaScript** (15 min)

**Acceptance Criteria**:
- [ ] `/projects` route returns projects page
- [ ] Permission-aware UI working
- [ ] Sharing functionality present
- [ ] Consistent with Lists/Todos UX

---

## Phase 6: Sharing Modal Implementation (60 minutes)

### Objective
Create reusable sharing modal for all resource types

### Tasks

**6.1 Create sharing modal component** (30 min)

Use existing `dialog.js` utility:
```javascript
function openShareModal(resourceType, resourceId, resourceName) {
  Dialog.show({
    title: `Share ${resourceName}`,
    content: createShareModalContent(resourceType, resourceId),
    width: '500px',
    onConfirm: async () => {
      await submitShare(resourceType, resourceId);
    }
  });
}

function createShareModalContent(resourceType, resourceId) {
  return `
    <div class="share-modal-content">
      <div class="form-group">
        <label>Email or Username</label>
        <input type="text" id="share-user-input"
               placeholder="user@example.com">
      </div>

      <div class="form-group">
        <label>Role</label>
        <select id="share-role-select">
          <option value="VIEWER">Viewer (Read only)</option>
          <option value="EDITOR">Editor (Can edit)</option>
          <option value="ADMIN">Admin (Can manage shares)</option>
        </select>
      </div>

      <div class="current-shares">
        <h4>Currently Shared With</h4>
        <div id="current-shares-list">Loading...</div>
      </div>
    </div>
  `;
}
```

**6.2 Add share API integration** (20 min)

Functions for:
- `GET /api/v1/{resource_type}/{id}/shares` - Get current shares
- `POST /api/v1/{resource_type}/{id}/share` - Add share
- `DELETE /api/v1/{resource_type}/{id}/share/{user_id}` - Remove share
- `PUT /api/v1/{resource_type}/{id}/share/{user_id}` - Update role

**6.3 Add error handling** (10 min)

Toast notifications for:
- Share added successfully
- Share removed successfully
- Role updated successfully
- Error messages (user not found, etc.)

**Acceptance Criteria**:
- [ ] Modal opens on "Share" button click
- [ ] Lists current shares with remove buttons
- [ ] Can add new share with role selection
- [ ] Can remove existing shares
- [ ] Can update share roles
- [ ] Toast notifications for all actions
- [ ] Error handling for failures

---

## Phase Z: Testing & Validation (30 minutes)

### Manual Testing Checklist

**Test as Owner**:
- [ ] Can see all owned resources
- [ ] Can create new resources
- [ ] Can edit owned resources
- [ ] Can delete owned resources
- [ ] Can share owned resources
- [ ] Share modal shows current shares

**Test as Editor** (shared resource):
- [ ] Can see shared resources
- [ ] Can edit shared resources
- [ ] Cannot delete shared resources
- [ ] Cannot share resources (not owner)
- [ ] Role badge shows "Editor"

**Test as Viewer** (shared resource):
- [ ] Can see shared resources
- [ ] Cannot see Edit button
- [ ] Cannot see Delete button
- [ ] Cannot see Share button
- [ ] Role badge shows "Viewer"

**Test as Admin**:
- [ ] Can see all resources
- [ ] Can edit any resource
- [ ] Can delete any resource
- [ ] Can share any resource
- [ ] Role badge shows "Admin"

**Responsive Testing**:
- [ ] Mobile (<480px): Buttons stack vertically
- [ ] Tablet (480-768px): Layout adjusts properly
- [ ] Desktop (>768px): Full layout visible

**Accessibility Testing**:
- [ ] All buttons have aria-labels
- [ ] Modal has proper focus management
- [ ] Keyboard navigation works
- [ ] Screen reader friendly

---

## Success Criteria

**Functionality**:
- [ ] 3 resource pages created (Lists, Todos, Projects)
- [ ] Permission-aware UI hides inappropriate actions
- [ ] Sharing modal functional for all resource types
- [ ] No 403 errors during normal use

**Quality**:
- [ ] Consistent UX across all 3 pages
- [ ] Mobile responsive
- [ ] Accessible (ARIA labels, keyboard nav)
- [ ] No JavaScript console errors
- [ ] Performance <100ms render

**Documentation**:
- [ ] Code comments for permission logic
- [ ] Session log updated
- [ ] GitHub issue #376 updated with evidence

---

## STOP Conditions

**STOP immediately if**:
- Backend API endpoints missing (lists/todos/projects)
- Sharing API endpoints not implemented
- User claims don't include is_admin flag
- Breaking changes to existing pages
- Performance degrades >500ms

**When stopped**: Document issue, propose solution, wait for PM decision

---

## Timeline Estimate

| Phase | Task | Time | Cumulative |
|-------|------|------|------------|
| 1 | Extend user context | 15 min | 15 min |
| 2 | Permission utilities | 30 min | 45 min |
| 3 | Lists page | 90 min | 2h 15m |
| 4 | Todos page | 90 min | 3h 45m |
| 5 | Projects page | 90 min | 5h 15m |
| 6 | Sharing modal | 60 min | 6h 15m |
| Z | Testing | 30 min | 6h 45m |

**Total**: 6 hours 45 minutes (with breaks: ~7-8 hours)

**Start**: 10:30 AM
**Estimated Complete**: 5:30-6:30 PM
**Buffer**: 30-60 minutes for issues

---

## Next Steps

1. PM approves gameplan
2. Create focused Code Agent prompt
3. Code Agent begins Phase 1
4. Lead Dev monitors progress
5. Testing & validation
6. Deployment to production (Issue #378)

---

**Gameplan Status**: ✅ Ready for execution
**Architecture Decision**: ✅ Jinja2 + Vanilla JS confirmed
**Approach**: ✅ Option B approved by PM
