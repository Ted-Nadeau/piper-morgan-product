# Router Pattern Architecture

**Status**: Implemented and Locked (CORE-QUERY-1 Phase 4-6)
**Last Updated**: 2025-09-29
**Maintainers**: Architecture Team

## Overview

The Router Pattern provides a unified abstraction layer over external integrations, enabling feature flag control and spatial intelligence capabilities while maintaining backward compatibility. This architecture was established during CORE-QUERY-1 to address direct adapter coupling and enable feature-driven integration control.

## Architecture

### Integration Routers

Three integration routers provide complete abstraction with 100% method compatibility:

#### 1. CalendarIntegrationRouter
- **Abstraction**: GoogleCalendarMCPAdapter
- **Methods**: 12/12 (100% complete)
- **Feature Flags**: `USE_SPATIAL_CALENDAR`, `ALLOW_LEGACY_CALENDAR`
- **Location**: `services/integrations/calendar/calendar_integration_router.py`

#### 2. NotionIntegrationRouter
- **Abstraction**: NotionMCPAdapter
- **Methods**: 22/22 (100% complete)
- **Feature Flags**: `USE_SPATIAL_NOTION`, `ALLOW_LEGACY_NOTION`
- **Location**: `services/integrations/notion/notion_integration_router.py`

#### 3. SlackIntegrationRouter
- **Abstraction**: SlackSpatialAdapter + SlackClient (dual-component)
- **Methods**: 15/15 (100% complete)
- **Feature Flags**: `USE_SPATIAL_SLACK`, `ALLOW_LEGACY_SLACK`
- **Location**: `services/integrations/slack/slack_integration_router.py`

### Feature Flag Control

Each router respects environment-based feature flags for spatial intelligence control:

| Integration | Spatial Flag | Legacy Flag | Default Behavior |
|------------|--------------|-------------|------------------|
| Calendar | `USE_SPATIAL_CALENDAR` | `ALLOW_LEGACY_CALENDAR` | Spatial enabled |
| Notion | `USE_SPATIAL_NOTION` | `ALLOW_LEGACY_NOTION` | Spatial enabled |
| Slack | `USE_SPATIAL_SLACK` | `ALLOW_LEGACY_SLACK` | Spatial enabled |

**Flag Values**: `true`, `1`, `yes`, `on`, `enabled` (case-insensitive)

### Router Implementation Pattern

```python
from services.infrastructure.config.feature_flags import FeatureFlags

class IntegrationRouter(BaseSpatialAdapter):
    """Base pattern for integration routers"""

    def __init__(self, config_service=None):
        super().__init__(config_service)
        self.use_spatial = FeatureFlags.should_use_spatial_[integration]()
        self.allow_legacy = FeatureFlags.is_legacy_[integration]_allowed()

        # Initialize spatial integration
        if self.use_spatial:
            self.spatial_integration = SpatialAdapter()

        # Initialize legacy integration if allowed
        if self.allow_legacy:
            self.legacy_integration = LegacyAdapter()

    def _get_preferred_integration(self, operation: str) -> Tuple[Optional[Any], bool]:
        """Get preferred integration based on feature flags"""
        # Try spatial first
        if self.use_spatial and self.spatial_integration:
            return self.spatial_integration, False

        # Fall back to legacy if allowed
        elif self.allow_legacy and self.legacy_integration:
            return self.legacy_integration, True

        # No integration available
        else:
            return None, False

    async def method_name(self, *args, **kwargs):
        """Delegate method calls to preferred integration"""
        integration, is_legacy = self._get_preferred_integration("method_name")

        if integration:
            self._warn_deprecation_if_needed("method_name", is_legacy)
            return await integration.method_name(*args, **kwargs)
        else:
            raise RuntimeError(f"No integration available for method_name")
```

## Service Migration Pattern

### Before Migration (Direct Import)
```python
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

class SomeService:
    def __init__(self):
        self.calendar = GoogleCalendarMCPAdapter()

    async def get_events(self):
        return await self.calendar.get_events()
```

### After Migration (Router Pattern)
```python
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

class SomeService:
    def __init__(self):
        self.calendar = CalendarIntegrationRouter()

    async def get_events(self):
        # Same method call - router handles delegation transparently
        return await self.calendar.get_events()
```

**Key Point**: Method calls remain identical. The router provides a drop-in replacement with transparent delegation.

## Architectural Protection

### Pre-Commit Hooks

**Hook**: `prevent-direct-adapter-imports`
- **Script**: `scripts/check_direct_imports.py`
- **Enforcement**: Blocks direct adapter imports before commit
- **Coverage**: All service files (excludes internal router implementations)

**Prohibited Patterns**:
- `from services.mcp.consumer.google_calendar_adapter import`
- `from services.integrations.mcp.notion_adapter import`
- `from services.integrations.slack.spatial_adapter import`
- `from services.integrations.slack.slack_client import`

### CI/CD Checks

**GitHub Actions Workflow**: `.github/workflows/router-enforcement.yml`

**Jobs**:
1. **architectural-protection** - Detects direct adapter imports
2. **router-completeness** - Verifies router method completeness
3. **integration-architecture** - Tests feature flag behavior

### Automated Enforcement

The architecture is protected at three levels:

1. **Development**: Pre-commit hooks prevent accidental violations
2. **Code Review**: CI/CD checks enforce patterns in PRs
3. **Documentation**: Clear migration guides prevent confusion

## Implementation History

### Phase 1: Router Design (CORE-GREAT-2B)
- Established GitHubIntegrationRouter pattern
- Defined feature flag architecture
- Created delegation pattern

