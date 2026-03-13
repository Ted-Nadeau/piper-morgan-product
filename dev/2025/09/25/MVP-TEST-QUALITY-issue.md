# MVP-TEST-QUALITY: Test Reliability for Production Confidence

## Context
Split from GREAT-1C-COMPLETION (#189). These test quality improvements are required for MVP 1.0 to ensure CI/CD reliability and production confidence.

## Background
QueryRouter functionality is complete and working. However, test suite has quality issues that reduce confidence in CI/CD and make it harder to prevent regressions.

## Acceptance Criteria

### Mock Pattern Fixes
- [ ] Replace MagicMock with AsyncMock for async operations
- [ ] Fix `TypeError: object MagicMock can't be used in 'await' expression`
- [ ] Ensure all async tests properly await mocked operations
- [ ] Document mock patterns for future test writing

### Integration Test Alignment
- [ ] Update test assertions to match actual API behavior
- [ ] Fix `assert 200 == 422` discrepancies
- [ ] Align test expectations with implementation reality
- [ ] Remove outdated test assumptions

### Critical Path Coverage
- [ ] Achieve 80% coverage for QueryRouter specifically
- [ ] Achieve 70% coverage for core OrchestrationEngine paths
- [ ] Document coverage targets per component
- [ ] Exclude legacy code from coverage requirements

### Error Scenario Fixes
- [ ] Fix test collection errors in error scenarios
- [ ] Ensure all error paths have basic test coverage
- [ ] Add tests for graceful degradation paths
- [ ] Verify error messages are helpful

## Success Validation
```bash
# All tests should pass without mock errors
pytest tests/ -v --tb=short

# Critical path coverage meets targets
pytest tests/ --cov=services/orchestration/queryrouter --cov-fail-under=80
pytest tests/ --cov=services/orchestration/engine --cov-fail-under=70

# No collection errors
pytest tests/ --collect-only | grep -c "error"  # Should be 0
```

## Priority: HIGH for MVP
These improvements directly impact:
- Developer confidence in changes
- CI/CD reliability
- Regression prevention
- Production stability

## Estimated Effort
- Mock pattern fixes: 2-3 hours
- Integration test alignment: 2-3 hours
- Coverage improvements: 3-4 hours
- Error scenario fixes: 1-2 hours
- **Total: 8-12 hours**

## NOT in Scope
- Web UI E2E testing (see POST-TEST-E2E)
- 100% coverage targets
- Legacy component testing
- Performance optimization

## Definition of Done
- All tests pass reliably
- No async/await mock errors
- Critical paths have good coverage
- CI/CD runs green consistently
- Test patterns documented

## Related
- Split from: GREAT-1C-COMPLETION (#189)
- Blocks: MVP 1.0 release
- After: CORE-GREAT-1 (#180)

---

**Labels**: mvp, testing, quality, debt
