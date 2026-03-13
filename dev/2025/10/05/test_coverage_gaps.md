# Test Coverage Gaps Report - GREAT-4A Phase 1

**Date**: October 5, 2025
**Test Run**: 25 canonical queries
**Pass Rate**: 24% (6/25 passed)
**Evidence**: `test_canonical_queries.py` execution

## Executive Summary

The intent classification system has **TEMPORAL**, **STATUS**, and **PRIORITY** categories defined in the enum, but the pre_classifier patterns are incomplete. Only 24% of canonical queries classify correctly. The issue is NOT missing categories - it's **missing pattern definitions**.

## Current Test Coverage (pytest --cov)

**Overall Intent Service Coverage: 29%** (960 statements, 679 missing)

### File-by-File Coverage:
- ✅ `__init__.py`: 100% (4/4 statements)
- ✅ `fuzzy_matcher.py`: 100% (10/10 statements)
- ✅ `prompts.py`: 100% (2/2 statements)
- ⚠️ `pre_classifier.py`: 79% (75 statements, 16 missing)
- ⚠️ `classifier.py`: 69% (241 statements, 74 missing)
- ⚠️ `intent_enricher.py`: 67% (58 statements, 19 missing)
- ❌ `canonical_handlers.py`: 0% (166 statements, 166 missing) **CRITICAL GAP**
- ❌ `llm_classifier.py`: 0% (301 statements, 301 missing)
- ❌ `llm_classifier_factory.py`: 0% (30 statements, 30 missing)
- ❌ `spatial_intent_classifier.py`: 0% (71 statements, 71 missing)
- ❌ `exceptions.py`: 0% (2 statements, 2 missing)

### Critical Findings:
1. **canonical_handlers.py has ZERO coverage** despite being critical for TEMPORAL/STATUS/PRIORITY responses
2. **27 existing tests** focus on search patterns, not canonical query categories
3. **Pre-classifier at 79%** but missing the new category pattern checks (lines 158-162, 171, 180, 189, 197, 205, 213, 221)

## Current Pattern Coverage

Analysis of `services/intent_service/pre_classifier.py`:

### TEMPORAL Patterns (Lines 54-62)
**Current**: 7 patterns
**Coverage**: 33% (4/12 queries passing)

✅ **Working patterns:**
- `\bwhat day is it\b` → "What day is it?" ✅
- `\bwhat'?s the date\b` → "What's today's date?" ✅
- `\bcurrent date\b` → "What's the current date?" ✅
- `\btoday'?s date\b` → (matches some variations) ✅

❌ **Missing patterns:**
- "What day of the week is it?" → Falls through to LLM → QUERY ❌
- "Tell me the date" → Falls through to LLM → QUERY ❌
- "What did we accomplish yesterday?" → Falls through to LLM → QUERY ❌
- "What did we do yesterday?" → Falls through to LLM → QUERY ❌
- "What happened yesterday?" → Falls through to LLM → QUERY ❌
- "What's on the agenda for today?" → Falls through to LLM → QUERY ❌
- "What should I work on today?" → Falls through to LLM → STRATEGY ❌
- "When was the last time we worked on this?" → Falls through to LLM → QUERY ❌
- "How long have we been working on this project?" → Falls through to LLM → QUERY ❌

### STATUS Patterns (Lines 64-73)
**Current**: 8 patterns
**Coverage**: 14% (1/7 queries passing)

✅ **Working patterns:**
- `\bmy projects\b` → "List all my projects" ✅

❌ **Missing patterns:**
- "Show me current projects" → Falls through to LLM → QUERY ❌
- "What projects are we working on?" → Falls through to LLM → QUERY ❌
- "Give me a project overview" → Falls through to LLM → QUERY ❌
- "What's the status of project X?" → Falls through to LLM → QUERY ❌
- "What am I working on?" → Should match `\bwhat am i working on\b` but doesn't ❓
- "Show me the project landscape" → Falls through to LLM → QUERY ❌

### PRIORITY Patterns (Lines 75-83)
**Current**: 7 patterns
**Coverage**: 17% (1/6 queries passing)

✅ **Working patterns:**
- `\bwhat'?s my top priority\b` → "What's my top priority?" ✅

