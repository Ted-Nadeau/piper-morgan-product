# Code Agent Prompt: GAP-3 Phase 1 - Accuracy Analysis

**Date**: October 13, 2025, 9:29 AM
**Phase**: GAP-3 Phase 1 (Analysis)
**Duration**: 2 hours (estimated)
**Priority**: HIGH (accuracy improvements)
**Agent**: Code Agent

---

## Mission

Investigate why IDENTITY and GUIDANCE categories underperform and identify specific patterns needed to improve accuracy from current levels to ≥90% for each category.

**Current State**:
- Overall accuracy: 89.3% (126/141 correct)
- IDENTITY: 76.0% (19/25 correct) ⚠️
- GUIDANCE: 76.7% (23/30 correct) ⚠️
- Target: ≥90% for both categories

**Goal**: Understand failure patterns and propose specific fixes

---

## Context

**What We Know** (from Pattern-032):

**Strong Categories** ✅:
- PRIORITY: 100.0% (25/25 correct)
- TEMPORAL: 96.7% (29/30 correct)
- STATUS: 96.7% (29/30 correct)

**Weak Categories** ⚠️:
- IDENTITY: 76.0% (6 misclassifications)
- GUIDANCE: 76.7% (7 misclassifications)

**Why This Matters**:
- These two categories pull overall average below 92% target
- Need +14 percentage points for IDENTITY
- Need +13.3 percentage points for GUIDANCE
- Fixing these gets us to target

---

## Task 1: Locate and Extract Test Data (30 minutes)

### Step 1.1: Find Intent Test Files

**Search for test files**:
```bash
# Find all intent-related test files
find tests/ -name "*intent*" -type f

# Find classification test files
find tests/ -name "*classif*" -type f

# Find accuracy test files
find tests/ -name "*accuracy*" -type f

# Check for test data directories
find tests/ -type d -name "*data*" -o -name "*fixtures*"
```

### Step 1.2: Extract IDENTITY Test Cases

**Look for IDENTITY tests**:
```bash
# Search for IDENTITY category in tests
grep -r "IDENTITY" tests/ --include="*.py" -A 3 -B 1

# Look for identity-related queries
grep -r "who are you\|what can you\|what do you do" tests/ --include="*.py"

# Check for test fixtures
find tests/ -name "*identity*" -o -name "*IDENTITY*"
```

**Expected to find**:
- 25 IDENTITY test queries
- Expected classification results
- Actual classification results (if logged)

### Step 1.3: Extract GUIDANCE Test Cases

**Look for GUIDANCE tests**:
```bash
# Search for GUIDANCE category in tests
grep -r "GUIDANCE" tests/ --include="*.py" -A 3 -B 1

# Look for guidance-related queries
grep -r "how do I\|how to\|how can I\|best way" tests/ --include="*.py"

# Check for test fixtures
find tests/ -name "*guidance*" -o -name "*GUIDANCE*"
```

**Expected to find**:
- 30 GUIDANCE test queries
- Expected classification results
- Actual classification results

### Step 1.4: Create Test Data Inventory

**Create file**: `dev/2025/10/13/gap-3-phase1-test-data.md`

**Structure**:
```markdown
# GAP-3 Phase 1: Test Data Inventory

**Date**: October 13, 2025
**Agent**: Code Agent

## IDENTITY Test Cases (25 queries)

| # | Query | Expected | Current Result | Status |
|---|-------|----------|----------------|--------|
| 1 | "who are you?" | IDENTITY | IDENTITY | ✅ |
| 2 | "what can you do?" | IDENTITY | QUERY | ❌ |
| ... | ... | ... | ... | ... |

**IDENTITY Summary**:
- Total queries: 25
- Correct: 19 (76.0%)
- Incorrect: 6 (24.0%)
- Misclassified as QUERY: X
- Misclassified as other: X

## GUIDANCE Test Cases (30 queries)

| # | Query | Expected | Current Result | Status |
|---|-------|----------|----------------|--------|
| 1 | "how do I create an issue?" | GUIDANCE | GUIDANCE | ✅ |
| 2 | "how are you doing?" | CONVERSATION | GUIDANCE | ❌ |
| ... | ... | ... | ... | ... |

**GUIDANCE Summary**:
- Total queries: 30
- Correct: 23 (76.7%)
- Incorrect: 7 (23.3%)
- Misclassified as CONVERSATION: X
- Misclassified as STRATEGY: X
- Misclassified as other: X

## Key Findings

[Your observations about patterns]
```

