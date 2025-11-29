# Prompt for Code: Create SLACK-SPATIAL GitHub Issue

## Your Task
Create a GitHub issue for the Slack Spatial Integration epic that's currently only tracked in beads. This is P0 priority work blocking alpha testing.

## Issue Details

**Title**: `SLACK-SPATIAL: Fix Slack Integration for Alpha Testing`

**Labels**: `epic`, `slack`, `p0-critical`, `alpha-blocking`, `integration`

**Milestone**: `MVP`

**Sprint**: `Test Repair (T1)`

**Assignees**: `@mediajunkie`

## Issue Body Content

Use the following structure:

```markdown
# SLACK-SPATIAL: Fix Slack Integration for Alpha Testing

## Problem
Slack integration is critical for alpha but has 47 skipped tests (39% of suite), blocking our ability to demo and test the Slack → Spatial → Workflow pipeline.

## Current State
- **Total Tests**: 120 Slack integration tests
- **Passing**: 73 (60.8%)
- **Skipped**: 47 (39.2%)
- **Blocked Features**: Slack OAuth, spatial mapping, workflow creation from Slack events

## Key Discovery
Phase 1 diagnostic found that 8 tests are immediate quick wins - the "missing" SlackSpatialMapper methods actually exist:
- ✅ `map_message_to_spatial_object`
- ✅ `map_reaction_to_emotional_marker`
- ✅ `map_mention_to_attention_attractor`
- ✅ `map_channel_to_room`

These tests just need skip decorators removed!

## Success Criteria

### Minimum (Alpha-Ready)
- [ ] 8 quick-win tests passing
- [ ] OAuth flow works end-to-end
- [ ] Basic message → spatial mapping functional
- [ ] Can demo Slack integration in alpha

### Target (Full Integration)
- [ ] 90%+ Slack tests passing (108/120)
- [ ] Spatial workflow factory implemented
- [ ] Complete pipeline: Slack → Spatial → Workflow
- [ ] All related beads closed

## Implementation Plan

### Phase 1: Quick Wins & Auth Fix (2 hours)
- Remove skip decorators for 8 recoverable tests
- Add `timestamp` field to `SpatialEvent`
- Investigate token blacklist auto-mock hiding bugs
- **Impact**: +8 tests immediately

### Phase 2: OAuth Spatial Methods (3 hours)
- Implement 4 missing SlackOAuthHandler methods
- Test OAuth → Spatial territory initialization
- **Impact**: +4 tests, OAuth multi-workspace support

### Phase 3: Spatial Workflow Factory (5 hours)
- Implement SpatialWorkflowFactory class
- Map spatial events to workflow types
- Fix mock serialization issues
- **Impact**: +18 tests, core feature complete

### Phase 4: System Integration (4 hours)
- Wire complete pipeline end-to-end
- Integration testing with test Slack workspace
- **Impact**: +7 tests, alpha-ready demo

## Effort & Priority

**Total Effort**: 14 hours (can be parallelized)
**Priority**: P0 - Blocks alpha testing
**Risk**: Without this, cannot demonstrate Slack integration to alpha users

## Related Beads
- `piper-morgan-23y` - Slack Spatial Integration epic
- `piper-morgan-1i5` - SlackSpatialMapper methods (now exist!)
- `piper-morgan-5eu` - OAuth get_spatial_capabilities()
- `piper-morgan-7sr` - OAuth refresh_spatial_territory()
- `piper-morgan-04y` - OAuth validate_and_initialize_spatial_territory()
- `piper-morgan-3v8` - OAuth get_user_spatial_context()
- `piper-morgan-8jn` - System integration issue
- `piper-morgan-agf` - System integration issue
- `piper-morgan-otf` - Token blacklist auto-mock investigation

## References
- Diagnostic Report: `dev/2025/11/20/slack-spatial-phase1-diagnostic-1408.md`
- Gameplan: `dev/2025/11/20/gameplan-slack-spatial-integration.md`
- Token Investigation: `dev/2025/11/20/conftest-automock-investigation-1405.md`

## Blocks
This issue blocks:
- Alpha testing launch
- Slack integration demo
- Multi-workspace support
- Real-time PM collaboration features
```

## Additional Instructions

1. Create this as a single epic issue (not multiple child issues yet)
2. Add it to any existing project boards
3. Set milestone to "Alpha Launch" if it exists
4. After creating, note the issue number for tracking
5. Report back with the issue number and URL

## Context for Code

This work was discovered during test infrastructure cleanup. We found that many "broken" tests actually just have skip decorators that were never removed after implementation was complete. The quick wins alone (8 tests in 45 minutes) provide immediate value, and the full implementation (14 hours) makes Slack integration alpha-ready.

The gameplan has been reviewed and approved by the Chief Architect. This is P0 priority alongside security work (RBAC, Encryption) for Sprint S1.

---

*End of prompt - hand this to Code to create the GitHub issue*
