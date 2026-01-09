"""
Preference Feedback Handler.

Issue #555: STANDUP-LEARNING - User Preference Learning
Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Handles user corrections and feedback on preferences:
- Detects correction patterns ("no, actually...", "not that...")
- Adjusts confidence based on corrections
- Suggests confirmation for low-confidence preferences
"""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import structlog

from services.standup.preference_models import (
    PreferenceChange,
    PreferenceSource,
    PreferenceType,
    UserStandupPreference,
)
from services.standup.preference_service import UserPreferenceService

logger = structlog.get_logger()


@dataclass
class CorrectionResult:
    """Result of processing a correction."""

    was_correction: bool = False
    corrected_preference: Optional[UserStandupPreference] = None
    previous_value: Optional[str] = None
    new_value: Optional[str] = None
    confidence_adjustment: float = 0.0
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "was_correction": self.was_correction,
            "previous_value": self.previous_value,
            "new_value": self.new_value,
            "confidence_adjustment": self.confidence_adjustment,
            "message": self.message,
        }


@dataclass
class ConfirmationPrompt:
    """Prompt for confirming a low-confidence preference."""

    preference: UserStandupPreference
    question: str
    options: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "preference_id": self.preference.id,
            "preference_type": self.preference.preference_type.value,
            "current_value": self.preference.value,
            "confidence": self.preference.confidence,
            "question": self.question,
            "options": self.options,
        }


