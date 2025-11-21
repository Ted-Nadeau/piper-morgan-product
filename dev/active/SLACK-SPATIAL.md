# SLACK-SPATIAL - Fix Slack Integration for Alpha Testing

**Priority**: P0
**Labels**: `epic`, `slack`, `p0-critical`, `alpha-blocking`, `integration`
**Milestone**: MVP
**Sprint**: Test Repair (T1)
**Epic**: SLACK-SPATIAL
**Related**: TEST epic (#341), piper-morgan-23y (bead)

---

## Problem Statement

### Current State
- 47 Slack tests skipped (39.2% of 120-test suite)
- Spatial mapping infrastructure exists but skip decorators not removed
- OAuth spatial methods missing (4 TDD specs)
- Workflow creation from Slack events not implemented
- Token blacklist auto-mock may be hiding test failures

### Impact
- **Blocks**: Alpha testing launch, Slack demo capability
- **User Impact**: Cannot use Slack integration features for PM collaboration
- **Technical Debt**: Tests incorrectly marked as skipped, hiding implementation status. False impression of incomplete work when infrastructure actually exists.

### Strategic Context
Critical for alpha - Slack is primary PM collaboration interface. Diagnostic revealed 8 tests are immediate quick wins (all 4 "missing" SlackSpatialMapper methods actually exist now). Total effort is 14 hours to get Slack alpha-ready, which unblocks critical demo capability.

---

## Goal

**Primary Objective**: Make Slack integration alpha-ready with 90%+ tests passing (108/120 target)

**Not In Scope** (explicitly):
- ❌ Advanced attention algorithms (TDD specs for post-MVP) - 5 tests in piper-morgan-ygy
- ❌ Complete workflow pipeline (alpha milestone, not MVP) - 5 tests deferred

---

## What Already Exists

### Infrastructure ✅
- **SlackSpatialMapper with all 4 "missing" methods** (they exist at lines 188-638!)
  - `map_message_to_spatial_object` (lines 361-394)
  - `map_reaction_to_emotional_marker` (lines 573-638)
  - `map_mention_to_attention_attractor` (lines 469-543)
  - `map_channel_to_room` (lines 188-205)
- **Basic OAuth flow**: 6/10 tests passing
- **Event spatial mapping**: 13/13 tests passing ✅
- **Ngrok webhook flow**: 16/16 tests passing ✅
- **Slack config**: 5/5 tests passing ✅
- **Spatial intent classification**: 15/15 tests passing ✅

### What's Missing ❌
- Skip decorators not removed from 8 recoverable tests (Categories 3 & 4)
- OAuth spatial methods in SlackOAuthHandler (4 methods - TDD specs)
- SpatialWorkflowFactory implementation (11 tests)
- Mock serialization fixes (7 tests)
- System integration wiring (5 tests)

---

## Requirements

### Phase 0: Investigation & Setup
**Status**: ✅ COMPLETE
- [x] Phase 1 diagnostic complete
- [x] Bead consolidation complete
- [x] Root cause analysis complete
- **Evidence**: `dev/2025/11/20/slack-spatial-phase1-diagnostic-1408.md`

### Phase 1: Quick Wins & Auth Fix (2 hours)
**Objective**: Recover 8 tests, investigate token blacklist issue

**Tasks**:
- [ ] Remove skip decorators from TestSlackEventHandler (6 tests - Category 3)
  - File: `tests/unit/services/integrations/slack/test_spatial_integration.py` lines 36-38
  - Bead: piper-morgan-1i5 (methods now exist!)
- [ ] Add `timestamp: datetime` field to SpatialEvent dataclass (2 tests - Category 4)
  - File: `services/integrations/slack/spatial_types.py`
  - Bead: piper-morgan-1i5 (reopened)
- [ ] Complete conftest auto-mock investigation (piper-morgan-otf)
  - **Decision needed**: Which option (A/B/C) to pursue
  - Document: `dev/2025/11/20/conftest-automock-investigation-1405.md`

**Deliverables**:
- 8 tests passing (from 73 → 81)
- SpatialEvent timestamp bug fixed
- Token blacklist investigation complete with decision

### Phase 2: OAuth Spatial Methods (3 hours)
**Objective**: Implement 4 missing SlackOAuthHandler methods

**Tasks**:
- [ ] Implement `get_spatial_capabilities()` - piper-morgan-5eu
- [ ] Implement `refresh_spatial_territory()` - piper-morgan-7sr
- [ ] Implement `validate_and_initialize_spatial_territory()` - piper-morgan-04y
- [ ] Implement `get_user_spatial_context()` - piper-morgan-3v8

**Deliverables**:
- 4 OAuth spatial methods implemented
- 4 tests passing (from 81 → 85)
- OAuth spatial integration complete

### Phase 3: Spatial Workflow Factory (5 hours)
**Objective**: Implement spatial event → workflow creation system

**Tasks**:
- [ ] Create `SpatialWorkflowFactory` class
- [ ] Implement event-to-workflow mappings (high/medium/emotional/new room)
- [ ] Fix mock serialization issues (7 tests - Category 7)
- [ ] Workflow context enrichment
- [ ] Error handling and statistics

**Deliverables**:
- SpatialWorkflowFactory implemented
- 18 tests passing (from 85 → 103)
- Bead piper-morgan-23y partially complete

### Phase 4: System Integration (4 hours)
**Objective**: Wire complete OAuth → Spatial → Workflow pipeline

**Tasks**:
- [ ] System integration layer (5 tests - Category 5)
  - Beads: piper-morgan-1i5, piper-morgan-8jn, piper-morgan-agf
- [ ] End-to-end workflow tests (2 tests - Category 8)
- [ ] Integration verification with test Slack workspace
- [ ] Performance testing

**Deliverables**:
- Complete pipeline functional
- 7 tests passing (from 103 → 110)
- 91.7% test pass rate achieved

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] Documentation updated
- [ ] All beads closed (10 beads total)
- [ ] GitHub issue fully updated
- [ ] Session log completed
- [ ] Cross-validation complete (if multi-agent)

