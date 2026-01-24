"""
Tests for RecognitionHandler.

Part of #411 MUX-INTERACT-RECOGNITION.
Feedback tests added in #412.

Tests cover:
- Selection matching and routing
- "None of these" flow
- Edge cases (empty input, out of range)
- Trust penalty rules
- Feedback recording (#412)
"""

from unittest.mock import MagicMock, patch

import pytest

from services.domain.models import IntentCategory
from services.mux.orientation import (
    ArticulationConfig,
    ChannelType,
    OrientationPillarType,
    RecognitionOption,
    RecognitionOptions,
)
from services.mux.recognition_feedback import (
    SELECTION_MATCHED,
    SELECTION_NO_MATCH,
    SELECTION_NONE_OF_THESE,
    FeedbackContext,
)
from services.mux.recognition_handler import (
    RecognitionHandler,
    RecognitionHandlerResult,
    RecognitionState,
    create_intent_from_hint,
)
from services.mux.recognition_response import SelectionResult

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def handler() -> RecognitionHandler:
    """Standard recognition handler."""
    return RecognitionHandler()


@pytest.fixture
def sample_options() -> RecognitionOptions:
    """Sample recognition options for testing."""
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


# =============================================================================
# Test: Successful Selection
# =============================================================================


class TestSuccessfulSelection:
    """Tests for successful option selection."""

    def test_numeric_selection_routes_to_handler(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """Numeric selection should route to correct handler."""
        result = handler.handle_selection("1", sample_options, web_config)

        assert result.selection_result == SelectionResult.MATCHED
        assert result.should_route_to_handler is True
        assert result.intent_hint == "prepare_standup"
        assert result.trust_penalty is False

    def test_text_selection_routes_to_handler(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """Text selection should route to correct handler."""
        result = handler.handle_selection("standup prep", sample_options, web_config)

        assert result.selection_result == SelectionResult.MATCHED
        assert result.should_route_to_handler is True
        assert result.intent_hint == "prepare_standup"

    def test_partial_selection_routes_to_handler(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """Partial text selection should route to correct handler."""
        result = handler.handle_selection("standup", sample_options, web_config)

        assert result.selection_result == SelectionResult.MATCHED
        assert result.should_route_to_handler is True
        assert result.intent_hint == "prepare_standup"

    def test_selection_returns_acknowledgment(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """Selection should return acknowledgment text."""
        result = handler.handle_selection("1", sample_options, web_config)

        assert result.response_text is not None
        assert "standup" in result.response_text.lower()

    def test_state_transition_to_normal(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """Selection should transition state to NORMAL."""
        result = handler.handle_selection("1", sample_options, web_config)

        assert "NORMAL" in result.state_transition
        assert "RECOGNITION_OFFERED" in result.state_transition


# =============================================================================
# Test: None of These
# =============================================================================


class TestNoneOfThese:
    """Tests for 'none of these' selection."""

    def test_none_triggers_clarification(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """'None' should trigger clarification prompt."""
        result = handler.handle_selection("none", sample_options, web_config)

        assert result.selection_result == SelectionResult.NONE_OF_THESE
        assert result.should_route_to_handler is False
        assert result.response_text is not None
        assert "?" in result.response_text  # Should be a question

    def test_something_else_triggers_clarification(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """'Something else' should trigger clarification prompt."""
        result = handler.handle_selection("something else", sample_options, web_config)

        assert result.selection_result == SelectionResult.NONE_OF_THESE
        assert result.should_route_to_handler is False

    def test_no_trust_penalty_for_none(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """'None of these' should NOT penalize trust."""
        result = handler.handle_selection("none", sample_options, web_config)

        assert result.trust_penalty is False

    def test_state_transition_to_clarifying(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """'None' should transition state to CLARIFYING."""
        result = handler.handle_selection("none", sample_options, web_config)

        assert "CLARIFYING" in result.state_transition


# =============================================================================
# Test: No Match / Unrelated Input
# =============================================================================


class TestNoMatch:
    """Tests for unmatched selections."""

    def test_unrelated_input_triggers_reclassify(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """Unrelated input should trigger re-classification."""
        result = handler.handle_selection("check my email", sample_options, web_config)

        assert result.selection_result == SelectionResult.NO_MATCH
        # Should route but with no intent_hint (signals re-classify)
        assert result.should_route_to_handler is True
        assert result.intent_hint is None  # Caller should re-classify

    def test_empty_input_reshows_options(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """Empty input should re-show options."""
        result = handler.handle_selection("", sample_options, web_config)

        assert result.selection_result == SelectionResult.NO_MATCH
        assert result.should_route_to_handler is False
        assert result.response_text is not None
        # Should mention options again
        assert "1." in result.response_text or "option" in result.response_text.lower()

    def test_whitespace_input_reshows_options(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """Whitespace-only input should re-show options."""
        result = handler.handle_selection("   ", sample_options, web_config)

        assert result.selection_result == SelectionResult.NO_MATCH
        assert result.should_route_to_handler is False

    def test_no_trust_penalty_for_unrelated(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """Unrelated input should NOT penalize trust."""
        result = handler.handle_selection("check my email", sample_options, web_config)

        assert result.trust_penalty is False


# =============================================================================
# Test: Numeric Out of Range
# =============================================================================


class TestNumericOutOfRange:
    """Tests for out-of-range numeric selection."""

    def test_out_of_range_returns_helpful_message(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """Out of range number should return helpful message."""
        result = handler.handle_selection("5", sample_options, web_config)

        assert result.selection_result == SelectionResult.NUMERIC_OUT_OF_RANGE
        assert result.should_route_to_handler is False
        assert result.response_text is not None
        assert "3" in result.response_text  # Max valid number

    def test_zero_is_out_of_range(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """0 should be out of range (1-indexed)."""
        result = handler.handle_selection("0", sample_options, web_config)

        assert result.selection_result == SelectionResult.NUMERIC_OUT_OF_RANGE

    def test_no_trust_penalty_for_out_of_range(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """Out of range should NOT penalize trust."""
        result = handler.handle_selection("5", sample_options, web_config)

        assert result.trust_penalty is False


# =============================================================================
# Test: Trust Penalty Rules
# =============================================================================


class TestTrustPenalty:
    """Tests for trust penalty rules."""

    def test_no_penalty_for_any_selection(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """No selection type should penalize trust."""
        # All selection types
        test_cases = [
            "1",  # Valid selection
            "standup",  # Text selection
            "none",  # None of these
            "check my email",  # Unrelated
            "",  # Empty
            "5",  # Out of range
        ]

        for selection in test_cases:
            result = handler.handle_selection(selection, sample_options, web_config)
            assert result.trust_penalty is False, f"Trust penalized for: {selection}"


# =============================================================================
# Test: create_intent_from_hint
# =============================================================================


class TestCreateIntentFromHint:
    """Tests for intent creation from hints."""

    def test_creates_intent_with_hint_as_action(self):
        """Intent action should match the hint."""
        intent = create_intent_from_hint("prepare_standup")
        assert intent.action == "prepare_standup"

    def test_intent_has_high_confidence(self):
        """Intent should have high confidence (user explicitly selected)."""
        intent = create_intent_from_hint("prepare_standup")
        assert intent.confidence == 1.0

    def test_intent_has_recognition_source(self):
        """Intent should have recognition_selection source."""
        intent = create_intent_from_hint("prepare_standup")
        assert intent.context.get("source") == "recognition_selection"

    def test_query_hints_get_query_category(self):
        """Query-related hints should get QUERY category."""
        query_hints = ["list_todos", "show_status", "get_calendar"]
        for hint in query_hints:
            intent = create_intent_from_hint(hint)
            assert intent.category == IntentCategory.QUERY

    def test_execution_hints_get_execution_category(self):
        """Execution-related hints should get EXECUTION category."""
        exec_hints = ["create_todo", "add_item", "review_pr"]
        for hint in exec_hints:
            intent = create_intent_from_hint(hint)
            assert intent.category == IntentCategory.EXECUTION


# =============================================================================
# Test: State Enum
# =============================================================================


class TestRecognitionState:
    """Tests for RecognitionState enum."""

    def test_normal_state_exists(self):
        """NORMAL state should exist."""
        assert RecognitionState.NORMAL.value == "normal"

    def test_offered_state_exists(self):
        """RECOGNITION_OFFERED state should exist."""
        assert RecognitionState.RECOGNITION_OFFERED.value == "offered"

    def test_clarifying_state_exists(self):
        """CLARIFYING state should exist."""
        assert RecognitionState.CLARIFYING.value == "clarifying"


# =============================================================================
# Test: Feedback Recording (#412)
# =============================================================================


@pytest.fixture
def feedback_context() -> FeedbackContext:
    """Feedback context for testing."""
    return FeedbackContext(
        original_message="check on things",
        confidence_at_trigger=0.55,
        user_id="user-123",
    )


class TestFeedbackRecording:
    """Tests for feedback recording integration (#412)."""

    def test_matched_selection_records_feedback(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
        feedback_context: FeedbackContext,
    ):
        """Matched selection should record feedback when context provided."""
        with patch("services.mux.recognition_handler.record_recognition_feedback") as mock_record:
            handler.handle_selection("1", sample_options, web_config, feedback_context)

            mock_record.assert_called_once()
            feedback = mock_record.call_args[0][0]
            assert feedback.selection_type == SELECTION_MATCHED
            assert feedback.selected_option == "prepare_standup"
            assert feedback.original_message == "check on things"

    def test_none_of_these_records_feedback(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
        feedback_context: FeedbackContext,
    ):
        """'None of these' should record feedback when context provided."""
        with patch("services.mux.recognition_handler.record_recognition_feedback") as mock_record:
            handler.handle_selection("none", sample_options, web_config, feedback_context)

            mock_record.assert_called_once()
            feedback = mock_record.call_args[0][0]
            assert feedback.selection_type == SELECTION_NONE_OF_THESE
            assert feedback.selected_option == "none_of_these"

    def test_unrelated_input_records_feedback(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
        feedback_context: FeedbackContext,
    ):
        """Unrelated input should record feedback when context provided."""
        with patch("services.mux.recognition_handler.record_recognition_feedback") as mock_record:
            handler.handle_selection("check my email", sample_options, web_config, feedback_context)

            mock_record.assert_called_once()
            feedback = mock_record.call_args[0][0]
            assert feedback.selection_type == SELECTION_NO_MATCH
            assert feedback.selected_option == "unrelated_input"

    def test_empty_input_does_not_record_feedback(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
        feedback_context: FeedbackContext,
    ):
        """Empty input should NOT record feedback (not meaningful)."""
        with patch("services.mux.recognition_handler.record_recognition_feedback") as mock_record:
            handler.handle_selection("", sample_options, web_config, feedback_context)

            mock_record.assert_not_called()

    def test_no_feedback_without_context(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
    ):
        """Should not record feedback when no context provided (backward compatible)."""
        with patch("services.mux.recognition_handler.record_recognition_feedback") as mock_record:
            # No feedback_context parameter - backward compatibility
            handler.handle_selection("1", sample_options, web_config)

            mock_record.assert_not_called()

    def test_feedback_includes_all_offered_options(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
        feedback_context: FeedbackContext,
    ):
        """Feedback should include all offered option hints."""
        with patch("services.mux.recognition_handler.record_recognition_feedback") as mock_record:
            handler.handle_selection("1", sample_options, web_config, feedback_context)

            feedback = mock_record.call_args[0][0]
            assert feedback.offered_options == [
                "prepare_standup",
                "review_pr",
                "list_todos",
            ]

    def test_feedback_includes_confidence(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
        feedback_context: FeedbackContext,
    ):
        """Feedback should include confidence at trigger time."""
        with patch("services.mux.recognition_handler.record_recognition_feedback") as mock_record:
            handler.handle_selection("1", sample_options, web_config, feedback_context)

            feedback = mock_record.call_args[0][0]
            assert feedback.confidence_at_trigger == 0.55

    def test_feedback_includes_user_id(
        self,
        handler: RecognitionHandler,
        sample_options: RecognitionOptions,
        web_config: ArticulationConfig,
        feedback_context: FeedbackContext,
    ):
        """Feedback should include user ID from context."""
        with patch("services.mux.recognition_handler.record_recognition_feedback") as mock_record:
            handler.handle_selection("1", sample_options, web_config, feedback_context)

            feedback = mock_record.call_args[0][0]
            assert feedback.user_id == "user-123"
