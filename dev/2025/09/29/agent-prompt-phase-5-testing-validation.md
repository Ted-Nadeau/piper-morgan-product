# Claude Code Prompt: Phase 5 - Router Testing & Validation

## Mission: Comprehensive Testing of Router Infrastructure

**Context**: Phase 4 completed all service migrations with 100% router completeness. Phase 5 validates the infrastructure works correctly with feature flag control, completeness verification, and architectural protection before final documentation.

**Objective**: Systematically test all 3 routers (Calendar, Notion, Slack) with feature flags, verify completeness tests pass, and confirm architectural protection prevents future direct imports.

## Phase 5 Testing Tasks

### Task 1: Test All Routers with Feature Flags

Verify each router responds correctly to feature flag changes:

#### Calendar Router Feature Flag Testing

```python
# Test Calendar router feature flag control
import os
import asyncio
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

async def test_calendar_feature_flags():
    """Test Calendar router responds to USE_SPATIAL_CALENDAR flag"""

    print("=== CALENDAR ROUTER FEATURE FLAG TESTING ===")

    # Test spatial mode enabled (default)
    os.environ['USE_SPATIAL_CALENDAR'] = 'true'
    os.environ['ALLOW_LEGACY_CALENDAR'] = 'false'

    router_spatial = CalendarIntegrationRouter()
    integration, is_legacy = router_spatial._get_preferred_integration("test")

    print(f"Spatial mode: integration={integration is not None}, legacy={is_legacy}")

    if integration and not is_legacy:
        print("✅ Spatial mode: WORKING")

        # Test a method call
        try:
            health = await router_spatial.health_check()
            print(f"✅ Method delegation: health_check works")
        except Exception as e:
            print(f"⚠️ Method delegation: {e}")
    else:
        print("❌ Spatial mode: FAILED")

    # Test spatial disabled
    os.environ['USE_SPATIAL_CALENDAR'] = 'false'

    router_disabled = CalendarIntegrationRouter()
    integration_disabled, is_legacy_disabled = router_disabled._get_preferred_integration("test")

    print(f"Disabled mode: integration={integration_disabled is not None}")

    if integration_disabled is None:
        print("✅ Disabled mode: WORKING")
    else:
        print("❌ Disabled mode: FAILED")

    return True

asyncio.run(test_calendar_feature_flags())
```

#### Notion Router Feature Flag Testing

```python
# Test Notion router feature flag control
import os
import asyncio
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

async def test_notion_feature_flags():
    """Test Notion router responds to USE_SPATIAL_NOTION flag"""

    print("\n=== NOTION ROUTER FEATURE FLAG TESTING ===")

    # Test spatial mode enabled (default)
    os.environ['USE_SPATIAL_NOTION'] = 'true'
    os.environ['ALLOW_LEGACY_NOTION'] = 'false'

    router_spatial = NotionIntegrationRouter()
    integration, is_legacy = router_spatial._get_preferred_integration("test")

    print(f"Spatial mode: integration={integration is not None}, legacy={is_legacy}")

    if integration and not is_legacy:
        print("✅ Spatial mode: WORKING")

        # Test a method call
        try:
            configured = router_spatial.is_configured()
            print(f"✅ Method delegation: is_configured works ({configured})")
        except Exception as e:
            print(f"⚠️ Method delegation: {e}")
    else:
        print("❌ Spatial mode: FAILED")

    # Test spatial disabled
    os.environ['USE_SPATIAL_NOTION'] = 'false'

    router_disabled = NotionIntegrationRouter()
    integration_disabled, is_legacy_disabled = router_disabled._get_preferred_integration("test")

    print(f"Disabled mode: integration={integration_disabled is not None}")

    if integration_disabled is None:
        print("✅ Disabled mode: WORKING")
    else:
        print("❌ Disabled mode: FAILED")

    return True

asyncio.run(test_notion_feature_flags())
```

#### Slack Router Feature Flag Testing

