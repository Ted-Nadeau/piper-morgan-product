# Claude Code Agent Prompt: GREAT-3C Phase 3 - Demo Plugin Implementation

## Session Log Management
Continue session log: `dev/2025/10/04/2025-10-04-[timestamp]-code-log.md`

Update with timestamped entries for Phase 3 work.

## Mission
**Implement Demo Plugin**: Create a functional example plugin following the developer guide, serving as a copy-paste template for future integrations.

## Context

**Phase 2 Complete**: Developer guide created
- `docs/guides/plugin-development-guide.md` exists (497 lines)
- 8-step tutorial with weather integration example
- Complete code patterns documented

**Phase 3 Goal**: Build actual demo plugin that developers can reference and copy.

## Your Tasks

### Task 1: Create Demo Integration Directory

```bash
mkdir -p services/integrations/demo
mkdir -p services/integrations/demo/tests
```

### Task 2: Create Demo Config Service

**File**: `services/integrations/demo/config_service.py`

```python
"""Configuration service for Demo integration

This is a template showing the standard config service pattern.
Copy and adapt this for your own integrations.
"""

import os
from typing import Optional


class DemoConfigService:
    """Manages configuration for Demo integration

    This service demonstrates the standard pattern:
    - Read from environment variables
    - Provide sensible defaults
    - Include is_configured() check
    """

    def __init__(self):
        # Configuration from environment
        self.api_key = os.getenv("DEMO_API_KEY", "")
        self.api_endpoint = os.getenv(
            "DEMO_API_ENDPOINT",
            "https://api.example.com"
        )
        self.enabled = os.getenv("DEMO_ENABLED", "true").lower() == "true"

    def is_configured(self) -> bool:
        """Check if integration is properly configured

        Returns:
            bool: True if all required config present
        """
        # For demo purposes, always configured
        # Real integrations should check API keys, etc.
        return self.enabled

    def get_api_key(self) -> Optional[str]:
        """Get API key if configured

        Returns:
            Optional[str]: API key or None
        """
        return self.api_key if self.api_key else None

    def get_endpoint(self) -> str:
        """Get API endpoint

        Returns:
            str: API endpoint URL
        """
        return self.api_endpoint
```

### Task 3: Create Demo Integration Router

**File**: `services/integrations/demo/demo_integration_router.py`

```python
"""Demo integration router - business logic template

This demonstrates the standard router pattern for integrations.
Routers contain business logic and FastAPI routes.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any
from datetime import datetime

from .config_service import DemoConfigService


class DemoIntegrationRouter:
    """Demo integration router showing standard patterns

    This is a template showing common integration patterns:
    - Router setup with prefix and tags
    - Config service dependency injection
    - Health check endpoint
    - Example data endpoint
    - Error handling
    """

    def __init__(self, config_service: DemoConfigService):
        """Initialize router with config service

        Args:
            config_service: Configuration service instance
        """
        self.config = config_service
        self.router = APIRouter(
            prefix="/api/integrations/demo",
            tags=["demo", "example"]
        )
        self._setup_routes()

    def _setup_routes(self):
        """Define API routes

        This method sets up all the routes for this integration.
        Use @self.router decorators to define routes.
        """

        @self.router.get("/health")
        async def health_check() -> Dict[str, str]:
            """Health check endpoint

            Every integration should have a health check.
            Returns configuration status and basic info.

            Returns:
                Dict with status and service info
            """
            is_configured = self.config.is_configured()
            return {
                "status": "ok" if is_configured else "unconfigured",
                "service": "demo",
                "timestamp": datetime.utcnow().isoformat()
            }

        @self.router.get("/echo")
        async def echo(
            message: str = Query(default="Hello from Demo plugin!")
        ) -> Dict[str, Any]:
            """Echo endpoint - returns the message sent

            Simple endpoint demonstrating:
            - Query parameters
            - JSON response
            - Configuration check

            Args:
                message: Message to echo back

            Returns:
                Dict with echoed message and metadata
            """
            if not self.config.is_configured():
                raise HTTPException(
                    status_code=503,
                    detail="Demo integration not configured"
                )

            return {
                "echo": message,
                "timestamp": datetime.utcnow().isoformat(),
                "service": "demo",
                "configured": True
            }

        @self.router.get("/status")
        async def get_status() -> Dict[str, Any]:
            """Status endpoint showing integration details

            Returns:
                Dict with integration configuration and status
            """
            return {
                "integration": "demo",
                "configured": self.config.is_configured(),
                "endpoint": self.config.get_endpoint(),
                "routes": [
                    route.path
                    for route in self.router.routes
                ],
                "timestamp": datetime.utcnow().isoformat()
            }
```

