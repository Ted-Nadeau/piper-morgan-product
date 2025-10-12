# Phase 4 Scope Definition: _handle_strategic_planning

**Date**: 2025-10-11
**Handler**: `_handle_strategic_planning`
**Category**: STRATEGY
**Location**: `services/intent/intent_service.py` (lines 3191-3223)

---

## Executive Summary

This document defines the complete scope for implementing the `_handle_strategic_planning` handler, the **first STRATEGY category handler**. STRATEGY handlers plan future actions (forward-looking), distinguishing them from ANALYSIS (backward-looking), SYNTHESIS (content creation), and EXECUTION (action-taking).

**Implementation Approach**: Hybrid (template-based structure + LLM customization)
**Time Estimate**: 45-60 minutes total
**Planning Types**: 3 (sprint, feature_roadmap, issue_resolution)

---

## STRATEGY Category Definition

### Category Distinctions

**EXECUTION** (complete):
- **Does**: Creates/updates resources
- **Example**: Create GitHub issue, update issue status
- **Direction**: Present action

**ANALYSIS** (complete):
- **Reads**: Existing data
- **Analyzes**: Patterns, metrics, trends
- **Example**: Analyze commits, calculate metrics
- **Direction**: Backward-looking (understanding past/present)

**SYNTHESIS** (complete):
- **Creates**: New content/documents
- **Example**: Generate reports, summarize content
- **Direction**: Present creation

**STRATEGY** (starting now):
- **Plans**: Future actions and approaches
- **Recommends**: Best courses of action
- **Decides**: Priorities and roadmaps
- **Example**: Create sprint plan, prioritize features
- **Direction**: Forward-looking (planning future)

### Key Characteristics of STRATEGY

1. **Forward-looking**: Plans what will happen, not what did happen
2. **Prescriptive**: Recommends actions, not just describes
3. **Structured**: Produces actionable plans with phases/tasks/milestones
4. **Reasoned**: Includes rationale and recommendations
5. **Flexible**: Plans are starting points, not rigid requirements

---

## Planning Types (3 Supported)

### Type 1: Sprint Planning

**Purpose**: Create structured sprint/iteration plans for development work

**Input Parameters**:
```python
{
    'planning_type': 'sprint',
    'goal': str,           # Required - Sprint goal/objective
    'timeframe': str,      # Optional - Duration (default: '2_weeks')
    'context': str         # Optional - Additional context/constraints
}
```

**Example Input**:
```python
{
    'planning_type': 'sprint',
    'goal': 'Complete OAuth integration and user authentication',
    'timeframe': '2_weeks',
    'context': 'Team of 3 developers, includes testing and deployment'
}
```

**Output Structure**:
```python
{
    'success': True,
    'planning_type': 'sprint',
    'goal': 'Complete OAuth integration and user authentication',
    'timeframe': '2_weeks',
    'plan': {
        'goal': 'Complete OAuth integration and user authentication',
        'duration': '14 days',
        'phases': [
            {
                'phase': 1,
                'name': 'Planning & Setup',
                'duration': '1-2 days',
                'tasks': [
                    {'task': 'Refine OAuth requirements', 'priority': 'high'},
                    {'task': 'Set up OAuth provider accounts', 'priority': 'high'},
                    {'task': 'Create task breakdown and estimates', 'priority': 'medium'}
                ]
            },
            {
                'phase': 2,
                'name': 'Implementation',
                'duration': '8-10 days',
                'tasks': [
                    {'task': 'Implement OAuth flow (Google, GitHub)', 'priority': 'high'},
                    {'task': 'Build user authentication service', 'priority': 'high'},
                    {'task': 'Create login/logout UI components', 'priority': 'high'},
                    {'task': 'Write comprehensive unit tests', 'priority': 'high'},
                    {'task': 'Code review and refinement', 'priority': 'medium'}
                ]
            },
            {
                'phase': 3,
                'name': 'Testing & Deployment',
                'duration': '2-3 days',
                'tasks': [
                    {'task': 'Integration testing with OAuth providers', 'priority': 'high'},
                    {'task': 'Security review and penetration testing', 'priority': 'high'},
                    {'task': 'Documentation (setup, usage, troubleshooting)', 'priority': 'medium'},
                    {'task': 'Deploy to staging environment', 'priority': 'high'},
                    {'task': 'Production deployment with monitoring', 'priority': 'high'}
                ]
            }
        ],
        'success_criteria': [
            'Users can authenticate via OAuth (Google, GitHub)',
            'All tests passing (unit, integration, security)',
            'Documentation complete and reviewed',
            'Successfully deployed to production with monitoring'
        ]
    },
    'recommendations': [
        'Start with highest priority tasks (OAuth flow) first',
        'Schedule daily stand-ups for team alignment and blocker removal',
        'Reserve 2-3 days buffer time for unexpected OAuth provider issues',
        'Conduct sprint retrospective at the end to capture learnings',
        'Track progress daily and adjust plan if OAuth integration proves complex'
    ]
}
```

