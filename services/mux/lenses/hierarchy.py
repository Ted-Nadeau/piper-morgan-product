"""
HierarchyLens - Perceives Containment Relationships

The HierarchyLens views targets through the dimension of containment:
- What contains this?
- What does this contain?
- Where does this fit in the structure?
- What's the nesting level?

Maps to HIERARCHY dimension in spatial infrastructure.

Integration approach (Direct Integration - Option B):
    integration.dimensions["HIERARCHY"](target)

References:
- ADR-038: Spatial Intelligence Patterns (HIERARCHY dimension)
- Slack spatial_types: Territory -> Room -> Path -> Object hierarchy
"""

from ..perception import Perception, PerceptionMode
from .base import Lens, Target


class HierarchyLens(Lens):
    """
    Perceives containment relationships and structural position.

    This lens answers hierarchy questions:
    - What project does this belong to?
    - What team owns this?
    - What subtasks exist?
    - How deep is this in the structure?

    Experience framing examples:
    - "This task is part of Project Alpha, owned by Team Backend"
    - "This channel contains 3 active threads"
    - "This sits at level 2 in the organization hierarchy"
    """

    name = "hierarchy"

    async def perceive(
        self, target: Target, mode: PerceptionMode = PerceptionMode.NOTICING
    ) -> Perception:
        """
        Perceive hierarchical aspects of the target.

        Args:
            target: Entity, Moment, or Place to perceive
            mode: Temporal perspective

        Returns:
            Perception with hierarchy observations
        """
        raw_data = await self._get_hierarchy_data(target, mode)
        observation = self._frame_as_experience(raw_data, mode)

        return Perception(
            lens_name=self.name,
            mode=mode,
            raw_data=raw_data,
            observation=observation,
            source="hierarchy_analysis",
        )

    async def _get_hierarchy_data(self, target: Target, mode: PerceptionMode) -> dict:
        """Get raw hierarchy data for target."""
        target_id = getattr(target, "id", "unknown")

        return {
            "target_id": target_id,
            "parent": None,
            "children": [],
            "siblings": [],
            "depth": 0,
            "breadcrumb": [target_id],
        }

    def _frame_as_experience(self, raw_data: dict, mode: PerceptionMode) -> str:
        """Transform hierarchy data into experience language."""
        target_id = raw_data.get("target_id", "this item")
        parent = raw_data.get("parent")
        children = raw_data.get("children", [])
        depth = raw_data.get("depth", 0)

        if mode == PerceptionMode.NOTICING:
            parts = []
            if parent:
                parts.append(f"contained within {parent}")
            if children:
                parts.append(f"contains {len(children)} items")
            if depth > 0:
                parts.append(f"at depth {depth}")

            if parts:
                return f"I notice {target_id} is " + ", ".join(parts)
            else:
                return f"I notice {target_id} is at the top level with no children"

        elif mode == PerceptionMode.REMEMBERING:
            return f"I recall the structural position of {target_id} in the hierarchy"

        else:  # ANTICIPATING
            return f"I anticipate {target_id} may gain or change its hierarchical position"
