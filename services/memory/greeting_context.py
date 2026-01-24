"""
Greeting context service for context-aware greetings.

Part of #662 MEM-ADR054-P2 (ADR-054 Phase 2: Greeting Context).

This module provides:
- GreetingCondition: Enum of greeting conditions from PDR-002
- GreetingContext: Context for generating appropriate greetings
- GreetingContextService: Determines greeting context from user history

PDR-002 defines context-aware greetings based on user's recent history:
- Same day return: "Back already! We were working on [X]—continue?"
- Next day active: "Yesterday we discussed [X]. Continue, or different focus?"
- Week gap: "It's been a bit! Want to pick up where we left off?"
- Month gap: "Welcome back! Want me to catch you up, or start fresh?"
- Previous negative: "What would you like to work on?" (clean slate)
- First session: Per FTUX flow
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import List, Optional

from services.memory.conversational_memory import (
    ConversationalMemoryEntry,
    ConversationalMemoryService,
)

# =============================================================================
# Greeting Conditions
# =============================================================================


class GreetingCondition(Enum):
    """
    Conditions from PDR-002 greeting table.

    Each condition maps to a different greeting approach,
    balancing continuity with respecting user context.
    """

    SAME_DAY_RECENT = "same_day_recent"  # Back within ~8 hours
    NEXT_DAY_ACTIVE = "next_day_active"  # 8-36 hours, was working on something
    WEEK_GAP = "week_gap"  # 36 hours - 1 week
    MONTH_GAP = "month_gap"  # 1+ week gap
    PREVIOUS_TRIVIAL = "previous_trivial"  # Last session was brief/unimportant
    PREVIOUS_NEGATIVE = "previous_negative"  # Last session ended badly
    FIRST_SESSION = "first_session"  # Brand new user


# =============================================================================
# Greeting Context
# =============================================================================


@dataclass
class GreetingContext:
    """
    Context for generating appropriate greeting.

    Provides all information needed to construct a context-aware
    greeting that respects the user's history and state.
    """

    condition: GreetingCondition
    last_session: Optional[ConversationalMemoryEntry]
    time_since_last: Optional[timedelta]
    suggested_greeting_approach: str
    can_reference_work: bool
    offer_fresh_start: bool

    # For templating - extracted from last session
    topic_reference: Optional[str] = None
    entity_references: List[str] = field(default_factory=list)


# =============================================================================
# Greeting Approach Templates
# =============================================================================

# Suggested approaches from PDR-002
GREETING_APPROACHES = {
    GreetingCondition.SAME_DAY_RECENT: ("Back already! We were working on {topic}—continue?"),
    GreetingCondition.NEXT_DAY_ACTIVE: (
        "Yesterday we discussed {topic}. Continue, or different focus?"
    ),
    GreetingCondition.WEEK_GAP: ("It's been a bit! Want to pick up where we left off?"),
    GreetingCondition.MONTH_GAP: ("Welcome back! Want me to catch you up, or start fresh?"),
    GreetingCondition.PREVIOUS_TRIVIAL: ("Hey! What would you like to work on?"),
    GreetingCondition.PREVIOUS_NEGATIVE: ("What would you like to work on?"),
    GreetingCondition.FIRST_SESSION: (
        "Welcome! I'm Piper, your AI assistant. What can I help you with?"
    ),
}


# =============================================================================
# Greeting Context Service
# =============================================================================


class GreetingContextService:
    """
    Generates greeting context based on user history.

    Uses ConversationalMemoryService to analyze the user's
    recent sessions and determine the appropriate greeting approach.
    """

    # Time thresholds in hours
    SAME_DAY_HOURS = 8
    NEXT_DAY_HOURS = 36
    WEEK_HOURS = 168  # 7 * 24
    MONTH_HOURS = 720  # 30 * 24

    def __init__(self, memory_service: ConversationalMemoryService):
        """
        Initialize with memory service.

        Args:
            memory_service: Service for accessing user's conversational memory
        """
        self.memory_service = memory_service

    async def get_greeting_context(self, user_id: str) -> GreetingContext:
        """
        Determine appropriate greeting context for user.

        Args:
            user_id: The user to get greeting context for

        Returns:
            GreetingContext with condition, flags, and templating data
        """
        memory_window = await self.memory_service.get_memory_window(user_id)
        last_entry = memory_window.get_most_recent()

        condition = self._determine_condition(last_entry)
        time_since = self._time_since(last_entry)

        return GreetingContext(
            condition=condition,
            last_session=last_entry,
            time_since_last=time_since,
            suggested_greeting_approach=self._get_suggested_approach(condition),
            can_reference_work=self._can_reference_work(condition),
            offer_fresh_start=self._should_offer_fresh_start(condition),
            topic_reference=last_entry.topic_summary if last_entry else None,
            entity_references=list(last_entry.entities_mentioned) if last_entry else [],
        )

    def _determine_condition(
        self, last_entry: Optional[ConversationalMemoryEntry]
    ) -> GreetingCondition:
        """
        Determine greeting condition from last session.

        Priority order:
        1. First session (no history)
        2. Previous negative sentiment (clean slate regardless of time)
        3. Time-based conditions
        """
        if not last_entry:
            return GreetingCondition.FIRST_SESSION

        # Negative sentiment always triggers clean slate
        if last_entry.user_sentiment == "negative":
            return GreetingCondition.PREVIOUS_NEGATIVE

        # Check for trivial session (no meaningful topic)
        if self._is_trivial_session(last_entry):
            return GreetingCondition.PREVIOUS_TRIVIAL

        # Time-based conditions
        hours_since = self._hours_since(last_entry)

        if hours_since < self.SAME_DAY_HOURS:
            return GreetingCondition.SAME_DAY_RECENT
        elif hours_since < self.NEXT_DAY_HOURS:
            return GreetingCondition.NEXT_DAY_ACTIVE
        elif hours_since < self.WEEK_HOURS:
            return GreetingCondition.WEEK_GAP
        else:
            return GreetingCondition.MONTH_GAP

    def _is_trivial_session(self, entry: ConversationalMemoryEntry) -> bool:
        """
        Check if session was trivial/unimportant.

        A trivial session has:
        - Very short/empty topic summary
        - No entities mentioned
        - No outcome recorded
        """
        has_short_topic = len(entry.topic_summary.strip()) < 10
        has_no_entities = len(entry.entities_mentioned) == 0
        has_no_outcome = entry.outcome is None or len(entry.outcome.strip()) == 0

        return has_short_topic and has_no_entities and has_no_outcome

    def _hours_since(self, entry: ConversationalMemoryEntry) -> float:
        """Calculate hours since entry timestamp."""
        now = datetime.now(timezone.utc)
        delta = now - entry.timestamp
        return delta.total_seconds() / 3600

    def _time_since(self, entry: Optional[ConversationalMemoryEntry]) -> Optional[timedelta]:
        """Calculate timedelta since entry, or None if no entry."""
        if not entry:
            return None
        return datetime.now(timezone.utc) - entry.timestamp

    def _get_suggested_approach(self, condition: GreetingCondition) -> str:
        """Get the suggested greeting approach template for a condition."""
        return GREETING_APPROACHES.get(
            condition,
            "Hello! What can I help you with?",
        )

    def _can_reference_work(self, condition: GreetingCondition) -> bool:
        """
        Check if we can reference previous work in greeting.

        Only appropriate for recent sessions where the work
        is still fresh in the user's mind.
        """
        return condition in (
            GreetingCondition.SAME_DAY_RECENT,
            GreetingCondition.NEXT_DAY_ACTIVE,
        )

    def _should_offer_fresh_start(self, condition: GreetingCondition) -> bool:
        """
        Check if we should offer a fresh start.

        Appropriate when there's been a significant gap or
        the previous session was negative.
        """
        return condition in (
            GreetingCondition.WEEK_GAP,
            GreetingCondition.MONTH_GAP,
            GreetingCondition.PREVIOUS_NEGATIVE,
        )
