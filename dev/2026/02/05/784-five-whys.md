# Five Whys Analysis: #784 Calendar Plugin Crash

**Date**: 2026-02-05
**Issue**: #784 - BUG: Calendar plugin is_configured() crashes

## The Problem

Calendar plugin crashes with `TypeError: CalendarConfigService.is_configured() missing 1 required positional argument: 'user_id'`

## Five Whys

### 1. Why does CalendarPlugin.is_configured() crash?
It calls `self.config_service.is_configured()` without passing `user_id` (line 65).

### 2. Why does it need a user_id?
Issue #734 made `user_id` required for multi-tenancy - config is now per-user.

### 3. Why doesn't the plugin have a user_id to pass?
At plugin startup (and in status endpoints), there's no user context available.

### 4. Why wasn't this caught before?
Same reason as #781 - the multi-tenancy change (#734) wasn't propagated to all callers.

### 5. Why does this matter at startup?
The plugin auto-registers at import time (line 95-96) and tests/status endpoints call `is_configured()`.

## Root Cause

**Same as #781**: `is_configured()` is called without user context at startup/status check time.

## Established Pattern (from #781 fix)

Return `False` from `is_configured()` when no user context available:

```python
def is_configured(self) -> bool:
    """Check if Calendar is properly configured.

    Note: At plugin startup, there's no user context available.
    This returns False until a user context is established.
    """
    # Without user context, we can't determine configuration
    # The config_service.is_configured() requires user_id (Issue #734)
    return False
```

## Files to Modify

| File | Change |
|------|--------|
| `services/integrations/calendar/calendar_plugin.py` | Apply same pattern as Notion fix |

## Verification

- Server starts cleanly with Calendar plugin loaded
- Plugin functional tests pass (no TypeError)
- Status endpoint returns `configured: false` without crashing
