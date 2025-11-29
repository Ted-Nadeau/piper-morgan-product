# Prompt for Code: Create SLACK-SPATIAL GitHub Issue Using Feature Template

## Your Task
Create a GitHub issue for the Slack Spatial Integration epic using the team's standard feature template located at `.github/issue_template/feature.md`. This is P0 priority work blocking alpha testing.

## Issue Configuration

**Title**: `SLACK-SPATIAL: Fix Slack Integration for Alpha Testing`
**Labels**: `epic`, `slack`, `p0-critical`, `alpha-blocking`, `integration`
**Milestone**: `MVP`
**Sprint**: `Test Repair (T1)`
**Assignees**: `@mediajunkie`

## Instructions for Using the Template

1. Use the feature template from `.github/issue_template/feature.md` as your structure
2. Fill in each section following the template's format
3. Include the Completion Matrix section (critical for tracking)
4. Maintain all template sections even if some are brief

## Content for Each Section

### Header
```markdown
# SLACK-SPATIAL - Fix Slack Integration for Alpha Testing

**Priority**: P0
**Labels**: `epic`, `slack`, `p0-critical`, `alpha-blocking`, `integration`
**Milestone**: MVP
**Sprint**: Test Repair (T1)
**Epic**: SLACK-SPATIAL
**Related**: TEST epic (#341), piper-morgan-23y (bead)
```

### Problem Statement

**Current State**:
- 47 Slack tests skipped (39% of suite)
- Spatial mapping incomplete
- OAuth spatial methods missing
- Workflow creation from Slack events broken

**Impact**:
- **Blocks**: Alpha testing launch, Slack demo
- **User Impact**: Cannot use Slack integration features
- **Technical Debt**: Tests incorrectly skipped, hiding implementation

**Strategic Context**:
Critical for alpha - Slack is primary PM collaboration interface

### Goal

**Primary Objective**: Make Slack integration alpha-ready with 90%+ tests passing

**Not In Scope**:
- ❌ Advanced attention algorithms (TDD specs for post-MVP)
- ❌ Complete workflow pipeline (alpha milestone, not MVP)

### What Already Exists

**Infrastructure ✅**:
- SlackSpatialMapper with all 4 "missing" methods (they exist!)
- Basic OAuth flow (6/10 tests passing)
- Event spatial mapping (13/13 tests passing)
- Ngrok webhook flow (16/16 tests passing)

**What's Missing ❌**:
- Skip decorators not removed (8 tests)
- OAuth spatial methods (4 methods)
- Spatial workflow factory
- System integration wiring

### Requirements

Use the 4-phase plan from the gameplan:

**Phase 1: Quick Wins & Auth Fix (2 hours)**
- [ ] Remove skip decorators for 8 recoverable tests
- [ ] Add timestamp field to SpatialEvent
- [ ] Investigate token blacklist auto-mock

**Phase 2: OAuth Spatial Methods (3 hours)**
- [ ] Implement get_spatial_capabilities()
- [ ] Implement refresh_spatial_territory()
- [ ] Implement validate_and_initialize_spatial_territory()
- [ ] Implement get_user_spatial_context()

**Phase 3: Spatial Workflow Factory (5 hours)**
- [ ] Create SpatialWorkflowFactory class
- [ ] Implement event-to-workflow mappings
- [ ] Fix mock serialization issues

**Phase 4: System Integration (4 hours)**
- [ ] Wire complete pipeline
- [ ] End-to-end testing
- [ ] Integration verification

**Phase Z: Completion & Handoff**
- [ ] 90%+ Slack tests passing
- [ ] All beads closed
- [ ] Documentation updated
- [ ] Alpha demo ready

### Acceptance Criteria

**Functionality**:
- [ ] 8 quick-win tests passing
- [ ] OAuth flow works end-to-end
- [ ] Basic message → spatial mapping functional
- [ ] Workflow creation from spatial events works

**Testing**:
- [ ] 90%+ Slack tests passing (target: 108/120)
- [ ] Integration tests with test Slack workspace
- [ ] No regression in other tests

**Quality**:
- [ ] No token blacklist bugs
- [ ] Performance acceptable for alpha
- [ ] Error handling for Slack API failures

### Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Quick win tests (8) | ❌ | [pending] |
| OAuth spatial methods (4) | ❌ | [pending] |
| SpatialWorkflowFactory | ❌ | [pending] |
| Mock fixes | ❌ | [pending] |
| System integration | ❌ | [pending] |
| E2E testing | ❌ | [pending] |

### Testing Strategy

**Unit Tests**:
- 120 Slack integration tests total
- Current: 73 passing, 47 skipped
- Target: 108+ passing

**Integration Tests**:
- OAuth flow with test workspace
- Message → Spatial → Workflow pipeline
- Multi-workspace scenarios

### Success Metrics

**Quantitative**:
- 90%+ test pass rate (108/120 tests)
- 0 P0 bugs
- 14 hours total effort

**Qualitative**:
- Can demo Slack integration to alpha users
- OAuth flow reliable
- Spatial mapping intuitive

### STOP Conditions

**STOP immediately if**:
- Auth token issues affect more than Slack
- Spatial mapper has architectural flaws
- OAuth flow cannot be fixed
- More than 20% tests start failing

### Effort Estimate

**Overall Size**: Medium (14 hours)

**Breakdown**:
- Phase 1: 2 hours (quick wins)
- Phase 2: 3 hours (OAuth)
- Phase 3: 5 hours (factory)
- Phase 4: 4 hours (integration)

### Dependencies

**Required**:
- [ ] TEST-DISCIPLINE-KNOWN (#344) - Known failures workflow
- [ ] Working test environment

**Optional**:
- [ ] TEST-PHANTOM-AUDIT (#351) - Would help identify more issues

### Related Documentation

- **Diagnostic Report**: `dev/2025/11/20/slack-spatial-phase1-diagnostic-1408.md`
- **Gameplan**: `dev/2025/11/20/gameplan-slack-spatial-integration.md`
- **Token Investigation**: `dev/2025/11/20/conftest-automock-investigation-1405.md`

### Related Beads
- `piper-morgan-23y` - Slack Spatial Integration epic
- `piper-morgan-1i5` - SlackSpatialMapper methods (now exist!)
- `piper-morgan-5eu` - OAuth get_spatial_capabilities()
- `piper-morgan-7sr` - OAuth refresh_spatial_territory()
- `piper-morgan-04y` - OAuth validate_and_initialize_spatial_territory()
- `piper-morgan-3v8` - OAuth get_user_spatial_context()
- `piper-morgan-8jn` - System integration issue
- `piper-morgan-agf` - System integration issue
- `piper-morgan-otf` - Token blacklist auto-mock investigation

## Additional Instructions

1. **Use the template**: Start with `.github/issue_template/feature.md`
2. **Keep all sections**: Don't skip any template sections
3. **Completion Matrix is critical**: This tracks our progress
4. **Evidence Section**: Leave blank for now (filled during implementation)
5. **Cross-Validation**: Note this will be multi-agent work
6. **Create as single epic**: Don't break into child issues yet

After creating:
- Report the issue number and URL
- Confirm it appears in the MVP milestone
- Verify it's in the Test Repair (T1) sprint

## Context

This consolidates work currently tracked only in beads. The diagnostic revealed that 8 tests are immediate quick wins (methods exist, just need skip removal). Total effort is 14 hours to get Slack alpha-ready, which unblocks a critical demo capability.

---

*End of prompt - provide this to Code to create the properly formatted GitHub issue*
