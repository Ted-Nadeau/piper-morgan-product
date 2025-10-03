# Claude Code Agent Prompt: GREAT-3A Phase 3B - Plugin Registry Implementation

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase 3B work.

## Mission
**Implement Plugin Registry**: Create PluginRegistry class to manage plugin lifecycle, registration, and discovery.

## Context

**Phase 3A Complete**: Plugin interface defined and tested (24/24 tests passing)
- PiperPlugin ABC with 6 abstract methods
- PluginMetadata dataclass
- Comprehensive test suite ready

**Phase 3B Goal**: Build registry that manages all plugins
**Why**: Centralized system for plugin registration, initialization, and lifecycle management

## Your Tasks

### Task 1: Create Plugin Registry Class

**File**: `services/plugins/plugin_registry.py`

**Implementation**:
```python
"""
Plugin Registry for Piper Integration Plugins

Manages plugin registration, lifecycle, and discovery.
Singleton pattern ensures global registry instance.
"""

import logging
from typing import Dict, List, Optional
from fastapi import APIRouter

from .plugin_interface import PiperPlugin, PluginMetadata


class PluginRegistry:
    """
    Manages plugin registration, lifecycle, and discovery.

    Singleton registry that all plugins register with at startup.
    Provides plugin lookup, health checks, and lifecycle management.

    Usage:
        registry = get_plugin_registry()
        registry.register(my_plugin)
        await registry.initialize_all()
        routers = registry.get_routers()
    """

    def __init__(self):
        """Initialize empty registry"""
        self._plugins: Dict[str, PiperPlugin] = {}
        self._initialized: bool = False
        self.logger = logging.getLogger(__name__)

    def register(self, plugin: PiperPlugin) -> None:
        """
        Register a plugin with the registry.

        Args:
            plugin: Plugin instance to register

        Raises:
            ValueError: If plugin name already registered
            TypeError: If plugin doesn't implement PiperPlugin
        """
        if not isinstance(plugin, PiperPlugin):
            raise TypeError(f"Plugin must implement PiperPlugin interface")

        metadata = plugin.get_metadata()

        if metadata.name in self._plugins:
            raise ValueError(f"Plugin '{metadata.name}' already registered")

        self._plugins[metadata.name] = plugin
        self.logger.info(
            f"Registered plugin: {metadata.name} v{metadata.version}",
            extra={
                "plugin_name": metadata.name,
                "plugin_version": metadata.version,
                "capabilities": metadata.capabilities
            }
        )

    def unregister(self, plugin_name: str) -> bool:
        """
        Unregister a plugin by name.

        Args:
            plugin_name: Name of plugin to unregister

        Returns:
            bool: True if unregistered, False if not found
        """
        if plugin_name in self._plugins:
            del self._plugins[plugin_name]
            self.logger.info(f"Unregistered plugin: {plugin_name}")
            return True
        return False

    def get_plugin(self, name: str) -> Optional[PiperPlugin]:
        """
        Get plugin by name.

        Args:
            name: Plugin name

        Returns:
            Optional[PiperPlugin]: Plugin instance or None if not found
        """
        return self._plugins.get(name)

    def list_plugins(self) -> List[str]:
        """
        List all registered plugin names.

        Returns:
            List[str]: List of plugin names
        """
        return list(self._plugins.keys())

    def get_all_plugins(self) -> Dict[str, PiperPlugin]:
        """
        Get all registered plugins.

        Returns:
            Dict[str, PiperPlugin]: Copy of plugins dictionary
        """
        return self._plugins.copy()

    def get_plugin_count(self) -> int:
        """
        Get count of registered plugins.

        Returns:
            int: Number of registered plugins
        """
        return len(self._plugins)

    async def initialize_all(self) -> Dict[str, bool]:
        """
        Initialize all registered plugins.

        Calls initialize() on each plugin. Continues even if some fail.

        Returns:
            Dict[str, bool]: Map of plugin name to success status
        """
        results = {}

        for name, plugin in self._plugins.items():
            try:
                await plugin.initialize()
                self.logger.info(f"Initialized plugin: {name}")
                results[name] = True
            except Exception as e:
                self.logger.error(
                    f"Failed to initialize plugin: {name}",
                    extra={"error": str(e), "plugin_name": name}
                )
                results[name] = False

        self._initialized = True
        return results

    async def shutdown_all(self) -> Dict[str, bool]:
        """
        Shutdown all registered plugins.

        Calls shutdown() on each plugin. Continues even if some fail.

        Returns:
            Dict[str, bool]: Map of plugin name to success status
        """
        results = {}

        for name, plugin in self._plugins.items():
            try:
                await plugin.shutdown()
                self.logger.info(f"Shutdown plugin: {name}")
                results[name] = True
            except Exception as e:
                self.logger.error(
                    f"Failed to shutdown plugin: {name}",
                    extra={"error": str(e), "plugin_name": name}
                )
                results[name] = False

        self._initialized = False
        return results

    def get_routers(self) -> List[APIRouter]:
        """
        Get all plugin routers for mounting.

        Returns:
            List[APIRouter]: List of routers from plugins that provide them
        """
        routers = []

        for name, plugin in self._plugins.items():
            try:
                router = plugin.get_router()
                if router is not None:
                    routers.append(router)
                    self.logger.debug(f"Added router from plugin: {name}")
            except Exception as e:
                self.logger.error(
                    f"Failed to get router from plugin: {name}",
                    extra={"error": str(e), "plugin_name": name}
                )

        return routers

    def get_status_all(self) -> Dict[str, Dict]:
        """
        Get status of all plugins.

        Returns:
            Dict[str, Dict]: Map of plugin name to status dict
        """
        status = {}

        for name, plugin in self._plugins.items():
            try:
                plugin_status = plugin.get_status()
                status[name] = plugin_status
            except Exception as e:
                status[name] = {
                    "error": str(e),
                    "status": "error"
                }

        return status

    def get_plugins_with_capability(self, capability: str) -> List[PiperPlugin]:
        """
        Get all plugins with a specific capability.

        Args:
            capability: Capability to filter by (e.g., "routes", "webhooks")

        Returns:
            List[PiperPlugin]: Plugins with the specified capability
        """
        plugins = []

        for plugin in self._plugins.values():
            metadata = plugin.get_metadata()
            if capability in metadata.capabilities:
                plugins.append(plugin)

        return plugins

    def is_initialized(self) -> bool:
        """
        Check if registry has been initialized.

        Returns:
            bool: True if initialize_all() has been called
        """
        return self._initialized


# Global registry instance (singleton)
_registry: Optional[PluginRegistry] = None


def get_plugin_registry() -> PluginRegistry:
    """
    Get the global plugin registry (singleton).

    Returns:
        PluginRegistry: Global registry instance
    """
    global _registry
    if _registry is None:
        _registry = PluginRegistry()
    return _registry


def reset_plugin_registry() -> None:
    """
    Reset the global plugin registry.

    Used primarily for testing. Creates a fresh registry instance.
    """
    global _registry
    _registry = PluginRegistry()
```

