# ADR-010: Configuration Access Patterns

## Status
**ACCEPTED** - July 21, 2025

## Context

PM-015 Group 2 analysis revealed configuration pattern inconsistency across services that blocks 100% test success rate:

- **MCPResourceManager**: Hybrid ConfigService + environment fallback violates clean architecture principles
- **FileRepository**: Direct `os.getenv()` calls in repository layer violate domain boundaries
- **Test Evidence**: `test_mcp_resource_manager_uses_configuration_service` and `test_file_repository_uses_configuration_service` failing

While achieving 91% test success rate demonstrates architectural robustness, the mixed patterns pose long-term maintainability risks, testing inconsistencies, and developer confusion about configuration access approaches.

**Business Impact**: Configuration inconsistency affects:
- Testing reliability and isolation
- Developer onboarding and patterns adoption
- Maintenance burden across service boundaries
- Architectural pattern enforcement

**Technical Debt**: Two GitHub issues created for systematic resolution:
- Issue #39: MCPResourceManager configuration architecture standardization
- Issue #40: FileRepository environment access cleanup

## Decision

We will implement **Hybrid Configuration Access with Clean Abstractions** using layer-appropriate patterns that balance pragmatism with architectural consistency.

### Layer-Specific Rules

1. **Application/Domain Layers**: Use ConfigService exclusively
   - WorkflowService, IntentService, OrchestrationEngine
   - Business logic requiring configuration decisions
   - All user-facing feature behavior

2. **Infrastructure Layer**: ConfigService preferred, direct environment access allowed for:
   - Feature flags and toggles (`ENABLE_MCP_FILE_SEARCH`)
   - Runtime detection (e.g., MCP availability)
   - Emergency overrides and circuit breakers
   - Container orchestration variables

3. **Testing**: Mock ConfigService, not environment variables
   - Consistent test behavior across environments
   - Elimination of environment-dependent test failures
   - Cleaner test setup and isolation

### Strategic Rationale

- **Pragmatic Balance**: Avoids dependency injection ceremony while maintaining clean boundaries
- **Existing Investment**: Leverages working ConfigService infrastructure without wholesale rewrites
- **Layer Boundaries**: Different layers have different configuration responsibilities and constraints
- **Testing Reality**: Accommodates varied testing needs across architectural layers
- **Gradual Migration**: Enables incremental improvement without breaking existing functionality

## Approved Patterns with Code Examples

### PRIMARY PATTERN - Application/Domain Services

```python
# ✅ APPROVED: Service layer with ConfigService injection
class WorkflowService:
    def __init__(self, config_service: ConfigService):
        self.config = config_service

    async def process_workflow(self, workflow_type: WorkflowType):
        # Application configuration through service
        if self.config.feature_enabled("advanced_workflows"):
            return await self._process_advanced_workflow(workflow_type)
        return await self._process_basic_workflow(workflow_type)

    def get_timeout_config(self) -> int:
        return self.config.get_timeout("workflow_execution", default=300)
```

### INFRASTRUCTURE PATTERN - Repository Layer

```python
# ✅ APPROVED: Repository with ConfigService + infrastructure utilities
from services.infrastructure.config.feature_flags import FeatureFlags

class FileRepository(BaseRepository):
    def __init__(self, session: AsyncSession, config_service: ConfigService):
        super().__init__(session)
        self.config = config_service

    async def search_files_with_content(self, session_id: str, query: str, limit: int = 10):
        # Get database results first (always available)
        filename_matches = await self.search_files_by_name(session_id, query)

        # Infrastructure layer feature detection
        if FeatureFlags.is_mcp_content_search_enabled():
            try:
                return await self._enhanced_mcp_search(session_id, query, filename_matches, limit)
            except Exception as e:
                logger.warning(f"MCP search failed, falling back: {e}")

        return filename_matches[:limit]

    def _get_repository_config(self) -> dict:
        # Repository-specific configuration through ConfigService
        return {
            "cache_ttl": self.config.get_int("file_cache_ttl", 300),
            "max_results": self.config.get_int("max_file_results", 1000)
        }
```

