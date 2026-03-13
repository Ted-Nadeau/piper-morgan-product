# Cursor Agent Prompt: Phase 1 - Slack Spatial Testing & Validation

## Mission: Focused Slack Spatial System Testing

**Context**: Phase 0 confirmed 11 Slack spatial files (6 core + 5 tests) exist. Phase 1 requires focused testing to verify these spatial systems work correctly through SlackIntegrationRouter with proper feature flag control.

**Objective**: Test Slack spatial functionality through router interface, validate feature flag behavior, and create comprehensive test validation for spatial system operations.

## Phase 1 Testing Tasks

### Task 1: Router-Based Spatial Testing

Test Slack spatial system through the router interface:

```python
# Test Slack spatial functionality through router
def test_slack_spatial_through_router():
    """Test Slack spatial system via SlackIntegrationRouter"""

    print("=== SLACK SPATIAL ROUTER TESTING ===")

    import os

    # Test with spatial enabled
    os.environ['USE_SPATIAL_SLACK'] = 'true'

    try:
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

        # Instantiate router with spatial enabled
        slack_router = SlackIntegrationRouter()
        print("✅ SlackIntegrationRouter instantiated with USE_SPATIAL_SLACK=true")

        # Test spatial adapter access
        spatial_adapter = None
        if hasattr(slack_router, 'get_spatial_adapter'):
            spatial_adapter = slack_router.get_spatial_adapter()
            if spatial_adapter:
                print("✅ Spatial adapter accessible through router")
                print(f"  Adapter type: {type(spatial_adapter).__name__}")

                # Test adapter methods
                adapter_methods = [m for m in dir(spatial_adapter) if not m.startswith('_')]
                print(f"  Available methods: {len(adapter_methods)}")
                for method in adapter_methods[:5]:
                    print(f"    - {method}")

            else:
                print("⚠️ Spatial adapter returned None")
        else:
            print("❌ get_spatial_adapter method not available")

        # Test router methods that should delegate to spatial
        router_methods = [m for m in dir(slack_router) if not m.startswith('_') and callable(getattr(slack_router, m))]
        spatial_related = [m for m in router_methods if 'spatial' in m.lower()]

        print(f"\n🔧 Router spatial methods: {len(spatial_related)}")
        for method in spatial_related:
            print(f"  - {method}")

        # Test basic router functionality
        if hasattr(slack_router, 'health_check'):
            try:
                health = slack_router.health_check()
                print(f"✅ Router health check: {health}")
            except Exception as e:
                print(f"⚠️ Router health check error: {e}")

        return slack_router, spatial_adapter

    except Exception as e:
        print(f"❌ Router spatial testing failed: {e}")
        return None, None

router, adapter = test_slack_spatial_through_router()
```

### Task 2: Feature Flag Behavior Validation

Validate USE_SPATIAL_SLACK flag controls spatial behavior:

```python
# Test feature flag control behavior
def validate_spatial_flag_behavior():
    """Validate USE_SPATIAL_SLACK flag controls behavior"""

    print("\n=== SPATIAL FLAG BEHAVIOR VALIDATION ===")

    import os
    import importlib
    import sys

    results = {}

    # Test scenarios
    test_scenarios = [
        ('true', 'Spatial enabled'),
        ('false', 'Spatial disabled'),
        (None, 'Default behavior')
    ]

    for flag_value, description in test_scenarios:
        print(f"\n🔧 Testing: {description} (USE_SPATIAL_SLACK={flag_value})")

        # Set flag
        if flag_value is None:
            if 'USE_SPATIAL_SLACK' in os.environ:
                del os.environ['USE_SPATIAL_SLACK']
        else:
            os.environ['USE_SPATIAL_SLACK'] = flag_value

        try:
            # Clear module cache to ensure flag change takes effect
            modules_to_reload = [m for m in sys.modules.keys() if 'slack' in m and 'router' in m]
            for module in modules_to_reload:
                if module in sys.modules:
                    importlib.reload(sys.modules[module])

            # Test router behavior
            from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
            test_router = SlackIntegrationRouter()

            # Check spatial access
            spatial_available = False
            if hasattr(test_router, 'get_spatial_adapter'):
                spatial_adapter = test_router.get_spatial_adapter()
                spatial_available = spatial_adapter is not None

            print(f"  Spatial adapter available: {spatial_available}")

            # Check flag method if available
            if hasattr(test_router, '_should_use_spatial'):
                uses_spatial = test_router._should_use_spatial()
                print(f"  Uses spatial: {uses_spatial}")

            results[flag_value] = {
                'spatial_available': spatial_available,
                'router_created': True
            }

            print(f"  ✅ {description} test successful")

        except Exception as e:
            print(f"  ❌ {description} test failed: {e}")
            results[flag_value] = {'error': str(e)}

    # Summary
    print(f"\n📊 FLAG BEHAVIOR SUMMARY:")
    for flag_value, description in test_scenarios:
        result = results.get(flag_value, {})
        if 'error' in result:
            print(f"  {description}: ❌ {result['error']}")
        else:
            spatial = result.get('spatial_available', False)
            print(f"  {description}: ✅ Spatial={spatial}")

    return results

flag_results = validate_spatial_flag_behavior()
```

