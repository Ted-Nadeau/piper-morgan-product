"""
Issue #490: Portfolio onboarding conversation handler.

Epic: FTUX (First Time User Experience)

Handles turn-by-turn conversation for portfolio onboarding,
following the pattern established by StandupConversationHandler (Epic #242).

Responsible for:
- Starting onboarding conversations
- Processing user responses
- Extracting project information from natural language
- Generating appropriate prompts
"""

import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

from services.onboarding.portfolio_manager import PortfolioOnboardingManager
from services.shared_types import PortfolioOnboardingState

logger = logging.getLogger(__name__)


@dataclass
class OnboardingResponse:
    """Response from the onboarding handler."""

    message: str
    state: PortfolioOnboardingState
    is_complete: bool = False
    captured_projects: Optional[list] = None
    metadata: Optional[Dict[str, Any]] = None


class PortfolioOnboardingHandler:
    """
    Issue #490: Handles portfolio onboarding conversation turns.

    Processes user messages, extracts project information, and generates
    appropriate responses based on conversation state.

    Follows StandupConversationHandler pattern from Epic #242.
    """

    # Patterns indicating user wants to decline
    DECLINE_PATTERNS = [
        r"\b(no|nope|not now|later|skip|cancel|never mind|nevermind)\b",
        r"\bno thanks\b",
        r"\bmaybe later\b",
        r"\bnot right now\b",
        r"\bi('m| am) (good|fine|ok|okay)\b",
    ]

    # Patterns indicating user is done adding projects
    DONE_PATTERNS = [
        r"\b(that'?s? (all|it)|done|finished|no more|nothing else)\b",
        r"\bjust (that one|the one|this one)\b",
        r"\bonly (that|this|one)\b",
        r"\bnope,? (that'?s? it|nothing else)\b",
    ]

    # Patterns indicating user wants to confirm
    CONFIRM_PATTERNS = [
        r"\b(yes|yeah|yep|sure|correct|right|looks good|perfect|great)\b",
        r"\bsave (it|them)\b",
        r"\bthat'?s? (correct|right)\b",
    ]

    def __init__(self, manager: PortfolioOnboardingManager):
        """
        Initialize the handler.

        Args:
            manager: PortfolioOnboardingManager for state management
        """
        self.manager = manager

    def start_onboarding(self, session_id: str, user_id: str) -> OnboardingResponse:
        """
        Start a new onboarding conversation.

        Args:
            session_id: Session identifier
            user_id: User identifier

        Returns:
            OnboardingResponse with initial prompt
        """
        session = self.manager.create_session(session_id, user_id)

        message = (
            "Hello! I'm Piper Morgan, your PM assistant. I notice we haven't "
            "set up your project portfolio yet. Would you like to tell me about "
            "the projects you're working on?"
        )

        # Record the turn (user message is implicit - greeting)
        self.manager.add_turn(
            session.id,
            user_message="[greeting]",
            assistant_response=message,
        )

        return OnboardingResponse(
            message=message,
            state=session.state,
            is_complete=False,
            metadata={"onboarding_id": session.id},
        )

    def handle_turn(
        self,
        onboarding_id: str,
        user_message: str,
    ) -> OnboardingResponse:
        """
        Process a user message and return appropriate response.

        Args:
            onboarding_id: Onboarding session ID
            user_message: User's input

        Returns:
            OnboardingResponse with next prompt or completion
        """
        session = self.manager.get_session(onboarding_id)
        if not session:
            logger.error(f"Onboarding session not found: {onboarding_id}")
            return OnboardingResponse(
                message="I'm sorry, I lost track of our conversation. Would you like to start over?",
                state=PortfolioOnboardingState.INITIATED,
                is_complete=False,
            )

        # Route based on current state
        if session.state == PortfolioOnboardingState.INITIATED:
            return self._handle_initiated(session, user_message)
        elif session.state == PortfolioOnboardingState.GATHERING_PROJECTS:
            return self._handle_gathering(session, user_message)
        elif session.state == PortfolioOnboardingState.CONFIRMING:
            return self._handle_confirming(session, user_message)
        else:
            # Terminal state - shouldn't receive turns
            return OnboardingResponse(
                message="This onboarding session has already ended.",
                state=session.state,
                is_complete=True,
            )

    def _handle_initiated(
        self,
        session,
        user_message: str,
    ) -> OnboardingResponse:
        """Handle response to initial onboarding offer."""
        message_lower = user_message.lower()

        # Check if user declined
        if self._matches_patterns(message_lower, self.DECLINE_PATTERNS):
            self.manager.transition_state(session.id, PortfolioOnboardingState.DECLINED)
            response_message = (
                "No problem! Whenever you're ready to tell me about your projects, "
                "just say 'set up my projects' and we can do this then. "
                "What can I help you with today?"
            )
            self.manager.add_turn(session.id, user_message, response_message)
            return OnboardingResponse(
                message=response_message,
                state=PortfolioOnboardingState.DECLINED,
                is_complete=True,
            )

        # User accepted - transition to gathering
        self.manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)
        response_message = "Great! What's the main project you're focused on right now?"
        self.manager.add_turn(session.id, user_message, response_message)

        return OnboardingResponse(
            message=response_message,
            state=PortfolioOnboardingState.GATHERING_PROJECTS,
            is_complete=False,
        )

    def _handle_gathering(
        self,
        session,
        user_message: str,
    ) -> OnboardingResponse:
        """Handle project info gathering."""
        message_lower = user_message.lower()

        # Check if user is done adding projects
        if self._matches_patterns(message_lower, self.DONE_PATTERNS):
            if not session.captured_projects:
                # No projects captured yet - prompt for at least one
                response_message = (
                    "I'd love to know about at least one project you're working on. "
                    "What are you building or working on right now?"
                )
                self.manager.add_turn(session.id, user_message, response_message)
                return OnboardingResponse(
                    message=response_message,
                    state=PortfolioOnboardingState.GATHERING_PROJECTS,
                    is_complete=False,
                )
            else:
                # Transition to confirming
                return self._transition_to_confirming(session, user_message)

        # Check for decline
        if self._matches_patterns(message_lower, self.DECLINE_PATTERNS):
            if session.captured_projects:
                # Have some projects - ask to confirm what we have
                return self._transition_to_confirming(session, user_message)
            else:
                # No projects - decline
                self.manager.transition_state(session.id, PortfolioOnboardingState.DECLINED)
                response_message = (
                    "No problem! Whenever you're ready, just let me know. "
                    "What can I help you with today?"
                )
                self.manager.add_turn(session.id, user_message, response_message)
                return OnboardingResponse(
                    message=response_message,
                    state=PortfolioOnboardingState.DECLINED,
                    is_complete=True,
                )

        # Extract project info from message
        project_info = self._extract_project_info(user_message)
        self.manager.add_project(session.id, project_info)

        # Ask if there are more projects
        project_name = project_info.get("name", "your project")
        response_message = (
            f"Got it - {project_name}. "
            f"Are there any other projects you'd like me to know about, "
            f"or is that your main focus?"
        )
        self.manager.add_turn(session.id, user_message, response_message)

        return OnboardingResponse(
            message=response_message,
            state=PortfolioOnboardingState.GATHERING_PROJECTS,
            is_complete=False,
        )

    def _handle_confirming(
        self,
        session,
        user_message: str,
    ) -> OnboardingResponse:
        """Handle confirmation of captured projects."""
        message_lower = user_message.lower()

        # Check for confirmation
        if self._matches_patterns(message_lower, self.CONFIRM_PATTERNS):
            self.manager.transition_state(session.id, PortfolioOnboardingState.COMPLETE)

            project_names = [p.get("name", "unnamed") for p in session.captured_projects]
            project_list = ", ".join(project_names)

            response_message = (
                f"All set! I've added {project_list} to your portfolio. "
                f"I'll help you stay on track with development coordination, "
                f"issue tracking, and planning. What would you like to focus on today?"
            )
            self.manager.add_turn(session.id, user_message, response_message)

            return OnboardingResponse(
                message=response_message,
                state=PortfolioOnboardingState.COMPLETE,
                is_complete=True,
                captured_projects=session.captured_projects,
            )

        # User wants to add more
        if "more" in message_lower or "another" in message_lower or "add" in message_lower:
            self.manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)
            response_message = "Sure! What other project would you like to add?"
            self.manager.add_turn(session.id, user_message, response_message)

            return OnboardingResponse(
                message=response_message,
                state=PortfolioOnboardingState.GATHERING_PROJECTS,
                is_complete=False,
            )

        # Check for decline/cancel
        if self._matches_patterns(message_lower, self.DECLINE_PATTERNS):
            self.manager.transition_state(session.id, PortfolioOnboardingState.DECLINED)
            response_message = (
                "No problem, I won't save those projects. "
                "Let me know if you'd like to set up your portfolio later. "
                "What can I help you with today?"
            )
            self.manager.add_turn(session.id, user_message, response_message)

            return OnboardingResponse(
                message=response_message,
                state=PortfolioOnboardingState.DECLINED,
                is_complete=True,
            )

        # Unclear response - re-prompt
        project_names = [p.get("name", "unnamed") for p in session.captured_projects]
        project_list = ", ".join(project_names)
        response_message = (
            f"I have {project_list} noted. "
            f"Should I save these to your portfolio? "
            f"Just say 'yes' to confirm or 'add more' if you have other projects."
        )
        self.manager.add_turn(session.id, user_message, response_message)

        return OnboardingResponse(
            message=response_message,
            state=PortfolioOnboardingState.CONFIRMING,
            is_complete=False,
        )

    def _transition_to_confirming(self, session, user_message: str) -> OnboardingResponse:
        """Transition to confirming state and generate confirmation prompt."""
        self.manager.transition_state(session.id, PortfolioOnboardingState.CONFIRMING)

        project_names = [p.get("name", "unnamed") for p in session.captured_projects]
        if len(project_names) == 1:
            project_summary = project_names[0]
        else:
            project_summary = ", ".join(project_names[:-1]) + f" and {project_names[-1]}"

        response_message = (
            f"Perfect. I have {project_summary} noted. "
            f"Should I save {'this' if len(project_names) == 1 else 'these'} "
            f"to your portfolio?"
        )
        self.manager.add_turn(session.id, user_message, response_message)

        return OnboardingResponse(
            message=response_message,
            state=PortfolioOnboardingState.CONFIRMING,
            is_complete=False,
        )

    def _extract_project_info(self, message: str) -> Dict[str, Any]:
        """
        Extract project name and description from user message.

        Simple extraction for MVP - looks for patterns like:
        - "called X"
        - "named X"
        - "X project"
        - Just uses the whole message as name if no pattern found

        Args:
            message: User's message describing their project

        Returns:
            Dict with 'name' and optionally 'description'
        """
        message = message.strip()

        # Try to extract name with "called" or "named"
        called_match = re.search(
            r"(?:called|named)\s+['\"]?([^'\",.]+)['\"]?", message, re.IGNORECASE
        )
        if called_match:
            name = called_match.group(1).strip()
            description = message
            return {"name": name, "description": description}

        # Try to extract "X project" pattern
        project_match = re.search(
            r"(?:a|an|my|the)\s+([^,.\n]+?)\s+(?:project|app|application|system|platform)",
            message,
            re.IGNORECASE,
        )
        if project_match:
            name = project_match.group(1).strip()
            description = message
            return {"name": name, "description": description}

        # Try to extract from "I'm building/working on X"
        building_match = re.search(
            r"(?:building|working on|developing|creating)\s+(?:a|an|the)?\s*([^,.\n]+?)(?:\.|,|$)",
            message,
            re.IGNORECASE,
        )
        if building_match:
            name = building_match.group(1).strip()
            # Clean up trailing words
            name = re.sub(
                r"\s+(?:right now|currently|at the moment)$", "", name, flags=re.IGNORECASE
            )
            description = message
            return {"name": name, "description": description}

        # Fallback - use first sentence or whole message as name
        first_sentence = message.split(".")[0].strip()
        if len(first_sentence) > 50:
            # Too long - just use first few words
            words = first_sentence.split()[:5]
            name = " ".join(words)
        else:
            name = first_sentence

        return {"name": name, "description": message}

    def _matches_patterns(self, text: str, patterns: list) -> bool:
        """Check if text matches any of the given regex patterns."""
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
