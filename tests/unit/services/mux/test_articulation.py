"""
Tests for Orientation Articulation.

These tests verify that OrientationArticulator:
1. Respects trust-aware surfacing depth
2. Uses CXO-approved language patterns
3. Adapts to channel (web vs Slack)
4. Applies observational vs declarative framing correctly
"""

from unittest.mock import MagicMock

import pytest

from services.mux.orientation import (
    ArticulationConfig,
    ChannelType,
    OrientationArticulator,
    OrientationPillar,
    OrientationPillarType,
    OrientationState,
    TrustContext,
)

# --- Test Fixtures ---


def create_test_orientation(
    temporal_confidence: float = 0.9,
    spatial_confidence: float = 0.95,
    agency_confidence: float = 0.8,
    trust_stage: int = 2,
) -> OrientationState:
    """Create a test orientation with configurable confidence levels."""
    return OrientationState(
        identity=OrientationPillar(
            pillar_type=OrientationPillarType.IDENTITY,
            lens_applied="self-awareness",
            perception="I am Piper Morgan, your PM assistant",
            confidence=1.0,
            source_context="PiperEntity",
        ),
        temporal=OrientationPillar(
            pillar_type=OrientationPillarType.TEMPORAL,
            lens_applied="temporal",
            perception="It's Thursday morning (3 meetings today)",
            confidence=temporal_confidence,
            source_context="ConsciousnessContext",
        ),
        spatial=OrientationPillar(
            pillar_type=OrientationPillarType.SPATIAL,
            lens_applied="contextual",
            perception="We're in the web chat",
            confidence=spatial_confidence,
            source_context="PlaceDetector",
        ),
        agency=OrientationPillar(
            pillar_type=OrientationPillarType.AGENCY,
            lens_applied="priority",
            perception="Your top priority looks like shipping v1.0",
            confidence=agency_confidence,
            source_context="UserContext.priorities",
        ),
        prediction=OrientationPillar(
            pillar_type=OrientationPillarType.PREDICTION,
            lens_applied="causal",
            perception="I can help with tasks, calendar, and project updates",
            confidence=0.85,
            source_context="PiperEntity",
        ),
        trust_context=TrustContext(stage=trust_stage, can_suggest=trust_stage >= 2),
    )


# --- ArticulationConfig Tests ---


class TestArticulationConfig:
    """Tests for ArticulationConfig."""

    def test_web_not_compressed(self):
        """Web channel should not use compressed format."""
        config = ArticulationConfig(channel=ChannelType.WEB)
        assert config.use_compressed_format is False

    def test_slack_is_compressed(self):
        """Slack channel should use compressed format."""
        config = ArticulationConfig(channel=ChannelType.SLACK)
        assert config.use_compressed_format is True

    def test_cli_is_compressed(self):
        """CLI channel should use compressed format."""
        config = ArticulationConfig(channel=ChannelType.CLI)
        assert config.use_compressed_format is True

    def test_escape_hatch_required_stage_1(self):
        """Stage 1 should always include escape hatch."""
        config = ArticulationConfig(trust_stage=1, include_escape_hatch=False)
        assert config.should_include_escape_hatch is True

    def test_escape_hatch_required_stage_2(self):
        """Stage 2 should always include escape hatch."""
        config = ArticulationConfig(trust_stage=2, include_escape_hatch=False)
        assert config.should_include_escape_hatch is True

    def test_escape_hatch_optional_stage_3(self):
        """Stage 3 can skip escape hatch if configured."""
        config = ArticulationConfig(trust_stage=3, include_escape_hatch=False)
        assert config.should_include_escape_hatch is False

    def test_escape_hatch_optional_stage_4(self):
        """Stage 4 can skip escape hatch if configured."""
        config = ArticulationConfig(trust_stage=4, include_escape_hatch=False)
        assert config.should_include_escape_hatch is False


# --- Trust-Aware Surfacing Tests ---


