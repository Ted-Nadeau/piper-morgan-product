# GitHub Integration Deprecation Plan - MCP+Spatial Migration

**Date:** August 12, 2025
**Status:** Phase 0 Investigation Complete
**Migration Target:** Unified MCP+Spatial Integration Pattern

## Archaeological Findings

### Current GitHub Implementation Layers

#### 1. Original Direct GitHub Implementation
**Location:** `services/integrations/github/`
- **GitHubAgent** (`github_agent.py`) - Direct PyGithub API wrapper
- **ProductionClient** (`production_client.py`) - Production API client
- **IssueGenerator/Analyzer** - Issue creation and analysis tools
- **ConfigService** - GitHub configuration management

**Pattern**: Direct API integration with PyGithub library
**Status**: Legacy - needs migration to MCP+Spatial

#### 2. MCP GitHub Implementation (Yesterday's Work)
**Location:** `services/mcp/consumer/github_adapter.py`
- **GitHubMCPSpatialAdapter** - MCP protocol with spatial mapping
- Inherits from `BaseSpatialAdapter`
- Uses `MCPConsumerCore` for protocol communication

**Pattern**: MCP protocol + spatial intelligence
**Status**: Gold standard implementation - extend this pattern

#### 3. Spatial Infrastructure (Gold Standard)
**Location:** `services/integrations/spatial_adapter.py`, `services/integrations/slack/spatial_adapter.py`
- **BaseSpatialAdapter** - Abstract spatial adapter protocol
- **SpatialPosition/Context** - 8-dimensional spatial intelligence
- **SlackSpatialAdapter** - Production spatial implementation

**Pattern**: 8-dimensional spatial intelligence with external system mapping
**Status**: Gold standard - replicate for all integrations

### Spatial Dimensions Analysis (Slack Gold Standard)

```python
@dataclass
class SpatialContext:
    # Core positioning
    territory_id: str         # External system namespace
    room_id: str             # Specific context (channel/repo)
    path_id: Optional[str]   # Navigation path

    # 8-Dimensional Intelligence
    attention_level: str     # low, medium, high, urgent
    emotional_valence: str   # positive, negative, neutral
    navigation_intent: str   # respond, investigate, monitor, explore

    # External system bridge
    external_system: str     # "slack", "github", "notion"
    external_id: str         # Native system identifier
    external_context: Dict  # System-specific metadata
```

### UI Layer Dependencies

**Investigation Result**: No web UI dependencies found on direct GitHub integration. All GitHub operations appear to be backend API-driven.

## Migration Strategy: Fragmented → Unified

### Phase 1: Deprecation Warning (This Sprint)
- Add deprecation warnings to `GitHubAgent` direct API usage
- Document migration timeline in code comments
- Ensure MCP+Spatial GitHub adapter handles all existing use cases

### Phase 2: Dual Implementation (Next Sprint)
- Maintain both implementations during transition
- Route new features exclusively through MCP+Spatial
- Add feature parity validation between implementations

### Phase 3: Migration Cutover (Sprint +2)
- Replace all `GitHubAgent` usage with `GitHubMCPSpatialAdapter`
- Update dependency injection throughout system
- Comprehensive integration testing

### Phase 4: Legacy Cleanup (Sprint +3)
- Remove `services/integrations/github/github_agent.py`
- Remove PyGithub dependency from requirements.txt
- Archive original implementation files

## Risk Assessment & Rollback Plans

### High Risk Areas
1. **Production GitHub Issue Creation**: Currently using direct API
   - **Mitigation**: Validate MCP+Spatial issue creation before cutover
   - **Rollback**: Feature flag to switch back to direct API

2. **Existing Workflow Dependencies**: Unknown workflow references
   - **Mitigation**: Comprehensive grep analysis of GitHub imports
   - **Rollback**: Maintain legacy imports with deprecation warnings

3. **Authentication Differences**: PyGithub vs MCP protocol auth
   - **Mitigation**: Ensure token compatibility between implementations
   - **Rollback**: Dual authentication support during transition

### Medium Risk Areas
1. **Rate Limiting Behavior**: Different rate limit handling
2. **Error Message Format**: Different exception types
3. **Response Data Structure**: Potential schema differences

### Rollback Strategy
- **Feature Flags**: `USE_MCP_GITHUB` environment variable
- **Import Aliases**: Maintain legacy import paths during transition
- **Configuration Fallback**: Support both auth methods simultaneously

## Migration Complexity Assessment

### Easy Migrations (1-2 hours)
- Configuration management
- Basic issue fetching
- Authentication setup

### Medium Migrations (4-6 hours)
- Issue creation workflow
- Bulk operations
- Error handling alignment

### Complex Migrations (1-2 days)
- Advanced issue analysis
- Webhook integration (if exists)
- Performance optimization

## Success Criteria

### Functional Parity
- [ ] All GitHub operations work identically via MCP+Spatial
- [ ] No regression in issue creation/fetching performance
- [ ] Authentication seamlessly migrated

### Architectural Alignment
- [ ] All GitHub operations use 8-dimensional spatial intelligence
- [ ] No direct API integrations remain
- [ ] Consistent spatial context mapping

### Code Quality
- [ ] Zero deprecated direct API usage
- [ ] Comprehensive spatial context documentation
- [ ] Test coverage maintained at 100%

## Next Steps

1. **ADR-013 Creation**: Document MCP+Spatial as mandatory pattern
2. **Feature Parity Analysis**: Detailed comparison of capabilities
3. **Migration Timeline**: Specific implementation roadmap
4. **Stakeholder Communication**: Alert teams about upcoming changes

---

*Archaeological investigation complete - Ready for ADR-013 foundation*