class PreferenceFeedbackHandler:
    """
    Handles user feedback and corrections on preferences.

    Correction patterns detected:
    - "no, focus on X" / "not X, focus on Y"
    - "actually, I want..." / "I meant..."
    - "wrong" / "incorrect" / "that's not right"
    - "instead of X, use Y"

    Confidence adjustments:
    - Correction reduces confidence by 0.15 (default)
    - Confirmation boosts confidence by 0.1 (default)
    - Repeated corrections can drop to 0
    """

    # Correction indicator patterns
    CORRECTION_INDICATORS = [
        r"\bno\s*,",
        r"\bactually\b",
        r"\bwrong\b",
        r"\bincorrect\b",
        r"\bthat'?s\s+not\s+right\b",
        r"\bi\s+meant\b",
        r"\bnot\s+that\b",
        r"\binstead\s+of\b",
        r"\brather\s+than\b",
        r"\bchange\s+(it\s+)?to\b",
        r"\bswitch\s+to\b",
        r"\bdon'?t\s+want\b",
    ]

    # Confirmation patterns
    CONFIRMATION_PATTERNS = [
        r"\byes\b",
        r"\byeah\b",
        r"\bthat'?s\s+right\b",
        r"\bcorrect\b",
        r"\bexactly\b",
        r"\bkeep\s+(it|that)\b",
        r"\bthat'?s\s+good\b",
        r"\bperfect\b",
    ]

    # Rejection patterns
    REJECTION_PATTERNS = [
        r"\bno\b",
        r"\bnope\b",
        r"\bdon'?t\b",
        r"\bstop\b",
        r"\bremove\b",
        r"\bdelete\b",
        r"\bforget\b",
    ]

    def __init__(
        self,
        preference_service: Optional[UserPreferenceService] = None,
        correction_penalty: float = 0.15,
        confirmation_boost: float = 0.1,
    ) -> None:
        """
        Initialize feedback handler.

        Args:
            preference_service: Service for preference persistence
            correction_penalty: Confidence reduction on correction
            confirmation_boost: Confidence increase on confirmation
        """
        self._service = preference_service or UserPreferenceService()
        self._correction_penalty = correction_penalty
        self._confirmation_boost = confirmation_boost

    def detect_correction(self, message: str) -> bool:
        """
        Detect if message contains a correction.

        Args:
            message: User message

        Returns:
            True if message appears to be a correction
        """
        message_lower = message.lower()
        for pattern in self.CORRECTION_INDICATORS:
            if re.search(pattern, message_lower):
                return True
        return False

    def detect_confirmation(self, message: str) -> bool:
        """
        Detect if message is a confirmation.

        Args:
            message: User message

        Returns:
            True if message is confirming something
        """
        message_lower = message.lower()
        for pattern in self.CONFIRMATION_PATTERNS:
            if re.search(pattern, message_lower):
                return True
        return False

    def detect_rejection(self, message: str) -> bool:
        """
        Detect if message is rejecting a preference.

        Args:
            message: User message

        Returns:
            True if message is rejecting something
        """
        message_lower = message.lower()
        # Check rejection patterns but not if also contains new value
        for pattern in self.REJECTION_PATTERNS:
            if re.search(pattern, message_lower):
                # Make sure it's a pure rejection, not "no, use X instead"
                if not self._has_new_value(message_lower):
                    return True
        return False

    def _has_new_value(self, message_lower: str) -> bool:
        """Check if message contains a new preference value."""
        new_value_patterns = [
            r"focus\s+on\s+(\w+)",
            r"use\s+(\w+)",
            r"instead\s+(\w+)",
            r"switch\s+to\s+(\w+)",
        ]
        for pattern in new_value_patterns:
            if re.search(pattern, message_lower):
                return True
        return False

    async def process_correction(
        self,
        user_id: str,
        message: str,
        current_preferences: List[UserStandupPreference],
        session_id: Optional[str] = None,
    ) -> CorrectionResult:
        """
        Process a user correction and update preferences.

        Args:
            user_id: User identifier
            message: User message containing correction
            current_preferences: Currently applied preferences
            session_id: Optional session for tracking

        Returns:
            CorrectionResult with details of what changed
        """
        if not self.detect_correction(message):
            return CorrectionResult(was_correction=False)

        message_lower = message.lower()

        # Try to identify what's being corrected
        corrected = self._identify_corrected_preference(message_lower, current_preferences)

        if not corrected:
            return CorrectionResult(
                was_correction=True,
                message="I detected a correction but couldn't identify what to change. Could you clarify?",
            )

        preference, new_value = corrected

        # Record the old value
        old_value = preference.value

        # Update the preference
        preference.value = new_value
        preference.reduce_confidence(self._correction_penalty)
        preference.source = PreferenceSource.CORRECTED

        # Persist the update
        try:
            await self._service.save_preference(preference, session_id)
            logger.info(
                "preference_corrected",
                user_id=user_id,
                preference_type=preference.preference_type.value,
                old_value=old_value,
                new_value=new_value,
                new_confidence=preference.confidence,
            )
        except Exception as e:
            logger.warning("correction_save_failed", error=str(e))

        return CorrectionResult(
            was_correction=True,
            corrected_preference=preference,
            previous_value=str(old_value) if old_value else None,
            new_value=str(new_value),
            confidence_adjustment=-self._correction_penalty,
            message=f"Got it! Changed from '{old_value}' to '{new_value}'.",
        )

    def _identify_corrected_preference(
        self,
        message_lower: str,
        current_preferences: List[UserStandupPreference],
    ) -> Optional[Tuple[UserStandupPreference, Any]]:
        """Identify which preference is being corrected and the new value."""
        # Extract new focus value
        focus_match = re.search(r"focus\s+on\s+(\w+)", message_lower)
        if focus_match:
            new_value = focus_match.group(1)
            # Find existing focus preference
            for pref in current_preferences:
                if pref.preference_type == PreferenceType.CONTENT_FILTER:
                    return (pref, new_value)
            # Create new if none exists
            new_pref = UserStandupPreference(
                user_id=current_preferences[0].user_id if current_preferences else "",
                preference_type=PreferenceType.CONTENT_FILTER,
                key="focus",
                value=new_value,
                confidence=0.7 - self._correction_penalty,  # Start lower due to correction
                source=PreferenceSource.CORRECTED,
            )
            return (new_pref, new_value)

        # Extract format change
        if "brief" in message_lower:
            for pref in current_preferences:
                if pref.preference_type == PreferenceType.FORMAT:
                    return (pref, "brief")
        elif "detailed" in message_lower:
            for pref in current_preferences:
                if pref.preference_type == PreferenceType.FORMAT:
                    return (pref, "detailed")

        # Extract exclusion removal
        remove_match = re.search(r"don'?t\s+(?:skip|exclude)\s+(\w+)", message_lower)
        if remove_match:
            removed = remove_match.group(1)
            for pref in current_preferences:
                if (
                    pref.preference_type == PreferenceType.EXCLUSION
                    and str(pref.value).lower() == removed
                ):
                    # This is a deletion, not a value change
                    return None

        return None

    async def process_confirmation(
        self,
        user_id: str,
        preference: UserStandupPreference,
        confirmed: bool,
        session_id: Optional[str] = None,
    ) -> UserStandupPreference:
        """
        Process user confirmation/rejection of a preference.

        Args:
            user_id: User identifier
            preference: Preference being confirmed
            confirmed: True if user confirmed, False if rejected
            session_id: Optional session for tracking

        Returns:
            Updated preference
        """
        if confirmed:
            preference.boost_confidence(self._confirmation_boost)
            logger.info(
                "preference_confirmed",
                user_id=user_id,
                preference_id=preference.id,
                new_confidence=preference.confidence,
            )
        else:
            preference.reduce_confidence(
                self._correction_penalty * 2
            )  # Double penalty for rejection
            logger.info(
                "preference_rejected",
                user_id=user_id,
                preference_id=preference.id,
                new_confidence=preference.confidence,
            )

        await self._service.save_preference(preference, session_id)
        return preference

    def generate_confirmation_prompts(
        self,
        preferences: List[UserStandupPreference],
        threshold: float = 0.5,
        max_prompts: int = 2,
    ) -> List[ConfirmationPrompt]:
        """
        Generate confirmation prompts for low-confidence preferences.

        Args:
            preferences: List of preferences to check
            threshold: Confidence threshold (below this triggers prompt)
            max_prompts: Maximum number of prompts to generate

        Returns:
            List of confirmation prompts
        """
        prompts = []

        # Sort by confidence (lowest first)
        low_confidence = sorted(
            [p for p in preferences if p.confidence < threshold],
            key=lambda p: p.confidence,
        )

        for pref in low_confidence[:max_prompts]:
            prompt = self._create_confirmation_prompt(pref)
            prompts.append(prompt)

        return prompts

    def _create_confirmation_prompt(self, pref: UserStandupPreference) -> ConfirmationPrompt:
        """Create a confirmation prompt for a preference."""
        if pref.preference_type == PreferenceType.CONTENT_FILTER:
            return ConfirmationPrompt(
                preference=pref,
                question=f"Should I focus on {pref.value} in your standups?",
                options=["Yes", "No", "Just this time"],
            )
        elif pref.preference_type == PreferenceType.EXCLUSION:
            return ConfirmationPrompt(
                preference=pref,
                question=f"Should I skip {pref.value} in your standups?",
                options=["Yes, skip it", "No, include it", "Just today"],
            )
        elif pref.preference_type == PreferenceType.FORMAT:
            return ConfirmationPrompt(
                preference=pref,
                question=f"Do you prefer {pref.value} format for your standups?",
                options=["Yes", "No, use standard", "Depends on the day"],
            )
        else:
            return ConfirmationPrompt(
                preference=pref,
                question=f"Keep this setting: {pref.key} = {pref.value}?",
                options=["Yes", "No"],
            )

    async def handle_feedback_message(
        self,
        user_id: str,
        message: str,
        current_preferences: List[UserStandupPreference],
        pending_confirmation: Optional[UserStandupPreference] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Handle a feedback message (correction, confirmation, or rejection).

        Args:
            user_id: User identifier
            message: User's feedback message
            current_preferences: Currently active preferences
            pending_confirmation: Preference awaiting confirmation (if any)
            session_id: Optional session for tracking

        Returns:
            Dict with feedback result and any needed follow-up
        """
        result: Dict[str, Any] = {
            "type": "none",
            "preference_updated": False,
            "message": "",
        }

        # Check if this is responding to a pending confirmation
        if pending_confirmation:
            if self.detect_confirmation(message):
                await self.process_confirmation(
                    user_id, pending_confirmation, confirmed=True, session_id=session_id
                )
                result["type"] = "confirmation"
                result["preference_updated"] = True
                result["message"] = (
                    f"Great, I'll remember that you like {pending_confirmation.value}."
                )
                return result
            elif self.detect_rejection(message):
                await self.process_confirmation(
                    user_id, pending_confirmation, confirmed=False, session_id=session_id
                )
                result["type"] = "rejection"
                result["preference_updated"] = True
                result["message"] = (
                    f"Understood, I won't assume {pending_confirmation.value} next time."
                )
                return result

        # Check for correction
        if self.detect_correction(message):
            correction = await self.process_correction(
                user_id, message, current_preferences, session_id
            )
            if correction.was_correction:
                result["type"] = "correction"
                result["preference_updated"] = correction.corrected_preference is not None
                result["message"] = correction.message
                result["correction"] = correction.to_dict()
                return result

        return result


# Convenience function
async def handle_preference_feedback(
    user_id: str,
    message: str,
    current_preferences: List[UserStandupPreference],
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function for handling feedback."""
    handler = PreferenceFeedbackHandler()
    return await handler.handle_feedback_message(
        user_id, message, current_preferences, session_id=session_id
    )
