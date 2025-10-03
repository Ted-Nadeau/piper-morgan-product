# Piper Morgan Plugin System Guide

## Overview

The Piper Morgan plugin system provides a flexible, extensible architecture for integrations. Built during GREAT-3A and enhanced in GREAT-3B, it enables dynamic discovery, configuration-based loading, and seamless integration management.

## Architecture

### Components

1. **PiperPlugin Interface** (`plugin_interface.py`)
   - Defines plugin contract with 6 required methods
   - Metadata system for plugin information
   - Abstract base class ensuring consistency

2. **PluginRegistry** (`plugin_registry.py`)
   - Singleton registry managing all plugins
   - Discovery and dynamic loading capabilities
   - Lifecycle management (init/shutdown)
   - Router collection and mounting

3. **Plugin Implementations**
   - Located in `services/integrations/*/`
   - Each has `[name]_plugin.py` file
   - Auto-register on import via module-level code

### Plugin Lifecycle

1. **Discovery** - Registry scans `services/integrations/*/` for `*_plugin.py` files
2. **Configuration** - Reads enabled list from `config/PIPER.user.md`
3. **Loading** - Imports enabled plugins dynamically using `importlib`
4. **Registration** - Plugins auto-register themselves on import
5. **Initialization** - `initialize()` called on each registered plugin
6. **Operation** - Plugins serve routes, handle events, provide capabilities
7. **Shutdown** - `shutdown()` called on each plugin during app shutdown

## Configuration

### Enabling/Disabling Plugins

Edit `config/PIPER.user.md` and add the Plugin Configuration section:

```markdown
## 🔌 Plugin Configuration

Configure which integration plugins are enabled and their settings.

```yaml
plugins:
  enabled:
    - github
    - slack
    - notion
    # - calendar  # Disabled
```
```

**Default Behavior**: All discovered plugins are enabled if no configuration exists.

### Plugin Settings

```yaml
plugins:
  enabled:
    - slack
    - github
  settings:
    slack:
      workspace: "engineering"
      timeout: 30
    github:
      timeout: 45
      retry_count: 3
```

Each plugin can read its own settings from the config using its config service.

## Creating a New Plugin

### Step 1: Create Plugin Directory

```bash
mkdir services/integrations/my_integration
touch services/integrations/my_integration/__init__.py
```

### Step 2: Implement Plugin Class

Create `services/integrations/my_integration/my_integration_plugin.py`:

```python
from services.plugins import PiperPlugin, PluginMetadata
from fastapi import APIRouter

class MyIntegrationPlugin(PiperPlugin):
    def get_metadata(self):
        return PluginMetadata(
            name="my_integration",
            version="1.0.0",
            description="My custom integration",
            author="Developer Name",
            capabilities=["routes"],
            dependencies=[]
        )

    def get_router(self):
        router = APIRouter(prefix="/api/v1/my-integration")

        @router.get("/status")
        async def get_status():
            return {"status": "active"}

        return router

    def is_configured(self):
        # Check if integration is properly configured
        return True

    async def initialize(self):
        # Startup logic here
        print("MyIntegration plugin initialized")

    async def shutdown(self):
        # Cleanup logic here
        print("MyIntegration plugin shutdown")

    def get_status(self):
        return {
            "status": "active",
            "configured": self.is_configured(),
            "capabilities": self.get_metadata().capabilities
        }

# Auto-register plugin when module is imported
from services.plugins import get_plugin_registry
_my_integration_plugin = MyIntegrationPlugin()
get_plugin_registry().register(_my_integration_plugin)
```

### Step 3: Add to Configuration

Add your plugin to the enabled list in `config/PIPER.user.md`:

```yaml
plugins:
  enabled:
    - github
    - slack
    - notion
    - calendar
    - my_integration  # Your new plugin
```

### Step 4: Test Your Plugin

```python
from services.plugins import get_plugin_registry

registry = get_plugin_registry()

# Test discovery
available = registry.discover_plugins()
assert "my_integration" in available

# Test loading
results = registry.load_enabled_plugins()
assert results.get("my_integration") == True

# Test functionality
plugin = registry.get_plugin("my_integration")
assert plugin is not None
```

## API Reference

### PluginRegistry Methods

#### Discovery and Loading

