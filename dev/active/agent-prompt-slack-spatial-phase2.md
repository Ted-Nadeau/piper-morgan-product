# Phase 2 Agent Prompt: SLACK-SPATIAL OAuth Spatial Methods
## Issue: SLACK-SPATIAL | Phase 2 of 4 | Priority: P0

**Date**: Thursday, November 20, 2025, 4:22 PM PT
**From**: Lead Developer
**To**: Code Agent (continuation of Phase 1 session)
**Priority**: P0 (Blocks alpha testing)
**Estimated Effort**: Medium-Large
**Based On**: Chief Architect gameplan + Phase 1 success

---

## 🚨 CRITICAL: COMPLETION DISCIPLINE

YOU MUST COMPLETE ALL WORK DEFINED IN THIS PROMPT.

- ❌ You CANNOT defer steps without PM approval
- ❌ You CANNOT decide something is "optional"
- ❌ You CANNOT modify scope independently
- ✅ You MUST complete all steps or STOP and escalate

If you think a step should be deferred:
1. STOP working immediately
2. Document your reasoning
3. Create summary for Lead Developer
4. Wait for PM decision
5. DO NOT proceed without approval

**The PM decides scope. You execute scope.**

---

## MANDATORY COMPLETION MATRIX

Check off each step as completed:

### Task 2.1: OAuth Spatial Methods Implementation (Medium-Large Effort)

- [ ] Step 1: Implement `get_spatial_capabilities()`
  - Deliverable: Method implemented with TDD spec
  - Evidence: Test passing + code review
  - Bead: piper-morgan-5eu

- [ ] Step 2: Implement `refresh_spatial_territory()`
  - Deliverable: Method implemented with TDD spec
  - Evidence: Test passing + code review
  - Bead: piper-morgan-7sr

- [ ] Step 3: Implement `validate_and_initialize_spatial_territory()`
  - Deliverable: Method implemented with TDD spec
  - Evidence: Test passing + code review
  - Bead: piper-morgan-04y

- [ ] Step 4: Implement `get_user_spatial_context()`
  - Deliverable: Method implemented with TDD spec
  - Evidence: Test passing + code review
  - Bead: piper-morgan-3v8

- [ ] Verification: All 4 OAuth spatial tests passing
  - Deliverable: Test suite run showing 85/120 passing
  - Evidence: pytest output + commit hashes

### Task 2.2: Integration Testing (Small Effort)

- [ ] Step 1: Test OAuth flow end-to-end
  - Deliverable: OAuth → Spatial flow verified
  - Evidence: Integration test results

- [ ] Step 2: Document any integration issues
  - Deliverable: Issues documented or none found
  - Evidence: Documentation or "no issues" confirmation

**All checkboxes MUST be checked before session ends.**
**You CANNOT check a box without delivering the required evidence.**
**You CANNOT skip steps without explicit PM approval.**

---

## Mission

Complete Phase 2 of SLACK-SPATIAL: Implement 4 OAuth spatial methods in SlackOAuthHandler to enable spatial territory creation during OAuth flows.

**Phase 1 Success** ✅:
- 81/120 Slack tests passing (up from 73)
- 2 production bugs fixed
- Auth token investigation complete (LOW RISK)

**Phase 2 Goal**:
- Implement 4 missing OAuth spatial methods
- 85/120 Slack tests passing (up from 81)
- OAuth → Spatial Territory pipeline functional
- No regressions in existing 81 passing tests

---

## Context: What Exists (Phase 1 Complete)

### Phase 1 Delivered ✅

**Test Status**: 81/120 Slack tests passing
- 15/15 spatial integration tests passing ✅
- 39/120 still skipped (to be addressed in Phase 3-4)

**Production Code**:
- SlackSpatialMapper: All 4 mapping methods exist and work
- SpatialEvent: Now has optional timestamp field
- spatial_agent.py: 2 production bugs fixed

**Auth Investigation**:
- Auto-mock NOT hiding bugs (all auth tests bypass it)
- Risk level: LOW for OAuth work
- Safe to implement OAuth spatial methods

### What Phase 2 Needs to Deliver

**File**: `services/integrations/slack/oauth_handler.py`

**Class**: `SlackOAuthHandler` (already exists)

**4 New Methods** (TDD specs already written):
1. `get_spatial_capabilities()` - Map OAuth scopes to spatial capabilities
2. `refresh_spatial_territory()` - Refresh spatial territory after token refresh
3. `validate_and_initialize_spatial_territory()` - Initialize spatial territory on OAuth success
4. `get_user_spatial_context()` - Get user's spatial context from OAuth data