### FEATURE FLAGS UTILITY (New Infrastructure Component)

```python
# ✅ APPROVED: Infrastructure utility for feature flags
# File: services/infrastructure/config/feature_flags.py

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class FeatureFlags:
    """
    Static utility for feature flag access in infrastructure layer.

    Use this for infrastructure-level toggles, runtime detection,
    and emergency overrides. Application logic should use ConfigService.
    """

    @staticmethod
    def is_mcp_content_search_enabled() -> bool:
        """Check if MCP content search is enabled"""
        return FeatureFlags._get_boolean_flag("ENABLE_MCP_FILE_SEARCH", False)

    @staticmethod
    def is_mcp_connection_pooling_enabled() -> bool:
        """Check if MCP connection pooling is enabled"""
        return FeatureFlags._get_boolean_flag("USE_MCP_POOL", False)

    @staticmethod
    def is_debug_mode_enabled() -> bool:
        """Check if debug mode is enabled (infrastructure logging)"""
        return FeatureFlags._get_boolean_flag("DEBUG", False)

    @staticmethod
    def get_max_connection_pool_size() -> int:
        """Get infrastructure connection pool configuration"""
        return FeatureFlags._get_int_flag("MAX_CONNECTION_POOL_SIZE", 5)

    @staticmethod
    def _get_boolean_flag(flag_name: str, default: bool = False) -> bool:
        """Internal: Get boolean environment variable"""
        value = os.getenv(flag_name, str(default)).lower()
        return value in ("true", "1", "yes", "on")

    @staticmethod
    def _get_int_flag(flag_name: str, default: int) -> int:
        """Internal: Get integer environment variable"""
        try:
            return int(os.getenv(flag_name, str(default)))
        except (ValueError, TypeError):
            logger.warning(f"Invalid integer value for {flag_name}, using default {default}")
            return default
```

### ENHANCED CONFIGSERVICE PATTERN

```python
# ✅ APPROVED: Enhanced ConfigService usage
class MCPResourceManager:
    def __init__(self, client_config: Optional[Dict[str, Any]] = None,
                 config_service: Optional[ConfigService] = None):
        self.client_config = client_config or self._get_default_client_config()
        self.config_service = config_service or get_config_service()

        # Application configuration through service
        self.cache_ttl = self.config_service.get_int("mcp_cache_ttl", 300)
        self.timeout = self.config_service.get_float("mcp_timeout", 5.0)

        # Infrastructure feature detection
        self.use_connection_pool = (
            FeatureFlags.is_mcp_connection_pooling_enabled() and
            self._is_pool_infrastructure_available()
        )

    def _get_default_client_config(self) -> Dict[str, Any]:
        # Configuration service for application config
        return {
            "url": self.config_service.get_string("mcp_server_url", "stdio://./scripts/mcp_file_server.py"),
            "timeout": self.config_service.get_float("mcp_timeout", 5.0)
        }

    def _is_pool_infrastructure_available(self) -> bool:
        # Infrastructure runtime detection
        try:
            from services.infrastructure.mcp.connection_pool import MCPConnectionPool
            return True
        except ImportError:
            return False
```

## Counter-Examples (What NOT to Do)

### ❌ AVOID: Direct environment access in domain/application layers

```python
# ❌ BAD: Domain service accessing environment directly
class WorkflowService:
    async def process_workflow(self, workflow_type: WorkflowType):
        # This violates layer boundaries - domain logic shouldn't know about environment
        if os.getenv("ENABLE_ADVANCED_WORKFLOWS", "false").lower() == "true":
            return await self._process_advanced_workflow(workflow_type)
        return await self._process_basic_workflow(workflow_type)
```

### ❌ AVOID: Mixed patterns in same service

