# Gameplan: Frontend RBAC Permission Awareness
**Issue**: #[TBD] FRONTEND-RBAC-AWARENESS
**Date**: November 23, 2025
**Priority**: P0 (Alpha blocking)
**Estimated Duration**: 4-6 hours

---

## Mission Statement

Implement frontend permission awareness to prevent user confusion and enable resource sharing before Michelle (first alpha tester) arrives tomorrow. Backend RBAC is complete and working - this makes it visible and user-friendly.

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Chief Architect's Current Understanding

**Infrastructure Status** (needs PM verification):
- [ ] Web framework: ____________ (Unknown - could be React/Vue/vanilla)
- [ ] State management: ____________ (Unknown - Redux/Context/other)
- [ ] Component structure: ____________ (Unknown - location of Lists/Todos/Projects)
- [ ] Auth system: ____________ (JWT exists but frontend integration unknown)
- [ ] Build system: ____________ (Unknown - webpack/vite/other)
- [ ] Existing permission code: ____________ (Probably none)

**My understanding of the task**:
- Backend RBAC is complete (Issue #357)
- Frontend has no permission awareness
- Need to add permission-aware components
- Need to add sharing UI
- Michelle arrives tomorrow for alpha testing

### Part B: PM Verification Required

**PM, please provide**:

1. **Frontend structure check**:
   ```bash
   ls -la web/
   ls -la web/static/
   ls -la web/static/js/
   find web/ -name "*.jsx" -o -name "*.vue" -o -name "*.js" | head -20
   ```

2. **Current auth implementation**:
   - Where is user context stored?
   - How is JWT handled?
   - Any existing user state management?

3. **Component locations**:
   - Where are Lists components?
   - Where are Todos components?
   - Where are Projects components?

4. **Known issues**:
   - Any frontend build issues?
   - Any state management quirks?
   - Previous permission attempts?

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** - Framework identified, approach valid
- [ ] **REVISE** - Different framework needs different approach
- [ ] **CLARIFY** - Need more context on: ____________

---

## Phase 0: Initial Investigation

### Purpose
Understand current frontend implementation and identify integration points

### Required Actions

1. **Examine Frontend Structure**
   ```bash
   # Identify framework
   find web/ -type f -name "*.js" -o -name "*.jsx" | xargs grep -l "React\|Vue\|Angular" | head -5

   # Find user/auth code
   grep -r "user\|auth\|jwt\|token" web/static/ --include="*.js"

   # Locate resource components
   grep -r "List\|Todo\|Project" web/static/ --include="*.js" | grep -i component
   ```

2. **Verify Backend Integration**
   ```bash
   # Check API responses include role/ownership
   curl -X GET http://localhost:8001/api/lists \
     -H "Authorization: Bearer $TOKEN" | jq '.'

   # Verify sharing endpoints exist
   curl -X POST http://localhost:8001/api/lists/[id]/share
   ```

3. **Document Findings**
   - Frontend framework: _____
   - State management approach: _____
   - Component file locations: _____
   - API integration pattern: _____

### STOP Conditions
- No frontend code found
- Completely different architecture than expected
- No API endpoints for sharing

---

## Phase 1: Permission Context Implementation

### Deploy: Lead Developer

**Objective**: Add user role awareness to frontend application

```markdown
## Your Task: Create Permission Context

1. Add user context to application state:
   - Extract user info from JWT or API response
   - Store current user ID and role
   - Make available throughout app

2. Create permission helper functions:
   - canEdit(resource, user)
   - canDelete(resource, user)
   - canShare(resource, user)
   - isOwner(resource, user)
   - isAdmin(user)

3. Verify with console logging:
   - Log current user on load
   - Log permission checks
   - Confirm role detection works

DO NOT guess at framework - use what exists
```

### Progressive Bookending
```bash
gh issue comment [ISSUE_NUMBER] -b "✅ Phase 1 Complete: Permission context added
- User role extracted from [JWT/API]
- Helper functions created
- Console logs confirm working"
```

---

## Phase 2: Permission-Aware Components

### Deploy: Lead Developer + Code Agent (Parallel)

**Objective**: Create wrapper components that hide inappropriate actions

#### Lead Developer Instructions
```markdown
## Create Permission Wrapper Components

Based on the framework found in Phase 0, create:

1. CanEdit component - renders children only if user can edit
2. CanDelete component - renders children only if user can delete
3. CanShare component - renders children only if user is owner

Use the permission helpers from Phase 1.
Make them easy to wrap around existing buttons/actions.
```

#### Code Agent Instructions
```markdown
## Apply Permission Wrappers to UI

Find all Edit/Delete/Share buttons in:
- Lists components
- Todos components
- Projects components

Wrap each with appropriate permission component:
- Edit buttons → CanEdit wrapper
- Delete buttons → CanDelete wrapper
- Share buttons → CanShare wrapper

Maintain existing styling and behavior.
```

### Cross-Validation
- Both agents verify no unwrapped actions remain
- Test manually with different user roles

---

## Phase 3: Sharing Status Indicators

### Deploy: Code Agent

**Objective**: Add visual feedback for shared resources

```markdown
## Add Sharing Indicators

1. Create SharedBadge component:
   - Shows "Shared" label
   - Displays owner name if not current user
   - Shows current user's role

2. Add to resource list views:
   - Lists index page
   - Todos index page
   - Projects index page

3. Add to resource detail views:
   - Individual list view
   - Individual todo view
   - Individual project view

4. Consistent styling:
   - Use existing badge/label patterns
   - Ensure visibility but not intrusive
```

---

## Phase 4: Sharing Modal Implementation

### Deploy: Lead Developer

**Objective**: Create UI for sharing resources

```markdown
## Build Sharing Modal

1. Create Share button (only on owned resources)

2. Build modal with:
   - Email input field
   - Role selector (Viewer/Editor/Admin)
   - Current shares list
   - Remove button for each share

3. Wire API calls:
   - POST to add share
   - DELETE to remove share
   - GET to list current shares

4. Add feedback:
   - Success messages
   - Error handling
   - Loading states

5. Apply to:
   - Lists
   - Todos
   - Projects

Use framework patterns found in Phase 0.
```

---

## Phase Z: Final Verification & Handoff

### Purpose
Verify all permission features work correctly for alpha launch

### Required Actions

1. **Manual Testing Matrix**
   ```
   | Role   | Can See | Can't See | Can Do | Can't Do |
   |--------|---------|-----------|--------|----------|
   | Viewer | Content | Delete btn| View   | Edit     |
   | Editor | Edit btn| Delete btn| Edit   | Delete   |
   | Owner  | All btns| -         | All    | -        |
   | Admin  | All btns| -         | All    | -        |
   ```

2. **Evidence Collection**
   - Screenshot each role's view
   - Record sharing flow
   - Capture console logs showing permissions

3. **GitHub Update**
   ```bash
   gh issue edit [ISSUE_NUMBER] --body "
   ## Status: Complete - Ready for PM Review

   ### Evidence
   - Permission context working: ✅
   - Actions hidden based on role: ✅
   - Sharing indicators visible: ✅
   - Sharing modal functional: ✅

   ### Testing Completed
   - Viewer role tested: ✅
   - Editor role tested: ✅
   - Owner capabilities verified: ✅
   - Admin override confirmed: ✅

   ### Ready for Alpha
   No 403 errors in normal use.
   Michelle can arrive tomorrow!
   "
   ```

4. **Documentation Updates**
   - [ ] Update frontend README with permission system
   - [ ] Document any new components created
   - [ ] Note any limitations for alpha

5. **PM Approval Request**
   ```
   @PM - Frontend RBAC complete:
   - All roles properly restricted ✅
   - Sharing UI functional ✅
   - No regressions ✅
   - Ready for Michelle tomorrow ✅
   ```

---

## Success Criteria

- [ ] No visible actions that would fail with 403
- [ ] Shared resources clearly marked
- [ ] Owners can share their resources
- [ ] All user roles tested manually
- [ ] Zero console errors related to permissions
- [ ] Performance unchanged (<100ms impact)

---

## STOP Conditions

**STOP and escalate if**:
- Frontend is not web-based (mobile app?)
- No authentication system exists
- Sharing APIs missing or broken
- Major framework discovery (Angular when expecting React)
- Performance degrades >500ms
- Security issues discovered

---

## Evidence Requirements

### Must Provide
- Screenshots of each role's view
- Console output showing permission checks
- Video/GIF of sharing flow
- Test results for each role

### Not Acceptable
- "Permissions working" without screenshots
- "Tested all roles" without evidence
- "Should work" without verification

---

## Risk Mitigation

**If framework is unknown**: Investigate thoroughly in Phase 0
**If no state management exists**: Create minimal solution
**If sharing APIs missing**: Document and escalate immediately
**If performance issues**: Profile and identify bottleneck

---

## Session Completion

- Satisfaction: [To be filled]
- Blockers encountered: [To be filled]
- Discoveries for future: [To be filled]
- Process improvements: [To be filled]

---

**Remember**:
- Complete each phase 100% before proceeding
- Evidence required for all claims
- PM validation required for acceptance criteria
- Michelle arrives tomorrow - this enables smooth alpha experience!

---

*Gameplan prepared by: Chief Architect*
*Date: November 23, 2025*
*For: Lead Developer + Code Agent*
