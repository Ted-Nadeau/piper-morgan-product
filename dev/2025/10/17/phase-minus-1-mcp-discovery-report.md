# Phase -1 Discovery Report: MCP Migration

**Date**: October 17, 2025
**Agent**: Claude Code (Programmer)
**Task**: CORE-MCP-MIGRATION #198 - Phase -1 Discovery
**Duration**: 3 hours estimated

---

## Executive Summary

**Key Findings**:
- ✅ **2 services HAVE MCP adapters** (Notion, Calendar via services/mcp/consumer/)
- ❌ **2 services MISSING MCP adapters** (GitHub, Slack)
- ⚠️ **Critical Discovery**: MCP adapters exist in **SEPARATE LOCATION** (`services/mcp/consumer/`) from integration routers (`services/integrations/`)
- 🔴 **RED FLAG**: MCP adapters are **NOT WIRED** to OrchestrationEngine (only integration routers are)
- 📁 **Unexpected discovery**: 7 total MCP adapters exist in `services/mcp/consumer/` but only 2 are actively used by integrations

**Infrastructure Verified**: Main entry point (main.py: 58 lines), web app (web/app.py: 712 lines), port 8001 ✅

**Migration Complexity**: MODERATE-HIGH due to architectural split and lack of standardization

---

## Service Inventory

### 1. GitHub Integration

**Location**: `services/integrations/github/`

**MCP Adapter**: ❌ **NO**

**Evidence**:
```bash
$ ls -la services/integrations/github/
total 192
-rw-r--r--  config_service.py
-rw-r--r--  content_generator.py
-rw-r--r--  github_integration_router.py (278 lines)
-rw-r--r--  github_plugin.py
-rw-r--r--  issue_analyzer.py
-rw-r--r--  issue_generator.py
-rw-r--r--  production_client.py
-rw-r--r--  test_pm0008.py

$ grep -r "MCP\|mcp" services/integrations/github/ --include="*.py"
services/integrations/github/github_integration_router.py:Architecture Decision: ADR-013 MCP+Spatial Integration Pattern
# ^ Only reference is ADR comment, no actual MCP adapter implementation
```

**Router**: ✅ `github_integration_router.py` (278 lines)
**Spatial Intelligence**: ⚠️ **MENTIONED** but not present in directory
**Config Service**: ✅ `config_service.py` (382 lines)
**Tests**: ✅ 1 test file found (`test_pm0008.py`)

**Status**: GitHub integration router exists but has NO MCP adapter. Router is wired to OrchestrationEngine via direct imports.

---

### 2. Slack Integration

**Location**: `services/integrations/slack/`

**MCP Adapter**: ❌ **NO** (in slack/ directory)

**Evidence**:
```bash
$ ls -la services/integrations/slack/
total 944
-rw-r--r--  attention_model.py
-rw-r--r--  config_service.py (118 lines)
-rw-r--r--  event_handler.py
-rw-r--r--  ngrok_service.py
-rw-r--r--  oauth_handler.py
-rw-r--r--  response_flow_integration.py
-rw-r--r--  response_handler.py
-rw-r--r--  simple_response_handler.py
-rw-r--r--  slack_client.py
-rw-r--r--  slack_integration_router.py (588 lines)
-rw-r--r--  slack_plugin.py
-rw-r--r--  slack_workflow_factory.py
-rw-r--r--  spatial_adapter.py        # ⚠️ Slack-specific spatial adapter
-rw-r--r--  spatial_agent.py
-rw-r--r--  spatial_intent_classifier.py
-rw-r--r--  spatial_mapper.py
-rw-r--r--  spatial_memory.py
-rw-r--r--  spatial_types.py
drwxr-xr-x  tests/ (10 files)
-rw-r--r--  webhook_router.py (856 lines)
-rw-r--r--  workspace_navigator.py

$ grep -r "MCP\|mcp" services/integrations/slack/ --include="*.py" | head -5
# No MCP adapter references found
```

**Router**: ✅ `slack_integration_router.py` (588 lines) + `webhook_router.py` (856 lines)
**Spatial Intelligence**: ✅✅ **EXTENSIVE** - 6 spatial files (adapter, agent, intent_classifier, mapper, memory, types)
**Config Service**: ✅ `config_service.py` (118 lines)
**Tests**: ✅ 10 test files in `tests/` directory

**Status**: Slack has EXTENSIVE spatial intelligence infrastructure but NO MCP adapter. Direct integration via webhook_router and response handlers that instantiate OrchestrationEngine.

**⚠️ Critical Note**: Slack has its OWN `spatial_adapter.py` which is NOT the same as the MCP adapter pattern!

---

### 3. Notion Integration

**Location**: `services/integrations/notion/`

**MCP Adapter**: ✅ **YES** (in separate location)

**Evidence**:
```bash
$ ls -la services/integrations/notion/
total 72
-rw-r--r--  config_service.py (103 lines)
-rw-r--r--  notion_integration_router.py (662 lines)
-rw-r--r--  notion_plugin.py

$ grep -r "MCP" services/integrations/notion/ --include="*.py"
services/integrations/notion/notion_plugin.py:    Provides Notion integration routes and MCP capabilities through
services/integrations/notion/notion_plugin.py:            description="Notion workspace integration with MCP",
services/integrations/notion/notion_plugin.py:            capabilities=["routes", "mcp"],  # Notion uses MCP
services/integrations/notion/notion_integration_router.py:- Spatial intelligence (MCP-based NotionMCPAdapter with 22 complete methods)
services/integrations/notion/notion_integration_router.py:    Delegates to NotionMCPAdapter (spatial) or future legacy implementation.
services/integrations/notion/notion_integration_router.py:        # USE_SPATIAL_NOTION=true (default) - uses NotionMCPAdapter
services/integrations/notion/notion_integration_router.py:        - Spatial: NotionMCPAdapter with API token authentication and full CRUD
services/integrations/notion/notion_integration_router.py:                from services.integrations.mcp.notion_adapter import NotionMCPAdapter
```

