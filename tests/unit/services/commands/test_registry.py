"""
Tests for CommandRegistry.

Issue #551: ARCH-COMMANDS
ADR-057: CommandRegistry
"""

import pytest

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


class TestCommandDefinition:
    """Test CommandDefinition dataclass."""

    def test_create_command_definition(self):
        """Test basic command definition creation."""
        cmd = CommandDefinition(
            name="test_command",
            display_name="Test Command",
            description="A test command",
            category=CommandCategory.STANDUP,
        )
        assert cmd.name == "test_command"
        assert cmd.display_name == "Test Command"
        assert cmd.category == CommandCategory.STANDUP

    def test_is_available_on_with_all_interface(self):
        """Test command with ALL interface is available everywhere."""
        cmd = CommandDefinition(
            name="universal",
            display_name="Universal",
            description="Available everywhere",
            category=CommandCategory.HELP,
            interfaces={CommandInterface.ALL: InterfaceConfig(enabled=True)},
        )
        assert cmd.is_available_on(CommandInterface.CLI) is True
        assert cmd.is_available_on(CommandInterface.SLACK) is True
        assert cmd.is_available_on(CommandInterface.WEB_CHAT) is True
        assert cmd.is_available_on(CommandInterface.URL) is True

    def test_is_available_on_specific_interfaces(self):
        """Test command with specific interfaces."""
        cmd = CommandDefinition(
            name="web_only",
            display_name="Web Only",
            description="Only on web",
            category=CommandCategory.CALENDAR,
            interfaces={
                CommandInterface.WEB_CHAT: InterfaceConfig(enabled=True),
                CommandInterface.SLACK: InterfaceConfig(enabled=False),
            },
        )
        assert cmd.is_available_on(CommandInterface.WEB_CHAT) is True
        assert cmd.is_available_on(CommandInterface.SLACK) is False
        assert cmd.is_available_on(CommandInterface.CLI) is False

    def test_get_interface_config(self):
        """Test getting interface-specific configuration."""
        cmd = CommandDefinition(
            name="configured",
            display_name="Configured",
            description="Has config",
            category=CommandCategory.STANDUP,
            interfaces={
                CommandInterface.SLACK: InterfaceConfig(
                    enabled=True,
                    slack_response_type="in_channel",
                    aliases=["daily"],
                )
            },
        )
        config = cmd.get_interface_config(CommandInterface.SLACK)
        assert config is not None
        assert config.slack_response_type == "in_channel"
        assert "daily" in config.aliases

    def test_get_interface_config_with_all(self):
        """Test that ALL config is returned for any interface."""
        cmd = CommandDefinition(
            name="universal",
            display_name="Universal",
            description="Uses ALL",
            category=CommandCategory.HELP,
            interfaces={
                CommandInterface.ALL: InterfaceConfig(
                    enabled=True,
                    description_override="Universal help",
                )
            },
        )
        config = cmd.get_interface_config(CommandInterface.CLI)
        assert config is not None
        assert config.description_override == "Universal help"