---

## Acceptance Criteria

### Functionality
- [ ] 8 quick-win tests passing (Phase 1)
- [ ] OAuth flow works end-to-end with spatial territory creation
- [ ] Basic message → spatial mapping functional
- [ ] Workflow creation from spatial events works for 4 event types
- [ ] Error handling for Slack API failures

### Testing
- [ ] 90%+ Slack tests passing (target: 108-110/120 tests)
- [ ] Integration tests with test Slack workspace
- [ ] No regression in other test suites (399 passing baseline)
- [ ] Token blacklist tests still passing (17 tests)

### Quality
- [ ] No token blacklist bugs introduced
- [ ] Performance acceptable for alpha (<500ms for spatial mapping)
- [ ] Error handling for Slack API failures
- [ ] No completion bias - all phases 100% complete

### Documentation
- [ ] Session logs completed for each phase
- [ ] Bead closure evidence documented
- [ ] Integration testing results documented
- [ ] Alpha demo readiness confirmed

---

## Completion Matrix

**Use this to verify 100% completion before declaring "done"**

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Quick win tests (8 tests) | ❌ | [pending] |
| SpatialEvent timestamp field | ❌ | [pending] |
| Token blacklist investigation | ❌ | [pending] |
| OAuth get_spatial_capabilities() | ❌ | [pending] |
| OAuth refresh_spatial_territory() | ❌ | [pending] |
| OAuth validate_and_initialize_spatial_territory() | ❌ | [pending] |
| OAuth get_user_spatial_context() | ❌ | [pending] |
| SpatialWorkflowFactory class | ❌ | [pending] |
| Event-to-workflow mappings | ❌ | [pending] |
| Mock serialization fixes (7 tests) | ❌ | [pending] |
| System integration layer (5 tests) | ❌ | [pending] |
| End-to-end workflow tests (2 tests) | ❌ | [pending] |
| Integration testing | ❌ | [pending] |

**Legend**:
- ✅ = Complete with evidence
- ⏸️ = In progress
- ❌ = Not started / Blocked

**Definition of COMPLETE**:
- ✅ ALL acceptance criteria checked
- ✅ Evidence provided (test outputs, commits, screenshots)
- ✅ No known issues remaining
- ✅ 90%+ test pass rate achieved
- ✅ All beads closed

