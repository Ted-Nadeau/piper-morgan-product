# Audit: #756 Issue against bug_report_alpha.md template

**Date**: 2026-02-02
**Document**: GitHub Issue #756
**Template**: `.github/ISSUE_TEMPLATE/bug_report_alpha.md`

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Bug Description | ✅ | "Pre-existing test failure discovered during #747 validation" |
| Steps to Reproduce | ❌ | Missing - no steps provided |
| Expected Behavior | ⚠️ | Implied but not explicit |
| Actual Behavior | ✅ | Error message shown |
| Environment | ❌ | Missing |
| Screenshots/Logs | ✅ | Error message included |
| Severity | ❌ | Missing checkboxes |
| Additional Context | ⚠️ | Analysis section covers this partially |

---

## Summary

- ✅ Present: 3
- ⚠️ Partial: 2
- ❌ Missing: 3

---

## Investigation Results

### Root Cause Analysis

**Test**: `test_identical_filenames_different_times`

The test creates 3 files with identical names ("report.pdf") but different upload times, then expects the FileResolver to return the most recent file.

**Expected by test** (line 125):
```python
file_id, confidence = await resolver.resolve_file_reference(intent, owner_id)
assert file_id == files[0].id  # Most recent
```

**Actual behavior**: FileResolver raises `AmbiguousFileReferenceError` because:

1. Files with identical names have identical name scores
2. Files with identical types have identical type scores
3. Recency scores differ but only by ~0.3 * time_decay (small difference for hourly gaps)
4. Usage scores are all 0 (no usage history)
5. The score difference is < 0.2 threshold → AmbiguousFileReferenceError

### Five Whys

1. **Why does the test fail?**
   - FileResolver raises AmbiguousFileReferenceError instead of returning the most recent file

2. **Why is AmbiguousFileReferenceError raised?**
   - Score difference between top files is < 0.2 threshold (line 117-121 in file_resolver.py)

3. **Why is the score difference < 0.2?**
   - Files have identical names (same name_score), identical types (same type_score), no usage history (all 0), only recency differs slightly

4. **Why was the test written to expect resolution?**
   - Test assumes "most recent wins" tiebreaker exists, but it doesn't

5. **Why doesn't "most recent wins" tiebreaker exist?**
   - Design decision: FileResolver prefers to ask for clarification when ambiguous rather than guess

### Decision: Bug in Test, Not in Code

The FileResolver's behavior is **correct by design**:
- When multiple files have similar relevance scores, ambiguity is real
- Asking user for clarification is better than guessing wrong
- The ambiguity threshold (0.2) prevents false confidence

The test's expectation is **incorrect**:
- Expecting automatic "most recent wins" tiebreaker
- This was never implemented in FileResolver

### Options

**Option A: Fix the Test (Recommended)**
Update test to expect AmbiguousFileReferenceError when identical filenames exist, similar to how `test_special_characters_in_filename` handles ambiguity.

**Option B: Add Tiebreaker to FileResolver**
Add "most recent wins" as final tiebreaker when scores are within ambiguity threshold. This changes product behavior.

**Recommendation**: Option A - The test should match the actual design intent.

---

## Required Fixes to Issue

### 1. Add Steps to Reproduce

```markdown
## Steps to Reproduce

1. Run `pytest tests/unit/services/test_file_resolver_edge_cases.py::TestFileResolverEdgeCases::test_identical_filenames_different_times -xvs`
2. Test creates 3 files with identical names but different upload times
3. FileResolver raises AmbiguousFileReferenceError instead of returning most recent
```

### 2. Add Expected vs Actual Behavior

```markdown
## Expected Behavior (per test)
FileResolver should return the most recent file when multiple files have identical names.

## Actual Behavior
FileResolver raises AmbiguousFileReferenceError because files have similar relevance scores (< 0.2 difference).
```

### 3. Add Environment

```markdown
## Environment
- Test framework: pytest
- Python: 3.12
- Database: PostgreSQL (async via asyncpg)
```

### 4. Add Severity Checkbox

```markdown
## Severity
- [ ] Blocker
- [ ] Major
- [x] Minor - Test expectation doesn't match design
- [ ] Enhancement
```

### 5. Update Analysis with Root Cause

Current analysis is good but should explicitly state the decision:
- This is a **test bug**, not a code bug
- FileResolver behavior is correct by design
- Test should be updated to expect AmbiguousFileReferenceError

---

## Status: READY FOR GAMEPLAN

Issue needs update, then gameplan for test fix.