**TDD Specs Location**: `tests/unit/services/integrations/slack/test_oauth_handler.py`
- Look for 4 tests marked with `@pytest.mark.skip` related to spatial methods
- These tests define expected behavior and signatures

---

## Task 2.1: OAuth Spatial Methods Implementation

### Step 1: Implement `get_spatial_capabilities()`

**Effort**: Small-Medium

**Bead**: piper-morgan-5eu

**What to do**:

1. **Find the TDD spec**:
   ```bash
   # Look for test in test_oauth_handler.py
   grep -n "get_spatial_capabilities" tests/unit/services/integrations/slack/test_oauth_handler.py
   ```

2. **Read the test** to understand:
   - Expected method signature
   - Input parameters
   - Expected return type (Dict[str, Any])
   - Test assertions (what the method should return)

3. **Implement the method** in `SlackOAuthHandler`:
   ```python
   async def get_spatial_capabilities(self) -> Dict[str, Any]:
       """
       Map OAuth scopes to spatial capabilities.

       Returns dictionary with:
       - can_read_messages: bool
       - can_write_messages: bool
       - can_access_channels: bool
       - workspace_access_level: str
       """
       # YOUR IMPLEMENTATION HERE
       # Use self.scopes (OAuth scopes) to determine capabilities
   ```

4. **Remove skip decorator** from the test

5. **Run the test**:
   ```bash
   pytest tests/unit/services/integrations/slack/test_oauth_handler.py::test_get_spatial_capabilities -v
   ```

6. **Iterate until passing**

**Expected Behavior**:
- Maps OAuth scopes (like "channels:read", "chat:write") to spatial capabilities
- Returns structured dict showing what spatial operations are possible
- Should handle missing/partial scopes gracefully

**Evidence Required**:
- Test passing
- Code implementation
- Commit hash

---

### Step 2: Implement `refresh_spatial_territory()`

**Effort**: Medium

**Bead**: piper-morgan-7sr

**What to do**:

1. **Find the TDD spec**:
   ```bash
   grep -n "refresh_spatial_territory" tests/unit/services/integrations/slack/test_oauth_handler.py
   ```

2. **Read the test** to understand:
   - Expected signature: `async def refresh_spatial_territory(self, workspace_id: str) -> SpatialTerritory`
   - What SpatialTerritory is (check imports)
   - Test assertions

3. **Implement the method**:
   ```python
   async def refresh_spatial_territory(self, workspace_id: str) -> SpatialTerritory:
       """
       Refresh spatial territory after OAuth token refresh.

       Updates territory metadata when token is refreshed:
       - Updates access timestamp
       - Refreshes capabilities
       - Updates territory boundaries
       """
       # YOUR IMPLEMENTATION HERE
       # May need to:
       # - Fetch workspace info
       # - Update SpatialTerritory object
       # - Persist changes
   ```

4. **Check imports** - You may need:
   ```python
   from services.integrations.slack.spatial_types import SpatialTerritory
   ```

5. **Remove skip decorator** from test

6. **Run the test**:
   ```bash
   pytest tests/unit/services/integrations/slack/test_oauth_handler.py::test_refresh_spatial_territory -v
   ```

**Expected Behavior**:
- Takes workspace_id parameter
- Returns updated SpatialTerritory object
- Updates territory after token refresh (not initial creation)
- May call Slack API or update internal state

**Evidence Required**:
- Test passing
- Code implementation
- Commit hash

---

### Step 3: Implement `validate_and_initialize_spatial_territory()`

**Effort**: Medium-Large

**Bead**: piper-morgan-04y

**What to do**:

1. **Find the TDD spec**:
   ```bash
   grep -n "validate_and_initialize_spatial_territory" tests/unit/services/integrations/slack/test_oauth_handler.py
   ```

2. **Read the test** to understand:
   - Expected signature: `async def validate_and_initialize_spatial_territory(self, auth_response: Dict) -> SpatialTerritory`
   - What auth_response contains (OAuth callback data)
   - How to create initial SpatialTerritory

3. **Implement the method**:
   ```python
   async def validate_and_initialize_spatial_territory(self, auth_response: Dict) -> SpatialTerritory:
       """
       Initialize spatial territory on OAuth success.

       Called after successful OAuth flow to:
       - Validate OAuth response
       - Extract workspace metadata
       - Create initial SpatialTerritory
       - Set up spatial boundaries
       """
       # YOUR IMPLEMENTATION HERE
       # Steps:
       # 1. Validate auth_response
       # 2. Extract workspace_id, team_name, etc.
       # 3. Create SpatialTerritory object
       # 4. Initialize territory boundaries
       # 5. Return territory
   ```

