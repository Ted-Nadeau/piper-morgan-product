# Memo: Anti-Pattern Index & Pattern Sweep Automation

**To**: Chief Architect
**From**: Documentation Management Agent (via PM)
**Date**: January 21, 2026
**Re**: Anti-pattern index (28→42 entries), Phase 2 experiment results, and pattern sweep automation

---

## Summary

Created an anti-pattern index that cross-references anti-patterns documented throughout patterns, ADRs, and MUX design docs. After initial pilot (28 anti-patterns), executed Phase 2 semantic analysis experiment which discovered **14 additional emergent anti-patterns** (now 42 total). Also implemented a GitHub Actions workflow and three automation scripts for pattern sweep.

---

## Deliverables

### 1. Anti-Pattern Index (Pilot + Phase 2)

**Location**: `docs/internal/architecture/current/anti-pattern-index.md`

**Scope**: 42 anti-patterns indexed across 5 categories:
- **Grammar/Consciousness (12)**: Query language in responses, timestamps without context, IDs instead of names, etc.
- **Testing (4)**: Mocked dependencies, schema drift, type mismatches
- **Architecture (11)**: Dual repositories, get_session(), LLM-for-Everything, Keyword-Only Matching, Thread-Local Injection, Verification Theater
- **Process (10)**: 75% abandonment, completion bias, "Good Enough" Trap, "Refactor Later" Lie, 80% Completion Trap, Escalation Timing Failure
- **Integration (5)**: Silent failures, generic errors, Forgetting initialize(), Non-Idempotent Init, Sync Init for Async

**Key Design Decisions**:
- **Index, don't duplicate**: Links to source documents rather than copying content
- **Bidirectional navigation**: Anti-pattern → recommended pattern AND pattern → anti-patterns it addresses
- **Stable IDs**: G-01, T-01, A-01, P-01, I-01 scheme (never renumbered)
- **Anchored links**: Markdown anchors for direct navigation where possible

### 2. Pattern Sweep Workflow

**Location**: `.github/workflows/pattern-sweep.yml`

**Implementation**:
- Runs every Monday at 9 AM Pacific
- Logic determines if it's a pattern sweep week (every 6 weeks per staggered calendar)
- Creates issue from template with date range
- Manual trigger available via `workflow_dispatch`

**Schedule Handling**: Rather than hardcoding 8 cron entries per year, the workflow runs weekly and checks against the 2026 sweep dates (Feb 3, Mar 17, Apr 27, Jun 8, Jul 20, Aug 31, Oct 12, Nov 23). This is cleaner and self-documenting.

### 3. Issue Template Update

**Location**: `.github/issue_template/pattern-sweep.md`

**Changes** (v1.0 → v1.1):
- Added "Phase 3: Anti-Pattern Index Update" section
- Agent D (Evolution Tracker) now includes anti-pattern index update
- Deliverables checklist includes anti-pattern-index.md
- Success criteria includes "Anti-pattern index updated"

---

## Architecture Questions for Your Review

### 1. Category Scheme

Current categories: Grammar (G), Testing (T), Architecture (A), Process (P), Integration (I)

**Question**: Are these the right top-level categories? Should we add/merge any? For example:
- Should "Security" be its own category?
- Should "Performance" be distinct from Architecture?

### 2. Placement in Pattern Catalog

The anti-pattern index lives alongside patterns in `docs/internal/architecture/current/`.

**Question**: Should it be referenced from the pattern README? Or kept as a separate navigation tool?

### 3. Phase 2: Emergent Anti-Pattern Detection (COMPLETED)

**Experiment Executed**: Same day (2026-01-21)

**5 Detection Strategies Tested**:
| Strategy | Precision | Recommendation |
|----------|-----------|----------------|
| Session log lessons learned | 60% ✅ | HIGH - primary strategy |
| Code comment mining (WARNING, HACK, XXX) | 50% | HIGH - easy automation |
| Negative language clustering | 50% | LOW - needs ML/proximity |
| Contrast patterns ("instead of X") | 38% | LOW - too variable |
| ADR rejected alternatives | 28% | MEDIUM - highest volume |

**Results**:
- ~80 candidates scanned
- 14 TRUE EMERGENT (added to index)
- 6 VARIATION (related to existing)
- 8 FALSE POSITIVE
- **Overall Precision: 63%**

**Automation Scripts Created**:
- `scripts/extract-session-lessons.sh` - Best strategy (60% precision)
- `scripts/extract-code-comments.sh` - Code comment mining
- `scripts/extract-adr-rejected.sh` - ADR rejected alternatives

**Integration**: Added Phase 3a to pattern sweep template (v1.2) with automated extraction workflow.

**Recommendation**: Session log mining should be the primary strategy for Agent D's evolution tracking work. The experiment validated that ~60% of candidates from structured "lessons learned" sections are true anti-patterns.

### 4. Reverse Index Utility

The index includes a reverse lookup: Pattern → Anti-patterns it addresses.

**Question**: Is this useful for architectural review? Should we expand it to show coverage gaps (patterns without documented anti-patterns)?

---

## Integration with Existing Work

### Pattern Sweep 2.0 Framework

The anti-pattern index update is now integrated into the Pattern Sweep methodology:
- **Agent D (Evolution Tracker)** owns the update
- **Phase 3** dedicated to anti-pattern index maintenance
- **Deliverables** checklist includes the index

### Completion Discipline Triad

The index prominently features Patterns 045, 046, 047 (the Completion Discipline Triad), which are themselves anti-pattern documentation. This creates a nice meta-coherence.

### MUX Grammar Anti-Patterns

The largest category (12 entries) covers grammar/consciousness anti-patterns from the recent MUX V1 Vision sprint. This aligns with ADR-045's goal of preserving consciousness in implementation.

---

## Recommended Actions

1. **Review** the anti-pattern index for completeness and accuracy
2. **Approve** the category scheme or suggest modifications
3. **Advise** on Phase 2 semantic analysis prioritization
4. **Consider** whether coverage gap analysis would be valuable

---

## Attachments

- `docs/internal/architecture/current/anti-pattern-index.md` (42 entries)
- `.github/workflows/pattern-sweep.yml`
- `.github/issue_template/pattern-sweep.md` (v1.2 - with Phase 3a)
- `dev/active/anti-pattern-index-design-v1.md` (design document)
- `dev/active/anti-pattern-phase2-experiment-design.md` (experiment methodology)
- `dev/active/anti-pattern-phase2-experiment-results.md` (full results)
- `scripts/extract-session-lessons.sh` (automation)
- `scripts/extract-code-comments.sh` (automation)
- `scripts/extract-adr-rejected.sh` (automation)

---

*Prepared by Documentation Management Agent*
*January 21, 2026*