```python
# Test Slack router feature flag control
import os
import asyncio
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

async def test_slack_feature_flags():
    """Test Slack router responds to USE_SPATIAL_SLACK flag"""

    print("\n=== SLACK ROUTER FEATURE FLAG TESTING ===")

    # Test spatial mode enabled (default)
    os.environ['USE_SPATIAL_SLACK'] = 'true'
    os.environ['ALLOW_LEGACY_SLACK'] = 'false'

    router_spatial = SlackIntegrationRouter()
    client, is_legacy = router_spatial._get_preferred_integration("test")

    print(f"Spatial mode: client={client is not None}, legacy={is_legacy}")

    if client and not is_legacy:
        print("✅ Spatial mode: WORKING")

        # Test spatial adapter access
        spatial_adapter = router_spatial.get_spatial_adapter()
        if spatial_adapter:
            print(f"✅ Spatial adapter access: {type(spatial_adapter).__name__}")
        else:
            print("❌ Spatial adapter access: FAILED")
    else:
        print("❌ Spatial mode: FAILED")

    # Test spatial disabled, legacy enabled
    os.environ['USE_SPATIAL_SLACK'] = 'false'
    os.environ['ALLOW_LEGACY_SLACK'] = 'true'

    router_legacy = SlackIntegrationRouter()
    client_legacy, is_legacy_legacy = router_legacy._get_preferred_integration("test")

    print(f"Legacy mode: client={client_legacy is not None}, legacy={is_legacy_legacy}")

    if client_legacy and is_legacy_legacy:
        print("✅ Legacy mode: WORKING")
    else:
        print("❌ Legacy mode: FAILED")

    return True

asyncio.run(test_slack_feature_flags())
```

### Task 2: Verify Completeness Tests Pass

Create and run completeness tests for each router:

#### Router Completeness Test Suite

```python
# Comprehensive completeness testing
import inspect
import asyncio

async def verify_router_completeness():
    """Verify all routers have complete method coverage"""

    print("\n=== ROUTER COMPLETENESS VERIFICATION ===")

    # Calendar completeness
    from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
    from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

    calendar_router = CalendarIntegrationRouter()
    calendar_adapter = GoogleCalendarMCPAdapter()

    calendar_router_methods = set(m for m in dir(calendar_router) if not m.startswith('_') and callable(getattr(calendar_router, m)))
    calendar_adapter_methods = set(m for m in dir(calendar_adapter) if not m.startswith('_') and callable(getattr(calendar_adapter, m)))

    calendar_missing = calendar_adapter_methods - calendar_router_methods
    calendar_completeness = len(calendar_adapter_methods & calendar_router_methods) / len(calendar_adapter_methods) * 100

    print(f"Calendar: {len(calendar_adapter_methods & calendar_router_methods)}/{len(calendar_adapter_methods)} = {calendar_completeness:.1f}%")
    if calendar_missing:
        print(f"  Missing: {calendar_missing}")
    else:
        print("  ✅ COMPLETE")

    # Notion completeness
    from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
    from services.integrations.mcp.notion_adapter import NotionMCPAdapter

    notion_router = NotionIntegrationRouter()
    notion_adapter = NotionMCPAdapter()

    notion_router_methods = set(m for m in dir(notion_router) if not m.startswith('_') and callable(getattr(notion_router, m)))
    notion_adapter_methods = set(m for m in dir(notion_adapter) if not m.startswith('_') and callable(getattr(notion_adapter, m)))

    notion_missing = notion_adapter_methods - notion_router_methods
    notion_completeness = len(notion_adapter_methods & notion_router_methods) / len(notion_adapter_methods) * 100

    print(f"Notion: {len(notion_adapter_methods & notion_router_methods)}/{len(notion_adapter_methods)} = {notion_completeness:.1f}%")
    if notion_missing:
        print(f"  Missing: {notion_missing}")
    else:
        print("  ✅ COMPLETE")

    # Slack completeness (dual-component)
    from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
    from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
    from services.integrations.slack.slack_client import SlackClient

    slack_router = SlackIntegrationRouter()
    slack_spatial = SlackSpatialAdapter()
    slack_client = SlackClient()

    slack_router_methods = set(m for m in dir(slack_router) if not m.startswith('_') and callable(getattr(slack_router, m)))
    slack_spatial_methods = set(m for m in dir(slack_spatial) if not m.startswith('_') and callable(getattr(slack_spatial, m)))
    slack_client_methods = set(m for m in dir(slack_client) if not m.startswith('_') and callable(getattr(slack_client, m)))

    slack_expected = slack_spatial_methods | slack_client_methods
    slack_missing = slack_expected - slack_router_methods
    slack_completeness = len(slack_expected & slack_router_methods) / len(slack_expected) * 100 if slack_expected else 0

    print(f"Slack: {len(slack_expected & slack_router_methods)}/{len(slack_expected)} = {slack_completeness:.1f}%")
    if slack_missing:
        print(f"  Missing: {slack_missing}")
    else:
        print("  ✅ COMPLETE")

    # Overall completeness
    total_expected = len(calendar_adapter_methods) + len(notion_adapter_methods) + len(slack_expected)
    total_present = (len(calendar_adapter_methods & calendar_router_methods) +
                    len(notion_adapter_methods & notion_router_methods) +
                    len(slack_expected & slack_router_methods))
    overall_completeness = total_present / total_expected * 100 if total_expected else 0

    print(f"\nOverall: {total_present}/{total_expected} = {overall_completeness:.1f}%")

    return overall_completeness == 100.0

asyncio.run(verify_router_completeness())
```

