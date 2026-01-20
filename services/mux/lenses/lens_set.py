"""
LensSet - Apply Multiple Lenses for Compound Perception

LensSet enables viewing targets through multiple dimensions simultaneously.
This creates a richer, multi-faceted perception that combines insights
from different lenses.

Example use:
    lens_set = LensSet([TemporalLens(), PriorityLens(), CollaborativeLens()])

    perceptions = await lens_set.perceive_through(
        ["temporal", "priority"],
        target,
        mode=PerceptionMode.NOTICING
    )

    synthesis = lens_set.synthesize(perceptions)
    # "Based on temporal and priority observations: ..."

References:
- ADR-045: Object Model Specification
- Morning Standup: Multi-dimensional analysis patterns
"""

from typing import Dict, List, Optional

from ..perception import Perception, PerceptionMode
from .base import Lens, Target


class LensSet:
    """
    Apply multiple lenses for compound perception.

    LensSet manages a collection of lenses and provides:
    - Perceiving through multiple lenses at once
    - Retrieving specific lenses by name
    - Synthesizing multiple perceptions into coherent observations

    This enables the rich, multi-dimensional perception that
    the MUX-VISION object model is designed for.
    """

    def __init__(self, lenses: List[Lens]):
        """
        Create a LensSet from a list of lenses.

        Args:
            lenses: List of Lens instances to include
        """
        self.lenses: Dict[str, Lens] = {lens.name: lens for lens in lenses}

    def get_lens(self, name: str) -> Optional[Lens]:
        """
        Get a specific lens by name.

        Args:
            name: Name of the lens (e.g., "temporal", "priority")

        Returns:
            The Lens if found, None otherwise
        """
        return self.lenses.get(name)

    async def perceive_through(
        self, lens_names: List[str], target: Target, mode: PerceptionMode = PerceptionMode.NOTICING
    ) -> List[Perception]:
        """
        Apply multiple lenses to build compound perception.

        Args:
            lens_names: Names of lenses to use
            target: Entity, Moment, or Place to perceive
            mode: Temporal perspective for all perceptions

        Returns:
            List of Perceptions from each requested lens
        """
        perceptions = []

        for name in lens_names:
            if name in self.lenses:
                lens = self.lenses[name]
                perception = await lens.perceive(target, mode)
                perceptions.append(perception)

        return perceptions

    def synthesize(self, perceptions: List[Perception]) -> str:
        """
        Combine multiple perceptions into coherent observation.

        This creates a unified narrative from multiple lens observations.

        Args:
            perceptions: List of Perceptions to synthesize

        Returns:
            Synthesized observation string
        """
        if not perceptions:
            return "No perceptions to synthesize."

        if len(perceptions) == 1:
            return perceptions[0].observation

        # Build synthesis from observations
        lens_names = [p.lens_name for p in perceptions]

        # Combine observations
        observations = [p.observation for p in perceptions]

        # Create synthesized summary
        synthesis_parts = [f"Looking through {len(perceptions)} lenses ({', '.join(lens_names)}):"]

        for perception in perceptions:
            # Clean up observation for synthesis (remove "I notice" prefix if present)
            obs = perception.observation
            if obs.startswith("I notice "):
                obs = obs[9:]
            elif obs.startswith("I recall "):
                obs = obs[9:]
            elif obs.startswith("I anticipate "):
                obs = obs[13:]

            synthesis_parts.append(f"  - {perception.lens_name.capitalize()}: {obs}")

        return "\n".join(synthesis_parts)

    @property
    def available_lenses(self) -> List[str]:
        """Get list of available lens names."""
        return list(self.lenses.keys())

    def __len__(self) -> int:
        """Return number of lenses in set."""
        return len(self.lenses)

    def __contains__(self, lens_name: str) -> bool:
        """Check if lens is in set."""
        return lens_name in self.lenses
