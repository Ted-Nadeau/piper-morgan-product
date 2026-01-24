"""
ProactivityGate - Stage-based behavior gating for trust gradient.

Issue #648: TRUST-LEVELS-2 - Integration
ADR-053: Trust Computation Architecture

Gates proactive behaviors based on user's current trust stage:
- Stage 1 (NEW): Responsive only, no proactive behavior
- Stage 2 (BUILDING): Can offer capability hints after successful interactions
- Stage 3 (ESTABLISHED): Can proactively suggest based on context
- Stage 4 (TRUSTED): Can act autonomously within learned preferences
"""

from dataclasses import dataclass
from typing import Dict

from services.shared_types import TrustStage


@dataclass
class ProactivityConfig:
    """Configuration for proactive behavior at a given trust stage."""

    can_offer_hints: bool
    can_suggest: bool
    can_act_autonomously: bool
    max_suggestions_per_session: int
    suggestion_delay_seconds: int  # Wait time after task completion


# Stage-specific configurations per ADR-053
PROACTIVITY_CONFIGS: Dict[TrustStage, ProactivityConfig] = {
    TrustStage.NEW: ProactivityConfig(
        can_offer_hints=False,
        can_suggest=False,
        can_act_autonomously=False,
        max_suggestions_per_session=0,
        suggestion_delay_seconds=0,
    ),
    TrustStage.BUILDING: ProactivityConfig(
        can_offer_hints=True,
        can_suggest=False,
        can_act_autonomously=False,
        max_suggestions_per_session=2,
        suggestion_delay_seconds=5,  # Wait 5s after completion before hint
    ),
    TrustStage.ESTABLISHED: ProactivityConfig(
        can_offer_hints=True,
        can_suggest=True,
        can_act_autonomously=False,
        max_suggestions_per_session=5,
        suggestion_delay_seconds=2,  # Shorter wait at established trust
    ),
    TrustStage.TRUSTED: ProactivityConfig(
        can_offer_hints=True,
        can_suggest=True,
        can_act_autonomously=True,
        max_suggestions_per_session=10,  # Effectively unlimited for trusted users
        suggestion_delay_seconds=0,  # No delay for trusted users
    ),
}


class ProactivityGate:
    """
    Gates proactive behaviors based on trust stage.

    This service provides the decision logic for when Piper can be proactive.
    It doesn't fetch trust stage itself - callers should provide the stage
    from TrustComputationService.get_trust_stage().

    Usage:
        gate = ProactivityGate()
        stage = await trust_service.get_trust_stage(user_id)

        if gate.can_offer_capability_hints(stage):
            # Show hint about available features
            pass

        if gate.can_proactive_suggest(stage):
            # Offer contextual suggestion
            pass

        if gate.can_act_without_asking(stage):
            # Take autonomous action
            pass
    """

    def can_offer_capability_hints(self, stage: TrustStage) -> bool:
        """
        Check if Piper can offer capability hints at this trust stage.

        Capability hints are gentle mentions of available features after
        successful task completion. Example: "By the way, I can also help
        you track time for projects."

        Args:
            stage: User's current trust stage

        Returns:
            True if hints are allowed (Stage 2+)
        """
        config = PROACTIVITY_CONFIGS.get(stage, PROACTIVITY_CONFIGS[TrustStage.NEW])
        return config.can_offer_hints

    def can_proactive_suggest(self, stage: TrustStage) -> bool:
        """
        Check if Piper can proactively suggest actions at this trust stage.

        Proactive suggestions are context-aware offers to help. Example:
        "I notice you have a meeting with the client tomorrow - would you
        like me to prepare a brief?"

        Args:
            stage: User's current trust stage

        Returns:
            True if suggestions are allowed (Stage 3+)
        """
        config = PROACTIVITY_CONFIGS.get(stage, PROACTIVITY_CONFIGS[TrustStage.NEW])
        return config.can_suggest

    def can_act_without_asking(self, stage: TrustStage) -> bool:
        """
        Check if Piper can act autonomously at this trust stage.

        Autonomous actions are taken without explicit confirmation. Example:
        Automatically scheduling a recurring meeting when user mentions
        "let's do this weekly."

        Args:
            stage: User's current trust stage

        Returns:
            True if autonomous action is allowed (Stage 4 only)
        """
        config = PROACTIVITY_CONFIGS.get(stage, PROACTIVITY_CONFIGS[TrustStage.NEW])
        return config.can_act_autonomously

    def get_proactivity_config(self, stage: TrustStage) -> Dict:
        """
        Get the full proactivity configuration for a trust stage.

        Args:
            stage: User's current trust stage

        Returns:
            Dict with all proactivity settings
        """
        config = PROACTIVITY_CONFIGS.get(stage, PROACTIVITY_CONFIGS[TrustStage.NEW])
        return {
            "can_offer_hints": config.can_offer_hints,
            "can_suggest": config.can_suggest,
            "can_act_autonomously": config.can_act_autonomously,
            "max_suggestions_per_session": config.max_suggestions_per_session,
            "suggestion_delay_seconds": config.suggestion_delay_seconds,
        }

    def get_max_suggestions_per_session(self, stage: TrustStage) -> int:
        """
        Get the maximum number of proactive suggestions per session.

        Limits prevent Piper from being overwhelming even at higher trust.

        Args:
            stage: User's current trust stage

        Returns:
            Maximum suggestions allowed (0 for NEW, increasing by stage)
        """
        config = PROACTIVITY_CONFIGS.get(stage, PROACTIVITY_CONFIGS[TrustStage.NEW])
        return config.max_suggestions_per_session

    def get_suggestion_delay_seconds(self, stage: TrustStage) -> int:
        """
        Get the delay before offering suggestions after task completion.

        Higher trust means faster suggestions (less hesitation).

        Args:
            stage: User's current trust stage

        Returns:
            Seconds to wait before suggesting (0 for TRUSTED)
        """
        config = PROACTIVITY_CONFIGS.get(stage, PROACTIVITY_CONFIGS[TrustStage.NEW])
        return config.suggestion_delay_seconds

    def should_suggest_now(
        self,
        stage: TrustStage,
        suggestions_this_session: int,
    ) -> bool:
        """
        Determine if Piper should offer a suggestion right now.

        Combines stage permission check with session limit check.

        Args:
            stage: User's current trust stage
            suggestions_this_session: How many suggestions already offered

        Returns:
            True if suggestion is allowed and under limit
        """
        if not self.can_proactive_suggest(stage):
            return False

        max_allowed = self.get_max_suggestions_per_session(stage)
        return suggestions_this_session < max_allowed
