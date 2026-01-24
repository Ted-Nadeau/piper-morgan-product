"""
Session lifecycle hooks for memory integration.

Part of #664 MEM-ADR054-P4: Memory Integration.

This module provides:
- on_session_end(): Record conversation to memory when session ends
- on_session_timeout(): Handle session timeout (calls on_session_end)

Integrates with:
- #657 ConversationalMemoryService (recording)
- ConversationSummarizer (extraction)
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from services.domain.models import ConversationTurn

from services.memory.conversation_summarizer import (
    ConversationSummarizer,
    ConversationSummaryResult,
)
from services.memory.conversational_memory import ConversationalMemoryService

logger = logging.getLogger(__name__)


# =============================================================================
# Session End Hook
# =============================================================================


async def on_session_end(
    user_id: str,
    conversation_id: str,
    turns: List["ConversationTurn"],
    memory_service: ConversationalMemoryService,
    summarizer: Optional[ConversationSummarizer] = None,
    is_private: bool = False,
) -> Optional[ConversationSummaryResult]:
    """
    Handle session end by recording to memory.

    Called when a conversation naturally concludes or times out.
    Summarizes the conversation and records it to memory for
    future context retrieval.

    Args:
        user_id: User ID for the session
        conversation_id: Unique conversation identifier
        turns: List of conversation turns
        memory_service: Service for recording to memory
        summarizer: Optional custom summarizer (uses default if None)
        is_private: If True, skip recording (private session)

    Returns:
        ConversationSummaryResult if recorded, None if skipped
    """
    if is_private:
        logger.info(
            "session_end_skipped_private",
            extra={
                "user_id": user_id,
                "conversation_id": conversation_id,
                "reason": "private_session",
            },
        )
        return None

    if not turns:
        logger.info(
            "session_end_skipped_empty",
            extra={
                "user_id": user_id,
                "conversation_id": conversation_id,
                "reason": "no_turns",
            },
        )
        return None

    # Summarize conversation
    summarizer = summarizer or ConversationSummarizer()
    summary = summarizer.summarize(turns)

    # Record to memory
    await memory_service.record_conversation_end(
        user_id=user_id,
        conversation_id=conversation_id,
        summary=summary.topic,
        entities=summary.entities,
        outcome=summary.outcome,
        sentiment=summary.sentiment,
    )

    logger.info(
        "session_end_recorded",
        extra={
            "user_id": user_id,
            "conversation_id": conversation_id,
            "topic": summary.topic,
            "entities_count": len(summary.entities),
            "outcome": summary.outcome,
            "sentiment": summary.sentiment,
        },
    )

    return summary


async def on_session_timeout(
    user_id: str,
    conversation_id: str,
    turns: List["ConversationTurn"],
    memory_service: ConversationalMemoryService,
    summarizer: Optional[ConversationSummarizer] = None,
    is_private: bool = False,
) -> Optional[ConversationSummaryResult]:
    """
    Handle session timeout.

    Alias for on_session_end - same behavior but with different
    logging context for observability.

    Args:
        user_id: User ID for the session
        conversation_id: Unique conversation identifier
        turns: List of conversation turns
        memory_service: Service for recording to memory
        summarizer: Optional custom summarizer
        is_private: If True, skip recording

    Returns:
        ConversationSummaryResult if recorded, None if skipped
    """
    logger.info(
        "session_timeout_triggered",
        extra={
            "user_id": user_id,
            "conversation_id": conversation_id,
            "turn_count": len(turns),
        },
    )

    return await on_session_end(
        user_id=user_id,
        conversation_id=conversation_id,
        turns=turns,
        memory_service=memory_service,
        summarizer=summarizer,
        is_private=is_private,
    )
