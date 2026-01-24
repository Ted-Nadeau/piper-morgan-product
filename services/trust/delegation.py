"""
Delegation Service.

Determines appropriate delegation types based on trust stage and action risk.
Part of #414 MUX-INTERACT-DELEGATION.

UX Research Finding: "System-initiated delegation increases perceived self-threat
and decreases willingness to accept delegation."

This service extends ProactivityGate with a risk dimension:
- Trust stage determines baseline proactivity
- Risk level constrains the maximum allowed proactivity
- Result: appropriate delegation type for each situation

Key Principle: High-risk actions NEVER get AUTO delegation, even at Stage 4.
"""

from typing import List, Optional

import structlog

from services.shared_types import DelegationType, RiskLevel, TrustStage

logger = structlog.get_logger(__name__)


# Language patterns for each delegation type
# {action} placeholder is replaced with the action description
DELEGATION_PATTERNS = {
    DelegationType.OBSERVE: "I notice {action}.",
    DelegationType.INFORM: "Just so you know, {action}.",
    DelegationType.OFFER: "Would you like me to {action}?",
    DelegationType.SUGGEST: "I think we should {action}.",
    DelegationType.CONFIRM: "I'll {action} unless you'd rather not.",
    DelegationType.AUTO: "✓ {action}",
}


# Trust × Risk → Allowed Delegations Matrix
# Each entry is a list of allowed delegation types, ordered least to most proactive
DELEGATION_MATRIX = {
    # NEW (Stage 1): Only observations, regardless of risk
    (TrustStage.NEW, RiskLevel.LOW): [DelegationType.OBSERVE],
    (TrustStage.NEW, RiskLevel.MEDIUM): [DelegationType.OBSERVE],
    (TrustStage.NEW, RiskLevel.HIGH): [DelegationType.OBSERVE],
    # BUILDING (Stage 2): Can inform for low risk
    (TrustStage.BUILDING, RiskLevel.LOW): [
        DelegationType.OBSERVE,
        DelegationType.INFORM,
    ],
    (TrustStage.BUILDING, RiskLevel.MEDIUM): [DelegationType.OBSERVE],
    (TrustStage.BUILDING, RiskLevel.HIGH): [DelegationType.OBSERVE],
    # ESTABLISHED (Stage 3): Can suggest for low, offer for medium
    (TrustStage.ESTABLISHED, RiskLevel.LOW): [
        DelegationType.OBSERVE,
        DelegationType.INFORM,
        DelegationType.OFFER,
        DelegationType.SUGGEST,
    ],
    (TrustStage.ESTABLISHED, RiskLevel.MEDIUM): [
        DelegationType.OBSERVE,
        DelegationType.OFFER,
    ],
    (TrustStage.ESTABLISHED, RiskLevel.HIGH): [DelegationType.OBSERVE],
    # TRUSTED (Stage 4): Full autonomy for low, confirm for medium, offer for high
    (TrustStage.TRUSTED, RiskLevel.LOW): [
        DelegationType.OBSERVE,
        DelegationType.INFORM,
        DelegationType.OFFER,
        DelegationType.SUGGEST,
        DelegationType.CONFIRM,
        DelegationType.AUTO,
    ],
    (TrustStage.TRUSTED, RiskLevel.MEDIUM): [
        DelegationType.OBSERVE,
        DelegationType.INFORM,
        DelegationType.OFFER,
        DelegationType.SUGGEST,
        DelegationType.CONFIRM,
    ],
    (TrustStage.TRUSTED, RiskLevel.HIGH): [
        DelegationType.OBSERVE,
        DelegationType.OFFER,
    ],
}


