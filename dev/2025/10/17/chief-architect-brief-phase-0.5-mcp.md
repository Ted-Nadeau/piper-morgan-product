# Chief Architect Brief: Phase 0.5 MCP Integration Architecture

**From**: Lead Developer
**To**: Chief Architect
**Date**: October 17, 2025, 1:35 PM
**Re**: MCP Migration Phase 0.5 - Architectural Decisions Required
**Sprint**: A3 (CORE-MCP-MIGRATION #198)

---

## Executive Summary

Phase -1 discovery revealed **MCP adapters exist but aren't wired to OrchestrationEngine**. This is a blocking architectural issue requiring foundational infrastructure (Phase 0.5) before we can proceed with pattern standardization (Phase 1) or parallel implementation (Phase 2).

**Key Discovery**: 7 MCP adapters exist in codebase, but only 2 are actively used, and none are accessible to OrchestrationEngine for orchestration-level decisions. They work only at individual router level.

**Request**: Architectural guidance on registry design, interface definition, and dependency injection pattern for Phase 0.5 implementation.

---

## Phase -1 Discoveries (Evidence-Based)

### Current State: MCP Adapters Exist But Isolated

**What We Have**:
```
✅ NotionMCPAdapter (738 lines, 22 methods) - Active, router-level only
✅ GoogleCalendarMCPAdapter (514 lines, 13 methods) - Active, router-level only
⚠️ GitHubAdapter (23KB) - EXISTS but unused by GitHub router
❌ 4 more adapters - Exist but completely unused (CICD, DevEnv, Linear, GitBook)
```

**Evidence of Isolation**:
```bash
$ grep -r "NotionMCPAdapter\|GoogleCalendarMCPAdapter" services/orchestration/ --include="*.py"
# NO RESULTS - MCP adapters NOT imported by OrchestrationEngine
```

**Current Integration Pattern** (Router-Level Only):
```python
# services/integrations/notion/notion_integration_router.py
from services.integrations.mcp.notion_adapter import NotionMCPAdapter

class NotionIntegrationRouter:
    def __init__(self, config_service):
        if USE_SPATIAL_NOTION:
            self.spatial_notion = NotionMCPAdapter(config_service)
        # Router uses adapter internally
        # OrchestrationEngine never sees the adapter
```

**OrchestrationEngine Current Pattern** (Direct Router Import):
```python
# services/orchestration/engine.py lines 23-30
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

async def _execute_github_action_task(self, task: Task, ...) -> Dict[str, Any]:
    github_agent = GitHubIntegrationRouter()
    # Direct instantiation - no awareness of MCP adapters
```

### Location Inconsistency

**MCP adapters scattered across TWO locations**:
- `services/integrations/mcp/` → Notion, GitBook
- `services/mcp/consumer/` → GitHub, Calendar, CICD, DevEnv, Linear, GitBook (duplicate!)

This inconsistency will be resolved in Phase 1, but we need Phase 0.5 infrastructure first.

---

## Phase 0.5 Requirements

### Goal
Enable OrchestrationEngine to **discover, access, and orchestrate** MCP adapters for cross-service decision-making and workflow coordination.

### Success Criteria
1. OrchestrationEngine can discover MCP adapters by service name
2. Adapters registered during ServiceContainer initialization
3. Integration routers can access adapters from central registry
4. Pattern supports future adapter additions without OrchestrationEngine changes
5. Backward compatibility maintained during transition

### Core Components Needed
1. **MCPAdapterRegistry** - Central adapter registry
2. **Canonical MCP Interface** - Required methods all adapters must implement
3. **ServiceContainer Integration** - Adapter registration at startup
4. **OrchestrationEngine Enhancement** - Adapter injection and usage
5. **Tests** - Registry, injection, and integration tests

---

## Architectural Questions for Chief Architect

### 1. Registry Architecture Pattern

**Question**: Should MCPAdapterRegistry follow the SpatialAdapterRegistry pattern?

**Context**: The Phase -1 report mentions "inspired by SpatialAdapterRegistry" but I haven't located this component.

**Need to Know**:
- Does SpatialAdapterRegistry exist? Where?
- If it exists, should we follow its pattern exactly?
- If it doesn't exist, what registry pattern do you recommend?
- Should the registry be a singleton or injected dependency?

**Proposed Pattern** (pending your guidance):
```python
# services/mcp/adapter_registry.py

class MCPAdapterRegistry:
    """Central registry for MCP adapters."""

    def __init__(self):
        self._adapters: Dict[str, BaseSpatialAdapter] = {}
        self._lock = asyncio.Lock()

    async def register(self, service_name: str, adapter: BaseSpatialAdapter) -> None:
        """Register an MCP adapter for a service."""
        async with self._lock:
            self._adapters[service_name] = adapter

    def get_adapter(self, service_name: str) -> Optional[BaseSpatialAdapter]:
        """Get adapter by service name."""
        return self._adapters.get(service_name)

    def list_adapters(self) -> List[str]:
        """List all registered service names."""
        return list(self._adapters.keys())

    async def health_check_all(self) -> Dict[str, Any]:
        """Check health of all registered adapters."""
        # Implementation
```

**Your Input Needed**:
- Is this pattern aligned with existing architecture?
- Should we support adapter lifecycle management (initialize, close)?
- Should we support adapter hot-swapping for testing?

---

### 2. Canonical MCP Adapter Interface

**Question**: What methods should ALL MCP adapters be required to implement?

**Context**: Current adapters extend BaseSpatialAdapter (276 lines) but add service-specific methods. We need to define the universal contract.

**Current BaseSpatialAdapter** (from Phase -1):
```python
class BaseSpatialAdapter(ABC):
    def __init__(self, system_name: str):
        self.system_name = system_name
        self._position_counter = 0
        self._mappings: Dict[str, SpatialPosition] = {}

    # Spatial-specific methods (15+ methods for position mapping)
    # No MCP-specific contract defined
```

**Proposed Canonical Interface** (pending your guidance):
```python
class IMCPAdapter(Protocol):
    """Canonical MCP adapter interface.

    All MCP adapters MUST implement these methods for orchestration.
    """

    # Connection & Health
    async def connect(self, **kwargs) -> bool
    async def test_connection(self) -> bool
    def is_configured(self) -> bool
    async def health_check(self) -> Dict[str, Any]
    async def close(self) -> None

    # Service Identity
    @property
    def service_name(self) -> str

    @property
    def adapter_version(self) -> str

    # Optional: Tool Discovery
    def get_available_tools(self) -> List[str]
    def get_tool_schema(self, tool_name: str) -> Dict[str, Any]
```

**Your Input Needed**:
- Should this be a Protocol, ABC, or both?
- Should we separate IMCPAdapter from BaseSpatialAdapter?
- Are spatial methods required for ALL adapters, or optional?
- Should adapters expose "tools" for orchestration discovery?

---

### 3. ServiceContainer Integration Pattern

**Question**: How should adapters be registered in ServiceContainer initialization?

**Context**: ServiceContainer is used in main.py but I need guidance on registration pattern.

**Current ServiceContainer Usage** (from main.py):
```python
async def main():
    from services.container import ServiceContainer
    container = ServiceContainer()
    await container.initialize()
    # Container initialization happens here
```

**Proposed Registration Pattern** (pending your guidance):
```python
# services/container.py

class ServiceContainer:
    async def initialize(self):
        # ... existing initialization ...

        # NEW: Initialize MCP adapter registry
        self.mcp_registry = MCPAdapterRegistry()

        # NEW: Register adapters if configured
        if USE_MCP_NOTION:
            notion_config = NotionConfigService()
            notion_adapter = NotionMCPAdapter(notion_config)
            await self.mcp_registry.register("notion", notion_adapter)

        if USE_MCP_CALENDAR:
            calendar_config = CalendarConfigService()
            calendar_adapter = GoogleCalendarMCPAdapter(calendar_config)
            await self.mcp_registry.register("calendar", calendar_adapter)

        # Similar for GitHub, Slack when ready
```

**Your Input Needed**:
- Is this the right place for adapter registration?
- Should adapters be lazy-loaded or initialized at startup?
- How should we handle adapter initialization failures?
- Should ServiceContainer expose `get_mcp_adapter(service_name)` method?

---

### 4. OrchestrationEngine Dependency Injection

**Question**: How should OrchestrationEngine receive and use the adapter registry?

**Context**: OrchestrationEngine currently instantiates routers directly. We need to inject the registry while maintaining backward compatibility.

**Proposed Pattern** (pending your guidance):

**Option A: Constructor Injection**
```python
class OrchestrationEngine:
    def __init__(self, mcp_registry: Optional[MCPAdapterRegistry] = None):
        self.mcp_registry = mcp_registry
        # Existing initialization

    async def _execute_github_action_task(self, task: Task, ...) -> Dict[str, Any]:
        # NEW: Try MCP adapter first
        if self.mcp_registry:
            github_adapter = self.mcp_registry.get_adapter("github")
            if github_adapter and github_adapter.is_configured():
                # Use adapter for orchestration-level operations
                pass

        # FALLBACK: Use existing router pattern
        github_agent = GitHubIntegrationRouter()
        # Existing logic
```

**Option B: ServiceContainer Method**
```python
class OrchestrationEngine:
    def __init__(self, service_container: ServiceContainer):
        self.container = service_container

    async def _execute_task(self, task: Task, ...) -> Dict[str, Any]:
        adapter = self.container.get_mcp_adapter(task.service_name)
        if adapter:
            # Use adapter
        else:
            # Fall back to router
```

**Your Input Needed**:
- Which injection pattern aligns with existing architecture?
- Should OrchestrationEngine own adapter selection logic?
- How do we maintain backward compatibility with routers?
- Should we phase out direct router imports?

---

### 5. Backward Compatibility Strategy

**Question**: How do we ensure existing router functionality continues working during and after Phase 0.5?

**Context**: Notion and Calendar routers currently use MCP adapters internally. GitHub and Slack use direct implementation. All must continue working.

**Proposed Strategy** (pending your guidance):

**Phase 0.5 (This sprint)**:
- Add registry infrastructure without changing existing routers
- OrchestrationEngine gains registry awareness but falls back to routers
- No breaking changes to working integrations

**Phase 1 (Next)**:
- Standardize adapter locations and patterns
- Routers begin using registry instead of direct imports
- Feature flags control transition

**Phase 2+ (Future)**:
- Gradually migrate routers to registry pattern
- Deprecate direct adapter imports
- Full orchestration-level MCP usage

**Your Input Needed**:
- Is this phased approach appropriate?
- Should routers continue to own adapters or delegate to registry?
- How do we handle routers that don't have MCP adapters yet (Slack)?
- ADR needed for backward compatibility guarantees?

---

## Recommended Deliverables for Phase 0.5

Based on your architectural guidance, Phase 0.5 should produce:

1. **ADR-0XX**: "MCP Adapter Registry and Orchestration Integration"
   - Registry pattern decision
   - Interface definition
   - Dependency injection approach
   - Backward compatibility guarantees

2. **Implementation**:
   - `services/mcp/adapter_registry.py` (MCPAdapterRegistry)
   - `services/mcp/interfaces.py` (IMCPAdapter protocol/interface)
   - `services/container.py` updates (adapter registration)
   - `services/orchestration/engine.py` updates (registry injection)

3. **Tests**:
   - `tests/mcp/test_adapter_registry.py` (registry operations)
   - `tests/integration/test_mcp_orchestration.py` (end-to-end)

4. **Documentation**:
   - Pattern doc: `docs/internal/architecture/current/patterns/pattern-0XX-mcp-registry.md`
   - Integration guide for future adapters

---

## Effort Estimate

**Phase 0.5 Duration**: 8-10 hours (from Phase -1 assessment)

**Breakdown**:
- Registry design & implementation: 3-4 hours
- ServiceContainer integration: 2 hours
- OrchestrationEngine enhancement: 2-3 hours
- Tests: 2-3 hours
- Documentation: 1 hour

**Complexity**: Medium-High (foundational architecture)
**Risk**: Medium (affects all integrations, but backward compatible)

---

## Request for Chief Architect

**Immediate Need**:
1. Review Phase -1 discoveries (full report available)
2. Answer the 5 architectural questions above
3. Approve/revise proposed patterns
4. Provide any additional architectural constraints or requirements

**Delivery Format**:
- Brief responses to each question (can be inline in this doc)
- Approval to proceed with Phase 0.5 implementation
- Any ADR drafts or pattern references I should review

**Timeline**:
- Awaiting your guidance to proceed
- Phase 0.5 execution can begin immediately after architectural decisions
- Estimated completion: 8-10 hours after guidance received

---

## Supporting Evidence

**Full Phase -1 Report**: Available at `dev/2025/10/17/phase-minus-1-mcp-discovery-report.md` (1,115 lines)

**Key Evidence**:
- Service inventory with MCP status (all 4+ integrations)
- Existing MCP adapter analysis (Notion, Calendar patterns)
- OrchestrationEngine import analysis (no MCP awareness)
- Infrastructure verification (port, paths, ServiceContainer)
- 75% pattern confirmation (7 adapters, 2 used)

**Discovery Duration**: 3 hours (as estimated)
**Services Audited**: 7 (GitHub, Slack, Notion, Calendar, Demo, MCP, Spatial)
**Critical Issues Found**: 3 (wiring, GitHub unused, location inconsistency)

---

## Appendix: Example Registry Usage (Proposed)

**After Phase 0.5, orchestration code could look like**:

```python
# services/orchestration/engine.py

async def _execute_cross_service_workflow(self, workflow: Workflow) -> Dict[str, Any]:
    """Example: Orchestrate across multiple services."""

    # Discover available adapters
    available_services = self.mcp_registry.list_adapters()

    # Get specific adapters for workflow
    github_adapter = self.mcp_registry.get_adapter("github")
    notion_adapter = self.mcp_registry.get_adapter("notion")

    # Check health before proceeding
    health = await self.mcp_registry.health_check_all()

    # Use adapters for orchestration-level decisions
    if github_adapter and github_adapter.is_configured():
        issue_data = await github_adapter.get_issue(workflow.issue_id)

        if notion_adapter and notion_adapter.is_configured():
            # Cross-service orchestration
            await notion_adapter.create_page(
                parent_id=workflow.notion_db,
                properties=self._transform_issue_to_notion(issue_data)
            )

    # Result: True cross-service orchestration
```

**This is currently impossible** because OrchestrationEngine has no adapter access.

---

**End of Brief**

Thank you for your architectural guidance! Ready to execute Phase 0.5 upon approval.

**— Lead Developer**
October 17, 2025, 1:45 PM
