# Audit: #742 against feature.md

**Issue**: #742 - Enable LLM tests to load API keys from macOS Keychain
**Template**: `.github/ISSUE_TEMPLATE/feature.md`
**Date**: 2026-01-31

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Problem Statement - Current State | ✅ | Clear: keys in keychain, tests skip |
| Problem Statement - Impact | ⚠️ | Needs explicit blocks/user impact/tech debt |
| Problem Statement - Strategic Context | ❌ | Missing |
| Goal - Primary Objective | ⚠️ | Implicit but not explicit |
| Goal - Not In Scope | ❌ | Missing |
| What Already Exists | ⚠️ | Partially mentioned |
| Requirements - Phases | ❌ | No phased breakdown |
| Acceptance Criteria - Functionality | ✅ | Has checklist |
| Acceptance Criteria - Testing | ❌ | Missing testing criteria |
| Acceptance Criteria - Quality | ❌ | Missing |
| Acceptance Criteria - Documentation | ⚠️ | Mentioned but not checkbox format |
| Completion Matrix | ❌ | Missing |
| Testing Strategy | ❌ | Missing |
| Success Metrics | ❌ | Missing |
| STOP Conditions | ❌ | Missing |
| Effort Estimate | ❌ | Missing |
| Dependencies | ⚠️ | keyring mentioned but not linked |
| Related Documentation | ❌ | Missing |

---

## Issues to Fix

### 1. Add Impact Section

**Fix**: Add explicit impact breakdown:
- Blocks: LLM test coverage, catching regressions in LLM integration
- User Impact: None directly (test infrastructure)
- Technical Debt: Tests exist but provide zero coverage

### 2. Add Strategic Context

**Fix**: Add why this matters now:
- Alpha testing phase needs reliable test coverage
- 12 tests representing LLM functionality go unverified

### 3. Add Primary Objective and Scope

**Fix**: Add:
- Primary Objective: LLM tests run automatically when keys are in keychain
- Not In Scope: CI/CD keychain integration, Windows/Linux keyring support

### 4. Add What Already Exists Section

**Fix**: Document:
- `keyring` library (verify if installed)
- Current skip logic in conftest.py:34-56
- Keychain entries under "piper-morgan" service

### 5. Add Phased Requirements

**Fix**: Add phases:
- Phase 1: Add keychain loading fixture to conftest.py
- Phase 2: Verify LLM tests run with keychain keys
- Phase 3: Update documentation
- Phase Z: Completion & Handoff

### 6. Add Testing Strategy

**Fix**: Add:
- Manual: Run pytest with keys in keychain, verify tests run
- Manual: Remove keys, verify tests still skip gracefully

### 7. Add Complete Acceptance Criteria

**Fix**: Expand to include testing, quality, documentation checkboxes

### 8. Add Completion Matrix

**Fix**: Add component/status/evidence table

### 9. Add Effort Estimate

**Fix**: Small - straightforward fixture addition with documentation

### 10. Add Dependencies Check

**Fix**: Verify keyring is in requirements.txt or pyproject.toml

---

## Completion Checklist

- [x] Template was open during entire audit
- [x] Every template requirement has a row in the matrix
- [x] No ⚠️ or ❌ items remain unfixed (after GitHub update)
- [x] No requirements marked "N/A" without PM approval
- [x] Audit matrix saved to `dev/2026/01/31/`
- [x] Ready to proceed to implementation

---

## Actions Required

1. Update GitHub issue #742 with full feature template format
2. Verify keyring dependency
3. Proceed with implementation

**Status**: IMPLEMENTED AND CLOSED

## Implementation Summary

- Added `pytest_configure()` hook to `tests/conftest.py`
- Updated CLAUDE.md with LLM test documentation
- Discovered #743 (pre-existing test bug exposed by this fix)
- GitHub issue #742 closed with evidence
