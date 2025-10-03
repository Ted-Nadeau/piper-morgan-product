# GREAT-3A Phase 3 Gameplan: Plugin Architecture Implementation

**Date**: October 2, 2025 - 5:45 PM PT
**Lead Developer**: Claude Sonnet 4.5
**GitHub Issue**: GREAT-3A (Plugin Architecture Foundation)

---

## Executive Summary

**Mission**: Implement plugin architecture foundation to enable integration plugins (Slack, Notion, GitHub, Calendar) to register as self-contained modules.

**Approach**: Define plugin interface, implement registry, enable lifecycle management, create plugin adapter layer for existing integrations.

**Estimated Duration**: ~3 mangos total

---

## Phase 2 Completion Status

**Achieved**: 56% reduction in web/app.py (1,052 → 467 lines)
- ✅ Phase 2A: Template extraction (464 lines)
- ✅ Phase 2B: Intent service extraction (136 lines)
- ✅ Phase 2C: Assessment confirmed optimal state

**Foundation Ready**:
- Template rendering system established
- Service layer with business logic extracted
- Thin route handlers (HTTP adapters only)
- Clear extension points for plugins

---

## Phase 3 Context

### What We're Building

**Plugin System Goals**:
1. Integration plugins self-register at startup
2. Each plugin provides routes, config, metadata
3. Plugin registry manages lifecycle
4. Plugins can be enabled/disabled without code changes
5. Clear interface for future plugin development

### Why This Matters

**Current Problem**: Adding new integrations requires:
- Manual route registration in web/app.py
- Manual config service setup in lifespan
- Manual feature flag checking
- Tight coupling to main application

**After Plugin System**: Adding new integrations requires:
- Create plugin class implementing PiperPlugin interface
- Plugin auto-registers at startup
- Plugin manages own routes, config, lifecycle
- Loose coupling via plugin interface

### Success Criteria

**Phase 3 Complete When**:
- ✅ PiperPlugin interface defined
- ✅ PluginRegistry implemented
- ✅ 4 existing integrations wrapped as plugins
- ✅ Plugins auto-register at startup
- ✅ Plugin metadata accessible
- ✅ Plugin lifecycle managed (init, shutdown)
- ✅ No breaking changes to existing functionality

---

## Phase 3A: Plugin Interface Definition

**Duration**: ~30 minutes
**Complexity**: Low (design work)
**Risk**: Low (no existing code changes)

### Objective

Define PiperPlugin abstract base class that all integration plugins must implement.

### Interface Design

**Location**: `services/plugins/plugin_interface.py`

**Core Interface**:
```python
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from fastapi import APIRouter
from dataclasses import dataclass

@dataclass
class PluginMetadata:
    """Metadata about a plugin"""
    name: str
    version: str
    description: str
    author: str
    capabilities: List[str]  # e.g., ["routes", "webhooks", "spatial"]
    dependencies: List[str] = None  # Other plugins required


class PiperPlugin(ABC):
    """
    Abstract base class for Piper integration plugins.

    All integration plugins (Slack, Notion, GitHub, Calendar)
    must implement this interface.
    """

    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata"""
        pass

    @abstractmethod
    def get_router(self) -> Optional[APIRouter]:
        """Return FastAPI router with plugin routes (if any)"""
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """Check if plugin is properly configured"""
        pass

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize plugin (called at startup)"""
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Cleanup plugin (called at shutdown)"""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Return plugin health/status information"""
        pass
```

### Plugin Capabilities

**Capability Types**:
- `routes`: Plugin provides HTTP routes
- `webhooks`: Plugin handles webhook callbacks
- `spatial`: Plugin uses spatial intelligence pattern
- `mcp`: Plugin uses MCP (Model Context Protocol)
- `background`: Plugin runs background tasks

### Design Principles

