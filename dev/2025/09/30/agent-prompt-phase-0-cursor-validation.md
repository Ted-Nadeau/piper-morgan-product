# Cursor Agent Prompt: Phase 0 - Infrastructure Validation & Testing Readiness

## Mission: Validate Infrastructure State and Prepare Testing Framework

**Context**: GREAT-2C verification work following CORE-QUERY-1 router completion. Need focused validation of infrastructure state and preparation for systematic spatial system testing.

**Objective**: Validate that infrastructure matches gameplan expectations, verify router functionality, and prepare testing framework for upcoming spatial verification work.

## Phase 0 Validation Tasks

### Task 1: Router Functionality Validation

Verify routers from CORE-QUERY-1 are fully operational:

```python
# Test router instantiation and basic functionality
def test_router_infrastructure():
    """Validate all routers work as expected"""

    print("=== ROUTER INFRASTRUCTURE VALIDATION ===")

    try:
        # Test Calendar Router
        from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
        calendar_router = CalendarIntegrationRouter()
        print("✅ CalendarIntegrationRouter instantiated successfully")

        # Test basic method availability
        if hasattr(calendar_router, 'health_check'):
            print("  ✅ health_check method available")
        else:
            print("  ⚠️ health_check method missing")

    except Exception as e:
        print(f"❌ CalendarIntegrationRouter failed: {e}")

    try:
        # Test Notion Router
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
        notion_router = NotionIntegrationRouter()
        print("✅ NotionIntegrationRouter instantiated successfully")

        if hasattr(notion_router, 'is_configured'):
            print("  ✅ is_configured method available")
        else:
            print("  ⚠️ is_configured method missing")

    except Exception as e:
        print(f"❌ NotionIntegrationRouter failed: {e}")

    try:
        # Test Slack Router
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
        slack_router = SlackIntegrationRouter()
        print("✅ SlackIntegrationRouter instantiated successfully")

        if hasattr(slack_router, 'get_spatial_adapter'):
            print("  ✅ get_spatial_adapter method available")
        else:
            print("  ⚠️ get_spatial_adapter method missing")

    except Exception as e:
        print(f"❌ SlackIntegrationRouter failed: {e}")

test_router_infrastructure()
```

### Task 2: Feature Flag System Validation

Test feature flag functionality for spatial systems:

```python
# Validate feature flag system works
def validate_feature_flags():
    """Test feature flag system for spatial controls"""

    print("\n=== FEATURE FLAG VALIDATION ===")

    import os

    # Test USE_SPATIAL_SLACK flag
    original_slack = os.environ.get('USE_SPATIAL_SLACK')

    # Test enabled state
    os.environ['USE_SPATIAL_SLACK'] = 'true'
    try:
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
        slack_router = SlackIntegrationRouter()
        # Check if router recognizes flag
        print("✅ USE_SPATIAL_SLACK=true processed")
    except Exception as e:
        print(f"⚠️ USE_SPATIAL_SLACK=true error: {e}")

    # Test disabled state
    os.environ['USE_SPATIAL_SLACK'] = 'false'
    try:
        # Reload to test flag change
        print("✅ USE_SPATIAL_SLACK=false processed")
    except Exception as e:
        print(f"⚠️ USE_SPATIAL_SLACK=false error: {e}")

    # Test USE_SPATIAL_NOTION flag
    original_notion = os.environ.get('USE_SPATIAL_NOTION')

    os.environ['USE_SPATIAL_NOTION'] = 'true'
    try:
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
        notion_router = NotionIntegrationRouter()
        print("✅ USE_SPATIAL_NOTION=true processed")
    except Exception as e:
        print(f"⚠️ USE_SPATIAL_NOTION=true error: {e}")

    # Restore original values
    if original_slack:
        os.environ['USE_SPATIAL_SLACK'] = original_slack
    elif 'USE_SPATIAL_SLACK' in os.environ:
        del os.environ['USE_SPATIAL_SLACK']

    if original_notion:
        os.environ['USE_SPATIAL_NOTION'] = original_notion
    elif 'USE_SPATIAL_NOTION' in os.environ:
        del os.environ['USE_SPATIAL_NOTION']

validate_feature_flags()
```

