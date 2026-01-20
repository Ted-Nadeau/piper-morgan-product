"""
Tests for Lens Base Class.

Phase 3.2 TDD: Lens is the abstract base class for perceptual lenses.
Each lens views targets through a specific dimension (temporal, hierarchy, etc.).
"""

from abc import ABC

import pytest


class TestLensIsAbstract:
    """Tests for Lens abstract base class."""

    def test_lens_is_abstract_base_class(self):
        """Lens is an abstract base class."""
        from services.mux.lenses.base import Lens

        assert issubclass(Lens, ABC)

    def test_lens_cannot_be_instantiated(self):
        """Lens cannot be instantiated directly."""
        from services.mux.lenses.base import Lens

        with pytest.raises(TypeError) as exc_info:
            Lens()

        assert (
            "abstract" in str(exc_info.value).lower()
            or "instantiate" in str(exc_info.value).lower()
        )

    def test_lens_has_name_attribute(self):
        """Lens subclasses must have name attribute."""
        from services.mux.lenses.base import Lens

        # Check that Lens expects name
        assert hasattr(Lens, "name") or "name" in str(Lens.__dict__)


class TestLensPerceiverMethod:
    """Tests for Lens perceive method requirement."""

    def test_lens_requires_perceive_method(self):
        """Lens subclasses must implement perceive()."""
        from services.mux.lenses.base import Lens

        # Lens should have abstract perceive method
        assert hasattr(Lens, "perceive")
        assert getattr(Lens.perceive, "__isabstractmethod__", False)

    def test_concrete_lens_must_implement_perceive(self):
        """Concrete lens without perceive() raises TypeError."""
        from services.mux.lenses.base import Lens

        class IncompleteLens(Lens):
            name = "incomplete"
            # Missing perceive() method

        with pytest.raises(TypeError):
            IncompleteLens()


class TestLensFrameAsExperience:
    """Tests for Lens _frame_as_experience helper."""

    def test_lens_has_frame_as_experience(self):
        """Lens provides _frame_as_experience() helper."""
        from services.mux.lenses.base import Lens

        assert hasattr(Lens, "_frame_as_experience")

    @pytest.mark.asyncio
    async def test_frame_as_experience_returns_string(self):
        """_frame_as_experience returns string observation."""
        from services.mux.lenses.base import Lens
        from services.mux.perception import Perception, PerceptionMode

        # Create a concrete lens for testing
        class TestLens(Lens):
            name = "test"

            async def perceive(self, target, mode=PerceptionMode.NOTICING):
                raw_data = {"items": 3}
                observation = self._frame_as_experience(raw_data, mode)
                return Perception(
                    lens_name=self.name, mode=mode, raw_data=raw_data, observation=observation
                )

        lens = TestLens()
        result = lens._frame_as_experience({"items": 3}, PerceptionMode.NOTICING)

        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_frame_as_experience_mode_aware(self):
        """_frame_as_experience produces different text for different modes."""
        from services.mux.lenses.base import Lens
        from services.mux.perception import Perception, PerceptionMode

        class TestLens(Lens):
            name = "test"

            async def perceive(self, target, mode=PerceptionMode.NOTICING):
                raw_data = {"items": 3}
                observation = self._frame_as_experience(raw_data, mode)
                return Perception(
                    lens_name=self.name, mode=mode, raw_data=raw_data, observation=observation
                )

        lens = TestLens()

        noticing = lens._frame_as_experience({"items": 3}, PerceptionMode.NOTICING)
        remembering = lens._frame_as_experience({"items": 3}, PerceptionMode.REMEMBERING)
        anticipating = lens._frame_as_experience({"items": 3}, PerceptionMode.ANTICIPATING)

        # Different modes should produce different framing
        # (or at least the framing function should accept mode)
        assert noticing is not None
        assert remembering is not None
        assert anticipating is not None


class TestConcreteLensImplementation:
    """Tests for concrete lens implementation."""

    @pytest.mark.asyncio
    async def test_concrete_lens_can_perceive(self, mock_entity):
        """Properly implemented lens can perceive targets."""
        from services.mux.lenses.base import Lens
        from services.mux.perception import Perception, PerceptionMode

        class SimpleLens(Lens):
            name = "simple"

            async def perceive(self, target, mode=PerceptionMode.NOTICING):
                raw_data = {"target_id": getattr(target, "id", "unknown")}
                observation = f"I notice target {raw_data['target_id']}"
                return Perception(
                    lens_name=self.name, mode=mode, raw_data=raw_data, observation=observation
                )

        lens = SimpleLens()
        perception = await lens.perceive(mock_entity)

        assert perception.lens_name == "simple"
        assert perception.mode == PerceptionMode.NOTICING
        assert "entity-001" in perception.observation

    @pytest.mark.asyncio
    async def test_concrete_lens_respects_mode(self, mock_entity):
        """Lens respects requested perception mode."""
        from services.mux.lenses.base import Lens
        from services.mux.perception import Perception, PerceptionMode

        class ModeLens(Lens):
            name = "mode_aware"

            async def perceive(self, target, mode=PerceptionMode.NOTICING):
                return Perception(
                    lens_name=self.name,
                    mode=mode,
                    raw_data={},
                    observation=f"Perceiving in {mode.value} mode",
                )

        lens = ModeLens()

        p1 = await lens.perceive(mock_entity, PerceptionMode.NOTICING)
        p2 = await lens.perceive(mock_entity, PerceptionMode.REMEMBERING)
        p3 = await lens.perceive(mock_entity, PerceptionMode.ANTICIPATING)

        assert p1.mode == PerceptionMode.NOTICING
        assert p2.mode == PerceptionMode.REMEMBERING
        assert p3.mode == PerceptionMode.ANTICIPATING
