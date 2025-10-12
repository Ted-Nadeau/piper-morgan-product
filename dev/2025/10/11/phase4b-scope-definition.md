# Phase 4B Scope Definition: _handle_prioritization

**Date**: 2025-10-11
**Handler**: `_handle_prioritization`
**Category**: STRATEGY
**Location**: `services/intent/intent_service.py` (lines 3634-3666)

---

## Executive Summary

This document defines the complete scope for implementing the `_handle_prioritization` handler, the **FINAL STRATEGY category handler**. This handler prioritizes items (issues, features, tasks) to help users decide what to work on first.

**Implementation Approach**: Scoring-based (weighted algorithms)
**Time Estimate**: 45-60 minutes total
**Prioritization Types**: 3 (issues, features, tasks)

---

## Prioritization vs Planning

### Phase 4 (_handle_strategic_planning)
- **Creates**: Multi-phase plans with tasks
- **Output**: Structured roadmaps
- **Focus**: How to execute (planning the work)
- **Example**: "Create 3-phase sprint plan for OAuth"

### Phase 4B (_handle_prioritization)
- **Ranks**: Items by importance/urgency
- **Output**: Ordered list with scores/reasoning
- **Focus**: What to do first (deciding priorities)
- **Example**: "Rank these 10 issues by priority"

**Both are STRATEGY** because they guide future decisions (forward-looking)

---

## Prioritization Types (3 Supported)

### Type 1: Issue Prioritization

**Purpose**: Rank GitHub issues/bugs by priority using impact, urgency, and effort

**Scoring Method**: `priority_score = (impact * urgency) / effort`
- Higher score = higher priority
- Impact (1-10): How many users affected? How critical?
- Urgency (1-10): How soon must this be addressed?
- Effort (1-10): How complex to implement? (lower = easier, inverse weight)

**Input Parameters**:
```python
{
    'prioritization_type': 'issues',
    'items': [  # List of issue objects or strings
        {
            'title': 'Critical authentication bug',
            'impact': 9,      # Optional - estimated if missing
            'urgency': 10,    # Optional - estimated if missing
            'effort': 2       # Optional - estimated if missing
        },
        # OR simple strings:
        'Fix login timeout',
        'Add dark mode feature',
        # ...
    ],
    'criteria': {  # Optional - custom weights
        'impact': 1.0,
        'urgency': 1.0,
        'effort': 1.0
    }
}
```

**Output Structure**:
```python
{
    'success': True,
    'prioritization_type': 'issues',
    'total_items': 3,
    'prioritized_items': [
        {
            'rank': 1,
            'item': {
                'title': 'Critical authentication bug',
                'impact': 9,
                'urgency': 10,
                'effort': 2
            },
            'priority_score': 45.0,  # (9 * 10) / 2 = 45
            'scores': {
                'impact': 9,
                'urgency': 10,
                'effort': 2
            },
            'reasoning': 'High impact, high urgency, low effort'
        },
        {
            'rank': 2,
            'item': 'Important database fix',
            'priority_score': 18.67,  # (8 * 7) / 3 = 18.67
            'scores': {
                'impact': 8,      # Estimated from title
                'urgency': 7,     # Estimated from "Important"
                'effort': 3       # Estimated
            },
            'reasoning': 'High impact, medium urgency, low effort'
        },
        {
            'rank': 3,
            'item': 'Nice to have feature',
            'priority_score': 1.88,  # (5 * 3) / 8 = 1.88
            'scores': {
                'impact': 5,      # Estimated
                'urgency': 3,     # Estimated from "nice to have"
                'effort': 8       # Estimated as complex
            },
            'reasoning': 'Medium impact, low urgency, high effort'
        }
    ],
    'recommendations': [
        'Start with rank #1: highest priority item',
        'Consider 1 quick win(s) with high impact and low effort',
        'Re-evaluate priorities weekly as context changes'
    ]
}
```

**Estimation from Titles** (when scores not provided):
- **Impact**:
  - 10: "critical", "security", "crash", "data loss"
  - 8: "important", "bug", "error", "broken"
  - 6: "feature", "enhancement", "improve"
  - 5: default
