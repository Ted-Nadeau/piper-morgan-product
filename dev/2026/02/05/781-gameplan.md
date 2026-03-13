# Gameplan: #781 - Notion Plugin Startup Crash

**Issue**: #781 - BUG: Notion plugin crashes on startup - missing user_id argument
**Date**: 2026-02-05
**Author**: Lead Developer

---

## Problem Statement

The Notion plugin crashes during server startup with:
```
NotionConfigService.get_config() missing 1 required positional argument: 'user_id'
```

This prevents the Notion plugin from loading, degrading the plugin system.

---

## Five Whys Analysis

1. **Why does the plugin crash?**
   → `NotionMCPAdapter.__init__` calls `config_service.get_config()` without a `user_id`

2. **Why does `get_config()` require `user_id`?**
   → Issue #734 added multi-tenancy isolation; all config services now require `user_id`

3. **Why is `get_config()` called without `user_id`?**
   → The adapter initialization happens at import time, before any user context exists

4. **Why does Slack work but Notion fails?**
   → Slack uses lazy config loading (stores service, accesses config later); Notion eagerly loads config in `__init__`

5. **Why is there also an AttributeError in `__del__`?**
   → When `__init__` fails at line 55, `_session` (set on line 62) is never initialized, causing `__del__` to crash

---

## Root Cause

Two bugs in `services/integrations/mcp/notion_adapter.py`:

### Bug 1: Eager Config Loading (Primary)
**File**: `services/integrations/mcp/notion_adapter.py`
**Line**: 55
**Code**: `self.config = config_service.get_config()`
**Issue**: Calls `get_config()` without required `user_id` during `__init__`

### Bug 2: Unguarded `__del__` (Secondary)
**File**: `services/integrations/mcp/notion_adapter.py`
**Lines**: 858-861
**Code**: `if self._session and not self._session.closed:`
**Issue**: References `self._session` which may not exist if `__init__` fails early

---

## Additional Discovery

`NotionPlugin.is_configured()` also calls `config_service.is_configured()` without `user_id`:
- **File**: `services/integrations/notion/notion_plugin.py`
- **Line**: 67

All plugins (Slack, GitHub, Calendar) have the same pattern but aren't crashing yet because they don't eagerly call `get_config()`.

---

## Solution

### Approach: Lazy Configuration Loading

Follow Slack's pattern: store the config_service but don't call `get_config()` until actually needed (when user context is available).

### Changes

#### 1. Fix `NotionMCPAdapter.__init__` (Primary Fix)

```python
# Before (line 55):
self.config = config_service.get_config()

# After:
self.config = None  # Lazy load when user context available
```

Also update `_initialize_client()` to handle `None` config gracefully.

#### 2. Fix `NotionMCPAdapter.__del__` (Secondary Fix)

```python
# Before:
def __del__(self):
    if self._session and not self._session.closed:
        asyncio.create_task(self.close())

# After:
def __del__(self):
    if hasattr(self, '_session') and self._session and not self._session.closed:
        asyncio.create_task(self.close())
```

#### 3. Fix `NotionPlugin.is_configured()` (Related Fix)

The plugin's `is_configured()` method can't work without user context. Options:

**Option A**: Return `False` at startup (no user context = not configured)
```python
def is_configured(self) -> bool:
    # Without user context, we can't determine configuration
    # Return False to indicate "not configured for current context"
    return False
```

**Option B**: Add method that checks environment-level config exists
```python
def is_configured(self) -> bool:
    # Check if any notion config exists (API key in env/keychain)
    return self.config_service.has_any_config()
```

**Recommendation**: Option A is simpler and safer. Plugin is "not configured" until a user context is established.

---

## Files to Modify

| File | Change |
|------|--------|
| `services/integrations/mcp/notion_adapter.py` | Bug 1 & 2: Lazy config, safe `__del__` |
| `services/integrations/notion/notion_plugin.py` | Bug 3: Return False when no user context |

---

## Phases

### Phase 1: Fix NotionMCPAdapter (Primary)
1. Modify `__init__` to use lazy config loading
2. Add `hasattr` guard to `__del__`
3. Ensure `_initialize_client()` handles None config

### Phase 2: Fix NotionPlugin
1. Modify `is_configured()` to return False (no user context)

### Phase 3: Verification
1. Start server, verify no crash
2. Check Notion plugin shows as loaded
3. Verify no AttributeError in logs

---

## Success Criteria

- [ ] Server starts without Notion plugin crash
- [ ] Notion plugin appears in loaded plugins list
- [ ] No `AttributeError` in `__del__`
- [ ] No `ValueError: user_id is required` at startup
- [ ] Clean startup logs

---

## Test Plan

1. `python main.py` - verify clean startup
2. Check output shows `📦 Loaded 5/5 plugin(s)` (or 4/5 if Notion not configured, but no crash)
3. No exceptions in startup logs

---

## Rollback Plan

Revert the two file changes if issues arise.

---

## Out of Scope

- Fixing `is_configured()` pattern across all plugins (systemic issue, separate ticket)
- Adding user context to plugin initialization (architectural change)
