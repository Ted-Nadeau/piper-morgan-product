"""
Tests for command definitions.

Issue #551: ARCH-COMMANDS
ADR-057: CommandRegistry
"""

import pytest

from services.commands.definitions import (
    ALL_COMMANDS,
    CALENDAR_TODAY_COMMAND,
    DISCOVERY_COMMAND,
    STANDUP_COMMAND,
    get_parity_gaps,
    register_all_commands,
)
from services.commands.registry import CommandCategory, CommandInterface, CommandRegistry


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear registry before and after each test."""
    CommandRegistry.clear()
    yield
    CommandRegistry.clear()


class TestCommandDefinitions:
    """Test individual command definitions."""

    def test_standup_command_definition(self):
        """Test standup command is properly defined."""
        assert STANDUP_COMMAND.name == "standup"
        assert STANDUP_COMMAND.category == CommandCategory.STANDUP
        assert STANDUP_COMMAND.is_available_on(CommandInterface.SLACK)
        assert STANDUP_COMMAND.is_available_on(CommandInterface.CLI)
        assert STANDUP_COMMAND.is_available_on(CommandInterface.WEB_CHAT)

    def test_calendar_today_command(self):
        """Test calendar today command definition."""
        assert CALENDAR_TODAY_COMMAND.name == "calendar_today"
        assert CALENDAR_TODAY_COMMAND.category == CommandCategory.CALENDAR
        assert CALENDAR_TODAY_COMMAND.requires_integration == "calendar"

        # Check interface availability - Issue #551 Phase 4: All interfaces enabled
        assert CALENDAR_TODAY_COMMAND.is_available_on(CommandInterface.WEB_CHAT)
        assert CALENDAR_TODAY_COMMAND.is_available_on(CommandInterface.CLI)
        assert CALENDAR_TODAY_COMMAND.is_available_on(CommandInterface.SLACK)

    def test_discovery_command(self):
        """Test discovery command definition (from #488)."""
        assert DISCOVERY_COMMAND.name == "discovery"
        assert DISCOVERY_COMMAND.category == CommandCategory.DISCOVERY
        assert DISCOVERY_COMMAND.handler_name == "_handle_discovery_query"

    def test_all_commands_have_required_fields(self):
        """Test all commands have required fields."""
        for cmd in ALL_COMMANDS:
            assert cmd.name, f"Command missing name"
            assert cmd.display_name, f"{cmd.name} missing display_name"
            assert cmd.description, f"{cmd.name} missing description"
            assert cmd.category, f"{cmd.name} missing category"


class TestRegisterAllCommands:
    """Test register_all_commands function."""

    def test_register_all_commands(self):
        """Test that all commands are registered."""
        count = register_all_commands()

        assert count == len(ALL_COMMANDS)
        assert CommandRegistry.get_command_count() == len(ALL_COMMANDS)
        assert CommandRegistry.is_initialized()

    def test_commands_accessible_after_registration(self):
        """Test commands can be retrieved after registration."""
        register_all_commands()

        standup = CommandRegistry.get_command("standup")
        assert standup is not None
        assert standup.display_name == "Daily Standup"

        discovery = CommandRegistry.get_command("discovery")
        assert discovery is not None

    def test_help_generation_after_registration(self):
        """Test help text can be generated."""
        register_all_commands()

        help_text = CommandRegistry.get_help(CommandInterface.WEB_CHAT)
        assert "Available Commands" in help_text
        assert "Standup" in help_text


class TestParityGaps:
    """Test parity gap detection."""

    def test_get_parity_gaps(self):
        """Test identifying commands with interface gaps.

        Issue #551 Phase 4: Most gaps are now closed.
        """
        gaps = get_parity_gaps()

        # Issue #551 Phase 4: Calendar, status, priority Slack gaps closed
        assert "calendar_today" not in gaps
        assert "priority" not in gaps
        assert "status" not in gaps

        # calendar_week has URL disabled (intentionally)
        assert "calendar_week" in gaps
        assert "url" in gaps["calendar_week"]

    def test_standup_has_no_gaps(self):
        """Test that standup (ALL interface) has no gaps."""
        gaps = get_parity_gaps()
        assert "standup" not in gaps


class TestSlackCommands:
    """Test Slack-specific command availability."""

    def test_slack_available_commands(self):
        """Test commands available on Slack.

        Issue #551 Phase 4: Calendar, status, priority now available.
        """
        register_all_commands()

        slack_commands = CommandRegistry.list_commands(interface=CommandInterface.SLACK)
        slack_names = [c.name for c in slack_commands]

        # Should be available
        assert "standup" in slack_names
        assert "discovery" in slack_names
        assert "identity" in slack_names
        assert "help" in slack_names

        # Issue #551 Phase 4: Gaps closed - these are now available
        assert "calendar_today" in slack_names
        assert "calendar_week" in slack_names
        assert "priority" in slack_names
        assert "status" in slack_names

    def test_slack_help_generation(self):
        """Test Slack-specific help generation."""
        register_all_commands()

        help_text = CommandRegistry.get_help(CommandInterface.SLACK)

        # Should include available commands
        assert "Daily Standup" in help_text
        assert "Capabilities" in help_text  # discovery

        # Issue #551 Phase 4: Calendar now available on Slack
        assert "Today's Calendar" in help_text


class TestCLICommands:
    """Test CLI-specific command availability."""

    def test_cli_available_commands(self):
        """Test commands available on CLI."""
        register_all_commands()

        cli_commands = CommandRegistry.list_commands(interface=CommandInterface.CLI)
        cli_names = [c.name for c in cli_commands]

        assert "standup" in cli_names
        assert "calendar_today" in cli_names
        assert "status" in cli_names


class TestWebChatCommands:
    """Test Web Chat command availability."""

    def test_webchat_has_most_commands(self):
        """Test that web chat has the most commands available."""
        register_all_commands()

        webchat_commands = CommandRegistry.list_commands(interface=CommandInterface.WEB_CHAT)
        slack_commands = CommandRegistry.list_commands(interface=CommandInterface.SLACK)

        # Web chat should have more or equal commands
        assert len(webchat_commands) >= len(slack_commands)
