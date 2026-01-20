"""
PriorityLens - Perceives Importance and Urgency

The PriorityLens views targets through the dimension of priority:
- How important is this?
- How urgent is this?
- What's the priority level?
- What needs attention first?

Maps to PRIORITY dimension in spatial infrastructure.

Integration approach (Direct Integration - Option B):
    integration.dimensions["PRIORITY"](target)

References:
- ADR-038: Spatial Intelligence Patterns (PRIORITY dimension)
- Slack spatial_types: AttentionLevel enum (AMBIENT to EMERGENCY)
"""

from ..perception import Perception, PerceptionMode
from .base import Lens, Target


class PriorityLens(Lens):
    """
    Perceives importance, urgency, and attention requirements.

    This lens answers priority questions:
    - How important is this?
    - How urgent is this?
    - What needs attention now?
    - What can wait?

    Experience framing examples:
    - "This requires urgent attention - deadline today"
    - "This is important but not time-sensitive"
    - "I notice 2 high-priority items need your focus"
    """

    name = "priority"

    async def perceive(
        self, target: Target, mode: PerceptionMode = PerceptionMode.NOTICING
    ) -> Perception:
        """
        Perceive priority aspects of the target.

        Args:
            target: Entity, Moment, or Place to perceive
            mode: Temporal perspective

        Returns:
            Perception with priority observations
        """
        raw_data = await self._get_priority_data(target, mode)
        observation = self._frame_as_experience(raw_data, mode)

        return Perception(
            lens_name=self.name,
            mode=mode,
            raw_data=raw_data,
            observation=observation,
            source="priority_analysis",
        )

    async def _get_priority_data(self, target: Target, mode: PerceptionMode) -> dict:
        """Get raw priority data for target."""
        target_id = getattr(target, "id", "unknown")

        return {
            "target_id": target_id,
            "importance": "normal",  # low, normal, high, critical
            "urgency": "normal",  # low, normal, high, immediate
            "attention_level": "ambient",  # ambient, focused, direct, urgent, emergency
            "priority_score": 50,  # 0-100 scale
            "labels": [],
        }

    def _frame_as_experience(self, raw_data: dict, mode: PerceptionMode) -> str:
        """Transform priority data into experience language."""
        target_id = raw_data.get("target_id", "this item")
        importance = raw_data.get("importance", "normal")
        urgency = raw_data.get("urgency", "normal")
        attention = raw_data.get("attention_level", "ambient")

        if mode == PerceptionMode.NOTICING:
            if urgency in ["high", "immediate"] or attention in ["urgent", "emergency"]:
                return f"I notice {target_id} requires urgent attention"
            elif importance == "high":
                return f"I notice {target_id} is marked as high importance"
            else:
                return f"I notice {target_id} has normal priority levels"

        elif mode == PerceptionMode.REMEMBERING:
            return f"I recall the priority status of {target_id} from before"

        else:  # ANTICIPATING
            return f"I anticipate {target_id} may need priority reassessment"
