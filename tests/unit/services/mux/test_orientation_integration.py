"""
Integration tests for Orientation System.

These tests verify the full orientation pipeline:
1. OrientationState gathering
2. Pipeline integration with IntentClassifier
3. End-to-end flow from context to articulation

Issue #410: MUX-INTERACT-CANONICAL-ENHANCE
"""

from unittest.mock import MagicMock, patch

import pytest

from services.intent_service.intent_types import IntentClassificationContext
from services.mux.orientation import (
    ArticulationConfig,
    ChannelType,
    OrientationArticulator,
    OrientationPillar,
    OrientationPillarType,
    OrientationState,
    RecognitionGenerator,
    TrustContext,
)
from services.shared_types import PlaceType

# --- Fixtures ---


def create_complete_orientation() -> OrientationState:
    """Create a fully-formed orientation for integration tests."""
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
            confidence=0.9,
            source_context="ConsciousnessContext",
        ),
        spatial=OrientationPillar(
            pillar_type=OrientationPillarType.SPATIAL,
            lens_applied="contextual",
            perception="We're chatting in the web interface",
            confidence=0.95,
            source_context="PlaceDetector",
        ),
        agency=OrientationPillar(
            pillar_type=OrientationPillarType.AGENCY,
            lens_applied="priority",
            perception="Your top priority looks like shipping v1.0",
            confidence=0.85,
            source_context="UserContext.priorities",
        ),
        prediction=OrientationPillar(
            pillar_type=OrientationPillarType.PREDICTION,
            lens_applied="causal",
            perception="I can help with tasks, calendar, and project updates",
            confidence=0.8,
            source_context="PiperEntity.capabilities",
        ),
        trust_context=TrustContext(stage=2, can_suggest=True),
    )


# --- Pipeline Integration Tests ---


class TestOrientationPipeline:
    """Tests for the full orientation pipeline."""

    def test_gather_to_articulate_flow(self):
        """Full flow: gather orientation → articulate → recognize."""
        # 1. Gather orientation
        orientation = create_complete_orientation()

        # 2. Articulate for web channel
        config = ArticulationConfig(channel=ChannelType.WEB, trust_stage=2)
        articulation = OrientationArticulator.articulate(orientation, config)

        # 3. Generate recognition options
        recognition = RecognitionGenerator.generate(orientation, config)

        # Verify articulation
        assert len(articulation) > 0
        assert "help" in articulation.lower()

        # Verify recognition
        assert len(recognition.options) >= 2
        assert recognition.narrative_frame != ""
        assert recognition.call_to_action != ""

    def test_classification_context_receives_orientation(self):
        """IntentClassificationContext can hold orientation."""
        orientation = create_complete_orientation()

        context = IntentClassificationContext(
            message="What's on my plate today?",
            user_id="user-123",
            place=PlaceType.WEB_CHAT,
            orientation=orientation,
        )

        assert context.orientation is not None
        assert context.orientation.identity.perception == "I am Piper Morgan, your PM assistant"
        assert context.orientation.trust_context.stage == 2

    def test_orientation_none_when_not_gathered(self):
        """Orientation can be None for backwards compatibility."""
        context = IntentClassificationContext(
            message="Hello",
            user_id="user-123",
            place=PlaceType.WEB_CHAT,
        )

        assert context.orientation is None

    def test_channel_affects_articulation_length(self):
        """Different channels produce different articulation lengths."""
        orientation = create_complete_orientation()

        web_config = ArticulationConfig(channel=ChannelType.WEB, trust_stage=3)
        slack_config = ArticulationConfig(channel=ChannelType.SLACK, trust_stage=3)

        web_articulation = OrientationArticulator.articulate(orientation, web_config)
        slack_articulation = OrientationArticulator.articulate(orientation, slack_config)

        # Web should be same or longer than Slack
        assert len(web_articulation) >= len(slack_articulation)


# --- Trust Gradient Integration Tests ---