**Implementation Method**:
- **Template-based**: 3-phase structure (Planning → Implementation → Testing)
- **Customization**: Task descriptions incorporate goal details
- **Duration parsing**: Convert timeframe strings to days
- **Recommendations**: Generic sprint best practices

---

### Type 2: Feature Roadmap

**Purpose**: Create phased roadmaps for feature development over multiple sprints/months

**Input Parameters**:
```python
{
    'planning_type': 'feature_roadmap',
    'goal': str,           # Required - Feature goal
    'timeframe': str,      # Optional - Duration (default: '3_months')
    'context': str         # Optional - Constraints, dependencies
}
```

**Example Input**:
```python
{
    'planning_type': 'feature_roadmap',
    'goal': 'Build comprehensive analytics dashboard',
    'timeframe': '3_months',
    'context': 'Need user research before starting, deploy incrementally'
}
```

**Output Structure**:
```python
{
    'success': True,
    'planning_type': 'feature_roadmap',
    'goal': 'Build comprehensive analytics dashboard',
    'timeframe': '3_months',
    'plan': {
        'goal': 'Build comprehensive analytics dashboard',
        'duration': '3_months',
        'phases': [
            {
                'phase': 1,
                'name': 'Research & Planning',
                'duration': '2-3 weeks',
                'tasks': [
                    {'task': 'Conduct user interviews (10+ users)', 'priority': 'high'},
                    {'task': 'Analyze competitor analytics dashboards', 'priority': 'medium'},
                    {'task': 'Define key metrics and visualizations', 'priority': 'high'},
                    {'task': 'Create feature specification document', 'priority': 'high'},
                    {'task': 'Design mockups and user flows', 'priority': 'medium'}
                ]
            },
            {
                'phase': 2,
                'name': 'MVP Development',
                'duration': '4-5 weeks',
                'tasks': [
                    {'task': 'Implement core analytics backend (data collection)', 'priority': 'high'},
                    {'task': 'Build basic dashboard UI with 3-5 key charts', 'priority': 'high'},
                    {'task': 'Create real-time data refresh capability', 'priority': 'medium'},
                    {'task': 'Initial performance testing and optimization', 'priority': 'medium'},
                    {'task': 'Internal alpha testing with team', 'priority': 'high'}
                ]
            },
            {
                'phase': 3,
                'name': 'Enhancement & Polish',
                'duration': '3-4 weeks',
                'tasks': [
                    {'task': 'Add advanced visualizations (heatmaps, trends)', 'priority': 'medium'},
                    {'task': 'Implement custom dashboard builder', 'priority': 'medium'},
                    {'task': 'Polish UI/UX based on alpha feedback', 'priority': 'high'},
                    {'task': 'Performance optimization for large datasets', 'priority': 'high'},
                    {'task': 'Comprehensive documentation', 'priority': 'medium'}
                ]
            },
            {
                'phase': 4,
                'name': 'Launch Preparation',
                'duration': '1-2 weeks',
                'tasks': [
                    {'task': 'Beta testing with 20+ external users', 'priority': 'high'},
                    {'task': 'Fix critical bugs from beta feedback', 'priority': 'high'},
                    {'task': 'Create marketing materials and announcement', 'priority': 'medium'},
                    {'task': 'Staged rollout to 10% → 50% → 100% users', 'priority': 'high'},
                    {'task': 'Monitor performance and user adoption metrics', 'priority': 'high'}
                ]
            }
        ],
        'milestones': [
            {'milestone': 'Research Complete & Specs Finalized', 'target_date': 'Week 3'},
            {'milestone': 'MVP Released to Alpha Testers', 'target_date': 'Week 8'},
            {'milestone': 'Beta Release with Full Features', 'target_date': 'Week 11'},
            {'milestone': 'Public Launch to All Users', 'target_date': 'Week 13'}
        ],
        'dependencies': [
            'User research must complete before MVP design',
            'Alpha testing must pass before enhancement phase',
            'Beta testing must complete before public launch'
        ]
    },
    'recommendations': [
        'Validate assumptions with user research early to avoid costly pivots',
        'Build MVP first (Phase 2), then iterate based on real user feedback',
        'Maintain regular communication with stakeholders throughout development',
        'Plan for technical debt reduction alongside new features',
        'Use feature flags for gradual rollout to minimize risk',
        'Track progress weekly and adjust timeline if research reveals complexity'
    ]
}
```

