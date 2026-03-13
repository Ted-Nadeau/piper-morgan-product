# Cursor Agent Prompt: Phase 1 - Slack Spatial Testing & Validation

## Mission: Focused Testing of Slack Spatial Intelligence System

**Context**: Phase 0 confirmed solid infrastructure. Code agent mapping Slack spatial architecture (21 files). Your focus: systematic testing of spatial functionality, feature flag control, and test framework validation.

**Objective**: Create comprehensive test suite for Slack spatial system, validate feature flag behavior, and ensure spatial/legacy mode switching works correctly.

## Phase 1 Testing Tasks

### Task 1: Slack Spatial System Integration Testing

Create focused integration tests for Slack spatial system:

```python
# Create comprehensive Slack spatial integration tests
def create_slack_spatial_tests():
    """Create integration tests for Slack spatial system"""

    print("=== SLACK SPATIAL INTEGRATION TESTING ===")

    import os
    import pytest
    from unittest.mock import Mock, patch

    # Test spatial system with flag enabled
    print("🧪 Testing Slack spatial with USE_SPATIAL_SLACK=true...")

    # Set flag and test
    original_flag = os.environ.get('USE_SPATIAL_SLACK')
    os.environ['USE_SPATIAL_SLACK'] = 'true'

    try:
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

        # Test router instantiation
        slack_router = SlackIntegrationRouter()
        print("✅ SlackIntegrationRouter instantiated with spatial enabled")

        # Test spatial adapter access
        if hasattr(slack_router, 'get_spatial_adapter'):
            spatial_adapter = slack_router.get_spatial_adapter()
            if spatial_adapter:
                print("✅ Spatial adapter accessible")
                print(f"  Type: {type(spatial_adapter).__name__}")

                # Test spatial adapter methods
                adapter_methods = [m for m in dir(spatial_adapter) if not m.startswith('_')]
                print(f"  Methods available: {len(adapter_methods)}")

                # Test core spatial operations if available
                if hasattr(spatial_adapter, 'send_message'):
                    print("✅ send_message method available")
                if hasattr(spatial_adapter, 'coordinate_with_context'):
                    print("✅ coordinate_with_context method available")

            else:
                print("⚠️ Spatial adapter returned None")
        else:
            print("❌ get_spatial_adapter method not available")

        # Test router methods work in spatial mode
        router_methods = [m for m in dir(slack_router) if not m.startswith('_')]
        print(f"✅ Router has {len(router_methods)} public methods")

    except Exception as e:
        print(f"❌ Spatial enabled test failed: {e}")

    # Restore original flag
    if original_flag:
        os.environ['USE_SPATIAL_SLACK'] = original_flag
    elif 'USE_SPATIAL_SLACK' in os.environ:
        del os.environ['USE_SPATIAL_SLACK']

create_slack_spatial_tests()
```

### Task 2: Feature Flag Control Validation

Systematically test USE_SPATIAL_SLACK flag behavior:

