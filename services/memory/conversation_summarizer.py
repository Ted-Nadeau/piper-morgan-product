"""
Rule-based conversation summarizer for memory recording.

Part of #664 MEM-ADR054-P4: Memory Integration.

This module provides:
- ConversationSummaryResult: Summary of a conversation
- ConversationSummarizer: Rule-based extraction of topic, entities, sentiment

Per ADR-054 recommendation: Start rule-based, enhance with LLM later.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional, Set

if TYPE_CHECKING:
    from services.domain.models import ConversationTurn


# =============================================================================
# Sentiment Word Lists
# =============================================================================

POSITIVE_SIGNALS = {
    # Gratitude
    "thanks",
    "thank you",
    "appreciate",
    "grateful",
    "helpful",
    # Success
    "great",
    "perfect",
    "excellent",
    "awesome",
    "wonderful",
    "amazing",
    # Completion
    "done",
    "finished",
    "completed",
    "resolved",
    "fixed",
    # Agreement
    "yes",
    "exactly",
    "correct",
    "right",
}

NEGATIVE_SIGNALS = {
    # Frustration
    "frustrated",
    "frustrating",
    "annoying",
    "annoyed",
    "confused",
    "confusing",
    # Problems
    "wrong",
    "broken",
    "doesn't work",
    "not working",
    "failed",
    "error",
    "bug",
    # Disagreement
    "no",
    "incorrect",
    "that's not",
    "that isn't",
}

OUTCOME_COMPLETION_SIGNALS = {
    "done",
    "finished",
    "completed",
    "resolved",
    "fixed",
    "thanks",
    "thank you",
    "that's it",
    "all set",
    "perfect",
}

OUTCOME_PROGRESS_SIGNALS = {
    "continue",
    "next",
    "later",
    "tomorrow",
    "will do",
    "i'll",
    "let me",
}

OUTCOME_BLOCKED_SIGNALS = {
    "blocked",
    "stuck",
    "can't",
    "cannot",
    "won't work",
    "doesn't work",
    "failed",
    "error",
}


# =============================================================================
# Domain Models
# =============================================================================


@dataclass
class ConversationSummaryResult:
    """
    Result of summarizing a conversation.

    Contains extracted topic, entities, outcome, and sentiment
    for recording in conversational memory.
    """

    topic: str
    entities: List[str] = field(default_factory=list)
    outcome: Optional[str] = None  # "completed", "in_progress", "blocked", None
    sentiment: str = "neutral"  # "positive", "neutral", "negative"

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "topic": self.topic,
            "entities": self.entities,
            "outcome": self.outcome,
            "sentiment": self.sentiment,
        }


# =============================================================================
# Summarizer
# =============================================================================


class ConversationSummarizer:
    """
    Rule-based conversation summarizer.

    Extracts meaningful summaries from conversation turns using
    heuristics rather than LLM calls. Fast and deterministic.
    """

    def __init__(
        self,
        max_topic_length: int = 100,
        positive_signals: Optional[Set[str]] = None,
        negative_signals: Optional[Set[str]] = None,
    ):
        """
        Initialize summarizer.

        Args:
            max_topic_length: Maximum characters for topic summary
            positive_signals: Custom positive sentiment words
            negative_signals: Custom negative sentiment words
        """
        self.max_topic_length = max_topic_length
        self.positive_signals = positive_signals or POSITIVE_SIGNALS
        self.negative_signals = negative_signals or NEGATIVE_SIGNALS

    def summarize(self, turns: List["ConversationTurn"]) -> ConversationSummaryResult:
        """
        Extract summary from conversation turns.

        Args:
            turns: List of conversation turns to summarize

        Returns:
            ConversationSummaryResult with topic, entities, outcome, sentiment
        """
        if not turns:
            return ConversationSummaryResult(
                topic="Empty conversation",
                entities=[],
                outcome=None,
                sentiment="neutral",
            )

        topic = self._extract_topic(turns)
        entities = self._extract_entities(turns)
        outcome = self._infer_outcome(turns)
        sentiment = self._detect_sentiment(turns)

        return ConversationSummaryResult(
            topic=topic,
            entities=entities,
            outcome=outcome,
            sentiment=sentiment,
        )

    def _extract_topic(self, turns: List["ConversationTurn"]) -> str:
        """
        Extract topic from conversation.

        Strategy:
        1. Use first meaningful user message
        2. Truncate if too long
        3. Clean up formatting
        """
        for turn in turns:
            message = turn.user_message.strip()
            if message and len(message) > 5:  # Skip trivial messages like "hi"
                # Clean up the message
                topic = self._clean_topic(message)
                return topic

        # Fallback: use intent if available
        for turn in turns:
            if turn.intent:
                return f"Intent: {turn.intent}"

        return "Conversation"

    def _clean_topic(self, message: str) -> str:
        """Clean and truncate a message for use as topic."""
        # Remove markdown formatting
        message = re.sub(r"\*\*|__|\*|_|`", "", message)

        # Remove URLs
        message = re.sub(r"https?://\S+", "[link]", message)

        # Truncate if too long
        if len(message) > self.max_topic_length:
            # Try to break at word boundary
            truncated = message[: self.max_topic_length]
            last_space = truncated.rfind(" ")
            if last_space > self.max_topic_length // 2:
                truncated = truncated[:last_space]
            message = truncated + "..."

        return message

    def _extract_entities(self, turns: List["ConversationTurn"]) -> List[str]:
        """
        Extract entities from all turns.

        Aggregates entities mentioned across all turns,
        deduplicating while preserving order.
        """
        seen: Set[str] = set()
        entities: List[str] = []

        for turn in turns:
            for entity in turn.entities:
                if entity not in seen:
                    seen.add(entity)
                    entities.append(entity)

        return entities

    def _infer_outcome(self, turns: List["ConversationTurn"]) -> Optional[str]:
        """
        Infer outcome from conversation.

        Looks at the last few turns for completion/progress/blocked signals.
        """
        if not turns:
            return None

        # Check last 3 turns (or fewer if conversation is shorter)
        recent_turns = turns[-3:]
        recent_text = " ".join(
            f"{t.user_message} {t.assistant_response}".lower() for t in recent_turns
        )

        # Check for completion first (most positive)
        for signal in OUTCOME_COMPLETION_SIGNALS:
            if signal in recent_text:
                return "completed"

        # Check for blocked (most negative)
        for signal in OUTCOME_BLOCKED_SIGNALS:
            if signal in recent_text:
                return "blocked"

        # Check for progress
        for signal in OUTCOME_PROGRESS_SIGNALS:
            if signal in recent_text:
                return "in_progress"

        return None

    def _detect_sentiment(self, turns: List["ConversationTurn"]) -> str:
        """
        Detect overall sentiment from conversation.

        Uses word lists to count positive/negative signals.
        Returns the dominant sentiment.
        """
        positive_count = 0
        negative_count = 0

        for turn in turns:
            text = f"{turn.user_message} {turn.assistant_response}".lower()

            for signal in self.positive_signals:
                if signal in text:
                    positive_count += 1

            for signal in self.negative_signals:
                if signal in text:
                    negative_count += 1

        # Determine overall sentiment
        if negative_count > positive_count and negative_count >= 2:
            return "negative"
        elif positive_count > negative_count and positive_count >= 2:
            return "positive"
        else:
            return "neutral"