### Task 3: Confirm Architectural Protection

Verify no direct imports exist and create protection mechanisms:

#### Architecture Validation Test

```python
# Test that no direct imports remain in the codebase
import os
import glob
import re

def confirm_architectural_protection():
    """Verify no direct adapter imports remain and all services use routers"""

    print("\n=== ARCHITECTURAL PROTECTION VERIFICATION ===")

    # Define patterns to search for
    direct_import_patterns = [
        # Calendar direct imports
        r'from\s+services\.mcp\.consumer\.google_calendar_adapter\s+import',
        r'from\s+.*google_calendar_adapter\s+import',
        r'GoogleCalendarMCPAdapter',

        # Notion direct imports
        r'from\s+services\.integrations\.mcp\.notion_adapter\s+import',
        r'from\s+.*notion_adapter\s+import',
        r'NotionMCPAdapter',

        # Slack direct imports
        r'from\s+services\.integrations\.slack\.spatial_adapter\s+import',
        r'from\s+services\.integrations\.slack\.slack_client\s+import',
        r'SlackSpatialAdapter(?!Router)',  # Don't match SlackSpatialAdapterRouter
        r'SlackClient(?!Router)',          # Don't match SlackClientRouter
    ]

    # Files to check (migrated services)
    service_files = [
        'services/intent_service/canonical_handlers.py',
        'services/features/morning_standup.py',
        'services/domain/notion_domain_service.py',
        'services/publishing/publisher.py',
        'services/intelligence/spatial/notion_spatial.py',
        'services/integrations/slack/webhook_router.py'
    ]

    violations = []

    print("Checking migrated services for direct imports...")

    for file_path in service_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()

            for pattern in direct_import_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                if matches:
                    violations.append(f"{file_path}: {pattern} -> {matches}")

        else:
            print(f"⚠️ File not found: {file_path}")

    if violations:
        print("❌ ARCHITECTURAL VIOLATIONS FOUND:")
        for violation in violations:
            print(f"  {violation}")
        return False
    else:
        print("✅ NO DIRECT IMPORTS FOUND - Architecture protected")
        return True

architectural_clean = confirm_architectural_protection()
```

#### Router Import Verification