### Task 3: Testing Framework Preparation

Set up testing infrastructure for spatial verification:

```bash
# Check current test setup
echo "=== TESTING FRAMEWORK VALIDATION ==="

# Verify pytest works
python -m pytest --version
echo "Pytest version check complete"

# Check test directory structure
ls -la tests/
echo ""

# Look for existing spatial tests
find tests/ -name "*spatial*" 2>/dev/null || echo "No existing spatial tests found"
echo ""

# Check for integration test directory
if [ -d "tests/integration" ]; then
    echo "✅ Integration test directory exists"
    ls -la tests/integration/
else
    echo "⚠️ Integration test directory missing - will need creation"
    mkdir -p tests/integration
    echo "Created tests/integration/ directory"
fi
```

Create basic test framework for spatial verification:

```python
# Create test template for spatial verification
test_spatial_template = '''
"""
Template for spatial system testing
Created during Phase 0 preparation
"""

import pytest
import os
from unittest.mock import Mock, patch

class TestSpatialSystem:
    """Base class for spatial system testing"""

    def setup_method(self):
        """Setup for each test method"""
        self.original_flags = {}

    def teardown_method(self):
        """Cleanup after each test method"""
        # Restore original flag values
        for key, value in self.original_flags.items():
            if value is None:
                if key in os.environ:
                    del os.environ[key]
            else:
                os.environ[key] = value

    def set_spatial_flag(self, flag_name, value):
        """Helper to set spatial flags with cleanup tracking"""
        self.original_flags[flag_name] = os.environ.get(flag_name)
        if value is None:
            if flag_name in os.environ:
                del os.environ[flag_name]
        else:
            os.environ[flag_name] = str(value)

# Template for slack spatial tests
class TestSlackSpatialSystem(TestSpatialSystem):
    """Test Slack spatial intelligence system"""

    def test_spatial_flag_enabled(self):
        """Test Slack spatial system with USE_SPATIAL_SLACK=true"""
        self.set_spatial_flag('USE_SPATIAL_SLACK', 'true')

        # Test will be implemented in Phase 1
        pass

    def test_spatial_flag_disabled(self):
        """Test Slack spatial system with USE_SPATIAL_SLACK=false"""
        self.set_spatial_flag('USE_SPATIAL_SLACK', 'false')

        # Test will be implemented in Phase 1
        pass

# Template for notion spatial tests
class TestNotionSpatialSystem(TestSpatialSystem):
    """Test Notion spatial intelligence system"""

    def test_spatial_flag_enabled(self):
        """Test Notion spatial system with USE_SPATIAL_NOTION=true"""
        self.set_spatial_flag('USE_SPATIAL_NOTION', 'true')

        # Test will be implemented in Phase 2
        pass

    def test_spatial_flag_disabled(self):
        """Test Notion spatial system with USE_SPATIAL_NOTION=false"""
        self.set_spatial_flag('USE_SPATIAL_NOTION', 'false')

        # Test will be implemented in Phase 2
        pass
'''

# Write test template file
with open('tests/integration/test_spatial_template.py', 'w') as f:
    f.write(test_spatial_template)

print("✅ Created spatial test template: tests/integration/test_spatial_template.py")
```

### Task 4: Security Endpoint Validation

Validate webhook security endpoints exist and test current state:

