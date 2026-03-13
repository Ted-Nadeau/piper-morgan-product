# Revised Gameplan: CORE-QUERY-1 - Router Wrappers for MCP Integrations

**Date**: September 28, 2025 (Final revision)
**Issue**: #199
**Architect**: Claude Opus 4.1
**Lead Developer**: Claude Sonnet 4

---

## Strategic Discovery from Phase -1B

ALL integrations use MCP pattern or have MCP adapters. This fundamentally changes our approach:
- **Slack**: Has traditional client + spatial, but could use MCP pattern
- **Notion**: MCP adapter at `services/integrations/mcp/notion_adapter.py`
- **Calendar**: MCP adapter at `services/mcp/consumer/google_calendar_adapter.py` (85% complete!)

---

## New Mission: Create Router Wrappers for Unified Access

Instead of auditing directory-based routers, we need to create lightweight router wrappers that:
1. Provide consistent interface for QueryRouter
2. Enable feature flag control
3. Delegate to appropriate backend (MCP/spatial/legacy)

---

## Phase 0: Architecture Alignment

### Deploy: Both Agents - Pattern Discovery

#### 0A. Understand MCP Architecture
```bash
# Find all MCP adapters
find . -path "*/mcp/*" -name "*.py" -type f

# Check base adapter pattern
cat services/mcp/consumer/google_calendar_adapter.py | grep "class\|def " | head -20

# Check spatial inheritance
grep -r "BaseSpatialAdapter" services/mcp/

# Understand MCP pattern
ls -la services/integrations/mcp/
ls -la services/mcp/consumer/
```

#### 0B. Audit What Needs Routers
```markdown
For each integration, determine:
1. Current access pattern (how services use it now)
2. Methods exposed by adapter/client
3. Feature flag requirements
4. Spatial intelligence availability
```

---

## Phase 1: Slack Router Wrapper

### Deploy: Code for Implementation, Cursor for Verification

#### 1A. Create SlackIntegrationRouter

```python
# services/integrations/slack/slack_integration_router.py
import os
from typing import Optional

class SlackIntegrationRouter:
    """Router wrapper for Slack integration with spatial/legacy control"""

    def __init__(self):
        self.use_spatial = os.getenv('USE_SPATIAL_SLACK', 'true').lower() == 'true'

        # Slack has both patterns available
        if self.use_spatial:
            from .slack_spatial import SlackSpatial
            self.backend = SlackSpatial()
        else:
            from .slack_client import SlackClient
            self.backend = SlackClient()

    # Delegate all methods to backend
    def __getattr__(self, name):
        """Delegate to appropriate backend"""
        return getattr(self.backend, name)
```

#### 1B. Test Feature Flag Control

```bash
# Test spatial mode
USE_SPATIAL_SLACK=true python -c "
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
router = SlackIntegrationRouter()
print(f'Using spatial: {router.use_spatial}')
"

# Test legacy mode
USE_SPATIAL_SLACK=false python -c "..."
```

---

## Phase 2: Calendar Router Wrapper

### Deploy: Code for Implementation, Cursor for Verification

#### 2A. Create CalendarIntegrationRouter

```python
# services/integrations/calendar/calendar_integration_router.py
import os

class CalendarIntegrationRouter:
    """Router wrapper for Calendar MCP adapter"""

    def __init__(self):
        # Calendar currently only has MCP implementation
        from services.mcp.consumer.google_calendar_adapter import GoogleCalendarAdapter
        self.backend = GoogleCalendarAdapter()

        # Future: Add spatial flag when spatial calendar exists
        self.use_spatial = False  # Placeholder for future

    # Expose key calendar methods
    def get_todays_events(self):
        return self.backend.get_todays_events()

    def get_current_meeting(self):
        return self.backend.get_current_meeting()

    def get_next_meeting(self):
        return self.backend.get_next_meeting()

    def find_free_time(self, duration_minutes=30):
        return self.backend.find_free_time(duration_minutes)
```

#### 2B. Verify OAuth Still Works

```python
# Test that OAuth flow isn't broken by router
# The adapter handles OAuth internally with credentials.json/token.json
```

---

## Phase 3: Notion Router Wrapper

### Deploy: Code for Implementation, Cursor for Verification

#### 3A. Create NotionIntegrationRouter

