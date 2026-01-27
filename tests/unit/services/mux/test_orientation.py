"""
Tests for the Orientation System.

These tests verify that OrientationState properly:
1. Gathers from available contexts
2. Applies lenses to perceive the Situation
3. Captures confidence levels accurately
4. Supports grammar-aligned vocabulary
"""

from dataclasses import dataclass
from typing import List, Optional
from unittest.mock import MagicMock

import pytest

from services.mux.orientation import (
    OrientationPillar,
    OrientationPillarType,
    OrientationState,
    TrustContext,
)

# --- Test Fixtures ---


@dataclass
class MockUserContext:
    """Mock UserContext for testing."""

    user_id: str = "test-user"
    organization: Optional[str] = "TestOrg"
    projects: List[str] = None
    priorities: List[str] = None
    preferences: dict = None

    def __post_init__(self):
        self.projects = self.projects or []
        self.priorities = self.priorities or []
        self.preferences = self.preferences or {}


@dataclass
class MockConsciousnessContext:
    """Mock ConsciousnessContext for testing."""

    time_of_day: str = "morning"
    is_first_interaction_today: bool = True
    current_hour: int = 9
    user_in_meeting: bool = False
    has_focus_time: bool = False
    meeting_load: str = "light"
    meeting_count: int = 0


class MockInteractionSpace:
    """Mock InteractionSpace enum for testing."""

    def __init__(self, name: str):
        self.name = name


class MockPiperEntity:
    """Mock PiperEntity for testing."""

    def who_am_i(self) -> str:
        return "I am Piper Morgan, your PM assistant"

    def what_can_i_do(self) -> str:
        return "5 capabilities available, 2 active, 0 blocked"


# --- OrientationPillarType Tests ---


class TestOrientationPillarType:
    """Tests for the OrientationPillarType enum."""

    def test_has_five_values(self):
        """OrientationPillarType should have exactly 5 values."""
        assert len(OrientationPillarType) == 5

    def test_pillar_types_exist(self):
        """All five pillar types should exist."""
        assert OrientationPillarType.IDENTITY.value == "identity"
        assert OrientationPillarType.TEMPORAL.value == "temporal"
        assert OrientationPillarType.SPATIAL.value == "spatial"
        assert OrientationPillarType.AGENCY.value == "agency"
        assert OrientationPillarType.PREDICTION.value == "prediction"


# --- OrientationPillar Tests ---


class TestOrientationPillar:
    """Tests for the OrientationPillar dataclass."""

    def test_create_pillar(self):
        """Should create a pillar with all required fields."""
        pillar = OrientationPillar(
            pillar_type=OrientationPillarType.IDENTITY,
            lens_applied="self-awareness",
            perception="I am Piper Morgan",
            confidence=1.0,
            source_context="PiperEntity",
        )
        assert pillar.pillar_type == OrientationPillarType.IDENTITY
        assert pillar.lens_applied == "self-awareness"
        assert pillar.perception == "I am Piper Morgan"
        assert pillar.confidence == 1.0
        assert pillar.source_context == "PiperEntity"

    def test_confidence_validation_valid(self):
        """Should accept confidence in valid range."""
        pillar = OrientationPillar(
            pillar_type=OrientationPillarType.TEMPORAL,
            lens_applied="temporal",
            perception="It's morning",
            confidence=0.5,
            source_context="test",
        )
        assert pillar.confidence == 0.5

    def test_confidence_validation_invalid_high(self):
        """Should reject confidence > 1.0."""
        with pytest.raises(ValueError, match="Confidence must be between"):
            OrientationPillar(
                pillar_type=OrientationPillarType.TEMPORAL,
                lens_applied="temporal",
                perception="It's morning",
                confidence=1.5,
                source_context="test",
            )

    def test_confidence_validation_invalid_low(self):
        """Should reject confidence < 0.0."""
        with pytest.raises(ValueError, match="Confidence must be between"):
            OrientationPillar(
                pillar_type=OrientationPillarType.TEMPORAL,
                lens_applied="temporal",
                perception="It's morning",
                confidence=-0.1,
                source_context="test",
            )


# --- TrustContext Tests ---


class TestTrustContext:
    """Tests for the TrustContext dataclass."""

    def test_create_trust_context(self):
        """Should create trust context with stage."""
        ctx = TrustContext(stage=2, can_offer_hints=True, can_suggest=False)
        assert ctx.stage == 2
        assert ctx.can_offer_hints is True
        assert ctx.can_suggest is False

    def test_from_proactivity_config(self):
        """Should create from ProactivityConfig."""
        mock_config = MagicMock()
        mock_config.can_offer_hints = True
        mock_config.can_suggest = True
        mock_config.can_act_autonomously = False

        ctx = TrustContext.from_proactivity_config(stage=3, config=mock_config)
        assert ctx.stage == 3
        assert ctx.can_offer_hints is True
        assert ctx.can_suggest is True
        assert ctx.can_act_autonomously is False


# --- OrientationState Tests ---


