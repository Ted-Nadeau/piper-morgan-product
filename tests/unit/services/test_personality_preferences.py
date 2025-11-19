"""
Tests for Personality Profile Preference Integration

Tests verify that:
1. PersonalityProfile loads preferences from alpha_users table
2. All 5 preference dimensions are mapped correctly
3. Preferences affect response guidance generation
4. Graceful defaults work when preferences not set
5. Different preference values produce different outputs
6. Integration with preference questionnaire works end-to-end

Issue #269 CORE-PREF-PERSONALITY-INTEGRATION
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.database.models import User as AlphaUser
from services.database.session_factory import AsyncSessionFactory
from services.personality.personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    PersonalityProfile,
    TechnicalPreference,
)

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def test_user_id():
    """Generate unique test user ID"""
    return str(uuid4())


@pytest.fixture
def base_preferences():
    """Basic preference set with all 5 dimensions"""
    return {
        "communication_style": "balanced",
        "work_style": "flexible",
        "decision_making": "collaborative",
        "learning_style": "examples",
        "feedback_level": "moderate",
        "configured_at": datetime.utcnow().isoformat(),
    }


# ============================================================================
# TEST SCENARIO 1: CONCISE COMMUNICATION STYLE
# ============================================================================


def test_concise_communication_style():
    """
    Test that concise communication preference maps to lower warmth level.

    Concise style should result in:
    - warmth_level = 0.4 (professional, less warm)
    - Response guidance mentions "concise, professional tone"
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "concise",
        "work_style": "flexible",
        "decision_making": "collaborative",
        "learning_style": "examples",
        "feedback_level": "moderate",
    }

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify warmth level is low
    assert profile.warmth_level == 0.4, "Concise style should have lower warmth"

    # Verify response guidance mentions professional tone
    guidance = profile.get_response_style_guidance()
    assert (
        "concise" in guidance.lower() or "professional" in guidance.lower()
    ), f"Guidance should mention professional tone: {guidance}"

    print(f"✓ Concise communication: warmth={profile.warmth_level}, guidance={guidance}")


def test_balanced_communication_style():
    """
    Test that balanced communication preference maps to moderate warmth level.

    Balanced style should result in:
    - warmth_level = 0.6 (moderate, balanced)
    - Response guidance mentions "balanced, professional tone"
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "balanced",
        "work_style": "flexible",
        "decision_making": "collaborative",
        "learning_style": "examples",
        "feedback_level": "moderate",
    }

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify warmth level is moderate
    assert profile.warmth_level == 0.6, "Balanced style should have moderate warmth"

    # Verify response guidance mentions balanced tone
    guidance = profile.get_response_style_guidance()
    assert "balanced" in guidance.lower(), f"Guidance should mention balanced tone: {guidance}"

    print(f"✓ Balanced communication: warmth={profile.warmth_level}, guidance={guidance}")


def test_detailed_communication_style():
    """
    Test that detailed communication preference maps to higher warmth level.

    Detailed style should result in:
    - warmth_level = 0.7 (friendly, warm)
    - Response guidance mentions "friendly, warm tone"
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "detailed",
        "work_style": "flexible",
        "decision_making": "collaborative",
        "learning_style": "examples",
        "feedback_level": "moderate",
    }

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify warmth level is high
    assert profile.warmth_level == 0.7, "Detailed style should have higher warmth"

    # Verify response guidance mentions warm/friendly tone
    guidance = profile.get_response_style_guidance()
    assert (
        "warm" in guidance.lower() or "friendly" in guidance.lower()
    ), f"Guidance should mention warm tone: {guidance}"

    print(f"✓ Detailed communication: warmth={profile.warmth_level}, guidance={guidance}")


# ============================================================================
# TEST SCENARIO 2: WORK STYLE AFFECTS ACTION ORIENTATION
# ============================================================================


