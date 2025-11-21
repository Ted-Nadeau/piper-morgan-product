# Phase 1 Agent Prompt: SLACK-SPATIAL Quick Wins & Auth Fix
## Issue: SLACK-SPATIAL | Phase 1 of 4 | Priority: P0

**Date**: Thursday, November 20, 2025, 3:50 PM PT
**From**: Lead Developer
**To**: Code Agent (continuation of Phase 0 session)
**Priority**: P0 (Blocks alpha testing)
**Estimated Effort**: Medium
**Based On**: Chief Architect gameplan + Phase 0 diagnostic (completed 2:08 PM)

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

### Task 1.1: Slack Quick Wins (Small Effort)
- [ ] Step 1: Remove skip from TestSlackEventHandler (6 tests)
  - Deliverable: 6 tests now running
  - Evidence: Test output showing 6 passing

- [ ] Step 2: Add timestamp field to SpatialEvent
  - Deliverable: Field added, dataclass updated
  - Evidence: Code changes + 2 tests passing

- [ ] Step 3: Remove skip from TestSpatialIntegration (2 tests)
  - Deliverable: 2 tests now running
  - Evidence: Test output showing 2 passing

- [ ] Verification: All 8 tests passing, no regressions
  - Deliverable: Test suite run showing 81/120 passing
  - Evidence: pytest output + commit hash

### Task 1.2: Token Blacklist Investigation (Medium Effort)
- [ ] Step 1: Temporarily disable autouse in conftest.py:50
  - Deliverable: conftest.py modified (commented or disabled)
  - Evidence: Diff showing change

- [ ] Step 2: Run auth test suite
  - Deliverable: Full auth test output captured
  - Evidence: `pytest tests/unit/services/auth/ -v > auth-tests-raw.txt`

- [ ] Step 3: Categorize failures
  - Deliverable: Analysis document with 3 categories
  - Evidence: Document showing async/blacklist/other breakdown

- [ ] Step 4: Re-enable auto-mock with documentation
  - Deliverable: conftest.py restored with explanation comment
  - Evidence: Diff + documentation in conftest

- [ ] Step 5: Create issues for discovered bugs
  - Deliverable: GitHub issues or Beads for real bugs
  - Evidence: Issue links in investigation doc

**All checkboxes MUST be checked before session ends.**
**You CANNOT check a box without delivering the required evidence.**
**You CANNOT skip steps without explicit PM approval.**

---

## Mission

Complete Phase 1 of SLACK-SPATIAL: Recover 8 quick-win tests and investigate hidden auth token bugs.

**Key Discovery from Phase 0**: All 4 "missing" SlackSpatialMapper methods actually exist! Tests are skipped due to outdated decorators, not missing functionality.

**Success looks like**:
- 81/120 Slack tests passing (up from 73)
- SpatialEvent timestamp bug fixed
- Auth token issues documented with clear decision path
- No regressions in existing 73 passing tests

---

## Context: What Already Exists (Phase 0 Complete)

### Your Phase 0 Diagnostic Found ✅

**Total Slack Tests**: 120 (73 passing, 47 skipped)

**Quick Win Categories**:
- **Category 3** (6 tests): Implementation complete, skip not removed
  - File: `tests/unit/services/integrations/slack/test_spatial_integration.py`
  - Tests: TestSlackEventHandler methods (lines 36-38)
  - Bead: piper-morgan-1i5

- **Category 4** (2 tests): SpatialEvent missing timestamp field
  - File: `services/integrations/slack/spatial_types.py`
  - Tests expect `timestamp: datetime` field
  - Bead: piper-morgan-1i5

**All 4 "Missing" Methods Now Exist** ✅:
- `map_message_to_spatial_object` (lines 361-394)
- `map_reaction_to_emotional_marker` (lines 573-638)
- `map_mention_to_attention_attractor` (lines 469-543)
- `map_channel_to_room` (lines 188-205)

### Token Blacklist Issue

**Location**: `tests/conftest.py` lines 50-86

**Problem**:
- `autouse=True` fixture always mocks TokenBlacklist.is_blacklisted() → False
- HIGH RISK: May hide auth/token revocation bugs
- Affects ALL tests automatically

**Decision**: Option C (Temporary Disable)
1. Disable autouse
2. Run auth tests
3. Categorize failures (async context / blacklist / other)
4. Re-enable with documentation
5. Create issues for real bugs

---

## Task 1.1: Slack Quick Wins (Small Effort)

### Step 1: Remove Skip Decorators from TestSlackEventHandler

**File**: `tests/unit/services/integrations/slack/test_spatial_integration.py`