class DelegationService:
    """
    Determines appropriate delegation types based on trust and risk.

    This service answers: "Given this user's trust level and the risk of this action,
    what kinds of system-initiated behavior are appropriate?"

    Usage:
        service = DelegationService()

        # Get all allowed types
        allowed = service.get_allowed_delegations(TrustStage.ESTABLISHED, RiskLevel.LOW)
        # Returns: [OBSERVE, INFORM, OFFER, SUGGEST]

        # Get the most proactive allowed type
        best = service.get_best_delegation(TrustStage.ESTABLISHED, RiskLevel.LOW)
        # Returns: SUGGEST

        # Format a message
        msg = service.format_delegation_message(DelegationType.OFFER, "draft a response")
        # Returns: "Would you like me to draft a response?"
    """

    def get_allowed_delegations(
        self,
        trust_stage: TrustStage,
        risk_level: RiskLevel,
    ) -> List[DelegationType]:
        """
        Get all delegation types allowed for this trust × risk combination.

        Args:
            trust_stage: User's current trust stage
            risk_level: Risk level of the proposed action

        Returns:
            List of allowed DelegationTypes, ordered least to most proactive.
            Always includes at least OBSERVE.
        """
        key = (trust_stage, risk_level)
        allowed = DELEGATION_MATRIX.get(key)

        if allowed is None:
            # Defensive: unknown combination defaults to OBSERVE only
            logger.warning(
                "Unknown trust/risk combination, defaulting to OBSERVE",
                trust_stage=trust_stage,
                risk_level=risk_level,
            )
            return [DelegationType.OBSERVE]

        return list(allowed)  # Return copy to prevent mutation

    def get_best_delegation(
        self,
        trust_stage: TrustStage,
        risk_level: RiskLevel,
    ) -> DelegationType:
        """
        Get the most proactive delegation type allowed.

        This is the "best" from Piper's perspective - the most autonomous
        behavior that's appropriate for the situation.

        Args:
            trust_stage: User's current trust stage
            risk_level: Risk level of the proposed action

        Returns:
            The most proactive allowed DelegationType
        """
        allowed = self.get_allowed_delegations(trust_stage, risk_level)
        # Return the last (most proactive) since list is ordered
        return allowed[-1]

    def get_safest_delegation(
        self,
        trust_stage: TrustStage,
        risk_level: RiskLevel,
    ) -> DelegationType:
        """
        Get the least proactive (safest) delegation type allowed.

        This is the most conservative choice - use when uncertain.

        Args:
            trust_stage: User's current trust stage
            risk_level: Risk level of the proposed action

        Returns:
            The least proactive allowed DelegationType (usually OBSERVE)
        """
        allowed = self.get_allowed_delegations(trust_stage, risk_level)
        return allowed[0]

    def is_delegation_allowed(
        self,
        trust_stage: TrustStage,
        risk_level: RiskLevel,
        delegation_type: DelegationType,
    ) -> bool:
        """
        Check if a specific delegation type is allowed.

        Args:
            trust_stage: User's current trust stage
            risk_level: Risk level of the proposed action
            delegation_type: The delegation type to check

        Returns:
            True if this delegation type is allowed
        """
        allowed = self.get_allowed_delegations(trust_stage, risk_level)
        return delegation_type in allowed

    def format_delegation_message(
        self,
        delegation_type: DelegationType,
        action_description: str,
    ) -> str:
        """
        Format a message using the delegation type's language pattern.

        Args:
            delegation_type: The type of delegation
            action_description: Description of the action (e.g., "draft a response")

        Returns:
            Formatted message using the appropriate pattern
        """
        pattern = DELEGATION_PATTERNS.get(delegation_type)
        if pattern is None:
            # Defensive fallback
            return action_description

        return pattern.format(action=action_description)

    def can_auto_execute(
        self,
        trust_stage: TrustStage,
        risk_level: RiskLevel,
    ) -> bool:
        """
        Check if AUTO (silent execution) is allowed.

        Convenience method for the common question:
        "Can Piper just do this without asking?"

        Args:
            trust_stage: User's current trust stage
            risk_level: Risk level of the proposed action

        Returns:
            True only if AUTO delegation is allowed (Stage 4 + Low risk)
        """
        return self.is_delegation_allowed(trust_stage, risk_level, DelegationType.AUTO)

    def can_confirm_execute(
        self,
        trust_stage: TrustStage,
        risk_level: RiskLevel,
    ) -> bool:
        """
        Check if CONFIRM ("I'll do X unless...") is allowed.

        Args:
            trust_stage: User's current trust stage
            risk_level: Risk level of the proposed action

        Returns:
            True if CONFIRM delegation is allowed
        """
        return self.is_delegation_allowed(trust_stage, risk_level, DelegationType.CONFIRM)
