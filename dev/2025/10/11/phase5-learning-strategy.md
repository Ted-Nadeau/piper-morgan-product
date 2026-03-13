# Phase 5 Learning Strategy: Pattern Learning Algorithm
**Date**: 2025-10-11, 5:10 PM
**Approach**: Issue Similarity with Keyword Clustering
**Complexity**: Medium (no ML, uses keyword extraction)

---

## Learning Algorithm: Issue Similarity Patterns

### Overview

**Method**: Keyword-based clustering with frequency analysis
**No ML required**: Uses simple text processing and grouping
**Scalable**: Works with any number of issues
**Interpretable**: Clear why patterns were identified

### Algorithm Steps

#### Step 1: Data Fetching
```python
# Fetch historical issues from GitHub
issues = await github_service.list_issues(
    repository='piper-morgan',
    state='all',
    limit=100
)

# Filter by search query if provided
if search_query:
    issues = filter_by_keywords(issues, search_query)

# Convert to standard format
historical_data = [
    {
        'number': issue.number,
        'title': issue.title,
        'body': issue.body,
        'labels': [label.name for label in issue.labels],
        'state': issue.state
    }
    for issue in issues
]
```

#### Step 2: Keyword Extraction
```python
# Extract significant keywords from each issue title
for item in historical_data:
    title = item['title'].lower()
    words = title.split()

    # Filter stop words and short words
    stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'are'}
    keywords = [
        w for w in words
        if len(w) > 3 and w not in stop_words
    ]

    item['keywords'] = keywords
```

#### Step 3: Keyword Grouping
```python
# Group issues by shared keywords
keyword_groups = {}

for item in historical_data:
    for keyword in item['keywords']:
        if keyword not in keyword_groups:
            keyword_groups[keyword] = []
        keyword_groups[keyword].append(item)

# Example result:
# keyword_groups = {
#     'authentication': [issue1, issue2, issue3, ...],
#     'database': [issue4, issue5, ...],
#     'performance': [issue6, issue7, issue8, ...],
# }
```

#### Step 4: Pattern Identification
```python
# Filter groups by min_occurrences threshold
patterns = []

for keyword, items in keyword_groups.items():
    if len(items) >= min_occurrences:  # e.g., >= 2
        # Calculate confidence
        confidence = min(len(items) / 10, 1.0)  # Scale to 1.0

        # Extract common labels
        all_labels = []
        for item in items:
            all_labels.extend(item['labels'])

        label_counts = Counter(all_labels)
        common_labels = [
            label for label, count in label_counts.items()
            if count >= len(items) * 0.3  # In 30%+ of items
        ]

        # Create pattern
        pattern = {
            'pattern_id': f"keyword_{keyword}",
            'description': f"Issues related to '{keyword}'",
            'keyword': keyword,
            'confidence': confidence,
            'occurrences': len(items),
            'common_labels': common_labels,
            'examples': [
                {'number': item['number'], 'title': item['title']}
                for item in items[:5]  # First 5 examples
            ],
            'recommended_actions': generate_recommendations(keyword, common_labels)
        }

        patterns.append(pattern)
```

#### Step 5: Ranking and Filtering
```python
# Sort by occurrences (most common first)
patterns.sort(key=lambda x: x['occurrences'], reverse=True)

# Return top 10 patterns
return patterns[:10]
```

---

## Helper Method Specifications

### Helper 1: `_validate_learning_request` (~60 lines)

**Purpose**: Validate intent parameters before processing

**Logic**:
```python
def _validate_learning_request(self, intent: Intent) -> Optional[IntentProcessingResult]:
    # Check pattern_type
    pattern_type = intent.context.get("pattern_type")
    if not pattern_type:
        return IntentProcessingResult(
            success=False,
            message="Pattern type is required. Supported: issue_similarity, resolution_patterns, tag_patterns.",
            requires_clarification=True,
            clarification_type="pattern_type_required",
            ...
        )

    # Check source
    source = intent.context.get("source")
    if not source:
        return IntentProcessingResult(
            success=False,
            message="Source is required (e.g., github_issues).",
            requires_clarification=True,
            clarification_type="source_required",
            ...
        )

    # Validate pattern_type
    supported = ['issue_similarity', 'resolution_patterns', 'tag_patterns']
    if pattern_type not in supported:
        return IntentProcessingResult(
            success=False,
            message=f"Unsupported pattern type: {pattern_type}. Supported: {', '.join(supported)}",
            requires_clarification=True,
            clarification_type="unsupported_pattern_type",
            ...
        )

    return None  # Validation passed
```

