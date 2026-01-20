"""
CausalLens - Perceives Cause and Effect Relationships

The CausalLens views targets through the dimension of causality:
- What caused this?
- What will this affect?
- What depends on this?
- What does this depend on?

Maps to CAUSAL dimension in spatial infrastructure.

Integration approach (Direct Integration - Option B):
    integration.dimensions["CAUSAL"](target)

References:
- ADR-038: Spatial Intelligence Patterns (CAUSAL dimension)
- GitHub spatial: analyze_dependencies
"""

from ..perception import Perception, PerceptionMode
from .base import Lens, Target


class CausalLens(Lens):
    """
    Perceives cause-effect relationships and dependencies.

    This lens answers causal questions:
    - What caused this?
    - What will this affect?
    - What depends on this?
    - What blocks this?

    Experience framing examples:
    - "This is blocked by 2 upstream tasks"
    - "Completing this will unblock 3 downstream items"
    - "I notice a dependency chain of 5 items"
    """

    name = "causal"

    async def perceive(
        self, target: Target, mode: PerceptionMode = PerceptionMode.NOTICING
    ) -> Perception:
        """
        Perceive causal aspects of the target.

        Args:
            target: Entity, Moment, or Place to perceive
            mode: Temporal perspective

        Returns:
            Perception with causal observations
        """
        raw_data = await self._get_causal_data(target, mode)
        observation = self._frame_as_experience(raw_data, mode)

        return Perception(
            lens_name=self.name,
            mode=mode,
            raw_data=raw_data,
            observation=observation,
            source="causal_analysis",
        )

    async def _get_causal_data(self, target: Target, mode: PerceptionMode) -> dict:
        """Get raw causal data for target."""
        target_id = getattr(target, "id", "unknown")

        return {
            "target_id": target_id,
            "caused_by": [],  # Upstream causes
            "causes": [],  # Downstream effects
            "depends_on": [],  # Dependencies
            "depended_by": [],  # Dependents
            "blocking": [],  # What this blocks
            "blocked_by": [],  # What blocks this
        }

    def _frame_as_experience(self, raw_data: dict, mode: PerceptionMode) -> str:
        """Transform causal data into experience language."""
        target_id = raw_data.get("target_id", "this item")
        depends_on = raw_data.get("depends_on", [])
        depended_by = raw_data.get("depended_by", [])
        blocked_by = raw_data.get("blocked_by", [])

        if mode == PerceptionMode.NOTICING:
            parts = []
            if blocked_by:
                parts.append(f"blocked by {len(blocked_by)} items")
            if depends_on:
                parts.append(f"depends on {len(depends_on)} items")
            if depended_by:
                parts.append(f"has {len(depended_by)} items depending on it")

            if parts:
                return f"I notice {target_id} " + ", ".join(parts)
            else:
                return f"I notice no causal relationships for {target_id}"

        elif mode == PerceptionMode.REMEMBERING:
            return f"I recall the causal history of {target_id}"

        else:  # ANTICIPATING
            if depended_by:
                return f"I anticipate completing {target_id} will unblock {len(depended_by)} items"
            else:
                return f"I anticipate {target_id} will have downstream effects"
