"""
Tests for RecognitionResponseService.

Part of #411 MUX-INTERACT-RECOGNITION.

Tests cover:
- Channel-specific formatting (web, Slack, CLI)
- Trust-aware language
- Selection matching (numeric, text, partial)
- None-of-these handling
- Edge cases
"""

import pytest

from services.mux.orientation import (
    ArticulationConfig,
    ChannelType,
    OrientationPillarType,
    RecognitionOption,
    RecognitionOptions,
)
from services.mux.recognition_response import (
    RecognitionResponseService,
    SelectionMatch,
    SelectionResult,
)

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def sample_options() -> RecognitionOptions:
    """Standard recognition options for testing."""
    return RecognitionOptions(
        options=[
            RecognitionOption(
                label="Standup prep",
                description="meeting in 45 min",
                intent_hint="prepare_standup",
                relevance=0.9,
                pillar_source=OrientationPillarType.TEMPORAL,
            ),
            RecognitionOption(
                label="API PR review",
                description="waiting for your review",
                intent_hint="review_pr",
                relevance=0.8,
                pillar_source=OrientationPillarType.AGENCY,
            ),
            RecognitionOption(
                label="Today's todos",
                description="3 items pending",
                intent_hint="list_todos",
                relevance=0.7,
                pillar_source=OrientationPillarType.AGENCY,
            ),
        ],
        narrative_frame="I can help with a few things:",
        escape_hatch="Or something else entirely?",
        call_to_action="Which would be helpful?",
    )


@pytest.fixture
def web_config() -> ArticulationConfig:
    """Web channel config."""
    return ArticulationConfig(channel=ChannelType.WEB, trust_stage=2)


@pytest.fixture
def slack_config() -> ArticulationConfig:
    """Slack channel config."""
    return ArticulationConfig(channel=ChannelType.SLACK, trust_stage=2)


@pytest.fixture
def high_trust_config() -> ArticulationConfig:
    """High trust stage config."""
    return ArticulationConfig(channel=ChannelType.WEB, trust_stage=4)


# =============================================================================
# Test: Channel-Specific Formatting
# =============================================================================


class TestFormatForWeb:
    """Tests for web formatting."""

    def test_web_format_includes_narrative_frame(
        self, sample_options: RecognitionOptions, web_config: ArticulationConfig
    ):
        """Web format should include the narrative frame."""
        result = RecognitionResponseService.format_for_web(sample_options, web_config)
        assert "I can help with a few things:" in result

    def test_web_format_includes_all_options(
        self, sample_options: RecognitionOptions, web_config: ArticulationConfig
    ):
        """Web format should list all options as bullets."""
        result = RecognitionResponseService.format_for_web(sample_options, web_config)
        assert "• Standup prep" in result
        assert "• API PR review" in result
        assert "• Today's todos" in result

    def test_web_format_includes_descriptions(
        self, sample_options: RecognitionOptions, web_config: ArticulationConfig
    ):
        """Web format should include option descriptions."""
        result = RecognitionResponseService.format_for_web(sample_options, web_config)
        assert "meeting in 45 min" in result
        assert "waiting for your review" in result

    def test_web_format_includes_call_to_action(
        self, sample_options: RecognitionOptions, web_config: ArticulationConfig
    ):
        """Web format should include call to action."""
        result = RecognitionResponseService.format_for_web(sample_options, web_config)
        assert "Which would be helpful?" in result

    def test_web_format_includes_escape_hatch_at_low_trust(
        self, sample_options: RecognitionOptions
    ):
        """Web format should include escape hatch at trust stage 1-2."""
        config = ArticulationConfig(channel=ChannelType.WEB, trust_stage=1)
        result = RecognitionResponseService.format_for_web(sample_options, config)
        assert "something else entirely" in result

    def test_web_format_escape_hatch_optional_at_high_trust(
        self, sample_options: RecognitionOptions
    ):
        """Web format escape hatch is optional at stage 3+."""
        config = ArticulationConfig(
            channel=ChannelType.WEB, trust_stage=4, include_escape_hatch=False
        )
        result = RecognitionResponseService.format_for_web(sample_options, config)
        # Should NOT include escape hatch when explicitly disabled at high trust
        assert "something else entirely" not in result


