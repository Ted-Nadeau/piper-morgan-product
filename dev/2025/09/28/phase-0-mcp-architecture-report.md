# Phase 0: MCP Architecture Investigation Report

**Date**: September 28, 2025, 9:15 PM Pacific
**Investigation Duration**: 29 minutes
**Status**: ✅ COMPLETE - Comprehensive understanding achieved

---

## Executive Summary

**Critical Discovery**: Piper Morgan has a sophisticated MCP (Model Context Protocol) architecture with THREE distinct integration patterns:

1. **MCP Consumer Pattern**: Calendar, Notion, GitHub (with MCP adapters)
2. **Spatial Pattern**: Slack (direct spatial inheritance, no MCP)
3. **Router Pattern**: GitHub only (established in CORE-GREAT-2B)

**Impact for CORE-QUERY-1**: Router wrappers must accommodate TWO different underlying patterns (MCP + Spatial), not just MCP as initially assumed.

---

## MCP Adapter Inventory

### Complete MCP Infrastructure (33 files)

**Primary Locations**:
- `services/mcp/consumer/` - 8 consumer adapters + core
- `services/integrations/mcp/` - 2 integration adapters
- `services/mcp/protocol/` - 4 protocol implementation files
- `services/mcp/server/` - 3 server core files
- Tests and domain objects - 16 additional support files

### Found Adapters

| Adapter | Location | Size | Status | Pattern |
|---------|----------|------|--------|---------|
| **Calendar** | `services/mcp/consumer/google_calendar_adapter.py` | 499 lines | ✅ Complete + OAuth | MCP Consumer |
| **Notion** | `services/integrations/mcp/notion_adapter.py` | 20631 bytes | ✅ Complete | MCP Integration |
| **GitHub** | `services/mcp/consumer/github_adapter.py` | 22772 bytes | ✅ Complete | MCP Consumer |
| **Slack** | N/A - Uses spatial pattern | N/A | ✅ Complete | Direct Spatial |

**Note**: Linear, GitBook, DevEnvironment, CI/CD adapters also exist but not relevant to CORE-QUERY-1.

---

## Calendar Adapter Analysis (Reference Pattern)

**File**: `services/mcp/consumer/google_calendar_adapter.py`
**Size**: 499 lines
**Class**: `GoogleCalendarMCPAdapter(BaseSpatialAdapter)`

### Inheritance Pattern
```python
from services.integrations.spatial_adapter import BaseSpatialAdapter
class GoogleCalendarMCPAdapter(BaseSpatialAdapter):
    def __init__(self):
        super().__init__("google_calendar_mcp")
        self.mcp_consumer = MCPConsumerCore()
```

### Authentication Pattern
- **OAuth 2.0**: Complete browser-based flow
- **Credentials**: `credentials.json` (client secrets) + `token.json` (access token)
- **Scopes**: Calendar read-only permissions
- **Setup**: `setup_google_calendar_oauth.py` script

### Public Methods (7 core methods)
```python
async def authenticate() -> bool                        # OAuth setup
async def get_todays_events() -> List[Dict[str, Any]]  # Calendar events
async def get_current_meeting() -> Optional[Dict]       # Active meeting
async def get_next_meeting() -> Optional[Dict]          # Upcoming meeting
async def get_free_time_blocks() -> List[Dict]         # Available time
async def get_temporal_summary() -> Dict[str, Any]     # Standup summary
async def health_check() -> Dict[str, Any]             # Status check
```

### Key Pattern Elements
1. **MCPConsumerCore Integration**: Uses MCP protocol for communication
2. **Circuit Breaker**: 3 errors triggers 5-minute timeout
3. **Spatial Context**: Overrides `_extract_spatial_context()` for calendar-specific mapping
4. **Async/Await**: All operations are asynchronous
5. **Error Handling**: Graceful fallback when Google libraries unavailable

---

## BaseSpatialAdapter Pattern

