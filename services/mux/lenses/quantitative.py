"""
QuantitativeLens - Perceives How Much/Many

The QuantitativeLens views targets through the dimension of quantity:
- How many items?
- What are the metrics?
- What are the counts?
- What are the sizes?

Maps to QUANTITATIVE dimension in spatial infrastructure.

Integration approach (Direct Integration - Option B):
    integration.dimensions["QUANTITATIVE"](target)

References:
- ADR-038: Spatial Intelligence Patterns (QUANTITATIVE dimension)
- Calendar integration: total_meetings_today, total_meeting_time_minutes
"""

from ..perception import Perception, PerceptionMode
from .base import Lens, Target


class QuantitativeLens(Lens):
    """
    Perceives quantities, metrics, and measurements.

    This lens answers quantitative questions:
    - How many tasks are there?
    - What's the completion percentage?
    - How many people involved?
    - What's the size/scope?

    Experience framing examples:
    - "You have 5 tasks, 2 completed"
    - "60% of the sprint is done"
    - "I notice 3 items need review"
    """

    name = "quantitative"

    async def perceive(
        self, target: Target, mode: PerceptionMode = PerceptionMode.NOTICING
    ) -> Perception:
        """
        Perceive quantitative aspects of the target.

        Args:
            target: Entity, Moment, or Place to perceive
            mode: Temporal perspective

        Returns:
            Perception with quantitative observations
        """
        raw_data = await self._get_quantitative_data(target, mode)
        observation = self._frame_as_experience(raw_data, mode)

        return Perception(
            lens_name=self.name,
            mode=mode,
            raw_data=raw_data,
            observation=observation,
            source="quantitative_analysis",
        )

    async def _get_quantitative_data(self, target: Target, mode: PerceptionMode) -> dict:
        """Get raw quantitative data for target."""
        target_id = getattr(target, "id", "unknown")

        return {
            "target_id": target_id,
            "count": 0,
            "total": 0,
            "completed": 0,
            "percentage": None,
            "metrics": {},
        }

    def _frame_as_experience(self, raw_data: dict, mode: PerceptionMode) -> str:
        """Transform quantitative data into experience language."""
        target_id = raw_data.get("target_id", "this item")
        count = raw_data.get("count", 0)
        total = raw_data.get("total", 0)
        completed = raw_data.get("completed", 0)
        percentage = raw_data.get("percentage")

        if mode == PerceptionMode.NOTICING:
            if total > 0 and completed > 0:
                pct = percentage or (completed / total * 100)
                return f"I notice {completed} of {total} completed ({pct:.0f}%) for {target_id}"
            elif count > 0:
                return f"I notice {count} items associated with {target_id}"
            else:
                return f"I notice no quantitative data available for {target_id}"

        elif mode == PerceptionMode.REMEMBERING:
            return f"I recall the previous metrics for {target_id}"

        else:  # ANTICIPATING
            return f"I anticipate the metrics for {target_id} will evolve"
