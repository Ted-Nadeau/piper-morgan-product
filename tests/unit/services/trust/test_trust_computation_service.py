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
    MINIMUM_STAGE_FLOOR,
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
    async def test_regresses_after_consecutive_negatives_no_floor(self, service, mock_repo):
        """User who never earned Stage 2 can regress to NEW."""
        user_id = uuid4()
        # User is at BUILDING but highest_stage_achieved is NEW (shouldn't happen
        # in practice, but tests the "no floor" case explicitly)
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
            highest_stage_achieved=TrustStage.NEW,  # Never truly earned Stage 2
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

    @pytest.mark.asyncio
    async def test_floor_enforced_stage3_to_stage2(self, service, mock_repo):
        """User at Stage 3 who earned Stage 2 regresses to Stage 2, not Stage 1."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.ESTABLISHED,  # Stage 3
            highest_stage_achieved=TrustStage.ESTABLISHED,  # Earned Stage 3
            consecutive_negative=MAX_CONSECUTIVE_NEGATIVE,
        )

        regressed_profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,  # Stage 2 (floor)
            consecutive_negative=0,
        )
        mock_repo.update_stage.return_value = regressed_profile
        mock_repo.create_or_update.return_value = regressed_profile

        result = await service._check_stage_regression(user_id, profile)

        mock_repo.update_stage.assert_called_once()
        call_args = mock_repo.update_stage.call_args
        # Should regress to BUILDING (Stage 2), not NEW
        assert call_args[0][1] == TrustStage.BUILDING

    @pytest.mark.asyncio
    async def test_floor_enforced_stage2_stays_at_stage2(self, service, mock_repo):
        """User at Stage 2 who earned Stage 2 stays at Stage 2 (floor)."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,  # Stage 2
            highest_stage_achieved=TrustStage.BUILDING,  # Earned Stage 2
            consecutive_negative=MAX_CONSECUTIVE_NEGATIVE,
        )

        result = await service._check_stage_regression(user_id, profile)

        # Should NOT regress - already at floor
        mock_repo.update_stage.assert_not_called()
        assert result.current_stage == TrustStage.BUILDING

    @pytest.mark.asyncio
    async def test_floor_enforced_stage4_to_stage3(self, service, mock_repo):
        """User at Stage 4 regresses to Stage 3 (one step), not Stage 2."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.TRUSTED,  # Stage 4
            highest_stage_achieved=TrustStage.TRUSTED,  # Earned Stage 4
            consecutive_negative=MAX_CONSECUTIVE_NEGATIVE,
        )

        regressed_profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.ESTABLISHED,  # Stage 3
            consecutive_negative=0,
        )
        mock_repo.update_stage.return_value = regressed_profile
        mock_repo.create_or_update.return_value = regressed_profile

        result = await service._check_stage_regression(user_id, profile)

        mock_repo.update_stage.assert_called_once()
        call_args = mock_repo.update_stage.call_args
        # Should regress to ESTABLISHED (Stage 3), one step down
        assert call_args[0][1] == TrustStage.ESTABLISHED


class TestGetFloor:
    """Test _get_floor helper method for floor enforcement."""

    @pytest.fixture
    def service(self):
        """Create service with mock repo."""
        return TrustComputationService(AsyncMock())

    def test_floor_is_building_when_earned_building(self, service):
        """Floor is BUILDING when user has reached BUILDING."""
        profile = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.BUILDING,
            highest_stage_achieved=TrustStage.BUILDING,
        )
        assert service._get_floor(profile) == TrustStage.BUILDING

    def test_floor_is_building_when_earned_established(self, service):
        """Floor is BUILDING when user has reached ESTABLISHED."""
        profile = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.ESTABLISHED,
            highest_stage_achieved=TrustStage.ESTABLISHED,
        )
        assert service._get_floor(profile) == TrustStage.BUILDING

    def test_floor_is_building_when_earned_trusted(self, service):
        """Floor is BUILDING when user has reached TRUSTED."""
        profile = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.TRUSTED,
            highest_stage_achieved=TrustStage.TRUSTED,
        )
        assert service._get_floor(profile) == TrustStage.BUILDING

    def test_floor_is_new_when_never_earned_building(self, service):
        """Floor is NEW when user has never reached BUILDING."""
        profile = UserTrustProfile(
            user_id=uuid4(),
            current_stage=TrustStage.NEW,
            highest_stage_achieved=TrustStage.NEW,
        )
        assert service._get_floor(profile) == TrustStage.NEW

    def test_minimum_stage_floor_constant(self):
        """Verify MINIMUM_STAGE_FLOOR is BUILDING."""
        assert MINIMUM_STAGE_FLOOR == TrustStage.BUILDING


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


class TestHandleExplicitComplaint:
    """Test handle_explicit_complaint method for immediate Stage 2 regression."""

    @pytest.fixture
    def mock_repo(self):
        """Create mock repository."""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repo):
        """Create service with mock repo."""
        return TrustComputationService(mock_repo)

    @pytest.mark.asyncio
    async def test_stage4_drops_to_stage2(self, service, mock_repo):
        """User at Stage 4 (TRUSTED) drops immediately to Stage 2 (BUILDING)."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.TRUSTED,
            highest_stage_achieved=TrustStage.TRUSTED,
        )
        mock_repo.get_by_user_id.return_value = profile

        building_profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
            consecutive_negative=0,
        )
        mock_repo.update_stage.return_value = building_profile
        mock_repo.create_or_update.return_value = building_profile

        result = await service.handle_explicit_complaint(user_id, "Stop doing that")

        mock_repo.update_stage.assert_called_once()
        call_args = mock_repo.update_stage.call_args
        assert call_args[0][1] == TrustStage.BUILDING
        assert "Stop doing that" in call_args[0][2]

    @pytest.mark.asyncio
    async def test_stage3_drops_to_stage2(self, service, mock_repo):
        """User at Stage 3 (ESTABLISHED) drops immediately to Stage 2 (BUILDING)."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.ESTABLISHED,
            highest_stage_achieved=TrustStage.ESTABLISHED,
        )
        mock_repo.get_by_user_id.return_value = profile

        building_profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
            consecutive_negative=0,
        )
        mock_repo.update_stage.return_value = building_profile
        mock_repo.create_or_update.return_value = building_profile

        result = await service.handle_explicit_complaint(user_id, "I didn't ask for this")

        mock_repo.update_stage.assert_called_once()
        call_args = mock_repo.update_stage.call_args
        assert call_args[0][1] == TrustStage.BUILDING

    @pytest.mark.asyncio
    async def test_stage2_stays_at_stage2(self, service, mock_repo):
        """User at Stage 2 (BUILDING) stays at Stage 2 (already at floor)."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
            highest_stage_achieved=TrustStage.BUILDING,
            consecutive_negative=2,  # Had some negatives
        )
        mock_repo.get_by_user_id.return_value = profile
        mock_repo.create_or_update.return_value = profile

        result = await service.handle_explicit_complaint(user_id, "Stop it")

        # Should NOT call update_stage since already at BUILDING
        mock_repo.update_stage.assert_not_called()
        # But should still reset consecutive_negative
        assert result.consecutive_negative == 0

    @pytest.mark.asyncio
    async def test_stage1_stays_at_stage1(self, service, mock_repo):
        """User at Stage 1 (NEW) stays at Stage 1."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.NEW,
            highest_stage_achieved=TrustStage.NEW,
        )
        mock_repo.get_by_user_id.return_value = profile
        mock_repo.create_or_update.return_value = profile

        result = await service.handle_explicit_complaint(user_id, "Don't do that")

        # Should NOT call update_stage since NEW < BUILDING
        mock_repo.update_stage.assert_not_called()

    @pytest.mark.asyncio
    async def test_creates_profile_if_none_exists(self, service, mock_repo):
        """Creates profile at BUILDING if user has no profile."""
        user_id = uuid4()
        mock_repo.get_by_user_id.return_value = None

        new_profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
            highest_stage_achieved=TrustStage.BUILDING,
        )
        mock_repo.create_or_update.return_value = new_profile

        result = await service.handle_explicit_complaint(user_id, "Complaint")

        mock_repo.create_or_update.assert_called()
        assert result.current_stage == TrustStage.BUILDING

    @pytest.mark.asyncio
    async def test_resets_consecutive_negative(self, service, mock_repo):
        """Resets consecutive_negative counter after complaint."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.ESTABLISHED,
            consecutive_negative=2,  # Had some negatives before complaint
        )
        mock_repo.get_by_user_id.return_value = profile

        building_profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
            consecutive_negative=2,  # Will be reset
        )
        mock_repo.update_stage.return_value = building_profile
        mock_repo.create_or_update.return_value = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
            consecutive_negative=0,
        )

        result = await service.handle_explicit_complaint(user_id, "Stop")

        # Verify consecutive_negative was reset
        assert result.consecutive_negative == 0

    @pytest.mark.asyncio
    async def test_truncates_long_complaint(self, service, mock_repo):
        """Truncates complaint reason to 100 chars in stage history."""
        user_id = uuid4()
        profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.TRUSTED,
        )
        mock_repo.get_by_user_id.return_value = profile

        building_profile = UserTrustProfile(
            user_id=user_id,
            current_stage=TrustStage.BUILDING,
        )
        mock_repo.update_stage.return_value = building_profile
        mock_repo.create_or_update.return_value = building_profile

        long_complaint = "x" * 200  # 200 chars
        await service.handle_explicit_complaint(user_id, long_complaint)

        call_args = mock_repo.update_stage.call_args
        reason = call_args[0][2]  # Third positional arg is reason
        # Should include truncated complaint (100 chars max)
        assert len(reason) <= 120  # "Explicit complaint: " + 100 chars


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
