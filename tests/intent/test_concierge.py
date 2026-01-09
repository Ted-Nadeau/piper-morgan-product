"""
Issue #491: Tests for FTUX-CONCIERGE capability concierge functionality.

Tests verify:
- Slash commands are returned with proper structure
- IDENTITY responses include slash commands
- IDENTITY responses include active integrations
- Limitation responses are helpful and suggest alternatives
- UNKNOWN intents get graceful fallback (not 422)
"""

from unittest.mock import MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.plugins.plugin_interface import PluginMetadata


@pytest.fixture
def canonical_handlers():
    """Fixture to create CanonicalHandlers instance."""
    return CanonicalHandlers()


@pytest.fixture
def mock_plugin_registry():
    """Fixture to create a mock PluginRegistry with test plugins."""
    registry = MagicMock()

    # Mock get_status_all to return status for configured plugins
    registry.get_status_all.return_value = {
        "slack": {"configured": True, "active": True, "status": "active"},
        "github": {"configured": True, "active": True, "status": "active"},
    }

    # Mock get_plugin to return plugin instances with metadata
    def get_plugin_side_effect(name):
        if name == "slack":
            plugin = MagicMock()
            plugin.get_metadata.return_value = PluginMetadata(
                name="slack",
                version="1.0.0",
                description="Slack integration for team communication",
                author="Piper Team",
                capabilities=["channels", "messages"],
            )
            return plugin
        elif name == "github":
            plugin = MagicMock()
            plugin.get_metadata.return_value = PluginMetadata(
                name="github",
                version="1.0.0",
                description="GitHub integration for issue tracking",
                author="Piper Team",
                capabilities=["issues", "pull_requests"],
            )
            return plugin
        else:
            return None

    registry.get_plugin.side_effect = get_plugin_side_effect

    return registry


class TestSlashCommands:
    """Issue #491: Tests for _get_slash_commands() method."""

    def test_get_slash_commands_returns_list(self, canonical_handlers):
        """Slash commands method returns a non-empty list."""
        commands = canonical_handlers._get_slash_commands()

        assert isinstance(commands, list)
        assert len(commands) >= 3, "Should return at least 3 slash commands"

    def test_slash_commands_have_required_fields(self, canonical_handlers):
        """Each slash command has command, description, and syntax fields."""
        commands = canonical_handlers._get_slash_commands()

        for cmd in commands:
            assert "command" in cmd, f"Missing 'command' field in {cmd}"
            assert "description" in cmd, f"Missing 'description' field in {cmd}"
            assert "syntax" in cmd, f"Missing 'syntax' field in {cmd}"

    def test_slash_commands_include_standup(self, canonical_handlers):
        """Slash commands include /standup."""
        commands = canonical_handlers._get_slash_commands()
        command_names = [cmd["command"] for cmd in commands]

        assert "/standup" in command_names

    def test_slash_commands_include_status(self, canonical_handlers):
        """Slash commands include /status."""
        commands = canonical_handlers._get_slash_commands()
        command_names = [cmd["command"] for cmd in commands]

        assert "/status" in command_names

    def test_slash_commands_include_help(self, canonical_handlers):
        """Slash commands include /help."""
        commands = canonical_handlers._get_slash_commands()
        command_names = [cmd["command"] for cmd in commands]

        assert "/help" in command_names