### Task 3: Spatial Test Execution

Run existing spatial tests and create additional validation:

```bash
# Execute spatial tests
echo "=== SLACK SPATIAL TEST EXECUTION ==="

# Find existing Slack spatial tests
echo "Finding existing Slack spatial tests..."
find tests/ -path "*slack*" -name "*spatial*" -type f | while read test_file; do
    echo "Found: $test_file"
done

# Check for organized test directories
if [ -d "tests/slack/spatial" ]; then
    echo "✅ Found organized spatial test directory"
    ls -la tests/slack/spatial/
elif [ -d "tests/integration" ]; then
    echo "✅ Found integration test directory"
    find tests/integration/ -name "*slack*" | head -3
else
    echo "⚠️ No organized test structure found"
fi

# Run spatial tests with flag enabled
echo ""
echo "=== RUNNING SPATIAL TESTS (ENABLED) ==="
export USE_SPATIAL_SLACK=true

# Try different test execution approaches
pytest tests/ -k "slack and spatial" -v --tb=short || echo "Method 1 failed"
pytest tests/ -k "SlackSpatial" -v --tb=short || echo "Method 2 failed"

# Run any found spatial test files directly
find tests/ -name "*slack*spatial*" -name "*.py" | while read test_file; do
    echo "Running: $test_file"
    pytest "$test_file" -v --tb=short || echo "Test file failed: $test_file"
done

# Test with spatial disabled
echo ""
echo "=== RUNNING TESTS (SPATIAL DISABLED) ==="
export USE_SPATIAL_SLACK=false

# Check if there are legacy tests
if [ -d "tests/slack/legacy" ]; then
    echo "Running legacy tests..."
    pytest tests/slack/legacy/ -v --tb=short
else
    echo "No dedicated legacy tests found"
fi
```

### Task 4: Integration Point Testing

Test integration points between spatial system and router:

```python
# Test integration points
def test_spatial_integration_points():
    """Test integration between spatial system and router"""

    print("\n=== SPATIAL INTEGRATION POINT TESTING ===")

    import os
    os.environ['USE_SPATIAL_SLACK'] = 'true'

    integration_tests = []

    try:
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
        router = SlackIntegrationRouter()

        # Test 1: Router -> Spatial Adapter
        print("🔧 Testing router to spatial adapter integration...")
        if hasattr(router, 'get_spatial_adapter'):
            adapter = router.get_spatial_adapter()
            if adapter:
                print("  ✅ Router successfully provides spatial adapter")
                integration_tests.append(('router_to_adapter', True))
            else:
                print("  ❌ Router spatial adapter is None")
                integration_tests.append(('router_to_adapter', False))
        else:
            print("  ❌ Router missing get_spatial_adapter method")
            integration_tests.append(('router_to_adapter', False))

        # Test 2: Method delegation
        print("\n🔧 Testing method delegation...")
        try:
            # Look for methods that should delegate to spatial
            delegation_methods = ['send_message', 'get_channels', 'process_event']
            for method_name in delegation_methods:
                if hasattr(router, method_name):
                    print(f"  ✅ Found delegatable method: {method_name}")
                    integration_tests.append((f'delegation_{method_name}', True))
                else:
                    print(f"  ⚠️ Method not found: {method_name}")
                    integration_tests.append((f'delegation_{method_name}', False))
        except Exception as e:
            print(f"  ❌ Method delegation test error: {e}")

        # Test 3: Configuration propagation
        print("\n🔧 Testing configuration propagation...")
        try:
            if hasattr(router, '_should_use_spatial'):
                uses_spatial = router._should_use_spatial()
                if uses_spatial:
                    print("  ✅ Configuration properly indicates spatial usage")
                    integration_tests.append(('config_propagation', True))
                else:
                    print("  ⚠️ Configuration indicates spatial not in use")
                    integration_tests.append(('config_propagation', False))
            else:
                print("  ⚠️ Cannot test configuration propagation")
                integration_tests.append(('config_propagation', None))
        except Exception as e:
            print(f"  ❌ Configuration test error: {e}")

    except Exception as e:
        print(f"❌ Integration testing failed: {e}")

    # Summary
    print(f"\n📊 INTEGRATION TEST SUMMARY:")
    for test_name, result in integration_tests:
        status = "✅ PASS" if result else "❌ FAIL" if result is not None else "⚠️ SKIP"
        print(f"  {test_name}: {status}")

    return integration_tests

integration_results = test_spatial_integration_points()
```

