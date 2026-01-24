"""
Unit tests for TrustIntegration.

Issue #648: TRUST-LEVELS-2 - Integration
ADR-053: Trust Computation Architecture

Tests the integration layer between intent processing and trust computation.
"""

from dataclasses import dataclass
from typing import Optional
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import UserTrustProfile
from services.shared_types import TrustStage
from services.trust.trust_integration import TrustIntegration


@dataclass
class MockIntentProcessingResult:
    """Mock IntentProcessingResult for testing."""

    success: bool
    message: str
    error: Optional[str] = None


class TestTrustIntegrationInit:
    """Test TrustIntegration initialization."""

    def test_init_with_trust_service(self):
        """TrustIntegration initializes with all components."""
        mock_service = MagicMock()
        integration = TrustIntegration(mock_service)

        assert integration.trust_service == mock_service
        assert integration.outcome_classifier is not None
        assert integration.signal_detector is not None
        assert integration.proactivity_gate is not None


class TestProcessInteraction:
    """Test process_interaction method."""

    @pytest.fixture
    def mock_trust_service(self):
        """Create mock TrustComputationService."""
        service = AsyncMock()
        service.get_trust_stage.return_value = TrustStage.NEW
        service.record_interaction.return_value = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.NEW,
        )
        service.progress_to_trusted.return_value = None  # Usually fails (not at ESTABLISHED)
        return service

    @pytest.fixture
    def integration(self, mock_trust_service):
        """Create TrustIntegration instance."""
        return TrustIntegration(mock_trust_service)

    @pytest.mark.asyncio
    async def test_successful_interaction_records_outcome(self, integration, mock_trust_service):
        """Successful interaction records outcome."""
        user_id = uuid4()
        result = MockIntentProcessingResult(success=True, message="Done!")

        outcome = await integration.process_interaction(
            user_id=user_id,
            user_message="thanks",
            processing_result=result,
        )

        # Should have recorded interaction
        mock_trust_service.record_interaction.assert_called_once()
        call_args = mock_trust_service.record_interaction.call_args
        assert call_args.kwargs["user_id"] == user_id

    @pytest.mark.asyncio
    async def test_gratitude_message_is_successful(self, integration, mock_trust_service):
        """Gratitude expression results in successful outcome."""
        user_id = uuid4()
        result = MockIntentProcessingResult(success=True, message="Done!")

        outcome = await integration.process_interaction(
            user_id=user_id,
            user_message="thanks so much!",
            processing_result=result,
        )

        # Check outcome was successful
        call_args = mock_trust_service.record_interaction.call_args
        assert call_args.kwargs["outcome"] == "successful"

    @pytest.mark.asyncio
    async def test_complaint_message_is_negative(self, integration, mock_trust_service):
        """Complaint results in negative outcome."""
        user_id = uuid4()
        result = MockIntentProcessingResult(success=True, message="Done")

        outcome = await integration.process_interaction(
            user_id=user_id,
            user_message="stop doing that",
            processing_result=result,
        )

        # Complaint signal should be detected
        assert outcome["complaint_detected"] is True
        assert outcome["outcome"] == "negative"

    @pytest.mark.asyncio
    async def test_error_in_result_influences_outcome(self, integration, mock_trust_service):
        """Error in processing result influences outcome classification."""
        user_id = uuid4()
        result = MockIntentProcessingResult(
            success=False, message="Failed", error="Something went wrong"
        )

        outcome = await integration.process_interaction(
            user_id=user_id,
            user_message="ok",  # Neutral message
            processing_result=result,
        )

        # Error context should push toward negative
        call_args = mock_trust_service.record_interaction.call_args
        # The context-based classification should detect error
        assert (
            "error" in call_args.kwargs["context"].lower()
            or call_args.kwargs["outcome"] == "negative"
        )


