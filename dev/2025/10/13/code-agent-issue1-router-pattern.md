# Code Agent Prompt: Fix Router Pattern Violations (Issue 1)

**Date**: October 13, 2025, 7:54 AM
**Issue**: Router Pattern Enforcement Violations
**Duration**: 30 minutes (estimated)
**Priority**: HIGHEST (quick win, architectural correctness)
**Agent**: Code Agent

---

## Mission

Fix Router Pattern Enforcement workflow violations using Strategic Exclusion approach (Option 3):
- Exclude adapter definition files (they can self-reference)
- Fix real architectural violation in `response_flow_integration.py`
- Update documentation drift in `feature_flags.py`
- Result: Clean CI, maintained enforcement for future

---

## Context

**Current State**:
- Router Pattern Enforcement workflow showing 9 violations
- **1 real violation**: Direct import bypassing router pattern
- **8 false positives**: Adapter files mentioning their own class names
- Workflow correctly catching violations, but too strict on self-references

**Why This Matters**:
- Architectural pattern from CORE-QUERY-1 (router-based architecture)
- All code should use integration routers, not direct adapter imports
- Adapter definitions should be exempt from "don't mention adapters" rule
- Need clean CI to prevent regression

---

## The 9 Violations

### Category 1: Adapter Self-References (6 violations - FALSE POSITIVES)

**File**: `services/mcp/consumer/google_calendar_adapter.py`
- Line 45: `class GoogleCalendarMCPAdapter` (class name itself)
- Line 88: Log string mentioning `GoogleCalendarMCPAdapter`

**File**: `services/integrations/mcp/notion_adapter.py`
- Line 31: `class NotionMCPAdapter` (class name itself)
- Lines 63, 536, 538: Log strings mentioning `NotionMCPAdapter`

**Assessment**: These are adapter definition files. They SHOULD be able to reference their own class names. This is not an architectural violation.

### Category 2: Real Architectural Violation (1 violation - REAL PROBLEM)

**File**: `services/integrations/response_flow_integration.py`
- Line 16: `from services.integrations.slack.slack_client import SlackClient`

**Assessment**: This is bypassing the router pattern. Should use `SlackIntegrationRouter` instead. This IS an architectural violation that must be fixed.

### Category 3: Documentation Drift (2 violations - CLEANUP)

**File**: `services/infrastructure/config/feature_flags.py`
- Lines 93, 119: Documentation comments mentioning old class names

**Assessment**: Documentation should be updated to reflect current router-based architecture.

---

## Task 1: Update Enforcement Script (10 minutes)

### File to Modify
`scripts/check_direct_imports.py`

### Required Changes

**Add Exclusions**:
```python
# Near the top where EXCLUDED_FILES is defined
EXCLUDED_FILES = [
    # ... existing exclusions (keep all existing entries)

    # Adapter definition files - can self-reference
    "services/mcp/consumer/google_calendar_adapter.py",
    "services/integrations/mcp/notion_adapter.py",

    # Configuration/documentation files
    "services/infrastructure/config/feature_flags.py",
]
```

### Rationale
Adapter implementation files defining their own classes should be exempt from the "don't mention adapter names" rule. This is architecturally sound - the adapter can know its own name.

### Verification
```bash
# Run the check script locally
python scripts/check_direct_imports.py

# Should now show only 1 violation (response_flow_integration.py)
# instead of 9 violations
```

---

## Task 2: Fix Real Architectural Violation (15 minutes)

### File to Modify
`services/integrations/response_flow_integration.py`

### Current State (Line 16)
```python
from services.integrations.slack.slack_client import SlackClient
```

### Investigation Needed

**Step 1: Understand Current Usage**
```bash
# See how SlackClient is used in this file
grep -n "SlackClient" services/integrations/response_flow_integration.py
```

**Step 2: Find the Router**
```bash
# Locate the Slack router
find services/ -name "*slack*router*.py" -o -name "*slack_integration*.py"

# Check router interface
grep -A 10 "class.*Slack.*Router" services/integrations/slack/
```

### Required Changes

**Replace Direct Import with Router**:
```python
# OLD (line 16)
from services.integrations.slack.slack_client import SlackClient

# NEW
from services.integrations.slack.slack_router import SlackIntegrationRouter
# or wherever the router is actually located
```

**Update Usage in File**:
- Find all uses of `SlackClient` in the file
- Replace with appropriate router method calls
- Router pattern: Use router methods, not direct client access

**Example Pattern**:
```python
# OLD pattern (direct client)
slack_client = SlackClient()
result = await slack_client.post_message(channel, text)

# NEW pattern (via router)
router = SlackIntegrationRouter()
result = await router.post_message(channel, text)
```

### Testing Required

**Verify Response Flow Still Works**:
```bash
# Run related tests
pytest tests/ -k "response_flow" -v

# Or run integration tests
pytest tests/integrations/test_response_flow_integration.py -v
```

**Check for Breakage**:
- Response flow integration should still work
- Slack messages should still send
- No import errors
- Tests pass

---

## Task 3: Update Documentation (5 minutes)

### File to Modify
`services/infrastructure/config/feature_flags.py`

