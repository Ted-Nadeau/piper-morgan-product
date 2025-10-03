# Piper Plugin Development Guide

## Overview

The Piper plugin system allows integrations to self-register as modular
components with standardized interfaces.

**Phase 3A**: Interface definition (this guide)
**Phase 3B**: Registry implementation
**Phase 3C**: Integration plugin wrappers

## Plugin Architecture

### Core Concepts

- **Plugin**: Self-contained integration module (Slack, Notion, GitHub, Calendar)
- **Interface**: Abstract base class (PiperPlugin) all plugins implement
- **Metadata**: Plugin identity, version, capabilities, dependencies
- **Lifecycle**: Registration → Initialization → Operation → Shutdown
- **Routes**: Optional FastAPI routes plugins can provide

### Plugin Capabilities

Plugins declare their capabilities via metadata:

- **routes**: Provides HTTP endpoints
- **webhooks**: Handles webhook callbacks
- **spatial**: Uses spatial intelligence
- **mcp**: Uses Model Context Protocol
- **background**: Runs background tasks

## Creating a Plugin

### Step 1: Implement PiperPlugin Interface

```python
from services.plugins import PiperPlugin, PluginMetadata
from fastapi import APIRouter
from typing import Optional, Dict, Any
import structlog

class MyPlugin(PiperPlugin):
    """My integration plugin"""

    def __init__(self):
        self.logger = structlog.get_logger()
        self.config = self._load_config()

    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata"""
        return PluginMetadata(
            name="my_plugin",
            version="1.0.0",
            description="My awesome integration plugin",
            author="Your Name",
            capabilities=["routes", "webhooks"],
            dependencies=[]  # Other plugins this depends on
        )

    def get_router(self) -> Optional[APIRouter]:
        """Return FastAPI router with plugin routes"""
        router = APIRouter(prefix="/api/v1/my-plugin", tags=["My Plugin"])

        @router.get("/status")
        async def get_status():
            return {"status": "active", "message": "Plugin operational"}

        @router.post("/webhook")
        async def handle_webhook(request: Request):
            data = await request.json()
            # Process webhook
            return {"status": "received"}

        return router

    def is_configured(self) -> bool:
        """Check if plugin is properly configured"""
        # Validate required configuration
        return self.config.api_key is not None

    async def initialize(self) -> None:
        """Initialize plugin resources at startup"""
        self.logger.info(f"Initializing {self.get_metadata().name}")

        # Initialize connections
        # Allocate resources
        # Validate configuration

        if not self.is_configured():
            self.logger.warning("Plugin not fully configured")
        else:
            self.logger.info("Plugin initialized successfully")

    async def shutdown(self) -> None:
        """Cleanup plugin resources at shutdown"""
        self.logger.info(f"Shutting down {self.get_metadata().name}")

        # Close connections
        # Release resources
        # Save state

        self.logger.info("Plugin shutdown complete")

    def get_status(self) -> Dict[str, Any]:
        """Return plugin health and status"""
        return {
            "name": self.get_metadata().name,
            "version": self.get_metadata().version,
            "configured": self.is_configured(),
            "active": True,
            "connections": {
                "api": "connected" if self.is_configured() else "not configured"
            },
            "metrics": {
                "requests_today": 0,
                "errors": 0
            }
        }
```

### Step 2: Auto-Register Plugin (Phase 3B)

```python
# At bottom of plugin module file
from services.plugins.plugin_registry import get_plugin_registry

# Create plugin instance
_plugin = MyPlugin()

# Auto-register with global registry
get_plugin_registry().register(_plugin)
```

**Note**: Registry implementation comes in Phase 3B.

### Step 3: Plugin Discovery

Plugins are discovered via import:

```python
# In web/app.py or plugin loader
from services.integrations.my_plugin import my_plugin_module
# Plugin auto-registers on import
```

## Plugin Lifecycle

### 1. Registration Phase

- Plugin module imported
- Plugin instantiated
- Plugin registers with global registry

### 2. Initialization Phase

- Application startup begins
- Registry calls `initialize()` on all plugins
- Plugins validate configuration, establish connections
- Plugins with missing config can still initialize (graceful degradation)

### 3. Operation Phase

- Plugin routes mounted to FastAPI app
- Plugin status queryable via `/api/v1/plugins` endpoint
- Plugins handle requests, webhooks, background tasks

### 4. Shutdown Phase

- Application shutdown begins
- Registry calls `shutdown()` on all plugins
- Plugins cleanup resources, close connections, save state

## Plugin Configuration

### Configuration Service Pattern

Plugins should use configuration services (ADR-010):

```python
class MyPlugin(PiperPlugin):
    def __init__(self, config_service: Optional[MyConfigService] = None):
        self.config_service = config_service or MyConfigService()

    def is_configured(self) -> bool:
        return self.config_service.is_configured()
```

### Graceful Degradation

Plugins should handle missing configuration gracefully:

```python
async def initialize(self) -> None:
    if not self.is_configured():
        self.logger.warning(f"{self.get_metadata().name} not configured - running in degraded mode")
        return

    # Full initialization only if configured
    await self._establish_connections()
```

## Plugin Routes

### Route Prefix Convention

- **Core API**: `/api/v1/{plugin_name}`
- **Webhooks**: `/api/v1/{plugin_name}/webhook`
- **Admin**: `/api/v1/{plugin_name}/admin`

### Route Example

```python
def get_router(self) -> Optional[APIRouter]:
    router = APIRouter(
        prefix="/api/v1/slack",
        tags=["Slack Integration"]
    )

    @router.get("/status")
    async def get_status():
        return self.get_status()

    @router.post("/webhook")
    async def handle_webhook(request: Request):
        # Slack webhook handling
        return {"status": "received"}

    @router.post("/message")
    async def send_message(message: str):
        # Send message to Slack
        return {"status": "sent"}

    return router
```

