"""
Tests for privacy mode service.

Part of #664 MEM-ADR054-P4: Memory Integration.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.memory.privacy_mode import PrivacyModeService, PrivacyReason, PrivacyState

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_history_service():
    """Mock UserHistoryService."""
    service = MagicMock()
    service.mark_private = AsyncMock(return_value=True)
    service.unmark_private = AsyncMock(return_value=True)
    return service


@pytest.fixture
def privacy_service(mock_history_service):
    """PrivacyModeService with mock history service."""
    return PrivacyModeService(history_service=mock_history_service)


@pytest.fixture
def privacy_service_no_history():
    """PrivacyModeService without history service."""
    return PrivacyModeService(history_service=None)


# =============================================================================
# PrivacyState Tests
# =============================================================================


class TestPrivacyState:
    """Tests for PrivacyState dataclass."""

    def test_public_factory(self):
        """Test public() factory method."""
        state = PrivacyState.public()
        assert state.is_private is False
        assert state.reason is None

    def test_private_factory_default_reason(self):
        """Test private() factory with default reason."""
        state = PrivacyState.private()
        assert state.is_private is True
        assert state.reason == PrivacyReason.USER_REQUEST

    def test_private_factory_custom_reason(self):
        """Test private() factory with custom reason."""
        state = PrivacyState.private(PrivacyReason.SENSITIVE_TOPIC)
        assert state.is_private is True
        assert state.reason == PrivacyReason.SENSITIVE_TOPIC

    def test_to_dict_public(self):
        """Test to_dict for public state."""
        state = PrivacyState.public()
        d = state.to_dict()
        assert d == {"is_private": False, "reason": None}

    def test_to_dict_private(self):
        """Test to_dict for private state."""
        state = PrivacyState.private(PrivacyReason.CLIENT_CONFIDENTIAL)
        d = state.to_dict()
        assert d == {"is_private": True, "reason": "client_confidential"}


# =============================================================================
# PrivacyReason Tests
# =============================================================================


class TestPrivacyReason:
    """Tests for PrivacyReason enum."""

    def test_all_reasons_exist(self):
        """All expected reasons are defined."""
        assert PrivacyReason.USER_REQUEST
        assert PrivacyReason.SENSITIVE_TOPIC
        assert PrivacyReason.CLIENT_CONFIDENTIAL
        assert PrivacyReason.PERSONAL

    def test_reason_values(self):
        """Reason values are strings."""
        assert PrivacyReason.USER_REQUEST.value == "user_request"
        assert PrivacyReason.SENSITIVE_TOPIC.value == "sensitive_topic"


# =============================================================================
# PrivacyModeService Session Management Tests
# =============================================================================


class TestSessionPrivacy:
    """Tests for session-level privacy management."""

    def test_start_private_session(self, privacy_service):
        """Starting private session tracks state."""
        state = privacy_service.start_private_session("conv-1")

        assert state.is_private is True
        assert state.reason == PrivacyReason.USER_REQUEST
        assert privacy_service.is_private("conv-1") is True

    def test_start_private_with_reason(self, privacy_service):
        """Starting private session with custom reason."""
        state = privacy_service.start_private_session(
            "conv-1", reason=PrivacyReason.SENSITIVE_TOPIC
        )

        assert state.reason == PrivacyReason.SENSITIVE_TOPIC

    def test_end_private_session(self, privacy_service):
        """Ending private session clears state."""
        privacy_service.start_private_session("conv-1")
        state = privacy_service.end_private_session("conv-1")

        assert state.is_private is False
        assert privacy_service.is_private("conv-1") is False

    def test_is_private_returns_false_by_default(self, privacy_service):
        """Unknown sessions default to public."""
        assert privacy_service.is_private("unknown-conv") is False

    def test_get_privacy_state_returns_public_by_default(self, privacy_service):
        """Unknown sessions return public state."""
        state = privacy_service.get_privacy_state("unknown-conv")
        assert state.is_private is False

    def test_multiple_sessions_independent(self, privacy_service):
        """Multiple sessions have independent privacy states."""
        privacy_service.start_private_session("conv-1")
        privacy_service.start_private_session("conv-2", reason=PrivacyReason.CLIENT_CONFIDENTIAL)

        assert privacy_service.is_private("conv-1") is True
        assert privacy_service.is_private("conv-2") is True
        assert privacy_service.is_private("conv-3") is False

        state_1 = privacy_service.get_privacy_state("conv-1")
        state_2 = privacy_service.get_privacy_state("conv-2")
        assert state_1.reason == PrivacyReason.USER_REQUEST
        assert state_2.reason == PrivacyReason.CLIENT_CONFIDENTIAL

    def test_clear_session_state(self, privacy_service):
        """Clears in-memory state for session."""
        privacy_service.start_private_session("conv-1")
        assert privacy_service.is_private("conv-1") is True

        privacy_service.clear_session_state("conv-1")
        # After clearing, defaults to public
        assert privacy_service.is_private("conv-1") is False

    def test_clear_nonexistent_session_no_error(self, privacy_service):
        """Clearing nonexistent session doesn't raise."""
        privacy_service.clear_session_state("nonexistent")  # Should not raise


