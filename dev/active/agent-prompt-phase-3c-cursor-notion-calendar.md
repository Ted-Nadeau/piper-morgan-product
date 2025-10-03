# Cursor Agent Prompt: GREAT-3A Phase 3C - Plugin Wrappers (Notion & Calendar)

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase 3C work.

## Mission
**Create Plugin Wrappers**: Wrap Notion and Calendar integrations as PiperPlugin implementations with auto-registration.

## Context

**Phase 3A Complete**: Plugin interface defined and tested
**Phase 3B Complete**: PluginRegistry implemented and integrated
**Phase 3C Goal**: Wrap existing integrations as plugins (you: Notion + Calendar)

**Current Integration Structure**:
- Notion: `services/integrations/notion/` with NotionIntegrationRouter + NotionConfigService
- Calendar: `services/integrations/calendar/` with CalendarIntegrationRouter + CalendarConfigService

## Your Tasks

### Task 1: Analyze Existing Integration Structure

```bash
cd ~/Development/piper-morgan

# Check Notion structure
ls -la services/integrations/notion/
cat services/integrations/notion/notion_integration_router.py | head -50

# Check Calendar structure
ls -la services/integrations/calendar/
cat services/integrations/calendar/calendar_integration_router.py | head -50

# Note what each integration has:
# - Router class
# - Config service
# - MCP adapters (if any)
```

**Document**:
- What does NotionIntegrationRouter provide?
- What does CalendarIntegrationRouter provide?
- How do they currently get used?
- What needs to be exposed via plugin interface?

### Task 2: Create Notion Plugin Wrapper

**File**: `services/integrations/notion/notion_plugin.py`

**Implementation Pattern**:
```python
"""
Notion Integration Plugin

Wraps Notion integration as a PiperPlugin for auto-registration
with the plugin system.
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter

from services.plugins import PiperPlugin, PluginMetadata
from .notion_integration_router import NotionIntegrationRouter
from .config_service import NotionConfigService


class NotionPlugin(PiperPlugin):
    """
    Notion workspace integration plugin.

    Provides Notion integration routes and MCP capabilities through
    the plugin system.
    """

    def __init__(self):
        """Initialize Notion plugin with config service"""
        self.config_service = NotionConfigService()
        self.integration_router = NotionIntegrationRouter(self.config_service)
        self._api_router: Optional[APIRouter] = None

    def get_metadata(self) -> PluginMetadata:
        """Return Notion plugin metadata"""
        return PluginMetadata(
            name="notion",
            version="1.0.0",
            description="Notion workspace integration with MCP",
            author="Piper Morgan Team",
            capabilities=["routes", "mcp"],  # Notion uses MCP
            dependencies=[]
        )

    def get_router(self) -> Optional[APIRouter]:
        """
        Return FastAPI router with Notion routes.

        Creates APIRouter wrapper around NotionIntegrationRouter
        for plugin system compatibility.
        """
        if self._api_router is None:
            self._api_router = APIRouter(
                prefix="/api/v1/integrations/notion",
                tags=["notion"]
            )

            # Simple status endpoint for plugin
            @self._api_router.get("/status")
            async def notion_status():
                """Get Notion integration status"""
                return {
                    "configured": self.is_configured(),
                    "spatial_enabled": self.integration_router.use_spatial,
                    "legacy_allowed": self.integration_router.allow_legacy
                }

        return self._api_router

    def is_configured(self) -> bool:
        """Check if Notion is properly configured"""
        return self.config_service.is_configured()

    async def initialize(self) -> None:
        """
        Initialize Notion plugin.

        Performs any startup initialization needed for Notion integration.
        """
        if self.is_configured():
            print(f"  ✅ Notion plugin initialized (spatial: {self.integration_router.use_spatial})")
        else:
            print(f"  ⚠️  Notion plugin initialized but not configured")

    async def shutdown(self) -> None:
        """
        Cleanup Notion plugin resources.

        Performs any cleanup needed when shutting down.
        """
        # Any cleanup needed
        pass

    def get_status(self) -> Dict[str, Any]:
        """
        Get Notion plugin status.

        Returns detailed status information for monitoring.
        """
        return {
            "configured": self.is_configured(),
            "config_service": "active",
            "router": "active" if self._api_router else "inactive",
            "spatial_enabled": self.integration_router.use_spatial,
            "legacy_allowed": self.integration_router.allow_legacy,
            "integration_router": "active"
        }


# Auto-register plugin when module is imported
from services.plugins import get_plugin_registry

_notion_plugin = NotionPlugin()
get_plugin_registry().register(_notion_plugin)
```

