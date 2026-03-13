# Gameplan: #703 MUX-LIFECYCLE-UI

**Issue**: #703 MUX-LIFECYCLE-UI: Lifecycle indicator integration for object displays
**Created**: 2026-01-26
**Author**: Lead Developer

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Testing framework: pytest
- [x] UI Components: lifecycle_indicator.html, lifecycle_detail.html, lifecycle_notification.html exist
- [x] JavaScript API: LifecycleIndicator.create(stage, compact) available
- [x] Backend: WorkItem.to_dict() includes lifecycle_state

**My understanding of the task**:
- I believe we need to: Integrate existing lifecycle UI components into views that display lifecycle-aware objects
- I think this involves: Including lifecycle_indicator.html in templates, adding JavaScript to render indicators
- I assume the current state is: Components exist and are tested but not used in any production templates

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel
- [ ] Task duration >30 minutes
- [ ] Multi-component work
- [x] Exploratory/risky changes where easy rollback is valuable

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [ ] Tightly coupled files
- [ ] Time-critical work

**Assessment**: **SKIP WORKTREE** - Single agent exploration, primarily investigation phase

### Part B: PM Verification Required

**PM, please correct/confirm**:

1. **What actually exists?**
   - Lifecycle components at `templates/components/lifecycle_*.html`
   - WorkItem.to_dict() returns lifecycle_state
   - No templates currently include lifecycle components

2. **Recent work in this area?**
   - #685 just completed backend wiring
   - #423 created UI components (CLOSED)

3. **Actual task needed?**
   - [x] Add to existing application (integrate components into existing templates)

4. **Critical context I'm missing?**
   - Which templates actually render WorkItem/Feature objects?

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** - After PM verification
- [ ] **REVISE** - If assumptions wrong
- [ ] **CLARIFY** - Which views to target

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**: ✅ #703 exists and is properly formatted

2. **Codebase Investigation**:
   ```bash
   # Find templates that might display lifecycle-aware objects
   grep -rn "WorkItem\|Feature\|Insight" templates/ --include="*.html"

   # Check API endpoints returning objects
   grep -rn "lifecycle_state\|to_dict" web/api/routes/ --include="*.py"

   # Verify lifecycle components exist
   ls templates/components/lifecycle_*.html
   ```

3. **Questions to answer**:
   - Which templates display WorkItem/Feature objects?
   - Which API endpoints return lifecycle_state?
   - What's the best integration point (insights page likely candidate)?

4. **Update GitHub Issue**:
   ```bash
   gh issue edit 703 --body "[updated body with]
   ## Status: Investigation Started
   - [ ] Templates identified that display lifecycle objects
   - [ ] API endpoints verified to return lifecycle_state
   - [ ] Integration approach determined
   "
   ```

---

## Phase 0.5: Frontend-Backend Contract Verification

### When to Apply
- ✅ Creating UI that displays data from backend API
- ✅ Adding JavaScript that reads lifecycle_state from API responses

### Required Actions

#### 1. Verify API Returns lifecycle_state
```bash
# Check WorkItem.to_dict() includes lifecycle_state
grep -A 30 "def to_dict" services/domain/models.py | grep lifecycle
```

#### 2. Verify JavaScript API Exists
```bash
# Check LifecycleIndicator.create exists
grep -n "LifecycleIndicator.create\|window.LifecycleIndicator" templates/components/lifecycle_indicator.html
```

#### 3. Document Integration Pattern
```markdown
| Data Source | Field | JS API | Element Created |
|-------------|-------|--------|-----------------|
| API response | lifecycle_state | LifecycleIndicator.create(state, compact) | .lifecycle-indicator |
```

#### 4. Evidence Required
```bash
# Document verified integration points
echo "Verified:"
echo "  WorkItem.to_dict() includes lifecycle_state ✓"
echo "  LifecycleIndicator.create() API available ✓"
echo "  Target template identified: [template name]"
```

---

## Phase -1 Investigation: Detailed Tasks

### Task 1: Identify Templates That Could Display Lifecycle Objects

