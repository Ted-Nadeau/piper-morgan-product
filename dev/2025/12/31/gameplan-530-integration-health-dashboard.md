# Gameplan: #530 ALPHA-SETUP-VERIFY - Integration Health Dashboard

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/530
**Created**: 2025-12-31 16:30
**Author**: Lead Developer (Claude Code Opus 4.5)

---

## Phase -1: Infrastructure Verification ✅ COMPLETE

### Part A: Current Understanding (Verified)

**Infrastructure Status**:
- [x] Web framework: FastAPI (verified)
- [x] Database: PostgreSQL on port 5433 (verified)
- [x] Testing framework: pytest with async support (verified)
- [x] Existing health infrastructure: `IntegrationHealthMonitor` at `services/health/integration_health_monitor.py`

**Existing Integration Routers** (verified via Serena):
| Router | File | test_connection Method | Signature |
|--------|------|----------------------|-----------|
| NotionIntegrationRouter | services/integrations/notion/notion_integration_router.py | `test_connection()` | async → bool |
| GitHubIntegrationRouter | services/integrations/github/github_integration_router.py | `test_connection()` | sync → Dict with `authenticated` key |
| SlackIntegrationRouter | services/integrations/slack/slack_integration_router.py | `test_auth()` | async → Dict with `ok` key |
| CalendarIntegrationRouter | services/integrations/calendar/calendar_integration_router.py | `health_check()` | async → Dict with `status` key |

**Toast System** (verified via codebase search):
- Uses convenience methods: `Toast.error(title, message)`, `Toast.success(title, message)`, etc.
- Requires `{% include 'components/toast.html' %}` and `<script src="/static/js/toast.js"></script>`
- Pattern used consistently across: todos.html, files.html, projects.html, lists.html

### Part A.2: Work Characteristics

**Worktree Assessment**: SKIP WORKTREE
- Single agent, sequential work
- Tightly coupled files (API + UI must match)
- Estimate ~2 hours
- Rationale: Worktree overhead exceeds benefit for this task

### Part B: PM Verification Required

**Identified Issues in Current Implementation:**
1. **Router signature mismatches**: Current code expects consistent Dict returns but each router returns different types
2. **Toast pattern violation**: Used `Toast.show(type, '', message)` instead of `Toast.error(title, message)` pattern
3. **IntegrationHealthMonitor not leveraged**: Existing service ignored, reinventing the wheel
4. **No tests written**: TDD not followed

**Critical Question for PM:**
- The issue requires CLI access (Phase 4: `piper status`). Should this be included in this gameplan or deferred to separate issue?

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** - After PM reviews this gameplan
- [ ] **REVISE** - If PM identifies additional issues

---

## Phase 0: Initial Bookending

### Required Actions

1. **GitHub Issue Verification** ✅
   - Issue #530 exists and contains detailed requirements
   - Completion matrix defined
   - Acceptance criteria clear

2. **Codebase Investigation** ✅
   - Existing IntegrationHealthMonitor found
   - Integration routers have inconsistent test interfaces
   - Toast system documented
   - Partial implementation exists (needs refactoring, not starting fresh)

3. **Root Cause of Current Bugs:**
   - **Toast not styled**: Used wrong API (`Toast.show(type, '', message)` vs `Toast.error(title, message)`)
   - **GitHub connection failed**: Likely router initialization issue or token problem - needs investigation with actual test

---

## Phase 0.5: Frontend-Backend Contract Verification (MANDATORY)

**Applies**: Yes - this issue involves both API endpoints and frontend JavaScript

### After Backend, Before Frontend

| Endpoint | Route Path | Mount Prefix | Full Path |
|----------|------------|--------------|-----------|
| get_integrations_health | /health | /api/v1/integrations | /api/v1/integrations/health |
| test_integration_connection | /test/{integration_name} | /api/v1/integrations | /api/v1/integrations/test/{name} |
| test_all_connections | /test-all | /api/v1/integrations | /api/v1/integrations/test-all |

### Verification Required
```bash
# After backend complete, before frontend work:
curl -s http://localhost:8001/api/v1/integrations/health | jq .
# Must NOT return 404
```

---

## Phase 1: Refactor Backend API (TDD)

**Objective**: Fix router interface inconsistencies and integrate with IntegrationHealthMonitor

### Step 1.1: Write Tests First

Create `tests/unit/web/api/routes/test_integrations.py`:

```python
# Test cases to write:
# 1. test_health_endpoint_returns_all_integrations
# 2. test_health_endpoint_shows_configured_status
# 3. test_single_integration_test_success
# 4. test_single_integration_test_failure
# 5. test_all_connections
# 6. test_unknown_integration_returns_404
```

### Step 1.2: Refactor API Implementation

Fix issues in `web/api/routes/integrations.py`:
1. Handle each router's different return type correctly
2. Catch exceptions properly for each router
3. Return consistent error types for frontend

### Step 1.3: Verify Tests Pass

```bash
python -m pytest tests/unit/web/api/routes/test_integrations.py -v
```