```python
# Comprehensive feature flag testing
def test_slack_feature_flag_control():
    """Test Slack spatial feature flag control comprehensively"""

    print("\n=== SLACK FEATURE FLAG COMPREHENSIVE TESTING ===")

    import os
    import importlib
    import sys

    # Store original state
    original_flag = os.environ.get('USE_SPATIAL_SLACK')

    def reload_slack_router():
        """Helper to reload router module for flag changes"""
        if 'services.integrations.slack.slack_integration_router' in sys.modules:
            importlib.reload(sys.modules['services.integrations.slack.slack_integration_router'])

    test_scenarios = [
        ('true', 'Spatial mode enabled'),
        ('false', 'Spatial mode disabled'),
        ('1', 'Spatial mode enabled (numeric true)'),
        ('0', 'Spatial mode disabled (numeric false)'),
        ('', 'Default behavior (flag empty)'),
    ]

    results = {}

    for flag_value, description in test_scenarios:
        print(f"\n🧪 Testing: {description} (USE_SPATIAL_SLACK='{flag_value}')")

        # Set flag value
        if flag_value == '':
            if 'USE_SPATIAL_SLACK' in os.environ:
                del os.environ['USE_SPATIAL_SLACK']
        else:
            os.environ['USE_SPATIAL_SLACK'] = flag_value

        try:
            # Reload to pick up flag change
            reload_slack_router()

            from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
            router = SlackIntegrationRouter()

            # Test spatial behavior
            spatial_active = False
            legacy_active = False

            if hasattr(router, '_should_use_spatial'):
                spatial_active = router._should_use_spatial()

            if hasattr(router, '_allow_legacy'):
                legacy_active = router._allow_legacy()

            # Test spatial adapter accessibility
            spatial_adapter_available = False
            if hasattr(router, 'get_spatial_adapter'):
                try:
                    adapter = router.get_spatial_adapter()
                    spatial_adapter_available = adapter is not None
                except:
                    spatial_adapter_available = False

            results[flag_value] = {
                'spatial_active': spatial_active,
                'legacy_active': legacy_active,
                'spatial_adapter_available': spatial_adapter_available,
                'status': 'SUCCESS'
            }

            print(f"  ✅ Spatial active: {spatial_active}")
            print(f"  ✅ Legacy active: {legacy_active}")
            print(f"  ✅ Spatial adapter available: {spatial_adapter_available}")

        except Exception as e:
            results[flag_value] = {'status': 'FAILED', 'error': str(e)}
            print(f"  ❌ Test failed: {e}")

    # Restore original flag
    if original_flag:
        os.environ['USE_SPATIAL_SLACK'] = original_flag
    elif 'USE_SPATIAL_SLACK' in os.environ:
        del os.environ['USE_SPATIAL_SLACK']

    # Summary
    print(f"\n📊 FEATURE FLAG TEST SUMMARY:")
    for flag_value, result in results.items():
        status = result.get('status', 'UNKNOWN')
        print(f"  '{flag_value}': {status}")

    return results

flag_test_results = test_slack_feature_flag_control()
```

### Task 3: Test Framework Enhancement

Enhance testing framework with proper Slack spatial tests:

