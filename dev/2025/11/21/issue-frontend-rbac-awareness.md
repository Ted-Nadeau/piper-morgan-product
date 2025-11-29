# FRONTEND-RBAC-AWARENESS: Add Permission-Aware UI Components

**Priority**: P0 (Alpha Prep)
**Sprint**: A9 (Final Alpha Prep)
**Size**: Medium (4-6 hours)
**Labels**: `frontend`, `rbac`, `alpha-blocking`, `ux`

---

## Problem Statement

### Current State
Backend RBAC is complete and working - it properly enforces permissions. However, the frontend doesn't know about user roles and shows all actions to all users, leading to:
- Viewers see "Delete" buttons that return 403 errors
- No visual indication of shared resources
- No way to share resources through UI
- Confusion about why some actions fail

### Impact
- **User Confusion**: Users try actions they can't perform
- **Support Burden**: "Why can't I delete?" tickets
- **Poor UX**: Error messages instead of hidden actions
- **Alpha Blocker**: First impression matters for alpha testers

---

## Goal

**Primary Objective**: Make the UI aware of user permissions and provide basic sharing capabilities

**Success State**:
- Viewers don't see actions they can't perform
- Shared resources are clearly marked
- Users can share their resources through UI
- Alpha testers have smooth experience

---

## Requirements

### Phase 1: Permission Context (1 hour)
- [ ] Add `currentUser` with role to React context
- [ ] Pass role information from backend
- [ ] Create `usePermissions()` hook
- [ ] Test role detection works

### Phase 2: Permission-Aware Components (2 hours)
- [ ] Create `<CanEdit>` wrapper component
- [ ] Create `<CanDelete>` wrapper component
- [ ] Create `<CanShare>` wrapper component
- [ ] Hide wrapped content based on permissions
- [ ] Apply to Lists, Todos, Projects UI

### Phase 3: Sharing Indicators (1 hour)
- [ ] Add "Shared" badge to shared resources
- [ ] Show owner name if not current user
- [ ] Display current user's role (Viewer/Editor/Admin)
- [ ] Style indicators consistently

### Phase 4: Basic Sharing Modal (2 hours)
- [ ] Create share button on owned resources
- [ ] Modal with email input field
- [ ] Role selector (Viewer/Editor/Admin)
- [ ] List of current shares with remove option
- [ ] API calls to add/remove shares
- [ ] Success/error feedback

---

## Acceptance Criteria

### Functionality
- [ ] Viewers cannot see Edit/Delete buttons
- [ ] Editors can see Edit but not Delete
- [ ] Admins can see all actions
- [ ] Shared resources show visual indicators
- [ ] Sharing modal successfully adds shares
- [ ] Remove share functionality works

### Testing
- [ ] Test as Viewer - verify restricted UI
- [ ] Test as Editor - verify appropriate access
- [ ] Test as Owner - verify full access
- [ ] Test as Admin - verify override access
- [ ] Test sharing flow end-to-end

### UX
- [ ] No 403 errors during normal use
- [ ] Clear visual feedback about permissions
- [ ] Intuitive sharing interface
- [ ] Consistent permission indicators

---

## Technical Approach

### Backend Already Provides
- User role in JWT token
- Ownership info in API responses
- Sharing endpoints ready

### Frontend Needs To
```javascript
// Context setup
const PermissionContext = createContext({
  currentUser: null,
  canEdit: (resource) => false,
  canDelete: (resource) => false,
  canShare: (resource) => false,
});

// Wrapper component example
function CanEdit({ resource, children }) {
  const { canEdit } = usePermissions();
  if (!canEdit(resource)) return null;
  return children;
}

// Usage
<CanDelete resource={list}>
  <Button onClick={deleteList}>Delete</Button>
</CanDelete>
```

---

## Success Metrics

- Zero 403 errors in alpha testing
- Alpha testers successfully share resources
- No confusion about permissions in feedback

---

## Notes

This is the final UX piece needed before Michelle (our first external alpha tester) arrives tomorrow. Backend security is solid - this just makes it visible and user-friendly.

---

## References

- Issue #357: SEC-RBAC implementation (complete)
- ADR-044: Lightweight RBAC architecture
- Current frontend: `web/static/js/`

---

_Issue created: November 23, 2025_
_Target completion: Today_
_First alpha user: Tomorrow!_
