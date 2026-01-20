"""
Tests for TemporalLens.

Phase 3.3 TDD: TemporalLens perceives when things happen, sequences, deadlines.
Maps to TEMPORAL dimension in spatial infrastructure.
"""

import pytest

from services.mux.perception import PerceptionMode


class TestTemporalLensBasics:
    """Tests for TemporalLens basic functionality."""

    def test_temporal_lens_has_correct_name(self):
        """TemporalLens has name 'temporal'."""
        from services.mux.lenses.temporal import TemporalLens

        lens = TemporalLens()
        assert lens.name == "temporal"

    def test_temporal_lens_inherits_from_lens(self):
        """TemporalLens inherits from Lens base class."""
        from services.mux.lenses.base import Lens
        from services.mux.lenses.temporal import TemporalLens

        assert issubclass(TemporalLens, Lens)


class TestTemporalLensPerception:
    """Tests for TemporalLens perceive functionality."""

    @pytest.mark.asyncio
    async def test_temporal_lens_noticing_mode(self, mock_entity):
        """TemporalLens perceives current temporal context."""
        from services.mux.lenses.temporal import TemporalLens
        from services.mux.perception import Perception

        lens = TemporalLens()
        perception = await lens.perceive(mock_entity, PerceptionMode.NOTICING)

        assert isinstance(perception, Perception)
        assert perception.lens_name == "temporal"
        assert perception.mode == PerceptionMode.NOTICING

    @pytest.mark.asyncio
    async def test_temporal_lens_remembering_mode(self, mock_entity):
        """TemporalLens can recall past temporal context."""
        from services.mux.lenses.temporal import TemporalLens

        lens = TemporalLens()
        perception = await lens.perceive(mock_entity, PerceptionMode.REMEMBERING)

        assert perception.mode == PerceptionMode.REMEMBERING
        # Observation should reflect past tense
        assert any(
            word in perception.observation.lower()
            for word in ["recall", "was", "had", "yesterday", "past"]
        )

    @pytest.mark.asyncio
    async def test_temporal_lens_anticipating_mode(self, mock_entity):
        """TemporalLens can anticipate future temporal context."""
        from services.mux.lenses.temporal import TemporalLens

        lens = TemporalLens()
        perception = await lens.perceive(mock_entity, PerceptionMode.ANTICIPATING)

        assert perception.mode == PerceptionMode.ANTICIPATING
        # Observation should reflect future tense
        assert any(
            word in perception.observation.lower()
            for word in ["anticipate", "will", "upcoming", "tomorrow", "future"]
        )

    @pytest.mark.asyncio
    async def test_temporal_lens_experience_framing(self, mock_entity):
        """TemporalLens observations are experience-framed."""
        from services.mux.lenses.temporal import TemporalLens

        lens = TemporalLens()
        perception = await lens.perceive(mock_entity)

        # Should be natural language, not data dump
        assert len(perception.observation) > 10
        # Should not look like raw JSON
        assert "{" not in perception.observation[:20]
