"""
Unit Tests for Preference Detection System

Tests for Issue #248 (CONV-LEARN-PREF) preference detection components:
- PreferenceHint and PreferenceConfirmation data structures
- ConversationAnalyzer preference detection
- Confidence scoring and thresholds
- Session-based hint storage and retrieval
"""

from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from services.intent_service.preference_handler import PreferenceDetectionHandler
from services.personality.conversation_analyzer import ConversationAnalyzer
from services.personality.personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    PersonalityProfile,
    TechnicalPreference,
)
from services.personality.preference_detection import (
    ConfidenceLevel,
    DetectionMethod,
    PreferenceConfirmation,
    PreferenceDimension,
    PreferenceHint,
)


class TestPreferenceHintStructure:
    """Test PreferenceHint data structure and methods"""

    def test_preference_hint_creation(self):
        """Verify PreferenceHint can be created with required fields"""
        hint = PreferenceHint(
            id="hint_001",
            user_id="user123",
            dimension=PreferenceDimension.WARMTH,
            current_value=0.5,
            detected_value=0.8,
            confidence_score=0.85,
            detection_method=DetectionMethod.LANGUAGE_PATTERNS,
            source_text="Please be more friendly",
        )
        assert hint.id == "hint_001"
        assert hint.user_id == "user123"
        assert hint.dimension == PreferenceDimension.WARMTH
        assert hint.current_value == 0.5
        assert hint.detected_value == 0.8
        assert hint.confidence_score == 0.85
        assert hint.source_text == "Please be more friendly"

    def test_preference_hint_to_dict(self):
        """PreferenceHint.to_dict() returns dict representation"""
        hint = PreferenceHint(
            id="hint_001",
            user_id="user123",
            dimension=PreferenceDimension.WARMTH,
            current_value=0.5,
            detected_value=0.8,
            confidence_score=0.85,
            detection_method=DetectionMethod.LANGUAGE_PATTERNS,
            source_text="Please be more friendly",
        )
        hint_dict = hint.to_dict()
        assert isinstance(hint_dict, dict)
        assert hint_dict["id"] == "hint_001"
        assert hint_dict["dimension"] == "warmth_level"
        assert hint_dict["confidence_score"] == 0.85
        assert hint_dict["user_id"] == "user123"

    def test_confidence_level_classification(self):
        """Test confidence_level() method classifies scores correctly"""
        # Very High confidence (≥0.9)
        hint_very_high = PreferenceHint(
            id="h1",
            user_id="user123",
            dimension=PreferenceDimension.TECHNICAL,
            current_value="BALANCED",
            detected_value="DETAILED",
            confidence_score=0.95,
            detection_method=DetectionMethod.LANGUAGE_PATTERNS,
            source_text="more technical detail",
        )
        assert hint_very_high.confidence_level() == ConfidenceLevel.VERY_HIGH

        # High confidence (0.7-0.89)
        hint_high = PreferenceHint(
            id="h2",
            user_id="user123",
            dimension=PreferenceDimension.WARMTH,
            current_value=0.5,
            detected_value=0.7,
            confidence_score=0.75,
            detection_method=DetectionMethod.LANGUAGE_PATTERNS,
            source_text="be friendly",
        )
        assert hint_high.confidence_level() == ConfidenceLevel.HIGH

        # Medium confidence (0.4-0.69)
        hint_medium = PreferenceHint(
            id="h3",
            user_id="user123",
            dimension=PreferenceDimension.ACTION,
            current_value="MEDIUM",
            detected_value="HIGH",
            confidence_score=0.55,
            detection_method=DetectionMethod.LANGUAGE_PATTERNS,
            source_text="action items",
        )
        assert hint_medium.confidence_level() == ConfidenceLevel.MEDIUM

        # Low confidence (<0.4)
        hint_low = PreferenceHint(
            id="h4",
            user_id="user123",
            dimension=PreferenceDimension.CONFIDENCE,
            current_value="CONTEXTUAL",
            detected_value="NUMERIC",
            confidence_score=0.25,
            detection_method=DetectionMethod.LANGUAGE_PATTERNS,
            source_text="unclear signal",
        )
        assert hint_low.confidence_level() == ConfidenceLevel.LOW

    def test_is_ready_for_suggestion(self):
        """Test is_ready_for_suggestion() checks confidence threshold (≥0.4)"""
        # Suggestion-ready (≥0.4)
        hint_ready = PreferenceHint(
            id="h1",
            user_id="user123",
            dimension=PreferenceDimension.WARMTH,
            current_value=0.5,
            detected_value=0.7,
            confidence_score=0.45,
            detection_method=DetectionMethod.LANGUAGE_PATTERNS,
            source_text="be friendly",
        )
        assert hint_ready.is_ready_for_suggestion() is True

        # Not ready for suggestion (<0.4)
        hint_not_ready = PreferenceHint(
            id="h2",
            user_id="user123",
            dimension=PreferenceDimension.WARMTH,
            current_value=0.5,
            detected_value=0.7,
            confidence_score=0.35,
            detection_method=DetectionMethod.LANGUAGE_PATTERNS,
            source_text="unclear",
        )
        assert hint_not_ready.is_ready_for_suggestion() is False

    def test_is_ready_for_auto_apply(self):
        """Test is_ready_for_auto_apply() checks high confidence threshold (≥0.9)"""
        # Auto-apply ready (≥0.9 + explicit feedback)
        hint_auto = PreferenceHint(
            id="h1",
            user_id="user123",
            dimension=PreferenceDimension.TECHNICAL,
            current_value="BALANCED",
            detected_value="DETAILED",
            confidence_score=0.92,
            detection_method=DetectionMethod.EXPLICIT_FEEDBACK,
            source_text="I said I prefer technical detail",
        )
        assert hint_auto.is_ready_for_auto_apply() is True

        # Not auto-apply ready (high confidence but wrong detection method)
        hint_no_auto = PreferenceHint(
            id="h2",
            user_id="user123",
            dimension=PreferenceDimension.WARMTH,
            current_value=0.5,
            detected_value=0.8,
            confidence_score=0.92,
            detection_method=DetectionMethod.LANGUAGE_PATTERNS,
            source_text="friendly",
        )
        assert hint_no_auto.is_ready_for_auto_apply() is False

    def test_confidence_score_validation(self):
        """Test that invalid confidence scores are rejected"""
        with pytest.raises(ValueError):
            PreferenceHint(
                id="h1",
                user_id="user123",
                dimension=PreferenceDimension.WARMTH,
                current_value=0.5,
                detected_value=0.7,
                confidence_score=1.5,  # Invalid: > 1.0
                detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                source_text="test",
            )


