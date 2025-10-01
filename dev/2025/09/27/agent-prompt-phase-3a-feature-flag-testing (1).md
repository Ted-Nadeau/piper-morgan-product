# Agent Prompt: Phase 3A - Feature Flag Testing Implementation (Code Agent)
*Following successful Phase 2A/2B: All services now use GitHubIntegrationRouter*

## Mission: Verify Spatial Intelligence Integration

Phase 2A/2B successfully converted all 5 services to use GitHubIntegrationRouter. You're now implementing comprehensive testing to verify that feature flags properly control spatial vs legacy GitHub integration modes.

**Strategic Goal**: Confirm the router correctly delegates to spatial intelligence when enabled, and falls back to legacy operations when disabled, across all converted services.

## GitHub Issue #193 Integration

**Update Progress**: After each testing phase, update GitHub issue with test results
**Evidence Collection**: Provide feature flag test output for both spatial and legacy modes
**PM Validation**: Request validation after comprehensive testing completion

## Feature Flag Testing Framework

### Current Feature Flag System
The system should use environment variables or configuration to control spatial vs legacy mode:
- `USE_SPATIAL_GITHUB=true` → Router uses spatial intelligence
- `USE_SPATIAL_GITHUB=false` → Router uses legacy GitHub operations

### Testing Approach
1. **Baseline Verification**: Confirm current flag configuration
2. **Spatial Mode Testing**: Test all services with spatial intelligence enabled
3. **Legacy Mode Testing**: Test all services with legacy mode enabled
4. **Switching Testing**: Verify behavior changes with flag changes
5. **Integration Testing**: Test actual GitHub operations in both modes

## Phase 3A Implementation Steps

### Step 1: Feature Flag Discovery
```bash
# Find current feature flag implementation
grep -r "USE_SPATIAL_GITHUB" . --include="*.py"
grep -r "spatial" config/ --include="*.md"
grep -r "SPATIAL" . --include="*.py"

# Check router's _get_preferred_integration method
grep -A 20 "_get_preferred_integration" services/integrations/github/github_integration_router.py
```

### Step 2: Test Environment Setup
```python
# Create test script for feature flag control
import os
import sys
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

def test_feature_flag_control():
    """Test router behavior with different feature flag settings"""

    print("=== Feature Flag Testing Framework ===")

    # Test spatial mode
    os.environ['USE_SPATIAL_GITHUB'] = 'true'
    router_spatial = GitHubIntegrationRouter()
    integration_spatial, is_legacy_spatial = router_spatial._get_preferred_integration("get_issue_by_url")

    print(f"Spatial Mode (USE_SPATIAL_GITHUB=true):")
    print(f"  Integration: {type(integration_spatial).__name__}")
    print(f"  Is Legacy: {is_legacy_spatial}")

    # Test legacy mode
    os.environ['USE_SPATIAL_GITHUB'] = 'false'
    router_legacy = GitHubIntegrationRouter()
    integration_legacy, is_legacy_legacy = router_legacy._get_preferred_integration("get_issue_by_url")

    print(f"Legacy Mode (USE_SPATIAL_GITHUB=false):")
    print(f"  Integration: {type(integration_legacy).__name__}")
    print(f"  Is Legacy: {is_legacy_legacy}")

    return integration_spatial, integration_legacy

test_feature_flag_control()
```

### Step 3: Service-Level Testing
Test each converted service with both spatial and legacy modes:

```python
def test_service_with_flags(service_module, service_class, test_method):
    """Test service behavior with different feature flags"""

    services_to_test = [
        ("services.orchestration.engine", "OrchestrationEngine", "some_github_method"),
        ("services.domain.github_domain_service", "GitHubDomainService", "some_method"),
        ("services.domain.pm_number_manager", "PMNumberManager", "some_method"),
        ("services.domain.standup_orchestration_service", "StandupOrchestrationService", "some_method"),
        ("services.integrations.github.issue_analyzer", "IssueAnalyzer", "some_method")
    ]

    for module_name, class_name, method_name in services_to_test:
        print(f"\n=== Testing {class_name} ===")

        # Test spatial mode
        os.environ['USE_SPATIAL_GITHUB'] = 'true'
        try:
            module = __import__(module_name, fromlist=[class_name])
            service = getattr(module, class_name)()
            print(f"✅ {class_name} initializes in spatial mode")
        except Exception as e:
            print(f"❌ {class_name} failed in spatial mode: {e}")

        # Test legacy mode
        os.environ['USE_SPATIAL_GITHUB'] = 'false'
        try:
            module = __import__(module_name, fromlist=[class_name])
            service = getattr(module, class_name)()
            print(f"✅ {class_name} initializes in legacy mode")
        except Exception as e:
            print(f"❌ {class_name} failed in legacy mode: {e}")

test_service_with_flags()
```

