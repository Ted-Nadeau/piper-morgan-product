"""
Tests for DelegationService.

Part of #414 MUX-INTERACT-DELEGATION.

Tests cover:
- Trust × Risk matrix correctness
- Delegation type ordering
- Language pattern formatting
- Edge cases and safety guarantees
"""

import pytest

from services.shared_types import DelegationType, RiskLevel, TrustStage
from services.trust.delegation import DELEGATION_MATRIX, DELEGATION_PATTERNS, DelegationService

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def service() -> DelegationService:
    """Standard delegation service."""
    return DelegationService()


# =============================================================================
# Test: Trust × Risk Matrix - Stage 1 (NEW)
# =============================================================================


class TestStageNew:
    """Tests for NEW trust stage - most restrictive."""

    def test_new_low_risk_observe_only(self, service: DelegationService):
        """NEW + LOW should only allow OBSERVE."""
        allowed = service.get_allowed_delegations(TrustStage.NEW, RiskLevel.LOW)
        assert allowed == [DelegationType.OBSERVE]

    def test_new_medium_risk_observe_only(self, service: DelegationService):
        """NEW + MEDIUM should only allow OBSERVE."""
        allowed = service.get_allowed_delegations(TrustStage.NEW, RiskLevel.MEDIUM)
        assert allowed == [DelegationType.OBSERVE]

    def test_new_high_risk_observe_only(self, service: DelegationService):
        """NEW + HIGH should only allow OBSERVE."""
        allowed = service.get_allowed_delegations(TrustStage.NEW, RiskLevel.HIGH)
        assert allowed == [DelegationType.OBSERVE]


# =============================================================================
# Test: Trust × Risk Matrix - Stage 2 (BUILDING)
# =============================================================================


class TestStageBuilding:
    """Tests for BUILDING trust stage."""

    def test_building_low_risk_allows_inform(self, service: DelegationService):
        """BUILDING + LOW should allow OBSERVE and INFORM."""
        allowed = service.get_allowed_delegations(TrustStage.BUILDING, RiskLevel.LOW)
        assert DelegationType.OBSERVE in allowed
        assert DelegationType.INFORM in allowed
        assert DelegationType.OFFER not in allowed

    def test_building_medium_risk_observe_only(self, service: DelegationService):
        """BUILDING + MEDIUM should only allow OBSERVE."""
        allowed = service.get_allowed_delegations(TrustStage.BUILDING, RiskLevel.MEDIUM)
        assert allowed == [DelegationType.OBSERVE]

    def test_building_high_risk_observe_only(self, service: DelegationService):
        """BUILDING + HIGH should only allow OBSERVE."""
        allowed = service.get_allowed_delegations(TrustStage.BUILDING, RiskLevel.HIGH)
        assert allowed == [DelegationType.OBSERVE]


# =============================================================================
# Test: Trust × Risk Matrix - Stage 3 (ESTABLISHED)
# =============================================================================


class TestStageEstablished:
    """Tests for ESTABLISHED trust stage."""

    def test_established_low_risk_allows_suggest(self, service: DelegationService):
        """ESTABLISHED + LOW should allow up to SUGGEST."""
        allowed = service.get_allowed_delegations(TrustStage.ESTABLISHED, RiskLevel.LOW)
        assert DelegationType.SUGGEST in allowed
        assert DelegationType.CONFIRM not in allowed
        assert DelegationType.AUTO not in allowed

    def test_established_medium_risk_allows_offer(self, service: DelegationService):
        """ESTABLISHED + MEDIUM should allow up to OFFER."""
        allowed = service.get_allowed_delegations(TrustStage.ESTABLISHED, RiskLevel.MEDIUM)
        assert DelegationType.OFFER in allowed
        assert DelegationType.SUGGEST not in allowed

    def test_established_high_risk_observe_only(self, service: DelegationService):
        """ESTABLISHED + HIGH should only allow OBSERVE."""
        allowed = service.get_allowed_delegations(TrustStage.ESTABLISHED, RiskLevel.HIGH)
        assert allowed == [DelegationType.OBSERVE]


# =============================================================================
# Test: Trust × Risk Matrix - Stage 4 (TRUSTED)
# =============================================================================