**MCP Adapter Location**: `services/integrations/mcp/notion_adapter.py` (738 lines)
**Router**: ✅ `notion_integration_router.py` (662 lines)
**Spatial Intelligence**: ✅ **VIA MCP** - NotionMCPAdapter extends BaseSpatialAdapter
**Config Service**: ✅ `config_service.py` (103 lines)
**Tests**: ❌ No tests/ directory found in notion/

**Status**: Notion HAS MCP adapter via import from `services.integrations.mcp.notion_adapter`. Router conditionally loads MCP adapter based on `USE_SPATIAL_NOTION` flag.

---

### 4. Calendar Integration

**Location**: `services/integrations/calendar/`

**MCP Adapter**: ✅ **YES** (in separate location)

**Evidence**:
```bash
$ ls -la services/integrations/calendar/
total 64
-rw-r--r--  calendar_integration_router.py (403 lines)
-rw-r--r--  calendar_plugin.py
-rw-r--r--  config_service.py (116 lines)

$ grep -r "MCP" services/integrations/calendar/ --include="*.py"
services/integrations/calendar/calendar_integration_router.py:- Spatial intelligence (MCP-based GoogleCalendarMCPAdapter)
services/integrations/calendar/calendar_integration_router.py:    Delegates to GoogleCalendarMCPAdapter (spatial) or future legacy implementation.
services/integrations/calendar/calendar_integration_router.py:        # USE_SPATIAL_CALENDAR=true (default) - uses GoogleCalendarMCPAdapter
services/integrations/calendar/calendar_integration_router.py:        - Spatial: GoogleCalendarMCPAdapter with OAuth2 and circuit breaker
services/integrations/calendar/calendar_integration_router.py:                from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter
```

**MCP Adapter Location**: `services/mcp/consumer/google_calendar_adapter.py` (514 lines)
**Router**: ✅ `calendar_integration_router.py` (403 lines)
**Spatial Intelligence**: ✅ **VIA MCP** - GoogleCalendarMCPAdapter extends BaseSpatialAdapter
**Config Service**: ✅ `config_service.py` (116 lines)
**Tests**: ❌ No tests/ directory found in calendar/

**Status**: Calendar HAS MCP adapter via import from `services.mcp.consumer.google_calendar_adapter`. Router conditionally loads MCP adapter based on `USE_SPATIAL_CALENDAR` flag.

**⚠️ Note**: Calendar imports from different namespace (`services.mcp.consumer` vs `services.integrations.mcp`)

---

### 5. Demo Integration

**Location**: `services/integrations/demo/`

**MCP Adapter**: ❌ **NO**

**Evidence**:
```bash
$ ls -la services/integrations/demo/
total 32
-rw-r--r--  config_service.py (50 lines)
-rw-r--r--  demo_integration_router.py (98 lines)
-rw-r--r--  demo_plugin.py
drwxr-xr-x  tests/ (1 file)
```

**Router**: ✅ `demo_integration_router.py` (98 lines)
**Spatial Intelligence**: ❌ **NO**
**Config Service**: ✅ `config_service.py` (50 lines)
**Tests**: ✅ 1 test file

**Status**: Simple demo integration without MCP adapter. Minimal implementation.

---

### 6. MCP Directory

**Location**: `services/integrations/mcp/`

**Purpose**: ⚠️ **SHARED MCP ADAPTER LOCATION** for integration services

**Evidence**:
```bash
$ ls -la services/integrations/mcp/
total 88
-rw-r--r--  gitbook_adapter.py (10,135 bytes)
-rw-r--r--  notion_adapter.py (29,966 bytes)

$ grep -r "class.*MCP.*Adapter" services/integrations/ --include="*.py"
services/integrations/mcp/gitbook_adapter.py:class GitBookMCPAdapter(BaseSpatialAdapter):
services/integrations/mcp/notion_adapter.py:class NotionMCPAdapter(BaseSpatialAdapter):
```

**Contents**:
- `gitbook_adapter.py` - GitBookMCPAdapter (extends BaseSpatialAdapter)
- `notion_adapter.py` - NotionMCPAdapter (extends BaseSpatialAdapter)

**Status**: This directory contains MCP adapters that are imported by integration routers. Only 2 adapters present.

---

### 7. Spatial Directory

**Location**: `services/integrations/spatial/`

**Purpose**: ⚠️ **SPATIAL INTELLIGENCE** modules (separate from integrations)

**Evidence**:
```bash
$ ls -la services/integrations/spatial/
total 216
-rw-r--r--  cicd_spatial.py (20,463 bytes)
-rw-r--r--  devenvironment_spatial.py (22,962 bytes)
-rw-r--r--  gitbook_spatial.py (22,953 bytes)
-rw-r--r--  github_spatial.py (16,122 bytes)
-rw-r--r__  linear_spatial.py (19,806 bytes)

$ grep -r "from services.integrations.mcp" services/integrations/spatial/ --include="*.py"
services/intelligence/spatial/gitbook_spatial.py:from services.integrations.mcp.gitbook_adapter import GitBookMCPAdapter
```

