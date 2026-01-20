"""
Tests for CausalLens.

Phase 3.3 TDD: CausalLens perceives cause and effect relationships.
Maps to CAUSAL dimension in spatial infrastructure.
"""

import pytest

from services.mux.perception import PerceptionMode


class TestCausalLensBasics:
    """Tests for CausalLens basic functionality."""

    def test_causal_lens_has_correct_name(self):
        """CausalLens has name 'causal'."""
        from services.mux.lenses.causal import CausalLens

        lens = CausalLens()
        assert lens.name == "causal"

    def test_causal_lens_inherits_from_lens(self):
        """CausalLens inherits from Lens base class."""
        from services.mux.lenses.base import Lens
        from services.mux.lenses.causal import CausalLens

        assert issubclass(CausalLens, Lens)


class TestCausalLensPerception:
    """Tests for CausalLens perceive functionality."""

    @pytest.mark.asyncio
    async def test_causal_lens_noticing_mode(self, mock_entity):
        """CausalLens perceives current causal relationships."""
        from services.mux.lenses.causal import CausalLens
        from services.mux.perception import Perception

        lens = CausalLens()
        perception = await lens.perceive(mock_entity, PerceptionMode.NOTICING)

        assert isinstance(perception, Perception)
        assert perception.lens_name == "causal"
        assert perception.mode == PerceptionMode.NOTICING

    @pytest.mark.asyncio
    async def test_causal_lens_experience_framing(self, mock_entity):
        """CausalLens observations are experience-framed."""
        from services.mux.lenses.causal import CausalLens

        lens = CausalLens()
        perception = await lens.perceive(mock_entity)

        # Should be natural language about cause/effect
        assert len(perception.observation) > 10