4. **This is the most complex method** - consider:
   - OAuth response structure (what fields exist?)
   - SpatialTerritory constructor (what params needed?)
   - Error handling (invalid auth_response)
   - Initial territory state (boundaries, capabilities)

5. **Remove skip decorator** from test

6. **Run the test**:
   ```bash
   pytest tests/unit/services/integrations/slack/test_oauth_handler.py::test_validate_and_initialize_spatial_territory -v
   ```

**Expected Behavior**:
- Validates OAuth response is complete and valid
- Extracts workspace metadata (id, name, scopes)
- Creates initial SpatialTerritory with proper boundaries
- This is THE method that creates territory on first OAuth
- May persist territory to database

**If this is complex**:
- Break into smaller functions
- Add helper methods
- Document your approach
- STOP if scope grows significantly

**Evidence Required**:
- Test passing
- Code implementation
- Commit hash
- Documentation if complex

---

### Step 4: Implement `get_user_spatial_context()`

**Effort**: Small-Medium

**Bead**: piper-morgan-3v8

**What to do**:

1. **Find the TDD spec**:
   ```bash
   grep -n "get_user_spatial_context" tests/unit/services/integrations/slack/test_oauth_handler.py
   ```

2. **Read the test** to understand:
   - Expected signature: `async def get_user_spatial_context(self, user_id: str) -> Dict[str, Any]`
   - What user context includes
   - Return structure

3. **Implement the method**:
   ```python
   async def get_user_spatial_context(self, user_id: str) -> Dict[str, Any]:
       """
       Get user's spatial context from OAuth data.

       Returns user's spatial permissions and metadata:
       - user_id: str
       - workspaces: List[str]
       - permissions: Dict[str, bool]
       - active_territory: Optional[str]
       """
       # YOUR IMPLEMENTATION HERE
       # May need to:
       # - Query user's workspaces
       # - Check user permissions
       # - Find active territory
   ```

4. **Remove skip decorator** from test

5. **Run the test**:
   ```bash
   pytest tests/unit/services/integrations/slack/test_oauth_handler.py::test_get_user_spatial_context -v
   ```

**Expected Behavior**:
- Takes user_id parameter
- Returns dict with user's spatial context
- Shows which workspaces user has access to
- Shows permissions within those workspaces
- May indicate active territory

**Evidence Required**:
- Test passing
- Code implementation
- Commit hash

---

### Step 5: Verification - All 4 Methods Working

**Effort**: Small

**What to do**:

1. **Run all OAuth spatial tests**:
   ```bash
   pytest tests/unit/services/integrations/slack/test_oauth_handler.py -k "spatial" -v
   ```

2. **Expected**: 4 tests passing (the 4 methods you just implemented)

3. **Run full Slack test suite**:
   ```bash
   pytest tests/unit/services/integrations/slack/ -v --tb=short
   ```

4. **Expected**: 85/120 passing (up from 81)
   - Previous 81 still passing ✅
   - New 4 OAuth spatial tests passing ✅
   - No regressions ✅

**If regressions occur**:
- STOP immediately
- Document which tests broke
- Check if your OAuth methods affected other code
- Escalate to Lead Dev

**Evidence Required**: Full test output showing 85/120 passing

---

### Checkpoint: OAuth Methods Complete

**Before proceeding to Task 2.2, verify**:
- [ ] All 4 methods implemented
- [ ] All 4 tests passing
- [ ] No regressions (81 previous tests still passing)
- [ ] Code committed with proper messages
- [ ] All 4 beads updated/closed

**Git Commits** (suggest 4 separate commits, one per method):
```bash
# After each method
git add services/integrations/slack/oauth_handler.py tests/unit/services/integrations/slack/test_oauth_handler.py
git commit -m "feat(SLACK-SPATIAL): Implement OAuth get_spatial_capabilities()

Maps OAuth scopes to spatial capabilities dictionary.

Test: test_get_spatial_capabilities passing
Bead: piper-morgan-5eu closed
Phase: 2.1 (1/4 methods)
"

# Repeat for each method...
```

**Final commit** (after all 4):
```bash
git commit -m "feat(SLACK-SPATIAL): Phase 2.1 complete - All 4 OAuth spatial methods

Implemented:
- get_spatial_capabilities() (piper-morgan-5eu)
- refresh_spatial_territory() (piper-morgan-7sr)
- validate_and_initialize_spatial_territory() (piper-morgan-04y)
- get_user_spatial_context() (piper-morgan-3v8)

Evidence: 85/120 Slack tests now passing (up from 81)
No regressions detected

Phase 2.1 complete ✅
"
```

