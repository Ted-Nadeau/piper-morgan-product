# Codebase TODO Inventory & Milestone Recommendations

**Date**: October 22, 2025, 2:05 PM PDT
**Prepared by**: Claude Code (prog-code)
**Purpose**: Comprehensive TODO analysis with milestone recommendations (Alpha, MVP, Post-MVP)
**Related**: Appendix to roadmap-accuracy-analysis-report.md

---

## Executive Summary

**Total TODOs**: 145 across Python files
**Location Distribution**: 59% in API scaffolds (todo/task management), 21% in tests, 20% in services

**Key Finding**: The majority of TODOs are concentrated in two **API scaffold files** (todo_management.py and task_management.py) that were created but never fully implemented. These represent a **deferred feature** (todo/task APIs), not technical debt.

**Critical Discovery**: The TODO/task management APIs are **semantically confusing** as the user noted - they were scaffolded to track "todos" and "tasks" as separate concepts, but Piper Morgan doesn't currently use either internally. This is **aspirational API work**, not core functionality.

**Recommendation**:
- **Alpha**: Address 11 critical TODOs (BoundaryEnforcer, auth, conversation)
- **MVP**: Defer all 86 API scaffold TODOs (todo/task management)
- **Post-MVP**: Address remaining 48 TODOs (tests, enhancements)

---

## Part 1: TODO Distribution Analysis

### By File Category

| Category | Count | % | Files | Priority |
|----------|-------|---|-------|----------|
| **API Scaffolds** | 86 | 59% | todo_management.py (47), task_management.py (39) | Post-MVP |
| **Tests** | 31 | 21% | test_pm033c_mcp_server.py (31) | Post-MVP |
| **Services** | 16 | 11% | knowledge_graph (5), auth (3), conversation (2), etc. | Alpha/MVP |
| **Infrastructure** | 12 | 8% | verification pyramid (2), lock tests (9), etc. | MVP |

### By Milestone Recommendation

| Milestone | Count | % | Rationale |
|-----------|-------|---|-----------|
| **Alpha** | 11 | 8% | Critical for production readiness |
| **MVP** | 12 | 8% | Important but not blocking Alpha |
| **Post-MVP** | 122 | 84% | Deferred features and test coverage |

---

## Part 2: Critical TODOs for Alpha Milestone

### 🚨 Priority 1: BoundaryEnforcer (5 TODOs)

**File**: `services/knowledge/knowledge_graph_service.py`
**Lines**: 58, 107, 259, 328
**Context**: BoundaryEnforcer integration incomplete

**TODOs**:
```python
# TODO: Add content-based boundary checking method to BoundaryEnforcer (x2)
# TODO: Implement proper boundary check (x2)
```

**Issue**: KnowledgeGraphService has TODOs for boundary checking via BoundaryEnforcer, but the integration is incomplete.

