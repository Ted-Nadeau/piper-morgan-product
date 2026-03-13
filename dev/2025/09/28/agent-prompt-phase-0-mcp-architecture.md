# Claude Code Prompt: Phase 0 - MCP Architecture Understanding

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- CURRENT-STATE.md - Current epic and focus
- role/PROGRAMMER.md - Your role requirements
- METHODOLOGY.md - Inchworm Protocol

## Session Log Management

Continue using your existing session log at: `dev/2025/09/28/2025-09-28-1724-prog-code-log.md`
- Add timestamped entry for Phase 0 work
- Document MCP architecture findings
- Include all evidence from investigation

## Mission: Understand MCP Architecture Pattern

**Context**: Phase -1B discovered all three integrations (Slack, Notion, Calendar) use or can use MCP (Model Context Protocol) pattern. Before creating router wrappers, we need to thoroughly understand:
1. How MCP adapters are structured
2. What pattern they follow
3. How spatial intelligence integrates with MCP
4. What methods they expose

**Objective**: Document MCP architecture comprehensively so router wrapper implementation follows correct patterns.

## Investigation Tasks

### Task 1: Find All MCP Adapters

Locate every MCP adapter in the codebase:

```bash
# Find all MCP-related files
echo "=== All MCP Files ==="
find . -path "*/mcp/*" -name "*.py" -type f

# Check both possible locations
echo "=== MCP Consumer Directory ==="
ls -la services/mcp/consumer/ 2>/dev/null || echo "Directory not found"

echo "=== MCP Integration Directory ==="
ls -la services/integrations/mcp/ 2>/dev/null || echo "Directory not found"
```

**Document**: List every MCP adapter found with full path

### Task 2: Study Google Calendar Adapter Pattern

The Calendar adapter is 85% complete and working. Use it as the reference pattern:

```bash
# Read the complete adapter
cat services/mcp/consumer/google_calendar_adapter.py

# Extract structure
echo "=== Class Definition ==="
grep "^class " services/mcp/consumer/google_calendar_adapter.py

echo "=== Inheritance ==="
grep "BaseSpatialAdapter\|BaseAdapter" services/mcp/consumer/google_calendar_adapter.py

echo "=== Public Methods ==="
grep "    def [a-z]" services/mcp/consumer/google_calendar_adapter.py | grep -v "__"

echo "=== Constructor Pattern ==="
grep -A 10 "def __init__" services/mcp/consumer/google_calendar_adapter.py
```

**Document**:
- What does the adapter inherit from?
- What methods does it expose?
- How does OAuth/authentication work?
- What's the initialization pattern?

### Task 3: Understand BaseSpatialAdapter

```bash
# Find the base class
find . -name "*spatial*adapter*.py" -type f | grep -i base

# If found, examine it
# [Read and document base class pattern]
```

**Document**:
- What does BaseSpatialAdapter provide?
- What methods must subclasses implement?
- How does spatial intelligence integrate?

### Task 4: Study Notion MCP Adapter

```bash
# Read Notion adapter
cat services/integrations/mcp/notion_adapter.py

# Extract structure
grep "^class " services/integrations/mcp/notion_adapter.py
grep "def [a-z]" services/integrations/mcp/notion_adapter.py | grep -v "__"
```

**Document**:
- Does it follow same pattern as Calendar?
- What methods does it expose?
- Any differences from Calendar adapter?

### Task 5: Check Slack MCP Pattern

```bash
# Check if Slack has or can use MCP pattern
echo "=== Slack Spatial Files ==="
ls -la services/integrations/slack/slack_spatial*.py

echo "=== Check for MCP Usage ==="
grep -r "mcp\|MCP" services/integrations/slack/ --include="*.py"

echo "=== Slack Client Structure ==="
grep "^class " services/integrations/slack/slack_client.py
grep "def [a-z]" services/integrations/slack/slack_client.py | grep -v "__" | head -20
```

**Document**:
- Does Slack use MCP pattern?
- What pattern does it currently use?
- How do slack_spatial_*.py files relate to client?

### Task 6: Identify Current Service Usage Patterns

```bash
# Find how services currently access these integrations
echo "=== Direct Calendar Usage ==="
grep -r "GoogleCalendarAdapter\|google_calendar" services/ --include="*.py" | grep -v "test" | head -10

echo "=== Direct Notion Usage ==="
grep -r "NotionAdapter\|notion_adapter" services/ --include="*.py" | grep -v "test" | head -10

echo "=== Direct Slack Usage ==="
grep -r "SlackClient\|SlackSpatial\|slack_client" services/ --include="*.py" | grep -v "test" | head -10
```

