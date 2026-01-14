# Gameplan: #552 STANDUP-CONV-STATE - Conversation State Management

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/552
**Created**: 2026-01-07
**Epic**: #242 (CONV-MCP-STANDUP-INTERACTIVE)
**Approach**: Extend existing conversation infrastructure for standup-specific state machine

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (verified)
- [x] CLI structure: Click (verified)
- [x] Database: PostgreSQL on 5433 (verified)
- [x] Testing framework: pytest (verified)
- [x] Existing endpoints: `/api/v1/standup/*` (stateless generation)
- [x] Missing features: Conversation state tracking for multi-turn standup

**My understanding of the task**:
- I believe we need to: Create state management infrastructure for interactive standup conversations
- I think this involves: New enum, dataclass, and manager service
- I assume the current state is: Stateless standup generation exists, no conversation tracking

**What Already Exists** (discovered via Serena investigation):

| Component | Location | Status |
|-----------|----------|--------|
| `Conversation` dataclass | `services/domain/models.py:1235-1265` | ✅ Exists - general conversation tracking |
| `ConversationTurn` dataclass | `services/domain/models.py:1268-1310` | ✅ Exists - turn tracking with entities |
| `ConversationState` dataclass | `services/conversation/context_tracker.py:41-54` | ✅ Exists - but for entity/topic tracking, NOT state machine |
| `ConversationSession` class | `services/session/session_manager.py:8-84` | ✅ Exists - session with clarification support |
| `SessionManager` class | `services/session/session_manager.py` | ✅ Exists - session lifecycle |
| `MorningStandupWorkflow` class | `services/features/morning_standup.py` | ✅ Exists - stateless generation |
| Enum patterns | `services/shared_types.py` | ✅ 13+ enums as reference |

**Critical Insight**:
- `ConversationState` in `context_tracker.py` is a **dataclass for entity tracking**, NOT an enum for state machine states
- We need a NEW `StandupConversationState` enum (not conflicting with existing)
- Existing `Conversation` and `ConversationTurn` can potentially be reused or extended

**What's Missing**:
- `StandupConversationState` enum (state machine states)
- `StandupConversation` dataclass (or extension of existing `Conversation`)
- `StandupConversationManager` service (state transitions + validation)
- Integration point with `MorningStandupWorkflow`

### Part A.2: Design Decision

**Option A**: Create entirely new `StandupConversation` dataclass
- Pro: Clean separation, standup-specific fields
- Con: Duplication with existing `Conversation`

**Option B**: Extend existing `Conversation` with standup-specific fields
- Pro: Reuse existing infrastructure
- Con: Pollutes general model with standup concerns

**Option C**: Create `StandupConversation` that WRAPS `Conversation`
- Pro: Composition over inheritance, clean boundaries
- Con: Slightly more complex

**Recommendation**: **Option C** - Create `StandupConversation` that contains a `Conversation` reference plus standup-specific state. This follows DDD composition patterns already in codebase.

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?** (Check all that apply)

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable
- [ ] Coordination queue prompt being claimed

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment:**
- [ ] **USE WORKTREE** - 2+ parallel criteria checked
- [x] **SKIP WORKTREE** - Overhead criteria dominate
- [ ] **PM DECISION** - Mixed signals, escalate

**Rationale**: Single agent work on tightly coupled domain models + service + tests. All files should be committed atomically. Worktree overhead exceeds benefit for ~5-7 hour task.

### Part B: PM Verification Required

**PM, please confirm**:

1. **Design approach**:
   - [ ] Option A: New standalone `StandupConversation`
   - [ ] Option B: Extend existing `Conversation`
   - [x] Option C: Composition - `StandupConversation` wraps `Conversation` (recommended)

2. **Enum naming**:
   - `StandupConversationState` (to avoid conflict with existing `ConversationState` dataclass)

3. **State machine states**:
   - INITIATED → GATHERING_PREFERENCES → GENERATING → REFINING → FINALIZING → COMPLETE

