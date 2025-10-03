# Cursor Agent Prompt: GREAT-3A Phase 1C - Config Pattern Test Suite

## Mission
**Create Reusable Test Suite**: Build validation tooling to verify config service pattern compliance across all integrations.

## Context from Phase 1B
We're aligning all 4 integrations to service injection pattern. Need automated way to verify compliance and catch regressions.

**Current Status**:
- ✅ Slack: Compliant (reference pattern)
- ✅ Notion: Compliant (just fixed)
- ⚠️ GitHub: Being fixed by Code agent now
- ❌ Calendar: Next to fix in Phase 1D

**Your Mission**: Create test suite that validates pattern compliance for any integration.

## Your Tasks

### Task 1: Design Test Suite Structure

**Location**: `tests/integration/config_pattern_compliance/`

**Files to Create**:
```
tests/integration/config_pattern_compliance/
├── __init__.py
├── test_config_pattern_compliance.py  # Main test suite
├── conftest.py                        # Pytest fixtures
└── README.md                          # Usage documentation
```

### Task 2: Pattern Compliance Checklist

**What Makes a Config Service Compliant?**

Based on Slack/Notion patterns, create tests for:

1. **File Structure**:
   - ✅ config_service.py exists in `services/integrations/{name}/`
   - ✅ Not in root `config/` directory (old pattern)

2. **Service Class**:
   - ✅ Has `{Name}ConfigService` class
   - ✅ Has `__init__` accepting optional FeatureFlags
   - ✅ Has `get_config()` method returning config dataclass
   - ✅ Has `is_configured()` method returning bool
   - ✅ Has `_load_config()` method loading from environment

3. **Config Dataclass**:
   - ✅ Has `{Name}Config` dataclass
   - ✅ Has `validate()` method
   - ✅ Has required fields (api_key/token, base_url, etc.)

4. **Router Integration**:
   - ✅ Router accepts `config_service` parameter in `__init__`
   - ✅ Parameter is Optional with type hint
   - ✅ Router stores config_service attribute
   - ✅ Router uses config_service (not direct env access)

5. **Graceful Degradation**:
   - ✅ Router works with config_service=None
   - ✅ Router creates default config if none provided
   - ✅ No crashes when config missing

### Task 3: Create Main Test Suite

**File**: `tests/integration/config_pattern_compliance/test_config_pattern_compliance.py`

**Test Structure**:
```python
import pytest
import os
import importlib
from pathlib import Path

# List of integrations to test
INTEGRATIONS = ["slack", "notion", "github", "calendar"]

class TestConfigPatternCompliance:
    """Test suite for config service pattern compliance"""

    @pytest.mark.parametrize("integration", INTEGRATIONS)
    def test_config_service_exists(self, integration):
        """Test that config_service.py exists in correct location"""
        # Check file exists at services/integrations/{integration}/config_service.py
        pass

    @pytest.mark.parametrize("integration", INTEGRATIONS)
    def test_config_service_class_exists(self, integration):
        """Test that {Name}ConfigService class exists"""
        # Import and check class exists
        pass

    @pytest.mark.parametrize("integration", INTEGRATIONS)
    def test_config_service_methods(self, integration):
        """Test that service has required methods"""
        # Check get_config(), is_configured(), _load_config()
        pass

    @pytest.mark.parametrize("integration", INTEGRATIONS)
    def test_router_accepts_config_service(self, integration):
        """Test that router accepts config_service parameter"""
        # Check router __init__ signature
        pass

    @pytest.mark.parametrize("integration", INTEGRATIONS)
    def test_router_uses_config_service(self, integration):
        """Test that router stores and uses config_service"""
        # Check router has config_service attribute
        pass

    @pytest.mark.parametrize("integration", INTEGRATIONS)
    def test_graceful_degradation(self, integration):
        """Test that router works without config_service"""
        # Instantiate router with no config, should not crash
        pass

    @pytest.mark.parametrize("integration", INTEGRATIONS)
    def test_no_direct_env_access(self, integration):
        """Test that router doesn't use os.getenv directly"""
        # Check router source for os.getenv/os.environ usage
        pass
```

### Task 4: Create Test Utilities

**Helper Functions**:
```python
def get_integration_config_service(integration_name: str):
    """Dynamically import config service for integration"""
    # Import services.integrations.{name}.config_service
    pass

def get_integration_router(integration_name: str):
    """Dynamically import router for integration"""
    # Import services.integrations.{name}.{name}_integration_router
    pass

def check_method_exists(cls, method_name: str) -> bool:
    """Check if class has method"""
    pass

def get_init_signature(cls):
    """Get __init__ parameter signature"""
    pass
```

### Task 5: Create Usage Documentation

**File**: `tests/integration/config_pattern_compliance/README.md`

**Document**:
- Purpose of test suite
- How to run tests
- How to interpret results
- How to add new integrations to test
- What each test validates

**Example**:
```markdown
# Config Pattern Compliance Test Suite

## Purpose
Validates that all integrations follow the service injection pattern.

## Running Tests

# Test all integrations
pytest tests/integration/config_pattern_compliance/ -v

# Test specific integration
pytest tests/integration/config_pattern_compliance/ -v -k slack

# Show compliance report
pytest tests/integration/config_pattern_compliance/ -v --tb=short

## Expected Output
- ✅ PASS: Integration follows pattern
- ❌ FAIL: Integration needs alignment
```

### Task 6: Create Compliance Report Script

**File**: `tests/integration/config_pattern_compliance/generate_report.py`

**Script that**:
- Runs all compliance tests
- Generates summary report
- Shows which integrations pass/fail each check
- Provides actionable recommendations

**Output Format**:
```
CONFIG PATTERN COMPLIANCE REPORT
================================

Integration | File | Class | Methods | Router | Usage | Status
----------- | ---- | ----- | ------- | ------ | ----- | ------
Slack       | ✅   | ✅    | ✅      | ✅     | ✅    | ✅ PASS
Notion      | ✅   | ✅    | ✅      | ✅     | ✅    | ✅ PASS
GitHub      | ✅   | ✅    | ✅      | ⚠️     | ⚠️    | ⚠️ PARTIAL
Calendar    | ❌   | ❌    | ❌      | ❌     | ❌    | ❌ FAIL

Overall Compliance: 50% (2 of 4 integrations)

Recommendations:
- GitHub: Wire config_service to router (30 min)
- Calendar: Create config_service.py (1-2 hours)
```

## Deliverable

Create: `dev/2025/10/02/phase-1c-cursor-test-suite.md`

Include:
1. **Test Suite Design**: Structure and approach
2. **Files Created**: All test files with implementation
3. **Usage Documentation**: How to run and interpret tests
4. **Compliance Report**: Initial run showing current status
5. **GitHub Validation**: Run tests on GitHub after Code finishes

## Time Estimate
30-45 minutes (parallel with Code's GitHub fix)

## Success Criteria
- [ ] Test suite structure created
- [ ] All compliance tests implemented
- [ ] Tests can be run with pytest
- [ ] Report generation script works
- [ ] Documentation complete
- [ ] Ready to validate GitHub fix immediately

## Coordination with Code

When Code completes GitHub alignment:
1. Run your test suite on GitHub integration
2. Verify all checks pass
3. Report results to Lead Developer
4. Provide compliance report

---

**Deploy at 3:50 PM**
**Coordinate with Code on GitHub validation**
