# Prompt for Claude Code: GREAT-4A Phase 3 - Add Missing Patterns

## Your Identity
You are Claude Code, continuing Phase 3 work on GREAT-4A after completing Phase 1 validation testing.

## Context from Phase 1

You discovered that 76% of canonical queries (19/25) fall through to LLM fallback because pattern definitions are incomplete in `pre_classifier.py`. Only 6 queries have matching patterns.

**Your Phase 1 findings:**
- TEMPORAL: 33% success (2/6 queries match)
- STATUS: 14% success (1/7 queries match)
- PRIORITY: 17% success (1/6 queries match)
- Total: 24% success (6/25 queries match)

**Gap analysis location**: `dev/2025/10/05/test_coverage_gaps.md`

## Session Log Management

Continue your existing session log: `dev/2025/10/05/2025-10-05-1342-prog-code-log.md`

Update with Phase 3 timestamped entries.

## Mission

**Add the 17+ missing patterns to pre_classifier.py** to achieve >80% pass rate on canonical queries, ensuring intent classification works without falling back to LLM.

---

## Phase 3: Add Missing Patterns

### Step 1: Review Your Gap Analysis

Read your own gap analysis to understand exactly which patterns are missing:

```bash
cat dev/2025/10/05/test_coverage_gaps.md
```

Confirm you have clear understanding of:
- Which specific queries failed
- What patterns they need
- Any pattern conflicts (e.g., PRIORITY vs GUIDANCE)

### Step 2: Add TEMPORAL Patterns

File: `services/intent_service/pre_classifier.py`

Location: Around line 54-67 (existing TEMPORAL_PATTERNS list)

**Current patterns** (from your Phase 1):
```python
TEMPORAL_PATTERNS = [
    r"\bwhat day is it\b",
    r"\bwhat'?s the date\b",
    # ... existing patterns
]
```

**Add missing patterns for these failed queries:**
- "What day of the week is it?" → Need day-of-week pattern
- "What did we accomplish yesterday?" → Need "yesterday" pattern
- "What did we do yesterday?" → Need "did yesterday" pattern
- "What happened yesterday?" → Need "happened yesterday" pattern
- "What's on the agenda for today?" → Need "agenda" pattern
- "What should I work on today?" → Need "work on today" pattern
- "When was the last time we worked on this?" → Need "when was last" pattern
- "How long have we been working on this project?" → Need "how long" pattern

**Suggested additions:**
```python
TEMPORAL_PATTERNS = [
    r"\bwhat day is it\b",
    r"\bwhat'?s the date\b",
    r"\bwhat day of the week\b",  # NEW
    r"\bwhat did .* yesterday\b",  # NEW - generic yesterday
    r"\bwhat happened yesterday\b",  # NEW
    r"\byesterday'?s? \w+\b",  # NEW - yesterday's X
    r"\bagenda .* today\b",  # NEW
    r"\bwork on today\b",  # NEW
    r"\bschedule .* today\b",  # NEW
    r"\bwhen .* last\b",  # NEW - when was last
    r"\bhow long .* working\b",  # NEW - duration
    r"\bhow long .* project\b",  # NEW - project duration
]
```

### Step 3: Add STATUS Patterns

Location: Around line 71-83 (existing STATUS_PATTERNS list)

**Add missing patterns for these failed queries:**
- "Show me current projects" → Need "show me" pattern
- "What projects are we working on?" → Need "projects working" pattern
- "Give me a project overview" → Need "overview" pattern
- "Show me all projects" → Need "show all" pattern
- "List our projects" → Need "list projects" pattern
- "What's the project status?" → Need "project status" pattern

**Suggested additions:**
```python
STATUS_PATTERNS = [
    r"\bwhat am i working on\b",
    r"\bwhat'?s my current project\b",
    r"\bshow me .* project\b",  # NEW - show me projects
    r"\blist .* project\b",  # NEW - list projects
    r"\bgive me .* overview\b",  # NEW - overview
    r"\bproject overview\b",  # NEW
    r"\bworking on .* project\b",  # NEW - what projects working on
    r"\bproject status\b",  # NEW
    r"\bstatus of .* project\b",  # NEW
    r"\bshow .* status\b",  # NEW
    r"\blandscape\b",  # NEW - project landscape
]
```