**Target templates to check**:
1. `templates/insights.html` - Displays Insight objects (composted = lifecycle?)
2. `templates/projects.html` - Displays Projects (do they have lifecycle?)
3. `templates/standup.html` - May reference WorkItems
4. `templates/todos.html` - May display task-like objects
5. Chat responses - May describe WorkItems/Features

**For each template, document**:
- Does it fetch objects via API?
- Does the API return lifecycle_state?
- Is there a render function that could add indicators?

### Task 2: Identify Best First Integration Point

**Criteria for ideal first integration**:
1. Objects already have lifecycle_state in backend
2. JavaScript already fetches and renders objects
3. Clear visual location to add indicator
4. Minimal risk of breaking existing functionality

**Likely candidate**: Insights page
- Insights may have lifecycle_state (COMPOSTED = "I learned that...")
- Already has confidence indicators (pattern to follow)
- Self-contained page

### Task 3: Document Trust-Gating Approach

**Current trust-gating**:
- lifecycle_notification.html uses `data-min-stage="3"`
- Should lifecycle_indicator also be trust-gated?

**Recommendation**: Indicators should NOT be trust-gated
- They're informational, not actionable
- Users should see lifecycle state at any trust level
- Notifications (actions) are different from indicators (status)

---

## Phase 1: First Integration

### Objective
Integrate lifecycle indicator into one view

### Approach

1. **Include component in template**:
   ```html
   {% include 'components/lifecycle_indicator.html' %}
   ```

2. **Add JavaScript to render indicator**:
   ```javascript
   function renderLifecycleIndicator(container, lifecycleState) {
     if (!lifecycleState || !window.LifecycleIndicator) return;
     const indicator = LifecycleIndicator.create(lifecycleState, true); // compact mode
     container.appendChild(indicator);
   }
   ```

3. **Call in existing render function**:
   ```javascript
   // In existing object rendering code
   if (object.lifecycle_state) {
     renderLifecycleIndicator(objectElement, object.lifecycle_state);
   }
   ```

### Deliverables
- Modified template with lifecycle_indicator include
- JavaScript function to render indicators
- Integration into existing render function

---

## Phase 2: Testing & Polish

### Unit Tests
```python
def test_indicator_renders_when_lifecycle_present():
    """Template includes indicator when object has lifecycle_state."""

def test_indicator_not_rendered_when_no_lifecycle():
    """Template omits indicator when lifecycle_state is None."""

def test_indicator_shows_experience_phrase():
    """Indicator text matches experience phrase for state."""
```

### Manual Testing
1. Navigate to integrated view
2. Verify indicator visible for objects with lifecycle_state
3. Hover to see tooltip with experience phrase
4. Verify no technical labels shown

---

## Phase Z: Completion & Handoff

### Required Evidence
- [ ] Template modified with lifecycle_indicator include
- [ ] JavaScript wiring code
- [ ] Tests added and passing
- [ ] Screenshot of indicator in UI
- [ ] No regressions in existing UI tests

### Documentation Updates
- [ ] Update lifecycle-experience-guide.md if integration pattern differs
- [ ] Add integration notes to lifecycle_indicator.html comments
- [ ] Session log completed with all evidence

### GitHub Update
```bash
gh issue edit 703 --body "[full body with]
## Status: Complete - Awaiting PM Approval

### Evidence
- Template: [modified file]
- Tests: [test output]
- Screenshot: [link or description]
- No regressions: [pytest output]
"
```

---

## STOP Conditions

- No templates found that display lifecycle-aware objects
- JavaScript API doesn't work as documented
- Existing UI tests fail after integration
- Performance degrades visibly

---

## Effort Estimate

| Phase | Size | Notes |
|-------|------|-------|
| Phase -1 | Small | Investigation |
| Phase 0/0.5 | Small | Verification |
| Phase 1 | Medium | Integration |
| Phase 2 | Small | Testing |
| Phase Z | Small | Documentation |

**Total**: Medium

---

## Dependencies

- [x] #685 MUX-LIFECYCLE-OBJECTS - Backend returns lifecycle_state ✅
- [x] #423 MUX-IMPLEMENT-LIFECYCLE - UI components exist ✅

---

*Gameplan Version: 1.0*
*Created: 2026-01-26*
