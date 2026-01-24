"""
Tests for session hooks.

Part of #664 MEM-ADR054-P4: Memory Integration.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import ConversationTurn
from services.memory.conversation_summarizer import (
    ConversationSummarizer,
    ConversationSummaryResult,
)
from services.memory.session_hooks import on_session_end, on_session_timeout

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_memory_service():
    """Mock ConversationalMemoryService."""
    service = MagicMock()
    service.record_conversation_end = AsyncMock()
    return service


@pytest.fixture
def sample_turns():
    """Sample conversation turns."""
    return [
        ConversationTurn(
            user_message="Help me with sprint planning",
            assistant_response="Sure, let's start with the backlog",
            entities=["sprint-42"],
        ),
        ConversationTurn(
            user_message="Thanks, that's exactly what I needed!",
            assistant_response="Glad I could help!",
        ),
    ]


# =============================================================================
# on_session_end Tests
# =============================================================================


class TestOnSessionEnd:
    """Tests for on_session_end hook."""

    @pytest.mark.asyncio
    async def test_records_to_memory(self, mock_memory_service, sample_turns):
        """Records conversation summary to memory."""
        result = await on_session_end(
            user_id="user-1",
            conversation_id="conv-1",
            turns=sample_turns,
            memory_service=mock_memory_service,
        )

        assert result is not None
        assert isinstance(result, ConversationSummaryResult)
        mock_memory_service.record_conversation_end.assert_called_once()

    @pytest.mark.asyncio
    async def test_passes_correct_arguments(self, mock_memory_service, sample_turns):
        """Passes correct arguments to memory service."""
        await on_session_end(
            user_id="user-1",
            conversation_id="conv-1",
            turns=sample_turns,
            memory_service=mock_memory_service,
        )

        call_kwargs = mock_memory_service.record_conversation_end.call_args.kwargs
        assert call_kwargs["user_id"] == "user-1"
        assert call_kwargs["conversation_id"] == "conv-1"
        assert "sprint planning" in call_kwargs["summary"]
        assert "sprint-42" in call_kwargs["entities"]

    @pytest.mark.asyncio
    async def test_skips_private_sessions(self, mock_memory_service, sample_turns):
        """Skips recording for private sessions."""
        result = await on_session_end(
            user_id="user-1",
            conversation_id="conv-1",
            turns=sample_turns,
            memory_service=mock_memory_service,
            is_private=True,
        )

        assert result is None
        mock_memory_service.record_conversation_end.assert_not_called()

    @pytest.mark.asyncio
    async def test_skips_empty_conversations(self, mock_memory_service):
        """Skips recording for empty conversations."""
        result = await on_session_end(
            user_id="user-1",
            conversation_id="conv-1",
            turns=[],
            memory_service=mock_memory_service,
        )

        assert result is None
        mock_memory_service.record_conversation_end.assert_not_called()

    @pytest.mark.asyncio
    async def test_uses_custom_summarizer(self, mock_memory_service, sample_turns):
        """Uses custom summarizer when provided."""
        custom_summarizer = MagicMock(spec=ConversationSummarizer)
        custom_summarizer.summarize.return_value = ConversationSummaryResult(
            topic="Custom topic",
            entities=["custom-entity"],
            outcome="completed",
            sentiment="positive",
        )

        result = await on_session_end(
            user_id="user-1",
            conversation_id="conv-1",
            turns=sample_turns,
            memory_service=mock_memory_service,
            summarizer=custom_summarizer,
        )

        custom_summarizer.summarize.assert_called_once_with(sample_turns)
        assert result.topic == "Custom topic"

    @pytest.mark.asyncio
    async def test_returns_summary_result(self, mock_memory_service, sample_turns):
        """Returns the ConversationSummaryResult."""
        result = await on_session_end(
            user_id="user-1",
            conversation_id="conv-1",
            turns=sample_turns,
            memory_service=mock_memory_service,
        )

        assert result.topic is not None
        assert isinstance(result.entities, list)
        assert result.sentiment in ("positive", "neutral", "negative")


class TestOnSessionEndLogging:
    """Tests for logging in on_session_end."""

    @pytest.mark.asyncio
    async def test_logs_success(self, mock_memory_service, sample_turns):
        """Logs successful recording."""
        with patch("services.memory.session_hooks.logger") as mock_logger:
            await on_session_end(
                user_id="user-1",
                conversation_id="conv-1",
                turns=sample_turns,
                memory_service=mock_memory_service,
            )

            mock_logger.info.assert_called()
            call_args = mock_logger.info.call_args
            assert call_args[0][0] == "session_end_recorded"

    @pytest.mark.asyncio
    async def test_logs_private_skip(self, mock_memory_service, sample_turns):
        """Logs when skipping private session."""
        with patch("services.memory.session_hooks.logger") as mock_logger:
            await on_session_end(
                user_id="user-1",
                conversation_id="conv-1",
                turns=sample_turns,
                memory_service=mock_memory_service,
                is_private=True,
            )

            mock_logger.info.assert_called()
            call_args = mock_logger.info.call_args
            assert call_args[0][0] == "session_end_skipped_private"

    @pytest.mark.asyncio
    async def test_logs_empty_skip(self, mock_memory_service):
        """Logs when skipping empty conversation."""
        with patch("services.memory.session_hooks.logger") as mock_logger:
            await on_session_end(
                user_id="user-1",
                conversation_id="conv-1",
                turns=[],
                memory_service=mock_memory_service,
            )

            mock_logger.info.assert_called()
            call_args = mock_logger.info.call_args
            assert call_args[0][0] == "session_end_skipped_empty"


# =============================================================================
# on_session_timeout Tests
# =============================================================================


class TestOnSessionTimeout:
    """Tests for on_session_timeout hook."""

    @pytest.mark.asyncio
    async def test_calls_on_session_end(self, mock_memory_service, sample_turns):
        """Calls on_session_end internally."""
        result = await on_session_timeout(
            user_id="user-1",
            conversation_id="conv-1",
            turns=sample_turns,
            memory_service=mock_memory_service,
        )

        assert result is not None
        mock_memory_service.record_conversation_end.assert_called_once()

    @pytest.mark.asyncio
    async def test_logs_timeout_trigger(self, mock_memory_service, sample_turns):
        """Logs timeout trigger."""
        with patch("services.memory.session_hooks.logger") as mock_logger:
            await on_session_timeout(
                user_id="user-1",
                conversation_id="conv-1",
                turns=sample_turns,
                memory_service=mock_memory_service,
            )

            # Should have at least 2 info calls - timeout trigger and recording
            assert mock_logger.info.call_count >= 2
            first_call = mock_logger.info.call_args_list[0]
            assert first_call[0][0] == "session_timeout_triggered"

    @pytest.mark.asyncio
    async def test_respects_privacy_flag(self, mock_memory_service, sample_turns):
        """Respects is_private flag."""
        result = await on_session_timeout(
            user_id="user-1",
            conversation_id="conv-1",
            turns=sample_turns,
            memory_service=mock_memory_service,
            is_private=True,
        )

        assert result is None
        mock_memory_service.record_conversation_end.assert_not_called()

    @pytest.mark.asyncio
    async def test_uses_custom_summarizer(self, mock_memory_service, sample_turns):
        """Uses custom summarizer when provided."""
        custom_summarizer = MagicMock(spec=ConversationSummarizer)
        custom_summarizer.summarize.return_value = ConversationSummaryResult(
            topic="Timeout topic",
        )

        result = await on_session_timeout(
            user_id="user-1",
            conversation_id="conv-1",
            turns=sample_turns,
            memory_service=mock_memory_service,
            summarizer=custom_summarizer,
        )

        custom_summarizer.summarize.assert_called_once()
        assert result.topic == "Timeout topic"