---

## Task 2: Analyze Misclassifications (45 minutes)

### Step 2.1: Categorize IDENTITY Failures

**For each IDENTITY misclassification**:

1. **Extract the query**
2. **Identify why it failed**
3. **Propose a pattern that would catch it**

**Analysis Template**:
```markdown
### IDENTITY Misclassification #1

**Query**: "what features do you have?"
**Expected**: IDENTITY
**Actual**: QUERY
**Why Failed**: Contains "what" + generic noun, looks like knowledge query
**Missing Signal**: "you have" + feature-related word
**Proposed Pattern**: r'\bwhat (features|capabilities|functions) (do you|does piper)\b'
**Would This Fix It**: Yes - directly matches capability inquiry

---
```

**Create file**: `dev/2025/10/13/gap-3-identity-failures.md`

### Step 2.2: Categorize GUIDANCE Failures

**For each GUIDANCE misclassification**:

1. **Extract the query**
2. **Identify why it failed**
3. **Understand the confusion** (CONVERSATION vs GUIDANCE vs STRATEGY)
4. **Propose disambiguation**

**Analysis Template**:
```markdown
### GUIDANCE Misclassification #1

**Query**: "how should I prioritize my work?"
**Expected**: GUIDANCE
**Actual**: STRATEGY
**Why Failed**: "how should I" + "prioritize" triggers strategic planning
**Disambiguation Needed**: Personal task prioritization vs strategic planning
**Key Signal**: Personal pronoun ("I", "my") + process question
**Proposed Pattern**: r'\bhow (should|can|do) I\b.*\bprioritize\b'
**Disambiguation Rule**: Personal + how-to = GUIDANCE, not STRATEGY

---
```

**Create file**: `dev/2025/10/13/gap-3-guidance-failures.md`

### Step 2.3: Pattern Commonalities

**Look for patterns across failures**:

**IDENTITY Failures - Common Themes**:
- [ ] Capability questions without "you" pronoun?
- [ ] Feature inquiries using generic words?
- [ ] Version/status questions?
- [ ] Background/creation questions?

**GUIDANCE Failures - Common Themes**:
- [ ] "How are you" being captured as GUIDANCE (should be CONVERSATION)?
- [ ] Strategic questions captured as GUIDANCE (should be STRATEGY)?
- [ ] Process questions lacking clear how-to markers?
- [ ] Advice requests without clear signals?

**Create file**: `dev/2025/10/13/gap-3-failure-patterns.md`

---

## Task 3: Check Existing Pre-Classifier Patterns (30 minutes)

### Step 3.1: Examine Current Pre-Classifier

**Locate pre-classifier code**:
```bash
# Find pre-classifier implementation
find services/ -name "*pre*class*" -type f

# Look at pre-classifier patterns
grep -A 100 "class PreClassifier" services/intent/

# Check IDENTITY patterns
grep -A 20 "IDENTITY" services/intent/*pre*.py

# Check GUIDANCE patterns
grep -A 20 "GUIDANCE" services/intent/*pre*.py
```

**Document current state**:
```markdown
# Current Pre-Classifier Patterns

## IDENTITY Category

**Patterns Found**: [count]

```python
# Paste actual patterns here
IDENTITY_PATTERNS = [
    # List current patterns
]
```

**Coverage Analysis**:
- Covers: [what types of queries]
- Missing: [what types fail]

## GUIDANCE Category

**Patterns Found**: [count]

```python
# Paste actual patterns here
GUIDANCE_PATTERNS = [
    # List current patterns
]
```

**Coverage Analysis**:
- Covers: [what types of queries]
- Missing: [what types fail]
```