**Returns**:
- `IntentProcessingResult` with error if validation fails
- `None` if validation passes

---

### Helper 2: `_fetch_learning_data` (~80 lines)

**Purpose**: Fetch historical data from specified source

**Logic**:
```python
async def _fetch_learning_data(self, intent: Intent) -> List[Dict[str, Any]]:
    source = intent.context.get("source")
    search_query = intent.context.get("query", "")
    timeframe = intent.context.get("timeframe", "6_months")

    if source == "github_issues":
        github_service = self.service_registry.get('github')
        if not github_service:
            self.logger.warning("GitHub service not available")
            return []

        try:
            # Fetch issues
            issues = await github_service.list_issues(
                repository='piper-morgan',
                state='all',
                limit=100
            )

            # Filter by search query
            if search_query:
                query_lower = search_query.lower()
                issues = [
                    issue for issue in issues
                    if query_lower in (issue.title or '').lower()
                    or query_lower in (issue.body or '').lower()
                ]

            # Convert to standard format
            return [
                {
                    'number': issue.number,
                    'title': issue.title,
                    'body': issue.body,
                    'labels': [label.name for label in (issue.labels or [])],
                    'state': issue.state
                }
                for issue in issues
            ]

        except Exception as e:
            self.logger.error(f"Failed to fetch GitHub issues: {e}")
            return []

    # Future: Add support for other sources
    return []
```

**Returns**: List of issue dictionaries

---

### Helper 3: `_learn_issue_similarity_patterns` (~140 lines)

**Purpose**: Core pattern learning algorithm

**Logic**: As described in Algorithm Steps above

**Input**:
- `historical_data`: List of issue dicts
- `search_query`: Optional query string
- `min_occurrences`: Minimum pattern frequency

**Returns**: List of pattern dicts

**Key Operations**:
1. Extract keywords from titles
2. Group issues by keywords
3. Filter by min_occurrences
4. Calculate confidence scores
5. Extract common labels
6. Generate recommendations
7. Sort by occurrences
8. Return top 10

---

### Helper 4: `_generate_pattern_recommendations` (~40 lines)

**Purpose**: Generate actionable recommendations for a pattern

**Logic**:
```python
def _generate_pattern_recommendations(
    self, keyword: str, common_labels: List[str], occurrences: int
) -> List[str]:
    recommendations = []

    # Always recommend reviewing similar issues
    recommendations.append(
        f"Review {occurrences} similar past issues with '{keyword}'"
    )

    # Recommend common labels if available
    if common_labels:
        recommendations.append(
            f"Consider applying labels: {', '.join(common_labels[:3])}"
        )

    # Add frequency-based recommendations
    if occurrences >= 5:
        recommendations.append(
            f"High frequency pattern ({occurrences} occurrences) - consider root cause analysis"
        )

    # Add pattern-specific recommendations
    if keyword in ['bug', 'error', 'issue', 'problem']:
        recommendations.append(
            "Investigate if a systemic fix can address multiple related issues"
        )

    return recommendations
```

---

### Helper 5: `_format_learning_response` (~30 lines)

**Purpose**: Format human-readable message

**Logic**:
```python
def _format_learning_response(
    self, patterns: List[Dict[str, Any]], total_analyzed: int
) -> str:
    if not patterns:
        return f"Analyzed {total_analyzed} items but found no recurring patterns."

    # Create preview of top 3 patterns
    preview = []
    for i, pattern in enumerate(patterns[:3], 1):
        preview.append(
            f"{i}. {pattern['description']} ({pattern['occurrences']} occurrences, "
            f"confidence: {pattern['confidence']:.2f})"
        )

    preview_text = "\n".join(preview)

    return (
        f"Learned {len(patterns)} patterns from {total_analyzed} items:\n\n"
        f"{preview_text}\n\n"
        f"See intent_data.patterns_found for complete details."
    )
```

