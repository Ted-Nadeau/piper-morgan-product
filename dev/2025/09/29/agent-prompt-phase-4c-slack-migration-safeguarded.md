# Claude Code Prompt: Phase 4C - Slack Service Migration with Proven Anti-80% Safeguards

## Mission: Migrate Slack Service After Router Completeness Verification

**Context**: Phase 4B successfully applied anti-80% pattern safeguards, achieving 100% router completeness verification before service migration. Phase 4C applies the same proven methodology to Slack's unique dual-component architecture.

**Objective**: Verify SlackIntegrationRouter is 100% complete, then migrate webhook_router.py from SlackSpatialAdapter + SlackClient to SlackIntegrationRouter.

## PROVEN SAFEGUARDS - MANDATORY APPLICATION

### Zero Authorization Clause
**YOU ARE EXPLICITLY PROHIBITED FROM:**
- Skipping any methods without architectural signoff
- Declaring "close enough" or "mostly complete"
- Rationalizing missing methods as "unused" or "optional"
- Proceeding with <100% router compatibility

**ONLY 100% MEANS 100%** - Proven effective in Phase 4B.

## Phase 4C Tasks

### Pre-Flight Task: Slack Router Completeness Verification

**MANDATORY FIRST STEP**: Verify SlackIntegrationRouter has ALL methods from both SlackSpatialAdapter and SlackClient.

```python
# Slack Router Completeness Check - MANDATORY FORMAT
import inspect
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.integrations.slack.slack_client import SlackClient

def enumerate_slack_methods():
    """
    Verify SlackIntegrationRouter has all methods from both components
    (SlackSpatialAdapter + SlackClient) since Slack uses dual-component architecture
    """

    router = SlackIntegrationRouter()
    spatial_adapter = SlackSpatialAdapter()
    slack_client = SlackClient()

    # Get all public methods from both source components
    spatial_methods = {name: getattr(spatial_adapter, name) for name in dir(spatial_adapter)
                      if not name.startswith('_') and callable(getattr(spatial_adapter, name))}

    client_methods = {name: getattr(slack_client, name) for name in dir(slack_client)
                     if not name.startswith('_') and callable(getattr(slack_client, name))}

    # Combine all expected methods (may have overlaps)
    all_expected = {}
    all_expected.update(spatial_methods)
    all_expected.update(client_methods)  # Client methods override if duplicated

    # Get router methods
    router_methods = {name: getattr(router, name) for name in dir(router)
                     if not name.startswith('_') and callable(getattr(router, name))}

    print("=== SLACK ROUTER COMPLETENESS VERIFICATION ===")
    print(f"SlackSpatialAdapter methods: {len(spatial_methods)}")
    print(f"SlackClient methods: {len(client_methods)}")
    print(f"Combined expected methods: {len(all_expected)}")
    print(f"Router methods: {len(router_methods)}")
    print("")

    # FORCED COMPARISON FORMAT - MANDATORY
    all_method_names = sorted(set(all_expected.keys()) | set(router_methods.keys()))

    print("Method Name                 | Expected | In Router | Status")
    print("-" * 65)

    missing_from_router = []

    for method_name in all_method_names:
        expected = method_name in all_expected
        in_router = method_name in router_methods

        if expected and not in_router:
            status = "❌ MISSING"
            missing_from_router.append(method_name)
        elif expected and in_router:
            status = "✅ PRESENT"
        elif not expected and in_router:
            status = "➕ ROUTER ONLY"
        else:
            status = "❓ UNKNOWN"

        print(f"{method_name:<27} | {str(expected):<8} | {str(in_router):<9} | {status}")

    print(f"\n=== OBJECTIVE COMPLETENESS METRICS ===")
    print(f"Expected Methods: {len(all_expected)}")
    print(f"Router Has Expected: {len([m for m in all_expected.keys() if m in router_methods])}")
    print(f"Missing From Router: {len(missing_from_router)}")

    expected_count = len(all_expected)
    present_count = len([m for m in all_expected.keys() if m in router_methods])
    completeness = (present_count/expected_count*100) if expected_count > 0 else 0

    print(f"Completeness: {present_count}/{expected_count} = {completeness:.1f}%")

    if missing_from_router:
        print(f"\n❌ ROUTER INCOMPLETE - MISSING METHODS:")
        for method in missing_from_router:
            source = "SlackClient" if method in client_methods else "SlackSpatialAdapter"
            print(f"  - {method} (from {source})")
        print(f"\n🛑 STOP: Cannot proceed with service migration until router is 100% complete")
        return False
    else:
        print(f"\n✅ ROUTER COMPLETE: 100% method compatibility achieved")
        return True

# EXECUTE VERIFICATION - MANDATORY
is_complete = enumerate_slack_methods()
assert is_complete, "Router must be 100% complete before proceeding"
```

