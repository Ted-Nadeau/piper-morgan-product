"""
Tests for PriorityLens.

Phase 3.3 TDD: PriorityLens perceives importance and urgency.
Maps to PRIORITY dimension in spatial infrastructure.
"""

import pytest

from services.mux.perception import PerceptionMode


class TestPriorityLensBasics:
    """Tests for PriorityLens basic functionality."""

    def test_priority_lens_has_correct_name(self):
        """PriorityLens has name 'priority'."""
        from services.mux.lenses.priority import PriorityLens

        lens = PriorityLens()
        assert lens.name == "priority"

    def test_priority_lens_inherits_from_lens(self):
        """PriorityLens inherits from Lens base class."""
        from services.mux.lenses.base import Lens
        from services.mux.lenses.priority import PriorityLens

        assert issubclass(PriorityLens, Lens)


class TestPriorityLensPerception:
    """Tests for PriorityLens perceive functionality."""

    @pytest.mark.asyncio
    async def test_priority_lens_noticing_mode(self, mock_entity):
        """PriorityLens perceives current importance/urgency."""
        from services.mux.lenses.priority import PriorityLens
        from services.mux.perception import Perception

        lens = PriorityLens()
        perception = await lens.perceive(mock_entity, PerceptionMode.NOTICING)

        assert isinstance(perception, Perception)
        assert perception.lens_name == "priority"
        assert perception.mode == PerceptionMode.NOTICING

    @pytest.mark.asyncio
    async def test_priority_lens_experience_framing(self, mock_entity):
        """PriorityLens observations are experience-framed."""
        from services.mux.lenses.priority import PriorityLens

        lens = PriorityLens()
        perception = await lens.perceive(mock_entity)

        # Should be natural language about importance
        assert len(perception.observation) > 10
