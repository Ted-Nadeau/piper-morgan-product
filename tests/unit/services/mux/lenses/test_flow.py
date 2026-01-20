"""
Tests for FlowLens.

Phase 3.3 TDD: FlowLens perceives workflow state and momentum.
Maps to FLOW dimension in spatial infrastructure.
"""

import pytest

from services.mux.perception import PerceptionMode


class TestFlowLensBasics:
    """Tests for FlowLens basic functionality."""

    def test_flow_lens_has_correct_name(self):
        """FlowLens has name 'flow'."""
        from services.mux.lenses.flow import FlowLens

        lens = FlowLens()
        assert lens.name == "flow"

    def test_flow_lens_inherits_from_lens(self):
        """FlowLens inherits from Lens base class."""
        from services.mux.lenses.base import Lens
        from services.mux.lenses.flow import FlowLens

        assert issubclass(FlowLens, Lens)


class TestFlowLensPerception:
    """Tests for FlowLens perceive functionality."""

    @pytest.mark.asyncio
    async def test_flow_lens_noticing_mode(self, mock_entity):
        """FlowLens perceives current workflow state."""
        from services.mux.lenses.flow import FlowLens
        from services.mux.perception import Perception

        lens = FlowLens()
        perception = await lens.perceive(mock_entity, PerceptionMode.NOTICING)

        assert isinstance(perception, Perception)
        assert perception.lens_name == "flow"
        assert perception.mode == PerceptionMode.NOTICING

    @pytest.mark.asyncio
    async def test_flow_lens_experience_framing(self, mock_entity):
        """FlowLens observations are experience-framed."""
        from services.mux.lenses.flow import FlowLens

        lens = FlowLens()
        perception = await lens.perceive(mock_entity)

        # Should be natural language about state/progress
        assert len(perception.observation) > 10