class TestPreferenceConfirmation:
    """Test PreferenceConfirmation data structure"""

    def test_preference_confirmation_creation(self):
        """Verify PreferenceConfirmation records user decision"""
        confirmation = PreferenceConfirmation(
            id="confirm_001",
            user_id="user123",
            dimension=PreferenceDimension.WARMTH,
            new_value=0.8,
            previous_value=0.5,
            hint_id="hint_001",
            confirmation_source="user_accepted",
        )
        assert confirmation.id == "confirm_001"
        assert confirmation.user_id == "user123"
        assert confirmation.dimension == PreferenceDimension.WARMTH
        assert confirmation.new_value == 0.8
        assert confirmation.previous_value == 0.5
        assert confirmation.hint_id == "hint_001"
        assert confirmation.confirmation_source == "user_accepted"


class TestConversationAnalyzerDetection:
    """Test ConversationAnalyzer preference detection"""

    @pytest.fixture
    def analyzer(self):
        """Fixture providing ConversationAnalyzer instance"""
        return ConversationAnalyzer()

    @pytest.fixture
    def sample_profile(self):
        """Fixture providing a mock personality profile for testing"""
        # Create a mock profile with standard preferences to test detection
        profile = MagicMock()
        profile.warmth_level = 0.5
        profile.confidence_style = ConfidenceDisplayStyle.CONTEXTUAL
        profile.action_orientation = ActionLevel.MEDIUM
        profile.technical_depth = TechnicalPreference.BALANCED
        return profile

    def test_analyzer_initialization(self, analyzer):
        """ConversationAnalyzer initializes with required components"""
        assert analyzer is not None
        assert hasattr(analyzer, "analyze_message")
        assert hasattr(analyzer, "analyze_response")
        assert hasattr(analyzer, "analyze_feedback")

    def test_detect_technical_preference_from_message(self, analyzer, sample_profile):
        """Detect 'more technical' preference from message"""
        # Use actual technical words that trigger detection
        message = "I want more information about the architecture and code implementation"
        result = analyzer.analyze_message("user123", message, sample_profile)

        assert result is not None
        assert hasattr(result, "hints")
        assert len(result.hints) > 0
        # Should detect technical depth preference
        technical_hints = [h for h in result.hints if h.dimension == PreferenceDimension.TECHNICAL]
        assert len(technical_hints) > 0

    def test_detect_warmth_preference_from_message(self, analyzer, sample_profile):
        """Detect 'be more friendly' preference from message"""
        # Use actual warmth words that trigger detection
        message = (
            "I really appreciate your friendly approach and love the casual conversation style"
        )
        result = analyzer.analyze_message("user123", message, sample_profile)

        assert result is not None
        warmth_hints = [h for h in result.hints if h.dimension == PreferenceDimension.WARMTH]
        assert len(warmth_hints) > 0

    def test_confidence_score_bounds(self, analyzer, sample_profile):
        """All confidence scores are in valid range [0.0, 1.0]"""
        message = "Please be more professional and include technical details"
        result = analyzer.analyze_message("user123", message, sample_profile)

        for hint in result.hints:
            assert (
                0.0 <= hint.confidence_score <= 1.0
            ), f"Confidence score {hint.confidence_score} out of bounds"

    def test_multiple_preferences_in_single_message(self, analyzer, sample_profile):
        """Detect multiple preferences in single message"""
        # Combine preference triggers: warm + technical + action words
        message = (
            "I love the casual approach. Please explain the architecture and "
            "code implementation with immediate action steps"
        )
        result = analyzer.analyze_message("user123", message, sample_profile)

        assert len(result.hints) >= 2, "Should detect multiple preferences"

    def test_no_false_positives_for_neutral_message(self, analyzer, sample_profile):
        """Neutral message shouldn't trigger false preference detections"""
        message = "What's the weather like today?"
        result = analyzer.analyze_message("user123", message, sample_profile)

        # Should have few/no hints for neutral message
        if result.hints:
            # If any hints, they should have low confidence
            for hint in result.hints:
                assert (
                    hint.confidence_score < 0.6
                ), "Neutral message shouldn't have high confidence hints"

    def test_analysis_result_has_required_fields(self, analyzer, sample_profile):
        """Analysis result has all required fields"""
        message = "Please be more technical"
        result = analyzer.analyze_message("user123", message, sample_profile)

        assert hasattr(result, "hints")
        assert hasattr(result, "suggested_hints")
        assert hasattr(result, "auto_apply_hints")
        assert hasattr(result, "analysis_summary")

    def test_analysis_summary_generated(self, analyzer, sample_profile):
        """Analysis includes human-readable summary"""
        message = "Please provide more technical detail"
        result = analyzer.analyze_message("user123", message, sample_profile)

        assert isinstance(result.analysis_summary, str)
        assert len(result.analysis_summary) > 0


