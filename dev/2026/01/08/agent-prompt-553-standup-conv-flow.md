# Claude Code Agent Prompt: #553 STANDUP-CONV-FLOW

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- BRIEFING-ESSENTIAL-AGENT.md - Your role requirements

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete GitHub Issue #553. Your work builds on #552 (State Management) which is complete.

### Acceptance Criteria
- [ ] `StandupConversationHandler` class exists with state-based routing
- [ ] `ConversationResponse` dataclass for structured responses
- [ ] Handler for each state (INITIATED, GATHERING, GENERATING, REFINING, FINALIZING)
- [ ] Preference extraction from user messages
- [ ] Refinement logic (add/remove blockers, modify content)
- [ ] Graceful fallback when workflow fails
- [ ] Unit tests for all state handlers
- [ ] Unit tests for full conversation flows
- [ ] Integration with existing `StandupConversationManager`
- [ ] No regressions in existing standup functionality

**Every checkbox must be addressed in your handoff.**

### Evidence You MUST Provide
1. **Test count**: "Added X tests in [file path]"
2. **Test verification**: "All tests passing" with actual output
3. **Files modified**: Complete list with line counts
4. **How to verify**: Step-by-step instructions

### Your Handoff Format
```
## Issue #553 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X tests added in tests/unit/services/standup/test_conversation_handler.py
- `pytest tests/unit/services/standup/ -v` output: [paste actual output]

**Verification**:
[Import verification commands with actual output]

**Files Modified**:
- services/standup/conversation_handler.py (new - ~250 lines)
- services/standup/__init__.py (+15 lines - exports)
- tests/unit/services/standup/test_conversation_handler.py (new - ~300 lines)

**User Testing Steps**:
1. [Step 1]
2. [Step 2]
3. [Expected result]

**Blockers** (if any):
- [Blocker description]
```

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check #552 Completion FIRST
```bash
# Verify #552 issue is closed
gh issue view 552 --json state -q '.state'
# Expected: CLOSED

# Verify state management infrastructure
python -c "from services.standup.conversation_manager import StandupConversationManager; print('OK')"
python -c "from services.shared_types import StandupConversationState; print(list(StandupConversationState))"

# Verify tests pass
pytest tests/unit/services/standup/test_conversation_state.py -v --tb=short

# Check existing standup workflow
python -c "from services.features.morning_standup import MorningStandupWorkflow; print('OK')"
```

**If ANY of these fail**:
1. **STOP immediately**
2. **Report the failure with evidence**
3. **Wait for revised instructions**

---

## Mission

Implement multi-turn conversation flow logic for interactive standup conversations, building on the state management from #552.

