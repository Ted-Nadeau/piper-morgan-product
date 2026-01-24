"""
Trust Computation Service

Issue #647: TRUST-LEVELS-1 - Core Infrastructure
ADR-053: Trust Computation Architecture
PDR-002: Conversational Glue

Computes and manages user trust stages to calibrate Piper's proactivity.
Trust is invisible to users but its effects are noticeable through behavior.

Key behaviors by stage:
- NEW (1): Respond to queries only; no unsolicited help
- BUILDING (2): Offer related capabilities after task completion
- ESTABLISHED (3): Proactive suggestions based on observed context
- TRUSTED (4): Anticipate needs; "I'll do X unless you stop me"
"""

import logging
from datetime import datetime, timezone
from typing import Optional, Tuple
from uuid import UUID, uuid4

from services.domain.models import TrustEvent, UserTrustProfile
from services.repositories.user_trust_profile_repository import UserTrustProfileRepository
from services.shared_types import TrustStage

logger = logging.getLogger(__name__)


# CALIBRATION: These thresholds are starting points for alpha testing
# Per ADR-053, they may be adjusted based on real user feedback
STAGE_THRESHOLDS = {
    # Stage 1→2: Need 10 successful interactions
    TrustStage.BUILDING: 10,
    # Stage 2→3: Need 50 successful interactions
    TrustStage.ESTABLISHED: 50,
    # Stage 3→4: Conversational signals only (per CXO memo)
    TrustStage.TRUSTED: None,  # Cannot auto-progress; requires user signals
}

# Maximum consecutive negative interactions before stage regression
MAX_CONSECUTIVE_NEGATIVE = 3


