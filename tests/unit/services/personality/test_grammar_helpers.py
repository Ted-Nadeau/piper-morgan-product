"""
Tests for Personality grammar helpers.

Issue #627: GRAMMAR-TRANSFORM: Personality System
Phase 3: Helper Integration Tests
"""

from datetime import datetime

import pytest

from services.personality.grammar_context import SituationType
from services.personality.grammar_helpers import (
    apply_personality,
    get_closing,
    get_confidence_phrase,
    get_error_phrase,
    get_formality,
    get_greeting,
    get_situation_tone,
    is_warm_user,
)
from services.personality.personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    PersonalityProfile,
    TechnicalPreference,
)


class TestApplyPersonality:
    """Test apply_personality helper."""

    def test_with_profile(self):
        """Apply personality with PersonalityProfile."""
        profile = PersonalityProfile(
            id="test",
            user_id="user-1",
            warmth_level=0.8,
            confidence_style=ConfidenceDisplayStyle.CONTEXTUAL,
            action_orientation=ActionLevel.MEDIUM,
            technical_depth=TechnicalPreference.BALANCED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        result = apply_personality(
            "Here's your data.",
            profile=profile,
            include_greeting=True,
        )

        assert "Here's your data." in result
        assert "Hi" in result or "Hey" in result

    def test_with_dict(self):
        """Apply personality with dictionary."""
        result = apply_personality(
            "Task done.",
            profile_data={"warmth_level": 0.7},
            situation=SituationType.SUCCESS,
        )

        assert "Task done." in result

    def test_without_profile(self):
        """Apply personality without profile uses defaults."""
        result = apply_personality("Original message.")

        assert "Original message." in result


class TestGetGreeting:
    """Test get_greeting helper."""

    def test_first_interaction(self):
        """Greeting for first interaction."""
        profile = PersonalityProfile.get_default("user-1")
        profile.warmth_level = 0.8

        result = get_greeting(profile=profile, is_first_interaction=True)

        assert "Hi" in result or "Hey" in result

    def test_returning_user(self):
        """Greeting for returning user."""
        result = get_greeting(
            profile_data={"warmth_level": 0.7},
            is_first_interaction=False,
        )

        assert "again" in result.lower() or "back" in result.lower()

    def test_no_profile(self):
        """Greeting without profile."""
        result = get_greeting(is_first_interaction=True)

        assert len(result) > 0


class TestGetErrorPhrase:
    """Test get_error_phrase helper."""

    def test_warm_error(self):
        """Error phrase for warm user."""
        profile = PersonalityProfile.get_default("user-1")
        profile.warmth_level = 0.9

        result = get_error_phrase(profile=profile)

        assert "help" in result.lower() or "trouble" in result.lower()

    def test_frustrated_user(self):
        """Error phrase for frustrated user."""
        result = get_error_phrase(
            profile_data={"warmth_level": 0.5},
            seems_frustrated=True,
        )

        # Should be warm even with medium warmth preference
        assert len(result) > 0


class TestGetClosing:
    """Test get_closing helper."""

    def test_warm_closing(self):
        """Closing for warm user."""
        profile = PersonalityProfile.get_default("user-1")
        profile.warmth_level = 0.8

        result = get_closing(profile=profile)

        assert "help" in result.lower() or "else" in result.lower()

    def test_busy_user_no_closing(self):
        """No closing for busy user."""
        result = get_closing(
            profile_data={"warmth_level": 0.8},
            is_busy=True,
        )

        assert result == ""


class TestGetConfidencePhrase:
    """Test get_confidence_phrase helper."""

    def test_high_confidence(self):
        """High confidence phrase."""
        profile = PersonalityProfile.get_default("user-1")
        profile.warmth_level = 0.7

        result = get_confidence_phrase(0.95, profile=profile)

        assert "confident" in result.lower()

    def test_low_confidence(self):
        """Low confidence phrase."""
        result = get_confidence_phrase(
            0.4,
            profile_data={"warmth_level": 0.6},
        )

        assert "uncertain" in result.lower() or "not entirely" in result.lower()


class TestGetSituationTone:
    """Test get_situation_tone helper."""

    def test_success(self):
        """Success situation tone."""
        profile = PersonalityProfile.get_default("user-1")
        profile.warmth_level = 0.8

        result = get_situation_tone(SituationType.SUCCESS, profile=profile)

        assert "well" in result.lower() or "worked" in result.lower()

    def test_error(self):
        """Error situation tone."""
        result = get_situation_tone(
            SituationType.ERROR,
            profile_data={"warmth_level": 0.8},
        )

        assert "ran into" in result.lower() or "something" in result.lower()


class TestGetFormality:
    """Test get_formality helper."""

    def test_warm_formality(self):
        """Warm user gets warm formality."""
        profile = PersonalityProfile.get_default("user-1")
        profile.warmth_level = 0.9

        result = get_formality(profile=profile)

        assert result == "warm"

    def test_professional_formality(self):
        """Low warmth gets professional formality."""
        result = get_formality(profile_data={"warmth_level": 0.2})

        assert result == "professional"


class TestIsWarmUser:
    """Test is_warm_user helper."""

    def test_warm_user(self):
        """Detect warm user."""
        profile = PersonalityProfile.get_default("user-1")
        profile.warmth_level = 0.8

        assert is_warm_user(profile=profile) is True

    def test_not_warm_user(self):
        """Detect not-warm user."""
        result = is_warm_user(profile_data={"warmth_level": 0.4})

        assert result is False

    def test_no_profile(self):
        """No profile returns False."""
        assert is_warm_user() is False


class TestContractorTest:
    """Verify helpers pass Contractor Test."""

    def test_no_raw_data_in_output(self):
        """Helpers don't expose raw data."""
        profile = PersonalityProfile.get_default("user-1")
        profile.warmth_level = 0.8

        greeting = get_greeting(profile=profile)
        error = get_error_phrase(profile=profile)
        closing = get_closing(profile=profile)

        combined = f"{greeting} {error} {closing}"

        assert "warmth_level" not in combined
        assert "user-1" not in combined

    def test_natural_language(self):
        """Helpers produce natural language."""
        profile = PersonalityProfile.get_default("user-1")

        result = apply_personality(
            "Here's what I found.",
            profile=profile,
            include_greeting=True,
            include_closing=True,
        )

        # Should be readable prose
        assert "!!!" not in result
        assert result[0].isupper()
