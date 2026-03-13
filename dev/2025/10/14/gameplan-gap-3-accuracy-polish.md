# Gameplan: GAP-3 Accuracy Polish

**Date**: Monday, October 13, 2025, 9:00 AM
**Epic**: CORE-CRAFT-GAP (3/3 - Final Phase)
**Focus**: Classification Accuracy & Pre-Classifier Optimization
**Lead Developer**: Claude Sonnet 4.5
**PM**: Christian Crumlish

---

## Executive Summary

**Mission**: Improve intent classification accuracy from 89.3% to ≥92% (stretch: ≥95%)

**Current State** (from Pattern-032):
- Overall canonical accuracy: 89.3% (126/141 correct)
- PRIORITY: 100.0% ✅ (exceeds target)
- TEMPORAL: 96.7% ✅ (meets target)
- STATUS: 96.7% ✅ (meets target)
- IDENTITY: 76.0% ⚠️ (below target)
- GUIDANCE: 76.7% ⚠️ (below target)

**Target**: ≥92% overall accuracy (all categories ≥90%)

**Duration**: 6-8 hours (with 1 hour bonus from Phase 0 efficiency!)

---

## Context from Knowledge Base

### What We Know (From GAP-2 & Pattern-032)

**Strengths** ✅:
- TEMPORAL/STATUS/PRIORITY: Core mission categories exceed 95% target
- Pre-classifier patterns: 44 patterns across 3 categories
- Fast path performance: Sub-millisecond (<1ms)
- Infrastructure: Robust, tested, deployed (Oct 6, 2025)

**Weaknesses** ⚠️:
- IDENTITY: Capability queries sometimes misclassify as QUERY (76.0%)
- GUIDANCE: Advice requests misclassify as CONVERSATION/STRATEGY (76.7%)
- These two categories pulling down overall average

**Root Causes Identified** (from ADR-039):
- "Disambiguation rules working" for personal context
- Challenge: Distinguishing capability queries from general knowledge
- Challenge: Advice vs conversation vs strategic planning

---

## Phase 1: Accuracy Analysis (2 hours)

**Goal**: Understand why IDENTITY and GUIDANCE underperform

### Task 1.1: Data Collection (30 min)

**Agent**: Code Agent

**Actions**:
```bash
# Find test files with classification data
find tests/ -name "*intent*" -o -name "*classification*"

# Extract IDENTITY test cases
grep -A 5 "IDENTITY" tests/intent/ -r

# Extract GUIDANCE test cases
grep -A 5 "GUIDANCE" tests/intent/ -r

# Check for classification logs
find . -name "*classification*log*" -o -name "*accuracy*"
```

**Deliverables**:
- List of all IDENTITY test queries (25 queries documented)
- List of all GUIDANCE test queries (30 queries documented)
- Classification results for each
- Misclassification patterns identified

### Task 1.2: Misclassification Analysis (45 min)

**Agent**: Lead Developer

**Investigation**:
1. **IDENTITY Failures** (24% misclassification rate):
   - Which queries misclassify as QUERY?
   - What distinguishes capability from general knowledge?
   - Example: "what can you do?" vs "what's quantum computing?"

2. **GUIDANCE Failures** (23.3% misclassification rate):
   - Which queries go to CONVERSATION vs STRATEGY?
   - What patterns trigger wrong classification?
   - Example: "how should I prioritize?" → STRATEGY or GUIDANCE?

**Analysis Framework**:
```markdown
For each misclassified query:
- Query text: [actual query]
- Expected: [correct category]
- Actual: [wrong category]
- Why wrong: [hypothesis]
- Signal missing: [what would fix it]
```

**Deliverables**:
- Misclassification pattern document
- Root cause hypotheses
- Proposed fixes (patterns or prompt changes)

### Task 1.3: Pattern Gap Analysis (45 min)

**Agent**: Lead Developer + Code

