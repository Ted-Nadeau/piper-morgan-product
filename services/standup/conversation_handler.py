"""
Issue #553: Standup conversation flow handler.

Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Handles multi-turn standup conversations by:
- Routing based on conversation state
- Generating context-aware follow-up questions
- Processing refinement requests
- Managing graceful fallback
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

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
    suggestions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class StandupConversationHandler:
    """
    Issue #553: Multi-turn conversation flow for standup generation.

    State Machine Flow:
    INITIATED -> GATHERING_PREFERENCES -> GENERATING -> REFINING -> FINALIZING -> COMPLETE
                                       |            ^
                                       +------------+ (skip preferences)

    Any state can transition to ABANDONED on timeout/cancel.
    """

    def __init__(
        self,
        conversation_manager: Optional[StandupConversationManager] = None,
        standup_workflow: Optional[Any] = None,
    ) -> None:
        """
        Initialize handler.

        Args:
            conversation_manager: State manager instance (creates new if None)
            standup_workflow: MorningStandupWorkflow instance for generation
        """
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

        Args:
            conversation: Current conversation
            user_message: User's message
            context: Optional additional context

        Returns:
            ConversationResponse with message and state
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

        Args:
            session_id: Session identifier
            user_id: User identifier
            initial_context: Optional context from integrations

        Returns:
            ConversationResponse with greeting and suggestions
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
            self.manager.transition_state(conversation.id, StandupConversationState.GENERATING)
            return await self._generate_standup(conversation, context)

        # Check for cancel
        if any(word in message_lower for word in ["no", "not now", "cancel", "later", "nope"]):
            self.manager.transition_state(conversation.id, StandupConversationState.ABANDONED)
            return ConversationResponse(
                message="No problem! Just say 'standup' when you're ready.",
                state=StandupConversationState.ABANDONED,
                requires_input=False,
            )

        # Normal flow - go straight to generating (skip preferences for MVP)
        self.manager.transition_state(conversation.id, StandupConversationState.GENERATING)
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
        self.manager.transition_state(conversation.id, StandupConversationState.GENERATING)
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
            self.manager.transition_state(conversation.id, StandupConversationState.REFINING)
            return ConversationResponse(
                message=(
                    f"Here's your standup:\n\n{conversation.current_standup}\n\n"
                    "Would you like to make any changes?"
                ),
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
        acceptance_words = [
            "good",
            "done",
            "looks good",
            "perfect",
            "yes",
            "ok",
            "fine",
            "great",
            "thanks",
        ]
        if any(word in message_lower for word in acceptance_words):
            self.manager.transition_state(conversation.id, StandupConversationState.FINALIZING)
            return ConversationResponse(
                message=(
                    f"Great! Here's your final standup:\n\n{conversation.current_standup}\n\n"
                    "Would you like to share this or save your preferences for next time?"
                ),
                state=StandupConversationState.FINALIZING,
                standup_content=conversation.current_standup,
                suggestions=["Just copy it", "Save preferences", "Share with team"],
            )

        # Check for start over
        if "start over" in message_lower or "restart" in message_lower:
            self.manager.transition_state(conversation.id, StandupConversationState.GENERATING)
            return await self._generate_standup(conversation, context)

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
        self.manager.transition_state(conversation.id, StandupConversationState.COMPLETE)
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
                standup_content = result.summary if hasattr(result, "summary") else str(result)
            else:
                # Fallback to basic generation
                standup_content = self._generate_basic_standup(context)

            self.manager.set_standup_content(conversation.id, standup_content)
            self.manager.transition_state(conversation.id, StandupConversationState.REFINING)

            return ConversationResponse(
                message=(
                    f"Here's your standup:\n\n{standup_content}\n\n"
                    "Would you like to make any changes?"
                ),
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
        preferences: Dict[str, Any] = {}
        message_lower = message.lower()

        if "github" in message_lower:
            preferences["focus"] = "github"
        elif "calendar" in message_lower:
            preferences["focus"] = "calendar"
        elif "todos" in message_lower or "tasks" in message_lower:
            preferences["focus"] = "todos"

        if "brief" in message_lower or "short" in message_lower:
            preferences["length"] = "brief"
        elif "detailed" in message_lower or "comprehensive" in message_lower:
            preferences["length"] = "detailed"

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
            # Extract blocker text - remove the "add blocker" prefix
            blocker_text = user_message
            for prefix in ["add blocker", "add a blocker", "add blocker:"]:
                if prefix in message_lower:
                    start_idx = message_lower.find(prefix) + len(prefix)
                    blocker_text = user_message[start_idx:].strip()
                    break

            if blocker_text:
                if "*Blockers:*" in current:
                    # Find the Blockers section and add to it
                    refined = current.replace("*Blockers:*\n", f"*Blockers:*\n* {blocker_text}\n")
                else:
                    # Add a Blockers section
                    refined = current + f"\n\n*Blockers:*\n* {blocker_text}"
                self.manager.set_standup_content(conversation.id, refined)
                return refined

        # Handle remove request
        if "remove" in message_lower:
            # Extract what to remove
            remove_target = user_message
            for prefix in ["remove", "remove the", "delete"]:
                if prefix in message_lower:
                    start_idx = message_lower.find(prefix) + len(prefix)
                    remove_target = user_message[start_idx:].strip().lower()
                    break

            # Try to remove matching lines
            lines = current.split("\n")
            filtered_lines = [line for line in lines if remove_target not in line.lower()]
            refined = "\n".join(filtered_lines)
            self.manager.set_standup_content(conversation.id, refined)
            return refined

        # Handle focus request
        if "focus on" in message_lower:
            focus_target = message_lower.split("focus on")[-1].strip()
            preferences = {"focus": focus_target}
            self.manager.update_preferences(conversation.id, preferences)
            # For now, just note the preference - would regenerate with focus
            return current

        # Default - return current content unchanged
        return current

    def _generate_basic_standup(self, context: Dict[str, Any]) -> str:
        """Generate basic standup when workflow unavailable."""
        return """*Yesterday:*
* Made progress on assigned tasks

*Today:*
* Continue current work items
* Review any blockers

*Blockers:*
* None at this time"""

    def _graceful_fallback(
        self,
        conversation: StandupConversation,
        error: str,
    ) -> ConversationResponse:
        """Handle graceful fallback when generation fails."""
        basic = self._generate_basic_standup({})
        self.manager.set_standup_content(conversation.id, basic)
        self.manager.transition_state(conversation.id, StandupConversationState.REFINING)

        return ConversationResponse(
            message=(
                f"Here's a basic standup template:\n\n{basic}\n\n"
                "You can customize it to fit your day."
            ),
            state=StandupConversationState.REFINING,
            standup_content=basic,
            suggestions=["Looks good", "Let me customize", "Try again"],
            metadata={"fallback": True, "error": error},
        )
