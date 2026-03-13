# Gameplan: GREAT-4A - Intent Foundation & Categories

**Date**: October 5, 2025
**Epic**: GREAT-4A (First sub-epic of GREAT-4)
**Context**: Establishing foundation for universal intent classification

## Mission

Add missing intent categories (TEMPORAL, STATUS, PRIORITY), fix pattern loading issues, and establish comprehensive test coverage with baseline metrics. This creates the foundation for universal intent classification.

## Background

Current intent classifier missing critical categories causing "Failed to process intent" errors on canonical queries. Pattern loading may have issues. Need solid foundation before enforcing universal classification.

## Phase -1: Infrastructure Verification
**Lead Developer - ALWAYS DO FIRST**

Check assumptions before proceeding:
```bash
# Verify intent service exists
ls -la services/intent_service/
ls -la services/intent/

# Check current intent categories
grep -r "IntentCategory\|IntentType" services/ --include="*.py"

# Verify pattern loading mechanism
grep -r "pattern" services/intent* --include="*.py"

# Check for existing tests
ls -la tests/intent/
ls -la tests/services/intent*/
```

If structure different than expected, STOP and report to PM.

## Phase 0: Investigation
**Both Agents - Simple task**

### Questions to Answer
1. What intent categories currently exist?
2. How are patterns loaded and matched?
3. What causes "Failed to process intent" errors?
4. What are the canonical test queries?

### Investigation Tasks
```bash
# Find current implementation
find . -name "*intent*" -type f -path "*/services/*"

# Check for shared types
cat services/shared_types.py | grep -A 20 "Intent"

# Look for pattern definitions
find . -name "*.json" -o -name "*.yaml" | xargs grep -l "intent"
```

### Document Findings
Create `dev/2025/10/05/intent-investigation.md` with:
- Current categories found
- Pattern loading mechanism
- Error sources identified
- Canonical queries list

## Phase 1: Add Intent Categories
**Code Agent - Medium complexity**

### Add to Enum
Update `services/shared_types.py` or equivalent:
```python
class IntentCategory(Enum):
    # Existing categories...
    TEMPORAL = "temporal"      # Time/date/schedule queries
    STATUS = "status"          # Current work/project status
    PRIORITY = "priority"      # Priority/focus queries
```

### Create Pattern Definitions
Add patterns for each category:
```python
TEMPORAL_PATTERNS = [
    "what day is it",
    "what's my schedule",
    "when is my next",
    "what time",
    # ... more patterns
]

STATUS_PATTERNS = [
    "what am i working on",
    "current projects",
    "show me status",
    "where are we on",
    # ... more patterns
]

PRIORITY_PATTERNS = [
    "top priority",
    "what should i focus on",
    "most important",
    "urgent tasks",
    # ... more patterns
]
```

### Pattern Requirements

Each category needs 10+ patterns minimum:

```python
TEMPORAL_PATTERNS = [
    # Time queries
    "what time is it",
    "what day is it",
    "what's the date",
    "what month are we in",
    # Schedule queries
    "what's my schedule",
    "when is my next meeting",
    "show me today's calendar",
    "what's on my agenda",
    # Relative time
    "what's happening tomorrow",
    "what did I do yesterday",
    # ... total 10+ patterns
]
```

### Update Classifier
Modify classification logic to handle new categories.

## Phase 2: Fix Pattern Loading
**Cursor Agent - Medium complexity**

### Verify Loading Mechanism
```python
# Ensure patterns load correctly
def load_patterns():
    """Load and validate all intent patterns."""
    patterns = {}

    # Load from files or constants
    # Validate each pattern set
    # Log what's loaded

    return patterns
```

### Add Logging
```python
import logging

logger = logging.getLogger(__name__)

def classify_intent(text: str):
    logger.debug(f"Classifying: {text}")
    # ... classification logic
    logger.info(f"Classified as: {intent_type}")
```

### Error Handling
Ensure graceful failures with informative messages.

## Phase 3: Create Test Suite
**Code Agent - Medium complexity**

