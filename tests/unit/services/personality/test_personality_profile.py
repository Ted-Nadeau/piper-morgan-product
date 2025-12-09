"""
Tests for PersonalityProfile domain model and context adaptation
"""

from unittest.mock import MagicMock

import pytest

from services.personality.personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    PersonalityProfile,
    ResponseContext,
    ResponseType,
    TechnicalPreference,
)


class TestPersonalityProfile:
    """Test PersonalityProfile domain model"""

    @pytest.fixture
    def default_profile(self):
        """Standard personality profile for testing"""
        from datetime import datetime

        return PersonalityProfile(
            id="test-default",
            user_id="test_user",
            warmth_level=0.6,
            confidence_style=ConfidenceDisplayStyle.CONTEXTUAL,
            action_orientation=ActionLevel.MEDIUM,
            technical_depth=TechnicalPreference.BALANCED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    @pytest.fixture
    def low_confidence_context(self):
        """Context with low intent confidence"""
        return ResponseContext(
            intent_confidence=0.2,
            intent_category="analysis",
            intent_action="investigate_issue",
            response_type=ResponseType.CLI,
        )

    @pytest.fixture
    def high_confidence_context(self):
        """Context with high intent confidence"""
        return ResponseContext(
            intent_confidence=0.9,
            intent_category="execution",
            intent_action="create_ticket",
            response_type=ResponseType.CLI,
        )

    @pytest.mark.smoke
    def test_profile_creation_with_valid_values(self):
        """Test creating PersonalityProfile with valid parameters"""
        from datetime import datetime

        profile = PersonalityProfile(
            id="test-id",
            user_id="test_user",
            warmth_level=0.8,
            confidence_style=ConfidenceDisplayStyle.NUMERIC,
            action_orientation=ActionLevel.HIGH,
            technical_depth=TechnicalPreference.DETAILED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert profile.warmth_level == 0.8
        assert profile.confidence_style == ConfidenceDisplayStyle.NUMERIC
        assert profile.action_orientation == ActionLevel.HIGH
        assert profile.technical_depth == TechnicalPreference.DETAILED

    @pytest.mark.smoke
    def test_profile_warmth_level_bounds(self):
        """Test warmth_level is properly bounded between 0.0-1.0"""
        from datetime import datetime

        # Valid bounds
        profile_min = PersonalityProfile(
            id="test-min",
            user_id="test_user",
            warmth_level=0.0,
            confidence_style=ConfidenceDisplayStyle.CONTEXTUAL,
            action_orientation=ActionLevel.MEDIUM,
            technical_depth=TechnicalPreference.BALANCED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        profile_max = PersonalityProfile(
            id="test-max",
            user_id="test_user",
            warmth_level=1.0,
            confidence_style=ConfidenceDisplayStyle.CONTEXTUAL,
            action_orientation=ActionLevel.MEDIUM,
            technical_depth=TechnicalPreference.BALANCED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert profile_min.warmth_level == 0.0
        assert profile_max.warmth_level == 1.0

    @pytest.mark.smoke
    def test_adjust_for_context_low_confidence(self, default_profile, low_confidence_context):
        """Test profile adaptation for low confidence context"""
        adapted = default_profile.adjust_for_context(low_confidence_context)

        # Low confidence should increase warmth and guidance
        assert adapted.warmth_level > default_profile.warmth_level
        assert adapted.confidence_style == ConfidenceDisplayStyle.HIDDEN
        assert adapted.action_orientation == ActionLevel.HIGH

    @pytest.mark.smoke
    def test_adjust_for_context_high_confidence(self, default_profile, high_confidence_context):
        """Test profile adaptation for high confidence context"""
        adapted = default_profile.adjust_for_context(high_confidence_context)

        # High confidence should be more professional (lower warmth)
        assert adapted.warmth_level < default_profile.warmth_level
        # Confidence style only changes from HIDDEN to CONTEXTUAL for high confidence
        assert adapted.confidence_style == default_profile.confidence_style
        # Technical depth doesn't change automatically
        assert adapted.technical_depth == default_profile.technical_depth

    @pytest.mark.smoke
    def test_get_default_creates_valid_profile(self):
        """Test get_default creates a valid default profile"""
        profile = PersonalityProfile.get_default("test_user")

        assert 0.0 <= profile.warmth_level <= 1.0
        assert isinstance(profile.confidence_style, ConfidenceDisplayStyle)
        assert isinstance(profile.action_orientation, ActionLevel)
        assert isinstance(profile.technical_depth, TechnicalPreference)


class TestResponseContext:
    """Test ResponseContext validation and behavior"""

    @pytest.mark.smoke
    def test_valid_context_creation(self):
        """Test creating valid ResponseContext"""
        context = ResponseContext(
            intent_confidence=0.7,
            intent_category="analysis",
            intent_action="investigate_issue",
            response_type=ResponseType.CLI,
        )

        assert context.intent_confidence == 0.7
        assert context.intent_category == "analysis"
        assert context.intent_action == "investigate_issue"
        assert context.response_type == ResponseType.CLI

    @pytest.mark.smoke
    def test_invalid_confidence_bounds(self):
        """Test ResponseContext validates confidence bounds"""
        with pytest.raises(ValueError, match="intent_confidence must be 0.0-1.0"):
            ResponseContext(
                intent_confidence=1.5,  # Invalid: > 1.0
                intent_category="analysis",
                intent_action="investigate",
                response_type=ResponseType.CLI,
            )

        with pytest.raises(ValueError, match="intent_confidence must be 0.0-1.0"):
            ResponseContext(
                intent_confidence=-0.1,  # Invalid: < 0.0
                intent_category="analysis",
                intent_action="investigate",
                response_type=ResponseType.CLI,
            )
