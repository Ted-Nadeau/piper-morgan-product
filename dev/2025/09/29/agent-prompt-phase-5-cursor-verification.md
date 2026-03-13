# Cursor Agent Prompt: Phase 5 - Testing & Validation Verification

## Mission: Verify Comprehensive Router Testing and Validation

**Context**: Phase 5 tests the complete router infrastructure built in Phases 1-4. Code agent is running systematic tests on all 3 routers with feature flags, completeness verification, and architectural protection. Your role is to independently verify these tests are thorough and results are accurate.

**Objective**: Cross-validate feature flag testing, completeness verification, and architectural protection to ensure the router infrastructure is production-ready.

## Testing Areas to Verify

### Area 1: Feature Flag Testing
**Expected**: All 3 routers (Calendar, Notion, Slack) respond correctly to feature flag changes

### Area 2: Completeness Testing
**Expected**: All routers maintain 100% method compatibility with their source adapters

### Area 3: Architectural Protection
**Expected**: No direct imports remain, all services use routers correctly

## Verification Tasks

### Task 1: Feature Flag Cross-Validation

Independently verify feature flag control across all routers:

```python
import os
import asyncio

async def cross_validate_feature_flags():
    """Independent verification of router feature flag behavior"""

    print("=== FEATURE FLAG CROSS-VALIDATION ===")

    # Calendar Router Verification
    from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

    print("\n--- Calendar Router ---")

    # Test spatial enabled
    os.environ['USE_SPATIAL_CALENDAR'] = 'true'
    calendar_router = CalendarIntegrationRouter()
    cal_integration, cal_is_legacy = calendar_router._get_preferred_integration("test")

    spatial_working = cal_integration is not None and not cal_is_legacy
    print(f"Spatial enabled: {spatial_working}")

    # Test spatial disabled
    os.environ['USE_SPATIAL_CALENDAR'] = 'false'
    calendar_router_off = CalendarIntegrationRouter()
    cal_integration_off, cal_is_legacy_off = calendar_router_off._get_preferred_integration("test")

    disabled_working = cal_integration_off is None
    print(f"Spatial disabled: {disabled_working}")

    # Notion Router Verification
    from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

    print("\n--- Notion Router ---")

    # Test spatial enabled
    os.environ['USE_SPATIAL_NOTION'] = 'true'
    notion_router = NotionIntegrationRouter()
    notion_integration, notion_is_legacy = notion_router._get_preferred_integration("test")

    notion_spatial_working = notion_integration is not None and not notion_is_legacy
    print(f"Spatial enabled: {notion_spatial_working}")

    # Test spatial disabled
    os.environ['USE_SPATIAL_NOTION'] = 'false'
    notion_router_off = NotionIntegrationRouter()
    notion_integration_off, notion_is_legacy_off = notion_router_off._get_preferred_integration("test")

    notion_disabled_working = notion_integration_off is None
    print(f"Spatial disabled: {notion_disabled_working}")

    # Slack Router Verification
    from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

    print("\n--- Slack Router ---")

    # Test spatial enabled
    os.environ['USE_SPATIAL_SLACK'] = 'true'
    os.environ['ALLOW_LEGACY_SLACK'] = 'false'
    slack_router = SlackIntegrationRouter()
    slack_client, slack_is_legacy = slack_router._get_preferred_integration("test")

    slack_spatial_working = slack_client is not None and not slack_is_legacy
    print(f"Spatial enabled: {slack_spatial_working}")

    # Test legacy enabled
    os.environ['USE_SPATIAL_SLACK'] = 'false'
    os.environ['ALLOW_LEGACY_SLACK'] = 'true'
    slack_router_legacy = SlackIntegrationRouter()
    slack_client_legacy, slack_is_legacy_legacy = slack_router_legacy._get_preferred_integration("test")

    slack_legacy_working = slack_client_legacy is not None and slack_is_legacy_legacy
    print(f"Legacy enabled: {slack_legacy_working}")

    # Summary
    all_flags_working = (spatial_working and disabled_working and
                        notion_spatial_working and notion_disabled_working and
                        slack_spatial_working and slack_legacy_working)

    print(f"\n=== FEATURE FLAG SUMMARY ===")
    print(f"All feature flags working: {all_flags_working}")

    return all_flags_working

asyncio.run(cross_validate_feature_flags())
```

**Verify**: All routers respond correctly to feature flag changes

### Task 2: Completeness Cross-Validation

Independently verify method completeness claims:

```python
import inspect

def cross_validate_completeness():
    """Independent verification of router method completeness"""

    print("\n=== COMPLETENESS CROSS-VALIDATION ===")

    results = {}

    # Calendar Completeness Check
    from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
    from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

    calendar_router = CalendarIntegrationRouter()
    calendar_adapter = GoogleCalendarMCPAdapter()

    cal_router_methods = {name for name in dir(calendar_router)
                         if not name.startswith('_') and callable(getattr(calendar_router, name))}
    cal_adapter_methods = {name for name in dir(calendar_adapter)
                          if not name.startswith('_') and callable(getattr(calendar_adapter, name))}

    cal_missing = cal_adapter_methods - cal_router_methods
    cal_completeness = len(cal_adapter_methods & cal_router_methods) / len(cal_adapter_methods) * 100

    print(f"Calendar: {len(cal_adapter_methods & cal_router_methods)}/{len(cal_adapter_methods)} = {cal_completeness:.1f}%")
    if cal_missing:
        print(f"  Missing: {sorted(cal_missing)}")
    results['calendar'] = cal_completeness == 100.0

    # Notion Completeness Check
    from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
    from services.integrations.mcp.notion_adapter import NotionMCPAdapter

    notion_router = NotionIntegrationRouter()
    notion_adapter = NotionMCPAdapter()

    notion_router_methods = {name for name in dir(notion_router)
                            if not name.startswith('_') and callable(getattr(notion_router, name))}
    notion_adapter_methods = {name for name in dir(notion_adapter)
                             if not name.startswith('_') and callable(getattr(notion_adapter, name))}

    notion_missing = notion_adapter_methods - notion_router_methods
    notion_completeness = len(notion_adapter_methods & notion_router_methods) / len(notion_adapter_methods) * 100

    print(f"Notion: {len(notion_adapter_methods & notion_router_methods)}/{len(notion_adapter_methods)} = {notion_completeness:.1f}%")
    if notion_missing:
        print(f"  Missing: {sorted(notion_missing)}")
    results['notion'] = notion_completeness == 100.0

    # Slack Completeness Check (dual-component)
    from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
    from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
    from services.integrations.slack.slack_client import SlackClient

    slack_router = SlackIntegrationRouter()
    slack_spatial = SlackSpatialAdapter()
    slack_client = SlackClient()

    slack_router_methods = {name for name in dir(slack_router)
                           if not name.startswith('_') and callable(getattr(slack_router, name))}
    slack_spatial_methods = {name for name in dir(slack_spatial)
                            if not name.startswith('_') and callable(getattr(slack_spatial, name))}
    slack_client_methods = {name for name in dir(slack_client)
                           if not name.startswith('_') and callable(getattr(slack_client, name))}

    slack_expected = slack_spatial_methods | slack_client_methods
    slack_missing = slack_expected - slack_router_methods
    slack_completeness = len(slack_expected & slack_router_methods) / len(slack_expected) * 100 if slack_expected else 100

    print(f"Slack: {len(slack_expected & slack_router_methods)}/{len(slack_expected)} = {slack_completeness:.1f}%")
    if slack_missing:
        print(f"  Missing: {sorted(slack_missing)}")
    results['slack'] = slack_completeness == 100.0

    # Overall Assessment
    all_complete = all(results.values())
    print(f"\n=== COMPLETENESS SUMMARY ===")
    print(f"All routers complete: {all_complete}")
    for router, complete in results.items():
        print(f"  {router.capitalize()}: {'✅' if complete else '❌'}")

    return all_complete

cross_validate_completeness()
```

**Verify**: All routers maintain 100% method compatibility

### Task 3: Architectural Protection Cross-Validation

Independently verify architectural cleanliness:

```bash
# Independent architectural protection verification
echo "=== ARCHITECTURAL PROTECTION CROSS-VALIDATION ==="

# Check for direct imports in migrated services
echo "Checking for direct adapter imports..."

# Calendar direct imports
calendar_violations=$(grep -r "GoogleCalendarMCPAdapter\|from.*google_calendar_adapter" \
  services/intent_service/canonical_handlers.py \
  services/features/morning_standup.py 2>/dev/null | wc -l)

echo "Calendar direct imports found: $calendar_violations"

# Notion direct imports
notion_violations=$(grep -r "NotionMCPAdapter\|from.*notion_adapter.*import" \
  services/domain/notion_domain_service.py \
  services/publishing/publisher.py \
  services/intelligence/spatial/notion_spatial.py 2>/dev/null | wc -l)

echo "Notion direct imports found: $notion_violations"

# Slack direct imports
slack_violations=$(grep -r "SlackSpatialAdapter\|SlackClient\|from.*spatial_adapter.*import\|from.*slack_client.*import" \
  services/integrations/slack/webhook_router.py 2>/dev/null | \
  grep -v "SlackIntegrationRouter" | wc -l)

echo "Slack direct imports found: $slack_violations"

total_violations=$((calendar_violations + notion_violations + slack_violations))
echo "Total direct import violations: $total_violations"

if [ $total_violations -eq 0 ]; then
    echo "✅ ARCHITECTURAL PROTECTION CONFIRMED"
else
    echo "❌ ARCHITECTURAL VIOLATIONS DETECTED"
fi
```

