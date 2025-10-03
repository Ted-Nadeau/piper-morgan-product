# Claude Code Agent Prompt: GREAT-3A Phase 3C - Plugin Wrappers (Slack & GitHub)

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase 3C work.

## Mission
**Create Plugin Wrappers**: Wrap Slack and GitHub integrations as PiperPlugin implementations with auto-registration.

## Context

**Phase 3A Complete**: Plugin interface defined and tested
**Phase 3B Complete**: PluginRegistry implemented and integrated
**Phase 3C Goal**: Wrap existing integrations as plugins (you: Slack + GitHub)

**Current Integration Structure**:
- Slack: `services/integrations/slack/` with SlackIntegrationRouter + SlackConfigService
- GitHub: `services/integrations/github/` with GitHubIntegrationRouter + GitHubConfigService

## Your Tasks

### Task 1: Analyze Existing Integration Structure

```bash
cd ~/Development/piper-morgan

# Check Slack structure
ls -la services/integrations/slack/
cat services/integrations/slack/slack_integration_router.py | head -50

# Check GitHub structure
ls -la services/integrations/github/
cat services/integrations/github/github_integration_router.py | head -50

# Note what each integration has:
# - Router class
# - Config service
# - Spatial/MCP adapters (if any)
```

**Document**:
- What does SlackIntegrationRouter provide?
- What does GitHubIntegrationRouter provide?
- How do they currently get used?
- What needs to be exposed via plugin interface?

### Task 2: Create Slack Plugin Wrapper

**File**: `services/integrations/slack/slack_plugin.py`

**Implementation Pattern**:
```python
"""
Slack Integration Plugin

Wraps Slack integration as a PiperPlugin for auto-registration
with the plugin system.
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter

from services.plugins import PiperPlugin, PluginMetadata
from .slack_integration_router import SlackIntegrationRouter
from .config_service import SlackConfigService


class SlackPlugin(PiperPlugin):
    """
    Slack workspace integration plugin.

    Provides Slack integration routes, webhooks, and spatial intelligence
    capabilities through the plugin system.
    """

    def __init__(self):
        """Initialize Slack plugin with config service"""
        self.config_service = SlackConfigService()
        self.integration_router = SlackIntegrationRouter(self.config_service)
        self._api_router: Optional[APIRouter] = None

    def get_metadata(self) -> PluginMetadata:
        """Return Slack plugin metadata"""
        return PluginMetadata(
            name="slack",
            version="1.0.0",
            description="Slack workspace integration with spatial intelligence",
            author="Piper Morgan Team",
            capabilities=["routes", "webhooks", "spatial"],
            dependencies=[]
        )

    def get_router(self) -> Optional[APIRouter]:
        """
        Return FastAPI router with Slack routes.

        Creates APIRouter wrapper around SlackIntegrationRouter
        for plugin system compatibility.
        """
        if self._api_router is None:
            self._api_router = APIRouter(
                prefix="/api/v1/integrations/slack",
                tags=["slack"]
            )

            # Delegate to existing router methods
            # Note: May need to adapt router methods to work with APIRouter
            # For now, create simple wrapper routes

            @self._api_router.get("/status")
            async def slack_status():
                """Get Slack integration status"""
                return {
                    "configured": self.is_configured(),
                    "spatial_enabled": self.integration_router.use_spatial,
                    "legacy_allowed": self.integration_router.allow_legacy
                }

        return self._api_router

    def is_configured(self) -> bool:
        """Check if Slack is properly configured"""
        return self.config_service.is_configured()

    async def initialize(self) -> None:
        """
        Initialize Slack plugin.

        Performs any startup initialization needed for Slack integration.
        """
        # Log initialization
        if self.is_configured():
            print(f"  ✅ Slack plugin initialized (spatial: {self.integration_router.use_spatial})")
        else:
            print(f"  ⚠️  Slack plugin initialized but not configured")

    async def shutdown(self) -> None:
        """
        Cleanup Slack plugin resources.

        Performs any cleanup needed when shutting down.
        """
        # Any cleanup needed
        pass

    def get_status(self) -> Dict[str, Any]:
        """
        Get Slack plugin status.

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

_slack_plugin = SlackPlugin()
get_plugin_registry().register(_slack_plugin)
```

### Task 3: Create GitHub Plugin Wrapper

**File**: `services/integrations/github/github_plugin.py`

