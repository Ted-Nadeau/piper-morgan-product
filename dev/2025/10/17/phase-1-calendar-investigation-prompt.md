# Phase 1 Investigation: Calendar MCP Completion

**Agent**: Claude Code (Programmer)
**Task**: CORE-MCP-MIGRATION #198 - Phase 1 Calendar Investigation
**Duration**: 1 hour estimated
**Date**: October 17, 2025, 1:50 PM

---

## Mission

Investigate the Calendar MCP implementation to identify the "missing 5%" and prepare for completion. Calendar is 95% complete and will serve as our **reference implementation** for tool-based MCP pattern.

## Context

**Phase -1 Discovery** found:
- Calendar has MCP adapter at `services/mcp/consumer/google_calendar_adapter.py` (514 lines)
- Feature flag: `USE_SPATIAL_CALENDAR=true`
- Status: 95% complete (tool-based implementation)
- Missing: Configuration loading from PIPER.user.md

**Chief Architect Guidance**:
- Calendar is our reference implementation
- Complete this first to establish pattern
- GitHub will follow the same pattern
- Notion and Slack will learn from this

**ADR-037 Decision**: Tool-based MCP is our standard (just approved)

---

## Your Deliverables

### 1. Calendar MCP Implementation Analysis

**Locate and document**:
```
File: services/mcp/consumer/google_calendar_adapter.py
Line count: [actual]
Key classes: [list]
Tool definitions: [count and list]
Methods implemented: [list with line numbers]
```

**Evidence format**:
```python
# Example:
class GoogleCalendarMCPAdapter(BaseSpatialAdapter):
    def __init__(self, config_service: Optional["CalendarConfigService"] = None):
        # Line XX-YY: Constructor with service injection

    async def get_todays_events(self) -> List[Dict[str, Any]]:
        # Line XX-YY: Today's events retrieval

    # ... list all methods
```

### 2. Configuration Loading Analysis

**Find the "missing 5%"** - what configuration isn't being loaded?

**Check**:
```python
# Where does Calendar get credentials?
# services/integrations/calendar/config_service.py

# What does PIPER.user.md contain for Calendar?
# config/PIPER.user.md - Calendar section

# How is config passed to MCP adapter?
# Trace from config_service to adapter
```

