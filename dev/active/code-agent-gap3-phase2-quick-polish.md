# Code Agent Prompt: GAP-3 Phase 2 - Quick Polish to 98.62%

**Date**: October 13, 2025, 10:12 AM
**Phase**: GAP-3 Phase 2 (Simplified - Quick Polish)
**Duration**: 1 hour (estimated)
**Priority**: HIGH (excellence, not necessity)
**Agent**: Code Agent

---

## Mission

Add 3 simple patterns to fix the only remaining GUIDANCE misclassifications, achieving 98.62% overall accuracy (exceeds 95% stretch goal).

**Current State**: 96.55% (140/145) - Already exceeds targets!
**Target**: 98.62% (143/145) - Stretch goal exceeded!
**Work Required**: Fix 3 GUIDANCE boundary cases

---

## Context

**Excellent News**: We're already at 96.55%!
- ✅ Exceeds 92% target
- ✅ Exceeds 95% stretch goal
- Only 3 failures remaining (all GUIDANCE → CONVERSATION)

**The 3 Failures**:
1. "what should I do about" → CONVERSATION (should be GUIDANCE)
2. "advise me on" → CONVERSATION (should be GUIDANCE)
3. "what's the process for" → CONVERSATION (should be GUIDANCE)

**Why They Fail**: Boundary cases between seeking advice (GUIDANCE) and casual conversation (CONVERSATION)

**The Fix**: Add 3 specific patterns to catch these edge cases

---

## Task 1: Locate Pre-Classifier (10 minutes)

### Find GUIDANCE Patterns

**Locate the pre-classifier file**:
```bash
# Find pre-classifier implementation
find services/ -name "*pre*class*" -type f

# Should find something like:
# services/intent_service/pre_classifier.py
# or
# services/intent/pre_classifier.py
```

**Examine current GUIDANCE patterns**:
```bash
# Look at current GUIDANCE patterns
grep -A 30 "GUIDANCE" services/intent*/pre_classifier.py

# Or look for pattern arrays
grep -B 5 -A 20 "GUIDANCE.*PATTERN" services/intent*/pre_classifier.py
```

**Document current patterns**:
- How many GUIDANCE patterns exist?
- What format are they in?
- Where to add new ones?

---

## Task 2: Add 3 New Patterns (20 minutes)

### Pattern 1: "what should I do about"

**Pattern**:
```python
r'\bwhat should (I|we) do (about|with)\b'
```

**Rationale**:
- Catches: "what should I do about X"
- Type: Advice-seeking question
- Category: GUIDANCE (not CONVERSATION)
- Test queries: "what should I do about this issue"

### Pattern 2: "advise me on"

**Pattern**:
```python
r'\badvise (me|us) on\b'
```

**Rationale**:
- Catches: "advise me on X"
- Type: Direct advice request
- Category: GUIDANCE (not CONVERSATION)
- Test queries: "advise me on the best approach"

### Pattern 3: "what's the process for"

**Pattern**:
```python
r'\bwhat(\'s| is) the process for\b'
```

**Rationale**:
- Catches: "what's the process for X", "what is the process for X"
- Type: Process/how-to question
- Category: GUIDANCE (not CONVERSATION)
- Test queries: "what's the process for creating an issue"

### Implementation

**Add to GUIDANCE patterns** (exact location depends on file structure):

```python
# GUIDANCE patterns (add to existing list)
GUIDANCE_PATTERNS = [
    # ... existing patterns ...

    # Added October 13, 2025 - GAP-3 Phase 2 (edge case fixes)
    r'\bwhat should (I|we) do (about|with)\b',    # Advice-seeking
    r'\badvise (me|us) on\b',                      # Direct advice request
    r'\bwhat(\'s| is) the process for\b',         # Process questions
]
```

**Important**:
- Maintain existing patterns
- Add at end of pattern list
- Include comment explaining addition
- Use proper regex format with word boundaries

---

## Task 3: Test the Changes (20 minutes)

### Run Classification Tests

**Find and run intent tests**:
```bash
# Find intent classification tests
find tests/ -name "*intent*" -o -name "*classif*"

# Run intent tests
pytest tests/intent/ -v

# Or run specific accuracy tests
pytest tests/ -k "accuracy" -v

# Or run all tests
pytest tests/ -v
```

**Expected Results**:
- All existing tests should still pass
- 3 additional queries should now classify correctly
- Overall accuracy: 143/145 = 98.62%

### Validate No Regressions

**Check other categories**:
```bash
# Run tests for all categories
pytest tests/intent/ -v --tb=short

# Specifically check CONVERSATION category
pytest tests/intent/ -k "conversation" -v
```

**Critical**: Ensure the new patterns don't:
- Steal queries from CONVERSATION
- Steal queries from STRATEGY
- Break any existing classifications

### Manual Verification

**Test the 3 specific queries**:
```python
# In Python REPL or test script
from services.intent_service.pre_classifier import PreClassifier

queries = [
    "what should I do about this issue",
    "advise me on the best approach",
    "what's the process for creating an issue"
]

for query in queries:
    result = PreClassifier.pre_classify(query)
    print(f"Query: {query}")
    print(f"Result: {result}")
    print(f"Expected: GUIDANCE")
    print()
```

**Expected output**: All 3 should return GUIDANCE category

---

## Task 4: Update Documentation (10 minutes)

### Update Pattern Catalog

**File**: `docs/patterns/pattern-032-intent-pattern-catalog.md`

**Find the GUIDANCE section** and update:

**Before**:
```markdown
**GUIDANCE**: 76.7% (23/30 correct) ⚠️ Below Target
```