```python
# Verify all services use router imports
def verify_router_imports():
    """Verify all migrated services import routers correctly"""

    print("\n=== ROUTER IMPORT VERIFICATION ===")

    expected_imports = [
        # Calendar services should import CalendarIntegrationRouter
        ('services/intent_service/canonical_handlers.py', 'CalendarIntegrationRouter'),
        ('services/features/morning_standup.py', 'CalendarIntegrationRouter'),

        # Notion services should import NotionIntegrationRouter
        ('services/domain/notion_domain_service.py', 'NotionIntegrationRouter'),
        ('services/publishing/publisher.py', 'NotionIntegrationRouter'),
        ('services/intelligence/spatial/notion_spatial.py', 'NotionIntegrationRouter'),

        # Slack service should import SlackIntegrationRouter
        ('services/integrations/slack/webhook_router.py', 'SlackIntegrationRouter')
    ]

    missing_imports = []

    for file_path, expected_router in expected_imports:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()

            if expected_router not in content:
                missing_imports.append(f"{file_path}: Missing {expected_router}")
            else:
                print(f"✅ {file_path}: {expected_router} imported")
        else:
            missing_imports.append(f"{file_path}: File not found")

    if missing_imports:
        print("❌ MISSING ROUTER IMPORTS:")
        for missing in missing_imports:
            print(f"  {missing}")
        return False
    else:
        print("✅ ALL ROUTER IMPORTS PRESENT")
        return True

router_imports_correct = verify_router_imports()
```

## Evidence Requirements

Document test results:

```markdown
# Phase 5: Router Testing & Validation Report

## Feature Flag Testing Results

### Calendar Router
- Spatial mode (USE_SPATIAL_CALENDAR=true): [WORKING/FAILED]
- Disabled mode (USE_SPATIAL_CALENDAR=false): [WORKING/FAILED]
- Method delegation: [WORKING/FAILED]

### Notion Router
- Spatial mode (USE_SPATIAL_NOTION=true): [WORKING/FAILED]
- Disabled mode (USE_SPATIAL_NOTION=false): [WORKING/FAILED]
- Method delegation: [WORKING/FAILED]

### Slack Router
- Spatial mode (USE_SPATIAL_SLACK=true): [WORKING/FAILED]
- Legacy mode (USE_SPATIAL_SLACK=false, ALLOW_LEGACY_SLACK=true): [WORKING/FAILED]
- Spatial adapter access: [WORKING/FAILED]

## Completeness Test Results

### Router Completeness
- Calendar: [X/X methods (100%/Y%)]
- Notion: [X/X methods (100%/Y%)]
- Slack: [X/X methods (100%/Y%)]
- Overall: [X/X methods (100%/Y%)]

## Architectural Protection Results

### Direct Import Check
- Calendar services: [CLEAN/VIOLATIONS]
- Notion services: [CLEAN/VIOLATIONS]
- Slack services: [CLEAN/VIOLATIONS]
- Overall architecture: [PROTECTED/VIOLATED]

### Router Import Verification
- All services use routers: [YES/NO]
- Missing router imports: [NONE/LIST]

## Summary
- Feature flag control: [WORKING/FAILED]
- Completeness tests: [PASSED/FAILED]
- Architectural protection: [CONFIRMED/VIOLATED]

## Ready for Phase 6: [YES/NO]
```

## Update Requirements

1. **Update Session Log**: Add Phase 5 completion with test results
2. **Update GitHub Issue #199**: Add comment with testing evidence
3. **Tag Lead Developer**: Request checkbox approval with evidence

## Success Criteria

✅ All routers respond correctly to feature flags
✅ All completeness tests show 100% coverage
✅ No direct imports remain in migrated services
✅ All services import routers correctly
✅ Architectural protection confirmed

---

**Your Mission**: Systematically validate the router infrastructure works correctly and architecture is protected before final documentation phase.

**Quality Standard**: Comprehensive testing with objective evidence for all 3 testing checkboxes.
