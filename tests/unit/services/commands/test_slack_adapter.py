"""
Tests for Slack CommandRegistry adapter.

Issue #551: ARCH-COMMANDS
ADR-057: CommandRegistry
"""

import pytest

from services.commands.adapters.slack_adapter import SlackCommandAdapter
from services.commands.definitions import register_all_commands
from services.commands.registry import (
    CommandCategory,
    CommandDefinition,
    CommandInterface,
    CommandRegistry,
    InterfaceConfig,
)


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear registry before and after each test."""
    CommandRegistry.clear()
    yield
    CommandRegistry.clear()


class TestSlackCommandAdapter:
    """Test SlackCommandAdapter class."""

    def test_interface_is_slack(self):
        """Test that adapter is for Slack interface."""
        assert SlackCommandAdapter.interface == CommandInterface.SLACK

    def test_get_commands_empty(self):
        """Test get_commands when registry is empty."""
        commands = SlackCommandAdapter.get_commands()
        assert commands == []

    def test_get_commands_with_registration(self):
        """Test get_commands after registration."""
        register_all_commands()

        commands = SlackCommandAdapter.get_commands()
        assert len(commands) > 0

        # Should only include Slack-enabled commands
        for cmd in commands:
            assert cmd.is_available_on(CommandInterface.SLACK)

    def test_format_command(self):
        """Test formatting a command for Slack."""
        cmd = CommandDefinition(
            name="test_cmd",
            display_name="Test Command",
            description="A test",
            category=CommandCategory.STANDUP,
            interfaces={
                CommandInterface.SLACK: InterfaceConfig(
                    enabled=True,
                    slack_response_type="in_channel",
                    aliases=["test"],
                )
            },
        )

        formatted = SlackCommandAdapter.format_command(cmd)

        assert formatted["name"] == "test_cmd"
        assert formatted["display_name"] == "Test Command"
        assert formatted["description"] == "A test"
        assert formatted["response_type"] == "in_channel"
        assert "test" in formatted["aliases"]

    def test_format_command_with_override(self):
        """Test formatting uses description override."""
        cmd = CommandDefinition(
            name="override_cmd",
            display_name="Override",
            description="Original description",
            category=CommandCategory.HELP,
            interfaces={
                CommandInterface.SLACK: InterfaceConfig(
                    enabled=True,
                    description_override="Slack-specific description",
                )
            },
        )

        formatted = SlackCommandAdapter.format_command(cmd)
        assert formatted["description"] == "Slack-specific description"

    def test_get_command_map(self):
        """Test getting command map with aliases."""
        cmd = CommandDefinition(
            name="mapped_cmd",
            display_name="Mapped",
            description="Test",
            category=CommandCategory.STANDUP,
            interfaces={
                CommandInterface.SLACK: InterfaceConfig(
                    enabled=True,
                    aliases=["alias1", "alias2"],
                )
            },
        )
        CommandRegistry.register(cmd)

        command_map = SlackCommandAdapter.get_command_map()

        # Primary name
        assert "mapped_cmd" in command_map
        # Aliases
        assert "alias1" in command_map
        assert "alias2" in command_map
        # All point to same command
        assert command_map["mapped_cmd"] == command_map["alias1"]

    def test_build_help_text_empty(self):
        """Test help text when no commands."""
        help_text = SlackCommandAdapter.build_help_text()
        assert "No commands available" in help_text

    def test_build_help_text_with_commands(self):
        """Test help text with registered commands."""
        register_all_commands()

        help_text = SlackCommandAdapter.build_help_text()

        assert "Piper" in help_text
        assert "/standup" in help_text
        assert "/piper help" in help_text

    def test_build_help_response(self):
        """Test complete help response structure."""
        register_all_commands()

        response = SlackCommandAdapter.build_help_response()

        assert response["response_type"] == "ephemeral"
        assert "text" in response
        assert "Piper" in response["text"]

    def test_build_help_blocks_empty(self):
        """Test help blocks when no commands."""
        blocks = SlackCommandAdapter.build_help_blocks()

        assert len(blocks) == 1
        assert "No commands available" in blocks[0]["text"]["text"]

    def test_build_help_blocks_with_commands(self):
        """Test help blocks with registered commands."""
        register_all_commands()

        blocks = SlackCommandAdapter.build_help_blocks()

        assert len(blocks) > 1
        # Should have header, divider, content sections
        assert blocks[0]["type"] == "section"
        assert "Piper" in blocks[0]["text"]["text"]


class TestSlackAdapterIntegration:
    """Integration tests for Slack adapter with full command set."""

    def test_standup_in_slack_help(self):
        """Test that standup appears in Slack help."""
        register_all_commands()

        help_text = SlackCommandAdapter.build_help_text()

        assert "/standup" in help_text
        assert "standup" in help_text.lower()

    def test_discovery_in_slack_help(self):
        """Test that discovery (from #488) appears in Slack help."""
        register_all_commands()

        help_text = SlackCommandAdapter.build_help_text()

        # Discovery should be available
        assert "Capabilities" in help_text or "Discovery" in help_text

    def test_calendar_in_slack_help(self):
        """Test that calendar appears in Slack help (Issue #551 Phase 4: gap closed)."""
        register_all_commands()

        help_text = SlackCommandAdapter.build_help_text()

        # Issue #551 Phase 4: Calendar gap closed - should be in Slack help
        assert "Today's Calendar" in help_text

    def test_help_categories_organized(self):
        """Test that help is organized by category."""
        register_all_commands()

        help_text = SlackCommandAdapter.build_help_text()

        # Should have category headers
        assert "*" in help_text  # Slack bold markers for categories