**Document**: How are services currently importing and using each integration?

### Task 7: Check Feature Flag System

```bash
# Verify USE_SPATIAL pattern from GitHub router
echo "=== Existing Feature Flags ==="
grep -r "USE_SPATIAL" services/ --include="*.py" | head -20

echo "=== Config References ==="
grep -r "USE_SPATIAL" config/ --include="*.md" 2>/dev/null || echo "No config flags found"

echo "=== Environment Variable Usage ==="
grep -r "os.getenv.*SPATIAL" services/ --include="*.py" | head -10
```

**Document**: How does feature flag system work from GitHub router implementation?

## Evidence Requirements

Create a comprehensive report documenting:

```markdown
# Phase 0: MCP Architecture Investigation Report

## MCP Adapter Inventory

### Found Adapters
- [List all MCP adapter files with full paths]
- [Note which are complete, which are partial]

### Calendar Adapter Analysis
**File**: services/mcp/consumer/google_calendar_adapter.py
**Size**: [line count]
**Inheritance**: [What it inherits from]
**Authentication**: [How OAuth works]
**Public Methods**:
- [List all public methods with brief description]

**Key Pattern Elements**:
[Describe initialization, method structure, error handling, etc.]

### Notion Adapter Analysis
**File**: services/integrations/mcp/notion_adapter.py
**Inheritance**: [What it inherits from]
**Public Methods**:
- [List all public methods]

**Pattern Comparison**: [How does it compare to Calendar adapter?]

### Slack Integration Analysis
**Current Pattern**: [MCP or traditional client?]
**Files**: [List relevant files]
**Spatial Integration**: [How spatial_*.py files work]

**Key Differences**: [How does Slack differ from Calendar/Notion?]

## BaseSpatialAdapter Pattern

**Location**: [file path if found]
**Purpose**: [What it provides]
**Required Methods**: [What subclasses must implement]
**Spatial Intelligence Integration**: [How it enables 8-dimensional analysis]

## Current Service Usage

### Calendar
**Used By**: [List services with evidence]
**Import Pattern**: [How they currently import]
**Example Usage**: [Show actual code snippet]

### Notion
**Used By**: [List services with evidence]
**Import Pattern**: [How they currently import]

### Slack
**Used By**: [List services with evidence]
**Import Pattern**: [How they currently import]

## Feature Flag System

**Pattern**: USE_SPATIAL_[INTEGRATION]=true/false
**Implementation**: [How it's checked in code]
**Current Flags**:
- USE_SPATIAL_GITHUB (exists from GREAT-2B)
- USE_SPATIAL_SLACK (needs creation)
- USE_SPATIAL_NOTION (needs creation)
- USE_SPATIAL_CALENDAR (needs creation)

## Router Wrapper Design Pattern

Based on MCP architecture investigation, router wrappers should:

1. **Initialization Pattern**:
[Describe how router should initialize based on feature flag]

2. **Delegation Pattern**:
[Describe how router should delegate to MCP adapter or spatial system]

3. **Method Exposure**:
[Describe which methods router should expose]

4. **Error Handling**:
[Describe error handling pattern from adapters]

## Recommendations for Router Implementation

### Slack Router
[Specific recommendations based on Slack's structure]

### Calendar Router
[Specific recommendations based on Calendar adapter]

### Notion Router
[Specific recommendations based on Notion adapter]

## Questions Requiring Resolution

[List any uncertainties or patterns that need clarification]
```

## Update Requirements

After completing investigation:

1. **Update Session Log**: Add Phase 0 completion with full MCP architecture understanding
2. **Update GitHub Issue #199**: Add comment with Phase 0 findings report
3. **Tag Lead Developer & Cursor**: Share findings for cross-validation before proceeding to router implementation

## Critical Success Factors

- **Thorough Investigation**: Read entire adapter files, don't just skim
- **Pattern Recognition**: Identify what's consistent across adapters vs what varies
- **Evidence Collection**: Provide actual code snippets and file contents
- **Question Identification**: Note anything unclear for resolution before implementation
- **No Assumptions**: If something's unclear, investigate further or explicitly note uncertainty

## STOP Conditions

- If MCP pattern is fundamentally different than expected
- If adapters don't follow consistent pattern
- If spatial intelligence integration is unclear
- If OAuth/authentication pattern can't be preserved through router

Report any STOP conditions immediately rather than proceeding with incomplete understanding.

---

**Your Mission**: Thoroughly understand MCP architecture pattern to inform router wrapper design. Provide comprehensive evidence-based documentation of adapter patterns, usage, and integration approaches.

**Quality Standard**: Complete understanding before implementation - thoroughness over speed.
