"""
Unit tests for TrustComputationService.

Issue #647: TRUST-LEVELS-1 - Core Infrastructure
ADR-053: Trust Computation Architecture

Tests service logic using mocked repository.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import TrustEvent, UserTrustProfile
from services.shared_types import TrustStage
from services.trust.trust_computation_service import (
    MAX_CONSECUTIVE_NEGATIVE,
    STAGE_THRESHOLDS,
    TrustComputationService,
)


class TestTrustComputationServiceInit:
    """Test service initialization."""

    def test_init_with_repository(self):
        """Service initializes with repository."""
        mock_repo = MagicMock()
        service = TrustComputationService(mock_repo)
        assert service.repository == mock_repo


class TestGetTrustStage:
    """Test get_trust_stage method."""

    @pytest.fixture
    def mock_repo(self):
        """Create mock repository."""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repo):
        """Create service with mock repo."""
        return TrustComputationService(mock_repo)

    @pytest.mark.asyncio
    async def test_returns_new_for_no_profile(self, service, mock_repo):
        """Returns NEW stage for users without a profile."""
        mock_repo.get_by_user_id.return_value = None
        user_id = uuid4()

        stage = await service.get_trust_stage(user_id)

        assert stage == TrustStage.NEW
        mock_repo.get_by_user_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_returns_profile_stage(self, service, mock_repo):
        """Returns the stage from user's profile."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
        )
        mock_repo.get_by_user_id.return_value = profile

        stage = await service.get_trust_stage(user_id)

        assert stage == TrustStage.BUILDING


class TestShouldOfferProactiveHelp:
    """Test should_offer_proactive_help method."""

    @pytest.fixture
    def service(self):
        """Create service without repo (not needed for this method)."""
        return TrustComputationService(MagicMock())

    def test_new_stage_no_proactive_help(self, service):
        """NEW stage: no proactive help."""
        assert service.should_offer_proactive_help(TrustStage.NEW) is False

    def test_building_stage_proactive_help(self, service):
        """BUILDING stage: offer proactive help."""
        assert service.should_offer_proactive_help(TrustStage.BUILDING) is True

    def test_established_stage_proactive_help(self, service):
        """ESTABLISHED stage: offer proactive help."""
        assert service.should_offer_proactive_help(TrustStage.ESTABLISHED) is True

    def test_trusted_stage_proactive_help(self, service):
        """TRUSTED stage: offer proactive help."""
        assert service.should_offer_proactive_help(TrustStage.TRUSTED) is True


class TestGetProactivityStyle:
    """Test get_proactivity_style method."""

    @pytest.fixture
    def service(self):
        """Create service without repo."""
        return TrustComputationService(MagicMock())

    def test_new_stage_style(self, service):
        """NEW stage: responsive only."""
        assert service.get_proactivity_style(TrustStage.NEW) == "responsive_only"

    def test_building_stage_style(self, service):
        """BUILDING stage: offer after completion."""
        assert service.get_proactivity_style(TrustStage.BUILDING) == "offer_after_completion"

    def test_established_stage_style(self, service):
        """ESTABLISHED stage: suggest contextually."""
        assert service.get_proactivity_style(TrustStage.ESTABLISHED) == "suggest_contextually"

    def test_trusted_stage_style(self, service):
        """TRUSTED stage: anticipate needs."""
        assert service.get_proactivity_style(TrustStage.TRUSTED) == "anticipate_needs"