**STOP CONDITION**: If router is not 100% complete, you MUST fix the router before migrating webhook_router.py. No exceptions.

### Service Migration Task (Only if router is 100% complete)

#### Service 1: webhook_router.py

**Location**: `services/integrations/slack/webhook_router.py`

**Pre-Migration Analysis**:
```bash
echo "=== Current Slack imports in webhook_router.py ==="
grep -n "SlackSpatialAdapter\|SlackClient\|spatial_adapter\|slack_client" services/integrations/slack/webhook_router.py

echo "=== Slack component usage patterns ==="
grep -A 10 -B 5 "SlackSpatialAdapter\|SlackClient" services/integrations/slack/webhook_router.py | head -30

echo "=== Import statements ==="
grep -n "^from.*slack" services/integrations/slack/webhook_router.py
```

**Expected Migration Pattern**:
```python
# OLD (dual imports):
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.integrations.slack.slack_client import SlackClient

# Initialize both components separately
self.spatial_adapter = SlackSpatialAdapter()
self.slack_client = SlackClient(config_service)

# NEW (single router):
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

# Router coordinates both components internally
self.slack_router = SlackIntegrationRouter(config_service)

# Access spatial functionality through router.get_spatial_adapter() if needed
# Access client functionality through router methods directly
```

**Critical Migration Considerations**:
- webhook_router.py may use BOTH SlackSpatialAdapter and SlackClient
- Router provides client methods directly, spatial adapter via get_spatial_adapter()
- Configuration service must be passed to router constructor
- Event handling logic must work with router's unified interface

**Migration Steps**:
```bash
# 1. Backup original
cp services/integrations/slack/webhook_router.py services/integrations/slack/webhook_router.py.backup

# 2. Update imports
# Replace dual imports with single router import

# 3. Update instantiation
# Replace separate adapter + client with unified router

# 4. Update method calls
# Direct client methods: slack_client.method() → slack_router.method()
# Spatial methods: spatial_adapter.method() → slack_router.get_spatial_adapter().method()

# 5. Verify changes
git diff services/integrations/slack/webhook_router.py
```

**Post-Migration Verification**:
```python
# Test webhook_router imports and works
python -c "
import sys
try:
    from services.integrations.slack.webhook_router import *
    print('✅ webhook_router imports successfully')
except Exception as e:
    print(f'❌ webhook_router import failed: {e}')
    sys.exit(1)
"

# Test router functionality through webhook_router
python -c "
import asyncio
from services.integrations.slack.webhook_router import *

async def test_router_integration():
    # Basic test that router is accessible through webhook_router
    print('✅ webhook_router integration test passed')

asyncio.run(test_router_integration())
"
```

**Commit Changes**:
```bash
git add services/integrations/slack/webhook_router.py
git commit -m "Phase 4C: Migrate webhook_router.py to SlackIntegrationRouter

- Replace SlackSpatialAdapter + SlackClient imports with SlackIntegrationRouter
- Router verified 100% compatible (X/X methods)
- Unified interface preserves all spatial + client functionality
- Event handling logic updated for router pattern
- Service tested and working"

git log --oneline -1
```

### Final Verification

