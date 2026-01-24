# services/commands/adapters - Interface adapters for CommandRegistry
# Issue #551: ARCH-COMMANDS

from .base import BaseAdapter
from .slack_adapter import SlackCommandAdapter

__all__ = ["BaseAdapter", "SlackCommandAdapter"]