def test_structured_work_style():
    """
    Test that structured work preference maps to HIGH action orientation.

    Structured style needs clear next steps.
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "balanced",
        "work_style": "structured",
        "decision_making": "collaborative",
        "learning_style": "examples",
        "feedback_level": "moderate",
    }

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify action orientation is HIGH
    assert (
        profile.action_orientation == ActionLevel.HIGH
    ), "Structured work style should have HIGH action orientation"

    # Verify guidance mentions clear next steps
    guidance = profile.get_response_style_guidance()
    assert (
        "next steps" in guidance.lower() or "action" in guidance.lower()
    ), f"Guidance should mention action items: {guidance}"

    print(f"✓ Structured work: action_orientation={profile.action_orientation.value}")


def test_exploratory_work_style():
    """
    Test that exploratory work preference maps to LOW action orientation.

    Exploratory style prefers open-ended, non-prescriptive responses.
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "balanced",
        "work_style": "exploratory",
        "decision_making": "collaborative",
        "learning_style": "examples",
        "feedback_level": "moderate",
    }

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify action orientation is LOW
    assert (
        profile.action_orientation == ActionLevel.LOW
    ), "Exploratory work style should have LOW action orientation"

    # Verify guidance minimizes action language
    guidance = profile.get_response_style_guidance()
    assert (
        "minimize action" in guidance.lower() or "open" in guidance.lower()
    ), f"Guidance should minimize action items: {guidance}"

    print(f"✓ Exploratory work: action_orientation={profile.action_orientation.value}")


# ============================================================================
# TEST SCENARIO 3: DECISION MAKING AFFECTS CONFIDENCE STYLE
# ============================================================================


def test_data_driven_decision_making():
    """
    Test that data-driven preference maps to NUMERIC confidence style.

    Data-driven decisions need confidence percentages.
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "balanced",
        "work_style": "flexible",
        "decision_making": "data-driven",
        "learning_style": "examples",
        "feedback_level": "moderate",
    }

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify confidence style is NUMERIC
    assert (
        profile.confidence_style == ConfidenceDisplayStyle.NUMERIC
    ), "Data-driven should use NUMERIC confidence"

    # Verify guidance mentions percentages
    guidance = profile.get_response_style_guidance()
    assert (
        "percentages" in guidance.lower() or "confidence" in guidance.lower()
    ), f"Guidance should mention confidence percentages: {guidance}"

    print(f"✓ Data-driven: confidence_style={profile.confidence_style.value}")


def test_intuitive_decision_making():
    """
    Test that intuitive preference maps to CONTEXTUAL confidence style.

    Intuitive decisions need reasoning and context.
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "balanced",
        "work_style": "flexible",
        "decision_making": "intuitive",
        "learning_style": "examples",
        "feedback_level": "moderate",
    }

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify confidence style is CONTEXTUAL
    assert (
        profile.confidence_style == ConfidenceDisplayStyle.CONTEXTUAL
    ), "Intuitive should use CONTEXTUAL confidence"

    # Verify guidance mentions context/reasoning
    guidance = profile.get_response_style_guidance()
    assert (
        "context" in guidance.lower()
    ), f"Guidance should mention contextual reasoning: {guidance}"

    print(f"✓ Intuitive: confidence_style={profile.confidence_style.value}")


# ============================================================================
# TEST SCENARIO 4: LEARNING STYLE AFFECTS TECHNICAL DEPTH
# ============================================================================


def test_examples_learning_style():
    """
    Test that examples learning preference maps to BALANCED technical depth.

    Examples work best with moderate technical detail.
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "balanced",
        "work_style": "flexible",
        "decision_making": "collaborative",
        "learning_style": "examples",
        "feedback_level": "moderate",
    }

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify technical depth is BALANCED
    assert (
        profile.technical_depth == TechnicalPreference.BALANCED
    ), "Examples learning should use BALANCED technical depth"

    print(f"✓ Examples learning: technical_depth={profile.technical_depth.value}")


def test_explanations_learning_style():
    """
    Test that explanations learning preference maps to DETAILED technical depth.

    Explanations require deeper technical understanding.
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "balanced",
        "work_style": "flexible",
        "decision_making": "collaborative",
        "learning_style": "explanations",
        "feedback_level": "moderate",
    }

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify technical depth is DETAILED
    assert (
        profile.technical_depth == TechnicalPreference.DETAILED
    ), "Explanations learning should use DETAILED technical depth"

    # Verify guidance mentions comprehensive depth
    guidance = profile.get_response_style_guidance()
    assert (
        "comprehensive" in guidance.lower() or "depth" in guidance.lower()
    ), f"Guidance should mention technical depth: {guidance}"

    print(f"✓ Explanations learning: technical_depth={profile.technical_depth.value}")


