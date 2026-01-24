"""
Tests for Recognition Option Generation.

These tests verify that RecognitionGenerator:
1. Derives options from orientation pillars
2. Uses Option C (narrative) framing
3. Respects 2-4 option limit
4. Applies trust-aware escape hatches
5. Uses appropriate call-to-action by trust level
"""

import pytest

from services.mux.orientation import (
    ArticulationConfig,
    ChannelType,
    OrientationPillar,
    OrientationPillarType,
    OrientationState,
    RecognitionGenerator,
    RecognitionOption,
    RecognitionOptions,
    TrustContext,
)

# --- Test Fixtures ---


def create_test_orientation(
    temporal_perception: str = "It's Thursday morning (3 meetings today)",
    temporal_confidence: float = 0.9,
    agency_confidence: float = 0.8,
    trust_stage: int = 2,
) -> OrientationState:
    """Create a test orientation."""
    return OrientationState(
        identity=OrientationPillar(
            pillar_type=OrientationPillarType.IDENTITY,
            lens_applied="self-awareness",
            perception="I am Piper Morgan",
            confidence=1.0,
            source_context="test",
        ),
        temporal=OrientationPillar(
            pillar_type=OrientationPillarType.TEMPORAL,
            lens_applied="temporal",
            perception=temporal_perception,
            confidence=temporal_confidence,
            source_context="test",
        ),
        spatial=OrientationPillar(
            pillar_type=OrientationPillarType.SPATIAL,
            lens_applied="contextual",
            perception="We're in the web chat",
            confidence=0.95,
            source_context="test",
        ),
        agency=OrientationPillar(
            pillar_type=OrientationPillarType.AGENCY,
            lens_applied="priority",
            perception="Your top priority looks like shipping v1.0",
            confidence=agency_confidence,
            source_context="test",
        ),
        prediction=OrientationPillar(
            pillar_type=OrientationPillarType.PREDICTION,
            lens_applied="causal",
            perception="I can help with tasks and calendar",
            confidence=0.85,
            source_context="test",
        ),
        trust_context=TrustContext(stage=trust_stage),
    )


# --- RecognitionOption Tests ---


class TestRecognitionOption:
    """Tests for RecognitionOption dataclass."""

    def test_create_option(self):
        """Should create option with all fields."""
        opt = RecognitionOption(
            label="Standup prep",
            description="Get ready for standup",
            intent_hint="standup",
            relevance=0.8,
            pillar_source=OrientationPillarType.TEMPORAL,
        )

        assert opt.label == "Standup prep"
        assert opt.description == "Get ready for standup"
        assert opt.intent_hint == "standup"
        assert opt.relevance == 0.8
        assert opt.pillar_source == OrientationPillarType.TEMPORAL


# --- RecognitionOptions Tests ---


class TestRecognitionOptions:
    """Tests for RecognitionOptions dataclass."""

    def test_enforces_max_4_options(self):
        """Should keep only top 4 options by relevance."""
        options = [
            RecognitionOption("A", "desc", "hint", 0.5, OrientationPillarType.AGENCY),
            RecognitionOption("B", "desc", "hint", 0.9, OrientationPillarType.TEMPORAL),
            RecognitionOption("C", "desc", "hint", 0.3, OrientationPillarType.SPATIAL),
            RecognitionOption("D", "desc", "hint", 0.8, OrientationPillarType.PREDICTION),
            RecognitionOption("E", "desc", "hint", 0.7, OrientationPillarType.IDENTITY),
        ]

        recognition = RecognitionOptions(
            options=options,
            narrative_frame="Test narrative",
            call_to_action="Which helps?",
        )

        assert len(recognition.options) == 4
        # Should be sorted by relevance (B=0.9, D=0.8, E=0.7, A=0.5)
        labels = [o.label for o in recognition.options]
        assert labels == ["B", "D", "E", "A"]

    def test_has_escape_hatch(self):
        """Should report escape hatch presence correctly."""
        with_hatch = RecognitionOptions(
            options=[],
            narrative_frame="Test",
            escape_hatch="Or something else?",
            call_to_action="Which helps?",
        )
        assert with_hatch.has_escape_hatch is True

        without_hatch = RecognitionOptions(
            options=[],
            narrative_frame="Test",
            call_to_action="Which helps?",
        )
        assert without_hatch.has_escape_hatch is False