class TestTrustAwareSurfacing:
    """Tests for trust-aware surfacing depth."""

    def test_stage_1_purely_reactive(self):
        """Stage 1 users should get purely reactive response."""
        orientation = create_test_orientation(trust_stage=1)
        config = ArticulationConfig(trust_stage=1)

        result = OrientationArticulator.articulate(orientation, config)

        # Stage 1 = minimal, reactive
        assert "How can I help?" in result
        # Should NOT proactively share orientation details
        assert "Thursday" not in result
        assert "priority" not in result

    def test_stage_2_reactive_contextual(self):
        """Stage 2 users get context when they ask for help."""
        orientation = create_test_orientation(trust_stage=2)
        config = ArticulationConfig(trust_stage=2)

        result = OrientationArticulator.articulate(orientation, config)

        # Should include orientation context
        assert len(result) > len("How can I help?")
        # Should include escape hatch
        assert "something else" in result.lower() or "help" in result.lower()

    def test_stage_3_proactive_contextual(self):
        """Stage 3 users can receive proactive context."""
        orientation = create_test_orientation(trust_stage=3)
        config = ArticulationConfig(trust_stage=3)

        result = OrientationArticulator.articulate(orientation, config)

        # Should include orientation context proactively
        assert len(result) > len("How can I help?")

    def test_orientation_can_surface_proactively(self):
        """OrientationState.can_surface_proactively respects trust."""
        # Stage 1-2: Cannot surface proactively
        orientation = create_test_orientation(trust_stage=1)
        assert orientation.can_surface_proactively() is False

        orientation = create_test_orientation(trust_stage=2)
        assert orientation.can_surface_proactively() is False

        # Stage 3+: Can surface proactively
        orientation = create_test_orientation(trust_stage=3)
        assert orientation.can_surface_proactively() is True

        orientation = create_test_orientation(trust_stage=4)
        assert orientation.can_surface_proactively() is True

    def test_can_use_i_notice(self):
        """'I notice' should only be used at Stage 3+."""
        orientation = create_test_orientation(trust_stage=2)
        assert orientation.can_use_i_notice() is False

        orientation = create_test_orientation(trust_stage=3)
        assert orientation.can_use_i_notice() is True


# --- Language Pattern Tests ---


class TestLanguagePatterns:
    """Tests for CXO-approved language patterns."""

    def test_uses_looks_like_not_seems(self):
        """Should use 'looks like' not 'seems to be'."""
        orientation = create_test_orientation()
        config = ArticulationConfig(trust_stage=2)

        result = OrientationArticulator.articulate(orientation, config)

        # Check agency perception uses "looks like"
        assert "seems to be" not in result.lower()

    def test_validate_articulation_catches_seems(self):
        """Validator should catch 'seems to be'."""
        warnings = OrientationArticulator.validate_articulation(
            "Your priority seems to be shipping"
        )
        assert len(warnings) > 0
        assert "seems" in warnings[0].lower()

    def test_validate_articulation_catches_i_think(self):
        """Validator should catch 'I think'."""
        warnings = OrientationArticulator.validate_articulation("I think your priority is shipping")
        assert len(warnings) > 0

    def test_validate_articulation_passes_looks_like(self):
        """Validator should pass 'looks like'."""
        warnings = OrientationArticulator.validate_articulation(
            "It looks like your priority is shipping"
        )
        assert len(warnings) == 0

    def test_observational_markers_defined(self):
        """Should have CXO-approved observational markers."""
        markers = OrientationArticulator.OBSERVATIONAL_MARKERS

        assert "It looks like" in markers.values()
        assert "I notice" in markers.values()
        assert "From what I can see" in markers.values()


# --- Channel Adaptation Tests ---