- **Urgency**:
  - 10: "urgent", "asap", "blocking", "critical"
  - 8: "soon", "high priority"
  - 3: "when possible", "nice to have"
  - 5: default
- **Effort**:
  - 9: "refactor", "rewrite", "major"
  - 7: "complex", "difficult"
  - 2: "quick", "simple", "typo", "minor"
  - 5: default

---

### Type 2: Feature Prioritization (RICE)

**Purpose**: Rank features using RICE framework (Reach, Impact, Confidence, Effort)

**Scoring Method**: `RICE_score = (reach * impact * confidence) / effort`
- Reach: How many users will this affect? (number or percentage)
- Impact: How much will it improve their experience? (0.25=minimal, 0.5=low, 1.0=medium, 2.0=high, 3.0=massive)
- Confidence: How confident are we? (0-100%, as decimal 0.0-1.0)
- Effort: Person-months of work (1-10+)

**Input Parameters**:
```python
{
    'prioritization_type': 'features',
    'items': [
        {
            'title': 'Analytics dashboard',
            'reach': 1000,      # Users per month
            'impact': 2.0,      # High impact
            'confidence': 0.8,  # 80% confident
            'effort': 3         # 3 person-months
        },
        # ...
    ]
}
```

**Output Structure**:
```python
{
    'success': True,
    'prioritization_type': 'features',
    'total_items': 3,
    'prioritized_items': [
        {
            'rank': 1,
            'item': {'title': 'Analytics dashboard', ...},
            'rice_score': 533.33,  # (1000 * 2.0 * 0.8) / 3 = 533.33
            'scores': {
                'reach': 1000,
                'impact': 2.0,
                'confidence': 0.8,
                'effort': 3
            },
            'reasoning': 'High reach (1000 users), high impact (2.0), good confidence (80%)'
        },
        # ... more items
    ],
    'recommendations': [
        'Start with rank #1: highest RICE score',
        'Validate reach estimates with user research',
        'Re-evaluate priorities quarterly as metrics change'
    ]
}
```

---

### Type 3: Task Prioritization (Eisenhower Matrix)

**Purpose**: Categorize tasks by urgency and importance into 4 quadrants

**Scoring Method**: Eisenhower Matrix quadrants
- **Quadrant 1** (Do First): High Urgency + High Importance
- **Quadrant 2** (Schedule): Low Urgency + High Importance
- **Quadrant 3** (Delegate): High Urgency + Low Importance
- **Quadrant 4** (Eliminate): Low Urgency + Low Importance

**Input Parameters**:
```python
{
    'prioritization_type': 'tasks',
    'items': [
        {
            'title': 'Fix production bug',
            'urgency': 'high',      # or 'low'
            'importance': 'high'    # or 'low'
        },
        {
            'title': 'Learn new framework',
            'urgency': 'low',
            'importance': 'high'
        },
        # ...
    ]
}
```

**Output Structure**:
```python
{
    'success': True,
    'prioritization_type': 'tasks',
    'total_items': 4,
    'prioritized_items': [
        {
            'rank': 1,
            'item': {'title': 'Fix production bug', ...},
            'quadrant': 1,
            'quadrant_name': 'Do First',
            'urgency': 'high',
            'importance': 'high',
            'action': 'Do immediately',
            'reasoning': 'Both urgent and important - highest priority'
        },
        {
            'rank': 2,
            'item': {'title': 'Learn new framework', ...},
            'quadrant': 2,
            'quadrant_name': 'Schedule',
            'urgency': 'low',
            'importance': 'high',
            'action': 'Schedule time for this',
            'reasoning': 'Important but not urgent - plan ahead'
        },
        # Quadrant 3 items (rank 3-X)
        # Quadrant 4 items (rank Y-N)
    ],
    'recommendations': [
        'Focus on Quadrant 1 tasks first (Do First)',
        'Schedule Quadrant 2 tasks to prevent them becoming urgent',
        'Consider delegating Quadrant 3 tasks',
        'Eliminate or defer Quadrant 4 tasks'
    ]
}
```

**Quadrant Priority Order**:
1. Quadrant 1 (Do First) - ranks 1-N
2. Quadrant 2 (Schedule) - ranks N+1-M
3. Quadrant 3 (Delegate) - ranks M+1-P
4. Quadrant 4 (Eliminate) - ranks P+1-Z

