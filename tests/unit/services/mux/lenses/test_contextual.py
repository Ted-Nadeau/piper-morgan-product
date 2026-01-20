"""
Tests for ContextualLens.

Phase 3.3 TDD: ContextualLens perceives surrounding context.
Maps to CONTEXTUAL dimension in spatial infrastructure.
"""

import pytest

from services.mux.perception import PerceptionMode


class TestContextualLensBasics:
    """Tests for ContextualLens basic functionality."""

    def test_contextual_lens_has_correct_name(self):
        """ContextualLens has name 'contextual'."""
        from services.mux.lenses.contextual import ContextualLens

        lens = ContextualLens()
        assert lens.name == "contextual"

    def test_contextual_lens_inherits_from_lens(self):
        """ContextualLens inherits from Lens base class."""
        from services.mux.lenses.base import Lens
        from services.mux.lenses.contextual import ContextualLens

        assert issubclass(ContextualLens, Lens)


class TestContextualLensPerception:
    """Tests for ContextualLens perceive functionality."""

    @pytest.mark.asyncio
    async def test_contextual_lens_noticing_mode(self, mock_entity):
        """ContextualLens perceives current surrounding context."""
        from services.mux.lenses.contextual import ContextualLens
        from services.mux.perception import Perception

        lens = ContextualLens()
        perception = await lens.perceive(mock_entity, PerceptionMode.NOTICING)

        assert isinstance(perception, Perception)
        assert perception.lens_name == "contextual"
        assert perception.mode == PerceptionMode.NOTICING

    @pytest.mark.asyncio
    async def test_contextual_lens_experience_framing(self, mock_entity):
        """ContextualLens observations are experience-framed."""
        from services.mux.lenses.contextual import ContextualLens

        lens = ContextualLens()
        perception = await lens.perceive(mock_entity)

        # Should be natural language about context/environment
        assert len(perception.observation) > 10
