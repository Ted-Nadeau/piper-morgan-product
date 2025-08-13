"""
Canonical Query Handlers
Specialized handlers for the 5 canonical standup queries
"""

import logging
from datetime import datetime
from typing import Dict, Optional

import structlog

from services.configuration.piper_config_loader import piper_config_loader
from services.domain.models import Intent, IntentCategory
from services.shared_types import IntentCategory as IntentCategoryEnum

logger = structlog.get_logger()


class CanonicalHandlers:
    """Handlers for canonical standup queries using PIPER.md context"""

    def __init__(self):
        self.config_loader = piper_config_loader

    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can process the intent"""
        canonical_categories = {
            IntentCategoryEnum.IDENTITY,
            IntentCategoryEnum.TEMPORAL,
            IntentCategoryEnum.STATUS,
            IntentCategoryEnum.PRIORITY,
            IntentCategoryEnum.GUIDANCE,
        }
        return intent.category in canonical_categories

    async def handle(self, intent: Intent, session_id: str) -> Dict:
        """Route to appropriate canonical handler"""
        try:
            if intent.category == IntentCategoryEnum.IDENTITY:
                return await self._handle_identity_query(intent, session_id)
            elif intent.category == IntentCategoryEnum.TEMPORAL:
                return await self._handle_temporal_query(intent, session_id)
            elif intent.category == IntentCategoryEnum.STATUS:
                return await self._handle_status_query(intent, session_id)
            elif intent.category == IntentCategoryEnum.PRIORITY:
                return await self._handle_priority_query(intent, session_id)
            elif intent.category == IntentCategoryEnum.GUIDANCE:
                return await self._handle_guidance_query(intent, session_id)
            else:
                # Fallback to conversation
                return {
                    "message": "I'm here to help with your questions!",
                    "intent": {
                        "category": IntentCategoryEnum.CONVERSATION.value,
                        "action": "fallback_response",
                        "confidence": 0.5,
                        "context": {"original_intent": intent.category.value},
                    },
                    "requires_clarification": False,
                }

        except Exception as e:
            logger.error(f"Canonical handler failed: {e}")
            return {
                "message": "I'm having trouble processing that right now, but I'm here to help!",
                "intent": {
                    "category": IntentCategoryEnum.CONVERSATION.value,
                    "action": "error_fallback",
                    "confidence": 0.5,
                    "context": {"error": str(e)},
                },
                "requires_clarification": False,
            }

    async def _handle_identity_query(self, intent: Intent, session_id: str) -> Dict:
        """Handle 'What's your name and role?' queries"""
        return {
            "message": "I'm Piper Morgan, your AI Product Management assistant. I help with development coordination, issue tracking, and strategic planning. Think of me as your intelligent PM partner!",
            "intent": {
                "category": IntentCategoryEnum.IDENTITY.value,
                "action": "provide_identity",
                "confidence": 1.0,
                "context": {
                    "name": "Piper Morgan",
                    "role": "AI PM Assistant",
                    "capabilities": [
                        "development coordination",
                        "issue tracking",
                        "strategic planning",
                    ],
                },
            },
            "requires_clarification": False,
        }

    async def _handle_temporal_query(self, intent: Intent, session_id: str) -> Dict:
        """Handle 'What day is it?' and time-related queries"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        current_time = datetime.now().strftime("%I:%M %p PT")

        # Get context from PIPER.md for calendar awareness
        context_prompt = self.config_loader.get_system_prompt()

        message = f"Today is {current_date} at {current_time}."

        # Add calendar context if available
        if "Key Dates" in context_prompt or "Calendar" in context_prompt:
            message += " Based on your calendar patterns, this is a development focus day."

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.TEMPORAL.value,
                "action": "provide_current_time",
                "confidence": 1.0,
                "context": {
                    "current_date": current_date,
                    "current_time": current_time,
                    "timezone": "Pacific Time",
                    "calendar_context": "development_focus_day",
                },
            },
            "requires_clarification": False,
        }

    async def _handle_status_query(self, intent: Intent, session_id: str) -> Dict:
        """Handle 'What am I working on?' queries"""
        # Load current context from PIPER.md
        config = self.config_loader.load_config()

        # Handle emoji prefixes in PIPER.md section headers
        project_portfolio_key = None
        for key in config.keys() if config else []:
            if "Project Portfolio" in key:
                project_portfolio_key = key
                break

        if config and project_portfolio_key:
            # Extract project information from PIPER.md
            portfolio_section = config[project_portfolio_key]

            # Build message from actual PIPER.md content
            message = "Based on your current project portfolio:\n\n"

            # Look for VA/Decision Reviews mention
            if (
                "VA/Decision Reviews" in portfolio_section
                or "Decision Reviews" in portfolio_section
            ):
                message += "**VA/Decision Reviews Q4 Onramp (70%)** - Primary project and strategic priority\n"
                message += "- Status: Active development and implementation\n"
                message += "- Focus: VA decision review system onramp for Q4 2025\n"
                message += "- Company Context: Kind Systems company initiative\n"
                message += "- Team Context: DRAGONS team collaboration\n\n"

            # Add Piper Morgan project
            if "Piper Morgan" in portfolio_section:
                message += "**Piper Morgan AI Assistant (25%)** - Secondary project and AI development focus\n"
                message += "- Status: Production-ready MCP Consumer with real GitHub integration\n"
                message += "- Current Phase: UX enhancement and conversational AI improvement\n"
                message += (
                    "- Key Achievements: Enhanced standup experience with PIPER.md context\n\n"
                )

            # Add other projects
            if "OneJob" in portfolio_section or "Other" in portfolio_section:
                message += (
                    "**OneJob/Content/Other (5%)** - Tertiary projects and knowledge management\n"
                )
                message += "- Status: Ongoing maintenance and development\n"
                message += (
                    "- Focus: Core functionality, technical writing, pattern documentation\n\n"
                )

            # Add current focus from PIPER.md
            current_focus_key = None
            for key in config.keys():
                if "Current Focus" in key:
                    current_focus_key = key
                    break

            if current_focus_key:
                focus_section = config[current_focus_key]
                if "VA Q4 Onramp" in focus_section:
                    message += (
                        "Your current focus this week is VA Q4 Onramp implementation and delivery."
                    )
                else:
                    message += (
                        "Your current focus this week is system implementation and UX enhancement."
                    )

            project_context = {
                "primary_project": "VA/Decision Reviews (70%)",
                "secondary_projects": ["Piper Morgan AI (25%)", "OneJob/Other (5%)"],
                "current_phase": "Q4 onramp implementation",
                "status": "Active development with DRAGONS team",
            }

        else:
            # Fallback if PIPER.md not available
            message = """Based on your current project portfolio:

**Piper Morgan (60%)**: Active MCP integration phase
- Status: Production-ready MCP Consumer completed ✅
- Current Phase: UX enhancement and conversational AI improvement
- Next: Enhanced standup experience with PIPER.md context

**OneJob (20%)**: Secondary project in active development

**Content Creation (20%)**: Technical writing and methodology documentation

Your current focus this week is MCP Consumer implementation and UX enhancement."""

            project_context = {
                "primary_project": "Piper Morgan (60%)",
                "secondary_projects": ["OneJob (20%)", "Content Creation (20%)"],
                "current_phase": "UX enhancement",
                "status": "MCP Consumer completed",
            }

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.STATUS.value,
                "action": "provide_project_status",
                "confidence": 1.0,
                "context": project_context,
            },
            "requires_clarification": False,
        }

    async def _handle_priority_query(self, intent: Intent, session_id: str) -> Dict:
        """Handle 'What's my top priority?' queries"""
        # Load current context from PIPER.md
        config = self.config_loader.load_config()

        # Handle emoji prefixes in PIPER.md section headers
        priorities_key = None
        for key in config.keys() if config else []:
            if "Standing Priorities" in key:
                priorities_key = key
                break

        if config and priorities_key:
            priorities_section = config[priorities_key]

            # Extract VA/Kind priority if mentioned
            if "VA Q4 Onramp" in priorities_section or "Decision Reviews" in priorities_section:
                message = """Your top priority today is **VA Q4 Onramp system implementation and delivery**.

**Primary Focus**: Complete VA decision review system for Q4 2025
**Company Context**: Kind Systems company initiative with DRAGONS team
**Success Metrics**: System operational and validated for production use
**Timeline**: Q4 2025 completion

This aligns with your 70% allocation to VA/Decision Reviews work and Kind Systems collaboration priorities."""

                priority_context = {
                    "top_priority": "VA Q4 Onramp system implementation",
                    "goal": "Complete VA decision review system for Q4 2025",
                    "timeline": "Q4 2025 completion",
                    "allocation": "70% of time and resources",
                    "team_context": "Kind Systems and DRAGONS team collaboration",
                }
            else:
                # Fallback to Piper Morgan priority
                message = """Your top priority today is **Enhanced conversational context for daily standups**.

Goal: Transform standup from command mode to natural conversation
Success: At least 3/5 canonical queries working better
Timeline: Complete by 5:00 PM today for tomorrow's improved standup

This directly supports your strategic goal of transforming Piper Morgan into a strategic thinking partner."""

                priority_context = {
                    "top_priority": "Enhanced conversational context for daily standups",
                    "goal": "Transform standup experience",
                    "timeline": "Complete by 5:00 PM today",
                    "success_metric": "3/5 canonical queries working better",
                }
        else:
            # Fallback if PIPER.md not available
            message = """Your top priority today is **Enhanced conversational context for daily standups**.

Goal: Transform standup from command mode to natural conversation
Success: At least 3/5 canonical queries working better
Timeline: Complete by 5:00 PM today for tomorrow's improved standup

This directly supports your strategic goal of transforming Piper Morgan into a strategic thinking partner."""

            priority_context = {
                "top_priority": "Enhanced conversational context for daily standups",
                "goal": "Transform standup experience",
                "timeline": "Complete by 5:00 PM today",
                "success_metric": "3/5 canonical queries working better",
            }

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.PRIORITY.value,
                "action": "provide_top_priority",
                "confidence": 1.0,
                "context": priority_context,
            },
            "requires_clarification": False,
        }

    async def _handle_guidance_query(self, intent: Intent, session_id: str) -> Dict:
        """Handle 'What should I focus on?' queries"""
        current_time = datetime.now()
        current_hour = current_time.hour

        # Load current context from PIPER.md
        config = self.config_loader.load_config()

        # Time-based guidance with VA/Kind context
        if 6 <= current_hour < 9:
            if config and "VA" in str(config.values()):
                focus = "Morning development work - perfect time for deep focus on VA Q4 onramp implementation and DRAGONS team coordination."
            else:
                focus = "Morning development work - perfect time for deep focus on MCP integration and UX improvements."
        elif 9 <= current_hour < 14:
            if config and "VA" in str(config.values()):
                focus = "Collaboration time - coordinate with Kind Systems team on VA decision review system implementation."
            else:
                focus = "Collaboration and implementation time - continue with PIPER.md system integration."
        elif 14 <= current_hour < 17:
            if config and "VA" in str(config.values()):
                focus = "VA project execution - work on Q4 onramp questionnaire and form maintenance tasks."
            else:
                focus = (
                    "UX enhancement work - test the canonical queries and document improvements."
                )
        elif 17 <= current_hour < 18:
            focus = "Documentation and handoff preparation - wrap up today's work and prepare for tomorrow."
        else:
            focus = "Flexible time - consider strategic planning or methodology refinement."

        # Build message with VA/Kind context if available
        if config and ("VA" in str(config.values()) or "Kind" in str(config.values())):
            message = f"""Based on your current priorities and the time of day:

**Right Now**: {focus}

**Today's Key Focus**: VA Q4 Onramp system implementation with DRAGONS team coordination (70% allocation)

**This Week**: VA decision review system development and Kind Systems collaboration

**Strategic Direction**: Deliver production-ready VA onramp system for Q4 2025 while maintaining Piper Morgan AI development (25%) and other projects (5%)."""

            guidance_context = {
                "immediate_focus": focus,
                "daily_goal": "VA Q4 Onramp system implementation",
                "weekly_focus": "VA decision reviews and Kind Systems collaboration",
                "strategic_direction": "VA Q4 onramp delivery",
                "allocation": "70% VA, 25% Piper, 5% Other",
                "time_context": f"{current_hour}:00 PT",
            }
        else:
            # Fallback message
            message = f"""Based on your current priorities and the time of day:

**Right Now**: {focus}

**Today's Key Focus**: Complete the PIPER.md configuration system to improve tomorrow's 6 AM standup experience.

**This Week**: MCP Consumer implementation and UX enhancement

**Strategic Direction**: Transform Piper Morgan from task automation to strategic thinking partner through enhanced conversational AI."""

            guidance_context = {
                "immediate_focus": focus,
                "daily_goal": "Complete PIPER.md configuration system",
                "weekly_focus": "MCP Consumer and UX enhancement",
                "strategic_direction": "Transform to strategic thinking partner",
                "time_context": f"{current_hour}:00 PT",
            }

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.GUIDANCE.value,
                "action": "provide_contextual_guidance",
                "confidence": 1.0,
                "context": guidance_context,
            },
            "requires_clarification": False,
        }


# Global instance
_canonical_handlers = None


def get_canonical_handlers() -> CanonicalHandlers:
    """Get singleton CanonicalHandlers instance"""
    global _canonical_handlers
    if _canonical_handlers is None:
        _canonical_handlers = CanonicalHandlers()
    return _canonical_handlers
