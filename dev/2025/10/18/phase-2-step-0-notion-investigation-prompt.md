# Phase 2 Step 0: Notion Implementation Investigation

**Agent**: Claude Code (Programmer)
**Task**: CORE-MCP-MIGRATION #198 - Phase 2 Step 0
**Duration**: 30 minutes estimated
**Date**: October 18, 2025, 7:05 AM

---

## Mission

Investigate current Notion implementation to understand the migration complexity from server-based to tool-based MCP. You'll provide a complete assessment that determines how we convert Notion to follow Calendar's tool-based pattern.

## Context

**Phase 1 Success**:
- ✅ Calendar: 100% complete (tool-based MCP)
- ✅ GitHub: 100% complete (Delegated MCP per ADR-038)
- ✅ Pattern established: Tool-based MCP with configuration

**Phase 2 Objective**: Migrate Notion from server-based to tool-based MCP

**Phase -1 Assessment** (from yesterday):
- Notion: 60% complete (server-based)
- Location: `services/mcp/` (server structure)
- Status: Architectural incomplete
- Problem: More complex than needed

**Your Job**: Find out exactly what exists and plan the migration

---

## Your Investigation Deliverables

### 1. Notion File Structure Analysis (5 minutes)

**Find ALL Notion-related files**:

```bash
# Find Notion implementation files
find services -name "*notion*" -type f
find services/mcp -name "*notion*" -type f

# Check for Notion integration directory
ls -la services/integrations/notion/ 2>/dev/null

# Check for Notion MCP server/consumer files
ls -la services/mcp/server/*notion* 2>/dev/null
ls -la services/mcp/consumer/*notion* 2>/dev/null

# Use Serena to find Notion references
mcp__serena__find_files("notion", scope="services")
```

**Document**:
```markdown
## Notion File Structure

**Files Found**:
1. [Full path] - [size] - [description]
2. [Full path] - [size] - [description]
3. ... (list ALL Notion files)

**Primary Locations**:
- Server files: [paths or "none"]
- Consumer files: [paths or "none"]
- Integration files: [paths or "none"]
- Config files: [paths or "none"]

**Architecture Type**:
- [ ] Server-based (separate MCP server process)
- [ ] Tool-based (direct MCP adapter like Calendar)
- [ ] Hybrid (both patterns present)
- [ ] Other: [describe]
```

---

### 2. Server-Based Implementation Analysis (10 minutes)

**If server-based files exist, analyze them**:

```bash
# Read server implementation
mcp__serena__read_file("<path_to_notion_server>")

# Check server structure
grep -n "class.*Server\|class.*MCP" services/mcp/server/*notion* 2>/dev/null

# Find server methods
grep -n "async def\|def " services/mcp/server/*notion* 2>/dev/null
```

**Document**:
```markdown
## Server-Based Implementation

**Primary File**: [path]
**Line Count**: [number]

**Server Class**: [class name and base class]

**Implemented Operations**:
1. [method name] - [purpose] - Lines XX-YY
2. [method name] - [purpose] - Lines XX-YY
3. ... (list ALL methods)

**Architecture**:
- Protocol handlers: [describe]
- Request/response cycle: [describe]
- Client communication: [describe]

**Complexity Assessment**:
- Simple (easy to convert)
- Medium (moderate conversion)
- Complex (significant refactor needed)

**Reasoning**: [why this complexity assessment]
```

---

### 3. Notion Operations Inventory (10 minutes)

**What can Notion do currently?**

```bash
# Find all Notion methods/operations
grep -r "async def.*notion\|def.*notion" services/ -i

# Check for Notion API usage
grep -r "notion.*client\|NotionClient" services/

# Look for Notion imports
grep -r "from notion\|import notion" services/
```

**Document**:
```markdown
## Notion Operations Inventory

**Database Operations**:
- [ ] Get database - [implemented? where?]
- [ ] Query database - [implemented? where?]
- [ ] Create database - [implemented? where?]
- [ ] Update database - [implemented? where?]

**Page Operations**:
- [ ] Get page - [implemented? where?]
- [ ] Create page - [implemented? where?]
- [ ] Update page - [implemented? where?]
- [ ] Delete page - [implemented? where?]

**Block Operations**:
- [ ] Get blocks - [implemented? where?]
- [ ] Append blocks - [implemented? where?]
- [ ] Update blocks - [implemented? where?]

**Search Operations**:
- [ ] Search - [implemented? where?]

**Other Operations**:
- [List any other operations found]

**Total Operations**: [count]
**Working Status**: [estimate how many work vs are broken]
```

