# Cursor Agent Prompt: Phase 1 - Calendar Router Cross-Validation

## Your Identity
You are Cursor Agent, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- CURRENT-STATE.md - Current epic and focus
- role/PROGRAMMER.md - Your role requirements
- METHODOLOGY.md - Inchworm Protocol

## Session Log Management

Continue using your existing session log at: `dev/2025/09/28/2025-09-28-1702-prog-cursor-log.md`
- Add timestamped entry for Phase 1 verification work
- Document router verification findings
- Include all test evidence

## Mission: Verify Calendar Router Implementation

**Context**: Code agent has implemented CalendarIntegrationRouter following GitHubIntegrationRouter pattern. Your role is to verify the implementation is correct, complete, and follows established patterns before proceeding to Notion router.

**Objective**: Provide independent verification that Calendar router works correctly with proper delegation, feature flag control, and OAuth preservation.

## Code's Implementation to Verify

Code should have created:
- `services/integrations/calendar/calendar_integration_router.py`
- Router class with 7 async methods
- Feature flag control (USE_SPATIAL_CALENDAR)
- Delegation pattern matching GitHub router
- OAuth preservation through router

## Your Verification Tasks

### Task 1: Verify File Structure

```bash
# Check router file exists
ls -la services/integrations/calendar/calendar_integration_router.py

# Check file size and structure
wc -l services/integrations/calendar/calendar_integration_router.py
grep "^class " services/integrations/calendar/calendar_integration_router.py
grep "async def " services/integrations/calendar/calendar_integration_router.py | wc -l
```

**Verify**: File exists, has CalendarIntegrationRouter class, has 7 async methods

### Task 2: Pattern Compliance Check

Compare with GitHub router pattern:

```bash
# Extract GitHub router patterns
echo "=== GitHub Router Pattern ==="
grep -A 10 "def __init__" services/integrations/github/github_integration_router.py | head -15
grep -A 15 "_get_preferred_integration" services/integrations/github/github_integration_router.py | head -20

# Extract Calendar router patterns
echo "=== Calendar Router Pattern ==="
grep -A 10 "def __init__" services/integrations/calendar/calendar_integration_router.py | head -15
grep -A 15 "_get_preferred_integration" services/integrations/calendar/calendar_integration_router.py | head -20
```

**Verify**: Pattern matches GitHub router structure exactly

### Task 3: Method Signature Verification

Check router methods match GoogleCalendarMCPAdapter:

```python
# Verify router method signatures
import asyncio
import inspect
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

async def verify_signatures():
    router = CalendarIntegrationRouter()
    adapter = GoogleCalendarMCPAdapter()

    # Expected methods
    methods = ['authenticate', 'get_todays_events', 'get_current_meeting',
               'get_next_meeting', 'get_free_time_blocks', 'get_temporal_summary',
               'health_check']

    mismatches = []

    for method_name in methods:
        # Check router has method
        if not hasattr(router, method_name):
            mismatches.append(f"❌ Router missing {method_name}")
            continue

        # Check both are async
        router_method = getattr(router, method_name)
        adapter_method = getattr(adapter, method_name)

        router_async = inspect.iscoroutinefunction(router_method)
        adapter_async = inspect.iscoroutinefunction(adapter_method)

        if router_async != adapter_async:
            mismatches.append(f"❌ {method_name} async mismatch: router={router_async}, adapter={adapter_async}")
        else:
            print(f"✅ {method_name} signature matches")

    return mismatches

asyncio.run(verify_signatures())
```

**Verify**: All 7 methods present and async matches adapter

### Task 4: Feature Flag Control Testing

Test that feature flags actually control behavior:

