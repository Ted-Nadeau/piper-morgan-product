# Gameplan: SLACK-SPATIAL - Fix Slack Integration for Alpha
**Epic**: SLACK-SPATIAL
**Priority**: P0 (Blocks alpha testing)
**Created**: 2025-11-20 3:10 PM
**Author**: Chief Architect

---

## Context

Slack integration is critical for alpha testing but 47 tests are skipped (39% of suite). Phase 1 diagnostic revealed:
- 8 tests are quick wins (methods exist, just need skip removal)
- 27 tests are TDD specs awaiting implementation
- Core spatial workflow feature partially complete
- Hidden auth token issues may affect Slack OAuth

**Key Discovery**: The 4 "missing" SlackSpatialMapper methods actually exist! We can recover 8 tests immediately.

---

## Success Criteria

### Minimum (Alpha-Ready)
- [ ] 8 quick-win tests passing (remove skips)
- [ ] OAuth flow works end-to-end
- [ ] Basic message → spatial mapping functional
- [ ] No auth token blacklist bugs

### Target (Full Integration)
- [ ] Spatial workflow factory implemented (11 tests)
- [ ] OAuth spatial methods complete (4 tests)
- [ ] System integration pipeline working (5 tests)
- [ ] 90%+ Slack tests passing

---

## Phase 0: Archaeological Investigation ✓ COMPLETE

**Completed by**: Code (2:08 PM)

**Findings**:
- Total: 120 tests (73 passing, 47 skipped)
- Quick wins: 8 tests recoverable in 30-45 min
- Root causes: 57% TDD specs, 17% complete but skipped, 15% mock issues
- All 4 "missing" methods now exist in SlackSpatialMapper

**Deliverable**: `dev/2025/11/20/slack-spatial-phase1-diagnostic-1408.md` ✓

---

## Phase 1: Quick Wins & Auth Fix (2 hours)

### Task 1.1: Slack Quick Wins (45 min)
**Owner**: Code Agent
**Priority**: Do first

**Actions**:
1. Remove skip decorator from 6 tests in `test_spatial_integration.py::TestSlackEventHandler`
2. Add `timestamp: datetime` field to `SpatialEvent` dataclass
3. Remove skip from 2 tests in `test_spatial_integration.py::TestSpatialIntegration`
4. Run tests, fix minor issues
5. Update known-failures if needed

**Success**: +8 tests passing, verify no regressions

### Task 1.2: Token Blacklist Investigation (1 hour)
**Owner**: Code Agent
**Priority**: Parallel or immediately after

**Actions** (Option C - Recommended):
1. Temporarily disable `autouse=True` in conftest.py:50
2. Run auth test suite: `pytest tests/unit/services/auth/ -v`
3. Categorize failures:
   - Async context errors → Document for later fix
   - Blacklist behavior → Fix test logic
   - Other → May be real bugs
4. Re-enable auto-mock with documentation
5. Create issues for any discovered bugs

**Success**: Hidden auth bugs revealed and documented

### Checkpoint 1
- [ ] 8 Slack tests recovered
- [ ] Auth token issues documented
- [ ] No new test failures introduced
- [ ] Beads updated: piper-morgan-1i5 (partial fix)

---

## Phase 2: OAuth Spatial Methods (3 hours)

### Task 2.1: Implement SlackOAuthHandler Methods
**Owner**: Lead Developer
**Beads**: piper-morgan-5eu, 7sr, 04y, 3v8

**Implement in `SlackOAuthHandler`:
```python
async def get_spatial_capabilities(self) -> Dict[str, Any]:
    """Map OAuth scopes to spatial capabilities"""

async def refresh_spatial_territory(self, workspace_id: str) -> SpatialTerritory:
    """Refresh spatial territory after OAuth token refresh"""

async def validate_and_initialize_spatial_territory(self, auth_response: Dict) -> SpatialTerritory:
    """Initialize spatial territory on OAuth success"""

async def get_user_spatial_context(self, user_id: str) -> Dict[str, Any]:
    """Get user's spatial context from OAuth data"""
```

**Success**: 4 OAuth spatial tests passing

### Task 2.2: Integration Testing
**Owner**: Code Agent

**Actions**:
1. Set up test Slack workspace (if needed)
2. Test OAuth flow end-to-end
3. Verify spatial territory initialization
4. Document any integration issues

**Success**: OAuth → Spatial flow works in test environment

### Checkpoint 2
- [ ] 4 OAuth methods implemented
- [ ] OAuth tests passing
- [ ] Integration verified
- [ ] Beads closed: piper-morgan-5eu, 7sr, 04y, 3v8

---

## Phase 3: Spatial Workflow Factory (5 hours)

### Task 3.1: Core Factory Implementation
**Owner**: Lead Developer
**Epic**: piper-morgan-23y

