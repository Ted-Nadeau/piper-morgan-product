# Audit Cascade: Test Infrastructure Issues for M1

**Phase**: Issue → Gameplan
**Date**: 2026-03-13
**Auditor**: Lead Developer

---

## Issue #739: TEST-FIX: Fix test_response_handler_observability Complex Mocking

### Audit against feature.md template

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Problem Statement | ⚠️ | Has description but lacks structured Current State / Impact / Strategic Context |
| Goal / Primary Objective | ⚠️ | Implicit (make test pass) but not stated as one-sentence objective |
| Not In Scope | ❌ | Missing |
| What Already Exists | ⚠️ | Mentions the test exists and is skipped, but doesn't list infrastructure |
| Requirements / Phases | ❌ | No phases, no tasks |
| Acceptance Criteria | ❌ | No acceptance criteria checklist |
| Testing Strategy | ❌ | Ironic for a test fix — no test strategy |
| Success Metrics | ❌ | Missing |
| STOP Conditions | ❌ | Missing |
| Effort Estimate | ❌ | Missing |
| Dependencies | ❌ | Missing |
| Completion Matrix | ❌ | Missing |

**Overall**: ❌ **Thin** — this is more of a note than an issue. Needs substantial enrichment before gameplan.

### Action Items
1. Investigate the test to understand actual root cause
2. Determine if this is worth fixing or if the test should be removed/rewritten
3. Enrich issue with structured sections before proceeding

---

## Issue #738: TEST-INFRA: Enable Attention System Time Simulation Tests (3 tests)

### Audit against feature.md template

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Problem Statement | ✅ | Clear: dataclass captures real datetime.now at definition time, mocking doesn't work |
| Goal / Primary Objective | ⚠️ | Implicit — enable 3 skipped tests |
| Not In Scope | ❌ | Missing |
| What Already Exists | ⚠️ | Mentions the tests exist but are skipped; doesn't list infrastructure |
| Requirements / Phases | ❌ | No structured phases |
| Acceptance Criteria | ❌ | Missing |
| Testing Strategy | ⚠️ | The issue IS about testing but no verification approach listed |
| Success Metrics | ❌ | Missing |
| STOP Conditions | ❌ | Missing |
| Effort Estimate | ❌ | Missing — likely Small |
| Dependencies | ❌ | Missing |
| Completion Matrix | ❌ | Missing |

**Overall**: ⚠️ **Good problem description, thin on structure.** Root cause is well-identified. Fix approach is clear (inject datetime factory). Small issue.

### Action Items
1. Verify the 3 tests and confirm root cause
2. Determine fix approach (datetime factory injection vs freezegun vs other)
3. Enrich issue minimally — this is small enough to gameplan directly

---

## Issue #247: BUG-TEST-ASYNC: AsyncSessionFactory causes event loop conflicts

### Audit against feature.md template

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Problem Statement | ✅ | Excellent — root cause identified, explained clearly |
| Goal / Primary Objective | ⚠️ | States "FIX IMPLEMENTED" in status but issue is still OPEN |
| Not In Scope | ❌ | Missing |
| What Already Exists | ✅ | Root cause analysis, fix approach documented |
| Requirements / Phases | ❌ | No phases |
| Acceptance Criteria | ❌ | Missing |
| Testing Strategy | ❌ | Missing |
| Success Metrics | ❌ | Missing |
| STOP Conditions | ❌ | Missing |
| Effort Estimate | ❌ | Missing |
| Dependencies | ⚠️ | Mentions "Database schema blocker prevents testing" |
| Completion Matrix | ❌ | Missing |

**Overall**: ⚠️ **Issue says "FIX IMPLEMENTED" but is still open.** Need to verify current state — is the fix actually in place? Is this closeable? The "database schema blocker" note needs investigation.

### Action Items
1. Verify if fix was actually implemented in codebase
2. Check if "database schema blocker" is still present
3. If fixed, close with evidence. If not, determine remaining work.

