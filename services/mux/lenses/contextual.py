"""
ContextualLens - Perceives Surrounding Context

The ContextualLens views targets through the dimension of context:
- What's the surrounding environment?
- What's the atmosphere?
- What related things are nearby?
- What's the broader situation?

Maps to CONTEXTUAL dimension in spatial infrastructure.

Integration approach (Direct Integration - Option B):
    integration.dimensions["CONTEXTUAL"](target)

References:
- ADR-038: Spatial Intelligence Patterns (CONTEXTUAL dimension)
- Slack spatial_types: Room.get_room_atmosphere()
"""

from ..perception import Perception, PerceptionMode
from .base import Lens, Target


class ContextualLens(Lens):
    """
    Perceives surrounding context and environment.

    This lens answers contextual questions:
    - What's the atmosphere here?
    - What else is happening nearby?
    - What's the broader context?
    - What related items exist?

    Experience framing examples:
    - "The atmosphere here is collaborative and focused"
    - "Related projects include X and Y"
    - "I notice this is part of a larger initiative"
    """

    name = "contextual"

    async def perceive(
        self, target: Target, mode: PerceptionMode = PerceptionMode.NOTICING
    ) -> Perception:
        """
        Perceive contextual aspects of the target.

        Args:
            target: Entity, Moment, or Place to perceive
            mode: Temporal perspective

        Returns:
            Perception with context observations
        """
        raw_data = await self._get_contextual_data(target, mode)
        observation = self._frame_as_experience(raw_data, mode)

        return Perception(
            lens_name=self.name,
            mode=mode,
            raw_data=raw_data,
            observation=observation,
            source="contextual_analysis",
        )

    async def _get_contextual_data(self, target: Target, mode: PerceptionMode) -> dict:
        """Get raw contextual data for target."""
        target_id = getattr(target, "id", "unknown")

        # Check if target has atmosphere attribute (Place protocol)
        atmosphere = getattr(target, "atmosphere", "neutral")

        return {
            "target_id": target_id,
            "atmosphere": atmosphere,
            "related_items": [],
            "tags": [],
            "broader_context": None,
            "environment": "workspace",
        }

    def _frame_as_experience(self, raw_data: dict, mode: PerceptionMode) -> str:
        """Transform contextual data into experience language."""
        target_id = raw_data.get("target_id", "this item")
        atmosphere = raw_data.get("atmosphere", "neutral")
        related = raw_data.get("related_items", [])
        tags = raw_data.get("tags", [])

        if mode == PerceptionMode.NOTICING:
            parts = []
            if atmosphere and atmosphere != "neutral":
                parts.append(f"the atmosphere is {atmosphere}")
            if related:
                parts.append(f"{len(related)} related items nearby")
            if tags:
                parts.append(f"tagged as {', '.join(tags[:3])}")

            if parts:
                return f"I notice for {target_id}: " + ", ".join(parts)
            else:
                return f"I notice {target_id} is in a neutral context"

        elif mode == PerceptionMode.REMEMBERING:
            return f"I recall the contextual environment of {target_id}"

        else:  # ANTICIPATING
            return f"I anticipate the context around {target_id} may evolve"