class TestStageTrusted:
    """Tests for TRUSTED trust stage - most permissive."""

    def test_trusted_low_risk_allows_auto(self, service: DelegationService):
        """TRUSTED + LOW should allow AUTO (full autonomy)."""
        allowed = service.get_allowed_delegations(TrustStage.TRUSTED, RiskLevel.LOW)
        assert DelegationType.AUTO in allowed
        assert DelegationType.CONFIRM in allowed

    def test_trusted_medium_risk_allows_confirm(self, service: DelegationService):
        """TRUSTED + MEDIUM should allow CONFIRM but not AUTO."""
        allowed = service.get_allowed_delegations(TrustStage.TRUSTED, RiskLevel.MEDIUM)
        assert DelegationType.CONFIRM in allowed
        assert DelegationType.AUTO not in allowed

    def test_trusted_high_risk_no_auto(self, service: DelegationService):
        """TRUSTED + HIGH should NOT allow AUTO (critical safety guarantee)."""
        allowed = service.get_allowed_delegations(TrustStage.TRUSTED, RiskLevel.HIGH)
        assert DelegationType.AUTO not in allowed

    def test_trusted_high_risk_no_confirm(self, service: DelegationService):
        """TRUSTED + HIGH should NOT allow CONFIRM."""
        allowed = service.get_allowed_delegations(TrustStage.TRUSTED, RiskLevel.HIGH)
        assert DelegationType.CONFIRM not in allowed

    def test_trusted_high_risk_allows_offer(self, service: DelegationService):
        """TRUSTED + HIGH should still allow OFFER."""
        allowed = service.get_allowed_delegations(TrustStage.TRUSTED, RiskLevel.HIGH)
        assert DelegationType.OFFER in allowed


# =============================================================================
# Test: Critical Safety Guarantees
# =============================================================================


class TestSafetyGuarantees:
    """Tests for safety guarantees that must never be violated."""

    def test_auto_never_allowed_for_high_risk(self, service: DelegationService):
        """AUTO must NEVER be allowed for HIGH risk at any trust level."""
        for stage in TrustStage:
            allowed = service.get_allowed_delegations(stage, RiskLevel.HIGH)
            assert DelegationType.AUTO not in allowed, f"AUTO allowed for {stage} + HIGH"

    def test_observe_always_allowed(self, service: DelegationService):
        """OBSERVE should always be in the allowed list."""
        for stage in TrustStage:
            for risk in RiskLevel:
                allowed = service.get_allowed_delegations(stage, risk)
                assert DelegationType.OBSERVE in allowed, f"OBSERVE missing for {stage} + {risk}"

    def test_allowed_list_never_empty(self, service: DelegationService):
        """Allowed list should never be empty."""
        for stage in TrustStage:
            for risk in RiskLevel:
                allowed = service.get_allowed_delegations(stage, risk)
                assert len(allowed) > 0, f"Empty list for {stage} + {risk}"


# =============================================================================
# Test: Best/Safest Delegation
# =============================================================================


class TestBestAndSafestDelegation:
    """Tests for get_best_delegation and get_safest_delegation."""

    def test_best_returns_most_proactive(self, service: DelegationService):
        """get_best_delegation should return the most proactive option."""
        best = service.get_best_delegation(TrustStage.TRUSTED, RiskLevel.LOW)
        assert best == DelegationType.AUTO

    def test_safest_returns_least_proactive(self, service: DelegationService):
        """get_safest_delegation should return OBSERVE for any combination."""
        safest = service.get_safest_delegation(TrustStage.TRUSTED, RiskLevel.LOW)
        assert safest == DelegationType.OBSERVE

    def test_best_respects_risk(self, service: DelegationService):
        """get_best_delegation should respect risk constraints."""
        # TRUSTED + HIGH should return OFFER, not AUTO
        best = service.get_best_delegation(TrustStage.TRUSTED, RiskLevel.HIGH)
        assert best == DelegationType.OFFER


# =============================================================================
# Test: is_delegation_allowed
# =============================================================================


class TestIsDelegationAllowed:
    """Tests for is_delegation_allowed method."""

    def test_allowed_returns_true(self, service: DelegationService):
        """Should return True for allowed delegations."""
        assert service.is_delegation_allowed(TrustStage.TRUSTED, RiskLevel.LOW, DelegationType.AUTO)

    def test_not_allowed_returns_false(self, service: DelegationService):
        """Should return False for disallowed delegations."""
        assert not service.is_delegation_allowed(TrustStage.NEW, RiskLevel.LOW, DelegationType.AUTO)