**Investigation**:
```bash
# Check pre-classifier patterns
grep -A 20 "class PreClassifier" services/intent/

# IDENTITY patterns
grep "IDENTITY" services/intent/pre_classifier.py

# GUIDANCE patterns
grep "GUIDANCE" services/intent/pre_classifier.py
```

**Questions**:
- Do IDENTITY/GUIDANCE have pre-classifier patterns?
- If yes: Are they comprehensive enough?
- If no: Should we add them?
- Pattern coverage: What variants are missing?

**Deliverables**:
- Current pattern inventory for IDENTITY/GUIDANCE
- Missing pattern identification
- Pattern addition proposals

---

## Phase 2: Pre-Classifier Enhancement (2-3 hours)

**Goal**: Add patterns to improve IDENTITY and GUIDANCE accuracy

### Task 2.1: IDENTITY Pattern Addition (1 hour)

**Agent**: Code Agent

**Current State** (from investigation):
- IDENTITY accuracy: 76.0%
- Problem: Capability queries → QUERY misclassification

**Pattern Strategy**:
```python
# Focus on capability-specific signals
IDENTITY_PATTERNS = [
    # Direct capability questions
    r'\bwhat can (you|piper)( do| help)\b',
    r'\bwhat (are you|is piper) (capable|able)\b',

    # Feature questions
    r'\bwhat (features|functions|commands) (do you|does piper)\b',
    r'\bwhat (tools|integrations) (do you|does piper)\b',

    # Identity questions
    r'\b(who|what) (are you|is piper)\b',
    r'\btell me about (yourself|piper)\b',

    # Version/status questions
    r'\bwhat version (are you|is piper)\b',
    r'\b(how|when) (were you|was piper) (built|created|made)\b',
]
```

**Test Approach**:
- Run against existing 25 IDENTITY queries
- Target: Improve from 76.0% to ≥90%
- Validate no false positives on other categories

**Acceptance Criteria**:
- [ ] New patterns added to PreClassifier
- [ ] Tests pass for IDENTITY category
- [ ] No regression in other categories
- [ ] Accuracy ≥90% on IDENTITY queries

### Task 2.2: GUIDANCE Pattern Addition (1-1.5 hours)

**Agent**: Code Agent

**Current State**:
- GUIDANCE accuracy: 76.7%
- Problem: Advice → CONVERSATION/STRATEGY misclassification

**Pattern Strategy**:
```python
# Focus on how-to and advice signals
GUIDANCE_PATTERNS = [
    # How-to questions
    r'\bhow (do|can|should) (i|we|you)\b.*\?',
    r'\bwhat(\'s| is) the (best way|right way) to\b',

    # Advice requests
    r'\b(advice|guidance|help|tips|suggestions?) (on|for|about)\b',
    r'\b(should|can|could) (i|we) (use|try|do)\b',

    # Process questions
    r'\bhow to (create|make|set up|configure)\b',
    r'\bwhat steps (to|for)\b',

    # Recommendation requests
    r'\b(recommend|suggest|advise) (me|us)\b',
    r'\bwhat would you (recommend|suggest|advise)\b',
]
```

**Disambiguation** (critical):
```python
# Distinguish GUIDANCE from CONVERSATION
if "how are you" in query.lower():
    return CONVERSATION  # Not GUIDANCE!

# Distinguish GUIDANCE from STRATEGY
if any(word in query.lower() for word in ["plan", "strategy", "roadmap"]):
    # Check for how-to context
    if "how to create" in query.lower():
        return GUIDANCE  # Process help
    else:
        return STRATEGY  # Strategic planning
```

**Test Approach**:
- Run against existing 30 GUIDANCE queries
- Target: Improve from 76.7% to ≥90%
- Critical: Don't steal CONVERSATION or STRATEGY queries

**Acceptance Criteria**:
- [ ] New patterns added with disambiguation
- [ ] Tests pass for GUIDANCE category
- [ ] No regression in CONVERSATION/STRATEGY
- [ ] Accuracy ≥90% on GUIDANCE queries

### Task 2.3: Cross-Validation (30 min)

**Agent**: Cursor Agent (verification)