```python
# ❌ BAD: Inconsistent configuration access
class MCPResourceManager:
    def __init__(self):
        # Sometimes use ConfigService
        if CONFIG_SERVICE_AVAILABLE:
            config = get_config()
            self.timeout = config.mcp_timeout
        else:
            # Sometimes use environment - creates confusion and testing issues
            self.timeout = float(os.getenv("MCP_TIMEOUT", "5.0"))
            self.use_pool = os.getenv("USE_MCP_POOL", "false").lower() == "true"
```

### ❌ AVOID: Testing environment variables directly

```python
# ❌ BAD: Environment patching in tests creates brittle, environment-dependent tests
@pytest.fixture
def test_with_mcp_enabled():
    original = os.environ.get("ENABLE_MCP_FILE_SEARCH")
    os.environ["ENABLE_MCP_FILE_SEARCH"] = "true"
    yield
    if original is None:
        del os.environ["ENABLE_MCP_FILE_SEARCH"]
    else:
        os.environ["ENABLE_MCP_FILE_SEARCH"] = original

def test_mcp_search_enabled(test_with_mcp_enabled):
    # Test becomes environment-dependent and brittle
    result = repository.search_files_with_content("session", "query")
```

### ✅ CORRECT: Mock configuration service

```python
# ✅ GOOD: Test configuration behavior through service mocking
@pytest.fixture
def mock_config_with_mcp_enabled():
    mock_config = Mock(spec=ConfigService)
    mock_config.feature_enabled.return_value = True
    mock_config.get_int.return_value = 300
    return mock_config

def test_mcp_search_enabled(mock_config_with_mcp_enabled):
    # Clean, predictable test that focuses on behavior
    repository = FileRepository(session, mock_config_with_mcp_enabled)
    result = await repository.search_files_with_content("session", "query")
    assert len(result) > 0
```

## Migration Strategy

### Phase 1: Document and Establish Patterns (This Week - July 21-25) ✅ COMPLETE

- ✅ Create ADR-010 with approved patterns and examples - COMPLETE (July 21, 2025)
- ✅ FeatureFlags utility implementation - COMPLETE (July 22, 2025, PM-015 Group 3)
- ✅ Configuration pattern standardization - COMPLETE (July 22, 2025)
- ✅ Migration foundation established - Ready for Phase 2 implementation
- ✅ PM-015 Group 3 systematic completion - All architectural decisions documented

### Phase 2: Gradual Service Migration (Next 2 Weeks - July 28 - August 8)

