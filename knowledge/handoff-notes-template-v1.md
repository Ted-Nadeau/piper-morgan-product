# Role Briefing Handoff Notes Template

**Version**: 1.0
**Created**: March 13, 2026
**Author**: HOSR
**Purpose**: Structured capture of what an exiting agent learned that their successor needs to know

---

## Design Principles

1. **Lightweight**: Completable in 5-10 minutes at session end
2. **Artifact-grounded**: Reference specific files, issues, conversations — not abstractions
3. **Feeds forward**: Notes should surface candidates for briefing document updates
4. **Friction-focused**: What surprised you? What was wrong? What's missing?

---

## Template

### Session Context

**Role**: [e.g., Lead Developer, CXO, Chief of Staff]
**Session Date**: [YYYY-MM-DD]
**Session Duration**: [approximate]
**Handoff To**: [successor instance / next session]

---

### 1. What Changed

*What's different now than when you started? List concrete changes.*

- [ ] Issues closed:
- [ ] Issues opened:
- [ ] Files created/modified:
- [ ] Decisions made:
- [ ] Commits (if applicable):

---

### 2. What's Pending

*What did you start but not finish? What's blocked?*

| Item | Status | Blocker (if any) | Next Action |
|------|--------|------------------|-------------|
| | | | |

---

### 3. What Surprised You

*Where did reality differ from your expectations? This is the most valuable section.*

- **Briefing said X, but actually Y**:
- **Expected to find X, but found Y**:
- **Assumed X was true, discovered it wasn't**:

---

### 4. What Your Successor Should Know

*If you could tell the next instance of this role one thing, what would it be?*

> [Free text — one paragraph max]

---

### 5. Briefing Update Candidates

*Based on your session, what should be updated in the role's briefing documents?*

| Document | Section | Suggested Change |
|----------|---------|------------------|
| BRIEFING-ESSENTIAL-[ROLE].md | | |
| BRIEFING-CURRENT-STATE.md | | |
| Other: | | |

---

## Usage Notes

**When to complete**: At session end, before final log commit
**Where to store**: Include in session log OR deliver to role's mailbox
**Who reviews**: HOSR (periodic), PM (as needed), next role instance (always)

**Feeding the loop**: Section 5 candidates should be reviewed by HOSR or Docs agent during weekly audit. High-frequency patterns (same update suggested 2+ times) indicate briefing drift that needs correction.

---

## Example (Abbreviated)

**Role**: Lead Developer
**Session Date**: 2026-03-12

**What Changed**: Closed #890-894, opened #895-898, pushed 3 commits to claude/distracted-sammet

**What's Pending**:
| Item | Status | Blocker | Next Action |
|------|--------|---------|-------------|
| #888 onboarding hijack | Investigated | CXO/PPM design guidance | Await mailbox response |
| #889 standup hijack | Investigated | CXO/PPM design guidance | Await mailbox response |

**What Surprised You**:
- Briefing said canonical test was 47.5% pass, but that was pre-wiring-fixes; actual impl rate reached 81.1%
- Expected classifier issues, found wiring issues instead

**What Your Successor Should Know**:
> Most test failures were plumbing bugs, not AI bugs. If you see a handler not firing, check if it's actually wired before assuming the classifier is wrong.

**Briefing Update Candidates**:
| Document | Section | Suggested Change |
|----------|---------|------------------|
| BRIEFING-ESSENTIAL-LEAD-DEV.md | Current Sprint | Update M1 status: Phase 1 in progress |
| BRIEFING-CURRENT-STATE.md | Test Suite | Update pass rate to 81.1% impl |

---

*Template v1.0 — For iteration based on first few uses*