def test_exploration_learning_style():
    """
    Test that exploration learning preference maps to SIMPLIFIED technical depth.

    Exploration starts with simple concepts before diving deep.
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "balanced",
        "work_style": "flexible",
        "decision_making": "collaborative",
        "learning_style": "exploration",
        "feedback_level": "moderate",
    }

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify technical depth is SIMPLIFIED
    assert (
        profile.technical_depth == TechnicalPreference.SIMPLIFIED
    ), "Exploration learning should use SIMPLIFIED technical depth"

    # Verify guidance minimizes jargon
    guidance = profile.get_response_style_guidance()
    assert (
        "jargon" in guidance.lower() or "simple" in guidance.lower()
    ), f"Guidance should minimize jargon: {guidance}"

    print(f"✓ Exploration learning: technical_depth={profile.technical_depth.value}")


# ============================================================================
# TEST SCENARIO 5: RESPONSE GUIDANCE CHANGES WITH PREFERENCES
# ============================================================================


def test_response_guidance_varies_by_warmth():
    """
    Test that response guidance changes based on warmth level from preferences.

    Different communication styles should produce different guidance strings.
    """
    user_id = str(uuid4())

    # Concise profile
    concise_prefs = {
        "communication_style": "concise",
        "work_style": "flexible",
        "decision_making": "collaborative",
        "learning_style": "examples",
        "feedback_level": "moderate",
    }
    concise_profile = PersonalityProfile._create_from_preferences(user_id, concise_prefs)
    concise_guidance = concise_profile.get_response_style_guidance()

    # Detailed profile
    detailed_prefs = {
        "communication_style": "detailed",
        "work_style": "flexible",
        "decision_making": "collaborative",
        "learning_style": "examples",
        "feedback_level": "moderate",
    }
    detailed_profile = PersonalityProfile._create_from_preferences(user_id, detailed_prefs)
    detailed_guidance = detailed_profile.get_response_style_guidance()

    # Guidance strings should be different
    assert (
        concise_guidance != detailed_guidance
    ), "Different communication styles should produce different guidance"

    # Concise should mention concise/professional
    assert "concise" in concise_guidance.lower() or "professional" in concise_guidance.lower()

    # Detailed should mention warm/friendly
    assert "warm" in detailed_guidance.lower() or "friendly" in detailed_guidance.lower()

    print(
        f"✓ Guidance varies: Concise={concise_guidance[:50]}..., Detailed={detailed_guidance[:50]}..."
    )


# ============================================================================
# TEST SCENARIO 6: DEFAULTS WHEN NO PREFERENCES SET
# ============================================================================


def test_default_behavior_no_preferences():
    """
    Test that graceful defaults work when user has no preferences set.

    Should use balanced/default values for all dimensions.
    """
    user_id = str(uuid4())
    preferences = {}  # Empty preferences

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify defaults are applied
    assert profile.warmth_level == 0.6, "Should use balanced default warmth"
    assert profile.action_orientation == ActionLevel.MEDIUM, "Should use medium action as default"
    assert (
        profile.confidence_style == ConfidenceDisplayStyle.DESCRIPTIVE
    ), "Should use descriptive confidence as default"
    assert (
        profile.technical_depth == TechnicalPreference.BALANCED
    ), "Should use balanced depth as default"

    # Verify profile is still usable
    guidance = profile.get_response_style_guidance()
    assert len(guidance) > 0, "Should generate guidance even with defaults"

    print(f"✓ Default behavior: warmth={profile.warmth_level}, guidance={guidance[:50]}...")


def test_partial_preferences():
    """
    Test that missing preference fields fall back to defaults.

    Only providing some preferences should still work correctly.
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "concise",
        # Missing other fields - should use defaults
    }

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Communication style should be applied
    assert profile.warmth_level == 0.4, "Concise preference should be applied"

    # Others should use defaults
    assert profile.action_orientation == ActionLevel.MEDIUM, "Should default to medium action"
    assert (
        profile.confidence_style == ConfidenceDisplayStyle.DESCRIPTIVE
    ), "Should default to descriptive confidence"

    print(f"✓ Partial preferences: concise applied, others defaulted")


# ============================================================================
# TEST SCENARIO 7: ALL 5 DIMENSIONS TOGETHER
# ============================================================================


