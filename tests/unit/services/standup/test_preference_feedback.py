"""
Unit tests for Preference Feedback Handler.

Issue #555: STANDUP-LEARNING - User Preference Learning
Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Tests for correction detection, confirmation handling, and confidence adjustments.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from services.standup.preference_feedback import (
    ConfirmationPrompt,
    CorrectionResult,
    PreferenceFeedbackHandler,
    handle_preference_feedback,
)
from services.standup.preference_models import (
    PreferenceSource,
    PreferenceType,
    UserStandupPreference,
)
from services.standup.preference_service import UserPreferenceService


class TestCorrectionResult:
    """Tests for CorrectionResult dataclass."""

    def test_default_creation(self):
        """Test creating correction result with defaults."""
        result = CorrectionResult()
        assert result.was_correction is False
        assert result.corrected_preference is None
        assert result.previous_value is None
        assert result.new_value is None
        assert result.confidence_adjustment == 0.0

    def test_to_dict(self):
        """Test converting to dictionary."""
        result = CorrectionResult(
            was_correction=True,
            previous_value="github",
            new_value="calendar",
            confidence_adjustment=-0.15,
            message="Changed focus",
        )
        d = result.to_dict()
        assert d["was_correction"] is True
        assert d["previous_value"] == "github"
        assert d["new_value"] == "calendar"


class TestConfirmationPrompt:
    """Tests for ConfirmationPrompt dataclass."""

    def test_creation(self):
        """Test creating confirmation prompt."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
            confidence=0.4,
        )
        prompt = ConfirmationPrompt(
            preference=pref,
            question="Focus on GitHub?",
            options=["Yes", "No"],
        )
        assert prompt.question == "Focus on GitHub?"
        assert len(prompt.options) == 2

    def test_to_dict(self):
        """Test converting to dictionary."""
        pref = UserStandupPreference(
            user_id="user-123",
            value="github",
            confidence=0.4,
        )
        prompt = ConfirmationPrompt(
            preference=pref,
            question="Focus on GitHub?",
            options=["Yes", "No"],
        )
        d = prompt.to_dict()
        assert d["question"] == "Focus on GitHub?"
        assert d["confidence"] == 0.4


