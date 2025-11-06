"""
Canonical Query Handlers
Specialized handlers for the 6 canonical categories:
- IDENTITY: "What's your name and role?"
- TEMPORAL: "What time is it?" / "What's on my calendar?"
- STATUS: "What am I working on?"
- PRIORITY: "What should I focus on?"
- GUIDANCE: "What should I do?" / "How can you help me?"
- CONVERSATION: Simple greetings and conversational responses

Issue #286: CONVERSATION added to canonical section (was handled separately)
"""

import logging
from datetime import datetime
from typing import Dict, Optional

import structlog

from services.configuration.piper_config_loader import piper_config_loader
from services.conversation.conversation_handler import ConversationHandler
from services.domain.models import Intent, IntentCategory
from services.shared_types import IntentCategory as IntentCategoryEnum
from services.user_context_service import user_context_service

logger = structlog.get_logger()

# Issue #287: Timezone abbreviation mapping
# Maps IANA timezone identifiers to common abbreviations
TIMEZONE_ABBREVIATIONS = {
    # US Timezones
    "America/Los_Angeles": "PT",
    "America/New_York": "ET",
    "America/Chicago": "CT",
    "America/Denver": "MT",
    "America/Phoenix": "MST",  # Arizona (no DST)
    "America/Anchorage": "AKT",
    "Pacific/Honolulu": "HST",
    # International
    "Europe/London": "GMT",
    "Europe/Paris": "CET",
    "Europe/Berlin": "CET",
    "Asia/Tokyo": "JST",
    "Asia/Shanghai": "CST",
    "Asia/Hong_Kong": "HKT",
    "Asia/Singapore": "SGT",
    "Australia/Sydney": "AEDT",
    "Australia/Melbourne": "AEDT",
    # Fallback
    "UTC": "UTC",
}


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
            IntentCategoryEnum.CONVERSATION,  # Issue #286: CONVERSATION is canonical
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
            elif intent.category == IntentCategoryEnum.CONVERSATION:
                # Issue #286: Handle CONVERSATION in canonical section
                return await self._handle_conversation_query(intent, session_id)
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
        """
        Handle 'What's your name and role?' queries with spatial awareness.

        GREAT-4C Phase 1: Minimal spatial intelligence (identity is fixed).
        """
        # Get spatial pattern (GREAT-4C Phase 1: Spatial intelligence)
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        # Adjust response detail based on spatial pattern
        if spatial_pattern == "GRANULAR":
            message = self._format_detailed_identity()
        elif spatial_pattern == "EMBEDDED":
            message = self._format_consolidated_identity()
        else:
            message = self._format_standard_identity()

        return {
            "message": message,
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
            "spatial_pattern": spatial_pattern,
            "requires_clarification": False,
        }

    def _format_detailed_identity(self) -> str:
        """GRANULAR: Full identity with comprehensive capabilities."""
        details = ["I'm **Piper Morgan**, your AI Product Management assistant.\n"]
        details.append("**Core Capabilities**:")
        details.append("  - Development coordination and team synchronization")
        details.append("  - Issue tracking and GitHub integration")
        details.append("  - Strategic planning and roadmap management")
        details.append("  - Calendar integration for meeting coordination")
        details.append("  - Notion integration for documentation management")
        details.append("  - Slack integration for team communication\n")
        details.append("**Role**: I serve as your intelligent PM partner, helping you stay")
        details.append("organized, focused, and productive across all your development work.")
        return "\n".join(details)

    def _format_consolidated_identity(self) -> str:
        """EMBEDDED: Brief identity for embedded context."""
        return "Piper Morgan, AI PM Assistant"

    def _format_standard_identity(self) -> str:
        """DEFAULT: Moderate detail for standard identity queries."""
        return "I'm Piper Morgan, your AI Product Management assistant. I help with development coordination, issue tracking, and strategic planning. Think of me as your intelligent PM partner!"

    async def _handle_temporal_query(self, intent: Intent, session_id: str) -> Dict:
        """
        Handle 'What day is it?' and time-related queries with spatial awareness.

        GREAT-4C Phase 1: Adds spatial intelligence for calendar detail level.
        """
        from services.configuration.piper_config_loader import piper_config_loader

        # Get spatial pattern (GREAT-4C Phase 1: Spatial intelligence)
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        current_date = datetime.now().strftime("%A, %B %d, %Y")
        # Load timezone from configuration
        standup_config = piper_config_loader.load_standup_config()
        timezone = standup_config["timing"]["timezone"]
        # Issue #287 Fix #1: Use timezone abbreviation instead of city name
        timezone_short = TIMEZONE_ABBREVIATIONS.get(timezone, "UTC")
        current_time = datetime.now().strftime(f"%I:%M %p {timezone_short}")

        # Base message
        if spatial_pattern == "EMBEDDED":
            # Brief: Just date/time
            message = f"{current_date}"
        else:
            # Standard/Granular: Include time
            message = f"Today is {current_date} at {current_time}."

        calendar_context = {}

        # Enhanced: Get real calendar data from CalendarIntegrationRouter
        try:
            from services.integrations.calendar.calendar_integration_router import (
                CalendarIntegrationRouter,
            )

            calendar_adapter = CalendarIntegrationRouter()
            temporal_summary = await calendar_adapter.get_temporal_summary()

            # Adjust calendar detail based on spatial pattern
            if spatial_pattern == "EMBEDDED":
                # EMBEDDED: Minimal - just current/next meeting
                if temporal_summary.get("current_meeting"):
                    current_meeting = temporal_summary["current_meeting"]
                    message += f" (in meeting)"
                    calendar_context["current_meeting"] = current_meeting.get("title", "Meeting")
                elif temporal_summary.get("next_meeting"):
                    next_meeting = temporal_summary["next_meeting"]
                    message += f" (next: {next_meeting.get('start_time', 'TBD')})"
                    calendar_context["next_meeting"] = {
                        "time": next_meeting.get("start_time", "TBD")
                    }

            elif spatial_pattern == "GRANULAR":
                # GRANULAR: Comprehensive calendar breakdown
                if temporal_summary.get("current_meeting"):
                    current_meeting = temporal_summary["current_meeting"]
                    message += f"\n\n**Current Meeting**: {current_meeting.get('title', 'Meeting')}"
                    message += f"\n- Duration: {current_meeting.get('duration', 'Unknown')}"
                    calendar_context["current_meeting"] = current_meeting.get("title", "Meeting")

                if temporal_summary.get("next_meeting"):
                    next_meeting = temporal_summary["next_meeting"]
                    message += f"\n\n**Next Meeting**: {next_meeting.get('title', 'Meeting')}"
                    message += f"\n- Time: {next_meeting.get('start_time', 'TBD')}"
                    calendar_context["next_meeting"] = {
                        "title": next_meeting.get("title", "Meeting"),
                        "time": next_meeting.get("start_time", "TBD"),
                    }

                free_blocks = temporal_summary.get("free_blocks", [])
                if free_blocks:
                    message += f"\n\n**Focus Time Available**: {len(free_blocks)} blocks"
                    for block in free_blocks[:3]:  # Top 3
                        message += f"\n- {block.get('duration_minutes', 0)} min at {block.get('start', 'TBD')}"

                stats = temporal_summary.get("stats", {})
                if stats.get("total_meetings_today", 0) > 0:
                    meeting_count = stats["total_meetings_today"]
                    meeting_hours = stats.get("total_meeting_time_minutes", 0) / 60
                    message += f"\n\n**Meeting Load**: {meeting_count} meetings ({meeting_hours:.1f} hours)"
                    calendar_context["meeting_load"] = {
                        "count": meeting_count,
                        "hours": meeting_hours,
                    }

            else:
                # DEFAULT: Standard detail
                # Issue #287 Fix #2: Prevent contradictory messages
                # Only show stats block if no current/next meeting mentioned
                if temporal_summary.get("current_meeting"):
                    current_meeting = temporal_summary["current_meeting"]
                    message += f" You're currently in: {current_meeting.get('title', 'a meeting')}"
                    calendar_context["current_meeting"] = current_meeting.get("title", "Meeting")
                elif temporal_summary.get("next_meeting"):
                    next_meeting = temporal_summary["next_meeting"]
                    message += f" Your next meeting is: {next_meeting.get('title', 'Meeting')} at {next_meeting.get('start_time', 'TBD')}"
                    calendar_context["next_meeting"] = {
                        "title": next_meeting.get("title", "Meeting"),
                        "time": next_meeting.get("start_time", "TBD"),
                    }
                else:
                    # No current or upcoming meeting - show daily summary
                    stats = temporal_summary.get("stats", {})
                    if stats.get("total_meetings_today", 0) > 0:
                        meeting_count = stats["total_meetings_today"]
                        message += f" ({meeting_count} meetings scheduled today)"
                        calendar_context["meeting_load"] = {"count": meeting_count}
                    else:
                        message += " (No meetings - great day for deep work!)"
                        calendar_context["calendar_status"] = "free_day"

        except Exception as e:
            # Issue #287 Fix #3: Enhanced calendar validation and error handling
            # Calendar unavailable - log but continue with helpful message
            logger.warning(f"Calendar service unavailable: {e}", exc_info=True)

            if spatial_pattern != "EMBEDDED":
                # Provide user-friendly error message (not for EMBEDDED - too verbose)
                error_type = type(e).__name__
                if "timeout" in str(e).lower() or "TimeoutError" in error_type:
                    message += "\n\n⚠️ Note: Calendar check timed out. Your calendar may be temporarily unavailable."
                elif "auth" in str(e).lower() or "permission" in str(e).lower():
                    message += "\n\n⚠️ Note: Calendar authentication needed. Please check your calendar connection."
                else:
                    message += "\n\n⚠️ Note: I couldn't access your calendar right now. The calendar service may be unavailable."

            calendar_context["calendar_service"] = "unavailable"
            calendar_context["fallback_used"] = True
            calendar_context["error_type"] = type(e).__name__

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.TEMPORAL.value,
                "action": "provide_current_time_with_calendar",
                "confidence": 1.0,
                "context": {
                    "current_date": current_date,
                    "current_time": current_time,
                    "timezone": "Pacific Time",
                    "calendar_context": calendar_context,
                },
            },
            "spatial_pattern": spatial_pattern,
            "requires_clarification": False,
        }

    async def _handle_status_query(self, intent: Intent, session_id: str) -> Dict:
        """
        Handle 'What am I working on?' queries with spatial awareness.

        GREAT-4C Phase 1: Adds spatial intelligence for response granularity.
        GREAT-4C Phase 2: Adds error handling for missing configuration.
        """
        # Try to get user context with error handling
        try:
            user_context = await user_context_service.get_user_context(session_id)
        except Exception as e:
            logger.error(f"Failed to load user context: {e}")
            return {
                "message": "I'm having trouble accessing your configuration right now. "
                "Your PIPER.md file may be missing or unreadable. "
                "Would you like help setting it up?",
                "error": "config_unavailable",
                "action_required": "setup_piper_config",
                "intent": {
                    "category": IntentCategoryEnum.STATUS.value,
                    "action": "provide_status",
                    "confidence": 1.0,
                },
            }

        # Get spatial pattern (GREAT-4C Phase 1: Spatial intelligence)
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        # Get projects from user context
        projects = user_context.projects

        # Check if we have project data
        if not projects:
            return {
                "message": "You don't have any active projects configured in your PIPER.md yet. "
                "Would you like me to help you set up your project portfolio?",
                "action_required": "configure_projects",
                "intent": {
                    "category": IntentCategoryEnum.STATUS.value,
                    "action": "provide_status",
                    "confidence": 1.0,
                },
            }

        # Adjust response detail based on spatial pattern
        if spatial_pattern == "GRANULAR":
            # Detailed status with full project breakdown
            message = self._format_detailed_status(projects, user_context)
        elif spatial_pattern == "EMBEDDED":
            # Brief consolidated status
            message = self._format_consolidated_status(projects, user_context)
        else:
            # Standard moderate detail
            message = self._format_standard_status(projects, user_context)

        project_context = {
            "projects": projects,
            "spatial_pattern": spatial_pattern,
            "organization": user_context.organization,
        }

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.STATUS.value,
                "action": "provide_project_status",
                "confidence": 1.0,
                "context": project_context,
            },
            "spatial_pattern": spatial_pattern,
            "requires_clarification": False,
        }

    def _format_detailed_status(self, projects: list, user_context) -> str:
        """GRANULAR: Full project details with comprehensive breakdown."""
        if not projects:
            return "No active projects configured in your PIPER.md."

        details = ["Here's your detailed project status:\n"]
        for i, project in enumerate(projects, 1):
            details.append(f"\n**{i}. {project}**")
            details.append(f"  - Status: Active development")
            details.append(f"  - Organization: {user_context.organization or 'Not specified'}")
            details.append(f"  - Next steps: Continue implementation")

        if user_context.priorities:
            details.append(f"\n\nCurrent priorities: {', '.join(user_context.priorities[:3])}")

        return "\n".join(details)

    def _format_consolidated_status(self, projects: list, user_context) -> str:
        """EMBEDDED: Brief overview suitable for embedded context."""
        if not projects:
            return "No active projects."

        if len(projects) == 1:
            return f"Working on: {projects[0]}"
        elif len(projects) <= 3:
            return f"Working on {len(projects)} projects: {', '.join(projects)}"
        else:
            return f"Working on {len(projects)} projects: {', '.join(projects[:3])} + {len(projects)-3} more"

    def _format_standard_status(self, projects: list, user_context) -> str:
        """DEFAULT: Moderate detail level for standard queries."""
        if not projects:
            return "No active projects configured in your PIPER.md. Add projects to the 'Projects' section to see them here."

        summary = [
            f"You're working on {len(projects)} active project{'s' if len(projects) != 1 else ''}:\n"
        ]
        for project in projects[:5]:  # Top 5
            summary.append(f"- {project}")

        if len(projects) > 5:
            summary.append(f"- ... and {len(projects) - 5} more")

        if user_context.organization:
            summary.append(f"\nOrganization: {user_context.organization}")

        return "\n".join(summary)

    async def _handle_priority_query(self, intent: Intent, session_id: str) -> Dict:
        """
        Handle 'What's my top priority?' queries with spatial awareness.

        GREAT-4C Phase 1: Adds spatial intelligence for response granularity.
        GREAT-4C Phase 2: Adds error handling for missing configuration.
        """
        # Try to get user context with error handling
        try:
            user_context = await user_context_service.get_user_context(session_id)
        except Exception as e:
            logger.error(f"Failed to load user context: {e}")
            return {
                "message": "I'm having trouble accessing your configuration right now. "
                "Your PIPER.md file may be missing or unreadable. "
                "Would you like help setting it up?",
                "error": "config_unavailable",
                "action_required": "setup_piper_config",
                "intent": {
                    "category": IntentCategoryEnum.PRIORITY.value,
                    "action": "provide_priority",
                    "confidence": 1.0,
                },
            }

        # Get spatial pattern (GREAT-4C Phase 1: Spatial intelligence)
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        # Get priorities from user context
        priorities = user_context.priorities

        # Check if we have priority data
        if not priorities:
            return {
                "message": "You don't have any priorities configured in your PIPER.md yet. "
                "Would you like me to help you set up your priority list?",
                "action_required": "configure_priorities",
                "intent": {
                    "category": IntentCategoryEnum.PRIORITY.value,
                    "action": "provide_priority",
                    "confidence": 1.0,
                },
            }

        # Adjust response detail based on spatial pattern
        if spatial_pattern == "GRANULAR":
            # Detailed priorities with breakdown
            message = self._format_detailed_priorities(priorities, user_context)
        elif spatial_pattern == "EMBEDDED":
            # Brief priority statement
            message = self._format_consolidated_priorities(priorities, user_context)
        else:
            # Standard moderate detail
            message = self._format_standard_priorities(priorities, user_context)

        priority_context = {
            "priorities": priorities,
            "spatial_pattern": spatial_pattern,
            "organization": user_context.organization,
        }

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.PRIORITY.value,
                "action": "provide_top_priority",
                "confidence": 1.0,
                "context": priority_context,
            },
            "spatial_pattern": spatial_pattern,
            "requires_clarification": False,
        }

    def _format_detailed_priorities(self, priorities: list, user_context) -> str:
        """GRANULAR: Detailed priority breakdown."""
        if not priorities:
            return "No priorities configured in your PIPER.md."

        details = ["Here are your priorities in detail:\n"]
        for i, priority in enumerate(priorities, 1):
            details.append(f"\n**Priority {i}: {priority}**")
            details.append(f"  - Status: Active")
            details.append(f"  - Focus area: Implementation and delivery")

        if user_context.organization:
            details.append(f"\n\nOrganization context: {user_context.organization}")

        return "\n".join(details)

    def _format_consolidated_priorities(self, priorities: list, user_context) -> str:
        """EMBEDDED: Brief priority summary."""
        if not priorities:
            return "No priorities set."

        if len(priorities) == 1:
            return f"Top priority: {priorities[0]}"
        else:
            return f"Top priority: {priorities[0]} ({len(priorities)} total)"

    def _format_standard_priorities(self, priorities: list, user_context) -> str:
        """DEFAULT: Moderate detail for priorities."""
        if not priorities:
            return "No priorities configured in your PIPER.md. Add priorities to the 'Priorities' section to see them here."

        message = [f"Your top priority today is: **{priorities[0]}**\n"]

        if len(priorities) > 1:
            message.append("\nOther priorities:")
            for priority in priorities[1:4]:  # Show up to 3 more
                message.append(f"- {priority}")

            if len(priorities) > 4:
                message.append(f"- ... and {len(priorities) - 4} more")

        if user_context.organization:
            message.append(f"\n\nOrganization: {user_context.organization}")

        return "\n".join(message)

    def _get_immediate_focus(self, current_hour: int, user_context) -> str:
        """Get time-based immediate focus suggestion with fallback for missing context."""
        if 6 <= current_hour < 9:
            if user_context and user_context.organization:
                return f"Morning development work - perfect time for deep focus on {user_context.organization} implementation and coordination."
            else:
                return "Morning development work - perfect time for deep focus and complex problem-solving."
        elif 9 <= current_hour < 14:
            if user_context and user_context.organization:
                return f"Collaboration time - coordinate with your team on {user_context.organization} implementation."
            else:
                return "Collaboration time - good for meetings and team coordination."
        elif 14 <= current_hour < 17:
            if user_context and user_context.projects:
                top_project = user_context.projects[0]
                return f"Project execution - work on {top_project} tasks."
            else:
                return "Execution time - work on your current tasks and deliverables."
        elif 17 <= current_hour < 18:
            return "Documentation and handoff preparation - wrap up today's work and prepare for tomorrow."
        else:
            return "Flexible time - consider strategic planning or methodology refinement."

    def _format_detailed_guidance(self, current_hour: int, user_context) -> str:
        """GRANULAR: Comprehensive guidance with all timeframes and context."""
        focus = self._get_immediate_focus(current_hour, user_context)
        priority_text = (
            user_context.priorities[0]
            if user_context and user_context.priorities
            else "your key priorities"
        )
        org_text = (
            user_context.organization
            if user_context and user_context.organization
            else "your projects"
        )

        details = ["Here's comprehensive guidance for your focus:\n"]
        details.append(f"**Immediate Focus (Right Now)**:")
        details.append(f"  {focus}\n")

        details.append(f"**Today's Key Focus**:")
        details.append(f"  - Primary priority: {priority_text}")
        if user_context and user_context.priorities and len(user_context.priorities) > 1:
            details.append(f"  - Secondary priorities:")
            for priority in user_context.priorities[1:3]:
                details.append(f"    • {priority}")

        details.append(f"\n**This Week**:")
        details.append(f"  - Continue work on {org_text}")
        if user_context.projects:
            details.append(f"  - Active projects:")
            for project in user_context.projects[:3]:
                details.append(f"    • {project}")

        details.append(f"\n**Strategic Direction**:")
        details.append(
            f"  - Deliver on your priorities while maintaining progress across all projects"
        )
        details.append(f"  - Balance deep focus work with collaboration and coordination")
        details.append(f"  - Maintain quality standards throughout implementation")

        return "\n".join(details)

    def _format_consolidated_guidance(self, current_hour: int, user_context) -> str:
        """EMBEDDED: Brief guidance suitable for embedded context."""
        focus = self._get_immediate_focus(current_hour, user_context)

        # Extract just the key action from the focus
        if "Morning development" in focus:
            return "Focus: Deep work"
        elif "Collaboration" in focus:
            return "Focus: Team coordination"
        elif "Project execution" in focus or "Execution time" in focus:
            return "Focus: Task execution"
        elif "Documentation" in focus:
            return "Focus: Wrap-up and handoff"
        else:
            return "Focus: Strategic planning"

    def _format_standard_guidance(self, current_hour: int, user_context) -> str:
        """DEFAULT: Moderate detail for standard guidance queries."""
        focus = self._get_immediate_focus(current_hour, user_context)
        priority_text = (
            user_context.priorities[0]
            if user_context and user_context.priorities
            else "your key priorities"
        )
        org_text = (
            user_context.organization
            if user_context and user_context.organization
            else "your projects"
        )

        message = [f"Based on your current priorities and the time of day:\n"]
        message.append(f"**Right Now**: {focus}\n")
        message.append(f"**Today's Key Focus**: {priority_text}\n")
        message.append(f"**This Week**: Continue work on {org_text}\n")
        message.append(
            f"**Strategic Direction**: Deliver on your priorities while maintaining progress across all projects."
        )

        return "\n".join(message)

    async def _handle_guidance_query(self, intent: Intent, session_id: str) -> Dict:
        """
        Handle 'What should I focus on?' queries with spatial awareness.

        GREAT-4C Phase 1: Adds spatial intelligence for guidance granularity.
        GREAT-4C Phase 2: Adds error handling with fallback guidance.
        """
        current_time = datetime.now()
        current_hour = current_time.hour

        # Try to get user-specific context with fallback to generic guidance
        user_context = None
        try:
            user_context = await user_context_service.get_user_context(session_id)
        except Exception as e:
            logger.warning(f"Using generic guidance, user context unavailable: {e}")

        # Get spatial pattern (GREAT-4C Phase 1: Spatial intelligence)
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        # Adjust response detail based on spatial pattern
        if spatial_pattern == "GRANULAR":
            message = self._format_detailed_guidance(current_hour, user_context)
        elif spatial_pattern == "EMBEDDED":
            message = self._format_consolidated_guidance(current_hour, user_context)
        else:
            message = self._format_standard_guidance(current_hour, user_context)

        # Load timezone from configuration (same for all users)
        from services.configuration.piper_config_loader import piper_config_loader

        standup_config = piper_config_loader.load_standup_config()
        timezone = standup_config["timing"]["timezone"]
        timezone_short = timezone.split("/")[-1].replace("_", " ")

        # Extract guidance context components for API response
        focus = self._get_immediate_focus(current_hour, user_context)
        priority_text = (
            user_context.priorities[0]
            if user_context and user_context.priorities
            else "your key priorities"
        )
        org_text = (
            user_context.organization
            if user_context and user_context.organization
            else "your projects"
        )

        guidance_context = {
            "immediate_focus": focus,
            "daily_goal": priority_text,
            "weekly_focus": f"Continue work on {org_text}",
            "strategic_direction": "Deliver on your priorities while maintaining progress across all projects",
            "time_context": f"{current_hour}:00 {timezone_short}",
        }

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.GUIDANCE.value,
                "action": "provide_contextual_guidance",
                "confidence": 1.0,
                "context": guidance_context,
            },
            "spatial_pattern": spatial_pattern,
            "personalized": bool(user_context),
            "fallback_guidance": not user_context,
            "requires_clarification": False,
        }

    async def _handle_conversation_query(self, intent: Intent, session_id: str) -> Dict:
        """
        Handle CONVERSATION category intents (Tier 1 bypass).

        Issue #286: Moved to canonical section for architectural consistency.
        CONVERSATION is a canonical category like IDENTITY, TEMPORAL, etc.

        Phase 3D: Conversation handling without full orchestration.
        """
        # Initialize conversation handler
        conversation_handler = ConversationHandler(session_manager=None)

        # Get conversation response
        result = await conversation_handler.respond(intent, session_id)

        # Return in canonical format (Dict)
        return {
            "message": result["message"],
            "intent": result["intent"],
            "workflow_id": result.get("workflow_id"),
            "requires_clarification": result.get("requires_clarification", False),
            "clarification_type": result.get("clarification_type"),
        }


# Global instance
_canonical_handlers = None


def get_canonical_handlers() -> CanonicalHandlers:
    """Get singleton CanonicalHandlers instance"""
    global _canonical_handlers
    if _canonical_handlers is None:
        _canonical_handlers = CanonicalHandlers()
    return _canonical_handlers
