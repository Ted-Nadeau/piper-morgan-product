"""
Unit tests for TrustExplainer service.

Tests verify that explanations:
1. Pass the Contractor Test (professional, not robotic)
2. Don't leak internal jargon
3. Are appropriate to each trust stage
4. Handle edge cases gracefully
"""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.shared_types import TrustStage
from services.trust.trust_explainer import ExplanationContext, TrustExplainer


@pytest.fixture
def mock_trust_service():
    """Create mock trust service for testing."""
    service = MagicMock()
    service.get_trust_stage = AsyncMock(return_value=TrustStage.NEW)
    service.explain_trust_state = AsyncMock(return_value="We're still getting to know each other.")
    return service


@pytest.fixture
def explainer(mock_trust_service):
    """Create TrustExplainer with mock service."""
    return TrustExplainer(mock_trust_service)


@pytest.fixture
def user_id():
    """Generate test user ID."""
    return uuid4()


class TestTrustExplainerInit:
    """Tests for TrustExplainer initialization."""

    def test_init_with_trust_service(self, mock_trust_service):
        """Should initialize with trust service."""
        explainer = TrustExplainer(mock_trust_service)
        assert explainer._trust_service is mock_trust_service


class TestExplainCurrentStage:
    """Tests for explain_current_stage method."""

    @pytest.mark.asyncio
    async def test_delegates_to_trust_service(self, explainer, mock_trust_service, user_id):
        """Should delegate to existing explain_trust_state."""
        result = await explainer.explain_current_stage(user_id)

        mock_trust_service.explain_trust_state.assert_called_once_with(user_id)
        assert result == "We're still getting to know each other."

    @pytest.mark.asyncio
    async def test_returns_string(self, explainer, user_id):
        """Should return a string explanation."""
        result = await explainer.explain_current_stage(user_id)
        assert isinstance(result, str)
        assert len(result) > 0


