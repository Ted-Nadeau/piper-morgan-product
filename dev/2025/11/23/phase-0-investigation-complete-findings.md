# Phase 0: Investigation Complete - Findings & Recommendations
**Issue**: #376 FRONTEND-RBAC-AWARENESS
**Date**: November 23, 2025, 10:05 AM
**Investigator**: Lead Developer (xian)

---

## Executive Summary

**Key Finding**: Lists/Todos/Projects do NOT have dedicated UI pages. This is primarily a conversational AI interface where resource management happens through chat commands.

**User Context**: ✅ FULLY IMPLEMENTED (Issue #307) - `window.currentUser` available on all pages

**Architecture**: Jinja2 server-side rendering + vanilla JavaScript (proven, working, no framework needed)

**Recommendation**: Build lightweight resource management UI using existing patterns, OR defer UI and focus on API-level permission awareness only.

---

## Question 1: Where are Lists/Todos/Projects UI components?

### Answer: THEY DON'T EXIST (conversational interface only)

**Evidence**:
1. ✅ `templates/` directory exists with 10 pages:
   - home.html (main chat interface - 34KB)
   - standup.html
   - learning-dashboard.html
   - personality-preferences.html
   - settings-index.html
   - account.html
   - files.html
   - privacy-settings.html
   - advanced-settings.html
   - 404/500/network-error pages

2. ❌ NO dedicated pages for:
   - Lists management
   - Todos management
   - Projects management

3. ✅ Main interface is conversational (`home.html`):
   - Chat window with message history
   - Text input for commands
   - Bot responds with actions
   - Resource management likely happens via text commands

**Implication**: We need to CREATE rudimentary resource management UI, not just add permissions to existing UI.

---

## Question 2: Where is user context set up?

### Answer: FULLY IMPLEMENTED in Issue #307 ✅

**From Issue #307 Completion Report** (Nov 22, 2025):

### User Context Implementation

**Location**: `web/app.py` (line 136)
```python
def _extract_user_context(request: Request) -> dict:
    """Extract user context from request state for template injection"""
    user_id = getattr(request.state, 'user_id', 'user')
    username = user_id  # Default to user_id
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

**All 9 route handlers extract and pass user context**:
```python
user_context = _extract_user_context(request)
return templates.TemplateResponse("template.html", {"request": request, "user": user_context})
```

**Frontend Access** (in all template <script> tags):
```javascript
{% if user %}
window.currentUser = {
  username: "{{ user.username }}",
  user_id: "{{ user.user_id }}"
};
{% else %}
window.currentUser = null;
{% endif %}
```

**Status**: ✅ User context fully working, verified in `home.html` lines 767-773

**Available Information**:
- `window.currentUser.username` - User's display name
- `window.currentUser.user_id` - User's unique ID
- Can access via JavaScript on any page

**Missing**:
- ❌ User role (is_admin flag) - NOT currently in `window.currentUser`
- ❌ User permissions - NO permission data passed to frontend

**Action Required**: Extend `_extract_user_context()` to include `is_admin` from user claims

---

## Question 3: Architecture - Jinja2 vs Alternatives

### Answer: Jinja2 + Vanilla JS is CORRECT and PROVEN ✅

### Current Architecture (Verified)

**Stack**:
- Backend: FastAPI (Python web framework)
- Templates: Jinja2 (server-side rendering)
- Frontend: Vanilla JavaScript (no framework)
- Styling: Inline CSS + external CSS files
- State: Global `window` objects (simple, works)

**Proven Patterns** (from Issue #307 + #310):
- Server passes data to templates via Jinja2 context
- Templates inject data into JavaScript via `<script>` tags
- JavaScript utility modules for common UI (toast, dialog, loading, etc.)
- Responsive design with CSS media queries
- Accessibility features (ARIA labels, semantic HTML)

### Pros of Current Architecture

**✅ Advantages**:
1. **Simple**: No build step, no transpiling, no package.json complexity
2. **Fast**: Server-side rendering = instant first paint
3. **Proven**: Issue #307 (navigation) and #310 (quick wins) both successful
4. **SEO-friendly**: HTML rendered server-side (if that matters)
5. **Low maintenance**: No framework version updates, no breaking changes
6. **Easy debugging**: View source = see actual code running
7. **No context switching**: Python devs can read/write frontend code
8. **Works everywhere**: No browser compatibility issues (vanilla JS)

**✅ Already Available**:
- User context injection pattern
- Utility modules (dialog, toast, loading spinners)
- CSS design system (spacing, colors, components)
- Navigation component
- Mobile-responsive patterns

**✅ Perfect for MVP/Alpha**:
- Fast to implement
- Easy to change
- No over-engineering
- Time-to-Michelle minimized

### Cons of Current Architecture

**❌ Limitations**:
1. **No reactive state**: Changes require manual DOM manipulation
2. **No component reusability**: Copy-paste HTML across templates
3. **No type safety**: JavaScript is untyped (but TypeScript adds complexity)
4. **Scaling concerns**: Large SPAs benefit from frameworks
5. **Testing**: No component unit tests (but we can add them)

### Alternative: React/Vue SPA

**Would Require**:
- ❌ Build system (webpack/vite)
- ❌ Package management (npm/yarn)
- ❌ Transpiling (Babel for JSX)
- ❌ State management (Redux/Vuex)
- ❌ Routing (React Router/Vue Router)
- ❌ API layer (fetch/axios wrappers)
- ❌ Learning curve for team
- ❌ 2-4 days setup time

**Benefits**:
- ✅ Component reusability
- ✅ Reactive state updates
- ✅ Better for complex UIs
- ✅ Strong ecosystem

**Verdict**: ❌ **NOT WORTH IT FOR ALPHA**
- Overkill for current needs
- Blocks Michelle's onboarding
- Can migrate later if needed

### Recommendation: STAY WITH JINJA2 + VANILLA JS ✅

**Reasoning**:
1. ✅ It's already working (Issue #307 proof)
2. ✅ Team knows it (fast implementation)
3. ✅ Simple UIs don't need frameworks
4. ✅ Can refactor later if needed
5. ✅ Unblocks alpha launch TODAY

**For RBAC UI**:
- Use existing patterns from #307 and #310
- Create simple HTML forms for sharing
- Use vanilla JavaScript for permission checks
- Follow design system (spacing, colors, buttons)
- Mobile-responsive with CSS media queries

---

## Recommended Approach for Issue #376

### Option A: Minimal API-Level Awareness Only (1-2 hours)

**What**: Add permission info to API responses, no UI changes

**Pros**:
- ✅ Fast (1-2 hours)
- ✅ Backend already enforces permissions
- ✅ Minimal code changes
- ✅ Unblocks alpha TODAY

**Cons**:
- ❌ Users still see 403 errors
- ❌ No visual permission indicators
- ❌ No sharing UI
- ❌ Poor UX for Michelle

**Verdict**: ❌ Not sufficient for good alpha experience

### Option B: Rudimentary Resource Management Pages (4-6 hours)

**What**: Create basic Lists/Todos/Projects pages with permission awareness

**Implementation**:
1. Create 3 new template pages:
   - `templates/lists.html` - View/manage lists
   - `templates/todos.html` - View/manage todos
   - `templates/projects.html` - View/manage projects

2. Add routes in `web/app.py`:
   ```python
   @app.get("/lists", response_class=HTMLResponse)
   async def lists_ui(request: Request):
       user_context = _extract_user_context(request)
       # Fetch user's lists from API
       lists = await fetch_user_lists(user_context['user_id'])
       return templates.TemplateResponse("lists.html", {
           "request": request,
           "user": user_context,
           "lists": lists
       })
   ```

3. Add permission-aware UI:
   ```html
   {% for list in lists %}
   <div class="list-item">
     <h3>{{ list.name }}</h3>
     {% if list.owner_id == user.user_id or user.is_admin %}
       <button class="edit-btn">Edit</button>
       <button class="delete-btn">Delete</button>
       <button class="share-btn">Share</button>
     {% elif list.shared_with|contains(user.user_id, role='EDITOR') %}
       <button class="edit-btn">Edit</button>
     {% endif %}
   </div>
   {% endfor %}
   ```

4. Add sharing modal (JavaScript):
   ```javascript
   function openShareModal(listId) {
     // Use existing dialog.js utility
     Dialog.show({
       title: "Share List",
       content: createShareForm(listId),
       onConfirm: async () => {
         await shareList(listId, selectedUser, selectedRole);
       }
     });
   }
   ```

**Pros**:
- ✅ Complete UX solution
- ✅ No 403 errors (buttons hidden)
- ✅ Visual sharing indicators
- ✅ Sharing UI functional
- ✅ Follows existing patterns
- ✅ Good alpha experience

**Cons**:
- ❌ Takes 4-6 hours (might miss Michelle)
- ❌ Creates pages we might not keep long-term
- ❌ Duplicates some conversational features

**Verdict**: ✅ **BEST FOR QUALITY ALPHA**

### Option C: Conversational Permission Awareness (2-3 hours)

**What**: Add permission indicators to chat responses, no dedicated pages

**Implementation**:
1. Bot responses include ownership info:
   ```
   Bot: "Here are your lists:
   • Project Alpha (Owner) - Edit | Delete | Share
   • Team Todos (Shared: Editor) - Edit
   • Read-only List (Shared: Viewer) - View only"
   ```

2. Bot blocks unpermitted actions:
   ```
   User: "Delete 'Read-only List'"
   Bot: "You don't have permission to delete this list. You're a Viewer. Contact @owner to request Editor or Admin access."
   ```

3. Add `/share` command:
   ```
   User: "/share 'Project Alpha' with user@example.com as Editor"
   Bot: "Shared 'Project Alpha' with user@example.com as Editor ✓"
   ```

**Pros**:
- ✅ Leverages existing conversational UI
- ✅ Fast implementation (2-3 hours)
- ✅ No new pages needed
- ✅ Natural language UX
- ✅ Could be done TODAY

**Cons**:
- ❌ Less discoverable than UI buttons
- ❌ Requires users to learn commands
- ❌ Harder to show "all shared resources"

**Verdict**: ⚠️ **FALLBACK OPTION** if time is critical

---

## Technical Requirements for Any Option

### Must Add to User Context (Required for ALL options)

**Current** (`web/app.py:136`):
```python
def _extract_user_context(request: Request) -> dict:
    return {
        'user_id': user_id,
        'username': username
    }
```

**Required Addition**:
```python
def _extract_user_context(request: Request) -> dict:
    user_claims = getattr(request.state, 'user_claims', None)
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

**Frontend Injection** (all templates):
```javascript
window.currentUser = {
  username: "{{ user.username }}",
  user_id: "{{ user.user_id }}",
  is_admin: {{ 'true' if user.is_admin else 'false' }}  // NEW
};
```

**Estimated Time**: 15 minutes (1 function change + template updates)

### Permission Helper Functions (JavaScript)

**Create** `web/static/js/permissions.js`:
```javascript
/**
 * Permission helper utilities for RBAC
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
```

**Estimated Time**: 30 minutes

---

## Final Recommendations

### For Immediate Alpha Launch (TODAY)

**Priority 1**: Extend user context with `is_admin` flag (15 min)
**Priority 2**: Create permission helper JavaScript (30 min)
**Priority 3**: Choose implementation option:
  - **Option B** (4-6 hours): Best UX, might be tight for today
  - **Option C** (2-3 hours): Conversational fallback, doable today

**Total Time**:
- Option B: 5-7 hours (might miss Michelle if starting at 10 AM)
- Option C: 3-4 hours (can finish by 2 PM)

### For Quality Alpha Experience

**Recommended**: Option B (rudimentary resource pages)
- Complete permission awareness
- No confusing 403 errors
- Sharing UI functional
- Professional appearance
- Worth the time investment

**Fallback**: Option C (conversational awareness)
- If time runs out
- Still better than 403 errors
- Can upgrade to Option B later

### Architecture Decision

**✅ CONFIRMED**: Jinja2 + Vanilla JavaScript
- Proven working (Issue #307, #310)
- Fast to implement
- Team familiar with it
- Perfect for alpha
- Can refactor to SPA later if needed

---

## Next Steps (Awaiting PM Decision)

**PM: Please choose ONE**:

1. [ ] **Option B** - Build rudimentary resource pages (4-6 hours)
   - Best UX
   - Might be tight timing
   - I'll create implementation prompt for Code Agent

2. [ ] **Option C** - Conversational permission awareness (2-3 hours)
   - Faster
   - Good enough for alpha
   - Upgrade later if needed

3. [ ] **Hybrid** - Option C today, Option B during alpha
   - Unblock Michelle with C
   - Polish with B next week

4. [ ] **Custom** - Something else you have in mind

**Once decided, I will**:
1. Update gameplan Phase 0 completion
2. Create detailed Phase 1-4 execution plan
3. Prepare Code Agent prompt
4. Begin implementation

---

**Status**: Investigation complete, awaiting PM decision on approach
**Next Action**: PM selects option, then implementation begins