**Priority 1: MCPResourceManager** (GitHub Issue #39)
- **Complexity**: Low-Medium (self-contained service)
- **Approach**:
  - Extract feature flag logic to FeatureFlags utility
  - Inject ConfigService for application configuration (timeouts, URLs)
  - Update tests to mock ConfigService instead of patching environment
  - Maintain backward compatibility during transition

**Priority 2: FileRepository** (GitHub Issue #40)
- **Complexity**: Medium-High (touches domain boundaries)
- **Approach**:
  - Extract infrastructure feature detection to FeatureFlags utility
  - Inject ConfigService for repository configuration (cache settings, limits)
  - Ensure domain purity through clean service injection
  - Update FileQueryService and other consumers as needed

### Phase 3: Enforcement and Automation (August 2025)

- Add linting rules against direct `os.getenv` in `services/domain/` and `services/orchestration/`
- Update code review checklist with configuration pattern verification
- Add configuration pattern examples to new developer documentation
- Create automated tests to verify configuration pattern adherence

## ConfigService vs Environment Variables Guidelines

### ConfigService Should Handle:

- **Application behavior configuration**: Feature toggles affecting business logic
- **User-facing features**: Settings that change user experience
- **Business logic parameters**: Timeouts, limits, thresholds for workflows
- **Integration endpoints**: API URLs, service discovery
- **Quality of service**: Performance tuning parameters

### Direct Environment Access Allowed For:

- **Infrastructure runtime detection**: Service availability, capability detection
- **Emergency overrides**: Circuit breakers, kill switches
- **Development/debugging flags**: Logging levels, debug modes
- **Container orchestration**: Port bindings, health check intervals
- **Security credentials**: When used through proper credential utilities

### Migration Checklist Template

For each service requiring configuration updates:

**Analysis Phase:**
- [ ] **Inventory current patterns**: Document all configuration access points
- [ ] **Categorize by layer**: Application logic vs infrastructure concerns
- [ ] **Identify test dependencies**: Which tests patch environment variables?
- [ ] **Map configuration types**: Feature flags vs application config vs credentials

**Implementation Phase:**
- [ ] **Create/update ConfigService injection**: Constructor parameter for application config
- [ ] **Extract feature flags**: Move infrastructure toggles to FeatureFlags utility
- [ ] **Update tests**: Replace environment patching with ConfigService mocking
- [ ] **Verify backward compatibility**: Ensure existing behavior preserved
- [ ] **Update documentation**: Service-specific configuration examples

**Validation Phase:**
- [ ] **Test isolation verified**: No environment variable dependencies in tests
- [ ] **Configuration consistency**: Service follows approved patterns
- [ ] **Performance impact**: No degradation from configuration changes
- [ ] **Developer experience**: Configuration easier to understand and modify

## Success Metrics and Validation

### Technical Metrics

- **Configuration Consistency Score**: 100% of services following approved patterns by August 2025
- **Test Reliability**: Zero environment-dependent test failures post-migration
- **Developer Velocity**: <15 minutes to implement configuration in new services
- **Production Stability**: Zero incidents related to configuration pattern issues

### Implementation Tracking

**GitHub Issues Progress:**
- **Issue #39 (MCPResourceManager)**: Ready for Phase 2 implementation (Week 2)
- **Issue #40 (FileRepository)**: Ready for Phase 2 implementation (Week 2)
- **Pattern Compliance**: ADR-010 foundation complete, ready for service migration
- **Foundation Sprint Impact**: All architectural decisions documented and approved

**Test Health Validation:**
- `test_mcp_resource_manager_uses_configuration_service`: Must pass after Issue #39
- `test_file_repository_uses_configuration_service`: Must pass after Issue #40
- PM-015 overall success rate: Target 100% (currently 91%)

### Quality Assurance

**Code Review Verification:**
- All configuration access follows layer-appropriate patterns
- No direct `os.getenv()` in application/domain layers without justification
- Tests mock ConfigService rather than patching environment
- New services include configuration pattern documentation

**Automated Enforcement:**
- Linting rules prevent regression to anti-patterns
- CI/CD pipeline validates configuration pattern compliance
- Test suite includes pattern adherence verification

### Long-term Benefits

**Developer Experience:**
- Consistent configuration patterns across all services
- Clear guidelines for feature flag vs application config decisions
- Improved test reliability and isolation
- Reduced onboarding time for configuration concepts

**Architectural Health:**
- Clean separation of concerns across layers
- Maintainable configuration management at scale
- Foundation for advanced configuration features (hot reload, environment-specific overrides)
- Technical debt elimination and prevention

## Related Documents

- **GitHub Issues**: #39 (MCPResourceManager), #40 (FileRepository)
- **Parent Issue**: PM-015 Test Infrastructure Isolation Fix (#29)
- **Implementation Tracking**: Foundation & Cleanup Sprint (July 21-25, 2025)
- **Architecture Patterns**: `docs/architecture/pattern-catalog.md`
- **Configuration Service**: `services/infrastructure/config/mcp_configuration.py`

---

**Decision Rationale**: This ADR provides the architectural foundation needed to eliminate configuration-related technical debt while supporting the pragmatic needs of different service layers. The hybrid approach balances architectural purity with development productivity, ensuring long-term maintainability without requiring disruptive wholesale rewrites.

**Next Steps**: Implement FeatureFlags utility, update pattern catalog, and begin Phase 2 service migrations per GitHub issues #39 and #40.
