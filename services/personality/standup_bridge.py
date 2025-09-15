"""
StandupToChatBridge - Domain Service

Bridges standup metrics to conversational chat format with personality enhancement.
Maintains data integrity while adding warm, engaging narrative flow.
"""

import logging
import re
from typing import Any, Dict, List, Optional

from .personality_profile import ActionLevel, ConfidenceDisplayStyle, PersonalityProfile

logger = logging.getLogger(__name__)


class StandupToChatBridge:
    """Service to unify standup and chat experiences"""

    def __init__(self):
        self.accomplishment_prefixes = {
            0.8: ["Outstanding work!", "Incredible progress!", "Fantastic achievement!"],
            0.6: ["Great job!", "Nice work!", "Well done!"],
            0.4: ["Good progress!", "Moving forward!", "Making headway!"],
            0.2: ["Progress made:", "Continuing work on:", "Working through:"],
        }

        self.metric_encouragements = {
            "fast": ["Lightning fast!", "Excellent performance!", "Right on track!"],
            "good": ["Good timing!", "Within target!", "Running smoothly!"],
            "slow": ["Taking a bit longer", "Working through complexity", "Building carefully"],
        }

    def adapt_standup_for_chat(self, standup_response: Dict[str, Any]) -> str:
        """Transform standup JSON to conversational format"""
        try:
            if not standup_response or "data" not in standup_response:
                return "I don't have standup information available right now."

            data = standup_response["data"]
            metadata = standup_response.get("metadata", {})

            # Build conversational narrative
            sections = []

            # Yesterday's accomplishments
            if data.get("yesterday_accomplishments"):
                sections.append(self._format_accomplishments(data["yesterday_accomplishments"]))

            # Today's priorities
            if data.get("today_priorities"):
                sections.append(self._format_priorities(data["today_priorities"]))

            # Blockers
            if data.get("blockers"):
                sections.append(self._format_blockers(data["blockers"]))
            else:
                sections.append("No blockers - clear path ahead! 🚀")

            # Performance summary
            if data.get("generation_time_ms") and data.get("time_saved_minutes"):
                sections.append(self._format_performance_summary(data, metadata))

            return "\n\n".join(sections)

        except Exception as e:
            logger.error(f"Error adapting standup for chat: {e}")
            return "I encountered an issue formatting your standup. Here's the raw data available."

    def apply_personality_to_standup(
        self, standup_data: Dict[str, Any], profile: PersonalityProfile
    ) -> str:
        """Apply personality preferences to standup content"""
        try:
            # First convert to chat format
            base_content = self.adapt_standup_for_chat(standup_data)

            # Apply personality enhancements
            enhanced_content = self._enhance_with_personality(base_content, profile, standup_data)

            return enhanced_content

        except Exception as e:
            logger.error(f"Error applying personality to standup: {e}")
            return self.adapt_standup_for_chat(standup_data)

    def _format_accomplishments(self, accomplishments: List[str]) -> str:
        """Format accomplishments with encouraging tone"""
        if not accomplishments:
            return ""

        intro = "Yesterday's achievements:"
        formatted_items = []

        for item in accomplishments:
            # Clean up the accomplishment text
            clean_item = self._clean_accomplishment_text(item)
            formatted_items.append(f"• {clean_item}")

        return f"{intro}\n" + "\n".join(formatted_items)

    def _format_priorities(self, priorities: List[str]) -> str:
        """Format today's priorities with motivational framing"""
        if not priorities:
            return ""

        intro = "Today's focus:"
        formatted_items = []

        for item in priorities:
            clean_item = self._clean_priority_text(item)
            formatted_items.append(f"• {clean_item}")

        return f"{intro}\n" + "\n".join(formatted_items)

    def _format_blockers(self, blockers: List[str]) -> str:
        """Format blockers with supportive problem-solving tone"""
        if not blockers:
            return ""

        intro = "Current challenges to work through:"
        formatted_items = []

        for item in blockers:
            clean_item = self._clean_blocker_text(item)
            formatted_items.append(f"• {clean_item}")

        return f"{intro}\n" + "\n".join(formatted_items)

    def _format_performance_summary(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Format performance metrics with encouraging context"""
        generation_time_ms = data.get("generation_time_ms", 0)
        time_saved = data.get("time_saved_minutes", 0)

        # Determine performance level
        if generation_time_ms < 5000:
            performance_level = "fast"
        elif generation_time_ms < 10000:
            performance_level = "good"
        else:
            performance_level = "slow"

        encouragement = self.metric_encouragements[performance_level][0]

        # Format time saved
        if time_saved >= 60:
            hours = int(time_saved // 60)
            minutes = int(time_saved % 60)
            time_saved_text = f"{hours}h {minutes}m"
        else:
            time_saved_text = f"{int(time_saved)}m"

        return f"Standup generated in {generation_time_ms/1000:.1f}s - {encouragement} Saved you {time_saved_text} of manual prep time."

    def _enhance_with_personality(
        self, content: str, profile: PersonalityProfile, standup_data: Dict[str, Any]
    ) -> str:
        """Apply personality profile to enhance content"""
        enhanced = content

        # Apply warmth level
        if profile.warmth_level >= 0.8:
            enhanced = self._add_high_warmth(enhanced, standup_data)
        elif profile.warmth_level >= 0.6:
            enhanced = self._add_medium_warmth(enhanced)

        # Apply action orientation
        if profile.action_orientation == ActionLevel.HIGH:
            enhanced = self._add_action_guidance(enhanced, standup_data)

        # Apply confidence display for metrics
        if profile.confidence_style != ConfidenceDisplayStyle.HIDDEN:
            enhanced = self._enhance_confidence_display(enhanced, profile.confidence_style)

        return enhanced

    def _add_high_warmth(self, content: str, standup_data: Dict[str, Any]) -> str:
        """Add high warmth personality touches"""
        # Add encouraging opening
        data = standup_data.get("data", {})
        accomplishments = data.get("yesterday_accomplishments", [])

        if accomplishments:
            warmth_intro = "What a productive day yesterday! 🌟 "
            return warmth_intro + content
        else:
            return content

    def _add_medium_warmth(self, content: str) -> str:
        """Add moderate warmth touches"""
        # Add positive framing to the start
        if "Yesterday's achievements:" in content:
            return content.replace("Yesterday's achievements:", "Nice progress yesterday:")
        return content

    def _add_action_guidance(self, content: str, standup_data: Dict[str, Any]) -> str:
        """Add actionable next steps for high action orientation"""
        data = standup_data.get("data", {})
        priorities = data.get("today_priorities", [])

        if priorities:
            action_section = "\n\nRecommended approach:\n• Start with your highest priority item\n• Break complex tasks into smaller steps\n• Check in on progress by midday"
            return content + action_section
        return content

    def _enhance_confidence_display(self, content: str, style: ConfidenceDisplayStyle) -> str:
        """Enhance confidence display based on style preference"""
        if style == ConfidenceDisplayStyle.CONTEXTUAL:
            # Add contextual confidence to performance section
            if "Standup generated" in content:
                return content.replace(
                    "Standup generated", "Based on your recent activity patterns, standup generated"
                )
        elif style == ConfidenceDisplayStyle.DESCRIPTIVE:
            # Add descriptive confidence indicators
            if "achievements:" in content:
                return content.replace(
                    "achievements:", "achievements (highly confident in accuracy):"
                )

        return content

    def _clean_accomplishment_text(self, text: str) -> str:
        """Clean up accomplishment text for better readability"""
        # Remove common prefixes like ✅, feat:, fix:
        cleaned = re.sub(r"^[✅✓☑️]\s*", "", text)
        cleaned = re.sub(r"^(feat|fix|docs|refactor|test):\s*", "", cleaned)
        cleaned = re.sub(r"^(feat|fix|docs|refactor|test)\([^)]+\):\s*", "", cleaned)

        # Capitalize first letter
        if cleaned:
            cleaned = cleaned[0].upper() + cleaned[1:]

        return cleaned

    def _clean_priority_text(self, text: str) -> str:
        """Clean up priority text"""
        # Remove emoji prefixes and normalize
        cleaned = re.sub(r"^[🎯🔥⭐]\s*", "", text)

        # Capitalize first letter
        if cleaned:
            cleaned = cleaned[0].upper() + cleaned[1:]

        return cleaned

    def _clean_blocker_text(self, text: str) -> str:
        """Clean up blocker text with supportive framing"""
        # Remove negative emoji and add supportive framing
        cleaned = re.sub(r"^[❌🚫⛔]\s*", "", text)

        # Add supportive framing if not already present
        if cleaned and not cleaned.lower().startswith(("waiting", "need", "require")):
            cleaned = f"Need to resolve: {cleaned.lower()}"

        return cleaned