class TestSessionHintStorage:
    """Test session-based hint storage in PreferenceDetectionHandler"""

    @pytest.fixture
    def handler(self):
        """Fixture providing PreferenceDetectionHandler"""
        return PreferenceDetectionHandler()

    @pytest.mark.asyncio
    async def test_store_and_retrieve_hint(self, handler):
        """Store hint in session and retrieve it"""
        session_id = "session_001"
        hint = PreferenceHint(
            id="hint_001",
            user_id="user123",
            dimension=PreferenceDimension.WARMTH,
            current_value=0.5,
            detected_value=0.8,
            confidence_score=0.85,
            detection_method=DetectionMethod.LANGUAGE_PATTERNS,
            source_text="be friendly",
        )

        # Store hint
        await handler._store_hints_in_session(session_id, [hint])

        # Retrieve hint
        retrieved = await handler._retrieve_hint_from_session(session_id, hint.id)
        assert retrieved is not None
        assert retrieved["id"] == hint.id
        assert retrieved["dimension"] == "warmth_level"
        assert retrieved["confidence_score"] == 0.85

    @pytest.mark.asyncio
    async def test_store_multiple_hints(self, handler):
        """Store multiple hints and retrieve them individually"""
        session_id = "session_002"
        hints = [
            PreferenceHint(
                id="hint_001",
                user_id="user123",
                dimension=PreferenceDimension.WARMTH,
                current_value=0.5,
                detected_value=0.8,
                confidence_score=0.85,
                detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                source_text="friendly",
            ),
            PreferenceHint(
                id="hint_002",
                user_id="user123",
                dimension=PreferenceDimension.TECHNICAL,
                current_value="BALANCED",
                detected_value="DETAILED",
                confidence_score=0.92,
                detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                source_text="technical detail",
            ),
        ]

        await handler._store_hints_in_session(session_id, hints)

        # Retrieve each hint
        h1 = await handler._retrieve_hint_from_session(session_id, "hint_001")
        h2 = await handler._retrieve_hint_from_session(session_id, "hint_002")

        assert h1 is not None and h1["id"] == "hint_001"
        assert h2 is not None and h2["id"] == "hint_002"

    @pytest.mark.asyncio
    async def test_retrieve_nonexistent_hint(self, handler):
        """Retrieve non-existent hint returns None"""
        session_id = "session_003"
        retrieved = await handler._retrieve_hint_from_session(session_id, "nonexistent")
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_hint_stored_with_timestamp(self, handler):
        """Stored hints include timestamp for TTL checking"""
        session_id = "session_004"
        hint = PreferenceHint(
            id="hint_001",
            user_id="user123",
            dimension=PreferenceDimension.WARMTH,
            current_value=0.5,
            detected_value=0.8,
            confidence_score=0.85,
            detection_method=DetectionMethod.LANGUAGE_PATTERNS,
            source_text="friendly",
        )

        await handler._store_hints_in_session(session_id, [hint])
        retrieved = await handler._retrieve_hint_from_session(session_id, hint.id)

        assert "stored_at" in retrieved
        # Verify it's a valid ISO format timestamp
        datetime.fromisoformat(retrieved["stored_at"])

    @pytest.mark.asyncio
    async def test_empty_hint_list_not_stored(self, handler):
        """Empty hint list doesn't cause errors"""
        session_id = "session_005"
        await handler._store_hints_in_session(session_id, [])
        # Should complete without error
        retrieved = await handler._retrieve_hint_from_session(session_id, "any_hint")
        assert retrieved is None


