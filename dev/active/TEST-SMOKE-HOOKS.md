# TEST-SMOKE-HOOKS: Add smoke tests to pre-commit hooks for immediate feedback

**Title**: Add smoke tests to pre-commit hooks for immediate feedback
**Labels**: enhancement, testing, developer-experience
**Priority**: Medium (Quick Win)

## Problem

Developers don't get immediate feedback about basic functionality before committing code. Smoke tests exist and run in 1 second, but aren't integrated into the pre-commit workflow.

## Current State

- ✅ **Smoke tests work**: `./scripts/run_tests.sh smoke` executes in 1 second
- ✅ **Pre-commit hooks exist**: `.pre-commit-config.yaml` has linting, formatting
- ❌ **No smoke test validation**: Developers can commit broken imports/basic functionality

## Proposed Solution

Add smoke tests to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: smoke-tests
      name: Smoke Tests
      entry: ./scripts/run_tests.sh smoke
      language: system
      pass_filenames: false
      stages: [commit]
```

## Benefits

- **Immediate feedback**: Know if basic functionality works before committing
- **Prevent broken commits**: Catch import errors and basic issues early
- **Fast execution**: 1-second validation doesn't slow down workflow
- **Developer confidence**: Commit with confidence that core functionality works

## Implementation

### Files to Modify

- `.pre-commit-config.yaml`
- Possibly update documentation about pre-commit workflow

### Considerations

1. **Performance**: Must stay under 5-second target (currently 1s)
2. **Reliability**: Should work without database/external dependencies
3. **Scope**: Only run smoke tests, not full test suite
4. **Bypass option**: Allow `--no-verify` for emergency commits

## Success Criteria

- [ ] Smoke tests run automatically before every commit
- [ ] Pre-commit completes in < 5 seconds total
- [ ] Developers can bypass with `git commit --no-verify` if needed
- [ ] Clear error messages when smoke tests fail

## Alternative Approaches

1. **Git hooks**: Direct git hook instead of pre-commit framework
2. **IDE integration**: VS Code/other editor integration
3. **Make target**: `make pre-commit` that includes smoke tests

## Priority

**Medium (Quick Win)** - Easy to implement, immediate developer experience improvement.

## Dependencies

- None (current smoke tests work fine)
- Independent of ChromaDB Bus error issue (#XXX)
- Works with existing pre-commit infrastructure

## Estimated Effort

- **Implementation**: 15-30 minutes
- **Testing**: Few commits to validate workflow
- **Documentation**: Update developer docs
- **Total**: < 1 hour

## Risks

- **False positives**: If smoke tests are flaky, could block valid commits
- **Developer friction**: If too slow or unreliable, developers might bypass
- **Mitigation**: Keep tests fast, reliable, and provide clear bypass option
