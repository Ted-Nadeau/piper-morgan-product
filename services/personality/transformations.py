"""
Transformation Service - Core Enhancement Logic

Applies personality transformations in order: warmth → confidence → actions
Rule-based transformations for fast, deterministic enhancement <100ms
"""

import logging
import re
from typing import Any, Dict, List, Optional

from .personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    Enhancement,
    PersonalityProfile,
    ResponseContext,
)

logger = logging.getLogger(__name__)


class TransformationService:
    """Domain service for content transformation"""

    def __init__(self):
        self.warmth_phrases = {
            0.8: ["Great work!", "Excellent!", "Perfect!", "Outstanding!"],
            0.6: ["Nice job!", "Well done!", "Good progress!", "Looking good!"],
            0.4: ["Thanks for", "I've got", "Here's what", "Let me help"],
            0.2: ["", "", "", ""],  # Minimal warmth additions
        }

        self.confidence_indicators = {
            ConfidenceDisplayStyle.NUMERIC: lambda conf: f"({conf:.0%} confident)",
            ConfidenceDisplayStyle.DESCRIPTIVE: self._descriptive_confidence,
            ConfidenceDisplayStyle.CONTEXTUAL: self._contextual_confidence,
            ConfidenceDisplayStyle.HIDDEN: lambda conf: "",
        }

        self.action_patterns = {
            ActionLevel.HIGH: [
                "Next steps:",
                "Here's what to do:",
                "Action items:",
                "To proceed:",
                "Your next move:",
                "Follow up by:",
            ],
            ActionLevel.MEDIUM: [
                "Consider:",
                "You might:",
                "Options include:",
                "Next you could:",
                "To continue:",
            ],
            ActionLevel.LOW: ["If needed:", "Optionally:", "When ready:"],
        }

    def add_warmth(self, content: str, warmth_level: float, context: ResponseContext) -> str:
        """Add appropriate warmth without losing professionalism"""
        if warmth_level <= 0.2:
            return content

        # Choose warmth level bracket
        if warmth_level >= 0.8:
            bracket = 0.8
        elif warmth_level >= 0.6:
            bracket = 0.6
        elif warmth_level >= 0.4:
            bracket = 0.4
        else:
            bracket = 0.2

        phrases = self.warmth_phrases[bracket]

        # Add warmth based on response type and context
        if context.response_type.value == "error":
            warm_content = self._add_error_warmth(content, warmth_level)
        elif context.intent_action in ["create_ticket", "create_task", "create_feature"]:
            # Success scenarios get congratulatory warmth
            if phrases[0]:  # Non-empty phrase
                warm_content = f"{phrases[0]} {content}"
            else:
                warm_content = content
        elif "analysis" in context.intent_category.lower():
            # Analysis gets supportive warmth
            if phrases[2]:  # "Here's what" style
                warm_content = f"{phrases[2]} I found: {content}"
            else:
                warm_content = content
        else:
            # General warmth application
            if phrases[1]:  # "Well done" style
                warm_content = f"{phrases[1]} {content}"
            else:
                warm_content = content

        return warm_content

    def inject_confidence(
        self,
        content: str,
        confidence: float,
        style: ConfidenceDisplayStyle,
        context: ResponseContext,
    ) -> str:
        """Add confidence indicators based on intent confidence"""
        if style == ConfidenceDisplayStyle.HIDDEN:
            return content

        indicator = self.confidence_indicators[style](confidence)
        if not indicator:
            return content

        # Insert confidence indicator appropriately
        if context.response_type.value == "error":
            # Don't add confidence to error messages
            return content
        elif "analysis" in context.intent_category.lower():
            # Add confidence at end of analysis
            return f"{content} {indicator}"
        elif confidence < 0.3:
            # Low confidence gets supportive framing
            return f"{content} (I'm working with limited information here, so please verify these details)"
        else:
            # Standard confidence placement
            sentences = content.split(". ")
            if len(sentences) > 1:
                # Add to first sentence
                sentences[0] = f"{sentences[0]} {indicator}"
                return ". ".join(sentences)
            else:
                return f"{content} {indicator}"

    def extract_actions(
        self, content: str, action_level: ActionLevel, context: ResponseContext
    ) -> str:
        """Make response actionable with clear next steps"""
        if action_level == ActionLevel.LOW:
            return content

        # Extract potential actions from content
        action_items = self._identify_action_opportunities(content, context)

        if not action_items:
            # Generate contextual actions
            action_items = self._generate_contextual_actions(context)

        if not action_items:
            return content

        # Format actions based on level
        action_intro = self._get_action_intro(action_level)

        if action_level == ActionLevel.HIGH:
            action_text = f"\n\n{action_intro}\n" + "\n".join(f"• {item}" for item in action_items)
        else:  # MEDIUM
            action_text = f" {action_intro} " + ", ".join(action_items[:2]) + "."

        return content + action_text

    def _add_error_warmth(self, content: str, warmth_level: float) -> str:
        """Add supportive warmth to error messages"""
        if warmth_level >= 0.8:
            prefix = "I understand this is frustrating. "
        elif warmth_level >= 0.6:
            prefix = "No worries - "
        elif warmth_level >= 0.4:
            prefix = "Let me help. "
        else:
            return content

        return prefix + content

    def _descriptive_confidence(self, confidence: float) -> str:
        """Convert confidence to descriptive text"""
        if confidence >= 0.9:
            return "(very confident)"
        elif confidence >= 0.7:
            return "(confident)"
        elif confidence >= 0.5:
            return "(moderately confident)"
        elif confidence >= 0.3:
            return "(less certain)"
        else:
            return "(uncertain)"

    def _contextual_confidence(self, confidence: float) -> str:
        """Generate contextual confidence indicators"""
        if confidence >= 0.8:
            return "(based on clear patterns)"
        elif confidence >= 0.6:
            return "(based on available data)"
        elif confidence >= 0.4:
            return "(preliminary assessment)"
        else:
            return "(limited information available)"

    def _identify_action_opportunities(self, content: str, context: ResponseContext) -> List[str]:
        """Extract potential actions from response content"""
        actions = []

        # Look for common action patterns
        if "issue" in content.lower() and "create" in context.intent_action:
            actions.append("Review the created issue for accuracy")
            actions.append("Add any missing details or context")

        if "analysis" in context.intent_category.lower():
            actions.append("Review the analysis findings")
            if "error" in content.lower() or "problem" in content.lower():
                actions.append("Consider implementing recommended fixes")

        if "github" in content.lower():
            actions.append("Check the related GitHub activity")

        if context.intent_confidence < 0.5:
            actions.append("Verify these results with additional context")

        return actions[:3]  # Limit to 3 actions

    def _generate_contextual_actions(self, context: ResponseContext) -> List[str]:
        """Generate actions based on context when none found in content"""
        actions = []

        if context.intent_category == "analysis":
            actions.append("Review the provided analysis")
            actions.append("Consider next steps based on findings")

        elif context.intent_category == "execution":
            actions.append("Verify the task completed successfully")
            actions.append("Check for any follow-up requirements")

        elif context.intent_category == "query":
            actions.append("Let me know if you need more details")

        return actions

    def _get_action_intro(self, action_level: ActionLevel) -> str:
        """Get appropriate action introduction"""
        intros = self.action_patterns[action_level]
        # Use first intro for consistency
        return intros[0] if intros else "Next:"