**What to do**:
1. Locate TestSlackEventHandler class (around line 36-38)
2. Find these 6 test methods with `@pytest.mark.skip`:
   - Tests for message_to_spatial_object
   - Tests for reaction_to_emotional_marker
   - Tests for mention_to_attention_attractor
   - Tests for channel_to_room
   - (Check diagnostic for exact method names)

3. Remove ONLY the `@pytest.mark.skip` decorator line
4. Leave test code unchanged

**Expected Result**: 6 tests now run and pass

**If they fail**:
- STOP and document failure
- Check if method signatures changed
- Verify imports are correct
- Escalate to Lead Dev if architectural issue

**Evidence Required**:
```bash
# Run just these tests
pytest tests/unit/services/integrations/slack/test_spatial_integration.py::TestSlackEventHandler -v

# Capture output showing 6 passing
```

---

### Step 2: Add Timestamp Field to SpatialEvent

**File**: `services/integrations/slack/spatial_types.py`

**What to do**:
1. Locate the `SpatialEvent` dataclass
2. Add field: `timestamp: datetime`
3. Place it logically (probably after event_id or event_type)
4. Add import if needed: `from datetime import datetime`

**Example**:
```python
from datetime import datetime
from dataclasses import dataclass

@dataclass
class SpatialEvent:
    event_id: str
    event_type: str
    timestamp: datetime  # NEW FIELD
    # ... other fields
```

**Expected Result**: 2 tests now pass (tests expecting timestamp field)

**Evidence Required**:
```bash
# Run tests expecting timestamp
pytest tests/unit/services/integrations/slack/test_spatial_integration.py -k "timestamp" -v

# Capture output showing 2 passing
```

---

### Step 3: Remove Skip from TestSpatialIntegration

**File**: `tests/unit/services/integrations/slack/test_spatial_integration.py`

**What to do**:
1. Locate TestSpatialIntegration class
2. Find 2 test methods with `@pytest.mark.skip` related to timestamp
3. Remove skip decorators

**Expected Result**: 2 tests now pass

**Evidence Required**:
```bash
# Run full TestSpatialIntegration
pytest tests/unit/services/integrations/slack/test_spatial_integration.py::TestSpatialIntegration -v
```

---

### Step 4: Verification - No Regressions

**What to do**:
1. Run FULL Slack test suite
2. Verify 81/120 passing (73 baseline + 8 recovered)
3. Verify 0 new failures

**Command**:
```bash
pytest tests/unit/services/integrations/slack/ -v --tb=short
```

**Expected**:
- 81 passing (up from 73)
- 39 skipped (down from 47)
- 0 failures

**If regressions occur**:
- STOP immediately
- Document which tests broke
- Provide pytest output
- Escalate to Lead Dev

**Evidence Required**: Full test output showing 81 passing

---

### Checkpoint 1: Quick Wins Complete

**Before proceeding to Task 1.2, verify**:
- [ ] All 8 tests now passing
- [ ] No regressions in existing 73 tests
- [ ] Code changes committed
- [ ] Bead piper-morgan-1i5 updated (partial completion)

**Git Commit**:
```bash
git add -A
git commit -m "feat(SLACK-SPATIAL): Phase 1.1 - Recover 8 quick-win tests

- Removed skip decorators from TestSlackEventHandler (6 tests)
- Added timestamp field to SpatialEvent dataclass (2 tests)
- Removed skip from TestSpatialIntegration timestamp tests (2 tests)

Evidence: 81/120 Slack tests now passing (up from 73)
No regressions detected

Bead: piper-morgan-1i5 (partial - quick wins complete)
"
```

---

## Task 1.2: Token Blacklist Investigation (Medium Effort)

### Background: Why This Matters

The `autouse=True` fixture in conftest.py automatically mocks TokenBlacklist for ALL tests. This could hide:
- Token revocation bugs
- Auth flow issues
- Blacklist logic errors

We need to know what's REALLY happening with auth tests.

---

### Step 1: Disable Auto-Mock

**File**: `tests/conftest.py`

**Effort**: Very small

**What to do**:
1. Locate fixture around line 50-86 (check your Phase 0 notes)
2. Find `autouse=True` parameter
3. Change to `autouse=False` (or comment out the fixture)
4. Add explanatory comment

**Example**:
```python
@pytest.fixture(autouse=False)  # TEMP DISABLED FOR INVESTIGATION - Phase 1.2
async def mock_token_blacklist(monkeypatch):
    """
    Temporarily disabled to investigate hidden auth bugs.
    See: SLACK-SPATIAL Phase 1.2 investigation
    Date: 2025-11-20
    """
    # ... rest of fixture
```

**Commit immediately** (for easy rollback):
```bash
git add tests/conftest.py
git commit -m "temp(SLACK-SPATIAL): Disable autouse for token blacklist investigation

Phase 1.2 investigation - will re-enable after analysis
"
```

