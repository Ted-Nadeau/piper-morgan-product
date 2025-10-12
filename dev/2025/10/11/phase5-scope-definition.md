# Phase 5 Scope Definition: LEARNING Handler
**Date**: 2025-10-11, 5:05 PM
**Handler**: `_handle_learn_pattern`
**Category**: LEARNING (1/1 handler - FINAL HANDLER!)
**Pattern**: Modern Intent/IntentProcessingResult

---

## Executive Summary

The `_handle_learn_pattern` handler implements genuine pattern learning from historical data. This is the **FINAL handler** needed to achieve 100% GAP-1 completion (10/10 handlers).

**Approach**: Issue pattern learning with similarity detection and clustering
**Implementation**: ~500-600 lines across main handler + helpers
**Tests**: 7-8 comprehensive tests
**External Dependencies**: GitHub service (already available)

---

## LEARNING vs Other Categories

### EXECUTION (complete) - Acts now
- Creates/updates resources immediately
- Example: Create issue, update status

### ANALYSIS (complete) - Understands past/present
- Reads and analyzes existing data
- Example: Analyze commits, generate report

### SYNTHESIS (complete) - Creates content
- Generates new documents/summaries
- Example: Write content, summarize text

### STRATEGY (complete) - Plans future
- Creates roadmaps and prioritizes
- Example: Sprint planning, prioritization

### LEARNING (final) - Learns from patterns
- **Identifies recurring patterns** across time
- **Learns from historical data** to improve
- **Recognizes similarities** for better decisions
- **Adapts over time** based on experience

**Key Distinction**: LEARNING looks across time to identify patterns that inform future decisions

---

## Pattern Learning Types (Choose 2-3)

### Type 1: Issue Similarity Patterns (PRIMARY - RECOMMENDED)

**Purpose**: Find similar past issues and identify common patterns

**Input Parameters**:
```python
{
  "pattern_type": "issue_similarity",
  "source": "github_issues",
  "query": "authentication",  # optional search query
  "timeframe": "6_months",    # optional, default 6_months
  "min_occurrences": 2        # optional, default 2
}
```

**Learning Method**:
1. Fetch historical issues from GitHub
2. Filter by query keywords (if provided)
3. Extract keywords from titles/descriptions
4. Group issues by keyword similarity
5. Identify patterns with min_occurrences threshold
6. Calculate confidence scores
7. Extract common labels/themes
8. Generate recommendations

**Output Structure**:
```python
{
  "pattern_id": "auth_timeout_pattern",
  "description": "Authentication timeout issues",
  "keyword": "authentication",
  "confidence": 0.85,
  "occurrences": 12,
  "common_labels": ["bug", "authentication", "high-priority"],
  "examples": [
    {"number": 123, "title": "User logged out unexpectedly"},
    {"number": 145, "title": "Session timeout too short"}
  ],
  "recommended_actions": [
    "Review similar past issues with 'authentication'",
    "Consider common labels: bug, authentication"
  ]
}
```

**Formula**:
- **Confidence**: `min(occurrences / 10, 1.0)` (scales to 1.0)
- **Pattern threshold**: `occurrences >= min_occurrences`
- **Common labels**: Labels appearing in 30%+ of grouped items

### Type 2: Resolution Patterns (SECONDARY - Optional)

**Purpose**: Learn solution approaches from resolved issues

**Input**:
```python
{
  "pattern_type": "resolution_patterns",
  "source": "github_issues",
  "query": "database error"
}
```

**Method**: Map problem types to solution approaches from closed issues

### Type 3: Tag Patterns (TERTIARY - Optional)

**Purpose**: Learn classification patterns for auto-tagging

**Input**:
```python
{
  "pattern_type": "tag_patterns",
  "source": "github_issues"
}
```

**Method**: Analyze label co-occurrence to suggest tags

---

## Modern Pattern Compliance

### Handler Signature ✅
```python
async def _handle_learn_pattern(
    self, intent: Intent, workflow_id: str
) -> IntentProcessingResult:
```

### Four-Phase Flow ✅
1. **Validate**: Check required params (pattern_type, source)
2. **Fetch**: Get historical data from source
3. **Learn**: Apply learning algorithm based on pattern_type
4. **Format**: Structure results and recommendations

### Validation Requirements ✅
- pattern_type required
- source required
- pattern_type must be supported
- Return clear error messages with clarification_type

---

## Implementation Plan

