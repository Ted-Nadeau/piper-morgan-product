# Phase 2 Experiment Results: Emergent Anti-Pattern Detection

**Date**: January 21, 2026
**Experiment Duration**: ~45 minutes
**Author**: Documentation Management Agent

---

## Executive Summary

**Outcome**: SUCCESS - Detected 14 emergent anti-patterns not in current index

**Metrics**:
- Candidates scanned: ~80 passages
- TRUE EMERGENT: 14 (new anti-patterns to add)
- VARIATION: 6 (related to existing indexed anti-patterns)
- FALSE POSITIVE: 8 (not actually anti-patterns)
- **Precision**: 63% (14 true / 22 classified as potential)
- **Recall**: N/A for emergent (no ground truth)

---

## Emergent Anti-Patterns Discovered

### Category: Process (P)

| ID | Anti-Pattern | Source | Recommended Response |
|----|--------------|--------|---------------------|
| P-05 | **"Good Enough" Trap** - Shipping code that "works" without considering maintainability | [systematic-excellence.md:201](../../piper-education/frameworks/emergent/systematic-excellence.md) | Define "done" to include excellence |
| P-06 | **"Refactor Later" Lie** - Promising cleanup that never happens | [systematic-excellence.md:206](../../piper-education/frameworks/emergent/systematic-excellence.md) | Refactor as you go |
| P-07 | **"Deadline" Pressure** - Sacrificing quality for speed | [systematic-excellence.md:196](../../piper-education/frameworks/emergent/systematic-excellence.md) | Negotiate scope, not quality |
| P-08 | **80% Completion Trap** - Declaring done without evidence | [the-completion-discipline-draft.md](../../public/comms/drafts/the-completion-discipline-draft.md) | Completion matrix with evidence |
| P-09 | **"Should Have Known" Syndrome** - Reactive discovery of obvious requirements | [2025-10-29-omnibus:446](../../omnibus-logs/2025-10-29-omnibus-log.md) | Comprehensive upfront audit |
| P-10 | **Escalation Timing Failure** - Debugging too long before seeking help | [2025-11-16-omnibus:77](../../omnibus-logs/2025-11-16-omnibus-log.md) | Escalate after first untested commit |

### Category: Architecture (A)

| ID | Anti-Pattern | Source | Recommended Response |
|----|--------------|--------|---------------------|
| A-07 | **LLM-for-Everything** - Using LLM for deterministic operations | [ADR-039:70](adrs/adr-039-canonical-handler-pattern.md) | Canonical handlers for simple queries |
| A-08 | **Keyword-Only Matching** - Pure keyword matching without LLM capability | [ADR-039:88](adrs/adr-039-canonical-handler-pattern.md) | Hybrid approach |
| A-09 | **Shared Dev Database** - Multiple environments sharing one database | [ADR-040:261](adrs/adr-040-local-database-per-environment.md) | Local database per environment |
| A-10 | **Thread-Local Injection** - Implicit context via thread locals | [ADR-051:207](adrs/adr-051-unified-user-session-context.md) | Explicit parameter passing |
| A-11 | **Verification Theater** - Process without actual verification | [ADR-028:142](adrs/adr-028-verification-pyramid.md) | Evidence-based verification pyramid |

### Category: Integration (I)

| ID | Anti-Pattern | Source | Recommended Response |
|----|--------------|--------|---------------------|
| I-03 | **Forgetting initialize()** - Using adapter without async initialization | [pattern-035:201](patterns/pattern-035-mcp-adapter-methods.md) | Lazy init pattern |
| I-04 | **Non-Idempotent Init** - Initialize that breaks on repeat calls | [pattern-035:203](patterns/pattern-035-mcp-adapter-methods.md) | Make initialize() idempotent |
| I-05 | **Sync Init for Async Ops** - Synchronous initialization for async operations | [pattern-035:202](patterns/pattern-035-mcp-adapter-methods.md) | Async initialization |

---

## Variations of Existing Anti-Patterns

These are related to already-indexed anti-patterns (not adding as new):

| Finding | Related To | Notes |
|---------|------------|-------|
| "Services should not directly access database" | A-02 (get_session pattern) | Same principle, different framing |
| "Enrichment failures should not prevent workflow" | I-01 (Silent failures) | Inverse - specifying what SHOULD happen |
| Classification drift from NL variation | G-01 (Query language) | Downstream effect |
| Context matcher expects strings, not None | G-03 (IDs instead of names) | Type-level manifestation |
| "Multi-agent consensus trap" | P-03 (Completion bias) | Variant for multi-agent |
| "User trapping" in process | G-12 (Alert spam tone) | Related UX issue |

---

## False Positives

Passages flagged but not actually anti-patterns:

1. "Results into dimensional dictionary" - normal code, not anti-pattern
2. "Root causes" mentions in methodology - describing solution, not problem
3. "Rejected because: No credibility" - explaining decision, not anti-pattern itself
4. "Bootstrap" references - technical term, not trap
5. "Lightning fast" - positive description
6. "Warnings" in security code - feature, not anti-pattern
7. "Processing time > 50" - threshold check, not anti-pattern
8. "Don't have DB session here" - explanation, not anti-pattern

---

## Strategy Effectiveness

| Strategy | Candidates Found | True Positives | Precision |
|----------|------------------|----------------|-----------|
| 1. Negative language clustering | 12 | 6 | 50% |
| 2. Contrast patterns | 8 | 3 | 38% |
| 3. Code comment mining | 6 | 3 | 50% |
| 4. ADR rejected alternatives | 18 | 5 | 28% |
| 5. Session log lessons learned | 10 | 6 | 60% |

**Best performing**: Session log lessons learned (60% precision)
**Most volume**: ADR rejected alternatives (18 candidates)
**Lowest noise**: Code comments and session logs

---

## Recommendations

### Immediate: Add to Anti-Pattern Index

Add the 14 TRUE EMERGENT anti-patterns identified above. This would bring the index from 28 to 42 anti-patterns.

### For Pattern Sweep Integration

1. **Session log mining is highest value** - Add as primary strategy for Agent D
2. **ADR mining has volume but noise** - Use with stricter filtering (only explicit "Rejected Because" sections)
3. **Code comment mining is targeted** - Focus on `# WARNING`, `# HACK`, `# XXX` markers
4. **Negative language needs proximity scoring** - Single keyword hits are noisy; require 2+ in 20 lines

### Automation Potential

| Strategy | Automation Feasibility | Effort |
|----------|------------------------|--------|
| Session log lessons | HIGH - clear markers | 1 hour script |
| Code comment mining | HIGH - regex patterns | 30 min script |
| ADR rejected sections | MEDIUM - section parsing | 2 hour script |
| Negative language | LOW - needs ML/proximity | Not recommended |
| Contrast patterns | LOW - too variable | Not recommended |

### Recommended Workflow Addition

```markdown
## Phase 3a: Emergent Anti-Pattern Scan

- [ ] Run session log lesson extractor (`grep -E "lesson learned|should have|in retrospect"`)
- [ ] Run code comment extractor (`grep -E "# WARNING|# HACK|# XXX|# FIXME"`)
- [ ] Review ADR "Rejected Because" sections added since last sweep
- [ ] Classify candidates: TRUE EMERGENT / VARIATION / FALSE POSITIVE
- [ ] Add TRUE EMERGENT to anti-pattern-index.md
```

---

## Experiment Observations

### What Worked Well

1. **Lessons learned sections are gold** - Developers document hard-won knowledge here
2. **"Trap" and "pitfall" are high-signal keywords** - Low false positive rate
3. **ADR structure helps** - "Rejected Because" sections are curated anti-patterns
4. **Code comments reveal operational anti-patterns** - Things that broke in production

### What Didn't Work

1. **Generic "should not" is too broad** - Matches normal requirements language
2. **"Avoid" without context is noisy** - Could be positive ("avoid downtime") or negative
3. **Single-keyword search floods results** - Need phrase-level or proximity matching
4. **Some anti-patterns are implicit** - Described by what they cause, not what they are

### Surprising Finds

1. **"80% trap" and "75% pattern" are the same anti-pattern** - Now indexed as P-01, but discussed across many docs
2. **systematic-excellence.md is an anti-pattern goldmine** - 4 emergent anti-patterns in one doc
3. **ADRs contain architectural anti-patterns as "rejected alternatives"** - Different framing but same content
4. **Code comments reveal integration anti-patterns** - MCP adapter has 5 pitfalls documented inline

---

## Updated Anti-Pattern Index

After this experiment, recommended index would be:

| Category | Before | After | New |
|----------|--------|-------|-----|
| Grammar (G) | 12 | 12 | 0 |
| Testing (T) | 4 | 4 | 0 |
| Architecture (A) | 6 | 11 | +5 |
| Process (P) | 4 | 10 | +6 |
| Integration (I) | 2 | 5 | +3 |
| **Total** | **28** | **42** | **+14** |

---

## Next Steps

1. **PM Decision**: Approve adding 14 emergent anti-patterns to index?
2. **Script Development**: Create extractors for pattern sweep automation?
3. **Template Update**: Add Phase 3a to pattern sweep issue template?
4. **Memo Update**: Add experiment results to Chief Architect memo?

---

*Experiment complete. Awaiting PM decisions.*
