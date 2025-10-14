# Gameplan: October 13, 2025 - Foundation Day + GAP-3

**Date**: Monday, October 13, 2025, 7:45 AM
**Epic**: CORE-CRAFT-GAP (2/3 complete)
**Today's Focus**: Clear blocking issues, then complete GAP-3
**Lead Developer**: Claude Sonnet 4.5
**PM**: Christian Crumlish

---

## Executive Summary

**Mission**: Address 3 critical blocking issues, then complete GAP-3 accuracy polish

**Why Today Matters**: Foundation-building work that enables everything else
- Clean CI workflows
- Working test infrastructure
- Clear architectural state
- Then: GAP-3 accuracy improvements

**PM's Take**: "I think deep down I knew things like this still needed attention?" ✅

**Total Estimated Time**: 8-10 hours (2 hours blocking + 6-8 hours GAP-3)

---

## Phase -1: Infrastructure Verification ✅ COMPLETE

**Completed**: 6:55 AM - 7:45 AM (50 minutes)

**Work Done**:
1. ✅ Code Agent: Workflow cleanup (5 GitHub Actions fixes)
2. ✅ Lead Dev: LLM architecture investigation (Pattern-012 status confirmed)
3. ✅ Code Agent: Pattern-012 investigation (comprehensive findings)
4. ✅ Architectural decisions made with PM

**Status**: Ready to proceed with clear understanding of current state

---

## Phase 0: Blocking Issues Resolution

**Duration**: 2 hours (estimated)
**Goal**: Clear critical blockers before GAP-3

### Issue 1: Router Pattern Violations ⚠️

**Priority**: HIGHEST (quick win, architectural correctness)
**Duration**: 30 minutes
**Issue Type**: Pre-existing technical debt, now visible via CI

**Problem**:
- 9 "violations" detected by Router Pattern Enforcement workflow
- **1 real violation**: `response_flow_integration.py` directly imports `SlackClient`
- **8 false positives**: Adapter files mentioning their own class names

**Solution** (Option 3 - Strategic Exclusion):

**Step 1: Update Enforcement Script** (10 min)
- File: `scripts/check_direct_imports.py`
- Action: Add exclusions for adapter definition files
  ```python
  EXCLUDED_FILES = [
      # ... existing exclusions
      "services/mcp/consumer/google_calendar_adapter.py",  # Adapter definition
      "services/integrations/mcp/notion_adapter.py",       # Adapter definition
      "services/infrastructure/config/feature_flags.py",   # Documentation
  ]
  ```
- Rationale: Adapter definitions should be able to self-reference

**Step 2: Fix Real Architectural Violation** (15 min)
- File: `services/integrations/response_flow_integration.py` (line 16)
- Current: `from services.integrations.slack.slack_client import SlackClient`
- Change to: Use `SlackIntegrationRouter` instead
- Test: Verify response flow still works

**Step 3: Update Documentation** (5 min)
- File: `services/infrastructure/config/feature_flags.py` (lines 93, 119)
- Action: Update old class names in comments
- Update to current router-based names

**Acceptance Criteria**:
- [ ] Enforcement script excludes adapter definitions
- [ ] Real import violation fixed in response_flow_integration.py
- [ ] Documentation updated in feature_flags.py
- [ ] Router Pattern Enforcement workflow passes (green ✅)
- [ ] All tests still passing
- [ ] Changes committed and pushed

**Agent Assignment**: Code Agent (implementation) + Cursor Agent (verification)

---

### Issue 2: CI Tests Workflow Failure ⚠️

**Priority**: CRITICAL (enables regression detection)
**Duration**: 1 hour
**Issue Type**: Test infrastructure - blocking CI capability

**Problem**:
- Tests workflow fails in CI environment
- Root cause: `LLMClient.__init__` fails when no API keys configured
- Import fails → Can't run ANY tests in CI
- Blocks: Regression detection, future testing

