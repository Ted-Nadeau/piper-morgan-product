# Agent Prompt: Phase 0B - Test GitHubIntegrationRouter Operations

## Mission: Verify Router Actually Works for Required Operations
**Objective**: Test that GitHubIntegrationRouter can successfully execute operations used by bypassing services

## Context from Lead Developer
**Scope**: About to refactor 5+ services to use router instead of direct GitHubAgent imports
**Risk**: Router might have methods but they might not work properly
**Need**: Functional verification, not just method existence

## Testing Strategy

### Task 1: Create Router Test Script
```python
# Create test_router_operations.py
"""
Test GitHubIntegrationRouter operations used by bypassing services
"""

import sys
sys.path.append('.')

from services.integrations.github.github_integration_router import GitHubIntegrationRouter

def test_router_initialization():
    """Test router can be initialized"""
    try:
        router = GitHubIntegrationRouter()
        print("✅ Router initialized successfully")

        # Check what integrations were loaded
        print(f"Spatial available: {router.spatial_github is not None}")
        print(f"Legacy available: {router.legacy_github is not None}")
        print(f"Feature flags: spatial={router.use_spatial}, legacy={router.allow_legacy}")

        return router
    except Exception as e:
        print(f"❌ Router initialization failed: {e}")
        return None

def test_router_operations(router):
    """Test key operations that bypassing services use"""

    operations_to_test = [
        # Based on what we expect bypassing services to use
        'create_issue',
        'get_issue',
        'update_issue',
        'list_issues',
        'create_workflow_issue',
        # Add more based on Code agent findings
    ]

    for op in operations_to_test:
        if hasattr(router, op):
            print(f"✅ Router has {op} method")
            try:
                # Test method exists and is callable
                method = getattr(router, op)
                if callable(method):
                    print(f"   ✅ {op} is callable")
                else:
                    print(f"   ❌ {op} is not callable")
            except Exception as e:
                print(f"   ❌ Error accessing {op}: {e}")
        else:
            print(f"❌ Router missing {op} method")

def test_feature_flag_switching(router):
    """Test router responds to feature flag changes"""

    print("\nTesting feature flag behavior:")

    # Test current integration selection
    try:
        integration, is_legacy = router._get_preferred_integration("test_operation")
        print(f"Current preferred: {'Legacy' if is_legacy else 'Spatial'}")
        print(f"Integration instance: {type(integration).__name__ if integration else 'None'}")
    except Exception as e:
        print(f"❌ Error testing integration selection: {e}")

if __name__ == "__main__":
    print("Testing GitHubIntegrationRouter...")

    router = test_router_initialization()
    if router:
        test_router_operations(router)
        test_feature_flag_switching(router)

    print("\nRouter testing complete")
```

### Task 2: Test Router with Mock Operations
```python
# Create mock_router_test.py
"""
Test router with safe mock operations to verify it works
"""

def test_router_safe_operations():
    """Test router operations that don't make external API calls"""

    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    router = GitHubIntegrationRouter()

    # Test status/info methods that should be safe
    safe_methods = [
        'get_status',
        'get_integration_info',
        'get_feature_flags',
        # Add other safe methods
    ]

    for method_name in safe_methods:
        if hasattr(router, method_name):
            try:
                method = getattr(router, method_name)
                result = method()
                print(f"✅ {method_name}(): {result}")
            except Exception as e:
                print(f"❌ {method_name}() failed: {e}")
```

### Task 3: Cross-Reference with Bypassing Service Usage
```bash
# For each bypassing service, check what specific methods they call
echo "=== Methods used by bypassing services ==="

# orchestration/engine.py
echo "orchestration/engine.py:"
grep -n "\.create_issue\|\.get_issue\|\.update_issue\|\.list_" services/orchestration/engine.py

# domain/github_domain_service.py
echo "domain/github_domain_service.py:"
grep -n "\.create_issue\|\.get_issue\|\.update_issue\|\.list_" services/domain/github_domain_service.py

# Continue for other services...
```

### Task 4: Verify Router Pattern Understanding
```python
# Create router_pattern_analysis.py
"""
Understand how the router pattern works
"""

def analyze_router_pattern():
    """Analyze the router's internal structure"""

    # Read router source to understand patterns
    with open('services/integrations/github/github_integration_router.py', 'r') as f:
        content = f.read()

    # Look for key patterns
    patterns = {
        'feature_flag_usage': 'FeatureFlags',
        'spatial_integration': 'GitHubSpatialIntelligence',
        'legacy_integration': 'GitHubAgent',
        'routing_logic': '_get_preferred_integration',
        'method_delegation': 'def '
    }

    for pattern_name, pattern in patterns.items():
        if pattern in content:
            print(f"✅ Found {pattern_name}: {pattern}")
        else:
            print(f"❌ Missing {pattern_name}: {pattern}")
```

## Verification Checklist

### Router Functionality
- [ ] Router initializes successfully
- [ ] Both spatial and legacy integrations detected
- [ ] Feature flags working
- [ ] Key methods exist and are callable

### Operation Coverage
- [ ] Router supports all operations used by orchestration/engine.py
- [ ] Router supports all operations used by domain/github_domain_service.py
- [ ] Router supports all operations used by domain/pm_number_manager.py
- [ ] Router supports all operations used by domain/standup_orchestration_service.py
- [ ] Router supports all operations used by integrations/github/issue_analyzer.py

### Pattern Verification
- [ ] Router properly routes between spatial/legacy
- [ ] Feature flag control works
- [ ] Error handling for missing integrations

## Reporting Format

```markdown
# Phase 0B Results: Router Operation Testing

## Router Initialization
[SUCCESS/FAILURE with details]

## Operation Support
- Operations tested: X
- Operations working: Y
- Operations failing: Z
- Missing operations: [list]

## Service-Specific Verification
- orchestration/engine.py: [SUPPORTED/GAPS]
- domain/github_domain_service.py: [SUPPORTED/GAPS]
- [etc for each service]

## Pattern Analysis
- Feature flag control: [WORKING/BROKEN]
- Spatial/legacy routing: [WORKING/BROKEN]
- Error handling: [ADEQUATE/NEEDS_WORK]

## Readiness Assessment
[READY for Phase 1 / NEEDS COMPLETION / DIFFERENT APPROACH NEEDED]
```

## Success Criteria
- ✅ Router initializes and runs without errors
- ✅ All operations needed by bypassing services work
- ✅ Feature flag switching verified
- ✅ Confident router can replace direct imports

---

**Deploy after Code agent completes Phase 0A method comparison.**