**Alpha Recommendation**: ✅ **ADDRESS IN ALPHA**
- **Why**: Ethics layer (BoundaryEnforcer) was activated in Sprint A3 (#197)
- **Impact**: Knowledge graph queries may bypass ethics layer
- **Effort**: 2-3 hours
- **Action**: Create issue "CORE-KNOW-BOUNDARY-COMPLETE: Complete BoundaryEnforcer Integration in KnowledgeGraphService"

---

### 🚨 Priority 2: Auth Service (3 TODOs)

**Files**:
- `web/api/routes/auth.py` (2 TODOs)
- `services/auth/user_service.py` (1 TODO)

**TODOs**:
```python
# web/api/routes/auth.py:49
TODO: Once jwt_service is in ServiceContainer, get from there.

# web/api/routes/auth.py:56
# TODO: Get from container when available

# services/auth/user_service.py:108
# TODO: In production, this would use proper database storage
```

**Issue**: JWT service not fully integrated into ServiceContainer, user service using temporary storage.

**Alpha Recommendation**: ✅ **ADDRESS IN ALPHA**
- **Why**: Sprint A6 delivered production auth (#227, #228), but integration not complete
- **Impact**: Auth not using proper dependency injection
- **Effort**: 1-2 hours
- **Action**: Create issue "CORE-AUTH-CONTAINER: Complete JWT Service Container Integration"

---

### 🚨 Priority 3: Conversation Reference Resolver (2 TODOs)

**File**: `services/conversation/reference_resolver.py`
**Lines**: 330, 349

**TODOs**:
```python
# Line 330
# TODO: Implement database query to get conversation history

# Line 349
# TODO: Implement with AsyncSessionFactory and ConversationTurn repository
```

**Issue**: Conversation history resolution not implemented with proper database queries.

**Alpha Recommendation**: ⚠️ **DEFER TO MVP**
- **Why**: Conversation history is operational via existing mechanisms
- **Impact**: Reference resolution may be incomplete but not blocking
- **Effort**: 3-4 hours
- **Action**: Defer to MVP, create issue "MVP-CONVO-REFS: Implement Database-Backed Conversation Reference Resolution"

---

### 🔧 Priority 4: Standup Reminder Integration (1 TODO)

**File**: `services/scheduler/standup_reminder_job.py`
**Line**: 147

**TODO**:
```python
# TODO (Task 2): Query UserPreferenceManager for users with
```

**Issue**: Standup reminder doesn't query user preferences for reminder times.

**Alpha Recommendation**: ⚠️ **DEFER TO MVP**
- **Why**: Standup handler exists and works (#240), preference integration is enhancement
- **Impact**: Reminders work but don't respect user preferences
- **Effort**: 2-3 hours
- **Action**: Defer to MVP, create issue "MVP-STAND-PREFS: Integrate UserPreferenceManager with Standup Reminders"

---

**Alpha TODO Summary**:
- ✅ **Must Address**: BoundaryEnforcer integration (5 TODOs, 2-3 hours)
- ✅ **Must Address**: JWT Service container integration (3 TODOs, 1-2 hours)
- ⚠️ **Defer to MVP**: Conversation reference resolver (2 TODOs, 3-4 hours)
- ⚠️ **Defer to MVP**: Standup preference integration (1 TODO, 2-3 hours)

**Total Alpha TODOs to Address**: 8 (5 + 3)
**Estimated Effort**: 3-5 hours

---

## Part 3: MVP TODOs (Deferred from Alpha)

### 📋 Category 1: Conversation Enhancements

**Files**:
- `services/conversation/reference_resolver.py` (2 TODOs)

**Recommendation**: MVP (not blocking Alpha)
**Effort**: 3-4 hours
**Issue**: "MVP-CONVO-REFS: Implement Database-Backed Conversation Reference Resolution"

---

### 📋 Category 2: Standup Enhancements

**Files**:
- `services/scheduler/standup_reminder_job.py` (1 TODO)

**Recommendation**: MVP (not blocking Alpha)
**Effort**: 2-3 hours
**Issue**: "MVP-STAND-PREFS: Integrate UserPreferenceManager with Standup Reminders"

---

### 📋 Category 3: LLM Integration

**Files**:
- `services/intent_service/llm_classifier_factory.py` (1 TODO)
- `services/integrations/github/issue_generator.py` (1 TODO)

**TODOs**:
```python
# llm_classifier_factory.py:55
boundary_enforcer=None,  # TODO: Wire BoundaryEnforcer when available

# issue_generator.py:34
# TODO: Replace with actual LLM call when API keys are properly loaded
```

**Recommendation**: MVP (not blocking Alpha)
**Effort**: 2-3 hours
**Issue**: "MVP-LLM-BOUNDARY: Complete BoundaryEnforcer Wiring in LLM Classifier"

---

### 📋 Category 4: User Context Service

**Files**:
- `services/user_context_service.py` (1 TODO)

**TODO**:
```python
# Line 74
user_id=session_id,  # TODO: Get actual user_id from session
```

**Recommendation**: MVP (not blocking Alpha)
**Effort**: 1-2 hours
**Issue**: "MVP-USER-CTX: Extract User ID from Session Token"

---

### 📋 Category 5: Document Analyzer

**Files**:
- `services/analysis/document_analyzer.py` (1 TODO)

**TODO**:
```python
# Line 74
# TODO: Move key_points to the top-level key_findings field in AnalysisResult
# to match the domain model.
```

**Recommendation**: MVP (not blocking Alpha)
**Effort**: 30 min
**Issue**: "MVP-ANALYZE-MODEL: Align DocumentAnalyzer with Domain Model"

---

### 📋 Category 6: Multi-Agent Coordinator

**Files**:
- `services/orchestration/multi_agent_coordinator.py` (1 TODO)

**TODO**:
```python
# Line 656
# TODO: More sophisticated parallel analysis for dependent task chains
```

**Recommendation**: Post-MVP (optimization)
**Effort**: 4-6 hours
**Issue**: "ENH-COORD-PARALLEL: Implement Sophisticated Parallel Analysis for Task Chains"

---

**MVP TODO Summary**:
- 📋 Conversation enhancements (2 TODOs, 3-4 hours)
- 📋 Standup enhancements (1 TODO, 2-3 hours)
- 📋 LLM boundary integration (2 TODOs, 2-3 hours)
- 📋 User context improvements (1 TODO, 1-2 hours)
- 📋 Document analyzer alignment (1 TODO, 30 min)

**Total MVP TODOs**: 7
**Estimated Effort**: 9-12 hours

---

## Part 4: Post-MVP TODOs (Deferred Features)

### 🔮 Category 1: TODO/Task Management APIs (86 TODOs - 59% of total!)

**Files**:
- `services/api/todo_management.py` (47 TODOs)
- `services/api/task_management.py` (39 TODOs)

**Context**: These files define REST API endpoints for managing "todos" and "tasks" as distinct concepts. They were scaffolded but never implemented.

**Semantic Confusion** (User's observation):
- **Problem**: Piper Morgan doesn't use "todos" or "tasks" internally
- **Reality**: These are **aspirational APIs** for external clients
- **Confusion**: Files named "todo_management" and "task_management" but implement REST APIs, not internal services

**All 86 TODOs Follow This Pattern**:
```python
# TODO: Implement TodoManagementService
# TODO: Implement TaskManagementService
# TODO: Integrate with PM-040 Knowledge Graph for todo relationships
# TODO: Integrate with PM-040 Knowledge Graph for task relationships
# TODO: Add task to knowledge graph with appropriate node type and metadata
# TODO: Trigger PM-034 intent classification for task updates
```

**Recommendation**: **POST-MVP (Enterprise feature)**
- **Why**: Not used by Piper internally, external API only
- **Impact**: Zero impact on Alpha or MVP (dead code)
- **Decision**: Keep or delete?
  - **Option 1**: Delete files (clean up aspirational code)
  - **Option 2**: Move to `aspirational/` directory
  - **Option 3**: Implement in Enterprise milestone

**Recommended Action**:
1. **Alpha**: Do nothing (not used, not breaking)
2. **MVP**: Decide if this feature is needed
3. **Post-MVP/Enterprise**: Implement if external API needed

**Estimated Effort if Implemented**: 20-30 hours (full implementation)

---

### 🔮 Category 2: MCP Server Tests (31 TODOs)

**Files**:
- `tests/integration/test_pm033c_mcp_server.py` (31 TODOs)

**All 31 TODOs**:
```python
# TODO: Implement when MCP server is available
```

**Context**: Integration tests for MCP server that was never deployed.

**Recommendation**: **POST-MVP**
- **Why**: MCP migration complete (#198), but MCP server deployment deferred
- **Impact**: MCP adapter works via client, server not deployed
- **Decision**: Implement when MCP server deployed

**Estimated Effort**: 8-12 hours (implement all 31 tests)

---

### 🔮 Category 3: Verification Pyramid (2 TODOs)

**Files**:
- `methodology/verification/pyramid.py` (2 TODOs)

**TODOs**:
```python
# Line 145
# TODO: Implement actual pattern search in codebase

# Line 192
# TODO: Implement actual dependency checking
```

**Recommendation**: **POST-MVP**
- **Why**: Methodology verification tooling, not production feature
- **Impact**: Development tool enhancement
- **Decision**: Implement when methodology tooling becomes priority

**Estimated Effort**: 3-4 hours

---

### 🔮 Category 4: QueryRouter Lock Tests (9 TODOs)

**Files**:
- `tests/regression/test_queryrouter_lock.py` (9 TODOs)

**Context**: Placeholder tests for QueryRouter regression prevention.

**Recommendation**: **MVP** (quality gate)
- **Why**: Regression tests important for stability
- **Impact**: QueryRouter is critical infrastructure
- **Decision**: Implement in MVP for quality assurance

**Estimated Effort**: 4-6 hours

---

**Post-MVP TODO Summary**:
- 🔮 TODO/Task Management APIs (86 TODOs, 20-30 hours OR DELETE)
- 🔮 MCP Server Tests (31 TODOs, 8-12 hours)
- 🔮 Verification Pyramid (2 TODOs, 3-4 hours)
- 🔮 QueryRouter Lock Tests (9 TODOs, 4-6 hours)

**Total Post-MVP TODOs**: 128
**Estimated Effort**: 35-52 hours (if all implemented)

---

## Part 5: Milestone Recommendations Summary

### Alpha Milestone (Recommended)

**Total TODOs**: 8
**Estimated Effort**: 3-5 hours
**Priority**: Critical for production readiness

1. ✅ **CORE-KNOW-BOUNDARY-COMPLETE**: Complete BoundaryEnforcer Integration (5 TODOs, 2-3h)
   - Files: services/knowledge/knowledge_graph_service.py
   - Why: Ethics layer activated in A3, integration incomplete

2. ✅ **CORE-AUTH-CONTAINER**: Complete JWT Service Container Integration (3 TODOs, 1-2h)
   - Files: web/api/routes/auth.py, services/auth/user_service.py
   - Why: Sprint A6 delivered auth, container integration incomplete

**Impact if NOT addressed**:
- Knowledge graph queries may bypass ethics layer (security risk)
- Auth service not using proper dependency injection (technical debt)

---

### MVP Milestone (Recommended)

**Total TODOs**: 16
**Estimated Effort**: 13-18 hours
**Priority**: Important but not blocking Alpha

1. 📋 **MVP-CONVO-REFS**: Database-Backed Conversation Reference Resolution (2 TODOs, 3-4h)
2. 📋 **MVP-STAND-PREFS**: Integrate UserPreferenceManager with Standup Reminders (1 TODO, 2-3h)
3. 📋 **MVP-LLM-BOUNDARY**: Complete BoundaryEnforcer Wiring in LLM Classifier (2 TODOs, 2-3h)
4. 📋 **MVP-USER-CTX**: Extract User ID from Session Token (1 TODO, 1-2h)
5. 📋 **MVP-ANALYZE-MODEL**: Align DocumentAnalyzer with Domain Model (1 TODO, 30min)
6. 📋 **MVP-QUERYROUTER-LOCKS**: Implement QueryRouter Regression Tests (9 TODOs, 4-6h)

---

### Post-MVP / Enterprise Milestone (Deferred)

**Total TODOs**: 121
**Estimated Effort**: 35-52 hours OR DELETE
**Priority**: Future features, not current roadmap

**Decision Required**:
1. **TODO/Task Management APIs** (86 TODOs):
   - **Option A**: Delete (aspirational code never used)
   - **Option B**: Move to aspirational/ directory
   - **Option C**: Implement in Enterprise milestone (20-30 hours)

   **Recommendation**: **Delete** (YAGNI principle - "You Ain't Gonna Need It")

2. **MCP Server Tests** (31 TODOs):
   - Implement when MCP server deployed (8-12 hours)

3. **Development Tooling** (4 TODOs):
   - Verification Pyramid, Multi-Agent Coordinator enhancements

---

## Part 6: Semantic Confusion Analysis (User's Observation)

### The "TODO Management" Irony

**User's Insight**: "The majority were located in the (ironically) semantically confusing todo type of list/item model."

**Analysis**:
- **File**: `services/api/todo_management.py` (47 TODOs)
- **Irony**: File managing "todos" is itself full of TODOs
- **Confusion**:
  - **Name**: "todo_management" suggests internal service
  - **Reality**: REST API for external clients
  - **Usage**: Not used anywhere in codebase

**Similar Pattern**:
- **File**: `services/api/task_management.py` (39 TODOs)
- **Name**: "task_management" suggests internal service
- **Reality**: REST API for external clients
- **Usage**: Not used anywhere in codebase

**Root Cause**: These were scaffolded during early development as "we might need this" APIs but never integrated.

**Recommendation**: **DELETE BOTH FILES**
- Not used internally
- Not exposed externally
- Not tested
- Not documented
- 59% of all TODOs (86/145)
- Removing them cleans up 59% of technical debt

**Impact of Deletion**:
- ✅ Removes 86 TODOs (59% reduction!)
- ✅ Clarifies codebase purpose
- ✅ Reduces maintenance burden
- ❌ Loses aspirational API scaffold (can recreate if needed)

---

## Part 7: Proposed Issues for Alpha Milestone

### Issue 1: CORE-KNOW-BOUNDARY-COMPLETE

**Title**: Complete BoundaryEnforcer Integration in KnowledgeGraphService

**Priority**: High
**Effort**: 2-3 hours
**Sprint**: A7 or A8

**Description**:
KnowledgeGraphService has 5 TODOs for boundary checking via BoundaryEnforcer, but integration is incomplete. This is critical for ensuring knowledge graph queries respect ethics layer boundaries activated in Sprint A3 (#197).

**Files**:
- services/knowledge/knowledge_graph_service.py (lines 58, 107, 259, 328)

**TODOs to Address**:
1. Add content-based boundary checking method to BoundaryEnforcer (x2)
2. Implement proper boundary check (x2)
3. [1 additional TODO]

**Acceptance Criteria**:
- [ ] All 5 TODOs in knowledge_graph_service.py resolved
- [ ] BoundaryEnforcer integration complete and tested
- [ ] Knowledge graph queries respect ethics layer boundaries
- [ ] Integration tests passing for boundary enforcement

**Related**:
- #197 CORE-ETHICS-ACTIVATE (Sprint A3)
- #230 CORE-KNOW-BOUNDARY (Sprint A3)

---

### Issue 2: CORE-AUTH-CONTAINER

**Title**: Complete JWT Service Container Integration

**Priority**: Medium
**Effort**: 1-2 hours
**Sprint**: A7 or A8

**Description**:
JWT service is operational (#227) but not fully integrated into ServiceContainer. Auth routes manually instantiate jwt_service instead of using dependency injection.

**Files**:
- web/api/routes/auth.py (lines 49, 56)
- services/auth/user_service.py (line 108)

**TODOs to Address**:
1. Move jwt_service to ServiceContainer
2. Update auth routes to get jwt_service from container
3. Replace temporary user storage with proper database

**Acceptance Criteria**:
- [ ] All 3 TODOs in auth files resolved
- [ ] JWT service available in ServiceContainer
- [ ] Auth routes use dependency injection
- [ ] User service uses proper database storage
- [ ] All auth tests passing

**Related**:
- #227 CORE-USERS-JWT (Sprint A6)
- #228 CORE-USERS-API (Sprint A6)

---

### Issue 3: CORE-CLEAN-ASPIRATIONAL

**Title**: Remove Aspirational TODO/Task Management APIs

**Priority**: Low
**Effort**: 30 minutes
**Sprint**: A8 (cleanup)

**Description**:
Remove unused TODO/Task management API scaffolds that were never implemented. These files contain 86 TODOs (59% of all TODOs) but are not used anywhere in the codebase.

**Files to Delete**:
- services/api/todo_management.py (47 TODOs, 682 lines)
- services/api/task_management.py (39 TODOs, 670 lines)

**Impact**:
- ✅ Removes 86 TODOs (59% reduction!)
- ✅ Clarifies codebase intent
- ✅ Reduces maintenance burden

**Acceptance Criteria**:
- [ ] Both files deleted
- [ ] No imports of deleted files elsewhere
- [ ] All tests passing
- [ ] TODO count reduced from 145 to 59

**Decision Point**: Confirm with PM before deletion (may want to keep as reference)

---

## Part 8: Action Items for PM and Chief Architect

### Immediate Actions (Today - Oct 22)

1. **Review TODO inventory** and milestone recommendations
2. **Decide on aspirational API deletion**:
   - Delete todo_management.py and task_management.py? (removes 59% of TODOs)
   - Or move to aspirational/ directory for future reference?
3. **Approve Alpha TODO issues**:
   - CORE-KNOW-BOUNDARY-COMPLETE (5 TODOs, 2-3 hours)
   - CORE-AUTH-CONTAINER (3 TODOs, 1-2 hours)

### Planning Actions (This Week)

4. **Create Alpha TODO issues** (if approved):
   - Issue: CORE-KNOW-BOUNDARY-COMPLETE
   - Issue: CORE-AUTH-CONTAINER
5. **Decide on Sprint A8 scope**:
   - Option 1: A7 only (UX enhancements)
   - Option 2: A7 + A8 (UX + TODO cleanup + #248)
6. **Plan MVP TODO cleanup**:
   - 16 TODOs, 13-18 hours estimated
   - Which are MVP-blocking?

### Documentation Actions (Next Week)

7. **Update technical debt tracking**:
   - Document decision on aspirational APIs
   - Track MVP TODOs in backlog
   - Archive Post-MVP TODOs for future consideration

---

## Part 9: Summary Statistics

### Before Cleanup

| Category | Count | % |
|----------|-------|---|
| Total TODOs | 145 | 100% |
| API Scaffolds | 86 | 59% |
| Tests | 31 | 21% |
| Services | 16 | 11% |
| Infrastructure | 12 | 8% |

### After Recommended Cleanup

| Category | Count | % | Change |
|----------|-------|---|--------|
| Total TODOs | 59 | 100% | -59% |
| Alpha TODOs | 8 | 14% | Critical |
| MVP TODOs | 16 | 27% | Important |
| Post-MVP TODOs | 35 | 59% | Deferred |

### Effort Estimates

| Milestone | TODOs | Effort | Priority |
|-----------|-------|--------|----------|
| Alpha | 8 | 3-5 hours | High |
| MVP | 16 | 13-18 hours | Medium |
| Post-MVP | 35 | 35-52 hours | Low |
| **Total** | **59** | **51-75 hours** | - |

---

## Appendices

### Appendix A: Full TODO List by File

**Services** (16 TODOs):
- knowledge_graph_service.py: 5 TODOs (Alpha)
- conversation/reference_resolver.py: 2 TODOs (MVP)
- auth/user_service.py: 1 TODO (Alpha)
- user_context_service.py: 1 TODO (MVP)
- scheduler/standup_reminder_job.py: 1 TODO (MVP)
- intent_service/llm_classifier_factory.py: 1 TODO (MVP)
- integrations/github/issue_generator.py: 1 TODO (MVP)
- orchestration/multi_agent_coordinator.py: 1 TODO (Post-MVP)
- analysis/document_analyzer.py: 1 TODO (MVP)

**Web** (2 TODOs):
- web/api/routes/auth.py: 2 TODOs (Alpha)

**Infrastructure** (12 TODOs):
- methodology/verification/pyramid.py: 2 TODOs (Post-MVP)
- tests/regression/test_queryrouter_lock.py: 9 TODOs (MVP)
- tests/services/test_file_resolver_edge_cases.py: 1 TODO (Post-MVP)

**Tests** (31 TODOs):
- tests/integration/test_pm033c_mcp_server.py: 31 TODOs (Post-MVP)

**API Scaffolds** (86 TODOs - RECOMMENDED FOR DELETION):
- services/api/todo_management.py: 47 TODOs
- services/api/task_management.py: 39 TODOs

### Appendix B: Recommended Deletion Impact

**Files**:
- services/api/todo_management.py (682 lines, 47 TODOs)
- services/api/task_management.py (670 lines, 39 TODOs)

**Total Removal**:
- 1,352 lines of code
- 86 TODOs (59% of all TODOs)
- 2 unused API files

**Risk Assessment**:
- ✅ No imports found elsewhere in codebase
- ✅ No tests reference these files
- ✅ No documentation mentions these APIs
- ⚠️ May lose reference if needed in future (can recreate from git history)

**Recommendation**: **DELETE** (clean up technical debt)

---

**Report Prepared By**: Claude Code (prog-code)
**Session Log**: dev/2025/10/22/2025-10-22-1149-prog-code-log.md
**Related**: roadmap-accuracy-analysis-report.md
**For**: PM and Chief Architect Alpha milestone planning session