class TestCommandRegistry:
    """Test CommandRegistry class methods."""

    def test_register_command(self):
        """Test registering a command."""
        cmd = CommandDefinition(
            name="register_test",
            display_name="Register Test",
            description="Testing registration",
            category=CommandCategory.STANDUP,
            interfaces={CommandInterface.CLI: InterfaceConfig(enabled=True)},
        )
        CommandRegistry.register(cmd)

        assert CommandRegistry.get_command("register_test") is not None
        assert CommandRegistry.get_command_count() == 1

    def test_unregister_command(self):
        """Test unregistering a command."""
        cmd = CommandDefinition(
            name="unregister_test",
            display_name="Unregister Test",
            description="Testing unregistration",
            category=CommandCategory.STANDUP,
        )
        CommandRegistry.register(cmd)
        assert CommandRegistry.get_command_count() == 1

        result = CommandRegistry.unregister("unregister_test")
        assert result is True
        assert CommandRegistry.get_command("unregister_test") is None
        assert CommandRegistry.get_command_count() == 0

    def test_unregister_nonexistent(self):
        """Test unregistering a command that doesn't exist."""
        result = CommandRegistry.unregister("nonexistent")
        assert result is False

    def test_list_commands_all(self):
        """Test listing all commands."""
        cmd1 = CommandDefinition(
            name="cmd1",
            display_name="Command 1",
            description="First",
            category=CommandCategory.STANDUP,
        )
        cmd2 = CommandDefinition(
            name="cmd2",
            display_name="Command 2",
            description="Second",
            category=CommandCategory.CALENDAR,
        )
        CommandRegistry.register(cmd1)
        CommandRegistry.register(cmd2)

        commands = CommandRegistry.list_commands()
        assert len(commands) == 2

    def test_list_commands_by_interface(self):
        """Test listing commands filtered by interface."""
        cmd1 = CommandDefinition(
            name="slack_cmd",
            display_name="Slack Command",
            description="Slack only",
            category=CommandCategory.STANDUP,
            interfaces={CommandInterface.SLACK: InterfaceConfig(enabled=True)},
        )
        cmd2 = CommandDefinition(
            name="cli_cmd",
            display_name="CLI Command",
            description="CLI only",
            category=CommandCategory.STANDUP,
            interfaces={CommandInterface.CLI: InterfaceConfig(enabled=True)},
        )
        CommandRegistry.register(cmd1)
        CommandRegistry.register(cmd2)

        slack_commands = CommandRegistry.list_commands(interface=CommandInterface.SLACK)
        assert len(slack_commands) == 1
        assert slack_commands[0].name == "slack_cmd"

    def test_list_commands_by_category(self):
        """Test listing commands filtered by category."""
        cmd1 = CommandDefinition(
            name="standup_cmd",
            display_name="Standup",
            description="Standup",
            category=CommandCategory.STANDUP,
        )
        cmd2 = CommandDefinition(
            name="calendar_cmd",
            display_name="Calendar",
            description="Calendar",
            category=CommandCategory.CALENDAR,
        )
        CommandRegistry.register(cmd1)
        CommandRegistry.register(cmd2)

        standup_commands = CommandRegistry.list_commands(category=CommandCategory.STANDUP)
        assert len(standup_commands) == 1
        assert standup_commands[0].name == "standup_cmd"

    def test_get_help(self):
        """Test help text generation."""
        cmd = CommandDefinition(
            name="help_test",
            display_name="Help Test",
            description="Testing help generation",
            category=CommandCategory.STANDUP,
            interfaces={CommandInterface.SLACK: InterfaceConfig(enabled=True)},
        )
        CommandRegistry.register(cmd)

        help_text = CommandRegistry.get_help(CommandInterface.SLACK)
        assert "Available Commands" in help_text
        assert "Help Test" in help_text
        assert "Testing help generation" in help_text

    def test_get_help_empty(self):
        """Test help text when no commands available."""
        help_text = CommandRegistry.get_help(CommandInterface.SLACK)
        assert "No commands available" in help_text

    def test_find_by_keyword(self):
        """Test finding commands by keyword."""
        cmd = CommandDefinition(
            name="standup",
            display_name="Daily Standup",
            description="Generate standup",
            category=CommandCategory.STANDUP,
            keywords=["standup", "daily", "morning"],
        )
        CommandRegistry.register(cmd)

        # Find by name
        matches = CommandRegistry.find_by_keyword("standup")
        assert len(matches) == 1

        # Find by keyword
        matches = CommandRegistry.find_by_keyword("morning")
        assert len(matches) == 1

        # Find by display name
        matches = CommandRegistry.find_by_keyword("daily")
        assert len(matches) == 1

        # No match
        matches = CommandRegistry.find_by_keyword("nonexistent")
        assert len(matches) == 0

    def test_get_categories(self):
        """Test getting categories with commands."""
        cmd1 = CommandDefinition(
            name="cmd1",
            display_name="Cmd1",
            description="First",
            category=CommandCategory.STANDUP,
        )
        cmd2 = CommandDefinition(
            name="cmd2",
            display_name="Cmd2",
            description="Second",
            category=CommandCategory.CALENDAR,
        )
        CommandRegistry.register(cmd1)
        CommandRegistry.register(cmd2)

        categories = CommandRegistry.get_categories()
        assert CommandCategory.STANDUP in categories
        assert CommandCategory.CALENDAR in categories
        assert len(categories) == 2

    def test_initialized_flag(self):
        """Test initialization tracking."""
        assert CommandRegistry.is_initialized() is False

        CommandRegistry.mark_initialized()
        assert CommandRegistry.is_initialized() is True

        CommandRegistry.clear()
        assert CommandRegistry.is_initialized() is False


class TestInterfaceConfig:
    """Test InterfaceConfig dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = InterfaceConfig()
        assert config.enabled is True
        assert config.requires_auth is True
        assert config.slack_response_type == "ephemeral"
        assert config.url_method == "GET"
        assert config.aliases == []

    def test_custom_values(self):
        """Test custom configuration values."""
        config = InterfaceConfig(
            enabled=True,
            aliases=["alias1", "alias2"],
            slack_response_type="in_channel",
            requires_auth=False,
        )
        assert config.aliases == ["alias1", "alias2"]
        assert config.slack_response_type == "in_channel"
        assert config.requires_auth is False


class TestCommandCategory:
    """Test CommandCategory enum."""

    def test_all_categories_exist(self):
        """Test that expected categories exist."""
        assert CommandCategory.CALENDAR.value == "calendar"
        assert CommandCategory.STANDUP.value == "standup"
        assert CommandCategory.TODOS.value == "todos"
        assert CommandCategory.HELP.value == "help"
        assert CommandCategory.DISCOVERY.value == "discovery"
        assert CommandCategory.IDENTITY.value == "identity"


class TestCommandInterface:
    """Test CommandInterface enum."""

    def test_all_interfaces_exist(self):
        """Test that expected interfaces exist."""
        assert CommandInterface.CLI.value == "cli"
        assert CommandInterface.WEB_CHAT.value == "web_chat"
        assert CommandInterface.SLACK.value == "slack"
        assert CommandInterface.URL.value == "url"
        assert CommandInterface.ALL.value == "all"
