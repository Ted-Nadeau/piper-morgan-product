"""
Tests for Slack Slash Commands.

Issue #520: Canonical Queries #49, #50
- Query #49: /standup - Generate daily standup
- Query #50: /piper help - Show available commands and capabilities

Test categories:
1. Routing tests - verify command routing logic
2. Handler tests - verify handler behavior
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.slack.webhook_router import SlackWebhookRouter


class TestSlashCommandRouting:
    """Test slash command routing logic.

    Issue #521 learning: Routing tests verify the full path
    from _process_slash_command → appropriate handler.
    """

    @pytest.fixture
    def router(self):
        """Create SlackWebhookRouter instance for testing."""
        return SlackWebhookRouter()

    @pytest.mark.asyncio
    async def test_piper_help_routes_correctly(self, router):
        """Verify /piper help routes to help handler."""
        result = await router._process_slash_command(
            {
                "command": "/piper",
                "text": "help",
                "user_id": "U123",
                "channel_id": "C456",
            }
        )
        assert "response_type" in result
        # Issue #628: Grammar-conscious help uses warm intro
        text = result.get("text", "")
        assert "Piper" in text
        assert "help" in text.lower()

    @pytest.mark.asyncio
    async def test_piper_empty_routes_to_help(self, router):
        """Verify /piper with no text routes to help."""
        result = await router._process_slash_command(
            {
                "command": "/piper",
                "text": "",
                "user_id": "U123",
                "channel_id": "C456",
            }
        )
        assert "response_type" in result
        # Issue #628: Grammar-conscious help uses warm intro
        assert "Piper" in result.get("text", "")

    @pytest.mark.asyncio
    async def test_standup_routes_correctly(self, router):
        """Verify /standup routes to standup handler."""
        result = await router._process_slash_command(
            {
                "command": "/standup",
                "text": "",
                "user_id": "U123",
                "channel_id": "C456",
            }
        )
        assert result["response_type"] == "in_channel"

    @pytest.mark.asyncio
    async def test_unknown_command_returns_help_hint(self, router):
        """Verify unknown command suggests /piper help."""
        result = await router._process_slash_command(
            {
                "command": "/unknown",
                "text": "",
                "user_id": "U123",
                "channel_id": "C456",
            }
        )
        assert "Unknown command" in result.get("text", "")
        assert "/piper help" in result.get("text", "")


class TestPiperHelpCommand:
    """Test /piper help command handler."""

    @pytest.fixture
    def router(self):
        """Create SlackWebhookRouter instance for testing."""
        return SlackWebhookRouter()

    @pytest.mark.asyncio
    async def test_help_includes_available_commands(self, router):
        """Test help lists available commands."""
        result = await router._handle_piper_command("help", "U123", "C456")
        assert "/piper help" in result.get("text", "")
        assert "/standup" in result.get("text", "")

    @pytest.mark.asyncio
    async def test_help_includes_capabilities(self, router):
        """Test help shows capabilities."""
        result = await router._handle_piper_command("help", "U123", "C456")
        # Issue #628: Grammar-conscious help uses "What I Can Do"
        text = result.get("text", "")
        assert "What I Can Do" in text or "Can Do" in text

    @pytest.mark.asyncio
    async def test_help_is_ephemeral(self, router):
        """Test help response is ephemeral (only visible to user)."""
        result = await router._handle_piper_command("help", "U123", "C456")
        assert result["response_type"] == "ephemeral"

    @pytest.mark.asyncio
    async def test_unknown_subcommand_suggests_help(self, router):
        """Test unknown subcommand suggests /piper help."""
        result = await router._handle_piper_command("foobar", "U123", "C456")
        # Issue #628: Grammar-conscious error message
        text = result.get("text", "")
        assert "don't recognize" in text or "foobar" in text
        assert "/piper help" in text


class TestStandupCommand:
    """Test /standup command handler."""

    @pytest.fixture
    def router(self):
        """Create SlackWebhookRouter instance for testing."""
        return SlackWebhookRouter()

    @pytest.mark.asyncio
    async def test_standup_has_three_sections(self, router):
        """Test standup includes yesterday, today, blockers."""
        result = await router._handle_standup_command("U123", "C456")
        text = result.get("text", "")
        assert "Yesterday" in text
        assert "Today" in text
        assert "Blockers" in text

    @pytest.mark.asyncio
    async def test_standup_is_public(self, router):
        """Test standup uses in_channel response (visible to team)."""
        result = await router._handle_standup_command("U123", "C456")
        assert result["response_type"] == "in_channel"

    @pytest.mark.asyncio
    async def test_standup_handles_empty_data_gracefully(self, router):
        """Test standup handles no data without errors."""
        result = await router._handle_standup_command("U123", "C456")
        # Should still return valid structure with defaults
        text = result.get("text", "")
        assert "Yesterday" in text
        assert "Today" in text
        # Should show placeholder when no data
        assert "No completed items" in text or "No high-priority" in text or "None" in text

    @pytest.mark.asyncio
    async def test_standup_handles_errors_gracefully(self, router):
        """Test standup returns ephemeral on error."""
        # Mock _get_completed_since_yesterday to throw
        with patch.object(
            router, "_get_completed_since_yesterday", side_effect=Exception("Test error")
        ):
            result = await router._handle_standup_command("U123", "C456")
            assert result["response_type"] == "ephemeral"
            assert "Unable to generate standup" in result.get("text", "")