```python
# Test feature flag control
import asyncio
import os
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

async def test_feature_flags():
    # Test 1: Spatial enabled (default)
    os.environ['USE_SPATIAL_CALENDAR'] = 'true'
    router_spatial = CalendarIntegrationRouter()
    integration_spatial, is_legacy_spatial = router_spatial._get_preferred_integration('test')

    print("=== Spatial Mode Test ===")
    print(f"Integration: {type(integration_spatial).__name__ if integration_spatial else 'None'}")
    print(f"Is legacy: {is_legacy_spatial}")
    print(f"Expected: GoogleCalendarMCPAdapter, False")

    if integration_spatial and not is_legacy_spatial:
        print("✅ Spatial mode works correctly")
    else:
        print("❌ Spatial mode failed")

    # Test 2: Spatial disabled
    os.environ['USE_SPATIAL_CALENDAR'] = 'false'
    router_disabled = CalendarIntegrationRouter()
    integration_disabled, is_legacy_disabled = router_disabled._get_preferred_integration('test')

    print("\n=== Spatial Disabled Test ===")
    print(f"Integration: {type(integration_disabled).__name__ if integration_disabled else 'None'}")
    print(f"Is legacy: {is_legacy_disabled}")
    print(f"Expected: None, False (no legacy exists)")

    if integration_disabled is None:
        print("✅ Disabled mode works correctly")
    else:
        print("❌ Disabled mode unexpected result")

asyncio.run(test_feature_flags())
```

**Verify**: Feature flags control which integration is used

### Task 5: Delegation Pattern Testing

Verify methods actually delegate to underlying adapter:

```python
# Test delegation works
import asyncio
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

async def test_delegation():
    router = CalendarIntegrationRouter()

    # Test health_check delegation (doesn't require auth)
    try:
        health = await router.health_check()
        print("✅ health_check delegates successfully")
        print(f"   Result type: {type(health)}")
        print(f"   Has status: {'status' in health if isinstance(health, dict) else 'N/A'}")
    except Exception as e:
        print(f"❌ health_check delegation failed: {e}")

    # Test that RuntimeError is raised with no integration
    import os
    os.environ['USE_SPATIAL_CALENDAR'] = 'false'
    router_disabled = CalendarIntegrationRouter()

    try:
        await router_disabled.health_check()
        print("❌ Should have raised RuntimeError")
    except RuntimeError as e:
        print(f"✅ RuntimeError raised correctly: {str(e)[:50]}...")
    except Exception as e:
        print(f"❌ Wrong exception type: {type(e)}")

asyncio.run(test_delegation())
```

**Verify**: Methods delegate correctly and raise RuntimeError when appropriate

### Task 6: OAuth Preservation Check

Critical verification that OAuth still works:

```python
# Verify OAuth patterns preserved
import asyncio
import inspect
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

async def verify_oauth_preservation():
    router = CalendarIntegrationRouter()
    adapter = GoogleCalendarMCPAdapter()

    # Check authenticate method
    router_auth = router.authenticate
    adapter_auth = adapter.authenticate

    print("=== OAuth Method Verification ===")
    print(f"Router authenticate exists: {router_auth is not None}")
    print(f"Router authenticate is async: {inspect.iscoroutinefunction(router_auth)}")
    print(f"Adapter authenticate is async: {inspect.iscoroutinefunction(adapter_auth)}")

    # Verify authentication flow isn't broken
    # (Don't actually authenticate in test - just verify method callable)
    print(f"\n✅ OAuth method structure preserved")

asyncio.run(verify_oauth_preservation())
```

**Verify**: OAuth authentication pattern works through router

### Task 7: Error Handling Verification

Check that errors are handled correctly:

```python
# Test error handling
import asyncio
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

async def test_error_handling():
    # Test with no integration available
    import os
    os.environ['USE_SPATIAL_CALENDAR'] = 'false'
    router = CalendarIntegrationRouter()

    methods_to_test = ['get_todays_events', 'get_current_meeting', 'get_next_meeting']

    for method_name in methods_to_test:
        try:
            method = getattr(router, method_name)
            await method()
            print(f"❌ {method_name} should have raised RuntimeError")
        except RuntimeError as e:
            error_msg = str(e)
            if "No calendar integration available" in error_msg:
                print(f"✅ {method_name} raises correct RuntimeError")
            else:
                print(f"⚠️ {method_name} RuntimeError message unexpected: {error_msg[:50]}")
        except Exception as e:
            print(f"❌ {method_name} raised wrong exception: {type(e)}")

asyncio.run(test_error_handling())
```