**MANDATORY COMPLETION CHECK**:
```bash
# Verify no direct Slack component imports remain
echo "=== Checking for remaining direct imports ==="
grep -r "from.*spatial_adapter import\|from.*slack_client import\|SlackSpatialAdapter\|SlackClient" \
  services/integrations/slack/webhook_router.py \
  && echo "❌ Direct imports still found - MIGRATION INCOMPLETE" \
  || echo "✅ No direct imports found - MIGRATION COMPLETE"

# Test webhook_router imports successfully
python -c "
import sys
try:
    from services.integrations.slack import webhook_router
    print('✅ webhook_router imports successfully')
except Exception as e:
    print(f'❌ webhook_router import failed: {e}')
    sys.exit(1)
"
```

**Architecture Test**:
```python
# Verify router provides unified access to both client and spatial functionality
import asyncio
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

async def test_unified_access():
    """Test that router provides access to both client and spatial functionality"""

    router = SlackIntegrationRouter()

    print("=== UNIFIED ACCESS VERIFICATION ===")

    # Test client method access (direct)
    client_methods = ['send_message', 'get_channel_info', 'list_channels', 'test_auth']

    for method_name in client_methods:
        if hasattr(router, method_name):
            print(f"✅ Client method {method_name}: Available directly")
        else:
            print(f"❌ Client method {method_name}: Missing")

    # Test spatial adapter access (via get_spatial_adapter)
    spatial_adapter = router.get_spatial_adapter()
    if spatial_adapter:
        print(f"✅ Spatial adapter accessible: {type(spatial_adapter).__name__}")
    else:
        print(f"❌ Spatial adapter not accessible")

asyncio.run(test_unified_access())
```

## Evidence Requirements - MANDATORY FORMAT

```markdown
# Phase 4C: Slack Service Migration Report

## Pre-Flight Router Verification
**SlackIntegrationRouter Completeness**: [X/X methods (100%)]
**SlackSpatialAdapter Methods**: [X methods]
**SlackClient Methods**: [X methods]
**Combined Expected**: [X methods]
**Missing Methods**: [list or "NONE"]
**Router Status**: [COMPLETE/INCOMPLETE]

## Service Migrated: 1/1

### webhook_router.py
- **Import Changes**: [number of import replacements]
- **Instantiation Changes**: [number of object creation changes]
- **Method Call Updates**: [number of method call updates]
- **Migration**: SlackSpatialAdapter + SlackClient → SlackIntegrationRouter
- **Configuration**: Config service properly passed to router
- **Testing**: [import test results]
- **Commit**: [hash and message]

## Unified Access Verification
**Direct Client Methods**: [X/X available]
**Spatial Adapter Access**: [AVAILABLE/NOT_AVAILABLE]
**Event Handling**: [PRESERVED/BROKEN]

## Final Verification
**Service Imports**: [YES/NO]
**No Direct Imports Remain**: [YES/NO]
**Router Unified Access**: [WORKING/BROKEN]

## Objective Completion Metrics
**Router Methods**: X/X (100%)
**Services Completed**: 1/1
**Import Replacements**: X total locations
**Architecture Test**: PASSED/FAILED

## Ready for Phase 5 (Testing): [YES/NO]
```

## Update Requirements

1. **Update Session Log**: Add Phase 4C completion with objective metrics
2. **Update GitHub Issue #199**: Add comment with Slack migration evidence
3. **Tag Lead Developer**: Request checkbox approval with evidence links

## STOP CONDITIONS - DO NOT IGNORE

- Router is not 100% complete (missing any methods from spatial adapter or client)
- webhook_router.py fails to import after migration
- Event handling functionality breaks after router replacement
- Direct SlackSpatialAdapter or SlackClient imports remain

## Success Criteria - OBJECTIVE MEASURES

✅ Router completeness: X/X methods (100%)
✅ Service migrated: 1/1
✅ webhook_router imports successfully
✅ No direct component imports remain
✅ Unified access to client + spatial functionality preserved
✅ Changes committed with evidence

---

**Your Mission**: Apply proven anti-80% pattern safeguards to Slack's unique dual-component architecture migration.

**Quality Standard**: Same 100% completion standard that succeeded in Phase 4B, adapted for Slack's non-MCP pattern.
