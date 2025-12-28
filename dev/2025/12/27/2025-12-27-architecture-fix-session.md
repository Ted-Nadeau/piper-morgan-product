# Session Log: Architecture Violation Fix

**Date**: December 27, 2025
**Lead Developer**: Opus 4.5
**Issue**: #518 (Canonical Queries Phase A) - Architecture violation repair

---

## Summary

Fixed CORE-QUERY-1 architecture pattern violations in calendar-related intent handlers.

## Methodological Observations

### The System Worked (In the Breach)

The pre-commit hook architecture enforcement caught the violation before it could be merged. This demonstrates:

1. **Defense in depth working**: Even though the gameplan review failed, the technical guardrails caught it
2. **Pre-commit hooks as safety net**: The "Prevent Direct Adapter Imports" check blocked the bad code
3. **Violation visible at commit time**: Not silently merged, forced immediate attention

### Process Gaps Identified

1. **Gameplan-to-Pattern Audit Missing**: No step verifies gameplan approach against pattern catalog
2. **"Missing Method" Escalation Path Unclear**: When router lacks a method, agents don't know to extend it
3. **Expediency Pressure**: Time pressure led to shortcut (bypass router) instead of correct fix (extend router)

### Resilience Demonstrated

- Pre-commit caught violation → forced stop
- Root cause analysis completed within same session
- Fix applied properly (extended infrastructure, didn't just remove the check)
- Retro issue filed (#525) for process improvement

### Recommendation

Add to gameplan template:
```markdown
## Infrastructure Compatibility Check
- [ ] Does the router have all required methods?
- [ ] If not, is "extend router" in scope, or should we STOP?
- [ ] CORE-QUERY-1 pattern compliance verified?
```

## Root Cause Analysis

### What Happened
- Issue #518 Phase A (Dec 26) included Calendar Cluster queries (#34, #35, #61)
- The gameplan specified direct `GoogleCalendarMCPAdapter` usage instead of `CalendarIntegrationRouter`
- Code agent followed the gameplan faithfully
- The violation was never committed due to session ending, but was detected on Dec 27 when trying to commit

### Why It Happened
1. **Gameplan not audited against patterns**: The CORE-QUERY-1 pattern requires router usage, but gameplan specified adapter bypass
2. **Missing router methods**: CalendarIntegrationRouter lacked `get_events_in_range()` and `get_recurring_events()` methods
3. **Expediency over correctness**: Rather than extending the router (correct approach), the gameplan took a shortcut

### What Should Have Happened
1. Gameplan should verify router has required methods
2. If not, Phase A should first extend CalendarIntegrationRouter
3. Then use those router methods from intent handlers

## Fix Applied

### Files Modified
1. **`services/mcp/consumer/google_calendar_adapter.py`**
   - Added `get_events_in_range(start, end)` method
   - Added `get_recurring_events(days_ahead)` method

2. **`services/integrations/calendar/calendar_integration_router.py`**
   - Added router wrapper for `get_events_in_range()`
   - Added router wrapper for `get_recurring_events()`

3. **`services/intent/intent_service.py`**
   - Fixed `_handle_meeting_time_query()` - replaced adapter with router
   - Fixed `_handle_recurring_meetings_query()` - replaced adapter with router + use new method
   - Fixed `_handle_week_calendar_query()` - replaced adapter with router + use new method
   - Fixed `_handle_attention_query()` calendar section - replaced adapter with router

## Lessons Learned

1. **Gameplans must be audited against pattern catalog** before PM approval
2. **"Router doesn't have method" should trigger router extension**, not bypass
3. **Pre-commit hooks caught the violation** - architecture enforcement working correctly
4. **Always extend infrastructure to support patterns**, don't work around them

## Verification

- All `GoogleCalendarMCPAdapter` direct imports removed from `intent_service.py`
- Pre-commit hook "Prevent Direct Adapter Imports" now passes
- Calendar handlers still function through router abstraction
