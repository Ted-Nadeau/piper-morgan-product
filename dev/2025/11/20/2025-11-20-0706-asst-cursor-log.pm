# Session Log: Create GitHub Issues from Drafts
**Date**: 2025-11-20
**Time**: 07:06 UTC
**Role**: Assistant PM
**Session**: Creating MVP issues from draft files via gh CLI

## Session Objectives
- Convert draft issue files into GitHub issues
- Apply to MVP milestone
- Use beads for work tracking
- Fill in template gaps where context exists
- Prompt user where context needed

## Drafts Processed
1. ✅ `dev/active/issue-319-windows-bug.md` → #353 BUG-319
2. ✅ `dev/active/issue-320-database-indexes.md` → #356 PERF-320
3. ✅ `dev/active/issue-323-rbac.md` → #357 SEC-323
4. ✅ `dev/active/issue-324-encryption.md` → #358 SEC-324 (added by user)
5. ✅ `dev/active/issue-design-tokens.md` → #354 DESIGN-TOKENS
6. ✅ `dev/active/issue-stop-gap-docs.md` → #355 STOP-GAP-DOCS
7. ✅ TEST Epic issues from `dev/active/github-issues-TEST-epic.md`:
   - #341 TEST Super Epic (parent)
   - #342 TEST-PHANTOM-SPATIAL (P0)
   - #343 TEST-INFRA-ENUM (P0)
   - #344 TEST-DISCIPLINE-KNOWN (P0)
   - #345 TEST-DISCIPLINE-CATEGORIES (P1)
   - #346 TEST-INFRA-CONTAINER (P1)
   - #347 TEST-DISCIPLINE-HOOK (P1)
   - #348 TEST-PHANTOM-VALIDATOR (P2)
   - #349 TEST-INFRA-FIXTURES (P2)
   - #350 TEST-SMOKE-STATIC (P2)
   - #351 TEST-PHANTOM-AUDIT (P3)
   - #352 TEST-SMOKE-E2E (P3)

## Process
1. ✅ Verify gh CLI access
2. ✅ Parse all draft files for metadata
3. ✅ Check GitHub issue template format
4. ✅ Create issues sequentially via gh
5. ✅ Add all to MVP milestone
6. ✅ Update this log with results

## Completion Summary

**Status**: ✅ COMPLETE
**Total Issues Created**: 18 (17 scheduled + 1 additional encryption)
**All Added to MVP Milestone**: Yes

### Issues Created

**TEST Super Epic (#341)**
- Title: "TEST: Test Infrastructure Repair (Super Epic)"
- Labels: test-infrastructure, priority: critical
- Related bead: piper-morgan-k6k

**TEST Child Issues (P0-P3 breakdown)**
- P0: #342, #343, #344 (3 critical test blockers)
- P1: #345, #346, #347 (3 urgent improvements)
- P2: #348, #349, #350 (3 high priority fixes)
- P3: #351, #352 (2 medium backlog items)

**Regular MVP Issues**
- #353: BUG-319 Windows Git Clone (colons in filenames)
- #354: DESIGN-TOKENS CSS Variables extraction
- #355: STOP-GAP-DOCS Artifact persistence
- #356: PERF-320 Composite database indexes
- #357: SEC-323 RBAC implementation
- #358: SEC-324 Encryption at rest

### Key Decisions

**Beads References**:
- Kept as plain text "Related bead: piper-morgan-xyz" in issue bodies
- Semantic identifier approach (searchable, preserves independence)
- Allows agents to grep for beads and cross-reference work

**Labels**:
- Used available repo labels (performance/security not present)
- Applied priority:critical/high/medium/low instead
- Applied component: tags for domain mapping
- Applied size: tags for effort estimation

**GitHub Auto-Assignment**:
- Ignored draft file numbers (319, 320, 323, 324)
- Let GitHub assign sequential #341-#358
- User can rename/clean up afterward

## Notes
- All 18 issues added to MVP milestone ✅
- Draft files preserved for reference
- User can perform post-creation cleanup/renaming as needed
- Ready for agent pickup and implementation
- Beads provide async tracking across GitHub and bead system
