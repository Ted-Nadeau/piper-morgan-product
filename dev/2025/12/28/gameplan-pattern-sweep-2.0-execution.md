# Gameplan: Pattern Sweep 2.0 Execution

**Issue**: #524
**Date**: December 27, 2025
**Lead**: Lead Developer (Specialist Instance)
**Status**: Approved - Executing

## Objective

Execute the Pattern Sweep 2.0 framework to perform a multi-lens pattern analysis of December 2025 development activity, distinguishing true emergence from pattern usage.

## Context

- **Problem**: Current sweep suffers from "pattern amnesia" - rediscovers known patterns as new
- **Solution**: Multi-agent analysis with pattern library awareness
- **Pattern Library**: 45 existing patterns in `docs/internal/architecture/current/patterns/`
- **Data Sources**: Late November + December 2025 (existing sweep data + fresh analysis)

## Architecture

### Agent Assignments

| Agent | Role | Model | Purpose |
|-------|------|-------|---------|
| A | Pattern Librarian | Haiku | Index existing patterns, extract signatures |
| B | Usage Analyst | Haiku | Detect pattern applications, frequency analysis |
| C | Novelty Detector | Sonnet | Identify genuinely new patterns |
| D | Evolution Tracker | Sonnet | Track pattern changes/refinements |
| E | Meta-Pattern Synthesizer | Opus | Synthesize insights, detect patterns about patterns |

### Model Rationale

- **Haiku** (A, B): Straightforward indexing/counting tasks, cost-efficient
- **Sonnet** (C, D): Nuanced comparison and tracking, balance of capability/cost
- **Opus** (E): High-level synthesis requiring sophisticated reasoning

## Execution Phases

### Phase 1: Pattern Library Index (Agent A - Haiku)

**Input**: `docs/internal/architecture/current/patterns/pattern-*.md` (45 files)

**Output**: Machine-readable pattern index with:
- Pattern ID, name, category
- Key signature terms (concepts it addresses)
- First documented date
- Known variations
- Related patterns

**Deliverable**: `dev/active/pattern-library-index.json`

**Acceptance Criteria**:
- [ ] All 45 patterns indexed
- [ ] Each pattern has signature terms extracted
- [ ] Output is valid JSON
- [ ] Categories assigned from existing taxonomy

### Phase 2: Multi-Lens Analysis (Agents B-E in parallel)

**Data Window**: November 20 - December 26, 2025

**Data Sources**:
- `docs/omnibus-logs/2025-12-*.md`
- `dev/active/*.md` (recent working documents)
- Existing sweep data: `late-dec-pattern-sweep.json`, `early-dec-pattern-sweep.json`
- Git commit history for the period

#### Agent B: Usage Analyst (Haiku)

**Task**: Analyze pattern applications in the data window

**Output**: Usage report with:
- Pattern usage frequency
- Context of each usage (what feature/task)
- Quality assessment (proper vs. degraded usage)

**Deliverable**: `dev/active/pattern-usage-analysis.md`

**Acceptance Criteria**:
- [ ] All pattern usages cataloged
- [ ] Frequency counts per pattern
- [ ] Top 10 most-used patterns identified
- [ ] Unusual applications flagged

#### Agent C: Novelty Detector (Sonnet)

**Task**: Identify genuinely new patterns NOT in the library

**Output**: Novelty candidates with:
- Evidence of novelty (why not in library)
- First appearance date/context
- Proposed classification
- Recommendation (catalog or not)

**Deliverable**: `dev/active/pattern-novelty-candidates.md`

**Acceptance Criteria**:
- [ ] All candidates verified against pattern library index
- [ ] Each candidate has evidence trail
- [ ] FALSE POSITIVE test: "75% pattern", "verification-first" NOT flagged as new
- [ ] Classification uses 5-tier system from framework

#### Agent D: Evolution Tracker (Sonnet)

**Task**: Track how existing patterns have evolved

**Output**: Evolution report with:
- Patterns showing variation/refinement
- Before/after comparison
- Maturity stage assessment
- Anti-pattern emergence detection

**Deliverable**: `dev/active/pattern-evolution-report.md`

**Acceptance Criteria**:
- [ ] Pattern variations documented
- [ ] Evolution vs. new pattern distinguished
- [ ] Anti-patterns identified with evidence
- [ ] Lifecycle stage assigned where applicable

#### Agent E: Meta-Pattern Synthesizer (Opus)

**Task**: Detect patterns about patterns (methodology evolution)

**Output**: Meta-analysis with:
- How pattern usage itself has patterned
- Methodology evolution insights
- Process improvement opportunities
- Cross-pattern interactions

**Deliverable**: `dev/active/pattern-meta-synthesis.md`

**Acceptance Criteria**:
- [ ] Meta-patterns identified
- [ ] Actionable insights provided
- [ ] Connections to Pattern-045 (Green Tests, Red User) explored
- [ ] Process recommendations made

### Phase 3: Synthesis & Classification

**Lead Developer Task**: Consolidate agent outputs into unified report

**Classification Tiers**:
1. **TRUE EMERGENCE** - Genuinely new, not in library
2. **PATTERN EVOLUTION** - Variation of existing
3. **PATTERN COMBINATION** - Novel mixing of known patterns
4. **PATTERN USAGE** - Standard application
5. **ANTI-PATTERN** - Degradation or misuse

**Deliverable**: `dev/active/pattern-sweep-2.0-results.md`

### Phase 4: Validation

**Test Cases**:
1. "75% pattern" (Pattern-045) recognized as existing, not new
2. "Verification-first" (Pattern-006) recognized as existing
3. Any TRUE EMERGENCE passes manual review
4. No false positives in novelty detection

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Over-classification (everything is "evolution") | Strict criteria per category, examples provided |
| Missing subtle emergence | Multiple agent perspectives, cross-validation |
| Agent hallucination | Pattern library index as ground truth |
| Performance/cost | Haiku for volume tasks, Opus only for synthesis |

## Success Criteria

1. **No False Positives**: Known patterns correctly identified as existing
2. **True Novelty Detection**: New patterns accurately flagged
3. **Pattern Evolution Tracking**: Changes documented
4. **Actionable Output**: Report useful for process improvement

## Expected Outcomes

Based on framework hypothesis for December 2025:
- TRUE EMERGENCE: 0-2 patterns
- PATTERN EVOLUTION: 5-10 variations
- PATTERN COMBINATION: 15-25 novel mixes
- PATTERN USAGE: 40+ standard applications
- ANTI-PATTERNS: 2-3 degradations

## Timeline

Not providing time estimates per CLAUDE.md guidelines. Work will proceed phase-by-phase with PM checkpoints.

## Completion Matrix

- [ ] Phase 1 complete: Pattern library indexed
- [ ] Phase 2 complete: All 4 agents delivered outputs
- [ ] Phase 3 complete: Synthesis report generated
- [ ] Phase 4 complete: Validation test cases pass
- [ ] Session log updated with evidence
- [ ] GitHub issue closed with deliverables linked

---

## PM Decisions (December 27, 2025)

1. **Scope**: November 20 - December 26, 2025 (priority timeframe; retrospective sweeps of earlier periods may follow)

2. **Archive**: Final report goes to `docs/internal/development/reports/`

3. **Pattern creation**: Create `DRAFT-pattern-0XX.md` files for Chief Architect review (likely to be adopted)
