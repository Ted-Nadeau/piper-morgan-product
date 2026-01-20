"""
Lens Base Class - Abstract Base for Perceptual Lenses

Lens is the abstract base class for all perceptual lenses.
Each lens views targets (Entities, Moments, Places) through a specific
dimension (temporal, hierarchy, priority, etc.).

Key design decisions:
1. Lenses are async - they may need to call integrations
2. Lenses produce Perceptions with experience-framed observations
3. Each lens has a name identifying its dimension
4. _frame_as_experience() helper transforms raw data to consciousness-preserving language

Integration approach (from P0 findings):
Lenses call integration-specific methods via the dimensions dict:
    integration.dimensions["TEMPORAL"](target)

References:
- ADR-045: Object Model Specification
- ADR-038: Spatial Intelligence Patterns
- P0 Investigation: Spatial Infrastructure Audit
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

from ..perception import Perception, PerceptionMode

if TYPE_CHECKING:
    from ..protocols import EntityProtocol, MomentProtocol, PlaceProtocol

# Type alias for anything that can be perceived through a lens
Target = Union["EntityProtocol", "MomentProtocol", "PlaceProtocol"]


class Lens(ABC):
    """
    Abstract base class for perceptual lenses.

    A lens is a way of perceiving targets through a specific dimension.
    Each lens:
    - Has a name (e.g., "temporal", "hierarchy")
    - Implements perceive() to view targets
    - Uses _frame_as_experience() to create consciousness-preserving observations

    Subclasses must implement:
    - name: str attribute
    - perceive(): async method that returns Perception

    Example:
        class TemporalLens(Lens):
            name = "temporal"

            async def perceive(self, target, mode=PerceptionMode.NOTICING):
                raw_data = await self._get_temporal_data(target)
                observation = self._frame_as_experience(raw_data, mode)
                return Perception(
                    lens_name=self.name,
                    mode=mode,
                    raw_data=raw_data,
                    observation=observation
                )
    """

    name: str = ""  # Subclasses must set this

    @abstractmethod
    async def perceive(
        self, target: Target, mode: PerceptionMode = PerceptionMode.NOTICING
    ) -> Perception:
        """
        Apply this lens to perceive a target.

        Args:
            target: Entity, Moment, or Place to perceive
            mode: Temporal perspective (NOTICING, REMEMBERING, ANTICIPATING)

        Returns:
            Perception with raw_data and experience-framed observation
        """
        ...

    def _frame_as_experience(self, raw_data: dict, mode: PerceptionMode) -> str:
        """
        Transform raw data into experience language.

        This is the consciousness-preserving transformation. Instead of
        returning "meetings: 3", we return "You have 3 meetings today".

        Subclasses can override for custom framing. Default implementation
        provides basic mode-aware framing.

        Args:
            raw_data: Raw data from integration
            mode: Temporal perspective

        Returns:
            Experience-framed observation string
        """
        # Default implementation - subclasses should override
        data_summary = self._summarize_data(raw_data)

        if mode == PerceptionMode.NOTICING:
            return f"I notice {data_summary}"
        elif mode == PerceptionMode.REMEMBERING:
            return f"I recall {data_summary}"
        elif mode == PerceptionMode.ANTICIPATING:
            return f"I anticipate {data_summary}"
        else:
            return f"Regarding {data_summary}"

    def _summarize_data(self, raw_data: dict) -> str:
        """
        Create a simple summary of raw data.

        Subclasses should override for meaningful summaries.

        Args:
            raw_data: Raw data from integration

        Returns:
            Human-readable summary
        """
        if not raw_data:
            return "no specific data"

        # Simple key-value summary
        items = []
        for key, value in raw_data.items():
            if isinstance(value, (list, tuple)):
                items.append(f"{len(value)} {key}")
            elif isinstance(value, dict):
                items.append(f"{key} details")
            else:
                items.append(f"{key}: {value}")

        if not items:
            return "no specific data"

        return ", ".join(items[:3])  # Limit to 3 items for brevity
