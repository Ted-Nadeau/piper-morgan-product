# Bypass Prevention Test Strategy

**Epic**: GREAT-4B - Intent Classification Universal Enforcement
**Phase**: Phase 2 - Bypass Prevention Tests
**Date**: October 5, 2025
**Author**: Cursor Agent

---

## Purpose

Ensure all natural language endpoints use intent classification.
Prevent regression where new code bypasses intent layer.

---

## Test Layers

### 1. Unit Tests

**Location**: `tests/intent/`

- **`test_bypass_prevention.py`** - Core prevention tests
  - Validates middleware configuration
  - Tests exempt paths work correctly
  - Verifies monitoring endpoint
  - Confirms personality enhancement is exempt
  - Checks request logging functionality

### 2. Detection Tests

- **`test_future_nl_endpoints.py`** - Catches new NL routes
  - Scans for routes matching NL patterns
  - Validates they're in middleware config
  - Detects direct service calls in routes
  - Provides warnings for manual review

### 3. Integration Tests

- **`test_enforcement_integration.py`** - Full pipeline tests
  - Validates intent endpoint works
  - Tests standup backend integration
  - Confirms monitoring accessibility
  - End-to-end enforcement validation

### 4. CI/CD Script

- **`scripts/check_intent_bypasses.py`** - Automated scanning
  - Runs on every PR
  - Fails build if bypasses detected
  - Provides clear failure messages
  - Focuses on NL-like endpoints

---

## Running Tests

### Local Testing

```bash
# Run all bypass prevention tests
pytest tests/intent/test_bypass_prevention.py -v
pytest tests/intent/test_future_nl_endpoints.py -v
pytest tests/intent/test_enforcement_integration.py -v

# Run CI script
python scripts/check_intent_bypasses.py
```

### Expected Output

```bash
$ pytest tests/intent/test_bypass_prevention.py -v
========================= test session starts =========================
tests/intent/test_bypass_prevention.py::TestBypassPrevention::test_middleware_is_registered PASSED
tests/intent/test_bypass_prevention.py::TestBypassPrevention::test_nl_endpoints_marked PASSED
tests/intent/test_bypass_prevention.py::TestBypassPrevention::test_exempt_paths_accessible PASSED
tests/intent/test_bypass_prevention.py::TestBypassPrevention::test_personality_enhance_is_exempt PASSED
tests/intent/test_bypass_prevention.py::TestBypassPrevention::test_monitoring_logs_requests PASSED
========================= 5 passed in 0.45s =========================

$ python scripts/check_intent_bypasses.py
✅ NO BYPASSES DETECTED
```

---

## CI Integration

### GitHub Actions

Add to `.github/workflows/tests.yml`:

```yaml
- name: Check for intent bypasses
  run: python scripts/check_intent_bypasses.py

- name: Run bypass prevention tests
  run: pytest tests/intent/test_bypass_prevention.py -v
```

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: check-bypasses
      name: Check for intent bypasses
      entry: python scripts/check_intent_bypasses.py
      language: system
      pass_filenames: false
```

---

## Middleware Architecture

### IntentEnforcementMiddleware

**Key Components**:

- **NL_ENDPOINTS**: List of natural language endpoints requiring intent
- **EXEMPT_PATHS**: List of paths explicitly exempt from intent requirements
- **Request Monitoring**: Logs all requests for compliance tracking
- **State Marking**: Marks NL requests as requiring intent classification

**Current Configuration**:

- **NL Endpoints (4)**: `/api/v1/intent`, `/api/standup`, `/api/chat`, `/api/message`
- **Exempt Paths (12)**: Health, docs, static, personality output, UI pages

### Enforcement Principles

1. **User INPUT** → intent classification (enforced)
2. **Piper OUTPUT** → transformation only (exempt)
3. **Structured commands** → direct execution (exempt)
4. **Static content** → no processing needed (exempt)

---

## Test Categories

### Bypass Prevention Tests

**Purpose**: Validate current middleware configuration
**Tests**:

- Middleware registration and activity
- NL endpoint identification
- Exempt path accessibility
- Request logging functionality

### Future Endpoint Detection

**Purpose**: Catch new NL endpoints added without proper configuration
**Tests**:

- Route scanning for NL patterns
- Middleware configuration validation
- Direct service call detection

### Integration Validation

**Purpose**: End-to-end enforcement pipeline testing
**Tests**:

- Intent endpoint functionality
- Backend integration validation
- Monitoring endpoint accessibility

### CI/CD Scanning

**Purpose**: Automated bypass detection in CI pipeline
**Features**:

- Static code analysis
- NL pattern recognition
- Build failure on bypasses
- Clear error reporting

---

## Maintenance

### Adding New NL Endpoint

1. **Add to middleware**: Update `IntentEnforcementMiddleware.NL_ENDPOINTS`
2. **Implement intent usage**: Ensure endpoint uses intent classification
3. **Run test suite**: Validate all tests pass
4. **Document exemption**: If applicable, add to exempt list with rationale

### Updating Exempt Paths

1. **Review exemption rationale**: Ensure path truly doesn't need intent
2. **Update middleware**: Add to `IntentEnforcementMiddleware.EXEMPT_PATHS`
3. **Update tests**: Modify test expectations if needed
4. **Document decision**: Record why exemption is appropriate

### CI/CD Integration

1. **GitHub Actions**: Add bypass check to CI pipeline
2. **Pre-commit hooks**: Catch bypasses before commit
3. **Build failures**: Ensure bypasses fail builds
4. **Clear messaging**: Provide actionable error messages

---

## Success Metrics

### Current Baseline

- **Middleware active**: IntentEnforcementMiddleware operational
- **NL endpoints configured**: 4 endpoints properly marked
- **Exempt paths defined**: 12 paths with clear exemption rationale
- **Monitoring enabled**: All requests logged for compliance

### Target State

- **Zero bypasses**: No NL endpoints without intent classification
- **Automated prevention**: CI/CD catches new bypasses
- **Clear documentation**: All exemptions documented with rationale
- **Comprehensive testing**: Full test coverage for enforcement

### Validation Criteria

- All prevention tests pass
- CI script reports no bypasses
- Integration tests validate end-to-end flow
- Monitoring endpoint provides accurate status

---

## Troubleshooting

### Test Failures

**Middleware not registered**:

- Check middleware is added to FastAPI app
- Verify import path is correct
- Ensure middleware initialization

**Exempt paths not accessible**:

- Check path is in EXEMPT_PATHS list
- Verify path matching logic
- Test with exact path strings

**NL endpoints not working**:

- Confirm endpoint is in NL_ENDPOINTS list
- Check intent classification implementation
- Validate request routing

### False Positives

**CI script false alarms**:

- Review exemption patterns in script
- Update keyword matching logic
- Add specific path exemptions

**Test environment issues**:

- Check test client configuration
- Verify middleware registration in tests
- Ensure proper test isolation

---

## Related Documentation

- **GREAT-4B Epic**: Complete universal enforcement plan
- **IntentEnforcementMiddleware**: `web/middleware/intent_enforcement.py`
- **Pattern-028**: Intent Classification pattern
- **ADR-032**: Intent Classification Universal Entry

---

**Status**: ✅ Bypass prevention strategy documented and implemented
