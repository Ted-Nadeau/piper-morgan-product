# Agent Prompt: Phase 3B - Feature Flag Testing Verification (Cursor Agent)
*Cross-verification of Code agent's Phase 3A feature flag testing work*

## Mission: Verify Feature Flag Integration Quality

Code agent has implemented feature flag testing to verify spatial vs legacy integration switching. Your role is to independently verify that both modes work correctly and that feature flags actually control router behavior.

**Critical Standard**: Both spatial and legacy modes must function without errors - no partial functionality accepted for foundational infrastructure.

## Verification Framework

### 1. Feature Flag Discovery Verification
```bash
# Verify feature flag system exists and is discoverable
echo "=== Feature Flag System Discovery ==="

# Check for feature flag references
grep -r "USE_SPATIAL_GITHUB" . --include="*.py" --exclude-dir=__pycache__
grep -r "SPATIAL" config/ --include="*.md" --include="*.py" 2>/dev/null || echo "No config directory found"

# Check router's integration selection logic
grep -A 30 "_get_preferred_integration" services/integrations/github/github_integration_router.py

# Verify spatial and legacy integrations exist
ls -la services/integrations/spatial/github_spatial.py 2>/dev/null || echo "❌ Spatial integration missing"
ls -la services/integrations/github/github_agent.py 2>/dev/null || echo "❌ Legacy integration missing"
```

### 2. Router Integration Switching Verification
```python
# Independent test of router behavior with feature flags
import os
import sys

def verify_router_flag_switching():
    """Independently verify router responds to feature flags"""

    print("=== Independent Router Flag Verification ===")

    try:
        from services.integrations.github.github_integration_router import GitHubIntegrationRouter

        # Test spatial mode
        os.environ['USE_SPATIAL_GITHUB'] = 'true'
        router_spatial = GitHubIntegrationRouter()

        try:
            integration_spatial, is_legacy_spatial = router_spatial._get_preferred_integration("get_issue_by_url")
            print(f"Spatial Mode (USE_SPATIAL_GITHUB=true):")
            print(f"  Integration: {type(integration_spatial).__name__ if integration_spatial else 'None'}")
            print(f"  Is Legacy: {is_legacy_spatial}")

            if integration_spatial and not is_legacy_spatial:
                print("  ✅ Spatial mode correctly configured")
            else:
                print("  ❌ Spatial mode not working correctly")

        except Exception as e:
            print(f"  ❌ Spatial mode failed: {e}")

        # Test legacy mode
        os.environ['USE_SPATIAL_GITHUB'] = 'false'
        router_legacy = GitHubIntegrationRouter()

        try:
            integration_legacy, is_legacy_legacy = router_legacy._get_preferred_integration("get_issue_by_url")
            print(f"Legacy Mode (USE_SPATIAL_GITHUB=false):")
            print(f"  Integration: {type(integration_legacy).__name__ if integration_legacy else 'None'}")
            print(f"  Is Legacy: {is_legacy_legacy}")

            if integration_legacy and is_legacy_legacy:
                print("  ✅ Legacy mode correctly configured")
            else:
                print("  ❌ Legacy mode not working correctly")

        except Exception as e:
            print(f"  ❌ Legacy mode failed: {e}")

        # Test switching behavior
        if 'integration_spatial' in locals() and 'integration_legacy' in locals():
            if type(integration_spatial) != type(integration_legacy):
                print("  ✅ Feature flags control different integrations")
            else:
                print("  ❌ Feature flags don't change integration type")

    except ImportError as e:
        print(f"❌ Router import failed: {e}")

    except Exception as e:
        print(f"❌ Router verification failed: {e}")

verify_router_flag_switching()
```

### 3. Service Initialization Verification
```python
def verify_service_flag_compatibility():
    """Verify all services work with both feature flag modes"""

    services_to_test = [
        ("services.orchestration.engine", "OrchestrationEngine"),
        ("services.domain.github_domain_service", "GitHubDomainService"),
        ("services.domain.pm_number_manager", "PMNumberManager"),
        ("services.domain.standup_orchestration_service", "StandupOrchestrationService"),
        ("services.integrations.github.issue_analyzer", "IssueAnalyzer")
    ]

    spatial_results = []
    legacy_results = []

    for module_name, class_name in services_to_test:
        print(f"\n=== Verifying {class_name} Flag Compatibility ===")

        # Test spatial mode
        os.environ['USE_SPATIAL_GITHUB'] = 'true'
        try:
            module = __import__(module_name, fromlist=[class_name])
            service_class = getattr(module, class_name)
            service = service_class()
            print(f"  ✅ {class_name} initializes in spatial mode")
            spatial_results.append(True)
        except Exception as e:
            print(f"  ❌ {class_name} failed in spatial mode: {e}")
            spatial_results.append(False)

        # Test legacy mode
        os.environ['USE_SPATIAL_GITHUB'] = 'false'
        try:
            # Reimport to ensure fresh initialization
            if module_name in sys.modules:
                del sys.modules[module_name]
            module = __import__(module_name, fromlist=[class_name])
            service_class = getattr(module, class_name)
            service = service_class()
            print(f"  ✅ {class_name} initializes in legacy mode")
            legacy_results.append(True)
        except Exception as e:
            print(f"  ❌ {class_name} failed in legacy mode: {e}")
            legacy_results.append(False)

    print(f"\n=== Service Flag Compatibility Summary ===")
    print(f"Spatial mode success: {sum(spatial_results)}/5 services")
    print(f"Legacy mode success: {sum(legacy_results)}/5 services")

    if sum(spatial_results) == 5 and sum(legacy_results) == 5:
        print("✅ All services compatible with both flag modes")
        return True
    else:
        print("❌ Some services incompatible with flag modes")
        return False

verify_service_flag_compatibility()
```

