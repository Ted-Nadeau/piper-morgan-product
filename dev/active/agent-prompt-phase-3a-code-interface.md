# Claude Code Agent Prompt: GREAT-3A Phase 3A - Plugin Interface Definition

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase 3A work.

## Mission
**Define Plugin Interface**: Create PiperPlugin abstract base class and supporting types for plugin architecture.

## Context

**Phase 2 Complete**: web/app.py refactored (1,052 → 467 lines)
- Templates extracted
- Intent service extracted
- Routes simplified to thin adapters

**Phase 3 Goal**: Implement plugin architecture so integrations self-register
**Phase 3A**: Define the interface all plugins must implement

## Your Tasks

### Task 1: Create Plugin Package Structure

```bash
cd ~/Development/piper-morgan

# Create directory
mkdir -p services/plugins

# Create files
touch services/plugins/__init__.py
touch services/plugins/plugin_interface.py

# Verify
ls -la services/plugins/
```

### Task 2: Define PluginMetadata Dataclass

**File**: `services/plugins/plugin_interface.py`

**Implementation**:
```python
"""
Plugin Interface for Piper Integration Plugins

Defines the abstract base class and types that all integration plugins
must implement to participate in the plugin architecture.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from fastapi import APIRouter


@dataclass
class PluginMetadata:
    """
    Metadata about a plugin.

    Provides information about plugin identity, version, capabilities,
    and dependencies.
    """

    # Identity
    name: str  # Unique plugin identifier (e.g., "slack", "notion")
    version: str  # Semantic version (e.g., "1.0.0")
    description: str  # Human-readable description
    author: str  # Plugin author/maintainer

    # Capabilities
    capabilities: List[str] = field(default_factory=list)
    # Supported capability types:
    # - "routes": Plugin provides HTTP routes
    # - "webhooks": Plugin handles webhook callbacks
    # - "spatial": Plugin uses spatial intelligence
    # - "mcp": Plugin uses Model Context Protocol
    # - "background": Plugin runs background tasks

    # Dependencies
    dependencies: List[str] = field(default_factory=list)
    # Other plugins this plugin requires (by name)
```

### Task 3: Define PiperPlugin Abstract Base Class

**Same file**, continue:

```python
class PiperPlugin(ABC):
    """
    Abstract base class for Piper integration plugins.

    All integration plugins (Slack, Notion, GitHub, Calendar) must
    implement this interface. The plugin system uses this interface
    to manage plugin lifecycle, routes, and status.

    Minimal Required Methods:
    - get_metadata(): Plugin identity and capabilities
    - get_router(): FastAPI routes (if any)
    - is_configured(): Configuration validation
    - initialize(): Startup initialization
    - shutdown(): Cleanup and resource release
    - get_status(): Health and status reporting

    Example Plugin:
    ```python
    class MyPlugin(PiperPlugin):
        def get_metadata(self) -> PluginMetadata:
            return PluginMetadata(
                name="my_plugin",
                version="1.0.0",
                description="My integration plugin",
                author="Developer Name",
                capabilities=["routes"],
                dependencies=[]
            )

        def get_router(self) -> Optional[APIRouter]:
            router = APIRouter(prefix="/api/v1/my-plugin")

            @router.get("/status")
            async def status():
                return {"status": "active"}

            return router

        def is_configured(self) -> bool:
            return True  # Check actual configuration

        async def initialize(self) -> None:
            # Setup resources
            pass

        async def shutdown(self) -> None:
            # Cleanup resources
            pass

        def get_status(self) -> Dict[str, Any]:
            return {
                "configured": self.is_configured(),
                "active": True
            }
    ```
    """

    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """
        Return plugin metadata.

        Provides information about plugin identity, version,
        capabilities, and dependencies.

        Returns:
            PluginMetadata: Plugin information
        """
        pass

    @abstractmethod
    def get_router(self) -> Optional[APIRouter]:
        """
        Return FastAPI router with plugin routes.

        If the plugin provides HTTP routes, return an APIRouter
        with those routes configured. If the plugin has no routes,
        return None.

        The router will be mounted automatically by the plugin system
        during application startup.

        Returns:
            Optional[APIRouter]: Router with plugin routes, or None
        """
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """
        Check if plugin is properly configured.

        Validates that all required configuration (environment variables,
        credentials, etc.) is present for the plugin to operate.

        Returns:
            bool: True if configured, False otherwise
        """
        pass

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize plugin resources.

        Called during application startup after all plugins are registered.
        Use this to:
        - Initialize connections
        - Allocate resources
        - Start background tasks
        - Validate configuration

        Raises:
            Exception: If initialization fails
        """
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """
        Cleanup plugin resources.

        Called during application shutdown. Use this to:
        - Close connections
        - Release resources
        - Stop background tasks
        - Save state

        Should not raise exceptions.
        """
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        Return plugin health and status information.

        Provides runtime status information for monitoring and debugging.
        Should include:
        - Configuration status
        - Connection status
        - Resource usage
        - Error counts
        - Any plugin-specific metrics

        Returns:
            Dict[str, Any]: Status information
        """
        pass
```

