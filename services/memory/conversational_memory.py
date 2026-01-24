"""
Conversational Memory Service.

Layer 1 of ADR-054 Cross-Session Memory Architecture.
Provides 24-hour memory window for natural continuity references.

Part of #657 MEM-ADR054-P1.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, List, Optional

import structlog

if TYPE_CHECKING:
    from services.repositories.conversational_memory_repository import (
        ConversationalMemoryRepository,
    )

logger = structlog.get_logger(__name__)


# =============================================================================
# Domain Models
# =============================================================================


@dataclass
class ConversationalMemoryEntry:
    """
    A memorable item from recent conversation.

    Captures the essence of what was discussed for natural continuity
    references like "yesterday we discussed...".
    """

    conversation_id: str  # Use str for consistency with ConversationDB.id
    timestamp: datetime
    topic_summary: str  # Brief summary of what was discussed
    entities_mentioned: List[str] = field(default_factory=list)  # Projects, issues, people
    outcome: Optional[str] = None  # What was decided/accomplished
    user_sentiment: Optional[str] = None  # positive/neutral/negative


@dataclass
class ConversationalMemoryWindow:
    """
    24-hour memory window for a user.

    Contains all memorable entries from the last 24 hours,
    enabling natural conversation continuity.
    """

    user_id: str
    entries: List[ConversationalMemoryEntry] = field(default_factory=list)
    window_start: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc) - timedelta(hours=24)
    )
    window_end: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def get_most_recent(self) -> Optional[ConversationalMemoryEntry]:
        """Get most recent conversation in window."""
        return self.entries[0] if self.entries else None

    def get_active_topics(self) -> List[str]:
        """Get topics discussed in window (deduplicated)."""
        return list(set(e.topic_summary for e in self.entries if e.topic_summary))

    def get_active_entities(self) -> List[str]:
        """Get all entities mentioned in window (deduplicated)."""
        entities = []
        for entry in self.entries:
            entities.extend(entry.entities_mentioned)
        return list(set(entities))

    def is_empty(self) -> bool:
        """Check if memory window has no entries."""
        return len(self.entries) == 0


# =============================================================================
# Service
# =============================================================================


class ConversationalMemoryService:
    """
    Manages 24-hour conversational memory (ADR-054 Layer 1).

    Enables natural continuity references like "yesterday we discussed..."
    without being creepy about remembering everything.

    Usage:
        service = ConversationalMemoryService(repository)

        # Record when conversation ends
        await service.record_conversation_end(
            user_id="user-123",
            conversation_id="conv-456",
            summary="Discussed sprint planning",
            entities=["Project Alpha", "Q1 roadmap"],
            outcome="Decided on 3 sprint goals",
        )

        # Get memory window for context
        window = await service.get_memory_window("user-123")
        recent = window.get_most_recent()
        if recent:
            print(f"Last discussed: {recent.topic_summary}")
    """

    WINDOW_HOURS = 24

    def __init__(self, repository: "ConversationalMemoryRepository"):
        self.repository = repository

    async def record_conversation_end(
        self,
        user_id: str,
        conversation_id: str,
        summary: str,
        entities: Optional[List[str]] = None,
        outcome: Optional[str] = None,
        sentiment: Optional[str] = None,
    ) -> None:
        """
        Record conversation summary when session ends.

        This is called when a conversation naturally concludes or times out.
        The summary becomes part of the 24-hour memory window.

        Args:
            user_id: User ID
            conversation_id: Conversation ID
            summary: Brief topic summary (e.g., "Discussed sprint planning")
            entities: Projects, issues, people mentioned
            outcome: What was decided/accomplished
            sentiment: User sentiment (positive/neutral/negative)
        """
        entry = ConversationalMemoryEntry(
            conversation_id=conversation_id,
            timestamp=datetime.now(timezone.utc),
            topic_summary=summary,
            entities_mentioned=entities or [],
            outcome=outcome,
            user_sentiment=sentiment,
        )

        await self.repository.save_entry(user_id, entry)
        await self._prune_old_entries(user_id)

        logger.info(
            "conversation_memory_recorded",
            user_id=user_id,
            conversation_id=conversation_id,
            topic=summary,
            entities_count=len(entities or []),
        )

    async def get_memory_window(self, user_id: str) -> ConversationalMemoryWindow:
        """
        Get 24-hour memory window for user.

        Returns a window containing all memorable entries from the last
        24 hours. Use this to provide context-aware greetings and
        natural conversation continuity.

        Args:
            user_id: User ID

        Returns:
            ConversationalMemoryWindow with recent entries (may be empty)
        """
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(hours=self.WINDOW_HOURS)

        entries = await self.repository.get_entries_since(user_id, window_start)

        return ConversationalMemoryWindow(
            user_id=user_id,
            entries=entries,
            window_start=window_start,
            window_end=now,
        )

    async def _prune_old_entries(self, user_id: str) -> None:
        """Remove entries older than window."""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=self.WINDOW_HOURS)
        deleted = await self.repository.delete_entries_before(user_id, cutoff)

        if deleted > 0:
            logger.debug(
                "conversation_memory_pruned",
                user_id=user_id,
                entries_deleted=deleted,
            )