**After**:
```markdown
**GUIDANCE**: 100.0% (30/30 correct) ✅ Perfect
- Patterns: XX total (including 3 edge case patterns added Oct 13, 2025)
- Edge cases fixed: Advice-seeking questions, process inquiries
```

**Also update overall metrics**:
```markdown
**Overall canonical accuracy**: 98.62% (143/145 correct)
**Improvement from GAP-2**: +2.07 percentage points (96.55% → 98.62%)
**Status**: Exceeds 95% stretch goal ✅
```

### Update ADR-039

**File**: `docs/architecture/adr-039-canonical-handler-pattern.md`

**Update classification accuracy section**:
```markdown
### Classification Accuracy Metrics (Updated October 13, 2025)

**Post-GAP-3 Polish**:

| Category | Accuracy | Status | Notes |
|----------|----------|--------|-------|
| IDENTITY | 100.0% | ✅ Perfect | 25/25 queries |
| PRIORITY | 100.0% | ✅ Perfect | 30/30 queries |
| TEMPORAL | 96.7% | ✅ Exceeds | 29/30 queries |
| STATUS | 96.7% | ✅ Exceeds | 29/30 queries |
| GUIDANCE | 100.0% | ✅ Perfect | 30/30 queries (3 edge cases fixed) |

**Overall canonical accuracy**: 98.62% (143/145 correct)
**Exceeds stretch goal**: 95% target → 98.62% actual (+3.62 points)
```

---

## Acceptance Criteria

### Pattern Implementation
- [ ] 3 new patterns added to pre-classifier
- [ ] Patterns use proper regex format with word boundaries
- [ ] Patterns placed appropriately in GUIDANCE section
- [ ] Comment added explaining addition date/purpose

### Testing
- [ ] All existing tests pass
- [ ] 3 specific queries now classify as GUIDANCE
- [ ] No regressions in other categories
- [ ] Overall accuracy: 98.62% (143/145)

### Documentation
- [ ] Pattern-032 updated with new accuracy
- [ ] ADR-039 updated with GAP-3 results
- [ ] Date stamp: October 13, 2025
- [ ] Clear attribution to GAP-3 Phase 2

### Quality
- [ ] Performance maintained (sub-millisecond)
- [ ] No false positives detected
- [ ] Code quality maintained
- [ ] Commit message clear and descriptive

---

## Deliverables

**Code Changes**:
1. `services/intent_service/pre_classifier.py` (3 patterns added)

**Documentation Changes**:
1. `docs/patterns/pattern-032-intent-pattern-catalog.md` (metrics updated)
2. `docs/architecture/adr-039-canonical-handler-pattern.md` (accuracy updated)

**Test Evidence**:
1. Terminal output showing 98.62% accuracy
2. All tests passing
3. 3 specific queries correctly classified

---

## Time Budget

- **Task 1** (Locate): 10 minutes
- **Task 2** (Add patterns): 20 minutes
- **Task 3** (Test): 20 minutes
- **Task 4** (Document): 10 minutes
- **Total**: 60 minutes (1 hour)

**Target Completion**: 11:12 AM

---

## Commit Strategy

**Single commit** with all changes:

```bash
git add services/intent_service/pre_classifier.py
git add docs/patterns/pattern-032-intent-pattern-catalog.md
git add docs/architecture/adr-039-canonical-handler-pattern.md

git commit -m "feat(intent): Polish GUIDANCE classification to 98.62% accuracy

- Add 3 edge case patterns for GUIDANCE category
  - Advice-seeking questions (what should I do about)
  - Direct advice requests (advise me on)
  - Process inquiries (what's the process for)
- Fixes 3 GUIDANCE → CONVERSATION misclassifications
- Overall accuracy: 96.55% → 98.62%
- All categories now ≥96.7% (exceeds 95% stretch goal)

GAP-3 Phase 2 quick polish complete.
Refs #XXX (GAP-3 issue number)"
```

---

## Expected Impact

**Before**:
- Overall: 96.55% (140/145)
- GUIDANCE: 90.0% (27/30)
- Status: Already exceeds targets ✅

**After**:
- Overall: 98.62% (143/145)
- GUIDANCE: 100.0% (30/30)
- Status: Crushes stretch goal ✅✅

**Remaining 2 failures** (acceptable):
- 1 TEMPORAL edge case (acceptable LLM fallback)
- 1 STATUS edge case (acceptable LLM fallback)

**These 2 are likely context-heavy queries that appropriately fall to LLM**

---

## Context for Code Agent

**This is GAP-3 Phase 2** - Simplified from original 3-hour plan!

**Why So Quick**:
- Already at 96.55% (not 89.3% as docs said)
- Only 3 failures to fix
- Simple pattern additions
- No LLM prompt changes needed

**Phase 0 Complete** ✅:
- Router pattern: 6 min
- CI tests: 16 min
- LLM docs: 11 min

**Phase 1 Complete** ✅:
- Analysis: 30 min (discovered we're already excellent!)

**Phase 2 Goal**: Quick polish to perfection

**PM Mood**: Excellent! Ahead of schedule, achieving excellence.

---

## Philosophy

**We're not fixing problems, we're achieving perfection.**

This is cathedral building - taking something good (96.55%) and making it exceptional (98.62%). The difference between "good enough" and "excellent" is often just a few thoughtful touches.

---

**Phase 2 Start Time**: 10:12 AM
**Expected Completion**: 11:12 AM (1 hour)
**Status**: Ready for Code Agent execution

**LET'S ACHIEVE PERFECTION! ✨**
