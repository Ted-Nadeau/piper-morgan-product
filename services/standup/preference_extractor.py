"""
Standup Preference Extractor - Rule-based preference extraction

Issue #555: STANDUP-LEARNING - User Preference Learning
Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Extracts user preferences from conversation turns using pattern matching.
PM Decision (2026-01-08): Start with rule-based (Option A), evolve to LLM later (#558).

Supported patterns:
- Content filters: "focus on X", "prioritize X", "mainly X"
- Exclusions: "skip X", "ignore X", "don't include X"
- Format: "brief", "detailed", "bullet points"
- Timing: "morning at 9am", "daily", "every Monday", "weekly"
- Notifications: "notify via Slack", "email summary", "no notifications"
"""

import logging
import re
from typing import List, Optional, Tuple

from services.standup.preference_models import ExtractedPreference, PreferenceSource, PreferenceType

logger = logging.getLogger(__name__)


class PreferenceExtractor:
    """
    Extract preferences from conversation turns using rule-based pattern matching.

    Usage:
        extractor = PreferenceExtractor()
        preferences = extractor.extract_from_turn("focus on GitHub and skip docs")
        # Returns: [ExtractedPreference(type=CONTENT_FILTER, key="focus", value="github"),
        #           ExtractedPreference(type=EXCLUSION, key="exclude", value="docs")]
    """

    def __init__(self):
        """Initialize pattern matchers for each preference type."""
        # Compile regex patterns for efficiency
        self._init_patterns()

    def _init_patterns(self) -> None:
        """Initialize regex patterns for preference extraction."""
        # Content filter patterns: "focus on X", "prioritize X", "mainly X"
        self.content_filter_patterns = [
            (r"focus\s+on\s+(\w+)", "focus"),
            (r"prioritize\s+(\w+)", "focus"),
            (r"mainly\s+(\w+)", "focus"),
            (r"concentrate\s+on\s+(\w+)", "focus"),
            (r"interested\s+in\s+(\w+)", "focus"),
            (r"care\s+about\s+(\w+)", "focus"),
            (r"show\s+me\s+(\w+)", "focus"),
        ]

        # Exclusion patterns: "skip X", "ignore X", "don't include X"
        self.exclusion_patterns = [
            (r"skip\s+(\w+)", "exclude"),
            (r"ignore\s+(\w+)", "exclude"),
            (r"don'?t\s+include\s+(\w+)", "exclude"),
            (r"exclude\s+(\w+)", "exclude"),
            (r"no\s+(\w+)\s+updates?", "exclude"),
            (r"without\s+(\w+)", "exclude"),
            (r"leave\s+out\s+(\w+)", "exclude"),
            (r"hide\s+(\w+)", "exclude"),
        ]

        # Format patterns: "brief", "detailed", "bullet points"
        self.format_patterns = [
            (r"\b(brief|short|concise|quick)\b", "format", "brief"),
            (r"\b(detailed|verbose|comprehensive|thorough)\b", "format", "detailed"),
            (r"\b(bullet\s*points?|bullets|bulleted)\b", "format", "bullets"),
            (r"\b(summary|summarize)\b", "format", "summary"),
            (r"make\s+it\s+(brief|short|detailed)", "format", None),  # capture group
            (r"keep\s+it\s+(brief|short|simple)", "format", "brief"),
        ]

        # Timing patterns: "morning at 9am", "daily", "every Monday", "weekly"
        self.timing_patterns = [
            (r"(?:morning|at)\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)", "time", None),
            (r"(\d{1,2}(?::\d{2})?\s*(?:am|pm))", "time", None),
            (r"\b(daily|every\s*day)\b", "frequency", "daily"),
            (r"\b(weekly|every\s*week)\b", "frequency", "weekly"),
            (r"every\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", "day", None),
            (r"\b(weekdays?|weekends?)\b", "days", None),
        ]

        # Notification patterns: "notify via Slack", "email summary"
        # Be specific to avoid false positives from "exclude notifications"
        self.notification_patterns = [
            (r"notify\s+(?:me\s+)?(?:via\s+)?(\w+)", "channel", None),
            (r"send\s+(?:updates?\s+)?to\s+(\w+)", "channel", None),
            (r"(slack|email|sms|teams)\s+(?:notification|message|update)s?", "channel", None),
            (r"email\s+(summary|digest|update)", "channel", "email"),
            (r"slack\s+(message|notification|update)", "channel", "slack"),
            (r"\bno\s+notifications?\b", "channel", "none"),
            (r"don'?t\s+notify\s+me", "channel", "none"),
            (r"turn\s+off\s+notifications?", "channel", "none"),
        ]

        # Temporary override patterns: "just for today", "only this time"
        self.temporary_patterns = [
            r"just\s+(?:for\s+)?today",
            r"only\s+(?:for\s+)?today",
            r"this\s+time\s+only",
            r"only\s+this\s+time",
            r"for\s+now",
            r"temporarily",
            r"one\s+time",
            r"this\s+once",
        ]

    def extract_from_turn(self, message: str) -> List[ExtractedPreference]:
        """
        Parse user message for preference expressions.

        Args:
            message: User's conversation turn text

        Returns:
            List of extracted preferences (may be empty)

        Examples:
            "focus on GitHub" → [ExtractedPreference(type=CONTENT_FILTER, key="focus", value="github")]
            "skip docs and make it brief" → [ExtractedPreference(type=EXCLUSION, ...), ExtractedPreference(type=FORMAT, ...)]
        """
        if not message or not message.strip():
            return []

        preferences: List[ExtractedPreference] = []
        message_lower = message.lower().strip()

        # Check if this is a temporary override
        is_temporary = self._is_temporary_override(message_lower)

        # Extract each preference type
        preferences.extend(self._extract_content_filters(message_lower, is_temporary))
        preferences.extend(self._extract_exclusions(message_lower, is_temporary))
        preferences.extend(self._extract_format(message_lower, is_temporary))
        preferences.extend(self._extract_timing(message_lower, is_temporary))
        preferences.extend(self._extract_notifications(message_lower, is_temporary))

        if preferences:
            logger.info(f"Extracted {len(preferences)} preferences from: '{message[:50]}...'")
            for pref in preferences:
                logger.debug(f"  - {pref.preference_type.value}: {pref.key}={pref.value}")

        return preferences

    def _is_temporary_override(self, message: str) -> bool:
        """Check if message indicates a temporary override."""
        for pattern in self.temporary_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        return False

    def _extract_content_filters(
        self, message: str, is_temporary: bool
    ) -> List[ExtractedPreference]:
        """Extract content filter preferences."""
        preferences = []
        for pattern, key in self.content_filter_patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                value = self._normalize_value(match)
                preferences.append(
                    ExtractedPreference(
                        raw_text=message,
                        preference_type=PreferenceType.CONTENT_FILTER,
                        key=key,
                        value=value,
                        confidence=0.8,  # Explicit mention = higher confidence
                        source=PreferenceSource.EXPLICIT,
                        is_temporary=is_temporary,
                    )
                )
        return preferences

    def _extract_exclusions(self, message: str, is_temporary: bool) -> List[ExtractedPreference]:
        """Extract exclusion preferences."""
        preferences = []
        for pattern, key in self.exclusion_patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                value = self._normalize_value(match)
                preferences.append(
                    ExtractedPreference(
                        raw_text=message,
                        preference_type=PreferenceType.EXCLUSION,
                        key=key,
                        value=value,
                        confidence=0.8,
                        source=PreferenceSource.EXPLICIT,
                        is_temporary=is_temporary,
                    )
                )
        return preferences

    def _extract_format(self, message: str, is_temporary: bool) -> List[ExtractedPreference]:
        """Extract format preferences."""
        preferences = []
        for item in self.format_patterns:
            pattern, key, fixed_value = item
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                value = fixed_value if fixed_value else self._normalize_format_value(match)
                if value:
                    preferences.append(
                        ExtractedPreference(
                            raw_text=message,
                            preference_type=PreferenceType.FORMAT,
                            key=key,
                            value=value,
                            confidence=0.85,  # Format preferences are usually clear
                            source=PreferenceSource.EXPLICIT,
                            is_temporary=is_temporary,
                        )
                    )
        # Deduplicate by value
        seen_values = set()
        unique_prefs = []
        for pref in preferences:
            if pref.value not in seen_values:
                seen_values.add(pref.value)
                unique_prefs.append(pref)
        return unique_prefs

    def _extract_timing(self, message: str, is_temporary: bool) -> List[ExtractedPreference]:
        """Extract timing preferences."""
        preferences = []
        for item in self.timing_patterns:
            pattern, key, fixed_value = item
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                value = fixed_value if fixed_value else self._normalize_timing_value(match)
                if value:
                    preferences.append(
                        ExtractedPreference(
                            raw_text=message,
                            preference_type=PreferenceType.TIMING,
                            key=key,
                            value=value,
                            confidence=0.9,  # Timing is usually explicit
                            source=PreferenceSource.EXPLICIT,
                            is_temporary=is_temporary,
                        )
                    )
        return preferences

    def _extract_notifications(self, message: str, is_temporary: bool) -> List[ExtractedPreference]:
        """Extract notification preferences."""
        preferences = []
        for item in self.notification_patterns:
            pattern, key, fixed_value = item
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                value = fixed_value if fixed_value else self._normalize_value(match)
                if value:
                    preferences.append(
                        ExtractedPreference(
                            raw_text=message,
                            preference_type=PreferenceType.NOTIFICATION,
                            key=key,
                            value=value,
                            confidence=0.85,
                            source=PreferenceSource.EXPLICIT,
                            is_temporary=is_temporary,
                        )
                    )
        # Deduplicate
        seen_values = set()
        unique_prefs = []
        for pref in preferences:
            if pref.value not in seen_values:
                seen_values.add(pref.value)
                unique_prefs.append(pref)
        return unique_prefs

    def _normalize_value(self, value: str) -> str:
        """Normalize extracted value (lowercase, strip)."""
        return value.lower().strip()

    def _normalize_format_value(self, value: str) -> str:
        """Normalize format values to standard terms."""
        value = value.lower().strip()
        if value in ("brief", "short", "concise", "quick"):
            return "brief"
        elif value in ("detailed", "verbose", "comprehensive", "thorough"):
            return "detailed"
        elif "bullet" in value:
            return "bullets"
        elif value in ("summary", "summarize"):
            return "summary"
        return value

    def _normalize_timing_value(self, value: str) -> str:
        """Normalize timing values."""
        value = value.lower().strip()
        # Normalize time formats
        if re.match(r"\d{1,2}(?::\d{2})?\s*(?:am|pm)?", value):
            return self._normalize_time(value)
        # Normalize day names
        days = {
            "monday": "monday",
            "tuesday": "tuesday",
            "wednesday": "wednesday",
            "thursday": "thursday",
            "friday": "friday",
            "saturday": "saturday",
            "sunday": "sunday",
        }
        if value in days:
            return days[value]
        return value

    def _normalize_time(self, time_str: str) -> str:
        """Normalize time string to HH:MM format."""
        time_str = time_str.lower().strip()
        # Handle "9am" -> "09:00"
        match = re.match(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", time_str)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2) or 0)
            period = match.group(3)

            if period == "pm" and hour < 12:
                hour += 12
            elif period == "am" and hour == 12:
                hour = 0

            return f"{hour:02d}:{minute:02d}"
        return time_str


def extract_preferences(message: str) -> List[ExtractedPreference]:
    """
    Convenience function for extracting preferences from a message.

    Args:
        message: User's conversation turn text

    Returns:
        List of extracted preferences
    """
    extractor = PreferenceExtractor()
    return extractor.extract_from_turn(message)
