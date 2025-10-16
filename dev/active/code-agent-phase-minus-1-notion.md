# Code Agent Prompt: Phase -1 - NotionMCPAdapter Investigation

**Date**: October 15, 2025, 8:06 AM
**Sprint**: A2 - Notion & Errors
**Issue**: CORE-NOTN #142 - API connectivity fix
**Phase**: -1 (Investigation)
**Duration**: 30-45 minutes
**Agent**: Code Agent

---

## Mission

Investigate the current state of NotionMCPAdapter to understand what exists, what's missing, and how to properly add the `get_current_user()` method.

**Context**: Enhanced validation in `config/notion_user_config.py:925` tries to call `adapter.get_current_user()` but the method doesn't exist. We need to understand the adapter architecture before implementing.

**Philosophy**: Understand before implementing. No assumptions.

---

## Investigation Steps

### Step 1: Locate NotionMCPAdapter

```bash
# Find the NotionMCPAdapter implementation
find . -name "*notion*adapter*.py" -type f | grep -v __pycache__ | grep -v .pyc

# Also check for notion plugin/integration files
find services/integrations/notion -name "*.py" -type f | head -20
```

**Document**:
- File location(s)
- Current class structure
- Existing methods

---

### Step 2: Review Current NotionMCPAdapter Implementation

**Read the adapter file** (likely in `services/integrations/notion/`):

```bash
# Use view tool to read the file
# Look for:
# - Class definition
# - Existing methods (especially any user-related methods)
# - MCP integration patterns
# - Error handling approach
```

**Document**:
- Current methods list
- Any user-related methods (if any)
- MCP tool usage patterns
- Base class (if inheriting)

---

### Step 3: Find the Error Location

**Examine the config loader** at `config/notion_user_config.py:925`:

```bash
# Read around line 925 to see the context
# Use view tool with line range like [900, 950]
```

**Document**:
- Exact error context
- How enhanced validation is trying to use `get_current_user()`
- What the method is expected to return
- Error handling expectations

---

### Step 4: Check for Similar Patterns

**Look for similar adapters** to understand the pattern:

```bash
# Check GitHub adapter (likely has similar user methods)
find services/integrations/github -name "*adapter*.py" -type f

# Check if there's a base adapter class
find services/integrations -name "base*.py" -o -name "*base*.py" | head -10
```

**Document**:
- Similar user-fetching methods in other adapters
- Common patterns for MCP adapters
- Expected method signatures

---

### Step 5: Review Notion MCP Tool Capabilities

**Check what Notion MCP server provides**:

```bash
# Look for Notion MCP configuration or documentation
find . -name "*notion*mcp*.py" -o -name "*mcp*notion*.py" | grep -v __pycache__

# Check if there are any MCP tool definitions for Notion
grep -r "notion.*get.*user\|get_current_user" services/ --include="*.py" | head -10
```

**Document**:
- Available Notion MCP tools
- User-related capabilities
- API access patterns

---

### Step 6: Check Notion API Documentation References

**Look for existing Notion API usage**:

```bash
# Find where Notion API is currently used
grep -r "notion.*api\|NotionClient" services/integrations/notion --include="*.py" | head -20

# Check for any existing user queries
grep -r "current.*user\|me\|whoami" services/integrations/notion --include="*.py"
```

**Document**:
- Current Notion API usage patterns
- Authentication approach
- Any existing user-related calls

---

### Step 7: Review Integration Tests

**Check what tests exist**:

```bash
# Find Notion integration tests
find tests -path "*notion*" -name "*.py" -type f | head -20

# Look for adapter tests specifically
find tests -name "*notion*adapter*.py" -type f
```

**Document**:
- Existing test patterns
- What's already tested
- Mock patterns used

---

## Investigation Report

Create a summary document: `/tmp/phase-minus-1-notion-investigation.md`

```markdown
# Phase -1: NotionMCPAdapter Investigation

## Current State

### NotionMCPAdapter Location
- File: [path]
- Lines: [total]
- Class structure: [summary]

### Existing Methods
[List all current methods with brief descriptions]

### Missing Method
- Method needed: `get_current_user()`
- Called from: config/notion_user_config.py:925
- Expected behavior: [what enhanced validation needs]

## Similar Patterns

### Other Adapters
[Document similar methods in GitHubAdapter, SlackAdapter, etc.]

### MCP Tool Patterns
[Document how other adapters use MCP tools]

## Notion API Context

### Current API Usage
[How Notion API is currently accessed]

### Authentication
[How authentication is handled]

### Available Capabilities
[What Notion MCP server provides]

## Implementation Approach

### Recommended Signature
```python
async def get_current_user(self) -> Dict[str, Any]:
    """
    Get current authenticated Notion user.
    
    Returns:
        Dict with user information (id, name, email, etc.)
        
    Raises:
        NotionAPIError: If API call fails
        AuthenticationError: If credentials invalid
    """
```

### Dependencies Needed
[Any new imports, MCP tools, etc.]

### Testing Approach
[How to test this method]

## Open Questions
[Any uncertainties or decisions needed]

## Next Steps
[Recommended implementation order]
```

---

## Deliverables

### Investigation Complete When:
- [ ] NotionMCPAdapter current state documented
- [ ] Missing method requirements understood
- [ ] Similar patterns identified
- [ ] Implementation approach recommended
- [ ] Open questions listed
- [ ] Summary report created

---

## Time Budget

**Target**: 30-45 minutes
- Step 1-2: Locate and review adapter (10 min)
- Step 3: Review error location (5 min)
- Step 4-5: Check patterns and MCP tools (10 min)
- Step 6: Review API usage (5 min)
- Step 7: Check tests (5 min)
- Report: Create summary (10 min)

---

## What NOT to Do

- ❌ Don't implement anything yet
- ❌ Don't modify any files
- ❌ Don't run tests (just identify them)
- ❌ Don't make assumptions about what's needed

## What TO Do

- ✅ Read existing code carefully
- ✅ Document current state accurately
- ✅ Identify patterns in similar code
- ✅ List all findings
- ✅ Recommend clear next steps
- ✅ Note any surprises or concerns

---

## Success Criteria

**Investigation is successful when**:
- We understand exactly what NotionMCPAdapter currently does
- We know exactly what `get_current_user()` needs to do
- We have a clear implementation plan
- We've identified any risks or complications
- We can start implementation confidently

---

## Context

**Why Phase -1 Matters**: 
- Notion integration is "partly done work" (per PM)
- Need to understand current state before adding
- Enhanced validation depends on this method
- Want to match existing patterns, not reinvent

**What Comes After**:
- Phase 1: Implement `get_current_user()` method
- Phase 2: Test enhanced validation
- Phase 3: Verify all validation tiers work

**This Phase**: Pure discovery - understand the landscape before making changes!

---

**Phase -1 Start Time**: 8:06 AM
**Expected Completion**: ~8:45 AM (30-45 minutes)
**Status**: Ready for Code Agent execution

**LET'S INVESTIGATE!** 🔍

---

*"Understand the ground before taking the next step."*
*- Phase -1 Philosophy*
