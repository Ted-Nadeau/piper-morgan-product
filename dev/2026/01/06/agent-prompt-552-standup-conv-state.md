# Claude Code Agent Prompt: #552 STANDUP-CONV-STATE

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- BRIEFING-ESSENTIAL-AGENT.md - Your role requirements

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete GitHub Issue #552. Your work is part of a multi-agent coordination chain.

### Acceptance Criteria
- [ ] `StandupConversationState` enum exists with 7 states
- [ ] `StandupConversation` dataclass tracks all required fields
- [ ] State transitions validate allowed paths
- [ ] Conversation history preserved across turns
- [ ] Session-scoped persistence working
- [ ] Unit tests for all state transitions
- [ ] Unit tests for conversation lifecycle
- [ ] Edge cases covered (invalid transitions)
- [ ] No regressions in existing standup functionality

**Every checkbox must be addressed in your handoff.**

### Evidence You MUST Provide
1. **Test count**: "Added X tests in [file path]"
2. **Test verification**: "All tests passing" with actual output
3. **Files modified**: Complete list with line counts
4. **How to verify**: Step-by-step instructions

### Your Handoff Format
```
## Issue #552 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X tests added in tests/unit/services/standup/test_conversation_state.py
- `pytest tests/unit/services/standup/ -v` output: [paste actual output]

**Verification**:
[Import verification commands with actual output]

**Files Modified**:
- services/shared_types.py (+X lines - StandupConversationState enum)
- services/domain/models.py (+X lines - StandupConversation dataclass)
- services/standup/__init__.py (new)
- services/standup/conversation_manager.py (new - ~200 lines)
- tests/unit/services/standup/__init__.py (new)
- tests/unit/services/standup/test_conversation_state.py (new - ~300 lines)

**User Testing Steps**:
1. [Step 1]
2. [Step 2]
3. [Expected result]

**Blockers** (if any):
- [Blocker description]
```

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Gameplan Assumptions FIRST
```bash
# Verify existing conversation infrastructure
ls -la services/domain/models.py
grep -n "class Conversation" services/domain/models.py
grep -n "class ConversationTurn" services/domain/models.py

# Verify shared_types.py exists and has enum patterns
ls -la services/shared_types.py
grep -n "class.*Enum" services/shared_types.py | head -5

# Check if standup directory exists (it shouldn't yet)
ls -la services/standup/ 2>/dev/null || echo "services/standup/ does not exist - EXPECTED"

# Verify test directory structure
ls -la tests/unit/services/
```

**If reality doesn't match expectations**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised instructions**

---

## Mission

Implement conversation state management infrastructure for interactive standup conversations.

**Scope Boundaries**:
- This prompt covers ONLY: Domain models, state management service, unit tests
- NOT in scope: Conversation flow logic, chat widget integration, preference learning
- Separate issues handle: #553 (flow), #554 (widget), #555 (learning), #556 (perf)

---

## Context
- **GitHub Issue**: #552 STANDUP-CONV-STATE: Conversation State Management
- **Epic**: #242 (CONV-MCP-STANDUP-INTERACTIVE)
- **Current State**: Stateless standup generation exists via `MorningStandupWorkflow`
- **Target State**: State machine tracking standup conversations across turns
- **Dependencies**: None (this is the foundation)
- **User Data Risk**: None (new infrastructure, no existing data)
- **Infrastructure Verified**: Pending your verification

---

## Implementation Approach

### Phase 1: Domain Models

#### Step 1a: Add StandupConversationState enum

**File**: `services/shared_types.py`
**Location**: After `PatternType` enum (around line 195)

```python
class StandupConversationState(Enum):
    """Issue #552: State machine for interactive standup conversations."""
    INITIATED = "initiated"                    # User requested standup
    GATHERING_PREFERENCES = "gathering_preferences"  # Asking refinement questions
    GENERATING = "generating"                  # Generating standup content
    REFINING = "refining"                      # User providing feedback/edits
    FINALIZING = "finalizing"                  # Confirming final version
    COMPLETE = "complete"                      # Standup delivered
    ABANDONED = "abandoned"                    # User cancelled or timed out
```

**Validation**:
```bash
python -c "from services.shared_types import StandupConversationState; print(list(StandupConversationState))"
```

**Expected output**: List of 7 enum members

#### Step 1b: Add StandupConversation dataclass

**File**: `services/domain/models.py`
**Location**: After `ConversationTurn` (around line 1312)

Add import at top:
```python
from services.shared_types import StandupConversationState
```

Add dataclass:
```python
@dataclass
class StandupConversation:
    """Issue #552: Domain model for interactive standup conversations."""

    id: str = field(default_factory=lambda: str(uuid4()))
    session_id: str = ""
    user_id: str = ""

    # State machine
    state: StandupConversationState = StandupConversationState.INITIATED
    previous_state: Optional[StandupConversationState] = None

    # User preferences for this standup
    preferences: Dict[str, Any] = field(default_factory=dict)

    # Generated content
    current_standup: Optional[str] = None
    standup_versions: List[str] = field(default_factory=list)

    # Conversation turns
    turns: List[ConversationTurn] = field(default_factory=list)

    # Context from integrations
    context: Dict[str, Any] = field(default_factory=dict)

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "state": self.state.value,
            "previous_state": self.previous_state.value if self.previous_state else None,
            "preferences": self.preferences,
            "current_standup": self.current_standup,
            "standup_versions": self.standup_versions,
            "turns": [t.to_dict() for t in self.turns],
            "context": self.context,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
```