❌ **Missing patterns:**
- "What should I focus on today?" → Matches GUIDANCE instead (line 86) ❌
- "What's most important today?" → Falls through to LLM → QUERY ❌
- "What needs my attention?" → Falls through to LLM → QUERY ❌
- "Which project should I focus on?" → Matches GUIDANCE instead (line 86) ❌
- "What patterns do you see?" → Falls through to LLM → ANALYSIS ❌

### GUIDANCE Pattern Conflict (Lines 85-95)
**Issue**: GUIDANCE patterns are capturing queries that should be PRIORITY

Conflicting pattern:
- `\bwhat should i focus on\b` (line 86) → Captures PRIORITY queries
- `\bshould i focus\b` (line 94) → Captures PRIORITY queries

## Untested Functions

From test execution logs, these functions are being called but not directly tested:

### services/intent_service/pre_classifier.py
- `PreClassifier._matches_patterns()` (line 286-291) - Called indirectly ✅
- `PreClassifier.detect_file_reference()` (line 231-245) - Not tested in canonical queries ❌
- `PreClassifier.get_file_reference_confidence()` (line 248-283) - Not tested ❌

### services/intent_service/classifier.py
- LLM fallback is being used for 19/25 queries (76%) - Expected to be rare
- Pre-classifier should handle majority of canonical queries

## Missing Test Cases

To reach >80% coverage and improve classification accuracy, need:

### TEMPORAL Category
- [ ] "day of the week" pattern
- [ ] "tell me the" temporal patterns
- [ ] "yesterday" patterns (accomplish, do, happened)
- [ ] "agenda for" patterns
- [ ] "last time" patterns
- [ ] "how long" duration patterns

### STATUS Category
- [ ] "show me" project patterns
- [ ] "current projects" pattern
- [ ] "project overview" pattern
- [ ] "project landscape" pattern
- [ ] Fix "what am i working on" pattern (not matching despite existing)

### PRIORITY Category
- [ ] "most important" pattern
- [ ] "needs my attention" pattern
- [ ] "which project" focus patterns
- [ ] "what patterns" analysis patterns
- [ ] **CRITICAL**: Move focus patterns from GUIDANCE to PRIORITY

### Edge Cases
- [ ] Pattern ordering (GUIDANCE checked before PRIORITY - conflict!)
- [ ] Case sensitivity handling
- [ ] Punctuation handling (working correctly)
- [ ] Apostrophe variations (already handled with `'?`)

## Recommendations

### Immediate (Phase 3 - Add Missing Patterns)
1. **Add 9 TEMPORAL patterns** for yesterday, agenda, duration queries
2. **Add 4 STATUS patterns** for show/overview/landscape queries
3. **Add 4 PRIORITY patterns** for importance/attention queries
4. **Move focus patterns from GUIDANCE to PRIORITY** (lines 86, 94)
5. **Fix pattern ordering** - check PRIORITY before GUIDANCE

### Testing (Phase 3)
1. Add test cases for each new pattern
2. Verify no regression in existing patterns
3. Test pattern ordering conflicts
4. Measure new pass rate (target: >80%)

### Validation
1. Re-run `test_canonical_queries.py` after pattern additions
2. Expect pass rate improvement from 24% → 80%+
3. Verify confidence scores remain >0.8
4. Document pattern→query mappings

## Coverage Metrics

### Current State
- **Pre-classifier coverage**: ~24% of canonical queries
- **LLM fallback usage**: 76% (too high - should be <20%)
- **Pattern completeness**:
  - TEMPORAL: 33%
  - STATUS: 14%
  - PRIORITY: 17%

### Target State (After Phase 3)
- **Pre-classifier coverage**: >80% of canonical queries
- **LLM fallback usage**: <20%
- **Pattern completeness**:
  - TEMPORAL: 90%+
  - STATUS: 90%+
  - PRIORITY: 90%+

## Evidence Links

- Test script: `dev/2025/10/05/test_canonical_queries.py`
- Test execution: Timestamped 1:46 PM - 1:47 PM
- Pre-classifier code: `services/intent_service/pre_classifier.py:54-95`
- Shared types: `services/shared_types.py:18-20` (categories exist)

## Next Steps

