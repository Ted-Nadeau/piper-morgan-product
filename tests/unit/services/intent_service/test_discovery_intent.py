"""
Tests for #488 DISCOVERY intent - capability discovery queries.

Issue #488: MUX-INTERACT-DISCOVERY
Tests that "What can you do?" queries route to DISCOVERY (not IDENTITY).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


class TestDiscoveryPatternMatching:
    """Test DISCOVERY_PATTERNS matching in pre_classifier."""

    @pytest.mark.parametrize(
        "message",
        [
            "what can you do",
            "What can you do?",
            "what are your capabilities",
            "show me your capabilities",
            "what services do you offer",
            "what features do you have",
            "what can you help with",
            "menu of services",
            "list your capabilities",
            "your capabilities",
            "capability menu",
            "capabilities menu",
            "show menu",
            "what are you able to do",
            "show features",
            "available features",
            "help me get started",
        ],
    )
    def test_discovery_patterns_match(self, message: str):
        """Test that capability queries route to DISCOVERY."""
        result = PreClassifier.pre_classify(message)

        assert result is not None, f"'{message}' should match a pattern"
        assert (
            result.category == IntentCategory.DISCOVERY
        ), f"'{message}' should route to DISCOVERY, got {result.category}"
        assert result.action == "get_capabilities"

    @pytest.mark.parametrize(
        "message",
        [
            "who are you",
            "what's your name",
            "your role",
            "what do you do",  # This is ambiguous but kept in IDENTITY
            "tell me about yourself",
            "introduce yourself",
        ],
    )
    def test_identity_patterns_still_work(self, message: str):
        """Test that identity queries still route to IDENTITY (regression test)."""
        result = PreClassifier.pre_classify(message)

        assert result is not None, f"'{message}' should match a pattern"
        assert (
            result.category == IntentCategory.IDENTITY
        ), f"'{message}' should route to IDENTITY, got {result.category}"
        assert result.action == "get_identity"

    def test_discovery_before_identity_precedence(self):
        """Test that DISCOVERY patterns are checked before IDENTITY."""
        # This tests the fix from #488 - capability queries shouldn't
        # accidentally match IDENTITY patterns

        discovery_message = "what can you do for me"
        result = PreClassifier.pre_classify(discovery_message)

        # Should match DISCOVERY, not IDENTITY
        assert result is not None
        assert result.category == IntentCategory.DISCOVERY


class TestCanonicalHandlerRouting:
    """Test that canonical handlers route DISCOVERY correctly."""

    @pytest.fixture
    def handler(self):
        """Create a CanonicalHandlers instance."""
        return CanonicalHandlers()

    def test_can_handle_discovery(self, handler):
        """Test that can_handle returns True for DISCOVERY."""
        intent = Intent(
            category=IntentCategory.DISCOVERY,
            action="get_capabilities",
            confidence=1.0,
            context={},
        )
        assert handler.can_handle(intent) is True

    def test_can_handle_identity(self, handler):
        """Test that can_handle still returns True for IDENTITY."""
        intent = Intent(
            category=IntentCategory.IDENTITY,
            action="get_identity",
            confidence=1.0,
            context={},
        )
        assert handler.can_handle(intent) is True

    @pytest.mark.asyncio
    async def test_handle_routes_to_discovery(self, handler):
        """Test that handle() routes DISCOVERY to _handle_discovery_query."""
        intent = Intent(
            category=IntentCategory.DISCOVERY,
            action="get_capabilities",
            confidence=1.0,
            context={"original_message": "what can you do"},
        )

        with patch.object(
            handler, "_handle_discovery_query", new_callable=AsyncMock
        ) as mock_discovery:
            mock_discovery.return_value = {
                "message": "test",
                "intent": {"category": "discovery"},
            }

            await handler.handle(intent, session_id="test-session")

            mock_discovery.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_routes_to_identity(self, handler):
        """Test that handle() still routes IDENTITY to _handle_identity_query."""
        intent = Intent(
            category=IntentCategory.IDENTITY,
            action="get_identity",
            confidence=1.0,
            context={"original_message": "who are you"},
        )

        with patch.object(
            handler, "_handle_identity_query", new_callable=AsyncMock
        ) as mock_identity:
            mock_identity.return_value = {
                "message": "test",
                "intent": {"category": "identity"},
            }

            await handler.handle(intent, session_id="test-session")

            mock_identity.assert_called_once()


class TestDiscoveryHandlerResponse:
    """Test _handle_discovery_query response content."""

    @pytest.fixture
    def handler(self):
        """Create a CanonicalHandlers instance."""
        return CanonicalHandlers()

    @pytest.mark.asyncio
    async def test_discovery_response_structure(self, handler):
        """Test that discovery response has correct structure."""
        intent = Intent(
            category=IntentCategory.DISCOVERY,
            action="get_capabilities",
            confidence=1.0,
            context={"original_message": "what can you do"},
        )

        # Mock plugin registry to return predictable data
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry"
        ) as mock_registry:
            mock_registry.return_value.get_status_all.return_value = {}

            result = await handler._handle_discovery_query(intent, "test-session")

        assert "message" in result
        assert "intent" in result
        assert result["intent"]["category"] == "discovery"
        assert result["intent"]["action"] == "provide_capabilities"
        assert "capabilities" in result["intent"]["context"]
        assert "core" in result["intent"]["context"]

    @pytest.mark.asyncio
    async def test_discovery_includes_core_capabilities(self, handler):
        """Test that discovery response includes core capabilities."""
        intent = Intent(
            category=IntentCategory.DISCOVERY,
            action="get_capabilities",
            confidence=1.0,
            context={},
        )

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry"
        ) as mock_registry:
            mock_registry.return_value.get_status_all.return_value = {}

            result = await handler._handle_discovery_query(intent, "test-session")

        core = result["intent"]["context"]["core"]
        assert "development coordination" in core
        assert "issue tracking" in core
        assert "strategic planning" in core

    @pytest.mark.asyncio
    async def test_discovery_with_integrations(self, handler):
        """Test that discovery response includes active integrations."""
        intent = Intent(
            category=IntentCategory.DISCOVERY,
            action="get_capabilities",
            confidence=1.0,
            context={},
        )

        # Mock an active integration
        mock_plugin = MagicMock()
        mock_plugin.get_metadata.return_value = MagicMock(
            description="Calendar integration",
            capabilities=["routes", "webhooks"],
        )

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry"
        ) as mock_registry:
            mock_registry.return_value.get_status_all.return_value = {
                "calendar": {"configured": True, "active": True}
            }
            mock_registry.return_value.get_plugin.return_value = mock_plugin

            result = await handler._handle_discovery_query(intent, "test-session")

        integrations = result["intent"]["context"]["integrations"]
        assert len(integrations) > 0
        assert integrations[0]["name"] == "calendar"


class TestDiscoveryFormatting:
    """Test discovery response formatting methods."""

    @pytest.fixture
    def handler(self):
        """Create a CanonicalHandlers instance."""
        return CanonicalHandlers()

    def test_format_discovery_standard(self, handler):
        """Test standard discovery format."""
        capabilities_data = {
            "core": ["development coordination", "issue tracking"],
            "integrations": [{"name": "slack", "description": "Team communication"}],
            "capabilities_list": [
                "development coordination",
                "issue tracking",
                "slack integration",
            ],
        }

        result = handler._format_discovery_standard(capabilities_data)

        assert "what i can help you with" in result.lower()
        assert "Core Capabilities" in result
        assert "Slack" in result

    def test_format_discovery_granular(self, handler):
        """Test granular discovery format."""
        capabilities_data = {
            "core": ["development coordination"],
            "integrations": [],
            "capabilities_list": ["development coordination"],
        }

        result = handler._format_discovery_granular(capabilities_data)

        assert "What I Can Do" in result
        assert "Quick Commands" in result

    def test_format_discovery_embedded(self, handler):
        """Test embedded (compact) discovery format."""
        capabilities_data = {
            "core": ["a", "b", "c"],
            "integrations": [{"name": "slack"}, {"name": "github"}],
            "capabilities_list": [],
        }

        result = handler._format_discovery_embedded(capabilities_data)

        # Should be brief
        assert len(result) < 150
        assert "2 integrations" in result


class TestIntentCategoryEnum:
    """Test that DISCOVERY is properly added to IntentCategory."""

    def test_discovery_in_enum(self):
        """Test that DISCOVERY exists in IntentCategory."""
        assert hasattr(IntentCategory, "DISCOVERY")
        assert IntentCategory.DISCOVERY.value == "discovery"

    def test_identity_still_exists(self):
        """Test that IDENTITY still exists (regression)."""
        assert hasattr(IntentCategory, "IDENTITY")
        assert IntentCategory.IDENTITY.value == "identity"