### Canonical Query Tests
Create `tests/intent/test_canonical_queries.py`:
```python
import pytest
from services.intent_service import IntentClassifier

CANONICAL_QUERIES = [
    ("What day is it?", IntentCategory.TEMPORAL),
    ("What's my schedule today?", IntentCategory.TEMPORAL),
    ("What am I working on?", IntentCategory.STATUS),
    ("Show me current projects", IntentCategory.STATUS),
    ("What's my top priority?", IntentCategory.PRIORITY),
]

@pytest.mark.parametrize("query,expected", CANONICAL_QUERIES)
def test_canonical_classification(query, expected):
    classifier = IntentClassifier()
    result = classifier.classify(query)
    assert result.category == expected
    assert result.confidence > 0.8
```

### Pattern Coverage Tests
Test each pattern set comprehensively.

### Edge Case Tests
Test ambiguous inputs, typos, variations.

## Phase 4: Baseline Metrics
**Cursor Agent - Simple task**

### Create Benchmark Script
`scripts/benchmark_intent_baseline.py`:
```python
import time
from statistics import mean, stdev

def benchmark_classification():
    """Establish baseline metrics."""

    times = []
    accuracies = []

    for query in test_queries:
        start = time.time()
        result = classifier.classify(query)
        elapsed = time.time() - start

        times.append(elapsed)
        accuracies.append(result.confidence)

    print(f"Avg time: {mean(times)*1000:.2f}ms")
    print(f"Avg accuracy: {mean(accuracies):.2%}")
```

### Document Baselines
Create `dev/2025/10/05/intent-baseline-metrics.md`:
- Current processing times
- Classification accuracy
- Error rates
- Memory usage

Confidence Validation

```python
@pytest.mark.parametrize("query,expected", CANONICAL_QUERIES)
def test_canonical_confidence(query, expected):
    """Test confidence scores meet threshold."""
    classifier = IntentClassifier()
    result = classifier.classify(query)
    assert result.confidence > 0.8, f"Low confidence {result.confidence} for '{query}'"
```


## Phase Z: Validation
**Both Agents**


### Run All Tests
```bash
# New category tests
pytest tests/intent/test_categories.py -v

# Canonical query tests
pytest tests/intent/test_canonical_queries.py -v

# Pattern loading tests
pytest tests/intent/test_pattern_loading.py -v

# Baseline benchmarks
python scripts/benchmark_intent_baseline.py
```

### Verify No Regressions
```bash
# Existing tests still pass
pytest tests/ -k intent -v
```

### Document Results
Update `dev/2025/10/05/GREAT-4A-completion.md`

## Success Criteria

- [ ] 3 new categories added to enum
- [ ] Pattern sets defined for each category
- [ ] Pattern loading verified working
- [ ] All 5 canonical queries classify correctly
- [ ] Confidence >0.8 for canonical queries
- [ ] Baseline metrics documented
- [ ] No regressions in existing tests
- [ ] Documentation complete

## Anti-80% Tracking

During validation, check off completed items:

```
Task         | Added | Tested | Working | Documented
------------ | ----- | ------ | ------- | ----------
TEMPORAL     | [x]   | [x]    | [x]     | [ ]
STATUS       | [x]   | [x]    | [x]     | [ ]
PRIORITY     | [x]   | [x]    | [x]     | [ ]
Patterns     | [x]   | [x]    | [x]     | [ ]
Loading      | [x]   | [x]    | [x]     | [ ]
Tests        | [x]   | [x]    | [x]     | [ ]
Baselines    | [x]   | [x]    | [x]     | [ ]
```

Only propose that 4A is done all 28 checkmarks complete.

## Effort Indicators

- Phase 0: Investigation (simple)
- Phase 1: Add categories (medium)
- Phase 2: Fix loading (medium)
- Phase 3: Test suite (medium)
- Phase 4: Baselines (simple)
- Phase Z: Validation (simple)

## Critical File Placement Rules

- **NEVER** create files in root without PM permission
- Test files → `tests/intent/`
- Working files → `dev/2025/10/05/`
- Scripts → `scripts/benchmarks/`
- When uncertain → ASK where file should go

## Documentation review and update

- Thorough check of existing architecture, ADR, and pattern documentation (in docs/internal/architecture current, primarily, but agents should refer to docs/NAVIGATION.md to find all relevant documentation that may need review or updating.

## GitHub commit and push

When work is done and approved, both agents commit their work and one agent pushes it to remote, and then they both finish their session logs.

---

*Ready to establish intent classification foundation!*