**NOT complete means**:
- ❌ "Works but Test X has issue"
- ❌ "N-1 tests passing"
- ❌ "Core done, extras optional"
- ❌ Any rationalization of incompleteness

---

## Testing Strategy

### Unit Tests
**Current State**: 120 tests total
- ✅ 73 passing (60.8%)
- ⏭️ 47 skipped (39.2%)
- ❌ 0 failing

**Target State**: 108-110 passing (90%+)
- Phase 1: +8 tests → 81 passing
- Phase 2: +4 tests → 85 passing
- Phase 3: +18 tests → 103 passing
- Phase 4: +7 tests → 110 passing

**Deferred**: 10 tests (advanced features, post-MVP)

### Integration Tests
**Scenarios**:
1. OAuth flow with test Slack workspace
2. Message → SpatialEvent → Workflow pipeline
3. Multi-workspace attention prioritization
4. Error handling for API failures

**Test Workspace Required**:
- Slack test workspace with OAuth app configured
- Test channels for spatial mapping
- Test users for mention/reaction events

### Manual Testing Checklist

**Scenario 1: OAuth Spatial Territory Initialization**
1. [ ] Initiate OAuth flow for Slack workspace
2. [ ] Verify spatial territory created with correct metadata
3. [ ] Check spatial capabilities based on OAuth scopes
4. [ ] Confirm territory persists across sessions

**Scenario 2: Message to Spatial Mapping**
1. [ ] Send test message in Slack channel
2. [ ] Verify SpatialEvent created with coordinates
3. [ ] Check spatial object properties (type, size)
4. [ ] Confirm event stored in spatial memory

**Scenario 3: Workflow Creation from Events**
1. [ ] Send high-attention event (mention + urgent keyword)
2. [ ] Verify task workflow created
3. [ ] Send emotional event (multiple reactions)
4. [ ] Verify feedback workflow created

---

## Success Metrics

### Quantitative
- 90%+ test pass rate achieved (108-110/120 tests)
- 0 P0 bugs remaining
- 14 hours total effort (per estimate)
- <500ms spatial mapping latency
- 10 beads closed

### Qualitative
- Can demo Slack integration to alpha users confidently
- OAuth flow reliable and intuitive
- Spatial mapping provides useful PM insights
- Code quality maintained (no completion bias)

---

## STOP Conditions

**STOP immediately and escalate if**:
- Auth token blacklist issues affect more than Slack integration
- SlackSpatialMapper has architectural flaws requiring redesign
- OAuth flow cannot be fixed within effort estimate
- More than 20% of tests start failing (regression threshold)
- Infrastructure doesn't match gameplan assumptions
- Pattern might already exist elsewhere
- User data at risk
- Completion bias detected (claiming "done" without evidence)
- Can't provide verification evidence for any phase

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Medium (14 hours)

**Breakdown by Phase**:
- Phase 0: Complete (investigation done)
- Phase 1: 2 hours (quick wins + auth investigation)
- Phase 2: 3 hours (OAuth methods)
- Phase 3: 5 hours (workflow factory)
- Phase 4: 4 hours (system integration)

**Complexity Notes**:
- Quick wins are low complexity (remove decorators, add field)
- OAuth methods are medium complexity (TDD specs exist)
- Workflow factory is high complexity (new system, mock serialization issues)
- System integration is medium complexity (wiring existing components)

---

## Dependencies