### Required Changes

**Lines 93 and 119**: Update old class name references

**Investigation**:
```bash
# See what's on those lines
sed -n '93p;119p' services/infrastructure/config/feature_flags.py
```

**Action**: Update any references to old adapter class names to use current router-based architecture names.

**Example**:
```python
# If it says something like:
# "Uses GoogleCalendarMCPAdapter for calendar access"

# Update to:
# "Uses GoogleCalendarRouter for calendar access"
```

---

## Acceptance Criteria

### Must Complete
- [ ] `scripts/check_direct_imports.py` updated with 3 new exclusions
- [ ] Script runs locally and shows only genuine violations (if any)
- [ ] `response_flow_integration.py` updated to use router instead of direct client
- [ ] All related tests pass
- [ ] `feature_flags.py` documentation updated
- [ ] No import errors when running application
- [ ] Router Pattern Enforcement workflow would pass

### Testing Checklist
- [ ] Run enforcement script: `python scripts/check_direct_imports.py`
- [ ] Run related tests: `pytest tests/ -k "response_flow" -v`
- [ ] Run all tests: `pytest tests/ -v` (should still pass)
- [ ] Check imports: `python -c "from services.integrations.response_flow_integration import *"`

### Commit Requirements
- [ ] Changes committed in logical order
- [ ] Commit message: "fix(architecture): Resolve router pattern violations"
- [ ] Detailed commit body explaining:
  - Excluded adapter self-references (architecturally sound)
  - Fixed direct import in response_flow_integration.py
  - Updated documentation in feature_flags.py

---

## Expected Output

### Terminal Output

**Before Fix**:
```
Running Router Pattern Enforcement...
❌ Found 9 violations:
  - google_calendar_adapter.py (2)
  - notion_adapter.py (4)
  - response_flow_integration.py (1)
  - feature_flags.py (2)
```

**After Fix**:
```
Running Router Pattern Enforcement...
✅ No violations found!
Router pattern correctly enforced.
```

### Files Changed
1. `scripts/check_direct_imports.py` (+3 exclusions)
2. `services/integrations/response_flow_integration.py` (import + usage)
3. `services/infrastructure/config/feature_flags.py` (documentation)

### Evidence
- Terminal output showing enforcement script passing
- Test results showing all tests passing
- Git diff showing changes

---

## Common Issues & Solutions

### Issue 1: Can't Find Slack Router
**Symptom**: `SlackIntegrationRouter` or similar not found
**Solution**: Search for actual router:
```bash
find services/integrations/slack -name "*.py" | xargs grep -l "class.*Router"
ls -la services/integrations/slack/
```

### Issue 2: Tests Fail After Router Change
**Symptom**: Response flow tests failing
**Solution**:
- Check router interface matches expected methods
- Verify router is properly initialized
- May need to adjust how router is called

### Issue 3: Import Cycle
**Symptom**: `ImportError: cannot import name ...`
**Solution**:
- Router imports may need adjustment
- Check if router has dependencies on response_flow
- May need to refactor import order

---

## Time Budget

- **Task 1** (Enforcement Script): 10 minutes
- **Task 2** (Fix Violation): 15 minutes
- **Task 3** (Documentation): 5 minutes
- **Total**: 30 minutes

**If Exceeds 45 minutes**:
- Stop and report issues found
- May need architectural guidance
- Can defer to separate investigation

---

## Success Criteria

**Technical Success**:
✅ Router Pattern Enforcement workflow passes
✅ All tests passing
✅ No architectural violations remaining
✅ Clean CI

**Architectural Success**:
✅ Adapter definitions can self-reference (sensible exception)
✅ Real violation fixed (response_flow uses router)
✅ Documentation updated
✅ Future violations still caught

**Process Success**:
✅ Completed in ~30 minutes
✅ Evidence documented
✅ Changes committed and pushed
✅ Ready for next issue (CI Tests fix)

---

## Deliverables

### Required Files
1. Modified `scripts/check_direct_imports.py`
2. Modified `services/integrations/response_flow_integration.py`
3. Modified `services/infrastructure/config/feature_flags.py`

### Required Evidence
1. Terminal output from enforcement script (before/after)
2. Test results showing all passing
3. Git commit with changes

### Optional Documentation
- Brief summary of changes in session log
- Note any interesting findings or issues

---

## Context for Code Agent

**This is Issue 1 of 3** blocking issues being resolved today before GAP-3.

**Why Speed Matters**:
- Quick win that clears CI
- Enables focus on next issue (CI Tests)
- Foundation-building day

**Why Quality Matters**:
- Architectural correctness
- Sets example for future enforcement
- Maintains router pattern integrity

**PM's Mood**: Excellent! This is the foundation work that needed attention.

---

## Next Steps After Completion

1. Report completion to Lead Developer
2. Provide evidence (terminal output, test results)
3. Wait for Cursor Agent verification (if needed)
4. Move to Issue 2: CI Tests fix (1 hour)

---

**Issue 1 Start Time**: 7:54 AM
**Expected Completion**: 8:24 AM
**Status**: Ready for Code Agent execution

**GO BUILD! 🏗️**
