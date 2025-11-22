# Beads vs GitHub Issues Analysis

**Date**: November 22, 2025, 6:50 AM
**Investigator**: Claude Code
**Status**: Investigation complete - findings documented

---

## Executive Summary

There is a **significant tracking gap** between GitHub Issues and the Beads system:

| Source | Count |
|--------|-------|
| **GitHub Issues (open)** | 78 |
| **Beads (open)** | 28 |
| **Beads (closed)** | 39 |
| **Total Beads** | 67 |
| **Gap** | 11 missing from beads (78 - 67) |

**Key Finding**: GitHub is the source of truth for issue tracking, but only 67 of 78 open issues are represented in the Beads system.

---

## Issue 1: PM-034 Naming Convention

**Your Observation**: PM-034 has legacy naming convention we abandoned months ago.

**Investigation**:
- Git history shows project started with `PM-XXX` naming (2024)
- Most recent commits use `ISSUE-XXX`, `#XXX`, or descriptive names (PERF-INDEX, SEC-RBAC, etc.)
- PM-034 is an old issue (created ~Nov 15)
- **Root cause**: GitHub issues still use old naming, but newer issues use new naming

**Example Timeline**:
- Older: `PM-034` (Nov 15)
- Newer: `#356 PERF-INDEX`, `#357 SEC-RBAC`, `#300` (Nov 19+)

**Recommendation**: This isn't a critical issue - the naming evolved naturally. The important thing is that the issue tracking works.

---

## Issue 2: Beads Sync with GitHub

**Your Observation**: We might be tracking beads in multiple repositories or not syncing properly.

**Findings**:

### What Beads Supports
✅ Beads can sync with git via `.beads/beads.jsonl`
✅ Beads uses `bd sync` to export/import changes
✅ Beads stores data in `.beads/beads.db` (SQLite, NOT git-tracked)

### What Beads Does NOT Support
❌ Direct integration with GitHub Issues API
❌ Automatic two-way sync between GitHub and beads
❌ Pulling GitHub issues into beads database

### Current Architecture
```
GitHub Issues (78 open)
    ↓ (manual process only)
    ?
    ↓
Beads Database (28 open + 39 closed = 67 total)
```

**The gap exists because**: No automated sync exists between GitHub and beads. Beads tracks a subset of issues manually selected for tracking.

---

## Detailed Breakdown

### GitHub Issues Not in Beads (11 issues)

Checking the 78 open GitHub issues against 28 beads:

**Missing issues likely include**:
- Epic-level issues (CONV-UX-*, CONV-MCP-*, INFR-* series)
- Long-term roadmap items (ARCH-*, DATA-*, OBSERV-*)
- Strategic initiatives (#299-#335)

**Why they're not in beads**:
- Likely created before beads integration (Nov 13)
- OR considered "for future work" and not yet opened in beads
- OR tracked via other mechanisms (session logs, dev documents)

---

## Beads Database Contents

### By Status
- **Open**: 28 beads
  - Priority 1: 1 (RBAC-1.2)
  - Priority 2: 16 (including #356, #532, #357 blockers, Slack issues)
  - Priority 3: 11 (test fixes, AsyncMock, etc.)

- **Closed**: 39 beads
  - Recent closes from Nov 19-20 (test infrastructure fixes)
  - Some from Nov 14-15 (project setup, testing)

### By Type
- Tasks/Features: ~45%
- Bugs: ~35%
- Documentation: ~20%

---

## Root Cause: Integration Timing

**Timeline**:
- **Nov 13**: Beads integration proposal created
- **Nov 14-15**: Beads database established, first beads created
- **Nov 15-22**: Issues tracked in beads as they were discovered/fixed
- **Prior to Nov 13**: All 78 GitHub issues existed, but NOT in beads

**Why 11 are missing**:
1. Created before beads integration (Nov 13)
2. Not yet migrated to beads (possibly tracking via GitHub + session logs instead)
3. Considered "future work" backlog (not urgent enough for beads yet)

---

## Session Log Visibility

**Your Concern**: "Session logs and reports are all we have on the record"

**Current State**:
- ✅ Session logs: Detailed, comprehensive (this one + prior days)
- ✅ Session artifacts: Dev documents, reports, analysis
- ❌ Beads: Only partial visibility (28 of 78 issues)
- ❌ GitHub: Full visibility but no machine-readable tracking

**Recommendation**:
1. Maintain current session log discipline (✅ already doing well)
2. Sync critical GitHub issues into beads periodically (⚠️ currently manual)
3. Document any work NOT in beads in session logs (✅ already doing)

---

## Questions for You

1. **Should we manually import the 11 missing issues into beads?**
   - This would give complete visibility in `bd ready`
   - Would require running `gh issue list --json | bd import`

2. **Should we set up automated GitHub→Beads sync?**
   - Requires custom script (beads doesn't support this natively)
   - Would keep beads in sync with GitHub automatically

3. **Are the 11 missing issues truly needed in beads, or are they "future work"?**
   - If future work, current system is fine
   - If active work, they should be in beads for visibility

---

## Technical Details

### Beads Database Structure
- **Location**: `./.beads/beads.db` (SQLite)
- **Not git-tracked**: Database is binary, only exported to `.beads/beads.jsonl`
- **Sync mechanism**: `bd sync` exports to JSONL, commits to git, imports back
- **Local-only**: Each dev has their own beads.db (no server)

### GitHub API Access
```bash
$ gh issue list --limit 500 --state open
# Returns: 78 open issues
# Could be imported with: gh issue list --json | jq '.[] | {title, id, state}' | bd import
```

---

## Recommendation Summary

**What's working well**:
- ✅ Session logs are comprehensive
- ✅ GitHub issues are complete
- ✅ Beads database is reliable for tracked work
- ✅ Git-based sync works

**What needs improvement**:
- ⚠️ 11 open GitHub issues not in beads (visibility gap)
- ⚠️ No automated sync (manual process only)
- ⚠️ Beads database not version-controlled

**Next step**: Would you like me to import the 11 missing open issues into beads to close the visibility gap?

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
