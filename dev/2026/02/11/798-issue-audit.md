# Issue Audit: #798 against bug_report_alpha.md

**Issue**: [DB] Schema validation reports 6 mismatches
**Template**: `.github/ISSUE_TEMPLATE/bug_report_alpha.md`
**Date**: 2026-02-11

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Bug Description | ✅ | Clear table of 6 mismatches |
| Steps to Reproduce | ⚠️ | Implicit (run schema validator) |
| Expected Behavior | ❌ | Missing |
| Actual Behavior | ✅ | Schema drift warning |
| Severity | ✅ | HIGH priority label |
| Acceptance Criteria | ✅ | 4 clear criteria |

## Investigation Notes

Several of these may already be fixed:
1. DateTime vs timestamptz - We just ran d73b3722eb03 which converts to timestamptz
2. todo_lists missing - Need to check if migration exists
3. embedding_vector type - Need to investigate

## Assessment

Need to investigate current state - some issues may be resolved by migrations we just fixed.