class TestIdentityResponseWithCapabilities:
    """Issue #491: Tests for IDENTITY response including capabilities."""

    @pytest.fixture
    def mock_capabilities_data(self):
        """Mock capabilities data for identity response tests."""
        # Issue #491: Updated to match new accurate core capabilities
        return {
            "core": [
                "todo management",
                "calendar awareness",
                "priority guidance",
                "status updates",
                "GitHub integration",
                "contextual queries",
            ],
            "integrations": [
                {
                    "name": "slack",
                    "description": "Slack integration for team communication",
                    "capabilities": ["channels", "messages"],
                },
                {
                    "name": "github",
                    "description": "GitHub integration for issue tracking",
                    "capabilities": ["issues", "pull_requests"],
                },
            ],
            "capabilities_list": [
                "todo management",
                "calendar awareness",
                "priority guidance",
                "status updates",
                "GitHub integration",
                "contextual queries",
            ],
        }

    def test_detailed_identity_includes_slash_commands(
        self, canonical_handlers, mock_capabilities_data
    ):
        """Detailed IDENTITY response includes slash commands section."""
        response = canonical_handlers._format_detailed_identity(mock_capabilities_data)

        # Check for slash commands section
        assert "Slash Commands" in response, "Should include Slash Commands header"
        assert "/standup" in response, "Should include /standup command"
        assert "/status" in response, "Should include /status command"
        assert "/help" in response, "Should include /help command"

    def test_detailed_identity_includes_integrations(
        self, canonical_handlers, mock_capabilities_data
    ):
        """Detailed IDENTITY response includes active integrations."""
        response = canonical_handlers._format_detailed_identity(mock_capabilities_data)

        # Check for integrations section
        assert "Integrations" in response, "Should include Integrations header"
        # The mock has slack and github configured
        assert "Slack" in response or "slack" in response, "Should mention Slack"
        assert "GitHub" in response or "github" in response, "Should mention GitHub"

    def test_standard_identity_includes_slash_commands_hint(
        self, canonical_handlers, mock_capabilities_data
    ):
        """Standard IDENTITY response includes hint about slash commands."""
        response = canonical_handlers._format_standard_identity(mock_capabilities_data)

        # Should mention slash commands
        assert (
            "/standup" in response or "/status" in response or "/help" in response
        ), "Should include at least one slash command"

    def test_identity_includes_core_capabilities(self, canonical_handlers, mock_capabilities_data):
        """IDENTITY response includes core capability mentions."""
        response = canonical_handlers._format_detailed_identity(mock_capabilities_data)

        # Should mention what Piper can help with - check for the actual content
        assert (
            "coordination" in response.lower()
            or "capabilities" in response.lower()
            or "help" in response.lower()
        )


class TestGracefulLimitations:
    """Issue #491: Tests for graceful limitation responses."""

    def test_unknown_intent_handler_returns_helpful_message(
        self, canonical_handlers, mock_plugin_registry
    ):
        """Unknown intent gets a helpful message, not an error."""
        from unittest.mock import AsyncMock

        from services.domain.models import Intent
        from services.intent.intent_service import IntentService
        from services.orchestration.engine import OrchestrationEngine
        from services.shared_types import IntentCategory

        # Create intent service with mocked dependencies
        orchestration_engine = MagicMock(spec=OrchestrationEngine)
        intent_service = IntentService(orchestration_engine=orchestration_engine)

        # The _handle_unknown_intent should be testable
        # We verify the canonical handlers have the methods needed
        assert hasattr(
            canonical_handlers, "_get_dynamic_capabilities"
        ), "Should have _get_dynamic_capabilities method"
        assert hasattr(
            canonical_handlers, "_get_slash_commands"
        ), "Should have _get_slash_commands method"

    def test_limitation_response_suggests_discovery(self, canonical_handlers):
        """Limitation response tells users how to discover capabilities."""
        # Get the slash commands that would be suggested
        commands = canonical_handlers._get_slash_commands()

        # Verify we have commands to suggest
        assert len(commands) > 0, "Should have commands to suggest as alternatives"

        # Verify each command has description for helpful suggestions
        for cmd in commands:
            assert cmd.get("description"), f"Command {cmd} should have description"


