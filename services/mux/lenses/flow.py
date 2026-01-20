"""
FlowLens - Perceives Workflow State and Momentum

The FlowLens views targets through the dimension of workflow:
- What state is this in?
- Is it progressing or stuck?
- What's the momentum?
- What's blocking progress?

Maps to FLOW dimension in spatial infrastructure.

Integration approach (Direct Integration - Option B):
    integration.dimensions["FLOW"](target)

References:
- ADR-038: Spatial Intelligence Patterns (FLOW dimension)
- Slack spatial_types: ConversationalPath.conversation_momentum
"""

from ..perception import Perception, PerceptionMode
from .base import Lens, Target


class FlowLens(Lens):
    """
    Perceives workflow state, progress, and momentum.

    This lens answers flow questions:
    - What state is this in? (todo, in_progress, done)
    - Is work flowing or stuck?
    - What's blocking progress?
    - How much momentum is there?

    Experience framing examples:
    - "This is in progress and moving well"
    - "I notice this has been stuck for 3 days"
    - "Work is flowing smoothly with good momentum"
    """

    name = "flow"

    async def perceive(
        self, target: Target, mode: PerceptionMode = PerceptionMode.NOTICING
    ) -> Perception:
        """
        Perceive workflow aspects of the target.

        Args:
            target: Entity, Moment, or Place to perceive
            mode: Temporal perspective

        Returns:
            Perception with flow observations
        """
        raw_data = await self._get_flow_data(target, mode)
        observation = self._frame_as_experience(raw_data, mode)

        return Perception(
            lens_name=self.name,
            mode=mode,
            raw_data=raw_data,
            observation=observation,
            source="flow_analysis",
        )

    async def _get_flow_data(self, target: Target, mode: PerceptionMode) -> dict:
        """Get raw flow data for target."""
        target_id = getattr(target, "id", "unknown")

        return {
            "target_id": target_id,
            "state": "unknown",  # todo, in_progress, review, done, blocked
            "momentum": "steady",  # stalled, slow, steady, fast, accelerating
            "blockers": [],
            "progress_percentage": None,
            "last_state_change": None,
        }

    def _frame_as_experience(self, raw_data: dict, mode: PerceptionMode) -> str:
        """Transform flow data into experience language."""
        target_id = raw_data.get("target_id", "this item")
        state = raw_data.get("state", "unknown")
        momentum = raw_data.get("momentum", "steady")
        blockers = raw_data.get("blockers", [])

        if mode == PerceptionMode.NOTICING:
            if blockers:
                return f"I notice {target_id} is blocked by {len(blockers)} issues"
            elif state == "done":
                return f"I notice {target_id} has been completed"
            elif momentum == "stalled":
                return f"I notice {target_id} has stalled and needs attention"
            else:
                return f"I notice {target_id} is in {state} state with {momentum} momentum"

        elif mode == PerceptionMode.REMEMBERING:
            return f"I recall the flow history of {target_id}"

        else:  # ANTICIPATING
            return f"I anticipate {target_id} will continue its current trajectory"