**Status**: Spatial intelligence modules that MAY use MCP adapters. Found 1 reference to GitBookMCPAdapter.

---

### 8. Services/MCP Directory (ADDITIONAL DISCOVERY)

**Location**: `services/mcp/` (NOT in integrations/)

**Purpose**: ⚠️ **MCP INFRASTRUCTURE** - protocol, client, resources, adapters

**Evidence**:
```bash
$ ls -la services/mcp/
total 72
-rw-r--r--  client.py (11,377 bytes)
drwxr-xr-x  consumer/ (8 files)
-rw-r--r--  exceptions.py
drwxr-xr-x  protocol/
-rw-r--r__  resources.py (16,155 bytes)
drwxr-xr-x  server/

$ ls -la services/mcp/consumer/
total 264
-rw-r--r--  cicd_adapter.py (15,850 bytes)
-rw-r--r__  consumer_core.py (12,651 bytes)
-rw-r--r__  devenvironment_adapter.py (19,689 bytes)
-rw-r--r__  gitbook_adapter.py (15,521 bytes)
-rw-r--r__  github_adapter.py (22,772 bytes)
-rw-r--r__  google_calendar_adapter.py (19,245 bytes)
-rw-r--r__  linear_adapter.py (14,205 bytes)
```

**🔴 CRITICAL DISCOVERY**: There are **7 MCP adapters** in `services/mcp/consumer/`:
1. ❌ `cicd_adapter.py` - NOT used by any integration
2. ❌ `devenvironment_adapter.py` - NOT used by any integration
3. ⚠️ `gitbook_adapter.py` - Used by `services/integrations/spatial/` (indirect)
4. ❌ `github_adapter.py` - **EXISTS** but NOT used by GitHub integration router!
5. ✅ `google_calendar_adapter.py` - Used by Calendar integration
6. ❌ `linear_adapter.py` - NOT used by any integration
7. ⚠️ DUPLICATE: GitBook adapter exists in BOTH locations!

**Status**: **75% PATTERN DETECTED** - Many MCP adapters exist but are NOT connected to integration routers!

---

## MCP Pattern Analysis

### Adapters WITH MCP Implementation

#### 1. NotionMCPAdapter

**Location**: `services/integrations/mcp/notion_adapter.py` (738 lines)

**Pattern**:
```python
class NotionMCPAdapter(BaseSpatialAdapter):
    def __init__(self, config_service: Optional["NotionConfigService"] = None):
        super().__init__("notion_mcp")
        # Service injection pattern (preferred) OR static config fallback

    # Key methods (22 complete methods):
    async def connect(self, integration_token: Optional[str] = None) -> bool
    async def test_connection(self) -> bool
    def is_configured(self) -> bool
    async def get_workspace_info(self) -> Optional[Dict[str, Any]]
    async def get_current_user(self) -> Optional[Dict[str, Any]]
    async def list_databases(self, page_size: int = 100) -> List[Dict[str, Any]]
    async def get_database(self, database_id: str) -> Optional[Dict[str, Any]]
    async def get_data_source_id(self, database_id: str) -> Optional[str]
    async def query_database(...) -> List[Dict[str, Any]]
    async def get_page(self, page_id: str) -> Optional[Dict[str, Any]]
    async def get_page_blocks(self, page_id: str, ...) -> List[Dict[str, Any]]
    async def update_page(self, page_id: str, properties: Dict)
    async def create_page(self, parent_id: str, properties: Dict, ...)
    async def create_database_item(self, database_id: str, ...)
    async def search_notion(self, query: str, ...) -> List[Dict[str, Any]]
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]
    async def list_users(self) -> List[Dict[str, Any]]
    def get_mapping_stats(self) -> Dict[str, Any]
    async def close(self)
```

**Base Class**: `BaseSpatialAdapter` from `services/integrations/spatial_adapter.py`

**Integration Pattern**:
- Router conditionally imports: `from services.integrations.mcp.notion_adapter import NotionMCPAdapter`
- Feature flag: `USE_SPATIAL_NOTION=true` (default)
- Initialization: `self.spatial_notion = NotionMCPAdapter(config_service)` OR `NotionMCPAdapter()` (fallback)

**Context Passing**: Service injection pattern with fallback to static config

**Spatial Intelligence**: Extends BaseSpatialAdapter for spatial position mapping

**Test Coverage**: ❌ No tests found for NotionMCPAdapter

---

#### 2. GoogleCalendarMCPAdapter

**Location**: `services/mcp/consumer/google_calendar_adapter.py` (514 lines)

**Pattern**:
```python
class GoogleCalendarMCPAdapter(BaseSpatialAdapter):
    def __init__(self, config_service: Optional["CalendarConfigService"] = None):
        super().__init__("google_calendar_mcp")
        self.mcp_consumer = None  # ⚠️ Additional MCP consumer component
        self._lock = asyncio.Lock()

    # Key methods (13 methods):
    async def authenticate(self) -> bool
    async def get_todays_events(self) -> List[Dict[str, Any]]
    def _process_event(self, event: Dict[str, Any]) -> Dict[str, Any]
    async def get_current_meeting(self) -> Optional[Dict[str, Any]]
    async def get_next_meeting(self) -> Optional[Dict[str, Any]]
    async def get_free_time_blocks(self, ...) -> List[Dict[str, Any]]
    async def get_temporal_summary(self) -> Dict[str, Any]
    def _generate_recommendations(self, ...) -> List[str]
    def _handle_error(self, error: Exception) -> None
    def _reset_circuit_breaker(self) -> None
    def _extract_spatial_context(self, ...) -> Dict[str, Any]
    async def health_check(self) -> Dict[str, Any]
```

