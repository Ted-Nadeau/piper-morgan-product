"""
TemporalLens - Perceives When Things Happen

The TemporalLens views targets through the dimension of time:
- When did this happen?
- What's the sequence?
- What are the deadlines?
- What's the rhythm/cadence?

Maps to TEMPORAL dimension in spatial infrastructure.

Integration approach (Direct Integration - Option B):
    integration.dimensions["TEMPORAL"](target)

References:
- ADR-038: Spatial Intelligence Patterns (TEMPORAL dimension)
- Morning Standup: Calendar temporal data patterns
"""

from typing import Any

from ..perception import Perception, PerceptionMode
from .base import Lens, Target


class TemporalLens(Lens):
    """
    Perceives when things happen, sequences, and deadlines.

    This lens answers temporal questions:
    - When is this due?
    - What happened before/after?
    - What's the timeline?
    - What's the cadence/rhythm?

    Experience framing examples:
    - NOTICING: "You have 3 meetings today, starting at 10am"
    - REMEMBERING: "Yesterday was quieter with only 1 meeting"
    - ANTICIPATING: "Tomorrow looks busy with back-to-back calls"
    """

    name = "temporal"

    async def perceive(
        self, target: Target, mode: PerceptionMode = PerceptionMode.NOTICING
    ) -> Perception:
        """
        Perceive temporal aspects of the target.

        Args:
            target: Entity, Moment, or Place to perceive
            mode: Temporal perspective (now, past, future)

        Returns:
            Perception with temporal observations
        """
        # Get raw temporal data
        raw_data = await self._get_temporal_data(target, mode)

        # Frame as experience
        observation = self._frame_as_experience(raw_data, mode)

        return Perception(
            lens_name=self.name,
            mode=mode,
            raw_data=raw_data,
            observation=observation,
            source="temporal_analysis",
        )

    async def _get_temporal_data(self, target: Target, mode: PerceptionMode) -> dict:
        """
        Get raw temporal data for target.

        In future, this will call integration.dimensions["TEMPORAL"](target).
        For now, provides mock data structure.
        """
        target_id = getattr(target, "id", "unknown")

        if mode == PerceptionMode.NOTICING:
            return {
                "target_id": target_id,
                "current_time": "now",
                "upcoming_events": [],
                "deadlines": [],
                "last_activity": None,
            }
        elif mode == PerceptionMode.REMEMBERING:
            return {
                "target_id": target_id,
                "past_events": [],
                "completed_at": None,
                "duration": None,
            }
        else:  # ANTICIPATING
            return {
                "target_id": target_id,
                "scheduled_events": [],
                "projected_deadline": None,
                "estimated_duration": None,
            }

    def _frame_as_experience(self, raw_data: dict, mode: PerceptionMode) -> str:
        """
        Transform temporal data into experience language.
        """
        target_id = raw_data.get("target_id", "this item")

        if mode == PerceptionMode.NOTICING:
            events = raw_data.get("upcoming_events", [])
            deadlines = raw_data.get("deadlines", [])

            if events:
                return f"I notice {len(events)} upcoming events for {target_id}"
            elif deadlines:
                return f"I notice deadlines approaching for {target_id}"
            else:
                return f"I notice no immediate temporal pressures for {target_id}"

        elif mode == PerceptionMode.REMEMBERING:
            past_events = raw_data.get("past_events", [])
            completed_at = raw_data.get("completed_at")

            if completed_at:
                return f"I recall {target_id} was completed at {completed_at}"
            elif past_events:
                return f"I recall {len(past_events)} past events for {target_id}"
            else:
                return f"I recall no significant past temporal events for {target_id}"

        else:  # ANTICIPATING
            scheduled = raw_data.get("scheduled_events", [])
            deadline = raw_data.get("projected_deadline")

            if deadline:
                return f"I anticipate {target_id} will be due by {deadline}"
            elif scheduled:
                return f"I anticipate {len(scheduled)} future events for {target_id}"
            else:
                return f"I anticipate no scheduled temporal events for {target_id}"
