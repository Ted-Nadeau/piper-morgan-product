"""
Service for handling simple conversational queries with PIPER.md context integration

This service now provides context-aware responses based on Christian's personal
configuration, improving the standup experience and conversational flow.
"""

from datetime import datetime
from typing import Optional

from services.config import piper_config_loader


class ConversationQueryService:
    """Handles simple, stateless conversational queries with PIPER.md context."""

    def __init__(self):
        """Initialize with PIPER.md configuration loader."""
        self.config_loader = piper_config_loader

    async def get_greeting(self) -> str:
        """Returns a context-aware greeting message."""
        # Check if it's morning standup time
        current_hour = datetime.now().hour
        if 5 <= current_hour <= 7:
            return "Good morning, Christian! Ready for our daily standup? I have your current priorities and project status ready."
        elif 8 <= current_hour <= 11:
            return "Good morning, Christian! How can I help you with today's development work?"
        elif 12 <= current_hour <= 16:
            return "Good afternoon, Christian! What would you like to focus on this afternoon?"
        else:
            return "Hello, Christian! How can I assist you today?"

    async def get_help(self) -> str:
        """Returns a context-aware help message."""
        config = self.config_loader.load_config()

        help_parts = [
            "I can help you with several areas:",
            "",
            "**Project Management**:",
            "- Check current project status and priorities",
            "- Review GitHub issues and progress",
            "- Get project portfolio overview",
            "",
            "**Daily Operations**:",
            "- Morning standup and priority review",
            "- Calendar and schedule information",
            "- Knowledge source navigation",
            "",
            "**Development Support**:",
            "- MCP Consumer operations",
            "- Pattern application guidance",
            "- Documentation access",
            "",
            "**Quick Queries**:",
            "- 'What's my top priority?'",
            "- 'What am I working on?'",
            "- 'What should I focus on today?'",
            "- 'What day is it?'",
            "- 'What's your name and role?'",
        ]

        return "\n".join(help_parts)

    async def get_status(self) -> str:
        """Returns a context-aware status message."""
        config = self.config_loader.load_config()

        if not config:
            return "I'm operating normally. All systems are go!"

        # Get current focus from config
        current_focus = config.get(
            "Current Focus (Q4 2025)", "MCP implementation and UX enhancement"
        )

        status_parts = [
            "I'm operating normally with enhanced context awareness!",
            "",
            "**Current Focus**: " + current_focus,
            "**Configuration**: PIPER.md loaded and active",
            "**Context**: Personalized for Christian's workflow",
            "**Status**: Ready for context-aware assistance",
        ]

        return "\n".join(status_parts)

    async def get_initial_contact(self) -> str:
        """Handles a user's initial greeting with context awareness."""
        config = self.config_loader.load_config()

        if not config:
            return "Hello to you too, Christian! How can I help you today?"

        # Get user context and current focus
        user_context = config.get("User Context", "")
        current_focus = config.get("Current Focus (Q4 2025)", "")

        # Check if it's standup time
        current_hour = datetime.now().hour
        is_standup_time = 5 <= current_hour <= 7

        if is_standup_time:
            return (
                "Good morning, Christian! Perfect timing for our daily standup. "
                "I have your current priorities, project status, and calendar context ready. "
                "What would you like to review first?"
            )
        else:
            return (
                f"Hello, Christian! I'm ready to assist you with {current_focus.lower()}. "
                "How can I help you today?"
            )

    async def get_identity(self) -> str:
        """Returns identity information with context."""
        config = self.config_loader.load_config()

        identity_parts = [
            "**Name**: Piper Morgan",
            "**Role**: Your intelligent product management assistant",
            "**Specialization**: MCP integration, project management, and development support",
            "**Context**: Personalized for Christian's workflow and priorities",
            "**Capabilities**: Context-aware responses, project tracking, knowledge navigation",
        ]

        return "\n".join(identity_parts)

    async def get_temporal_context(self) -> str:
        """Returns current date/time with calendar context."""
        now = datetime.now()
        config = self.config_loader.load_config()

        temporal_parts = [
            f"**Current Time**: {now.strftime('%A, %B %d, %Y at %I:%M %p PT')}",
            f"**Day of Week**: {now.strftime('%A')}",
            f"**Week**: Week {now.isocalendar()[1]} of {now.year}",
        ]

        if config:
            calendar_patterns = config.get("Calendar Patterns", "")
            if calendar_patterns:
                temporal_parts.extend(["", "**Calendar Context**:", calendar_patterns])

        return "\n".join(temporal_parts)

    async def get_project_status(self) -> str:
        """Returns current project portfolio status."""
        config = self.config_loader.load_config()

        if not config:
            return "I don't have access to your current project portfolio. Please check your PIPER.md configuration."

        project_portfolio = config.get("Project Portfolio", "")
        current_focus = config.get("Current Focus (Q4 2025)", "")

        status_parts = [
            "**Current Project Portfolio**:",
            project_portfolio,
            "",
            "**Strategic Focus**:",
            current_focus,
        ]

        return "\n".join(status_parts)

    async def get_priorities(self) -> str:
        """Returns current standing priorities."""
        config = self.config_loader.load_config()

        if not config:
            return "I don't have access to your current priorities. Please check your PIPER.md configuration."

        standing_priorities = config.get("Standing Priorities", "")

        priority_parts = [
            "**Your Current Standing Priorities**:",
            standing_priorities,
            "",
            "**Recommendation**: Focus on Priority 1 first - it's designed to improve our daily interactions!",
        ]

        return "\n".join(priority_parts)

    async def get_guidance(self) -> str:
        """Returns synthesized guidance based on current context."""
        config = self.config_loader.load_config()

        if not config:
            return "I don't have enough context to provide specific guidance. Please check your PIPER.md configuration."

        # Get current time for context
        current_hour = datetime.now().hour

        guidance_parts = ["**Context-Aware Guidance**:"]

        if 5 <= current_hour <= 7:
            guidance_parts.extend(
                [
                    "It's standup time! Here's what I recommend:",
                    "1. Review today's top priority: Enhanced conversational context",
                    "2. Check project portfolio status and allocation",
                    "3. Plan your development focus blocks",
                    "4. Review any pending GitHub issues",
                ]
            )
        elif 8 <= current_hour <= 11:
            guidance_parts.extend(
                [
                    "Morning development focus time! Consider:",
                    "1. Deep work on MCP Consumer deployment",
                    "2. Pattern application to current tasks",
                    "3. Documentation updates and knowledge sharing",
                ]
            )
        elif 12 <= current_hour <= 16:
            guidance_parts.extend(
                [
                    "Afternoon productivity time! Focus on:",
                    "1. UX enhancement and user experience improvements",
                    "2. Testing and validation of recent changes",
                    "3. Planning for tomorrow's priorities",
                ]
            )
        else:
            guidance_parts.extend(
                [
                    "Evening planning time! Good time to:",
                    "1. Review today's accomplishments",
                    "2. Plan tomorrow's priorities",
                    "3. Update PIPER.md with any changes",
                ]
            )

        return "\n".join(guidance_parts)
