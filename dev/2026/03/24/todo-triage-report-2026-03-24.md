# TODO/FIXME Triage Report — 2026-03-24

**Scope**: `services/`, `web/`, `cli/` directories (production code only)
**Method**: Grep for TODO/FIXME comments, cross-referenced against GitHub issues (all states, 200+) and roadmap v14.3
**Total TODOs found**: ~107 unique actionable TODO comments across 22 files (excluding enum values, pattern lists, and doc references that mention "todo" as a domain concept)

---

## Critical — Security or Hot Code Path

### 1. HIBP integration missing — key leak detection is a stub
- **File**: `services/security/key_leak_detector.py:92`
- **Comment**: `# TODO: Implement actual HIBP integration`
- **Context**: `check_key_leaked()` returns a "safe" result with 0.8 confidence without actually checking Have I Been Pwned. Users get false assurance about key safety.
- **GitHub issue**: None found
- **Roadmap**: Not listed
- **Status**: **ORPHANED** — Security gap with no tracking. Needs an issue.

### 2. API key validation disabled for alpha
- **File**: `services/security/user_api_key_service.py:76`
- **Comment**: `# TODO: Re-enable after alpha onboarding complete`
- **Context**: `skip_validation = True` bypasses all API key format/security validation. Alpha is active; this needs a decision on when to re-enable.
- **GitHub issue**: None found (related #485 is closed — that was about FK violations, not re-enabling validation)
- **Roadmap**: Not listed
- **Status**: **ORPHANED** — Active security bypass with no tracking.

### 3. Hardcoded `user_id="default-user"` in todo management API (4 occurrences)
- **File**: `services/api/todo_management.py:304, 322, 339, 385`
- **Comment**: `# TODO: Get from auth context`
- **Context**: Four endpoints use `user_id="default-user"` instead of extracting from auth context. This bypasses multi-tenancy isolation.
- **GitHub issue**: #746 `[TECH-DEBT] Auth context injection for hardcoded user_id values` — **CLOSED**
- **Status**: **STALE or INCOMPLETE** — #746 was closed but these hardcoded values remain. Either the issue missed these call sites or work was incomplete. Needs verification.

### 4. BoundaryEnforcer not wired
- **File**: `services/intent_service/llm_classifier_factory.py:55`
- **Comment**: `# TODO: Wire BoundaryEnforcer when available`
- **Context**: Knowledge graph service created with `boundary_enforcer=None`. BoundaryEnforcer controls data access boundaries — passing None means no boundary enforcement on KG queries used by the LLM classifier.
- **GitHub issue**: None found specifically
- **Roadmap**: #470 (RBAC epic) is open in M1 — may cover this implicitly
- **Status**: **ORPHANED** — Potentially covered by RBAC epic but not explicitly tracked.

---

## Covered — Has Issue or Roadmap Entry

### 5. GitHub issue generator uses placeholder instead of LLM
- **File**: `services/integrations/github/issue_generator.py:34`
- **Comment**: `# TODO: Replace with actual LLM call when API keys are properly loaded`
- **GitHub issue**: **#694 WIRE-GITHUB-LLM** (OPEN, M2)
- **Status**: **COVERED**

### 6. Standup workflow configuration fetch stubs (3 occurrences)
- **File**: `services/integrations/mcp/skills/standup_workflow_skill.py:466, 471, 476`
- **Comments**: `# TODO: Fetch from user configuration` (for standup time, standup days, and digest preferences)
- **GitHub issue**: **#693 WIRE-STANDUP** (OPEN, M2)
- **Status**: **COVERED**

### 7. Slack webhook todo/blocker integration stubs (3 occurrences)
- **File**: `services/integrations/slack/webhook_router.py:1389, 1399, 1409`
- **Comments**: `# TODO: Integrate with TodoManagementService when user context available` / `# TODO: Integrate with blocker detection when available`
- **GitHub issue**: **#692 WIRE-SLACK** (OPEN, M2)
- **Status**: **COVERED**

### 8. UniversalList migration incomplete — TodoDB memberships disabled
- **File**: `services/database/models.py:1845`
- **Comment**: `# TODO: Re-enable after UniversalList migration is complete`
- **Context**: `memberships` relationship on TodoDB commented out after list_memberships table was dropped.
- **GitHub issue**: Part of the foundation/item-list-primitives refactor. Universal list work is implicit in M2 (MUX lifecycle issues #703, #714, #715).
- **Status**: **COVERED** (implicitly by M2 sprint work)

### 9. Standup reminder job — user preference query
- **File**: `services/scheduler/standup_reminder_job.py:148`
- **Comment**: `# TODO (Task 2): Query UserPreferenceManager for users with...`
- **GitHub issue**: **#693 WIRE-STANDUP** covers standup configuration wiring
- **Status**: **COVERED**

### 10. Slack webhook security backup — signature verification
- **File**: `services/integrations/slack/webhook_router.py.security-fix-backup:185`
- **Comment**: `# TODO: Re-enable signature verification for production`
- **Context**: This is a `.security-fix-backup` file, not active production code.
- **Status**: **STALE** — Backup file; the active `webhook_router.py` is the canonical source.

---

## Orphaned — Real Work, No Tracking

### 11. Budget manager — all database storage is stubbed (5 occurrences)
- **File**: `services/analytics/budget_manager.py:126, 400, 411, 416, 427`
- **Comments**: `# TODO: Store in database` / `# TODO: Implement actual database storage` / `# TODO: Implement actual database query` (x3)
- **Context**: BudgetManager has no persistent storage — all budget data is in-memory only. Restarting the server loses all budget tracking.
- **GitHub issue**: None found
- **Roadmap**: Not listed
- **Status**: **ORPHANED**

### 12. API usage tracker — all persistence is stubbed (7 occurrences)
- **File**: `services/analytics/api_usage_tracker.py:223, 233, 264, 328, 345, 370, 381`
- **Comments**: Various `# TODO: Implement actual database queries` / `# TODO: Implement budget checking logic` / `# TODO: Implement recommendation logic based on usage patterns`
- **Context**: Like BudgetManager, APIUsageTracker has no real persistence. Budget checks, usage queries, and recommendations are all stubs.
- **GitHub issue**: None found
- **Roadmap**: Not listed
- **Status**: **ORPHANED**

### 13. UserService uses in-memory dicts instead of database
- **File**: `services/auth/user_service.py:116`
- **Comment**: `# TODO: In production, this would use proper database storage`
- **Context**: `_users`, `_sessions`, `_email_to_user_id` are all plain dicts. Users are lost on server restart.
- **GitHub issue**: None found (related auth work in M1 #470/M5 #441 doesn't explicitly cover this)
- **Roadmap**: Not specifically listed
- **Status**: **ORPHANED** — Significant architectural gap.

### 14. Document analyzer — key_points field mapping
- **File**: `services/analysis/document_analyzer.py:74`
- **Comment**: `# TODO: Move key_points to the top-level key_findings field in AnalysisResult to match the domain model.`
- **GitHub issue**: None found
- **Roadmap**: M4 (Document Revolution) may address implicitly
- **Status**: **ORPHANED** — Minor but could cause confusion between key_points and key_findings.

### 15. Knowledge graph — sophisticated path algorithms
- **File**: `services/knowledge/knowledge_graph_service.py:348`
- **Comment**: `# TODO: Implement more sophisticated algorithms (Dijkstra, A*, etc.)`
- **GitHub issue**: None found
- **Roadmap**: Not listed
- **Status**: **ORPHANED** — Enhancement, low priority.

### 16. Intent service — suggestion tracking and hardcoded projects
- **File**: `services/intent/intent_service.py:226, 2151`
- **Comments**: `# TODO: Track across session` (suggestion count) / `# TODO: Replace hardcoded projects with actual data from repository`
- **GitHub issue**: None found for suggestion tracking. Hardcoded projects may be partially addressed by portfolio wiring.
- **Status**: **ORPHANED** — Line 2151 (hardcoded projects) is a real UX bug; line 226 is minor.

### 17. GitHub issue command — integration stub
- **File**: `services/actions/commands/github_issue_command.py:24`
- **Comment**: `# TODO: Integrate with actual GitHub service`
- **GitHub issue**: Possibly related to #694 (WIRE-GITHUB-LLM) but this is about service integration, not LLM calls
- **Status**: **ORPHANED** — May overlap with #694 but not explicitly covered.

### 18. Canonical handlers — hardcoded repo for testing
- **File**: `services/intent_service/canonical_handlers.py:4455`
- **Comment**: `# TODO: Replace with database-backed repository when available`
- **GitHub issue**: None found
- **Status**: **ORPHANED**

### 19. Context matcher — time parsing
- **File**: `services/learning/context_matcher.py:82`
- **Comment**: `# TODO: Parse time specifications like "9am", "monday morning"`
- **GitHub issue**: None found
- **Roadmap**: #101 (CONV-FEAT-TIME: Temporal Context System) in M5 may cover this
- **Status**: **ORPHANED** — Potentially covered by M5 temporal system but not explicitly tracked.

### 20. Multi-agent coordinator — parallel analysis
- **File**: `services/orchestration/multi_agent_coordinator.py:656`
- **Comment**: `# TODO: More sophisticated parallel analysis for dependent task chains`
- **GitHub issue**: #118 (INFR-AGENT: Multi-Agent Coordinator) in M3 may cover this
- **Roadmap**: M3
- **Status**: **ORPHANED** — Enhancement, potentially covered by M3 work.

### 21. Portfolio service — missing repository method
- **File**: `services/onboarding/portfolio_service.py:431`
- **Comment**: `# TODO: Add list_all_projects to ProjectRepository`
- **GitHub issue**: None found
- **Status**: **ORPHANED**

### 22. Learning dashboard — hardcoded user ID
- **File**: `web/assets/learning-dashboard.html:610`
- **Comment**: `const USER_ID = 'current_user'; // TODO: Make configurable`
- **GitHub issue**: #746 was about auth context injection but is closed. This HTML file may have been missed.
- **Status**: **ORPHANED** — Multi-tenancy gap in web layer.

---

## Stale — Completed or Superseded

### 23. task_management.py — massive stub file (~50 TODOs)
- **File**: `services/api/task_management.py` (lines 151-658)
- **Comments**: ~50 TODOs referencing PM-040 Knowledge Graph, PM-034 Intent Classification, TaskManagementService, etc.
- **Context**: This entire file appears to be a scaffold/spec that was never implemented. Every endpoint returns stub responses with `"status": "stub"`. The actual task/todo management is handled by `services/api/todo_management.py` and the intent service handlers.
- **Status**: **STALE** — This file is either dead code or a future spec. The PM-034/PM-040 references are internal epic codes not matching any GitHub issue format. Recommend decision: archive or delete.

### 24. todo_management.py — list/membership stubs (~25 TODOs)
- **File**: `services/api/todo_management.py` (lines 518-809)
- **Comments**: ~25 TODOs for list CRUD, membership, knowledge graph integration, intent classification
- **Context**: List endpoints (lines 518+) are all stubs returning `"status": "stub"`. The core CRUD endpoints (lines 259-420) work but have the hardcoded user_id issue noted in item #3.
- **Status**: **STALE** (list/KG/intent stubs) + **ORPHANED** (hardcoded user_id, item #3 above)

### 25. Slack webhook router backup file
- **File**: `services/integrations/slack/webhook_router.py.security-fix-backup:185`
- **Status**: **STALE** — Backup file, not production code.

---

## Summary Statistics

| Category | Count | Action Needed |
|----------|-------|---------------|
| **Critical** | 4 | File issues immediately |
| **Covered** | 6 | No action — will resolve when parent issues close |
| **Orphaned** | 12 | Need issues filed or explicit defer decisions |
| **Stale** | 3 | Need cleanup: delete dead code or archive |
| **Total unique items** | **25** | |

### Highest Priority Actions

1. **File issue**: HIBP integration stub in key_leak_detector.py (security gap)
2. **File issue**: API key validation disabled with no re-enable plan (security bypass)
3. **Verify**: #746 closure — 4 hardcoded `user_id="default-user"` remain in todo_management.py
4. **Decision needed**: Is `services/api/task_management.py` dead code? (~50 TODOs in a fully-stubbed file)
5. **File issue**: BudgetManager + APIUsageTracker have zero persistence (12 TODOs across 2 files)
6. **File issue**: UserService stores all user data in-memory dicts

### Files with Most TODOs

| File | Count | Nature |
|------|-------|--------|
| `services/api/task_management.py` | ~50 | Entire file is a stub |
| `services/api/todo_management.py` | ~25 | List endpoints are stubs; core has hardcoded user_id |
| `services/analytics/api_usage_tracker.py` | 7 | No persistence layer |
| `services/analytics/budget_manager.py` | 5 | No persistence layer |
| `services/integrations/slack/webhook_router.py` | 3 | Covered by #692 |
| `services/integrations/mcp/skills/standup_workflow_skill.py` | 3 | Covered by #693 |

---

*Report generated 2026-03-24 by Lead Developer agent. No TODOs were modified — analysis only.*