### Task 3: Create Calendar Plugin Wrapper

**File**: `services/integrations/calendar/calendar_plugin.py`

**Follow same pattern as Notion**:
```python
"""
Calendar Integration Plugin

Wraps Calendar integration as a PiperPlugin for auto-registration
with the plugin system.
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter

from services.plugins import PiperPlugin, PluginMetadata
from .calendar_integration_router import CalendarIntegrationRouter
from .config_service import CalendarConfigService


class CalendarPlugin(PiperPlugin):
    """
    Google Calendar integration plugin.

    Provides Calendar integration routes and spatial intelligence
    through the plugin system.
    """

    def __init__(self):
        """Initialize Calendar plugin with config service"""
        self.config_service = CalendarConfigService()
        self.integration_router = CalendarIntegrationRouter(self.config_service)
        self._api_router: Optional[APIRouter] = None

    def get_metadata(self) -> PluginMetadata:
        """Return Calendar plugin metadata"""
        return PluginMetadata(
            name="calendar",
            version="1.0.0",
            description="Google Calendar integration with spatial intelligence",
            author="Piper Morgan Team",
            capabilities=["routes", "spatial"],  # Calendar has spatial
            dependencies=[]
        )

    def get_router(self) -> Optional[APIRouter]:
        """
        Return FastAPI router with Calendar routes.

        Creates APIRouter wrapper around CalendarIntegrationRouter.
        """
        if self._api_router is None:
            self._api_router = APIRouter(
                prefix="/api/v1/integrations/calendar",
                tags=["calendar"]
            )

            @self._api_router.get("/status")
            async def calendar_status():
                """Get Calendar integration status"""
                return {
                    "configured": self.is_configured(),
                    "spatial_enabled": self.integration_router.use_spatial,
                    "legacy_allowed": self.integration_router.allow_legacy
                }

        return self._api_router

    def is_configured(self) -> bool:
        """Check if Calendar is properly configured"""
        return self.config_service.is_configured()

    async def initialize(self) -> None:
        """Initialize Calendar plugin"""
        if self.is_configured():
            print(f"  ✅ Calendar plugin initialized (spatial: {self.integration_router.use_spatial})")
        else:
            print(f"  ⚠️  Calendar plugin initialized but not configured")

    async def shutdown(self) -> None:
        """Cleanup Calendar plugin resources"""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get Calendar plugin status"""
        return {
            "configured": self.is_configured(),
            "config_service": "active",
            "router": "active" if self._api_router else "inactive",
            "spatial_enabled": self.integration_router.use_spatial,
            "legacy_allowed": self.integration_router.allow_legacy,
            "integration_router": "active"
        }


# Auto-register plugin when module is imported
from services.plugins import get_plugin_registry

_calendar_plugin = CalendarPlugin()
get_plugin_registry().register(_calendar_plugin)
```

### Task 4: Update web/app.py to Import Plugins

**File**: `web/app.py`

**Find where Code added Slack/GitHub imports** and add yours:

```python
# Phase 3C: Import plugins (triggers auto-registration)
print("  📦 Loading plugins...")
from services.integrations.slack.slack_plugin import _slack_plugin
from services.integrations.github.github_plugin import _github_plugin
from services.integrations.notion.notion_plugin import _notion_plugin
from services.integrations.calendar.calendar_plugin import _calendar_plugin
```

