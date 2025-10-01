# Updated Description for Issue #199

## CORE-QUERY-1: Complete Integration Router Infrastructure

**Previously**: Limited query operations epic
**Now**: Complete remaining integration routers (Slack, Notion, Calendar)

## Context
During GREAT-2B investigation, we discovered that integration routers are only 14-20% complete. Services bypass routers through direct imports because routers don't support needed operations. This blocks the entire integration cleanup epic.

**UPDATE (Sept 28)**: GitHub router completed in GREAT-2B (17/14 methods - 121%). This issue now focuses on the remaining three routers.

## Background
- QueryRouter operational (from GREAT-1) but basic
- ✅ GitHubIntegrationRouter: COMPLETE (17 methods from GREAT-2B)
- Other routers likely similarly incomplete
- Services forced to use direct imports
- Sophisticated architecture design, incomplete implementation

## Current State
- **GitHub Router**: ✅ COMPLETE (17 methods, 121%)
- **Slack Router**: Unknown (audit needed)
- **Notion Router**: Unknown (audit needed)
- **Calendar Router**: Unknown (audit needed)
- **QueryRouter**: Basic operations only

## Acceptance Criteria

### ~~GitHub Router Completion~~ ✅ DONE in GREAT-2B
- ✅ All GitHubAgent methods available through router
- ✅ Proper spatial/legacy delegation for each method
- ✅ Feature flag control working for all operations
- ✅ Tests for router completeness

### Slack Router Completion
- [ ] Audit current completeness (PM will validate)
- [ ] Implement missing router methods (PM will validate)
- [ ] Spatial/legacy delegation working (PM will validate)
- [ ] Feature flag control verified (PM will validate)

### Notion Router Completion
- [ ] Audit current completeness (PM will validate)
- [ ] Implement missing router methods (PM will validate)
- [ ] MCP/spatial/legacy delegation working (PM will validate)
- [ ] Feature flag control verified (PM will validate)

### Calendar Router Completion
- [ ] Audit current completeness (PM will validate)
- [ ] Implement missing router methods (PM will validate)
- [ ] MCP/legacy delegation working (PM will validate)
- [ ] Feature flag control verified (PM will validate)

### QueryRouter Enhancement
- [ ] Verify can route to all integration routers (PM will validate)
- [ ] Add any missing query operations (PM will validate)
- [ ] Performance acceptable (PM will validate)
- [ ] Error handling robust (PM will validate)

## Progressive Update Protocol

Agents should update this issue after each phase:

### Phase 0 Completion
Add audit results as comment with:
- Completeness percentages for each router
- List of bypassing services
- Recommended implementation order

### After Each Router
Update checkboxes and add evidence:
- Methods implemented count
- Test results showing feature flags work
- List of services migrated

### Evidence Required
- Terminal output for audits
- Test results with full output
- Before/after for service migrations
- No "should work" - only proven results

## Tasks (Revised)

### Phase -1: Infrastructure Reality Check (30 min)
- [ ] Verify router file locations
- [ ] Check spatial/MCP systems exist
- [ ] Confirm integration structure

### Phase 0: Router Audit (2 hours)
- [ ] Audit Slack completeness and bypassing services
- [ ] Audit Notion completeness and bypassing services
- [ ] Audit Calendar completeness and bypassing services
- [ ] Document router patterns
- [ ] Recommend implementation order

### Phase 1-3: Router Completion (9-10 hours total)
*Order determined by Phase 0 audit*
- [ ] First router: Implement all missing methods
- [ ] Second router: Implement all missing methods
- [ ] Third router: Implement all missing methods

### Phase 4: Service Migration (2 hours)
- [ ] Replace all direct Slack imports
- [ ] Replace all direct Notion imports
- [ ] Replace all direct Calendar imports
- [ ] Verify no direct imports remain

### Phase 5: Testing & Validation (2 hours)
- [ ] Test all routers with feature flags
- [ ] Verify completeness tests pass
- [ ] Confirm architectural protection

### Phase 6: Lock & Document (1 hour)
- [ ] Add pre-commit hooks
- [ ] Update CI/CD
- [ ] Document patterns

[Rest remains the same...]