# --- RecognitionGenerator Tests ---


class TestRecognitionGenerator:
    """Tests for RecognitionGenerator."""

    def test_generate_from_orientation(self):
        """Should generate options from orientation."""
        orientation = create_test_orientation()
        config = ArticulationConfig(trust_stage=2)

        result = RecognitionGenerator.generate(orientation, config)

        assert isinstance(result, RecognitionOptions)
        assert len(result.options) >= 2
        assert len(result.options) <= 4
        assert result.narrative_frame != ""

    def test_temporal_pillar_influences_options(self):
        """Morning temporal context should generate standup option."""
        orientation = create_test_orientation(
            temporal_perception="It's Monday morning",
            temporal_confidence=0.9,
        )
        config = ArticulationConfig(trust_stage=2)

        result = RecognitionGenerator.generate(orientation, config)

        # Should have standup-related option due to morning
        labels = [o.label.lower() for o in result.options]
        assert any("standup" in label for label in labels)

    def test_meeting_context_generates_calendar(self):
        """Meeting context should generate calendar option."""
        orientation = create_test_orientation(
            temporal_perception="It's afternoon (5 meetings today)",
            temporal_confidence=0.9,
        )
        config = ArticulationConfig(trust_stage=2)

        result = RecognitionGenerator.generate(orientation, config)

        # Should have calendar option due to meetings
        labels = [o.label.lower() for o in result.options]
        assert any("calendar" in label for label in labels)

    def test_agency_pillar_generates_priorities(self):
        """Agency pillar should generate priorities option."""
        orientation = create_test_orientation(agency_confidence=0.9)
        config = ArticulationConfig(trust_stage=2)

        result = RecognitionGenerator.generate(orientation, config)

        labels = [o.label.lower() for o in result.options]
        assert any("priorit" in label for label in labels)

    def test_minimum_2_options(self):
        """Should always generate at least 2 options."""
        orientation = create_test_orientation(
            temporal_confidence=0.2,  # Low
            agency_confidence=0.2,  # Low
        )
        config = ArticulationConfig(trust_stage=2)

        result = RecognitionGenerator.generate(orientation, config)

        assert len(result.options) >= 2


# --- Escape Hatch Tests ---


class TestEscapeHatch:
    """Tests for trust-aware escape hatch."""

    def test_stage_1_has_escape_hatch(self):
        """Stage 1 should always have escape hatch."""
        orientation = create_test_orientation(trust_stage=1)
        config = ArticulationConfig(trust_stage=1)

        result = RecognitionGenerator.generate(orientation, config)

        assert result.escape_hatch is not None
        assert "something else" in result.escape_hatch.lower()

    def test_stage_2_has_escape_hatch(self):
        """Stage 2 should always have escape hatch."""
        orientation = create_test_orientation(trust_stage=2)
        config = ArticulationConfig(trust_stage=2)

        result = RecognitionGenerator.generate(orientation, config)

        assert result.escape_hatch is not None

    def test_stage_3_no_escape_hatch_if_disabled(self):
        """Stage 3 can skip escape hatch if configured."""
        orientation = create_test_orientation(trust_stage=3)
        config = ArticulationConfig(trust_stage=3, include_escape_hatch=False)

        result = RecognitionGenerator.generate(orientation, config)

        assert result.escape_hatch is None

    def test_stage_3_has_escape_hatch_by_default(self):
        """Stage 3 includes escape hatch by default."""
        orientation = create_test_orientation(trust_stage=3)
        config = ArticulationConfig(trust_stage=3, include_escape_hatch=True)

        result = RecognitionGenerator.generate(orientation, config)

        assert result.escape_hatch is not None