---

### 4. Configuration Analysis (5 minutes)

**How is Notion configured?**

```bash
# Check for NotionConfigService
find services -name "*notion*config*" -type f

# Check PIPER.user.md for Notion config
grep -A 20 "^notion:" config/PIPER.user.md

# Check environment variables
grep -r "NOTION_" services/ config/

# Use Serena to read config service
mcp__serena__find_symbol("NotionConfig", scope="services")
```

**Document**:
```markdown
## Configuration Analysis

**Config Service Exists**: [yes/no]
**Location**: [path if exists]

**Current Configuration Method**:
- [ ] PIPER.user.md - [yes/no, show section if exists]
- [ ] Environment variables - [list vars]
- [ ] Hardcoded - [where?]

**Config Fields**:
- API token: [how loaded?]
- Database IDs: [how loaded?]
- Other: [list]

**Needs Work**:
- [ ] Add PIPER.user.md support
- [ ] Already has PIPER.user.md support
- [ ] Create config service from scratch
```

---

### 5. Integration Router Analysis (5 minutes)

**Does NotionIntegrationRouter exist?**

```bash
# Find Notion router
find services/integrations -name "*notion*router*" -type f

# Check for Notion integration patterns
ls -la services/integrations/notion/ 2>/dev/null

# Use Serena
mcp__serena__find_symbol("NotionIntegrationRouter", scope="services")
```

**Document**:
```markdown
## Integration Router Analysis

**Router Exists**: [yes/no]
**Location**: [path if exists]

**Current Architecture** (if exists):
- Uses server-based: [yes/no]
- Uses tool-based: [yes/no]
- Delegation pattern: [describe]
- Feature flags: [list]

**Needs Work**:
- [ ] Create router from scratch
- [ ] Update existing router for tool-based
- [ ] Wire new MCP adapter
- [ ] Add feature flags
```

---

### 6. Test Coverage Analysis (5 minutes)

**What Notion tests exist?**

```bash
# Find Notion tests
find tests -name "*notion*" -type f

# Check test content
grep -l "notion\|Notion" tests/**/*.py

# Count test cases
grep -c "def test_" tests/integration/*notion* 2>/dev/null
```

**Document**:
```markdown
## Test Coverage

**Test Files Found**:
1. [path] - [number of tests]
2. [path] - [number of tests]

**Test Categories**:
- Unit tests: [count]
- Integration tests: [count]
- MCP tests: [count]

**Coverage Assessment**:
- Operations tested: [count/total]
- Server tests: [count]
- Config tests: [count]

**Test Quality**:
- [ ] Comprehensive
- [ ] Partial
- [ ] Minimal
- [ ] None

**Needs Work**:
- [ ] Create test suite from scratch
- [ ] Expand existing tests
- [ ] Update tests for tool-based pattern
```

---

### 7. Migration Complexity Assessment (5 minutes)

**Based on your findings, assess migration complexity**:

```markdown
## Migration Complexity Assessment

### Current State Summary
- Architecture: [server-based/tool-based/hybrid]
- Operations: [count] implemented
- Configuration: [describe current state]
- Router: [exists/doesn't exist]
- Tests: [comprehensive/partial/minimal/none]

### Migration Complexity: [LOW/MEDIUM/HIGH]

**LOW** = Simple conversion
- Criteria: Few operations, simple server, good patterns
- Time: 2-3 hours

**MEDIUM** = Moderate conversion
- Criteria: Multiple operations, some complexity, partial patterns
- Time: 3-4 hours

**HIGH** = Complex conversion
- Criteria: Many operations, complex server, unclear patterns
- Time: 5+ hours or reconsider approach

### Complexity Rating: [chosen rating]

**Reasoning**:
- [Factor 1]: [explanation]
- [Factor 2]: [explanation]
- [Factor 3]: [explanation]

### Risks Identified:
1. [Risk 1]: [description and impact]
2. [Risk 2]: [description and impact]
3. [Risk 3]: [description and impact]

### Recommendations:
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]
```

