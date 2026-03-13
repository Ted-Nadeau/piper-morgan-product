# TODO/FIXME Audit - January 26, 2026

**Total**: 73 TODOs (after filtering out todo-feature false positives)
**Original grep count**: 117 (44 were false positives from todo feature code)

---

## Category Summary

| Category | Count | Priority | Notes |
|----------|-------|----------|-------|
| Task Management API Stubs | 36 | LOW | `services/api/task_management.py` - intentional stubs |
| Analytics/Budget Tracking | 10 | MEDIUM | Database integration pending |
| Integration Wiring | 8 | MEDIUM | Feature completion items |
| Security/Auth | 4 | MEDIUM | Production hardening |
| Knowledge Graph | 2 | LOW | Future enhancement |
| Domain Model Cleanup | 2 | LOW | Code organization |
| Miscellaneous | 11 | LOW | Various small items |

---

## 1. Task Management API Stubs (36 TODOs) - LOW PRIORITY

**File**: `services/api/task_management.py`

These are **intentional placeholder stubs** for a future TaskManagementService. The pattern is consistent: "Implement X with TaskManagementService" + "Integrate with PM-040 Knowledge Graph".

**Assessment**: This is scaffolding code, not technical debt. The TODOs serve as implementation roadmap. No action needed unless/until TaskManagementService becomes a priority.

**Sample**:
```python
# TODO: Implement task creation with TaskManagementService
# TODO: Integrate with PM-040 Knowledge Graph for task relationships
# TODO: Add task to knowledge graph with appropriate node type and metadata
```

---

## 2. Analytics/Budget Tracking (10 TODOs) - MEDIUM PRIORITY

**Files**:
- `services/analytics/api_usage_tracker.py` (7 TODOs)
- `services/analytics/budget_manager.py` (3 TODOs)

**Nature**: Database integration for analytics features. Currently using in-memory or placeholder implementations.

| Line | Description |
|------|-------------|
| api_usage_tracker.py:223 | Implement budget checking logic |
| api_usage_tracker.py:233 | Implement actual database queries |
| api_usage_tracker.py:264 | Implement actual database queries |
| api_usage_tracker.py:328 | Implement actual database queries |
| api_usage_tracker.py:345 | Implement actual database queries |
| api_usage_tracker.py:370 | Implement actual database queries |
| api_usage_tracker.py:381 | Implement recommendation logic based on usage patterns |
| budget_manager.py:126 | Store in database |
| budget_manager.py:400 | Implement actual database storage |
| budget_manager.py:411-427 | Implement actual database queries (3 TODOs) |

**Recommendation**: Bundle into a CORE-ANALYTICS epic when budget tracking becomes alpha-critical.

---

## 3. Integration Wiring (8 TODOs) - MEDIUM PRIORITY

**Various integration points not fully wired**:

| File | Line | Description |
|------|------|-------------|
| intent_service/llm_classifier_factory.py | 55 | Wire BoundaryEnforcer when available |
| intent_service/canonical_handlers.py | 4294 | Replace with database-backed repository |
| integrations/slack/webhook_router.py | 1391 | Integrate with blocker detection |
| integrations/mcp/skills/standup_workflow_skill.py | 466,471,476 | Fetch from user configuration (3 TODOs) |
| integrations/github/issue_generator.py | 34 | Replace with actual LLM call |
| actions/commands/github_issue_command.py | 24 | Integrate with actual GitHub service |

**Recommendation**: These are feature completion items. Address as part of respective feature epics.

---

## 4. Security/Auth (4 TODOs) - MEDIUM PRIORITY

| File | Line | Description |
|------|------|-------------|
| security/key_leak_detector.py | 92 | Implement actual HIBP integration |
| security/user_api_key_service.py | 76 | Re-enable after alpha onboarding complete |
| auth/user_service.py | 116 | In production, use proper database storage |
| web/api/routes/settings_integrations.py | 1280 | Get user_id from auth context |

**Assessment**:
- HIBP integration is a nice-to-have security enhancement
- The "re-enable after alpha" is intentional temporary disable
- "In production" note is documentation, not urgent
- Auth context user_id is a real bug (using "system" instead of actual user)

**Recommendation**: #1280 (settings_integrations.py) should be fixed as it's using hardcoded "system" user_id.

---

## 5. Knowledge Graph (2 TODOs) - LOW PRIORITY

| File | Line | Description |
|------|------|-------------|
| knowledge/knowledge_graph_service.py | 348 | Implement more sophisticated algorithms (Dijkstra, A*, etc.) |
| orchestration/multi_agent_coordinator.py | 656 | More sophisticated parallel analysis for dependent task chains |

**Assessment**: Future enhancements for graph traversal efficiency. Not blocking current functionality.

---

## 6. Domain Model Cleanup (2 TODOs) - LOW PRIORITY

| File | Line | Description |
|------|------|-------------|
| database/models.py | 1596 | Re-enable after UniversalList migration is complete |
| analysis/document_analyzer.py | 74 | Move key_points to key_findings field in AnalysisResult |

**Assessment**: Code organization items. The document_analyzer one is a data model alignment task.

---

## 7. Miscellaneous (11 TODOs) - LOW PRIORITY

| File | Line | Description |
|------|------|-------------|
| intent_service/action_mapper.py | 75 | Section header "TODO ACTIONS" (false positive - it's a category name) |
| learning/context_matcher.py | 82 | Parse time specifications like "9am", "monday morning" |
| scheduler/standup_reminder_job.py | 148 | Query UserPreferenceManager for users |
| intent/intent_service.py | 1194 | Replace hardcoded projects with repository data |
| intent/intent_service.py | 3624 | Get actual user_id (using "default") |
| onboarding/portfolio_service.py | 431 | Add list_all_projects to ProjectRepository |

**Assessment**: Mix of feature enhancements and minor wiring fixes.

---

## Actionable Recommendations

### Immediate (File Issues)
1. **BUG**: `settings_integrations.py:1280` - Using "system" instead of auth context user_id
2. **BUG**: `intent_service.py:3624` - Using "default" instead of actual user_id

### Near-Term (Bundle into Epics)
3. **CORE-ANALYTICS**: Bundle the 10 analytics TODOs when budget tracking is prioritized
4. **Integration wiring**: Address as part of respective feature work

### No Action Needed
5. **Task Management stubs** (36 TODOs): Intentional scaffolding
6. **Knowledge graph enhancements**: Future optimization
7. **Domain cleanup**: Low-impact code organization

---

## False Positives Excluded

The following patterns were excluded from the 117 total:
- `todo_` - Variable/function naming
- `Todo` - Class names
- `TODO_` - Constant naming
- `todos` - Feature references
- `todo_list`, `todo_service`, `todo_management` - Service names
- `TodoCreate`, `TodoUpdate`, `TodoDelete` - Operation names
- `todo_repository` - Repository name
- `test_todo` - Test names

This reduced the count from 117 to 73 actual TODO comments.

---

*Audit completed: January 26, 2026*