### Required (Must be complete first)
- [x] TEST-DISCIPLINE-KNOWN (#344) - Known failures workflow ✅
- [x] Phase 1 Diagnostic complete ✅
- [ ] Slack test workspace configured
- [ ] Token blacklist investigation decision (conftest auto-mock)

### Optional (Nice to have)
- [ ] TEST-PHANTOM-AUDIT (#351) - Would help identify more issues
- [ ] Advanced attention algorithms (deferred to post-MVP)

---

## Related Documentation

- **Diagnostic Report**: `dev/2025/11/20/slack-spatial-phase1-diagnostic-1408.md`
- **Token Investigation**: `dev/2025/11/20/conftest-automock-investigation-1405.md`
- **Gameplan**: (Pending from architect - awaiting Phase 2+ details)
- **Architecture**:
  - SlackSpatialMapper: `services/integrations/slack/spatial_mapper.py`
  - SpatialTypes: `services/integrations/slack/spatial_types.py`
  - OAuth Handler: `services/integrations/slack/oauth_handler.py`

### Related Beads (10 total)
- **piper-morgan-23y** - Slack Spatial Integration epic (27 tests)
- **piper-morgan-1i5** - SlackSpatialMapper methods (NOW EXIST!) + timestamp bug
- **piper-morgan-5eu** - OAuth `get_spatial_capabilities()` method
- **piper-morgan-7sr** - OAuth `refresh_spatial_territory()` method
- **piper-morgan-04y** - OAuth `validate_and_initialize_spatial_territory()` method
- **piper-morgan-3v8** - OAuth `get_user_spatial_context()` method
- **piper-morgan-8jn** - System integration issue
- **piper-morgan-agf** - System integration issue
- **piper-morgan-ygy** - Advanced attention algorithms (5 tests, deferred)
- **piper-morgan-otf** - Token blacklist auto-mock investigation (P2)

---

## Evidence Section

[This section will be filled in during/after implementation]

### Phase 1 Evidence
```bash
[Pending: Test output showing 8 tests recovered]
[Pending: Commit hash for skip decorator removal]
[Pending: Commit hash for SpatialEvent timestamp field]
[Pending: Token blacklist investigation decision]
```

### Phase 2 Evidence
```bash
[Pending: Test output showing OAuth methods working]
[Pending: Commit hash for OAuth method implementations]
```

### Phase 3 Evidence
```bash
[Pending: Test output showing workflow factory working]
[Pending: Commit hash for SpatialWorkflowFactory]
```

### Phase 4 Evidence
```bash
[Pending: Test output showing 90%+ pass rate]
[Pending: Integration test results]
[Pending: Performance metrics]
```

### Cross-Validation (if applicable)
**Verified By**: [Pending]
**Date**: [Pending]
**Report**: [Pending]

---

## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met ✅
- [ ] Completion matrix 100% ✅
- [ ] Evidence provided for each criterion ✅
- [ ] Tests passing with output ✅ (90%+ achieved)
- [ ] Documentation updated ✅
- [ ] No regressions confirmed ✅
- [ ] STOP conditions all clear ✅
- [ ] Session log complete ✅
- [ ] All 10 beads closed ✅
- [ ] Cross-validation complete (if multi-agent) ✅

**Status**: Not Started - Awaiting Phase 2+ Gameplan

---

## Notes for Implementation

**From Diagnostic (Phase 1 Complete)**:

**Root Cause Analysis - 3 Core Issues**:
1. **TDD specs before implementation** (27 tests - 57%)
2. **Implementation complete but tests still skipped** (8 tests - 17%) ← Quick wins
3. **Mock setup complexity** (7 tests - 15%)

**Key Finding**: All 4 "missing" SlackSpatialMapper methods NOW EXIST in production code. Tests are skipped due to outdated decorators, not missing functionality.

**Verification**:
- ✅ `map_message_to_spatial_object` exists at lines 361-394
- ✅ `map_reaction_to_emotional_marker` exists at lines 573-638
- ✅ `map_mention_to_attention_attractor` exists at lines 469-543
- ✅ `map_channel_to_room` exists at lines 188-205

**Token Blacklist Auto-Mock**:
- `tests/conftest.py` lines 50-86 has `autouse=True` fixture
- Always mocks `TokenBlacklist.is_blacklisted()` to return `False`
- HIGH RISK: May hide auth/token revocation bugs
- 3 options documented, decision needed before Phase 1

**Recommendations**:
- Phase 1 quick wins are extremely low-hanging fruit (30-45 min)
- OAuth methods have TDD specs, clear implementation path
- Workflow factory is highest complexity, budget extra time
- Integration testing requires test Slack workspace setup

---

**Remember**:
- Quality over speed (Time Lord philosophy)
- Evidence required for all claims
- No 80% completions
- PM closes issues after approval

---

_Issue created: 2025-11-20_
_Last updated: 2025-11-20_
