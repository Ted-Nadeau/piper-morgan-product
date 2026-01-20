"""
Tests for Perception and PerceptionMode.

Phase 3.1 TDD: Perception is the result of perceiving through a lens.
PerceptionMode captures temporal perspective (NOTICING, REMEMBERING, ANTICIPATING).
"""

import pytest


class TestPerceptionMode:
    """Tests for PerceptionMode enum."""

    def test_perception_mode_has_noticing(self):
        """PerceptionMode has NOTICING for current state."""
        from services.mux.perception import PerceptionMode

        assert hasattr(PerceptionMode, "NOTICING")
        assert PerceptionMode.NOTICING.value == "noticing"

    def test_perception_mode_has_remembering(self):
        """PerceptionMode has REMEMBERING for historical state."""
        from services.mux.perception import PerceptionMode

        assert hasattr(PerceptionMode, "REMEMBERING")
        assert PerceptionMode.REMEMBERING.value == "remembering"

    def test_perception_mode_has_anticipating(self):
        """PerceptionMode has ANTICIPATING for future state."""
        from services.mux.perception import PerceptionMode

        assert hasattr(PerceptionMode, "ANTICIPATING")
        assert PerceptionMode.ANTICIPATING.value == "anticipating"

    def test_perception_mode_is_enum(self):
        """PerceptionMode is a proper enum."""
        from enum import Enum

        from services.mux.perception import PerceptionMode

        assert issubclass(PerceptionMode, Enum)


class TestPerception:
    """Tests for Perception dataclass."""

    def test_perception_has_lens_name(self):
        """Perception records which lens created it."""
        from services.mux.perception import Perception, PerceptionMode

        perception = Perception(
            lens_name="temporal",
            mode=PerceptionMode.NOTICING,
            raw_data={"meetings": 3},
            observation="You have 3 meetings today",
        )

        assert perception.lens_name == "temporal"

    def test_perception_has_mode(self):
        """Perception records the perception mode."""
        from services.mux.perception import Perception, PerceptionMode

        perception = Perception(
            lens_name="temporal",
            mode=PerceptionMode.REMEMBERING,
            raw_data={},
            observation="Yesterday was quieter",
        )

        assert perception.mode == PerceptionMode.REMEMBERING

    def test_perception_has_raw_data(self):
        """Perception contains raw data from integration."""
        from services.mux.perception import Perception, PerceptionMode

        perception = Perception(
            lens_name="quantitative",
            mode=PerceptionMode.NOTICING,
            raw_data={"tasks_count": 5, "completed": 2},
            observation="2 of 5 tasks complete",
        )

        assert perception.raw_data["tasks_count"] == 5
        assert perception.raw_data["completed"] == 2

    def test_perception_has_observation(self):
        """Perception has experience-framed observation (not raw data)."""
        from services.mux.perception import Perception, PerceptionMode

        perception = Perception(
            lens_name="priority",
            mode=PerceptionMode.NOTICING,
            raw_data={"urgent": 2, "normal": 5},
            observation="I notice 2 urgent items need your attention",
        )

        # Observation should be human-friendly, not raw data dump
        assert "I notice" in perception.observation
        assert "urgent" in perception.observation

    def test_perception_has_default_confidence(self):
        """Perception has default confidence of 1.0."""
        from services.mux.perception import Perception, PerceptionMode

        perception = Perception(
            lens_name="temporal", mode=PerceptionMode.NOTICING, raw_data={}, observation="Test"
        )

        assert perception.confidence == 1.0

    def test_perception_confidence_can_be_set(self):
        """Perception confidence can be explicitly set."""
        from services.mux.perception import Perception, PerceptionMode

        perception = Perception(
            lens_name="causal",
            mode=PerceptionMode.ANTICIPATING,
            raw_data={},
            observation="This might cause delays",
            confidence=0.7,
        )

        assert perception.confidence == 0.7

    def test_perception_experience_framing_not_raw_dump(self):
        """Observation uses experience language, not data language."""
        from services.mux.perception import Perception, PerceptionMode

        # Good: Experience-framed
        good = Perception(
            lens_name="temporal",
            mode=PerceptionMode.NOTICING,
            raw_data={"meetings": [{"time": "10am"}, {"time": "2pm"}]},
            observation="You have 2 meetings today, at 10am and 2pm",
        )

        # The observation should be natural language
        assert "meetings" not in good.observation.lower() or "You have" in good.observation
        assert len(good.observation) > 10  # Not just a data dump


class TestPerceptionMetadata:
    """Tests for Perception metadata fields."""

    def test_perception_has_optional_timestamp(self):
        """Perception can have optional timestamp."""
        from datetime import datetime

        from services.mux.perception import Perception, PerceptionMode

        now = datetime.now()
        perception = Perception(
            lens_name="temporal",
            mode=PerceptionMode.NOTICING,
            raw_data={},
            observation="Test",
            timestamp=now,
        )

        assert perception.timestamp == now

    def test_perception_timestamp_defaults_to_none(self):
        """Perception timestamp is None by default."""
        from services.mux.perception import Perception, PerceptionMode

        perception = Perception(
            lens_name="temporal", mode=PerceptionMode.NOTICING, raw_data={}, observation="Test"
        )

        assert perception.timestamp is None

    def test_perception_has_optional_source(self):
        """Perception can record its data source."""
        from services.mux.perception import Perception, PerceptionMode

        perception = Perception(
            lens_name="collaborative",
            mode=PerceptionMode.NOTICING,
            raw_data={},
            observation="3 team members online",
            source="slack",
        )

        assert perception.source == "slack"
