"""Fixtures for contract testing all plugins

These fixtures provide automatic plugin discovery and parametrization
for testing that ALL plugins comply with the PiperPlugin interface.
"""

import pytest

from services.plugins import get_plugin_registry, reset_plugin_registry


@pytest.fixture(scope="session")
def contract_registry():
    """Session-scoped plugin registry for contract tests

    Loads all enabled plugins once per test session for efficiency.
    """
    reset_plugin_registry()
    registry = get_plugin_registry()
    registry.load_enabled_plugins()
    return registry


@pytest.fixture(scope="session")
def all_plugin_names(contract_registry):
    """List of all registered plugin names

    Returns:
        List[str]: Names of all plugins in the registry
    """
    return contract_registry.list_plugins()


@pytest.fixture
def plugin_instance(request, contract_registry):
    """Get a specific plugin instance by name

    Used with parametrize to test each plugin individually.

    Args:
        request: pytest request with plugin name as param
        contract_registry: The session-scoped registry

    Returns:
        PiperPlugin: The requested plugin instance
    """
    plugin_name = request.param
    return contract_registry.get_plugin(plugin_name)


def pytest_generate_tests(metafunc):
    """Auto-parametrize tests that use plugin_instance fixture

    This hook automatically parametrizes any test using the plugin_instance
    fixture to run against all registered plugins.

    Example:
        def test_something(plugin_instance):
            # This will run once for each plugin automatically
            assert plugin_instance is not None
    """
    if "plugin_instance" in metafunc.fixturenames:
        # Get all plugin names for parametrization
        registry = get_plugin_registry()
        reset_plugin_registry()
        registry = get_plugin_registry()
        registry.load_enabled_plugins()
        plugin_names = registry.list_plugins()

        # Parametrize the test with all plugin names
        metafunc.parametrize(
            "plugin_instance", plugin_names, indirect=True, ids=lambda name: f"plugin={name}"
        )