### 4. Router Method Availability Verification
```python
def verify_router_method_availability():
    """Verify critical methods work in both flag modes"""

    critical_methods = [
        "get_issue_by_url",
        "get_open_issues",
        "get_recent_issues",
        "get_recent_activity",
        "list_repositories"
    ]

    spatial_method_results = []
    legacy_method_results = []

    for method_name in critical_methods:
        print(f"\n=== Verifying {method_name} Availability ===")

        # Spatial mode method check
        os.environ['USE_SPATIAL_GITHUB'] = 'true'
        try:
            from services.integrations.github.github_integration_router import GitHubIntegrationRouter
            router = GitHubIntegrationRouter()

            if hasattr(router, method_name):
                method = getattr(router, method_name)
                if callable(method):
                    print(f"  ✅ {method_name} available in spatial mode")
                    spatial_method_results.append(True)
                else:
                    print(f"  ❌ {method_name} not callable in spatial mode")
                    spatial_method_results.append(False)
            else:
                print(f"  ❌ {method_name} missing in spatial mode")
                spatial_method_results.append(False)

        except Exception as e:
            print(f"  ❌ {method_name} failed in spatial mode: {e}")
            spatial_method_results.append(False)

        # Legacy mode method check
        os.environ['USE_SPATIAL_GITHUB'] = 'false'
        try:
            # Fresh router instance for legacy mode
            router = GitHubIntegrationRouter()

            if hasattr(router, method_name):
                method = getattr(router, method_name)
                if callable(method):
                    print(f"  ✅ {method_name} available in legacy mode")
                    legacy_method_results.append(True)
                else:
                    print(f"  ❌ {method_name} not callable in legacy mode")
                    legacy_method_results.append(False)
            else:
                print(f"  ❌ {method_name} missing in legacy mode")
                legacy_method_results.append(False)

        except Exception as e:
            print(f"  ❌ {method_name} failed in legacy mode: {e}")
            legacy_method_results.append(False)

    print(f"\n=== Method Availability Summary ===")
    print(f"Spatial mode methods: {sum(spatial_method_results)}/5 available")
    print(f"Legacy mode methods: {sum(legacy_method_results)}/5 available")

    if sum(spatial_method_results) == 5 and sum(legacy_method_results) == 5:
        print("✅ All critical methods available in both modes")
        return True
    else:
        print("❌ Some methods unavailable in one or both modes")
        return False

verify_router_method_availability()
```

## Quality Assurance Checklist

### Feature Flag Functionality
- [ ] Feature flag system discovered and functional
- [ ] Router responds to USE_SPATIAL_GITHUB=true with spatial integration
- [ ] Router responds to USE_SPATIAL_GITHUB=false with legacy integration
- [ ] Feature flag switching changes integration behavior

### Service Compatibility
- [ ] All 5 services initialize successfully in spatial mode
- [ ] All 5 services initialize successfully in legacy mode
- [ ] No breaking changes when switching between modes
- [ ] Services maintain functionality in both modes

### Router Method Compatibility
- [ ] All critical methods available in spatial mode
- [ ] All critical methods available in legacy mode
- [ ] Method signatures consistent between modes
- [ ] No errors when calling methods in either mode

## Common Issues to Verify

### Feature Flag Implementation
- Feature flag environment variable not being read correctly
- Hardcoded integration selection ignoring flags
- Configuration not being applied during initialization

### Integration Availability
- Spatial integration not properly imported or configured
- Legacy integration not accessible or functioning
- Integration selection logic broken or inconsistent

### Service Compatibility
- Services failing to initialize with router in one mode
- Method calls failing with specific integration types
- Async/sync compatibility issues between modes

## Reporting Format

### Phase 3B Verification Results
```markdown
## Phase 3B Results: Feature Flag Testing Verification

### Feature Flag System
- Flag discovery: [FOUND/NOT_FOUND]
- Spatial mode switching: [WORKING/BROKEN]
- Legacy mode switching: [WORKING/BROKEN]
- Integration behavior change: [CONFIRMED/NOT_CONFIRMED]

### Service Compatibility
- Services in spatial mode: X/5 working
- Services in legacy mode: X/5 working
- Breaking changes detected: [NONE/IDENTIFIED]

### Router Method Availability
- Methods in spatial mode: X/5 available
- Methods in legacy mode: X/5 available
- Method compatibility: [FULL/PARTIAL/BROKEN]

### Quality Assessment
[READY_FOR_PHASE_4 / NEEDS_FIXES]

### Issues Requiring Resolution
[List any problems that must be fixed before Phase 4]
```

## Success Criteria (All Must Pass)

- [ ] Feature flag system functional and responsive
- [ ] Router correctly switches between spatial and legacy integrations
- [ ] All 5 services work in both spatial and legacy modes
- [ ] All 5 critical methods available in both modes
- [ ] No errors or crashes in either mode
- [ ] Evidence provided for all verification steps

## Critical Standards Reminder

**100% Functionality**: Both spatial and legacy modes must work completely. Partial functionality is not acceptable for foundational infrastructure.

**Evidence Required**: All verification must include test output. No "looks good" without evidence.

**Quality Gate**: This verification determines readiness for Phase 4 architectural lock. Only proceed if both modes work perfectly.

---

**Your Mission**: Independently verify the feature flag system works correctly and both spatial and legacy modes function without errors across all converted services.
