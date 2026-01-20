"""
Tests for CollaborativeLens.

Phase 3.3 TDD: CollaborativeLens perceives who is involved.
Maps to COLLABORATIVE dimension in spatial infrastructure.
"""

import pytest

from services.mux.perception import PerceptionMode


class TestCollaborativeLensBasics:
    """Tests for CollaborativeLens basic functionality."""

    def test_collaborative_lens_has_correct_name(self):
        """CollaborativeLens has name 'collaborative'."""
        from services.mux.lenses.collaborative import CollaborativeLens

        lens = CollaborativeLens()
        assert lens.name == "collaborative"

    def test_collaborative_lens_inherits_from_lens(self):
        """CollaborativeLens inherits from Lens base class."""
        from services.mux.lenses.base import Lens
        from services.mux.lenses.collaborative import CollaborativeLens

        assert issubclass(CollaborativeLens, Lens)


class TestCollaborativeLensPerception:
    """Tests for CollaborativeLens perceive functionality."""

    @pytest.mark.asyncio
    async def test_collaborative_lens_noticing_mode(self, mock_entity):
        """CollaborativeLens perceives current team involvement."""
        from services.mux.lenses.collaborative import CollaborativeLens
        from services.mux.perception import Perception

        lens = CollaborativeLens()
        perception = await lens.perceive(mock_entity, PerceptionMode.NOTICING)

        assert isinstance(perception, Perception)
        assert perception.lens_name == "collaborative"
        assert perception.mode == PerceptionMode.NOTICING

    @pytest.mark.asyncio
    async def test_collaborative_lens_experience_framing(self, mock_entity):
        """CollaborativeLens observations are experience-framed."""
        from services.mux.lenses.collaborative import CollaborativeLens

        lens = CollaborativeLens()
        perception = await lens.perceive(mock_entity)

        # Should be natural language about people/team
        assert len(perception.observation) > 10
