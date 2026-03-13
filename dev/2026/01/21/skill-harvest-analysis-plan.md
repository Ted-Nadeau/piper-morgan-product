# Plan: Skill Harvest Analysis

**Date**: January 21, 2026
**Author**: Documentation Management Agent
**Status**: DRAFT - Awaiting PM Approval

---

## Objective

Analyze the piper-morgan methodology to identify implicit skills that have emerged organically, then propose which ones to formalize as Agent Skills (per the [anthropics/skills](https://github.com/anthropics/skills) specification) and in what order.

**Deliverable**: Memo to Chief Innovation Officer with skill candidates, prioritization, and adoption roadmap.

---

## Background: What Makes a Good Skill Candidate?

Per the Agent Skills specification:

1. **Self-contained** - Can be invoked independently with clear inputs/outputs
2. **Repeatable** - Produces consistent results across invocations
3. **Trigger + Context → Output** - Has a clear activation pattern
4. **Procedural knowledge** - Teaches Claude *how* to do something specific
5. **Concise** - Fits in context window efficiently (<500 lines SKILL.md)

**Key insight from skill-creator**: "Design for another Claude instance to use" - skills should transform Claude from general-purpose to specialized for a specific task.

---

## Phase 1: Source Inventory (Research)

**Goal**: Catalog all locations where implicit skills might be hiding.

### 1.1 Primary Sources

| Source | Description | Expected Skill Types |
|--------|-------------|---------------------|
| `CLAUDE.md` | Master instructions | Session discipline, git workflow, debugging, reporting |
| `docs/briefing/BRIEFING-ESSENTIAL-*.md` | Role briefings | Role-specific workflows |
| `docs/internal/development/methodology-core/` | Core methodology | Process workflows |
| `docs/internal/development/methodology/` | Methodology docs | Specific methodologies (omnibus-log, etc.) |
| `.github/issue_template/*.md` | Issue templates | Issue creation patterns |
| `.github/workflows/*.yml` | GitHub Actions | Automated workflows |
| `scripts/` | Automation scripts | Scripted operations |

### 1.2 Secondary Sources

| Source | Description | Expected Skill Types |
|--------|-------------|---------------------|
| `docs/internal/architecture/current/patterns/` | Pattern catalog | Implementation patterns |
| `docs/internal/operations/` | Operations docs | Audit workflows |
| `config/PIPER.md`, `config/PIPER.user.md` | Configuration | Config management |
| Session log conventions | Naming/structure | Documentation creation |
| Beads workflow (`bd` commands) | Issue tracking | Project management |

### 1.3 Implicit Skills (Undocumented but practiced)

These require inference from observed behavior:
- Session log creation (trigger: "start a session")
- Omnibus log creation (trigger: "create omnibus for date X")
- Role assumption (trigger: "you are my [role] agent")
- Anti-pattern scanning (trigger: "scan for anti-patterns")
- Gameplan creation/execution
- Evidence-based issue closure

---

## Phase 2: Skill Candidate Extraction (Analysis)

**Goal**: For each source, extract skill candidates using consistent criteria.

### 2.1 Extraction Template

For each candidate, document:

```markdown
### Candidate: [Name]

**Trigger Pattern**: How is this skill invoked? (phrase, context, command)
**Current Implementation**: Where do instructions live today?
**Inputs**: What does Claude need to execute this?
**Outputs**: What does successful execution produce?
**Dependencies**: Files, templates, other skills needed
**Complexity**: LOW / MEDIUM / HIGH (lines of instruction needed)
**Frequency**: How often is this used? (daily / weekly / per-sprint / rare)
**Formalization Value**: Why would making this a skill help?
```

### 2.2 Candidate Classification

Classify each candidate:

| Classification | Criteria | Action |
|---------------|----------|--------|
| **STRONG CANDIDATE** | Clear trigger, repeatable, self-contained, high frequency | Prioritize for skill creation |
| **COMPOSITE SKILL** | Combines multiple sub-skills | Consider decomposition |
| **CONTEXT-DEPENDENT** | Needs too much dynamic context | May not be good skill fit |
| **ALREADY AUTOMATED** | Script or workflow exists | Evaluate if skill wrapper adds value |
| **TOO SIMPLE** | One-liner, no procedure | Not worth skill overhead |

---

## Phase 3: Dependency Mapping (Analysis)

**Goal**: Understand what each skill candidate needs to function.

### 3.1 Dependency Types

1. **Templates** - Files that provide structure (e.g., session log template)
2. **References** - Documentation needed for context (e.g., role briefings)
3. **Scripts** - Executable code (e.g., `bd` commands, extraction scripts)
4. **Assets** - Static files (e.g., naming conventions, examples)
5. **Other Skills** - Skills that might compose together

### 3.2 Dependency Matrix

Create matrix showing:
- Which candidates share dependencies (bundling opportunities)
- Which candidates are prerequisites for others (ordering)
- Which dependencies are already packaged vs. scattered

---

## Phase 4: Prioritization (Synthesis)

**Goal**: Rank candidates for implementation order.

### 4.1 Scoring Criteria

| Factor | Weight | Scale |
|--------|--------|-------|
| Frequency of use | 30% | 1-5 (daily=5, rare=1) |
| Complexity reduction | 25% | 1-5 (saves most context/effort=5) |
| Error prevention | 20% | 1-5 (high error rate without=5) |
| Dependency simplicity | 15% | 1-5 (self-contained=5, complex deps=1) |
| Cross-role utility | 10% | 1-5 (all roles=5, single role=1) |

### 4.2 Implementation Tiers

- **Tier 1 (Quick Wins)**: High score, low complexity, few dependencies
- **Tier 2 (Core Skills)**: High score, medium complexity, foundational
- **Tier 3 (Advanced)**: Medium score, high complexity, builds on Tier 1-2
- **Tier 4 (Deferred)**: Low score or requires significant prerequisites

---

## Phase 5: Memo Drafting (Deliverable)

**Goal**: Produce actionable memo for Chief Innovation Officer.

### 5.1 Memo Structure

```markdown
# Memo: Skill Adoption Proposal

## Executive Summary
- X skill candidates identified
- Y recommended for immediate adoption
- Expected benefits: [consistency, onboarding, error reduction]

## Methodology
- How we identified candidates
- Evaluation criteria used

## Recommended Skills (Prioritized)

### Tier 1: Quick Wins
[2-3 skills with full specifications]

### Tier 2: Core Skills
[3-5 skills with outlines]

### Tier 3-4: Future Candidates
[List with brief descriptions]

## Implementation Roadmap
- Phase 1: Create Tier 1 skills (timeframe)
- Phase 2: Create Tier 2 skills (timeframe)
- Phase 3: Evaluate and iterate

## Open Questions for CIO
1. [Strategic questions about skill adoption]
2. [Questions about scope/priorities]

## Attachments
- Full candidate analysis
- Dependency matrix
- Scoring details
```

---

## Execution Plan

### Step 1: Source Scan (Phase 1)
- Read CLAUDE.md thoroughly
- Read all BRIEFING-ESSENTIAL-*.md files
- Scan issue templates
- Review scripts/ directory
- Check for methodology docs

### Step 2: Candidate Extraction (Phase 2)
- Apply extraction template to each source
- Classify candidates
- Document in working file

### Step 3: Dependency Analysis (Phase 3)
- Map dependencies for strong candidates
- Identify bundling opportunities
- Note missing templates/assets

### Step 4: Prioritization (Phase 4)
- Score each strong candidate
- Assign to tiers
- Validate ordering makes sense

### Step 5: Memo Creation (Phase 5)
- Draft memo structure
- Write Tier 1 skill specifications
- Outline Tier 2 skills
- List remaining candidates
- Formulate CIO questions

### Step 6: Review & Refinement
- PM review of draft memo
- Incorporate feedback
- Finalize for CIO

---

## Estimated Effort

| Phase | Effort | Notes |
|-------|--------|-------|
| Phase 1: Source Inventory | 30 min | Reading/cataloging |
| Phase 2: Candidate Extraction | 1-2 hours | Depends on source density |
| Phase 3: Dependency Mapping | 30 min | Matrix creation |
| Phase 4: Prioritization | 30 min | Scoring and tiering |
| Phase 5: Memo Drafting | 1 hour | Writing deliverable |
| Review/Refinement | 30 min | PM feedback loop |

**Total**: ~4-5 hours

---

## Success Criteria

1. **Completeness**: All major sources scanned
2. **Actionability**: Tier 1 skills are ready to implement
3. **Clarity**: CIO can make decisions from memo alone
4. **Grounded**: Recommendations tied to actual methodology
5. **Realistic**: Implementation roadmap is achievable

---

## PM Decisions (2026-01-21)

1. **Scope**: Cross-role skills first, but assess each candidate for whether it's role-specific or broadly applicable.

2. **Depth**: For each Tier 1 skill: (a) write spec, (b) write full SKILL.md draft, (c) audit draft for thoroughness.

3. **CIO Context**: TBD - will frame memo appropriately.

4. **Timeline**: Thorough. Not urgent, but doing it well is important.

5. **Validation**: **Pilot one skill first**, then discuss how to proceed before writing full memo.

---

## Revised Execution Plan

Given PM decision to pilot first:

### Step 1: Source Scan (Phase 1)
- Read CLAUDE.md thoroughly
- Read all BRIEFING-ESSENTIAL-*.md files
- Scan issue templates
- Review scripts/ directory
- **Check methodology docs** (including omnibus-log methodology)
- Check operations docs

### Step 2: Candidate Extraction (Phase 2)
- Apply extraction template to each source
- Classify candidates
- **Flag each as cross-role or role-specific**
- Document in working file

### Step 3: Dependency Analysis (Phase 3)
- Map dependencies for strong candidates
- Identify bundling opportunities
- Note missing templates/assets

### Step 4: Prioritization (Phase 4)
- Score each strong candidate
- Assign to tiers
- **Select ONE Tier 1 candidate for pilot**

### Step 5: Pilot Skill Creation
- Write specification for pilot skill
- Write full SKILL.md draft
- Audit draft for thoroughness
- **Test pilot skill in real usage**

### Step 6: Pilot Retrospective
- Document what worked / what didn't
- Refine skill creation approach
- **Discuss with PM how to proceed** (memo scope, additional pilots, etc.)

### Step 7: Memo Creation (Post-Pilot)
- Incorporate pilot learnings
- Draft memo with validated approach
- Full specs for Tier 1, outlines for Tier 2+

---

*Plan approved. Ready to execute Phase 1.*