### Main Handler (~130-150 lines)
```python
async def _handle_learn_pattern(self, intent: Intent, workflow_id: str) -> IntentProcessingResult:
    # Phase 1: Validate
    validation_result = self._validate_learning_request(intent)
    if validation_result:
        return validation_result

    # Phase 2: Fetch historical data
    historical_data = await self._fetch_learning_data(intent)

    if not historical_data:
        return IntentProcessingResult(
            success=True,
            message="No historical data available for pattern learning",
            intent_data={...},
            workflow_id=workflow_id
        )

    # Phase 3: Learn patterns
    pattern_type = intent.context.get("pattern_type")

    if pattern_type == "issue_similarity":
        patterns = self._learn_issue_similarity_patterns(...)
    elif pattern_type == "resolution_patterns":
        patterns = self._learn_resolution_patterns(...)
    elif pattern_type == "tag_patterns":
        patterns = self._learn_tag_patterns(...)

    # Phase 4: Format and return
    return IntentProcessingResult(
        success=True,
        message=f"Learned {len(patterns)} patterns from {len(historical_data)} items",
        intent_data={
            "pattern_type": pattern_type,
            "patterns_found": patterns,
            "total_items_analyzed": len(historical_data),
            "patterns_count": len(patterns)
        },
        workflow_id=workflow_id
    )
```

### Helper Methods (~350-450 lines)

1. **`_validate_learning_request`** (~60 lines)
   - Check pattern_type present
   - Check source present
   - Validate pattern_type is supported
   - Return validation errors

2. **`_fetch_learning_data`** (~80 lines)
   - Fetch from GitHub service
   - Filter by query if provided
   - Apply timeframe filtering
   - Return structured data list

3. **`_learn_issue_similarity_patterns`** (~120 lines)
   - Extract keywords from titles
   - Group issues by keyword similarity
   - Filter by min_occurrences
   - Calculate confidence scores
   - Extract common labels
   - Generate recommendations
   - Return top 10 patterns

4. **`_learn_resolution_patterns`** (~80 lines)
   - Analyze closed issues
   - Extract resolution approaches
   - Group by problem type
   - Return solution patterns

5. **`_learn_tag_patterns`** (~60 lines)
   - Analyze label co-occurrence
   - Find common tag combinations
   - Return tagging patterns

---

## Test Strategy (7-8 tests)

### Validation Tests (4 tests)
1. Handler exists (not placeholder)
2. Missing pattern_type validation
3. Missing source validation
4. Unknown pattern_type error

### Success Tests (3-4 tests)
5. Issue similarity learning success
6. Patterns include examples
7. No placeholder response (requires_clarification=False)
8. (Optional) Multiple pattern types work

**Key Verification**:
- No `requires_clarification=True` responses
- Patterns have structure (pattern_id, confidence, examples)
- Actual learning from data (not hardcoded responses)

---

## Output Structure

```python
IntentProcessingResult(
    success=True,
    message="Learned 3 patterns from 42 issues:\n\n1. Authentication patterns (12 occurrences)\n2. Database error patterns (8 occurrences)\n3. Performance issues patterns (6 occurrences)\n\nSee intent_data.patterns_found for details.",
    intent_data={
        "category": "learning",
        "action": "learn_pattern",
        "pattern_type": "issue_similarity",
        "total_items_analyzed": 42,
        "patterns_count": 3,
        "patterns_found": [
            {
                "pattern_id": "auth_timeout_pattern",
                "description": "Authentication timeout issues",
                "keyword": "authentication",
                "confidence": 0.85,
                "occurrences": 12,
                "common_labels": ["bug", "authentication"],
                "examples": [
                    {"number": 123, "title": "User logged out"},
                    {"number": 145, "title": "Session timeout"}
                ],
                "recommended_actions": [
                    "Review similar issues with 'authentication'",
                    "Check session configuration"
                ]
            },
            # ... more patterns
        ]
    },
    workflow_id="wf-123"
)
```

---

## GitHub Service Integration

**Existing Service**: `services/integrations/github/github_integration_service.py`

**Available Methods**:
- `list_issues()` - Fetch issues
- Issue filtering by state, labels

**Usage Pattern**:
```python
github_service = self.service_registry.get('github')
if github_service:
    issues = await github_service.list_issues(
        repository='piper-morgan',
        state='all',
        limit=100
    )
```

---

## Quality Criteria

### Functional Requirements ✅
- Learns actual patterns from data
- Groups similar issues meaningfully
- Calculates confidence scores
- Provides actionable recommendations
- Handles no-data gracefully

### Code Quality ✅
- Modern Intent/IntentProcessingResult pattern
- Comprehensive docstrings
- Type hints throughout
- Error handling with logging
- Helper methods for separation of concerns

### Test Quality ✅
- TDD approach (red → green)
- Validates all edge cases
- Demonstrates real learning
- No placeholder responses

---

## Implementation Estimates

**Main handler**: ~130-150 lines
**Helper methods**: ~400 lines (5 methods)
**Total**: ~530-550 lines
**Tests**: ~250 lines (7-8 tests)
**Time**: 45-60 minutes

---

## Next Steps (Part 2)

1. Mark Part 1 complete
2. Move to Part 2: Define learning strategy document
3. Choose pattern types (recommend: issue_similarity + tag_patterns)
4. Design algorithm details
5. Estimate implementation complexity

**Status**: Part 1 complete - requirements understood ✅

---

**Created**: 2025-10-11, 5:05 PM
**Phase**: 5 (FINAL HANDLER)
**Target**: 100% GAP-1 completion