Within each quadrant, items maintain relative order from input.

---

## Main Handler Design

### Handler Signature (Modern Pattern)

```python
async def _handle_prioritization(
    self,
    intent: Intent,
    workflow_id: str
) -> IntentProcessingResult:
    """
    Handle prioritization requests - FULLY IMPLEMENTED.

    Prioritizes items (issues, features, tasks) based on various criteria
    to help determine what should be worked on first.

    Supported prioritization_types:
        - 'issues': Prioritize GitHub issues by impact/urgency/effort
        - 'features': Prioritize features using RICE framework
        - 'tasks': Prioritize tasks using Eisenhower matrix

    Intent Context Parameters:
        - prioritization_type (required): Type of prioritization
        - items (required): List of items to prioritize
        - criteria (optional): Custom criteria/weights

    Returns:
        IntentProcessingResult with prioritized items, scores, and recommendations
    """
```

### 4-Phase Handler Flow

**Phase 1: VALIDATION**
- Check `prioritization_type` presence
- Check `items` presence and is list
- Validate `prioritization_type` in supported types
- Extract optional `criteria` parameter
- Log validation results

**Phase 2: PRIORITIZATION** (type-specific)
- Route to appropriate helper method
- `issues` → `_prioritize_issues()`
- `features` → `_prioritize_features_rice()`
- `tasks` → `_prioritize_tasks_eisenhower()`

**Phase 3: RECOMMENDATIONS**
- Generate prioritization recommendations
- Use `_generate_prioritization_recommendations()`
- Include type-specific best practices

**Phase 4: RESPONSE BUILDING**
- Build IntentProcessingResult
- Include prioritized items with scores
- Include recommendations
- Include metadata
- Log success
- Handle errors

---

## Helper Methods Design

### Helper 1: _prioritize_issues

**Purpose**: Prioritize issues using impact/urgency/effort scoring

**Signature**:
```python
def _prioritize_issues(
    self,
    items: List[Any],
    criteria: Dict[str, float]
) -> List[Dict[str, Any]]:
    """
    Prioritize issues by impact, urgency, and effort.

    Args:
        items: List of issue objects or strings
        criteria: Optional weights for impact/urgency/effort (default: 1.0 each)

    Returns:
        List of prioritized items with scores, sorted by priority_score (descending)
    """
```

**Implementation**:
1. Extract weights from criteria (default 1.0)
2. For each item:
   - Extract or estimate impact/urgency/effort scores
   - Calculate: `priority_score = (impact * impact_weight * urgency * urgency_weight) / (effort * effort_weight)`
   - Generate reasoning string
   - Add to scored_items list
3. Sort by priority_score descending
4. Add ranks (1, 2, 3, ...)
5. Return prioritized list

**Estimation Methods** (3 sub-helpers):
- `_estimate_impact_from_title(title)` → 1-10
- `_estimate_urgency_from_title(title)` → 1-10
- `_estimate_effort_from_title(title)` → 1-10

**Estimated Lines**: ~80-90 lines

---

### Helper 2: _prioritize_features_rice

**Purpose**: Prioritize features using RICE framework

**Signature**:
```python
def _prioritize_features_rice(
    self,
    items: List[Any],
    criteria: Dict[str, float]
) -> List[Dict[str, Any]]:
    """
    Prioritize features using RICE (Reach, Impact, Confidence, Effort).

    Args:
        items: List of feature objects
        criteria: Optional (not used for RICE - fixed formula)

    Returns:
        List of prioritized features with RICE scores
    """
```

**Implementation**:
1. For each item:
   - Extract reach, impact, confidence, effort
   - Validate values (reach > 0, impact 0.25-3.0, confidence 0-1.0, effort > 0)
   - Calculate: `rice_score = (reach * impact * confidence) / effort`
   - Generate reasoning string
   - Add to scored_items list
2. Sort by rice_score descending
3. Add ranks
4. Return prioritized list

**Estimated Lines**: ~60-70 lines

---

### Helper 3: _prioritize_tasks_eisenhower

**Purpose**: Prioritize tasks using Eisenhower matrix (4 quadrants)