# =============================================================================
# PrivacyModeService Retroactive Privacy Tests
# =============================================================================


class TestRetroactivePrivacy:
    """Tests for retroactive privacy operations."""

    @pytest.mark.asyncio
    async def test_retroactively_mark_private(self, privacy_service, mock_history_service):
        """Marking conversation private calls history service."""
        result = await privacy_service.retroactively_mark_private("user-1", "conv-1")

        assert result is True
        mock_history_service.mark_private.assert_called_once_with("user-1", "conv-1")

    @pytest.mark.asyncio
    async def test_retroactively_mark_private_failure(self, privacy_service, mock_history_service):
        """Returns False when history service fails."""
        mock_history_service.mark_private.return_value = False

        result = await privacy_service.retroactively_mark_private("user-1", "conv-1")

        assert result is False

    @pytest.mark.asyncio
    async def test_retroactively_mark_private_no_history_service(self, privacy_service_no_history):
        """Returns False when no history service available."""
        result = await privacy_service_no_history.retroactively_mark_private("user-1", "conv-1")

        assert result is False

    @pytest.mark.asyncio
    async def test_retroactively_unmark_private(self, privacy_service, mock_history_service):
        """Unmarking private calls history service."""
        result = await privacy_service.retroactively_unmark_private("user-1", "conv-1")

        assert result is True
        mock_history_service.unmark_private.assert_called_once_with("user-1", "conv-1")

    @pytest.mark.asyncio
    async def test_retroactively_unmark_private_failure(
        self, privacy_service, mock_history_service
    ):
        """Returns False when history service fails."""
        mock_history_service.unmark_private.return_value = False

        result = await privacy_service.retroactively_unmark_private("user-1", "conv-1")

        assert result is False

    @pytest.mark.asyncio
    async def test_retroactively_unmark_private_no_history_service(
        self, privacy_service_no_history
    ):
        """Returns False when no history service available."""
        result = await privacy_service_no_history.retroactively_unmark_private("user-1", "conv-1")

        assert result is False


# =============================================================================
# Logging Tests
# =============================================================================


class TestPrivacyLogging:
    """Tests for privacy operation logging."""

    def test_logs_private_session_start(self, privacy_service):
        """Logs when private session starts."""
        with patch("services.memory.privacy_mode.logger") as mock_logger:
            privacy_service.start_private_session("conv-1")

            mock_logger.info.assert_called()
            call_args = mock_logger.info.call_args
            assert call_args[0][0] == "private_session_started"

    def test_logs_private_session_end(self, privacy_service):
        """Logs when private session ends."""
        privacy_service.start_private_session("conv-1")

        with patch("services.memory.privacy_mode.logger") as mock_logger:
            privacy_service.end_private_session("conv-1")

            mock_logger.info.assert_called()
            call_args = mock_logger.info.call_args
            assert call_args[0][0] == "private_session_ended"

    @pytest.mark.asyncio
    async def test_logs_retroactive_mark(self, privacy_service, mock_history_service):
        """Logs when retroactively marking private."""
        with patch("services.memory.privacy_mode.logger") as mock_logger:
            await privacy_service.retroactively_mark_private("user-1", "conv-1")

            mock_logger.info.assert_called()
            call_args = mock_logger.info.call_args
            assert call_args[0][0] == "conversation_marked_private"

    @pytest.mark.asyncio
    async def test_logs_retroactive_unmark(self, privacy_service, mock_history_service):
        """Logs when retroactively unmarking private."""
        with patch("services.memory.privacy_mode.logger") as mock_logger:
            await privacy_service.retroactively_unmark_private("user-1", "conv-1")

            mock_logger.info.assert_called()
            call_args = mock_logger.info.call_args
            assert call_args[0][0] == "conversation_unmarked_private"

    @pytest.mark.asyncio
    async def test_logs_warning_no_history_service(self, privacy_service_no_history):
        """Logs warning when history service unavailable."""
        with patch("services.memory.privacy_mode.logger") as mock_logger:
            await privacy_service_no_history.retroactively_mark_private("user-1", "conv-1")

            mock_logger.warning.assert_called()
            call_args = mock_logger.warning.call_args
            assert call_args[0][0] == "retroactive_privacy_unavailable"

    @pytest.mark.asyncio
    async def test_logs_warning_mark_failure(self, privacy_service, mock_history_service):
        """Logs warning when mark operation fails."""
        mock_history_service.mark_private.return_value = False

        with patch("services.memory.privacy_mode.logger") as mock_logger:
            await privacy_service.retroactively_mark_private("user-1", "conv-1")

            mock_logger.warning.assert_called()
            call_args = mock_logger.warning.call_args
            assert call_args[0][0] == "conversation_privacy_failed"