### Step 4: Add PRIORITY Patterns

Location: Around line 87-95 (existing PRIORITY_PATTERNS list)

**Add missing patterns for these failed queries:**
- "What's most important today?" → Need "most important" pattern
- "What needs my attention?" → Need "needs attention" pattern
- "Which project should I focus on?" → Need "which project focus" pattern
- Handle conflict: "What should I focus on today?" captured by GUIDANCE

**Suggested additions:**
```python
PRIORITY_PATTERNS = [
    r"\bwhat'?s my top priority\b",
    r"\bhighest priority\b",
    r"\bmost important\b",  # NEW
    r"\bneeds? (?:my )?attention\b",  # NEW - needs attention
    r"\bwhich .* focus\b",  # NEW - which should I focus on
    r"\bwhat .* priority\b",  # NEW - what's priority
    r"\btop task\b",  # NEW
    r"\bmost urgent\b",  # NEW
]
```

**Critical**: Check GUIDANCE_PATTERNS for conflicts. If "focus on today" is in GUIDANCE, you may need to:
- Add negative lookahead: `r"\bfocus on(?! today)\b"` in GUIDANCE
- Or move specific "focus on today" to PRIORITY

### Step 5: Test Changes Immediately

After adding patterns, run your test script again:

```bash
python3 dev/2025/10/05/test_canonical_queries.py
```

**Expected outcome**: Pass rate should increase from 24% to >80%

**Validation**: Check that added patterns match intended queries

**Evidence**: Terminal output showing improved pass rate

### Step 6: Handle Edge Cases

Check for:

1. **Pattern Conflicts**
   - Does any new pattern overlap with existing categories?
   - Test ambiguous queries: "What should I focus on today?"
   - Ensure most specific pattern wins

2. **Pattern Specificity**
   - Are patterns too broad (matching unintended queries)?
   - Are patterns too narrow (missing variations)?
   - Use `.*` and `\w+` appropriately for flexibility

3. **Case Sensitivity**
   - Confirm all patterns work case-insensitive
   - Pre-classifier lowercases input before matching

### Step 7: Re-run Coverage Analysis

```bash
pytest tests/services/test_intent*.py --cov=services.intent_service --cov-report=term-missing
```

**Expected**: Pre-classifier coverage should increase from 79%

**Document**: Note any improvement in coverage percentage

### Step 8: Update Gap Analysis

Edit your gap analysis document: `dev/2025/10/05/test_coverage_gaps.md`

Add section:

```markdown
## Phase 3 Pattern Additions

### Patterns Added
- TEMPORAL: +8 patterns (now XX total)
- STATUS: +7 patterns (now XX total)
- PRIORITY: +5 patterns (now XX total)

### Test Results After Changes
- Total: 25 queries
- Passed: XX (XX%)
- Failed: XX (XX%)
- Improvement: +XX percentage points

### Remaining Gaps
[List any queries still failing]

### Pattern Conflicts Resolved
[Document any conflicts found and how resolved]
```

---

## Success Criteria

- [ ] 17+ new patterns added to pre_classifier.py
- [ ] Test pass rate >80% (20+ of 25 queries)
- [ ] No pattern conflicts introduced
- [ ] Coverage improved from 79%
- [ ] Gap analysis updated with results
- [ ] GitHub issue #205 updated
- [ ] Evidence provided (test output)

---

## Critical Implementation Notes

### Pattern Syntax Rules

1. **Word boundaries**: Use `\b` to match whole words
   - Good: `r"\bwhat day\b"` matches "what day is it"
   - Bad: `r"what day"` matches "somewhat daylight"

2. **Optional characters**: Use `?` for optional chars
   - `r"\bwhat'?s\b"` matches both "what's" and "whats"