**Location**: `services/integrations/spatial_adapter.py`
**Size**: 277 lines
**Purpose**: Abstract base class for spatial position mapping

### Core Interface
```python
class BaseSpatialAdapter(ABC):
    def map_to_position(external_id: str, context: Dict) -> SpatialPosition
    def map_from_position(position: SpatialPosition) -> Optional[str]
    def store_mapping(external_id: str, position: SpatialPosition) -> bool
    def get_context(external_id: str) -> Optional[SpatialContext]
```

### Spatial Intelligence Integration

**SpatialContext Structure** (8-dimensional analysis):
```python
@dataclass
class SpatialContext:
    # Location dimensions
    territory_id: str     # High-level area
    room_id: str         # Specific space
    path_id: str         # Navigation path

    # Behavioral dimensions
    attention_level: str      # low, medium, high, urgent
    emotional_valence: str    # positive, negative, neutral
    navigation_intent: str    # respond, investigate, monitor, explore

    # System mapping
    external_system: str      # Source system name
    external_id: str         # External identifier
```

### Required Subclass Implementation
- Subclasses inherit mapping functionality
- Must override `_extract_spatial_context()` for system-specific mapping
- Spatial position counter automatically managed
- In-memory mapping storage provided

---

## Notion Adapter Analysis

**File**: `services/integrations/mcp/notion_adapter.py`
**Size**: 20631 bytes (largest adapter)
**Class**: `NotionMCPAdapter(BaseSpatialAdapter)`

### Pattern Comparison with Calendar
- **Same inheritance**: `BaseSpatialAdapter`
- **Same constructor pattern**: `super().__init__("notion_mcp")`
- **Different config**: Uses `NotionConfig()` instead of OAuth files
- **Different focus**: Full CRUD operations vs read-only calendar

### Public Methods (20+ methods)
**Connection**: `connect()`, `test_connection()`, `is_configured()`
**Workspace**: `get_workspace_info()`, `list_users()`, `get_user()`
**Databases**: `fetch_databases()`, `list_databases()`, `get_database()`, `query_database()`
**Pages**: `get_page()`, `get_page_blocks()`, `update_page()`, `create_page()`
**Items**: `create_database_item()`, `search_notion()`
**Utility**: `get_mapping_stats()`, `close()`

### Key Differences from Calendar
- **No OAuth**: Uses API token authentication
- **Full CRUD**: Create, read, update operations (vs calendar read-only)
- **Workspace Management**: Multi-database, multi-page operations
- **Configuration**: External config class vs inline environment variables

---

## Slack Integration Analysis

**Current Pattern**: Direct Spatial (NOT MCP)
**Class**: `SlackSpatialAdapter(BaseSpatialAdapter)`
**Files**: 6 spatial implementation files

### Spatial System Files
```
services/integrations/slack/
├── spatial_adapter.py       # BaseSpatialAdapter implementation
├── spatial_agent.py         # Agent logic
├── spatial_intent_classifier.py  # Intent analysis
├── spatial_mapper.py        # Spatial mapping
├── spatial_memory.py        # Memory management
└── spatial_types.py         # Type definitions
```

### Client Pattern
```python
class SlackClient:
    async def send_message(channel: str, text: str) -> SlackResponse
    async def get_channel_info(channel: str) -> SlackResponse
    async def list_channels() -> SlackResponse
    async def get_user_info(user: str) -> SlackResponse
    async def test_auth() -> SlackResponse
```

### Integration Approach
- **Webhook-based**: Uses `webhook_router.py` with spatial components
- **No MCP**: Direct client usage without MCP consumer layer
- **Spatial Intelligence**: Full 6-file spatial implementation

### Key Differences from MCP Pattern
- **Direct inheritance**: `SlackSpatialAdapter(BaseSpatialAdapter)` (no MCP consumer)
- **Webhook routing**: Event-driven vs API polling
- **Rich spatial system**: 6 specialized files vs single adapter file