class TestFormatForSlack:
    """Tests for Slack formatting."""

    def test_slack_format_uses_numbered_options(
        self, sample_options: RecognitionOptions, slack_config: ArticulationConfig
    ):
        """Slack format should use numbered options."""
        result = RecognitionResponseService.format_for_slack(sample_options, slack_config)
        assert "1. Standup prep" in result
        assert "2. API PR review" in result
        assert "3. Today's todos" in result

    def test_slack_format_is_more_compact(
        self, sample_options: RecognitionOptions, slack_config: ArticulationConfig
    ):
        """Slack format should be shorter than web format."""
        web_result = RecognitionResponseService.format_for_web(
            sample_options, ArticulationConfig(channel=ChannelType.WEB)
        )
        slack_result = RecognitionResponseService.format_for_slack(sample_options, slack_config)
        # Slack should be noticeably shorter
        assert len(slack_result) < len(web_result)

    def test_slack_format_compressed_cta(
        self, sample_options: RecognitionOptions, slack_config: ArticulationConfig
    ):
        """Slack format should use compressed call to action."""
        result = RecognitionResponseService.format_for_slack(sample_options, slack_config)
        assert "Which?" in result


class TestFormatForChannel:
    """Tests for channel routing."""

    def test_routes_to_web_format(
        self, sample_options: RecognitionOptions, web_config: ArticulationConfig
    ):
        """Should route to web format for web channel."""
        result = RecognitionResponseService.format_for_channel(sample_options, web_config)
        # Web format uses bullets
        assert "•" in result

    def test_routes_to_slack_format(
        self, sample_options: RecognitionOptions, slack_config: ArticulationConfig
    ):
        """Should route to Slack format for Slack channel."""
        result = RecognitionResponseService.format_for_channel(sample_options, slack_config)
        # Slack format uses numbers
        assert "1." in result

    def test_routes_to_cli_format(self, sample_options: RecognitionOptions):
        """Should route to CLI format for CLI channel."""
        config = ArticulationConfig(channel=ChannelType.CLI)
        result = RecognitionResponseService.format_for_channel(sample_options, config)
        # CLI uses same format as Slack (numbered)
        assert "1." in result


# =============================================================================
# Test: Trust-Aware Language
# =============================================================================


class TestTrustAwareLanguage:
    """Tests for trust-stage language adaptation."""

    def test_low_trust_uses_cautious_language(self, sample_options: RecognitionOptions):
        """Trust stage 1-2 should use more cautious language."""
        config = ArticulationConfig(channel=ChannelType.WEB, trust_stage=1)
        result = RecognitionResponseService.format_for_web(sample_options, config)
        # The call to action should be present
        assert "helpful" in result.lower()

    def test_high_trust_uses_confident_language(self, sample_options: RecognitionOptions):
        """Trust stage 3-4 should use more confident language."""
        # Create options without custom call_to_action to test default language
        options = RecognitionOptions(
            options=sample_options.options,
            narrative_frame="",  # Empty to use trust-based intro
            escape_hatch=sample_options.escape_hatch,
            call_to_action="",  # Empty to use trust-based CTA
        )
        config = ArticulationConfig(channel=ChannelType.WEB, trust_stage=4)
        result = RecognitionResponseService.format_for_web(options, config)
        # Should use stage 4 language
        assert "Here's what I'm seeing:" in result

    def test_none_response_varies_by_trust(self):
        """'None of these' response should vary by trust stage."""
        low_trust = ArticulationConfig(trust_stage=1)
        high_trust = ArticulationConfig(trust_stage=4)

        low_response = RecognitionResponseService.handle_none_of_these(low_trust)
        high_response = RecognitionResponseService.handle_none_of_these(high_trust)

        # Both should be helpful but different
        assert "help" in low_response.lower()
        assert low_response != high_response


