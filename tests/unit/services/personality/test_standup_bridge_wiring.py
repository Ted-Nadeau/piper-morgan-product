"""
Wiring tests for standup bridge consciousness integration.
Issue #632 - Verifies imports and method calls work correctly.

These tests verify the WIRING, not the consciousness output itself.
"""

from datetime import datetime

import pytest


class TestStandupBridgeWiring:
    """Wiring tests for standup_bridge.py consciousness integration."""

    def test_consciousness_import_works(self):
        """Verify consciousness can be imported from standup_bridge."""
        from services.personality.standup_bridge import StandupToChatBridge

        # If this imports, wiring is correct
        bridge = StandupToChatBridge()
        assert bridge is not None

    def test_adapt_standup_for_chat_uses_consciousness(self):
        """Verify adapt_standup_for_chat produces conscious output."""
        from services.personality.standup_bridge import StandupToChatBridge

        bridge = StandupToChatBridge()
        standup_response = {
            "data": {
                "yesterday_accomplishments": ["Fixed bug"],
                "today_priorities": ["Continue work"],
                "blockers": [],
                "generation_time_ms": 1000,
                "time_saved_minutes": 15,
                "github_activity": {"commits": [{"message": "test"}]},
            },
            "metadata": {"context_source": "persistent"},
        }

        result = bridge.adapt_standup_for_chat(standup_response)

        # Should have identity voice
        assert "I " in result or "I'" in result, "Output should have identity voice"
        # Should have invitation
        assert "?" in result, "Output should have dialogue invitation"

    def test_personality_still_applies(self):
        """Verify personality system still works on top of consciousness."""
        from services.personality.personality_profile import (
            ActionLevel,
            ConfidenceDisplayStyle,
            PersonalityProfile,
            TechnicalPreference,
        )
        from services.personality.standup_bridge import StandupToChatBridge

        bridge = StandupToChatBridge()
        standup_response = {
            "data": {
                "yesterday_accomplishments": ["Fixed bug"],
                "today_priorities": ["Continue work"],
                "blockers": [],
            },
            "metadata": {},
        }

        profile = PersonalityProfile(
            id="test-profile",
            user_id="test-user",
            warmth_level=0.9,  # High warmth
            action_orientation=ActionLevel.HIGH,
            confidence_style=ConfidenceDisplayStyle.CONTEXTUAL,
            technical_depth=TechnicalPreference.BALANCED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        result = bridge.apply_personality_to_standup(standup_response, profile)

        # Should still be string output
        assert isinstance(result, str)
        # Should have content
        assert len(result) > 50

    def test_empty_response_handled_gracefully(self):
        """Verify empty response doesn't crash."""
        from services.personality.standup_bridge import StandupToChatBridge

        bridge = StandupToChatBridge()

        # Empty response
        result = bridge.adapt_standup_for_chat({})
        assert "I " in result, "Error message should have identity"
        assert "?" in result, "Error message should have invitation"

        # None response
        result = bridge.adapt_standup_for_chat(None)
        assert "I " in result

    def test_consciousness_exports_available(self):
        """Verify consciousness functions are exported."""
        from services.consciousness import (
            format_accomplishments_conscious,
            format_blockers_conscious,
            format_priorities_conscious,
            format_standup_closing_conscious,
            format_standup_greeting_conscious,
        )

        # All should be callable
        assert callable(format_standup_greeting_conscious)
        assert callable(format_accomplishments_conscious)
        assert callable(format_priorities_conscious)
        assert callable(format_blockers_conscious)
        assert callable(format_standup_closing_conscious)