**Scope Boundaries**:
- This prompt covers ONLY: Conversation handler, turn routing, refinement logic, tests
- NOT in scope: Chat widget UI (#554), preference persistence (#555), performance (#556)
- Depends on: #552 (State Management) - MUST be complete

---

## Context
- **GitHub Issue**: #553 STANDUP-CONV-FLOW: Multi-Turn Conversation Flow
- **Epic**: #242 (CONV-MCP-STANDUP-INTERACTIVE)
- **Current State**: State machine exists, single-turn standup generation exists
- **Target State**: Multi-turn conversation handling with refinement
- **Dependencies**: #552 (complete)
- **User Data Risk**: None (in-memory, session-scoped)

---

## Implementation Approach

### Phase 1: Create ConversationHandler

**File**: `services/standup/conversation_handler.py` (~250 lines)

**Key Components**:

1. **ConversationResponse dataclass**
```python
@dataclass
class ConversationResponse:
    message: str
    state: StandupConversationState
    requires_input: bool = True
    standup_content: Optional[str] = None
    suggestions: List[str] = None
    metadata: Dict[str, Any] = None
```

2. **StandupConversationHandler class**
- `__init__()` - Initialize with manager and optional workflow
- `start_conversation()` - Start new conversation
- `handle_turn()` - Route based on state
- State handlers: `_handle_initiated`, `_handle_gathering`, etc.
- `_generate_standup()` - Generate content via workflow
- `_apply_refinement()` - Handle add/remove requests
- `_graceful_fallback()` - Handle errors gracefully

**Validation**:
```bash
python -c "from services.standup.conversation_handler import StandupConversationHandler, ConversationResponse; print('OK')"
```

### Phase 2: Unit Tests

**File**: `tests/unit/services/standup/test_conversation_handler.py` (~300 lines)

**Test Classes**:
- `TestConversationResponse` - Dataclass tests
- `TestStandupConversationHandler` - Handler initialization
- `TestStartConversation` - Start conversation tests
- `TestHandleTurnInitiated` - INITIATED state handling
- `TestHandleTurnRefining` - REFINING state handling
- `TestHandleTurnFinalizing` - FINALIZING state handling
- `TestHandleTerminalStates` - Terminal state handling
- `TestGracefulFallback` - Error handling tests
- `TestPreferenceExtraction` - Preference parsing tests
- `TestFullConversationFlow` - End-to-end flow tests

**Expected**: ~17 tests covering all states and flows

**Validation**:
```bash
pytest tests/unit/services/standup/test_conversation_handler.py -v
```

### Phase 3: Package Exports

**File**: `services/standup/__init__.py`

Update to export handler:
```python
from services.standup.conversation_handler import (
    StandupConversationHandler,
    ConversationResponse,
)

__all__ = [
    "StandupConversationManager",
    "InvalidStateTransitionError",
    "StandupConversationHandler",
    "ConversationResponse",
]
```

**Validation**:
```bash
python -c "from services.standup import StandupConversationHandler, ConversationResponse; print('OK')"
```

### Phase Z: Final Verification

#### Regression check
```bash
pytest tests/unit/services/standup/ -v
pytest tests/ -k standup --tb=short
```

#### Evidence collection
```bash
# Line counts
wc -l services/standup/*.py tests/unit/services/standup/*.py

# Import verification
python -c "from services.standup import StandupConversationHandler; print('Handler: OK')"
python -c "
import asyncio
from services.standup import StandupConversationHandler

async def test():
    handler = StandupConversationHandler()
    response = await handler.start_conversation('s1', 'u1')
    print(f'State: {response.state.value}')
    return response

asyncio.run(test())
"
```

---

## Success Criteria (With Evidence)

- [ ] Infrastructure verified (#552 complete)
- [ ] `ConversationResponse` dataclass complete (show import)
- [ ] `StandupConversationHandler` instantiable (show import)
- [ ] All state handlers implemented (show test coverage)
- [ ] Refinement logic working (show test output)
- [ ] Graceful fallback working (show test output)
- [ ] All tests pass (show pytest output with 17+ passing)
- [ ] No regressions (show `pytest tests/ -k standup` output)
- [ ] GitHub issue updated with progress

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] #552 state management not complete
- [ ] `StandupConversationManager` API doesn't match expected
- [ ] `StandupConversationState` enum missing states
- [ ] `MorningStandupWorkflow` not importable
- [ ] Tests fail for any reason
- [ ] Import errors after changes

---

## Progressive Bookending

Update GitHub issue after each phase:

**After Phase 1**:
```bash
gh issue comment 553 -b "Phase 1 Complete: ConversationHandler
- Created services/standup/conversation_handler.py (~250 lines)
- ConversationResponse dataclass
- StandupConversationHandler with 5 state handlers
- Import verification: [paste output]"
```

**After Phase 2**:
```bash
gh issue comment 553 -b "Phase 2 Complete: Unit tests
- Created tests/unit/services/standup/test_conversation_handler.py (~300 lines)
- 17 tests covering all states and flows
- All passing: [paste pytest output]"
```

**After Phase 3**:
```bash
gh issue comment 553 -b "Phase 3 Complete: Package exports
- Updated services/standup/__init__.py
- Export verification: [paste output]"
```

---

## Gameplan Reference

Full implementation details are in:
`dev/active/gameplan-553-standup-conv-flow.md`

This includes:
- Complete code for handler and response dataclass
- Complete test file with all test cases
- State routing logic

---

## Self-Check Before Claiming Complete

1. Did I verify #552 infrastructure first?
2. Does ConversationResponse have all required fields?
3. Does the handler have all 5 state handlers?
4. Does refinement support add/remove blockers?
5. Does graceful fallback work on workflow errors?
6. Are there 17+ tests covering all components?
7. Do all tests pass?
8. Did I check for regressions?
9. Did I provide terminal output evidence?
10. Am I guessing or do I have proof?

---

## Related Documentation
- `dev/active/gameplan-553-standup-conv-flow.md` - Full gameplan
- `services/standup/conversation_manager.py` - State management (#552)
- `services/shared_types.py` - StandupConversationState enum
- `services/features/morning_standup.py` - MorningStandupWorkflow

---

*Prompt Version: 1.0*
*Issue: #553*
*Epic: #242*
*Created: 2026-01-07*