1. **Minimal Required Methods**: Only essential interface
2. **Flexible Capabilities**: Plugins declare what they provide
3. **Lifecycle Hooks**: Initialize and shutdown for resource management
4. **Health Reporting**: get_status() for monitoring
5. **FastAPI Integration**: get_router() returns standard APIRouter

### Agent Assignment

**Code Agent**:
- Create plugin_interface.py
- Define PiperPlugin ABC
- Define PluginMetadata dataclass
- Document interface with examples
- Create __init__.py for services/plugins/

### Success Criteria

- [ ] services/plugins/ directory created
- [ ] plugin_interface.py with PiperPlugin ABC
- [ ] PluginMetadata dataclass defined
- [ ] Interface documented with docstrings
- [ ] Example plugin skeleton provided

### Deliverable

`dev/2025/10/02/phase-3a-code-plugin-interface.md`

---

## Phase 3B: Plugin Registry Implementation

**Duration**: ~1 mango
**Complexity**: Medium (registry logic)
**Risk**: Medium (integrates with startup)

### Objective

Implement PluginRegistry that manages plugin lifecycle, registration, and discovery.

### Registry Design

**Location**: `services/plugins/plugin_registry.py`

**Core Registry**:
```python
class PluginRegistry:
    """
    Manages plugin registration, lifecycle, and discovery.

    Singleton registry that all plugins register with at startup.
    Provides plugin lookup, health checks, and lifecycle management.
    """

    def __init__(self):
        self._plugins: Dict[str, PiperPlugin] = {}
        self._initialized: bool = False
        self.logger = logging.getLogger(__name__)

    def register(self, plugin: PiperPlugin) -> None:
        """Register a plugin with the registry"""
        metadata = plugin.get_metadata()
        if metadata.name in self._plugins:
            raise ValueError(f"Plugin {metadata.name} already registered")
        self._plugins[metadata.name] = plugin
        self.logger.info(f"Registered plugin: {metadata.name} v{metadata.version}")

    def get_plugin(self, name: str) -> Optional[PiperPlugin]:
        """Get plugin by name"""
        return self._plugins.get(name)

    def list_plugins(self) -> List[str]:
        """List all registered plugin names"""
        return list(self._plugins.keys())

    def get_all_plugins(self) -> Dict[str, PiperPlugin]:
        """Get all registered plugins"""
        return self._plugins.copy()

    async def initialize_all(self) -> None:
        """Initialize all registered plugins"""
        for name, plugin in self._plugins.items():
            try:
                await plugin.initialize()
                self.logger.info(f"Initialized plugin: {name}")
            except Exception as e:
                self.logger.error(f"Failed to initialize {name}: {e}")

    async def shutdown_all(self) -> None:
        """Shutdown all registered plugins"""
        for name, plugin in self._plugins.items():
            try:
                await plugin.shutdown()
                self.logger.info(f"Shutdown plugin: {name}")
            except Exception as e:
                self.logger.error(f"Failed to shutdown {name}: {e}")

    def get_routers(self) -> List[APIRouter]:
        """Get all plugin routers for mounting"""
        routers = []
        for plugin in self._plugins.values():
            router = plugin.get_router()
            if router:
                routers.append(router)
        return routers

    def get_status_all(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all plugins"""
        return {
            name: plugin.get_status()
            for name, plugin in self._plugins.items()
        }

# Global registry instance
_registry = None

def get_plugin_registry() -> PluginRegistry:
    """Get the global plugin registry (singleton)"""
    global _registry
    if _registry is None:
        _registry = PluginRegistry()
    return _registry
```

### Integration with web/app.py

