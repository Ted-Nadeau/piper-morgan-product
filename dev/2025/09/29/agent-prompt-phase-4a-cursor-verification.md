# Cursor Agent Prompt: Phase 4A - Calendar Migration Verification

## Mission: Verify Calendar Service Migration

**Context**: Code agent has migrated 2 Calendar services from GoogleCalendarMCPAdapter to CalendarIntegrationRouter. Your role is to independently verify the migrations are complete, correct, and preserve service functionality.

**Objective**: Confirm both Calendar services work correctly after router migration with no functionality regressions.

## Services to Verify

### Service 1: canonical_handlers.py
**Expected Migration**: `GoogleCalendarMCPAdapter` → `CalendarIntegrationRouter`
**Location**: `services/intent_service/canonical_handlers.py`

### Service 2: morning_standup.py
**Expected Migration**: `GoogleCalendarMCPAdapter` → `CalendarIntegrationRouter`
**Location**: `services/features/morning_standup.py`

## Verification Tasks

### Task 1: Import Migration Verification

Check that imports were correctly replaced:

```bash
# Verify correct imports in both services
echo "=== canonical_handlers.py imports ==="
grep -n "CalendarIntegrationRouter\|GoogleCalendarMCPAdapter" services/intent_service/canonical_handlers.py

echo "=== morning_standup.py imports ==="
grep -n "CalendarIntegrationRouter\|GoogleCalendarMCPAdapter" services/features/morning_standup.py

# Check that old imports are completely removed
echo "=== Checking for any remaining direct imports ==="
grep -r "from.*google_calendar_adapter import\|GoogleCalendarMCPAdapter" services/intent_service/canonical_handlers.py services/features/morning_standup.py && echo "❌ Direct imports still found" || echo "✅ No direct imports found"
```

**Verify**: Both services import CalendarIntegrationRouter, no GoogleCalendarMCPAdapter imports remain

### Task 2: Service Import Functionality

Test that both services can be imported without errors:

```python
import sys
import traceback

def test_service_imports():
    services = [
        ('canonical_handlers', 'services.intent_service.canonical_handlers'),
        ('morning_standup', 'services.features.morning_standup')
    ]

    results = {}

    for name, module_path in services:
        try:
            __import__(module_path)
            print(f"✅ {name}: Imports successfully")
            results[name] = True
        except Exception as e:
            print(f"❌ {name}: Import failed - {e}")
            traceback.print_exc()
            results[name] = False

    return results

results = test_service_imports()
all_passed = all(results.values())
print(f"\nOverall result: {'✅ All services import successfully' if all_passed else '❌ Some services failed to import'}")
```

**Verify**: Both services import without errors

### Task 3: Router Instantiation Verification

Check that services can create router instances:

```python
import asyncio

async def test_router_instantiation():
    # Test canonical_handlers
    try:
        from services.intent_service import canonical_handlers
        print("✅ canonical_handlers module loaded")

        # Look for calendar-related classes or functions
        calendar_attrs = [attr for attr in dir(canonical_handlers)
                         if 'calendar' in attr.lower()]
        print(f"Calendar-related attributes: {calendar_attrs}")

    except Exception as e:
        print(f"❌ canonical_handlers instantiation issue: {e}")

    # Test morning_standup
    try:
        from services.features import morning_standup
        print("✅ morning_standup module loaded")

        calendar_attrs = [attr for attr in dir(morning_standup)
                         if 'calendar' in attr.lower()]
        print(f"Calendar-related attributes: {calendar_attrs}")

    except Exception as e:
        print(f"❌ morning_standup instantiation issue: {e}")

asyncio.run(test_router_instantiation())
```

**Verify**: Services can instantiate router instances without errors

### Task 4: Method Compatibility Check

Verify router provides same methods as original adapter:

```python
import asyncio
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

async def verify_method_compatibility():
    router = CalendarIntegrationRouter()
    adapter = GoogleCalendarMCPAdapter()

    # Get methods from both
    router_methods = set(method for method in dir(router)
                        if not method.startswith('_') and callable(getattr(router, method)))
    adapter_methods = set(method for method in dir(adapter)
                         if not method.startswith('_') and callable(getattr(adapter, method)))

    print(f"Router methods: {len(router_methods)}")
    print(f"Adapter methods: {len(adapter_methods)}")

    # Check router has all adapter methods
    missing_in_router = adapter_methods - router_methods
    if missing_in_router:
        print(f"❌ Router missing adapter methods: {missing_in_router}")
    else:
        print("✅ Router has all adapter methods")

    # Check for unexpected router methods
    extra_in_router = router_methods - adapter_methods
    if extra_in_router:
        print(f"ℹ️ Additional router methods: {extra_in_router}")

    return len(missing_in_router) == 0

asyncio.run(verify_method_compatibility())
```

