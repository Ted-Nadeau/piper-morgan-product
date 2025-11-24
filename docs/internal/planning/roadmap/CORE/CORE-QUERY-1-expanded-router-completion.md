# CORE-QUERY-1: Complete Integration Router Infrastructure

**Previously**: Limited query operations epic
**Now**: Complete all integration routers to enable proper architecture

## Context
During GREAT-2B investigation, we discovered that integration routers are only 14-20% complete. Services bypass routers through direct imports because routers don't support needed operations. This blocks the entire integration cleanup epic.

## Background
- QueryRouter operational (from GREAT-1) but basic
- GitHubIntegrationRouter: 2 of 14 methods (14%)
- Other routers likely similarly incomplete
- Services forced to use direct imports
- Sophisticated architecture design, incomplete implementation

## Current State
- **GitHub Router**: 14% complete (2/14 methods)
- **Slack Router**: Unknown (likely similar)
- **Notion Router**: Unknown (likely similar)
- **Calendar Router**: Unknown (likely similar)
- **QueryRouter**: Basic operations only

## Acceptance Criteria
### GitHub Router Completion
- [ ] All 14 GitHubAgent methods available through router
- [ ] Proper spatial/legacy delegation for each method
- [ ] Feature flag control working for all operations
- [ ] Tests for router completeness

### Slack Router Completion
- [ ] Audit current completeness
- [ ] Implement missing router methods
- [ ] Spatial/legacy delegation working
- [ ] Feature flag control verified

### Notion Router Completion
- [ ] Audit current completeness
- [ ] Implement missing router methods
- [ ] Spatial/legacy delegation working
- [ ] Feature flag control verified

### Calendar Router Completion
- [ ] Audit current completeness
- [ ] Implement missing router methods
- [ ] MCP/legacy delegation working
- [ ] Feature flag control verified

### QueryRouter Enhancement
- [ ] Verify can route to all integration routers
- [ ] Add any missing query operations
- [ ] Performance acceptable
- [ ] Error handling robust

## Tasks

### Phase 1: Router Audit (4 hours)
- [ ] List all methods in each legacy agent
- [ ] List all methods in each router
- [ ] Calculate completeness percentages
- [ ] Identify critical missing methods
- [ ] Document router patterns

### Phase 2: GitHub Router (3 hours)
- [ ] Implement get_issue_by_url
- [ ] Implement get_open_issues
- [ ] Implement get_recent_issues
- [ ] Implement get_recent_activity
- [ ] Implement list_repositories
- [ ] Implement remaining 7 methods
- [ ] Test spatial/legacy switching

### Phase 3: Slack Router (3 hours)
- [ ] Audit and implement missing methods
- [ ] Connect to spatial intelligence
- [ ] Test feature flag control
- [ ] Verify workspace operations

### Phase 4: Notion Router (2 hours)
- [ ] Audit and implement missing methods
- [ ] Connect to MCP adapter
- [ ] Test routing operations
- [ ] Verify database operations

### Phase 5: Calendar Router (2 hours)
- [ ] Audit and implement missing methods
- [ ] Connect to MCP adapter
- [ ] Test routing operations
- [ ] Verify event operations

### Phase 6: QueryRouter Integration (2 hours)
- [ ] Verify routes to all integration routers
- [ ] Add missing query operations
- [ ] Test end-to-end flows
- [ ] Performance optimization

## Lock Strategy
- Router completeness tests in CI/CD
- No direct agent imports allowed (after completion)
- Feature flag tests for all routers
- Performance benchmarks

## Success Validation
```bash
# Router completeness check
python verify_router_completeness.py

# All routers have all methods
pytest tests/routers/test_completeness.py -v

# Feature flags control all operations
SPATIAL_ENABLED=true pytest tests/integrations/ -v
SPATIAL_ENABLED=false pytest tests/integrations/ -v

# No direct imports remain
grep -r "import.*Agent" services/ --include="*.py" | grep -v Router
```

## Dependencies
- After: GREAT-1 (QueryRouter operational)
- Before: GREAT-2B-E (integration fixes)
- Enables: Proper architectural flow

## Estimated Duration
2-3 days (16-20 hours total)
- Can be parallelized across agents
- Each router can be completed independently

## Priority
CRITICAL - This blocks all integration work

## Risk Assessment
### Medium Risk
- Router patterns may vary between services
- Some methods may not fit router pattern
- Performance overhead of routing layer

### Mitigation
- Follow existing router patterns where they work
- Document exceptions clearly
- Performance test each router

## Strategic Impact
Completing routers enables:
- GREAT-2B-E become simple import replacements
- Feature flag control of all integrations
- Spatial/legacy switching works properly
- Clean architecture for plugin system (GREAT-3)

## The Inchworm Path
1. Complete routers (this epic)
2. Replace direct imports (GREAT-2B-E simplified)
3. Verify spatial systems work (already built)
4. Move to plugin architecture (GREAT-3)

Without complete routers, none of the integration cleanup can proceed properly.

---

**Labels**: core, critical-path, infrastructure, routers