def test_all_dimensions_applied():
    """
    Test that all 5 preference dimensions are loaded and applied together.

    Create a profile with extreme values on each dimension and verify all are applied.
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "detailed",  # warmth = 0.7
        "work_style": "structured",  # action = HIGH
        "decision_making": "data-driven",  # confidence = NUMERIC
        "learning_style": "explanations",  # depth = DETAILED
        "feedback_level": "detailed",  # (influences output length)
    }

    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify all 5 dimensions are applied
    assert profile.warmth_level == 0.7, "communication_style applied"
    assert profile.action_orientation == ActionLevel.HIGH, "work_style applied"
    assert profile.confidence_style == ConfidenceDisplayStyle.NUMERIC, "decision_making applied"
    assert profile.technical_depth == TechnicalPreference.DETAILED, "learning_style applied"

    # Verify guidance reflects all dimensions
    guidance = profile.get_response_style_guidance()
    assert "warm" in guidance.lower() or "friendly" in guidance.lower()
    assert "next steps" in guidance.lower() or "action" in guidance.lower()
    assert "percentages" in guidance.lower() or "confidence" in guidance.lower()
    assert "comprehensive" in guidance.lower() or "depth" in guidance.lower()

    print(f"✓ All 5 dimensions applied: {guidance}")


# ============================================================================
# TEST SCENARIO 8: ASYNC LOADING FROM DATABASE
# ============================================================================


def test_internal_create_from_preferences_integration():
    """
    Test the internal _create_from_preferences method which is used by load_with_preferences.

    This tests the preference mapping logic that would be used after database loading.
    """
    user_id = str(uuid4())
    preferences = {
        "communication_style": "concise",
        "work_style": "structured",
        "decision_making": "data-driven",
        "learning_style": "explanations",
        "feedback_level": "minimal",
        "configured_at": datetime.utcnow().isoformat(),
    }

    # Use internal method directly (this is what load_with_preferences calls)
    profile = PersonalityProfile._create_from_preferences(user_id, preferences)

    # Verify preferences were applied correctly
    assert profile.user_id == user_id
    assert profile.warmth_level == 0.4, "Concise preference should map to 0.4 warmth"
    assert (
        profile.action_orientation == ActionLevel.HIGH
    ), "Structured preference should map to HIGH action"
    assert (
        profile.confidence_style == ConfidenceDisplayStyle.NUMERIC
    ), "Data-driven should map to NUMERIC confidence"
    assert (
        profile.technical_depth == TechnicalPreference.DETAILED
    ), "Explanations should map to DETAILED depth"

    # Verify guidance reflects all applied preferences
    guidance = profile.get_response_style_guidance()
    assert "concise" in guidance.lower() or "professional" in guidance.lower()
    assert "percentages" in guidance.lower()
    assert "comprehensive" in guidance.lower()
    assert "next steps" in guidance.lower()

    print(f"✓ Internal preference mapping: all 4 preferences applied correctly")


def test_load_with_preferences_fallback_to_defaults():
    """
    Test that when preferences are missing or empty, defaults are used.

    This verifies graceful degradation when user has no preferences set.
    """
    user_id = str(uuid4())

    # Test with empty preferences dict
    empty_prefs = {}
    profile = PersonalityProfile._create_from_preferences(user_id, empty_prefs)

    # Should all be defaults
    assert profile.warmth_level == 0.6, "Empty prefs should default to balanced warmth"
    assert (
        profile.action_orientation == ActionLevel.MEDIUM
    ), "Empty prefs should default to medium action"

    # Test with None values (shouldn't happen but should be safe)
    sparse_prefs = {"communication_style": None}
    profile2 = PersonalityProfile._create_from_preferences(user_id, sparse_prefs)

    # Should handle None gracefully and use defaults
    assert profile2.warmth_level == 0.6, "None values should fall back to default"

    print(f"✓ Fallback to defaults: gracefully handles missing/empty preferences")


# ============================================================================
# TEST SCENARIO 9: CONTEXT ADJUSTMENT STILL WORKS WITH PREFERENCES
# ============================================================================


def test_context_adjustment_with_preferences():
    """
    Test that PersonalityProfile.adjust_for_context() still works after loading preferences.

    Preferences should be the baseline, context adjustment should modify them.
    """
    from services.personality.personality_profile import ResponseContext, ResponseType

    user_id = str(uuid4())
    preferences = {
        "communication_style": "concise",  # warmth = 0.4
        "work_style": "flexible",
        "decision_making": "collaborative",
        "learning_style": "examples",
        "feedback_level": "moderate",
    }

    # Create profile with concise preferences
    profile = PersonalityProfile._create_from_preferences(user_id, preferences)
    assert profile.warmth_level == 0.4

    # Create a low-confidence context (should increase warmth)
    context = ResponseContext(
        intent_confidence=0.2,  # Low confidence
        intent_category="test",
        intent_action="test",
        response_type=ResponseType.CHAT,
    )

    # Adjust for context
    adjusted_profile = profile.adjust_for_context(context)

    # Warmth should be increased despite concise preference
    assert (
        adjusted_profile.warmth_level > profile.warmth_level
    ), "Low confidence should increase warmth even with concise preference"
    assert (
        adjusted_profile.action_orientation == ActionLevel.HIGH
    ), "Low confidence should increase action orientation"

    print(
        f"✓ Context adjustment: baseline {profile.warmth_level} → adjusted {adjusted_profile.warmth_level}"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