### Task 2: Update Package __init__.py

**File**: `services/plugins/__init__.py`

**Add exports**:
```python
"""
Plugin System for Piper Integration Plugins

Provides the plugin interface and registry for managing
integration plugins (Slack, Notion, GitHub, Calendar, etc.)
"""

from .plugin_interface import PiperPlugin, PluginMetadata
from .plugin_registry import PluginRegistry, get_plugin_registry, reset_plugin_registry

__all__ = [
    "PiperPlugin",
    "PluginMetadata",
    "PluginRegistry",
    "get_plugin_registry",
    "reset_plugin_registry",
]
```

### Task 3: Integrate with web/app.py Startup

**File**: `web/app.py`

**Find the lifespan function** and add plugin initialization:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan with plugin management"""

    # ... existing initialization (orchestration engine, services, etc.) ...

    # Phase 3B: Plugin system initialization
    print("\n🔌 Phase 3B: Initializing Plugin System...")

    try:
        from services.plugins import get_plugin_registry

        registry = get_plugin_registry()

        # Plugins auto-register when their modules are imported
        # Phase 3C will add plugin imports here

        # Initialize all registered plugins
        init_results = await registry.initialize_all()

        success_count = sum(1 for success in init_results.values() if success)
        total_count = len(init_results)

        print(f"✅ Plugin initialization: {success_count}/{total_count} successful")

        # Mount plugin routers
        routers = registry.get_routers()
        for router in routers:
            app.include_router(router)

        print(f"✅ Mounted {len(routers)} plugin router(s)")

        # Store registry in app state for access
        app.state.plugin_registry = registry

        print(f"✅ Plugin system initialized: {total_count} plugin(s) registered\n")

    except Exception as e:
        print(f"⚠️ Plugin system initialization failed: {e}")
        print("   Continuing without plugin system\n")
        # Don't fail startup if plugin system has issues
        app.state.plugin_registry = None

    yield

    # Shutdown: cleanup plugins
    print("\n🔌 Shutting down Plugin System...")

    if hasattr(app.state, 'plugin_registry') and app.state.plugin_registry:
        try:
            shutdown_results = await app.state.plugin_registry.shutdown_all()
            success_count = sum(1 for success in shutdown_results.values() if success)
            print(f"✅ Plugin shutdown: {success_count}/{len(shutdown_results)} successful")
        except Exception as e:
            print(f"⚠️ Plugin shutdown error: {e}")

    print("🛑 Plugin system shutdown complete\n")
```

### Task 4: Test Registry Operations

```bash
# Test 1: Import registry
python -c "from services.plugins import get_plugin_registry; print('✅ Import OK')"

# Test 2: Create registry
python -c "from services.plugins import get_plugin_registry; r = get_plugin_registry(); print('✅ Registry created')"

# Test 3: Singleton pattern
python -c "from services.plugins import get_plugin_registry; r1 = get_plugin_registry(); r2 = get_plugin_registry(); print('✅ Singleton:', r1 is r2)"

# Test 4: Registry methods
python -c "
from services.plugins import get_plugin_registry
r = get_plugin_registry()
print('Plugins:', r.list_plugins())
print('Count:', r.get_plugin_count())
print('✅ Registry methods work')
"

# Test 5: App startup (syntax check)
python -m py_compile web/app.py && echo "✅ App syntax OK"
```

### Task 5: Create Registry Tests

**File**: `tests/plugins/test_plugin_registry.py`

```python
"""
Plugin Registry Tests