class TestChannelAdaptation:
    """Tests for channel-specific articulation."""

    def test_web_full_narrative(self):
        """Web channel should use full narrative."""
        orientation = create_test_orientation()
        config = ArticulationConfig(channel=ChannelType.WEB, trust_stage=3)

        result = OrientationArticulator.articulate(orientation, config)

        # Full narrative includes temporal + spatial + agency
        assert "Thursday" in result or "morning" in result
        assert "help" in result.lower()

    def test_slack_compressed(self):
        """Slack channel should use compressed format."""
        orientation = create_test_orientation()
        config = ArticulationConfig(channel=ChannelType.SLACK, trust_stage=3)

        result = OrientationArticulator.articulate(orientation, config)

        # Compressed format uses em-dash and shorter phrases
        # Should not include long preambles
        assert len(result) < 200  # Reasonably short

    def test_web_longer_than_slack(self):
        """Web articulation should be longer than Slack."""
        orientation = create_test_orientation()

        web_result = OrientationArticulator.articulate(
            orientation, ArticulationConfig(channel=ChannelType.WEB, trust_stage=3)
        )
        slack_result = OrientationArticulator.articulate(
            orientation, ArticulationConfig(channel=ChannelType.SLACK, trust_stage=3)
        )

        assert len(web_result) >= len(slack_result)


# --- Pillar Articulation Tests ---


class TestPillarArticulation:
    """Tests for individual pillar articulation."""

    def test_articulate_temporal_pillar(self):
        """Temporal pillar should use declarative framing (it's factual)."""
        pillar = OrientationPillar(
            pillar_type=OrientationPillarType.TEMPORAL,
            lens_applied="temporal",
            perception="It's Thursday morning",
            confidence=0.9,
            source_context="test",
        )

        result = OrientationArticulator.articulate_pillar(pillar)

        # Declarative - just states the fact
        assert result == "It's Thursday morning"

    def test_articulate_agency_pillar_no_i_notice(self):
        """Agency pillar without 'I notice' permission."""
        pillar = OrientationPillar(
            pillar_type=OrientationPillarType.AGENCY,
            lens_applied="priority",
            perception="Your top priority looks like shipping",
            confidence=0.8,
            source_context="test",
        )

        result = OrientationArticulator.articulate_pillar(pillar, use_i_notice=False)

        # Should use existing "looks like" phrasing
        assert "looks like" in result

    def test_articulate_agency_pillar_with_i_notice(self):
        """Agency pillar with 'I notice' permission (Stage 3+)."""
        pillar = OrientationPillar(
            pillar_type=OrientationPillarType.AGENCY,
            lens_applied="priority",
            perception="Your top priority looks like shipping",
            confidence=0.9,
            source_context="test",
        )

        result = OrientationArticulator.articulate_pillar(pillar, use_i_notice=True)

        # Should use "I notice" for Stage 3+ users
        assert "I notice" in result


# --- Edge Cases ---


class TestEdgeCases:
    """Tests for edge cases."""

    def test_low_confidence_pillars_excluded(self):
        """Low confidence pillars should be excluded from articulation."""
        orientation = create_test_orientation(
            temporal_confidence=0.3,  # Low
            agency_confidence=0.2,  # Very low
        )
        config = ArticulationConfig(trust_stage=3)

        result = OrientationArticulator.articulate(orientation, config)

        # Low confidence content should not dominate
        # Should still have something to say
        assert len(result) > 0

    def test_no_trust_context(self):
        """Should handle missing trust context gracefully."""
        orientation = create_test_orientation()
        orientation.trust_context = None

        # Should not raise
        assert orientation.can_surface_proactively() is False
        assert orientation.can_use_i_notice() is False

    def test_empty_articulation_fallback(self):
        """Should fall back gracefully when nothing to articulate."""
        orientation = create_test_orientation(
            temporal_confidence=0.1,
            spatial_confidence=0.1,
            agency_confidence=0.1,
        )
        config = ArticulationConfig(trust_stage=3)

        result = OrientationArticulator.articulate(orientation, config)

        # Should have a fallback
        assert "help" in result.lower()
