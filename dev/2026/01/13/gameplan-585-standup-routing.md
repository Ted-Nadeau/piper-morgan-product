# Gameplan: Issue #585 - Standup Routing Bug

**Issue**: #585 - /standup routes to STATUS handler instead of interactive standup flow
**Priority**: P1
**Sprint**: A20 (Alpha Testing)
**Created**: 2026-01-13
**Template Version**: v9.3

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status** (VERIFIED before writing this gameplan):
- [x] `StandupConversationHandler` exists: `services/standup/conversation_handler.py`
- [x] `StandupConversationManager` exists: `services/standup/conversation_manager.py`
- [x] `StandupOrchestrationService` exists: `services/domain/standup_orchestration_service.py`
- [x] Intent routing: `_handle_standup_query()` in `intent_service.py:834`
- [x] Portfolio pattern: `_get_onboarding_components()` in `conversation_handler.py`

**My understanding of the task**:
- Two separate standup systems exist:
  1. **One-shot**: `StandupOrchestrationService` - generates immediate standup summary
  2. **Interactive**: `StandupConversationHandler` - multi-turn conversation flow (Epic #242)
- `/standup` currently routes to #1 (one-shot via `_handle_standup_query`)
- User expects #2 (interactive multi-turn flow)
- The interactive handler was never wired to the intent routing

**Root Cause Hypothesis**: The 75% pattern - `StandupConversationHandler` was built (Epic #242) but never integrated into the intent routing system the way `PortfolioOnboardingHandler` was integrated.

### Part A.2: Work Characteristics Assessment

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel
- [x] Task duration >30 minutes
- [x] Multi-component work (intent routing + standup service)

**Assessment**: **NO WORKTREE** - Sequential work, single component integration

### Part B: PM Verification Required

**PM confirmed (11:08)**:

1. **Desired behavior**: ✅ `/standup` triggers **interactive flow** (multi-turn conversation)

2. **Pattern to follow**: ✅ Same pattern as `PortfolioOnboardingHandler` (singleton in conversation_handler.py)

3. **Scope question**: ✅ **Option C - Keep both with clear semantic separation**:
   - `/standup` = **Command**: Interactive flow, creates/updates standup (→ `StandupConversationHandler`)
   - `/status` = **Query**: Automated view of current status (→ existing `_handle_status_query()`)

   This follows DDD Query/Command separation. "Status" is a noun (view), "standup" is a verb (action).

4. **Follow-up required**: Document `/standup` vs `/status` distinction in capability-naming docs.

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - PM confirmed all three questions

---

## Phase 0: Five-Whys Investigation

### Objective
Verify hypothesis and identify exact integration point.

### Five Whys Framework

**Problem**: `/standup` returns one-shot summary instead of interactive conversation.

**Why #1**: What handler is being called for `/standup`?
- Expected: `StandupConversationHandler.start_conversation()`
- Actual: `IntentService._handle_standup_query()` → `StandupOrchestrationService`

**Why #2**: Why is `_handle_standup_query` called instead of `StandupConversationHandler`?
- Because intent action `show_standup`/`get_standup` maps to `_handle_standup_query` at line 824
- There is NO routing path to `StandupConversationHandler`

**Why #3**: Why is there no routing to `StandupConversationHandler`?
- `StandupConversationHandler` was built for Epic #242 but never integrated
- Unlike `PortfolioOnboardingHandler` which IS integrated via:
  - Module-level singleton in `conversation_handler.py`
  - Check in `ConversationHandler.respond()`
  - Active session detection in `IntentService._check_active_onboarding()`

**Why #4**: What would integration look like?
- Similar to portfolio onboarding:
  1. Create singleton manager/handler in `conversation_handler.py` or new file
  2. Add session detection before intent classification
  3. Route `/standup` command to `handler.start_conversation()`
  4. Handle subsequent turns via `handler.handle_turn()`

**Why #5**: What triggers the interactive flow?
- Need an **entry point** that:
  - Detects `/standup` command (or `start_standup` action)
  - Creates new standup conversation session
  - Returns first prompt ("Which project would you like to start with?")
- Need a **continuation check** that:
  - Detects active standup session
  - Routes subsequent messages to `handler.handle_turn()`

### Investigation Tasks

- [ ] Verify `StandupConversationHandler.start_conversation()` works standalone
- [ ] Check if `StandupConversationManager` exists and manages sessions
- [ ] Identify exact integration points needed
- [ ] Document the wiring gap

### Deliverables
- Root cause confirmation
- Integration plan with specific file:line changes

---

## Phase 0.6: Data Flow & Integration Verification

### Current Flow (Broken)

```
User: "/standup"
    ↓
POST /api/v1/intent
    ↓
IntentService.process_intent()
    ↓
LLM classifies → IntentCategory.QUERY, action="show_standup"
    ↓
_route_query_intent() → line 824: action in ["show_standup", "get_standup"]
    ↓
_handle_standup_query() → StandupOrchestrationService.orchestrate_standup_workflow()
    ↓
Returns ONE-SHOT summary
```

### Expected Flow (Fixed)

```
User: "/standup"
    ↓
POST /api/v1/intent
    ↓
IntentService.process_intent()
    ↓
[NEW] Check for "/standup" command OR active standup session
    ↓
[If new session] StandupConversationHandler.start_conversation()
    ↓
Returns: "Which project would you like to start with?" + project list
    ↓
[Store session state]

User: "1" (selects project)
    ↓
POST /api/v1/intent
    ↓
[NEW] Check for active standup session → FOUND
    ↓
StandupConversationHandler.handle_turn(message)
    ↓
Returns: "What did you accomplish yesterday?"
    ↓
[Continue multi-turn flow...]
```

### Integration Points Checklist

| Caller | Callee | Exists? | Wired? |
|--------|--------|---------|--------|
| IntentService | StandupConversationHandler | ✅ | ❌ |
| IntentService | StandupConversationManager | ✅ | ❌ |
| conversation_handler.py | StandupConversationHandler | N/A | ❌ |

---

## Phase 0.7: Conversation Design (REQUIRED - Conversational Feature)

### Purpose
Design the interactive standup conversation flow before implementing.

### Part A: Happy Path Script

```
Turn 1:
  User: "/standup"
  Piper: "Good morning! Let's do your standup. Which project would you like to start with?
          1. Decision Reviews
          2. One Job
          3. Piper Morgan"
  State: INITIATED → GATHERING_PROJECT

Turn 2:
  User: "1" or "Decision Reviews"
  Piper: "Great! For Decision Reviews - what did you accomplish yesterday?"
  State: GATHERING_PROJECT → GATHERING_ACCOMPLISHMENTS

Turn 3:
  User: "Reviewed 3 pull requests and fixed the auth bug"
  Piper: "Got it! What are you planning to work on today?"
  State: GATHERING_ACCOMPLISHMENTS → GATHERING_PLANS

Turn 4:
  User: "Finish the API refactor and start on tests"
  Piper: "Sounds good! Any blockers or impediments?"
  State: GATHERING_PLANS → GATHERING_BLOCKERS

Turn 5:
  User: "Waiting on design review for the new dashboard"
  Piper: "Thanks! Here's your standup summary:
          [Summary of accomplishments, plans, blockers]
          Want to continue with another project or are you done?"
  State: GATHERING_BLOCKERS → CONFIRMING

Turn 6:
  User: "done" or "2" (another project)
  Piper: [Complete or loop back to GATHERING_PROJECT for next project]
  State: CONFIRMING → COMPLETE or GATHERING_PROJECT
```

### Part B: Edge Cases Table

| User Input | Current State | Expected Behavior | Response |
|------------|---------------|-------------------|----------|
| "/standup" | ANY (no session) | Start new session | Project selection prompt |
| "/standup" | Active session | Ask continue/restart? | "You have a standup in progress..." |
| "1", "2", "3" | GATHERING_PROJECT | Select project by number | Accomplishments prompt |
| Project name | GATHERING_PROJECT | Select project by name | Accomplishments prompt |
| "skip" | ANY gathering | Skip to next section | Next prompt |
| "done" / "that's all" | CONFIRMING | Complete standup | Summary + farewell |
| "cancel" / "quit" | ANY | Abort session | Confirmation + exit |
| Empty input | ANY | Re-prompt | "I didn't catch that..." |

### Part C: State Machine

```
NO_SESSION
    └── [/standup command] → INITIATED

INITIATED
    └── [project list shown] → GATHERING_PROJECT

GATHERING_PROJECT
    ├── [project selected] → GATHERING_ACCOMPLISHMENTS
    └── [cancel] → ABANDONED

GATHERING_ACCOMPLISHMENTS
    ├── [input received] → GATHERING_PLANS
    ├── [skip] → GATHERING_PLANS
    └── [cancel] → ABANDONED

GATHERING_PLANS
    ├── [input received] → GATHERING_BLOCKERS
    ├── [skip] → GATHERING_BLOCKERS
    └── [cancel] → ABANDONED

GATHERING_BLOCKERS
    ├── [input received] → CONFIRMING
    ├── [skip] → CONFIRMING
    └── [cancel] → ABANDONED

CONFIRMING
    ├── [done] → COMPLETE (terminal)
    ├── [another project] → GATHERING_PROJECT
    └── [cancel] → ABANDONED

COMPLETE (terminal)
ABANDONED (terminal)
```

---

## Phase 0.8: Post-Completion Integration

### Purpose
Ensure standup data is properly stored and affects downstream features.

### Completion Side-Effects

When standup completes successfully:

| Side Effect | Table/Field | Value | Verified? |
|-------------|-------------|-------|-----------|
| Standup entry created | standup_entries | New row with summary | [ ] |
| Timestamp recorded | standup_entries.created_at | now() | [ ] |
| User linked | standup_entries.user_id | Current user | [ ] |
| Project linked | standup_entries.project_id | Selected project(s) | [ ] |

### Downstream Behavior Changes

| Feature | Before Standup | After Standup |
|---------|----------------|---------------|
| Status query | No standup today | Shows today's standup |
| Daily summary | Missing standup | Includes standup data |
| History view | No entry | New entry visible |

### Verification Query

```sql
-- Verify standup was saved after completion
SELECT id, user_id, project_id, accomplishments, plans, blockers, created_at
FROM standup_entries
WHERE user_id = '[user_id]' AND DATE(created_at) = CURRENT_DATE;
```

---

## Phase 1: TDD - Write Failing Tests First

### Objective
Create tests that FAIL with current code, proving the routing gap exists.

### Test Requirements (from template v9.3)

**Must include**:
- [ ] Unit tests for routing logic
- [ ] **Wiring tests** (verify import chains work without mocking internals)
- [ ] Integration tests for /standup → handler path

### Test Cases

```python
# tests/unit/services/standup/test_standup_routing_585.py

@pytest.mark.asyncio
async def test_standup_command_starts_interactive_flow():
    """
    Issue #585: /standup should start interactive conversation, not one-shot.

    GIVEN: User sends "/standup" command
    WHEN: Intent is processed
    THEN: Response should ask which project to start with
          NOT return a complete standup summary
    """
    # This should FAIL before fix
    pass

@pytest.mark.asyncio
async def test_standup_session_continues_across_turns():
    """
    Issue #585: Standup conversation should maintain state across turns.

    GIVEN: User started standup with "/standup"
    WHEN: User responds to project selection
    THEN: Handler should process as continuation, not new intent
    """
    # This should FAIL before fix
    pass

@pytest.mark.asyncio
async def test_standup_handler_invoked_not_orchestration_service():
    """
    Issue #585: Verify StandupConversationHandler is called.

    GIVEN: /standup command
    WHEN: Routed through intent system
    THEN: StandupConversationHandler.start_conversation() is called
          NOT StandupOrchestrationService.orchestrate_standup_workflow()
    """
    # This should FAIL before fix
    pass
```

---

## Phase 2: Implementation

### Objective
Wire `StandupConversationHandler` into the intent routing system.

### Implementation Options

**Option A: Follow Portfolio Pattern Exactly**
- Add `_standup_manager`, `_standup_handler` singletons to `conversation_handler.py`
- Add `_check_active_standup()` to `IntentService`
- Add `/standup` command detection before classification

**Option B: Unified Multi-Turn Handler**
- Create generic multi-turn conversation router
- Register both portfolio and standup handlers
- More architectural change, better long-term

**Recommendation**: Option A (lower risk, proven pattern)

### Implementation Tasks (Option A)

1. **Add standup singleton pattern** to `services/conversation/conversation_handler.py`:
   ```python
   _standup_manager = None
   _standup_handler = None

   def _get_standup_components():
       global _standup_manager, _standup_handler
       if _standup_manager is None:
           from services.standup import StandupConversationHandler, StandupConversationManager
           _standup_manager = StandupConversationManager()
           _standup_handler = StandupConversationHandler(_standup_manager)
       return _standup_manager, _standup_handler
   ```

2. **Add active session check** to `IntentService._check_active_onboarding()`:
   - Rename to `_check_active_conversations()` or add separate `_check_active_standup()`
   - Check for active standup session by user_id
   - If found, route to `_standup_handler.handle_turn()`

3. **Add `/standup` command detection**:
   - Before or during classification, detect `/standup` command
   - Create new standup session
   - Call `_standup_handler.start_conversation()`

4. **Update routing** in `_route_query_intent()`:
   - Change `show_standup`/`get_standup` handling
   - Or add new action `start_standup` for interactive

---

## Phase 3: Cross-Validation

### Objective
Independent verification of fix.

### Audit Tasks

1. Code review of integration
2. Verify no regressions in:
   - Portfolio onboarding
   - Status queries
   - Other intent categories
3. Manual testing of full standup flow

---

## Phase Z: Completion & Handoff

### Completion Checklist

- [ ] Root cause documented
- [ ] Unit tests written and passing
- [ ] Integration implemented
- [ ] Cross-validation complete
- [ ] Manual testing verified
- [ ] No regressions
- [ ] Session log updated
- [ ] GitHub issue updated with evidence

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent | Role | Evidence Required |
|-------|-------|------|-------------------|
| 0 | Lead Dev | Investigation | Root cause doc |
| 1 | Agent A | TDD Test Writer | Failing test file |
| 2 | Agent B | Implementer | Fix + passing tests |
| 3 | Agent C | Auditor | Review report |

### Verification Gates

- [ ] **Gate 0→1**: Root cause confirmed, integration plan approved
- [ ] **Gate 1→2**: Failing tests exist and committed
- [ ] **Gate 2→3**: All tests pass, no regressions
- [ ] **Gate 3→Z**: Audit report approves fix

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] `StandupConversationHandler` doesn't work standalone
- [ ] `StandupConversationManager` has fundamental issues
- [ ] Integration requires changes to authentication/session
- [ ] Multiple unrelated routing bugs discovered
- [ ] Changes affect portfolio onboarding negatively

---

## Appendix: Key File Locations (VERIFIED)

```
services/standup/conversation_handler.py
  - StandupConversationHandler class
  - start_conversation() method - line 169
  - handle_turn() method - line 103

services/standup/conversation_manager.py
  - StandupConversationManager class
  - Session state management

services/conversation/conversation_handler.py
  - _get_onboarding_components() - line 20 (PATTERN TO FOLLOW)
  - ConversationHandler class

services/intent/intent_service.py
  - _check_active_onboarding() - line ~612 (ADD STANDUP CHECK)
  - _route_query_intent() - line ~756
  - _handle_standup_query() - line 834 (CURRENT, WRONG HANDLER)
```

---

_Gameplan created: 2026-01-13 11:00_
_Status: Awaiting PM verification of Phase -1_
