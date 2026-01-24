"""
CommandRegistry - Central registry for all Piper commands.

Issue #551: ARCH-COMMANDS - Command Parity Across Interfaces
ADR-057: CommandRegistry - Unified Command Discovery and Routing

This module provides:
- CommandDefinition: Dataclass defining a command across all interfaces
- InterfaceConfig: Per-interface configuration for a command
- CommandRegistry: Central registry for command lookup and discovery
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class CommandInterface(Enum):
    """Interfaces where a command can be exposed."""

    CLI = "cli"
    WEB_CHAT = "web_chat"
    SLACK = "slack"
    URL = "url"
    ALL = "all"  # Exposed on all interfaces


class CommandCategory(Enum):
    """Functional categories for command organization."""

    CALENDAR = "calendar"
    TODOS = "todos"
    PROJECTS = "projects"
    GITHUB = "github"
    STANDUP = "standup"
    SETTINGS = "settings"
    HELP = "help"
    ADMIN = "admin"
    IDENTITY = "identity"
    DISCOVERY = "discovery"
    STATUS = "status"
    PRIORITY = "priority"


@dataclass
class InterfaceConfig:
    """Configuration for a specific interface."""

    enabled: bool = True
    aliases: List[str] = field(default_factory=list)
    description_override: Optional[str] = None
    requires_auth: bool = True

    # Interface-specific options
    slack_response_type: str = "ephemeral"  # or "in_channel"
    cli_group: Optional[str] = None  # Click group name
    url_method: str = "GET"  # HTTP method
    url_path: Optional[str] = None  # Route path override


@dataclass
class CommandDefinition:
    """Central definition of a command across all interfaces."""

    # Identity
    name: str  # Canonical name (e.g., "calendar_today")
    display_name: str  # Human-readable (e.g., "Today's Calendar")
    description: str  # What it does
    category: CommandCategory

    # Interface Exposure
    interfaces: Dict[CommandInterface, InterfaceConfig] = field(default_factory=dict)

    # Handler Reference (existing handlers continue to work)
    handler_module: str = ""  # e.g., "services.intent_service.canonical_handlers"
    handler_name: str = ""  # e.g., "_handle_temporal_query"

    # Discovery Metadata
    examples: List[str] = field(default_factory=list)  # Example invocations
    keywords: List[str] = field(default_factory=list)  # Search terms
    help_text: Optional[str] = None  # Detailed help

    # Execution Metadata
    requires_integration: Optional[str] = None  # e.g., "calendar", "github"
    execution_type: str = "query"  # "query", "mutation", "action"

    def is_available_on(self, interface: CommandInterface) -> bool:
        """Check if command is available on given interface."""
        if CommandInterface.ALL in self.interfaces:
            return self.interfaces[CommandInterface.ALL].enabled
        return interface in self.interfaces and self.interfaces[interface].enabled

    def get_interface_config(self, interface: CommandInterface) -> Optional[InterfaceConfig]:
        """Get configuration for specific interface."""
        if CommandInterface.ALL in self.interfaces:
            return self.interfaces[CommandInterface.ALL]
        return self.interfaces.get(interface)


class CommandRegistry:
    """Central registry for all Piper commands."""

    _commands: Dict[str, CommandDefinition] = {}
    _by_category: Dict[CommandCategory, List[str]] = {}
    _by_interface: Dict[CommandInterface, List[str]] = {}
    _initialized: bool = False

    @classmethod
    def register(cls, command: CommandDefinition) -> None:
        """Register a command definition."""
        cls._commands[command.name] = command

        # Index by category
        if command.category not in cls._by_category:
            cls._by_category[command.category] = []
        if command.name not in cls._by_category[command.category]:
            cls._by_category[command.category].append(command.name)

        # Index by interface
        for interface in command.interfaces:
            if interface not in cls._by_interface:
                cls._by_interface[interface] = []
            if command.name not in cls._by_interface[interface]:
                cls._by_interface[interface].append(command.name)

        logger.debug(f"Registered command: {command.name}")

    @classmethod
    def unregister(cls, name: str) -> bool:
        """Unregister a command by name."""
        if name not in cls._commands:
            return False

        command = cls._commands[name]

        # Remove from category index
        if command.category in cls._by_category:
            if name in cls._by_category[command.category]:
                cls._by_category[command.category].remove(name)

        # Remove from interface index
        for interface in command.interfaces:
            if interface in cls._by_interface:
                if name in cls._by_interface[interface]:
                    cls._by_interface[interface].remove(name)

        del cls._commands[name]
        logger.debug(f"Unregistered command: {name}")
        return True

    @classmethod
    def get_command(cls, name: str) -> Optional[CommandDefinition]:
        """Get a command by canonical name."""
        return cls._commands.get(name)

    @classmethod
    def list_commands(
        cls,
        interface: Optional[CommandInterface] = None,
        category: Optional[CommandCategory] = None,
    ) -> List[CommandDefinition]:
        """List commands, optionally filtered."""
        commands = list(cls._commands.values())

        if interface:
            commands = [c for c in commands if c.is_available_on(interface)]
        if category:
            commands = [c for c in commands if c.category == category]

        return commands

    @classmethod
    def get_help(cls, interface: CommandInterface) -> str:
        """Generate help text for an interface."""
        commands = cls.list_commands(interface=interface)

        if not commands:
            return "No commands available."

        # Group by category
        by_category: Dict[CommandCategory, List[CommandDefinition]] = {}
        for cmd in commands:
            if cmd.category not in by_category:
                by_category[cmd.category] = []
            by_category[cmd.category].append(cmd)

        # Format help
        lines = ["**Available Commands**\n"]
        for category, cmds in sorted(by_category.items(), key=lambda x: x[0].value):
            lines.append(f"\n**{category.value.title()}**")
            for cmd in cmds:
                config = cmd.get_interface_config(interface)
                desc = (
                    config.description_override
                    if config and config.description_override
                    else cmd.description
                )
                lines.append(f"  • {cmd.display_name}: {desc}")

        return "\n".join(lines)

    @classmethod
    def find_by_keyword(
        cls, keyword: str, interface: Optional[CommandInterface] = None
    ) -> List[CommandDefinition]:
        """Find commands matching a keyword."""
        keyword_lower = keyword.lower()
        matches = []

        for cmd in cls.list_commands(interface=interface):
            if (
                keyword_lower in cmd.name.lower()
                or keyword_lower in cmd.display_name.lower()
                or any(keyword_lower in kw.lower() for kw in cmd.keywords)
            ):
                matches.append(cmd)

        return matches

    @classmethod
    def get_command_count(cls) -> int:
        """Get total number of registered commands."""
        return len(cls._commands)

    @classmethod
    def get_categories(cls) -> List[CommandCategory]:
        """Get all categories that have commands."""
        return list(cls._by_category.keys())

    @classmethod
    def clear(cls) -> None:
        """Clear all registered commands. Useful for testing."""
        cls._commands.clear()
        cls._by_category.clear()
        cls._by_interface.clear()
        cls._initialized = False

    @classmethod
    def is_initialized(cls) -> bool:
        """Check if registry has been initialized with commands."""
        return cls._initialized

    @classmethod
    def mark_initialized(cls) -> None:
        """Mark registry as initialized."""
        cls._initialized = True