**Deliverables:**
- [ ] 6+ unit tests written and passing
- [ ] All router types handled correctly
- [ ] Terminal output provided as evidence

---

## Phase 2: Fix Frontend Toast Integration

**Objective**: Use correct Toast API pattern matching rest of codebase

### Step 2.1: Audit Existing Pattern

From `templates/todos.html` (reference implementation):
```javascript
Toast.error('Load Error', 'Failed to load todos');
Toast.success('Success', 'Todo created successfully');
```

### Step 2.2: Fix integrations.html

Replace all `showToast(type, message)` calls with direct Toast method calls:
```javascript
// WRONG (current)
showToast('error', result.message);

// CORRECT (matches codebase pattern)
Toast.error('Connection Failed', result.message);
```

### Step 2.3: Verify Toast Displays Correctly

Manual test in browser:
1. Click "Test" on an integration
2. Verify toast appears with correct styling
3. Verify toast dismisses after 5 seconds

**Deliverables:**
- [ ] Toast calls match codebase pattern
- [ ] Screenshot of correctly styled toast
- [ ] No console errors

---

## Phase 3: Investigate GitHub Connection Failure

**Objective**: Determine why GitHub shows "connection_failed"

### Step 3.1: Check Token Configuration

```bash
# Verify token is set
echo "GITHUB_TOKEN exists: ${GITHUB_TOKEN:+yes}"

# Test token directly
curl -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user
```

### Step 3.2: Test Router Directly

```python
# Python test script
from services.integrations.github.github_integration_router import GitHubIntegrationRouter
router = GitHubIntegrationRouter()
result = router.test_connection()
print(result)
```

### Step 3.3: Fix if Router Issue

If issue is in router initialization or test_connection logic, fix and document.

**Deliverables:**
- [ ] Root cause identified
- [ ] Fix applied if code issue
- [ ] Evidence of working connection OR documented external issue

---

## Phase 4: Integration Tests

**Objective**: Verify full flow works end-to-end

### Step 4.1: Create Integration Test

Create `tests/integration/test_integrations_dashboard.py`:
```python
# Test cases:
# 1. test_dashboard_page_loads
# 2. test_api_health_endpoint
# 3. test_api_test_endpoint_with_mock
```

### Step 4.2: Run Full Test Suite

```bash
python -m pytest tests/unit/web/api/routes/test_integrations.py tests/integration/test_integrations_dashboard.py -v
```

**Deliverables:**
- [ ] Integration tests written
- [ ] All tests passing
- [ ] Terminal output as evidence

---

## Phase 5: CLI Command (Scope Question)

**PM Decision Required**: Include CLI `piper status` command in this issue or defer?

If included:
- Add to `cli/commands/` following existing patterns
- Output matches dashboard information
- Support `--json` flag

If deferred:
- Create follow-up issue
- Link to #530

---

## Phase Z: Final Bookending & Handoff

### Evidence Requirements

1. **Unit Tests**
   - [ ] 6+ tests in `tests/unit/web/api/routes/test_integrations.py`
   - [ ] All passing with terminal output

2. **Integration Tests**
   - [ ] Tests in `tests/integration/test_integrations_dashboard.py`
   - [ ] All passing with terminal output

3. **Manual Verification**
   - [ ] Screenshot: Dashboard with all 4 integrations visible
   - [ ] Screenshot: Toast displaying correctly on test
   - [ ] Screenshot: Error state with fix suggestion

4. **Code Quality**
   - [ ] No linting errors
   - [ ] Follows existing patterns

### Completion Matrix Update

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Dashboard UI | ⏳ | |
| Status Indicators | ⏳ | |
| Test Buttons | ⏳ | |
| Toast Notifications | ⏳ | |
| Error Guidance | ⏳ | |
| Unit Tests | ⏳ | |
| Integration Tests | ⏳ | |

---

## Multi-Agent Deployment Plan

| Phase | Agent Type | Task | Evidence Required |
|-------|------------|------|-------------------|
| 1 | Code Agent | Write unit tests | Test file + passing output |
| 1 | Code Agent | Refactor API | Fixed integrations.py |
| 2 | Lead Dev | Fix frontend | Updated integrations.html |
| 3 | Code Agent | Investigate GitHub | Root cause + fix |
| 4 | Code Agent | Integration tests | Test file + passing output |
| Z | Lead Dev | Final verification | All evidence compiled |

---

## STOP Conditions

- [ ] Router method doesn't exist → STOP, extend router first
- [ ] Toast component missing from template → STOP, add include
- [ ] Tests fail → STOP, fix before proceeding
- [ ] GitHub token missing → STOP, clarify with PM

---

## Awaiting PM Approval

Questions for PM:
1. Is Phase 5 (CLI command) in scope or should be separate issue?
2. Any specific styling requirements for the dashboard?
3. Should we leverage IntegrationHealthMonitor for persistent health tracking or keep it simple with on-demand checks?

---

*Gameplan created following template v9.2*