# =============================================================================
# Test: Selection Handling
# =============================================================================


class TestSelectionHandling:
    """Tests for user selection matching."""

    def test_numeric_selection_matches(self, sample_options: RecognitionOptions):
        """Numeric selection should match corresponding option."""
        result = RecognitionResponseService.handle_selection("1", sample_options)
        assert result.result == SelectionResult.MATCHED
        assert result.matched_option.label == "Standup prep"
        assert result.intent_hint == "prepare_standup"

    def test_numeric_selection_second_option(self, sample_options: RecognitionOptions):
        """Numeric '2' should match second option."""
        result = RecognitionResponseService.handle_selection("2", sample_options)
        assert result.result == SelectionResult.MATCHED
        assert result.matched_option.label == "API PR review"

    def test_numeric_out_of_range(self, sample_options: RecognitionOptions):
        """Numeric selection out of range should return appropriate result."""
        result = RecognitionResponseService.handle_selection("5", sample_options)
        assert result.result == SelectionResult.NUMERIC_OUT_OF_RANGE

    def test_exact_label_match(self, sample_options: RecognitionOptions):
        """Exact label match should work."""
        result = RecognitionResponseService.handle_selection("Standup prep", sample_options)
        assert result.result == SelectionResult.MATCHED
        assert result.matched_option.label == "Standup prep"

    def test_case_insensitive_match(self, sample_options: RecognitionOptions):
        """Match should be case insensitive."""
        result = RecognitionResponseService.handle_selection("STANDUP PREP", sample_options)
        assert result.result == SelectionResult.MATCHED

    def test_partial_match_prefix(self, sample_options: RecognitionOptions):
        """Partial match on prefix should work."""
        result = RecognitionResponseService.handle_selection("standup", sample_options)
        assert result.result == SelectionResult.MATCHED
        assert result.matched_option.label == "Standup prep"

    def test_partial_match_keyword(self, sample_options: RecognitionOptions):
        """Partial match on keyword should work."""
        result = RecognitionResponseService.handle_selection("todos", sample_options)
        assert result.result == SelectionResult.MATCHED
        assert result.matched_option.label == "Today's todos"

    def test_none_of_these_explicit(self, sample_options: RecognitionOptions):
        """'None of these' should be detected."""
        result = RecognitionResponseService.handle_selection("none of these", sample_options)
        assert result.result == SelectionResult.NONE_OF_THESE

    def test_none_of_these_variations(self, sample_options: RecognitionOptions):
        """Various 'none' phrases should be detected."""
        phrases = ["none", "something else", "other", "nope"]
        for phrase in phrases:
            result = RecognitionResponseService.handle_selection(phrase, sample_options)
            assert result.result == SelectionResult.NONE_OF_THESE, f"Failed for: {phrase}"

    def test_no_match(self, sample_options: RecognitionOptions):
        """Unrelated input should return no match."""
        result = RecognitionResponseService.handle_selection("check my email", sample_options)
        assert result.result == SelectionResult.NO_MATCH


# =============================================================================
# Test: None of These Handling
# =============================================================================


class TestNoneOfTheseHandling:
    """Tests for 'none of these' response generation."""

    def test_returns_clarification_prompt(self):
        """Should return a clarification prompt."""
        response = RecognitionResponseService.handle_none_of_these()
        assert response  # Non-empty
        assert "?" in response  # Should be a question

    def test_response_varies_by_trust_stage(self):
        """Response should be trust-appropriate."""
        low = RecognitionResponseService.handle_none_of_these(ArticulationConfig(trust_stage=1))
        high = RecognitionResponseService.handle_none_of_these(ArticulationConfig(trust_stage=4))
        # Both should prompt for input
        assert "?" in low or "help" in low.lower()
        assert "?" in high or "mind" in high.lower()


