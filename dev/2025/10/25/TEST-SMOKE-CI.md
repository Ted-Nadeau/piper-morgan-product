# TEST-SMOKE-CI: Integrate smoke tests into GitHub Actions CI pipeline

**Title**: Integrate smoke tests into GitHub Actions CI pipeline
**Labels**: enhancement, testing, ci-cd
**Priority**: Medium (Quick Win)

## Problem

Smoke tests exist and work perfectly (`./scripts/run_tests.sh smoke` runs in 1s), but they don't run automatically in our CI pipeline.

## Current State

- ✅ **Smoke tests work**: `./scripts/run_tests.sh smoke` executes in 1 second
- ✅ **13 smoke tests found**: In `tests/unit/test_slack_components.py`
- ✅ **Infrastructure exists**: Comprehensive smoke test framework
- ❌ **No CI integration**: `.github/workflows/ci.yml` doesn't include smoke tests

## Proposed Solution

Add smoke test execution to `.github/workflows/ci.yml`:

```yaml
- name: Run smoke tests
  run: ./scripts/run_tests.sh smoke
  timeout-minutes: 1
```

## Benefits

- **Fast feedback**: 1-second validation on every PR/push
- **Catch regressions early**: Basic functionality validated immediately
- **Developer confidence**: Know if core imports/functionality work
- **Foundation for more**: Enable adding more smoke tests later

## Implementation

### Files to Modify

- `.github/workflows/ci.yml`

### Expected Changes

1. Add smoke test step after dependency installation
2. Set appropriate timeout (1-2 minutes max)
3. Ensure it runs on both PR and push events
4. Consider running before longer test suites for fast feedback

## Success Criteria

- [ ] Smoke tests run automatically on every PR
- [ ] Smoke tests run automatically on every push to main/develop
- [ ] CI fails fast if smoke tests fail (< 2 minutes)
- [ ] Smoke tests complete in < 5 seconds as designed

## Priority

**Medium (Quick Win)** - Easy to implement, immediate value, enables future smoke test expansion.

## Dependencies

- None (current smoke tests work fine)
- Independent of ChromaDB Bus error issue (#XXX)

## Estimated Effort

- **Implementation**: 15-30 minutes
- **Testing**: 1-2 PR cycles to validate
- **Total**: < 1 hour
