# Action Mapping Analysis - Issue #284

## Classification Output vs Handler Methods

### Classifier Actions Found (from classifier.py)
1. `clarification_needed`
2. `count_projects`
3. `get_default_project`
4. `find_project`
5. `get_project_details`
6. `get_project`
7. `create_item`
8. `search_content`
9. `find_documents`
10. `search_files`
11. `analyze_data`
12. `generate_content`
13. `strategic_planning`
14. `list_items`
15. `learn_pattern`

### Additional Actions from WorkflowFactory
16. `create_github_issue`
17. `create_ticket`
18. `create_issue`
19. `generate_report`
20. `review_issue`
21. `analyze_github_issue`
22. `review_github_issue`
23. `check_github_issue`
24. `analyze_file`
25. `performance_analysis`
26. `user_feedback_analysis`
27. `system_analysis`
28. `list_projects`
29. `list_all_projects`
30. `show_projects`
31. `create_feature`
32. `analyze_metrics`
33. `create_task`
34. `plan_strategy`
35. `analyze_feedback`
36. `confirm_project`
37. `select_project`

### Handler Methods Found (from IntentService)
1. `_handle_missing_engine`
2. `_handle_conversation_intent`
3. `_handle_query_intent`
4. `_handle_standup_query`
5. `_handle_projects_query`
6. `_handle_generic_query`
7. `_handle_execution_intent` (dispatcher)
8. `_handle_create_issue`
9. `_handle_update_issue`
10. `_handle_analysis_intent` (dispatcher)
11. `_handle_analyze_commits`
12. `_handle_generate_report`
13. `_handle_analyze_data`
14. `_handle_synthesis_intent` (dispatcher)
15. `_handle_generate_content`
16. `_handle_summarize`
17. `_handle_strategy_intent` (dispatcher)
18. `_handle_strategic_planning`
19. `_handle_prioritization`
20. `_handle_learning_intent` (dispatcher)
21. `_handle_learn_pattern`
22. `_handle_unknown_intent`

## Current Routing Logic

### EXECUTION Intent Handler (lines 464-499)
```python
if intent.action in ["create_issue", "create_ticket"]:
    return await self._handle_create_issue(...)
elif intent.action in ["update_issue", "update_ticket"]:
    return await self._handle_update_issue(...)
else:
    # Falls through to "not yet implemented"
```

**Problem**:
- Classifier outputs: `"create_github_issue"`, `"create_item"`
- Handler expects: `"create_issue"` or `"create_ticket"`
- Mismatch = Error!

### ANALYSIS Intent Handler (lines 680-732)
```python
if "commit" in intent.action.lower():
    return await self._handle_analyze_commits(...)
elif "report" in intent.action.lower():
    return await self._handle_generate_report(...)
elif "data" in intent.action.lower():
    return await self._handle_analyze_data(...)
elif "summarize" in intent.action.lower():
    return await self._handle_summarize(...)
```

**Current**: Uses substring matching (fragile)

### SYNTHESIS Intent Handler (lines 1289-1322)
```python
if "content" in intent.action.lower():
    return await self._handle_generate_content(...)
elif "report" in intent.action.lower():
    return await self._handle_generate_report(...)
```

**Current**: Uses substring matching (fragile)

### STRATEGY Intent Handler (lines 3206-3239)
```python
if "plan" in intent.action.lower():
    return await self._handle_strategic_planning(...)
elif "priorit" in intent.action.lower():
    return await self._handle_prioritization(...)
```

**Current**: Uses substring matching (fragile)

### LEARNING Intent Handler (lines 4417-4447)
```python
if "pattern" in intent.action.lower():
    return await self._handle_learn_pattern(...)
```

**Current**: Uses substring matching (fragile)

## Proposed ActionMapper

### Mapping Strategy
1. Explicit mappings for known mismatches
2. Normalize action names (e.g., `"create_github_issue"` → `"create_issue"`)
3. Log unmapped actions for future additions
4. Graceful fallback to original action name

### Key Mappings Needed
```python
ACTION_MAPPING = {
    # EXECUTION actions
    "create_github_issue": "create_issue",
    "create_item": "create_issue",
    "update_github_issue": "update_issue",

    # ANALYSIS actions
    "analyze_data": "analyze_data",  # Already matches
    "analyze_github_issue": "analyze_data",
    "review_github_issue": "analyze_data",
    "check_github_issue": "analyze_data",
    "analyze_file": "analyze_data",
    "analyze_metrics": "analyze_data",
    "analyze_feedback": "analyze_data",

    # SYNTHESIS actions
    "generate_content": "generate_content",  # Already matches
    "generate_report": "generate_report",  # Already matches

    # STRATEGY actions
    "strategic_planning": "strategic_planning",  # Already matches
    "plan_strategy": "strategic_planning",
    "prioritize": "prioritization",

    # LEARNING actions
    "learn_pattern": "learn_pattern",  # Already matches

    # QUERY actions (handled differently - by method routing)
    "list_projects": "projects_query",
    "list_all_projects": "projects_query",
    "show_projects": "projects_query",
    "get_project": "projects_query",
}
```

## Implementation Notes

1. **Create new file**: `services/intent_service/action_mapper.py`
2. **Integration point**: After classification, before routing
3. **Logging**: Warn on unmapped actions (helps discover new patterns)
4. **Testing**: Verify create_github_issue → create_issue works

## Success Criteria
- [ ] All known action mismatches mapped
- [ ] create_github_issue test case works
- [ ] No regressions in existing working actions
- [ ] Unmapped actions logged (not errored)
- [ ] Clear documentation of mapping rationale
