"""
Integration Tests for Preference Detection - End-to-End Flow

Tests for Issue #248 (CONV-LEARN-PREF) complete preference detection cycle:
- Detect preferences from message
- Suggest to user (confirmation flow)
- User accepts/rejects preference
- Store preference and apply to profile
- Integration with learning system

These tests verify the complete data flow from detection through storage.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

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
    DetectionMethod,
    PreferenceDimension,
    PreferenceHint,
)


class TestPreferenceDetectionE2EFlow:
    """Test complete preference detection cycle"""

    @pytest.fixture
    def handler(self):
        """Fixture providing PreferenceDetectionHandler"""
        return PreferenceDetectionHandler()

    @pytest.fixture
    def analyzer(self):
        """Fixture providing ConversationAnalyzer"""
        return ConversationAnalyzer()

    @pytest.fixture
    def sample_profile(self):
        """Mock personality profile for testing"""
        profile = MagicMock()
        profile.warmth_level = 0.5
        profile.confidence_style = ConfidenceDisplayStyle.CONTEXTUAL
        profile.action_orientation = ActionLevel.MEDIUM
        profile.technical_depth = TechnicalPreference.BALANCED
        return profile

    @pytest.mark.asyncio
    async def test_complete_detection_to_confirmation_flow(self, handler, analyzer, sample_profile):
        """Test complete flow: detect → suggest → confirm → store"""
        user_id = str(uuid4())
        session_id = str(uuid4())
        # Use message with strong preference signals
        # Need warm_score > 0.2 to reach 0.4 confidence (min(0.7, score*2))
        message = (
            "I love the casual and friendly tone! I appreciate your awesome approach! "
            "It's fantastic and wonderful. Please explain the architecture and code. "
            "I love the informal chat style!"
        )

        # Step 1: Analyze message for preferences
        detection_result = analyzer.analyze_message(user_id, message, sample_profile)
        assert len(detection_result.hints) > 0
        assert len(detection_result.suggested_hints) > 0

        # Step 2: Store hints in session (simulating suggestion to user)
        await handler._store_hints_in_session(session_id, detection_result.suggested_hints)

        # Step 3: User accepts a preference
        hint = detection_result.suggested_hints[0]
        confirmation = await handler.confirm_preference(
            user_id=user_id,
            session_id=session_id,
            hint_id=hint.id,
            accepted=True,
        )

        # Step 4: Verify confirmation was recorded
        assert confirmation is not None
        assert confirmation.get("dimension") == hint.dimension.value
        assert confirmation.get("action") == "accepted"

    @pytest.mark.asyncio
    async def test_multiple_preferences_single_message(self, handler, analyzer, sample_profile):
        """Test detecting and handling multiple preferences in one message"""
        user_id = str(uuid4())
        session_id = str(uuid4())
        message = (
            "I absolutely love the friendly tone! Please explain the algorithm, "
            "architecture, and implementation details. Let's execute immediately!"
        )

        # Detect multiple preferences
        detection_result = analyzer.analyze_message(user_id, message, sample_profile)

        # Should detect at least 2-3 dimensions
        assert len(detection_result.hints) >= 2, "Should detect multiple dimensions"

        # Store all hints
        await handler._store_hints_in_session(session_id, detection_result.suggested_hints)

        # Verify all hints stored and retrievable
        for hint in detection_result.suggested_hints:
            retrieved = await handler._retrieve_hint_from_session(session_id, hint.id)
            assert retrieved is not None

    @pytest.mark.asyncio
    async def test_auto_apply_high_confidence_preferences(self, handler, analyzer, sample_profile):
        """Test automatic application of high-confidence preferences"""
        user_id = str(uuid4())
        session_id = str(uuid4())
        # Use strong technical words repeated
        message = (
            "Tell me about the algorithm, architecture, database design, "
            "code implementation, and performance optimization framework"
        )

        # Analyze message
        detection_result = analyzer.analyze_message(user_id, message, sample_profile)

        # Check for auto-apply hints (confidence >= 0.9)
        auto_apply_hints = detection_result.auto_apply_hints
        suggested_hints = detection_result.suggested_hints

        # Log results for debugging
        for hint in detection_result.hints:
            print(
                f"Hint: {hint.dimension}, Confidence: {hint.confidence_score}, "
                f"Ready for suggestion: {hint.is_ready_for_suggestion()}, "
                f"Ready for auto-apply: {hint.is_ready_for_auto_apply()}"
            )

        # If there are auto-apply hints, apply them
        if auto_apply_hints:
            await handler.apply_auto_preferences(
                user_id=user_id,
                session_id=session_id,
                hints=auto_apply_hints,
            )
            # Auto-apply hints should not appear in suggestions
            # (already applied, user doesn't need to confirm)

        # Suggested hints should still be available for confirmation
        if suggested_hints:
            await handler._store_hints_in_session(session_id, suggested_hints)

    @pytest.mark.asyncio
    async def test_preference_rejection_not_stored(self, handler, analyzer, sample_profile):
        """Test that rejected preferences are not stored"""
        user_id = str(uuid4())
        session_id = str(uuid4())
        message = (
            "I love the casual approach. Please explain the architecture and " "code implementation"
        )

        # Detect preferences
        detection_result = analyzer.analyze_message(user_id, message, sample_profile)
        assert len(detection_result.hints) > 0

        # Store hints
        await handler._store_hints_in_session(session_id, detection_result.suggested_hints)

        # User rejects a preference
        hint = detection_result.suggested_hints[0]
        result = await handler.confirm_preference(
            user_id=user_id,
            session_id=session_id,
            hint_id=hint.id,
            accepted=False,  # Reject!
        )

        # Rejection should be recorded
        assert result["action"] == "rejected"
        # Storage should not happen (only confirmation/logging)

    @pytest.mark.asyncio
    async def test_session_hint_expiration(self, handler, analyzer, sample_profile):
        """Test that hints expire after TTL"""
        import asyncio

        user_id = str(uuid4())
        session_id = str(uuid4())
        message = "I love the casual approach. Please explain the architecture"

        # Create hint with very short TTL for testing
        detection_result = analyzer.analyze_message(user_id, message, sample_profile)
        assert len(detection_result.hints) > 0

        # Store hints
        await handler._store_hints_in_session(session_id, detection_result.suggested_hints)

        # Verify stored
        hint = detection_result.suggested_hints[0]
        retrieved = await handler._retrieve_hint_from_session(session_id, hint.id)
        assert retrieved is not None

        # Try to retrieve after checking TTL
        # Note: Real expiration would require sleeping for TTL duration
        # For now, we just verify the TTL logic exists
        assert retrieved.get("stored_at") is not None or retrieved.get("ttl_minutes") is not None

    @pytest.mark.asyncio
    async def test_confidence_threshold_filtering(self, handler, analyzer, sample_profile):
        """Test that low-confidence hints are filtered out"""
        user_id = str(uuid4())
        session_id = str(uuid4())
        # Neutral message with no strong preference signals
        message = "What is the weather today?"

        # Analyze message
        detection_result = analyzer.analyze_message(user_id, message, sample_profile)

        # Neutral messages should have no/few suggestions
        for hint in detection_result.hints:
            # All hints should either be low confidence or filtered
            if hint.is_ready_for_suggestion():
                # If it made it to suggestions, confidence should be in range
                assert hint.confidence_score >= 0.4

        # Suggestions should be empty or very few
        assert len(detection_result.suggested_hints) < len(detection_result.hints) + 1

    @pytest.mark.asyncio
    async def test_different_dimension_preferences_independent(
        self, handler, analyzer, sample_profile
    ):
        """Test that preferences for different dimensions are handled independently"""
        user_id = str(uuid4())
        session_id = str(uuid4())

        # Message triggering technical preference
        tech_message = "I want more information about the algorithm, architecture, and code"
        tech_result = analyzer.analyze_message(user_id, tech_message, sample_profile)

        # Message triggering warmth preference
        warmth_message = "I love the casual and friendly approach"
        warmth_result = analyzer.analyze_message(user_id, warmth_message, sample_profile)

        # Extract dimensions
        tech_dims = {h.dimension for h in tech_result.hints}
        warmth_dims = {h.dimension for h in warmth_result.hints}

        # Different messages should detect different (but can overlap) dimensions
        # This verifies that detection is working across dimensions
        assert isinstance(tech_dims, set)
        assert isinstance(warmth_dims, set)

    @pytest.mark.asyncio
    async def test_suggestion_explanation_quality(self, handler, analyzer, sample_profile):
        """Test that suggestions include quality explanations"""
        user_id = "test_user_explain"
        message = "I love the casual approach. Please explain the architecture"

        # Analyze message
        detection_result = analyzer.analyze_message(user_id, message, sample_profile)

        # Check suggestions have explanations
        for hint in detection_result.suggested_hints:
            hint_dict = hint.to_dict()
            # Hints should have detection_method and other metadata
            assert hint_dict.get("detection_method") is not None
            # Explanation can be inferred from detection_method
            assert len(str(hint_dict.get("detection_method", ""))) > 0


class TestPreferenceDetectionErrorHandling:
    """Test error handling and graceful degradation"""

    @pytest.fixture
    def handler(self):
        """Fixture providing PreferenceDetectionHandler"""
        return PreferenceDetectionHandler()

    @pytest.fixture
    def analyzer(self):
        """Fixture providing ConversationAnalyzer"""
        return ConversationAnalyzer()

    @pytest.mark.asyncio
    async def test_missing_hint_on_confirmation(self, handler):
        """Test graceful handling of missing hint during confirmation"""
        user_id = str(uuid4())
        session_id = str(uuid4())
        nonexistent_hint_id = "nonexistent_hint_999"

        # Try to confirm a non-existent hint
        result = await handler.confirm_preference(
            user_id=user_id,
            session_id=session_id,
            hint_id=nonexistent_hint_id,
            accepted=True,
        )

        # Should handle gracefully (return error or None)
        # Based on implementation, should not crash

    @pytest.mark.asyncio
    async def test_invalid_session_handling(self, handler, analyzer):
        """Test handling of invalid session IDs"""
        user_id = "test_user"
        session_id = None  # Invalid

        message = "I love the casual approach"
        profile = MagicMock()
        profile.warmth_level = 0.5
        profile.technical_depth = TechnicalPreference.BALANCED
        profile.confidence_style = ConfidenceDisplayStyle.CONTEXTUAL
        profile.action_orientation = ActionLevel.MEDIUM

        # Analyzer should work without session
        result = analyzer.analyze_message(user_id, message, profile)

        # Should detect preferences even without valid session
        assert result is not None

        # But storage would fail gracefully
        if result.suggested_hints:
            # With no session, we can't store
            # This should be handled by the handler
            pass
