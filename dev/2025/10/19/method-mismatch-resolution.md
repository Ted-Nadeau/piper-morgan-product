# Method Mismatch Resolution - GitHubIntegrationRouter

**Agent**: Claude Code
**Time**: 11:32 AM
**Issue**: GitHubIntegrationRouter → GitHubMCPSpatialAdapter method mismatch

---

## Architectural Context (ADR-013)

**From ADR-013** (MCP Spatial Integration Pattern):

All external integrations MUST use MCP+Spatial pattern:
```
Integration Router (standup, etc.)
    ↓ uses
GitHubIntegrationRouter (integration point)
    ↓ delegates to
GitHubMCPSpatialAdapter (MCP+Spatial implementation)
    ↓ uses
GitHub API
```

**Current State**: Phase 2 (Dual Implementation) - INCOMPLETE

The migration to MCP+Spatial is partially done:
- ✅ GitHubMCPSpatialAdapter exists with new methods
- ❌ GitHubIntegrationRouter still expects old method names
- Result: Methods don't match!

---

## The Solution: Add Adapter Methods

**GitHubIntegrationRouter** should provide the interface that consumers expect, then delegate to the MCP adapter.

### Required Adapter Methods

Add these methods to `GitHubIntegrationRouter`:

```python
# File: services/integrations/github/github_integration_router.py

class GitHubIntegrationRouter:
    """
    Integration router for GitHub operations.
    Provides stable interface while delegating to MCP+Spatial implementation.
    """

    def __init__(self, mcp_adapter: GitHubMCPSpatialAdapter):
        self._mcp_adapter = mcp_adapter

    # ADAPTER METHODS (stable interface for consumers)

    async def get_recent_issues(
        self,
        repo: str = None,
        limit: int = 10,
        state: str = "open"
    ) -> List[Dict[str, Any]]:
        """
        Get recent issues (adapter method).
        Delegates to MCP spatial adapter.
        """
        # Delegate to MCP adapter
        return await self._mcp_adapter.list_github_issues_direct(
            repository=repo,
            limit=limit,
            state=state
        )

    async def get_issue(
        self,
        issue_number: int,
        repo: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get single issue by number (adapter method).
        Delegates to MCP spatial adapter.
        """
        # Delegate to MCP adapter
        return await self._mcp_adapter.get_github_issue_direct(
            issue_number=issue_number,
            repository=repo
        )

    async def get_open_issues(
        self,
        repo: str = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get open issues (adapter method).
        Delegates to MCP spatial adapter.
        """
        # Same as get_recent_issues with state="open"
        return await self.get_recent_issues(
            repo=repo,
            limit=limit,
            state="open"
        )
```

---

## Implementation Steps

### Step 1: Locate the Router (5 minutes)

```bash
# Find GitHubIntegrationRouter
find services -name "*github*router*.py" -o -name "*github*integration*.py"

# Or use Serena
mcp__serena__find_symbol(
    name_regex="GitHubIntegrationRouter",
    scope="services"
)
```

### Step 2: Add Adapter Methods (20 minutes)

Add the three adapter methods shown above to `GitHubIntegrationRouter`.

**Key points**:
- These are **thin adapters** - just map parameters and delegate
- Don't duplicate logic - just translate interfaces
- Keep error handling in the MCP adapter layer

### Step 3: Update Imports if Needed (5 minutes)

Ensure the router has access to the MCP adapter:

```python
from services.integrations.github.github_mcp_spatial_adapter import GitHubMCPSpatialAdapter
```

### Step 4: Test the Fix (15 minutes)

```bash
# Run standup tests
pytest tests/features/test_morning_standup.py -v

# Try actual generation
python cli/commands/standup.py

# Should work now!
```

### Step 5: Document the Pattern (10 minutes)

Add a docstring to the router explaining the adapter pattern:

```python
"""
GitHubIntegrationRouter - Integration Router for GitHub

This router provides a stable interface for GitHub operations while delegating
to the MCP+Spatial implementation (GitHubMCPSpatialAdapter).

ARCHITECTURAL PATTERN (ADR-013):
- Consumers call router methods (get_recent_issues, get_issue, etc.)
- Router delegates to MCP+Spatial adapter
- Adapter provides 8-dimensional spatial context
- Adapter handles MCP protocol and circuit breakers

MIGRATION STATUS: Phase 2 (Dual Implementation)
- Adapter methods provide backward compatibility
- MCP+Spatial pattern provides new capabilities
- Legacy direct API methods deprecated

See ADR-013 for full architectural pattern.
"""
```

---

## Why This is the Right Fix

**From ADR-013 Migration Path**:

> **Phase 2: Dual Implementation** - Support both patterns during transition

That's exactly what we're doing:
- Router provides stable interface (backward compatible)
- Router delegates to MCP adapter (new pattern)
- Consumers don't need to change
- Migration can continue incrementally

**This is NOT a workaround** - it's the intended migration pattern!

---

## After the Fix

Once adapter methods are added:

1. ✅ Standup generation will work
2. ✅ All 4 modes will function
3. ✅ Phase 1B testing can continue
4. ✅ Architecture aligns with ADR-013

Future work (not now):
- Phase 3: Migrate consumers to use MCP directly
- Phase 4: Remove adapter methods (legacy cleanup)

But for Sprint A4, the adapter methods are the correct solution!

---

## Verification

After adding adapter methods, verify:

```bash
# Check method exists
python3 -c "
from services.integrations.github.github_integration_router import GitHubIntegrationRouter
import inspect
router = GitHubIntegrationRouter(None)
methods = [m for m in dir(router) if not m.startswith('_')]
print('get_recent_issues' in methods)  # Should be True
print('get_issue' in methods)  # Should be True
print('get_open_issues' in methods)  # Should be True
"

# Try standup generation
python cli/commands/standup.py
```

---

## Summary

**Problem**: Method name mismatch between router and adapter
**Root Cause**: Incomplete MCP+Spatial migration (Phase 2)
**Solution**: Add adapter methods to router (as per ADR-013)
**Impact**: Unblocks Sprint A4, aligns with architecture
**Time**: ~1 hour to implement and test

**This is the architecturally correct fix per ADR-013!**

---

**Confidence**: HIGH
**Architectural Alignment**: CORRECT (ADR-013)
**Action**: Add adapter methods to GitHubIntegrationRouter
