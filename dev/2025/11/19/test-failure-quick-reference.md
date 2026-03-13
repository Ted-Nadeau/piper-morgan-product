# Test Failure Quick Reference
**Date**: 2025-11-19
**Purpose**: PM decision-making guide

---

## TL;DR - What to Do

### Immediate Actions (Do Today - < 1 hour)

**1. Add 5 enum values** (15 minutes):
```python
# In services/shared_types.py (IntentCategory enum)
PLANNING = "planning"
REVIEW = "review"

# In services/integrations/slack/spatial_types.py (AttentionLevel enum)
HIGH = "high"
MEDIUM = "medium"
LOW = "low"
```
**Impact**: ~25 tests pass (4% improvement)

**2. Add stub method OR skip tests** (15 minutes):
```python
# Option A: In services/integrations/slack/spatial_mapper.py
async def map_channel_to_room(self, channel_id: str) -> Room:
    """Stub: To be implemented"""
    raise NotImplementedError("Feature planned for Phase 5")

# Option B: Skip tests
@pytest.mark.skip(reason="Waiting for map_channel_to_room implementation")
```
**Impact**: 4 tests pass OR properly skipped (1% improvement)

**Total Quick Wins**: ~30 tests, 5% improvement, < 1 hour

---

### Next Priority (Do This Week - 1-2 hours)

**3. Fix OrchestrationEngine fixture**:
```python
# In tests/unit/services/orchestration/test_orchestration_engine.py
@pytest.fixture
def engine(mocker):
    # Mock container service lookup
    mock_llm = mocker.Mock()
    mocker.patch('services.container.service_container.get_service',
                 return_value=mock_llm)
    return OrchestrationEngine()
```
**Impact**: 11 tests pass (2% improvement)

---

### Defer to Beads

**4. Fixture errors** (53 tests):
- Missing `async_transaction` fixture
- Already documented in test-suite-failure-analysis.md
- Action: Create GitHub issue for fixture refactor work

**5. OAuth integration** (1 test):
- test_oauth_flow_creates_spatial_workspace_territory
- Needs: OAuth state management investigation
- Action: Create GitHub issue for Slack OAuth testing

**6. Spatial integration** (4 tests):
- Complex end-to-end tests
- May need feature completion
- Action: Investigate individually, create issues as needed

---

## Decision Tree

```
Test failing?
├─ Error: "AttributeError: PLANNING" or "MEDIUM" or "HIGH"
│  └─ ✅ FIX NOW: Add enum value (15 min)
│
├─ Error: "ContainerNotInitializedError"
│  └─ 🔧 THIS WEEK: Fix fixture (1-2 hrs)
│
├─ Error: "fixture 'async_transaction' not found"
│  └─ 📋 DEFER: Create GitHub issue
│
├─ Error: "SlackAuthFailedError: Invalid OAuth state"
│  └─ 📋 DEFER: Create GitHub issue
│
└─ Error: "AttributeError: object has no attribute 'map_channel_to_room'"
   └─ ⚡ CHOICE: Add stub (15 min) OR skip test (5 min)
```

---

## Expected Results Timeline

### Today (< 1 hour work)
- **Actions**: Add 5 enum values + stub method
- **Before**: 422/617 passing (68.4%)
- **After**: ~452/617 passing (73.3%)
- **Improvement**: +30 tests, +5%

### This Week (1-2 hours work)
- **Actions**: Fix OrchestrationEngine fixture
- **Before**: ~452/617 passing (73.3%)
- **After**: ~463/617 passing (75.0%)
- **Improvement**: +11 tests, +2%

### After Beads Work (future)
- **Actions**: Fix async_transaction fixtures
- **Before**: ~463/617 passing (75.0%)
- **After**: ~478/617 passing (77.5%)
- **Improvement**: +15 tests, +2.5%

---

## Files to Edit

### Quick Fixes (15 min each)

**1. services/shared_types.py**
- Line ~8-21 (IntentCategory enum)
- Add: `PLANNING = "planning"` and `REVIEW = "review"`

**2. services/integrations/slack/spatial_types.py**
- Line ~62-69 (AttentionLevel enum)
- Add: `HIGH = "high"`, `MEDIUM = "medium"`, `LOW = "low"`

**3. services/integrations/slack/spatial_mapper.py** OR test file
- Add stub method OR add `@pytest.mark.skip()` to 4 tests

### Infrastructure Fix (1-2 hours)

**4. tests/unit/services/orchestration/test_orchestration_engine.py**
- Line ~20-25 (engine fixture)
- Add container mock

---

## Risk Assessment

### Quick Fixes (Enum Values)
- **Risk**: LOW
- **Why**: Just adding enum values that code already references
- **Rollback**: Easy (remove values)
- **Testing**: Run affected tests

### Stub Method
- **Risk**: LOW
- **Why**: Explicitly raises NotImplementedError
- **Rollback**: Easy (remove method)
- **Alternative**: Skip tests instead (zero risk)

### Container Fixture
- **Risk**: MEDIUM
- **Why**: Changes test infrastructure pattern
- **Testing**: Run all orchestration tests
- **Rollback**: Revert commit

---

## Verification Commands

```bash
# After enum fixes
pytest tests/unit/services/integrations/slack/test_workflow_integration.py -v
pytest tests/unit/services/integrations/slack/test_spatial_workflow_factory.py -v

# After stub method
pytest tests/unit/services/integrations/slack/test_workflow_pipeline_integration.py -v

# After container fixture
pytest tests/unit/services/orchestration/test_orchestration_engine.py -v

# Overall progress
pytest tests/ --tb=no -q | tail -5
```

---

## Questions for PM

1. **Enum values**: Add HIGH/MEDIUM/LOW to AttentionLevel, or map to existing values?
   - Recommend: Add (simpler, clearer intent)

2. **Stub method**: Add NotImplementedError stub, or skip tests?
   - Recommend: Skip tests (clearer that feature isn't ready)

3. **Container fixture**: Mock approach or DI refactor?
   - Recommend: Mock (faster, less invasive)

4. **Fixture errors**: Create single GitHub issue or multiple?
   - Recommend: Single issue "Fix async_transaction fixture pattern"

---

## Related Documents

- **Full Analysis**: test-failure-categorization-report.md
- **Detailed Breakdown**: test-failure-detailed-breakdown.md
- **Original Baseline**: test-suite-failure-analysis.md (from this morning)

---

**Generated**: 2025-11-19 12:08 PM
**Agent**: Claude Code (Sonnet 4.5)
