"""
Preference Applicator for Standup Generation.

Issue #555: STANDUP-LEARNING - User Preference Learning
Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Applies learned preferences to standup generation:
- Loads persisted preferences at conversation start
- Extracts preferences from conversation turns
- Filters content based on preferences
- Formats output per user preferences
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

import structlog

from services.standup.preference_extractor import PreferenceExtractor
from services.standup.preference_models import (
    ExtractedPreference,
    PreferenceSource,
    PreferenceType,
    UserStandupPreference,
)
from services.standup.preference_service import UserPreferenceService

logger = structlog.get_logger()


@dataclass
class AppliedPreferences:
    """Result of applying preferences to standup generation."""

    # Content filters applied
    focus_areas: List[str] = field(default_factory=list)
    excluded_areas: List[str] = field(default_factory=list)

    # Format preferences
    format_style: str = "standard"  # "brief", "detailed", "standard"

    # One-time overrides (not persisted)
    temporary_overrides: Dict[str, Any] = field(default_factory=dict)

    # What was applied (for transparency)
    applied_from_history: List[str] = field(default_factory=list)
    applied_from_turn: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for context passing."""
        return {
            "focus_areas": self.focus_areas,
            "excluded_areas": self.excluded_areas,
            "format_style": self.format_style,
            "temporary_overrides": self.temporary_overrides,
            "applied_from_history": self.applied_from_history,
            "applied_from_turn": self.applied_from_turn,
        }

    def describe_applied(self) -> str:
        """Human-readable description of applied preferences."""
        parts = []

        if self.focus_areas:
            parts.append(f"Focusing on: {', '.join(self.focus_areas)}")
        if self.excluded_areas:
            parts.append(f"Excluding: {', '.join(self.excluded_areas)}")
        if self.format_style != "standard":
            parts.append(f"Format: {self.format_style}")
        if self.temporary_overrides:
            parts.append(f"One-time: {', '.join(self.temporary_overrides.keys())}")

        return "; ".join(parts) if parts else "Using default preferences"