3. **Wildcards**: Use `.*` to match anything
   - `r"\bshow .* project\b"` matches "show me current projects"

4. **Word characters**: Use `\w+` to match word sequences
   - `r"\byesterday'?s? \w+\b"` matches "yesterday's work"

5. **Grouping**: Use `(?:...)` for non-capturing groups
   - `r"\bneeds? (?:my )?attention\b"` matches "needs attention" or "needs my attention"

### Testing Individual Patterns

Before adding to file, test patterns:

```python
import re

pattern = r"\bwhat day of the week\b"
test_strings = [
    "what day of the week is it",
    "what day is it",  # Should NOT match
    "What Day Of The Week?",  # Test case insensitive
]

for test in test_strings:
    match = re.search(pattern, test, re.IGNORECASE)
    print(f"{test:40} | {'MATCH' if match else 'NO MATCH'}")
```

### File Editing Safety

1. **Backup first**:
   ```bash
   cp services/intent_service/pre_classifier.py services/intent_service/pre_classifier.py.backup
   ```

2. **Edit carefully**: Maintain existing code structure

3. **Verify syntax**: Python should still import cleanly
   ```bash
   python3 -c "from services.intent_service import pre_classifier; print('OK')"
   ```

4. **Git commit**:
   ```bash
   git add services/intent_service/pre_classifier.py
   git commit -m "Add missing intent patterns for TEMPORAL, STATUS, PRIORITY categories"
   git log --oneline -1  # Show commit
   ```

---

## Deliverables

1. **Modified File**: `services/intent_service/pre_classifier.py` with new patterns
2. **Test Results**: Updated test output showing >80% pass rate
3. **Updated Gap Analysis**: `test_coverage_gaps.md` with Phase 3 section
4. **Git Commit**: Evidence of committed changes
5. **GitHub Update**: Issue #205 with Phase 3 completion
6. **Coverage Report**: Updated pytest-cov output

---

## Cross-Validation Preparation

After Phase 3 completion:

1. **Notify Cursor**: Phase 3 complete, patterns added
2. **Cursor re-runs Phase 2**: Verify metrics with new patterns
3. **Cursor checks Phase 4**: Documentation may need pattern count updates

Leave evidence:
- Which patterns were added
- Test results before/after
- Any conflicts encountered and resolved
- Recommendations for Cursor's validation

---

## STOP Conditions

Stop and escalate if:
- [ ] Pattern additions break existing tests
- [ ] Cannot achieve >80% pass rate (fundamental issue)
- [ ] Pattern conflicts cannot be resolved
- [ ] File syntax errors after editing
- [ ] Uncertain about pattern precedence
- [ ] Need to modify handlers (out of scope)

---

## Evidence Format

```bash
# Show backup created
$ ls -la services/intent_service/pre_classifier.py*
-rw-r--r-- pre_classifier.py (modified)
-rw-r--r-- pre_classifier.py.backup (original)

# Show test results improved
$ python3 dev/2025/10/05/test_canonical_queries.py
✅ PASS | What day is it? | TEMPORAL | 1.00
✅ PASS | What day of the week is it? | TEMPORAL | 1.00  # NEW
✅ PASS | What did we do yesterday? | TEMPORAL | 1.00    # NEW
...
================================
CANONICAL QUERY TEST RESULTS
================================
Total:  25
Passed: 22 (88.0%)  ← IMPROVED from 24%
Failed: 3 (12.0%)

# Show patterns added
$ git diff services/intent_service/pre_classifier.py | head -30
+ r"\bwhat day of the week\b",
+ r"\bwhat did .* yesterday\b",
+ r"\bagenda .* today\b",
...

# Show commit
$ git log --oneline -1
abc1234 Add missing intent patterns for TEMPORAL, STATUS, PRIORITY categories
```

---

**Remember**: You are COMPLETING existing functionality by filling pattern gaps. The categories and handlers already work - they just need comprehensive pattern coverage.

---

*Template Version: 9.0*
*Task: Pattern Addition for GREAT-4A Phase 3*
*Estimated Effort: Medium (2-3 hours)*