class TestPreferenceApplicationLogic:
    """Test preference confirmation and application"""

    @pytest.fixture
    def handler(self):
        """Fixture providing PreferenceDetectionHandler"""
        return PreferenceDetectionHandler()

    @pytest.mark.asyncio
    async def test_confirm_preference_rejection(self, handler):
        """Test rejection path (no storage)"""
        result = await handler.confirm_preference(
            user_id="user123",
            session_id="session_001",
            hint_id="hint_001",
            accepted=False,
        )

        assert result["success"] is True
        assert result["action"] == "rejected"
        assert result["hint_id"] == "hint_001"

    @pytest.mark.asyncio
    async def test_confirm_preference_missing_hint(self, handler):
        """Test acceptance when hint not in session"""
        result = await handler.confirm_preference(
            user_id="user123",
            session_id="session_nonexistent",
            hint_id="hint_missing",
            accepted=True,
        )

        assert result["success"] is False
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_suggest_preferences_generates_suggestions(self, handler):
        """Test preference suggestion generation"""
        hints = [
            PreferenceHint(
                id="hint_001",
                user_id="user123",
                dimension=PreferenceDimension.WARMTH,
                current_value=0.5,
                detected_value=0.8,
                confidence_score=0.75,
                detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                source_text="friendly",
            ),
            PreferenceHint(
                id="hint_002",
                user_id="user123",
                dimension=PreferenceDimension.TECHNICAL,
                current_value="BALANCED",
                detected_value="DETAILED",
                confidence_score=0.4,
                detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                source_text="technical",
            ),
        ]

        result = await handler.suggest_preferences("user123", "session_001", hints)

        assert result["success"] is True
        assert result["has_suggestions"] is True
        assert len(result["suggestions"]) >= 1

    @pytest.mark.asyncio
    async def test_apply_auto_preferences_high_confidence(self, handler):
        """Test auto-application of high-confidence hints"""
        hints = [
            PreferenceHint(
                id="hint_001",
                user_id="user123",
                dimension=PreferenceDimension.TECHNICAL,
                current_value="BALANCED",
                detected_value="DETAILED",
                confidence_score=0.95,  # High confidence for auto-apply
                detection_method=DetectionMethod.EXPLICIT_FEEDBACK,
                source_text="I prefer technical detail",
            ),
        ]

        result = await handler.apply_auto_preferences("user123", "session_001", hints)

        assert result["success"] is True
        assert len(result["applied"]) >= 1
        assert result["applied"][0]["dimension"] == "technical_depth"


