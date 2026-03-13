# Cursor Research: GitHub Implementation Architecture

**Agent**: Cursor (Research Assistant)
**Task**: Investigate GitHub dual implementations for architectural clarity
**Duration**: 15-30 minutes estimated
**Date**: October 17, 2025, 2:27 PM

---

## Mission

Research and document the architectural status of two GitHub implementations to determine which is canonical and provide clear guidance for Code agent's GitHub MCP completion work.

## Context

**Code Agent Discovery**: Found TWO separate GitHub implementations:
1. **GitHubSpatialIntelligence** - 424 lines (currently used by router)
2. **GitHubMCPSpatialAdapter** - 22KB (in mcp/consumer, unused)

**Problem**: Unclear which is canonical, which to use, or if both serve different purposes

**Impact**: Code is blocked on GitHub completion work pending architectural clarity

---

## Your Research Deliverables

### 1. File Analysis - GitHubSpatialIntelligence (30 minutes)

**Location**: Find and analyze GitHubSpatialIntelligence

**Use Serena MCP queries**:
```bash
# Find the file
mcp__serena__find_files("GitHubSpatialIntelligence", scope="services")

# Read the implementation
mcp__serena__read_file("<path_to_file>")

# Check class structure
mcp__serena__find_symbol("GitHubSpatialIntelligence")
```

**Document**:
```markdown
## GitHubSpatialIntelligence Analysis

**Location**: [full path]
**Line Count**: [actual line count]
**Created/Modified**: [git log dates if available]

**Class Structure**:
- Base class: [what does it inherit from?]
- Constructor: [signature and dependencies]
- Key methods: [list main methods]

**Purpose**: [what does this implementation do?]

**Integration Points**:
- Used by: [which files import/use this?]
- Dependencies: [what does it depend on?]

**Pattern**:
- MCP integration: [yes/no, how?]
- Spatial intelligence: [8-dimensional analysis?]
- Configuration: [how is it configured?]
```

---

### 2. File Analysis - GitHubMCPSpatialAdapter (30 minutes)

**Location**: `services/mcp/consumer/github_adapter.py` (or similar)

**Use Serena MCP queries**:
```bash
# Read the file
mcp__serena__read_file("services/mcp/consumer/github_adapter.py")

# Check line count
wc -l services/mcp/consumer/github_adapter.py

# Check class structure
mcp__serena__find_symbol("GitHubMCPSpatialAdapter", scope="services/mcp")
```

**Document**:
```markdown
## GitHubMCPSpatialAdapter Analysis

**Location**: services/mcp/consumer/github_adapter.py (or actual path)
**Line Count**: [actual line count - reported as 22KB]
**Created/Modified**: [git log dates if available]

**Class Structure**:
- Base class: [what does it inherit from?]
- Constructor: [signature and dependencies]
- Key methods: [list main methods]

**Purpose**: [what does this implementation do?]

**Integration Points**:
- Used by: [which files import/use this? (currently "unused")]
- Dependencies: [what does it depend on?]

**Pattern**:
- MCP integration: [how is MCP implemented?]
- Spatial intelligence: [8-dimensional analysis?]
- Configuration: [how is it configured?]
```

---

### 3. Historical Analysis - Creation Timeline (15 minutes)

**Use git to understand evolution**:
```bash
# Find when each file was created/modified
git log --oneline --all -- "*GitHubSpatialIntelligence*"
git log --oneline --all -- "services/mcp/consumer/github_adapter.py"

# Check recent commits affecting GitHub integration
git log --oneline --all --since="2025-08-01" --grep="GitHub\|github" -- services/

# Look for ADR references
grep -r "GitHubSpatialIntelligence\|GitHubMCPSpatialAdapter" docs/architecture/
```

**Document**:
```markdown
## Historical Timeline

**GitHubSpatialIntelligence**:
- Created: [date from git log]
- Last modified: [date]
- Related commits: [key commits]
- ADR references: [any ADRs mentioning it?]

**GitHubMCPSpatialAdapter**:
- Created: [date from git log]
- Last modified: [date]
- Related commits: [key commits]
- ADR references: [any ADRs mentioning it?]

**Architectural Evolution**:
- Which came first?
- Was one meant to replace the other?
- Any deprecation notices?
```

---

### 4. Usage Analysis - Current Integration (15 minutes)

**Find how GitHubIntegrationRouter currently uses GitHub implementations**:

```bash
# Read the router
mcp__serena__read_file("services/integrations/github/github_integration_router.py")

# Find imports
grep -n "import.*GitHub" services/integrations/github/github_integration_router.py

# Find usage patterns
grep -n "GitHubSpatial\|GitHubMCP" services/integrations/github/github_integration_router.py
```

**Document**:
```markdown
## Current Router Implementation

**File**: services/integrations/github/github_integration_router.py

**Current Imports**:
[list actual imports]

**Current Usage**:
- Which GitHub implementation is instantiated?
- How is it initialized?
- What methods are called?

**Architecture**:
- Feature flags used? [check for USE_SPATIAL_GITHUB, etc.]
- Fallback patterns? [legacy client mentions?]
- Configuration injection? [config service usage?]
```

---

### 5. ADR Analysis - Architectural Decisions (15 minutes)

**Find relevant ADRs that explain the GitHub architecture**:

```bash
# Search ADRs for GitHub mentions
grep -l "GitHub" docs/architecture/adr/*.md

# Check ADR-013 (MCP+Spatial pattern)
mcp__serena__read_file("docs/architecture/adr/adr-013-mcp-spatial-integration-pattern.md")

# Check ADR-017 (Spatial MCP)
mcp__serena__read_file("docs/architecture/adr/adr-017-spatial-mcp.md")

# Look for GitHub migration plans
find docs -name "*github*" -o -name "*migration*" -o -name "*deprecation*" | grep -i github
```

**Document**:
```markdown
## Architectural Decisions

**Relevant ADRs**:
- ADR-013: [what does it say about GitHub?]
- ADR-017: [what does it say about GitHub?]
- Other ADRs: [any others relevant?]

**Stated Architecture**:
- What pattern should GitHub follow?
- Is there a migration plan documented?
- Which implementation aligns with ADRs?

**Deprecation Plans**:
- Any deprecation notices found?
- Migration timelines mentioned?
```

---

### 6. Pattern Comparison - Calendar vs GitHub (15 minutes)

**Compare Calendar's working pattern with GitHub implementations**:

```bash
# Read Calendar adapter (our reference)
mcp__serena__read_file("services/mcp/consumer/google_calendar_adapter.py", start=1, end=100)

# Compare base classes
grep -n "class.*Adapter.*BaseSpatial" services/mcp/consumer/*.py
grep -n "class.*Intelligence.*BaseSpatial" services/integrations/*/spatial*.py
```

**Document**:
```markdown
## Pattern Comparison

**Calendar Pattern** (Reference Implementation):
- File: services/mcp/consumer/google_calendar_adapter.py
- Base class: BaseSpatialAdapter
- Pattern: [tool-based MCP with spatial]

**GitHubSpatialIntelligence Pattern**:
- Base class: [what?]
- Matches Calendar? [yes/no/partially]
- Differences: [list key differences]

**GitHubMCPSpatialAdapter Pattern**:
- Base class: [what?]
- Matches Calendar? [yes/no/partially]
- Differences: [list key differences]

**Alignment Assessment**:
- Which GitHub implementation matches Calendar pattern?
- Which follows current architectural standards?
```

---

## Research Questions to Answer

By the end of your research, you should be able to answer:

1. **Which is canonical?** GitHubSpatialIntelligence or GitHubMCPSpatialAdapter?

2. **Why do both exist?** Historical accident? Different purposes? Migration in progress?

3. **Which to use?** For completing GitHub MCP integration, which should Code wire to the router?

4. **What to do with the other?** Deprecate? Keep? Different use case?

5. **What's the pattern?** Does either follow Calendar's pattern (our reference)?

6. **Migration path?** Is there a documented migration plan? Should we create one?

---

## Reporting Format

**Provide findings in this structure**:

```markdown
# GitHub Implementation Architecture Research Report

## Executive Summary
[2-3 sentences: Which is canonical, why both exist, recommendation]

## Implementation Analysis

### GitHubSpatialIntelligence
[Complete analysis from deliverable #1]

### GitHubMCPSpatialAdapter
[Complete analysis from deliverable #2]

## Historical Context
[Timeline and evolution from deliverable #3]

## Current Usage
[Router integration from deliverable #4]

## Architectural Alignment
[ADR analysis from deliverable #5]
[Pattern comparison from deliverable #6]

## Recommendation

**For Code Agent's GitHub Completion Task**:

**Option A: Use GitHubSpatialIntelligence**
- Reasoning: [why this is correct]
- Implementation: [how Code should wire it]

**OR**

**Option B: Use GitHubMCPSpatialAdapter**
- Reasoning: [why this is correct]
- Implementation: [how Code should wire it]

**OR**

**Option C: Hybrid/Migration Approach**
- Reasoning: [why both are needed]
- Implementation: [how to handle both]

**OR**

**Option D: Consult Chief Architect**
- Reasoning: [why this needs escalation]
- Questions for Chief Architect: [specific questions]

## Evidence Appendix
[All code excerpts, git log output, grep results]
```

---

## Critical Success Factors

1. **Use Serena MCP** - Most token-efficient research method
2. **Provide Evidence** - Code excerpts, file paths, line numbers
3. **Be Definitive** - Clear recommendation, not vague analysis
4. **Document Reasoning** - Explain WHY one implementation over another
5. **Consider Patterns** - How does this align with Calendar (our reference)?
6. **Speed Matters** - Code is blocked, need answer quickly

---

## Time Budget

- **Total**: 15-30 minutes
- **File Analysis**: 10 minutes (both files)
- **Historical**: 5 minutes (git logs)
- **Usage**: 5 minutes (router check)
- **ADRs**: 5 minutes (skim relevant sections)
- **Comparison**: 5 minutes (Calendar vs GitHub)
- **Report**: 10 minutes (synthesize findings)

---

## Remember

- Code is BLOCKED waiting for this research
- Lead Dev needs clear direction for Code
- May need to escalate to Chief Architect
- Your research determines implementation path
- Use Serena MCP for token efficiency
- Be thorough but FAST

---

**Ready to research GitHub implementation architecture!** 🔍

**Deliverable**: Clear recommendation on which GitHub implementation to use and how Code should proceed.