1. ✅ Test coverage gaps identified (this document)
2. ⏭️ Coordinate with Cursor for Phase 2 baseline metrics
3. ⏭️ Phase 3: Add missing patterns to pre_classifier.py
4. ⏭️ Re-test to validate 80%+ pass rate
5. ⏭️ Update GitHub issue #205 with findings

---

## Phase 3 Pattern Additions (October 5, 2025, 1:56-2:00 PM)

### Patterns Added

**TEMPORAL Category**:
- Added 10 new patterns (7 → 17 total):
  - `\bday of the week\b` - "What day of the week is it?"
  - `\btell me the date\b` - "Tell me the date"
  - `\bwhat.*yesterday\b` - "What did we do yesterday?"
  - `\bdid.*yesterday\b` - "What did we accomplish yesterday?"
  - `\bhappened yesterday\b` - "What happened yesterday?"
  - `\bagenda.*today\b` - "What's on the agenda for today?"
  - `\bwork on today\b` - "What should I work on today?"
  - `\blast time.*worked\b` - "When was the last time we worked on this?"
  - `\bhow long.*working\b` - "How long have we been working?"
  - `\bhow long.*been working\b` - Duration queries

**STATUS Category**:
- Added 6 new patterns (8 → 14 total):
  - `\bshow.*projects\b` - "Show me current projects"
  - `\bcurrent projects\b` - "Current projects"
  - `\bproject overview\b` - "Give me a project overview"
  - `\bproject landscape\b` - "Show me the project landscape"
  - `\blist.*projects\b` - "List all my projects"
  - `\bprojects.*working on\b` - "What projects are we working on?"

**PRIORITY Category**:
- Added 6 new patterns (7 → 13 total):
  - `\bmost important\b` - "What's most important today?"
  - `\bneeds.*attention\b` - "What needs my attention?"
  - `\bwhich project.*focus\b` - "Which project should I focus on?"
  - `\bwhat should i focus on\b` - Moved from GUIDANCE
  - `\bshould i focus\b` - Moved from GUIDANCE
  - `\bwhat.*focus on\b` - General focus patterns

### Test Results After Changes

**Before Phase 3**:
- Total: 25 queries
- Passed: 6 (24%)
- Failed: 19 (76%)

**After Phase 3**:
- Total: 25 queries
- Passed: 23 (92%)
- Failed: 2 (8%)
- **Improvement: +68 percentage points** ✅

### Remaining Gaps (2 queries)

1. **"What's the status of project X?"** → LLM → QUERY
   - Needs pattern: `\bstatus of.*project\b`
   - Note: LLM correctly identifies this as project status query (confidence 0.85)
   - May be acceptable to use LLM for project-specific queries

2. **"What patterns do you see?"** → LLM → ANALYSIS
   - Currently classifies as ANALYSIS (confidence 0.7)
   - This is arguably correct - pattern analysis is analytical, not priority
   - May need category re-evaluation rather than pattern fix

### Pattern Conflicts Resolved

**GUIDANCE/PRIORITY Conflict** ✅:
- **Issue**: `\bwhat should i focus on\b` was in GUIDANCE (line 86)
- **Issue**: `\bshould i focus\b` was in GUIDANCE (line 94)
- **Solution**: Moved both patterns to PRIORITY
- **Removed from GUIDANCE**: Focus-related patterns
- **Result**: "What should I focus on today?" now correctly → PRIORITY

**Verification**: PRIORITY checked before GUIDANCE in pre_classify() (lines 236, 244)

### Coverage Improvement

**File**: `services/intent_service/pre_classifier.py`
- **Before**: 79% coverage (75 statements, 16 missing)
- **After**: Expected increase due to pattern usage
- **New patterns**: 22 total additions across 3 categories

### Success Metrics

- ✅ **22 patterns added** (exceeded 17+ requirement)
- ✅ **92% pass rate** (exceeded 80% target)
- ✅ **No pattern conflicts** (GUIDANCE/PRIORITY resolved)
- ✅ **Backup created** (pre_classifier.py.backup)
- ✅ **Test evidence** (test_patterns.py output)

---

**Conclusion**: Pattern additions successful. 92% of canonical queries now classify correctly via pre_classifier, with only 2 edge cases falling through to LLM. The issue was incomplete pattern definitions - now resolved.
