"""
Feedback Narrative Bridge - Transform feedback data to warm acknowledgments.

This module transforms feedback data into human-readable acknowledgments
that treat feedback as a Moment of connection, not just data submission.

Issue #623: GRAMMAR-TRANSFORM: Feedback System
Phase 2: Narrative Bridge
"""

from dataclasses import dataclass
from typing import Optional

from services.feedback.response_context import FeedbackResponseContext


@dataclass
class FeedbackNarrativeBridge:
    """Transform feedback data into warm, connection-oriented narratives.

    In MUX grammar: this bridges the Moment of feedback to human expression.
    The goal is responses that acknowledge the trust in sharing feedback.
    """

    # Type-specific acknowledgments
    TYPE_ACKNOWLEDGMENTS = {
        "bug": "Thanks for flagging that - I'll make sure this gets attention",
        "feature": "Great suggestion - I've noted this for the team",
        "ux": "Thanks for helping improve the experience",
        "general": "Thanks for the feedback - it helps me improve",
    }

    # First-time contributor acknowledgments
    FIRST_TIME_ACKNOWLEDGMENTS = {
        "bug": "Thanks for taking the time to report this - it really helps",
        "feature": "Thanks for your first suggestion - these insights are valuable",
        "ux": "Thanks for sharing this - understanding your experience helps us improve",
        "general": "Thanks for your feedback - it's great to hear from you",
    }

    # Repeat contributor acknowledgments
    REPEAT_CONTRIBUTOR_ACKNOWLEDGMENTS = {
        "bug": "Thanks again for flagging this - your reports are always helpful",
        "feature": "Another great idea - thanks for continuing to share",
        "ux": "Thanks for the ongoing feedback - it shapes how we improve",
        "general": "Thanks for staying in touch - your input is valued",
    }

    # Sentiment-aware additions
    SENTIMENT_PHRASES = {
        "positive": "I'm glad you're enjoying it!",
        "negative": "I hear your frustration - we'll look into this.",
        "neutral": "",
    }

    # Rating acknowledgments
    RATING_PHRASES = {
        5: "I'm glad you're enjoying the experience!",
        4: "Thanks for the positive rating!",
        3: "Thanks for the honest assessment.",
        2: "I appreciate you sharing where we can improve.",
        1: "I'm sorry the experience hasn't been great - we'll work on it.",
    }

    def acknowledge_feedback(self, ctx: FeedbackResponseContext) -> str:
        """Generate warm acknowledgment for feedback.

        This is the main method - creates a complete acknowledgment
        that treats the feedback as a Moment of connection.

        Examples:
            Bug report -> "Thanks for flagging that - I'll make sure this gets attention"
            Feature from repeat contributor -> "Another great idea - thanks for continuing to share"
        """
        if not ctx.feedback_available:
            return "Thanks for reaching out - I couldn't process the feedback right now, but I appreciate you taking the time."

        # Choose acknowledgment based on contributor status
        if ctx.is_first_feedback:
            base = self.FIRST_TIME_ACKNOWLEDGMENTS.get(
                ctx.feedback_type,
                self.FIRST_TIME_ACKNOWLEDGMENTS["general"],
            )
        elif ctx.is_repeat_contributor():
            base = self.REPEAT_CONTRIBUTOR_ACKNOWLEDGMENTS.get(
                ctx.feedback_type,
                self.REPEAT_CONTRIBUTOR_ACKNOWLEDGMENTS["general"],
            )
        else:
            base = self.TYPE_ACKNOWLEDGMENTS.get(
                ctx.feedback_type,
                self.TYPE_ACKNOWLEDGMENTS["general"],
            )

        return base

    def acknowledge_with_sentiment(self, ctx: FeedbackResponseContext) -> str:
        """Generate acknowledgment with sentiment-aware addition.

        Adds a sentiment-appropriate phrase to the base acknowledgment.

        Examples:
            Positive bug report -> "Thanks for flagging that. I'm glad you're enjoying it!"
            Negative feedback -> "Thanks for the feedback. I hear your frustration - we'll look into this."
        """
        base = self.acknowledge_feedback(ctx)
        sentiment_phrase = self.SENTIMENT_PHRASES.get(ctx.sentiment, "")

        if sentiment_phrase:
            return f"{base}. {sentiment_phrase}"
        return base

    def acknowledge_with_rating(self, ctx: FeedbackResponseContext) -> str:
        """Generate acknowledgment with rating-specific response.

        For feedback that includes a rating, add appropriate response.

        Examples:
            5-star rating -> "Thanks! I'm glad you're enjoying the experience!"
            2-star rating -> "Thanks for your feedback. I appreciate you sharing where we can improve."
        """
        base = self.acknowledge_feedback(ctx)

        if ctx.has_rating and ctx.rating_value:
            rating_phrase = self.RATING_PHRASES.get(ctx.rating_value)
            if rating_phrase:
                return f"{base}. {rating_phrase}"

        return base

    def narrate_feedback_type(self, feedback_type: str) -> str:
        """Describe feedback type in human terms.

        Examples:
            "bug" -> "bug report"
            "feature" -> "feature suggestion"
        """
        type_names = {
            "bug": "bug report",
            "feature": "feature suggestion",
            "ux": "experience feedback",
            "general": "feedback",
        }
        return type_names.get(feedback_type, "feedback")

    def narrate_contributor_status(self, ctx: FeedbackResponseContext) -> str:
        """Describe contributor status.

        Examples:
            First feedback -> "first time sharing feedback"
            5 previous -> "shared feedback 5 times before"
        """
        if ctx.is_first_feedback:
            return "first time sharing feedback"
        elif ctx.feedback_count > 0:
            return f"shared feedback {ctx.feedback_count} times"
        return ""

    def narrate_detailed_response(
        self,
        ctx: FeedbackResponseContext,
        include_type: bool = True,
        include_sentiment: bool = True,
    ) -> str:
        """Generate a detailed, complete response.

        Combines acknowledgment with optional type and sentiment info.

        Examples:
            "Thanks for the bug report! I'll make sure this gets attention.
             I hear your frustration - we'll look into this."
        """
        if not ctx.feedback_available:
            return (
                "Thanks for reaching out - I couldn't process the feedback "
                "right now, but I appreciate you taking the time."
            )

        parts = []

        # Base acknowledgment with type mention
        if include_type:
            type_name = self.narrate_feedback_type(ctx.feedback_type)
            parts.append(f"Thanks for the {type_name}!")
        else:
            parts.append("Thanks!")

        # Add type-specific action
        action = self._get_action_phrase(ctx.feedback_type)
        if action:
            parts.append(action)

        # Add sentiment response
        if include_sentiment and ctx.sentiment != "neutral":
            sentiment_phrase = self.SENTIMENT_PHRASES.get(ctx.sentiment)
            if sentiment_phrase:
                parts.append(sentiment_phrase)

        return " ".join(parts)

    def _get_action_phrase(self, feedback_type: str) -> str:
        """Get action phrase for feedback type."""
        actions = {
            "bug": "I'll make sure this gets attention.",
            "feature": "I've noted this for the team.",
            "ux": "This helps us improve.",
            "general": "It helps me improve.",
        }
        return actions.get(feedback_type, "It helps me improve.")