**Implementation Method**:
- **Template-based**: 4-phase structure (Research → MVP → Enhancement → Launch)
- **Scaling**: Number of phases adjusts based on timeframe duration
- **Milestones**: Auto-generated with target weeks
- **Dependencies**: Standard feature development dependencies
- **Recommendations**: Feature development best practices

---

### Type 3: Issue Resolution Strategy

**Purpose**: Create strategic approaches for resolving complex issues/bugs

**Input Parameters**:
```python
{
    'planning_type': 'issue_resolution',
    'goal': str,           # Required - Issue description
    'context': str         # Optional - Issue details, attempted solutions
}
```

**Example Input**:
```python
{
    'planning_type': 'issue_resolution',
    'goal': 'Database queries timing out during peak load',
    'context': 'Affects 10% of users, happens 2-3 PM daily, query times >30s'
}
```

**Output Structure**:
```python
{
    'success': True,
    'planning_type': 'issue_resolution',
    'goal': 'Database queries timing out during peak load',
    'plan': {
        'goal': 'Resolve: Database queries timing out during peak load',
        'phases': [
            {
                'phase': 1,
                'name': 'Investigation',
                'tasks': [
                    {'task': 'Reproduce issue in staging environment', 'priority': 'high'},
                    {'task': 'Analyze slow query logs (2-3 PM timeframe)', 'priority': 'high'},
                    {'task': 'Profile database performance under load', 'priority': 'high'},
                    {'task': 'Check for missing indexes on frequently queried tables', 'priority': 'high'},
                    {'task': 'Review application code for N+1 queries', 'priority': 'medium'}
                ]
            },
            {
                'phase': 2,
                'name': 'Root Cause Analysis',
                'tasks': [
                    {'task': 'Identify specific slow queries (EXPLAIN ANALYZE)', 'priority': 'high'},
                    {'task': 'Determine if issue is query, index, or infrastructure', 'priority': 'high'},
                    {'task': 'Analyze query execution plans', 'priority': 'medium'},
                    {'task': 'Check database connection pool settings', 'priority': 'medium'},
                    {'task': 'Document findings and root cause', 'priority': 'high'}
                ]
            },
            {
                'phase': 3,
                'name': 'Solution Implementation',
                'tasks': [
                    {'task': 'Add missing database indexes', 'priority': 'high'},
                    {'task': 'Optimize slow queries (rewrite, denormalize if needed)', 'priority': 'high'},
                    {'task': 'Implement query result caching for frequent reads', 'priority': 'medium'},
                    {'task': 'Add database query monitoring/alerting', 'priority': 'medium'},
                    {'task': 'Write regression tests to prevent reoccurrence', 'priority': 'high'}
                ]
            },
            {
                'phase': 4,
                'name': 'Verification & Documentation',
                'tasks': [
                    {'task': 'Test fix in staging under simulated peak load', 'priority': 'high'},
                    {'task': 'Verify query times <1s during 2-3 PM window', 'priority': 'high'},
                    {'task': 'Deploy to production with monitoring', 'priority': 'high'},
                    {'task': 'Monitor for 1 week to confirm resolution', 'priority': 'high'},
                    {'task': 'Document root cause and solution for future reference', 'priority': 'medium'}
                ]
            }
        ],
        'success_criteria': [
            'All queries complete in <1 second during peak load',
            'Zero timeout errors during 2-3 PM daily peak',
            'Regression tests added to prevent reoccurrence',
            'Solution documented for team knowledge base'
        ]
    },
    'recommendations': [
        'Investigate root cause systematically before implementing fixes',
        'Use database profiling tools (EXPLAIN, slow query log) for evidence',
        'Write regression tests to prevent the issue from recurring',
        'Document the solution clearly for future team reference',
        'Monitor query performance after deployment for 1-2 weeks',
        'Consider adding database query performance alerting',
        'Track progress daily and adjust plan if root cause proves complex'
    ]
}
```