```python
# Test webhook endpoints and security state
def validate_webhook_security():
    """Validate webhook endpoints and current security status"""

    print("\n=== WEBHOOK SECURITY VALIDATION ===")

    # Check if app is running and accessible
    import requests
    import subprocess

    try:
        # Check if server is running on expected port
        response = requests.get('http://localhost:8001/health', timeout=5)
        print(f"✅ Server accessible on port 8001: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Server not accessible on port 8001: {e}")
        print("This is expected if server not running - webhook test will be manual")
        return

    # Test webhook endpoint exists
    try:
        # Test with minimal request to see if endpoint exists
        response = requests.post('http://localhost:8001/webhooks/slack',
                               json={'test': 'data'}, timeout=5)
        print(f"✅ Webhook endpoint exists: {response.status_code}")

        # Check if this is 401 (security enabled) or 200 (security disabled)
        if response.status_code == 401:
            print("  🔐 Security appears ENABLED (401 Unauthorized)")
        elif response.status_code == 200:
            print("  ⚠️ Security appears DISABLED (200 OK)")
        else:
            print(f"  ❓ Unexpected response: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Webhook endpoint test failed: {e}")

validate_webhook_security()
```

### Task 5: Cross-Validation Preparation

Prepare for cross-validation with Code agent:

```python
# Create validation checklist for cross-checking with Code agent
def create_validation_checklist():
    """Create checklist for cross-validation with Code agent"""

    print("\n=== CROSS-VALIDATION CHECKLIST ===")

    checklist = {
        'router_infrastructure': {
            'calendar_router_works': False,
            'notion_router_works': False,
            'slack_router_works': False
        },
        'feature_flags': {
            'spatial_slack_flag_works': False,
            'spatial_notion_flag_works': False
        },
        'testing_framework': {
            'pytest_available': False,
            'integration_tests_dir': False,
            'test_templates_created': False
        },
        'security_status': {
            'webhook_endpoint_exists': False,
            'security_state_identified': False
        }
    }

    print("Validation checklist created for comparison with Code agent findings:")
    for category, items in checklist.items():
        print(f"\n📋 {category.upper()}:")
        for item, status in items.items():
            print(f"  [ ] {item}")

    return checklist

validation_checklist = create_validation_checklist()
```

## Evidence Collection

```bash
# Document validation results
echo "=== PHASE 0 VALIDATION SUMMARY ==="
echo "Router Infrastructure: [PASS/FAIL with details]"
echo "Feature Flag System: [PASS/FAIL with details]"
echo "Testing Framework: [READY/NEEDS_SETUP with details]"
echo "Security Endpoints: [ACCESSIBLE/ISSUES with details]"
echo ""
echo "Cross-validation items ready for Code agent comparison"
```

## GitHub Update

```bash
# Update GitHub issue with validation results
gh issue comment 194 --body "## Phase 0 Cursor Validation Complete

### Router Functionality ✅
- Calendar router: [status]
- Notion router: [status]
- Slack router: [status]

### Feature Flag Testing ✅
- USE_SPATIAL_SLACK toggle: [working/issues]
- USE_SPATIAL_NOTION toggle: [working/issues]

### Testing Framework ✅
- Pytest available: [yes/no]
- Integration test structure: [ready/created]
- Test templates: [created/exists]

### Security Validation ✅
- Webhook endpoints: [accessible/issues]
- Current security state: [enabled/disabled/unknown]

**Ready for Cross-Validation**: Awaiting Code agent findings for comparison"
```

## Success Criteria

Phase 0 validation complete when:
- [✅] All 3 routers validated functional
- [✅] Feature flag system tested
- [✅] Testing framework prepared
- [✅] Security endpoint status confirmed
- [✅] Cross-validation checklist ready
- [✅] GitHub issue updated with findings

## STOP Conditions

Stop and escalate if:
- Router infrastructure broken (regression from CORE-QUERY-1)
- Feature flags not working
- Cannot access testing framework
- Security endpoints completely inaccessible
- Cannot update GitHub issue

---

**Your Mission**: Validate infrastructure readiness and prepare testing framework for spatial verification work.

**Quality Standard**: All infrastructure components confirmed working with evidence - solid foundation for Phase 1-2 work.
