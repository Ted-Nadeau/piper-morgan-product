# Cursor Agent Prompt: Phase 0 - MCP Architecture Cross-Validation

## Your Identity
You are Cursor Agent, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- CURRENT-STATE.md - Current epic and focus
- role/PROGRAMMER.md - Your role requirements
- METHODOLOGY.md - Inchworm Protocol

## Session Log Management

**If you have not already started a session log for this session**:
- Create one at: `dev/2025/09/28/2025-09-28-1702-prog-cursor-log.md`

**If you already have a session log running**:
- Continue using existing log
- Add timestamped entry for Phase 0 work

## Mission: Cross-Validate MCP Architecture Understanding

**Context**: Code agent has completed Phase 0 investigation of MCP architecture patterns across Slack, Notion, and Calendar integrations. Your role is to independently verify findings and identify any gaps, inconsistencies, or edge cases before router wrapper implementation begins.

**Objective**: Provide independent verification that MCP architecture is correctly understood and router wrapper design patterns are sound.

## Code's Investigation to Validate

Code agent will have documented:
1. MCP adapter inventory and locations
2. BaseSpatialAdapter pattern analysis
3. Current service usage patterns
4. Feature flag system understanding
5. Router wrapper design recommendations

## Your Verification Tasks

### Task 1: Verify MCP Adapter Completeness

```bash
# Independent search for MCP adapters
echo "=== Independent MCP Adapter Search ==="
find . -type f -name "*.py" | xargs grep -l "class.*Adapter" | grep -i "mcp\|calendar\|notion"

# Check for any missed adapters
find services/integrations/ -name "*adapter*" -o -name "*mcp*" 2>/dev/null
```

**Verify**: Did Code find all MCP adapters, or are there additional ones?

### Task 2: Test Adapter Functionality

Verify adapters actually work as Code documented:

```python
# Test Calendar adapter can initialize
try:
    from services.mcp.consumer.google_calendar_adapter import GoogleCalendarAdapter
    adapter = GoogleCalendarAdapter()
    print("✅ Calendar adapter initializes")
except Exception as e:
    print(f"❌ Calendar adapter failed: {e}")

# Test Notion adapter can initialize
try:
    from services.integrations.mcp.notion_adapter import NotionAdapter
    adapter = NotionAdapter()
    print("✅ Notion adapter initializes")
except Exception as e:
    print(f"❌ Notion adapter failed: {e}")

# Check method availability
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarAdapter
adapter = GoogleCalendarAdapter()
methods = [m for m in dir(adapter) if not m.startswith('_') and callable(getattr(adapter, m))]
print(f"Calendar adapter methods: {len(methods)}")
for method in sorted(methods):
    print(f"  - {method}")
```

**Verify**: Do adapters actually initialize and provide documented methods?

### Task 3: Check BaseSpatialAdapter Pattern

```bash
# Find base adapter class
find . -name "*base*adapter*.py" -type f

# If found, verify Code's documentation is accurate
# [Read base class and compare to Code's description]
```

**Verify**: Does BaseSpatialAdapter provide what Code documented?

### Task 4: Validate Service Usage Patterns

```bash
# Cross-check Code's findings on service usage
echo "=== Services Using Calendar ==="
grep -r "GoogleCalendarAdapter" services/ --include="*.py" -n | grep -v "test"

echo "=== Services Using Notion ==="
grep -r "NotionAdapter" services/ --include="*.py" -n | grep -v "test"

echo "=== Services Using Slack ==="
grep -r "SlackClient\|SlackSpatial" services/ --include="*.py" -n | grep -v "test" | head -20
```

**Verify**: Are Code's service usage findings accurate and complete?

### Task 5: Test Feature Flag Pattern

```bash
# Verify feature flag pattern from GitHub router
echo "=== GitHub Router Feature Flag ==="
grep -A 5 "USE_SPATIAL_GITHUB" services/integrations/github/github_integration_router.py

echo "=== Feature Flag Checking Pattern ==="
grep -B 2 -A 5 "os.getenv.*SPATIAL" services/integrations/github/github_integration_router.py
```

**Verify**: Is Code's understanding of feature flag pattern correct?

### Task 6: Check Edge Cases

Look for patterns Code might have missed:

```bash
# Check for error handling patterns
echo "=== Error Handling in Adapters ==="
grep -n "try:\|except\|raise" services/mcp/consumer/google_calendar_adapter.py | head -20

# Check for OAuth/auth patterns
echo "=== Authentication Patterns ==="
grep -n "auth\|oauth\|token\|credential" services/mcp/consumer/google_calendar_adapter.py -i | head -15

# Check for async patterns
echo "=== Async Patterns ==="
grep -n "async def\|await" services/mcp/consumer/google_calendar_adapter.py | head -10
```

**Document**: Any patterns Code didn't mention that router wrappers need to handle?

### Task 7: Verify Router Wrapper Design

Review Code's router wrapper recommendations against actual patterns:

```python
# Test if proposed delegation pattern would work
# [Create minimal test of router pattern Code proposed]
```

**Verify**: Would Code's proposed router wrapper patterns actually work with existing adapters?

## Cross-Validation Report Format

```markdown
# Phase 0: MCP Architecture Cross-Validation Report

## Verification Summary
[CONFIRMED / GAPS_FOUND / ISSUES_IDENTIFIED]

## MCP Adapter Inventory

### Code's Findings
[List what Code documented]

### Verification Results
- ✅ Confirmed: [What matched]
- ⚠️ Missing: [What Code missed]
- ❌ Incorrect: [What Code got wrong]

## Adapter Functionality Testing

### Calendar Adapter
- Initialization: [WORKS / FAILS / NOTES]
- Methods Available: [Count and any discrepancies]
- OAuth Pattern: [VERIFIED / ISSUES]

### Notion Adapter
- Initialization: [WORKS / FAILS / NOTES]
- Methods Available: [Count and any discrepancies]

### Slack Pattern
- [Verification of Code's Slack findings]

## BaseSpatialAdapter Verification

**Code's Documentation**: [Summary]
**Verification**: [ACCURATE / INACCURATE / PARTIAL]
**Issues Found**: [Any problems]

## Service Usage Pattern Verification

### Calendar Usage
**Code Found**: [X services]
**Actually Found**: [Y services]
**Discrepancies**: [Any differences]

### Notion Usage
[Similar format]

### Slack Usage
[Similar format]

## Feature Flag Pattern Verification

**Code's Understanding**: [Summary]
**Verification**: [CORRECT / NEEDS ADJUSTMENT]
**GitHub Router Pattern**: [Actual pattern from code]

## Edge Cases Identified

### Error Handling
[Patterns that router wrappers must handle]

### Authentication
[OAuth/auth considerations for router wrappers]

### Async Patterns
[Any async/await patterns to preserve]

### Other Edge Cases
[Anything else Code might have missed]

## Router Wrapper Design Assessment

### Code's Proposed Patterns
[Summary of Code's recommendations]

### Assessment
- ✅ Sound Patterns: [What would work]
- ⚠️ Needs Adjustment: [What needs refinement]
- ❌ Won't Work: [What needs rethinking]

### Additional Recommendations
[Any patterns or considerations Code didn't mention]

## Questions Requiring Resolution

[List any uncertainties, conflicts, or unclear patterns]

## Readiness Assessment

[READY_FOR_PHASE_1 / NEEDS_MORE_INVESTIGATION / BLOCKING_ISSUES]

### If Ready
Router wrapper implementation can proceed with documented patterns

### If Not Ready
[Specific issues that must be resolved first]
```

## Update Requirements

After completing cross-validation:

1. **Update Session Log**: Add Phase 0 verification completion
2. **Update GitHub Issue #199**: Add comment with cross-validation findings
3. **Tag Lead Developer**: Report verification results and readiness for Phase 1

## Critical Verification Standards

- **Independent Investigation**: Don't just confirm Code's work, verify independently
- **Functional Testing**: Actually try to initialize and use adapters
- **Edge Case Detection**: Look for patterns Code might have missed
- **Constructive Feedback**: If issues found, provide specific, actionable corrections
- **Evidence Required**: Back all findings with actual command output or code inspection

## Questions to Ask

- Did Code's investigation miss any adapters or patterns?
- Do adapters actually work as documented?
- Are there error handling or authentication patterns not mentioned?
- Would proposed router wrapper patterns actually work?
- Are there edge cases that would break the router design?

---

**Your Mission**: Independently verify MCP architecture understanding before router implementation begins. Find gaps, validate findings, identify edge cases.

**Quality Standard**: Thorough cross-validation prevents implementation failures - catch issues now rather than during router development.