class TestConversationAnalyzerExplanationGeneration:
    """Test human-readable explanation generation"""

    @pytest.fixture
    def handler(self):
        """Fixture providing PreferenceDetectionHandler"""
        return PreferenceDetectionHandler()

    def test_language_patterns_explanation(self, handler):
        """Generate explanation for language pattern detection"""
        hint = PreferenceHint(
            id="hint_001",
            user_id="user123",
            dimension=PreferenceDimension.WARMTH,
            current_value=0.5,
            detected_value=0.8,
            confidence_score=0.85,
            detection_method=DetectionMethod.LANGUAGE_PATTERNS,
            source_text="be friendly",
        )

        explanation = handler._generate_suggestion_explanation(hint)
        assert isinstance(explanation, str)
        assert len(explanation) > 0

    def test_explicit_feedback_explanation(self, handler):
        """Generate explanation for explicit feedback detection"""
        hint = PreferenceHint(
            id="hint_001",
            user_id="user123",
            dimension=PreferenceDimension.TECHNICAL,
            current_value="BALANCED",
            detected_value="DETAILED",
            confidence_score=0.9,
            detection_method=DetectionMethod.EXPLICIT_FEEDBACK,
            source_text="I prefer technical detail",
        )

        explanation = handler._generate_suggestion_explanation(hint)
        assert isinstance(explanation, str)

    def test_behavioral_signals_explanation(self, handler):
        """Generate explanation for behavioral signal detection"""
        hint = PreferenceHint(
            id="hint_001",
            user_id="user123",
            dimension=PreferenceDimension.ACTION,
            current_value="MEDIUM",
            detected_value="HIGH",
            confidence_score=0.7,
            detection_method=DetectionMethod.BEHAVIORAL_SIGNALS,
            source_text="asks for action items",
        )

        explanation = handler._generate_suggestion_explanation(hint)
        assert isinstance(explanation, str)