---

## Current Service Usage

### Calendar Integration
**Direct MCP Usage**:
```python
# services/intent_service/canonical_handlers.py
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter
calendar_adapter = GoogleCalendarMCPAdapter()

# services/features/morning_standup.py
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter
calendar_adapter = GoogleCalendarMCPAdapter()
```

### Notion Integration
**Mixed Usage Patterns**:
```python
# services/domain/notion_domain_service.py (Domain wrapper)
from services.integrations.mcp.notion_adapter import NotionMCPAdapter
self._notion_adapter = notion_adapter or NotionMCPAdapter()

# services/publishing/publisher.py (Direct usage)
from services.integrations.mcp.notion_adapter import NotionMCPAdapter

# services/intelligence/spatial/notion_spatial.py (Spatial intelligence)
from services.integrations.mcp.notion_adapter import NotionMCPAdapter
```

### Slack Integration
**Spatial + Client Pattern**:
```python
# services/integrations/slack/webhook_router.py
from .spatial_adapter import SlackSpatialAdapter
from .spatial_mapper import SlackSpatialMapper
from services.integrations.slack.slack_client import SlackClient

self.spatial_mapper = spatial_mapper or SlackSpatialMapper()
self.spatial_adapter = spatial_adapter or SlackSpatialAdapter()
slack_client = SlackClient(self.config_service)
```

---

## Feature Flag System

### Existing Implementation (from CORE-GREAT-2B)
```python
# services/infrastructure/config/feature_flags.py
@staticmethod
def should_use_spatial_github() -> bool:
    return FeatureFlags._get_boolean_flag("USE_SPATIAL_GITHUB", True)
```

### Missing Flags (need creation)
- `USE_SPATIAL_SLACK` - Control spatial vs basic Slack integration
- `USE_SPATIAL_NOTION` - Control spatial vs basic Notion integration
- `USE_SPATIAL_CALENDAR` - Control spatial vs basic calendar integration

### GitHub Router Delegation Pattern (Reference)
```python
def _get_preferred_integration(self, operation: str) -> tuple[Any, bool]:
    """Get preferred integration based on feature flags"""
    # Try spatial first if enabled
    if self.use_spatial and self.spatial_github:
        return self.spatial_github, False  # Use spatial integration

    # Fall back to legacy if allowed
    elif self.allow_legacy and self.legacy_github:
        return self.legacy_github, True   # Use legacy integration

    # No integration available
    else:
        return None, False
```

---

## Router Wrapper Design Pattern

Based on MCP architecture investigation, router wrappers should follow this pattern:

### 1. Initialization Pattern
```python
class CalendarIntegrationRouter:
    def __init__(self):
        # Feature flag checking
        self.use_spatial = FeatureFlags.should_use_spatial_calendar()
        self.allow_legacy = FeatureFlags.is_legacy_calendar_allowed()

        # Initialize integrations based on flags
        if self.use_spatial:
            self.spatial_calendar = GoogleCalendarMCPAdapter()
        if self.allow_legacy:
            self.legacy_calendar = BasicCalendarClient()  # If exists
```

### 2. Delegation Pattern
```python
async def get_todays_events(self) -> List[Dict[str, Any]]:
    integration, is_legacy = self._get_preferred_integration("get_todays_events")
    if integration:
        if is_legacy:
            self._warn_deprecation_if_needed("get_todays_events", is_legacy)
        return await integration.get_todays_events()
    else:
        raise RuntimeError("No calendar integration available")
```

### 3. Method Exposure
Router should expose ALL public methods from underlying MCP adapter:
- **Calendar**: 7 core methods (authenticate, get_todays_events, etc.)
- **Notion**: 20+ methods (connect, get_workspace_info, etc.)
- **Slack**: Combination of SlackClient + spatial methods

### 4. Error Handling
- Preserve circuit breaker patterns from MCP adapters
- Add router-level error handling for integration failures
- Maintain spatial context through delegation