```python
# services/integrations/notion/notion_integration_router.py
import os

class NotionIntegrationRouter:
    """Router wrapper for Notion MCP adapter"""

    def __init__(self):
        from services.integrations.mcp.notion_adapter import NotionAdapter
        self.backend = NotionAdapter()

        # Future spatial support
        self.use_spatial = os.getenv('USE_SPATIAL_NOTION', 'false').lower() == 'true'

    # Delegate to MCP adapter
    def __getattr__(self, name):
        return getattr(self.backend, name)
```

---

## Phase 4: Service Migration

### Deploy: Both Agents - Update Import Patterns

#### 4A. Find Services Using Direct Access

```bash
# Find direct Slack usage
grep -r "SlackClient\|SlackSpatial" services/ --include="*.py" | grep -v router

# Find direct Calendar usage
grep -r "GoogleCalendarAdapter" services/ --include="*.py" | grep -v router

# Find direct Notion usage
grep -r "NotionAdapter" services/ --include="*.py" | grep -v router
```

#### 4B. Replace with Router Imports

Update all found services to use routers instead of direct access.

---

## Phase 5: QueryRouter Integration

### Deploy: Both Agents - Wire Routers to QueryRouter

#### 5A. Verify QueryRouter Can Access All Routers

```python
# In QueryRouter or orchestration
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

# All should be accessible through unified interface
```

#### 5B. Test End-to-End Query Flow

Test that queries can reach each integration through QueryRouter.

---

## Phase 6: Lock & Document

### Deploy: Both Agents

1. Create architecture test preventing direct adapter access
2. Document MCP router pattern
3. Update architecture diagrams

---

## Success Criteria

- [ ] All three integrations have router wrappers
- [ ] QueryRouter can access all integrations
- [ ] Feature flags control Slack spatial/legacy
- [ ] Calendar OAuth still works through router
- [ ] No direct adapter/client usage
- [ ] Architecture tests prevent regression

---

## Scope Assessment

This approach is significantly simpler than originally expected because:
- Calendar integration exists and is 85% complete (not missing)
- All integrations follow or can follow MCP pattern
- Router wrappers are lightweight delegators, not complex implementations
- Working OAuth and functionality are preserved

The discovery of existing infrastructure means we're wrapping and connecting rather than building from scratch.

---

## Cathedral Context

The MCP pattern discovery simplifies everything. Instead of building complex routers from scratch, we're creating thin wrappers that enable:
- Consistent access pattern for QueryRouter
- Feature flag control where applicable
- Future spatial intelligence migration
- Preservation of working OAuth and functionality

Calendar being 85% complete changes the entire scope calculation!

---

*Wrap the adapters. Enable the QueryRouter. Preserve what works.*

### Deploy: Both Agents - Pattern Discovery

#### 0A. Understand MCP Architecture
```bash
# Find all MCP adapters
find . -path "*/mcp/*" -name "*.py" -type f

# Check base adapter pattern
cat services/mcp/consumer/google_calendar_adapter.py | grep "class\|def " | head -20

# Check spatial inheritance
grep -r "BaseSpatialAdapter" services/mcp/

# Understand MCP pattern
ls -la services/integrations/mcp/
ls -la services/mcp/consumer/
```

#### 0B. Audit What Needs Routers
```markdown
For each integration, determine:
1. Current access pattern (how services use it now)
2. Methods exposed by adapter/client
3. Feature flag requirements
4. Spatial intelligence availability
```

---

## Phase 1: Slack Router Wrapper (3 hours)

### Deploy: Code for Implementation, Cursor for Verification

#### 1A. Create SlackIntegrationRouter

```python
# services/integrations/slack/slack_integration_router.py
import os
from typing import Optional

class SlackIntegrationRouter:
    """Router wrapper for Slack integration with spatial/legacy control"""

    def __init__(self):
        self.use_spatial = os.getenv('USE_SPATIAL_SLACK', 'true').lower() == 'true'

        # Slack has both patterns available
        if self.use_spatial:
            from .slack_spatial import SlackSpatial
            self.backend = SlackSpatial()
        else:
            from .slack_client import SlackClient
            self.backend = SlackClient()

    # Delegate all methods to backend
    def __getattr__(self, name):
        """Delegate to appropriate backend"""
        return getattr(self.backend, name)
```

#### 1B. Test Feature Flag Control

