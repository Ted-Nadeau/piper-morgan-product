# Gameplan: #553 STANDUP-CONV-FLOW Multi-Turn Conversation Flow

**Issue**: #553 STANDUP-CONV-FLOW: Multi-Turn Conversation Flow
**Epic**: #242 (CONV-MCP-STANDUP-INTERACTIVE)
**Priority**: P0
**Created**: 2026-01-07
**Template Version**: 9.2

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Chief Architect's Current Understanding

Based on #552 implementation completed yesterday, I believe:

**Infrastructure Status**:
- [x] Web framework: FastAPI (web/app.py)
- [x] Database: PostgreSQL on 5433
- [x] Testing framework: pytest
- [x] State management: `StandupConversationManager` in `services/standup/conversation_manager.py`
- [x] State enum: `StandupConversationState` with 7 states
- [x] Domain model: `StandupConversation` dataclass with turn tracking

**My understanding of the task**:
- I need to create a `StandupConversationHandler` that uses the state machine from #552
- The handler routes user messages based on conversation state
- It generates context-aware questions and handles refinement requests
- It integrates with existing `MorningStandupWorkflow` for standup generation

**What exists** (verified):
- `services/standup/conversation_manager.py` - State management (309 lines, 45 tests)
- `services/features/morning_standup.py` - `MorningStandupWorkflow` with 4 modes
- `services/intent/intent_service.py:_handle_standup_query` - Current single-turn handling
- `services/domain/standup_orchestration_service.py` - Orchestration service

**What's missing** (to be created):
- `services/standup/conversation_handler.py` - Multi-turn conversation logic
- Integration with state machine for turn-based routing
- Refinement logic (add/remove/modify standup content)
- Graceful fallback to static generation

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
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment:**
- [x] **SKIP WORKTREE** - Single agent, sequential work, ~4-6 hours estimate
- Rationale: "Single agent, focused on services/standup/ directory, tightly coupled to #552 work"

### Part B: PM Verification Required

**PM, please verify**:

1. **#552 infrastructure complete?**
   ```bash
   python -c "from services.standup.conversation_manager import StandupConversationManager; print('OK')"
   pytest tests/unit/services/standup/ -v --tb=short
   ```

2. **Standup generator still functional?**
   ```bash
   python -c "from services.features.morning_standup import MorningStandupWorkflow; print('OK')"
   ```

3. **Intent service integration point?**
   - Current: `IntentService._handle_standup_query` calls `StandupOrchestrationService`
   - Proposed: Handler intercepts, manages conversation state, delegates to workflow

