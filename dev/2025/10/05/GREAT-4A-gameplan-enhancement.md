# GREAT-4A Gameplan Enhancement

## Add to Phase 1: Pattern Requirements

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

## Add to Phase 3: Confidence Validation

```python
@pytest.mark.parametrize("query,expected", CANONICAL_QUERIES)
def test_canonical_confidence(query, expected):
    """Test confidence scores meet threshold."""
    classifier = IntentClassifier()
    result = classifier.classify(query)
    assert result.confidence > 0.8, f"Low confidence {result.confidence} for '{query}'"
```

## Add to Phase Z: Anti-80% Tracking

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

Only proceed to GREAT-4B when all 28 checkmarks complete.