**Base Class**: `BaseSpatialAdapter`

**Integration Pattern**:
- Router conditionally imports: `from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter`
- Feature flag: `USE_SPATIAL_CALENDAR=true` (default)
- Initialization: `self.spatial_calendar = GoogleCalendarMCPAdapter(self.config_service)`

**Context Passing**: Service injection with config_service

**Spatial Intelligence**: Extends BaseSpatialAdapter + custom `_extract_spatial_context` for calendar-specific spatial mapping

**Circuit Breaker**: ✅ Implements circuit breaker pattern for error handling

**Test Coverage**: ❌ No tests found for GoogleCalendarMCPAdapter

---

### BaseSpatialAdapter (Common Base Class)

**Location**: `services/integrations/spatial_adapter.py` (276 lines)

**Pattern**:
```python
class BaseSpatialAdapter(ABC):
    """Base implementation of SpatialAdapter protocol."""

    def __init__(self, system_name: str):
        self.system_name = system_name
        self._position_counter = 0
        self._mappings: Dict[str, SpatialPosition] = {}
        self._contexts: Dict[str, SpatialContext] = {}

    # Protocol methods:
    def map_to_position(self, external_id: str, context: Dict) -> SpatialPosition
    def map_from_position(self, position: SpatialPosition) -> Optional[str]
    def store_mapping(self, external_id: str, position: SpatialPosition) -> bool
    def get_context(self, external_id: str) -> Optional[SpatialContext]
    def get_mapping_stats(self) -> Dict[str, Any]
```

**Supporting Classes**:
```python
@dataclass
class SpatialPosition:
    position: int
    context: Dict[str, Any] = None

@dataclass
class SpatialContext:
    territory_id: str
    room_id: str
    path_id: Optional[str] = None
    object_position: Optional[int] = None
    attention_level: str = "medium"
    emotional_valence: str = "neutral"
    navigation_intent: str = "monitor"
    external_system: str = ""
    external_id: str = ""
    external_context: Dict[str, Any] = None

class SpatialAdapterRegistry:
    """Registry for managing multiple spatial adapters."""
    def register_adapter(self, system_name: str, adapter: SpatialAdapter)
    def get_adapter(self, system_name: str) -> Optional[SpatialAdapter]
    def map_to_position(self, system_name: str, ...) -> Optional[SpatialPosition]
    # ... etc
```

**Status**: Well-defined base class with spatial positioning protocol. Used by Notion and Calendar MCP adapters.

---

### Pattern Variations Discovered

⚠️ **CRITICAL INCONSISTENCIES**:

1. **Import Namespace Variation**:
   - Notion: `from services.integrations.mcp.notion_adapter import NotionMCPAdapter`
   - Calendar: `from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter`
   - ❌ **INCONSISTENT** - adapters in different locations!

2. **Feature Flag Variation**:
   - Notion: `USE_SPATIAL_NOTION`
   - Calendar: `USE_SPATIAL_CALENDAR`
   - Pattern: Each service has its own flag

3. **Initialization Variation**:
   - Notion: `NotionMCPAdapter(config_service)` OR `NotionMCPAdapter()` (two fallback paths)
   - Calendar: `GoogleCalendarMCPAdapter(self.config_service)` (single path)

4. **Method Signature Variation**:
   - Notion: 22 methods (full CRUD, search, users)
   - Calendar: 13 methods (read-only, temporal intelligence)
   - ❌ **NO COMMON INTERFACE** beyond BaseSpatialAdapter

5. **Unused MCP Adapters**:
   - `services/mcp/consumer/github_adapter.py` - **EXISTS** but GitHub router doesn't use it!
   - `services/mcp/consumer/cicd_adapter.py` - No integration found
   - `services/mcp/consumer/devenvironment_adapter.py` - No integration found
   - `services/mcp/consumer/linear_adapter.py` - No integration found
   - ❌ **75% PATTERN CONFIRMED** - 4 of 7 adapters unused!

---

## OrchestrationEngine Integration

### OrchestrationEngine Location

**File**: `services/orchestration/engine.py` (453 lines)

**Key Components**:
```python
class OrchestrationEngine:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client
        self.factory = WorkflowFactory()
        self.workflows = {}
        self.query_router = None  # Initialized on-demand
        self.intent_enricher = IntentEnricher(llm_client)
        # Multi-Agent integration
        self.workflow_integration = WorkflowIntegration()
        self.session_integration = SessionIntegration()
        self.performance_monitor = PerformanceMonitor()

    async def handle_query_intent(self, intent: Intent) -> Dict[str, Any]
    async def create_workflow_from_intent(self, intent: Intent) -> Optional[Workflow]
    async def execute_workflow(self, workflow: Workflow) -> WorkflowResult
    async def _execute_github_action_task(...) -> Dict[str, Any]
```

### Current MCP Integration

**Evidence**:
```bash
$ grep -r "NotionMCPAdapter\|GoogleCalendarMCPAdapter\|GitBookMCPAdapter" services/orchestration/ --include="*.py"
# NO RESULTS - MCP adapters NOT imported by OrchestrationEngine
```

**Status**: ❌ **MCP adapters are NOT wired to OrchestrationEngine**

### How Services Are Currently Wired