**Startup Integration**:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan with plugin management"""

    # ... existing initialization ...

    # Phase 3B: Plugin system initialization
    from services.plugins.plugin_registry import get_plugin_registry

    registry = get_plugin_registry()

    # Plugins will auto-register in Phase 3C
    # (When plugin modules are imported)

    # Initialize all registered plugins
    await registry.initialize_all()

    # Mount plugin routers
    for router in registry.get_routers():
        app.include_router(router)

    # Store registry in app state
    app.state.plugin_registry = registry

    print(f"✅ Plugin system initialized: {len(registry.list_plugins())} plugins")

    yield

    # Shutdown all plugins
    await registry.shutdown_all()
    print("🛑 Plugin system shutdown complete")
```

### Agent Assignment

**Code Agent**:
- Create plugin_registry.py
- Implement PluginRegistry class
- Implement singleton pattern
- Add integration to web/app.py lifespan
- Test registry operations

### Success Criteria

- [ ] plugin_registry.py created
- [ ] PluginRegistry class implemented
- [ ] Singleton pattern working
- [ ] Startup integration in web/app.py
- [ ] Plugin lifecycle managed
- [ ] Router mounting working

### Deliverable

`dev/2025/10/02/phase-3b-code-plugin-registry.md`

---

## Phase 3C: Integration Plugin Wrappers

**Duration**: ~1.5 mangos
**Complexity**: Medium-High (4 plugins to wrap)
**Risk**: Medium (changes to existing integrations)

### Objective

Wrap 4 existing integrations (Slack, Notion, GitHub, Calendar) as PiperPlugin implementations.

### Plugin Structure

**For Each Integration** (Slack example):

**Location**: `services/integrations/slack/slack_plugin.py`

```python
from services.plugins.plugin_interface import PiperPlugin, PluginMetadata
from fastapi import APIRouter
from typing import Optional, Dict, Any

from .slack_integration_router import SlackIntegrationRouter
from .config_service import SlackConfigService


class SlackPlugin(PiperPlugin):
    """Slack integration plugin"""

    def __init__(self):
        self.config_service = SlackConfigService()
        self.router_instance = SlackIntegrationRouter(self.config_service)
        self._api_router = None

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="slack",
            version="1.0.0",
            description="Slack workspace integration",
            author="Piper Morgan Team",
            capabilities=["routes", "webhooks", "spatial"],
            dependencies=[]
        )

    def get_router(self) -> Optional[APIRouter]:
        """Return FastAPI router with Slack routes"""
        if self._api_router is None:
            self._api_router = APIRouter(
                prefix="/api/v1/integrations/slack",
                tags=["slack"]
            )
            # Add routes from SlackIntegrationRouter
            # (May need to refactor router to work with APIRouter)
        return self._api_router

    def is_configured(self) -> bool:
        """Check if Slack is configured"""
        return self.config_service.is_configured()

    async def initialize(self) -> None:
        """Initialize Slack plugin"""
        # Any startup initialization
        pass

    async def shutdown(self) -> None:
        """Cleanup Slack plugin"""
        # Any cleanup needed
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get Slack plugin status"""
        return {
            "configured": self.is_configured(),
            "config_service": "active",
            "router": "active" if self._api_router else "inactive",
            "spatial_enabled": self.router_instance.use_spatial
        }


# Auto-register plugin at module import
from services.plugins.plugin_registry import get_plugin_registry

_plugin = SlackPlugin()
get_plugin_registry().register(_plugin)
```

### Router Refactoring

**Current Integration Routers** may need updates:
- Currently have route methods on router class
- May need to convert to APIRouter pattern
- Or create adapter that wraps existing router

**Option A** (Minimal Changes):
- Keep existing router as-is
- Plugin creates APIRouter
- Plugin adds routes that delegate to existing router methods

**Option B** (Full Refactor):
- Convert router class methods to APIRouter routes
- More FastAPI-idiomatic
- More work

**Recommendation**: Option A for Phase 3, Option B as future improvement

### Plugin Discovery

**Auto-Registration Pattern**:
```python
# At bottom of each plugin file:
from services.plugins.plugin_registry import get_plugin_registry