class TrustComputationService:
    """
    Service for computing and managing user trust levels.

    Responsibilities:
    - Record interaction outcomes
    - Compute stage progression/regression
    - Provide trust stage for behavior calibration
    - Support discussability ("Why did you do that?")
    """

    def __init__(self, repository: UserTrustProfileRepository):
        """Initialize with repository for persistence."""
        self.repository = repository

    async def record_interaction(
        self,
        user_id: UUID,
        outcome: str,
        context: str,
    ) -> UserTrustProfile:
        """
        Record an interaction outcome and update trust state.

        Args:
            user_id: User's UUID
            outcome: "successful", "neutral", or "negative"
            context: Brief description for discussability

        Returns:
            Updated UserTrustProfile

        Side effects:
            - May trigger stage progression or regression
            - Updates counters and recent_events
        """
        if outcome not in ("successful", "neutral", "negative"):
            raise ValueError(
                f"Invalid outcome: {outcome}. Must be successful, neutral, or negative."
            )

        # Get current trust state (or create new profile)
        profile = await self.repository.get_by_user_id(user_id)
        current_stage = profile.current_stage if profile else TrustStage.NEW

        # Create trust event
        event = TrustEvent(
            event_id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            outcome=outcome,
            context=context,
            stage_at_time=current_stage,
        )

        # Record event (handles profile creation if needed)
        profile = await self.repository.record_event(user_id, event)

        # Check for stage changes
        profile = await self._check_stage_progression(user_id, profile)
        profile = await self._check_stage_regression(user_id, profile)

        logger.info(
            f"Recorded {outcome} interaction for user {user_id}, "
            f"stage={profile.current_stage.name}, "
            f"successful={profile.successful_count}"
        )

        return profile

    async def get_trust_stage(self, user_id: UUID) -> TrustStage:
        """
        Get the current trust stage for a user.

        Returns TrustStage.NEW for users without a profile (implicit default).
        """
        profile = await self.repository.get_by_user_id(user_id)
        if profile is None:
            return TrustStage.NEW
        return profile.current_stage

    async def get_trust_profile(self, user_id: UUID) -> Optional[UserTrustProfile]:
        """
        Get the full trust profile for a user.

        Returns None for users without a profile.
        """
        return await self.repository.get_by_user_id(user_id)

    def should_offer_proactive_help(self, stage: TrustStage) -> bool:
        """
        Determine if Piper should offer proactive help at this trust level.

        Per ADR-053:
        - NEW: No proactive help
        - BUILDING: Offer related capabilities after task completion
        - ESTABLISHED: Proactive suggestions based on context
        - TRUSTED: Anticipate needs proactively
        """
        return stage.value >= TrustStage.BUILDING.value

    def get_proactivity_style(self, stage: TrustStage) -> str:
        """
        Get the proactivity style description for a trust stage.

        Returns a style hint for response generation.
        """
        styles = {
            TrustStage.NEW: "responsive_only",  # Only respond to queries
            TrustStage.BUILDING: "offer_after_completion",  # Offer related capabilities
            TrustStage.ESTABLISHED: "suggest_contextually",  # Proactive suggestions
            TrustStage.TRUSTED: "anticipate_needs",  # Full proactive mode
        }
        return styles.get(stage, "responsive_only")

    async def _check_stage_progression(
        self,
        user_id: UUID,
        profile: UserTrustProfile,
    ) -> UserTrustProfile:
        """
        Check if user should progress to a higher trust stage.

        Stage progression based on successful interaction count:
        - 1→2: 10 successful interactions
        - 2→3: 50 successful interactions
        - 3→4: NOT auto-progressed (requires conversational signals)
        """
        current = profile.current_stage

        # Stage 3→4 cannot auto-progress per CXO memo
        if current == TrustStage.ESTABLISHED:
            return profile

        # Check if we've reached threshold for next stage
        if current == TrustStage.NEW:
            threshold = STAGE_THRESHOLDS[TrustStage.BUILDING]
            if profile.successful_count >= threshold:
                return await self._progress_to_stage(
                    user_id, TrustStage.BUILDING, f"Reached {threshold} successful interactions"
                )

        elif current == TrustStage.BUILDING:
            threshold = STAGE_THRESHOLDS[TrustStage.ESTABLISHED]
            if profile.successful_count >= threshold:
                return await self._progress_to_stage(
                    user_id, TrustStage.ESTABLISHED, f"Reached {threshold} successful interactions"
                )

        return profile

    async def _check_stage_regression(
        self,
        user_id: UUID,
        profile: UserTrustProfile,
    ) -> UserTrustProfile:
        """
        Check if user should regress to a lower trust stage.

        Regression triggered by consecutive negative interactions.
        Per ADR-053: Regression drops one stage at a time.
        """
        if profile.consecutive_negative >= MAX_CONSECUTIVE_NEGATIVE:
            current = profile.current_stage

            # Can't regress below NEW
            if current == TrustStage.NEW:
                return profile

            # Determine new stage (one step down)
            new_stage = TrustStage(current.value - 1)

            return await self._regress_to_stage(
                user_id, new_stage, f"{MAX_CONSECUTIVE_NEGATIVE} consecutive negative interactions"
            )

        return profile

    async def _progress_to_stage(
        self,
        user_id: UUID,
        new_stage: TrustStage,
        reason: str,
    ) -> UserTrustProfile:
        """Progress user to a higher trust stage."""
        profile = await self.repository.update_stage(user_id, new_stage, reason)
        logger.info(f"User {user_id} progressed to {new_stage.name}: {reason}")
        return profile

    async def _regress_to_stage(
        self,
        user_id: UUID,
        new_stage: TrustStage,
        reason: str,
    ) -> UserTrustProfile:
        """Regress user to a lower trust stage and reset consecutive counter."""
        profile = await self.repository.update_stage(user_id, new_stage, reason)

        # Reset consecutive negative counter after regression
        profile.consecutive_negative = 0
        profile = await self.repository.create_or_update(profile)

        logger.warning(f"User {user_id} regressed to {new_stage.name}: {reason}")
        return profile

    async def progress_to_trusted(
        self,
        user_id: UUID,
        reason: str = "User explicitly requested higher autonomy",
    ) -> Optional[UserTrustProfile]:
        """
        Manually progress user to TRUSTED stage.

        Per ADR-053 and CXO memo: Stage 3→4 requires conversational signals,
        not automatic progression. This method is called when those signals
        are detected (e.g., "Just do it", "I trust your judgment").

        Returns None if user doesn't have a profile or isn't at ESTABLISHED.
        """
        profile = await self.repository.get_by_user_id(user_id)
        if profile is None:
            logger.warning(f"Cannot progress to TRUSTED: no profile for user {user_id}")
            return None

        if profile.current_stage != TrustStage.ESTABLISHED:
            logger.warning(
                f"Cannot progress to TRUSTED: user {user_id} is at "
                f"{profile.current_stage.name}, not ESTABLISHED"
            )
            return None

        return await self._progress_to_stage(user_id, TrustStage.TRUSTED, reason)

    async def explain_trust_state(self, user_id: UUID) -> str:
        """
        Generate an explanation of user's current trust state.

        Supports discussability: "Why are you being so cautious/proactive?"
        """
        profile = await self.repository.get_by_user_id(user_id)

        if profile is None:
            return (
                "I'm being careful because we haven't worked together much yet. "
                "As we collaborate more, I'll learn how to help you better."
            )

        stage = profile.current_stage
        explanations = {
            TrustStage.NEW: (
                "We're still getting to know each other. I'm focused on being "
                "helpful when you ask, without jumping ahead."
            ),
            TrustStage.BUILDING: (
                f"After {profile.successful_count} successful interactions, "
                "I'm starting to understand how you work. I might occasionally "
                "suggest related things after completing a task."
            ),
            TrustStage.ESTABLISHED: (
                "We've built a good working relationship. I feel comfortable "
                "making proactive suggestions based on what I've learned about "
                "your preferences and patterns."
            ),
            TrustStage.TRUSTED: (
                "You've given me the green light to be proactive. I'll anticipate "
                "your needs and sometimes take action on your behalf, always with "
                "the option for you to redirect me."
            ),
        }

        return explanations.get(stage, explanations[TrustStage.NEW])
