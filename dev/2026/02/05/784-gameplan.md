# Gameplan: #784 Calendar Plugin Crash

**Issue**: #784 - BUG: Calendar plugin is_configured() crashes
**Date**: 2026-02-05

## Problem Statement

Calendar plugin crashes when `is_configured()` is called without user context, because `CalendarConfigService.is_configured()` requires `user_id` (Issue #734 multi-tenancy).

## Five Whys Summary

Same root cause as #781 (Notion plugin): plugin calls config service method that requires user context, but at startup/status check time there is no user context.

## Established Fix Pattern

From #781 fix: return `False` from plugin's `is_configured()` when no user context available.

## Files to Modify

| File | Change |
|------|--------|
| `services/integrations/calendar/calendar_plugin.py` | Line 63-65: Apply same pattern as Notion fix |

---

## Phase 1: Fix CalendarPlugin.is_configured()

**File**: `services/integrations/calendar/calendar_plugin.py`
**Lines**: 63-65

```python
# Before:
def is_configured(self) -> bool:
    """Check if Calendar is properly configured"""
    return self.config_service.is_configured()

# After:
def is_configured(self) -> bool:
    """Check if Calendar is properly configured.

    Note: At plugin startup, there's no user context available.
    This returns False until a user context is established.
    Issue #784: Fixed crash from calling is_configured() without user_id.
    """
    # Without user context, we can't determine configuration
    # The config_service.is_configured() requires user_id (Issue #734)
    return False
```

---

## Phase Z: Verification

### Success Criteria

- [ ] Server starts cleanly with Calendar plugin loaded
- [ ] No TypeError in logs
- [ ] Plugin functional tests pass
- [ ] Status endpoint returns without crash

### Test Plan

1. Start server, verify "Loaded 5/5 plugin(s)" includes Calendar
2. Run: `pytest tests/test_all_plugins_functional.py -v`
3. Check `/api/v1/integrations/calendar/status` returns `{"configured": false, ...}`

### Rollback Plan

Revert single method change in `calendar_plugin.py`.

---

## Work Characteristics

- **Scope**: Single method fix in one file
- **Risk**: Low - follows established pattern from #781
- **Duration**: < 10 minutes
- **Worktree**: Skip (trivial fix)