**Signature**:
```python
def _prioritize_tasks_eisenhower(
    self,
    items: List[Any],
    criteria: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Prioritize tasks using Eisenhower matrix (urgency vs importance).

    Args:
        items: List of task objects with urgency/importance
        criteria: Optional (not used - fixed quadrants)

    Returns:
        List of tasks categorized by quadrant and ranked
    """
```

**Implementation**:
1. Create 4 quadrant lists
2. For each item:
   - Extract urgency (high/low) and importance (high/low)
   - Determine quadrant (1-4)
   - Add to appropriate quadrant list with metadata
3. Combine quadrants in priority order: Q1 → Q2 → Q3 → Q4
4. Add sequential ranks across all quadrants
5. Return combined prioritized list

**Quadrant Actions**:
- Q1: "Do immediately"
- Q2: "Schedule time for this"
- Q3: "Consider delegating"
- Q4: "Eliminate or defer"

**Estimated Lines**: ~70-80 lines

---

### Helper 4: _generate_prioritization_recommendations

**Purpose**: Generate strategic recommendations based on prioritization results

**Signature**:
```python
def _generate_prioritization_recommendations(
    self,
    prioritized_items: List[Dict[str, Any]],
    prioritization_type: str
) -> List[str]:
    """
    Generate recommendations for acting on prioritized items.

    Args:
        prioritized_items: The prioritized list
        prioritization_type: Type of prioritization used

    Returns:
        List of 3-5 strategic recommendations
    """
```

**Implementation**:
1. Start with top item recommendation
2. **Issues**: Identify quick wins (low effort + high priority)
3. **Features**: Validate reach estimates, quarterly review
4. **Tasks**: Focus on Q1, schedule Q2, delegate Q3, eliminate Q4
5. Add focus recommendation (top 3-5 items)
6. Add re-evaluation cadence recommendation
7. Return 3-5 recommendations

**Estimated Lines**: ~40-50 lines

---

### Helper 5-7: Estimation Helpers (for Issues)

**Purpose**: Estimate scores from title keywords when not provided

**Signatures**:
```python
def _estimate_impact_from_title(self, title: str) -> int:
    """Estimate impact (1-10) from title keywords"""

def _estimate_urgency_from_title(self, title: str) -> int:
    """Estimate urgency (1-10) from title keywords"""

def _estimate_effort_from_title(self, title: str) -> int:
    """Estimate effort (1-10) from title keywords"""
```

**Implementation**:
Each method checks title for keywords and returns appropriate score (1-10).

**Estimated Lines**: ~15-20 lines each (45-60 lines total)

---

### Helper 8: _generate_priority_reasoning

**Purpose**: Generate human-readable reasoning for priority score

**Signature**:
```python
def _generate_priority_reasoning(
    self,
    impact: int,
    urgency: int,
    effort: int,
    priority_score: float
) -> str:
    """Generate reasoning string explaining the priority"""
```

**Implementation**:
Convert numeric scores to levels (high/medium/low) and format string.

**Example**: `"High impact, high urgency, low effort"` or `"Medium impact, low urgency, medium effort"`

**Estimated Lines**: ~15-20 lines

---

## Implementation Summary

### Total Lines Estimate
- Main handler: ~130-140 lines
- Helper 1 (issues): ~80-90 lines
- Helper 2 (RICE): ~60-70 lines
- Helper 3 (Eisenhower): ~70-80 lines
- Helper 4 (recommendations): ~40-50 lines
- Helper 5-7 (estimation): ~45-60 lines
- Helper 8 (reasoning): ~15-20 lines
- **Total**: ~440-510 lines

### Code Organization
All methods in `services/intent/intent_service.py`:
1. Main handler replaces placeholder (lines 3634-3666)
2. Helper methods added after main handler
3. No new files required

### Dependencies
- **No external services**: Scoring-based, all calculations local
- **No new imports**: Uses existing List, Dict, Any types
- **Standalone**: No integration with other handlers or services

### Error Handling
- Validate required parameters (prioritization_type, items)
- Validate items is non-empty list
- Validate prioritization_type in supported list
- Try/except around entire handler
- Log all errors with context
- Return failed IntentProcessingResult on error

---

## Test Strategy

### Test File
**Location**: `tests/intent/test_strategy_handlers.py` (add to existing)
**Test Class**: `TestHandlePrioritization`

