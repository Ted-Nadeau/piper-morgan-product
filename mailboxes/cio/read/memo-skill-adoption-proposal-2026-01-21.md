# Memo: Agent Skills Adoption Proposal

**To**: Chief Innovation Officer
**From**: Documentation Management Agent (via PM)
**Date**: January 21, 2026
**Re**: Formalizing implicit methodology skills using the Agent Skills specification

---

## Executive Summary

We analyzed the piper-morgan methodology to identify implicit skills that have emerged organically and could be formalized as Agent Skills (per the [anthropics/skills](https://github.com/anthropics/skills) specification).

**Key findings**:
- **16 skill candidates** identified across 3 priority tiers
- **1 pilot skill** created, audited, and tested: `create-session-log`
- **Validation**: 4 test scenarios passed, including nuanced subagent behavior
- **Recommendation**: Proceed with Tier 1 skill formalization

---

## Background: What Are Agent Skills?

Agent Skills (per the Anthropic specification) are self-contained procedural instructions that transform Claude from general-purpose to specialized for specific tasks. Think of them as "procedural memory" that ensures consistent execution.

**Key characteristics**:
- Self-contained SKILL.md files
- Clear trigger patterns (when to use)
- Step-by-step procedures
- Examples of good/bad behavior
- Quality checklists

**Why this matters for piper-morgan**: Our methodology has accumulated significant procedural knowledge (session logs, omnibus creation, gameplans, pattern sweeps, etc.) that currently lives scattered across CLAUDE.md, methodology docs, and tribal knowledge. Formalizing these as skills would:

1. **Ensure consistency** across all agents
2. **Reduce onboarding friction** for new agent roles
3. **Prevent drift** from established procedures
4. **Make procedures auditable** and improvable

---

## Analysis Methodology

### Sources Scanned

| Source | Files | Implicit Skills Found |
|--------|-------|----------------------|
| CLAUDE.md | 1 (1258 lines) | 12+ workflows |
| BRIEFING-ESSENTIAL-*.md | 3 files | Role-specific procedures |
| methodology-core/ | 36 files | 6+ formal methodologies |
| .github/issue_template/ | 4 templates | Issue creation patterns |
| scripts/ | 127 files | Automation patterns |
| docs/internal/operations/ | 25 files | Audit procedures |

### Extraction Criteria

For each candidate, we evaluated:
- **Trigger pattern**: How is this invoked?
- **Frequency**: Daily / weekly / per-sprint / rare
- **Cross-role utility**: Benefits all agents or role-specific?
- **Complexity**: Lines of instruction needed
- **Formalization value**: Would a skill meaningfully improve consistency?

---

## Skill Candidates Identified

### Tier 1: High Priority (6 candidates)

| Skill | Frequency | Scope | Complexity | Value |
|-------|-----------|-------|------------|-------|
| **create-session-log** | Every session | Cross-role | LOW | HIGH |
| **create-omnibus-log** | Daily | Docs role | HIGH | HIGH |
| **check-mailbox** | Every session | Cross-role | LOW | MEDIUM |
| **create-gameplan** | Per epic | Architect | HIGH | HIGH |
| **pattern-sweep-execution** | 6 weeks | Lead Dev | HIGH | HIGH |
| **close-issue-properly** | Multiple/session | Cross-role | MEDIUM | HIGH |

### Tier 2: Medium Priority (6 candidates)

| Skill | Frequency | Scope | Notes |
|-------|-----------|-------|-------|
| run-debug-protocol | As needed | Coding agents | Prevents symptom-fixing |
| anti-pattern-scan | 6 weeks | Docs role | New process (today!) |
| beads-session-start | Every session | Cross-role | Issue tracking discipline |
| create-memo | As needed | Cross-role | Mailbox consistency |
| doc-audit | 3-4 weeks | CoS/Docs | Recurring checklist |
| verification-first-implementation | Every coding task | Coding agents | Core methodology |

### Tier 3: Lower Priority (4 candidates)

role-health-check, methodology-audit, create-adr, create-pattern

---

## Pilot Skill: `create-session-log`

### Why This Pilot

- **Highest frequency** - Every agent, every session
- **Lowest complexity** - ~170 lines SKILL.md
- **Cross-role** - Benefits all agents immediately
- **Deeply ingrained** - Most reinforced habit, good baseline

### Key Features Implemented

1. **One-log-per-day principle** - Check for existing same-day log before creating
2. **Role slug reference table** - All 11 roles documented
3. **Subagent nuance** - Distinguishes Task tool (no log) from programmer subagents (log for substantive work)
4. **3 examples** - New log, resume existing, Lead Dev variant
5. **Anti-pattern table** - Common mistakes and corrections
6. **Quality checklist** - 6-point verification

### Validation Results

| Test | Scenario | Expected | Result |
|------|----------|----------|--------|
| 1 | Task tool subagent (search) | No log | ✅ PASSED |
| 2 | New session (no existing log) | Create new log | ✅ PASSED |
| 3 | Resume session (existing log) | Continue existing | ✅ PASSED |
| 4 | Programmer subagent (bug fix) | Create log | ✅ PASSED |
| 5 | Programmer subagent (trivial task) | No log | ✅ PASSED |

### Location

`.claude/skills/create-session-log/SKILL.md`

---

## Recommendations

### Immediate (Tier 1 Skills)

1. **Approve `create-session-log`** for production use
2. **Create `check-mailbox`** skill next (similar complexity, cross-role)
3. **Create `close-issue-properly`** skill (highest value per PM feedback)

### Near-Term (After Tier 1 Validated)

4. **Create `create-omnibus-log`** skill (complex but high-value for docs role)
5. **Create `verification-first-implementation`** skill (core coding methodology)

### Process Recommendations

- **Skill creation process**: Spec → Draft → Audit → Pilot Test → Deploy
- **Location**: `.claude/skills/{skill-name}/SKILL.md`
- **Maintenance**: Review skills during methodology audits (6-8 week cadence)
- **Metrics**: Track consistency improvements after skill deployment

---

## Open Questions for CIO

1. **Adoption scope**: Should skills be mandatory for all agents or opt-in initially?

2. **Skill discovery**: How should agents know which skills are available?
   - Option A: List in CLAUDE.md
   - Option B: Skill index file
   - Option C: Agents discover via `.claude/skills/` directory

3. **Cross-project potential**: Could skills like `create-session-log` be generalized for other projects, or are they piper-morgan specific?

4. **Versioning**: Should skills have version numbers for tracking changes?

5. **Skill dependencies**: Some skills may depend on others (e.g., `pattern-sweep-execution` might invoke `anti-pattern-scan`). How formal should dependency management be?

---

## Attachments

### Analysis Documents
- `dev/active/skill-harvest-analysis-plan.md` - Full methodology
- `dev/active/skill-harvest-candidates.md` - All 16 candidates with details

### Pilot Skill
- `.claude/skills/create-session-log/SKILL.md` - The skill itself
- `dev/active/skill-create-session-log-spec.md` - Specification
- `dev/active/skill-create-session-log-audit.md` - Audit results

---

## Summary

The pilot validates that formalizing implicit methodology as Agent Skills is:
- **Feasible** - Skills can be extracted from existing docs
- **Testable** - Scenarios can verify correct behavior
- **Valuable** - Nuanced behavior (like subagent distinctions) is now explicit and consistent

**Recommended next action**: Approve Tier 1 skill creation and establish skill maintenance in methodology audit cadence.

---

*Prepared by Documentation Management Agent*
*January 21, 2026*