**Implementation Method**:
- **Template-based**: 4-phase structure (Investigation → Analysis → Implementation → Verification)
- **Customization**: Task descriptions reference the specific issue
- **Generic approach**: Applicable to most technical issues
- **Recommendations**: Debugging and resolution best practices

---

## Main Handler Design

### Handler Signature (Modern Pattern)

```python
async def _handle_strategic_planning(
    self,
    intent: Intent,
    workflow_id: str
) -> IntentProcessingResult:
    """
    Handle strategic planning requests - FULLY IMPLEMENTED.

    Creates strategic plans for projects, sprints, features, and issue resolution.
    This is a STRATEGY operation that plans future actions and provides recommendations.

    Supported planning_types:
        - 'sprint': Sprint/iteration planning with 3-phase structure
        - 'feature_roadmap': Feature development roadmap with 4-phase structure
        - 'issue_resolution': Strategic issue resolution with 4-phase structure

    Intent Context Parameters:
        - planning_type (required): Type of plan to create
        - goal (required): Primary goal/objective for the plan
        - timeframe (optional): Duration/deadline (default: type-specific)
        - context (optional): Additional context or constraints

    Returns:
        IntentProcessingResult with:
            - success: Boolean
            - message: Human-readable status
            - intent_data: Contains plan, recommendations, etc.
            - error: Error message (if failed)
    """
```

### 6-Phase Handler Flow

**Phase 1: VALIDATION**
- Check `planning_type` presence
- Check `goal` presence
- Validate `planning_type` in supported types
- Extract optional parameters (timeframe, context)
- Log validation results

**Phase 2: PLANNING** (type-specific)
- Route to appropriate helper method
- `sprint` → `_create_sprint_plan()`
- `feature_roadmap` → `_create_feature_roadmap()`
- `issue_resolution` → `_create_issue_resolution_plan()`

**Phase 3: RECOMMENDATIONS**
- Generate strategic recommendations
- Use `_generate_strategic_recommendations()`
- Include type-specific best practices
- Add general planning guidance

**Phase 4: RESPONSE BUILDING**
- Build IntentProcessingResult
- Include plan structure
- Include recommendations
- Include metadata

**Phase 5: LOGGING**
- Log successful plan creation
- Include planning_type and goal

**Phase 6: ERROR HANDLING**
- Catch exceptions
- Log errors with context
- Return failed IntentProcessingResult

---

## Helper Methods Design

### Helper 1: _create_sprint_plan

**Purpose**: Generate sprint/iteration plan with 3-phase structure

**Signature**:
```python
def _create_sprint_plan(
    self,
    goal: str,
    timeframe: str,
    context: str
) -> Dict[str, Any]:
    """
    Create a sprint plan with 3 phases (Planning, Implementation, Testing).

    Args:
        goal: Sprint goal/objective
        timeframe: Duration (e.g., '2_weeks', '1_week', '3_weeks')
        context: Additional context or constraints

    Returns:
        Dictionary containing:
            - goal: Sprint goal
            - duration: Parsed duration in days
            - phases: List of 3 phases with tasks
            - success_criteria: List of success criteria
    """
```

**Implementation**:
1. Parse timeframe to days using `_parse_timeframe_to_days()`
2. Build 3-phase structure:
   - Phase 1: Planning & Setup (1-2 days)
   - Phase 2: Implementation (bulk of time)
   - Phase 3: Testing & Deployment (2-3 days)
3. Each phase includes:
   - Phase number and name
   - Duration estimate
   - Tasks with priorities (high/medium/low)
4. Add success criteria (4 standard criteria)
5. Return structured plan

**Tasks per Phase**:
- Phase 1: Requirements, environment setup, task breakdown
- Phase 2: Core implementation, testing, code review
- Phase 3: Integration testing, documentation, deployment

**Estimated Lines**: ~60-70 lines

---

### Helper 2: _create_feature_roadmap

**Purpose**: Generate feature development roadmap with 4-phase structure

**Signature**:
```python
def _create_feature_roadmap(
    self,
    goal: str,
    timeframe: str,
    context: str
) -> Dict[str, Any]:
    """
    Create a feature development roadmap with 4 phases.

    Args:
        goal: Feature goal/objective
        timeframe: Duration (e.g., '3_months', '1_month', '6_months')
        context: Additional context or constraints

    Returns:
        Dictionary containing:
            - goal: Feature goal
            - duration: Timeframe
            - phases: List of 4 phases with tasks
            - milestones: Key milestones with target dates
            - dependencies: Phase dependencies
    """
```

