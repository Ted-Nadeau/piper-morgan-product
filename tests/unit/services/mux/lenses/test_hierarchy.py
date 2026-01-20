"""
Tests for HierarchyLens.

Phase 3.3 TDD: HierarchyLens perceives containment relationships.
Maps to HIERARCHY dimension in spatial infrastructure.
"""

import pytest

from services.mux.perception import PerceptionMode


class TestHierarchyLensBasics:
    """Tests for HierarchyLens basic functionality."""

    def test_hierarchy_lens_has_correct_name(self):
        """HierarchyLens has name 'hierarchy'."""
        from services.mux.lenses.hierarchy import HierarchyLens

        lens = HierarchyLens()
        assert lens.name == "hierarchy"

    def test_hierarchy_lens_inherits_from_lens(self):
        """HierarchyLens inherits from Lens base class."""
        from services.mux.lenses.base import Lens
        from services.mux.lenses.hierarchy import HierarchyLens

        assert issubclass(HierarchyLens, Lens)


class TestHierarchyLensPerception:
    """Tests for HierarchyLens perceive functionality."""

    @pytest.mark.asyncio
    async def test_hierarchy_lens_noticing_mode(self, mock_entity):
        """HierarchyLens perceives current containment relationships."""
        from services.mux.lenses.hierarchy import HierarchyLens
        from services.mux.perception import Perception

        lens = HierarchyLens()
        perception = await lens.perceive(mock_entity, PerceptionMode.NOTICING)

        assert isinstance(perception, Perception)
        assert perception.lens_name == "hierarchy"
        assert perception.mode == PerceptionMode.NOTICING

    @pytest.mark.asyncio
    async def test_hierarchy_lens_perceives_containment(self, mock_place):
        """HierarchyLens identifies what contains and is contained by target."""
        from services.mux.lenses.hierarchy import HierarchyLens

        lens = HierarchyLens()
        perception = await lens.perceive(mock_place)

        # Raw data should have containment info
        assert "raw_data" in dir(perception) or hasattr(perception, "raw_data")

    @pytest.mark.asyncio
    async def test_hierarchy_lens_experience_framing(self, mock_entity):
        """HierarchyLens observations are experience-framed."""
        from services.mux.lenses.hierarchy import HierarchyLens

        lens = HierarchyLens()
        perception = await lens.perceive(mock_entity)

        # Should be natural language
        assert len(perception.observation) > 10
