# Low-Hanging Fruit Discovery Process

**Date**: November 22, 2025, 6:53 AM
**Purpose**: Systematic method for identifying work Claude Code can tackle without heavy dependencies

---

## Recommended Discovery Process

Instead of manual curation, use this **three-filter approach**:

### Filter 1: Scope (Size)
```bash
# Find small, medium, self-contained issues
gh issue list --state open --json number,title,labels \
  | jq '.[] | select(.labels | any(.name | contains("size: small|size: medium")))'
```

**Why this works**:
- Large issues have more dependencies
- Small/medium issues are faster to validate
- Clear scope = fewer unknowns

### Filter 2: Type (What kind of work)
Look for issues with these patterns:
- **Bug fixes** (isolated problems, no new features needed)
- **Documentation** (ADRs, patterns, comments - low risk)
- **Build/infra** (fixes to CI, paths, config - contained scope)
- **Test cleanup** (test fixes, removing skips - no product logic)

**Avoid these patterns**:
- **Architecture changes** (multi-file refactoring)
- **New integrations** (untested external dependencies)
- **Large features** (UI, new endpoints, core logic)

### Filter 3: Dependencies (Can it be done standalone?)
Before starting, ask:
1. **Does this depend on other open issues?** (Check "Related" or "Blocked by")
2. **Does this touch shared code?** (Might conflict with concurrent work)
3. **Does this need another team's work first?** (RBAC, Slack team assigned)
4. **Does this need fresh database state?** (Might be blocked by migration issues)

---

## Current Low-Hanging Fruit in GitHub

### Tier 1: Immediate (Can start right now)

**#353 - BUILD-WINDOWS-CLONE: Fix Illegal Filename**
- **Size**: Small ⭐
- **Type**: Bug fix (file rename)
- **Scope**: Rename 1 file with colon in directory name
- **Effort**: 5-10 minutes
- **Why it's low-hanging**:
  - Clear problem (colon in Windows path)
  - Clear solution (rename file)
  - No dependencies
  - No code changes needed
- **What to do**:
  1. Find file: `archive/piper-morgan-0.1.1/docs/claude docs 5:30/conversational_refactor.md`
  2. Rename to: `claude docs 530` (remove colon)
  3. Test: `git status` should show rename
  4. Commit with evidence

---

### Tier 2: Quick wins (Small, no blockers)

**#332 - DOCUMENTATION-STORED-PROCS: Document Application-Layer Stored Procedures Pattern (ADR)**
- **Size**: Medium (documentation)
- **Type**: Documentation/ADR
- **Scope**: Write ADR explaining stored procedures pattern already in codebase
- **Effort**: 30-45 minutes
- **Why it's doable**:
  - Pattern already exists in code (just needs documentation)
  - No code changes
  - Clear template (ADR format)
  - High value (documents existing work)

---

### Tier 3: Possible (Depends on investigation)

**#355 - DOCS-STOPGAP: Basic Artifact Persistence**
- **Size**: Medium
- **Type**: Documentation/UX
- **Dependencies**: Need to check if related to #356 work

---

## How to Use This Process

### For Each Session:
1. **Run filter commands** to get current low-hanging fruit
2. **Check Tier 1 issues first** (smallest scope)
3. **Verify no blockers** before starting
4. **Document your choice** in session log
5. **Report findings** if you discover new blockers

### Automated Script (Optional)

Could create a helper script:
```bash
#!/bin/bash
# Find low-hanging fruit issues
gh issue list --state open --json number,title,labels,body \
  | jq '.[] |
    select(
      (.labels | any(.name | contains("size: small"))) or
      (.labels | any(.name | contains("documentation"))) or
      (.labels | any(.name | contains("bug")) and (.labels | any(.name | contains("size: medium"))))
    ) |
    {number, title, labels: (.labels | map(.name))}' \
  | jq -s 'sort_by(.number) | reverse | .[0:10]'
```

---

## My Recommendation

**Start with #353 (Windows filename bug)** because:
1. ✅ Clearly defined problem
2. ✅ Zero dependencies
3. ✅ No code changes needed
4. ✅ Literally a 5-minute fix
5. ✅ Unblocks Windows developers
6. ✅ Great confidence builder for session

Then **look at #332 (ADR documentation)** if you want something with more depth.

---

## What NOT to Do

❌ Avoid #358, #357, #356 - You're already working on these
❌ Avoid SLACK-* issues - Team assigned
❌ Avoid CONV-* issues - Blocked on ORM models (PM-034 Phase 2)
❌ Avoid ARCH-*, DATA-* - Large strategic initiatives
❌ Avoid issues without clear acceptance criteria

---

## Your Call

**Option A**: I can go ahead and fix #353 (Windows filename) right now - takes 5 min

**Option B**: I can generate a comprehensive ranked list of all 78 issues by low-hanging-fruit-ness and let you pick

**Option C**: I can run discovery process each time you ask and show you top 3 candidates

What's your preference?

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