---

## Issue #352: TEST-SMOKE-E2E: Create core user journey smoke tests

### Audit against feature.md template

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Problem Statement | ❌ | Just a scope list, no current state / impact / strategic context |
| Goal / Primary Objective | ⚠️ | Implicit — "end-to-end tests for critical paths" |
| Not In Scope | ❌ | Missing |
| What Already Exists | ❌ | Missing — do any smoke tests exist? |
| Requirements / Phases | ⚠️ | Has scope list (4 areas) but no structured phases |
| Acceptance Criteria | ⚠️ | Has "10+ journey tests, Run in CI/CD, Catch integration issues" but not detailed |
| Testing Strategy | ❌ | Missing — needs to define what "smoke test" means operationally |
| Success Metrics | ❌ | Missing |
| STOP Conditions | ❌ | Missing |
| Effort Estimate | ❌ | Missing — likely Large |
| Dependencies | ❌ | Missing — depends on running server, database, integrations |
| Completion Matrix | ❌ | Missing |

**Overall**: ❌ **Stub issue.** Needs substantial enrichment. This is a large effort that needs proper scoping before M1 can include it.

### Action Items
1. Determine M1 scope — do we need ALL smoke tests or a critical subset?
2. Check what test infrastructure exists (can we run server in test mode?)
3. Define what "smoke test" means: pytest with live server? httpx against FastAPI app? Playwright?
4. Enrich issue substantially before gameplanning

---

## Issue #375: QA: Manual testing for preference detection system

### Audit against feature.md template

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Problem Statement | ❌ | Just a scenarios list |
| Goal / Primary Objective | ❌ | Missing |
| Not In Scope | ❌ | Missing |
| What Already Exists | ❌ | Missing — does preference detection work? |
| Requirements / Phases | ❌ | Has scenario list but no phases |
| Acceptance Criteria | ❌ | Missing |
| Testing Strategy | ⚠️ | The scenarios ARE the testing strategy but need structure |
| Success Metrics | ❌ | Missing |
| STOP Conditions | ❌ | Missing |
| Effort Estimate | ❌ | Missing |
| Dependencies | ⚠️ | References #248 (CONV-LEARN-PREF) — is that implemented? |
| Completion Matrix | ❌ | Missing |

**Overall**: ❌ **Stub issue.** Also, this is MANUAL QA — is this M1 scope? Needs PM decision on whether this belongs in M1 or later.

### Action Items
1. **PM Decision needed**: Is manual QA testing in M1 scope?
2. Check if #248 preference detection is even implemented
3. If in scope, enrich issue with structured acceptance criteria

---

## TEST-QUALITY: Test Reliability for Production Confidence

**No issue exists.** This was mentioned in the PM's list but has no GitHub issue.

### Action Items
1. **File issue** or determine if this is covered by other issues
2. Define what "test reliability" means concretely (flaky test audit? coverage report? test suite speed?)

---

## Summary

| Issue | Template Conformance | Readiness for Gameplan | Recommended Action |
|-------|---------------------|----------------------|-------------------|
| #739 | ❌ Thin | Not ready | Investigate first, then enrich or close |
| #738 | ⚠️ Good root cause | Near-ready (small) | Quick investigation + gameplan |
| #247 | ⚠️ "Fix implemented"? | Verify state | May be closeable already |
| #352 | ❌ Stub | Not ready | Needs PM scoping decision + enrichment |
| #375 | ❌ Stub | Not ready | PM decision: M1 scope? |
| (no #) | N/A | N/A | File issue or defer |

### Cascade Recommendation

**Before gameplanning, we need**:
1. **Quick investigation** on #247 (may be closeable) and #739 (may be closeable or trivial)
2. **PM decision** on #352 and #375 scope for M1
3. **PM decision** on TEST-QUALITY — file issue or defer?
4. **#738 is ready** for a quick gameplan — small, clear root cause

Shall I start with the investigations (#247 and #739) to determine which are actually actionable?
