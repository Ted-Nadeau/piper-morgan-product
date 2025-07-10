from typing import Any, Dict

from services.api.serializers import intent_to_dict
from services.domain.models import Intent
from services.intelligence.conversation_aware import \
    ConversationAwareClarifyingGenerator
from services.session.session_manager import SessionManager
from services.shared_types import IntentCategory


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

        # Handle clarification_needed action
        if intent.action == "clarification_needed":
            return await self._handle_clarification_needed(intent, session_id)

        # Handle other conversational actions
        responses = self.RESPONSES.get(intent.action, self.RESPONSES["chitchat"])
        response = random.choice(responses)

        return {
            "message": response,
            "intent": intent_to_dict(intent),
            "workflow_id": None,
        }

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
            questions_text = self.clarifying_generator.format_questions_for_user(
                analysis
            )

            # Store clarification state in session if available
            if self.session_manager and session_id:
                session = self.session_manager.get_or_create_session(session_id)
                session.set_pending_clarification(
                    original_intent=intent,
                    missing_info={
                        "detected_issues": [
                            issue.value for issue in analysis.detected_issues
                        ],
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
                    "detected_issues": [
                        issue.value for issue in analysis.detected_issues
                    ],
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
            questions_text = self.clarifying_generator.format_questions_for_user(
                analysis
            )

            # Update the pending clarification
            session.set_pending_clarification(
                original_intent=original_intent,
                missing_info={
                    "detected_issues": [
                        issue.value for issue in analysis.detected_issues
                    ],
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
                    "detected_issues": [
                        issue.value for issue in analysis.detected_issues
                    ],
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
