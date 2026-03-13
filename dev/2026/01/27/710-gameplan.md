# Gameplan: #710 MUX-WORKITEMS-VIEW

**Issue**: #710 MUX-WORKITEMS-VIEW
**Type**: Create new view (Medium)
**Date**: 2026-01-27
**Pattern**: Follows #708/#709 but creates NEW template + route

---

## Phase -1: Infrastructure Verification ✅

### Verified from code:

**Domain Model** (`services/domain/models.py`):
- [x] WorkItem class exists (lines 250-305)
- [x] Has `lifecycle_state: Optional[LifecycleState] = None` (line 274)
- [x] Has `to_dict()` with lifecycle serialization

**Database Model** (`services/database/models.py`):
- [x] `WorkItem` class exists (lines 294-342) - NOTE: not "WorkItemDB"
- [x] Has `lifecycle_state` column from #718 migration
- [ ] `to_domain()` does NOT map lifecycle_state (lines 325-342) - **NEEDS FIX**

**API Routes**:
- [ ] No `/api/v1/work-items` endpoint exists - **NEEDS CREATION**

**Templates**:
- [ ] No `work_items.html` exists - **NEEDS CREATION**

**Navigation** (`templates/components/navigation.html`):
- [x] "Your stuff" dropdown exists (lines 528-541)
- [x] Pattern: `<a href="/todos" class="nav-dropdown-item">To-dos</a>`
- [ ] No work items link - **NEEDS ADDITION**

### Decision: PROCEED with known work items:
1. Fix WorkItem.to_domain() to map lifecycle_state
2. Create work items API endpoint
3. Create work_items.html template
4. Add navigation link

---

## Phase 0: Database Model Fix

### Objective
Fix WorkItem.to_domain() to map lifecycle_state (same issue as #718 for ProjectDB).

### Tasks
1. Add lifecycle_state column definition to WorkItem class (if missing)
2. Update to_domain() to convert string → LifecycleState enum

### Files
- `services/database/models.py` - WorkItem class (lines 294-342)

### Pattern (from ProjectDB fix)
```python
# In to_domain():
lifecycle_state = None
if self.lifecycle_state:
    try:
        lifecycle_state = LifecycleState(self.lifecycle_state)
    except ValueError:
        pass
# Add to WorkItem constructor
```

---

## Phase 1: API Endpoint

### Objective
Create `/api/v1/work-items` endpoint returning work items with lifecycle_state.

### Tasks
1. Create `web/api/routes/work_items.py`
2. Implement `list_work_items()` endpoint
3. Register router in main app
4. Include lifecycle_state in response

### Files
- `web/api/routes/work_items.py` (NEW)
- `main.py` or router registration file

### Pattern (from todos.py/projects.py)
```python
@router.get("")
async def list_work_items(
    current_user: JWTClaims = Depends(get_current_user),
    # ... repository dependency
) -> dict:
    work_items = await repo.list_work_items(owner_id=current_user.sub)
    return {
        "work_items": [
            {
                "id": w.id,
                "title": w.title,
                "type": w.type,
                "status": w.status,
                "lifecycle_state": w.lifecycle_state.value if w.lifecycle_state else None,
                # ... other fields
            }
            for w in work_items
        ],
        "count": len(work_items),
    }
```

---

## Phase 2: Template Creation

### Objective
Create work_items.html following projects.html pattern.

### Tasks
1. Create `templates/work_items.html`
2. Include lifecycle_indicator.html component
3. Implement renderWorkItems() JS with lifecycle indicator
4. Handle empty state

### Files
- `templates/work_items.html` (NEW)

### Key Elements
- Breadcrumb: Home → Work Items
- Page header with title
- JS fetch from `/api/v1/work-items`
- renderWorkItems() with lifecycle indicator pattern
- Empty state component

---

## Phase 3: Route & Navigation

### Objective
Wire view into application.

### Tasks
1. Add UI route in `web/api/routes/ui.py` for `/work-items`
2. Add navigation link in "Your stuff" dropdown
3. Add to stuffLinks JS object for active state

### Files
- `web/api/routes/ui.py`
- `templates/components/navigation.html`

### Navigation Pattern
```html
<a href="/work-items" class="nav-dropdown-item" id="nav-work-items">Work Items</a>
```

### JS Active State
```javascript
const stuffLinks = {
    '/todos': 'nav-todos',
    '/projects': 'nav-projects',
    '/work-items': 'nav-work-items',  // ADD
    ...
};
```

---

## Phase Z: Completion

- [ ] WorkItem.to_domain() fixed
- [ ] API endpoint working
- [ ] Template renders correctly
- [ ] Navigation link works
- [ ] Manual test: work item with lifecycle shows indicator
- [ ] Manual test: empty state works
- [ ] GitHub issue updated
- [ ] Session log updated

---

## Success Criteria

- [ ] `/work-items` page loads without errors
- [ ] Work items display with title, type, status
- [ ] Lifecycle indicator shows when lifecycle_state present
- [ ] Empty state shows when no work items
- [ ] Navigation "Your stuff" → "Work Items" works

---

## STOP Conditions

- WorkItem repository doesn't exist or has different interface
- Unexpected authentication requirements
- Template structure significantly different from projects.html

---

*Gameplan created: 2026-01-27 3:28 PM*
*Status: Ready for execution*