### Task 5: Cross-Validation with Code Agent

Prepare validation data for cross-checking with Code agent:

```python
# Cross-validation preparation
def prepare_cross_validation():
    """Prepare validation data for Code agent comparison"""

    print("\n=== CROSS-VALIDATION PREPARATION ===")

    validation_data = {
        'router_functionality': {},
        'spatial_access': {},
        'feature_flags': {},
        'test_results': {}
    }

    # Router functionality validation
    try:
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
        router = SlackIntegrationRouter()

        validation_data['router_functionality'] = {
            'instantiates': True,
            'type': type(router).__name__,
            'methods_count': len([m for m in dir(router) if not m.startswith('_')])
        }
    except Exception as e:
        validation_data['router_functionality'] = {'error': str(e)}

    # Spatial access validation
    import os
    os.environ['USE_SPATIAL_SLACK'] = 'true'

    try:
        router = SlackIntegrationRouter()
        if hasattr(router, 'get_spatial_adapter'):
            adapter = router.get_spatial_adapter()
            validation_data['spatial_access'] = {
                'method_exists': True,
                'adapter_available': adapter is not None,
                'adapter_type': type(adapter).__name__ if adapter else None
            }
        else:
            validation_data['spatial_access'] = {'method_exists': False}
    except Exception as e:
        validation_data['spatial_access'] = {'error': str(e)}

    # Feature flag validation summary
    validation_data['feature_flags'] = flag_results

    # Test results summary
    validation_data['test_results'] = {
        'integration_tests': integration_results,
        'total_tests_run': len(integration_results),
        'passed_tests': len([r for r in integration_results if r[1] is True])
    }

    print("📋 Validation data prepared for Code agent comparison:")
    for category, data in validation_data.items():
        print(f"  {category}: {len(data) if isinstance(data, dict) else 'N/A'} items")

    return validation_data

cross_validation_data = prepare_cross_validation()
```

## GitHub Evidence Update

```bash
# Update GitHub with focused testing results
gh issue comment 194 --body "## Phase 1: Cursor Slack Spatial Testing Complete

### Router Functionality Testing ✅
- SlackIntegrationRouter instantiation: [PASS/FAIL]
- Spatial adapter access: [AVAILABLE/UNAVAILABLE]
- Method delegation: [X methods tested]

### Feature Flag Validation ✅
- USE_SPATIAL_SLACK=true: [behavior confirmed]
- USE_SPATIAL_SLACK=false: [behavior confirmed]
- Default behavior: [behavior confirmed]
- Flag control: [WORKING/ISSUES]

### Test Execution ✅
- Existing spatial tests found: [X tests]
- Test execution results: [X passed / Y failed]
- Integration tests: [X passed / Y failed]

### Cross-Validation Ready ✅
- Router functionality data: [prepared]
- Spatial access data: [prepared]
- Feature flag data: [prepared]
- Test results data: [prepared]

**Status**: Slack spatial testing [COMPLETE/ISSUES_FOUND]
**Ready for Code comparison**: YES"
```

## Success Criteria

Phase 1 testing complete when:
- [✅] SlackIntegrationRouter spatial functionality tested
- [✅] USE_SPATIAL_SLACK flag behavior validated
- [✅] Existing spatial tests executed
- [✅] Integration points verified
- [✅] Cross-validation data prepared
- [✅] GitHub issue updated with test results

## STOP Conditions

Stop and escalate if:
- Router fundamentally broken
- Spatial system completely inaccessible
- Feature flags not working at all
- All tests failing consistently
- Cannot instantiate basic components

---

**Your Mission**: Validate Slack spatial system functionality through focused testing and prepare comprehensive comparison data.

**Quality Standard**: All spatial functionality tested with evidence - ready for Code agent cross-validation.
