---
name: Pattern Sweep 2.0
about: Recurring multi-lens pattern analysis to detect true emergence vs pattern usage
title: 'PATTERN-SWEEP: [Date Range]'
labels: 'process, patterns'
assignees: ''
---

# Pattern Sweep 2.0 - [Date Range]

**Generated**: [Date]
**Lead**: Lead Developer
**Framework**: `dev/active/pattern-sweep-2.0-framework.md`

---

## Scope

**Analysis Period**: [Start Date] - [End Date]
**Pattern Library**: `docs/internal/architecture/current/patterns/` (check count)

---

## Pre-Sweep Checklist

- [ ] Pattern library index exists or needs regeneration
- [ ] Data sources available for analysis period:
  - [ ] `docs/omnibus-logs/` for the period
  - [ ] `dev/YYYY/MM/` session logs
  - [ ] Git history accessible

---

## Phase 1: Pattern Library Index (Agent A - Haiku)

**Task**: Create/update `dev/active/pattern-library-index.json`

**Acceptance Criteria**:
- [ ] All patterns in catalog indexed
- [ ] Each pattern has signature terms
- [ ] Valid JSON output
- [ ] Categories assigned

---

## Phase 2: Multi-Lens Analysis (Agents B-E in parallel)

### Agent B: Usage Analyst (Haiku)
- [ ] Create `dev/active/pattern-usage-analysis.md`
- [ ] Frequency counts per pattern
- [ ] Top 10 most-used identified
- [ ] Unusual applications flagged

### Agent C: Novelty Detector (Sonnet)
- [ ] Create `dev/active/pattern-novelty-candidates.md`
- [ ] Candidates verified against library
- [ ] FALSE POSITIVE TEST passed
- [ ] 5-tier classification applied

### Agent D: Evolution Tracker (Sonnet)
- [ ] Create `dev/active/pattern-evolution-report.md`
- [ ] Variations documented
- [ ] Anti-patterns identified
- [ ] Lifecycle stages assigned

### Agent E: Meta-Pattern Synthesizer (Opus)
- [ ] Create `dev/active/pattern-meta-synthesis.md`
- [ ] Meta-patterns identified
- [ ] Pattern-045 connections explored
- [ ] Process recommendations made

---

## Phase 3: Synthesis & Validation

- [ ] Final report created in `docs/internal/development/reports/`
- [ ] All validation test cases pass:
  - [ ] Known patterns NOT flagged as new
  - [ ] TRUE EMERGENCE has evidence trail
- [ ] DRAFT-pattern files created for any TRUE EMERGENCE

---

## Classification Tiers

1. **TRUE EMERGENCE** - Genuinely new pattern
2. **PATTERN EVOLUTION** - Variation of existing
3. **PATTERN COMBINATION** - Novel mixing of known patterns
4. **PATTERN USAGE** - Standard application
5. **ANTI-PATTERN** - Degradation or misuse

---

## Expected Outcomes

Based on previous sweeps:
- TRUE EMERGENCE: 0-2 patterns per 6 weeks
- PATTERN EVOLUTION: 5-10 refinements
- PATTERN USAGE: 40+ applications

---

## Deliverables Checklist

- [ ] `dev/active/pattern-library-index.json`
- [ ] `dev/active/pattern-usage-analysis.md`
- [ ] `dev/active/pattern-novelty-candidates.md`
- [ ] `dev/active/pattern-evolution-report.md`
- [ ] `dev/active/pattern-meta-synthesis.md`
- [ ] `docs/internal/development/reports/pattern-sweep-2.0-results-YYYY-MM-DD.md`
- [ ] DRAFT-pattern files (if TRUE EMERGENCE found)

---

## Success Criteria

- [ ] FALSE POSITIVE TEST passed (known patterns not flagged as new)
- [ ] All 5 agent deliverables complete
- [ ] Final report in reports directory
- [ ] GitHub issue updated with results
- [ ] Session log completed

---

## Notes

[Add any specific focus areas or context for this sweep]

---

**Methodology**: Pattern Sweep 2.0 (#524)
**Template Version**: 1.0 (December 27, 2025)