```bash
# Test spatial mode
USE_SPATIAL_SLACK=true python -c "
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
router = SlackIntegrationRouter()
print(f'Using spatial: {router.use_spatial}')
"

# Test legacy mode
USE_SPATIAL_SLACK=false python -c "..."
```

---

## Phase 2: Calendar Router Wrapper (2 hours)

### Deploy: Code for Implementation, Cursor for Verification

#### 2A. Create CalendarIntegrationRouter

```python
# services/integrations/calendar/calendar_integration_router.py
import os

class CalendarIntegrationRouter:
    """Router wrapper for Calendar MCP adapter"""

    def __init__(self):
        # Calendar currently only has MCP implementation
        from services.mcp.consumer.google_calendar_adapter import GoogleCalendarAdapter
        self.backend = GoogleCalendarAdapter()

        # Future: Add spatial flag when spatial calendar exists
        self.use_spatial = False  # Placeholder for future

    # Expose key calendar methods
    def get_todays_events(self):
        return self.backend.get_todays_events()

    def get_current_meeting(self):
        return self.backend.get_current_meeting()

    def get_next_meeting(self):
        return self.backend.get_next_meeting()

    def find_free_time(self, duration_minutes=30):
        return self.backend.find_free_time(duration_minutes)
```

#### 2B. Verify OAuth Still Works

```python
# Test that OAuth flow isn't broken by router
# The adapter handles OAuth internally with credentials.json/token.json
```

---

## Phase 3: Notion Router Wrapper (2 hours)

### Deploy: Code for Implementation, Cursor for Verification

#### 3A. Create NotionIntegrationRouter

```python
# services/integrations/notion/notion_integration_router.py
import os

class NotionIntegrationRouter:
    """Router wrapper for Notion MCP adapter"""

    def __init__(self):
        from services.integrations.mcp.notion_adapter import NotionAdapter
        self.backend = NotionAdapter()

        # Future spatial support
        self.use_spatial = os.getenv('USE_SPATIAL_NOTION', 'false').lower() == 'true'

    # Delegate to MCP adapter
    def __getattr__(self, name):
        return getattr(self.backend, name)
```

---

## Phase 4: Service Migration (2 hours)

### Deploy: Both Agents - Update Import Patterns

#### 4A. Find Services Using Direct Access

```bash
# Find direct Slack usage
grep -r "SlackClient\|SlackSpatial" services/ --include="*.py" | grep -v router

# Find direct Calendar usage
grep -r "GoogleCalendarAdapter" services/ --include="*.py" | grep -v router

# Find direct Notion usage
grep -r "NotionAdapter" services/ --include="*.py" | grep -v router
```

#### 4B. Replace with Router Imports

Update all found services to use routers instead of direct access.

---

## Phase 5: QueryRouter Integration (1 hour)

### Deploy: Both Agents - Wire Routers to QueryRouter

#### 5A. Verify QueryRouter Can Access All Routers

```python
# In QueryRouter or orchestration
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

# All should be accessible through unified interface
```

#### 5B. Test End-to-End Query Flow

Test that queries can reach each integration through QueryRouter.

---

## Phase 6: Lock & Document (1 hour)

### Deploy: Both Agents

1. Create architecture test preventing direct adapter access
2. Document MCP router pattern
3. Update architecture diagrams

---

## Success Criteria

- [ ] All three integrations have router wrappers
- [ ] QueryRouter can access all integrations
- [ ] Feature flags control Slack spatial/legacy
- [ ] Calendar OAuth still works through router
- [ ] No direct adapter/client usage
- [ ] Architecture tests prevent regression

---

## Time Estimate (Revised)

- Phase 0: 1 hour (understand MCP pattern)
- Phase 1: 3 hours (Slack router)
- Phase 2: 2 hours (Calendar router)
- Phase 3: 2 hours (Notion router)
- Phase 4: 2 hours (service migration)
- Phase 5: 1 hour (QueryRouter integration)
- Phase 6: 1 hour (lock & document)
- **Total: 12 hours**

Much more achievable than original 32-56 hours!

---

## Cathedral Context

The MCP pattern discovery simplifies everything. Instead of building complex routers from scratch, we're creating thin wrappers that enable:
- Consistent access pattern for QueryRouter
- Feature flag control where applicable
- Future spatial intelligence migration
- Preservation of working OAuth and functionality

Calendar being 85% complete changes the entire scope calculation!

---

*Wrap the adapters. Enable the QueryRouter. Preserve what works.*