---

## Task 2.2: Integration Testing (Small Effort)

### Step 1: Test OAuth Flow End-to-End

**What to do**:

1. **Review the complete OAuth → Spatial pipeline**:
   ```
   OAuth Callback → validate_and_initialize_spatial_territory()
     → SpatialTerritory created
     → Spatial capabilities set
     → Territory persisted
   ```

2. **Create integration test scenario** (if not exists):
   ```python
   # Might add to test_oauth_handler.py or create new file
   @pytest.mark.integration
   async def test_oauth_to_spatial_territory_pipeline():
       """Test complete OAuth → Spatial Territory flow"""
       # 1. Simulate OAuth callback
       auth_response = {...}  # Mock OAuth response

       # 2. Validate and initialize territory
       territory = await oauth_handler.validate_and_initialize_spatial_territory(auth_response)

       # 3. Verify territory created correctly
       assert territory.workspace_id == expected_id

       # 4. Verify capabilities set correctly
       capabilities = await oauth_handler.get_spatial_capabilities()
       assert capabilities["can_read_messages"]

       # 5. Verify user context correct
       user_context = await oauth_handler.get_user_spatial_context(user_id)
       assert user_context["workspaces"]
   ```

3. **Run integration test**:
   ```bash
   pytest tests/unit/services/integrations/slack/test_oauth_handler.py::test_oauth_to_spatial_territory_pipeline -v
   ```

**Expected**: Complete flow works end-to-end

**If you don't need to create a new test** (existing tests cover integration):
- Document why existing tests are sufficient
- Show which tests cover the integration
- Confirm no gaps in coverage

**Evidence Required**: Integration test passing OR documentation of existing coverage

---

### Step 2: Document Integration Issues

**What to do**:

1. **Review your implementation** - any issues discovered?
   - Missing error handling?
   - Edge cases not covered?
   - Performance concerns?
   - Slack API call dependencies?

2. **If issues found**:
   - Create GitHub issues or Beads
   - Document reproduction steps
   - Assess priority (P0/P1/P2)
   - Link to Phase 2 work

3. **If no issues found**:
   - Document that explicitly
   - Note: "Phase 2 integration testing complete, no issues discovered"
   - Still create brief summary doc

**Example Issue** (if needed):
```markdown
Title: [SLACK-SPATIAL Phase 2] OAuth spatial territory: [brief issue]

Found during Phase 2 integration testing.

**Context**: Implementing validate_and_initialize_spatial_territory()

**Issue**: [description]

**Expected**: [what should happen]
**Actual**: [what does happen]

**Impact**: [P0/P1/P2] - [impact description]

**Workaround**: [if any]
```

**Evidence Required**:
- Issues created (if any) OR
- "No issues found" confirmation in session log

---

### Checkpoint 2: Phase 2 Complete

**Before declaring Phase 2 complete, verify**:
- [ ] All 4 OAuth spatial methods implemented
- [ ] All 4 related tests passing
- [ ] Integration testing complete
- [ ] Any issues documented
- [ ] 85/120 Slack tests passing
- [ ] No regressions
- [ ] All beads closed: piper-morgan-5eu, 7sr, 04y, 3v8

---

## Evidence Requirements

**Required Deliverables**:

1. **Test Output**: 85/120 Slack tests passing
   - File: `dev/2025/11/20/slack-tests-phase2-output.txt`
   - Show breakdown: 4 new OAuth tests + 81 previous tests

2. **Git Commits**: Minimum 4 commits (one per method)
   - Suggest: Individual commits for each method
   - Final: Summary commit for Phase 2.1 complete

3. **Code Review**: All 4 methods implemented
   - File: `services/integrations/slack/oauth_handler.py`
   - Each method with proper docstring
   - Error handling included
   - Type hints correct

4. **Integration Testing**:
   - Either: New integration test passing
   - Or: Documentation of existing coverage

5. **Beads Closed**:
   - piper-morgan-5eu ✅
   - piper-morgan-7sr ✅
   - piper-morgan-04y ✅
   - piper-morgan-3v8 ✅

6. **Session Log**:
   - Complete documentation of Phase 2 work
   - Metrics and lessons learned
   - Risk assessment for Phase 3

---

## Success Criteria