Tests for PluginRegistry lifecycle and operations.
"""

import pytest
from services.plugins import (
    PiperPlugin,
    PluginMetadata,
    PluginRegistry,
    get_plugin_registry,
    reset_plugin_registry
)
from fastapi import APIRouter
from typing import Optional, Dict, Any


@pytest.fixture
def fresh_registry():
    """Create fresh registry for each test"""
    reset_plugin_registry()
    return get_plugin_registry()


@pytest.fixture
def sample_plugin():
    """Sample plugin for testing"""
    class SamplePlugin(PiperPlugin):
        def get_metadata(self):
            return PluginMetadata(
                name="sample",
                version="1.0.0",
                description="Sample plugin",
                author="Test",
                capabilities=["routes"],
                dependencies=[]
            )

        def get_router(self):
            return None

        def is_configured(self):
            return True

        async def initialize(self):
            pass

        async def shutdown(self):
            pass

        def get_status(self):
            return {"status": "ok"}

    return SamplePlugin()


class TestPluginRegistry:
    """Tests for PluginRegistry class"""

    def test_registry_creation(self, fresh_registry):
        """Test registry can be created"""
        assert fresh_registry is not None
        assert fresh_registry.get_plugin_count() == 0

    def test_singleton_pattern(self):
        """Test registry is singleton"""
        r1 = get_plugin_registry()
        r2 = get_plugin_registry()
        assert r1 is r2

    def test_register_plugin(self, fresh_registry, sample_plugin):
        """Test plugin registration"""
        fresh_registry.register(sample_plugin)
        assert fresh_registry.get_plugin_count() == 1
        assert "sample" in fresh_registry.list_plugins()

    def test_register_duplicate_fails(self, fresh_registry, sample_plugin):
        """Test duplicate registration fails"""
        fresh_registry.register(sample_plugin)
        with pytest.raises(ValueError, match="already registered"):
            fresh_registry.register(sample_plugin)

    def test_get_plugin(self, fresh_registry, sample_plugin):
        """Test getting plugin by name"""
        fresh_registry.register(sample_plugin)
        plugin = fresh_registry.get_plugin("sample")
        assert plugin is sample_plugin

    def test_get_nonexistent_plugin(self, fresh_registry):
        """Test getting nonexistent plugin returns None"""
        plugin = fresh_registry.get_plugin("nonexistent")
        assert plugin is None

    def test_unregister_plugin(self, fresh_registry, sample_plugin):
        """Test plugin unregistration"""
        fresh_registry.register(sample_plugin)
        result = fresh_registry.unregister("sample")
        assert result is True
        assert fresh_registry.get_plugin_count() == 0

    @pytest.mark.asyncio
    async def test_initialize_all(self, fresh_registry, sample_plugin):
        """Test initializing all plugins"""
        fresh_registry.register(sample_plugin)
        results = await fresh_registry.initialize_all()
        assert results["sample"] is True
        assert fresh_registry.is_initialized()

    @pytest.mark.asyncio
    async def test_shutdown_all(self, fresh_registry, sample_plugin):
        """Test shutting down all plugins"""
        fresh_registry.register(sample_plugin)
        await fresh_registry.initialize_all()
        results = await fresh_registry.shutdown_all()
        assert results["sample"] is True
        assert not fresh_registry.is_initialized()

    def test_get_status_all(self, fresh_registry, sample_plugin):
        """Test getting status of all plugins"""
        fresh_registry.register(sample_plugin)
        status = fresh_registry.get_status_all()
        assert "sample" in status
        assert status["sample"]["status"] == "ok"
```

### Task 6: Verify Line Counts

```bash
# Count lines in registry
wc -l services/plugins/plugin_registry.py

# Expected: ~300-350 lines

# Count total plugin system
wc -l services/plugins/*.py

# Expected: ~600-700 lines total
```

## Deliverable

Create: `dev/2025/10/02/phase-3b-code-plugin-registry.md`

Include:
1. **Registry Implementation**: Complete PluginRegistry class
2. **Startup Integration**: web/app.py lifespan updates
3. **Singleton Pattern**: Global registry access
4. **Test Results**: All registry tests passing
5. **Line Counts**: Implementation metrics

## Critical Requirements

- **DO implement** full lifecycle management (init, shutdown)
- **DO use** singleton pattern for global registry
- **DO integrate** with FastAPI startup/shutdown
- **DO handle** errors gracefully (don't fail startup)
- **DO provide** status reporting for all plugins
- **DON'T create** any plugin implementations yet (Phase 3C)

## Time Estimate
60 minutes (1 mango)

## Success Criteria
- [ ] PluginRegistry class created (~300 lines)
- [ ] Singleton pattern working
- [ ] Startup integration in web/app.py
- [ ] Plugin lifecycle managed (init/shutdown)
- [ ] Router mounting working
- [ ] Status reporting working
- [ ] All test commands pass
- [ ] Registry tests created and passing

---

**Deploy at 5:50 PM**
**Foundation for plugin wrapping in Phase 3C**