class PreferenceApplicator:
    """
    Applies user preferences to standup generation.

    Flow:
    1. Load persisted preferences for user
    2. Extract any preferences from current turn
    3. Merge with appropriate priority (explicit > inferred, current > historical)
    4. Apply to content filtering and formatting
    5. Track what was applied for transparency
    """

    def __init__(
        self,
        preference_service: Optional[UserPreferenceService] = None,
        extractor: Optional[PreferenceExtractor] = None,
    ) -> None:
        """
        Initialize applicator.

        Args:
            preference_service: Service for persisted preferences
            extractor: Preference extractor for current turn
        """
        self._service = preference_service or UserPreferenceService()
        self._extractor = extractor or PreferenceExtractor()

    async def prepare_preferences(
        self,
        user_id: str,
        current_message: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> AppliedPreferences:
        """
        Prepare preferences for standup generation.

        Loads historical preferences, extracts from current message,
        and merges with appropriate priority.

        Args:
            user_id: User identifier
            current_message: Optional current turn message to extract from
            session_id: Optional session for tracking

        Returns:
            AppliedPreferences ready for use in generation
        """
        applied = AppliedPreferences()

        # 1. Load persisted high-confidence preferences
        historical = await self._load_historical_preferences(user_id)
        self._apply_historical(applied, historical)

        # 2. Extract from current message if provided
        if current_message:
            extracted = self._extractor.extract_from_turn(current_message)
            await self._apply_extracted(applied, extracted, user_id, session_id)

        logger.info(
            "preferences_prepared",
            user_id=user_id,
            from_history=len(applied.applied_from_history),
            from_turn=len(applied.applied_from_turn),
            focus_areas=applied.focus_areas,
            excluded_areas=applied.excluded_areas,
        )

        return applied

    async def _load_historical_preferences(
        self, user_id: str, confidence_threshold: float = 0.7
    ) -> List[UserStandupPreference]:
        """Load persisted preferences above confidence threshold."""
        try:
            all_prefs = await self._service.get_preferences(user_id)
            # Filter by confidence
            high_confidence = [p for p in all_prefs if p.confidence >= confidence_threshold]
            return high_confidence
        except Exception as e:
            logger.warning(
                "failed_to_load_preferences",
                user_id=user_id,
                error=str(e),
            )
            return []

    def _apply_historical(
        self,
        applied: AppliedPreferences,
        historical: List[UserStandupPreference],
    ) -> None:
        """Apply historical preferences to AppliedPreferences."""
        for pref in historical:
            if pref.preference_type == PreferenceType.CONTENT_FILTER:
                if pref.value and pref.value not in applied.focus_areas:
                    applied.focus_areas.append(str(pref.value))
                    applied.applied_from_history.append(
                        f"focus:{pref.value} (conf:{pref.confidence:.0%})"
                    )

            elif pref.preference_type == PreferenceType.EXCLUSION:
                if pref.value and pref.value not in applied.excluded_areas:
                    applied.excluded_areas.append(str(pref.value))
                    applied.applied_from_history.append(
                        f"exclude:{pref.value} (conf:{pref.confidence:.0%})"
                    )

            elif pref.preference_type == PreferenceType.FORMAT:
                if pref.value in ("brief", "detailed"):
                    applied.format_style = str(pref.value)
                    applied.applied_from_history.append(
                        f"format:{pref.value} (conf:{pref.confidence:.0%})"
                    )

    async def _apply_extracted(
        self,
        applied: AppliedPreferences,
        extracted: List[ExtractedPreference],
        user_id: str,
        session_id: Optional[str] = None,
    ) -> None:
        """Apply extracted preferences, save persistent ones."""
        for ext in extracted:
            # Track as applied from turn
            applied.applied_from_turn.append(f"{ext.key}:{ext.value}")

            # Apply based on type
            if ext.preference_type == PreferenceType.CONTENT_FILTER:
                if ext.is_temporary:
                    applied.temporary_overrides["focus"] = ext.value
                else:
                    if ext.value and ext.value not in applied.focus_areas:
                        applied.focus_areas.append(str(ext.value))

            elif ext.preference_type == PreferenceType.EXCLUSION:
                if ext.is_temporary:
                    applied.temporary_overrides["exclude"] = ext.value
                else:
                    if ext.value and ext.value not in applied.excluded_areas:
                        applied.excluded_areas.append(str(ext.value))

            elif ext.preference_type == PreferenceType.FORMAT:
                if ext.is_temporary:
                    applied.temporary_overrides["format"] = ext.value
                else:
                    if ext.value in ("brief", "detailed"):
                        applied.format_style = str(ext.value)

            # Persist non-temporary preferences
            if not ext.is_temporary:
                try:
                    pref = ext.to_preference(user_id)
                    await self._service.save_preference(pref, session_id)
                except Exception as e:
                    logger.warning(
                        "failed_to_save_preference",
                        user_id=user_id,
                        preference=ext.key,
                        error=str(e),
                    )

    def filter_content(
        self,
        content: Dict[str, Any],
        applied: AppliedPreferences,
    ) -> Dict[str, Any]:
        """
        Filter content based on applied preferences.

        Args:
            content: Raw content from integrations
                     Expected keys: github, calendar, todos, etc.
            applied: Applied preferences

        Returns:
            Filtered content dict
        """
        filtered = {}

        # Determine what to include
        focus_set: Set[str] = set(applied.focus_areas)
        exclude_set: Set[str] = set(applied.excluded_areas)

        # Handle temporary overrides
        if "focus" in applied.temporary_overrides:
            focus_set = {applied.temporary_overrides["focus"]}
        if "exclude" in applied.temporary_overrides:
            exclude_set.add(applied.temporary_overrides["exclude"])

        for key, value in content.items():
            key_lower = key.lower()

            # If we have focus areas, only include those
            if focus_set:
                if not any(focus.lower() in key_lower for focus in focus_set):
                    logger.debug("content_filtered_not_in_focus", key=key)
                    continue

            # Check exclusions
            if any(excl.lower() in key_lower for excl in exclude_set):
                logger.debug("content_filtered_excluded", key=key)
                continue

            filtered[key] = value

        return filtered

    def format_output(
        self,
        standup_text: str,
        applied: AppliedPreferences,
    ) -> str:
        """
        Format standup output based on preferences.

        Args:
            standup_text: Raw standup text
            applied: Applied preferences

        Returns:
            Formatted standup text
        """
        format_style = applied.temporary_overrides.get("format", applied.format_style)

        if format_style == "brief":
            return self._make_brief(standup_text)
        elif format_style == "detailed":
            return self._make_detailed(standup_text)

        return standup_text

    def _make_brief(self, text: str) -> str:
        """Convert standup to brief format."""
        lines = text.split("\n")
        brief_lines = []

        for line in lines:
            # Keep headers
            if line.startswith("*") and line.endswith("*"):
                brief_lines.append(line)
            # Keep first item under each header
            elif line.strip().startswith("*") or line.strip().startswith("-"):
                if brief_lines and brief_lines[-1].startswith("*"):
                    brief_lines.append(line)
                # Skip additional items

        return "\n".join(brief_lines)

    def _make_detailed(self, text: str) -> str:
        """Enhance standup with more detail prompts."""
        # For detailed mode, we'd add context/prompts for more info
        # For now, just return as-is (detailed generation happens upstream)
        return text


# Convenience functions for integration
async def get_user_applied_preferences(
    user_id: str,
    current_message: Optional[str] = None,
    session_id: Optional[str] = None,
) -> AppliedPreferences:
    """Convenience function to prepare preferences."""
    applicator = PreferenceApplicator()
    return await applicator.prepare_preferences(user_id, current_message, session_id)