class TestRecordInteraction:
    """Test record_interaction method."""

    @pytest.fixture
    def mock_repo(self):
        """Create mock repository with default behavior."""
        repo = AsyncMock()
        # Default: no existing profile
        repo.get_by_user_id.return_value = None
        # Default: record_event returns a new profile
        repo.record_event.return_value = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.NEW,
            successful_count=1,
        )
        return repo

    @pytest.fixture
    def service(self, mock_repo):
        """Create service with mock repo."""
        return TrustComputationService(mock_repo)

    @pytest.mark.asyncio
    async def test_rejects_invalid_outcome(self, service):
        """Rejects invalid outcome values."""
        with pytest.raises(ValueError, match="Invalid outcome"):
            await service.record_interaction(uuid4(), "invalid", "test")

    @pytest.mark.asyncio
    async def test_accepts_valid_outcomes(self, service, mock_repo):
        """Accepts valid outcome values."""
        for outcome in ("successful", "neutral", "negative"):
            await service.record_interaction(uuid4(), outcome, "test")

    @pytest.mark.asyncio
    async def test_creates_trust_event(self, service, mock_repo):
        """Creates TrustEvent and records it."""
        user_id = uuid4()

        await service.record_interaction(user_id, "successful", "Test context")

        # Verify record_event was called with user_id and a TrustEvent
        mock_repo.record_event.assert_called_once()
        call_args = mock_repo.record_event.call_args
        assert call_args[0][0] == user_id
        event = call_args[0][1]
        assert isinstance(event, TrustEvent)
        assert event.outcome == "successful"
        assert event.context == "Test context"


class TestStageProgression:
    """Test stage progression logic."""

    @pytest.fixture
    def mock_repo(self):
        """Create mock repository."""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repo):
        """Create service with mock repo."""
        return TrustComputationService(mock_repo)

    @pytest.mark.asyncio
    async def test_new_to_building_threshold(self, service, mock_repo):
        """NEW→BUILDING at 10 successful interactions."""
        user_id = uuid4()
        # Profile at NEW with 10 successful (just hit threshold)
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.NEW,
            successful_count=10,
        )
        mock_repo.get_by_user_id.return_value = profile

        # Mock update_stage to return progressed profile
        progressed_profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
            successful_count=10,
        )
        mock_repo.update_stage.return_value = progressed_profile

        result = await service._check_stage_progression(user_id, profile)

        mock_repo.update_stage.assert_called_once()
        call_args = mock_repo.update_stage.call_args
        assert call_args[0][1] == TrustStage.BUILDING

    @pytest.mark.asyncio
    async def test_building_to_established_threshold(self, service, mock_repo):
        """BUILDING→ESTABLISHED at 50 successful interactions."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
            successful_count=50,
        )
        mock_repo.get_by_user_id.return_value = profile

        progressed_profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.ESTABLISHED,
            successful_count=50,
        )
        mock_repo.update_stage.return_value = progressed_profile

        result = await service._check_stage_progression(user_id, profile)

        mock_repo.update_stage.assert_called_once()
        call_args = mock_repo.update_stage.call_args
        assert call_args[0][1] == TrustStage.ESTABLISHED

    @pytest.mark.asyncio
    async def test_established_cannot_auto_progress(self, service, mock_repo):
        """ESTABLISHED→TRUSTED requires conversational signals, not auto-progress."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.ESTABLISHED,
            successful_count=100,  # Way above any threshold
        )

        # Should NOT call update_stage
        result = await service._check_stage_progression(user_id, profile)

        mock_repo.update_stage.assert_not_called()
        assert result.current_stage == TrustStage.ESTABLISHED


