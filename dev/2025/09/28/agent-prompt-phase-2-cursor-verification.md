# Cursor Agent Prompt: Phase 2 - Notion Router Cross-Validation

## Mission: Verify Notion Router Implementation

**Context**: Code has implemented NotionIntegrationRouter with 22+ methods (vs Calendar's 7). Your role is to verify pattern compliance, method completeness, and functional correctness before Phase 3.

**Objective**: Provide independent verification that Notion router follows Calendar pattern and delegates correctly to NotionMCPAdapter.

## Verification Tasks

### Task 1: Pattern Compliance Check

Compare with Calendar router pattern:

```bash
# Compare initialization patterns
echo "=== Calendar Router Init ==="
grep -A 15 "def __init__" services/integrations/calendar/calendar_integration_router.py | head -20

echo "=== Notion Router Init ==="
grep -A 15 "def __init__" services/integrations/notion/notion_integration_router.py | head -20

# Compare delegation patterns
echo "=== Calendar Delegation ==="
grep -A 10 "_get_preferred_integration" services/integrations/calendar/calendar_integration_router.py | head -15

echo "=== Notion Delegation ==="
grep -A 10 "_get_preferred_integration" services/integrations/notion/notion_integration_router.py | head -15
```

**Verify**: Notion follows Calendar pattern exactly

### Task 2: Method Completeness Verification

Check router has all NotionMCPAdapter methods:

```python
import asyncio
import inspect
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
from services.integrations.mcp.notion_adapter import NotionMCPAdapter

async def verify_completeness():
    router = NotionIntegrationRouter()
    adapter = NotionMCPAdapter()

    # Get all public methods from adapter
    adapter_methods = [m for m in dir(adapter)
                      if not m.startswith('_') and callable(getattr(adapter, m))]

    print(f"Adapter has {len(adapter_methods)} public methods")

    # Check router has each method
    missing = []
    for method_name in adapter_methods:
        if not hasattr(router, method_name):
            missing.append(method_name)

    if missing:
        print(f"❌ Router missing {len(missing)} methods:")
        for m in missing:
            print(f"  - {m}")
    else:
        print(f"✅ Router has all {len(adapter_methods)} adapter methods")

    return missing

asyncio.run(verify_completeness())
```

**Verify**: No missing methods

### Task 3: Method Signature Verification

Check async/sync patterns match:

```python
import asyncio
import inspect
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
from services.integrations.mcp.notion_adapter import NotionMCPAdapter

async def verify_signatures():
    router = NotionIntegrationRouter()
    adapter = NotionMCPAdapter()

    methods = ['connect', 'test_connection', 'is_configured', 'get_workspace_info',
               'list_users', 'get_user', 'fetch_databases', 'get_database',
               'query_database', 'get_page', 'create_page', 'search_notion',
               'get_mapping_stats', 'close']

    mismatches = []

    for method_name in methods:
        if not hasattr(router, method_name) or not hasattr(adapter, method_name):
            continue

        router_method = getattr(router, method_name)
        adapter_method = getattr(adapter, method_name)

        router_async = inspect.iscoroutinefunction(router_method)
        adapter_async = inspect.iscoroutinefunction(adapter_method)

        if router_async != adapter_async:
            mismatches.append(f"{method_name}: router={router_async}, adapter={adapter_async}")
        else:
            print(f"✅ {method_name} signature matches")

    if mismatches:
        print(f"\n❌ Signature mismatches:")
        for m in mismatches:
            print(f"  {m}")

    return mismatches

asyncio.run(verify_signatures())
```

**Verify**: All signatures match (async/sync)

### Task 4: Feature Flag Control Testing

```python
import asyncio
import os
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

async def test_feature_flags():
    # Test spatial mode
    os.environ['USE_SPATIAL_NOTION'] = 'true'
    router_spatial = NotionIntegrationRouter()
    integration_spatial, is_legacy_spatial = router_spatial._get_preferred_integration('test')

    print("=== Spatial Mode ===")
    print(f"Integration: {type(integration_spatial).__name__ if integration_spatial else 'None'}")
    print(f"Is legacy: {is_legacy_spatial}")

    if integration_spatial and not is_legacy_spatial:
        print("✅ Spatial mode works")
    else:
        print("❌ Spatial mode failed")

    # Test disabled mode
    os.environ['USE_SPATIAL_NOTION'] = 'false'
    router_disabled = NotionIntegrationRouter()
    integration_disabled, is_legacy_disabled = router_disabled._get_preferred_integration('test')

    print("\n=== Spatial Disabled ===")
    print(f"Integration: {type(integration_disabled).__name__ if integration_disabled else 'None'}")

    if integration_disabled is None:
        print("✅ Disabled mode works")
    else:
        print("❌ Unexpected integration present")

asyncio.run(test_feature_flags())
```

**Verify**: Feature flags control behavior

### Task 5: Delegation Testing

Test methods actually delegate:

```python
import asyncio
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

async def test_delegation():
    router = NotionIntegrationRouter()

    # Test synchronous method
    try:
        configured = router.is_configured()
        print(f"✅ is_configured delegates: {type(configured)}")
    except Exception as e:
        print(f"❌ is_configured failed: {e}")

    # Test get_mapping_stats
    try:
        stats = router.get_mapping_stats()
        print(f"✅ get_mapping_stats delegates: {type(stats)}")
    except Exception as e:
        print(f"❌ get_mapping_stats failed: {e}")

    # Test RuntimeError with no integration
    import os
    os.environ['USE_SPATIAL_NOTION'] = 'false'
    router_disabled = NotionIntegrationRouter()

    try:
        await router_disabled.connect()
        print("❌ Should have raised RuntimeError")
    except RuntimeError as e:
        if "No Notion integration available" in str(e):
            print(f"✅ RuntimeError raised correctly")
        else:
            print(f"⚠️ RuntimeError message unexpected: {str(e)[:50]}")
    except Exception as e:
        print(f"❌ Wrong exception: {type(e)}")

asyncio.run(test_delegation())
```

**Verify**: Delegation and error handling work

### Task 6: Configuration Preservation Check

```python
import asyncio
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

async def verify_config():
    router = NotionIntegrationRouter()

    # Verify NotionConfig is accessible through adapter
    if router.spatial_notion:
        has_config = hasattr(router.spatial_notion, 'config')
        print(f"Adapter has config: {has_config}")

        if has_config:
            print("✅ NotionConfig preserved through router")
        else:
            print("⚠️ Config pattern may differ")
    else:
        print("ℹ️ Spatial notion not initialized")

asyncio.run(verify_config())
```

**Verify**: NotionConfig works through router

## Cross-Validation Report Format

```markdown
# Phase 2: Notion Router Cross-Validation Report

## Verification Summary
[APPROVED / ISSUES_FOUND / BLOCKING_PROBLEMS]

## Pattern Compliance
- [ ] __init__ matches Calendar pattern
- [ ] _get_preferred_integration matches
- [ ] _warn_deprecation_if_needed matches
- [ ] RuntimeError pattern matches
Issues: [none or list]

## Method Completeness
**Adapter Methods**: [count]
**Router Methods**: [count]
**Missing**: [list or "none"]

## Signature Verification
**Methods Checked**: [count]
**Mismatches**: [list or "none"]
[List any async/sync mismatches]

## Feature Flag Control
**Spatial Mode**: [WORKS / FAILS]
**Disabled Mode**: [WORKS / FAILS]
Evidence: [test output]

## Delegation Testing
**Synchronous Methods**: [WORK / FAIL]
**Asynchronous Methods**: [WORK / FAIL]
**RuntimeError Handling**: [CORRECT / INCORRECT]

## Configuration Preservation
**NotionConfig**: [ACCESSIBLE / NOT_ACCESSIBLE]

## Issues Identified
### Blocking
[Issues preventing router from working]

### Non-Blocking
[Minor issues]

## Comparison with Calendar Router
**Pattern Compliance**: [EXACT / DEVIATIONS]
**Method Count**: Calendar=7, Notion=[X]
**Quality**: [EQUIVALENT / BETTER / WORSE]

## Readiness Assessment
[APPROVED_FOR_PHASE_3 / NEEDS_FIXES / BLOCKING_PROBLEMS]
```

## Update Requirements

1. **Update Session Log**: Add Phase 2 verification completion
2. **Update GitHub Issue #199**: Add comment with verification results
3. **Tag Lead Developer**: Report approval or required fixes

## Critical Verification Standards

- **Pattern Consistency**: Must match Calendar router pattern
- **Method Completeness**: All adapter methods must be in router
- **Signature Matching**: Async/sync patterns must match adapter
- **Functional Testing**: Actually execute methods to verify delegation

---

**Your Mission**: Verify Notion router is complete, correct, and pattern-compliant before Phase 3 Slack router.

**Quality Standard**: Same thoroughness as Phase 1 verification - zero defects accepted.
