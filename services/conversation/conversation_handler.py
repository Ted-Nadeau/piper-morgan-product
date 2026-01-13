from typing import Any, Dict, Optional

import structlog

from services.api.serializers import intent_to_dict
from services.domain.models import Intent
from services.intelligence.conversation_aware import ConversationAwareClarifyingGenerator
from services.session.session_manager import SessionManager
from services.shared_types import IntentCategory, PortfolioOnboardingState

logger = structlog.get_logger()


# Issue #490: Global onboarding manager and handler instances
# These are module-level singletons to persist onboarding state across requests
_onboarding_manager = None
_onboarding_handler = None


def _get_onboarding_components():
    """Lazy-load onboarding components to avoid circular imports."""
    global _onboarding_manager, _onboarding_handler
    if _onboarding_manager is None:
        from services.onboarding import PortfolioOnboardingHandler, PortfolioOnboardingManager

        _onboarding_manager = PortfolioOnboardingManager()
        _onboarding_handler = PortfolioOnboardingHandler(_onboarding_manager)
        # Issue #490 INVESTIGATION: First creation
        print(f"[ConversationHandler] Singleton CREATED: manager id={id(_onboarding_manager)}")
    return _onboarding_manager, _onboarding_handler


# Issue #585: Global standup conversation components (mirrors portfolio pattern)
# These are module-level singletons to persist standup conversation state across requests
_standup_manager = None
_standup_handler = None


def _get_standup_components():
    """Lazy-load standup conversation components to avoid circular imports."""
    global _standup_manager, _standup_handler
    if _standup_manager is None:
        from services.standup.conversation_handler import StandupConversationHandler
        from services.standup.conversation_manager import StandupConversationManager

        _standup_manager = StandupConversationManager()
        _standup_handler = StandupConversationHandler(conversation_manager=_standup_manager)
        # Issue #585 INVESTIGATION: First creation
        print(f"[ConversationHandler] Standup singleton CREATED: manager id={id(_standup_manager)}")
    return _standup_manager, _standup_handler


