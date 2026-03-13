# Gameplan: #708 MUX-LIFECYCLE-UI-TODOS

**Issue**: #708 MUX-LIFECYCLE-UI-TODOS
**Type**: Wire existing components (Small)
**Date**: 2026-01-27

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Database: PostgreSQL (port 5433)
- [x] Testing framework: pytest
- [x] Todo model: `services/domain/models.py`
- [x] Todos view: `templates/todos.html`
- [x] Lifecycle indicator: `templates/components/lifecycle_indicator.html`

**My understanding of the task**:
- Add optional `lifecycle_state` field to Todo model
- Update `Todo.to_dict()` to serialize lifecycle_state
- Wire `lifecycle_indicator.html` into `todos.html`
- Graceful degradation when lifecycle_state is None

### Part A.2: Work Characteristics Assessment

**Worktree Assessment**:
- [ ] Multiple agents in parallel - NO (single developer)
- [ ] Duration >30 min - MAYBE (~1.5 hrs total)
- [ ] Multi-component work - NO (model + template, same developer)
- [ ] Exploratory/risky - NO (well-defined wiring task)

**Decision**: ☐ SKIP WORKTREE
**Rationale**: Single developer, sequential work on 2-3 files, low risk.

### Part B: Self-Verification (Completed)

**Verified from code**:
1. ✅ Todo model at `services/domain/models.py` lines 1261-1441
2. ✅ `Todo.to_dict()` exists at lines 1394-1441
3. ✅ No existing lifecycle_state on Todo (only WorkItem line 274, Feature line 204)
4. ✅ Pattern: `lifecycle_state: Optional[LifecycleState] = None` with conditional serialization

**Discovery - Architecture Difference:**
- `todos.html` fetches data via JavaScript from `/api/v1/todos`
- API endpoint `list_todos()` in `web/api/routes/todos.py` manually constructs response (lines 246-258)
- **API does NOT use Todo.to_dict()** - inline dict with: id, text, status, priority, owner_id, created_at

**Lifecycle work in last 48 hours:**
- Commit c29f3a34: Feature.to_dict() + WorkItem.to_dict() lifecycle serialization (#705)
- No work on Todo lifecycle yet

### Part C: Decision - Option A Selected

**PM Decision (1:07 PM)**: Option A - minimal change, don't overload the hybrid model.

**Rationale**: Todos use a novel adaptation (simple status + optional lifecycle). Keep this ticket focused on lifecycle wiring, not API refactoring.

**Scope confirmed**:
- Add `lifecycle_state` field to Todo model
- Update `Todo.to_dict()` for completeness
- Update API `list_todos()` to include `lifecycle_state` in inline response
- Update JavaScript `renderTodos()` to render indicator

### Part C: Proceed/Revise

- [x] **PROCEED** - With Option A (PM confirmed 1:07 PM)

---

## Phase 0: Investigation

### 0.1 Verify Todo Model Structure
```bash
grep -n "class Todo" services/domain/models.py
grep -n "def to_dict" services/domain/models.py -A 20
```

**Looking for**:
- Todo class definition
- Current fields
- Existing to_dict() method
- Any existing lifecycle_state reference

### 0.2 Verify Todos Template Structure
```bash
head -50 templates/todos.html
grep -n "todo\." templates/todos.html
```

**Looking for**:
- How todos are iterated/rendered
- Where indicator should be placed
- Existing component includes

### 0.3 Verify Lifecycle Indicator API
```bash
head -30 templates/components/lifecycle_indicator.html
```

**Looking for**:
- Required parameters (state, compact, etc.)
- How to conditionally render

### 0.4 Verify Route Context
```bash
grep -n "todos" web/api/routes/ui.py -A 10
```

**Looking for**:
- What data is passed to template
- How to ensure lifecycle_state reaches template

### STOP Conditions
- Todo model not found at expected location
- Todo.to_dict() doesn't exist
- lifecycle_indicator.html API changed
- Route doesn't pass todo objects to template

---

## Phase 0.5: Frontend-Backend Contract

**Applies?** Partially - we're wiring template to model, not creating new API endpoints.

| Component | Path/Location | Verified? |
|-----------|---------------|-----------|
| Todo model | services/domain/models.py | [ ] |
| Todos template | templates/todos.html | [ ] |
| Lifecycle indicator | templates/components/lifecycle_indicator.html | [ ] |
| UI route | web/api/routes/ui.py | [ ] |

---

## Phase 0.6-0.8: Skip

- **Phase 0.6 (Data Flow)**: N/A - not multi-layer data flow
- **Phase 0.7 (Conversation Design)**: N/A - not conversational
- **Phase 0.8 (Post-Completion)**: N/A - no state changes beyond model field

---

## Phase 1: Model Update

### Objective
Add optional lifecycle_state to Todo model with proper serialization.

### Tasks
1. Add `lifecycle_state: Optional[LifecycleState] = None` to Todo class (after line 1335, with other MUX fields)
2. Update `to_dict()` to include lifecycle_state when present (follow WorkItem/Feature pattern)
3. Write unit test for serialization

### Files
- `services/domain/models.py` - Todo class (lines 1261-1441)

### Evidence Required
- [ ] Modified model code
- [ ] Unit test passing

### STOP Conditions
- Existing tests fail after model change
- Import issues with LifecycleState enum

---

## Phase 2: API Update

### Objective
Include lifecycle_state in API response so frontend receives it.

### Tasks
1. Update `list_todos()` inline dict to include `lifecycle_state` (line 246-258)
2. Follow pattern: `"lifecycle_state": t.lifecycle_state.value if t.lifecycle_state else None`

### Files
- `web/api/routes/todos.py` - `list_todos()` function (lines 221-270)

### Evidence Required
- [ ] Modified API code
- [ ] API returns lifecycle_state field

### STOP Conditions
- API tests fail
- Response format breaks frontend

---

## Phase 3: Frontend Integration

### Objective
Render lifecycle indicator in todos.html when lifecycle_state present.

### Tasks
1. Update JavaScript `renderTodos()` function to include lifecycle indicator
2. Add conditional: only render when `todo.lifecycle_state` exists
3. Use inline indicator style (compact, next to todo text)
4. Include experience phrase on hover (from lifecycle constants or API)

### Files
- `templates/todos.html` - `renderTodos()` function (around line 163)

### Evidence Required
- [ ] Modified template code
- [ ] Visual verification

### STOP Conditions
- JavaScript errors
- Layout breaks
- Indicator doesn't render

---

## Phase Z: Completion

### Checklist
- [ ] All Phase 0 verifications complete
- [ ] Phase 1 model update complete with test
- [ ] Phase 2 template integration complete
- [ ] Manual testing scenarios verified
- [ ] No regressions in todo functionality
- [ ] GitHub issue #708 updated with evidence
- [ ] Session log updated

### Evidence Compilation
- Model change: [commit or diff]
- Unit test: [pytest output]
- Template change: [commit or diff]
- Visual verification: [description]

### PM Approval Request
After completion, update #708 with evidence and request PM review.

---

## Agent Deployment

**Single Agent**: Lead Developer (Claude Code Opus)
**Rationale**: Small task, sequential phases, no parallelization benefit

---

## Success Criteria

From #708 Acceptance Criteria:
- [ ] Todos with lifecycle_state show compact indicator
- [ ] Todos without lifecycle_state show no indicator
- [ ] Indicator shows experience phrase on hover
- [ ] Todo check/uncheck still works
- [ ] Unit test passes
- [ ] No regressions

---

*Gameplan created: 2026-01-27*
*Status: Awaiting Phase -1 PM verification*