**Implementation**:
1. Parse timeframe to determine number of phases
2. Build 4-phase structure:
   - Phase 1: Research & Planning
   - Phase 2: MVP Development
   - Phase 3: Enhancement & Polish
   - Phase 4: Launch Preparation
3. Each phase includes tasks with priorities
4. Generate milestones (4 milestones at phase boundaries)
5. Add standard dependencies
6. Return structured roadmap

**Milestones**: Generated based on timeframe
- Milestone 1: Research complete (Week 2-3)
- Milestone 2: MVP released (Week 7-8)
- Milestone 3: Beta release (Week 10-11)
- Milestone 4: Public launch (end of timeframe)

**Estimated Lines**: ~80-90 lines

---

### Helper 3: _create_issue_resolution_plan

**Purpose**: Generate issue resolution strategy with 4-phase structure

**Signature**:
```python
def _create_issue_resolution_plan(
    self,
    goal: str,
    context: str
) -> Dict[str, Any]:
    """
    Create an issue resolution plan with 4 phases.

    Args:
        goal: Issue description
        context: Issue details, attempted solutions, symptoms

    Returns:
        Dictionary containing:
            - goal: Issue description (prefixed with "Resolve:")
            - phases: List of 4 phases with tasks
            - success_criteria: Resolution success criteria
    """
```

**Implementation**:
1. Build 4-phase structure:
   - Phase 1: Investigation
   - Phase 2: Root Cause Analysis
   - Phase 3: Solution Implementation
   - Phase 4: Verification & Documentation
2. Each phase includes debugging/resolution tasks
3. Add success criteria (4 standard criteria)
4. Return structured plan

**Tasks per Phase**:
- Phase 1: Reproduce, analyze logs, profile performance
- Phase 2: Identify root cause, analyze execution plans
- Phase 3: Implement fix, add monitoring, write tests
- Phase 4: Verify fix, deploy, monitor, document

**Estimated Lines**: ~70-80 lines

---

### Helper 4: _generate_strategic_recommendations

**Purpose**: Generate strategic recommendations for plan execution

**Signature**:
```python
def _generate_strategic_recommendations(
    self,
    plan: Dict[str, Any],
    planning_type: str
) -> List[str]:
    """
    Generate strategic recommendations based on plan type.

    Args:
        plan: The generated plan structure
        planning_type: Type of plan ('sprint', 'feature_roadmap', 'issue_resolution')

    Returns:
        List of strategic recommendations (4-6 recommendations)
    """
```

**Implementation**:
1. Choose recommendations based on planning_type
2. **Sprint**: Stand-ups, buffer time, priorities, retrospective
3. **Feature Roadmap**: User research, MVP first, stakeholder communication, tech debt
4. **Issue Resolution**: Root cause first, regression tests, documentation
5. Add general recommendation: "Track progress and adjust as needed"
6. Return list of 4-6 recommendations

**Estimated Lines**: ~35-40 lines

---

### Helper 5: _parse_timeframe_to_days

**Purpose**: Parse timeframe strings into days

**Signature**:
```python
def _parse_timeframe_to_days(self, timeframe: str) -> int:
    """
    Parse timeframe string to number of days.

    Args:
        timeframe: String like '2_weeks', '1_month', '14_days'

    Returns:
        Integer number of days

    Examples:
        '2_weeks' → 14
        '1_month' → 30
        '3_months' → 90
        '7_days' → 7
        'not_specified' → 14 (default 2 weeks)
    """
```

**Implementation**:
1. Convert to lowercase
2. Extract numeric portion (if present)
3. Check for 'week' → multiply by 7
4. Check for 'month' → multiply by 30
5. Check for 'day' → use directly
6. Default to 14 days if unparseable
7. Return days as int

**Estimated Lines**: ~15-20 lines

---

## Implementation Summary

### Total Lines Estimate
- Main handler: ~120-140 lines
- Helper 1 (sprint): ~60-70 lines
- Helper 2 (roadmap): ~80-90 lines
- Helper 3 (issue resolution): ~70-80 lines
- Helper 4 (recommendations): ~35-40 lines
- Helper 5 (parse timeframe): ~15-20 lines
- **Total**: ~380-440 lines

