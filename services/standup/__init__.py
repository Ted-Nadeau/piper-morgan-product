"""
Issue #552, #553: Standup conversation management package.

Provides:
- StandupConversationManager: State machine for conversations
- InvalidStateTransitionError: Exception for invalid transitions
- StandupConversationHandler: Multi-turn conversation flow handler
- ConversationResponse: Response dataclass for handler output
"""

from services.standup.conversation_handler import ConversationResponse, StandupConversationHandler
from services.standup.conversation_manager import (
    InvalidStateTransitionError,
    StandupConversationManager,
)

__all__ = [
    "StandupConversationManager",
    "InvalidStateTransitionError",
    "StandupConversationHandler",
    "ConversationResponse",
]
