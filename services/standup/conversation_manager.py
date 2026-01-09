"""
Issue #552: Standup conversation state management service.

Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Provides state machine management for interactive standup conversations,
including state transitions, turn recording, and preference tracking.

Issue #556 Phase 4: Enhanced with structured performance logging.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

from services.domain.models import ConversationTurn, StandupConversation
from services.shared_types import StandupConversationState

logger = structlog.get_logger()


class InvalidStateTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""

    pass


class StandupConversationManager:
    """
    Issue #552: Manages standup conversation state and transitions.

    Provides:
    - Conversation lifecycle (create, get, complete)
    - State machine validation
    - Turn recording
    - Session-scoped persistence (in-memory initially)
    """

    # Issue #556: Memory optimization - limit turn history to prevent unbounded growth
    MAX_TURN_HISTORY = 50  # Typical standups complete in 5-10 turns

    # Valid state transitions - defines the state machine
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

    def __init__(self) -> None:
        """Initialize with in-memory session storage."""
        self._conversations: Dict[str, StandupConversation] = {}

    def create_conversation(
        self,
        session_id: str,
        user_id: str,
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> StandupConversation:
        """
        Create a new standup conversation.

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
        """
        Retrieve active conversation for a session.

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
        new_state: StandupConversationState,
    ) -> StandupConversation:
        """
        Transition conversation to a new state.

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
            # Issue #556 Phase 4: Log conversation completion metrics
            duration_seconds = (conversation.completed_at - conversation.created_at).total_seconds()
            logger.info(
                "standup_conversation_completed",
                conversation_id=conversation_id,
                total_turns=len(conversation.turns),
                duration_seconds=round(duration_seconds, 2),
                has_standup_content=conversation.current_standup is not None,
                versions_created=(
                    len(conversation.standup_versions) + 1 if conversation.current_standup else 0
                ),
            )
        elif new_state == StandupConversationState.ABANDONED:
            # Issue #556 Phase 4: Log abandoned conversation metrics
            duration_seconds = (datetime.now() - conversation.created_at).total_seconds()
            logger.info(
                "standup_conversation_abandoned",
                conversation_id=conversation_id,
                turns_before_abandon=len(conversation.turns),
                duration_seconds=round(duration_seconds, 2),
                last_state=current_state.value,
            )

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
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversationTurn:
        """
        Record a conversation turn.

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

        # Issue #556: Memory optimization - trim old turns if exceeding limit
        if len(conversation.turns) > self.MAX_TURN_HISTORY:
            # Keep only the most recent turns
            conversation.turns = conversation.turns[-self.MAX_TURN_HISTORY :]
            logger.debug(
                "standup_conversation_turns_trimmed",
                conversation_id=conversation_id,
                kept_turns=self.MAX_TURN_HISTORY,
            )

        logger.debug(
            "standup_conversation_turn_added",
            conversation_id=conversation_id,
            turn_number=turn.turn_number,
        )

        return turn

    def update_preferences(
        self,
        conversation_id: str,
        preferences: Dict[str, Any],
    ) -> StandupConversation:
        """
        Update conversation preferences.

        Args:
            conversation_id: Conversation to update
            preferences: Preference dict to merge

        Returns:
            Updated conversation

        Raises:
            KeyError: If conversation not found
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
        content: str,
    ) -> StandupConversation:
        """
        Set/update the current standup content.

        Keeps version history for refinement tracking.

        Args:
            conversation_id: Conversation to update
            content: New standup content

        Returns:
            Updated conversation

        Raises:
            KeyError: If conversation not found
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
        """
        Remove abandoned/expired conversations.

        Args:
            max_age_minutes: Maximum age in minutes before cleanup

        Returns:
            Count of removed conversations
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