**Document**:
- Current config loading: [describe what exists]
- Missing config loading: [describe what's missing]
- Config source: [PIPER.user.md section]
- Config fields needed: [list]

### 3. Integration Router Analysis

**Locate and document**:
```
File: services/integrations/calendar/calendar_integration_router.py
How it uses MCP adapter: [describe]
Feature flag check: [show code]
Service injection: [show code]
```

**Evidence**:
```python
# Example:
if USE_SPATIAL_CALENDAR:
    self.spatial_calendar = GoogleCalendarMCPAdapter(self.config_service)
# What happens after this?
```

### 4. Orchestration Layer Connection

**Find how Calendar connects to orchestration**:
```
OrchestrationEngine imports: [list]
How Calendar is called: [show code path]
Tool registration: [where/how]
```

**Trace the call path**:
```
User request
  → IntentService
  → OrchestrationEngine
  → [Calendar integration point?]
  → CalendarIntegrationRouter
  → GoogleCalendarMCPAdapter
  → Google Calendar API
```

### 5. Tool Definitions

**List all Calendar tools**:
```python
# Example format:
Tool 1: get_todays_events
  - Purpose: Retrieve today's calendar events
  - Parameters: [list]
  - Returns: List[Dict[str, Any]]
  - Line: XX-YY

Tool 2: get_current_meeting
  - Purpose: Get current meeting if in progress
  - Parameters: [list]
  - Returns: Optional[Dict[str, Any]]
  - Line: XX-YY

# ... continue for all tools
```

### 6. Test Coverage Analysis

**Find and analyze tests**:
```bash
# Find Calendar tests
find tests -name "*calendar*" -type f

# Check test coverage
grep -r "GoogleCalendarMCPAdapter" tests/
```

**Document**:
- Test files: [list]
- Test count: [number]
- What's tested: [list]
- What's NOT tested: [list]

### 7. Completion Plan

**Based on your findings, create a specific completion plan**:

```markdown
## What's Complete (95%)
- [List everything that works]

## What's Missing (5%)
- [Specific items to complete]

## Completion Steps
1. [Specific task 1] - [estimated time]
2. [Specific task 2] - [estimated time]
3. [Test addition needed] - [estimated time]

Total time: [estimate]
```

---

## Investigation Checklist

Use Serena MCP queries for precision:

```bash
# 1. Read Calendar MCP adapter
mcp__serena__read_file("services/mcp/consumer/google_calendar_adapter.py")

# 2. Read Calendar config service
mcp__serena__read_file("services/integrations/calendar/config_service.py")

# 3. Read Calendar integration router
mcp__serena__read_file("services/integrations/calendar/calendar_integration_router.py")

# 4. Find PIPER.user.md Calendar config
mcp__serena__read_file("config/PIPER.user.md", start=1, end=200)
# Look for Calendar section

# 5. Find OrchestrationEngine Calendar references
mcp__serena__find_symbol("calendar", scope="services/orchestration")

# 6. Check BaseSpatialAdapter
mcp__serena__read_file("services/integrations/spatial_adapter.py")
```

Use filesystem commands to verify:

```bash
# Structure
ls -la services/mcp/consumer/
ls -la services/integrations/calendar/

# Line counts
wc -l services/mcp/consumer/google_calendar_adapter.py
wc -l services/integrations/calendar/calendar_integration_router.py

# Tool search
grep -n "async def" services/mcp/consumer/google_calendar_adapter.py

# Config search
grep -n "calendar\|Calendar" config/PIPER.user.md -i

# Test search
find tests -name "*calendar*" -type f -exec wc -l {} \;
```

---

## Key Questions to Answer

1. **What methods does GoogleCalendarMCPAdapter implement?**
2. **How many tools are exposed for orchestration?**
3. **Where does config loading fail or not happen?**
4. **What's in PIPER.user.md for Calendar?**
5. **How is the adapter wired to orchestration layer?**
6. **What tests exist and what's missing?**
7. **What exactly is the "missing 5%"?**

---

## Success Criteria

Investigation is complete when you can answer:

- ✅ Complete list of Calendar tools with purposes
- ✅ Exact location and nature of the "missing 5%"
- ✅ Specific steps needed to reach 100% completion
- ✅ Estimated time for completion work
- ✅ Pattern documented for GitHub to follow
- ✅ Test gaps identified

---

## Reporting Format

Provide findings in this structure:

```markdown
# Phase 1 Calendar Investigation Report

## Executive Summary
[2-3 sentences: What Calendar MCP does, what's missing, time to complete]

## Architecture Analysis
### MCP Adapter Implementation
[Detailed class/method analysis]

### Tool Definitions
[Complete list of tools]

### Configuration Management
[Current vs. needed config loading]

### Integration Points
[How Calendar connects to orchestration]

## The Missing 5%
[Specific, detailed description of what's incomplete]

## Completion Plan
[Step-by-step plan with time estimates]

## Pattern for GitHub
[Key patterns GitHub should follow]

## Test Coverage
[What exists, what's needed]

## Appendix: Evidence
[All code excerpts, grep results, Serena queries]
```

---

## Remember

- Calendar is **95% complete** - don't overcomplicate
- This is **detective work** - understand what exists
- Focus on **configuration loading** - that's likely the 5%
- Document **patterns** - GitHub needs to follow them
- Use **Serena MCP** - faster and more accurate
- Provide **evidence** - code excerpts and line numbers

---

**Time Budget**: 1 hour for investigation
**Expected Output**: Clear understanding of missing 5% and completion plan
**Next Phase**: Implement the completion based on your findings

---

**Ready to investigate Calendar MCP and find the missing 5%!** 🔍
