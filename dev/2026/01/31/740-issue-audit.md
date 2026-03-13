# Audit: #740 against bug_report_alpha.md

**Issue**: #740 - BUG: Entity Extraction Regex Over-Matching in Context Tracker
**Template**: `.github/ISSUE_TEMPLATE/bug_report_alpha.md`
**Date**: 2026-01-31

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Bug Description | ✅ | Clear: regex patterns too aggressive, matching "i" and "my" as user entities |
| Steps to Reproduce | ⚠️ | Code path described but no literal steps. Test input provided. |
| Expected Behavior | ✅ | "2 entities (issue:#456, project:myapp)" |
| Actual Behavior | ✅ | "4 entities extracted" with full list |
| Environment | ❌ | Missing - but this is a code bug, not environment-specific |
| Screenshots/Logs | ✅ | Code snippets and test output equivalent |
| Severity | ❌ | Missing severity checkbox |
| Additional Context | ✅ | Related bead, related issue #248, 3 fix options |

---

## Issues to Fix

### 1. Steps to Reproduce (⚠️ → ✅)

Need explicit reproduction steps. Current description is code-focused.

**Fix**: Add:
```
1. Run: `python -m pytest tests/unit/services/conversation/test_context_tracker.py::TestEnhancedContextTracker::test_entity_extraction_and_tracking -v -p no:randomly`
2. Observe: Test is skipped
3. Remove `@pytest.mark.skip` decorator from test
4. Re-run test
5. Observe: AssertionError - Expected 2 entities, got 4
```

### 2. Environment (❌ → ✅)

**Fix**: Add:
```
## Environment
- **Not environment-specific**: This is a regex logic bug in `context_tracker.py`
- **Python version**: 3.11+
- **Piper Morgan Version**: 0.8.5.1
```

### 3. Severity (❌ → ✅)

**Fix**: Add:
```
## Severity
- [x] Minor - Workaround exists (tests skipped, feature still works)
```

This is Minor because:
- Tests are skipped (workaround exists)
- The entity extraction still works, just extracts extra noise
- No user-facing impact currently

---

## Completion Checklist

- [x] Template was open during entire audit
- [x] Every template requirement has a row in the matrix
- [x] No ⚠️ or ❌ items remain unfixed
- [x] No requirements marked "N/A" without PM approval
- [x] Audit matrix saved to `dev/2026/01/31/`
- [x] Ready to proceed to next phase

---

## Actions Completed

1. ✅ Added Steps to Reproduce section
2. ✅ Added Environment section
3. ✅ Added Severity section (Minor)
4. ✅ GitHub issue #740 updated

**Status**: Issue audit COMPLETE - ready for gameplan phase.