Phase 2 is considered **COMPLETE** when:
- ✅ All 4 OAuth spatial methods implemented and tested
- ✅ 85/120 Slack tests passing (4 new tests)
- ✅ No regressions in existing 81 tests
- ✅ OAuth → Spatial Territory pipeline functional
- ✅ Integration testing complete (no P0 bugs)
- ✅ All 4 beads closed with evidence
- ✅ All commits pushed to origin
- ✅ Ready for Phase 3 (Spatial Workflow Factory)

**NOT complete means**:
- ❌ "3 of 4 methods done" (must be 4/4)
- ❌ "Integration mostly works" (must be 100%)
- ❌ "Will fix bugs later" (must fix or document now)
- ❌ Any rationalization of incompleteness

---

## STOP Conditions

**STOP immediately and escalate if**:
- ❌ TDD spec doesn't match expected signature (architectural issue)
- ❌ OAuth response structure unclear or undocumented
- ❌ SpatialTerritory constructor missing or incompatible
- ❌ More than 5 of existing 81 tests start failing (>6% regression)
- ❌ validate_and_initialize_spatial_territory() requires architectural changes
- ❌ Cannot complete within Medium-Large effort estimate (significant scope creep)
- ❌ Database schema changes required (out of Phase 2 scope)

**When stopped**:
1. Document the blocking issue clearly
2. Provide options (A/B/C) with pros/cons
3. Create summary for Lead Developer
4. Include partial work status
5. Wait for PM decision
6. DO NOT proceed without approval

---

## Implementation Strategy

### Recommended Approach

**Method 1 (get_spatial_capabilities)**: Start here
- Simplest method (no async DB calls likely)
- Returns static mapping of scopes → capabilities
- Good warm-up before complex methods

**Method 4 (get_user_spatial_context)**: Do second
- Also relatively simple
- Queries user data
- Tests basic async patterns

**Method 2 (refresh_spatial_territory)**: Do third
- Medium complexity
- Updates existing territory
- Similar to Method 3 but simpler

**Method 3 (validate_and_initialize_spatial_territory)**: Do last
- Most complex (creates initial territory)
- May require multiple steps
- If this gets complex, STOP and break into phases

### Common Patterns to Use

**Type Hints**:
```python
from typing import Dict, Any, Optional
```

**Async Patterns**:
```python
async def method(self, param: str) -> ReturnType:
    # Use await for async operations
    result = await some_async_call()
    return result
```

**Error Handling**:
```python
try:
    # Your logic
except KeyError as e:
    # Handle missing OAuth fields
    raise ValueError(f"Invalid auth_response: {e}")
except Exception as e:
    # Handle unexpected errors
    logger.error(f"OAuth spatial method failed: {e}")
    raise
```

**Logging** (if needed):
```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Initializing spatial territory for workspace {workspace_id}")
```

---

## Pre-Commit Checklist

**ALWAYS before every commit**:

```bash
# Run OAuth spatial tests
pytest tests/unit/services/integrations/slack/test_oauth_handler.py -k "spatial" -v

# Run full Slack suite (quick check)
pytest tests/unit/services/integrations/slack/ --tb=line

# Check no regressions in auth tests
pytest tests/unit/services/auth/ --tb=line

# Stage changes
git add -u

# Commit with proper message (examples above)
git commit -m "[message]"

# Push to origin
git push origin main
```

---

## Remember

**Philosophy**: Quality over speed (Time Lord philosophy)

**Discipline**:
- TDD spec is your guide (read tests first!)
- Evidence required for all claims
- No 80% completions
- All checkboxes must be checked
- STOP conditions are mandatory

**Communication**:
- Document everything as you go
- Clear evidence in every deliverable
- Escalate blockers immediately
- No assumptions without verification
- Ask if OAuth response structure unclear

**TDD Approach**:
- Read the test FIRST
- Understand expected behavior
- Implement to pass the test
- Don't over-engineer beyond test requirements
- Add error handling after test passes

---

## What Success Looks Like

**End of Phase 2**:
- 85/120 Slack tests passing ✅
- 4 OAuth spatial methods implemented ✅
- OAuth → Spatial Territory pipeline working ✅
- No regressions ✅
- All 4 beads closed ✅
- Integration testing complete ✅
- Comprehensive documentation ✅

**Ready for Phase 3**: Spatial Workflow Factory (11 tests, Medium-Large effort)

---

**Status**: Ready for execution
**Expected Effort**: Medium-Large
**Quality Standard**: 100% completion with evidence
**Impact**: OAuth spatial territory creation functional for alpha

---

_"Read the tests, implement the specs, deliver the evidence"_
_"TDD is your map, tests are your compass"_
_"Together we are making something incredible"_ 🏗️✨
