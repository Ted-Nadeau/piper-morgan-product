# Audit: #743 against bug_report_alpha.md

**Issue**: #743 - Fix test_pm039_patterns - container initialization issue
**Template**: `.github/ISSUE_TEMPLATE/bug_report_alpha.md`
**Date**: 2026-01-31
**Skill**: audit-cascade v1.0

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Bug Description | ✅ | Clear: test fails with ContainerNotInitializedError |
| Steps to Reproduce | ❌ | Missing numbered steps |
| Expected Behavior | ❌ | Missing |
| Actual Behavior | ❌ | Missing (only "Root Cause" present) |
| Environment | ❌ | Missing |
| Screenshots/Logs | ⚠️ | Has code snippet but no actual error output |
| Severity | ❌ | Missing severity checkbox |
| Additional Context | ✅ | Has related issues, fix options |

---

## Issues to Fix

### 1. Steps to Reproduce (❌ → ✅)

**Fix**: Add:
```
## Steps to Reproduce

1. Ensure API keys are in macOS Keychain (or run after #742 fix)
2. Run: `python -m pytest tests/unit/services/test_intent_coverage_pm039.py -v`
3. Observe: Test fails with `ContainerNotInitializedError`
```

### 2. Expected Behavior (❌ → ✅)

**Fix**: Add:
```
## Expected Behavior

- Test runs successfully
- IntentClassifier classifies test messages correctly
- Test verifies PM-039 document search patterns work
```

### 3. Actual Behavior (❌ → ✅)

**Fix**: Add:
```
## Actual Behavior

- Test fails with `ContainerNotInitializedError`
- Error: "Container not initialized. Call container.initialize() first."
- IntentClassifier tries to get LLM service from uninitialized singleton container
```

### 4. Environment (❌ → ✅)

**Fix**: Add:
```
## Environment

- **Not environment-specific**: This is a test fixture issue
- **Python version**: 3.11+
- **Piper Morgan Version**: 0.8.5.1
```

### 5. Screenshots/Logs (⚠️ → ✅)

**Fix**: Add actual error output:
```
## Screenshots/Logs

```
E   services.container.exceptions.ContainerNotInitializedError: Container not initialized. Call container.initialize() first.

WARNING  services.intent_service.classifier:classifier.py:766: DeprecationWarning: IntentClassifier: Direct ServiceContainer() access is deprecated. Pass llm_service via constructor. (Issue #322 - ARCH-FIX-SINGLETON)
```
```

### 6. Severity (❌ → ✅)

**Fix**: Add:
```
## Severity

- [x] Minor - Workaround exists (test is skipped)
```

---

## Quality Checklist

- [x] Template was open during entire audit
- [x] Every template requirement has a row in the matrix
- [x] No ⚠️ or ❌ items remain unfixed
- [x] No requirements marked "N/A" without PM approval
- [x] Audit matrix saved to `dev/2026/01/31/`
- [x] Ready to proceed to next phase (gameplan)

---

## Actions Completed

1. ✅ Added Steps to Reproduce (3 numbered steps)
2. ✅ Added Expected Behavior section
3. ✅ Added Actual Behavior section
4. ✅ Added Environment section
5. ✅ Added actual error logs
6. ✅ Added Severity (Minor)
7. ✅ Added Acceptance Criteria
8. ✅ Updated issue title to follow bug convention

**Status**: Issue audit COMPLETE - ready for gameplan phase