**Validation**:
```bash
python -c "from services.domain.models import StandupConversation; print(StandupConversation.__annotations__)"
```

### Phase 2: State Management Service

#### Step 2a: Create services/standup/ package

```bash
mkdir -p services/standup
echo '"""Issue #552: Standup conversation management package."""' > services/standup/__init__.py
```

#### Step 2b: Create StandupConversationManager

**File**: `services/standup/conversation_manager.py`

See gameplan for full implementation (~200 lines). Key components:
- `VALID_TRANSITIONS` dict defining state machine
- `InvalidStateTransitionError` exception
- `create_conversation()` method
- `get_conversation()` and `get_conversation_by_session()` methods
- `transition_state()` with validation
- `add_turn()` method
- `update_preferences()` method
- `set_standup_content()` method
- `cleanup_expired()` method

**Validation**:
```bash
python -c "from services.standup.conversation_manager import StandupConversationManager; m = StandupConversationManager(); print('OK')"
```

### Phase 3: Tests

#### Step 3a: Create test package

```bash
mkdir -p tests/unit/services/standup
echo '"""Issue #552: Standup conversation tests."""' > tests/unit/services/standup/__init__.py
```

#### Step 3b: Create comprehensive unit tests

**File**: `tests/unit/services/standup/test_conversation_state.py`

See gameplan for full test file (~300 lines). Required test classes:
- `TestStandupConversationState` - enum tests
- `TestStandupConversation` - dataclass tests
- `TestStandupConversationManager` - manager tests
- `TestStateTransitions` - state machine tests
- `TestConversationTurns` - turn management tests
- `TestPreferencesAndContent` - preferences tests

**Validation**:
```bash
pytest tests/unit/services/standup/test_conversation_state.py -v
```

**Expected**: 20+ tests passing

### Phase Z: Final Verification

#### Regression check
```bash
pytest tests/ -k standup --tb=short
```

#### Evidence collection
```bash
# Line counts
wc -l services/shared_types.py services/domain/models.py services/standup/*.py tests/unit/services/standup/*.py

# Import verification
python -c "from services.shared_types import StandupConversationState; print(f'Enum: {len(list(StandupConversationState))} states')"
python -c "from services.domain.models import StandupConversation; print(f'Dataclass: {len(StandupConversation.__annotations__)} fields')"
python -c "from services.standup.conversation_manager import StandupConversationManager, InvalidStateTransitionError; print('Manager: OK')"
```

---

## Success Criteria (With Evidence)

- [ ] Infrastructure matches expectations (verified with ls/grep)
- [ ] `StandupConversationState` enum has 7 states (show import)
- [ ] `StandupConversation` dataclass complete (show annotations)
- [ ] `StandupConversationManager` instantiable (show import)
- [ ] All tests pass (show pytest output with 20+ passing)
- [ ] No regressions (show `pytest tests/ -k standup` output)
- [ ] GitHub issue updated with progress

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] `ConversationState` dataclass conflicts with new enum name
- [ ] Domain model patterns differ from documented
- [ ] `SessionManager` API changed unexpectedly
- [ ] Tests fail for any reason
- [ ] Import errors in existing code after changes
- [ ] Any infrastructure mismatch with gameplan

---

## Progressive Bookending

Update GitHub issue after each phase:

**After Phase 1**:
```bash
gh issue comment 552 -b "Phase 1 Complete: Domain models
- StandupConversationState enum: 7 states in services/shared_types.py
- StandupConversation dataclass: services/domain/models.py
- Import verification: [paste output]"
```

**After Phase 2**:
```bash
gh issue comment 552 -b "Phase 2 Complete: StandupConversationManager
- Location: services/standup/conversation_manager.py
- Methods: create, get, transition, add_turn, update_preferences, set_content, cleanup
- Import verification: [paste output]"
```

**After Phase 3**:
```bash
gh issue comment 552 -b "Phase 3 Complete: Unit tests
- Location: tests/unit/services/standup/test_conversation_state.py
- Test count: X tests in 5 classes
- All passing: [paste pytest output]"
```

---

## Gameplan Reference

Full implementation details are in:
`dev/active/gameplan-552-standup-conv-state.md`

This includes:
- Complete code for enum, dataclass, and manager
- Complete test file with all test cases
- State transition validation matrix

---

## Self-Check Before Claiming Complete

1. Did I verify infrastructure first?
2. Are all 7 enum states present?
3. Does the dataclass have all required fields?
4. Does the manager have all required methods?
5. Are there 20+ tests covering all components?
6. Do all tests pass?
7. Did I check for regressions?
8. Did I provide terminal output evidence?
9. Am I guessing or do I have proof?

---

## Related Documentation
- `dev/active/gameplan-552-standup-conv-state.md` - Full gameplan
- `dev/active/issue-552-update.md` - Issue template
- `services/domain/models.py` - Existing domain models
- `services/shared_types.py` - Enum patterns

---

*Prompt Version: 1.0*
*Issue: #552*
*Epic: #242*
*Created: 2026-01-07*
