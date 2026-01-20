"""
Tests for LensSet - Compound Perception from Multiple Lenses.

Phase 3.4 TDD: LensSet applies multiple lenses to build compound perception.
This enables viewing targets through multiple dimensions simultaneously.
"""

import pytest

from services.mux.perception import PerceptionMode


class TestLensSetBasics:
    """Tests for LensSet basic functionality."""

    def test_lens_set_can_be_created_with_lenses(self):
        """LensSet can be created with a list of lenses."""
        from services.mux.lenses.lens_set import LensSet
        from services.mux.lenses.priority import PriorityLens
        from services.mux.lenses.temporal import TemporalLens

        lens_set = LensSet([TemporalLens(), PriorityLens()])

        assert len(lens_set.lenses) == 2

    def test_lens_set_indexes_by_name(self):
        """LensSet indexes lenses by their name."""
        from services.mux.lenses.hierarchy import HierarchyLens
        from services.mux.lenses.lens_set import LensSet
        from services.mux.lenses.temporal import TemporalLens

        lens_set = LensSet([TemporalLens(), HierarchyLens()])

        assert "temporal" in lens_set.lenses
        assert "hierarchy" in lens_set.lenses

    def test_lens_set_can_get_lens_by_name(self):
        """LensSet can retrieve lens by name."""
        from services.mux.lenses.lens_set import LensSet
        from services.mux.lenses.temporal import TemporalLens

        lens_set = LensSet([TemporalLens()])
        temporal = lens_set.get_lens("temporal")

        assert temporal is not None
        assert temporal.name == "temporal"


class TestLensSetPerception:
    """Tests for LensSet perceive_through functionality."""

    @pytest.mark.asyncio
    async def test_perceive_through_single_lens(self, mock_entity):
        """LensSet can perceive through a single lens."""
        from services.mux.lenses.lens_set import LensSet
        from services.mux.lenses.temporal import TemporalLens

        lens_set = LensSet([TemporalLens()])
        perceptions = await lens_set.perceive_through(["temporal"], mock_entity)

        assert len(perceptions) == 1
        assert perceptions[0].lens_name == "temporal"

    @pytest.mark.asyncio
    async def test_perceive_through_multiple_lenses(self, mock_entity):
        """LensSet can perceive through multiple lenses."""
        from services.mux.lenses.collaborative import CollaborativeLens
        from services.mux.lenses.lens_set import LensSet
        from services.mux.lenses.priority import PriorityLens
        from services.mux.lenses.temporal import TemporalLens

        lens_set = LensSet([TemporalLens(), PriorityLens(), CollaborativeLens()])
        perceptions = await lens_set.perceive_through(
            ["temporal", "priority", "collaborative"], mock_entity
        )

        assert len(perceptions) == 3
        lens_names = [p.lens_name for p in perceptions]
        assert "temporal" in lens_names
        assert "priority" in lens_names
        assert "collaborative" in lens_names

    @pytest.mark.asyncio
    async def test_perceive_through_respects_mode(self, mock_entity):
        """LensSet passes mode to all lenses."""
        from services.mux.lenses.lens_set import LensSet
        from services.mux.lenses.priority import PriorityLens
        from services.mux.lenses.temporal import TemporalLens

        lens_set = LensSet([TemporalLens(), PriorityLens()])
        perceptions = await lens_set.perceive_through(
            ["temporal", "priority"], mock_entity, mode=PerceptionMode.REMEMBERING
        )

        assert all(p.mode == PerceptionMode.REMEMBERING for p in perceptions)

    @pytest.mark.asyncio
    async def test_perceive_through_skips_missing_lens(self, mock_entity):
        """LensSet skips lens names that don't exist."""
        from services.mux.lenses.lens_set import LensSet
        from services.mux.lenses.temporal import TemporalLens

        lens_set = LensSet([TemporalLens()])
        perceptions = await lens_set.perceive_through(["temporal", "nonexistent"], mock_entity)

        assert len(perceptions) == 1
        assert perceptions[0].lens_name == "temporal"


class TestLensSetSynthesis:
    """Tests for LensSet synthesize functionality."""

    @pytest.mark.asyncio
    async def test_synthesize_combines_perceptions(self, mock_entity):
        """LensSet can synthesize multiple perceptions."""
        from services.mux.lenses.lens_set import LensSet
        from services.mux.lenses.priority import PriorityLens
        from services.mux.lenses.temporal import TemporalLens

        lens_set = LensSet([TemporalLens(), PriorityLens()])
        perceptions = await lens_set.perceive_through(["temporal", "priority"], mock_entity)

        synthesis = lens_set.synthesize(perceptions)

        assert isinstance(synthesis, str)
        assert len(synthesis) > 0

    @pytest.mark.asyncio
    async def test_synthesize_mentions_each_lens(self, mock_entity):
        """Synthesis mentions each contributing lens."""
        from services.mux.lenses.hierarchy import HierarchyLens
        from services.mux.lenses.lens_set import LensSet
        from services.mux.lenses.temporal import TemporalLens

        lens_set = LensSet([TemporalLens(), HierarchyLens()])
        perceptions = await lens_set.perceive_through(["temporal", "hierarchy"], mock_entity)

        synthesis = lens_set.synthesize(perceptions)

        # Synthesis should reference the observations
        assert len(synthesis) > 10


class TestLensSetAllLenses:
    """Tests for LensSet with all 8 lenses."""

    @pytest.mark.asyncio
    async def test_full_lens_set_perceive_all(self, mock_entity):
        """LensSet can perceive through all 8 lenses."""
        from services.mux.lenses.causal import CausalLens
        from services.mux.lenses.collaborative import CollaborativeLens
        from services.mux.lenses.contextual import ContextualLens
        from services.mux.lenses.flow import FlowLens
        from services.mux.lenses.hierarchy import HierarchyLens
        from services.mux.lenses.lens_set import LensSet
        from services.mux.lenses.priority import PriorityLens
        from services.mux.lenses.quantitative import QuantitativeLens
        from services.mux.lenses.temporal import TemporalLens

        all_lenses = [
            TemporalLens(),
            HierarchyLens(),
            PriorityLens(),
            CollaborativeLens(),
            FlowLens(),
            QuantitativeLens(),
            CausalLens(),
            ContextualLens(),
        ]
        lens_set = LensSet(all_lenses)

        perceptions = await lens_set.perceive_through(
            [
                "temporal",
                "hierarchy",
                "priority",
                "collaborative",
                "flow",
                "quantitative",
                "causal",
                "contextual",
            ],
            mock_entity,
        )

        assert len(perceptions) == 8
