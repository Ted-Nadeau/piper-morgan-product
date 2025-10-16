# Code Agent Prompt: Phase 1 - Implement get_current_user() Method

**Date**: October 15, 2025, 8:48 AM
**Sprint**: A2 - Notion & Errors
**Issue**: CORE-NOTN #142 - API connectivity fix
**Phase**: 1 (Implementation)
**Duration**: ~20 minutes
**Agent**: Code Agent

---

## Mission

Implement the `get_current_user()` method in NotionMCPAdapter by extracting the existing working pattern from `test_connection()` and `get_workspace_info()`.

**Context**: Phase -1 investigation found that `self._notion_client.users.me()` already works perfectly in two places. We just need to expose it as a public method.

**Philosophy**: Use what works. Extract, don't reinvent.

---

## Implementation Plan

### File to Modify
`services/integrations/mcp/notion_adapter.py`

### Method to Add

Based on investigation findings, add this method after the existing connection-related methods (around line 110-140):

```python
async def get_current_user(self) -> Dict[str, Any]:
    """
    Get the current authenticated Notion user.

    Retrieves information about the user associated with the API token.
    Used by enhanced validation in configuration loader.

    Returns:
        Dict containing user information with keys:
            - id (str): User's Notion ID
            - name (str): User's display name
            - avatar_url (str): URL to user's avatar
            - type (str): User type (person/bot)
            - email (str, optional): User's email if available

    Raises:
        NotionConnectionError: If API call fails

    Example:
        >>> adapter = NotionMCPAdapter(token="secret")
        >>> user = await adapter.get_current_user()
        >>> print(user['name'])
        'John Doe'
    """
    try:
        # Use existing working pattern from test_connection() and get_workspace_info()
        user = self._notion_client.users.me()

        return {
            "id": user.id,
            "name": user.name if hasattr(user, 'name') else "Unknown",
            "avatar_url": user.avatar_url if hasattr(user, 'avatar_url') else None,
            "type": user.type if hasattr(user, 'type') else "unknown",
            "email": getattr(user, 'email', None),
        }

    except Exception as e:
        raise NotionConnectionError(
            f"Failed to get current user: {str(e)}"
        ) from e
```

### Location Guidance

**Where to place the method**:
1. Look for the connection-related methods section
2. Place after `test_connection()` (around line 110)
3. Keep it near other user/workspace methods for logical grouping

**Pattern to follow**:
- Look at how `test_connection()` calls `self._notion_client.users.me()`
- Look at how `get_workspace_info()` calls `self._notion_client.users.me()`
- Use the same error handling pattern

---

## Implementation Steps

### Step 1: Read Current Implementation

```bash
# Review the file structure first
view services/integrations/mcp/notion_adapter.py -r [100, 150]
```

**Verify**:
- Line numbers for insertion point
- Existing error handling patterns
- Import statements at top (check if NotionConnectionError is available)

---

### Step 2: Add the Method

Use `str_replace` to insert the new method:

```bash
# Find the insertion point (likely after test_connection method)
# Use str_replace to add the new method
```

**Make sure**:
- Proper indentation (4 spaces)
- Docstring follows existing style
- Error handling matches existing patterns
- Return type annotation is correct

---

### Step 3: Verify No Syntax Errors

```bash
# Quick syntax check
python -m py_compile services/integrations/mcp/notion_adapter.py
```

**If errors**: Fix syntax before proceeding

---

### Step 4: Check Integration Point

```bash
# Verify the config loader can now call this method
view config/notion_user_config.py -r [370, 380]
```

**Confirm**:
- The call site (line 373) will now work
- Method signature matches what's being called
- No other changes needed in config loader

---

## Testing Strategy (Brief Check)

### Quick Manual Test

```bash
# Just verify the file loads without errors
python -c "from services.integrations.mcp.notion_adapter import NotionMCPAdapter; print('Import successful')"
```

**Note**: Full testing will be Phase 2, but verify import works

---

## Deliverables

### Phase 1 Complete When:
- [ ] Method added to NotionMCPAdapter
- [ ] Proper docstring with examples
- [ ] Error handling matches existing patterns
- [ ] No syntax errors
- [ ] File imports successfully
- [ ] Changes committed to git

### Git Commit

```bash
git add services/integrations/mcp/notion_adapter.py
git commit -m "feat(notion): add get_current_user() method to NotionMCPAdapter

Implements missing method needed by enhanced validation in config loader.

- Extracts existing self._notion_client.users.me() pattern
- Returns user info dict with id, name, avatar_url, type, email
- Proper error handling with NotionConnectionError
- Matches patterns from test_connection() and get_workspace_info()

Fixes: CORE-NOTN #142
Part of: Sprint A2, Phase 1"

git push origin main
```

---

## What NOT to Do

- ❌ Don't add any new API calls (use existing pattern)
- ❌ Don't modify test_connection() or get_workspace_info()
- ❌ Don't add tests yet (that's Phase 2)
- ❌ Don't modify config/notion_user_config.py (should work as-is)
- ❌ Don't change any other methods

## What TO Do

- ✅ Extract the exact pattern that already works
- ✅ Match existing code style
- ✅ Use same error handling approach
- ✅ Keep it simple and clean
- ✅ Commit and push when done

---

## Success Criteria

**Implementation is successful when**:
- Method exists in NotionMCPAdapter
- Follows existing patterns exactly
- Docstring is complete and helpful
- No syntax errors
- File imports successfully
- Committed to git

---

## Time Budget

**Target**: ~20 minutes
- Read current code: 5 min
- Add method: 5 min
- Verify syntax: 2 min
- Check integration: 3 min
- Git commit: 5 min

---

## Context

**Why This Matters**:
- Unblocks enhanced validation in config loader
- Exposes existing working functionality
- Completes partly-done work
- Very low risk (no new functionality)

**What Comes After**:
- Phase 2: Add comprehensive tests
- Phase 3: Verify enhanced validation works end-to-end

---

**Phase 1 Start Time**: 8:48 AM
**Expected Completion**: ~9:08 AM (20 minutes)
**Status**: Ready for implementation

**LET'S BUILD IT!** 🔨

---

*"Extract what works. Make it public. Keep it simple."*
*- Phase 1 Philosophy*