---

## Critical Questions to Answer

Your investigation must answer:

1. **What architecture does Notion currently use?**
   - Server-based? Tool-based? Something else?

2. **What operations are implemented?**
   - List all Notion operations we need to preserve

3. **What's working vs broken?**
   - Can we test operations? Are they functional?

4. **How complex is the migration?**
   - Easy refactor? Major rebuild? Somewhere in between?

5. **What can we reuse from Calendar/GitHub patterns?**
   - Configuration approach? Adapter structure? Testing?

6. **Are there any Notion-specific challenges?**
   - API quirks? Complex operations? Special requirements?

7. **What's the migration path?**
   - Direct conversion? Parallel operation? Feature flag migration?

---

## Migration Plan Output

**Based on your investigation, create a specific migration plan**:

```markdown
## Notion Migration Plan (Detailed)

### Step 1: Create NotionMCPAdapter
**Time**: [estimate]
**Files to Create**: [list]
**Operations to Implement**: [list from inventory]
**Pattern to Follow**: Calendar (tool-based)
**Complexity**: [low/medium/high]

### Step 2: Configuration Service
**Time**: [estimate]
**Needs**: [what's needed: create? update? nothing?]
**Pattern to Follow**: Calendar (PIPER.user.md loading)

### Step 3: Integration Router
**Time**: [estimate]
**Needs**: [create? update? wire?]
**Pattern to Follow**: GitHub (delegation if needed)

### Step 4: Testing
**Time**: [estimate]
**Tests to Create**: [count and types]
**Tests to Update**: [count and types]

### Step 5: Deprecation
**Time**: [estimate]
**Files to Remove**: [list]
**Strategy**: [immediate? gradual? feature flag?]

### Total Estimated Time: [hours]

### Feasibility: [FEASIBLE/CHALLENGING/RECONSIDER]
**Reasoning**: [explanation]
```

---

## Success Criteria

Your Step 0 investigation is complete when you can answer:

- ✅ Current architecture identified
- ✅ All operations inventoried
- ✅ Configuration approach documented
- ✅ Router status determined
- ✅ Test coverage assessed
- ✅ Migration complexity rated
- ✅ Specific migration plan created
- ✅ Time estimates provided
- ✅ Risks identified
- ✅ Feasibility assessment made

---

## Reporting Format

Provide findings in this structure:

```markdown
# Notion Implementation Investigation Report

## Executive Summary
[3-4 sentences: What exists, migration complexity, time estimate, feasibility]

## Current Architecture
[Detailed findings from deliverable #2]

## Operations Inventory
[Detailed findings from deliverable #3]

## Configuration Analysis
[Detailed findings from deliverable #4]

## Router Analysis
[Detailed findings from deliverable #5]

## Test Coverage
[Detailed findings from deliverable #6]

## Migration Complexity
[Detailed findings from deliverable #7]

## Detailed Migration Plan
[Step-by-step plan with time estimates]

## Recommendations
[What should we do? Any concerns? Any shortcuts?]

## Evidence Appendix
[All file listings, code excerpts, grep results]
```

---

## Time Budget

- **Total**: 30 minutes
- **File structure**: 5 min
- **Server analysis**: 10 min
- **Operations inventory**: 10 min
- **Configuration**: 5 min
- **Router**: 5 min
- **Tests**: 5 min
- **Complexity assessment**: 5 min
- **Report synthesis**: 10 min

---

## Remember

- Use Serena MCP for efficient file reading
- Provide evidence (code excerpts, line numbers)
- Be honest about complexity (don't underestimate)
- Focus on migration path (server→tool)
- Think about Calendar pattern application
- Identify any architectural surprises
- Consider feature flag migration if needed

---

## Key Comparison Points

**Server-Based** (what we're migrating FROM):
- Separate MCP server process
- Protocol handlers for requests
- More complex architecture
- Harder to maintain

**Tool-Based** (what we're migrating TO):
- Direct MCP adapter (like Calendar)
- Simple tool definitions
- Cleaner architecture
- Easier to maintain

**Your job**: Figure out how to get from A to B efficiently!

---

**Ready to investigate Notion and plan the migration!** 🔍

**Deliverable**: Complete investigation report with detailed migration plan and time estimates.