### Task 4: Create Demo Plugin Wrapper

**File**: `services/integrations/demo/demo_plugin.py`

```python
"""Demo integration plugin wrapper

This demonstrates the standard plugin wrapper pattern.
Plugins are thin adapters that wrap routers to implement the PiperPlugin interface.
"""

from services.plugins.plugin_interface import PiperPlugin, PluginMetadata
from fastapi import APIRouter
from typing import Dict, Any

from .config_service import DemoConfigService
from .demo_integration_router import DemoIntegrationRouter


class DemoPlugin(PiperPlugin):
    """Demo plugin wrapper showing standard patterns

    This is a template showing the minimal plugin wrapper:
    - Implements all 6 PiperPlugin interface methods
    - Wraps an integration router
    - Uses config service for configuration
    - Provides metadata
    - Handles lifecycle (initialize/shutdown)

    Copy this pattern for your own plugins.
    """

    def __init__(self):
        """Initialize plugin with config and router

        Standard pattern:
        1. Create config service
        2. Create router with config
        3. Store both for interface methods
        """
        self.config_service = DemoConfigService()
        self.router_instance = DemoIntegrationRouter(self.config_service)

    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata

        Metadata describes the plugin's capabilities and identity.

        Returns:
            PluginMetadata with name, version, description, etc.
        """
        return PluginMetadata(
            name="demo",
            version="1.0.0",  # Use semantic versioning
            description="Demo integration template for developers",
            author="Piper Morgan Team",
            capabilities=["routes"]  # What this plugin provides
        )

    def get_router(self) -> APIRouter:
        """Return FastAPI router

        The router will be mounted into the main application.

        Returns:
            APIRouter with all integration routes
        """
        return self.router_instance.router

    def is_configured(self) -> bool:
        """Check if plugin is configured

        Delegates to config service to check configuration.

        Returns:
            bool: True if configured and ready to use
        """
        return self.config_service.is_configured()

    async def initialize(self):
        """Initialize plugin on startup

        Called when application starts.
        Use for:
        - Setting up connections
        - Loading resources
        - Validating configuration

        For demo, no initialization needed.
        """
        # Demo plugin needs no initialization
        # Real integrations might connect to APIs here
        pass

    async def shutdown(self):
        """Cleanup on shutdown

        Called when application stops.
        Use for:
        - Closing connections
        - Releasing resources
        - Cleanup tasks

        For demo, no cleanup needed.
        """
        # Demo plugin needs no cleanup
        # Real integrations might close connections here
        pass

    def get_status(self) -> Dict[str, Any]:
        """Return plugin status

        Provides runtime information about the plugin.

        Returns:
            Dict with status information
        """
        return {
            "configured": self.is_configured(),
            "router_prefix": self.router_instance.router.prefix,
            "routes": len(self.router_instance.router.routes),
            "tags": self.router_instance.router.tags
        }


# Auto-registration
# This code runs when the module is imported, registering the plugin
from services.plugins import get_plugin_registry

_demo_plugin = DemoPlugin()
get_plugin_registry().register(_demo_plugin)
```

### Task 5: Create __init__.py

**File**: `services/integrations/demo/__init__.py`

```python
"""Demo integration module

This is a template integration showing standard patterns.
Use this as a starting point for your own integrations.
"""

from .demo_plugin import DemoPlugin

__all__ = ["DemoPlugin"]
```

### Task 6: Create Tests

**File**: `services/integrations/demo/tests/test_demo_plugin.py`

