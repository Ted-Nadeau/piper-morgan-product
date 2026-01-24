"""
Base adapter interface for CommandRegistry.

Issue #551: ARCH-COMMANDS
ADR-057: CommandRegistry

Interface adapters translate CommandRegistry commands to interface-specific formats.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..registry import CommandDefinition, CommandInterface, CommandRegistry


class BaseAdapter(ABC):
    """Base class for interface adapters."""

    interface: CommandInterface

    @classmethod
    def get_commands(cls) -> List[CommandDefinition]:
        """Get all commands available on this interface."""
        return CommandRegistry.list_commands(interface=cls.interface)

    @classmethod
    def get_help(cls) -> str:
        """Get help text for this interface."""
        return CommandRegistry.get_help(cls.interface)

    @classmethod
    @abstractmethod
    def format_command(cls, command: CommandDefinition) -> Dict[str, Any]:
        """Format a command for this interface."""
        pass

    @classmethod
    @abstractmethod
    def get_command_map(cls) -> Dict[str, Any]:
        """Get a mapping of command triggers to handlers for this interface."""
        pass
