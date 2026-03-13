# Phase -1: MCP Discovery & Infrastructure Verification

**Agent**: Claude Code (Programmer)
**Task**: CORE-MCP-MIGRATION #198 - Phase -1 Discovery
**Duration**: 3 hours estimated
**Date**: October 17, 2025

---

## Mission

Audit the current state of MCP (Model Context Protocol) adoption across all Piper Morgan integrations. Verify infrastructure assumptions and document findings with filesystem evidence.

## Context

During GREAT-2 investigation, inconsistent MCP adoption was discovered:
- **Notion**: Has MCP adapter ✅
- **Calendar**: Has MCP adapter ✅
- **GitHub**: Status unknown
- **Slack**: Has spatial intelligence, MCP status unknown

We need complete visibility before defining patterns or deploying agents.

---

## Phase -1 Requirements (Inchworm Protocol)

**BEFORE any pattern work or implementation:**

1. **Verify infrastructure assumptions**
2. **Document what actually exists** (not what should exist)
3. **Identify pattern variations**
4. **Assess migration effort per service**
5. **Find unexpected discoveries** (75% pattern warning!)

---

## Your Deliverables

### 1. Integration Services Inventory

For each integration service, document:

```
Service: [name]
Location: [exact filepath]
MCP Adapter: [Yes/No/Partial]
  - If Yes: [filepath to adapter]
  - If Partial: [what exists, what's missing]
  - If No: [confirm no MCP files found]
Router: [filepath]
Spatial Intelligence: [Yes/No] [filepath if yes]
Config Service: [filepath]
Tests: [directory with test count]
```

**Services to audit**:
- GitHub (`services/integrations/github/`)
- Slack (`services/integrations/slack/`)
- Notion (`services/integrations/notion/`)
- Calendar (`services/integrations/calendar/`)
- Any others discovered in `services/integrations/`

### 2. MCP Pattern Analysis

For services WITH MCP adapters:

```python
# Document actual implementation patterns found:
- Class name(s)
- Interface/base class (if any)
- Key methods implemented
- How tools are defined
- How context is passed
- Integration with spatial intelligence
- Integration with router
- Test coverage
```

Note any pattern variations between services!

### 3. OrchestrationEngine Integration

Locate and document:
```
OrchestrationEngine location: [filepath]
Current MCP integration: [describe what you find]
How services are wired: [current pattern]
Context passing mechanism: [describe]
```

### 4. Infrastructure Verification

Confirm or correct:
- [ ] Main entry point: `main.py` (line count: ___)
- [ ] Web app: `web/app.py` (line count: ___)
- [ ] Port: 8001 (verify in code: ___)
- [ ] Services directory structure matches expectations
- [ ] Test framework location and conventions

### 5. Migration Effort Assessment

For each service, estimate:
```
Service: [name]
Current MCP Status: [None/Partial/Complete]
Estimated Work:
  - If None: [X hours] - Create from scratch
  - If Partial: [X hours] - Complete and standardize
  - If Complete: [X hours] - Validate and enhance

Complexity Factors:
  - Existing spatial intelligence integration
  - Number of tools/operations
  - Test coverage requirements
  - Documentation needs
```

---

## Investigation Checklist

Run these Serena MCP queries and document results:

```bash
# 1. List all integration services
mcp__serena__list_dir("services/integrations")

# 2. For each service, check for MCP adapter
mcp__serena__find_symbol("MCPAdapter", scope="services/integrations/[service]")
mcp__serena__find_symbol("mcp_adapter", scope="services/integrations/[service]")

# 3. Find OrchestrationEngine
mcp__serena__find_symbol("OrchestrationEngine", depth=2)

# 4. Check for MCP-related imports
mcp__serena__find_symbol("mcp", scope="services")

# 5. Verify main entry point
mcp__serena__read_file("main.py")
mcp__serena__read_file("web/app.py", start=1, end=50)
```

Use filesystem commands to verify:

```bash
# Find all files with 'mcp' in name
find services/integrations -name "*mcp*" -type f

# Check for MCP adapter pattern
grep -r "class.*MCP.*Adapter" services/integrations/ --include="*.py"

# Count lines in key files
wc -l main.py web/app.py

# Verify port configuration
grep -r "8001\|8080" . --include="*.py" | head -20
```

---

## Red Flags to Watch For

Based on the **75% Pattern**:

⚠️ **Inconsistent implementations**:
- Different class names for same pattern
- Varying method signatures
- Incomplete tool definitions
- Missing context passing

⚠️ **Abandoned work**:
- TODO comments without issue numbers
- Half-implemented features
- Tests that are skipped/disabled
- Documentation that doesn't match code

⚠️ **Integration gaps**:
- MCP adapters not wired to OrchestrationEngine
- Spatial intelligence not integrated with MCP
- Config services disconnected from MCP

---

## Evidence Format

For EVERY claim in your report:

```markdown
**Claim**: "GitHub integration has no MCP adapter"

**Evidence**:
```bash
$ ls -la services/integrations/github/
total 48
-rw-r--r--  1 user  staff  1234 Oct 15 github_integration_router.py
-rw-r--r--  1 user  staff  5678 Oct 14 github_config_service.py
# No mcp_adapter.py found

$ grep -r "MCP" services/integrations/github/
# No results

$ mcp__serena__find_symbol("MCPAdapter", scope="services/integrations/github")
# Result: No symbols found
```

**Conclusion**: Confirmed - GitHub has no MCP adapter implementation.
```

---

## Success Criteria

Phase -1 is complete when:

- [ ] All 4+ integration services documented with evidence
- [ ] MCP adapter status confirmed for each service
- [ ] Existing MCP patterns analyzed and compared
- [ ] OrchestrationEngine location and integration pattern documented
- [ ] Infrastructure assumptions verified
- [ ] Migration effort estimated per service
- [ ] Red flags identified and documented
- [ ] Report includes filesystem evidence for all claims

---

## Time Budget

- **Hour 1**: Service inventory and basic MCP status
- **Hour 2**: Deep dive on existing MCP patterns
- **Hour 3**: OrchestrationEngine investigation and effort assessment

---

## Reporting Back

Provide your findings in this format:

```markdown
# Phase -1 Discovery Report: MCP Migration

## Executive Summary
[2-3 sentence overview of findings]

## Service Inventory
[Detailed per-service findings with evidence]

## Pattern Analysis
[What patterns exist, how they differ]

## OrchestrationEngine Integration
[Current state and wiring mechanism]

## Infrastructure Verification
[Confirmed or corrected assumptions]

## Migration Effort
[Estimated hours per service with complexity factors]

## Red Flags
[Any concerns discovered]

## Recommendations for Phase 1
[What pattern should we standardize on?]

## Appendix: Evidence
[All filesystem outputs, Serena queries, grep results]
```

---

## Remember

- **Verify, don't assume**: Every claim needs evidence
- **Document what IS, not what SHOULD BE**: Reality over expectations
- **Note pattern variations**: Inconsistencies inform pattern design
- **Use Serena MCP**: Precise, auditable, fast
- **Flag the 75% pattern**: Incomplete work is everywhere
- **No implementation**: Phase -1 is investigation only

---

**Ready to discover the truth about MCP adoption? Let's see what's really there! 🔍**