class TestStageRegression:
    """Test stage regression logic."""

    @pytest.fixture
    def mock_repo(self):
        """Create mock repository."""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repo):
        """Create service with mock repo."""
        return TrustComputationService(mock_repo)

    @pytest.mark.asyncio
    async def test_regresses_after_consecutive_negatives(self, service, mock_repo):
        """Regresses one stage after MAX_CONSECUTIVE_NEGATIVE failures."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
            consecutive_negative=MAX_CONSECUTIVE_NEGATIVE,
        )

        regressed_profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.NEW,
            consecutive_negative=0,
        )
        mock_repo.update_stage.return_value = regressed_profile
        mock_repo.create_or_update.return_value = regressed_profile

        result = await service._check_stage_regression(user_id, profile)

        mock_repo.update_stage.assert_called_once()
        call_args = mock_repo.update_stage.call_args
        assert call_args[0][1] == TrustStage.NEW

    @pytest.mark.asyncio
    async def test_cannot_regress_below_new(self, service, mock_repo):
        """Cannot regress below NEW stage."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.NEW,
            consecutive_negative=MAX_CONSECUTIVE_NEGATIVE,
        )

        result = await service._check_stage_regression(user_id, profile)

        mock_repo.update_stage.assert_not_called()
        assert result.current_stage == TrustStage.NEW

    @pytest.mark.asyncio
    async def test_no_regression_below_threshold(self, service, mock_repo):
        """No regression if below consecutive negative threshold."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
            consecutive_negative=MAX_CONSECUTIVE_NEGATIVE - 1,
        )

        result = await service._check_stage_regression(user_id, profile)

        mock_repo.update_stage.assert_not_called()


class TestProgressToTrusted:
    """Test manual progress_to_trusted method."""

    @pytest.fixture
    def mock_repo(self):
        """Create mock repository."""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repo):
        """Create service with mock repo."""
        return TrustComputationService(mock_repo)

    @pytest.mark.asyncio
    async def test_returns_none_for_no_profile(self, service, mock_repo):
        """Returns None if user has no profile."""
        mock_repo.get_by_user_id.return_value = None

        result = await service.progress_to_trusted(uuid4())

        assert result is None
        mock_repo.update_stage.assert_not_called()

    @pytest.mark.asyncio
    async def test_returns_none_if_not_established(self, service, mock_repo):
        """Returns None if user is not at ESTABLISHED stage."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,  # Not ESTABLISHED
        )
        mock_repo.get_by_user_id.return_value = profile

        result = await service.progress_to_trusted(user_id)

        assert result is None
        mock_repo.update_stage.assert_not_called()

    @pytest.mark.asyncio
    async def test_progresses_established_to_trusted(self, service, mock_repo):
        """Progresses ESTABLISHED user to TRUSTED."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.ESTABLISHED,
        )
        mock_repo.get_by_user_id.return_value = profile

        trusted_profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.TRUSTED,
        )
        mock_repo.update_stage.return_value = trusted_profile

        result = await service.progress_to_trusted(user_id, "User said 'just do it'")

        mock_repo.update_stage.assert_called_once()
        call_args = mock_repo.update_stage.call_args
        assert call_args[0][1] == TrustStage.TRUSTED
        assert "just do it" in call_args[0][2]


class TestExplainTrustState:
    """Test explain_trust_state method for discussability."""

    @pytest.fixture
    def mock_repo(self):
        """Create mock repository."""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repo):
        """Create service with mock repo."""
        return TrustComputationService(mock_repo)

    @pytest.mark.asyncio
    async def test_explanation_for_no_profile(self, service, mock_repo):
        """Provides explanation for users without profile."""
        mock_repo.get_by_user_id.return_value = None

        explanation = await service.explain_trust_state(uuid4())

        assert "haven't worked together" in explanation.lower()

    @pytest.mark.asyncio
    async def test_explanation_for_new_stage(self, service, mock_repo):
        """Provides appropriate explanation for NEW stage."""
        profile = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.NEW,
        )
        mock_repo.get_by_user_id.return_value = profile

        explanation = await service.explain_trust_state(profile.user_id)

        assert "getting to know" in explanation.lower()

    @pytest.mark.asyncio
    async def test_explanation_includes_count_for_building(self, service, mock_repo):
        """BUILDING explanation includes interaction count."""
        profile = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.BUILDING,
            successful_count=15,
        )
        mock_repo.get_by_user_id.return_value = profile

        explanation = await service.explain_trust_state(profile.user_id)

        assert "15" in explanation


class TestStageThresholds:
    """Test calibration thresholds per ADR-053."""

    def test_building_threshold(self):
        """BUILDING threshold is 10."""
        assert STAGE_THRESHOLDS[TrustStage.BUILDING] == 10

    def test_established_threshold(self):
        """ESTABLISHED threshold is 50."""
        assert STAGE_THRESHOLDS[TrustStage.ESTABLISHED] == 50

    def test_trusted_has_no_auto_threshold(self):
        """TRUSTED has no auto threshold (requires signals)."""
        assert STAGE_THRESHOLDS[TrustStage.TRUSTED] is None

    def test_max_consecutive_negative(self):
        """Max consecutive negative is 3."""
        assert MAX_CONSECUTIVE_NEGATIVE == 3