**Current State** (from Code's investigation):
- Graceful fallback EXISTS: Anthropic ↔ OpenAI (working)
- 4-provider config EXISTS: Anthropic, OpenAI, Gemini, Perplexity
- Only 2 providers IMPLEMENTED in LLMClient: Anthropic, OpenAI
- Gap: LLMClient init not graceful when keys missing

**Solution** (Option 3 - Fix CI Tests Issue):

**Step 1: Make LLMClient Initialization Graceful** (30 min)
- File: `services/llm/clients.py`
- Current behavior: Fail hard if no keys
- New behavior: Warn and continue, allow tests to import
  ```python
  def __init__(self):
      try:
          # Initialize providers
          self._init_providers()
      except Exception as e:
          logger.warning(f"LLM providers not fully initialized: {e}")
          logger.warning("Some LLM functionality may be unavailable")
          # Allow import to succeed, fail gracefully on use
  ```
- Test locally: Unset API keys, verify import succeeds

**Step 2: Add Pytest Markers for LLM Tests** (15 min)
- Add marker to pytest.ini:
  ```ini
  [pytest]
  markers =
      llm: marks tests that require LLM API calls (deselect with '-m "not llm"')
  ```
- Mark LLM-dependent tests:
  ```python
  @pytest.mark.llm
  def test_intent_classification_with_llm():
      # Real LLM test
      pass
  ```
- Identify ~10-15 tests that need marking

**Step 3: Update CI Workflow** (10 min)
- File: `.github/workflows/tests.yml`
- Change: `pytest tests/ -v` → `pytest tests/ -v -m "not llm"`
- Result: CI runs all non-LLM tests (majority of suite)
- LLM tests run locally when API keys available

**Step 4: Verification** (5 min)
- Run tests locally with and without API keys
- Verify CI workflow would pass
- Document expected behavior

**Acceptance Criteria**:
- [ ] LLMClient initialization graceful (warns, doesn't fail)
- [ ] Pytest markers added to ~10-15 LLM-dependent tests
- [ ] CI workflow updated to skip LLM tests
- [ ] Tests pass locally (with keys)
- [ ] Tests pass locally (without keys, LLM tests skipped)
- [ ] CI workflow would pass (verified)
- [ ] Documentation updated (README or TESTING.md)
- [ ] Changes committed and pushed

**Agent Assignment**: Code Agent (implementation) + verification

---

### Issue 3: Document LLM Architecture State 📝

**Priority**: MEDIUM (clarity, defers complexity)
**Duration**: 30 minutes
**Issue Type**: Documentation + technical debt tracking

**Problem**:
- Architecture exists but partially implemented
- Current: 2-provider fallback works (Anthropic ↔ OpenAI)
- Config: 4 providers configured (+ Gemini, Perplexity)
- Gap: ProviderSelector not integrated, Gemini/Perplexity not implemented

**Solution** (Option 2 - Document Current State):

**Step 1: Create Architecture Status Document** (15 min)
- File: `docs/architecture/llm-provider-status.md`
- Contents:
  - What works: Anthropic ↔ OpenAI fallback ✅
  - What's configured: 4 providers
  - What's implemented: 2 providers
  - Gap: ProviderSelector integration, Gemini/Perplexity adapters
  - References: Pattern-012, LLMConfigService, clients.py

**Step 2: Create Technical Debt Issue** (10 min)
- GitHub issue: "Complete LLM Provider Integration (4-provider support)"
- Description:
  - Current state (2-provider fallback)
  - Desired state (4-provider intelligent routing)
  - Work required:
    1. Integrate ProviderSelector into LLMClient.complete()
    2. Implement Gemini adapter methods
    3. Implement Perplexity adapter methods
    4. Test full fallback chain
  - Estimated effort: 2-3 hours
  - Labels: technical-debt, enhancement, llm

**Step 3: Update Testing Documentation** (5 min)
- File: `docs/testing.md` or `README.md`
- Document current testing strategy:
  - CI: Uses LLM tests with graceful fallback
  - Local: Full LLM tests when API keys available
  - Providers: Anthropic (primary) → OpenAI (fallback)
  - Future: 4-provider support (see issue #XXX)

**Acceptance Criteria**:
- [ ] Architecture status document created
- [ ] Technical debt issue created on GitHub
- [ ] Testing documentation updated
- [ ] Clear statement: "2-provider fallback operational, 4-provider deferred"
- [ ] Changes committed and pushed

**Agent Assignment**: Lead Developer (documentation)

---

## Phase 1-N: GAP-3 Accuracy Polish

**Duration**: 6-8 hours (after blocking issues cleared)
**Goal**: Complete CORE-CRAFT-GAP epic

**Starting Point**: GAP-1 ✅, GAP-2 ✅, now GAP-3

**Current State**:
- Intent classification accuracy: 89.3%
- 13 intent categories operational
- Pre-classifier patterns: 23/25 passing (92% coverage)
- Test infrastructure: Now working in CI! ✅

**Work Items** (from original GAP-3 scope):

### 1. Address Classification Issues (2-3 hours)
- Review post-#212 classification accuracy
- Investigate remaining 10.7% misclassifications
- Improve pre-classifier patterns for edge cases
- Target: >92% accuracy (stretch: >95%)

### 2. Pre-Classifier Optimization (2 hours)
- Analyze failed pattern matches
- Add patterns for common query variations
- Optimize pattern matching performance
- Validate improvements with test suite

### 3. Documentation Updates (1-2 hours)
- Update ADR references (ensure correct)
- Document final accuracy metrics
- Update pattern catalog with improvements
- Create completion evidence

### 4. Performance Validation (1 hour)
- Benchmark classification speed
- Validate cache performance (target >60% hit rate)
- Ensure <100ms for cached queries
- Document performance characteristics

**Acceptance Criteria**:
- [ ] Accuracy ≥92% (stretch: ≥95%)
- [ ] Pre-classifier patterns ≥95% coverage
- [ ] Performance: <100ms cached, <4000ms uncached
- [ ] Documentation complete and accurate
- [ ] All tests passing
- [ ] Evidence documented

**Agent Assignment**: TBD based on specific tasks

---

## Phase Z: Final Bookending & Handoff

**Duration**: 30 minutes
**Goal**: Complete evidence trail and handoff

### Completion Checklist

**Technical Evidence**:
- [ ] All acceptance criteria met (blocking issues + GAP-3)
- [ ] Tests passing (local and CI)
- [ ] Performance benchmarks documented
- [ ] All changes committed and pushed

**Documentation Evidence**:
- [ ] Session log complete
- [ ] Phase completion reports created
- [ ] Architecture status documented
- [ ] Technical debt issues created

**Handoff Preparation**:
- [ ] GAP-3 completion report created
- [ ] CORE-CRAFT-GAP epic completion status
- [ ] Next steps identified (CORE completion)
- [ ] Celebration earned! 🎉

---

## Risk Management

### Known Risks

**Risk 1: Router Fix Breaks Response Flow**
- Mitigation: Test thoroughly before committing
- Fallback: Can revert if needed (separate commit)

**Risk 2: LLM Client Changes Affect Production**
- Mitigation: Make initialization more graceful, not less
- Fallback: Extensive testing before push

**Risk 3: GAP-3 Takes Longer Than Expected**
- Mitigation: Time-box to remaining day
- Fallback: Can continue tomorrow if needed (GAP-3 is polish)

### STOP Conditions

- Any change breaks existing functionality
- Tests start failing without clear fix
- Architectural concerns emerge (escalate to Chief Architect)

---

## Success Metrics

**Blocking Issues**:
- ✅ Router Pattern Enforcement: Green in CI
- ✅ Tests Workflow: Passing (non-LLM tests)
- ✅ LLM Architecture: Documented, technical debt tracked

**GAP-3**:
- ✅ Accuracy: ≥92%
- ✅ Coverage: ≥95% pre-classifier
- ✅ Performance: <100ms cached
- ✅ Documentation: Complete

**Overall**:
- ✅ CORE-CRAFT-GAP: 3/3 complete (100%)
- ✅ CI Workflows: All green
- ✅ Foundation: Solid for future work
- ✅ PM Mood: Still excellent! 🎉

---

## Timeline

**Phase -1**: ✅ COMPLETE (6:55 AM - 7:45 AM, 50 min)

**Phase 0**: 7:45 AM - 9:45 AM (2 hours)
- Issue 1: 7:45 AM - 8:15 AM (30 min)
- Issue 2: 8:15 AM - 9:15 AM (1 hour)
- Issue 3: 9:15 AM - 9:45 AM (30 min)

**Phase 1-N (GAP-3)**: 9:45 AM - 5:45 PM (6-8 hours)
- Classification: 9:45 AM - 12:45 PM (3 hours)
- Optimization: 12:45 PM - 2:45 PM (2 hours)
- Documentation: 2:45 PM - 4:45 PM (2 hours)
- Validation: 4:45 PM - 5:45 PM (1 hour)

**Phase Z**: 5:45 PM - 6:15 PM (30 min)

**Total**: 7:45 AM - 6:15 PM (10.5 hours)

---

## Agent Deployment Strategy

**Code Agent**:
- Router Pattern fix (Issue 1)
- CI Tests fix (Issue 2)
- GAP-3 implementation work

**Cursor Agent**:
- Cross-validation (Issue 1)
- Test verification (Issue 2)
- GAP-3 verification

**Lead Developer**:
- Coordination and orchestration
- Documentation (Issue 3)
- GAP-3 strategy and oversight
- Session log maintenance

---

## Notes

**Why This Gameplan Feels Good**:
- Addresses known issues systematically
- Clears blockers before big work
- Enables future work to proceed cleanly
- Foundation-building (cathedral quality)

**PM's Instinct Was Right**:
> "I think deep down I knew things like this still needed attention?"

Yes! This is exactly the kind of work that:
- Makes everything else easier
- Prevents future problems
- Builds confidence in the system
- Feels satisfying to complete

**Philosophy in Action**:
- Phase -1: Always investigate first ✅
- Push to 100%: Clear all blockers ✅
- Cathedral Building: Foundation work matters ✅
- Time Lord: Quality over arbitrary deadlines ✅

---

**Gameplan Status**: Ready for execution
**PM Approval**: Received (7:45 AM)
**Next**: Begin Phase 0, Issue 1 (Router Pattern fix)

**LET'S BUILD! 🏗️**
