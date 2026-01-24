"""
Privacy mode management for conversations.

Part of #664 MEM-ADR054-P4: Memory Integration.

This module provides:
- PrivacyState: Current privacy state for a session
- PrivacyModeService: Manages privacy mode for conversations

Privacy modes:
- Session-level: Current session won't be remembered
- Retroactive: Mark already-recorded conversation as private

Integrates with:
- #663 UserHistoryService (mark_private, unmark_private)
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

from services.memory.user_history import UserHistoryService

logger = logging.getLogger(__name__)


# =============================================================================
# Domain Models
# =============================================================================


class PrivacyReason(Enum):
    """Reason for privacy mode."""

    USER_REQUEST = "user_request"  # User explicitly requested
    SENSITIVE_TOPIC = "sensitive_topic"  # Auto-detected sensitive content
    CLIENT_CONFIDENTIAL = "client_confidential"  # Client-related confidentiality
    PERSONAL = "personal"  # Personal matter


@dataclass
class PrivacyState:
    """
    Current privacy state for a session.

    Tracks whether a session is private and why.
    """

    is_private: bool
    reason: Optional[PrivacyReason] = None

    @classmethod
    def public(cls) -> "PrivacyState":
        """Create a public (non-private) state."""
        return cls(is_private=False, reason=None)

    @classmethod
    def private(cls, reason: PrivacyReason = PrivacyReason.USER_REQUEST) -> "PrivacyState":
        """Create a private state."""
        return cls(is_private=True, reason=reason)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "is_private": self.is_private,
            "reason": self.reason.value if self.reason else None,
        }


# =============================================================================
# Privacy Mode Service
# =============================================================================


class PrivacyModeService:
    """
    Manages privacy mode for conversations.

    Provides two types of privacy:
    1. Session-level: Mark current session as private (won't be remembered)
    2. Retroactive: Mark already-recorded conversation as private

    Privacy state is tracked in-memory for the current session and
    persisted via UserHistoryService for retroactive privacy.
    """

    def __init__(self, history_service: Optional[UserHistoryService] = None):
        """
        Initialize privacy mode service.

        Args:
            history_service: Optional service for retroactive privacy.
                            If None, retroactive operations will fail gracefully.
        """
        self.history_service = history_service
        self._session_privacy: Dict[str, PrivacyState] = {}

    def start_private_session(
        self,
        conversation_id: str,
        reason: PrivacyReason = PrivacyReason.USER_REQUEST,
    ) -> PrivacyState:
        """
        Mark current session as private.

        The session won't be recorded to memory when it ends.

        Args:
            conversation_id: Session/conversation to mark private
            reason: Why the session is private

        Returns:
            PrivacyState for the session
        """
        state = PrivacyState.private(reason)
        self._session_privacy[conversation_id] = state

        logger.info(
            "private_session_started",
            extra={
                "conversation_id": conversation_id,
                "reason": reason.value,
            },
        )

        return state

    def end_private_session(self, conversation_id: str) -> PrivacyState:
        """
        End private mode for a session.

        Future turns will be eligible for memory recording.
        Note: This does NOT retroactively make private turns public.

        Args:
            conversation_id: Session to end privacy for

        Returns:
            New PrivacyState (public)
        """
        state = PrivacyState.public()
        self._session_privacy[conversation_id] = state

        logger.info(
            "private_session_ended",
            extra={"conversation_id": conversation_id},
        )

        return state

    def get_privacy_state(self, conversation_id: str) -> PrivacyState:
        """
        Get current privacy state for a session.

        Args:
            conversation_id: Session to check

        Returns:
            PrivacyState (defaults to public if not set)
        """
        return self._session_privacy.get(conversation_id, PrivacyState.public())

    def is_private(self, conversation_id: str) -> bool:
        """
        Check if session is currently private.

        Args:
            conversation_id: Session to check

        Returns:
            True if private, False otherwise
        """
        return self.get_privacy_state(conversation_id).is_private

    async def retroactively_mark_private(
        self,
        user_id: str,
        conversation_id: str,
    ) -> bool:
        """
        Mark already-recorded conversation as private.

        This excludes the conversation from:
        - Memory/learning
        - Search results
        - History (unless explicitly requested)

        Args:
            user_id: User who owns the conversation
            conversation_id: Conversation to mark private

        Returns:
            True if successful, False if failed or no history service
        """
        if not self.history_service:
            logger.warning(
                "retroactive_privacy_unavailable",
                extra={
                    "conversation_id": conversation_id,
                    "reason": "no_history_service",
                },
            )
            return False

        result = await self.history_service.mark_private(user_id, conversation_id)

        if result:
            logger.info(
                "conversation_marked_private",
                extra={
                    "user_id": user_id,
                    "conversation_id": conversation_id,
                },
            )
        else:
            logger.warning(
                "conversation_privacy_failed",
                extra={
                    "user_id": user_id,
                    "conversation_id": conversation_id,
                },
            )

        return result

    async def retroactively_unmark_private(
        self,
        user_id: str,
        conversation_id: str,
    ) -> bool:
        """
        Remove private flag from a conversation.

        Args:
            user_id: User who owns the conversation
            conversation_id: Conversation to unmark

        Returns:
            True if successful, False if failed or no history service
        """
        if not self.history_service:
            return False

        result = await self.history_service.unmark_private(user_id, conversation_id)

        if result:
            logger.info(
                "conversation_unmarked_private",
                extra={
                    "user_id": user_id,
                    "conversation_id": conversation_id,
                },
            )

        return result

    def clear_session_state(self, conversation_id: str) -> None:
        """
        Clear in-memory privacy state for a session.

        Called when session ends to clean up memory.

        Args:
            conversation_id: Session to clear
        """
        if conversation_id in self._session_privacy:
            del self._session_privacy[conversation_id]
