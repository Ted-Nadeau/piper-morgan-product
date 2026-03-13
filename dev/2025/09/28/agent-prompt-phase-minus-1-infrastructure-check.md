# Claude Code Prompt: Phase -1 Infrastructure Reality Check

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- CURRENT-STATE.md - Current epic and focus
- role/PROGRAMMER.md - Your role requirements
- METHODOLOGY.md - Inchworm Protocol

## Session Log Management (CRITICAL)

**If you have not already started a session log for this session**:
- Create one at: `dev/2025/09/28/2025-09-28-1702-prog-code-log.md`
- Update throughout work with evidence and progress

**If you already have a session log running**:
- Continue using the existing log
- Do NOT create a new one
- Add timestamped entry for Phase -1 work

## Mission: Infrastructure Reality Check (30 minutes max)

**Context**: CORE-QUERY-1 requires completing Slack, Notion, and Calendar routers. GitHub router was completed yesterday in GREAT-2B. Before proceeding with router audits, verify infrastructure matches gameplan assumptions.

**Objective**: Verify actual integration structure exists as gameplan expects, or report mismatches for gameplan revision.

## What the Gameplan Assumes

The gameplan makes these assumptions about infrastructure:

1. **Router Files Exist** (or can be created):
   - `services/integrations/slack/*router*` (may not exist)
   - `services/integrations/notion/*router*` (may not exist)
   - `services/integrations/calendar/*router*` (may not exist)

2. **Integration Clients Exist**:
   - Slack client/agent with multiple methods
   - Notion client/agent with multiple methods
   - Calendar client/agent with multiple methods

3. **Spatial/MCP Systems Referenced in GREAT-2A**:
   - Slack: 20+ spatial_*.py files found in GREAT-2A investigation
   - Notion: MCP-based integration mentioned
   - Calendar: MCP-based integration mentioned

4. **Service Directory Structure**:
   - `services/integrations/` contains subdirectories for each integration
   - Services can import from integration clients
   - Feature flag system exists (USE_SPATIAL_* pattern from GitHub)

## Verification Commands

Execute these commands and report findings:

```bash
# 1. Verify integration directory structure
echo "=== Integration Directory Structure ==="
ls -la services/integrations/

# 2. Check for router files
echo "=== Existing Router Files ==="
find services/integrations/ -name "*router*" -type f 2>/dev/null || echo "No router files found"

# 3. Check Slack integration structure
echo "=== Slack Integration Files ==="
ls -la services/integrations/slack/ 2>/dev/null || echo "Slack directory not found"
find services/integrations/slack/ -name "*.py" -type f 2>/dev/null | head -20

# 4. Check Notion integration structure
echo "=== Notion Integration Files ==="
ls -la services/integrations/notion/ 2>/dev/null || echo "Notion directory not found"
find services/integrations/notion/ -name "*.py" -type f 2>/dev/null | head -20

# 5. Check Calendar integration structure
echo "=== Calendar Integration Files ==="
ls -la services/integrations/calendar/ 2>/dev/null || echo "Calendar directory not found"
find services/integrations/calendar/ -name "*.py" -type f 2>/dev/null | head -20

# 6. Verify spatial system files (from GREAT-2A findings)
echo "=== Spatial System Files ==="
find services/integrations/ -name "spatial*.py" -type f 2>/dev/null || echo "No spatial files found"

# 7. Verify MCP references
echo "=== MCP System References ==="
grep -r "mcp" services/integrations/ --include="*.py" 2>/dev/null | head -20 || echo "No MCP references found"

# 8. Check for existing integration clients (not routers)
echo "=== Integration Client Files ==="
find services/integrations/slack/ -name "*client*.py" -o -name "*agent*.py" 2>/dev/null || echo "No Slack client found"
find services/integrations/notion/ -name "*client*.py" -o -name "*agent*.py" 2>/dev/null || echo "No Notion client found"
find services/integrations/calendar/ -name "*client*.py" -o -name "*agent*.py" 2>/dev/null || echo "No Calendar client found"

# 9. Verify feature flag system exists
echo "=== Feature Flag System ==="
grep -r "USE_SPATIAL" services/ --include="*.py" 2>/dev/null | head -10 || echo "No feature flag references found"
grep -r "USE_SPATIAL" config/ --include="*.md" 2>/dev/null || echo "No config flags found"
```

## Reality Check Criteria

### Report GREEN (Proceed) If:
- All three integration directories exist
- Each has identifiable client/agent files
- Spatial/MCP systems are present as expected
- Structure matches GitHub router pattern from GREAT-2B

### Report YELLOW (Minor Issues) If:
- Integrations exist but structure differs from GitHub pattern
- Some spatial/MCP files missing but core clients exist
- Routers partially implemented but need completion

### Report RED (STOP - Need Revised Gameplan) If:
- Integration directories don't exist
- No identifiable clients/agents found
- Spatial/MCP systems completely absent
- Structure fundamentally different from assumptions

## Evidence Requirements

For your Phase -1 report, provide:

```markdown
# Phase -1 Infrastructure Reality Check Report

## Executive Summary
[GREEN/YELLOW/RED] - [One sentence assessment]

## Verification Results

### Integration Directory Structure
[Output from ls command]
[Assessment: Does structure exist as expected?]

### Slack Integration
- **Directory exists**: [YES/NO]
- **Client/agent files found**: [list files or "NONE"]
- **Spatial system present**: [YES/NO - file count]
- **Router exists**: [YES/NO/PARTIAL]
- **Assessment**: [Can proceed / needs adjustment / blocked]

### Notion Integration
- **Directory exists**: [YES/NO]
- **Client/agent files found**: [list files or "NONE"]
- **MCP integration present**: [YES/NO - evidence]
- **Router exists**: [YES/NO/PARTIAL]
- **Assessment**: [Can proceed / needs adjustment / blocked]

### Calendar Integration
- **Directory exists**: [YES/NO]
- **Client/agent files found**: [list files or "NONE"]
- **MCP integration present**: [YES/NO - evidence]
- **Router exists**: [YES/NO/PARTIAL]
- **Assessment**: [Can proceed / needs adjustment / blocked]

### Feature Flag System
- **USE_SPATIAL pattern found**: [YES/NO]
- **Location**: [where found]
- **Pattern matches GitHub**: [YES/NO]

## Gameplan Alignment

### Assumptions Confirmed
[List what matches gameplan expectations]

### Assumptions Violated
[List what doesn't match - with evidence]

### Recommended Action
[PROCEED to Phase 0 / REVISE gameplan / STOP and investigate]
```

## Update Requirements

After completing verification:

1. **Update Session Log**: Add Phase -1 completion with findings
2. **Update GitHub Issue #199**: Add comment with infrastructure verification results
3. **Tag Lead Developer**: Request approval to proceed to Phase 0 or await gameplan revision

## Critical Success Factors

- **Never guess** - If unclear, report uncertainty with evidence
- **Show actual output** - Don't summarize, show real terminal output
- **Report mismatches** - Any deviation from assumptions needs reporting
- **Stop if blocked** - Don't proceed to Phase 0 if RED status

---

**Your Mission**: Verify infrastructure matches gameplan assumptions or report mismatches for revision. Provide evidence-based reality check before router audit work begins.

**Time Limit**: 30 minutes maximum for this verification phase