class TestPreferenceFeedbackHandler:
    """Tests for PreferenceFeedbackHandler class."""

    @pytest.fixture
    def temp_storage(self):
        """Create a temporary storage directory."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def handler(self, temp_storage):
        """Create a handler with temporary storage."""
        service = UserPreferenceService(storage_path=temp_storage)
        return PreferenceFeedbackHandler(preference_service=service)

    # =========================================================================
    # Correction Detection Tests
    # =========================================================================

    def test_detect_correction_no(self, handler):
        """Test detecting 'no, ...' correction."""
        assert handler.detect_correction("no, focus on calendar instead")
        assert handler.detect_correction("No, I meant GitHub")

    def test_detect_correction_actually(self, handler):
        """Test detecting 'actually' correction."""
        assert handler.detect_correction("actually, I want brief format")
        assert handler.detect_correction("Actually I prefer detailed")

    def test_detect_correction_wrong(self, handler):
        """Test detecting 'wrong' correction."""
        assert handler.detect_correction("that's wrong, use calendar")
        assert handler.detect_correction("wrong focus area")

    def test_detect_correction_instead(self, handler):
        """Test detecting 'instead of' correction."""
        assert handler.detect_correction("instead of github, use calendar")
        assert handler.detect_correction("switch to calendar instead")

    def test_detect_correction_not_that(self, handler):
        """Test detecting 'not that' correction."""
        assert handler.detect_correction("not that, focus on todos")

    def test_detect_correction_change_to(self, handler):
        """Test detecting 'change to' correction."""
        assert handler.detect_correction("change it to brief")
        assert handler.detect_correction("change to detailed")

    def test_detect_correction_negative(self, handler):
        """Test non-corrections aren't detected."""
        assert not handler.detect_correction("focus on github")
        assert not handler.detect_correction("make it brief")
        assert not handler.detect_correction("looks good")

    # =========================================================================
    # Confirmation Detection Tests
    # =========================================================================

    def test_detect_confirmation_yes(self, handler):
        """Test detecting 'yes' confirmation."""
        assert handler.detect_confirmation("yes")
        assert handler.detect_confirmation("Yes, that's right")
        assert handler.detect_confirmation("yeah")

    def test_detect_confirmation_correct(self, handler):
        """Test detecting 'correct' confirmation."""
        assert handler.detect_confirmation("correct")
        assert handler.detect_confirmation("that's correct")

    def test_detect_confirmation_good(self, handler):
        """Test detecting 'good' confirmation."""
        assert handler.detect_confirmation("that's good")
        assert handler.detect_confirmation("perfect")

    def test_detect_confirmation_keep(self, handler):
        """Test detecting 'keep' confirmation."""
        assert handler.detect_confirmation("keep it")
        assert handler.detect_confirmation("keep that setting")

    def test_detect_confirmation_negative(self, handler):
        """Test non-confirmations aren't detected."""
        assert not handler.detect_confirmation("focus on github")
        assert not handler.detect_confirmation("no")
        assert not handler.detect_confirmation("remove that")

    # =========================================================================
    # Rejection Detection Tests
    # =========================================================================

    def test_detect_rejection_no(self, handler):
        """Test detecting 'no' rejection."""
        assert handler.detect_rejection("no")
        assert handler.detect_rejection("nope")

    def test_detect_rejection_dont(self, handler):
        """Test detecting 'don't' rejection."""
        assert handler.detect_rejection("don't keep that")
        assert handler.detect_rejection("dont want that")

    def test_detect_rejection_remove(self, handler):
        """Test detecting 'remove' rejection."""
        assert handler.detect_rejection("remove that")
        assert handler.detect_rejection("delete it")

    def test_detect_rejection_with_new_value(self, handler):
        """Test that rejection with new value isn't pure rejection."""
        # "no, focus on X" is a correction, not a rejection
        assert not handler.detect_rejection("no, focus on calendar")
        assert not handler.detect_rejection("no, use github instead")

    # =========================================================================
    # Correction Processing Tests
    # =========================================================================

    @pytest.mark.asyncio
    async def test_process_correction_not_a_correction(self, handler):
        """Test processing non-correction message."""
        prefs = [
            UserStandupPreference(
                user_id="user-123",
                preference_type=PreferenceType.CONTENT_FILTER,
                value="github",
            )
        ]
        result = await handler.process_correction("user-123", "looks good", prefs)
        assert result.was_correction is False

    @pytest.mark.asyncio
    async def test_process_correction_focus_change(self, handler):
        """Test processing focus area correction."""
        prefs = [
            UserStandupPreference(
                user_id="user-123",
                preference_type=PreferenceType.CONTENT_FILTER,
                key="focus",
                value="github",
                confidence=0.8,
            )
        ]
        result = await handler.process_correction("user-123", "no, focus on calendar", prefs)
        assert result.was_correction is True
        assert result.previous_value == "github"
        assert result.new_value == "calendar"
        assert result.confidence_adjustment == -0.15

    @pytest.mark.asyncio
    async def test_process_correction_reduces_confidence(self, handler):
        """Test that correction reduces preference confidence."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
            confidence=0.9,
        )
        result = await handler.process_correction("user-123", "no, focus on calendar", [pref])

        # Check confidence was reduced
        if result.corrected_preference:
            assert result.corrected_preference.confidence < 0.9

    @pytest.mark.asyncio
    async def test_process_correction_updates_source(self, handler):
        """Test that correction updates preference source."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
            source=PreferenceSource.INFERRED,
        )
        result = await handler.process_correction("user-123", "no, focus on calendar", [pref])

        if result.corrected_preference:
            assert result.corrected_preference.source == PreferenceSource.CORRECTED

    # =========================================================================
    # Confirmation Processing Tests
    # =========================================================================

    @pytest.mark.asyncio
    async def test_process_confirmation_boosts_confidence(self, handler):
        """Test that confirmation boosts confidence."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            value="github",
            confidence=0.5,
        )
        updated = await handler.process_confirmation("user-123", pref, confirmed=True)
        assert updated.confidence > 0.5

    @pytest.mark.asyncio
    async def test_process_confirmation_rejection_reduces(self, handler):
        """Test that rejection reduces confidence."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            value="github",
            confidence=0.5,
        )
        updated = await handler.process_confirmation("user-123", pref, confirmed=False)
        assert updated.confidence < 0.5

    # =========================================================================
    # Confirmation Prompt Generation Tests
    # =========================================================================

    def test_generate_confirmation_prompts_empty(self, handler):
        """Test no prompts for high confidence preferences."""
        prefs = [
            UserStandupPreference(
                user_id="user-123",
                preference_type=PreferenceType.CONTENT_FILTER,
                value="github",
                confidence=0.9,
            )
        ]
        prompts = handler.generate_confirmation_prompts(prefs, threshold=0.5)
        assert len(prompts) == 0

    def test_generate_confirmation_prompts_low_confidence(self, handler):
        """Test prompts generated for low confidence preferences."""
        prefs = [
            UserStandupPreference(
                user_id="user-123",
                preference_type=PreferenceType.CONTENT_FILTER,
                value="github",
                confidence=0.4,
            )
        ]
        prompts = handler.generate_confirmation_prompts(prefs, threshold=0.5)
        assert len(prompts) == 1
        assert "github" in prompts[0].question

    def test_generate_confirmation_prompts_max_limit(self, handler):
        """Test max prompts limit is respected."""
        prefs = [
            UserStandupPreference(
                user_id="user-123",
                preference_type=PreferenceType.CONTENT_FILTER,
                value=f"item{i}",
                confidence=0.3,
            )
            for i in range(5)
        ]
        prompts = handler.generate_confirmation_prompts(prefs, threshold=0.5, max_prompts=2)
        assert len(prompts) == 2

    def test_generate_confirmation_prompts_sorted_by_confidence(self, handler):
        """Test prompts are sorted by confidence (lowest first)."""
        prefs = [
            UserStandupPreference(
                user_id="user-123",
                preference_type=PreferenceType.CONTENT_FILTER,
                value="high",
                confidence=0.45,
            ),
            UserStandupPreference(
                user_id="user-123",
                preference_type=PreferenceType.CONTENT_FILTER,
                value="low",
                confidence=0.3,
            ),
        ]
        prompts = handler.generate_confirmation_prompts(prefs, threshold=0.5, max_prompts=1)
        assert len(prompts) == 1
        assert "low" in prompts[0].question  # Lowest confidence first

    def test_generate_confirmation_prompt_content_filter(self, handler):
        """Test prompt text for content filter preference."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            value="github",
            confidence=0.4,
        )
        prompts = handler.generate_confirmation_prompts([pref], threshold=0.5)
        assert "focus on github" in prompts[0].question.lower()

    def test_generate_confirmation_prompt_exclusion(self, handler):
        """Test prompt text for exclusion preference."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.EXCLUSION,
            value="docs",
            confidence=0.4,
        )
        prompts = handler.generate_confirmation_prompts([pref], threshold=0.5)
        assert "skip docs" in prompts[0].question.lower()

    def test_generate_confirmation_prompt_format(self, handler):
        """Test prompt text for format preference."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            value="brief",
            confidence=0.4,
        )
        prompts = handler.generate_confirmation_prompts([pref], threshold=0.5)
        assert "brief format" in prompts[0].question.lower()

    # =========================================================================
    # Full Feedback Handling Tests
    # =========================================================================

    @pytest.mark.asyncio
    async def test_handle_feedback_no_action(self, handler):
        """Test handling message with no feedback intent."""
        result = await handler.handle_feedback_message(
            "user-123",
            "what's on my calendar?",
            [],
        )
        assert result["type"] == "none"
        assert result["preference_updated"] is False

    @pytest.mark.asyncio
    async def test_handle_feedback_confirmation(self, handler):
        """Test handling confirmation of pending preference."""
        pending = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            value="github",
            confidence=0.4,
        )
        result = await handler.handle_feedback_message(
            "user-123",
            "yes, that's right",
            [],
            pending_confirmation=pending,
        )
        assert result["type"] == "confirmation"
        assert result["preference_updated"] is True

    @pytest.mark.asyncio
    async def test_handle_feedback_rejection(self, handler):
        """Test handling rejection of pending preference."""
        pending = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            value="github",
            confidence=0.4,
        )
        result = await handler.handle_feedback_message(
            "user-123",
            "no",
            [],
            pending_confirmation=pending,
        )
        assert result["type"] == "rejection"
        assert result["preference_updated"] is True

    @pytest.mark.asyncio
    async def test_handle_feedback_correction(self, handler):
        """Test handling correction message."""
        prefs = [
            UserStandupPreference(
                user_id="user-123",
                preference_type=PreferenceType.CONTENT_FILTER,
                key="focus",
                value="github",
            )
        ]
        result = await handler.handle_feedback_message(
            "user-123",
            "no, focus on calendar",
            prefs,
        )
        assert result["type"] == "correction"
        assert "correction" in result


class TestConvenienceFunction:
    """Tests for convenience function."""

    @pytest.mark.asyncio
    async def test_handle_preference_feedback(self):
        """Test convenience function works."""
        result = await handle_preference_feedback(
            "test-user",
            "looks good",
            [],
        )
        assert isinstance(result, dict)
        assert "type" in result