# --- Call to Action Tests ---


class TestCallToAction:
    """Tests for trust-aware call to action."""

    def test_stage_1_explicit_cta(self):
        """Stage 1 should use explicit CTA."""
        orientation = create_test_orientation(trust_stage=1)
        config = ArticulationConfig(trust_stage=1)

        result = RecognitionGenerator.generate(orientation, config)

        # Explicit: "Which would be helpful?"
        assert "helpful" in result.call_to_action.lower()

    def test_stage_2_explicit_cta(self):
        """Stage 2 should use explicit CTA."""
        orientation = create_test_orientation(trust_stage=2)
        config = ArticulationConfig(trust_stage=2)

        result = RecognitionGenerator.generate(orientation, config)

        assert "helpful" in result.call_to_action.lower()

    def test_stage_3_assumptive_cta(self):
        """Stage 3 should use assumptive CTA."""
        orientation = create_test_orientation(trust_stage=3)
        config = ArticulationConfig(trust_stage=3)

        result = RecognitionGenerator.generate(orientation, config)

        # Assumptive: "Want me to start with...?"
        assert "want" in result.call_to_action.lower() or "start" in result.call_to_action.lower()


# --- Narrative Framing Tests ---


class TestNarrativeFraming:
    """Tests for Option C narrative framing."""

    def test_uses_narrative_not_list(self):
        """Should use narrative framing, not a bullet list."""
        orientation = create_test_orientation()
        config = ArticulationConfig(trust_stage=2)

        result = RecognitionGenerator.generate(orientation, config)

        # Narrative = prose, not bullets
        assert "-" not in result.narrative_frame
        assert "*" not in result.narrative_frame
        assert "1." not in result.narrative_frame

    def test_narrative_includes_temporal_context(self):
        """Narrative should mention temporal context."""
        orientation = create_test_orientation(
            temporal_perception="It's a busy Thursday morning",
            temporal_confidence=0.9,
        )
        config = ArticulationConfig(trust_stage=2)

        result = RecognitionGenerator.generate(orientation, config)

        # Should mention morning/Thursday in narrative
        narrative_lower = result.narrative_frame.lower()
        assert "morning" in narrative_lower or "thursday" in narrative_lower

    def test_web_uses_full_narrative(self):
        """Web channel should use full narrative."""
        orientation = create_test_orientation()
        config = ArticulationConfig(channel=ChannelType.WEB, trust_stage=2)

        result = RecognitionGenerator.generate(orientation, config)

        # Full narrative is longer
        assert len(result.narrative_frame) > 20

    def test_slack_uses_compressed_narrative(self):
        """Slack channel should use compressed narrative."""
        orientation = create_test_orientation()
        config = ArticulationConfig(channel=ChannelType.SLACK, trust_stage=2)

        result = RecognitionGenerator.generate(orientation, config)

        # Compressed uses em-dash
        assert "—" in result.narrative_frame or len(result.narrative_frame) < 100


# --- Display Formatting Tests ---


class TestDisplayFormatting:
    """Tests for format_for_display."""

    def test_includes_all_parts(self):
        """Formatted output should include narrative, CTA, and escape hatch."""
        orientation = create_test_orientation(trust_stage=2)
        config = ArticulationConfig(trust_stage=2)

        recognition = RecognitionGenerator.generate(orientation, config)
        display = RecognitionGenerator.format_for_display(recognition, config)

        assert recognition.narrative_frame in display
        assert recognition.call_to_action in display
        if recognition.escape_hatch:
            assert recognition.escape_hatch in display

    def test_no_escape_hatch_when_disabled(self):
        """Formatted output should omit escape hatch when disabled."""
        orientation = create_test_orientation(trust_stage=3)
        config = ArticulationConfig(trust_stage=3, include_escape_hatch=False)

        recognition = RecognitionGenerator.generate(orientation, config)
        display = RecognitionGenerator.format_for_display(recognition, config)

        assert "something else" not in display.lower()