# =============================================================================
# Test: Selection Acknowledgment
# =============================================================================


class TestSelectionAcknowledgment:
    """Tests for selection acknowledgment."""

    def test_acknowledgment_includes_label(self, sample_options: RecognitionOptions):
        """Acknowledgment should reference the selected option."""
        option = sample_options.options[0]
        ack = RecognitionResponseService.get_selection_acknowledgment(option)
        assert "standup prep" in ack.lower()

    def test_acknowledgment_varies_by_trust(self, sample_options: RecognitionOptions):
        """Acknowledgment style should vary by trust."""
        option = sample_options.options[0]
        low_ack = RecognitionResponseService.get_selection_acknowledgment(
            option, ArticulationConfig(trust_stage=1)
        )
        high_ack = RecognitionResponseService.get_selection_acknowledgment(
            option, ArticulationConfig(trust_stage=4)
        )
        # Both acknowledge, but language differs
        assert "standup" in low_ack.lower()
        assert "standup" in high_ack.lower()


# =============================================================================
# Test: Reshow Options
# =============================================================================


class TestReshowOptions:
    """Tests for re-showing options after empty input."""

    def test_reshow_has_different_framing(self, sample_options: RecognitionOptions):
        """Re-shown options should have different intro."""
        original = RecognitionResponseService.format_for_web(sample_options)
        reshow = RecognitionResponseService.format_reshow_options(sample_options)

        # Should have different intros
        assert "again" in reshow.lower()
        assert original != reshow

    def test_reshow_includes_all_options(self, sample_options: RecognitionOptions):
        """Re-show should include all options."""
        result = RecognitionResponseService.format_reshow_options(sample_options)
        assert "Standup prep" in result
        assert "API PR review" in result
        assert "Today's todos" in result


# =============================================================================
# Test: Edge Cases
# =============================================================================


class TestEdgeCases:
    """Edge case tests."""

    def test_empty_selection(self, sample_options: RecognitionOptions):
        """Empty selection should return no match."""
        result = RecognitionResponseService.handle_selection("", sample_options)
        assert result.result == SelectionResult.NO_MATCH

    def test_whitespace_selection(self, sample_options: RecognitionOptions):
        """Whitespace-only selection should return no match."""
        result = RecognitionResponseService.handle_selection("   ", sample_options)
        assert result.result == SelectionResult.NO_MATCH

    def test_single_option(self):
        """Should handle single option gracefully."""
        options = RecognitionOptions(
            options=[
                RecognitionOption(
                    label="Only option",
                    description="the only choice",
                    intent_hint="single",
                    relevance=1.0,
                    pillar_source=OrientationPillarType.AGENCY,
                )
            ],
            narrative_frame="There's one thing I can help with:",
            call_to_action="Want me to do this?",
        )
        result = RecognitionResponseService.format_for_web(options)
        assert "Only option" in result

    def test_no_description_option(self):
        """Should handle options without descriptions."""
        options = RecognitionOptions(
            options=[
                RecognitionOption(
                    label="Quick check",
                    description="",  # No description
                    intent_hint="check",
                    relevance=0.8,
                    pillar_source=OrientationPillarType.PREDICTION,
                )
            ],
            narrative_frame="I can:",
            call_to_action="Want this?",
        )
        result = RecognitionResponseService.format_for_web(options)
        assert "• Quick check" in result
        # Should not have empty parens
        assert "()" not in result

    def test_numeric_zero_selection(self, sample_options: RecognitionOptions):
        """Zero should be out of range (1-indexed)."""
        result = RecognitionResponseService.handle_selection("0", sample_options)
        assert result.result == SelectionResult.NUMERIC_OUT_OF_RANGE

    def test_default_config_when_none_provided(self, sample_options: RecognitionOptions):
        """Should use sensible defaults when no config provided."""
        result = RecognitionResponseService.format_for_channel(sample_options, None)
        # Should use web format by default
        assert "•" in result