**Validation Tasks**:
1. Run full test suite (all 141 canonical queries)
2. Verify no regressions in TEMPORAL/STATUS/PRIORITY
3. Check boundary cases between categories
4. Measure overall accuracy improvement

**Acceptance Criteria**:
- [ ] All category tests passing
- [ ] Overall accuracy ≥92%
- [ ] No category below 90%
- [ ] Performance still sub-millisecond

---

## Phase 3: LLM Classifier Enhancement (1-2 hours)

**Goal**: Improve fallback classifier for queries that miss pre-classifier

### Task 3.1: Prompt Enhancement (45 min)

**Agent**: Lead Developer

**Current Prompt Analysis**:
```bash
# Find LLM classifier prompt
grep -A 50 "classify.*prompt" services/intent/
grep -A 50 "canonical.*category" services/intent/
```

**Enhancement Areas**:

**1. Category Definitions** (from ADR-039):
- Ensure IDENTITY clearly defined
- Ensure GUIDANCE clearly distinguished from CONVERSATION/STRATEGY
- Add disambiguation examples

**2. Example Queries**:
```python
IDENTITY_EXAMPLES = [
    "what can you do?" → IDENTITY,
    "what features does Piper have?" → IDENTITY,
    "who built you?" → IDENTITY,
    "what's quantum computing?" → QUERY  # Not IDENTITY!
]

GUIDANCE_EXAMPLES = [
    "how do I create an issue?" → GUIDANCE,
    "what's the best way to organize sprints?" → GUIDANCE,
    "hey how are you?" → CONVERSATION,  # Not GUIDANCE!
    "plan our Q4 strategy" → STRATEGY,  # Not GUIDANCE!
]
```

**3. Disambiguation Rules**:
- Personal pronouns (I, my, our) + action → Canonical
- General knowledge questions → QUERY
- Capability questions → IDENTITY
- How-to process questions → GUIDANCE
- Strategic planning → STRATEGY

**Deliverables**:
- Updated LLM classifier prompt
- Clear category definitions
- Disambiguation rules documented

### Task 3.2: Validation Testing (45 min)

**Agent**: Code Agent

**Test Scenarios**:
1. **IDENTITY Edge Cases**:
   - "what can you do" → IDENTITY ✓
   - "what's machine learning" → QUERY ✓
   - "tell me about yourself" → IDENTITY ✓
   - "tell me about Python" → QUERY ✓

2. **GUIDANCE Edge Cases**:
   - "how do I create an issue" → GUIDANCE ✓
   - "how are you doing" → CONVERSATION ✓
   - "how should we plan Q4" → STRATEGY ✓
   - "what's the best way to code" → GUIDANCE ✓

**Test Method**:
```bash
# Run with updated prompt
pytest tests/intent/ -v -k "identity or guidance"

# Check accuracy on edge cases
python -m services.intent.test_edge_cases
```

**Acceptance Criteria**:
- [ ] Edge cases correctly classified
- [ ] No boundary confusion
- [ ] Accuracy improvement measurable

---

## Phase 4: Documentation & Validation (1-2 hours)

**Goal**: Document improvements and validate final accuracy

### Task 4.1: Update Pattern Catalog (30 min)

**Agent**: Lead Developer

**Files to Update**:
1. `docs/patterns/pattern-032-intent-pattern-catalog.md`
2. `docs/architecture/adr-039-canonical-handler-pattern.md`

**Updates Needed**:
- New IDENTITY pattern count
- New GUIDANCE pattern count
- Updated accuracy metrics
- New overall accuracy percentage
- Date stamp: October 13, 2025