### Task 5: Test Plugin Registration

```bash
# Test 1: Plugin imports
python -c "from services.integrations.notion.notion_plugin import _notion_plugin; print('✅ Notion plugin imports')"

python -c "from services.integrations.calendar.calendar_plugin import _calendar_plugin; print('✅ Calendar plugin imports')"

# Test 2: Plugins auto-register
python -c "
from services.plugins import get_plugin_registry, reset_plugin_registry
reset_plugin_registry()

from services.integrations.notion.notion_plugin import _notion_plugin
from services.integrations.calendar.calendar_plugin import _calendar_plugin

registry = get_plugin_registry()
print('Registered plugins:', registry.list_plugins())
print('Count:', registry.get_plugin_count())
assert 'notion' in registry.list_plugins()
assert 'calendar' in registry.list_plugins()
print('✅ Auto-registration works')
"

# Test 3: Plugin interface validation
python -c "
from services.integrations.notion.notion_plugin import _notion_plugin
from tests.plugins.test_plugin_interface import validate_plugin_interface

validate_plugin_interface(_notion_plugin)
print('✅ Notion plugin validates')
"

python -c "
from services.integrations.calendar.calendar_plugin import _calendar_plugin
from tests.plugins.test_plugin_interface import validate_plugin_interface

validate_plugin_interface(_calendar_plugin)
print('✅ Calendar plugin validates')
"

# Test 4: All 4 plugins together
python -c "
from services.plugins import get_plugin_registry, reset_plugin_registry
reset_plugin_registry()

from services.integrations.slack.slack_plugin import _slack_plugin
from services.integrations.github.github_plugin import _github_plugin
from services.integrations.notion.notion_plugin import _notion_plugin
from services.integrations.calendar.calendar_plugin import _calendar_plugin

registry = get_plugin_registry()
plugins = registry.list_plugins()
print('All plugins registered:', plugins)
print('Count:', registry.get_plugin_count())
assert len(plugins) == 4
print('✅ All 4 plugins working together')
"
```

### Task 6: Test Full Integration

```bash
# Test app startup with all plugins
python -c "
import sys
sys.path.insert(0, '.')
from web.app import app
print('✅ App loads with all plugins')
"

# Syntax check
python -m py_compile web/app.py && echo "✅ App syntax OK"
```

### Task 7: Verify Line Counts

```bash
# Count plugin wrappers
wc -l services/integrations/notion/notion_plugin.py
wc -l services/integrations/calendar/calendar_plugin.py

# Expected: ~80-100 lines each
```

## Deliverable

Create: `dev/2025/10/02/phase-3c-cursor-notion-calendar-plugins.md`

Include:
1. **Notion Plugin**: Complete implementation
2. **Calendar Plugin**: Complete implementation
3. **Integration Analysis**: How plugins wrap existing routers
4. **Test Results**: All validation tests passing
5. **Auto-Registration**: Proof plugins register on import
6. **All 4 Plugins**: Testing all plugins together

## Critical Requirements

- **DO wrap** existing integration routers (don't rewrite them)
- **DO auto-register** plugins at module import
- **DO preserve** existing functionality
- **DO implement** all PiperPlugin methods
- **DON'T modify** existing router classes (Phase 3C is wrapper only)
- **DON'T break** existing integration behavior

## Time Estimate
45 minutes (half of Phase 3C, Code does other half)

## Success Criteria
- [ ] NotionPlugin created and working
- [ ] CalendarPlugin created and working
- [ ] Both plugins auto-register on import
- [ ] Both plugins validate against interface
- [ ] Plugins imported in web/app.py
- [ ] All test commands pass
- [ ] All 4 plugins work together
- [ ] Plugin metadata accurate

---

**Deploy at 6:35 PM**
**Coordinate with Code on Slack + GitHub plugins**
