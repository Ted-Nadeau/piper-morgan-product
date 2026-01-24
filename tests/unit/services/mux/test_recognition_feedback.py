"""
Tests for RecognitionFeedback recording.

Part of #412 MUX-INTERACT-INTENT-BRIDGE.

Tests cover:
- Dataclass creation
- Feedback recording
- Helper functions for different selection types
"""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from services.mux.recognition_feedback import (
    SELECTED_NONE_OF_THESE,
    SELECTED_UNRELATED_INPUT,
    SELECTION_MATCHED,
    SELECTION_NO_MATCH,
    SELECTION_NONE_OF_THESE,
    FeedbackContext,
    RecognitionFeedback,
    create_feedback_from_match,
    create_feedback_from_no_match,
    create_feedback_from_none_of_these,
    record_recognition_feedback,
)

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def feedback_context() -> FeedbackContext:
    """Sample feedback context."""
    return FeedbackContext(
        original_message="check on things",
        confidence_at_trigger=0.55,
        user_id="user-123",
    )


@pytest.fixture
def offered_options() -> list:
    """Sample offered options (intent hints)."""
    return ["prepare_standup", "review_pr", "list_todos"]


# =============================================================================
# Test: FeedbackContext
# =============================================================================


class TestFeedbackContext:
    """Tests for FeedbackContext dataclass."""

    def test_create_with_all_fields(self):
        """Should create context with all fields."""
        ctx = FeedbackContext(
            original_message="test message",
            confidence_at_trigger=0.5,
            user_id="user-456",
        )
        assert ctx.original_message == "test message"
        assert ctx.confidence_at_trigger == 0.5
        assert ctx.user_id == "user-456"

    def test_create_without_user_id(self):
        """Should create context without user_id (optional)."""
        ctx = FeedbackContext(
            original_message="test message",
            confidence_at_trigger=0.5,
        )
        assert ctx.original_message == "test message"
        assert ctx.user_id is None


# =============================================================================
# Test: RecognitionFeedback
# =============================================================================


class TestRecognitionFeedback:
    """Tests for RecognitionFeedback dataclass."""

    def test_create_with_required_fields(self):
        """Should create feedback with required fields."""
        feedback = RecognitionFeedback(
            original_message="check things",
            confidence_at_trigger=0.55,
            offered_options=["opt1", "opt2"],
            selected_option="opt1",
            selection_type=SELECTION_MATCHED,
        )
        assert feedback.original_message == "check things"
        assert feedback.confidence_at_trigger == 0.55
        assert feedback.offered_options == ["opt1", "opt2"]
        assert feedback.selected_option == "opt1"
        assert feedback.selection_type == SELECTION_MATCHED

    def test_timestamp_auto_generated(self):
        """Should auto-generate timestamp."""
        before = datetime.now(timezone.utc)
        feedback = RecognitionFeedback(
            original_message="test",
            confidence_at_trigger=0.5,
            offered_options=[],
            selected_option="test",
            selection_type=SELECTION_MATCHED,
        )
        after = datetime.now(timezone.utc)

        assert feedback.timestamp is not None
        assert before <= feedback.timestamp <= after

    def test_user_id_optional(self):
        """Should allow None user_id."""
        feedback = RecognitionFeedback(
            original_message="test",
            confidence_at_trigger=0.5,
            offered_options=[],
            selected_option="test",
            selection_type=SELECTION_MATCHED,
            user_id=None,
        )
        assert feedback.user_id is None


# =============================================================================
# Test: record_recognition_feedback
# =============================================================================


class TestRecordRecognitionFeedback:
    """Tests for the logging function."""

    def test_logs_feedback_info(self, feedback_context, offered_options):
        """Should log feedback with structured data."""
        feedback = RecognitionFeedback(
            original_message="check things",
            confidence_at_trigger=0.55,
            offered_options=offered_options,
            selected_option="prepare_standup",
            selection_type=SELECTION_MATCHED,
            user_id="user-123",
        )

        with patch("services.mux.recognition_feedback.logger") as mock_logger:
            record_recognition_feedback(feedback)

            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args

            # Check event name
            assert call_args[0][0] == "recognition_feedback"

            # Check kwargs
            kwargs = call_args[1]
            assert kwargs["original_message"] == "check things"
            assert kwargs["confidence_at_trigger"] == 0.55
            assert kwargs["offered_options"] == offered_options
            assert kwargs["selected_option"] == "prepare_standup"
            assert kwargs["selection_type"] == SELECTION_MATCHED
            assert kwargs["user_id"] == "user-123"

    def test_logs_timestamp_as_iso(self, feedback_context):
        """Should log timestamp in ISO format."""
        timestamp = datetime(2026, 1, 23, 21, 16, 0)
        feedback = RecognitionFeedback(
            original_message="test",
            confidence_at_trigger=0.5,
            offered_options=[],
            selected_option="test",
            selection_type=SELECTION_MATCHED,
            timestamp=timestamp,
        )

        with patch("services.mux.recognition_feedback.logger") as mock_logger:
            record_recognition_feedback(feedback)

            kwargs = mock_logger.info.call_args[1]
            assert kwargs["timestamp"] == "2026-01-23T21:16:00"


# =============================================================================
# Test: Helper Functions
# =============================================================================


class TestCreateFeedbackFromMatch:
    """Tests for create_feedback_from_match helper."""

    def test_creates_matched_feedback(self, feedback_context, offered_options):
        """Should create feedback with MATCHED type."""
        feedback = create_feedback_from_match(
            context=feedback_context,
            offered_options=offered_options,
            selected_intent_hint="prepare_standup",
        )

        assert feedback.original_message == "check on things"
        assert feedback.confidence_at_trigger == 0.55
        assert feedback.offered_options == offered_options
        assert feedback.selected_option == "prepare_standup"
        assert feedback.selection_type == SELECTION_MATCHED
        assert feedback.user_id == "user-123"


class TestCreateFeedbackFromNoneOfThese:
    """Tests for create_feedback_from_none_of_these helper."""

    def test_creates_none_of_these_feedback(self, feedback_context, offered_options):
        """Should create feedback with NONE_OF_THESE type."""
        feedback = create_feedback_from_none_of_these(
            context=feedback_context,
            offered_options=offered_options,
        )

        assert feedback.original_message == "check on things"
        assert feedback.selected_option == SELECTED_NONE_OF_THESE
        assert feedback.selection_type == SELECTION_NONE_OF_THESE


class TestCreateFeedbackFromNoMatch:
    """Tests for create_feedback_from_no_match helper."""

    def test_creates_no_match_feedback(self, feedback_context, offered_options):
        """Should create feedback with NO_MATCH type."""
        feedback = create_feedback_from_no_match(
            context=feedback_context,
            offered_options=offered_options,
        )

        assert feedback.original_message == "check on things"
        assert feedback.selected_option == SELECTED_UNRELATED_INPUT
        assert feedback.selection_type == SELECTION_NO_MATCH


# =============================================================================
# Test: Constants
# =============================================================================


class TestConstants:
    """Tests for module constants."""

    def test_selection_type_constants(self):
        """Should have expected selection type values."""
        assert SELECTION_MATCHED == "matched"
        assert SELECTION_NONE_OF_THESE == "none_of_these"
        assert SELECTION_NO_MATCH == "no_match"

    def test_sentinel_constants(self):
        """Should have expected sentinel values."""
        assert SELECTED_NONE_OF_THESE == "none_of_these"
        assert SELECTED_UNRELATED_INPUT == "unrelated_input"
