"""
Tests for QuantitativeLens.

Phase 3.3 TDD: QuantitativeLens perceives how much/many.
Maps to QUANTITATIVE dimension in spatial infrastructure.
"""

import pytest

from services.mux.perception import PerceptionMode


class TestQuantitativeLensBasics:
    """Tests for QuantitativeLens basic functionality."""

    def test_quantitative_lens_has_correct_name(self):
        """QuantitativeLens has name 'quantitative'."""
        from services.mux.lenses.quantitative import QuantitativeLens

        lens = QuantitativeLens()
        assert lens.name == "quantitative"

    def test_quantitative_lens_inherits_from_lens(self):
        """QuantitativeLens inherits from Lens base class."""
        from services.mux.lenses.base import Lens
        from services.mux.lenses.quantitative import QuantitativeLens

        assert issubclass(QuantitativeLens, Lens)


class TestQuantitativeLensPerception:
    """Tests for QuantitativeLens perceive functionality."""

    @pytest.mark.asyncio
    async def test_quantitative_lens_noticing_mode(self, mock_entity):
        """QuantitativeLens perceives current metrics."""
        from services.mux.lenses.quantitative import QuantitativeLens
        from services.mux.perception import Perception

        lens = QuantitativeLens()
        perception = await lens.perceive(mock_entity, PerceptionMode.NOTICING)

        assert isinstance(perception, Perception)
        assert perception.lens_name == "quantitative"
        assert perception.mode == PerceptionMode.NOTICING

    @pytest.mark.asyncio
    async def test_quantitative_lens_experience_framing(self, mock_entity):
        """QuantitativeLens observations are experience-framed."""
        from services.mux.lenses.quantitative import QuantitativeLens

        lens = QuantitativeLens()
        perception = await lens.perceive(mock_entity)

        # Should be natural language about quantities
        assert len(perception.observation) > 10
