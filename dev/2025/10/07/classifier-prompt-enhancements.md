# Classifier Prompt Enhancements - GREAT-4F Phase 2

**Date**: October 7, 2025
**Agent**: Cursor Agent
**Mission**: Enhance classifier prompts to improve canonical category accuracy from 85-95% to 95%+

---

## Changes Made

### File Modified: `services/intent_service/prompts.py`

**Problem Identified**: The main classification prompt was missing the canonical categories (TEMPORAL, STATUS, PRIORITY, IDENTITY, GUIDANCE) that exist in the system, causing the LLM to default to QUERY for these intents.

### 1. Added Missing Canonical Categories

**Before**: Only had workflow categories (EXECUTION, ANALYSIS, etc.)
**After**: Added complete canonical category section with clear descriptions

```markdown
## Canonical Categories (Fast-Path Processing)

- IDENTITY: Who am I, my role, my information
- TEMPORAL: Time-related queries (calendar, schedule, meetings, dates)
- STATUS: Current work status, progress, standup updates
- PRIORITY: What to focus on, importance ranking, priorities
- GUIDANCE: How-to questions, advice, best practices
```

### 2. Added Comprehensive Disambiguation Rules

Added detailed rules for distinguishing canonical categories from QUERY:

#### TEMPORAL vs QUERY

- **TEMPORAL**: Personal time-related queries (my calendar, my meetings)
- **QUERY**: General time facts (history of timekeeping)
- **Key indicators**: Personal pronouns + time/schedule words

#### STATUS vs QUERY

- **STATUS**: Personal work status (what am I working on?)
- **QUERY**: General status information (status of economy)
- **Key indicators**: Personal pronouns + work/progress words

#### PRIORITY vs QUERY

- **PRIORITY**: Personal focus/importance (what should I focus on?)
- **QUERY**: General rankings (top 10 movies)
- **Key indicators**: Personal pronouns + priority/importance words

#### IDENTITY vs QUERY

- **IDENTITY**: Personal information (who am I?, my role)
- **QUERY**: General information about people (who is the CEO?)

#### GUIDANCE vs QUERY

- **GUIDANCE**: How-to advice (how do I create a ticket?)
- **QUERY**: Factual information (what is a ticket?)

### 3. Added Confidence Scoring Guidance

Provided specific confidence thresholds:

- **High confidence (0.9-1.0)**: Personal pronouns + clear category keywords
- **Medium confidence (0.7-0.9)**: Category keywords present but ambiguous context
- **Low confidence (<0.7)**: Consider QUERY instead

### 4. Updated Category List in JSON Schema

**Before**: `"category": "execution|analysis|synthesis|strategy|learning|query|conversation|unknown"`
**After**: `"category": "identity|temporal|status|priority|guidance|execution|analysis|synthesis|strategy|learning|query|conversation|unknown"`

### 5. Added Comprehensive Examples

Added 18 new examples covering:

- **9 Canonical category examples** with high confidence scores
- **6 Workflow category examples** (existing)
- **4 Disambiguation examples** showing edge cases

---

## Rationale for Each Change

### Missing Categories Issue

The core problem was that the LLM classifier didn't know about canonical categories, so queries like "what's on my calendar?" were being classified as QUERY instead of TEMPORAL.

### Disambiguation Rules

Based on Phase 1 patterns from Code Agent, added specific rules to help the LLM distinguish between:

- Personal queries (canonical categories)
- General knowledge queries (QUERY)
- How-to questions (GUIDANCE)

### Confidence Scoring

Added guidance to help the LLM assign appropriate confidence scores, with lower confidence for ambiguous cases that might need fallback handling.

### Examples Enhancement

Provided clear positive and negative examples to train the LLM on the distinction between canonical categories and QUERY.

---

## Expected Impact on Accuracy

### Before Enhancement

- **TEMPORAL queries** → Often classified as QUERY (85-95% accuracy)
- **STATUS queries** → Often classified as QUERY (85-95% accuracy)
- **PRIORITY queries** → Often classified as QUERY (85-95% accuracy)

### After Enhancement

- **Clear disambiguation rules** should improve accuracy to 95%+
- **Personal pronoun + keyword pattern** provides strong signal
- **Confidence scoring** helps with edge cases
- **Comprehensive examples** train the LLM on correct patterns

### Key Improvement Mechanisms

1. **Category Awareness**: LLM now knows canonical categories exist
2. **Pattern Recognition**: Personal pronouns + keywords = canonical category
3. **Context Distinction**: Personal vs general knowledge queries
4. **Confidence Calibration**: Appropriate confidence for ambiguous cases

---

## Verification

### Prompt Enhancement Verification

```bash
# Verify canonical categories added
grep -n "TEMPORAL\|STATUS\|PRIORITY\|IDENTITY\|GUIDANCE" services/intent_service/prompts.py

# Count disambiguation rules added
grep -c "vs QUERY" services/intent_service/prompts.py
# Should show 5 (one for each canonical category)

# Count examples added
grep -c "✅\|❌" services/intent_service/prompts.py
# Should show positive/negative examples

# Check file modification
ls -la services/intent_service/prompts.py
```

### Expected Results

- **5 disambiguation rule sections** added
- **18 new examples** with canonical categories
- **Confidence scoring guidance** for edge cases
- **Complete category list** in JSON schema

---

## Next Steps (Phase 3)

1. **Create accuracy test suite** to measure improvement
2. **Test classification** with problematic queries from Phase 1
3. **Measure accuracy** against 95% target
4. **Iterate on prompts** if needed based on test results

---

## Files Modified

1. **`services/intent_service/prompts.py`** - Enhanced main classification prompt
2. **`dev/2025/10/07/classifier-prompt-enhancements.md`** - This documentation

**Total Lines Added**: ~80 lines of disambiguation rules and examples
**Impact**: Should significantly improve canonical category classification accuracy