class TestOrientationState:
    """Tests for the OrientationState dataclass."""

    def test_gather_with_no_context(self):
        """Should gather orientation even with no context (using defaults)."""
        state = OrientationState.gather()

        assert state.identity is not None
        assert state.temporal is not None
        assert state.spatial is not None
        assert state.agency is not None
        assert state.prediction is not None

    def test_gather_with_user_context(self):
        """Should incorporate user context into agency pillar."""
        user_ctx = MockUserContext(priorities=["Ship v1.0", "Fix bugs"])
        state = OrientationState.gather(user_context=user_ctx)

        assert "Ship v1.0" in state.agency.perception
        assert state.agency.confidence > 0.5

    def test_gather_with_consciousness_context(self):
        """Should incorporate consciousness context into temporal pillar."""
        consciousness = MockConsciousnessContext(
            time_of_day="afternoon",
            meeting_load="heavy",
            meeting_count=5,
        )
        state = OrientationState.gather(consciousness_context=consciousness)

        assert "afternoon" in state.temporal.perception
        assert "5 meetings" in state.temporal.perception

    def test_gather_with_place(self):
        """Should incorporate place into spatial pillar."""
        place = MockInteractionSpace("SLACK_DM")
        state = OrientationState.gather(place=place)

        assert "direct message" in state.spatial.perception
        assert "Slack" in state.spatial.perception

    def test_gather_with_piper_entity(self):
        """Should use PiperEntity for identity and prediction."""
        piper = MockPiperEntity()
        state = OrientationState.gather(piper_entity=piper)

        assert "Piper Morgan" in state.identity.perception
        assert "capabilities" in state.prediction.perception

    def test_gather_with_trust_context(self):
        """Should include trust context when provided."""
        trust = TrustContext(stage=3, can_suggest=True)
        state = OrientationState.gather(trust_context=trust)

        assert state.trust_context is not None
        assert state.trust_context.stage == 3
        assert state.trust_context.can_suggest is True

    def test_get_pillar_by_type(self):
        """Should retrieve specific pillar by type."""
        state = OrientationState.gather()

        identity = state.get_pillar(OrientationPillarType.IDENTITY)
        assert identity.pillar_type == OrientationPillarType.IDENTITY

        temporal = state.get_pillar(OrientationPillarType.TEMPORAL)
        assert temporal.pillar_type == OrientationPillarType.TEMPORAL

    def test_get_high_confidence_pillars(self):
        """Should return only high-confidence pillars."""
        piper = MockPiperEntity()
        consciousness = MockConsciousnessContext()
        place = MockInteractionSpace("WEB_CHAT")

        state = OrientationState.gather(
            piper_entity=piper,
            consciousness_context=consciousness,
            place=place,
        )

        high_conf = state.get_high_confidence_pillars(threshold=0.7)
        # Identity (1.0), Temporal (0.9), Spatial (0.95) should be included
        assert len(high_conf) >= 3
        for pillar in high_conf:
            assert pillar.confidence >= 0.7

    def test_to_dict(self):
        """Should convert to dictionary for debugging."""
        state = OrientationState.gather()
        d = state.to_dict()

        assert "identity" in d
        assert "perception" in d["identity"]
        assert "confidence" in d["identity"]
        assert "source" in d["identity"]

        assert "temporal" in d
        assert "spatial" in d
        assert "agency" in d
        assert "prediction" in d


# --- Grammar Alignment Tests ---


class TestGrammarAlignment:
    """Tests verifying grammar vocabulary in orientation."""

    def test_identity_uses_self_awareness_lens(self):
        """Identity pillar should use self-awareness lens."""
        state = OrientationState.gather()
        assert state.identity.lens_applied == "self-awareness"

    def test_temporal_uses_temporal_lens(self):
        """Temporal pillar should use temporal lens."""
        state = OrientationState.gather()
        assert state.temporal.lens_applied == "temporal"

    def test_spatial_uses_contextual_lens(self):
        """Spatial pillar should use contextual lens."""
        state = OrientationState.gather()
        assert state.spatial.lens_applied == "contextual"

    def test_agency_uses_priority_lens(self):
        """Agency pillar should use priority lens."""
        state = OrientationState.gather()
        assert state.agency.lens_applied == "priority"

    def test_prediction_uses_causal_lens(self):
        """Prediction pillar should use causal lens."""
        state = OrientationState.gather()
        assert state.prediction.lens_applied == "causal"


# --- Perception Language Tests ---


class TestPerceptionLanguage:
    """Tests for CXO-guided perception language patterns."""

    def test_agency_uses_looks_like_not_seems(self):
        """Agency pillar should use 'looks like' not 'seems to be' (CXO guidance)."""
        user_ctx = MockUserContext(priorities=["Ship v1.0"])
        state = OrientationState.gather(user_context=user_ctx)

        assert "looks like" in state.agency.perception
        assert "seems to be" not in state.agency.perception

    def test_spatial_uses_partnership_language(self):
        """Spatial pillar should use 'we're' for partnership (CXO guidance)."""
        place = MockInteractionSpace("WEB_CHAT")
        state = OrientationState.gather(place=place)

        assert "We're" in state.spatial.perception or "we're" in state.spatial.perception