---

## Example Input/Output

### Example 1: Basic Issue Similarity

**Input**:
```python
Intent(
    category=IntentCategory.LEARNING,
    action="learn_pattern",
    context={
        "pattern_type": "issue_similarity",
        "source": "github_issues",
        "query": "authentication",
        "min_occurrences": 2
    }
)
```

**Output**:
```python
IntentProcessingResult(
    success=True,
    message="Learned 2 patterns from 15 items:\n\n1. Issues related to 'authentication' (8 occurrences, confidence: 0.80)\n2. Issues related to 'timeout' (3 occurrences, confidence: 0.30)",
    intent_data={
        "category": "learning",
        "action": "learn_pattern",
        "pattern_type": "issue_similarity",
        "total_items_analyzed": 15,
        "patterns_count": 2,
        "patterns_found": [
            {
                "pattern_id": "keyword_authentication",
                "description": "Issues related to 'authentication'",
                "keyword": "authentication",
                "confidence": 0.80,
                "occurrences": 8,
                "common_labels": ["bug", "security"],
                "examples": [
                    {"number": 123, "title": "Auth token expires too quickly"},
                    {"number": 145, "title": "Authentication fails after logout"}
                ],
                "recommended_actions": [
                    "Review 8 similar past issues with 'authentication'",
                    "Consider applying labels: bug, security"
                ]
            },
            {
                "pattern_id": "keyword_timeout",
                "description": "Issues related to 'timeout'",
                "keyword": "timeout",
                "confidence": 0.30,
                "occurrences": 3,
                "common_labels": ["bug"],
                "examples": [
                    {"number": 150, "title": "Request timeout in API calls"}
                ],
                "recommended_actions": [
                    "Review 3 similar past issues with 'timeout'"
                ]
            }
        ]
    }
)
```

### Example 2: No Patterns Found

**Input**:
```python
Intent(
    context={
        "pattern_type": "issue_similarity",
        "source": "github_issues",
        "query": "quantum_entanglement"
    }
)
```

**Output**:
```python
IntentProcessingResult(
    success=True,
    message="Analyzed 0 items but found no recurring patterns.",
    intent_data={
        "pattern_type": "issue_similarity",
        "total_items_analyzed": 0,
        "patterns_count": 0,
        "patterns_found": []
    }
)
```

---

## Test Strategy

### Test 1: Handler Not Placeholder
```python
async def test_learn_pattern_handler_not_placeholder(intent_service):
    result = await intent_service._handle_learn_pattern(intent, "wf-1")

    # Should NOT have requires_clarification=True
    assert result.requires_clarification is not True
```

### Test 2-4: Validation Tests
- Missing pattern_type
- Missing source
- Unknown pattern_type

### Test 5-7: Success Tests
- Issue similarity with results
- Patterns have proper structure
- No placeholder messages

---

## Implementation Complexity

**Estimated Lines**:
- Main handler: ~130 lines
- Helper 1 (validate): ~60 lines
- Helper 2 (fetch): ~80 lines
- Helper 3 (learn): ~140 lines
- Helper 4 (recommendations): ~40 lines
- Helper 5 (format): ~30 lines
- **Total**: ~480 lines

**Estimated Time**: 40-50 minutes

**Difficulty**: Medium
- No ML/NLP libraries needed
- Uses simple text processing
- Leverages existing GitHub service
- Clear algorithm steps

---

## Success Criteria

✅ Genuine learning from historical data
✅ Keyword-based clustering works
✅ Confidence scores calculated correctly
✅ Common labels extracted meaningfully
✅ Recommendations are actionable
✅ Handles edge cases gracefully
✅ No placeholder responses
✅ Modern pattern compliance

---

**Strategy Complete**: Ready for Part 3 (Tests)
**Next**: Write TDD tests to drive implementation
**Goal**: 100% GAP-1 completion! 🎯
