"""
Tests for CLI consciousness wrapper.
Issue #633 CONSCIOUSNESS-TRANSFORM: CLI Output
"""

import pytest

from services.consciousness.validation import validate_mvc


class TestCLIConsciousness:
    """Test consciousness wrapper for CLI output."""

    def test_startup_message_has_identity(self):
        """Startup message must have identity voice."""
        from services.consciousness.cli_consciousness import format_startup_conscious

        result = format_startup_conscious()
        assert "I" in result or "I'" in result or "me" in result.lower(), "Should have identity"

    def test_ready_message_has_identity(self):
        """Ready message must have identity voice."""
        from services.consciousness.cli_consciousness import format_ready_conscious

        result = format_ready_conscious("http://localhost:8001")
        assert "I" in result or "I'" in result, "Should have identity"
        assert "8001" in result or "localhost" in result, "Should include URL info"

    def test_shutdown_message_has_identity(self):
        """Shutdown message must have identity voice."""
        from services.consciousness.cli_consciousness import format_shutdown_conscious

        result = format_shutdown_conscious()
        assert "I" in result or "me" in result.lower(), "Should have identity"

    def test_success_message_has_identity(self):
        """Success confirmations must have identity voice."""
        from services.consciousness.cli_consciousness import format_cli_success_conscious

        result = format_cli_success_conscious("stored", "your API key")
        assert "I" in result or "I'" in result, "Should have identity"

    def test_error_message_has_invitation(self):
        """Error messages must have dialogue invitation."""
        from services.consciousness.cli_consciousness import format_cli_error_conscious

        result = format_cli_error_conscious("Could not connect to database")
        assert "?" in result, "Should have invitation to retry or get help"
        assert "I" in result or "I'" in result, "Should have identity"

    def test_progress_message_has_identity(self):
        """Progress messages should have identity."""
        from services.consciousness.cli_consciousness import format_cli_progress_conscious

        result = format_cli_progress_conscious("Initializing services", 3, 5)
        assert "I" in result.lower() or "working" in result.lower() or "getting" in result.lower()

    def test_services_ready_message(self):
        """Services ready confirmation should be conversational."""
        from services.consciousness.cli_consciousness import format_services_ready_conscious

        result = format_services_ready_conscious(5)
        assert "5" in result, "Should mention count"

    def test_key_stored_success(self):
        """Key storage success should be conversational."""
        from services.consciousness.cli_consciousness import format_cli_success_conscious

        result = format_cli_success_conscious("stored", "your OpenAI key in the OS keychain")
        assert "I" in result, "Should have identity"
        assert "openai" in result.lower() or "key" in result.lower()