# =============================================================================
# Test: Language Pattern Formatting
# =============================================================================


class TestLanguagePatterns:
    """Tests for format_delegation_message."""

    def test_observe_pattern(self, service: DelegationService):
        """OBSERVE pattern should start with 'I notice'."""
        msg = service.format_delegation_message(
            DelegationType.OBSERVE, "your standup is in 10 minutes"
        )
        assert msg == "I notice your standup is in 10 minutes."

    def test_inform_pattern(self, service: DelegationService):
        """INFORM pattern should start with 'Just so you know'."""
        msg = service.format_delegation_message(DelegationType.INFORM, "the PR has new comments")
        assert msg == "Just so you know, the PR has new comments."

    def test_offer_pattern(self, service: DelegationService):
        """OFFER pattern should be a question."""
        msg = service.format_delegation_message(DelegationType.OFFER, "draft a response")
        assert msg == "Would you like me to draft a response?"

    def test_suggest_pattern(self, service: DelegationService):
        """SUGGEST pattern should express opinion."""
        msg = service.format_delegation_message(DelegationType.SUGGEST, "check the API status")
        assert msg == "I think we should check the API status."

    def test_confirm_pattern(self, service: DelegationService):
        """CONFIRM pattern should be opt-out."""
        msg = service.format_delegation_message(DelegationType.CONFIRM, "send the reminder")
        assert msg == "I'll send the reminder unless you'd rather not."

    def test_auto_pattern(self, service: DelegationService):
        """AUTO pattern should be brief confirmation."""
        msg = service.format_delegation_message(DelegationType.AUTO, "Reminder sent")
        assert msg == "✓ Reminder sent"


# =============================================================================
# Test: Convenience Methods
# =============================================================================


class TestConvenienceMethods:
    """Tests for can_auto_execute and can_confirm_execute."""

    def test_can_auto_execute_trusted_low(self, service: DelegationService):
        """can_auto_execute should return True for TRUSTED + LOW."""
        assert service.can_auto_execute(TrustStage.TRUSTED, RiskLevel.LOW)

    def test_can_auto_execute_trusted_high(self, service: DelegationService):
        """can_auto_execute should return False for TRUSTED + HIGH."""
        assert not service.can_auto_execute(TrustStage.TRUSTED, RiskLevel.HIGH)

    def test_can_confirm_execute_trusted_medium(self, service: DelegationService):
        """can_confirm_execute should return True for TRUSTED + MEDIUM."""
        assert service.can_confirm_execute(TrustStage.TRUSTED, RiskLevel.MEDIUM)

    def test_can_confirm_execute_established_low(self, service: DelegationService):
        """can_confirm_execute should return False for ESTABLISHED + LOW."""
        assert not service.can_confirm_execute(TrustStage.ESTABLISHED, RiskLevel.LOW)


# =============================================================================
# Test: Delegation Type Enum
# =============================================================================


class TestDelegationTypeEnum:
    """Tests for DelegationType enum ordering."""

    def test_proactivity_ordering(self):
        """Delegation types should be ordered by proactivity level."""
        assert DelegationType.OBSERVE < DelegationType.INFORM
        assert DelegationType.INFORM < DelegationType.OFFER
        assert DelegationType.OFFER < DelegationType.SUGGEST
        assert DelegationType.SUGGEST < DelegationType.CONFIRM
        assert DelegationType.CONFIRM < DelegationType.AUTO

    def test_all_types_have_patterns(self):
        """All delegation types should have language patterns."""
        for dtype in DelegationType:
            assert dtype in DELEGATION_PATTERNS, f"Missing pattern for {dtype}"


# =============================================================================
# Test: Matrix Completeness
# =============================================================================


class TestMatrixCompleteness:
    """Tests for delegation matrix completeness."""

    def test_all_combinations_defined(self):
        """All trust × risk combinations should be in the matrix."""
        for stage in TrustStage:
            for risk in RiskLevel:
                key = (stage, risk)
                assert key in DELEGATION_MATRIX, f"Missing matrix entry for {key}"