class TestExplainProactiveAction:
    """Tests for explain_proactive_action method."""

    @pytest.mark.asyncio
    async def test_trusted_stage_includes_action(self, explainer, mock_trust_service, user_id):
        """Trusted users get explanation referencing the action."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.TRUSTED

        result = await explainer.explain_proactive_action(
            user_id, action="rescheduled your meeting"
        )

        assert "rescheduled your meeting" in result
        assert "latitude" in result or "proactively" in result

    @pytest.mark.asyncio
    async def test_established_stage_acknowledges_should_confirm(
        self, explainer, mock_trust_service, user_id
    ):
        """Established users get apology for not confirming."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.ESTABLISHED

        result = await explainer.explain_proactive_action(
            user_id, action="suggested a meeting time"
        )

        assert "suggested a meeting time" in result
        assert "confirm" in result.lower() or "ask" in result.lower()

    @pytest.mark.asyncio
    async def test_new_stage_expresses_confusion(self, explainer, mock_trust_service, user_id):
        """New users shouldn't see proactive actions - express confusion."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.NEW

        result = await explainer.explain_proactive_action(user_id, action="sent an email")

        assert "not sure" in result.lower() or "typically" in result.lower()

    @pytest.mark.asyncio
    async def test_includes_context_when_provided(self, explainer, mock_trust_service, user_id):
        """Should include additional context in explanation."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.TRUSTED

        result = await explainer.explain_proactive_action(
            user_id,
            action="moved the deadline",
            context="I noticed a conflict with another meeting.",
        )

        assert "conflict" in result.lower()

    @pytest.mark.asyncio
    async def test_includes_followup_offer(self, explainer, mock_trust_service, user_id):
        """Should offer to adjust behavior."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.TRUSTED

        result = await explainer.explain_proactive_action(user_id, action="did something")

        assert "let me know" in result.lower() or "prefer" in result.lower()


class TestExplainWhyNotProactive:
    """Tests for explain_why_not_proactive method."""

    @pytest.mark.asyncio
    async def test_new_stage_mentions_getting_to_know(self, explainer, mock_trust_service, user_id):
        """New users hear about building relationship."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.NEW

        result = await explainer.explain_why_not_proactive(user_id)

        assert "getting to know" in result.lower() or "still" in result.lower()

    @pytest.mark.asyncio
    async def test_building_stage_mentions_learning(self, explainer, mock_trust_service, user_id):
        """Building users hear about learning preferences."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.BUILDING

        result = await explainer.explain_why_not_proactive(user_id)

        assert "learning" in result.lower() or "preferences" in result.lower()

    @pytest.mark.asyncio
    async def test_established_stage_offers_escalation(
        self, explainer, mock_trust_service, user_id
    ):
        """Established users get hint about escalation phrases."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.ESTABLISHED

        result = await explainer.explain_why_not_proactive(user_id)

        assert "just handle it" in result.lower() or "autonomous" in result.lower()

    @pytest.mark.asyncio
    async def test_trusted_stage_notes_already_proactive(
        self, explainer, mock_trust_service, user_id
    ):
        """Trusted users are reminded they already get proactive help."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.TRUSTED

        result = await explainer.explain_why_not_proactive(user_id)

        assert "proactively" in result.lower() or "handle" in result.lower()


class TestExplainBehaviorChange:
    """Tests for explain_behavior_change method."""

    @pytest.mark.asyncio
    async def test_progression_new_to_building(self, explainer, user_id):
        """Explains progression from NEW to BUILDING."""
        result = await explainer.explain_behavior_change(
            user_id, TrustStage.NEW, TrustStage.BUILDING
        )

        assert "suggestions" in result.lower() or "offer" in result.lower()

    @pytest.mark.asyncio
    async def test_progression_building_to_established(self, explainer, user_id):
        """Explains progression from BUILDING to ESTABLISHED."""
        result = await explainer.explain_behavior_change(
            user_id, TrustStage.BUILDING, TrustStage.ESTABLISHED
        )

        assert "proactive" in result.lower()

    @pytest.mark.asyncio
    async def test_progression_established_to_trusted(self, explainer, user_id):
        """Explains progression from ESTABLISHED to TRUSTED."""
        result = await explainer.explain_behavior_change(
            user_id, TrustStage.ESTABLISHED, TrustStage.TRUSTED
        )

        assert "autonomously" in result.lower() or "routine" in result.lower()

    @pytest.mark.asyncio
    async def test_regression_explains_stepping_back(self, explainer, user_id):
        """Explains regression with care."""
        result = await explainer.explain_behavior_change(
            user_id, TrustStage.ESTABLISHED, TrustStage.BUILDING
        )

        assert "overstepped" in result.lower() or "careful" in result.lower()


class TestContractorTest:
    """Tests that explanations pass the Contractor Test."""

    JARGON_TERMS = [
        "TrustStage",
        "Stage 1",
        "Stage 2",
        "Stage 3",
        "Stage 4",
        "BUILDING",
        "ESTABLISHED",
        "TRUSTED",
        "user_id",
        "profile",
        "enum",
        "regression",
    ]

    @pytest.mark.asyncio
    async def test_current_stage_no_jargon(self, explainer, mock_trust_service, user_id):
        """Current stage explanation contains no jargon."""
        # Test with different stage responses
        explanations = [
            "We're still getting to know each other.",
            "We've built a good working relationship.",
        ]
        for explanation in explanations:
            mock_trust_service.explain_trust_state.return_value = explanation
            result = await explainer.explain_current_stage(user_id)

            for jargon in self.JARGON_TERMS:
                assert jargon.lower() not in result.lower(), f"Found jargon: {jargon}"

    @pytest.mark.asyncio
    async def test_proactive_action_no_jargon(self, explainer, mock_trust_service, user_id):
        """Proactive action explanation contains no jargon."""
        for stage in TrustStage:
            mock_trust_service.get_trust_stage.return_value = stage
            result = await explainer.explain_proactive_action(user_id, action="did something")

            for jargon in self.JARGON_TERMS:
                assert jargon.lower() not in result.lower(), f"Found jargon: {jargon}"

    @pytest.mark.asyncio
    async def test_why_not_proactive_no_jargon(self, explainer, mock_trust_service, user_id):
        """Why not proactive explanation contains no jargon."""
        for stage in TrustStage:
            mock_trust_service.get_trust_stage.return_value = stage
            result = await explainer.explain_why_not_proactive(user_id)

            for jargon in self.JARGON_TERMS:
                assert jargon.lower() not in result.lower(), f"Found jargon: {jargon}"

    @pytest.mark.asyncio
    async def test_behavior_change_no_jargon(self, explainer, user_id):
        """Behavior change explanation contains no jargon."""
        for old_stage in TrustStage:
            for new_stage in TrustStage:
                if old_stage != new_stage:
                    result = await explainer.explain_behavior_change(user_id, old_stage, new_stage)

                    for jargon in self.JARGON_TERMS:
                        assert jargon.lower() not in result.lower(), f"Found jargon: {jargon}"


class TestGetFollowupOffer:
    """Tests for get_followup_offer method."""

    def test_current_stage_followup(self, explainer):
        """Current stage gets proactivity preference question."""
        result = explainer.get_followup_offer(ExplanationContext.CURRENT_STAGE)
        assert "proactive" in result.lower()

    def test_proactive_action_followup(self, explainer):
        """Proactive action gets confirmation preference question."""
        result = explainer.get_followup_offer(ExplanationContext.PROACTIVE_ACTION)
        assert "check" in result.lower() or "next time" in result.lower()

    def test_why_not_proactive_followup(self, explainer):
        """Why not proactive gets independence offer."""
        result = explainer.get_followup_offer(ExplanationContext.WHY_NOT_PROACTIVE)
        assert "independently" in result.lower() or "handle" in result.lower()

    def test_behavior_change_followup(self, explainer):
        """Behavior change gets relationship check."""
        result = explainer.get_followup_offer(ExplanationContext.BEHAVIOR_CHANGE)
        assert "feel" in result.lower() or "right" in result.lower()


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_handles_missing_trust_service_gracefully(self, user_id):
        """Should handle None trust service response gracefully."""
        mock_service = MagicMock()
        mock_service.get_trust_stage = AsyncMock(return_value=None)
        mock_service.explain_trust_state = AsyncMock(return_value="Default explanation")

        explainer = TrustExplainer(mock_service)

        # Should not raise, should return default
        result = await explainer.explain_why_not_proactive(user_id)
        assert isinstance(result, str)
