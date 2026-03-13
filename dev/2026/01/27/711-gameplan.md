# Gameplan: #711 MUX-PROJECT-DETAIL-VIEW

**Date**: 2026-01-27 4:03 PM
**Author**: Lead Developer (Claude Code Opus)
**Issue**: #711 MUX-PROJECT-DETAIL-VIEW: Create Project Detail View with Lifecycle

---

## Investigation Summary

### What Exists ✅
1. **WorkItem.project_id field** - WorkItems can be linked to Projects
2. **GET /api/v1/projects/{id}** - Returns project (but missing lifecycle_state!)
3. **WorkItemRepository** with `list()` method from BaseRepository
4. **projects.html** - List view pattern (no detail click handler yet)
5. **work_items.html** - WorkItem display pattern with lifecycle
6. **lifecycle_indicator.html** component

### Gaps Found ❌
1. **GET project endpoint missing lifecycle_state** in response
2. **No endpoint to get work items by project_id**
3. **No click handler** in projects.html to navigate to detail
4. **No project_detail.html template**
5. **No /projects/{id} UI route** (distinct from API)

---

## Implementation Plan

### Phase 0: API Enhancements (Small)

**Task 0.1**: Update GET /api/v1/projects/{id} to include lifecycle_state
- File: `web/api/routes/projects.py` - `get_project()` function
- Add: `"lifecycle_state": getattr(project_obj, 'lifecycle_state', None).value if getattr(project_obj, 'lifecycle_state', None) else None`
- Pattern: Same as list_projects() already does

**Task 0.2**: Add endpoint GET /api/v1/projects/{id}/work-items
- File: `web/api/routes/projects.py`
- New function: `get_project_work_items(project_id, current_user, work_item_repo)`
- Query: Filter WorkItems where project_id matches
- Return: List of work items with lifecycle_state

**Deliverable**: API returns project with lifecycle + its work items

### Phase 1: Template Creation (Medium)

**Task 1.1**: Create `templates/project_detail.html`

Structure:
```
- Include navigation.html
- Include toast.html
- Include lifecycle_indicator.html
- Breadcrumb: Home > Projects > {Project Name}
- Project card with:
  - Name, description
  - Lifecycle indicator (if lifecycle_state)
  - Created/updated dates
- Work Items section:
  - If empty: "No work items for this project"
  - If items: List with lifecycle indicators (reuse work_items.html pattern)
```

Pattern: Combine projects.html (project display) + work_items.html (work item list)

**Deliverable**: `templates/project_detail.html`

### Phase 2: Route & Navigation (Small)

**Task 2.1**: Add UI route `/projects/{project_id}`
- File: `web/api/routes/ui.py`
- New function: `project_detail_ui(request, project_id)`
- Return: Render project_detail.html with user context + project_id

**Task 2.2**: Add click handler in projects.html
- File: `templates/projects.html`
- Make project title/card clickable → `/projects/{id}`
- Could be: `onclick="viewProject('${project.id}')"` or `<a href="/projects/${project.id}">`

**Deliverable**: Navigation flow complete

### Phase 3: Testing & Verification (Small)

**Manual Tests**:
1. Project with lifecycle, no work items → shows project lifecycle, empty work items message
2. Project with work items (some with lifecycle) → shows both indicators
3. Invalid project ID → 404 or error message
4. Breadcrumb navigation → returns to projects list
5. Click from list → navigates to detail

---

## File Changes Summary

| File | Change Type | Description |
|------|-------------|-------------|
| `web/api/routes/projects.py` | MODIFY | Add lifecycle_state to get_project, add get_project_work_items |
| `templates/project_detail.html` | CREATE | New detail view template |
| `web/api/routes/ui.py` | MODIFY | Add /projects/{id} route |
| `templates/projects.html` | MODIFY | Add click handler for detail navigation |

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| WorkItem filtering by project_id slow | Low | Simple WHERE clause, indexes exist |
| SEC-RBAC: work items from other users | Medium | Filter by current_user ownership |
| No test data | Low | Can seed via SQL like #710 |

---

## Effort Estimate

- Phase 0 (API): ~15 min
- Phase 1 (Template): ~20 min
- Phase 2 (Route/Nav): ~10 min
- Phase 3 (Testing): ~10 min

**Total**: ~55 min (Medium effort, as scoped)

---

## Success Criteria

1. Navigate to `/projects/{id}` shows project detail
2. Project lifecycle indicator displays when lifecycle_state set
3. Work items listed below with their lifecycle indicators
4. Breadcrumb navigation works
5. Click from projects list navigates to detail
6. Invalid project ID handled gracefully

---

## STOP Conditions

- If SEC-RBAC check for work items is complex → ask PM
- If work items endpoint requires new repository method → proceed (small scope)
- If template pattern significantly different from expectation → check with PM

---

**Status**: Ready for implementation upon PM approval
