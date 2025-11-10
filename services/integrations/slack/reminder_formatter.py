"""
Reminder Message Formatter

Formats daily standup reminder messages for Slack.
Includes web, CLI, and API access methods.

Issue: #161 (CORE-STAND-SLACK-REMIND)
Task: 3 of 4 - Message Formatting
"""

from datetime import datetime
from typing import Any, Dict
from uuid import UUID
from zoneinfo import ZoneInfo

import structlog

logger = structlog.get_logger(__name__)


class ReminderMessageFormatter:
    """
    Formats daily standup reminder messages.

    Responsibilities:
    - Generate timezone-aware greeting
    - Format web/CLI/API links
    - Create user-friendly message
    - Include disable instructions
    """

    def __init__(self, base_url: str = "https://piper-morgan.com"):
        """
        Initialize formatter.

        Args:
            base_url: Base URL for web links (default: https://piper-morgan.com)
        """
        self.base_url = base_url.rstrip("/")

    def format_reminder_message(
        self, user_id: str, user_timezone: str = "America/Los_Angeles"
    ) -> str:
        """
        Format reminder message for user.

        Args:
            user_id: User ID for personalization
            user_timezone: User's timezone for greeting

        Returns:
            Formatted Slack message text
        """
        # Get timezone-aware greeting
        greeting = self._get_greeting(user_timezone)

        # Generate links
        web_link = self._generate_web_link()
        cli_command = self._generate_cli_command()
        api_endpoint = self._generate_api_endpoint()

        # Format message
        message = f"""{greeting}

Generate your standup:
• Web: {web_link}
• CLI: `{cli_command}`
• API: {api_endpoint}

Disable reminders: Reply "STOP" or update preferences"""

        return message

    def _get_greeting(self, timezone: str) -> str:
        """
        Get timezone-aware greeting.

        Args:
            timezone: IANA timezone name

        Returns:
            Greeting string with emoji
        """
        try:
            # Get current hour in user's timezone
            user_time = datetime.now(ZoneInfo(timezone))
            hour = user_time.hour

            # Choose greeting based on time of day
            if 5 <= hour < 12:
                return "🌅 Good morning! Time for your daily standup."
            elif 12 <= hour < 17:
                return "☀️ Good afternoon! Time for your daily standup."
            elif 17 <= hour < 21:
                return "🌆 Good evening! Time for your daily standup."
            else:
                return "🌙 Hello! Time for your daily standup."

        except Exception as e:
            logger.warning("Error getting timezone-aware greeting", timezone=timezone, error=str(e))
            # Fallback to neutral greeting
            return "👋 Hello! Time for your daily standup."

    def _generate_web_link(self) -> str:
        """
        Generate web standup link.

        Returns:
            Full URL to standup page
        """
        return f"{self.base_url}/standup"

    def _generate_cli_command(self) -> str:
        """
        Generate CLI command.

        Returns:
            CLI command string
        """
        return "piper standup"

    def _generate_api_endpoint(self) -> str:
        """
        Generate API endpoint.

        Returns:
            API endpoint description
        """
        return "POST /api/v1/standup/generate"

    def format_example_message(self) -> str:
        """
        Generate example message for testing.

        Returns:
            Example formatted message
        """
        return self.format_reminder_message(
            user_id="example_user", user_timezone="America/Los_Angeles"
        )


# Global formatter instance
_formatter = None


def get_reminder_formatter(
    base_url: str = "https://piper-morgan.com",
) -> ReminderMessageFormatter:
    """
    Get or create global reminder formatter.

    Args:
        base_url: Base URL for web links

    Returns:
        ReminderMessageFormatter instance
    """
    global _formatter

    if _formatter is None:
        _formatter = ReminderMessageFormatter(base_url)

    return _formatter
