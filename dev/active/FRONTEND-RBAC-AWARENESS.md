# FRONTEND-RBAC-AWARENESS - Frontend Permission Awareness & Sharing UI

**Priority**: P0 (Alpha blocking)
**Labels**: `frontend`, `rbac`, `alpha-prep`, `ux`
**Milestone**: Sprint A9 (Final Alpha Prep)
**Epic**: Alpha Launch
**Related**: Issue #357 (SEC-RBAC), ADR-044 (Lightweight RBAC)

---

## Problem Statement

### Current State
Backend RBAC implementation is complete and properly enforces permissions. The frontend application has no awareness of user roles or permissions, resulting in:
- All UI elements visible to all users regardless of permissions
- Actions that will fail (403) are still presented to users
- No visual indication when viewing shared resources
- No UI mechanism to share resources with other users

### Impact
- **Blocks**: Smooth alpha user experience (Michelle arrives tomorrow!)
- **User Impact**: Confusion when actions fail, no way to share resources, poor first impression
- **Technical Debt**: Support burden from permission-related confusion

### Strategic Context
Backend security is complete. This is the final technical work before alpha launch. Making permissions visible in the UI will dramatically improve the alpha testing experience.

---

## Goal

**Primary Objective**: Create permission-aware UI components and basic sharing functionality

**Example User Experience**:
```
BEFORE:
- Viewer clicks "Delete" → 403 error → confusion
- Owner wants to share list → no UI → uses workaround

AFTER:
- Viewer doesn't see "Delete" button at all
- Owner clicks "Share" → adds collaborator → smooth experience
```

**Not In Scope** (explicitly):
- ❌ Complex permission hierarchies
- ❌ Team-based sharing
- ❌ Bulk operations
- ❌ Advanced admin UI

---

## What Already Exists

### Infrastructure ✅ (if any)
- Backend provides user role in JWT token
- Backend provides ownership info in API responses
- Sharing endpoints implemented and working
- Role-based permissions enforced server-side

### What's Missing ❌
- Frontend role context/state management
- Permission-aware UI components
- Visual indicators for shared resources
- UI for sharing resources

---

## Requirements

### Phase 0: Investigation & Setup
- [ ] Verify current frontend framework/structure
- [ ] Identify where user context is stored
- [ ] Locate Lists/Todos/Projects components
- [ ] Check for existing permission patterns

### Phase 1: Permission Context Setup
**Objective**: Establish user role awareness in frontend

**Tasks**:
- [ ] Add currentUser with role to application state
- [ ] Extract role from JWT or API response
- [ ] Create usePermissions() hook or equivalent
- [ ] Verify role detection works

**Deliverables**:
- User context available throughout app
- Console logs showing correct role

### Phase 2: Permission-Aware Components
**Objective**: Hide actions users cannot perform

**Tasks**:
- [ ] Create CanEdit wrapper component
- [ ] Create CanDelete wrapper component
- [ ] Create CanShare wrapper component
- [ ] Apply wrappers to Lists UI elements
- [ ] Apply wrappers to Todos UI elements
- [ ] Apply wrappers to Projects UI elements

**Deliverables**:
- Components that conditionally render based on permissions
- No inappropriate actions visible to restricted users

### Phase 3: Sharing Status Indicators
**Objective**: Show users when resources are shared

**Tasks**:
- [ ] Add "Shared" badge component
- [ ] Display owner name when not current user
- [ ] Show current user's role (Viewer/Editor/Admin)
- [ ] Apply indicators to list views
- [ ] Style consistently across resource types

**Deliverables**:
- Visual feedback about resource ownership and sharing

### Phase 4: Basic Sharing Modal
**Objective**: Enable users to share their resources

**Tasks**:
- [ ] Create Share button on owned resources
- [ ] Build modal with email input
- [ ] Add role selector (Viewer/Editor/Admin)
- [ ] Display current shares with remove option
- [ ] Wire API calls for add/remove shares
- [ ] Add success/error feedback

**Deliverables**:
- Functional sharing interface
- Users can manage resource sharing

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met
- [ ] Manual testing completed
- [ ] No regressions confirmed
- [ ] Documentation updated
- [ ] GitHub issue updated with evidence
- [ ] Ready for PM approval

---

## Acceptance Criteria

### Functionality
- [ ] Viewers see only appropriate actions (PM will validate)
- [ ] Editors see edit but not delete actions (PM will validate)
- [ ] Owners see all actions for their resources (PM will validate)
- [ ] Admins see all actions globally (PM will validate)
- [ ] Shared resources display visual indicators (PM will validate)
- [ ] Sharing modal successfully adds/removes shares (PM will validate)

### Testing
- [ ] Manual test as Viewer role
- [ ] Manual test as Editor role
- [ ] Manual test as Owner role
- [ ] Manual test as Admin role
- [ ] Test sharing flow end-to-end
- [ ] Verify no 403 errors in normal use

