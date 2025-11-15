"""Context matching for pattern application"""
from datetime import datetime, time
from typing import Any, Dict


class ContextMatcher:
    """Match current context to pattern trigger conditions"""

    @classmethod
    async def matches(
        cls, pattern_context: Dict[str, Any], current_context: Dict[str, Any]
    ) -> bool:
        """
        Check if pattern applies to current context

        Args:
            pattern_context: Trigger conditions from pattern.pattern_data
            current_context: Current execution context

        Returns:
            bool: True if pattern should trigger
        """
        # No triggers defined = always matches (for testing)
        if not pattern_context:
            return True

        # Check temporal triggers
        if "trigger_time" in pattern_context:
            if not cls._check_temporal(
                pattern_context["trigger_time"], current_context
            ):
                return False

        # Check sequential triggers (after specific action)
        if "after_action" in pattern_context:
            last_action = current_context.get("last_action")
            if last_action != pattern_context["after_action"]:
                return False

        # Check intent matching (optional)
        if "trigger_intent" in pattern_context:
            current_intent = current_context.get("intent")
            if current_intent != pattern_context["trigger_intent"]:
                return False

        # All conditions met
        return True

    @staticmethod
    def _check_temporal(
        trigger_time: str, current_context: Dict[str, Any]
    ) -> bool:
        """
        Check if current time matches trigger

        Args:
            trigger_time: Time specification (e.g., "after standup", "9am", "eod")
            current_context: Must contain "current_time" or "current_event"

        Returns:
            bool: True if time matches
        """
        # Simple keyword matching for alpha
        trigger_lower = trigger_time.lower()

        # Check for event-based temporal triggers
        current_event = current_context.get("current_event", "").lower()
        if current_event:
            # "after standup" matches if current_event is "standup_complete"
            if "standup" in trigger_lower and "standup" in current_event:
                return True
            # "end of day" matches if current_event is "eod" or "end_of_day"
            if "eod" in trigger_lower or "end of day" in trigger_lower:
                if "eod" in current_event or "end_of_day" in current_event:
                    return True

        # Check for time-based triggers (future enhancement)
        current_time = current_context.get("current_time")
        if current_time and isinstance(current_time, (datetime, time)):
            # TODO: Parse time specifications like "9am", "monday morning"
            # For alpha: Simple hour matching
            if "9am" in trigger_lower or "morning" in trigger_lower:
                hour = (
                    current_time.hour if hasattr(current_time, "hour") else 0
                )
                return 7 <= hour <= 11

        # Default: trigger doesn't match
        return False

    @staticmethod
    def _calculate_similarity(
        conditions: Dict[str, Any], current_context: Dict[str, Any]
    ) -> float:
        """
        Calculate similarity between conditions and context
        (Future enhancement - defer to post-alpha)

        Returns:
            float: Similarity score 0.0-1.0
        """
        # Placeholder for future similarity matching
        return 1.0  # For alpha, assume match if present