### Task 4: Update Package __init__.py

**File**: `services/plugins/__init__.py`

```python
"""
Plugin System for Piper Integration Plugins

Provides the plugin interface and registry for managing
integration plugins (Slack, Notion, GitHub, Calendar, etc.)
"""

from .plugin_interface import PiperPlugin, PluginMetadata

__all__ = ["PiperPlugin", "PluginMetadata"]
```

### Task 5: Create Example Plugin Documentation

**File**: `services/plugins/PLUGIN_GUIDE.md`

```markdown
# Piper Plugin Development Guide

## Overview

The Piper plugin system allows integrations to self-register as modular
components with standardized interfaces.

## Creating a Plugin

### 1. Implement PiperPlugin Interface

```python
from services.plugins import PiperPlugin, PluginMetadata
from fastapi import APIRouter

class MyPlugin(PiperPlugin):
    def __init__(self):
        # Initialize your plugin
        self.config = load_config()

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="my_plugin",
            version="1.0.0",
            description="My awesome plugin",
            author="Your Name",
            capabilities=["routes"],
            dependencies=[]
        )

    # Implement other required methods...
```

### 2. Auto-Register Plugin

```python
# At bottom of plugin file
from services.plugins.plugin_registry import get_plugin_registry

_plugin = MyPlugin()
get_plugin_registry().register(_plugin)
```

### 3. Plugin Lifecycle

- **Registration**: Plugin auto-registers when module imported
- **Initialization**: `initialize()` called at app startup
- **Operation**: Routes active, status queryable
- **Shutdown**: `shutdown()` called at app shutdown

## Plugin Capabilities

- **routes**: Provides HTTP endpoints
- **webhooks**: Handles webhook callbacks
- **spatial**: Uses spatial intelligence
- **mcp**: Uses Model Context Protocol
- **background**: Runs background tasks

## Best Practices

1. Keep plugins self-contained
2. Use dependency injection for config
3. Handle initialization errors gracefully
4. Provide detailed status information
5. Clean up resources in shutdown()
```

### Task 6: Test Interface Definition

```bash
# Test imports
python -c "from services.plugins import PiperPlugin, PluginMetadata; print('✅ Imports OK')"

# Test interface can be subclassed
python -c "
from services.plugins import PiperPlugin, PluginMetadata
from fastapi import APIRouter
from typing import Optional, Dict, Any

class TestPlugin(PiperPlugin):
    def get_metadata(self):
        return PluginMetadata('test', '1.0', 'Test', 'Test Author', ['routes'])
    def get_router(self):
        return None
    def is_configured(self):
        return True
    async def initialize(self):
        pass
    async def shutdown(self):
        pass
    def get_status(self):
        return {}

p = TestPlugin()
print('✅ Interface can be implemented')
print('Metadata:', p.get_metadata())
"
```

### Task 7: Verify Structure

```bash
# Check all files created
ls -la services/plugins/

# Should see:
# __init__.py
# plugin_interface.py
# PLUGIN_GUIDE.md

# Count lines
wc -l services/plugins/*.py
```

## Deliverable

Create: `dev/2025/10/02/phase-3a-code-plugin-interface.md`

Include:
1. **Interface Design**: PiperPlugin and PluginMetadata
2. **Files Created**: All plugin package files
3. **Documentation**: Plugin development guide
4. **Test Results**: Interface validation tests
5. **Example Plugin**: Skeleton implementation

## Critical Requirements

- **DO define** clear abstract interface
- **DO document** all methods thoroughly
- **DO provide** example plugin skeleton
- **DO use** standard Python ABC patterns
- **DON'T implement** registry yet (that's Phase 3B)
- **DON'T modify** existing integrations yet (that's Phase 3C)

## Time Estimate
30 minutes

## Success Criteria
- [ ] services/plugins/ directory created
- [ ] PiperPlugin ABC defined
- [ ] PluginMetadata dataclass defined
- [ ] All methods documented with docstrings
- [ ] Package __init__.py exports interface
- [ ] Plugin guide created
- [ ] Test imports pass
- [ ] Example plugin validates interface

---

**Deploy at 5:30 PM**
**Foundation for plugin architecture**
