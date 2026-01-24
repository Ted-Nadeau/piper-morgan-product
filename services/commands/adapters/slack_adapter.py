"""
Slack adapter for CommandRegistry.

Issue #551: ARCH-COMMANDS
ADR-057: CommandRegistry

Translates CommandRegistry commands to Slack-specific formats.
"""

from typing import Any, Dict, List

from ..registry import CommandDefinition, CommandInterface, CommandRegistry
from .base import BaseAdapter


class SlackCommandAdapter(BaseAdapter):
    """Adapter for Slack slash commands."""

    interface = CommandInterface.SLACK

    @classmethod
    def format_command(cls, command: CommandDefinition) -> Dict[str, Any]:
        """Format a command for Slack display."""
        config = command.get_interface_config(CommandInterface.SLACK)
        return {
            "name": command.name,
            "display_name": command.display_name,
            "description": (
                config.description_override
                if config and config.description_override
                else command.description
            ),
            "response_type": config.slack_response_type if config else "ephemeral",
            "aliases": config.aliases if config else [],
        }

    @classmethod
    def get_command_map(cls) -> Dict[str, CommandDefinition]:
        """Get a mapping of slash command triggers to command definitions."""
        commands = cls.get_commands()
        command_map = {}

        for cmd in commands:
            # Add primary command
            command_map[cmd.name] = cmd

            # Add aliases
            config = cmd.get_interface_config(CommandInterface.SLACK)
            if config and config.aliases:
                for alias in config.aliases:
                    command_map[alias] = cmd

        return command_map

    @classmethod
    def build_help_blocks(cls) -> List[Dict[str, Any]]:
        """
        Build Slack Block Kit blocks for help display.

        Returns formatted blocks for rich Slack display.
        """
        commands = cls.get_commands()

        if not commands:
            return [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "No commands available."},
                }
            ]

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hi! I'm Piper, your PM assistant. Here's what I can help with:",
                },
            },
            {"type": "divider"},
        ]

        # Group by category
        by_category: Dict[str, List[CommandDefinition]] = {}
        for cmd in commands:
            cat_name = cmd.category.value.title()
            if cat_name not in by_category:
                by_category[cat_name] = []
            by_category[cat_name].append(cmd)

        # Build sections per category
        for category, cmds in sorted(by_category.items()):
            cmd_lines = []
            for cmd in cmds:
                config = cmd.get_interface_config(CommandInterface.SLACK)
                desc = (
                    config.description_override
                    if config and config.description_override
                    else cmd.description
                )
                # Show slash command format if available
                if cmd.name == "standup":
                    cmd_lines.append(f"• `/standup` - {desc}")
                elif cmd.name == "help":
                    cmd_lines.append(f"• `/piper help` - {desc}")
                else:
                    cmd_lines.append(f"• *{cmd.display_name}* - {desc}")

            if cmd_lines:
                blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{category}*\n" + "\n".join(cmd_lines),
                        },
                    }
                )

        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\nJust message me anything about your projects - I'm here to help!",
                },
            }
        )

        return blocks

    @classmethod
    def build_help_text(cls) -> str:
        """
        Build plain text help for Slack.

        Used when blocks aren't supported or for simpler display.
        """
        commands = cls.get_commands()

        if not commands:
            return "No commands available."

        lines = ["Hi! I'm Piper, your PM assistant. Here's how I can help:\n"]

        # Quick commands first
        lines.append("*Quick Commands*")
        for cmd in commands:
            if cmd.name == "standup":
                lines.append("• `/standup` - I'll help you prep for standup")
            elif cmd.name == "help":
                lines.append("• `/piper help` - Show this message")

        lines.append("")

        # Group remaining by category
        by_category: Dict[str, List[CommandDefinition]] = {}
        for cmd in commands:
            if cmd.name in ("standup", "help"):
                continue  # Already shown
            cat_name = cmd.category.value.title()
            if cat_name not in by_category:
                by_category[cat_name] = []
            by_category[cat_name].append(cmd)

        for category, cmds in sorted(by_category.items()):
            lines.append(f"*{category}*")
            for cmd in cmds:
                config = cmd.get_interface_config(CommandInterface.SLACK)
                desc = (
                    config.description_override
                    if config and config.description_override
                    else cmd.description
                )
                lines.append(f"• {cmd.display_name} - {desc}")
            lines.append("")

        lines.append("Just ask me anything about your projects - I'm here to help!")

        return "\n".join(lines)

    @classmethod
    def build_help_response(cls) -> Dict[str, Any]:
        """
        Build complete Slack help response.

        Returns dict ready for Slack API response.
        """
        return {
            "response_type": "ephemeral",
            "text": cls.build_help_text(),
            # Could also include blocks for richer display:
            # "blocks": cls.build_help_blocks(),
        }