**Follow same pattern as Slack**:
```python
"""
GitHub Integration Plugin

Wraps GitHub integration as a PiperPlugin for auto-registration
with the plugin system.
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter

from services.plugins import PiperPlugin, PluginMetadata
from .github_integration_router import GitHubIntegrationRouter
from .config_service import GitHubConfigService


class GitHubPlugin(PiperPlugin):
    """
    GitHub repository integration plugin.

    Provides GitHub integration routes and capabilities through
    the plugin system.
    """

    def __init__(self):
        """Initialize GitHub plugin with config service"""
        self.config_service = GitHubConfigService()
        self.integration_router = GitHubIntegrationRouter(self.config_service)
        self._api_router: Optional[APIRouter] = None

    def get_metadata(self) -> PluginMetadata:
        """Return GitHub plugin metadata"""
        return PluginMetadata(
            name="github",
            version="1.0.0",
            description="GitHub repository integration",
            author="Piper Morgan Team",
            capabilities=["routes"],  # GitHub doesn't have spatial/webhooks yet
            dependencies=[]
        )

    def get_router(self) -> Optional[APIRouter]:
        """
        Return FastAPI router with GitHub routes.

        Creates APIRouter wrapper around GitHubIntegrationRouter.
        """
        if self._api_router is None:
            self._api_router = APIRouter(
                prefix="/api/v1/integrations/github",
                tags=["github"]
            )

            @self._api_router.get("/status")
            async def github_status():
                """Get GitHub integration status"""
                return {
                    "configured": self.is_configured(),
                    "spatial_enabled": self.integration_router.use_spatial,
                    "legacy_allowed": self.integration_router.allow_legacy
                }

        return self._api_router

    def is_configured(self) -> bool:
        """Check if GitHub is properly configured"""
        return self.config_service.is_configured()

    async def initialize(self) -> None:
        """Initialize GitHub plugin"""
        if self.is_configured():
            print(f"  ✅ GitHub plugin initialized (spatial: {self.integration_router.use_spatial})")
        else:
            print(f"  ⚠️  GitHub plugin initialized but not configured")

    async def shutdown(self) -> None:
        """Cleanup GitHub plugin resources"""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get GitHub plugin status"""
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

_github_plugin = GitHubPlugin()
get_plugin_registry().register(_github_plugin)
```

### Task 4: Update web/app.py to Import Plugins

**File**: `web/app.py`

**Find the Phase 3B plugin initialization section** and add imports:

```python
# Phase 3B: Plugin system initialization
print("\n🔌 Phase 3B: Initializing Plugin System...")

try:
    from services.plugins import get_plugin_registry

    # Phase 3C: Import plugins (triggers auto-registration)
    print("  📦 Loading plugins...")
    from services.integrations.slack.slack_plugin import _slack_plugin
    from services.integrations.github.github_plugin import _github_plugin
    # Cursor will add Notion and Calendar

    registry = get_plugin_registry()

    # ... rest of Phase 3B code ...
```

### Task 5: Test Plugin Registration

```bash
# Test 1: Plugin imports
python -c "from services.integrations.slack.slack_plugin import _slack_plugin; print('✅ Slack plugin imports')"

python -c "from services.integrations.github.github_plugin import _github_plugin; print('✅ GitHub plugin imports')"

# Test 2: Plugins auto-register
python -c "
from services.plugins import get_plugin_registry, reset_plugin_registry
reset_plugin_registry()

from services.integrations.slack.slack_plugin import _slack_plugin
from services.integrations.github.github_plugin import _github_plugin

registry = get_plugin_registry()
print('Registered plugins:', registry.list_plugins())
print('Count:', registry.get_plugin_count())
assert 'slack' in registry.list_plugins()
assert 'github' in registry.list_plugins()
print('✅ Auto-registration works')
"

# Test 3: Plugin interface validation
python -c "
from services.integrations.slack.slack_plugin import _slack_plugin
from tests.plugins.test_plugin_interface import validate_plugin_interface

validate_plugin_interface(_slack_plugin)
print('✅ Slack plugin validates')
"

python -c "
from services.integrations.github.github_plugin import _github_plugin
from tests.plugins.test_plugin_interface import validate_plugin_interface

validate_plugin_interface(_github_plugin)
print('✅ GitHub plugin validates')
"

# Test 4: Plugin metadata
python -c "
from services.integrations.slack.slack_plugin import _slack_plugin
metadata = _slack_plugin.get_metadata()
print('Slack metadata:')
print(f'  Name: {metadata.name}')
print(f'  Version: {metadata.version}')
print(f'  Capabilities: {metadata.capabilities}')
"
```

### Task 6: Test Full Integration

```bash
# Test app startup with plugins
python -c "
import sys
sys.path.insert(0, '.')
from web.app import app
print('✅ App loads with plugins')
"

# Check app.state has plugin_registry
python -c "
import sys
sys.path.insert(0, '.')
from web.app import app
# Note: This won't work outside lifespan context
# But verifies no import errors
print('✅ App structure validates')
"
```

### Task 7: Verify Line Counts

```bash
# Count plugin wrappers
wc -l services/integrations/slack/slack_plugin.py
wc -l services/integrations/github/github_plugin.py

# Expected: ~80-100 lines each
```

## Deliverable

Create: `dev/2025/10/02/phase-3c-code-slack-github-plugins.md`

Include:
1. **Slack Plugin**: Complete implementation
2. **GitHub Plugin**: Complete implementation
3. **Integration Analysis**: How plugins wrap existing routers
4. **Test Results**: All validation tests passing
5. **Auto-Registration**: Proof plugins register on import
6. **Status Reporting**: Plugin status outputs

## Critical Requirements

- **DO wrap** existing integration routers (don't rewrite them)
- **DO auto-register** plugins at module import
- **DO preserve** existing functionality
- **DO implement** all PiperPlugin methods
- **DON'T modify** existing router classes (Phase 3C is wrapper only)
- **DON'T break** existing integration behavior

## Time Estimate
45 minutes (half of Phase 3C, Cursor does other half)

## Success Criteria
- [ ] SlackPlugin created and working
- [ ] GitHubPlugin created and working
- [ ] Both plugins auto-register on import
- [ ] Both plugins validate against interface
- [ ] Plugins imported in web/app.py
- [ ] All test commands pass
- [ ] Plugin metadata accurate
- [ ] Status reporting working

---

**Deploy at 6:35 PM**
**Coordinate with Cursor on Notion + Calendar plugins**