### Step 4: Router Method Testing
Test critical GitHub methods in both modes:

```python
def test_router_methods_both_modes():
    """Test router methods work in both spatial and legacy modes"""

    critical_methods = [
        "get_issue_by_url",
        "get_open_issues",
        "get_recent_issues",
        "get_recent_activity",
        "list_repositories"
    ]

    for method_name in critical_methods:
        print(f"\n=== Testing {method_name} ===")

        # Spatial mode test
        os.environ['USE_SPATIAL_GITHUB'] = 'true'
        try:
            router = GitHubIntegrationRouter()
            method = getattr(router, method_name)
            print(f"✅ {method_name} available in spatial mode")
        except Exception as e:
            print(f"❌ {method_name} failed in spatial mode: {e}")

        # Legacy mode test
        os.environ['USE_SPATIAL_GITHUB'] = 'false'
        try:
            router = GitHubIntegrationRouter()
            method = getattr(router, method_name)
            print(f"✅ {method_name} available in legacy mode")
        except Exception as e:
            print(f"❌ {method_name} failed in legacy mode: {e}")

test_router_methods_both_modes()
```

## Integration Testing Requirements

### Mock Testing (If GitHub API unavailable)
```python
def test_with_mocks():
    """Test router behavior with mocked GitHub responses"""

    # Mock successful responses for both spatial and legacy integrations
    # Verify different response patterns between spatial and legacy
    # Confirm feature flag controls which integration is called
    pass
```

### Live Testing (If GitHub API available)
```python
def test_with_live_api():
    """Test router with actual GitHub API calls"""

    # Use test repository or read-only operations
    # Verify spatial mode provides enhanced analysis
    # Verify legacy mode provides basic responses
    # Confirm no errors in either mode
    pass
```

## Evidence Collection Requirements

### For GitHub Issue #193 Updates
```bash
# Feature flag verification
echo "=== Feature Flag Testing Evidence ==="
echo "Spatial Mode Test:"
USE_SPATIAL_GITHUB=true python test_feature_flags.py

echo "Legacy Mode Test:"
USE_SPATIAL_GITHUB=false python test_feature_flags.py

echo "Service Initialization Test:"
python test_all_services_both_modes.py

echo "Router Method Availability Test:"
python test_router_methods_both_modes.py
```

## Quality Assurance Standards

### 100% Feature Flag Functionality
- Both spatial and legacy modes must work without errors
- All 5 services must initialize successfully in both modes
- All critical router methods must be available in both modes
- Feature flag changes must actually change integration behavior

### No Regression Testing
- Services must maintain existing functionality in legacy mode
- No breaking changes when switching between modes
- All method signatures must remain compatible
- Error handling must work consistently in both modes

## Success Criteria Checklist

- [ ] Feature flag system discovered and verified
- [ ] Router delegates to spatial integration when USE_SPATIAL_GITHUB=true
- [ ] Router delegates to legacy integration when USE_SPATIAL_GITHUB=false
- [ ] All 5 services initialize successfully in spatial mode
- [ ] All 5 services initialize successfully in legacy mode
- [ ] All critical methods work in both spatial and legacy modes
- [ ] Feature flag switching changes integration behavior
- [ ] No errors or crashes in either mode
- [ ] Evidence collected and documented

## Common Issues to Watch For

### Feature Flag Not Working
- Feature flag environment variable not being read
- Router hardcoded to one integration type
- Configuration not being applied correctly

### Integration Availability Issues
- Spatial integration not properly configured
- Legacy integration not accessible
- Import or initialization problems

### Method Compatibility Issues
- Methods missing from one integration but not the other
- Different method signatures between spatial and legacy
- Async/sync compatibility problems

## PM Validation Request Format

```markdown
@PM - Phase 3A complete and ready for validation:

**Feature Flag Testing**: Both spatial and legacy modes functional ✅
**Service Compatibility**: 5/5 services work in both modes ✅
**Router Methods**: All critical methods available in both modes ✅
**Integration Switching**: Feature flags control behavior correctly ✅

**Evidence**: [link to test outputs showing both modes working]
**Testing**: Comprehensive feature flag functionality verified

Request validation before proceeding to Phase 4 (architectural lock).
```

---

**Your Mission**: Verify the spatial intelligence feature flag system works correctly across all converted services. Ensure both spatial and legacy modes function without errors, proving the architectural migration is successful.
