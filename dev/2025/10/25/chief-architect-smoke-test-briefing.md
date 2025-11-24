# Chief Architect Briefing: Smoke Test Infrastructure Status

**Date**: October 24, 2025
**Context**: Alpha onboarding preparation and infrastructure assessment
**Prepared for**: Roadmapping and prioritization discussions

## Executive Summary

Smoke test infrastructure investigation reveals **mixed results**: excellent manual execution capabilities but **broken automation integration**. Four specific issues identified for roadmap consideration.

## Current State Assessment

### ✅ What Works Well

- **Manual execution**: `./scripts/run_tests.sh smoke` runs perfectly in 1 second
- **Infrastructure exists**: Comprehensive smoke test framework with timing/reporting
- **Performance target met**: <5 second target achieved (actual: 1s)
- **Foundation solid**: 13 confirmed smoke tests, documentation claims 599+

### ❌ Critical Gaps

- **CI integration missing**: No automatic execution in GitHub Actions
- **Pre-commit integration missing**: No developer workflow integration
- **Pytest collection broken**: ChromaDB/numpy Bus error prevents test discovery
- **Automation blocked**: Can't reliably enumerate or integrate smoke tests

## Proposed GitHub Issues for Roadmap

### Issue 1: ChromaDB Import Bus Error ⚠️ **HIGH PRIORITY**

- **Impact**: Blocks 599+ smoke tests from discovery/execution
- **Technical debt**: ChromaDB/numpy compatibility issue on macOS
- **Workaround exists**: Manual script works fine
- **Effort estimate**: 4-8 hours investigation + fix

### Issue 2: CI Integration 🚀 **QUICK WIN**

- **Impact**: No automatic smoke test execution on PR/push
- **Implementation**: Add one step to `.github/workflows/ci.yml`
- **Value**: Fast feedback (1s) on every code change
- **Effort estimate**: 30 minutes

### Issue 3: Pre-commit Integration 🚀 **QUICK WIN**

- **Impact**: No immediate developer feedback before commits
- **Implementation**: Add hook to `.pre-commit-config.yaml`
- **Value**: Prevent broken commits, improve developer experience
- **Effort estimate**: 30 minutes

### Issue 4: Test Discovery Infrastructure 📊 **NICE TO HAVE**

- **Impact**: Can't enumerate/validate smoke test coverage
- **Dependency**: Blocked by Issue 1 (ChromaDB fix)
- **Alternative**: Static analysis approach possible
- **Effort estimate**: 2-4 hours

## Roadmap Recommendations

### Immediate (Sprint A8)

- **Issue 2 & 3**: Implement CI and pre-commit integration
- **Rationale**: Quick wins, immediate value, independent of technical issues
- **Total effort**: 1 hour
- **Impact**: Automated smoke test execution in development workflow

### Next Sprint (A9/B1)

- **Issue 1**: Investigate and fix ChromaDB Bus error
- **Rationale**: Unlocks full smoke test infrastructure (599+ tests)
- **Risk**: May require dependency updates or architecture changes

### Future/Optional

- **Issue 4**: Enhanced test discovery and reporting
- **Rationale**: Nice to have for metrics and coverage validation
- **Priority**: Low, can be deferred

## Strategic Considerations

### Alpha Testing Impact

- **Current capability sufficient**: Manual smoke tests work for alpha validation
- **CI integration valuable**: Automated feedback improves alpha development velocity
- **Risk mitigation**: Issues 2&3 provide immediate value without technical risk

### Technical Debt vs. Value

- **High-value, low-risk**: CI and pre-commit integration (Issues 2&3)
- **High-impact, medium-risk**: ChromaDB fix (Issue 1)
- **Low-priority**: Discovery infrastructure (Issue 4)

### Resource Allocation

- **Developer time**: 1 hour immediate, 4-8 hours for technical investigation
- **Risk profile**: Quick wins available while technical issues are investigated
- **Parallel work**: Issues 2&3 can proceed independently of Issue 1

## Questions for Leadership Discussion

1. **Priority of quick wins**: Should we implement CI/pre-commit integration immediately?
2. **Technical debt tolerance**: How much effort to invest in ChromaDB Bus error fix?
3. **Alpha timeline impact**: Do smoke test gaps affect alpha testing schedule?
4. **Resource allocation**: Who should tackle technical investigation vs. quick wins?

---

**Bottom Line**: Smoke test infrastructure is **functional but not automated**. Quick wins available (1 hour) while technical issues are investigated separately (4-8 hours). Recommend implementing automation first, then addressing technical debt.
