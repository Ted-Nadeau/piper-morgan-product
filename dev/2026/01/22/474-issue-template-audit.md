# Issue Template Audit: #474 MUX-TECH-LISTS: Enable full list management

## Feature Template Checklist

| Template Section | Present in #474? | Notes |
|------------------|------------------|-------|
| **Header** | | |
| Priority | ❌ Missing | "Backlog - Feature completion" is informal |
| Labels | ⚠️ Minimal | Only "enhancement" label |
| Milestone | ❌ Missing | No sprint assignment |
| Epic | ❌ Missing | Should link to #629 MUX-LISTS |
| Related | ❌ Missing | No related issues listed |
| **Problem Statement** | | |
| Current State | ✅ Yes | "Lists can be created and deleted, but items cannot be added" |
| Impact (Blocks/User/Debt) | ❌ Missing | No impact analysis |
| Strategic Context | ❌ Missing | No context about MUX or L1 sprint |
| **Goal** | | |
| Primary Objective | ⚠️ Implicit | Required Functionality list implies goal |
| Example User Experience | ❌ Missing | No before/after scenario |
| Not In Scope | ❌ Missing | Reorder marked "nice to have" but no formal scope section |
| **What Already Exists** | | |
| Infrastructure ✅ | ❌ Missing | What list code already exists? |
| What's Missing ❌ | ⚠️ Partial | "Edit button shows Coming soon" but no code analysis |
| **Requirements** | | |
| Phase 0: Investigation | ❌ Missing | No investigation phase |
| Phases 1-N | ❌ Missing | No phased breakdown |
| Phase Z: Completion | ❌ Missing | No handoff phase |
| **Acceptance Criteria** | ❌ Missing | No checkboxes |
| Functionality | ❌ Missing | Bullet points but no checkboxes |
| Testing | ❌ Missing | No test requirements |
| Quality | ❌ Missing | No quality gates |
| Documentation | ❌ Missing | No doc requirements |
| **Completion Matrix** | ❌ Missing | No matrix |
| **Testing Strategy** | ❌ Missing | No test scenarios |
| **Success Metrics** | ❌ Missing | No quantitative/qualitative measures |
| **STOP Conditions** | ❌ Missing | No explicit stop conditions |
| **Effort Estimate** | ❌ Missing | No size estimate |
| **Dependencies** | ❌ Missing | Not listed |
| **Related Documentation** | ❌ Missing | No resources section |

---

## Gap Summary

### Critical Gaps (Must Address)

1. **No epic linkage** - Should be child of #629 MUX-LISTS
2. **No phased implementation plan** - Just bullet points
3. **No acceptance criteria checkboxes** - Can't track completion
4. **No testing strategy** - UI/backend CRUD needs tests
5. **No infrastructure audit** - What exists in `services/list/`?

### Moderate Gaps (Should Address)

6. **No API contract specification** - What endpoints exist/needed?
7. **No frontend-backend contract** - Routes and JS calls
8. **No UI wireframe/description** - How should add/edit/delete work?
9. **No completion matrix** - Can't verify 100% done
10. **No STOP conditions** - When to halt work

### Minor Gaps (Nice to Have)

11. **Priority not formal** - "Backlog" is informal
12. **No effort estimate** - Size unknown
13. **Reorder scope unclear** - "nice to have" needs decision

---

## Investigation Questions (Phase 0 Content)

Before gameplan, need to answer:

1. **What list endpoints exist?**
   ```bash
   grep -r "lists" web/api/routes/ --include="*.py"
   ```

2. **What list repository methods exist?**
   ```bash
   grep -n "def.*" services/repositories/list_repository.py | head -20
   ```

3. **What list service exists?**
   ```bash
   ls -la services/list_service.py services/list/ 2>/dev/null
   ```

4. **What frontend exists for lists?**
   ```bash
   grep -r "lists" templates/ --include="*.html" | head -10
   ```

5. **What "Coming soon" message exists?**
   ```bash
   grep -r "Coming soon" templates/ web/ --include="*.html" --include="*.js"
   ```

---

## Proposed Issue Update

### Recommended Structure

```markdown
**Parent Epic**: #629 (MUX-LISTS)
**Sprint**: L1
**Priority**: P2 (Feature completion)
**Status**: Ready for Implementation

---

## Current State
Lists can be created and deleted, but items cannot be added to lists.
The "Edit" button currently shows "Coming soon".

## What Exists
- [ ] List endpoints: [to investigate]
- [ ] List repository: [to investigate]
- [ ] List templates: [to investigate]
- [ ] Item CRUD: [to investigate]

## Required Functionality

### Must Have
- [ ] Add items to a list
- [ ] Edit items in a list
- [ ] Delete items from a list

### Nice to Have (deferred)
- [ ] Reorder items via drag-drop

## Out of Scope
- List sharing/collaboration
- List templates
- Bulk operations

## Acceptance Criteria

### API
- [ ] POST /api/v1/lists/{id}/items - Add item
- [ ] PUT /api/v1/lists/{id}/items/{item_id} - Edit item
- [ ] DELETE /api/v1/lists/{id}/items/{item_id} - Delete item

### UI
- [ ] Add item form/input in list view
- [ ] Edit item inline or modal
- [ ] Delete item with confirmation
- [ ] Optimistic updates for responsiveness

### Testing
- [ ] Unit tests for repository methods
- [ ] Unit tests for service methods
- [ ] Integration tests for API endpoints
- [ ] E2E test for add/edit/delete flow

## Completion Matrix

| Criterion | Evidence Required | Status |
|-----------|------------------|--------|
| Add item API works | curl output | ⬜ |
| Edit item API works | curl output | ⬜ |
| Delete item API works | curl output | ⬜ |
| Add item UI works | Screenshot | ⬜ |
| Edit item UI works | Screenshot | ⬜ |
| Delete item UI works | Screenshot | ⬜ |
| Tests pass | pytest output | ⬜ |

## STOP Conditions
- If ListRepository missing required methods
- If List model needs schema changes
- If no clear UI pattern established
```

---

## Next Steps

1. **Run investigation commands** to fill in "What Exists" section
2. **Update issue #474** with complete structure
3. **Create gameplan** based on investigation findings
4. **Audit gameplan** against template v9.3