**Template**:
```markdown
### Classification Accuracy Metrics (Updated October 13, 2025)

**Post-GAP-3 Enhancement**:

| Category | Accuracy | Status | Patterns | Notes |
|----------|----------|--------|----------|-------|
| PRIORITY | 100.0% | ✅ Perfect | 13 | No changes needed |
| TEMPORAL | 96.7% | ✅ Exceeds | 17 | No changes needed |
| STATUS | 96.7% | ✅ Exceeds | 14 | No changes needed |
| IDENTITY | XX.X% | ✅/⚠️ | XX | Improved from 76.0% |
| GUIDANCE | XX.X% | ✅/⚠️ | XX | Improved from 76.7% |

**Overall canonical accuracy**: XX.X% (XXX correct / 141 total)
**Improvement**: +X.X percentage points from GAP-2 baseline
```

### Task 4.2: Performance Benchmarking (30 min)

**Agent**: Code Agent

**Benchmarks to Run**:
```bash
# Response time (should still be <1ms)
pytest tests/performance/test_canonical_response_time.py

# Classification accuracy
pytest tests/intent/test_classification_accuracy.py -v

# Full integration
pytest tests/integration/ -v -k "intent"
```

**Metrics to Capture**:
- Average response time per category
- Accuracy per category
- Overall accuracy
- Performance regression check (must stay <1ms)

**Acceptance Criteria**:
- [ ] Response time <1ms maintained
- [ ] Accuracy ≥92% overall
- [ ] All categories ≥90%
- [ ] No performance degradation

### Task 4.3: Create Completion Evidence (30 min)

**Agent**: Lead Developer

**Evidence Document**: `dev/2025/10/13/gap-3-completion-evidence.md`

**Contents**:
```markdown
# GAP-3 Completion Evidence

**Date**: October 13, 2025
**Epic**: CORE-CRAFT-GAP
**Phase**: 3 of 3 (Final)

## Objectives Achieved

### Primary Goal: Accuracy ≥92%
- **Before**: 89.3% (126/141 correct)
- **After**: XX.X% (XXX/141 correct)
- **Improvement**: +X.X percentage points
- **Status**: ✅ Target met

### Category Improvements

**IDENTITY**: 76.0% → XX.X%
- New patterns added: X patterns
- Misclassification reduction: X.X%
- Key improvements: [list]

**GUIDANCE**: 76.7% → XX.X%
- New patterns added: X patterns
- Disambiguation rules: [list]
- Key improvements: [list]

### Performance Maintained

- Response time: XX.Xms (target: <1ms)
- Throughput: [metrics]
- Cache hit rate: XX.X%
- Status: ✅ Performance maintained

## Technical Changes

### Pre-Classifier Enhancements
- Files modified: [list]
- Patterns added: [count]
- Tests updated: [count]

### LLM Classifier Enhancements
- Prompt updated: [Yes/No]
- Disambiguation rules: [count]
- Edge cases handled: [count]

## Test Results

[Paste test output showing all passing]

## Documentation Updated

- [ ] Pattern-032 updated with new metrics
- [ ] ADR-039 updated with accuracy improvements
- [ ] Completion evidence created

## Handoff Notes

**What Works**: [summary]
**What's Next**: [future improvements if any]
**Known Issues**: [if any]

---

**GAP-3 Status**: ✅ COMPLETE
**CORE-CRAFT-GAP Epic**: ✅ COMPLETE (3/3 phases)
```

---

## Phase 5: Epic Completion (30 min)

**Goal**: Close out CORE-CRAFT-GAP epic

### Task 5.1: Epic Summary Document

**Agent**: Lead Developer

**File**: `dev/2025/10/13/CORE-CRAFT-GAP-completion.md`

**Contents**:
- GAP-1 summary (validation & prevention) ✅
- GAP-2 summary (infrastructure modernization) ✅
- GAP-3 summary (accuracy polish) ✅
- Total epic achievement
- Lessons learned
- Recommendations for next epic

### Task 5.2: GitHub Issue Updates

**Actions**:
- Close GAP-3 issue
- Close CORE-CRAFT-GAP epic
- Update project board
- Link completion evidence

---

## Success Metrics

### Primary Metrics
- [ ] Overall accuracy ≥92% (stretch: ≥95%)
- [ ] All categories ≥90% accuracy
- [ ] IDENTITY improvement ≥14 percentage points
- [ ] GUIDANCE improvement ≥13 percentage points
- [ ] Performance maintained (<1ms)