**Verify**: Router has all methods that original adapter provided

### Task 5: Git Verification

Check that changes are properly committed:

```bash
# Check git status
echo "=== Git Status ==="
git status

# Check recent commits for these services
echo "=== Recent commits affecting Calendar services ==="
git log --oneline -5 --grep="canonical_handlers\|morning_standup\|CalendarIntegrationRouter"

# Check actual changes made
echo "=== Changes in canonical_handlers.py ==="
git show HEAD~1:services/intent_service/canonical_handlers.py > /tmp/old_canonical.py 2>/dev/null || echo "No previous version found"
if [ -f /tmp/old_canonical.py ]; then
    diff -u /tmp/old_canonical.py services/intent_service/canonical_handlers.py | head -20
fi

echo "=== Changes in morning_standup.py ==="
git show HEAD~1:services/features/morning_standup.py > /tmp/old_standup.py 2>/dev/null || echo "No previous version found"
if [ -f /tmp/old_standup.py ]; then
    diff -u /tmp/old_standup.py services/features/morning_standup.py | head -20
fi
```

**Verify**: Changes are committed with appropriate messages

### Task 6: Integration Test

Test that router actually works through the service:

```python
import asyncio

async def integration_test():
    """Test that Calendar router works when accessed through migrated services"""

    # Test basic router functionality
    from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

    router = CalendarIntegrationRouter()
    print(f"Router initialized: {router is not None}")
    print(f"Router uses spatial: {router.use_spatial}")

    # Try a simple health check if available
    try:
        health = await router.health_check()
        print(f"✅ Router health_check works: {type(health)}")
    except Exception as e:
        print(f"ℹ️ Router health_check info: {e}")

    # Verify feature flag control
    integration, is_legacy = router._get_preferred_integration("test")
    print(f"Router delegation working: integration={integration is not None}, legacy={is_legacy}")

asyncio.run(integration_test())
```

**Verify**: Router functionality is accessible through services

## Cross-Validation Report Format

```markdown
# Phase 4A: Calendar Migration Cross-Validation Report

## Verification Summary
[APPROVED / ISSUES_FOUND / BLOCKING_PROBLEMS]

## Import Migration Verification
### canonical_handlers.py
- **Old import removed**: [YES/NO]
- **New import added**: [YES/NO]
- **Import works**: [YES/NO]

### morning_standup.py
- **Old import removed**: [YES/NO]
- **New import added**: [YES/NO]
- **Import works**: [YES/NO]

## Service Functionality
- **canonical_handlers imports**: [WORKS/FAILS]
- **morning_standup imports**: [WORKS/FAILS]
- **Router instantiation**: [WORKS/FAILS]

## Method Compatibility
- **Router has all adapter methods**: [YES/NO]
- **Missing methods**: [list or "none"]

## Git Verification
- **Changes committed**: [YES/NO]
- **Commit messages appropriate**: [YES/NO]
- **Git diff shows correct changes**: [YES/NO]

## Integration Testing
- **Router health check**: [WORKS/FAILS/N/A]
- **Feature flag control**: [WORKS/FAILS]
- **Router delegation**: [WORKS/FAILS]

## Issues Identified
### Blocking Issues
[Issues that prevent services from working]

### Non-Blocking Issues
[Minor issues that should be addressed]

## Readiness Assessment
[APPROVED_FOR_PHASE_4B / NEEDS_FIXES / BLOCKING_PROBLEMS]

### If Approved
Both Calendar services successfully migrated - ready for Notion migration

### If Needs Fixes
[Specific fixes required before proceeding]
```

## Update Requirements

After completing verification:

1. **Update Session Log**: Add Phase 4A verification completion
2. **Update GitHub Issue #199**: Add comment with Calendar migration verification results
3. **Tag Lead Developer**: Report approval or required fixes

## Critical Verification Standards

- **Import Replacement**: Must be complete with no direct adapter imports remaining
- **Functionality Preservation**: Services must work identically after migration
- **Router Compatibility**: Router must provide all methods services expect
- **Git Hygiene**: Changes must be properly committed with clear messages

## Questions to Answer

- Are both services completely migrated from direct imports?
- Do both services work the same way after migration?
- Does the router provide all methods the services need?
- Are the changes properly tracked in git?
- Are there any regressions or functionality breaks?

---

**Your Mission**: Verify Calendar service migration is complete and correct before proceeding to Notion services.

**Quality Standard**: Same rigor as previous router verifications - zero tolerance for functionality regressions.
