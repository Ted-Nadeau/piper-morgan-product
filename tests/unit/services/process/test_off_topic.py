"""
Tests for Issue #899: Off-topic detection for guided processes (Layer C).

Tests the conservative regex-based detection of clear non-sequiturs
during active guided processes (onboarding, standup, slot-filling).

PM decisions (2026-03-16):
- Conservative: only clear non-sequiturs
- All 3 process types
- Regex first
- Option A UX: auto-pause + answer question
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from services.process.off_topic import (
    OffTopicConfidence,
    OffTopicResult,
    detect_off_topic,
    format_off_topic_pause_message,
)
from services.process.registry import ProcessCheckResult, ProcessType


# ---- Test detect_off_topic() ----


class TestGenericOffTopicDetection:
    """Test that generic off-topic patterns are detected across all process types."""

    @pytest.mark.parametrize(
        "message",
        [
            "What's the weather like?",
            "Is it raining outside?",
            "What time is it?",
            "What's the time?",
            "What day is it?",
        ],
    )
    def test_weather_time_date_queries_are_off_topic_onboarding(self, message):
        """Weather, time, and date queries are clear non-sequiturs during onboarding."""
        result = detect_off_topic(message, ProcessType.ONBOARDING)
        assert result.is_off_topic, f"'{message}' should be off-topic during onboarding"
        assert result.confidence == OffTopicConfidence.CLEAR

    @pytest.mark.parametrize(
        "message",
        [
            "What's the weather like?",
            "Is it raining outside?",
            "What time is it?",
            "What's the time?",
        ],
    )
    def test_weather_time_queries_off_topic_standup(self, message):
        """Weather/time queries are off-topic during standup (but not date queries
        which contain 'today'/'day' — standup on-topic keywords)."""
        result = detect_off_topic(message, ProcessType.STANDUP)
        assert result.is_off_topic, f"'{message}' should be off-topic during standup"

    @pytest.mark.parametrize(
        "message",
        [
            "Who are you?",
            "What are you?",
            "Tell me about yourself",
        ],
    )
    def test_identity_queries_are_off_topic(self, message):
        """Identity queries about Piper are off-topic during guided processes."""
        result = detect_off_topic(message, ProcessType.ONBOARDING)
        assert result.is_off_topic, f"'{message}' should be off-topic during onboarding"

    @pytest.mark.parametrize(
        "message",
        [
            "What can you do?",
            "What can you help me with?",
            "Show me your capabilities",
        ],
    )
    def test_capability_queries_are_off_topic(self, message):
        """Capability discovery queries are off-topic during guided processes."""
        result = detect_off_topic(message, ProcessType.STANDUP)
        assert result.is_off_topic, f"'{message}' should be off-topic during standup"

    @pytest.mark.parametrize(
        "message",
        [
            "Tell me a joke",
            "Sing me a song",
            "Write me a poem",
        ],
    )
    def test_entertainment_requests_are_off_topic(self, message):
        result = detect_off_topic(message, ProcessType.ONBOARDING)
        assert result.is_off_topic

    def test_topic_change_detected(self):
        result = detect_off_topic(
            "By the way, can you check my calendar?", ProcessType.STANDUP
        )
        assert result.is_off_topic

    def test_utility_request_detected(self):
        result = detect_off_topic(
            "Translate this text to Spanish", ProcessType.ONBOARDING
        )
        assert result.is_off_topic


class TestOnboardingOnTopicPatterns:
    """Test that messages relevant to onboarding are NOT flagged."""

    @pytest.mark.parametrize(
        "message",
        [
            "yes",
            "no",
            "sure",
            "ok",
            "nope",
            "not really",
            "that's all",
            "none",
        ],
    )
    def test_affirmative_negative_responses(self, message):
        """Short affirmative/negative responses are on-topic for onboarding."""
        result = detect_off_topic(message, ProcessType.ONBOARDING)
        assert not result.is_off_topic, f"'{message}' should NOT be off-topic during onboarding"

    @pytest.mark.parametrize(
        "message",
        [
            "https://github.com/my-org/my-project",
            "piper-morgan",
            "My main project is the customer portal",
            "I have a repo called data-pipeline",
        ],
    )
    def test_project_info_is_on_topic(self, message):
        """Project names, URLs, and descriptions are on-topic for onboarding."""
        result = detect_off_topic(message, ProcessType.ONBOARDING)
        assert not result.is_off_topic, f"'{message}' should NOT be off-topic during onboarding"

    def test_short_names_are_on_topic(self):
        """Short text that could be project names are on-topic."""
        result = detect_off_topic("My API Service", ProcessType.ONBOARDING)
        assert not result.is_off_topic

    def test_numbers_are_on_topic(self):
        """Numbers (project counts) are on-topic."""
        result = detect_off_topic("3", ProcessType.ONBOARDING)
        assert not result.is_off_topic


class TestStandupOnTopicPatterns:
    """Test that messages relevant to standup are NOT flagged."""

    @pytest.mark.parametrize(
        "message",
        [
            "I'm working on the API refactor",
            "Finished the PR review yesterday",
            "Blocked on the database migration",
            "I started the new feature branch",
            "Waiting on code review",
            "I'll be done with the bug fix today",
            "Deployed the fix to staging",
        ],
    )
    def test_work_updates_are_on_topic(self, message):
        """Work-related updates are on-topic for standup."""
        result = detect_off_topic(message, ProcessType.STANDUP)
        assert not result.is_off_topic, f"'{message}' should NOT be off-topic during standup"

    @pytest.mark.parametrize(
        "message",
        [
            "yes",
            "nope",
            "nothing else",
            "that's it",
        ],
    )
    def test_affirmative_responses_on_topic(self, message):
        result = detect_off_topic(message, ProcessType.STANDUP)
        assert not result.is_off_topic


class TestSlotFillingOnTopicPatterns:
    """Test that slot-filling is very conservative (short answers are on-topic)."""

    def test_short_answers_are_on_topic(self):
        """Slot filling accepts almost any short message."""
        short_messages = ["high", "3", "next Tuesday", "Alice", "bug fix"]
        for msg in short_messages:
            result = detect_off_topic(msg, ProcessType.SLOT_FILLING)
            assert not result.is_off_topic, f"'{msg}' should NOT be off-topic during slot-filling"

    def test_very_short_messages_on_topic(self):
        """Messages under 3 chars are always on-topic."""
        result = detect_off_topic("ok", ProcessType.SLOT_FILLING)
        assert not result.is_off_topic


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_message(self):
        result = detect_off_topic("", ProcessType.ONBOARDING)
        assert not result.is_off_topic

    def test_whitespace_only(self):
        result = detect_off_topic("   ", ProcessType.ONBOARDING)
        assert not result.is_off_topic

    def test_two_char_message(self):
        """Messages under 3 chars are never off-topic."""
        result = detect_off_topic("no", ProcessType.ONBOARDING)
        assert not result.is_off_topic

    def test_unknown_process_type(self):
        """Non-standard process types should still work (no on-topic patterns, but generic detection runs)."""
        result = detect_off_topic("What's the weather?", ProcessType.PLANNING)
        assert result.is_off_topic

    def test_on_topic_overrides_off_topic(self):
        """On-topic patterns take priority over off-topic patterns.

        E.g., during standup, "I have a meeting today" mentions 'today' (on-topic)
        even though it could be confused with a date query.
        """
        result = detect_off_topic(
            "I have a meeting today about the sprint", ProcessType.STANDUP
        )
        assert not result.is_off_topic

    def test_matched_pattern_is_reported(self):
        """The matched pattern name should be available for logging."""
        result = detect_off_topic("What's the weather?", ProcessType.ONBOARDING)
        assert result.matched_pattern == "weather_query"


# ---- Test format_off_topic_pause_message() ----


class TestPauseMessage:
    """Test the auto-pause UX message formatting."""

    def test_onboarding_pause_message(self):
        msg = format_off_topic_pause_message(ProcessType.ONBOARDING)
        assert "onboarding" in msg
        assert "resume" in msg.lower()

    def test_standup_pause_message(self):
        msg = format_off_topic_pause_message(ProcessType.STANDUP)
        assert "standup" in msg
        assert "resume" in msg.lower()

    def test_slot_filling_pause_message(self):
        msg = format_off_topic_pause_message(ProcessType.SLOT_FILLING)
        assert "resume" in msg.lower()


# ---- Test ProcessCheckResult.off_topic_pause ----


class TestOffTopicPauseResult:
    """Test the ProcessCheckResult.off_topic_pause factory method."""

    def test_off_topic_pause_not_handled(self):
        """off_topic_pause should set handled=False so intent processing continues."""
        result = ProcessCheckResult.off_topic_pause(
            process_type=ProcessType.ONBOARDING,
            pause_message="I've paused onboarding.",
        )
        assert not result.handled
        assert result.escaped
        assert result.process_type == ProcessType.ONBOARDING
        assert result.response_message == "I've paused onboarding."

    def test_off_topic_pause_intent_data(self):
        result = ProcessCheckResult.off_topic_pause(
            process_type=ProcessType.STANDUP,
            pause_message="Paused.",
        )
        assert result.intent_data["action"] == "off_topic_pause"
        assert result.intent_data["context"]["off_topic_detected"] is True
        assert result.intent_data["context"]["bypassed_classification"] is False


# ---- Test Registry Integration ----


class TestRegistryOffTopicIntegration:
    """Test off-topic detection integration with ProcessRegistry."""

    @pytest.fixture
    def registry(self):
        from services.process.registry import ProcessRegistry

        ProcessRegistry.reset_instance()
        reg = ProcessRegistry()
        return reg

    @pytest.fixture
    def mock_handler(self):
        handler = AsyncMock()
        handler.process_type = ProcessType.ONBOARDING
        handler.check_active = AsyncMock(return_value=True)
        handler.handle_message = AsyncMock(
            return_value=ProcessCheckResult.handled_by(
                ProcessType.ONBOARDING, "Next step...", {"category": "guidance"}
            )
        )
        handler.suspend = AsyncMock()
        handler.has_suspended_session = AsyncMock(return_value=None)
        return handler

    @pytest.mark.asyncio
    async def test_on_topic_message_passes_through(self, registry, mock_handler):
        """On-topic messages should be handled normally by the process handler."""
        registry.register(mock_handler)

        result = await registry.check_active_processes(
            user_id="u1", session_id="s1", message="My project is called Dashboard"
        )
        assert result.handled
        mock_handler.handle_message.assert_called_once()
        mock_handler.suspend.assert_not_called()

    @pytest.mark.asyncio
    async def test_off_topic_triggers_suspend(self, registry, mock_handler):
        """Off-topic messages should suspend the process and return off_topic_pause."""
        registry.register(mock_handler)

        result = await registry.check_active_processes(
            user_id="u1", session_id="s1", message="What's the weather?"
        )
        # Process should be suspended
        mock_handler.suspend.assert_called_once()
        # Result should be off_topic_pause (not handled, but escaped)
        assert not result.handled
        assert result.escaped
        # Handler should NOT have processed the message
        mock_handler.handle_message.assert_not_called()

    @pytest.mark.asyncio
    async def test_escape_takes_priority_over_off_topic(self, registry, mock_handler):
        """Escape commands should still work (Layer A > Layer C)."""
        registry.register(mock_handler)

        result = await registry.check_active_processes(
            user_id="u1", session_id="s1", message="cancel"
        )
        assert result.handled  # Escape is handled=True
        assert result.escaped

    @pytest.mark.asyncio
    async def test_off_topic_with_inactive_process(self, registry, mock_handler):
        """If no process is active, off-topic detection doesn't run."""
        mock_handler.check_active = AsyncMock(return_value=False)
        registry.register(mock_handler)

        result = await registry.check_active_processes(
            user_id="u1", session_id="s1", message="What's the weather?"
        )
        assert not result.handled
        assert not result.escaped

    @pytest.mark.asyncio
    async def test_suspend_failure_doesnt_break_off_topic(self, registry, mock_handler):
        """If suspend fails, off-topic pause should still return."""
        mock_handler.suspend = AsyncMock(side_effect=Exception("DB error"))
        registry.register(mock_handler)

        result = await registry.check_active_processes(
            user_id="u1", session_id="s1", message="What's the weather?"
        )
        # Should still return off_topic_pause despite suspend failure
        assert not result.handled
        assert result.escaped
