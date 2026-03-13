# GREAT-1C-COMPLETION: Test Quality and Remaining Work

## Context
Follow-up issue from CORE-GREAT-1C (#187). Infrastructure work is complete - tests collect and execute. This issue tracks remaining test quality improvements and missing capabilities.

## Background
During GREAT-1C investigation (Sept 23), we achieved:
- ✅ Test infrastructure working (all tests collect and execute)
- ✅ Fixed import paths and dependencies
- ✅ Created missing mock infrastructure
- ✅ Fixed constructor bugs

But discovered:
- ❌ Many tests fail on assertions/business logic
- ❌ LLM JSON parsing regression (worked before, broken now)
- ❌ Mock async patterns need improvement
- ❌ Web UI E2E testing doesn't exist

## Acceptance Criteria

### Fix Regression
- [ ] Fix LLM JSON parsing that worked previously
- [ ] Verify API key configuration is correct
- [ ] Performance tests pass with <500ms requirement

### Test Quality Improvements
- [ ] Fix mock async patterns (MagicMock await issues)
- [ ] Update integration test assertions to match actual behavior
- [ ] Fix error scenario test collection issues
- [ ] Achieve 80% test coverage for orchestration module

### New Capabilities (Future)
- [ ] Implement web UI E2E testing for GitHub issue creation
- [ ] Add Playwright or Selenium for chat interface testing
- [ ] Create true end-to-end test: UI → Backend → GitHub

## Evidence Required
- Test output showing all tests passing
- Coverage report showing >80%
- LLM JSON parsing working (terminal output)
- Performance benchmarks meeting targets

## Known Issues to Fix

### 1. LLM JSON Parsing Regression
```
LowConfidenceIntentError: Could not determine intent with sufficient confidence
```
- This WORKED before (per PM confirmation)
- Blocking performance and classification tests
- Likely configuration or API integration issue

### 2. Mock Async Pattern Errors
```
TypeError: object MagicMock can't be used in 'await' expression
```
- Need AsyncMock instead of MagicMock
- Affects multiple test files

### 3. Integration Test Assertions
```
assert 200 == 422  # Expectations don't match actual behavior
```
- Tests expect different status codes than implementation returns
- Need to align tests with actual behavior

## Success Validation
```bash
# All tests should pass
pytest tests/ -v

# Coverage should exceed 80%
pytest tests/ --cov=services/orchestration --cov-report=term

# Performance tests should validate <500ms
pytest tests/regression/test_queryrouter_lock.py -k performance -v

# No collection errors
pytest tests/ --collect-only
```

## Priority
HIGH - The LLM regression is blocking other work
MEDIUM - Test quality improvements for CI/CD confidence
LOW - Web UI E2E (new capability, not regression)

## Estimated Effort
- Fix regression: 1-2 hours
- Test quality: 2-3 hours
- Web UI E2E: 4-6 hours (new development)

## Related
- Parent: CORE-GREAT-1C (#187)
- Blocks: CI/CD reliability
- Discovered during: GREAT-1C investigation (Sept 23)

## Notes
- Infrastructure work from GREAT-1C is valuable and complete
- This issue separates test quality from test infrastructure
- Maintains Inchworm Protocol: infrastructure layer done, quality layer tracked

---

**Labels**: testing, debt, regression, follow-up