**Verify**: Proper RuntimeError with helpful message when integration unavailable

## Cross-Validation Report Format

```markdown
# Phase 1: Calendar Router Cross-Validation Report

## Verification Summary
[APPROVED / ISSUES_FOUND / BLOCKING_PROBLEMS]

## File Structure Verification
- File exists: [YES/NO]
- Location correct: [YES/NO]
- Line count: [number]
- Class name correct: [YES/NO]

## Pattern Compliance

### Initialization Pattern
- [ ] Matches GitHub router __init__ structure
- [ ] Feature flag checking present
- [ ] Integration initialization correct
- Issues: [none or list]

### Delegation Pattern
- [ ] _get_preferred_integration follows GitHub pattern
- [ ] Returns (integration, is_legacy) tuple
- [ ] Checks spatial first, then legacy
- Issues: [none or list]

### Deprecation Warning Pattern
- [ ] _warn_deprecation_if_needed implemented
- [ ] Follows GitHub pattern
- Issues: [none or list]

## Method Verification

### Method Completeness: X/7
- [ ] authenticate
- [ ] get_todays_events
- [ ] get_current_meeting
- [ ] get_next_meeting
- [ ] get_free_time_blocks
- [ ] get_temporal_summary
- [ ] health_check

### Signature Compliance
[List any signature mismatches between router and adapter]

## Feature Flag Control Testing

### Spatial Mode (USE_SPATIAL_CALENDAR=true)
**Result**: [WORKS / FAILS]
**Integration Used**: [GoogleCalendarMCPAdapter / Other / None]
**Evidence**: [test output]

### Spatial Disabled (USE_SPATIAL_CALENDAR=false)
**Result**: [WORKS / FAILS]
**Integration Used**: [None expected]
**Evidence**: [test output]

## Delegation Testing

### Method Delegation
**health_check**: [WORKS / FAILS]
**Evidence**: [test output showing delegation]

### RuntimeError Handling
**Behavior**: [Raises RuntimeError / Fails silently / Other]
**Message Quality**: [Helpful / Generic / Missing]
**Evidence**: [test output]

## OAuth Preservation

**authenticate method**: [PRESERVED / BROKEN]
**Async pattern**: [CORRECT / INCORRECT]
**Evidence**: [test output]

## Error Handling

**RuntimeError when no integration**: [YES / NO]
**Error message quality**: [GOOD / NEEDS_IMPROVEMENT]
**Tested methods**: [list methods tested]

## Issues Identified

### Blocking Issues
[Issues that prevent router from working]

### Non-Blocking Issues
[Minor issues that should be fixed but don't block functionality]

### Recommendations
[Suggestions for improvement]

## Readiness Assessment

[APPROVED_FOR_PHASE_2 / NEEDS_FIXES / BLOCKING_PROBLEMS]

### If Approved
Calendar router pattern validated - ready for Notion implementation

### If Needs Fixes
[Specific fixes required before proceeding]
```

## Update Requirements

After completing verification:

1. **Update Session Log**: Add Phase 1 verification completion
2. **Update GitHub Issue #199**: Add comment with Calendar router verification results
3. **Tag Lead Developer**: Report approval or issues requiring fixes

## Critical Verification Standards

- **Independent Testing**: Run your own tests, don't just review Code's output
- **Pattern Compliance**: GitHub router is the standard - flag any deviations
- **Functional Testing**: Actually execute methods to verify they work
- **Edge Cases**: Test error conditions, not just happy path
- **OAuth Critical**: Authentication MUST work through router

## Questions to Answer

- Does router follow GitHub pattern exactly?
- Do all 7 methods work correctly?
- Does feature flag control actually work?
- Is OAuth preserved through delegation?
- Are errors handled properly?
- Any edge cases Code missed?

---

**Your Mission**: Verify Calendar router is correct, complete, and pattern-compliant before proceeding to Notion router implementation.

**Quality Standard**: Thorough independent verification prevents implementation errors from propagating to other routers.