---

### Step 2: Run Auth Test Suite

**Effort**: Small

**What to do**:
1. Run full auth test suite with verbose output
2. Capture ALL output (don't stop on first failure)
3. Save to investigation document

**Command**:
```bash
pytest tests/unit/services/auth/ -v --tb=short --maxfail=999 > dev/2025/11/20/auth-tests-without-automock.txt 2>&1
```

**Also capture summary**:
```bash
pytest tests/unit/services/auth/ --tb=line | tee -a dev/2025/11/20/auth-tests-without-automock.txt
```

**Expected**: Some tests will fail (that's the point!)

**Evidence Required**: Full test output file

---

### Step 3: Categorize Failures

**Effort**: Medium (requires analysis)

**Create Document**: `dev/2025/11/20/token-blacklist-investigation-results.md`

**Analysis Template**:
```markdown
# Token Blacklist Investigation Results
**Date**: 2025-11-20 [time]
**Phase**: SLACK-SPATIAL Phase 1.2
**Context**: Investigating autouse=True fixture hiding potential bugs

## Summary

**Total auth tests**: [X]
**Passing with autouse disabled**: [X]
**Failing with autouse disabled**: [X]

## Failure Categories

### Category 1: Async Context Errors
**Count**: [X]
**Pattern**: RuntimeError: Event loop is closed / No running event loop
**Assessment**: Test infrastructure issue, NOT actual bugs
**Action**: Document for later async test fixture improvements

**Examples**:
- test_xyz: [error message]
- test_abc: [error message]

### Category 2: Blacklist Behavior
**Count**: [X]
**Pattern**: Tests expect TokenBlacklist.is_blacklisted() calls
**Assessment**: Tests need blacklist logic, NOT bugs
**Action**: Keep using mock (these tests verify blacklist integration)

**Examples**:
- test_token_revocation: [error message]
- test_blacklist_check: [error message]

### Category 3: Real Bugs (if any)
**Count**: [X]
**Pattern**: Unexpected failures not matching above
**Assessment**: May be real auth/token bugs
**Action**: Create GitHub issues/Beads

**Examples**:
- test_xyz: [detailed analysis]

## Recommendations

1. [Recommendation for Category 1]
2. [Recommendation for Category 2]
3. [Recommendation for Category 3]

## Decision

[Should autouse stay? Should tests be fixed? Should issues be created?]
```

**Your Job**: Fill out this template accurately by analyzing the test failures

---

### Step 4: Re-Enable Auto-Mock with Documentation

**Effort**: Small

**What to do**:
1. Revert conftest.py to `autouse=True`
2. Add comprehensive documentation explaining:
   - Why auto-mock exists
   - What it's hiding
   - When it should be disabled
   - Investigation results from Phase 1.2

**Example**:
```python
@pytest.fixture(autouse=True)
async def mock_token_blacklist(monkeypatch):
    """
    Automatically mocks TokenBlacklist.is_blacklisted() to return False.

    Why this exists:
    - Prevents token blacklist checks from failing during normal testing
    - Many tests don't care about blacklist logic
    - Simplifies test setup

    What it's hiding:
    - Investigated 2025-11-20 in SLACK-SPATIAL Phase 1.2
    - Found: [X] async context errors, [X] legitimate blacklist tests
    - Real bugs: [X] (see investigation results)

    When to disable:
    - When specifically testing token revocation flows
    - When debugging auth integration issues
    - Use autouse=False and handle blacklist explicitly in those tests

    Investigation: dev/2025/11/20/token-blacklist-investigation-results.md
    """
    async def mock_is_blacklisted(token: str) -> bool:
        return False

    monkeypatch.setattr(
        "services.auth.token_blacklist.TokenBlacklist.is_blacklisted",
        mock_is_blacklisted
    )
```

**Commit**:
```bash
git add tests/conftest.py
git commit -m "docs(SLACK-SPATIAL): Re-enable autouse with investigation results

Phase 1.2 investigation complete
- Categorized [X] failures
- Found [X] async context errors (test infrastructure)
- Found [X] legitimate blacklist tests (expected)
- Found [X] potential real bugs (issues created)

See: dev/2025/11/20/token-blacklist-investigation-results.md
"
```

---

### Step 5: Create Issues for Real Bugs

**Effort**: Small (depends on findings)

**If Category 3 has any items**:
1. Create GitHub issues or Beads
2. Provide clear reproduction steps
3. Link to investigation document

**Example Issue**:
```markdown
Title: [SLACK-SPATIAL Phase 1.2] Auth bug: [brief description]

Found during token blacklist investigation.

**Reproduction**:
1. Disable autouse in conftest.py
2. Run: pytest tests/unit/services/auth/test_xyz.py -v
3. See: [error]

**Expected**: [what should happen]
**Actual**: [what does happen]

**Investigation**: dev/2025/11/20/token-blacklist-investigation-results.md
**Category**: Real bug (not async context or blacklist test)
```

**If no real bugs found**: Document that clearly in investigation results

---

### Checkpoint 2: Investigation Complete

**Before declaring Phase 1 complete, verify**:
- [ ] Investigation document created with all 3 categories
- [ ] Auto-mock re-enabled with documentation
- [ ] Issues created for any real bugs
- [ ] conftest.py has comprehensive explanation
- [ ] Bead piper-morgan-otf updated (investigation complete)

---

## Evidence Requirements

**Required Deliverables**:
1. **Test Output**: 81/120 Slack tests passing
   - File: `dev/2025/11/20/slack-tests-phase1-output.txt`

2. **Git Commits**: Minimum 3 commits
   - Quick wins (skip removal + timestamp)
   - Auto-mock disable (temporary)
   - Auto-mock re-enable (with docs)

3. **Investigation Document**: Complete analysis
   - File: `dev/2025/11/20/token-blacklist-investigation-results.md`
   - All 3 categories analyzed
   - Clear recommendations

4. **Beads Updated**:
   - piper-morgan-1i5: Mark quick wins complete
   - piper-morgan-otf: Mark investigation complete

---

## Success Criteria

Phase 1 is considered **COMPLETE** when:
- ✅ 81/120 Slack tests passing (8 recovered)
- ✅ SpatialEvent has timestamp field
- ✅ No regressions in existing 73 tests
- ✅ Token blacklist investigation complete with analysis
- ✅ Auto-mock re-enabled with comprehensive documentation
- ✅ Any real bugs have issues created
- ✅ All evidence documented
- ✅ All commits pushed to origin

**NOT complete means**:
- ❌ "7 of 8 tests passing" (must be 8/8)
- ❌ "Investigation mostly done" (must be 100%)
- ❌ "Will create issues later" (must create now)
- ❌ Any rationalization of incompleteness

---

## STOP Conditions

**STOP immediately and escalate if**:
- ❌ More than 2 of the 8 quick-win tests fail (architectural issue)
- ❌ Token blacklist investigation reveals auth bugs beyond Slack
- ❌ SpatialEvent timestamp causes cascading failures
- ❌ Existing 73 passing tests start failing (>5 regressions)
- ❌ Investigation reveals systemic auth architecture problems
- ❌ Scope significantly exceeds medium effort estimate

**When stopped**:
1. Document the blocking issue
2. Provide options (A/B/C)
3. Create summary for Lead Developer
4. Wait for PM decision
5. DO NOT proceed without approval

---

## Effort Breakdown

**Overall**: Medium

**Task 1.1 (Quick wins)**: Small
  - Step 1 (6 tests): Very small
  - Step 2 (timestamp): Very small
  - Step 3 (2 tests): Very small
  - Step 4 (verification): Very small

**Task 1.2 (Investigation)**: Medium
  - Step 1 (disable): Very small
  - Step 2 (run tests): Small
  - Step 3 (categorize): Medium (analysis required)
  - Step 4 (re-enable): Small
  - Step 5 (create issues): Small (depends on findings)

**Documentation/commits**: Small

**If effort grows significantly**: STOP and report progress, don't skip steps

---

## Pre-Commit Checklist

**ALWAYS before every commit**:

```bash
# Run affected tests
pytest tests/unit/services/integrations/slack/ -v

# Verify no regressions
pytest tests/unit/services/auth/ --tb=line  # Quick check

# Stage changes
git add -u

# Commit with proper message (examples provided above)
git commit -m "[message]"

# Push to origin
git push origin main
```

---

## Remember

**Philosophy**: Quality over speed (Time Lord philosophy)

**Discipline**:
- Evidence required for all claims
- No 80% completions
- All checkboxes must be checked
- STOP conditions are mandatory

**Communication**:
- Document everything as you go
- Clear evidence in every deliverable
- Escalate blockers immediately
- No assumptions without verification

---

## What Success Looks Like

**End of Phase 1**:
- 81/120 Slack tests passing ✅
- 8 quick-win tests recovered ✅
- Token blacklist investigation complete ✅
- Clear path forward to Phase 2 ✅
- No hidden auth bugs affecting Slack ✅
- Comprehensive documentation ✅

**Ready for Phase 2**: OAuth spatial methods implementation

---

**Status**: Ready for execution
**Expected Effort**: Medium
**Quality Standard**: 100% completion with evidence
**Impact**: Unblocks Slack integration for alpha testing

---

_"Recover the quick wins, investigate the mysteries"_
_"Evidence, not claims"_
_"Together we are making something incredible"_ 🏗️✨