## Plugin Status Endpoint

All plugins automatically get a status endpoint:

```
GET /api/v1/plugins
GET /api/v1/plugins/{plugin_name}
```

Status response format:

```json
{
  "name": "slack",
  "version": "1.0.0",
  "configured": true,
  "active": true,
  "connections": {
    "api": "connected",
    "webhooks": "active"
  },
  "metrics": {
    "requests_today": 142,
    "errors": 0
  }
}
```

## Plugin Dependencies

Plugins can declare dependencies on other plugins:

```python
def get_metadata(self) -> PluginMetadata:
    return PluginMetadata(
        name="advanced_plugin",
        version="1.0.0",
        description="Advanced plugin requiring Slack",
        author="Developer",
        capabilities=["routes"],
        dependencies=["slack"]  # Requires slack plugin
    )
```

Registry ensures dependencies are initialized first (Phase 3B).

## Best Practices

### 1. Keep Plugins Self-Contained

- Plugin should be a single module or package
- All plugin logic in one place
- Minimal dependencies on other plugins

### 2. Use Dependency Injection

```python
def __init__(
    self,
    config_service: Optional[ConfigService] = None,
    adapter: Optional[Adapter] = None
):
    self.config_service = config_service or ConfigService()
    self.adapter = adapter or Adapter(self.config_service)
```

### 3. Handle Initialization Errors Gracefully

```python
async def initialize(self) -> None:
    try:
        await self._initialize_connections()
    except Exception as e:
        self.logger.error(f"Initialization failed: {e}")
        # Continue in degraded mode, don't crash
```

### 4. Provide Detailed Status

```python
def get_status(self) -> Dict[str, Any]:
    return {
        "name": self.get_metadata().name,
        "configured": self.is_configured(),
        "active": True,
        "health": "healthy" if self._check_health() else "degraded",
        "connections": self._get_connection_status(),
        "metrics": self._get_metrics(),
        "last_error": self._last_error,
        "uptime_seconds": self._get_uptime()
    }
```

### 5. Clean Up Resources in Shutdown

```python
async def shutdown(self) -> None:
    try:
        # Close connections
        if hasattr(self, 'client'):
            await self.client.close()

        # Stop background tasks
        if hasattr(self, 'background_task'):
            self.background_task.cancel()

        # Save state
        await self._save_state()
    except Exception as e:
        # Log but don't raise
        self.logger.error(f"Shutdown error: {e}")
```

## Testing Plugins

### Unit Testing

```python
import pytest
from services.plugins import PluginMetadata

def test_plugin_metadata():
    plugin = MyPlugin()
    metadata = plugin.get_metadata()

    assert metadata.name == "my_plugin"
    assert metadata.version == "1.0.0"
    assert "routes" in metadata.capabilities

def test_plugin_configuration():
    plugin = MyPlugin()
    assert isinstance(plugin.is_configured(), bool)

@pytest.mark.asyncio
async def test_plugin_lifecycle():
    plugin = MyPlugin()

    # Test initialization
    await plugin.initialize()

    # Test status
    status = plugin.get_status()
    assert "name" in status
    assert "configured" in status

    # Test shutdown
    await plugin.shutdown()
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_plugin_router():
    from fastapi.testclient import TestClient
    from fastapi import FastAPI

    app = FastAPI()
    plugin = MyPlugin()

    # Mount plugin router
    router = plugin.get_router()
    if router:
        app.include_router(router)

    # Test routes
    client = TestClient(app)
    response = client.get("/api/v1/my-plugin/status")
    assert response.status_code == 200
```

## Example: Slack Plugin Wrapper

```python
from services.plugins import PiperPlugin, PluginMetadata
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
from services.integrations.slack.config_service import SlackConfigService
from fastapi import APIRouter

class SlackPlugin(PiperPlugin):
    """Slack integration plugin wrapper"""

    def __init__(self):
        self.config_service = SlackConfigService()
        self.router_impl = SlackIntegrationRouter(self.config_service)
        self.logger = structlog.get_logger()

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="slack",
            version="1.0.0",
            description="Slack integration with spatial intelligence",
            author="Piper Team",
            capabilities=["routes", "webhooks", "spatial"],
            dependencies=[]
        )

    def get_router(self) -> Optional[APIRouter]:
        router = APIRouter(prefix="/api/v1/slack", tags=["Slack"])

        @router.post("/webhook")
        async def handle_webhook(request: Request):
            # Delegate to router implementation
            return await self.router_impl.handle_webhook(request)

        return router

    def is_configured(self) -> bool:
        return self.config_service.is_configured()

    async def initialize(self) -> None:
        self.logger.info("Initializing Slack plugin")
        # Additional setup if needed

    async def shutdown(self) -> None:
        self.logger.info("Shutting down Slack plugin")
        # Cleanup if needed

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": "slack",
            "version": "1.0.0",
            "configured": self.is_configured(),
            "active": True,
            "router": "SlackIntegrationRouter",
            "spatial_enabled": True
        }
```

## Next Steps

- **Phase 3B**: Implement PluginRegistry for plugin management
- **Phase 3C**: Create plugin wrappers for existing integrations
- **Phase 3D**: Integrate plugins with web/app.py startup

## Resources

- **Interface**: `services/plugins/plugin_interface.py`
- **Package**: `services/plugins/__init__.py`
- **ADR-034**: Plugin Architecture Decision Record
- **ADR-010**: Configuration Access Patterns

---

**Phase 3A**: Interface definition complete
**Generated**: 2025-10-02