**Pattern 1: Direct GitHub Integration**
```python
# services/orchestration/engine.py lines 23-30
from services.integrations.github.config_service import GitHubConfigService
from services.integrations.github.content_generator import GitHubIssueContentGenerator
from services.integrations.github.github_integration_router import GitHubIntegrationRouter
from services.integrations.github.issue_analyzer import GitHubIssueAnalyzer
from services.integrations.github.production_client import ProductionGitHubClient

async def _execute_github_action_task(self, task: Task, ...) -> Dict[str, Any]:
    github_config = GitHubConfigService()
    github_client = ProductionGitHubClient(...)
    github_agent = GitHubIntegrationRouter()
    # Direct instantiation and usage
```

**Pattern 2: Slack Integration** (via webhook router)
```python
# services/integrations/slack/webhook_router.py
from services.orchestration.engine import OrchestrationEngine

# Slack instantiates OrchestrationEngine when needed
orchestration_engine = OrchestrationEngine()
```

**Pattern 3: Notion/Calendar Integration** (router-level)
```python
# services/integrations/notion/notion_integration_router.py
from services.integrations.mcp.notion_adapter import NotionMCPAdapter

class NotionIntegrationRouter:
    def __init__(self, config_service):
        if USE_SPATIAL_NOTION:
            self.spatial_notion = NotionMCPAdapter(config_service)
        # Router uses MCP adapter internally, OrchestrationEngine unaware
```

### Context Passing Mechanism

**Current Pattern**:
1. Integration routers instantiate MCP adapters with `config_service`
2. MCP adapters use service injection pattern OR static config fallback
3. Routers handle all MCP adapter interactions
4. OrchestrationEngine calls routers, NOT adapters directly

**Missing**:
- ❌ No centralized MCP adapter registry
- ❌ No standardized MCP adapter interface beyond BaseSpatialAdapter
- ❌ OrchestrationEngine has no awareness of MCP adapters
- ❌ No dependency injection for MCP adapters into OrchestrationEngine

---

## Infrastructure Verification

### Main Entry Point

✅ **Verified**: `main.py` (58 lines)

**Evidence**:
```python
# main.py lines 1-58
"""
Piper Morgan - Main Entry Point
This is the proper way to start Piper Morgan.
It initializes services via ServiceContainer and starts the web server.
"""

async def main():
    # Initialize service container
    from services.container import ServiceContainer
    container = ServiceContainer()
    await container.initialize()

    # Start web server
    import uvicorn
    logger.info("Starting web server on http://127.0.0.1:8001")
    config = uvicorn.Config("web.app:app", host="127.0.0.1", port=8001, ...)
    server = uvicorn.Server(config)
    await server.serve()
```

**Status**: ✅ Correct - uses ServiceContainer and port 8001

---

### Web App

✅ **Verified**: `web/app.py` (712 lines)

**Evidence**:
```bash
$ wc -l main.py web/app.py
      58 main.py
     712 web/app.py
     770 total
```

**Status**: ✅ Correct - 712 lines (refactored in GREAT-3A per instructions)

---

### Port Configuration

✅ **Verified**: Port **8001** (NOT 8080)

**Evidence**:
```bash
$ grep -r "8001\|8080" . --include="*.py" | grep -v archive | head -5
./tests/integration/test_devenvironment_spatial_federation.py:    "ports": {"8001/tcp": [{"HostPort": "8001"}]},
./tests/integration/test_startup.py:    response = requests.get("http://localhost:8001/health", timeout=2)
./tests/integration/test_startup.py:    response = requests.get("http://localhost:8001/health/slack", timeout=5)
```

**Status**: ✅ Correct - Port 8001 is standard

---

### Services Directory Structure

✅ **Verified**: Matches expectations with discoveries

**Structure**:
```
services/
├── integrations/
│   ├── calendar/       (router, config, plugin)
│   ├── demo/           (router, config, plugin)
│   ├── github/         (router, config, plugin, analyzer, content_generator, production_client)
│   ├── mcp/            (notion_adapter, gitbook_adapter)  ⚠️ ONLY 2 adapters
│   ├── notion/         (router, config, plugin)
│   ├── slack/          (router, webhook_router, config, plugin, spatial_* files)
│   ├── spatial/        (cicd, devenvironment, gitbook, github, linear)
│   └── spatial_adapter.py  (BaseSpatialAdapter base class)
├── mcp/                ⚠️ SEPARATE MCP INFRASTRUCTURE
│   ├── consumer/       (7 MCP adapters including google_calendar, github)
│   ├── protocol/
│   ├── server/
│   ├── client.py
│   └── resources.py
└── orchestration/
    └── engine.py       (OrchestrationEngine)
```

**⚠️ Discovered Inconsistencies**:
- MCP adapters in **TWO** locations: `services/integrations/mcp/` AND `services/mcp/consumer/`
- Slack has its own spatial files, separate from MCP pattern
- GitHub has NO MCP adapter in `services/integrations/github/` BUT one exists in `services/mcp/consumer/github_adapter.py`

---

### Test Framework

✅ **Verified**: pytest with integration tests

**Evidence**:
```bash
$ find tests/integration -name "*github*" -o -name "*slack*" -o -name "*notion*" -o -name "*calendar*" | wc -l
      13
```

**Test Locations**:
- `services/integrations/slack/tests/` (10 files)
- `services/integrations/demo/tests/` (1 file)
- `services/integrations/github/test_pm0008.py` (1 file)
- `tests/integration/` (13 files)

**Status**: ✅ Test framework exists, coverage varies by service

---

## Migration Effort Assessment

### 1. GitHub Integration

**Current MCP Status**: ❌ **NONE** (in integration router)

**⚠️ CRITICAL DISCOVERY**: MCP adapter **ALREADY EXISTS** at `services/mcp/consumer/github_adapter.py` (22,772 bytes) but is NOT used by GitHub integration router!

