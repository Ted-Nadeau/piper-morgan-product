# Gameplan: Issue #490 - FTUX-PORTFOLIO: Project Portfolio Onboarding

**Issue**: [#490](https://github.com/mediajunkie/piper-morgan-product/issues/490)
**Priority**: P0 (Alpha Critical)
**Size**: Medium
**Created**: 2026-01-09

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Chief Architect's Current Understanding

Based on investigation completed earlier today:

**Infrastructure Status**:
- [x] Web framework: **FastAPI** (confirmed)
- [x] CLI structure: **Click** (confirmed)
- [x] Database: **PostgreSQL 5433** (confirmed)
- [x] Testing framework: **pytest** (confirmed)
- [x] Existing endpoints: `/api/v1/intent`, `/api/v1/projects/`
- [x] Missing features: `PortfolioOnboardingManager`, first-meeting trigger, entity extraction

**My understanding of the task**:
- I believe we need to: Create conversational onboarding when user has 0 projects
- I think this involves: State machine (follow standup pattern), handler, detection
- I assume the current state is: Dead-end messages exist ("Would you like me to help you set up your project portfolio?") but no workflow follows

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [x] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable
- [ ] Coordination queue prompt being claimed

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [ ] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment:**
- [x] **SKIP WORKTREE** - Overhead criteria dominate

**Rationale**: Sequential phased work by single agent. Phases are clearly scoped and testable. Worktree overhead exceeds benefit.

### Part B: PM Verification Required

**What actually exists in the filesystem:**

```
services/standup/
├── conversation_manager.py      # StandupConversationManager - OUR TEMPLATE
├── conversation_handler.py      # StandupConversationHandler - OUR TEMPLATE
├── preference_*.py              # Preference extraction (may inform entity extraction)
└── __init__.py

services/domain/models.py:194-252  # Project class (full CRUD)
services/database/repositories.py:173-491  # ProjectRepository with count_active_projects()
services/intent_service/canonical_handlers.py:2209-2249  # _detect_setup_request()
```

**Recent work in this area:**
- Last changes: Epic #242 (Standup Interactive) just completed - provides exact pattern
- Known issues: The "Would you like me to help..." messages are dead ends (lines 1108, 1414)
- Previous attempts: None - this is new work

**Actual task needed:**
- [x] Create new feature from scratch (but following established standup pattern)

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding is correct, gameplan appropriate

**Evidence**:
- Infrastructure audit completed in session log
- StandupConversationManager/Handler provide exact template
- ProjectRepository already has `count_active_projects()`
- All dependencies exist

---

## Phase 0: Initial Bookending - GitHub Investigation

### Purpose
Verify issue state and current codebase readiness

### Required Actions

1. **GitHub Issue Verification** ✅ COMPLETE
   - Issue #490 exists and updated to template compliance
   - All required sections present
   - Completion matrix initialized

2. **Codebase Investigation** ✅ COMPLETE (from earlier today)
   - Standup pattern verified: `services/standup/conversation_manager.py`
   - Project repo verified: `ProjectRepository.count_active_projects()` exists
   - Dead-end messages identified: lines 1108, 1414 in canonical_handlers.py

3. **Update GitHub Issue**
   ```bash
   gh issue edit 490 --body "[Add] ## Status: Investigation Complete - Ready for Phase 1"
   ```

### STOP Conditions
- ✅ Issue exists
- ✅ Pattern template available (standup)
- ✅ Required infrastructure confirmed

---

## Phase 0.5: Frontend-Backend Contract Verification

**SKIP** - This is backend-only work. No new API endpoints or frontend changes in scope.

The onboarding flow happens entirely through the existing `/api/v1/intent` endpoint which already handles conversation turns.

---

## Phase 1: First-Meeting Detection

### Objective
Detect when user has no projects and should be offered onboarding

### Deploy: Single Agent (Claude Code)

Create detection service that hooks into greeting/hello handling.

### Tasks

1. **Create `FirstMeetingDetector` class**
   - Location: `services/onboarding/first_meeting_detector.py`
   - Uses `ProjectRepository.count_active_projects(user_id)`
   - Returns boolean indicating if onboarding should trigger
   - Checks for decline flag in user preferences

2. **Create unit tests**
   - Location: `tests/unit/services/onboarding/test_first_meeting_detector.py`
   - Tests:
     - `test_detects_empty_projects_state`
     - `test_skips_when_projects_exist`
     - `test_handles_database_error_gracefully`
     - `test_respects_decline_flag`

3. **Create `__init__.py`**
   - Location: `services/onboarding/__init__.py`
   - Export `FirstMeetingDetector`

### Deliverables
- `services/onboarding/__init__.py`
- `services/onboarding/first_meeting_detector.py`
- `tests/unit/services/onboarding/test_first_meeting_detector.py`

### Evidence Required
```bash
pytest tests/unit/services/onboarding/test_first_meeting_detector.py -v
# All 4 tests passing
```

### STOP Conditions
- ProjectRepository doesn't have `count_active_projects()` → STOP (verify first)
- Database access pattern unclear → STOP (ask PM)

---

## Phase 2: Conversational Onboarding State Machine

### Objective
Create multi-turn conversation handler following standup pattern

### Deploy: Single Agent (Claude Code)

Follow `StandupConversationManager` pattern exactly.

### Tasks

1. **Create `PortfolioOnboardingState` enum**
   - States: INITIATED, GATHERING_PROJECTS, CONFIRMING, COMPLETE, DECLINED

2. **Create `PortfolioOnboardingManager`**
   - Location: `services/onboarding/portfolio_manager.py`
   - Mirror `StandupConversationManager` structure:
     - `create_session(user_id)` - start onboarding
     - `get_session(session_id)` - retrieve state
     - `transition_state(session_id, new_state)` - change state
     - `add_project(session_id, project_data)` - store extracted project
     - `complete_session(session_id)` - finalize and persist

3. **Create `PortfolioOnboardingHandler`**
   - Location: `services/onboarding/portfolio_handler.py`
   - Mirror `StandupConversationHandler` structure:
     - `handle_turn(session_id, user_message)` - main entry
     - `start_onboarding(user_id)` - initiate flow
     - `_handle_initiated()` - waiting for user response to offer
     - `_handle_gathering()` - collecting project info
     - `_handle_confirming()` - verify before save
     - `_extract_project_info(message)` - simple entity extraction

4. **Create unit tests**
   - Location: `tests/unit/services/onboarding/test_portfolio_onboarding.py`
   - Tests:
     - `test_state_transitions_initiated_to_gathering`
     - `test_state_transitions_gathering_to_confirming`
     - `test_state_transitions_to_complete`
     - `test_state_transitions_to_declined`
     - `test_project_extraction_from_message`
     - `test_decline_flow`
     - `test_graceful_fallback_on_malformed_input`

### Deliverables
- `services/onboarding/portfolio_manager.py`
- `services/onboarding/portfolio_handler.py`
- `tests/unit/services/onboarding/test_portfolio_onboarding.py`

### Evidence Required
```bash
pytest tests/unit/services/onboarding/test_portfolio_onboarding.py -v
# All 7+ tests passing
```

### STOP Conditions
- Standup pattern doesn't apply → STOP (escalate)
- Entity extraction too complex → STOP (simplify to name-only)
- State machine design unclear → STOP (ask PM)

---

## Phase 3: Handler Integration & Project Persistence

### Objective
Connect onboarding handler to canonical_handlers and ProjectRepository

### Deploy: Single Agent (Claude Code)

Integration work connecting new components to existing system.

### Tasks

1. **Modify greeting handler in `canonical_handlers.py`**
   - Hook `FirstMeetingDetector` into hello/greeting handling
   - Return onboarding prompt when detector triggers
   - Route onboarding turns to `PortfolioOnboardingHandler`

2. **Connect to `ProjectRepository.create()`**
   - In `PortfolioOnboardingHandler._handle_confirming()`
   - Create Project domain object from extracted info
   - Persist via repository
   - Return confirmation message

3. **Add session storage for onboarding state**
   - Use existing session/conversation patterns
   - Store onboarding session ID in user context

4. **Create integration test**
   - Location: `tests/integration/test_portfolio_onboarding_e2e.py`
   - Test full flow: greeting → onboarding → project saved → subsequent greeting normal

### Deliverables
- Modified `services/intent_service/canonical_handlers.py`
- Integration test at `tests/integration/test_portfolio_onboarding_e2e.py`
- Project persistence working

### Evidence Required
```bash
pytest tests/integration/test_portfolio_onboarding_e2e.py -v
# Integration test passing

pytest tests/unit/services/onboarding/ -v
# All unit tests still passing (no regressions)
```

### STOP Conditions
- ProjectRepository interface changed → STOP (verify API)
- Canonical handlers structure different than expected → STOP (investigate)
- Session management pattern unclear → STOP (ask PM)

---

## Phase Z: Completion & Handoff

### Purpose
Final verification, documentation, PM approval request

### Required Actions

#### 1. Run All Tests
```bash
# All onboarding tests
pytest tests/unit/services/onboarding/ -v
pytest tests/integration/test_portfolio_onboarding_e2e.py -v

# Regression check - greeting/GUIDANCE still works
pytest tests/unit/services/intent_service/ -v -k "greeting or guidance"

# Full test suite (smoke)
pytest tests/ -m smoke
```

#### 2. Update Documentation
- [ ] Update `docs/ALPHA_TESTING_GUIDE.md` - mention project onboarding
- [ ] Add docstrings to all new classes explaining state machine
- [ ] Update session log with completion evidence

#### 3. GitHub Final Update
```bash
gh issue edit 490 --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] All acceptance criteria met
- [x] Tests passing: [paste output]
- [x] No regressions: [paste output]
- [x] Documentation updated

### Completion Matrix (Updated)
| Component | Status | Evidence |
|-----------|--------|----------|
| FirstMeetingDetector | ✅ | test output |
| PortfolioOnboardingManager | ✅ | test output |
| PortfolioOnboardingHandler | ✅ | test output |
| Handler integration | ✅ | integration test |
| Unit tests (detection) | ✅ | 4 tests |
| Unit tests (manager) | ✅ | N tests |
| Unit tests (handler) | ✅ | N tests |
| Integration test | ✅ | 2 tests |
| Documentation | ✅ | ALPHA_TESTING_GUIDE.md |

### Ready for PM Review
"
```

#### 4. PM Approval Request
```markdown
@PM - Issue #490 complete and ready for review:
- All acceptance criteria met ✓
- Evidence provided ✓
- Documentation updated ✓
- No regressions confirmed ✓

Please review and close if satisfied.
```

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent Type | Issue | Evidence Required | Handoff |
|-------|------------|-------|------------------|---------|
| 1 | Code Agent | #490 | 4 tests, FirstMeetingDetector | Detector ready |
| 2 | Code Agent | #490 | 7+ tests, Manager/Handler | State machine ready |
| 3 | Code Agent | #490 | Integration test, canonical_handlers modified | Full flow working |
| Z | Lead Dev | #490 | All tests, docs, GitHub updated | PM approval request |

### Verification Gates
- [ ] Phase 1: Unit tests passing (4 tests)
- [ ] Phase 2: Unit tests passing (11+ tests total)
- [ ] Phase 3: Integration test passing
- [ ] Phase 3a: **Routing integration tests** (for greeting → onboarding flow)
- [ ] Phase Z: Full regression check, documentation complete

### CRITICAL: Routing Integration Tests (Issue #521 Learning)

**For Phase 3 intent handler integration:**

Unit tests that mock routing are NOT sufficient. We MUST include **routing integration tests** that verify the full path from greeting to onboarding:

```python
# BAD: Tests handler in isolation (mocked routing)
async def test_onboarding_handler_works():
    result = await handler._handle_initiated(mock_intent, session_id)
    assert "project" in result  # ✅ Passes but doesn't prove routing works

# GOOD: Tests full routing path (greeting → FirstMeetingDetector → onboarding)
async def test_greeting_triggers_onboarding_for_new_user():
    # User with 0 projects says "Hi Piper"
    response = await intent_service.process("Hi Piper", user_with_no_projects)
    assert "Would you like to tell me about the projects" in response
    # Proves: greeting → detector → onboarding prompt (full path)
```

**Why this matters:** Issue #521 had 17 passing unit tests but queries failed because the pre-classifier intercepted them. We must verify the greeting → onboarding path works end-to-end.

### Evidence Collection Points

1. **After Phase 1 complete**: Collect FirstMeetingDetector test output immediately
2. **After Phase 2 complete**: Collect state machine test output, verify all transitions
3. **After Phase 3 complete**: Collect integration test output + routing test output
4. **Before Phase Z**: Compile all evidence into GitHub issue before requesting PM review

### Handoff Quality Checklist

Before accepting handoff from any subagent phase:
- [ ] All acceptance criteria checkboxes addressed
- [ ] Test output provided (not just "tests pass")
- [ ] Files modified list included
- [ ] User verification steps documented (how to manually test)
- [ ] Blockers explicitly stated (if any)

---

## STOP Conditions (Apply Throughout)

Stop immediately and escalate if:
- Infrastructure doesn't match assumptions (Project model changed)
- Tests fail for any reason
- State machine pattern from standup doesn't apply
- Entity extraction too complex for scope
- User data at risk
- Completion bias detected

---

## Evidence Requirements

### What Counts as Evidence
✅ Terminal output showing test results
✅ Pytest output with test counts
✅ Git commits/diffs
✅ curl/manual testing of conversation flow

❌ "Should work"
❌ "Tests pass" without output
❌ "Fixed" without proof

---

## Success Criteria

### Issue Completion Requires
- [ ] All acceptance criteria met (17 criteria across 4 categories)
- [ ] Evidence provided for each criterion
- [ ] Tests passing (with output): 15+ tests across unit/integration
- [ ] No regressions introduced
- [ ] Documentation updated (ALPHA_TESTING_GUIDE.md)
- [ ] GitHub issue fully updated
- [ ] PM approval received

---

## Key Implementation Notes

### Pattern to Follow
The standup conversation handler is our exact template:
- `StandupConversationManager` → `PortfolioOnboardingManager`
- `StandupConversationHandler` → `PortfolioOnboardingHandler`
- `StandupConversationState` → `PortfolioOnboardingState`

### Integration Point
The greeting handler in `canonical_handlers.py` currently returns generic responses. The key change is:
1. Check `FirstMeetingDetector.should_trigger(user_id)` before returning
2. If true, return onboarding prompt and start onboarding session
3. Subsequent turns routed to `PortfolioOnboardingHandler`

### Entity Extraction (Keep Simple)
MVP scope: Just extract project name from message like "I'm building a mobile app called HealthTrack"
- Pattern: "called X", "named X", "X project", or just use the whole message as name
- Don't over-engineer - can enhance in future iterations

---

## Remember

- **Inchworm Protocol**: Complete each phase 100% before moving
- **Evidence Required**: No claims without proof
- **75% Pattern**: Complete existing work, don't replace
- **PM Closes Issues**: Agents request approval only
- **Follow Standup Pattern**: Don't reinvent - copy what works

---

*Gameplan created: 2026-01-09*
*Ready for Phase 1 execution*