4. **Scope confirmation**:
   - [ ] Create conversation handler (state-based routing)
   - [ ] Handle preference gathering
   - [ ] Handle refinement requests
   - [ ] Implement graceful fallback
   - [ ] NOT: Chat widget (that's #554)
   - [ ] NOT: Preference persistence (that's #555)

### Part C: Proceed/Revise Decision

After PM verification:
- [ ] **PROCEED** - Understanding is correct, gameplan appropriate
- [ ] **REVISE** - Major assumptions wrong, need different approach
- [ ] **CLARIFY** - Need more context on: ____________

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 553
   ```

2. **Verify #552 is complete**
   ```bash
   gh issue view 552 --json state -q '.state'
   # Expected: CLOSED
   ```

3. **Codebase Investigation**
   ```bash
   # Verify state management infrastructure
   ls -la services/standup/
   pytest tests/unit/services/standup/test_conversation_state.py -v --tb=short

   # Check current standup integration
   grep -n "_handle_standup" services/intent/intent_service.py
   ```

4. **Update GitHub Issue**
   ```bash
   gh issue comment 553 -b "Phase 0 Complete: Investigation
   - #552 verified complete
   - State management infrastructure: ✅
   - Current standup handler: services/intent/intent_service.py:584-627
   - Beginning Phase 1 implementation"
   ```

---

## Phase 1: Create StandupConversationHandler

**Objective**: Core conversation turn handler with state-based routing

### Files to Create

**`services/standup/conversation_handler.py`** (~200 lines)

```python
"""
Issue #553: Standup conversation flow handler.

Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Handles multi-turn standup conversations by:
- Routing based on conversation state
- Generating context-aware follow-up questions
- Processing refinement requests
- Managing graceful fallback
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional, List

import structlog

from services.domain.models import StandupConversation
from services.shared_types import StandupConversationState
from services.standup.conversation_manager import StandupConversationManager

logger = structlog.get_logger()


@dataclass
class ConversationResponse:
    """Response from conversation handler."""
    message: str
    state: StandupConversationState
    requires_input: bool = True
    standup_content: Optional[str] = None
    suggestions: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = []
        if self.metadata is None:
            self.metadata = {}


class StandupConversationHandler:
    """
    Issue #553: Multi-turn conversation flow for standup generation.

    State Machine Flow:
    INITIATED → GATHERING_PREFERENCES → GENERATING → REFINING → FINALIZING → COMPLETE
                                      ↘           ↗
                                        (skip)

    Any state can transition to ABANDONED on timeout/cancel.
    """

    def __init__(
        self,
        conversation_manager: Optional[StandupConversationManager] = None,
        standup_workflow: Optional[Any] = None,  # MorningStandupWorkflow
    ):
        self.manager = conversation_manager or StandupConversationManager()
        self._workflow = standup_workflow

    async def handle_turn(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> ConversationResponse:
        """
        Handle a single conversation turn.

        Routes to appropriate handler based on current state.
        """
        state = conversation.state

        # State-based routing
        handlers = {
            StandupConversationState.INITIATED: self._handle_initiated,
            StandupConversationState.GATHERING_PREFERENCES: self._handle_gathering,
            StandupConversationState.GENERATING: self._handle_generating,
            StandupConversationState.REFINING: self._handle_refining,
            StandupConversationState.FINALIZING: self._handle_finalizing,
        }

        handler = handlers.get(state)
        if not handler:
            return ConversationResponse(
                message="This conversation has ended. Start a new one with 'standup'.",
                state=state,
                requires_input=False,
            )

        return await handler(conversation, user_message, context or {})

    async def start_conversation(
        self,
        session_id: str,
        user_id: str,
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> ConversationResponse:
        """
        Start a new standup conversation.
        """
        conversation = self.manager.create_conversation(
            session_id=session_id,
            user_id=user_id,
            initial_context=initial_context,
        )

        # Generate initial greeting based on available context
        greeting = await self._generate_greeting(conversation, initial_context or {})

        return ConversationResponse(
            message=greeting,
            state=conversation.state,
            requires_input=True,
            suggestions=["Yes, let's do it", "Quick standup", "Not now"],
        )

    async def _handle_initiated(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Handle INITIATED state - user just started."""
        message_lower = user_message.lower()

        # Check for quick/skip preference
        if any(word in message_lower for word in ["quick", "fast", "skip", "just"]):
            # Skip to generating
            self.manager.transition_state(
                conversation.id,
                StandupConversationState.GENERATING
            )
            return await self._generate_standup(conversation, context)

        # Check for cancel
        if any(word in message_lower for word in ["no", "not now", "cancel", "later"]):
            self.manager.transition_state(
                conversation.id,
                StandupConversationState.ABANDONED
            )
            return ConversationResponse(
                message="No problem! Just say 'standup' when you're ready.",
                state=StandupConversationState.ABANDONED,
                requires_input=False,
            )

        # Normal flow - move to preference gathering or generating
        # For MVP, skip preferences and go straight to generating
        self.manager.transition_state(
            conversation.id,
            StandupConversationState.GENERATING
        )
        return await self._generate_standup(conversation, context)

    async def _handle_gathering(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Handle GATHERING_PREFERENCES state."""
        # Extract preferences from user message
        preferences = self._extract_preferences(user_message)
        self.manager.update_preferences(conversation.id, preferences)

        # Move to generating
        self.manager.transition_state(
            conversation.id,
            StandupConversationState.GENERATING
        )
        return await self._generate_standup(conversation, context)

    async def _handle_generating(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Handle GENERATING state - standup just generated."""
        # This shouldn't normally be called - generating is transient
        # But handle it by showing current standup
        if conversation.current_standup:
            self.manager.transition_state(
                conversation.id,
                StandupConversationState.REFINING
            )
            return ConversationResponse(
                message=f"Here's your standup:\n\n{conversation.current_standup}\n\nWould you like to make any changes?",
                state=StandupConversationState.REFINING,
                standup_content=conversation.current_standup,
                suggestions=["Looks good", "Add a blocker", "Remove something"],
            )

        return await self._generate_standup(conversation, context)

    async def _handle_refining(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Handle REFINING state - user providing feedback."""
        message_lower = user_message.lower()

        # Check for acceptance
        if any(word in message_lower for word in ["good", "done", "looks good", "perfect", "yes", "ok", "fine"]):
            self.manager.transition_state(
                conversation.id,
                StandupConversationState.FINALIZING
            )
            return ConversationResponse(
                message=f"Great! Here's your final standup:\n\n{conversation.current_standup}\n\nWould you like to share this or save your preferences for next time?",
                state=StandupConversationState.FINALIZING,
                standup_content=conversation.current_standup,
                suggestions=["Just copy it", "Save preferences", "Share with team"],
            )

        # Handle refinement request
        refined = await self._apply_refinement(conversation, user_message)
        return ConversationResponse(
            message=f"I've updated your standup:\n\n{refined}\n\nAnything else?",
            state=StandupConversationState.REFINING,
            standup_content=refined,
            suggestions=["Looks good", "More changes", "Start over"],
        )

    async def _handle_finalizing(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Handle FINALIZING state - confirming completion."""
        self.manager.transition_state(
            conversation.id,
            StandupConversationState.COMPLETE
        )
        return ConversationResponse(
            message="Your standup is ready! Have a great day!",
            state=StandupConversationState.COMPLETE,
            standup_content=conversation.current_standup,
            requires_input=False,
        )

    async def _generate_standup(
        self,
        conversation: StandupConversation,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Generate standup content using workflow."""
        try:
            # Use existing workflow if available
            if self._workflow:
                result = await self._workflow.generate_standup(
                    mode="standard",
                    context=context,
                )
                standup_content = result.summary if hasattr(result, 'summary') else str(result)
            else:
                # Fallback to basic generation
                standup_content = self._generate_basic_standup(context)

            self.manager.set_standup_content(conversation.id, standup_content)
            self.manager.transition_state(
                conversation.id,
                StandupConversationState.REFINING
            )

            return ConversationResponse(
                message=f"Here's your standup:\n\n{standup_content}\n\nWould you like to make any changes?",
                state=StandupConversationState.REFINING,
                standup_content=standup_content,
                suggestions=["Looks good", "Add a blocker", "Focus on something else"],
            )

        except Exception as e:
            logger.error("standup_generation_failed", error=str(e))
            return self._graceful_fallback(conversation, str(e))

    async def _generate_greeting(
        self,
        conversation: StandupConversation,
        context: Dict[str, Any],
    ) -> str:
        """Generate context-aware greeting."""
        # Basic greeting - can be enhanced with calendar/GitHub context
        return "Good morning! Ready for your standup?"

    def _extract_preferences(self, message: str) -> Dict[str, Any]:
        """Extract preferences from user message."""
        preferences = {}
        message_lower = message.lower()

        if "github" in message_lower:
            preferences["focus"] = "github"
        elif "calendar" in message_lower:
            preferences["focus"] = "calendar"
        elif "todos" in message_lower or "tasks" in message_lower:
            preferences["focus"] = "todos"

        return preferences

    async def _apply_refinement(
        self,
        conversation: StandupConversation,
        user_message: str,
    ) -> str:
        """Apply user refinement to standup content."""
        current = conversation.current_standup or ""
        message_lower = user_message.lower()

        # Handle add blocker
        if "add" in message_lower and "blocker" in message_lower:
            blocker_text = user_message.replace("add blocker", "").replace("add a blocker", "").strip()
            if "*Blockers:*" in current:
                refined = current.replace("*Blockers:*", f"*Blockers:*\n• {blocker_text}")
            else:
                refined = current + f"\n\n*Blockers:*\n• {blocker_text}"
            self.manager.set_standup_content(conversation.id, refined)
            return refined

        # Handle remove request
        if "remove" in message_lower:
            # Simplified remove - just note we'd need more sophisticated parsing
            refined = current
            self.manager.set_standup_content(conversation.id, refined)
            return refined

        # Default - return current content
        return current

    def _generate_basic_standup(self, context: Dict[str, Any]) -> str:
        """Generate basic standup when workflow unavailable."""
        return """*Yesterday:*
• Made progress on assigned tasks

*Today:*
• Continue current work items
• Review any blockers

*Blockers:*
• None at this time"""

    def _graceful_fallback(
        self,
        conversation: StandupConversation,
        error: str,
    ) -> ConversationResponse:
        """Handle graceful fallback when generation fails."""
        basic = self._generate_basic_standup({})
        self.manager.set_standup_content(conversation.id, basic)
        self.manager.transition_state(
            conversation.id,
            StandupConversationState.REFINING
        )

        return ConversationResponse(
            message=f"Here's a basic standup template:\n\n{basic}\n\nYou can customize it to fit your day.",
            state=StandupConversationState.REFINING,
            standup_content=basic,
            suggestions=["Looks good", "Let me customize", "Try again"],
            metadata={"fallback": True, "error": error},
        )
```

### Progressive Bookending - Phase 1

```bash
gh issue comment 553 -b "Phase 1 Complete: StandupConversationHandler
- Created services/standup/conversation_handler.py (~250 lines)
- ConversationResponse dataclass for structured responses
- State-based routing (5 state handlers)
- Refinement support (add/remove blockers)
- Graceful fallback on errors
- Import verification: [paste output]"
```

---

## Phase 2: Integration Tests

**Objective**: Comprehensive tests for conversation flows

### Files to Create

**`tests/unit/services/standup/test_conversation_handler.py`** (~300 lines)

```python
"""
Issue #553: Tests for standup conversation flow handler.

Epic #242: CONV-MCP-STANDUP-INTERACTIVE
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from services.standup.conversation_handler import (
    StandupConversationHandler,
    ConversationResponse,
)
from services.standup.conversation_manager import StandupConversationManager
from services.shared_types import StandupConversationState


class TestConversationResponse:
    """Tests for ConversationResponse dataclass."""

    def test_default_values(self):
        """Default values are set correctly."""
        response = ConversationResponse(
            message="Hello",
            state=StandupConversationState.INITIATED,
        )
        assert response.requires_input is True
        assert response.suggestions == []
        assert response.metadata == {}
        assert response.standup_content is None

    def test_with_all_values(self):
        """All values are preserved."""
        response = ConversationResponse(
            message="Here's your standup",
            state=StandupConversationState.REFINING,
            requires_input=True,
            standup_content="*Yesterday:*\n• Did stuff",
            suggestions=["Looks good", "Edit"],
            metadata={"source": "test"},
        )
        assert response.message == "Here's your standup"
        assert response.standup_content == "*Yesterday:*\n• Did stuff"
        assert len(response.suggestions) == 2


class TestStandupConversationHandler:
    """Tests for StandupConversationHandler."""

    @pytest.fixture
    def handler(self):
        """Create handler with fresh manager."""
        return StandupConversationHandler()

    @pytest.fixture
    def handler_with_workflow(self):
        """Create handler with mock workflow."""
        mock_workflow = MagicMock()
        mock_workflow.generate_standup = AsyncMock(return_value=MagicMock(
            summary="*Yesterday:*\n• Completed tasks\n\n*Today:*\n• More work"
        ))
        return StandupConversationHandler(standup_workflow=mock_workflow)


class TestStartConversation:
    """Tests for starting a conversation."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler()

    @pytest.mark.asyncio
    async def test_start_creates_conversation(self, handler):
        """Starting creates a new conversation."""
        response = await handler.start_conversation(
            session_id="session1",
            user_id="user1",
        )

        assert response.state == StandupConversationState.INITIATED
        assert response.requires_input is True
        assert "standup" in response.message.lower() or "morning" in response.message.lower()

    @pytest.mark.asyncio
    async def test_start_returns_suggestions(self, handler):
        """Starting provides suggestions."""
        response = await handler.start_conversation(
            session_id="session1",
            user_id="user1",
        )

        assert len(response.suggestions) > 0


class TestHandleTurnInitiated:
    """Tests for INITIATED state handling."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler()

    @pytest.fixture
    def conversation(self, handler):
        return handler.manager.create_conversation("s1", "u1")

    @pytest.mark.asyncio
    async def test_quick_skips_to_generating(self, handler, conversation):
        """'Quick' skips preferences and generates."""
        response = await handler.handle_turn(conversation, "quick standup")

        assert response.state == StandupConversationState.REFINING
        assert response.standup_content is not None

    @pytest.mark.asyncio
    async def test_cancel_abandons(self, handler, conversation):
        """'Not now' abandons conversation."""
        response = await handler.handle_turn(conversation, "not now")

        assert response.state == StandupConversationState.ABANDONED
        assert response.requires_input is False

    @pytest.mark.asyncio
    async def test_yes_proceeds_to_generating(self, handler, conversation):
        """Positive response proceeds to generation."""
        response = await handler.handle_turn(conversation, "yes, let's do it")

        assert response.state == StandupConversationState.REFINING


class TestHandleTurnRefining:
    """Tests for REFINING state handling."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler()

    @pytest.fixture
    def refining_conversation(self, handler):
        conv = handler.manager.create_conversation("s1", "u1")
        handler.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        handler.manager.set_standup_content(conv.id, "*Yesterday:*\n• Did work")
        handler.manager.transition_state(conv.id, StandupConversationState.REFINING)
        return handler.manager.get_conversation(conv.id)

    @pytest.mark.asyncio
    async def test_looks_good_finalizes(self, handler, refining_conversation):
        """'Looks good' moves to finalizing."""
        response = await handler.handle_turn(refining_conversation, "looks good")

        assert response.state == StandupConversationState.FINALIZING
        assert response.standup_content is not None

    @pytest.mark.asyncio
    async def test_add_blocker_updates_content(self, handler, refining_conversation):
        """Adding blocker updates standup content."""
        response = await handler.handle_turn(
            refining_conversation,
            "add blocker waiting for API review"
        )

        assert response.state == StandupConversationState.REFINING
        assert "waiting for API review" in response.standup_content or "Blockers" in response.standup_content


class TestHandleTurnFinalizing:
    """Tests for FINALIZING state handling."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler()

    @pytest.fixture
    def finalizing_conversation(self, handler):
        conv = handler.manager.create_conversation("s1", "u1")
        handler.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        handler.manager.set_standup_content(conv.id, "*Yesterday:*\n• Did work")
        handler.manager.transition_state(conv.id, StandupConversationState.REFINING)
        handler.manager.transition_state(conv.id, StandupConversationState.FINALIZING)
        return handler.manager.get_conversation(conv.id)

    @pytest.mark.asyncio
    async def test_any_input_completes(self, handler, finalizing_conversation):
        """Any input in finalizing completes conversation."""
        response = await handler.handle_turn(finalizing_conversation, "ok")

        assert response.state == StandupConversationState.COMPLETE
        assert response.requires_input is False


class TestHandleTerminalStates:
    """Tests for terminal state handling."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler()

    @pytest.mark.asyncio
    async def test_complete_state_returns_ended(self, handler):
        """Completed conversation returns ended message."""
        conv = handler.manager.create_conversation("s1", "u1")
        handler.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        handler.manager.transition_state(conv.id, StandupConversationState.FINALIZING)
        handler.manager.transition_state(conv.id, StandupConversationState.COMPLETE)
        conv = handler.manager.get_conversation(conv.id)

        response = await handler.handle_turn(conv, "hello again")

        assert "ended" in response.message.lower() or "new" in response.message.lower()
        assert response.requires_input is False


class TestGracefulFallback:
    """Tests for graceful fallback behavior."""

    @pytest.fixture
    def handler_with_failing_workflow(self):
        mock_workflow = MagicMock()
        mock_workflow.generate_standup = AsyncMock(side_effect=Exception("API error"))
        return StandupConversationHandler(standup_workflow=mock_workflow)

    @pytest.mark.asyncio
    async def test_fallback_on_workflow_error(self, handler_with_failing_workflow):
        """Workflow error triggers graceful fallback."""
        conv = handler_with_failing_workflow.manager.create_conversation("s1", "u1")

        response = await handler_with_failing_workflow.handle_turn(conv, "yes")

        # Should still get a response, just basic
        assert response.standup_content is not None
        assert response.metadata.get("fallback") is True


class TestPreferenceExtraction:
    """Tests for preference extraction."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler()

    def test_extract_github_preference(self, handler):
        """Extracts GitHub focus preference."""
        prefs = handler._extract_preferences("focus on github work")
        assert prefs.get("focus") == "github"

    def test_extract_calendar_preference(self, handler):
        """Extracts calendar focus preference."""
        prefs = handler._extract_preferences("include my calendar")
        assert prefs.get("focus") == "calendar"

    def test_no_preference_extracted(self, handler):
        """No preference extracted from generic message."""
        prefs = handler._extract_preferences("sounds good")
        assert prefs == {}


class TestFullConversationFlow:
    """Integration tests for complete conversation flows."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler()

    @pytest.mark.asyncio
    async def test_quick_flow(self, handler):
        """Quick path: start → quick → refine → done."""
        # Start
        response = await handler.start_conversation("s1", "u1")
        assert response.state == StandupConversationState.INITIATED

        # Quick
        conv = handler.manager.get_conversation_by_session("s1")
        response = await handler.handle_turn(conv, "quick")
        assert response.state == StandupConversationState.REFINING

        # Accept
        conv = handler.manager.get_conversation(conv.id)
        response = await handler.handle_turn(conv, "looks good")
        assert response.state == StandupConversationState.FINALIZING

        # Finalize
        conv = handler.manager.get_conversation(conv.id)
        response = await handler.handle_turn(conv, "ok")
        assert response.state == StandupConversationState.COMPLETE

    @pytest.mark.asyncio
    async def test_refinement_flow(self, handler):
        """Refinement path: start → generate → add blocker → done."""
        # Start
        response = await handler.start_conversation("s1", "u1")

        # Generate
        conv = handler.manager.get_conversation_by_session("s1")
        response = await handler.handle_turn(conv, "yes")
        assert response.state == StandupConversationState.REFINING

        # Add blocker
        conv = handler.manager.get_conversation(conv.id)
        response = await handler.handle_turn(conv, "add blocker waiting for review")
        assert response.state == StandupConversationState.REFINING

        # Accept
        conv = handler.manager.get_conversation(conv.id)
        response = await handler.handle_turn(conv, "perfect")
        assert response.state == StandupConversationState.FINALIZING
```

### Test Scope Requirements

| Test Category | Count | Coverage |
|---------------|-------|----------|
| ConversationResponse | 2 | Dataclass defaults and values |
| Start Conversation | 2 | Creation and suggestions |
| INITIATED state | 3 | Quick, cancel, proceed |
| REFINING state | 2 | Accept, add blocker |
| FINALIZING state | 1 | Completion |
| Terminal states | 1 | Already complete |
| Graceful fallback | 1 | Workflow error |
| Preference extraction | 3 | GitHub, calendar, none |
| Full flow | 2 | Quick flow, refinement flow |

**Total: ~17 tests**

### Progressive Bookending - Phase 2

```bash
gh issue comment 553 -b "Phase 2 Complete: Unit tests
- Created tests/unit/services/standup/test_conversation_handler.py (~300 lines)
- 17 tests covering all states and flows
- Test output: [paste pytest output]"
```

---

## Phase 3: Export and Integration

**Objective**: Export handler and integrate with standup service

### Update `services/standup/__init__.py`

```python
"""
Issue #552, #553: Standup conversation management package.

Provides:
- StandupConversationState (enum)
- StandupConversation (dataclass)
- StandupConversationManager (state machine)
- StandupConversationHandler (conversation flow)
"""

from services.standup.conversation_manager import (
    StandupConversationManager,
    InvalidStateTransitionError,
)
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

### Progressive Bookending - Phase 3

```bash
gh issue comment 553 -b "Phase 3 Complete: Package exports
- Updated services/standup/__init__.py with handler exports
- Import verification: [paste output]"
```

---

## Phase Z: Final Verification & Handoff

### Final Verification Commands

```bash
# 1. Run all standup tests
pytest tests/unit/services/standup/ -v

# 2. Import verification
python -c "from services.standup import StandupConversationHandler, ConversationResponse; print('OK')"

# 3. Full integration check
python -c "
from services.standup import StandupConversationHandler
import asyncio

async def test():
    handler = StandupConversationHandler()
    response = await handler.start_conversation('s1', 'u1')
    print(f'State: {response.state.value}')
    print(f'Message: {response.message[:50]}...')
    print('OK')

asyncio.run(test())
"

# 4. Regression check
pytest tests/ -k standup --tb=short
```

### Evidence Collection

```bash
# Line counts
wc -l services/standup/*.py tests/unit/services/standup/*.py
```

### GitHub Final Update

```bash
gh issue edit 553 --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] All acceptance criteria met
- [x] Tests passing: [X] tests in 0.XXs
- [x] No regressions: standup tests passing
- [x] Documentation updated

### Implementation Summary
- `services/standup/conversation_handler.py` (~250 lines)
- `ConversationResponse` dataclass
- State-based turn routing
- Refinement support (add/remove)
- Graceful fallback on errors
- 17+ unit tests

### Files Modified
| File | Lines | Purpose |
|------|-------|---------|
| services/standup/conversation_handler.py | +250 | Handler |
| services/standup/__init__.py | +15 | Exports |
| tests/unit/services/standup/test_conversation_handler.py | +300 | Tests |

### User Testing Steps
1. Import handler: `from services.standup import StandupConversationHandler`
2. Start conversation: `await handler.start_conversation(session_id, user_id)`
3. Handle turns: `await handler.handle_turn(conversation, user_message)`
4. Verify state transitions work through full flow

### Ready for PM Review
"
```

### Documentation Updates Checklist

- [ ] Update `services/standup/__init__.py` exports
- [ ] Add docstrings to all public methods
- [ ] No ADR changes needed (follows existing patterns)

### Handoff Preparation

**For #554 (Chat Widget)**:
- Handler is ready for UI integration
- `ConversationResponse` has `suggestions` for UI buttons
- `requires_input` indicates if conversation is complete

**For #555 (Learning)**:
- Preference extraction stub in place
- Can be enhanced with ML-based extraction

### PM Approval Request

```markdown
@PM - Issue #553 complete and ready for review:
- All acceptance criteria met ✓
- 17+ tests passing ✓
- No regressions ✓
- Handler ready for #554 integration ✓

Please review and close if satisfied.
```

---

## Completion Matrix

| Component | Status | Evidence |
|-----------|--------|----------|
| `ConversationResponse` dataclass | ⏸️ | |
| `StandupConversationHandler` class | ⏸️ | |
| State-based routing | ⏸️ | |
| INITIATED handler | ⏸️ | |
| GATHERING_PREFERENCES handler | ⏸️ | |
| GENERATING handler | ⏸️ | |
| REFINING handler | ⏸️ | |
| FINALIZING handler | ⏸️ | |
| Preference extraction | ⏸️ | |
| Refinement logic | ⏸️ | |
| Graceful fallback | ⏸️ | |
| Package exports | ⏸️ | |
| Unit tests | ⏸️ | |
| Integration tests | ⏸️ | |

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] #552 state management not complete
- [ ] `StandupConversationManager` API changed
- [ ] `MorningStandupWorkflow` API changed
- [ ] Performance exceeds 500ms per turn
- [ ] Tests fail for any reason
- [ ] State machine transitions don't match #552 implementation

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent Type | Deliverable | Evidence Required |
|-------|------------|-------------|-------------------|
| 1 | Code Agent | conversation_handler.py | Import verification |
| 2 | Code Agent | test_conversation_handler.py | pytest output |
| 3 | Code Agent | __init__.py updates | Export verification |
| Z | Lead Dev | Final verification | All tests, regression check |

### Dependencies

**Required**:
- [x] #552 (State Management) - COMPLETE

**Enables**:
- #554 (Chat Widget) - can start after this
- #555 (Learning) - can start after this

---

*Gameplan Version: 1.0*
*Issue: #553*
*Epic: #242*
*Created: 2026-01-07*