class TestEscalationSignalHandling:
    """Test escalation signal detection and handling."""

    @pytest.fixture
    def mock_trust_service(self):
        """Create mock TrustComputationService."""
        service = AsyncMock()
        service.get_trust_stage.return_value = TrustStage.ESTABLISHED
        service.record_interaction.return_value = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.ESTABLISHED,
        )
        # progress_to_trusted succeeds when at ESTABLISHED
        service.progress_to_trusted.return_value = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.TRUSTED,
        )
        return service

    @pytest.fixture
    def integration(self, mock_trust_service):
        """Create TrustIntegration instance."""
        return TrustIntegration(mock_trust_service)

    @pytest.mark.asyncio
    async def test_escalation_triggers_progress_to_trusted(self, integration, mock_trust_service):
        """Escalation signal triggers progress_to_trusted."""
        user_id = uuid4()
        result = MockIntentProcessingResult(success=True, message="Done")

        outcome = await integration.process_interaction(
            user_id=user_id,
            user_message="I trust you, just handle it",
            processing_result=result,
        )

        # Should have called progress_to_trusted
        mock_trust_service.progress_to_trusted.assert_called_once()
        assert outcome["escalation_detected"] is True
        assert outcome["stage_changed"] is True

    @pytest.mark.asyncio
    async def test_escalation_without_established_stage(self):
        """Escalation signal without ESTABLISHED stage doesn't progress."""
        mock_service = AsyncMock()
        mock_service.get_trust_stage.return_value = TrustStage.BUILDING
        # progress_to_trusted returns None (user not at ESTABLISHED)
        mock_service.progress_to_trusted.return_value = None
        mock_service.record_interaction.return_value = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.BUILDING,
        )

        integration = TrustIntegration(mock_service)
        user_id = uuid4()
        result = MockIntentProcessingResult(success=True, message="Done")

        outcome = await integration.process_interaction(
            user_id=user_id,
            user_message="I trust you, just handle it",
            processing_result=result,
        )

        # Escalation detected but stage didn't change
        mock_service.progress_to_trusted.assert_called_once()
        # Since progress_to_trusted returned None, we fall through to normal recording
        mock_service.record_interaction.assert_called_once()


class TestGetProactivityConfig:
    """Test get_proactivity_config method."""

    @pytest.fixture
    def mock_trust_service(self):
        """Create mock TrustComputationService."""
        return AsyncMock()

    @pytest.fixture
    def integration(self, mock_trust_service):
        """Create TrustIntegration instance."""
        return TrustIntegration(mock_trust_service)

    @pytest.mark.asyncio
    async def test_returns_config_for_new_stage(self, integration, mock_trust_service):
        """Returns restrictive config for NEW stage."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.NEW
        user_id = uuid4()

        config = await integration.get_proactivity_config(user_id)

        assert config["can_offer_hints"] is False
        assert config["can_suggest"] is False
        assert config["can_act_autonomously"] is False
        assert config["trust_stage"] == TrustStage.NEW.value
        assert config["trust_stage_name"] == "NEW"

    @pytest.mark.asyncio
    async def test_returns_config_for_trusted_stage(self, integration, mock_trust_service):
        """Returns full config for TRUSTED stage."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.TRUSTED
        user_id = uuid4()

        config = await integration.get_proactivity_config(user_id)

        assert config["can_offer_hints"] is True
        assert config["can_suggest"] is True
        assert config["can_act_autonomously"] is True
        assert config["trust_stage"] == TrustStage.TRUSTED.value

    @pytest.mark.asyncio
    async def test_handles_error_gracefully(self, integration, mock_trust_service):
        """Returns safe defaults on error."""
        mock_trust_service.get_trust_stage.side_effect = Exception("DB error")
        user_id = uuid4()

        config = await integration.get_proactivity_config(user_id)

        # Should return NEW stage defaults
        assert config["can_offer_hints"] is False
        assert config["trust_stage"] == 1