class ConversationHandler:
    """Handles conversational intents like greetings and chitchat"""

    RESPONSES = {
        "greeting": [
            "Hello! I'm ready to help with your PM tasks. What would you like to work on today?",
            "Hi there! How can I assist with your product management needs?",
            "Good to see you! What PM challenge can I help you tackle?",
        ],
        "farewell": [
            "Goodbye! Feel free to return if you need PM assistance.",
            "See you later! Happy product managing!",
            "Take care! I'll be here when you need help with your PM tasks.",
        ],
        "thanks": [
            "You're welcome! Is there anything else I can help with?",
            "Happy to help! Let me know if you need anything else.",
            "My pleasure! Feel free to ask if you have more PM questions.",
        ],
        "chitchat": [
            "I'm doing well, thanks! Ready to help with any PM tasks you have.",
            "I'm here and ready to assist! What PM work can I help with?",
            "All systems operational! What would you like to work on?",
        ],
    }

    def __init__(self, session_manager: SessionManager = None):
        self.clarifying_generator = ConversationAwareClarifyingGenerator()
        self.session_manager = session_manager

    async def respond(self, intent: Intent, session_id: str = None) -> Dict[str, Any]:
        """Generate appropriate conversational response"""
        import random

        # Issue #490: Check for active onboarding session first
        user_id = intent.context.get("user_id") if intent.context else None
        if user_id and session_id:
            onboarding_response = await self._handle_active_onboarding(user_id, session_id, intent)
            if onboarding_response:
                return onboarding_response

        # Handle clarification_needed action
        if intent.action == "clarification_needed":
            return await self._handle_clarification_needed(intent, session_id)

        # Issue #102: Enhanced greeting with calendar awareness
        if intent.action == "greeting":
            return await self._respond_to_greeting(intent, session_id)

        # Handle other conversational actions
        responses = self.RESPONSES.get(intent.action, self.RESPONSES["chitchat"])
        response = random.choice(responses)

        return {
            "message": response,
            "intent": intent_to_dict(intent),
            "workflow_id": None,
        }

    async def _get_calendar_summary(self) -> Optional[Dict[str, Any]]:
        """Issue #102: Get calendar summary for greeting enhancement."""
        try:
            from services.integrations.calendar.calendar_integration_router import (
                CalendarIntegrationRouter,
            )

            calendar_router = CalendarIntegrationRouter()
            summary = await calendar_router.get_temporal_summary()
            return summary
        except Exception as e:
            logger.warning(f"Could not fetch calendar for greeting: {e}")
            return None

    async def _respond_to_greeting(self, intent: Intent, session_id: str = None) -> Dict[str, Any]:
        """
        Issue #102: Generate calendar-aware greeting response.
        Issue #490: Check for portfolio onboarding trigger.
        """
        import random

        # Issue #490: Check if this user should be offered portfolio onboarding
        user_id = intent.context.get("user_id") if intent.context else None

        # DEBUG Issue #490: Trace greeting flow
        logger.info(
            "greeting_onboarding_trace",
            user_id=user_id,
            session_id=session_id,
            has_context=intent.context is not None,
            context_keys=list(intent.context.keys()) if intent.context else [],
        )

        if user_id and session_id:
            onboarding_response = await self._check_portfolio_onboarding(user_id, session_id)
            if onboarding_response:
                return onboarding_response

        # Get calendar summary (may be None if unavailable)
        calendar_summary = await self._get_calendar_summary()

        if calendar_summary and not calendar_summary.get("error"):
            # Build enhanced greeting with calendar insights
            response = self._format_calendar_greeting(calendar_summary)
        else:
            # Fallback to standard greeting
            response = random.choice(self.RESPONSES["greeting"])

        return {
            "message": response,
            "intent": intent_to_dict(intent),
            "workflow_id": None,
        }

    async def _check_portfolio_onboarding(
        self, user_id: str, session_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Issue #490: Check if user should be offered portfolio onboarding.

        Returns an onboarding response if the user has no projects,
        otherwise returns None to continue with normal greeting.
        """
        try:
            from services.database.repositories import ProjectRepository
            from services.database.session_factory import AsyncSessionFactory
            from services.onboarding import FirstMeetingDetector

            async with AsyncSessionFactory.session_scope() as db_session:
                project_repo = ProjectRepository(db_session)
                detector = FirstMeetingDetector(project_repo)

                if await detector.should_trigger(user_id):
                    # Start onboarding flow
                    _, onboarding_handler = _get_onboarding_components()
                    response = onboarding_handler.start_onboarding(session_id, user_id)

                    logger.info(
                        "portfolio_onboarding_triggered",
                        user_id=user_id,
                        session_id=session_id,
                        onboarding_id=response.metadata.get("onboarding_id"),
                    )

                    return {
                        "message": response.message,
                        "intent": {
                            "category": IntentCategory.GUIDANCE.value,
                            "action": "portfolio_onboarding",
                            "confidence": 1.0,
                            "context": {
                                "onboarding_id": response.metadata.get("onboarding_id"),
                                "state": response.state.value,
                            },
                        },
                        "workflow_id": None,
                        "onboarding_session": response.metadata.get("onboarding_id"),
                    }

        except Exception as e:
            logger.warning(f"Could not check portfolio onboarding: {e}")

        return None

    async def _handle_active_onboarding(
        self, user_id: str, session_id: str, intent: Intent
    ) -> Optional[Dict[str, Any]]:
        """
        Issue #490: Handle messages when user has an active onboarding session.

        Routes user messages to the portfolio onboarding handler if an active
        session exists for this user.
        """
        try:
            onboarding_manager, onboarding_handler = _get_onboarding_components()

            # Check if user has an active onboarding session
            session = onboarding_manager.get_session_by_user(user_id)
            if not session:
                return None

            # Check if session is in a terminal state
            if session.state in (
                PortfolioOnboardingState.COMPLETE,
                PortfolioOnboardingState.DECLINED,
            ):
                return None

            # Route the message to the onboarding handler
            user_message = intent.context.get("original_message", "") if intent.context else ""
            if not user_message:
                return None

            response = onboarding_handler.handle_turn(session.id, user_message)

            # If onboarding completed, persist the projects
            if response.is_complete and response.state == PortfolioOnboardingState.COMPLETE:
                await self._persist_onboarding_projects(user_id, response.captured_projects)

            logger.info(
                "portfolio_onboarding_turn_handled",
                user_id=user_id,
                session_id=session_id,
                onboarding_id=session.id,
                state=response.state.value,
                is_complete=response.is_complete,
            )

            return {
                "message": response.message,
                "intent": {
                    "category": IntentCategory.GUIDANCE.value,
                    "action": "portfolio_onboarding",
                    "confidence": 1.0,
                    "context": {
                        "onboarding_id": session.id,
                        "state": response.state.value,
                    },
                },
                "workflow_id": None,
                "onboarding_session": session.id if not response.is_complete else None,
            }

        except Exception as e:
            logger.warning(f"Could not handle active onboarding: {e}")

        return None

    async def _persist_onboarding_projects(self, user_id: str, captured_projects: list) -> None:
        """
        Issue #490: Persist projects captured during onboarding.

        Creates Project entities in the database for each project the user
        described during the onboarding conversation, then marks the user's
        setup as complete.
        """
        if not captured_projects:
            return

        try:
            from datetime import datetime

            from sqlalchemy import text

            from services.database.repositories import ProjectRepository
            from services.database.session_factory import AsyncSessionFactory
            from services.domain import models as domain

            async with AsyncSessionFactory.session_scope() as db_session:
                project_repo = ProjectRepository(db_session)

                for project_data in captured_projects:
                    project = domain.Project(
                        id=None,  # Will be generated
                        owner_id=user_id,
                        name=project_data.get("name", "Untitled Project"),
                        description=project_data.get("description", ""),
                        is_default=False,
                        is_archived=False,
                    )

                    # Use BaseRepository.create via ProjectRepository
                    await project_repo.create(
                        owner_id=user_id,
                        name=project.name,
                        description=project.description,
                        is_default=False,
                        is_archived=False,
                    )

                # Mark user's setup as complete (Issue #490)
                await db_session.execute(
                    text(
                        "UPDATE users SET setup_complete = true, "
                        "setup_completed_at = :now WHERE id = :user_id"
                    ),
                    {"now": datetime.now(), "user_id": user_id},
                )

                await db_session.commit()

                logger.info(
                    "portfolio_onboarding_projects_persisted",
                    user_id=user_id,
                    project_count=len(captured_projects),
                    setup_complete=True,
                )

        except Exception as e:
            logger.error(f"Failed to persist onboarding projects: {e}")

    def _format_calendar_greeting(self, summary: Dict[str, Any]) -> str:
        """Issue #102: Format greeting with calendar insights."""
        from datetime import datetime

        now = datetime.now()
        time_greeting = self._get_time_of_day_greeting(now.hour)

        lines = [f"{time_greeting}! Here's your day at a glance:\n"]

        # Current/next meeting
        if summary.get("current_meeting"):
            meeting = summary["current_meeting"]
            lines.append(f"📍 **Now**: {meeting.get('summary', 'Meeting in progress')}")
        elif summary.get("next_meeting"):
            meeting = summary["next_meeting"]
            # Parse start_time to get readable format
            start_time = meeting.get("start_time", "soon")
            if "T" in str(start_time):
                try:
                    dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                    start_time = dt.strftime("%I:%M %p").lstrip("0")
                except (ValueError, AttributeError):
                    pass
            lines.append(f"📅 **Next**: {meeting.get('summary', 'Meeting')} at {start_time}")

        # Free time blocks
        if summary.get("free_blocks"):
            blocks = summary["free_blocks"][:2]  # Show up to 2 free blocks
            if blocks:
                block_texts = []
                for b in blocks:
                    start = b.get("start_time", "")
                    end = b.get("end_time", "")
                    # Format times
                    try:
                        if "T" in str(start):
                            start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                            start = start_dt.strftime("%I:%M").lstrip("0")
                        if "T" in str(end):
                            end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
                            end = end_dt.strftime("%I:%M").lstrip("0")
                    except (ValueError, AttributeError):
                        pass
                    block_texts.append(f"{start}-{end}")
                lines.append(f"⏰ **Free time**: {', '.join(block_texts)}")

        # Today's meeting count from stats
        stats = summary.get("stats", {})
        total_meetings = stats.get("total_meetings_today", 0)
        if total_meetings > 0:
            lines.append(f"\n📋 {total_meetings} meeting{'s' if total_meetings != 1 else ''} today")
        else:
            lines.append("\n✨ Clear calendar today!")

        lines.append("\nWhat would you like to focus on?")

        return "\n".join(lines)

    def _get_time_of_day_greeting(self, hour: int) -> str:
        """Issue #102: Return appropriate time-of-day greeting."""
        if hour < 12:
            return "Good morning"
        elif hour < 17:
            return "Good afternoon"
        else:
            return "Good evening"

    async def _handle_clarification_needed(
        self, intent: Intent, session_id: str = None
    ) -> Dict[str, Any]:
        """Handle vague/unclear requests by generating clarifying questions"""
        original_message = intent.context.get("original_message", "")
        trigger = intent.context.get("trigger", "unknown")

        # Use conversation-aware clarifying generator
        analysis = await self.clarifying_generator.analyze_request(
            description=original_message, conversation_id=session_id
        )

        if analysis.questions:
            # Format questions for user
            questions_text = self.clarifying_generator.format_questions_for_user(analysis)

            # Store clarification state in session if available
            if self.session_manager and session_id:
                session = self.session_manager.get_or_create_session(session_id)
                session.set_pending_clarification(
                    original_intent=intent,
                    missing_info={
                        "detected_issues": [issue.value for issue in analysis.detected_issues],
                        "questions": [
                            {
                                "question": q.question,
                                "type": q.type.value,
                                "priority": q.priority,
                                "example_answer": q.example_answer,
                            }
                            for q in analysis.questions
                        ],
                    },
                    clarification_prompt=questions_text,
                )

            return {
                "message": questions_text,
                "intent": intent_to_dict(intent),
                "workflow_id": None,
                "clarification_data": {
                    "is_ambiguous": analysis.is_ambiguous,
                    "detected_issues": [issue.value for issue in analysis.detected_issues],
                    "questions": [
                        {
                            "question": q.question,
                            "type": q.type.value,
                            "priority": q.priority,
                            "example_answer": q.example_answer,
                        }
                        for q in analysis.questions
                    ],
                    "can_proceed": analysis.can_proceed,
                    "trigger": trigger,
                },
            }
        else:
            # Fallback if no questions generated
            return {
                "message": "I need a bit more information to help you effectively. Could you provide more details about what you'd like me to do?",
                "intent": intent_to_dict(intent),
                "workflow_id": None,
            }

    async def handle_clarification_response(
        self, user_response: str, session_id: str
    ) -> Dict[str, Any]:
        """Handle user's response to clarification questions"""
        if not self.session_manager or not session_id:
            return {
                "message": "I'm sorry, but I lost track of our conversation. Could you please start over?",
                "intent": {
                    "category": "CONVERSATION",
                    "action": "clarification_needed",
                    "confidence": 0.5,
                },
                "workflow_id": None,
            }

        session = self.session_manager.get_or_create_session(session_id)
        pending_clarification = session.get_pending_clarification()

        if not pending_clarification:
            return {
                "message": "I don't have any pending clarification questions. How can I help you?",
                "intent": {
                    "category": "CONVERSATION",
                    "action": "chitchat",
                    "confidence": 0.8,
                },
                "workflow_id": None,
            }

        # Get the original intent and missing info
        original_intent = pending_clarification["original_intent"]
        missing_info = pending_clarification["missing_info"]

        # Combine original message with clarification response
        original_message = original_intent.context.get("original_message", "")
        combined_message = f"{original_message} {user_response}".strip()

        # Re-analyze with the combined context
        analysis = await self.clarifying_generator.analyze_request(
            description=combined_message, conversation_id=session_id
        )

        if analysis.can_proceed:
            # We have enough information now
            session.clear_pending_clarification()

            # Create a new intent with the clarified information
            clarified_intent = Intent(
                category=original_intent.category,
                action=original_intent.action,
                confidence=0.8,  # Higher confidence with clarification
                context={
                    "original_message": original_message,
                    "clarification_response": user_response,
                    "combined_message": combined_message,
                    "clarification_resolved": True,
                },
            )

            return {
                "message": f"Perfect! Now I understand. Let me help you with that.",
                "intent": intent_to_dict(clarified_intent),
                "workflow_id": None,
                "clarification_resolved": True,
                "original_intent": intent_to_dict(original_intent),
            }
        else:
            # Still need more clarification
            questions_text = self.clarifying_generator.format_questions_for_user(analysis)

            # Update the pending clarification
            session.set_pending_clarification(
                original_intent=original_intent,
                missing_info={
                    "detected_issues": [issue.value for issue in analysis.detected_issues],
                    "questions": [
                        {
                            "question": q.question,
                            "type": q.type.value,
                            "priority": q.priority,
                            "example_answer": q.example_answer,
                        }
                        for q in analysis.questions
                    ],
                },
                clarification_prompt=questions_text,
            )

            return {
                "message": questions_text,
                "intent": {
                    "category": "CONVERSATION",
                    "action": "clarification_needed",
                    "confidence": 0.6,
                },
                "workflow_id": None,
                "clarification_data": {
                    "is_ambiguous": analysis.is_ambiguous,
                    "detected_issues": [issue.value for issue in analysis.detected_issues],
                    "questions": [
                        {
                            "question": q.question,
                            "type": q.type.value,
                            "priority": q.priority,
                            "example_answer": q.example_answer,
                        }
                        for q in analysis.questions
                    ],
                    "can_proceed": analysis.can_proceed,
                },
            }