_plugin = SlackPlugin()  # Create instance
get_plugin_registry().register(_plugin)  # Auto-register
```

**Import in web/app.py**:
```python
# Force plugin module imports (triggers auto-registration)
from services.integrations.slack.slack_plugin import _plugin as _slack
from services.integrations.notion.notion_plugin import _plugin as _notion
from services.integrations.github.github_plugin import _plugin as _github
from services.integrations.calendar.calendar_plugin import _plugin as _calendar
```

### Agent Assignment

**Both Agents** (split work):

**Code Agent**:
- Create SlackPlugin wrapper
- Create GitHubPlugin wrapper
- Test plugin registration
- Verify lifecycle hooks

**Cursor Agent**:
- Create NotionPlugin wrapper
- Create CalendarPlugin wrapper
- Test plugin registration
- Verify lifecycle hooks

### Success Criteria (Per Plugin)

- [ ] Plugin wrapper class created
- [ ] Implements PiperPlugin interface
- [ ] Auto-registers at import
- [ ] Router integration working
- [ ] Config service integration working
- [ ] Metadata accurate
- [ ] Status reporting working

### Deliverables

- `dev/2025/10/02/phase-3c-code-slack-github-plugins.md`
- `dev/2025/10/02/phase-3c-cursor-notion-calendar-plugins.md`

---

## Phase 3 Summary

### Total Changes

**New Files Created**:
- services/plugins/__init__.py
- services/plugins/plugin_interface.py
- services/plugins/plugin_registry.py
- services/integrations/slack/slack_plugin.py
- services/integrations/notion/notion_plugin.py
- services/integrations/github/github_plugin.py
- services/integrations/calendar/calendar_plugin.py

**Modified Files**:
- web/app.py (plugin system integration in lifespan)

**Estimated Lines**:
- Plugin interface: ~100 lines
- Plugin registry: ~150 lines
- Each plugin wrapper: ~80 lines × 4 = ~320 lines
- Total new code: ~570 lines

### Plugin Architecture Benefits

**Before Phase 3**:
- Manual route registration per integration
- Tight coupling to web/app.py
- No standardized interface
- No centralized management

**After Phase 3**:
- Auto-registration via plugin system
- Loose coupling via PiperPlugin interface
- Standardized lifecycle management
- Centralized plugin registry
- Easy to add new integrations

### Future Extensions

**Phase 3 Enables**:
- Dynamic plugin loading (load plugins from config)
- Plugin marketplace (community plugins)
- Plugin dependencies (plugin A requires plugin B)
- Plugin versioning
- Plugin hot-reload
- Plugin sandboxing

---

## Time Estimates

- Phase 3A: Plugin interface (~30 min)
- Phase 3B: Plugin registry (~60 min)
- Phase 3C: Plugin wrappers (~90 min)
- **Total**: ~3 hours (3 mangos)

### Risk Mitigation

**Incremental Approach**:
1. Phase 3A: Define interface (no integration changes)
2. Phase 3B: Implement registry (minimal integration)
3. Phase 3C: Wrap one plugin at a time
4. Test each plugin individually
5. Verify all plugins together

**Rollback Plan**:
- Each phase self-contained
- Plugin wrappers don't modify existing routers
- Can disable plugin system and use old patterns
- No breaking changes to existing functionality

---

## Success Criteria (Overall)

- [ ] PiperPlugin interface defined
- [ ] PluginRegistry implemented and tested
- [ ] All 4 integrations wrapped as plugins
- [ ] Plugins auto-register at startup
- [ ] Plugin routers mounted correctly
- [ ] Plugin lifecycle managed (init/shutdown)
- [ ] Plugin status reporting working
- [ ] No breaking changes to existing functionality
- [ ] All existing routes still work
- [ ] All existing features preserved

---

## Next Steps

**Immediate**: Execute Phase 3A (plugin interface definition)
**Then**: Execute Phase 3B (plugin registry)
**Finally**: Execute Phase 3C (plugin wrappers)
**After Phase 3**: Test plugin system end-to-end

---

**Gameplan Status**: Ready for Execution
**Time**: 5:45 PM PT
**Estimated Completion**: ~8:45 PM PT (3 hours from start)

---

**End of Gameplan**