### Documentation Metrics
- [ ] Pattern-032 updated
- [ ] ADR-039 updated
- [ ] Completion evidence created
- [ ] Epic summary documented

### Quality Metrics
- [ ] All tests passing
- [ ] No performance regression
- [ ] No new bugs introduced
- [ ] Code quality maintained

---

## Risk Management

### Known Risks

**Risk 1: Pattern Overlap**
- New patterns might match wrong categories
- **Mitigation**: Careful pattern ordering, thorough testing
- **Fallback**: Can revert specific patterns if needed

**Risk 2: Performance Degradation**
- More patterns might slow pre-classifier
- **Mitigation**: Benchmark after each change
- **Threshold**: Must stay <1ms

**Risk 3: Can't Reach 92% Target**
- Categories might be inherently ambiguous
- **Mitigation**: Focus on highest-impact improvements
- **Fallback**: Document achieved accuracy, defer to future

### STOP Conditions
- Accuracy improvements break other categories
- Performance degrades beyond acceptable (<1ms)
- Tests start failing without clear fix
- Time exceeds 8 hours (end of day)

---

## Timeline

**Phase 1: Accuracy Analysis**
9:00 AM - 11:00 AM (2 hours)
- Data collection
- Misclassification analysis
- Pattern gap analysis

**Phase 2: Pre-Classifier Enhancement**
11:00 AM - 2:00 PM (3 hours)
- IDENTITY patterns (1 hour)
- GUIDANCE patterns (1.5 hours)
- Cross-validation (30 min)

**Break**: 2:00 PM - 2:30 PM (30 min)

**Phase 3: LLM Classifier Enhancement**
2:30 PM - 4:00 PM (1.5 hours)
- Prompt enhancement (45 min)
- Validation testing (45 min)

**Phase 4: Documentation & Validation**
4:00 PM - 5:30 PM (1.5 hours)
- Update pattern catalog (30 min)
- Performance benchmarking (30 min)
- Completion evidence (30 min)

**Phase 5: Epic Completion**
5:30 PM - 6:00 PM (30 min)
- Epic summary
- GitHub updates
- Handoff preparation

**Total**: 8.5 hours (9:00 AM - 6:00 PM with 30 min break)

---

## Agent Deployment Strategy

**Code Agent**:
- Data collection (Phase 1.1)
- Pattern implementation (Phase 2.1, 2.2)
- Test execution (Phase 3.2, 4.2)

**Cursor Agent**:
- Cross-validation (Phase 2.3)
- Verification testing throughout

**Lead Developer**:
- Misclassification analysis (Phase 1.2, 1.3)
- Prompt enhancement (Phase 3.1)
- Documentation (Phase 4.1, 4.3, 5.1)
- Overall coordination

---

## Philosophy in Action

**Push to 100%**: Not stopping at "good enough" - targeting excellence
**Evidence-Based**: Every change validated with data
**Cathedral Building**: Quality that lasts, not quick fixes
**Time Lord**: Quality over deadline (but we're ahead of schedule!)

---

## Notes for PM

**Why This Feels Right**:
- Addresses known weaknesses (IDENTITY, GUIDANCE)
- Builds on GAP-2 infrastructure work
- Completes the CORE-CRAFT-GAP mission
- Foundation is solid (Phase 0 complete)

**What Makes This Achievable**:
- Clear metrics (89.3% → 92%+)
- Identified root causes
- Proven patterns work (TEMPORAL/STATUS/PRIORITY)
- Infrastructure ready (tests, benchmarks, docs)

**Success Indicators**:
- Every category performing well
- User experience improved
- Architecture maintained
- Documentation complete

---

**Gameplan Status**: Ready for execution
**Start Time**: 9:05 AM (after VA standup)
**Expected Completion**: 5:30-6:00 PM
**Bonus**: 1 hour ahead from Phase 0 efficiency!

**LET'S ACHIEVE 92%+ ACCURACY! 🎯**