**Create `SpatialWorkflowFactory`:
```python
class SpatialWorkflowFactory:
    """Creates workflows from spatial events"""

    def __init__(self, workflow_factory: WorkflowFactory):
        self.mappings = self._initialize_mappings()

    async def create_workflow_from_spatial_event(self, event: SpatialEvent) -> Optional[Workflow]:
        """Main entry point - maps spatial events to workflows"""

    def calculate_mapping_score(self, event: SpatialEvent, mapping: WorkflowMapping) -> float:
        """Score how well event matches workflow criteria"""
```

**Mappings**:
- High attention → Task workflow
- Medium attention → Report workflow
- Emotional marker → Feedback workflow
- New room → Pattern discovery workflow

**Success**: 11 factory tests passing

### Task 3.2: Fix Mock Serialization
**Owner**: Code Agent
**Epic**: piper-morgan-23y

**Actions**:
1. Investigate mock serialization issues in `test_workflow_integration.py`
2. Either:
   - Refactor to simpler mocks, OR
   - Create dataclass factories for test data
3. Update 7 affected tests

**Success**: Mock setup working, tests runnable

### Checkpoint 3
- [ ] Workflow factory implemented
- [ ] 11 factory tests passing
- [ ] 7 mock tests fixed
- [ ] Epic progress: piper-morgan-23y (partial)

---

## Phase 4: System Integration (4 hours)

### Task 4.1: Pipeline Wiring
**Owner**: Lead Developer
**Beads**: piper-morgan-8jn, agf

**Wire the complete pipeline**:
```
Slack Event → EventHandler → SpatialMapper → SpatialEvent
    → WorkflowFactory → Workflow → Execution
```

**Key integration points**:
- Event handler calls spatial mapper
- Spatial events trigger workflow factory
- Workflows execute with spatial context

**Success**: 5 system integration tests passing

### Task 4.2: End-to-End Testing
**Owner**: Code Agent

**Actions**:
1. Create test scenarios for complete flow
2. Test with real Slack events (test workspace)
3. Verify workflows created correctly
4. Document any gaps

**Success**: Can demonstrate Slack → Workflow in alpha

### Checkpoint 4
- [ ] Pipeline fully wired
- [ ] 5 integration tests passing
- [ ] E2E demo working
- [ ] Beads closed: piper-morgan-8jn, agf

---

## Phase Z: Verification & Cleanup

### Comprehensive Testing
1. Run full Slack test suite
2. Verify no regressions
3. Update known-failures file
4. Close completed beads

### Documentation
1. Update Slack integration guide
2. Document spatial workflow mappings
3. Create troubleshooting guide

### Metrics
- [ ] Slack tests: 90%+ passing (target: 108/120)
- [ ] No P0 bugs remaining
- [ ] Alpha testing unblocked
- [ ] All quick wins captured

---

## Risk Mitigation

### Risk 1: Hidden Auth Bugs
**Mitigation**: Phase 1.2 investigation before OAuth work

### Risk 2: Complex Mock Issues
**Mitigation**: Timebox mock fixes to 2 hours, use known-failures if needed

### Risk 3: Integration Complexity
**Mitigation**: Incremental testing at each phase checkpoint

### Risk 4: Time Overrun
**Mitigation**: Phase 1-2 are must-have for alpha, Phase 3-4 can be deferred if needed

---

## Resource Allocation

**Total Effort**: 14 hours (can be split across team)

**Suggested Split**:
- Code Agent: Phase 1 + test work (4 hours)
- Lead Developer: Phase 2-3 implementation (8 hours)
- Code Agent: Phase 4 testing + cleanup (2 hours)

**Critical Path**: Phase 1 → Phase 2 (OAuth) → Can parallelize 3 & 4

---

## Stop Conditions

**Stop and escalate if**:
- Auth token issues affect more than Slack
- Spatial mapper has architectural flaws
- OAuth flow cannot be fixed
- More than 20% tests start failing

---

## Success Metrics

### Minimum Success (Alpha-Ready)
- 8 quick wins complete ✓
- OAuth working ✓
- Basic Slack integration functional ✓
- Can demo in alpha ✓

### Full Success
- 90%+ Slack tests passing
- Complete spatial workflow pipeline
- All beads closed
- Production-ready integration

---

## Next Steps

1. **Immediate**: Start Phase 1.1 (quick wins) - 45 minutes
2. **Today**: Complete Phase 1.2 (auth investigation) - 1 hour
3. **Tomorrow**: Begin Phase 2 (OAuth methods) if Phase 1 successful
4. **Decision Point**: After Phase 2, assess if Phase 3-4 needed for alpha

---

**Gameplan Status**: Ready for execution
**First Action**: Remove skip decorators, recover 8 tests
**Success Criteria**: Slack integration alpha-ready