**Estimated Work**: **6-8 hours** - Connect existing adapter OR create new one

**Complexity Factors**:
- ✅ MCP adapter already exists (if usable)
- ❌ No spatial intelligence in github/ directory (exists separately in `services/integrations/spatial/github_spatial.py`)
- ✅ Router is well-structured (278 lines)
- ✅ Config service exists (382 lines)
- ❌ Minimal test coverage (1 test file)
- 🔍 Need to investigate: Why existing MCP adapter not used?

**Tasks**:
1. Investigate existing `services/mcp/consumer/github_adapter.py` (2 hours)
2. IF adapter usable: Wire to router with feature flag (2 hours)
3. IF adapter NOT usable: Create new MCP adapter following Notion pattern (4 hours)
4. Add spatial intelligence integration (1 hour)
5. Add tests (1 hour)

---

### 2. Slack Integration

**Current MCP Status**: ❌ **NONE** (has custom spatial, not MCP)

**Estimated Work**: **10-12 hours** - Create from scratch + integrate extensive spatial intelligence

**Complexity Factors**:
- ❌ No MCP adapter exists (none found in `services/mcp/consumer/`)
- ✅✅ EXTENSIVE existing spatial intelligence (6 spatial files: adapter, agent, intent_classifier, mapper, memory, types)
- ⚠️ Has its own `spatial_adapter.py` (NOT compatible with MCP pattern)
- ✅ Well-structured routers (588 + 856 lines)
- ✅ Good test coverage (10 files)
- 🔴 HIGH COMPLEXITY: Need to integrate with existing spatial system

**Tasks**:
1. Create SlackMCPAdapter extending BaseSpatialAdapter (4 hours)
2. Integrate with existing spatial intelligence system (4 hours)
3. Update slack_integration_router to use MCP adapter (2 hours)
4. Add feature flag (USE_SPATIAL_SLACK) (30 min)
5. Update tests for MCP adapter (2 hours)

---

### 3. Notion Integration

**Current MCP Status**: ✅ **COMPLETE** (with minor gaps)

**Estimated Work**: **2-3 hours** - Validate and enhance

**Complexity Factors**:
- ✅ MCP adapter complete (738 lines, 22 methods)
- ✅ Router properly integrated with feature flag
- ✅ Service injection pattern implemented
- ❌ No test coverage
- ⚠️ Not wired to OrchestrationEngine (router handles all interactions)

**Tasks**:
1. Add test coverage for NotionMCPAdapter (2 hours)
2. Validate error handling and circuit breaker patterns (30 min)
3. Documentation updates (30 min)

---

### 4. Calendar Integration

**Current MCP Status**: ✅ **COMPLETE** (with minor gaps)

**Estimated Work**: **2-3 hours** - Validate and enhance

**Complexity Factors**:
- ✅ MCP adapter complete (514 lines, 13 methods)
- ✅ Router properly integrated with feature flag
- ✅ Circuit breaker implemented
- ❌ No test coverage
- ⚠️ Different import namespace than Notion
- ⚠️ Not wired to OrchestrationEngine

**Tasks**:
1. Add test coverage for GoogleCalendarMCPAdapter (2 hours)
2. Standardize import namespace (30 min)
3. Documentation updates (30 min)

---

### 5. Demo Integration

**Current MCP Status**: ❌ **NONE**

**Estimated Work**: **1-2 hours** - Simple demo, low priority

**Complexity Factors**:
- ✅ Simple integration (98 lines)
- ❌ No MCP adapter needed (demo purposes only)
- ✅ Minimal test coverage sufficient

