# Plugin Interface Tests

## Purpose

Validates that plugins correctly implement the PiperPlugin interface.

## Running Tests

```bash
# Run all plugin tests
pytest tests/plugins/ -v

# Run specific test class
pytest tests/plugins/test_plugin_interface.py::TestPiperPluginInterface -v

# Run with coverage
pytest tests/plugins/ --cov=services.plugins --cov-report=html
```

## Test Coverage

- **PluginMetadata**: Dataclass creation and fields
- **PiperPlugin Interface**: All required methods
- **Plugin Lifecycle**: Initialize and shutdown
- **Router Integration**: FastAPI router handling
- **Status Reporting**: Status dict validation

## Using Tests for New Plugins

When creating a new plugin, use `validate_plugin_interface()`:

```python
from tests.plugins.test_plugin_interface import validate_plugin_interface

# Validate your plugin
plugin = MyNewPlugin()
validate_plugin_interface(plugin)  # Raises AssertionError if invalid
```

## Phase 3C Usage

These tests will be used to validate all 4 integration plugin wrappers:

- SlackPlugin
- NotionPlugin
- GitHubPlugin
- CalendarPlugin
