# Gameplan: #709 MUX-LIFECYCLE-UI-PROJECTS

**Issue**: #709 MUX-LIFECYCLE-UI-PROJECTS
**Type**: Wire existing components (Small)
**Date**: 2026-01-27
**Pattern**: Follows #708 (Todo lifecycle) exactly

---

## Phase -1: Infrastructure Verification ✅

### Verified from code:
- [x] Project model at `services/domain/models.py` lines 333-395
- [x] `Project.to_dict()` exists at lines 371-395
- [x] No `lifecycle_state` on Project yet (has `mux_ownership` at line 349)
- [x] `projects.html` uses same JS rendering pattern as todos.html
- [x] API `list_projects()` uses inline dict (same as todos)
- [x] `lifecycle_indicator.html` component available

### Decision: PROCEED
Same architecture as #708 - apply identical pattern.

---

## Phase 0: Investigation ✅ (Completed above)

All verification done in Phase -1. No blockers found.

---

## Phase 1: Model Update

### Objective
Add optional lifecycle_state to Project model.

### Tasks
1. Add `lifecycle_state: Optional[LifecycleState] = None` after `mux_ownership` (line 349)
2. Update `to_dict()` to include lifecycle_state when present
3. Write unit test

### Files
- `services/domain/models.py` - Project class (lines 333-395)

### Pattern (from #708)
```python
# After mux_ownership field
lifecycle_state: Optional[LifecycleState] = None

# In to_dict(), after building result dict
if self.lifecycle_state is not None:
    result["lifecycle_state"] = self.lifecycle_state.value
```

---

## Phase 2: API Update

### Objective
Include lifecycle_state in list_projects() response.

### Tasks
1. Add `"lifecycle_state": p.lifecycle_state.value if p.lifecycle_state else None` to inline dict

### Files
- `web/api/routes/projects.py` - `list_projects()` function

---

## Phase 3: Template Integration

### Objective
Render lifecycle indicator in projects.html.

### Tasks
1. Add `{% include 'components/lifecycle_indicator.html' %}` after confirmation-dialog
2. Update `renderProjects()` to include lifecycle indicator (same pattern as todos)

### Files
- `templates/projects.html`

### Pattern (from #708)
```javascript
// Build lifecycle indicator
let lifecycleIndicator = '';
if (project.lifecycle_state && window.LifecycleIndicator) {
  const phrase = LifecycleIndicator.getPhrase(project.lifecycle_state);
  lifecycleIndicator = `
    <div class="lifecycle-indicator"
         data-lifecycle-stage="${project.lifecycle_state}"
         data-compact="true"
         ...>
    </div>
  `;
}
```

---

## Phase Z: Completion

- [ ] All tests pass
- [ ] No regressions
- [ ] GitHub issue updated
- [ ] Session log updated

---

## Success Criteria

- [ ] Projects with lifecycle_state show compact indicator
- [ ] Projects without lifecycle_state show no indicator
- [ ] Indicator shows experience phrase on hover
- [ ] Project CRUD still works

---

*Gameplan created: 2026-01-27*
*Status: Ready for execution (follows #708 pattern exactly)*