class TestTrustGradientIntegration:
    """Tests for trust-aware behavior across components."""

    def test_stage_1_minimal_exposure(self):
        """Stage 1 keeps orientation internal."""
        orientation = create_complete_orientation()
        orientation.trust_context = TrustContext(stage=1)

        config = ArticulationConfig(trust_stage=1)
        articulation = OrientationArticulator.articulate(orientation, config)
        recognition = RecognitionGenerator.generate(orientation, config)

        # Stage 1: minimal exposure
        assert "How can I help?" in articulation
        # But recognition still provides options (just with escape hatch)
        assert recognition.escape_hatch is not None

    def test_stage_3_proactive_surfacing(self):
        """Stage 3 can proactively surface orientation."""
        orientation = create_complete_orientation()
        orientation.trust_context = TrustContext(stage=3, can_suggest=True)

        config = ArticulationConfig(trust_stage=3)
        articulation = OrientationArticulator.articulate(orientation, config)

        # Stage 3: richer context
        assert len(articulation) > len("How can I help?")
        assert orientation.can_surface_proactively() is True
        assert orientation.can_use_i_notice() is True


# --- Pillar Confidence Integration Tests ---


class TestPillarConfidenceIntegration:
    """Tests for confidence-based pillar filtering."""

    def test_low_confidence_pillars_handled_gracefully(self):
        """Low confidence doesn't break the pipeline."""
        orientation = OrientationState(
            identity=OrientationPillar(
                pillar_type=OrientationPillarType.IDENTITY,
                lens_applied="self-awareness",
                perception="I am Piper Morgan",
                confidence=1.0,
                source_context="PiperEntity",
            ),
            temporal=OrientationPillar(
                pillar_type=OrientationPillarType.TEMPORAL,
                lens_applied="temporal",
                perception="Unknown time",
                confidence=0.1,  # Very low
                source_context="test",
            ),
            spatial=OrientationPillar(
                pillar_type=OrientationPillarType.SPATIAL,
                lens_applied="contextual",
                perception="Unknown place",
                confidence=0.1,  # Very low
                source_context="test",
            ),
            agency=OrientationPillar(
                pillar_type=OrientationPillarType.AGENCY,
                lens_applied="priority",
                perception="Unknown priority",
                confidence=0.1,  # Very low
                source_context="test",
            ),
            prediction=OrientationPillar(
                pillar_type=OrientationPillarType.PREDICTION,
                lens_applied="causal",
                perception="I can help",
                confidence=0.8,
                source_context="test",
            ),
            trust_context=TrustContext(stage=2),
        )

        config = ArticulationConfig(trust_stage=2)

        # Should not raise, should produce valid output
        articulation = OrientationArticulator.articulate(orientation, config)
        recognition = RecognitionGenerator.generate(orientation, config)

        assert len(articulation) > 0
        assert len(recognition.options) >= 2  # Minimum enforced


# --- Format for Display Integration Tests ---


class TestDisplayFormatIntegration:
    """Tests for end-to-end display formatting."""

    def test_format_for_display_includes_all_components(self):
        """Formatted display includes narrative, options, and CTA."""
        orientation = create_complete_orientation()
        config = ArticulationConfig(trust_stage=2)

        recognition = RecognitionGenerator.generate(orientation, config)
        display = RecognitionGenerator.format_for_display(recognition, config)

        # Should include all parts
        assert recognition.narrative_frame in display
        assert recognition.call_to_action in display
        if recognition.escape_hatch:
            assert recognition.escape_hatch in display

    def test_articulation_and_recognition_can_combine(self):
        """Articulation and recognition can be combined for full response."""
        orientation = create_complete_orientation()
        config = ArticulationConfig(trust_stage=2, channel=ChannelType.WEB)

        articulation = OrientationArticulator.articulate(orientation, config)
        recognition = RecognitionGenerator.generate(orientation, config)
        formatted_recognition = RecognitionGenerator.format_for_display(recognition, config)

        # Both should be valid strings that can be combined
        full_response = f"{articulation}\n\n{formatted_recognition}"

        assert len(full_response) > len(articulation)
        assert len(full_response) > len(formatted_recognition)