---

## Recommendations for Router Implementation

### Slack Router (Most Complex)
**Challenge**: No MCP adapter exists - uses direct spatial pattern
**Approach**: Router delegates to existing SlackSpatialAdapter + SlackClient
```python
class SlackIntegrationRouter:
    def __init__(self):
        self.use_spatial = FeatureFlags.should_use_spatial_slack()
        if self.use_spatial:
            self.spatial_slack = SlackSpatialAdapter()
            self.slack_client = SlackClient(config_service)
        # Note: No legacy slack integration exists
```

### Calendar Router (Reference Implementation)
**Advantage**: Complete MCP adapter with OAuth working
**Approach**: Direct delegation to GoogleCalendarMCPAdapter
```python
class CalendarIntegrationRouter:
    def __init__(self):
        self.spatial_calendar = GoogleCalendarMCPAdapter()
        # Note: No legacy calendar integration exists

    async def get_todays_events(self):
        return await self.spatial_calendar.get_todays_events()
```

### Notion Router (Straightforward)
**Advantage**: Complete MCP adapter with full CRUD operations
**Approach**: Direct delegation to NotionMCPAdapter
```python
class NotionIntegrationRouter:
    def __init__(self):
        self.spatial_notion = NotionMCPAdapter()
        # Note: No legacy notion integration exists
```

---

## Questions Requiring Resolution

### 1. Legacy Integration Support
**Question**: Do any legacy (non-spatial) integrations exist for Slack, Notion, or Calendar?
**Current Evidence**: Only GitHub has legacy integration (GitHubAgent)
**Impact**: If no legacy integrations exist, routers are simple delegation wrappers

### 2. Slack Router Complexity
**Question**: Should SlackIntegrationRouter expose SlackClient methods directly or create wrapper methods?
**Current Evidence**: SlackClient has 12+ async methods vs 7 calendar methods
**Impact**: Affects router interface size and maintenance burden

### 3. Feature Flag Defaults
**Question**: Should new spatial flags default to True (like GitHub) or False for safety?
**Current Evidence**: `USE_SPATIAL_GITHUB` defaults to True
**Impact**: Affects migration strategy and user experience

### 4. MCP Consumer Integration
**Question**: Should routers also initialize MCPConsumerCore or rely on adapters?
**Current Evidence**: Adapters handle MCP consumer initialization internally
**Impact**: Affects router initialization complexity

---

## Critical Success Factors for Implementation

### 1. Pattern Consistency
- Follow GitHub router delegation pattern exactly
- Maintain same error handling and warning patterns
- Use same feature flag checking logic

### 2. Spatial Intelligence Preservation
- Ensure spatial context flows through router delegation
- Preserve 8-dimensional analysis capabilities
- Maintain BaseSpatialAdapter inheritance benefits

### 3. OAuth/Authentication Preservation
- Calendar OAuth must work through router
- Notion API token authentication must work through router
- Slack webhook authentication must work through router

### 4. Service Migration Strategy
- Update all existing direct imports to use routers
- Maintain backward compatibility during transition
- Comprehensive testing of service integration

---

## Implementation Priority

### Phase 1: Calendar Router (Simplest)
- Single MCP adapter delegation
- OAuth preservation critical
- 7 methods to expose
- **Estimate**: 2-3 hours

### Phase 2: Notion Router (Medium Complexity)
- Single MCP adapter delegation
- 20+ methods to expose
- Configuration preservation critical
- **Estimate**: 3-4 hours

### Phase 3: Slack Router (Most Complex)
- No MCP adapter - direct spatial delegation
- SlackClient + spatial components integration
- Webhook routing preservation critical
- **Estimate**: 4-6 hours

---

**Investigation Complete**: September 28, 2025, 9:15 PM Pacific
**Next Phase**: Router implementation based on established patterns
**Confidence Level**: High - comprehensive understanding achieved
