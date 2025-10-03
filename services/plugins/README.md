# Piper Plugin System

## Overview

The Piper plugin system enables integration plugins (Slack, Notion, GitHub, Calendar) to self-register as modular components with standardized interfaces.

**Built**: October 2, 2025 (GREAT-3A Phase 3)

## Architecture

### Components

- **PiperPlugin Interface** (`plugin_interface.py`): Abstract base class all plugins implement
- **PluginRegistry** (`plugin_registry.py`): Singleton registry managing plugin lifecycle
- **Auto-Registration**: Plugins register on module import
- **FastAPI Integration**: Plugin routers auto-mount at startup

### How It Works

1. **Plugin Definition**: Implement `PiperPlugin` interface
2. **Auto-Registration**: Plugin registers on import
3. **Startup**: Registry initializes all plugins
4. **Router Mounting**: Plugin routes auto-mount to FastAPI
5. **Lifecycle**: Registry manages init/shutdown

## Current Plugins

| Plugin | Capabilities | Status |
|--------|-------------|--------|
| **Slack** | routes, webhooks, spatial | ✅ Active |
| **GitHub** | routes, spatial | ✅ Active |
| **Notion** | routes, mcp | ✅ Active |
| **Calendar** | routes, spatial | ✅ Active |

## Adding New Plugins

See `PLUGIN_GUIDE.md` for complete development guide.

### Quick Start

```python
from services.plugins import PiperPlugin, PluginMetadata
from fastapi import APIRouter

class MyPlugin(PiperPlugin):
    def get_metadata(self):
        return PluginMetadata(
            name="my_plugin",
            version="1.0.0",
            description="My integration",
            author="Developer Name",
            capabilities=["routes"],
            dependencies=[]
        )

    def get_router(self):
        router = APIRouter(prefix="/api/v1/my-plugin")
        # Add routes...
        return router

    def is_configured(self):
        return True  # Check actual config

    async def initialize(self):
        # Startup logic
        pass

    async def shutdown(self):
        # Cleanup logic
        pass

    def get_status(self):
        return {"status": "active"}

# Auto-register
from services.plugins import get_plugin_registry
_plugin = MyPlugin()
get_plugin_registry().register(_plugin)
```

### Integration Steps

1. Create plugin class in `services/integrations/my_integration/my_plugin.py`
2. Implement all `PiperPlugin` methods
3. Add auto-registration at module bottom
4. Import plugin in `web/app.py` lifespan
5. Plugin auto-loads at startup

## Testing Plugins

### Interface Validation

```python
from my_plugin import _plugin
from tests.plugins.test_plugin_interface import validate_plugin_interface

validate_plugin_interface(_plugin)  # Raises if invalid
```

### Full Test Suite

```bash
# Run all plugin tests
pytest tests/plugins/ -v

# Run specific test
pytest tests/plugins/test_plugin_interface.py::TestPiperPluginInterface -v
```

## Monitoring

### Plugin Status

```python
from services.plugins import get_plugin_registry

registry = get_plugin_registry()

# List all plugins
plugins = registry.list_plugins()

# Get plugin status
status = registry.get_status_all()

# Get specific plugin
slack_plugin = registry.get_plugin("slack")
```

### Health Checks

Each plugin provides status via `get_status()`:

```python
plugin = registry.get_plugin("slack")
status = plugin.get_status()
# Returns: {"configured": bool, "router": str, ...}
```

## Plugin Capabilities

Plugins declare capabilities in metadata:

- **routes**: Provides HTTP endpoints
- **webhooks**: Handles webhook callbacks
- **spatial**: Uses spatial intelligence (MCP-based)
- **mcp**: Uses Model Context Protocol
- **background**: Runs background tasks

## Architecture Decisions

See ADRs for design rationale:
- ADR-010: Configuration Access Patterns
- ADR-038: Spatial Intelligence Patterns

## Files

```
services/plugins/
├── __init__.py              # Package exports
├── plugin_interface.py      # PiperPlugin ABC + PluginMetadata
├── plugin_registry.py       # PluginRegistry singleton
├── PLUGIN_GUIDE.md          # Development guide
└── README.md               # This file

tests/plugins/
├── test_plugin_interface.py # Interface compliance tests
├── test_plugin_registry.py  # Registry tests
└── conftest.py              # Test fixtures
```

## Future Enhancements

Potential improvements:
- Dynamic plugin loading from config
- Plugin marketplace
- Plugin dependencies resolution
- Hot-reload support
- Plugin sandboxing
- Version management
