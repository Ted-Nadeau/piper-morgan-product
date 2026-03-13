# Phase 2 Experiment: Emergent Anti-Pattern Detection

**Date**: January 21, 2026
**Author**: Documentation Management Agent
**Status**: Design Draft

---

## Hypothesis

Undocumented anti-patterns exist in our codebase and documentation that can be detected through semantic analysis of:
1. Negative language patterns ("should not", "avoid", "don't", "problem", "issue")
2. Before/after code comparisons ("Bad:", "Wrong:", "Instead of")
3. Warning clusters (multiple cautions in close proximity)
4. Implicit contrasts (describing what something is by what it isn't)

These "emergent" anti-patterns aren't explicitly labeled as such but represent learned knowledge that should be surfaced and potentially formalized.

---

## Experiment Goals

1. **Validate detection method**: Can we reliably distinguish emergent anti-patterns from noise?
2. **Measure signal-to-noise**: What percentage of candidates are true anti-patterns vs. false positives?
3. **Assess formalization value**: Are detected anti-patterns worth adding to the index?
4. **Refine for automation**: Can this become part of the pattern sweep workflow?

---

## Detection Strategies

### Strategy 1: Negative Language Clustering

**Method**: Search for clusters of negative/cautionary language within proximity (e.g., 20 lines).

**Keywords**:
```
Primary: "should not", "must not", "never", "avoid", "don't", "do not"
Secondary: "problem", "issue", "wrong", "incorrect", "mistake", "error-prone"
Tertiary: "careful", "beware", "warning", "caution", "risk", "dangerous"
```

**Scoring**:
- 3+ primary keywords in 20 lines = HIGH signal
- 2 primary + 2 secondary = MEDIUM signal
- Scattered tertiary only = LOW signal (likely noise)

**Expected output**: Candidate passages with signal scores

### Strategy 2: Contrast Pattern Detection

**Method**: Find passages that describe incorrect approaches alongside correct ones.

**Markers**:
```
"instead of X, do Y"
"rather than X"
"not X but Y"
"X is wrong because"
"the problem with X"
"X leads to Y (negative outcome)"
```

**Validation**: Must have both negative example AND positive alternative to qualify

**Expected output**: Before/after pairs not currently in anti-pattern index

### Strategy 3: Code Comment Mining

**Method**: Extract cautionary comments from Python source files.

**Patterns**:
```python
# WARNING:
# CAUTION:
# NOTE: Don't
# TODO: Fix this anti-pattern
# HACK: (implicit anti-pattern - something is wrong)
# XXX: (marks problematic code)
# FIXME:
```

**Scope**: `services/`, `web/`, `cli/` directories

**Expected output**: Code locations with implicit anti-pattern knowledge

### Strategy 4: ADR "Rejected Alternatives" Mining

**Method**: ADRs often document rejected approaches - these are implicit anti-patterns.

**Structure**: ADRs typically have "Alternatives Considered" or "Options" sections with rejected options marked ❌

**Extraction**: Pull rejected alternatives that aren't in the anti-pattern index

**Expected output**: Architectural anti-patterns from decision history

### Strategy 5: Session Log Lessons Learned

**Method**: Mine omnibus logs and session logs for "lessons learned" and "what went wrong" sections.

**Patterns**:
```
"lesson learned"
"what went wrong"
"mistake was"
"should have"
"next time"
"in retrospect"
"root cause"
```

**Scope**: `docs/omnibus-logs/`, `dev/2026/` (recent logs)

**Expected output**: Process/methodology anti-patterns from experience

---

## Experiment Protocol

### Phase 2a: Controlled Baseline (1 hour)

**Goal**: Establish false positive rate on known content

**Method**:
1. Run all 5 strategies against files already in the anti-pattern index
2. Count how many known anti-patterns are detected (recall)
3. Count how many false positives are generated (precision)

**Success criteria**:
- Recall > 70% (finds most known anti-patterns)
- Precision > 50% (at least half of candidates are real)

### Phase 2b: Discovery Scan (2 hours)

**Goal**: Find emergent anti-patterns in unscanned content

**Scope**:
- Remaining 47 patterns (not in pilot)
- Remaining 47 ADRs (not in pilot)
- `services/` code comments
- Recent session logs (Jan 2026)

**Method**:
1. Run all 5 strategies
2. Deduplicate candidates
3. Rank by signal score
4. Manual review of top 20 candidates

**Output**: Candidate list with classifications:
- TRUE EMERGENT: Genuine anti-pattern, should add to index
- VARIATION: Related to existing indexed anti-pattern
- FALSE POSITIVE: Not actually an anti-pattern
- ALREADY INDEXED: Detection worked but already captured

### Phase 2c: Formalization (30 min)

**Goal**: Add validated emergent anti-patterns to index

**Method**:
1. Assign IDs to TRUE EMERGENT candidates
2. Determine category (G/T/A/P/I)
3. Link to source document
4. Identify recommended pattern (if any)
5. Update anti-pattern-index.md

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Recall on known | >70% | Known anti-patterns detected / total known |
| Precision | >50% | True positives / total candidates |
| New discoveries | 5-10 | TRUE EMERGENT count |
| Time efficiency | <4 hours | Total experiment time |
| Automation potential | HIGH/MED/LOW | Can strategies be scripted? |

---

## Risk Mitigation

**Risk**: High false positive rate drowns signal
**Mitigation**: Start with high-threshold scoring, tune down if recall too low

**Risk**: Duplicate detection (same anti-pattern found multiple ways)
**Mitigation**: Deduplicate by source file + line range before manual review

**Risk**: Subjective classification ("is this really an anti-pattern?")
**Mitigation**: Use existing index as calibration - if similar to indexed entry, it qualifies

**Risk**: Time sink on manual review
**Mitigation**: Cap manual review at top 20 candidates; revisit threshold if needed

---

## Tool Requirements

**Existing tools sufficient**:
- `grep` / Grep tool for keyword search
- Read tool for context extraction
- Manual classification (agent judgment)

**Optional enhancements** (not required for experiment):
- Script to calculate proximity scores
- Deduplication helper
- Candidate ranking output

---

## Pilot Execution Plan

### Step 1: Baseline calibration (30 min)
- Run Strategy 1 (negative language) against grammar-transformation-guide.md
- Verify it finds the 7 known anti-patterns
- Note any false positives
- Adjust keyword weights if needed

### Step 2: Expand to code comments (30 min)
- Run Strategy 3 against `services/`
- Collect WARNING/CAUTION/HACK comments
- Classify candidates

### Step 3: ADR rejected alternatives (30 min)
- Run Strategy 4 against ADRs not in pilot
- Extract rejected options
- Cross-reference against index

### Step 4: Session log mining (30 min)
- Run Strategy 5 against Jan 2026 omnibus logs
- Look for lessons learned
- Classify candidates

### Step 5: Synthesis (30 min)
- Deduplicate all candidates
- Rank by confidence
- Manual review top 20
- Formalize TRUE EMERGENT into index

### Step 6: Retrospective (30 min)
- Document precision/recall
- Identify best-performing strategies
- Recommend automation path
- Update experiment design for next sweep

---

## Expected Outcomes

**Optimistic**: 8-12 emergent anti-patterns discovered, precision >60%, clear automation path

**Realistic**: 5-8 emergent anti-patterns, precision ~50%, 2-3 strategies worth automating

**Pessimistic**: <5 discoveries, precision <40%, manual review required for foreseeable future

---

## Questions for PM

1. **Scope**: Should we include code comments in `tests/` or just production code?
2. **History depth**: How far back in session logs? (Jan 2026 only, or include Dec 2025?)
3. **Automation priority**: If experiment succeeds, should automation be part of Feb 3 sweep or later?
4. **Classification authority**: Should emergent anti-patterns require PM/Architect approval before indexing?

---

## Relationship to Pattern Sweep

If successful, this experiment would inform:
- **Agent D (Evolution Tracker)**: Add semantic scan to anti-pattern detection duties
- **Phase 3 expansion**: From "scan for explicit anti-patterns" to "scan + detect emergent"
- **New deliverable**: `dev/active/emergent-anti-pattern-candidates.md` per sweep

---

*Design complete. Ready for PM approval to execute.*
