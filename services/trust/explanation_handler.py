"""
ExplanationHandler service for processing trust explanation queries.

This service orchestrates the flow from query detection to explanation generation,
providing a clean integration point for the intent processing pipeline.

Usage:
    handler = ExplanationHandler(trust_service)

    # Check if message needs explanation handling
    result = await handler.try_handle(user_id, message)

    if result.handled:
        return result.response  # Explanation response
    else:
        # Continue with normal intent processing
        pass
"""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from services.shared_types import TrustStage
from services.trust.explanation_detector import (
    ExplanationDetectionResult,
    ExplanationDetector,
    ExplanationQueryType,
)
from services.trust.trust_explainer import ExplanationContext, TrustExplainer


@dataclass
class ExplanationHandlerResult:
    """Result of attempting to handle an explanation query."""

    handled: bool
    response: Optional[str] = None
    query_type: Optional[ExplanationQueryType] = None
    followup_offer: Optional[str] = None

    @property
    def full_response(self) -> Optional[str]:
        """Get full response including follow-up offer if applicable."""
        if not self.response:
            return None
        if self.followup_offer:
            return f"{self.response}\n\n{self.followup_offer}"
        return self.response


class ExplanationHandler:
    """
    Handles trust explanation queries by routing to appropriate explainer methods.

    This is the integration layer between query detection and explanation generation.
    It provides a simple API for the intent processing pipeline to check if a message
    should be handled as an explanation query.

    Architecture:
        Message → ExplanationDetector → ExplanationHandler → TrustExplainer → Response

    Design principle: The handler returns structured results rather than raising
    exceptions, making it easy to integrate with existing intent processing flows.
    """

    def __init__(self, trust_service):
        """
        Initialize with trust computation service.

        Args:
            trust_service: TrustComputationService instance
        """
        self._detector = ExplanationDetector()
        self._explainer = TrustExplainer(trust_service)
        self._trust_service = trust_service

    async def try_handle(
        self,
        user_id: UUID,
        message: str,
        recent_action: Optional[str] = None,
    ) -> ExplanationHandlerResult:
        """
        Try to handle message as an explanation query.

        This is the main entry point. Call this with user messages to check
        if they should be handled as explanation queries rather than normal
        intent processing.

        Args:
            user_id: User asking the question
            message: User's message
            recent_action: Optional description of recent proactive action
                          (for "why did you do that?" context)

        Returns:
            ExplanationHandlerResult indicating if handled and the response
        """
        # Detect if this is an explanation query
        detection = self._detector.detect(message)

        if not detection.is_explanation_query:
            return ExplanationHandlerResult(handled=False)

        # Route to appropriate explainer method
        try:
            response = await self._route_to_explainer(
                user_id=user_id,
                query_type=detection.query_type,
                recent_action=recent_action,
            )

            followup = self._get_followup_for_query_type(detection.query_type)

            return ExplanationHandlerResult(
                handled=True,
                response=response,
                query_type=detection.query_type,
                followup_offer=followup,
            )

        except Exception as e:
            # Log error but return graceful fallback
            # In production, this should use proper logging
            return ExplanationHandlerResult(
                handled=True,
                response=self._get_fallback_response(detection.query_type),
                query_type=detection.query_type,
            )

    async def _route_to_explainer(
        self,
        user_id: UUID,
        query_type: ExplanationQueryType,
        recent_action: Optional[str] = None,
    ) -> str:
        """Route to appropriate explainer method based on query type."""
        if query_type == ExplanationQueryType.WHY_ACTION:
            # User asking about a specific action taken
            action = recent_action or "took that action"
            return await self._explainer.explain_proactive_action(user_id, action)

        elif query_type == ExplanationQueryType.WHY_NO_ACTION:
            # User asking why we're not more proactive
            return await self._explainer.explain_why_not_proactive(user_id)

        elif query_type == ExplanationQueryType.TRUST_LEVEL:
            # User asking about our relationship
            return await self._explainer.explain_current_stage(user_id)

        elif query_type == ExplanationQueryType.BEHAVIOR_QUESTION:
            # General behavior question - explain current stage
            return await self._explainer.explain_current_stage(user_id)

        else:
            # Fallback to current stage explanation
            return await self._explainer.explain_current_stage(user_id)

    def _get_followup_for_query_type(
        self,
        query_type: ExplanationQueryType,
    ) -> Optional[str]:
        """Get appropriate follow-up offer for query type."""
        context_map = {
            ExplanationQueryType.WHY_ACTION: ExplanationContext.PROACTIVE_ACTION,
            ExplanationQueryType.WHY_NO_ACTION: ExplanationContext.WHY_NOT_PROACTIVE,
            ExplanationQueryType.TRUST_LEVEL: ExplanationContext.CURRENT_STAGE,
            ExplanationQueryType.BEHAVIOR_QUESTION: ExplanationContext.BEHAVIOR_CHANGE,
        }

        context = context_map.get(query_type)
        if context:
            return self._explainer.get_followup_offer(context)
        return None

    def _get_fallback_response(self, query_type: ExplanationQueryType) -> str:
        """Get fallback response when explainer fails."""
        fallbacks = {
            ExplanationQueryType.WHY_ACTION: (
                "I try to be helpful based on what I've learned about how you work. "
                "Let me know if I should adjust my approach."
            ),
            ExplanationQueryType.WHY_NO_ACTION: (
                "I want to make sure I'm being helpful without being presumptuous. "
                "As we work together more, I'll get a better sense of when to take initiative."
            ),
            ExplanationQueryType.TRUST_LEVEL: (
                "We're developing our working relationship. I try to balance being "
                "helpful with being respectful of your preferences."
            ),
            ExplanationQueryType.BEHAVIOR_QUESTION: (
                "I adapt how I work based on our interactions. Let me know if "
                "you'd like me to adjust anything."
            ),
        }
        return fallbacks.get(query_type, "I'm here to help in whatever way works best for you.")

    async def is_explanation_query(self, message: str) -> bool:
        """
        Quick check if message is an explanation query.

        Convenience method for pre-filtering before full handling.
        """
        detection = self._detector.detect(message)
        return detection.is_explanation_query

    async def get_query_type(self, message: str) -> Optional[ExplanationQueryType]:
        """
        Get the query type for a message.

        Returns None if not an explanation query.
        """
        detection = self._detector.detect(message)
        if detection.is_explanation_query:
            return detection.query_type
        return None

    async def handle_with_context(
        self,
        user_id: UUID,
        message: str,
        old_stage: Optional[TrustStage] = None,
        new_stage: Optional[TrustStage] = None,
    ) -> ExplanationHandlerResult:
        """
        Handle explanation query with stage change context.

        Use this when the user might be asking about a recent behavior change
        due to stage transition.

        Args:
            user_id: User asking
            message: User's message
            old_stage: Previous stage (if known)
            new_stage: Current stage (if changed)

        Returns:
            ExplanationHandlerResult with stage-aware explanation
        """
        detection = self._detector.detect(message)

        if not detection.is_explanation_query:
            return ExplanationHandlerResult(handled=False)

        # If we have stage change context and it's a behavior question, use that
        if (
            old_stage
            and new_stage
            and old_stage != new_stage
            and detection.query_type == ExplanationQueryType.BEHAVIOR_QUESTION
        ):
            response = await self._explainer.explain_behavior_change(user_id, old_stage, new_stage)
            return ExplanationHandlerResult(
                handled=True,
                response=response,
                query_type=detection.query_type,
                followup_offer=self._explainer.get_followup_offer(
                    ExplanationContext.BEHAVIOR_CHANGE
                ),
            )

        # Otherwise, use standard handling
        return await self.try_handle(user_id, message)
