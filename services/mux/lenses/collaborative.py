"""
CollaborativeLens - Perceives Who Is Involved

The CollaborativeLens views targets through the dimension of collaboration:
- Who is involved?
- Who created/owns this?
- Who needs to be notified?
- What teams are connected?

Maps to COLLABORATIVE dimension in spatial infrastructure.

Integration approach (Direct Integration - Option B):
    integration.dimensions["COLLABORATIVE"](target)

References:
- ADR-038: Spatial Intelligence Patterns (COLLABORATIVE dimension)
- Slack spatial_types: Room.current_inhabitants, active_participants
"""

from ..perception import Perception, PerceptionMode
from .base import Lens, Target


class CollaborativeLens(Lens):
    """
    Perceives people involvement and team dynamics.

    This lens answers collaboration questions:
    - Who is working on this?
    - Who owns this?
    - Who should be notified?
    - Which teams are involved?

    Experience framing examples:
    - "Alice and Bob are actively working on this"
    - "This involves the Backend team and DevOps"
    - "I notice 3 collaborators have contributed recently"
    """

    name = "collaborative"

    async def perceive(
        self, target: Target, mode: PerceptionMode = PerceptionMode.NOTICING
    ) -> Perception:
        """
        Perceive collaborative aspects of the target.

        Args:
            target: Entity, Moment, or Place to perceive
            mode: Temporal perspective

        Returns:
            Perception with collaboration observations
        """
        raw_data = await self._get_collaborative_data(target, mode)
        observation = self._frame_as_experience(raw_data, mode)

        return Perception(
            lens_name=self.name,
            mode=mode,
            raw_data=raw_data,
            observation=observation,
            source="collaborative_analysis",
        )

    async def _get_collaborative_data(self, target: Target, mode: PerceptionMode) -> dict:
        """Get raw collaborative data for target."""
        target_id = getattr(target, "id", "unknown")

        return {
            "target_id": target_id,
            "owner": None,
            "contributors": [],
            "teams": [],
            "mentioned_users": [],
            "active_participants": [],
        }

    def _frame_as_experience(self, raw_data: dict, mode: PerceptionMode) -> str:
        """Transform collaborative data into experience language."""
        target_id = raw_data.get("target_id", "this item")
        owner = raw_data.get("owner")
        contributors = raw_data.get("contributors", [])
        teams = raw_data.get("teams", [])

        if mode == PerceptionMode.NOTICING:
            parts = []
            if owner:
                parts.append(f"owned by {owner}")
            if contributors:
                parts.append(f"{len(contributors)} contributors involved")
            if teams:
                parts.append(f"involves {', '.join(teams)}")

            if parts:
                return f"I notice {target_id} is " + ", ".join(parts)
            else:
                return f"I notice no specific collaborators assigned to {target_id}"

        elif mode == PerceptionMode.REMEMBERING:
            return f"I recall who was involved with {target_id} previously"

        else:  # ANTICIPATING
            return f"I anticipate {target_id} may need additional collaborators"
