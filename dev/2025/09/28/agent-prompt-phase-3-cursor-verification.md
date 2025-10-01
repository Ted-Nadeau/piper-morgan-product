# Cursor Agent Prompt: Phase 3 - Slack Router Cross-Validation

## Mission: Verify Slack Router Implementation

**Context**: Code has implemented SlackIntegrationRouter with a fundamentally different pattern than Calendar/Notion - coordinating SlackSpatialAdapter + SlackClient instead of delegating to a single MCP adapter. This requires verification that pattern consistency is maintained despite architectural differences.

**Objective**: Verify Slack router follows established pattern while correctly adapting for Slack's non-MCP spatial architecture.

## Verification Tasks

### Task 1: Architectural Pattern Verification

Check that router correctly handles Slack's unique architecture:

```bash
# Compare with Calendar MCP pattern
echo "=== Calendar Pattern (MCP) ==="
grep -A 5 "self.spatial_calendar" services/integrations/calendar/calendar_integration_router.py | head -8

# Check Slack pattern adaptation
echo "=== Slack Pattern (Direct Spatial) ==="
grep -A 10 "self.spatial_slack\|self.slack_client" services/integrations/slack/slack_integration_router.py | head -15
```

**Verify**: Router correctly initializes both SlackSpatialAdapter and SlackClient for spatial mode

### Task 2: Pattern Consistency Check

Verify core pattern elements maintained despite architectural differences:

```bash
# Check delegation pattern
grep -A 15 "_get_preferred_integration" services/integrations/slack/slack_integration_router.py

# Check deprecation warning
grep -A 10 "_warn_deprecation_if_needed" services/integrations/slack/slack_integration_router.py

# Check feature flags
grep -A 3 "USE_SPATIAL_SLACK\|ALLOW_LEGACY_SLACK" services/integrations/slack/slack_integration_router.py
```

**Verify**: Core pattern elements present and following Calendar/Notion approach

### Task 3: SlackClient Method Verification

Check router exposes SlackClient methods:

```python
import asyncio
import inspect
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
from services.integrations.slack.slack_client import SlackClient

async def verify_methods():
    router = SlackIntegrationRouter()

    # Expected core methods from Phase 0
    expected_methods = ['send_message', 'get_channel_info', 'list_channels',
                       'get_user_info', 'list_users', 'get_conversation_history',
                       'get_thread_replies', 'add_reaction', 'test_auth']

    print(f"Checking {len(expected_methods)} expected methods...")

    missing = []
    for method_name in expected_methods:
        if not hasattr(router, method_name):
            missing.append(method_name)
            print(f"❌ Missing: {method_name}")
        else:
            router_method = getattr(router, method_name)
            is_async = inspect.iscoroutinefunction(router_method)
            print(f"✅ {method_name} (async: {is_async})")

    if missing:
        print(f"\n❌ Router missing {len(missing)} methods")
    else:
        print(f"\n✅ All {len(expected_methods)} methods present")

    return missing

asyncio.run(verify_methods())
```

**Verify**: All expected SlackClient methods present in router

### Task 4: Feature Flag Control Testing

```python
import asyncio
import os
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

async def test_feature_flags():
    # Test spatial mode
    os.environ['USE_SPATIAL_SLACK'] = 'true'
    os.environ['ALLOW_LEGACY_SLACK'] = 'false'

    router_spatial = SlackIntegrationRouter()
    client_spatial, is_legacy_spatial = router_spatial._get_preferred_integration('test')

    print("=== Spatial Mode ===")
    print(f"Client: {type(client_spatial).__name__ if client_spatial else 'None'}")
    print(f"Is legacy: {is_legacy_spatial}")
    print(f"Spatial adapter available: {router_spatial.spatial_slack is not None}")

    if client_spatial and not is_legacy_spatial:
        print("✅ Spatial mode works")
    else:
        print("❌ Spatial mode failed")

    # Test legacy mode
    os.environ['USE_SPATIAL_SLACK'] = 'false'
    os.environ['ALLOW_LEGACY_SLACK'] = 'true'

    router_legacy = SlackIntegrationRouter()
    client_legacy, is_legacy_legacy = router_legacy._get_preferred_integration('test')

    print("\n=== Legacy Mode ===")
    print(f"Client: {type(client_legacy).__name__ if client_legacy else 'None'}")
    print(f"Is legacy: {is_legacy_legacy}")

    if client_legacy and is_legacy_legacy:
        print("✅ Legacy mode works")
    else:
        print("❌ Legacy mode failed")

    # Test disabled mode (no integration)
    os.environ['USE_SPATIAL_SLACK'] = 'false'
    os.environ['ALLOW_LEGACY_SLACK'] = 'false'

    router_disabled = SlackIntegrationRouter()
    client_disabled, is_legacy_disabled = router_disabled._get_preferred_integration('test')

    print("\n=== Disabled Mode ===")
    print(f"Client: {type(client_disabled).__name__ if client_disabled else 'None'}")

    if client_disabled is None:
        print("✅ Disabled mode works")
    else:
        print("❌ Unexpected client present")

asyncio.run(test_feature_flags())
```