### Phase 2: Router Development (CORE-QUERY-1 Phase 1-3)
- Implemented CalendarIntegrationRouter (12 methods)
- Implemented NotionIntegrationRouter (22 methods)
- Implemented SlackIntegrationRouter (15 methods, dual-component)

### Phase 3: Router Completion (CORE-QUERY-1 Phase 1-3)
- Verified 100% method compatibility for all routers
- Added missing spatial intelligence methods
- Corrected Phase 4A incomplete router (58.3% → 100%)

### Phase 4: Service Migration (CORE-QUERY-1 Phase 4A-C)
- **Phase 4A**: Migrated Calendar services (2 services)
  - canonical_handlers.py
  - morning_standup.py (2 locations)
- **Phase 4B**: Migrated Notion services (3 services)
  - notion_domain_service.py
  - publisher.py
  - notion_spatial.py
- **Phase 4C**: Migrated Slack services (1 service)
  - webhook_router.py

### Phase 5: Testing & Validation (CORE-QUERY-1 Phase 5)
- Feature flag testing: 100% pass rate (3/3 routers)
- Completeness verification: 49/49 methods (100%)
- Architectural protection: 0 violations (6/6 services clean)

### Phase 6: Lock & Document (CORE-QUERY-1 Phase 6)
- Added pre-commit hooks for automated protection
- Created GitHub Actions workflow for CI/CD enforcement
- Documented router patterns comprehensively
- Locked architecture with automated enforcement

## Benefits

### 1. Feature Flag Control
Enable or disable spatial intelligence per integration without code changes:
```bash
# Enable spatial calendar
export USE_SPATIAL_CALENDAR=true

# Disable spatial notion
export USE_SPATIAL_NOTION=false

# Enable legacy slack fallback
export ALLOW_LEGACY_SLACK=true
```

### 2. Backward Compatibility
Legacy mode support where needed, with deprecation warnings to guide migration.

### 3. Uniform Interface
Consistent API across all integrations simplifies service development:
```python
# All routers follow same pattern
calendar = CalendarIntegrationRouter()
notion = NotionIntegrationRouter()
slack = SlackIntegrationRouter()

# Same method patterns
await calendar.get_events()
await notion.get_database(db_id)
await slack.send_message(channel, text)
```

### 4. Spatial Intelligence
Built-in spatial adapter coordination for 8-dimensional spatial analysis:
- Territory mapping (team/workspace level)
- Room tracking (channel/page level)
- Path navigation (thread/hierarchy level)
- Attention management (priority/focus level)
- Temporal awareness (time/scheduling level)
- Emotional context (sentiment/reaction level)
- Significance tracking (importance level)
- Inhabitant awareness (user/member level)

### 5. Architectural Protection
Automated enforcement prevents regression to direct imports:
- Pre-commit hooks block violations during development
- CI/CD checks enforce patterns in pull requests
- Documentation guides proper usage

## Testing

### Feature Flag Testing
All routers tested with multiple flag combinations:
- Spatial mode enabled (default)
- Spatial mode disabled
- Legacy mode enabled (Slack only)
- Method delegation verification

**Results**: 100% pass rate across all routers

### Completeness Testing
All routers verified for 100% method compatibility:
- Calendar: 12/12 methods
- Notion: 22/22 methods
- Slack: 15/15 methods (dual-component)

**Results**: 49/49 total methods (100% complete)

### Architectural Protection Testing
All migrated services verified clean:
- No direct adapter imports detected
- All router imports present and correct
- Architecture protection confirmed

**Results**: 6/6 services clean (0 violations)

## Troubleshooting

### "Integration not available" Error
**Cause**: All integration modes disabled via feature flags
**Solution**: Enable at least one mode:
```bash
export USE_SPATIAL_CALENDAR=true
# or
export ALLOW_LEGACY_CALENDAR=true
```

### "Direct adapter import detected" Error
**Cause**: Using direct adapter import instead of router
**Solution**: Replace with router import:
```python
# ❌ Wrong
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

# ✅ Correct
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
```

### Pre-Commit Hook Failure
**Cause**: Direct adapter import in staged files
**Solution**: Migrate service to router pattern (see migration guide)

## Future Extensions

The router pattern can be extended for:

1. **New Integration Types**
   - Additional external services (Jira, Confluence, etc.)
   - Following established router pattern

2. **Enhanced Feature Flag Granularity**
   - Method-level feature flags
   - User-specific feature flags
   - Dynamic feature flag updates

3. **Advanced Spatial Intelligence**
   - Multi-dimensional analysis
   - Cross-integration spatial mapping
   - Temporal-spatial correlation

4. **Performance Optimization**
   - Connection pooling
   - Caching layers
   - Async batch operations

5. **Observability**
   - Router-level metrics
   - Feature flag usage tracking
   - Integration health monitoring

## Related Documentation

- [Migration Guide](../migration/router-migration-guide.md) - Step-by-step migration instructions
- [Feature Flags](../../services/infrastructure/config/feature_flags.py) - Feature flag implementation
- [ADR-039](../internal/architecture/current/adrs/adr-039-slack-integration-router.md) - Slack router architecture decision

## Maintenance

**Review Frequency**: Quarterly
**Owner**: Architecture Team
**Last Review**: 2025-09-29
**Next Review**: 2025-12-29

When extending this pattern:
1. Verify 100% method compatibility before migration
2. Add feature flags following established naming convention
3. Update pre-commit hooks for new integration types
4. Document architectural decisions in ADRs
5. Update this guide with new patterns

---

**Version**: 1.0
**Established**: 2025-09-29 (CORE-QUERY-1 Phase 6)
**Status**: Locked with automated enforcement