**Create file**: `dev/2025/10/13/gap-3-current-patterns.md`

### Step 3.2: Pattern Gap Analysis

**Compare failures to existing patterns**:

1. **For IDENTITY**:
   - Do current patterns address the 6 failures?
   - What new patterns are needed?
   - Would new patterns conflict with existing?

2. **For GUIDANCE**:
   - Do current patterns address the 7 failures?
   - What disambiguation is needed?
   - Would new patterns steal from CONVERSATION/STRATEGY?

**Create file**: `dev/2025/10/13/gap-3-pattern-gaps.md`

---

## Task 4: Propose Pattern Additions (30 minutes)

### Step 4.1: IDENTITY Pattern Proposals

**Based on failure analysis, propose specific patterns**:

**Format**:
```python
# Proposed IDENTITY Patterns (to add to pre-classifier)

IDENTITY_NEW_PATTERNS = [
    # Pattern 1: [description]
    r'\bpattern here\b',
    # Rationale: [why this helps]
    # Catches: [examples]
    # Misses: [what it won't catch - that's OK]

    # Pattern 2: [description]
    r'\banother pattern\b',
    # Rationale: [why this helps]

    # ... etc
]

# Expected Impact:
# - Should catch X additional queries
# - Would improve IDENTITY from 76.0% to ~XX.X%
# - Risk of false positives: [low/medium/high]
```

**Create file**: `dev/2025/10/13/gap-3-identity-proposals.md`

### Step 4.2: GUIDANCE Pattern Proposals

**Based on failure analysis, propose specific patterns WITH disambiguation**:

**Format**:
```python
# Proposed GUIDANCE Patterns (to add to pre-classifier)

GUIDANCE_NEW_PATTERNS = [
    # Pattern 1: [description]
    r'\bpattern here\b',
    # Rationale: [why this helps]
    # Catches: [examples]
    # Disambiguation: [how to avoid CONVERSATION/STRATEGY confusion]

    # Pattern 2: [description]
    r'\banother pattern\b',
    # Rationale: [why this helps]
    # Disambiguation: [rules]

    # ... etc
]

# Disambiguation Rules:
GUIDANCE_DISAMBIGUATION = {
    "CONVERSATION": [
        # If query matches these, prefer CONVERSATION over GUIDANCE
        r'\bhow are you\b',
        r'\bhow('s| is) it going\b',
    ],
    "STRATEGY": [
        # If query matches these, prefer STRATEGY over GUIDANCE
        r'\bplan\b.*\b(quarter|sprint|strategy|roadmap)\b',
        r'\bstrategic\b',
    ]
}

# Expected Impact:
# - Should catch X additional queries
# - Would improve GUIDANCE from 76.7% to ~XX.X%
# - Disambiguation reduces false positives
```

**Create file**: `dev/2025/10/13/gap-3-guidance-proposals.md`

---

## Deliverables

**Phase 1 Complete Deliverables**:

1. ✅ **Test Data Inventory** (`gap-3-phase1-test-data.md`)
   - All 25 IDENTITY queries documented
   - All 30 GUIDANCE queries documented
   - Misclassification counts

2. ✅ **IDENTITY Failure Analysis** (`gap-3-identity-failures.md`)
   - Each of 6 failures analyzed
   - Root causes identified
   - Patterns proposed

3. ✅ **GUIDANCE Failure Analysis** (`gap-3-guidance-failures.md`)
   - Each of 7 failures analyzed
   - Confusion patterns identified
   - Disambiguation rules proposed

4. ✅ **Failure Pattern Summary** (`gap-3-failure-patterns.md`)
   - Common themes across failures
   - Systemic issues identified

