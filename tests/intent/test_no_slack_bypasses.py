"""
Test that Slack integration uses intent classification.
"""

from pathlib import Path

import pytest


class TestSlackIntentEnforcement:
    """Ensure Slack handlers use intent classification."""

    def test_slack_handlers_use_intent(self):
        """All Slack event handlers should use intent."""
        slack_dir = Path("services/integrations/slack")

        if not slack_dir.exists():
            pytest.skip("Slack integration directory not found")

        # Find all handler files
        handler_files = [
            f
            for f in slack_dir.glob("**/*.py")
            if "handler" in f.name.lower() or "event" in f.name.lower()
        ]

        for file in handler_files:
            content = file.read_text()

            # Check if file mentions intent
            has_intent = "intent" in content.lower()

            # If this is a handler file, it should use intent
            if "handler" in file.name.lower():
                assert has_intent, f"{file.name} handler does not use intent"

    def test_slack_plugin_uses_intent(self):
        """Slack plugin should reference intent system."""
        slack_plugin = Path("services/integrations/slack/slack_plugin.py")

        if not slack_plugin.exists():
            pytest.skip("Slack plugin not found")

        content = slack_plugin.read_text()

        # Plugin should either use intent directly or delegate to handlers that do
        has_intent_ref = (
            "intent" in content.lower()
            or "canonical" in content.lower()
            or "handler" in content.lower()
        )

        assert has_intent_ref, "Slack plugin does not reference intent system"
