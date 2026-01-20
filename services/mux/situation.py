"""
Situation Context Manager - Frame for Holding Sequences of Moments

Situation is a FRAME (not a substrate like Entity/Moment/Place).
It holds sequences of Moments and provides theatrical context:
- Description: What is happening
- Dramatic Tension: Why it matters
- Goals: What we hoped to achieve
- Outcomes: What actually happened
- Learning: The delta between goals and outcomes

Use as an async context manager:

    async with Situation(
        description="Morning standup",
        dramatic_tension="Deadline pressure",
        goals=["Align on priorities", "Surface blockers"]
    ) as standup:
        standup.add_moment(discussion_moment)
        standup.add_moment(decision_moment)
        standup.add_outcome("Agreed to defer feature X")

    learning = standup.extract_learning()

References:
- ADR-045: Object Model Specification
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from .protocols import MomentProtocol


@dataclass
class SituationLearning:
    """
    What was learned when a situation closed.

    Captures the delta between intentions (goals) and reality (outcomes).
    This is where consciousness-preserving reflection happens.
    """

    goals: List[str]
    outcomes: List[str]
    delta: str  # The gap/learning - what we learned from the difference

    def __post_init__(self):
        """Compute delta if not provided."""
        if not self.delta:
            self.delta = self._compute_delta()

    def _compute_delta(self) -> str:
        """Compute the learning delta between goals and outcomes."""
        if not self.goals and not self.outcomes:
            return "No goals or outcomes recorded"

        if not self.outcomes:
            return f"Goals set but no outcomes recorded: {', '.join(self.goals)}"

        if not self.goals:
            return f"Outcomes achieved without explicit goals: {', '.join(self.outcomes)}"

        # Simple delta computation - can be enhanced with LLM later
        goal_count = len(self.goals)
        outcome_count = len(self.outcomes)

        if outcome_count >= goal_count:
            return f"Achieved {outcome_count} outcomes against {goal_count} goals"
        else:
            return f"Partial completion: {outcome_count} outcomes from {goal_count} goals"


@dataclass
class Situation:
    """
    Frame holding sequences of Moments (not a substrate).

    Situation provides theatrical context for a bounded period of activity.
    It captures what happened, why it mattered, and what was learned.

    Use as async context manager to automatically track timing.
    """

    description: str
    dramatic_tension: str
    goals: List[str] = field(default_factory=list)
    moments: List[Any] = field(default_factory=list)  # List[MomentProtocol]
    outcomes: List[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    async def __aenter__(self) -> "Situation":
        """Enter the situation context."""
        self.started_at = datetime.now()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the situation context."""
        self.ended_at = datetime.now()
        # Learning extraction can happen here or explicitly via extract_learning()
        return None  # Don't suppress exceptions

    def add_moment(self, moment: "MomentProtocol") -> None:
        """
        Add a moment to this situation.

        Moments are significant occurrences that happen during the situation.
        They're added in chronological order.

        Args:
            moment: A Moment (or anything satisfying MomentProtocol)
        """
        self.moments.append(moment)

    def add_outcome(self, outcome: str) -> None:
        """
        Record an outcome that occurred during this situation.

        Outcomes are results, decisions, or accomplishments.

        Args:
            outcome: Description of what was achieved/decided
        """
        self.outcomes.append(outcome)

    def extract_learning(self) -> SituationLearning:
        """
        Extract learning from goals vs outcomes delta.

        This is where reflection happens - comparing what we intended
        to achieve with what actually happened.

        Returns:
            SituationLearning with goals, outcomes, and computed delta
        """
        return SituationLearning(
            goals=self.goals.copy(),
            outcomes=self.outcomes.copy(),
            delta="",  # Will be computed in __post_init__
        )

    @property
    def duration(self) -> Optional[float]:
        """Get duration in seconds if situation has ended."""
        if self.started_at and self.ended_at:
            return (self.ended_at - self.started_at).total_seconds()
        return None

    @property
    def is_active(self) -> bool:
        """Check if situation is currently active (entered but not exited)."""
        return self.started_at is not None and self.ended_at is None