5. ✅ **Current Pattern Inventory** (`gap-3-current-patterns.md`)
   - Existing IDENTITY patterns documented
   - Existing GUIDANCE patterns documented
   - Coverage analysis

6. ✅ **Pattern Gap Analysis** (`gap-3-pattern-gaps.md`)
   - What's missing from current patterns
   - Why failures occur

7. ✅ **IDENTITY Pattern Proposals** (`gap-3-identity-proposals.md`)
   - Specific patterns to add
   - Expected impact (76% → XX%)

8. ✅ **GUIDANCE Pattern Proposals** (`gap-3-guidance-proposals.md`)
   - Specific patterns to add
   - Disambiguation rules
   - Expected impact (77% → XX%)

---

## Acceptance Criteria

**Data Collection**:
- [ ] All 25 IDENTITY test queries found and documented
- [ ] All 30 GUIDANCE test queries found and documented
- [ ] Misclassifications clearly identified

**Analysis**:
- [ ] Each IDENTITY failure analyzed with root cause
- [ ] Each GUIDANCE failure analyzed with confusion type
- [ ] Common patterns identified across failures

**Pattern Work**:
- [ ] Current pre-classifier patterns documented
- [ ] Gaps clearly identified
- [ ] Specific new patterns proposed

**Impact Estimation**:
- [ ] Estimated improvement for IDENTITY (target: ≥90%)
- [ ] Estimated improvement for GUIDANCE (target: ≥90%)
- [ ] Risk assessment for false positives

**Quality**:
- [ ] All deliverables in `dev/2025/10/13/` directory
- [ ] Clear, actionable recommendations
- [ ] Ready for implementation in Phase 2

---

## Time Budget

- **Task 1** (Data Collection): 30 minutes
- **Task 2** (Misclassification Analysis): 45 minutes
- **Task 3** (Current Pattern Check): 30 minutes
- **Task 4** (Pattern Proposals): 30 minutes
- **Buffer**: 15 minutes
- **Total**: 2 hours 30 minutes (includes buffer)

**Target Completion**: 11:30 AM (allowing extra 30 min buffer)

---

## Expected Findings

**Likely IDENTITY Patterns Needed**:
- Capability questions: "what can you do", "what features"
- Identity questions: "who are you", "what are you"
- Version questions: "what version", "when were you built"
- Tool questions: "what tools", "what integrations"

**Likely GUIDANCE Patterns Needed**:
- How-to questions: "how do I", "how can I", "how to"
- Best practice questions: "best way to", "right way to"
- Advice requests: "advice on", "help with", "tips for"
- Process questions: "what steps", "how should I"

**Likely Disambiguation Rules**:
- "how are you" → CONVERSATION (not GUIDANCE)
- "how should we plan Q4" → STRATEGY (not GUIDANCE)
- "how do I create issue" → GUIDANCE (not STRATEGY)
- Personal pronouns + process → GUIDANCE
- Strategic keywords → STRATEGY

---

## Context for Code Agent

**This is GAP-3 Phase 1** - Analysis phase before implementation.

**Phase 0 Complete** ✅:
- Router pattern fixed (6 min)
- CI tests fixed (16 min)
- LLM architecture documented (11 min)
- 87 minutes ahead of schedule!

**Why This Matters**:
- IDENTITY and GUIDANCE are pulling down overall accuracy
- Need detailed understanding before adding patterns
- Pattern additions in Phase 2 will be precise, not guesswork

**PM Mood**: Excellent! Foundation work complete, now accuracy polish.

**Philosophy**: Evidence-based improvements. Understand before acting.

---

## Next Steps After Phase 1

**Hand off to Lead Developer**:
- Review analysis
- Validate pattern proposals
- Make strategic decisions

**Then Phase 2**:
- Implement proposed patterns
- Test accuracy improvements
- Validate no regressions

---

**Phase 1 Start Time**: 9:29 AM
**Expected Completion**: 11:30 AM (2 hours + 30 min buffer)
**Status**: Ready for Code Agent execution

**LET'S ANALYZE! 🔍**