```python
"""Tests for Demo plugin

This demonstrates standard testing patterns for plugins.
"""

import pytest
from services.integrations.demo.demo_plugin import DemoPlugin
from services.integrations.demo.config_service import DemoConfigService


class TestDemoPlugin:
    """Test suite for Demo plugin"""

    def test_plugin_metadata(self):
        """Test plugin metadata is correct"""
        plugin = DemoPlugin()
        metadata = plugin.get_metadata()

        assert metadata.name == "demo"
        assert metadata.version == "1.0.0"
        assert metadata.description == "Demo integration template for developers"
        assert "routes" in metadata.capabilities

    def test_plugin_has_router(self):
        """Test plugin provides router"""
        plugin = DemoPlugin()
        router = plugin.get_router()

        assert router is not None
        assert router.prefix == "/api/integrations/demo"
        assert "demo" in router.tags

    def test_plugin_is_configured(self):
        """Test plugin configuration check"""
        plugin = DemoPlugin()

        # Demo plugin should always be configured
        assert plugin.is_configured() is True

    @pytest.mark.asyncio
    async def test_plugin_lifecycle(self):
        """Test plugin initialization and shutdown"""
        plugin = DemoPlugin()

        # Should not raise errors
        await plugin.initialize()
        await plugin.shutdown()

    def test_plugin_status(self):
        """Test plugin status reporting"""
        plugin = DemoPlugin()
        status = plugin.get_status()

        assert "configured" in status
        assert "router_prefix" in status
        assert "routes" in status
        assert status["configured"] is True
        assert status["router_prefix"] == "/api/integrations/demo"
        assert status["routes"] >= 3  # At least health, echo, status

    def test_router_has_expected_routes(self):
        """Test router has all expected endpoints"""
        plugin = DemoPlugin()
        router = plugin.get_router()

        # Get all route paths
        paths = [route.path for route in router.routes]

        assert "/api/integrations/demo/health" in paths
        assert "/api/integrations/demo/echo" in paths
        assert "/api/integrations/demo/status" in paths


class TestDemoConfigService:
    """Test suite for Demo config service"""

    def test_config_service_creation(self):
        """Test config service can be created"""
        config = DemoConfigService()
        assert config is not None

    def test_config_is_configured(self):
        """Test is_configured method"""
        config = DemoConfigService()
        # Demo should always be configured
        assert config.is_configured() is True

    def test_config_get_endpoint(self):
        """Test endpoint retrieval"""
        config = DemoConfigService()
        endpoint = config.get_endpoint()

        assert endpoint is not None
        assert isinstance(endpoint, str)
```

### Task 7: Run Tests

```bash
cd ~/Development/piper-morgan
PYTHONPATH=. pytest services/integrations/demo/tests/ -v
```

**Expected**: All tests passing

### Task 8: Add Demo to Config (Optional)

**File**: `config/PIPER.user.md`

The demo plugin will auto-register, but for documentation purposes, show how it would be added:

```yaml
# Demo plugin is available but typically disabled in production
# Uncomment to enable:
# - demo
```

### Task 9: Test Integration Works

**Create test script**: `test_demo_integration.py` (temporary)

```python
"""Test demo integration is functional"""

from services.plugins import get_plugin_registry, reset_plugin_registry

# Reset and load
reset_plugin_registry()

# Import triggers registration
from services.integrations.demo import DemoPlugin

# Get registry
registry = get_plugin_registry()

# Check demo plugin loaded
plugins = registry.list_plugins()
print(f"Loaded plugins: {plugins}")
assert "demo" in plugins, "Demo plugin should be registered"

# Get plugin
demo = registry.get_plugin("demo")
assert demo is not None, "Should be able to get demo plugin"

# Check metadata
metadata = demo.get_metadata()
print(f"\nDemo Plugin Metadata:")
print(f"  Name: {metadata.name}")
print(f"  Version: {metadata.version}")
print(f"  Description: {metadata.description}")
print(f"  Capabilities: {metadata.capabilities}")

# Check router
router = demo.get_router()
print(f"\nDemo Router:")
print(f"  Prefix: {router.prefix}")
print(f"  Routes: {len(router.routes)}")

# Check status
status = demo.get_status()
print(f"\nDemo Status:")
for key, value in status.items():
    print(f"  {key}: {value}")

print("\n✅ Demo integration test passed!")
```

Run:
```bash
PYTHONPATH=. python3 test_demo_integration.py
```

## Deliverable

Create: `dev/2025/10/04/phase-3-code-demo-plugin.md`

Include:
1. **Files Created** (5 files):
   - config_service.py (~60 lines)
   - demo_integration_router.py (~120 lines)
   - demo_plugin.py (~130 lines)
   - __init__.py (~10 lines)
   - tests/test_demo_plugin.py (~100 lines)
2. **Test Results**: All tests passing
3. **Integration Test**: Demo plugin loads and works
4. **Code Quality**: Well-commented template code
5. **Total Lines**: ~420 lines of template code

## Success Criteria
- [ ] All 5 demo files created
- [ ] Tests passing (6+ tests)
- [ ] Demo plugin loads successfully
- [ ] Routes accessible
- [ ] Code heavily commented as template
- [ ] Follows patterns from developer guide
- [ ] Ready for developers to copy

---

**Deploy at 1:37 PM**
**Validates developer guide patterns**