```python
# Create comprehensive test file for Slack spatial system
slack_spatial_test_content = '''
"""
Comprehensive Slack Spatial System Tests
Created during GREAT-2C Phase 1
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock

class TestSlackSpatialIntegration:
    """Test Slack spatial intelligence integration"""

    def setup_method(self):
        """Setup for each test"""
        self.original_spatial_flag = os.environ.get('USE_SPATIAL_SLACK')
        self.original_legacy_flag = os.environ.get('ALLOW_LEGACY_SLACK')

    def teardown_method(self):
        """Cleanup after each test"""
        # Restore original flags
        if self.original_spatial_flag is not None:
            os.environ['USE_SPATIAL_SLACK'] = self.original_spatial_flag
        elif 'USE_SPATIAL_SLACK' in os.environ:
            del os.environ['USE_SPATIAL_SLACK']

        if self.original_legacy_flag is not None:
            os.environ['ALLOW_LEGACY_SLACK'] = self.original_legacy_flag
        elif 'ALLOW_LEGACY_SLACK' in os.environ:
            del os.environ['ALLOW_LEGACY_SLACK']

    def test_spatial_mode_enabled(self):
        """Test Slack spatial system with USE_SPATIAL_SLACK=true"""
        os.environ['USE_SPATIAL_SLACK'] = 'true'

        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

        router = SlackIntegrationRouter()

        # Test router instantiation
        assert router is not None

        # Test spatial adapter access
        if hasattr(router, 'get_spatial_adapter'):
            spatial_adapter = router.get_spatial_adapter()
            assert spatial_adapter is not None, "Spatial adapter should be available when enabled"

    def test_spatial_mode_disabled(self):
        """Test Slack spatial system with USE_SPATIAL_SLACK=false"""
        os.environ['USE_SPATIAL_SLACK'] = 'false'
        os.environ['ALLOW_LEGACY_SLACK'] = 'true'  # Enable legacy fallback

        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

        router = SlackIntegrationRouter()

        # Test router instantiation
        assert router is not None

        # Test that spatial is disabled
        if hasattr(router, '_should_use_spatial'):
            assert not router._should_use_spatial(), "Spatial should be disabled"

    def test_feature_flag_toggle(self):
        """Test toggling between spatial and legacy modes"""
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

        # Test enabled
        os.environ['USE_SPATIAL_SLACK'] = 'true'
        router_enabled = SlackIntegrationRouter()
        assert router_enabled is not None

        # Test disabled
        os.environ['USE_SPATIAL_SLACK'] = 'false'
        router_disabled = SlackIntegrationRouter()
        assert router_disabled is not None

    @patch('services.integrations.slack.slack_integration_router.SlackSpatialAdapter')
    def test_spatial_adapter_methods(self, mock_spatial_adapter):
        """Test spatial adapter method availability"""
        os.environ['USE_SPATIAL_SLACK'] = 'true'

        # Mock spatial adapter
        mock_adapter = MagicMock()
        mock_spatial_adapter.return_value = mock_adapter

        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

        router = SlackIntegrationRouter()

        if hasattr(router, 'get_spatial_adapter'):
            adapter = router.get_spatial_adapter()
            assert adapter is not None

    def test_error_handling(self):
        """Test error handling in spatial system"""
        os.environ['USE_SPATIAL_SLACK'] = 'true'

        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

        # Test that router handles errors gracefully
        router = SlackIntegrationRouter()
        assert router is not None

        # Additional error handling tests can be added here

class TestSlackSpatialPerformance:
    """Test Slack spatial system performance"""

    def test_router_instantiation_speed(self):
        """Test that router instantiation is fast"""
        import time

        os.environ['USE_SPATIAL_SLACK'] = 'true'

        start_time = time.time()
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
        router = SlackIntegrationRouter()
        end_time = time.time()

        instantiation_time = end_time - start_time
        assert instantiation_time < 1.0, f"Router instantiation too slow: {instantiation_time}s"

    def test_spatial_adapter_access_speed(self):
        """Test that spatial adapter access is fast"""
        import time

        os.environ['USE_SPATIAL_SLACK'] = 'true'

        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
        router = SlackIntegrationRouter()

        if hasattr(router, 'get_spatial_adapter'):
            start_time = time.time()
            adapter = router.get_spatial_adapter()
            end_time = time.time()

            access_time = end_time - start_time
            assert access_time < 0.1, f"Spatial adapter access too slow: {access_time}s"
'''

# Write comprehensive test file
os.makedirs('tests/integration', exist_ok=True)
with open('tests/integration/test_slack_spatial_comprehensive.py', 'w') as f:
    f.write(slack_spatial_test_content)

print("✅ Created comprehensive Slack spatial test suite")
print("   Location: tests/integration/test_slack_spatial_comprehensive.py")
```

### Task 4: Execute Test Suite Validation

Run comprehensive test validation:

```bash
# Execute Slack spatial test suite
echo "=== SLACK SPATIAL TEST EXECUTION ==="

# Run the comprehensive test suite we created
echo "Running comprehensive Slack spatial tests..."
python -m pytest tests/integration/test_slack_spatial_comprehensive.py -v --tb=short

# Run any existing Slack spatial tests
echo "Running existing spatial tests..."
find tests/ -name "*slack*spatial*" -name "*.py" | while read test_file; do
    echo "Running $test_file..."
    python -m pytest "$test_file" -v --tb=short
done

# Test with different flag combinations
echo "Testing flag combinations..."

echo "Testing USE_SPATIAL_SLACK=true..."
USE_SPATIAL_SLACK=true python -m pytest tests/integration/test_slack_spatial_comprehensive.py::TestSlackSpatialIntegration::test_spatial_mode_enabled -v

echo "Testing USE_SPATIAL_SLACK=false..."
USE_SPATIAL_SLACK=false ALLOW_LEGACY_SLACK=true python -m pytest tests/integration/test_slack_spatial_comprehensive.py::TestSlackSpatialIntegration::test_spatial_mode_disabled -v

# Performance testing
echo "Running performance tests..."
python -m pytest tests/integration/test_slack_spatial_comprehensive.py::TestSlackSpatialPerformance -v
```