### Code Organization
All methods in `services/intent/intent_service.py`:
1. Main handler replaces placeholder (lines 3191-3223)
2. Helper methods added after main handler
3. No new files required (unlike Phase 3B which was self-contained)

### Dependencies
- **No external services**: Template-based, no GitHub/LLM calls needed
- **No new imports**: Uses existing Dict, List, Any types
- **Standalone**: No integration with other handlers or services

### Error Handling
- Validate required parameters (planning_type, goal)
- Validate planning_type in supported list
- Try/except around entire handler
- Log all errors with context
- Return failed IntentProcessingResult on error

---

## Test Strategy

### Test File
**Location**: `tests/intent/test_strategy_handlers.py` (NEW FILE)
**Test Class**: `TestHandleStrategicPlanning`

### Test Coverage (6 tests)

**Test 1: Handler Exists (Not Placeholder)**
- Call handler with valid sprint plan request
- Assert `requires_clarification` is False or absent
- Assert `success` is True

**Test 2: Missing planning_type**
- Call handler without planning_type
- Assert `success` is False
- Assert error message mentions "planning_type"

**Test 3: Missing goal**
- Call handler without goal
- Assert `success` is False
- Assert error message mentions "goal"

**Test 4: Unknown planning_type**
- Call handler with invalid planning_type ('invalid_type')
- Assert `success` is False
- Assert error message lists supported types

**Test 5: Successful Sprint Plan**
- Call handler with valid sprint parameters
- Assert `success` is True
- Assert `plan` exists with required structure
- Assert plan has phases, tasks, success_criteria
- Verify task count > 0
- Verify recommendations exist

**Test 6: All Planning Types**
- Loop through 3 planning types
- Call handler for each type
- Assert all succeed
- Assert each returns appropriate structure

### Test Lines Estimate
- Fixture setup: ~15 lines
- Test 1: ~20 lines
- Test 2: ~15 lines
- Test 3: ~15 lines
- Test 4: ~15 lines
- Test 5: ~35 lines
- Test 6: ~30 lines
- **Total**: ~145-160 lines

---

## Pattern Consistency

### Comparison with Phase 3B (SYNTHESIS)

**Similarities**:
✅ Uses Intent/IntentProcessingResult pattern
✅ 6-phase handler flow (validation → process → format → response)
✅ Multiple helper methods for different types
✅ Comprehensive error handling with logging
✅ Returns structured data in intent_data
✅ Validation includes type checking

**Differences**:
- **No external services**: STRATEGY uses templates, SYNTHESIS used LLM
- **Simpler**: No complex fetching or LLM integration
- **Static**: Plans are template-based, not dynamically generated
- **Faster**: No async service calls, instant response

**Quality maintained**:
- Same error handling patterns
- Same validation approach
- Same logging discipline
- Same test coverage goals

---

## Success Criteria

- [ ] Handler creates real strategic plans (not placeholders)
- [ ] Plans have actionable phases and tasks
- [ ] Tests demonstrate all 3 planning types work
- [ ] Pattern follows established approach (validation, process, response)
- [ ] Zero `requires_clarification` placeholder responses
- [ ] Evidence shows actual strategic plans
- [ ] Quality maintained at A+ level
- [ ] Implementation complete in 45-60 minutes

---

## Completion Checklist

### Part 1: Requirements Study ✅
- [x] Analyzed current placeholder
- [x] Identified available infrastructure
- [x] Reviewed LLM integration patterns
- [x] Confirmed no existing planning utilities

### Part 2: Scope Definition ✅ (THIS DOCUMENT)
- [x] Chose 3 planning types
- [x] Designed input/output structures
- [x] Defined helper methods
- [x] Estimated implementation size
- [x] Planned test strategy

### Part 3: Write Tests ⏳
- [ ] Create test_strategy_handlers.py
- [ ] Write 6 comprehensive tests
- [ ] Confirm TDD red phase (tests fail)

### Part 4: Implementation ⏳
- [ ] Replace placeholder handler
- [ ] Implement 5 helper methods
- [ ] Add error handling
- [ ] Add logging

### Part 5: Run Tests ⏳
- [ ] Run test suite
- [ ] Verify 6/6 passing
- [ ] Fix any bugs

### Part 6: Evidence Collection ⏳
- [ ] Create completion report
- [ ] Create sample plans document
- [ ] Capture test output

---

**Scope Definition Complete**: 2025-10-11
**Next**: Part 3 - Write TDD tests (20 min)
**Time Remaining**: ~60 minutes for Parts 3-6
