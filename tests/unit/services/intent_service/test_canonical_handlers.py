"""
Unit tests for canonical_handlers.py

Tests for CanonicalHandlers class, focusing on:
- _get_dynamic_capabilities() method (Issue #493)
- Plugin registry integration
- Error handling for registry failures
"""

from unittest.mock import MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.plugins.plugin_interface import PluginMetadata


@pytest.fixture
def canonical_handlers():
    """Fixture to create CanonicalHandlers instance"""
    return CanonicalHandlers()


@pytest.fixture
def mock_plugin_registry():
    """Fixture to create a mock PluginRegistry"""
    registry = MagicMock()

    # Mock get_status_all to return status for configured plugins
    registry.get_status_all.return_value = {
        "slack": {"configured": True, "active": True, "status": "active"},
        "github": {"configured": True, "active": False, "status": "inactive"},
        "notion": {"configured": False, "active": False, "status": "not_configured"},
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
                capabilities=["channels", "messages", "spatial"],
            )
            return plugin
        elif name == "github":
            plugin = MagicMock()
            plugin.get_metadata.return_value = PluginMetadata(
                name="github",
                version="1.0.0",
                description="GitHub integration for issue tracking",
                author="Piper Team",
                capabilities=["issues", "pull_requests", "webhooks"],
            )
            return plugin
        else:
            return None

    registry.get_plugin.side_effect = get_plugin_side_effect

    return registry


class TestGetDynamicCapabilities:
    """Test suite for _get_dynamic_capabilities() method"""

    def test_returns_expected_structure(self, canonical_handlers, mock_plugin_registry):
        """
        Test that _get_dynamic_capabilities() returns the expected dict structure
        with 'core', 'integrations', and 'capabilities_list' keys.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert
        assert isinstance(result, dict)
        assert "core" in result
        assert "integrations" in result
        assert "capabilities_list" in result

        # Verify structure types
        assert isinstance(result["core"], list)
        assert isinstance(result["integrations"], list)
        assert isinstance(result["capabilities_list"], list)

    def test_core_capabilities_always_present(self, canonical_handlers, mock_plugin_registry):
        """
        Test that core PM capabilities are always included regardless of plugin state.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Core capabilities should be present
        core = result["core"]
        assert "development coordination" in core
        assert "issue tracking" in core
        assert "strategic planning" in core
        assert len(core) == 3

    def test_includes_active_plugins(self, canonical_handlers, mock_plugin_registry):
        """
        Test that active and configured plugins are included in integrations list.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Should include slack (active) and github (configured)
        integrations = result["integrations"]
        assert len(integrations) == 2

        # Check slack integration
        slack_integration = next((i for i in integrations if i["name"] == "slack"), None)
        assert slack_integration is not None
        assert slack_integration["description"] == "Slack integration for team communication"
        assert "channels" in slack_integration["capabilities"]

        # Check github integration
        github_integration = next((i for i in integrations if i["name"] == "github"), None)
        assert github_integration is not None
        assert github_integration["description"] == "GitHub integration for issue tracking"
        assert "issues" in github_integration["capabilities"]

    def test_excludes_unconfigured_plugins(self, canonical_handlers, mock_plugin_registry):
        """
        Test that unconfigured and inactive plugins are excluded from integrations.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Notion should NOT be included (not configured, not active)
        integrations = result["integrations"]
        notion_names = [i["name"] for i in integrations]
        assert "notion" not in notion_names

    def test_capabilities_list_includes_all(self, canonical_handlers, mock_plugin_registry):
        """
        Test that capabilities_list includes core capabilities plus integration names.
        """
        # Arrange
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert
        capabilities_list = result["capabilities_list"]

        # Should contain core capabilities
        assert "development coordination" in capabilities_list
        assert "issue tracking" in capabilities_list
        assert "strategic planning" in capabilities_list

        # Should contain integration summaries
        assert "slack integration" in capabilities_list
        assert "github integration" in capabilities_list

        # Total should be 3 core + 2 integrations = 5
        assert len(capabilities_list) == 5

    def test_handles_registry_unavailable(self, canonical_handlers):
        """
        Test that method gracefully handles PluginRegistry being unavailable.
        Should return core capabilities only without raising exception.
        """
        # Arrange - Mock get_plugin_registry to raise exception
        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry"
        ) as mock_get_registry:
            mock_get_registry.side_effect = Exception("Registry not available")

            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Should still return valid structure with core capabilities
        assert isinstance(result, dict)
        assert "core" in result
        assert "integrations" in result
        assert "capabilities_list" in result

        # Core capabilities should be present
        assert len(result["core"]) == 3

        # Integrations should be empty list (not None)
        assert result["integrations"] == []

        # Capabilities list should only have core
        assert len(result["capabilities_list"]) == 3

    def test_handles_plugin_metadata_error(self, canonical_handlers, mock_plugin_registry):
        """
        Test that method handles errors when getting plugin metadata.
        Current implementation: entire plugin processing aborts on first error.
        Returns core capabilities only.
        """

        # Arrange - Make slack plugin raise error on get_metadata
        def get_plugin_error_side_effect(name):
            if name == "slack":
                plugin = MagicMock()
                plugin.get_metadata.side_effect = Exception("Metadata error")
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
            return None

        mock_plugin_registry.get_plugin.side_effect = get_plugin_error_side_effect

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=mock_plugin_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Current implementation: entire loop aborts on error
        # So no integrations are returned (caught by broad exception handler)
        integrations = result["integrations"]
        assert len(integrations) == 0  # No plugins included due to error

        # Core capabilities should still be present
        assert len(result["core"]) == 3
        assert len(result["capabilities_list"]) == 3

    def test_empty_plugin_registry(self, canonical_handlers):
        """
        Test behavior when plugin registry has no plugins registered.
        Should return only core capabilities.
        """
        # Arrange
        empty_registry = MagicMock()
        empty_registry.get_status_all.return_value = {}

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry",
            return_value=empty_registry,
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert
        assert len(result["core"]) == 3
        assert len(result["integrations"]) == 0
        assert len(result["capabilities_list"]) == 3

    def test_plugin_returns_none(self, canonical_handlers):
        """
        Test that method handles when get_plugin returns None for a plugin.
        Should skip that plugin gracefully.
        """
        # Arrange - Create fresh mock with get_plugin returning None
        registry = MagicMock()
        registry.get_status_all.return_value = {
            "slack": {"configured": True, "active": True},
            "github": {"configured": True, "active": False},
        }
        # All get_plugin calls return None
        registry.get_plugin.return_value = None

        with patch(
            "services.intent_service.canonical_handlers.get_plugin_registry", return_value=registry
        ):
            # Act
            result = canonical_handlers._get_dynamic_capabilities()

        # Assert - Should have core but no integrations (plugins returned None)
        assert len(result["core"]) == 3
        assert len(result["integrations"]) == 0
        assert len(result["capabilities_list"]) == 3
