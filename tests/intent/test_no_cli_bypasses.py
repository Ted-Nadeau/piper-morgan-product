"""
Test that all CLI commands use intent classification.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest


class TestCLIIntentEnforcement:
    """Ensure all CLI commands use intent classification."""

    @pytest.fixture
    def mock_classifier(self):
        """Mock intent classifier for testing."""
        with patch("services.intent_service.classifier.classifier") as mock:
            yield mock

    def test_standup_uses_intent(self, mock_classifier):
        """Standup command should use intent."""
        from cli.commands.standup import StandupCommand

        cmd = StandupCommand()
        # Execute command
        # Verify classifier was called
        # mock_classifier.classify.assert_called()
        pass  # Implement based on actual CLI structure

    def test_all_commands_import_intent(self):
        """All CLI commands should import intent service."""
        cli_commands = Path("cli/commands")

        if not cli_commands.exists():
            pytest.skip("CLI commands directory not found")

        for file in cli_commands.glob("*.py"):
            if file.name == "__init__.py":
                continue

            content = file.read_text()

            # Each command should reference intent somehow
            has_intent_ref = (
                "intent" in content.lower()
                or "CanonicalHandlers" in content
                or "IntentService" in content
            )

            # If this fails, that command bypasses intent
            assert has_intent_ref, f"{file.name} does not use intent classification"