### Test Coverage (8 tests)

**Test 1: Handler Exists**
- Call handler with valid parameters
- Assert success=True, requires_clarification=False

**Test 2: Missing prioritization_type**
- Call without prioritization_type
- Assert success=False, error message mentions parameter

**Test 3: Missing items**
- Call without items
- Assert success=False, error message mentions items

**Test 4: Empty items list**
- Call with empty list
- Assert success=False, error about empty list

**Test 5: Unknown prioritization_type**
- Call with invalid type
- Assert success=False, lists supported types

**Test 6: Issue Prioritization Success**
- Call with 3 issues (different impact/urgency/effort)
- Assert success=True
- Assert prioritized_items has 3 items with ranks
- Assert items ranked correctly (high priority first)
- Assert scores calculated correctly

**Test 7: Ranking Order Verification**
- Call with issues in specific order
- Verify highest priority item gets rank 1
- Verify lowest priority item gets last rank
- Verify scores determine order

**Test 8: All Types**
- Loop through 3 types (issues, features, tasks)
- Call handler for each
- Assert all succeed
- Assert appropriate structure for each type

### Test Lines Estimate
- Fixture: reuse from Phase 4
- Test 1: ~20 lines
- Test 2: ~15 lines
- Test 3: ~15 lines
- Test 4: ~15 lines
- Test 5: ~15 lines
- Test 6: ~40 lines
- Test 7: ~35 lines
- Test 8: ~40 lines
- **Total**: ~195-210 lines

---

## Pattern Consistency

### Comparison with Phase 4 (Planning)

**Similarities**:
✅ Uses Intent/IntentProcessingResult pattern
✅ Validates required parameters
✅ Type-specific processing (routing to helpers)
✅ Comprehensive error handling
✅ Returns structured data in intent_data
✅ Generates recommendations
✅ No external services needed

**Differences**:
- **Scoring vs Planning**: PRIORITIZATION scores/ranks, PLANNING creates phases
- **Single output**: Ordered list vs multi-phase structure
- **Numeric scores**: Priority scores vs phase descriptions
- **Simpler output**: Ranked list vs nested phase structure

**Quality Maintained**:
- Same error handling patterns
- Same validation approach
- Same logging discipline
- Same test coverage goals
- Same documentation quality

---

## Success Criteria

- [ ] Handler prioritizes real items (not placeholders)
- [ ] Items ranked correctly by score
- [ ] Tests demonstrate all 3 types work
- [ ] Pattern follows Phase 4 STRATEGY approach
- [ ] Zero `requires_clarification` placeholder responses
- [ ] Evidence shows actual prioritization
- [ ] Quality maintained at A+ level
- [ ] STRATEGY category 100% complete (2/2 handlers)

---

## Completion Checklist

### Part 1: Requirements Study ✅
- [x] Analyzed current placeholder
- [x] Identified 3 prioritization types
- [x] Reviewed scoring methods
- [x] Confirmed no existing prioritization utilities

### Part 2: Scope Definition ✅ (THIS DOCUMENT)
- [x] Chose 3 prioritization types
- [x] Designed scoring methods
- [x] Defined 8 helper methods
- [x] Estimated implementation size
- [x] Planned test strategy

### Part 3: Write Tests ⏳
- [ ] Add TestHandlePrioritization to test_strategy_handlers.py
- [ ] Write 8 comprehensive tests
- [ ] Confirm TDD red phase (tests fail)

### Part 4: Implementation ⏳
- [ ] Replace placeholder handler
- [ ] Implement 8 helper methods
- [ ] Add error handling
- [ ] Add logging

### Part 5: Run Tests ⏳
- [ ] Run test suite
- [ ] Verify 8/8 passing
- [ ] Fix any bugs

### Part 6: Evidence Collection ⏳
- [ ] Create completion report
- [ ] Create STRATEGY category completion document
- [ ] Capture test output
- [ ] Document sample prioritizations

---

**Scope Definition Complete**: 2025-10-11
**Next**: Part 3 - Write TDD tests (20 min)
**Time Remaining**: ~60 minutes for Parts 3-6
**Goal**: Complete STRATEGY category (2/2 handlers, 90% total progress)