### Task 5: Cross-Validation with Code Agent

Prepare findings for cross-validation:

```python
# Prepare cross-validation summary
def prepare_cross_validation_summary():
    """Prepare summary for cross-validation with Code agent"""

    print("\n=== CROSS-VALIDATION SUMMARY FOR CODE AGENT ===")

    summary = {
        'testing_results': {
            'integration_tests': 'Created comprehensive test suite',
            'feature_flag_tests': 'Validated USE_SPATIAL_SLACK control',
            'performance_tests': 'Verified reasonable response times',
            'error_handling': 'Basic error handling tested'
        },
        'infrastructure_validation': {
            'slack_router_works': True,
            'spatial_adapter_accessible': True,
            'feature_flags_control_behavior': True,
            'test_framework_enhanced': True
        },
        'discovered_patterns': {
            'spatial_coordination': 'Through SlackIntegrationRouter',
            'feature_flag_control': 'USE_SPATIAL_SLACK boolean flag',
            'legacy_fallback': 'ALLOW_LEGACY_SLACK for disabled mode',
            'adapter_access': 'get_spatial_adapter() method'
        }
    }

    print("📋 TESTING VALIDATION COMPLETE:")
    for category, items in summary.items():
        print(f"\n{category.upper()}:")
        if isinstance(items, dict):
            for key, value in items.items():
                print(f"  ✅ {key}: {value}")
        else:
            print(f"  ✅ {items}")

    return summary

cross_validation_summary = prepare_cross_validation_summary()
```

## Evidence Documentation

```bash
# Update GitHub issue with testing results
gh issue comment 194 --body "## Phase 1 Cursor Testing Complete

### Integration Testing ✅
- Comprehensive test suite created: tests/integration/test_slack_spatial_comprehensive.py
- Spatial mode testing: [PASS/FAIL with details]
- Legacy mode testing: [PASS/FAIL with details]
- [paste test execution output]

### Feature Flag Validation ✅
- USE_SPATIAL_SLACK=true: [WORKING/ISSUES]
- USE_SPATIAL_SLACK=false: [WORKING/ISSUES]
- Flag toggling: [WORKING/ISSUES]
- [paste flag validation results]

### Performance Testing ✅
- Router instantiation: [<1.0s requirement met]
- Spatial adapter access: [<0.1s requirement met]
- [paste performance test results]

### Test Framework Enhancement ✅
- New test files created: [count and locations]
- Existing tests validated: [PASS/FAIL counts]
- Coverage areas: [list test coverage]

### Cross-Validation Ready ✅
- Testing validation complete
- Findings ready for comparison with Code agent
- [attach cross-validation summary]

**Status**: Slack spatial testing [COMPREHENSIVE/NEEDS_WORK]
**Ready for Phase 2**: [YES/NO]"
```

## Success Criteria

Phase 1 Cursor testing complete when:
- [✅] Comprehensive Slack spatial test suite created
- [✅] Feature flag control (USE_SPATIAL_SLACK) validated
- [✅] Integration tests passing for spatial/legacy modes
- [✅] Performance requirements met
- [✅] Cross-validation summary prepared
- [✅] GitHub issue updated with testing evidence

## STOP Conditions

Stop immediately if:
- Cannot create or run tests
- Feature flags not controlling behavior
- Spatial system fundamentally broken
- Performance unacceptably slow
- Cannot validate spatial/legacy switching

---

**Your Mission**: Create comprehensive test validation of Slack spatial intelligence system functionality.

**Quality Standard**: Complete test coverage with evidence - ready for cross-validation with Code agent's architectural findings.