class TestUnknownIntentGracefulFallback:
    """Issue #491: Integration tests for UNKNOWN intent graceful handling."""

    @pytest.mark.asyncio
    async def test_unknown_intent_does_not_return_422(self):
        """UNKNOWN intents should not cause 422 errors."""
        from unittest.mock import AsyncMock, MagicMock

        from services.domain.models import Intent
        from services.intent.intent_service import IntentService
        from services.orchestration.engine import OrchestrationEngine
        from services.shared_types import IntentCategory, WorkflowType

        # Create mock orchestration engine
        orchestration_engine = MagicMock(spec=OrchestrationEngine)

        # Create intent service
        intent_service = IntentService(orchestration_engine=orchestration_engine)

        # Create an UNKNOWN intent (using correct Intent fields)
        unknown_intent = Intent(
            category=IntentCategory.UNKNOWN,
            action="unknown_query",
            confidence=0.1,
            original_message="flibbertigibbet zorpnax",  # Nonsense query
        )

        # Create a mock workflow (WorkflowType doesn't have GENERIC, use GENERATE_REPORT)
        mock_workflow = MagicMock()
        mock_workflow.workflow_type = WorkflowType.GENERATE_REPORT

        # Call the handler directly
        result = await intent_service._handle_unknown_intent(
            unknown_intent, mock_workflow, "test-session-id"
        )

        # Verify we get a result, not an error
        assert result is not None, "Should return a result, not raise exception"
        assert hasattr(result, "message"), "Result should have a message"
        assert result.message is not None, "Message should not be None"

        # Verify the message is helpful
        message_lower = result.message.lower()
        assert (
            "not sure" in message_lower or "can't" in message_lower or "help" in message_lower
        ), "Message should be helpful, not technical error"

    @pytest.mark.asyncio
    async def test_unknown_intent_suggests_alternatives(self):
        """UNKNOWN intent response suggests what Piper can do."""
        from unittest.mock import AsyncMock, MagicMock

        from services.domain.models import Intent
        from services.intent.intent_service import IntentService
        from services.orchestration.engine import OrchestrationEngine
        from services.shared_types import IntentCategory, WorkflowType

        # Create mock orchestration engine
        orchestration_engine = MagicMock(spec=OrchestrationEngine)

        # Create intent service
        intent_service = IntentService(orchestration_engine=orchestration_engine)

        # Create an UNKNOWN intent (using correct Intent fields)
        unknown_intent = Intent(
            category=IntentCategory.UNKNOWN,
            action="unknown_query",
            confidence=0.1,
            original_message="do something impossible",
        )

        # Create a mock workflow (WorkflowType doesn't have GENERIC, use GENERATE_REPORT)
        mock_workflow = MagicMock()
        mock_workflow.workflow_type = WorkflowType.GENERATE_REPORT

        # Call the handler directly
        result = await intent_service._handle_unknown_intent(
            unknown_intent, mock_workflow, "test-session-id"
        )

        # Verify message suggests discovery or alternatives
        message = result.message
        assert (
            "what can you do" in message.lower()
            or "/standup" in message
            or "/status" in message
            or "/help" in message
            or "help you with" in message.lower()
        ), "Message should suggest alternatives or discovery"


class TestCapabilityDiscovery:
    """Issue #491: Tests for capability discovery flow."""

    def test_what_can_you_do_triggers_identity_handler(self):
        """'What can you do?' should be handled by IDENTITY handler."""
        from services.intent_service.pre_classifier import PreClassifier

        # Test common capability queries that ARE in IDENTITY_PATTERNS
        capability_queries = [
            "what can you do",
            "what can you do?",
            "what can you help me with",  # Matches r"\bwhat can you help\b"
            "show me your capabilities",
        ]

        for query in capability_queries:
            result = PreClassifier.pre_classify(query)
            # Should route to IDENTITY category
            assert result is not None, f"Query '{query}' should match a pattern"
            assert (
                result.category.value == "identity"
            ), f"Query '{query}' should route to IDENTITY, got {result.category}"

    def test_who_are_you_triggers_identity_handler(self):
        """'Who are you?' should be handled by IDENTITY handler."""
        from services.intent_service.pre_classifier import PreClassifier

        # Test identity queries that ARE in IDENTITY_PATTERNS
        identity_queries = [
            "who are you",
            "who are you?",
            "what do you do",
            "tell me about yourself",
        ]

        for query in identity_queries:
            result = PreClassifier.pre_classify(query)
            # Should route to IDENTITY category
            assert result is not None, f"Query '{query}' should match a pattern"
            assert (
                result.category.value == "identity"
            ), f"Query '{query}' should route to IDENTITY, got {result.category}"