**Verify**: Feature flags control which integration is used

### Task 5: Spatial Adapter Access Verification

Check that spatial adapter is accessible when needed:

```python
import asyncio
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

async def verify_spatial_access():
    # Test spatial mode
    import os
    os.environ['USE_SPATIAL_SLACK'] = 'true'

    router = SlackIntegrationRouter()

    # Check spatial adapter accessible
    spatial_adapter = router.get_spatial_adapter()

    print("=== Spatial Adapter Access ===")
    print(f"Spatial adapter: {type(spatial_adapter).__name__ if spatial_adapter else 'None'}")

    if spatial_adapter:
        print("✅ Spatial adapter accessible")

        # Check it's the right type
        from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
        if isinstance(spatial_adapter, SlackSpatialAdapter):
            print("✅ Correct type (SlackSpatialAdapter)")
        else:
            print(f"⚠️ Unexpected type: {type(spatial_adapter)}")
    else:
        print("❌ Spatial adapter not accessible")

asyncio.run(verify_spatial_access())
```

**Verify**: Spatial adapter accessible for advanced spatial operations

### Task 6: Error Handling Verification

```python
import asyncio
import os
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

async def test_error_handling():
    # Test with no integration available
    os.environ['USE_SPATIAL_SLACK'] = 'false'
    os.environ['ALLOW_LEGACY_SLACK'] = 'false'

    router = SlackIntegrationRouter()

    # Test RuntimeError on method call
    try:
        await router.send_message("test", "test")
        print("❌ Should have raised RuntimeError")
    except RuntimeError as e:
        if "No Slack integration available" in str(e):
            print(f"✅ RuntimeError raised correctly")
        else:
            print(f"⚠️ RuntimeError message unexpected: {str(e)[:50]}")
    except Exception as e:
        print(f"❌ Wrong exception type: {type(e)}")

asyncio.run(test_error_handling())
```

**Verify**: Proper error handling when no integration available

## Cross-Validation Report Format

```markdown
# Phase 3: Slack Router Cross-Validation Report

## Verification Summary
[APPROVED / ISSUES_FOUND / BLOCKING_PROBLEMS]

## Architectural Adaptation Verification

### Pattern Differences from Calendar/Notion
**Calendar/Notion**: Single MCP adapter delegation
**Slack**: SlackSpatialAdapter + SlackClient coordination

### Adaptation Assessment
- [ ] Correctly initializes both spatial adapter and client
- [ ] Delegation logic adapted for dual-component pattern
- [ ] Spatial adapter accessible for advanced operations
- [ ] Client methods work through router

Issues: [none or list]

## Pattern Consistency Verification

### Core Pattern Elements
- [ ] _get_preferred_integration follows established logic
- [ ] _warn_deprecation_if_needed matches pattern
- [ ] RuntimeError handling consistent
- [ ] Feature flag checking same approach

Issues: [none or list]

## Method Completeness
**Expected Methods**: 9 (send_message, get_channel_info, list_channels, get_user_info, list_users, get_conversation_history, get_thread_replies, add_reaction, test_auth)
**Implemented**: [count]
**Missing**: [list or "none"]

## Feature Flag Control
**Spatial Mode**: [WORKS / FAILS]
**Legacy Mode**: [WORKS / FAILS]
**Disabled Mode**: [WORKS / FAILS]
Evidence: [test output]

## Spatial Adapter Access
**get_spatial_adapter()**: [WORKS / FAILS]
**Type Correct**: [YES / NO]
**Available in spatial mode**: [YES / NO]

## Error Handling
**RuntimeError when no integration**: [YES / NO]
**Error message quality**: [GOOD / NEEDS_IMPROVEMENT]

## Comparison with Calendar/Notion Routers

### Pattern Compliance
**Core pattern**: [MAINTAINED / BROKEN]
**Necessary adaptations**: [APPROPRIATE / INAPPROPRIATE]
**Quality**: [EQUIVALENT / BETTER / WORSE]

### Architectural Differences Summary
[List key differences and whether they're appropriate for Slack's architecture]

## Issues Identified

### Blocking
[Issues preventing router from working]

### Non-Blocking
[Minor issues or improvements]

## Readiness Assessment
[APPROVED_FOR_PHASE_4 / NEEDS_FIXES / BLOCKING_PROBLEMS]

### If Approved
All three routers complete - ready for service migration phase

### If Needs Fixes
[Specific fixes required]
```

## Update Requirements

1. **Update Session Log**: Add Phase 3 verification completion
2. **Update GitHub Issue #199**: Add Slack router verification results
3. **Tag Lead Developer**: Report approval or required fixes

## Critical Verification Standards

- **Pattern Consistency**: Core pattern must be maintained despite architectural differences
- **Architectural Appropriateness**: Adaptations must be necessary and correct for Slack's architecture
- **Functional Completeness**: All SlackClient methods must work through router
- **Spatial Intelligence**: Spatial adapter must be accessible when needed

---

**Your Mission**: Verify Slack router maintains pattern consistency while correctly adapting for non-MCP spatial architecture.

**Quality Standard**: Same rigor as Phases 1 and 2, with additional verification of architectural adaptation correctness.