class TestShouldBeProactive:
    """Test should_be_proactive convenience method."""

    @pytest.fixture
    def mock_trust_service(self):
        """Create mock TrustComputationService."""
        return AsyncMock()

    @pytest.fixture
    def integration(self, mock_trust_service):
        """Create TrustIntegration instance."""
        return TrustIntegration(mock_trust_service)

    @pytest.mark.asyncio
    async def test_hints_allowed_at_building(self, integration, mock_trust_service):
        """Hints allowed at BUILDING stage."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.BUILDING
        user_id = uuid4()

        result = await integration.should_be_proactive(user_id, "hints")

        assert result is True

    @pytest.mark.asyncio
    async def test_suggestions_not_allowed_at_building(self, integration, mock_trust_service):
        """Suggestions not allowed at BUILDING stage."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.BUILDING
        user_id = uuid4()

        result = await integration.should_be_proactive(user_id, "suggestions")

        assert result is False

    @pytest.mark.asyncio
    async def test_autonomous_only_at_trusted(self, integration, mock_trust_service):
        """Autonomous action only at TRUSTED stage."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.ESTABLISHED
        user_id = uuid4()

        result = await integration.should_be_proactive(user_id, "autonomous")

        assert result is False

        # Now at TRUSTED
        mock_trust_service.get_trust_stage.return_value = TrustStage.TRUSTED
        result = await integration.should_be_proactive(user_id, "autonomous")

        assert result is True

    @pytest.mark.asyncio
    async def test_unknown_behavior_returns_false(self, integration, mock_trust_service):
        """Unknown behavior type returns False."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.TRUSTED
        user_id = uuid4()

        result = await integration.should_be_proactive(user_id, "unknown_behavior")

        assert result is False

    @pytest.mark.asyncio
    async def test_error_returns_false(self, integration, mock_trust_service):
        """Error in lookup returns False."""
        mock_trust_service.get_trust_stage.side_effect = Exception("DB error")
        user_id = uuid4()

        result = await integration.should_be_proactive(user_id, "hints")

        assert result is False


class TestGetWelcomeBackMessage:
    """Test welcome back message for returning users."""

    @pytest.fixture
    def mock_trust_service(self):
        """Create mock TrustComputationService."""
        return AsyncMock()

    @pytest.fixture
    def integration(self, mock_trust_service):
        """Create TrustIntegration instance."""
        return TrustIntegration(mock_trust_service)

    @pytest.mark.asyncio
    async def test_returns_message_for_regressed_user(self, integration, mock_trust_service):
        """Returns welcome back message for regressed user."""
        mock_trust_service.explain_trust_state.return_value = (
            "We're still getting to know each other."
        )
        user_id = uuid4()

        message = await integration.get_welcome_back_message(user_id)

        assert message is not None
        assert "welcome back" in message.lower()

    @pytest.mark.asyncio
    async def test_returns_none_for_established_user(self, integration, mock_trust_service):
        """Returns None for established user (no regression)."""
        mock_trust_service.explain_trust_state.return_value = (
            "We've had 50 successful interactions."
        )
        user_id = uuid4()

        message = await integration.get_welcome_back_message(user_id)

        assert message is None


class TestErrorHandling:
    """Test error handling in integration."""

    @pytest.mark.asyncio
    async def test_process_interaction_handles_errors(self):
        """process_interaction handles errors gracefully."""
        mock_service = AsyncMock()
        mock_service.record_interaction.side_effect = Exception("DB error")

        integration = TrustIntegration(mock_service)
        user_id = uuid4()
        result = MockIntentProcessingResult(success=True, message="Done")

        # Should not raise
        outcome = await integration.process_interaction(
            user_id=user_id,
            user_message="thanks",
            processing_result=result,
        )

        # Should return safe defaults
        assert outcome["outcome"] == "neutral"
        assert "error" in outcome


class TestIntegrationStateless:
    """Test that integration is stateless per-request."""

    @pytest.mark.asyncio
    async def test_multiple_users_independent(self):
        """Multiple users' interactions are independent."""
        mock_service = AsyncMock()
        mock_service.get_trust_stage.return_value = TrustStage.NEW
        mock_service.record_interaction.return_value = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.NEW,
        )

        integration = TrustIntegration(mock_service)

        user1 = uuid4()
        user2 = uuid4()
        result = MockIntentProcessingResult(success=True, message="Done")

        # Process for user 1
        await integration.process_interaction(
            user_id=user1,
            user_message="thanks",
            processing_result=result,
        )

        # Process for user 2
        await integration.process_interaction(
            user_id=user2,
            user_message="stop that",
            processing_result=result,
        )

        # Both calls should have been made independently
        assert mock_service.record_interaction.call_count == 2