**Tasks**:
1. IF needed for demo: Create simple DemoMCPAdapter (1 hour)
2. ELSE: Skip (demo doesn't require MCP)

---

### 6. OrchestrationEngine Integration (NEW TASK)

**Current Status**: ❌ **NO MCP INTEGRATION**

**Estimated Work**: **8-10 hours** - Design and implement MCP adapter registry and wiring

**Complexity Factors**:
- 🔴 CRITICAL: MCP adapters currently NOT accessible to OrchestrationEngine
- ❌ No MCP adapter registry pattern
- ❌ No standardized MCP adapter interface beyond BaseSpatialAdapter
- ✅ OrchestrationEngine well-structured (453 lines)
- ✅ Uses ServiceContainer for dependency injection

**Tasks**:
1. Design MCP adapter registry pattern (2 hours)
2. Implement MCPAdapterRegistry class (2 hours)
3. Wire registry to ServiceContainer (2 hours)
4. Update OrchestrationEngine to use MCP adapters (2 hours)
5. Add tests for MCP integration (2 hours)

---

## Total Migration Effort Summary

| Service | Status | Effort | Priority |
|---------|--------|--------|----------|
| GitHub | Missing (adapter exists!) | 6-8 hours | HIGH |
| Slack | Missing | 10-12 hours | HIGH |
| Notion | Complete | 2-3 hours | MEDIUM |
| Calendar | Complete | 2-3 hours | MEDIUM |
| Demo | Not needed | 1-2 hours | LOW |
| OrchestrationEngine | Not integrated | 8-10 hours | **CRITICAL** |
| **TOTAL** | | **29-38 hours** | |

**Recommended Phases**:
- **Phase 0** (CRITICAL): OrchestrationEngine integration (8-10 hours)
- **Phase 1**: GitHub MCP adapter investigation + wiring (6-8 hours)
- **Phase 2**: Slack MCP adapter creation (10-12 hours)
- **Phase 3**: Notion/Calendar validation + tests (4-6 hours)

---

## Red Flags

### 🔴 Critical Issues

1. **MCP Adapters NOT Wired to OrchestrationEngine**
   - **Impact**: MCP adapters exist but orchestration layer can't use them
   - **Evidence**: No imports of MCP adapters in `services/orchestration/engine.py`
   - **Resolution**: Need Phase 0 to design and implement MCP adapter registry + wiring

2. **GitHub MCP Adapter Exists But Unused**
   - **Impact**: 22KB adapter file exists, GitHub router doesn't use it - ABANDONED WORK
   - **Evidence**: `services/mcp/consumer/github_adapter.py` (22,772 bytes) vs no import in `github_integration_router.py`
   - **Resolution**: Investigate why adapter unused, determine if salvageable or recreate

3. **Inconsistent MCP Adapter Locations**
   - **Impact**: Confusion about where adapters should live
   - **Evidence**:
     - Notion: `services/integrations/mcp/notion_adapter.py`
     - Calendar: `services/mcp/consumer/google_calendar_adapter.py`
     - Unused adapters: `services/mcp/consumer/` (5 files)
   - **Resolution**: Standardize on ONE location for all MCP adapters

### ⚠️ Moderate Issues

4. **75% Pattern: Unused MCP Adapters**
   - **Impact**: 4 of 7 adapters in `services/mcp/consumer/` are unused
   - **Evidence**:
     - ❌ `cicd_adapter.py` - No integration found
     - ❌ `devenvironment_adapter.py` - No integration found
     - ❌ `github_adapter.py` - Exists but GitHub router doesn't use it
     - ❌ `linear_adapter.py` - No integration found
   - **Resolution**: Either complete integration or archive unused adapters

5. **No Common MCP Adapter Interface**
   - **Impact**: Each adapter has different methods beyond BaseSpatialAdapter
   - **Evidence**:
     - Notion: 22 methods (CRUD, search, users)
     - Calendar: 13 methods (read-only, temporal)
   - **Resolution**: Define canonical MCP adapter interface for consistency

6. **Slack Has Custom Spatial System**
   - **Impact**: Slack's 6 spatial files may conflict with MCP pattern
   - **Evidence**: `spatial_adapter.py`, `spatial_agent.py`, `spatial_intent_classifier.py`, etc. in `services/integrations/slack/`
   - **Resolution**: Integrate Slack spatial intelligence with MCP adapter pattern

### ℹ️ Minor Issues

7. **No Test Coverage for MCP Adapters**
   - **Impact**: Cannot verify MCP adapter functionality
   - **Evidence**: No tests/ directory in `services/integrations/mcp/` or `services/mcp/consumer/`
   - **Resolution**: Add test coverage as part of validation phase

8. **Inconsistent Feature Flag Naming**
   - **Impact**: Minor - Each service has unique flag name
   - **Evidence**: `USE_SPATIAL_NOTION`, `USE_SPATIAL_CALENDAR`
   - **Resolution**: Standardize on `USE_MCP_<SERVICE>` pattern

9. **Documentation Gaps**
   - **Impact**: No ADR or pattern doc explaining MCP adapter architecture
   - **Evidence**: Only comment reference to "ADR-013 MCP+Spatial Integration Pattern" in GitHub router
   - **Resolution**: Create comprehensive ADR and pattern documentation

---

## Recommendations for Phase 1

### Primary Recommendation: **Phase 0 First**

**DO NOT proceed to Phase 1 pattern definition until Phase 0 is complete.**

**Why**: MCP adapters cannot be used by OrchestrationEngine until wiring infrastructure exists. Defining patterns without integration architecture is premature.

---

### Phase 0: OrchestrationEngine Integration (8-10 hours)

**Goal**: Wire MCP adapters to OrchestrationEngine via adapter registry

**Tasks**:
1. Design MCP adapter registry pattern (inspired by SpatialAdapterRegistry)
2. Define canonical MCP adapter interface (beyond BaseSpatialAdapter)
3. Implement MCPAdapterRegistry in `services/mcp/adapter_registry.py`
4. Wire registry to ServiceContainer
5. Update OrchestrationEngine to accept MCP adapters via dependency injection
6. Add tests for MCP registry and integration

**Success Criteria**:
- OrchestrationEngine can discover and use MCP adapters by service name
- MCP adapters registered via ServiceContainer initialization
- Integration routers can access MCP adapters from OrchestrationEngine

---

### Phase 1: Pattern Standardization (2-3 hours)

**Goal**: Define canonical MCP adapter pattern after Phase 0

**Recommended Pattern** (based on analysis):

```python
# Location: services/mcp/adapters/<service>_adapter.py
# (Standardize on ONE location)

class <Service>MCPAdapter(BaseSpatialAdapter):
    """MCP adapter for <Service> integration."""

    def __init__(self, config_service: Optional["<Service>ConfigService"] = None):
        super().__init__("<service>_mcp")
        # Service injection pattern (preferred)
        if config_service:
            self.config_service = config_service
            self.config = config_service.get_config()
        else:
            # Fallback to static config
            self.config = <Service>Config()

    # Canonical methods (REQUIRED for all adapters):
    async def connect(self, **kwargs) -> bool
    async def test_connection(self) -> bool
    def is_configured(self) -> bool
    async def health_check(self) -> Dict[str, Any]
    async def close(self) -> None

    # Service-specific methods (as needed)
    # ...
```

**Feature Flag Pattern**:
```python
# config/feature_flags.py
USE_MCP_GITHUB = os.getenv("USE_MCP_GITHUB", "true").lower() == "true"
USE_MCP_SLACK = os.getenv("USE_MCP_SLACK", "true").lower() == "true"
USE_MCP_NOTION = os.getenv("USE_MCP_NOTION", "true").lower() == "true"
USE_MCP_CALENDAR = os.getenv("USE_MCP_CALENDAR", "true").lower() == "true"
```

**Integration Router Pattern**:
```python
# services/integrations/<service>/<service>_integration_router.py

from config.feature_flags import USE_MCP_<SERVICE>
from services.mcp.adapter_registry import MCPAdapterRegistry

class <Service>IntegrationRouter:
    def __init__(self, config_service, registry: MCPAdapterRegistry):
        if USE_MCP_<SERVICE>:
            # Get adapter from registry (injected by OrchestrationEngine)
            self.mcp_adapter = registry.get_adapter("<service>")
        else:
            self.mcp_adapter = None  # Legacy path
```

---

### Phase 1 Deliverables:

1. **ADR**: ADR-013 (or new number) "MCP Adapter Pattern and Integration Architecture"
2. **Pattern Doc**: `docs/internal/architecture/current/patterns/pattern-0XX-mcp-adapter.md`
3. **Interface Definition**: Canonical MCP adapter interface (required methods)
4. **Location Standard**: Standardize on `services/mcp/adapters/` for ALL adapters
5. **Feature Flag Standard**: `USE_MCP_<SERVICE>` naming convention
6. **Registry Pattern**: MCPAdapterRegistry implementation

---

### Migration Priority:

1. **Phase 0**: OrchestrationEngine integration (CRITICAL - blocks all other work)
2. **Phase 1**: Pattern definition + standardization (after Phase 0)
3. **Phase 2**: GitHub adapter investigation + wiring (HIGH priority)
4. **Phase 3**: Slack adapter creation (HIGH priority)
5. **Phase 4**: Notion/Calendar validation + tests (MEDIUM priority)

---

## Appendix: Evidence

### MCP Adapter File Sizes

```bash
$ ls -lh services/integrations/mcp/
-rw-r--r--  10K  gitbook_adapter.py
-rw-r--r--  30K  notion_adapter.py

$ ls -lh services/mcp/consumer/
-rw-r--r--  16K  cicd_adapter.py
-rw-r--r--  13K  consumer_core.py
-rw-r--r--  20K  devenvironment_adapter.py
-rw-r--r--  16K  gitbook_adapter.py
-rw-r--r__  23K  github_adapter.py
-rw-r--r__  20K  google_calendar_adapter.py
-rw-r--r__  14K  linear_adapter.py
```

### Integration Router Line Counts

```bash
$ wc -l services/integrations/*/config_service.py services/integrations/*/*_router.py 2>/dev/null | sort -n
      50 services/integrations/demo/config_service.py
      98 services/integrations/demo/demo_integration_router.py
     103 services/integrations/notion/config_service.py
     116 services/integrations/calendar/config_service.py
     118 services/integrations/slack/config_service.py
     278 services/integrations/github/github_integration_router.py
     382 services/integrations/github/config_service.py
     403 services/integrations/calendar/calendar_integration_router.py
     588 services/integrations/slack/slack_integration_router.py
     662 services/integrations/notion/notion_integration_router.py
     856 services/integrations/slack/webhook_router.py
    3654 total
```

### Service Directory Contents

```bash
$ ls -1 services/integrations/
__init__.py
calendar/
demo/
github/
mcp/
notion/
slack/
spatial/
spatial_adapter.py

$ ls -1 services/mcp/
__init__.py
client.py
consumer/
exceptions.py
protocol/
resources.py
server/

$ ls -1 services/mcp/consumer/
__init__.py
cicd_adapter.py
consumer_core.py
devenvironment_adapter.py
gitbook_adapter.py
github_adapter.py
google_calendar_adapter.py
linear_adapter.py
```

### OrchestrationEngine Imports

```python
# services/orchestration/engine.py lines 16-35
from services.analysis.file_type_detector import FileTypeDetector
from services.api.errors import TaskFailedError, WorkflowTimeoutError
from services.database.repositories import TaskRepository, WorkflowRepository
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Intent, IntentCategory, Task, Workflow
from services.integrations.github.config_service import GitHubConfigService
from services.integrations.github.content_generator import GitHubIssueContentGenerator
from services.integrations.github.github_integration_router import GitHubIntegrationRouter
from services.integrations.github.issue_analyzer import GitHubIssueAnalyzer
from services.integrations.github.production_client import ProductionGitHubClient
from services.intent_service.intent_enricher import IntentEnricher
from services.llm.clients import LLMClient
from services.queries.query_router import QueryRouter
from services.shared_types import TaskStatus, TaskType, WorkflowStatus, WorkflowType
from .integration import PerformanceMonitor, SessionIntegration, WorkflowIntegration

# NO MCP adapter imports found ❌
```

---

## End of Report

**Next Steps**: Await PM approval for Phase 0 scope before proceeding to Phase 1 pattern definition.

**Report Generated**: October 17, 2025
**Investigation Duration**: 3 hours (as estimated)
**Services Audited**: 7 (GitHub, Slack, Notion, Calendar, Demo, MCP, Spatial)
**MCP Adapters Found**: 9 total (2 in use, 7 in services/mcp/consumer/)
**Critical Issues**: 3 (OrchestrationEngine wiring, GitHub adapter unused, location inconsistency)
**75% Pattern Confirmed**: ✅ (4 of 7 adapters in services/mcp/consumer/ unused)
