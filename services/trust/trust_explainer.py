"""
TrustExplainer service for generating natural language explanations.

This service provides rich, human-friendly explanations of trust-based behavior
for the discussability feature. All explanations must pass the Contractor Test:
they should sound like something a thoughtful colleague would say.

Per ADR-053 and product philosophy:
- No internal jargon ("Stage 2", "TrustStage.BUILDING")
- Professional but warm tone
- References shared history naturally
- Offers agency to the user
"""

from enum import Enum
from typing import Optional
from uuid import UUID

from services.shared_types import TrustStage


class ExplanationContext(str, Enum):
    """Context for what type of explanation is being requested."""

    CURRENT_STAGE = "current_stage"  # "Why are you being cautious?"
    PROACTIVE_ACTION = "proactive_action"  # "Why did you do that?"
    WHY_NOT_PROACTIVE = "why_not_proactive"  # "Why don't you just do things?"
    BEHAVIOR_CHANGE = "behavior_change"  # "Why did you start doing this?"


class TrustExplainer:
    """
    Generates natural language explanations for trust-based behavior.

    This is the discussability layer - allowing Piper to explain her reasoning
    when users ask "Why did you do that?" or "Why are you being so cautious?"

    Design principle: Explanations should feel like a colleague explaining
    themselves, not a system reporting its state.

    Usage:
        explainer = TrustExplainer(trust_service)

        # User asks "Why are you being so cautious?"
        explanation = await explainer.explain_current_stage(user_id)

        # User asks "Why did you just reschedule my meeting?"
        explanation = await explainer.explain_proactive_action(
            user_id,
            action="rescheduled your meeting"
        )
    """

    def __init__(self, trust_service):
        """
        Initialize with trust computation service.

        Args:
            trust_service: TrustComputationService instance for accessing
                          user trust profiles and stage information.
        """
        self._trust_service = trust_service

    async def explain_current_stage(self, user_id: UUID) -> str:
        """
        Explain current trust relationship in natural language.

        This is the primary method for "Why are you being so cautious?"
        or "How do we work together?" type questions.

        Args:
            user_id: User to explain trust state for

        Returns:
            Natural language explanation passing Contractor Test
        """
        # Delegate to existing implementation which already has good explanations
        return await self._trust_service.explain_trust_state(user_id)

    async def explain_proactive_action(
        self,
        user_id: UUID,
        action: str,
        context: Optional[str] = None,
    ) -> str:
        """
        Explain why Piper took a proactive action.

        For Stage 3-4 users who receive proactive assistance and ask
        "Why did you do that?" or "I didn't ask you to..."

        Args:
            user_id: User who received the proactive action
            action: Description of what was done (e.g., "suggested a meeting time")
            context: Optional additional context about why

        Returns:
            Explanation including the action and reasoning
        """
        stage = await self._trust_service.get_trust_stage(user_id)

        if stage == TrustStage.TRUSTED:
            base = (
                f"I {action} because you've given me latitude to help proactively. "
                "Based on our work together, it seemed like the right thing to do."
            )
            followup = " Let me know if you'd prefer I check with you first next time."

        elif stage == TrustStage.ESTABLISHED:
            base = (
                f"I {action} because I noticed something that might need your attention. "
                "I wanted to be helpful, though I should have confirmed first."
            )
            followup = " I'll make sure to ask before acting on things like this."

        else:
            # Stage 1-2 shouldn't be taking proactive actions,
            # so this is likely a misunderstanding
            base = (
                f"I'm not sure I {action} without being asked - "
                "that's not something I'd typically do at this point in our work together."
            )
            followup = " Can you tell me more about what happened?"

        if context:
            return f"{base} {context}{followup}"
        return f"{base}{followup}"

    async def explain_why_not_proactive(self, user_id: UUID) -> str:
        """
        Explain why Piper isn't being more proactive.

        For Stage 1-2 users who ask "Why don't you just do things?"
        or "Why do you always ask me first?"

        Args:
            user_id: User asking about proactivity

        Returns:
            Explanation appropriate to their stage
        """
        stage = await self._trust_service.get_trust_stage(user_id)

        explanations = {
            TrustStage.NEW: (
                "We're still getting to know each other, so I want to make sure "
                "I understand what's helpful before jumping in. As we work together "
                "more, I'll get a better sense of when to take initiative."
            ),
            TrustStage.BUILDING: (
                "We've been working together for a bit, and I'm starting to learn "
                "your preferences. I'll occasionally suggest things, but I still "
                "want to make sure I'm being helpful rather than presumptuous."
            ),
            TrustStage.ESTABLISHED: (
                "I do try to be proactive when I notice things that might need "
                "your attention. If you'd like me to be more autonomous, just "
                "let me know - like saying 'just handle it' or 'you don't need "
                "to ask about that.'"
            ),
            TrustStage.TRUSTED: (
                "I actually do handle quite a bit proactively! If there's something "
                "specific you'd like me to take more initiative on, let me know "
                "and I'll adjust."
            ),
        }

        return explanations.get(stage, explanations[TrustStage.NEW])

    async def explain_behavior_change(
        self,
        user_id: UUID,
        old_stage: TrustStage,
        new_stage: TrustStage,
    ) -> str:
        """
        Explain a change in behavior due to stage transition.

        Used when Piper's behavior noticeably changes and user asks why.

        Args:
            user_id: User whose stage changed
            old_stage: Previous trust stage
            new_stage: New trust stage

        Returns:
            Explanation of the behavior change
        """
        if new_stage.value > old_stage.value:
            # Progression
            return self._explain_progression(old_stage, new_stage)
        else:
            # Regression
            return self._explain_regression(old_stage, new_stage)

    def _explain_progression(
        self,
        old_stage: TrustStage,
        new_stage: TrustStage,
    ) -> str:
        """Explain moving to a higher trust stage."""
        progressions = {
            (TrustStage.NEW, TrustStage.BUILDING): (
                "We've been working together successfully, so I'm starting to "
                "offer more suggestions. I'll still ask before doing anything "
                "significant."
            ),
            (TrustStage.BUILDING, TrustStage.ESTABLISHED): (
                "After all our successful collaborations, I feel comfortable "
                "being more proactive. I'll point out things I notice without "
                "waiting to be asked."
            ),
            (TrustStage.ESTABLISHED, TrustStage.TRUSTED): (
                "You've let me know it's okay to act more autonomously, so "
                "I'll take care of routine things on your behalf. I'll always "
                "keep you informed about what I've done."
            ),
        }

        key = (old_stage, new_stage)
        return progressions.get(
            key, "Our working relationship has evolved, so I'm adjusting how I help you."
        )

    def _explain_regression(
        self,
        old_stage: TrustStage,
        new_stage: TrustStage,
    ) -> str:
        """Explain moving to a lower trust stage."""
        return (
            "I've noticed I might have overstepped recently, so I'm going to "
            "be more careful about checking with you first. I want to make sure "
            "I'm being helpful in the way you prefer."
        )

    def get_followup_offer(self, context: ExplanationContext) -> str:
        """
        Get an appropriate follow-up offer based on context.

        Supports conversational flow after explanations.

        Args:
            context: What type of explanation was just given

        Returns:
            A natural follow-up question or offer
        """
        offers = {
            ExplanationContext.CURRENT_STAGE: ("Would you like me to be more or less proactive?"),
            ExplanationContext.PROACTIVE_ACTION: (
                "Should I check with you before doing something like this next time?"
            ),
            ExplanationContext.WHY_NOT_PROACTIVE: (
                "Is there something specific you'd like me to handle more independently?"
            ),
            ExplanationContext.BEHAVIOR_CHANGE: (
                "Does this way of working together feel right to you?"
            ),
        }

        return offers.get(context, "Let me know how I can adjust.")