4. **Persistence scope**:
   - Session-scoped (in-memory initially, database later in #556)

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** - Understanding correct
- [ ] **REVISE** - Different approach needed
- [ ] **CLARIFY** - Need more context on: ____________

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 552
   ```

2. **Codebase Investigation** ✅ (Completed via Serena)
   - Existing conversation models identified
   - Session management patterns documented
   - Enum conventions verified in shared_types.py

3. **Update GitHub Issue** (at start of work)
   ```bash
   gh issue edit 552 --body "
   ## Status: Implementation Started

   ### Progress
   - [x] Investigation complete
   - [x] Gameplan approved
   - [ ] Phase 1: Domain models
   - [ ] Phase 2: State management service
   - [ ] Phase 3: Tests
   - [ ] Phase Z: Final verification

   ### Current State
   Working on: [update as work progresses]
   "
   ```

### STOP Conditions for Phase 0
- [ ] Issue doesn't exist or wrong number
- [ ] Feature already implemented differently
- [ ] Blocking dependencies not met

---

## Phase 1: Domain Models

### 1a: Add `StandupConversationState` enum

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

**Acceptance**:
- [ ] Enum in shared_types.py
- [ ] 7 states defined
- [ ] Docstring references issue #552

**Progressive Bookending** (after completion):
```bash
gh issue comment 552 -b "✓ Phase 1a Complete: StandupConversationState enum
- Location: services/shared_types.py
- 7 states defined: INITIATED, GATHERING_PREFERENCES, GENERATING, REFINING, FINALIZING, COMPLETE, ABANDONED
- Docstring references #552"
```

### 1b: Create `StandupConversation` dataclass

**File**: `services/domain/models.py`

**Location**: After `ConversationTurn` (around line 1312)

```python
@dataclass
class StandupConversation:
    """Issue #552: Domain model for interactive standup conversations.

    Wraps a base Conversation with standup-specific state machine and preferences.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    session_id: str = ""
    user_id: str = ""

    # State machine
    state: StandupConversationState = StandupConversationState.INITIATED
    previous_state: Optional[StandupConversationState] = None

    # User preferences for this standup
    preferences: Dict[str, Any] = field(default_factory=dict)
    # Examples: {"focus": "github", "exclude": ["docs"], "format": "brief"}

    # Generated content (evolves through refinement)
    current_standup: Optional[str] = None
    standup_versions: List[str] = field(default_factory=list)  # Version history

    # Conversation turns (standup-specific)
    turns: List[ConversationTurn] = field(default_factory=list)

    # Context from integrations
    context: Dict[str, Any] = field(default_factory=dict)
    # Examples: {"github_activity": [...], "calendar_events": [...]}

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

**Acceptance**:
- [ ] Dataclass in domain/models.py
- [ ] Uses `StandupConversationState` enum
- [ ] Tracks preferences, versions, turns
- [ ] `to_dict()` method for serialization

**Progressive Bookending** (after completion):
```bash
gh issue comment 552 -b "✓ Phase 1b Complete: StandupConversation dataclass
- Location: services/domain/models.py
- Fields: id, session_id, user_id, state, preferences, turns, context, timestamps
- Includes to_dict() serialization method"
```

### 1c: Update imports

**File**: `services/domain/models.py`

Add import at top:
```python
from services.shared_types import StandupConversationState
```

---

## Phase 2: State Management Service

### 2a: Create `StandupConversationManager`

**File**: `services/standup/__init__.py` (create if needed)

```python
# services/standup/__init__.py
"""Issue #552: Standup conversation management package."""
```

**File**: `services/standup/conversation_manager.py` (new file)

```python
"""Issue #552: Standup conversation state management service."""

from datetime import datetime
from typing import Dict, Optional, List
import structlog

from services.domain.models import StandupConversation, ConversationTurn
from services.shared_types import StandupConversationState

logger = structlog.get_logger()


class InvalidStateTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
    pass


class StandupConversationManager:
    """Issue #552: Manages standup conversation state and transitions.

    Provides:
    - Conversation lifecycle (create, get, complete)
    - State machine validation
    - Turn recording
    - Session-scoped persistence
    """

    # Valid state transitions
    VALID_TRANSITIONS: Dict[StandupConversationState, List[StandupConversationState]] = {
        StandupConversationState.INITIATED: [
            StandupConversationState.GATHERING_PREFERENCES,
            StandupConversationState.GENERATING,  # Skip preferences if user wants quick standup
            StandupConversationState.ABANDONED,
        ],
        StandupConversationState.GATHERING_PREFERENCES: [
            StandupConversationState.GENERATING,
            StandupConversationState.ABANDONED,
        ],
        StandupConversationState.GENERATING: [
            StandupConversationState.REFINING,
            StandupConversationState.FINALIZING,  # Skip refinement if user accepts
            StandupConversationState.ABANDONED,
        ],
        StandupConversationState.REFINING: [
            StandupConversationState.GENERATING,  # Re-generate with new preferences
            StandupConversationState.FINALIZING,
            StandupConversationState.ABANDONED,
        ],
        StandupConversationState.FINALIZING: [
            StandupConversationState.COMPLETE,
            StandupConversationState.REFINING,  # User wants more changes
            StandupConversationState.ABANDONED,
        ],
        StandupConversationState.COMPLETE: [],  # Terminal state
        StandupConversationState.ABANDONED: [],  # Terminal state
    }

    def __init__(self):
        """Initialize with in-memory session storage."""
        self._conversations: Dict[str, StandupConversation] = {}

    def create_conversation(
        self,
        session_id: str,
        user_id: str,
        initial_context: Optional[Dict] = None
    ) -> StandupConversation:
        """Create a new standup conversation.

        Args:
            session_id: Session identifier
            user_id: User identifier
            initial_context: Optional initial context (e.g., from integrations)

        Returns:
            New StandupConversation instance
        """
        conversation = StandupConversation(
            session_id=session_id,
            user_id=user_id,
            context=initial_context or {},
        )

        self._conversations[conversation.id] = conversation

        logger.info(
            "standup_conversation_created",
            conversation_id=conversation.id,
            session_id=session_id,
            user_id=user_id,
        )

        return conversation

    def get_conversation(self, conversation_id: str) -> Optional[StandupConversation]:
        """Retrieve a conversation by ID."""
        return self._conversations.get(conversation_id)

    def get_conversation_by_session(self, session_id: str) -> Optional[StandupConversation]:
        """Retrieve active conversation for a session.

        Returns the most recent non-terminal conversation for the session.
        """
        for conv in reversed(list(self._conversations.values())):
            if conv.session_id == session_id and conv.state not in [
                StandupConversationState.COMPLETE,
                StandupConversationState.ABANDONED,
            ]:
                return conv
        return None

    def transition_state(
        self,
        conversation_id: str,
        new_state: StandupConversationState
    ) -> StandupConversation:
        """Transition conversation to a new state.

        Args:
            conversation_id: Conversation to transition
            new_state: Target state

        Returns:
            Updated conversation

        Raises:
            InvalidStateTransitionError: If transition is not valid
            KeyError: If conversation not found
        """
        conversation = self._conversations.get(conversation_id)
        if not conversation:
            raise KeyError(f"Conversation not found: {conversation_id}")

        current_state = conversation.state
        valid_targets = self.VALID_TRANSITIONS.get(current_state, [])

        if new_state not in valid_targets:
            raise InvalidStateTransitionError(
                f"Cannot transition from {current_state.value} to {new_state.value}. "
                f"Valid transitions: {[s.value for s in valid_targets]}"
            )

        conversation.previous_state = current_state
        conversation.state = new_state
        conversation.updated_at = datetime.now()

        if new_state == StandupConversationState.COMPLETE:
            conversation.completed_at = datetime.now()

        logger.info(
            "standup_conversation_state_changed",
            conversation_id=conversation_id,
            from_state=current_state.value,
            to_state=new_state.value,
        )

        return conversation

    def add_turn(
        self,
        conversation_id: str,
        user_message: str,
        assistant_response: str,
        intent: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> ConversationTurn:
        """Record a conversation turn.

        Args:
            conversation_id: Conversation to add turn to
            user_message: User's input
            assistant_response: Piper's response
            intent: Classified intent for this turn
            metadata: Additional metadata

        Returns:
            Created ConversationTurn

        Raises:
            KeyError: If conversation not found
        """
        conversation = self._conversations.get(conversation_id)
        if not conversation:
            raise KeyError(f"Conversation not found: {conversation_id}")

        turn = ConversationTurn(
            conversation_id=conversation_id,
            turn_number=len(conversation.turns) + 1,
            user_message=user_message,
            assistant_response=assistant_response,
            intent=intent,
            metadata=metadata or {},
            completed_at=datetime.now(),
        )

        conversation.turns.append(turn)
        conversation.updated_at = datetime.now()

        logger.debug(
            "standup_conversation_turn_added",
            conversation_id=conversation_id,
            turn_number=turn.turn_number,
        )

        return turn

    def update_preferences(
        self,
        conversation_id: str,
        preferences: Dict[str, Any]
    ) -> StandupConversation:
        """Update conversation preferences.

        Args:
            conversation_id: Conversation to update
            preferences: Preference dict to merge

        Returns:
            Updated conversation
        """
        conversation = self._conversations.get(conversation_id)
        if not conversation:
            raise KeyError(f"Conversation not found: {conversation_id}")

        conversation.preferences.update(preferences)
        conversation.updated_at = datetime.now()

        return conversation

    def set_standup_content(
        self,
        conversation_id: str,
        content: str
    ) -> StandupConversation:
        """Set/update the current standup content.

        Keeps version history for refinement tracking.
        """
        conversation = self._conversations.get(conversation_id)
        if not conversation:
            raise KeyError(f"Conversation not found: {conversation_id}")

        # Save previous version if exists
        if conversation.current_standup:
            conversation.standup_versions.append(conversation.current_standup)

        conversation.current_standup = content
        conversation.updated_at = datetime.now()

        return conversation

    def cleanup_expired(self, max_age_minutes: int = 60) -> int:
        """Remove abandoned/expired conversations.

        Returns count of removed conversations.
        """
        now = datetime.now()
        expired_ids = []

        for conv_id, conv in self._conversations.items():
            age_minutes = (now - conv.updated_at).total_seconds() / 60
            if age_minutes > max_age_minutes and conv.state not in [
                StandupConversationState.COMPLETE
            ]:
                expired_ids.append(conv_id)

        for conv_id in expired_ids:
            del self._conversations[conv_id]
            logger.info("standup_conversation_expired", conversation_id=conv_id)

        return len(expired_ids)
```

**Acceptance**:
- [ ] File created at `services/standup/conversation_manager.py`
- [ ] `StandupConversationManager` class implemented
- [ ] `VALID_TRANSITIONS` dict defines state machine
- [ ] `InvalidStateTransitionError` for invalid transitions
- [ ] All CRUD methods: create, get, transition, add_turn, update_preferences
- [ ] Logging with structlog

**Progressive Bookending** (after completion):
```bash
gh issue comment 552 -b "✓ Phase 2 Complete: StandupConversationManager service
- Location: services/standup/conversation_manager.py
- State machine with 7 states and validated transitions
- Methods: create_conversation, get_conversation, transition_state, add_turn, update_preferences, set_standup_content, cleanup_expired
- InvalidStateTransitionError for invalid transitions
- Structured logging integrated"
```

---

## Phase 3: Tests

### 3a: Unit tests for state transitions

**File**: `tests/unit/services/standup/test_conversation_state.py` (new file)

```python
"""Issue #552: Tests for standup conversation state management."""

import pytest
from datetime import datetime

from services.shared_types import StandupConversationState
from services.domain.models import StandupConversation, ConversationTurn
from services.standup.conversation_manager import (
    StandupConversationManager,
    InvalidStateTransitionError,
)


class TestStandupConversationState:
    """Tests for StandupConversationState enum."""

    def test_enum_has_all_states(self):
        """All required states exist."""
        states = [s.value for s in StandupConversationState]

        assert "initiated" in states
        assert "gathering_preferences" in states
        assert "generating" in states
        assert "refining" in states
        assert "finalizing" in states
        assert "complete" in states
        assert "abandoned" in states

    def test_enum_count(self):
        """Exactly 7 states defined."""
        assert len(StandupConversationState) == 7


class TestStandupConversation:
    """Tests for StandupConversation dataclass."""

    def test_default_state_is_initiated(self):
        """New conversation starts in INITIATED state."""
        conv = StandupConversation(session_id="test", user_id="user1")

        assert conv.state == StandupConversationState.INITIATED
        assert conv.previous_state is None

    def test_to_dict_serialization(self):
        """to_dict() produces valid dictionary."""
        conv = StandupConversation(
            session_id="test",
            user_id="user1",
            preferences={"focus": "github"},
        )

        result = conv.to_dict()

        assert result["session_id"] == "test"
        assert result["user_id"] == "user1"
        assert result["state"] == "initiated"
        assert result["preferences"] == {"focus": "github"}
        assert "id" in result
        assert "created_at" in result


class TestStandupConversationManager:
    """Tests for StandupConversationManager service."""

    @pytest.fixture
    def manager(self):
        """Fresh manager for each test."""
        return StandupConversationManager()

    def test_create_conversation(self, manager):
        """Create conversation initializes correctly."""
        conv = manager.create_conversation(
            session_id="session1",
            user_id="user1",
            initial_context={"source": "test"},
        )

        assert conv.session_id == "session1"
        assert conv.user_id == "user1"
        assert conv.state == StandupConversationState.INITIATED
        assert conv.context == {"source": "test"}

    def test_get_conversation(self, manager):
        """Retrieve conversation by ID."""
        conv = manager.create_conversation("s1", "u1")

        retrieved = manager.get_conversation(conv.id)

        assert retrieved is not None
        assert retrieved.id == conv.id

    def test_get_conversation_not_found(self, manager):
        """Non-existent conversation returns None."""
        result = manager.get_conversation("nonexistent")

        assert result is None

    def test_get_conversation_by_session(self, manager):
        """Find active conversation for session."""
        conv = manager.create_conversation("session1", "user1")

        found = manager.get_conversation_by_session("session1")

        assert found is not None
        assert found.id == conv.id

    def test_get_conversation_by_session_ignores_complete(self, manager):
        """Completed conversations are not returned by session lookup."""
        conv = manager.create_conversation("session1", "user1")
        manager.transition_state(conv.id, StandupConversationState.GENERATING)
        manager.transition_state(conv.id, StandupConversationState.FINALIZING)
        manager.transition_state(conv.id, StandupConversationState.COMPLETE)

        found = manager.get_conversation_by_session("session1")

        assert found is None


class TestStateTransitions:
    """Tests for state transition validation."""

    @pytest.fixture
    def manager(self):
        return StandupConversationManager()

    @pytest.fixture
    def conversation(self, manager):
        return manager.create_conversation("s1", "u1")

    def test_valid_transition_initiated_to_gathering(self, manager, conversation):
        """INITIATED → GATHERING_PREFERENCES is valid."""
        result = manager.transition_state(
            conversation.id,
            StandupConversationState.GATHERING_PREFERENCES
        )

        assert result.state == StandupConversationState.GATHERING_PREFERENCES
        assert result.previous_state == StandupConversationState.INITIATED

    def test_valid_transition_initiated_to_generating(self, manager, conversation):
        """INITIATED → GENERATING is valid (skip preferences)."""
        result = manager.transition_state(
            conversation.id,
            StandupConversationState.GENERATING
        )

        assert result.state == StandupConversationState.GENERATING

    def test_valid_transition_generating_to_refining(self, manager, conversation):
        """GENERATING → REFINING is valid."""
        manager.transition_state(conversation.id, StandupConversationState.GENERATING)

        result = manager.transition_state(
            conversation.id,
            StandupConversationState.REFINING
        )

        assert result.state == StandupConversationState.REFINING

    def test_valid_transition_to_complete(self, manager, conversation):
        """Full path to COMPLETE."""
        manager.transition_state(conversation.id, StandupConversationState.GENERATING)
        manager.transition_state(conversation.id, StandupConversationState.FINALIZING)

        result = manager.transition_state(
            conversation.id,
            StandupConversationState.COMPLETE
        )

        assert result.state == StandupConversationState.COMPLETE
        assert result.completed_at is not None

    def test_invalid_transition_raises_error(self, manager, conversation):
        """Invalid transition raises InvalidStateTransitionError."""
        with pytest.raises(InvalidStateTransitionError) as exc_info:
            manager.transition_state(
                conversation.id,
                StandupConversationState.COMPLETE  # Can't go directly to COMPLETE
            )

        assert "Cannot transition" in str(exc_info.value)
        assert "initiated" in str(exc_info.value).lower()

    def test_transition_from_complete_raises_error(self, manager, conversation):
        """Cannot transition out of COMPLETE (terminal state)."""
        manager.transition_state(conversation.id, StandupConversationState.GENERATING)
        manager.transition_state(conversation.id, StandupConversationState.FINALIZING)
        manager.transition_state(conversation.id, StandupConversationState.COMPLETE)

        with pytest.raises(InvalidStateTransitionError):
            manager.transition_state(
                conversation.id,
                StandupConversationState.REFINING
            )

    def test_transition_to_abandoned_from_any_state(self, manager, conversation):
        """Can abandon from any non-terminal state."""
        # From INITIATED
        result = manager.transition_state(
            conversation.id,
            StandupConversationState.ABANDONED
        )

        assert result.state == StandupConversationState.ABANDONED


class TestConversationTurns:
    """Tests for turn management."""

    @pytest.fixture
    def manager(self):
        return StandupConversationManager()

    @pytest.fixture
    def conversation(self, manager):
        return manager.create_conversation("s1", "u1")

    def test_add_turn(self, manager, conversation):
        """Add turn records correctly."""
        turn = manager.add_turn(
            conversation.id,
            user_message="standup",
            assistant_response="Ready for your standup?",
            intent="standup_request",
        )

        assert turn.turn_number == 1
        assert turn.user_message == "standup"
        assert turn.assistant_response == "Ready for your standup?"
        assert turn.intent == "standup_request"

    def test_turn_numbers_increment(self, manager, conversation):
        """Turn numbers increment correctly."""
        turn1 = manager.add_turn(conversation.id, "msg1", "resp1")
        turn2 = manager.add_turn(conversation.id, "msg2", "resp2")
        turn3 = manager.add_turn(conversation.id, "msg3", "resp3")

        assert turn1.turn_number == 1
        assert turn2.turn_number == 2
        assert turn3.turn_number == 3

        conv = manager.get_conversation(conversation.id)
        assert len(conv.turns) == 3


class TestPreferencesAndContent:
    """Tests for preferences and standup content management."""

    @pytest.fixture
    def manager(self):
        return StandupConversationManager()

    @pytest.fixture
    def conversation(self, manager):
        return manager.create_conversation("s1", "u1")

    def test_update_preferences(self, manager, conversation):
        """Preferences merge correctly."""
        manager.update_preferences(conversation.id, {"focus": "github"})
        manager.update_preferences(conversation.id, {"exclude": ["docs"]})

        conv = manager.get_conversation(conversation.id)

        assert conv.preferences["focus"] == "github"
        assert conv.preferences["exclude"] == ["docs"]

    def test_set_standup_content_tracks_versions(self, manager, conversation):
        """Content changes are versioned."""
        manager.set_standup_content(conversation.id, "Version 1")
        manager.set_standup_content(conversation.id, "Version 2")
        manager.set_standup_content(conversation.id, "Version 3")

        conv = manager.get_conversation(conversation.id)

        assert conv.current_standup == "Version 3"
        assert conv.standup_versions == ["Version 1", "Version 2"]
```

**Acceptance**:
- [ ] Test file created
- [ ] All state transitions tested
- [ ] Invalid transitions tested
- [ ] Turn management tested
- [ ] Preferences and content tested
- [ ] All tests pass

**Test Scope Requirements**:
- **Unit tests**: StandupConversationState enum, StandupConversation dataclass, StandupConversationManager methods
- **Integration tests**: N/A for this issue (deferred to #553)
- **Performance tests**: N/A for this issue (deferred to #556)
- **Regression tests**: Verify existing standup functionality unchanged (`pytest tests/ -k standup`)

**Progressive Bookending** (after completion):
```bash
gh issue comment 552 -b "✓ Phase 3 Complete: Unit tests
- Location: tests/unit/services/standup/test_conversation_state.py
- Test count: 20+ tests across 5 test classes
- Coverage: enum states, dataclass serialization, state transitions, turn management, preferences
- All tests passing: [paste pytest output]"
```

---

## Phase Z: Final Bookending & Handoff

### Verification Gates

- [ ] Phase 1: Domain models created (enum + dataclass)
- [ ] Phase 2: StandupConversationManager implemented
- [ ] Phase 3: All tests passing
- [ ] Regression tests: `pytest tests/ -k standup` passes

### GitHub Final Update

```bash
gh issue edit 552 --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] All acceptance criteria met
- [x] Tests passing: [link to test output]
- [x] No regressions: pytest tests/ -k standup passed
- [x] Documentation updated

### Implementation Details
- StandupConversationState enum: 7 states in services/shared_types.py
- StandupConversation dataclass: services/domain/models.py
- StandupConversationManager: services/standup/conversation_manager.py
- Tests: tests/unit/services/standup/test_conversation_state.py (20+ tests)

### Ready for PM Review
"
```

### Documentation Updates Checklist

- [ ] Update relevant ADRs if decisions made (N/A - no architectural changes)
- [ ] Update architecture.md if flow changed (N/A - infrastructure only)
- [ ] Remove/update misleading TODO comments
- [ ] Update CURRENT-STATE.md if significant (add #552 to completed)

### Evidence Compilation

- [ ] All terminal outputs in session log
- [ ] Key code changes documented (files created/modified list)
- [ ] Before/after behavior captured (N/A - new feature)
- [ ] Performance metrics if relevant (N/A - deferred to #556)

### Completion Matrix

| Component | Status | Evidence |
|-----------|--------|----------|
| `StandupConversationState` enum | ⏸️ | |
| `StandupConversation` dataclass | ⏸️ | |
| `services/standup/__init__.py` | ⏸️ | |
| `StandupConversationManager` class | ⏸️ | |
| State transition validation | ⏸️ | |
| Unit tests | ⏸️ | |

### Manual Testing Checklist

- [ ] Create conversation via manager
- [ ] Walk through full state machine: INITIATED → GATHERING_PREFERENCES → GENERATING → REFINING → FINALIZING → COMPLETE
- [ ] Verify invalid transitions raise errors
- [ ] Verify turn history preserved
- [ ] Verify preferences merge correctly

### Evidence Required

1. Test output showing all tests pass
2. Files created with line counts
3. No regressions in existing standup functionality (`pytest tests/ -k standup`)

### Handoff Preparation (for #553)

- [ ] Document any discoveries for next issue
- [ ] Note unexpected complexities encountered
- [ ] Flag architectural concerns (if any)
- [ ] Prepare context: #553 can now use `StandupConversationManager` for conversation flow logic

### Handoff Quality Checklist

Before accepting as complete:
- [ ] All acceptance criteria checkboxes addressed
- [ ] Test output provided (not just "tests pass")
- [ ] Files modified list included
- [ ] User verification steps documented
- [ ] Blockers explicitly stated (if any)

### PM Approval Request Template

```markdown
@PM - Issue #552 complete and ready for review:
- All acceptance criteria met ✓
- Evidence provided ✓
- Documentation updated ✓
- No regressions confirmed ✓
- Tests: 20+ passing (output in session log)

Files created:
- services/shared_types.py (modified - added StandupConversationState enum)
- services/domain/models.py (modified - added StandupConversation dataclass)
- services/standup/__init__.py (new)
- services/standup/conversation_manager.py (new)
- tests/unit/services/standup/__init__.py (new)
- tests/unit/services/standup/test_conversation_state.py (new)

Please review and close if satisfied.
```

### Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met
- [ ] Completion matrix 100%
- [ ] Evidence provided for each criterion
- [ ] Tests passing with output
- [ ] No regressions confirmed
- [ ] STOP conditions all clear
- [ ] GitHub issue fully updated
- [ ] PM approval requested

**Status**: Not Started

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent Type | Task | Evidence Required | Handoff |
|-------|------------|------|-------------------|---------|
| 0 | Lead Dev | GitHub setup | Issue updated | - |
| 1 | Code Agent | Domain models | Enum + dataclass in files | Import verification |
| 2 | Code Agent | Service implementation | Manager class complete | Method count |
| 3 | Code Agent | Tests | 20+ tests passing | pytest output |
| Z | Lead Dev | Final verification | All criteria met | PM approval request |

### Agent Instructions

**Single Agent Recommended** (see Part A.2 assessment)

This is tightly-coupled sequential work best suited for a single code agent:
1. Domain models must exist before service can import them
2. Service must exist before tests can import it
3. All files should be committed atomically

**Claude Code Instructions** (if assigned):
```markdown
Issue #552: Implement standup conversation state management

1. Create StandupConversationState enum in services/shared_types.py
2. Create StandupConversation dataclass in services/domain/models.py
3. Create services/standup/ package with conversation_manager.py
4. Create comprehensive unit tests
5. Verify no regressions: pytest tests/ -k standup

Evidence: Provide test output and file locations for each phase.
```

### Evidence Collection Points

1. **After Phase 1**: Verify enum and dataclass importable
   ```bash
   python -c "from services.shared_types import StandupConversationState; print(list(StandupConversationState))"
   python -c "from services.domain.models import StandupConversation; print(StandupConversation.__annotations__)"
   ```

2. **After Phase 2**: Verify service instantiable
   ```bash
   python -c "from services.standup.conversation_manager import StandupConversationManager; m = StandupConversationManager(); print('OK')"
   ```

3. **After Phase 3**: Full test suite
   ```bash
   pytest tests/unit/services/standup/test_conversation_state.py -v
   ```

4. **Before Phase Z closure**: Regression check
   ```bash
   pytest tests/ -k standup --tb=short
   ```

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] Existing `ConversationState` dataclass conflicts with new enum
- [ ] Domain model patterns differ from documented
- [ ] `SessionManager` API changed
- [ ] Tests fail for any reason
- [ ] Integration points with `MorningStandupWorkflow` unclear

---

## Evidence Requirements

### What Counts as Evidence
✅ Terminal output showing success
✅ Test results with full output
✅ Import verification commands
✅ Git commits/diffs
✅ File line counts

❌ "Should work"
❌ "Tests pass" without output
❌ "Fixed" without proof
❌ Assumptions about behavior

---

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `services/shared_types.py` | Modify | Add `StandupConversationState` enum |
| `services/domain/models.py` | Modify | Add `StandupConversation` dataclass |
| `services/standup/__init__.py` | Create | Package init |
| `services/standup/conversation_manager.py` | Create | State management service |
| `tests/unit/services/standup/__init__.py` | Create | Test package init |
| `tests/unit/services/standup/test_conversation_state.py` | Create | Unit tests |

---

## Effort Estimate

**Overall Size**: Medium (1-2 days)

| Phase | Estimate |
|-------|----------|
| Phase -1 | Done (investigation complete) |
| Phase 1 | 1-2 hours (domain models) |
| Phase 2 | 2-3 hours (service implementation) |
| Phase 3 | 1-2 hours (tests) |
| Phase Z | 30 min (documentation) |

**Total**: ~5-7 hours

---

## Deferred (to #553)

- Integration with `MorningStandupWorkflow`
- Actual conversation flow logic
- Multi-turn response generation
- Preference application to standup generation

These require #553 (Conversation Flow) which depends on this infrastructure.

---

_Gameplan created: 2026-01-07_
_Investigation method: Serena symbolic queries_