```python
# Cross-validate router imports are present
import os

def cross_validate_router_imports():
    """Verify all services import their respective routers"""

    print("\n=== ROUTER IMPORT CROSS-VALIDATION ===")

    service_router_map = [
        ('services/intent_service/canonical_handlers.py', 'CalendarIntegrationRouter'),
        ('services/features/morning_standup.py', 'CalendarIntegrationRouter'),
        ('services/domain/notion_domain_service.py', 'NotionIntegrationRouter'),
        ('services/publishing/publisher.py', 'NotionIntegrationRouter'),
        ('services/intelligence/spatial/notion_spatial.py', 'NotionIntegrationRouter'),
        ('services/integrations/slack/webhook_router.py', 'SlackIntegrationRouter')
    ]

    all_correct = True

    for service_path, expected_router in service_router_map:
        if os.path.exists(service_path):
            with open(service_path, 'r') as f:
                content = f.read()

            if expected_router in content:
                print(f"✅ {service_path}: {expected_router} imported")
            else:
                print(f"❌ {service_path}: {expected_router} NOT imported")
                all_correct = False
        else:
            print(f"❌ {service_path}: File not found")
            all_correct = False

    print(f"\nAll router imports correct: {all_correct}")
    return all_correct

cross_validate_router_imports()
```

**Verify**: Architecture is clean and protected

### Task 4: Integration Testing

Test that routers actually work through services:

```python
import asyncio

async def integration_testing():
    """Test that services can actually use routers successfully"""

    print("\n=== INTEGRATION TESTING ===")

    # Test Calendar router through service
    try:
        from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
        calendar_router = CalendarIntegrationRouter()

        # Basic functionality test
        health = await calendar_router.health_check()
        print(f"✅ Calendar router integration: health_check works")

    except Exception as e:
        print(f"❌ Calendar router integration: {e}")

    # Test Notion router through service
    try:
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
        notion_router = NotionIntegrationRouter()

        # Basic functionality test
        configured = notion_router.is_configured()
        print(f"✅ Notion router integration: is_configured works ({configured})")

    except Exception as e:
        print(f"❌ Notion router integration: {e}")

    # Test Slack router through service
    try:
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
        slack_router = SlackIntegrationRouter()

        # Basic functionality test
        spatial_adapter = slack_router.get_spatial_adapter()
        if spatial_adapter:
            print(f"✅ Slack router integration: spatial adapter accessible")
        else:
            print(f"⚠️ Slack router integration: spatial adapter not available (may be expected)")

    except Exception as e:
        print(f"❌ Slack router integration: {e}")

asyncio.run(integration_testing())
```

**Verify**: Routers work correctly in integration scenarios

## Cross-Validation Report Format

```markdown
# Phase 5: Testing & Validation Cross-Validation Report

## Verification Summary
[APPROVED / ISSUES_FOUND / BLOCKING_PROBLEMS]

## Feature Flag Testing Verification
### Calendar Router
- Spatial mode control: [VERIFIED/FAILED]
- Disabled mode control: [VERIFIED/FAILED]

### Notion Router
- Spatial mode control: [VERIFIED/FAILED]
- Disabled mode control: [VERIFIED/FAILED]

### Slack Router
- Spatial mode control: [VERIFIED/FAILED]
- Legacy mode control: [VERIFIED/FAILED]

**Overall Feature Flags**: [ALL WORKING/X FAILED]

## Completeness Testing Verification
### Method Coverage
- Calendar: [X/X = 100% or Y%]
- Notion: [X/X = 100% or Y%]
- Slack: [X/X = 100% or Y%]

**Overall Completeness**: [100%/Y%]

## Architectural Protection Verification
### Direct Import Check
- Calendar violations: [0/X found]
- Notion violations: [0/X found]
- Slack violations: [0/X found]
- **Total violations**: [0/X]

### Router Import Check
- All services use routers: [YES/NO]
- Missing imports: [NONE/LIST]

## Integration Testing
- Calendar router integration: [WORKS/FAILS]
- Notion router integration: [WORKS/FAILS]
- Slack router integration: [WORKS/FAILS]

## Issues Identified
### Blocking Issues
[Critical issues preventing Phase 6]

### Non-Blocking Issues
[Minor issues for future improvement]

## Testing Quality Assessment
**Test Coverage**: [COMPREHENSIVE/INSUFFICIENT]
**Evidence Quality**: [STRONG/WEAK]
**Results Accuracy**: [VERIFIED/QUESTIONABLE]

## Readiness Assessment
[APPROVED_FOR_PHASE_6 / NEEDS_FIXES / BLOCKING_PROBLEMS]

### Phase 5 Checkboxes Status
- [ ] Test all routers with feature flags: [COMPLETE/INCOMPLETE]
- [ ] Verify completeness tests pass: [COMPLETE/INCOMPLETE]
- [ ] Confirm architectural protection: [COMPLETE/INCOMPLETE]
```

## Update Requirements

1. **Update Session Log**: Add Phase 5 verification completion
2. **Update GitHub Issue #199**: Add comment with testing verification
3. **Tag Lead Developer**: Report Phase 5 approval status

## Critical Verification Standards

- **Feature Flag Control**: All routers must respond correctly to configuration changes
- **Method Completeness**: All routers must maintain 100% compatibility with source adapters
- **Architectural Protection**: Zero direct imports allowed, all services must use routers
- **Integration Functionality**: Routers must work correctly in real usage scenarios

---

**Your Mission**: Independently verify the router infrastructure testing is comprehensive and accurate before Phase 6 documentation.

**Quality Standard**: Same rigorous verification standards applied throughout CORE-QUERY-1.