- `discover_plugins() -> Dict[str, str]` - Find available plugins
- `load_plugin(name: str, module_path: str) -> bool` - Load single plugin
- `load_enabled_plugins() -> Dict[str, bool]` - Load all enabled plugins
- `get_enabled_plugins() -> List[str]` - Get enabled plugin names from config

#### Registry Management

- `register(plugin: PiperPlugin) -> None` - Register plugin instance
- `unregister(plugin_name: str) -> bool` - Remove plugin from registry
- `get_plugin(name: str) -> Optional[PiperPlugin]` - Get plugin by name
- `list_plugins() -> List[str]` - List all registered plugin names
- `get_plugin_count() -> int` - Count of registered plugins

#### Lifecycle Management

- `initialize_all() -> Dict[str, bool]` - Initialize all registered plugins
- `shutdown_all() -> Dict[str, bool]` - Shutdown all registered plugins
- `is_initialized() -> bool` - Check if registry is initialized

#### Router and Status

- `get_routers() -> List[APIRouter]` - Get all plugin routers for mounting
- `get_status_all() -> Dict[str, Dict]` - Get status of all plugins
- `get_plugins_with_capability(capability: str) -> List[PiperPlugin]` - Filter by capability

### PiperPlugin Interface

All plugins must implement these methods:

```python
def get_metadata(self) -> PluginMetadata:
    """Return plugin metadata"""

def get_router(self) -> Optional[APIRouter]:
    """Return FastAPI router or None"""

def is_configured(self) -> bool:
    """Check if plugin is properly configured"""

async def initialize(self) -> None:
    """Initialize plugin (startup logic)"""

async def shutdown(self) -> None:
    """Shutdown plugin (cleanup logic)"""

def get_status(self) -> Dict[str, Any]:
    """Return current plugin status"""
```

## Troubleshooting

### Common Issues

**Plugin Not Discovered**
- Check file naming: must be `[name]_plugin.py`
- Verify directory structure: `services/integrations/[name]/[name]_plugin.py`
- Ensure directory has `__init__.py`

**Plugin Not Loading**
- Check if enabled in `config/PIPER.user.md`
- Verify no syntax errors in plugin file
- Check logs for import errors

**Plugin Not Registering**
- Ensure auto-registration code at module bottom
- Check for duplicate plugin names
- Verify plugin implements PiperPlugin interface

**Configuration Not Working**
- Check YAML syntax in `config/PIPER.user.md`
- Ensure Plugin Configuration section exists
- Verify plugin names match discovery names

### Debug Commands

```python
# Check what's discovered
from services.plugins import get_plugin_registry
registry = get_plugin_registry()
print("Available:", registry.discover_plugins())

# Check what's enabled
print("Enabled:", registry.get_enabled_plugins())

# Check what's loaded
print("Loaded:", registry.list_plugins())

# Check plugin status
print("Status:", registry.get_status_all())
```

### Logging

Plugin system uses structured logging. Enable debug logging to see detailed information:

```python
import logging
logging.getLogger("services.plugins").setLevel(logging.DEBUG)
```

## Best Practices

### Plugin Development

1. **Keep plugins focused** - One integration per plugin
2. **Handle errors gracefully** - Don't crash the app
3. **Implement all interface methods** - Even if some return None
4. **Use descriptive metadata** - Help users understand capabilities
5. **Test thoroughly** - Unit tests and integration tests

### Configuration

1. **Provide sensible defaults** - Plugin should work without config
2. **Validate configuration** - Check in `is_configured()`
3. **Document settings** - Clear comments in config examples
4. **Handle missing config** - Graceful degradation

### Performance

1. **Lazy initialization** - Don't do heavy work in `__init__`
2. **Async operations** - Use async/await for I/O
3. **Resource cleanup** - Properly implement `shutdown()`
4. **Efficient routing** - Minimize route overhead

## Examples

See existing plugins for reference:
- `services/integrations/slack/slack_plugin.py` - Full-featured with webhooks
- `services/integrations/github/github_plugin.py` - API integration
- `services/integrations/notion/notion_plugin.py` - MCP adapter pattern
- `services/integrations/calendar/calendar_plugin.py` - Simple routes

## Version History

- **GREAT-3A (Oct 2, 2025)**: Initial plugin system with interface and registry
- **GREAT-3B (Oct 3, 2025)**: Added discovery, dynamic loading, and configuration