### Quality
- [ ] No regressions introduced
- [ ] Performance unchanged (<100ms render)
- [ ] Consistent UX across resource types
- [ ] Clear error messages if operations fail

### Documentation
- [ ] Code comments for permission logic
- [ ] Update frontend README if needed
- [ ] Session log completed

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Permission Context | ❌ | [pending] |
| CanEdit Component | ❌ | [pending] |
| CanDelete Component | ❌ | [pending] |
| CanShare Component | ❌ | [pending] |
| Lists UI Integration | ❌ | [pending] |
| Todos UI Integration | ❌ | [pending] |
| Projects UI Integration | ❌ | [pending] |
| Shared Badge | ❌ | [pending] |
| Sharing Modal | ❌ | [pending] |
| API Integration | ❌ | [pending] |

**Definition of COMPLETE**:
- ✅ ALL acceptance criteria checked by PM
- ✅ Evidence provided (screenshots, console output)
- ✅ No known issues remaining
- ✅ Manual testing verified all roles

---

## Testing Strategy

### Manual Testing Scenarios

**Scenario 1**: Viewer Restrictions
1. [ ] Login as viewer role user
2. [ ] Navigate to shared list
3. [ ] Verify no Edit button visible
4. [ ] Verify no Delete button visible
5. [ ] Verify can view content

**Scenario 2**: Owner Capabilities
1. [ ] Login as resource owner
2. [ ] Navigate to owned list
3. [ ] Verify all actions visible
4. [ ] Click Share button
5. [ ] Add collaborator successfully
6. [ ] Remove collaborator successfully

**Scenario 3**: Admin Override
1. [ ] Login as admin user
2. [ ] Navigate to any resource
3. [ ] Verify all actions visible
4. [ ] Verify can perform all actions

---

## Success Metrics

### Quantitative
- Zero 403 errors during normal alpha use
- All role-based tests passing
- <100ms additional render time

### Qualitative
- Alpha testers understand permissions intuitively
- No permission-related support requests
- Smooth sharing experience

---

## STOP Conditions

**STOP immediately and escalate if**:
- Frontend framework unknown or different than expected
- No user context system exists
- JWT/auth system incompatible with approach
- Sharing APIs don't exist or don't work
- Performance degrades >500ms
- Security vulnerabilities discovered
- Breaking changes to existing functionality

**When stopped**: Document findings, propose alternatives, wait for PM decision

---

## Effort Estimate

**Overall Size**: Medium (4-6 hours)

**Breakdown by Phase**:
- Phase 0: 30 minutes (investigation)
- Phase 1: 1 hour (context setup)
- Phase 2: 2 hours (permission components)
- Phase 3: 1 hour (sharing indicators)
- Phase 4: 2 hours (sharing modal)
- Testing: 30 minutes
- Documentation: 30 minutes

**Complexity Notes**:
- Unknown frontend framework details
- Possible state management complexity
- API integration uncertainty

---

## Dependencies

### Required (Must be complete first)
- [x] #357 - SEC-RBAC implementation (COMPLETE)
- [ ] Backend sharing endpoints operational (needs verification)
- [ ] Frontend build system working (needs verification)

### Optional (Nice to have)
- [ ] Design system/component library

---

## Related Documentation

- **Architecture**: ADR-044 (Lightweight RBAC)
- **Backend**: Issue #357 completion evidence
- **API**: Sharing endpoints documentation (location TBD)

---

## Evidence Section

[To be filled during implementation]

### Implementation Evidence
```bash
# Build verification
# Console output showing role detection
# Screenshots of permission-aware UI
# Sharing flow demonstration
```

### Manual Testing Evidence
- [ ] Viewer test screenshots
- [ ] Editor test screenshots
- [ ] Owner test screenshots
- [ ] Admin test screenshots
- [ ] Sharing modal screenshots

---

## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met ✅
- [ ] Completion matrix 100% ✅
- [ ] Evidence provided for each component ✅
- [ ] Manual tests completed ✅
- [ ] Documentation updated ✅
- [ ] No regressions confirmed ✅
- [ ] STOP conditions all clear ✅
- [ ] Session log complete ✅
- [ ] GitHub issue updated ✅

**Status**: Not Started

---

## Notes for Implementation

Frontend framework investigation needed first. Do not assume React/Vue/vanilla JS - verify actual implementation. Sharing endpoints should exist from SEC-RBAC work but verify they're accessible and documented.

---

**Remember**:
- Quality over speed (Time Lord philosophy)
- Evidence required for all claims
- No 80% completions
- PM closes issues after approval

---

_Issue created: November 23, 2025_
_Last updated: November 23, 2025_
_Target: Complete today for Michelle tomorrow!_
