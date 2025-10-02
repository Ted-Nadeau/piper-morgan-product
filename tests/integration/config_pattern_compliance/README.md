# Config Pattern Compliance Test Suite

## Purpose

Validates that all integrations follow the service injection pattern for consistent configuration management across the Piper Morgan system.

This test suite ensures architectural consistency and prevents regressions when refactoring integration configurations.

## Service Injection Pattern Requirements

Each integration should follow this pattern:

### 1. File Structure

- `services/integrations/{name}/config_service.py` exists
- Not in legacy `config/` directory

### 2. Config Service Class

- `{Name}ConfigService` class exists
- `__init__(self, feature_flags: Optional[FeatureFlags] = None)`
- `get_config()` method returning config dataclass
- `is_configured()` method returning bool
- `_load_config()` method loading from environment variables

### 3. Config Dataclass

- `{Name}Config` dataclass with required fields
- `validate()` method returning bool
- Environment variable mapping

### 4. Router Integration

- Router accepts `config_service` parameter in `__init__`
- Parameter is Optional with type hint
- Router stores `config_service` attribute
- Router uses config_service (not direct env access)

### 5. Graceful Degradation

- Router works with `config_service=None`
- No crashes when config missing
- Fallback behavior implemented

## Running Tests

### Test All Integrations

```bash
# Run complete test suite
pytest tests/integration/config_pattern_compliance/ -v

# Run with detailed output
pytest tests/integration/config_pattern_compliance/ -v --tb=short

# Run specific test category
pytest tests/integration/config_pattern_compliance/ -v -k "config_service"
```

### Test Specific Integration

```bash
# Test only Slack integration
pytest tests/integration/config_pattern_compliance/ -v -k slack

# Test only Notion integration
pytest tests/integration/config_pattern_compliance/ -v -k notion

# Test GitHub integration (after Code agent fixes)
pytest tests/integration/config_pattern_compliance/ -v -k github
```

### Generate Compliance Report

```bash
# Generate detailed compliance report
python tests/integration/config_pattern_compliance/generate_report.py

# Run report with specific integrations
python tests/integration/config_pattern_compliance/generate_report.py --integrations slack,notion
```

## Expected Output

### ✅ PASS: Integration Follows Pattern

```
test_config_service_file_exists[slack] PASSED
test_config_service_class_exists[slack] PASSED
test_config_service_required_methods[slack] PASSED
test_router_accepts_config_service[slack] PASSED
test_graceful_degradation[slack] PASSED
```

### ❌ FAIL: Integration Needs Alignment

```
test_config_service_file_exists[calendar] FAILED
AssertionError: Config service file missing: services/integrations/calendar/config_service.py
Expected: services/integrations/calendar/config_service.py
```

## Test Categories

### File Structure Tests

- `test_config_service_file_exists`: Validates file location
- `test_config_dataclass_exists`: Validates config dataclass

### Class Structure Tests

- `test_config_service_class_exists`: Validates class naming
- `test_config_service_required_methods`: Validates required methods
- `test_config_service_init_signature`: Validates constructor

### Router Integration Tests

- `test_router_accepts_config_service`: Validates router constructor
- `test_router_stores_config_service`: Validates config storage
- `test_graceful_degradation`: Validates fallback behavior

### Code Quality Tests

- `test_no_direct_env_access_in_router`: Prevents direct env access

## Adding New Integrations

To add a new integration to the test suite:

1. Add integration name to `INTEGRATIONS` list in `conftest.py`
2. Ensure integration follows the pattern requirements
3. Run tests to validate compliance

Example:

```python
# In conftest.py
@pytest.fixture
def integration_names():
    return ["slack", "notion", "github", "calendar", "new_integration"]
```

## Interpreting Results

### Compliance Levels

- **✅ FULL COMPLIANCE**: All tests pass - integration ready for production
- **⚠️ PARTIAL COMPLIANCE**: Some tests pass - integration needs minor fixes
- **❌ NON-COMPLIANT**: Most tests fail - integration needs major refactoring

### Common Failure Patterns

1. **Missing Config Service**: Create `config_service.py` file
2. **Wrong Class Name**: Use `{Name}ConfigService` pattern
3. **Missing Methods**: Implement `get_config()`, `is_configured()`, `_load_config()`
4. **Router Not Updated**: Add `config_service` parameter to router `__init__`
5. **Direct Env Access**: Replace `os.getenv()` with config service usage

## Integration Status

Current status of integrations:

- **Slack**: ✅ Reference implementation (fully compliant)
- **Notion**: ✅ Compliant (implemented in Phase 1B)
- **GitHub**: ⚠️ Being fixed by Code agent
- **Calendar**: ❌ Needs implementation (Phase 1D)

## Troubleshooting

### Import Errors

If tests fail with import errors, ensure:

- Integration directory exists in `services/integrations/`
- `__init__.py` files are present
- Class names follow naming conventions

### Test Skips

Tests are skipped when:

- Config service class not found
- Router class not found
- Import failures occur

This is expected for integrations not yet implementing the pattern.

### False Positives

If tests pass but integration doesn't work:

- Check environment variable configuration
- Verify actual config service usage in router
- Test with real configuration values

## Development Workflow

1. **Before Changes**: Run tests to establish baseline
2. **During Development**: Run specific integration tests
3. **After Changes**: Run full suite to verify compliance
4. **Before Merge**: Generate compliance report for documentation

## Related Documentation

- [ADR-010: Configuration Access Patterns](../../docs/architecture/adrs/ADR-010-config-access-patterns.md)
- [Service Injection Pattern Guide](../../docs/patterns/service-injection.md)
- [Integration Development Guide](../../docs/development/integration-guide.md)
