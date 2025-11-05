# Gameplan: Sprint A8 Phase 3 - P1 Critical Issues
**Date**: November 2, 2025, 4:00 PM PT
**Issues**: #283, #284, #285
**Total Effort**: 14-18 hours
**Lead Developer**: To be deployed
**Based on**: gameplan-template.md v9.0

---

## Phase Structure Overview

### Complete Phase Sequence for This Work
- **Phase -1**: Infrastructure Verification (with PM) - MANDATORY
- **Phase 0**: Initial Bookending (GitHub investigation)
- **Phase 1**: Error Messages (#283) - 4 hours
- **Phase 2**: Action Mapping (#284) - 2 hours
- **Phase 3**: Todo System (#285) - 8-12 hours
- **Phase Z**: Final Bookending & Handoff

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### STOP! Complete This Section WITH PM Before Writing Rest of Gameplan

**Purpose**: Prevent wrong gameplans based on incorrect assumptions about what actually exists

### Part A: Chief Architect's Current Understanding

Based on available context from recent P0 work, I believe:

**Infrastructure Status**:
- [x] Web framework: **FastAPI** (confirmed via P0 work on auth/upload)
- [x] CLI structure: **Click** (main.py entry point with commands)
- [x] Database: **PostgreSQL** (alpha_users table, JSONB fields)
- [x] Testing framework: **pytest** (21 tests passing from P0 work)
- [x] Existing endpoints: **/auth/login, /auth/logout, /upload, /documents/** (added in P0s)
- [ ] Intent handling: **Partially working** (some actions missing handlers)
- [ ] Todo infrastructure: **Tables exist** (todos, todo_lists) but **not wired up**

**My understanding of the tasks**:
1. **#283**: Add conversational error messages to replace technical errors
2. **#284**: Create mapping layer between classifier actions and handler methods
3. **#285**: Wire up existing todo tables to REST API and chat interface

**I believe the current state is**:
- Auth working (JWT implemented)
- File upload working (5 file types)
- Document processing working (6 workflows)
- Error messages are technical/unfriendly
- Some classifier actions don't match handlers
- Todo system exists in DB but not exposed

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What actually exists in the filesystem?**
   ```bash
   # Quick verification commands
   ls -la web/api/routes/  # What routes exist?
   ls -la services/intent_service/  # Handler structure?
   grep -r "class.*Todo" services/  # Todo service exists?
   find . -name "*todo*" -type f  # All todo-related files?
   ```

2. **Recent work in this area?**
   - Last changes to error handling: ___________
   - Known issues with intent routing: ___________
   - Previous todo implementation attempts: ___________

3. **Actual task priorities?**
   - [ ] All three issues equally important
   - [ ] Error messages most critical for UX
   - [ ] Todo system blocks beta
   - [ ] Other priority: ___________

4. **Critical context I'm missing?**
   - Any existing error message patterns to follow?
   - Preferred todo UI approach (chat-only or also web)?
   - Known classifier/handler mismatches beyond create_github_issue?

### Part C: Proceed/Revise Decision

After PM verification:
- [ ] **PROCEED** - Understanding is correct, gameplan appropriate
- [ ] **REVISE** - Major assumptions wrong, need different approach
- [ ] **CLARIFY** - Need more context on: ___________

**If REVISE or CLARIFY checked, STOP and create new gameplan**

---

## Phase 0: Initial Bookending - GitHub Investigation

### Purpose
Establish context for all three issues, verify current state, understand interdependencies

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 283  # Error messages
   gh issue view 284  # Action mapping
   gh issue view 285  # Todo system
   ```

2. **Current State Investigation**
   ```bash
   # Error handling patterns
   grep -r "raise HTTPException\|except\|error" web/ --include="*.py"

   # Action/handler mapping
   grep -r "def.*handle.*action\|ACTION_MAPPING" services/ --include="*.py"

   # Todo infrastructure
   grep -r "Todo\|todo" services/database/models.py
   find . -path "*/test*" -prune -o -name "*todo*" -type f -print
   ```

3. **Test Current Behavior**
   ```bash
   # Test error messages
   curl -X POST http://localhost:8001/chat \
     -H "Content-Type: application/json" \
     -d '{"message": ""}'  # Empty should trigger error

   # Test action mapping
   python main.py chat "create a github issue"  # Should fail with mapping error

   # Check if todo endpoints exist
   curl http://localhost:8001/todos  # Likely 404
   ```

### Evidence to Collect
- Current error message examples (screenshot/copy)
- List of classifier actions that fail
- Todo table schema from database
- Any existing todo service code

### Expected Discoveries
- Error messages are raw exceptions
- Multiple action mismatches exist
- Todo tables exist but no API/handlers

### Dependency Analysis
- #283 and #284 are independent
- #285 depends on neither but is largest scope
- Could do in parallel with 2 agents

---

## Phase 1: Error Messages (#283) - 4 hours

### Objectives
Transform technical error messages into conversational, helpful responses

### Agent Assignment: **Cursor** (focused changes to specific error paths)

### Specific Tasks

1. **Create Error Message Service**
   ```python
   # services/errors/conversational_errors.py
   class ConversationalErrorService:
       ERROR_MAPPINGS = {
           'empty_input': "I didn't quite catch that...",
           'unknown_action': "I'm still learning...",
           'timeout': "That's complex, could you break it down?",
           'unknown_intent': "I'm not sure I understood...",
           'system_error': "Something went wrong on my end..."
       }
   ```

2. **Update Error Handlers**
   - web/api/routes/chat.py - catch empty input
   - services/intent_service/intent_service.py - handle unknown actions
   - services/conversation/conversation_handler.py - fallback responses
   - web/middleware/error_handler.py - system errors

3. **Add Input Validation**
   ```python
   # Before processing
   if not message or message.strip() == "":
       return ConversationalErrorService.empty_input_response()
   ```

4. **Maintain Technical Logging**
   ```python
   logger.error(f"Technical details: {str(e)}")  # For debugging
   return conversational_response  # For user
   ```

### Evidence Requirements
- Before: Screenshot of current error messages
- After: Same triggers showing friendly messages
- Test output showing all 5 error types handled
- Logs still capture technical details

### STOP Conditions
- Any existing conversational patterns found (use those instead)
- Error handling more complex than expected
- Breaking existing error reporting

---

## Phase 2: Action Mapping (#284) - 2 hours

### Objectives
Create mapping layer between classifier output and handler methods

### Agent Assignment: **Code** (investigation + implementation across services)

### Specific Tasks

1. **Investigate Current Mismatches**
   ```bash
   # Find all classifier actions
   grep -r "action=" services/intent_service/classifier.py

   # Find all handler methods
   grep -r "async def.*handle_" services/ --include="*.py"

   # Create comprehensive list of mismatches
   ```

2. **Create Action Mapper**
   ```python
   # services/intent_service/action_mapper.py
   class ActionMapper:
       # Based on investigation findings
       ACTION_MAPPING = {
           "create_github_issue": "create_issue",
           "list_github_issues": "list_issues",
           "create_notion_page": "create_page",
           # ... discovered mappings
       }

       @classmethod
       def map_action(cls, classifier_action: str) -> str:
           return cls.ACTION_MAPPING.get(
               classifier_action,
               classifier_action  # Fallback to original
           )
   ```

3. **Integrate into Intent Service**
   ```python
   # services/intent_service/intent_service.py
   mapped_action = ActionMapper.map_action(intent.action)
   handler = getattr(self, f"_handle_{mapped_action}", None)
   ```

4. **Add Logging for Unmapped Actions**
   ```python
   if classifier_action not in self.ACTION_MAPPING:
       logger.warning(f"Unmapped action: {classifier_action}")
       # Still try to handle, but log for future mapping
   ```

### Evidence Requirements
- List of all discovered mismatches
- Test showing create_github_issue now works
- Log output showing unmapped action warnings
- No regressions in existing working actions

### STOP Conditions
- More than 10 mismatched actions (indicates bigger problem)
- Handler naming pattern inconsistent
- Would require classifier retraining

---

## Phase 3: Todo System (#285) - 4-6 hours [UPDATED BASED ON PHASE -1 DISCOVERY]

### 🎉 MAJOR DISCOVERY: 75% Already Built!

Phase -1 investigation revealed extensive existing todo infrastructure:
- ✅ Complete database models (TodoDB, TodoListDB)
- ✅ Full repository layer (TodoRepository, TodoListRepository)
- ✅ Service layer (TodoKnowledgeService)
- ✅ API models (TodoCreateRequest, TodoResponse, etc.)
- ✅ Tests already written (test_todo_management_api.py)
- ✅ Documentation exists (PM-081-todo-api-documentation.md)

**Original Estimate**: 8-12 hours (build from scratch)
**Revised Estimate**: 4-6 hours (wire up existing infrastructure)

### Objectives [UPDATED]
Wire up existing todo system to web routes and chat interface

### Agent Assignment: **Code Agent Primary** (investigation + integration)
Cursor can assist with specific UI updates if needed

### Revised Implementation Plan

#### Step 1: Verify Existing Infrastructure (30 minutes)
```bash
# Check what exactly exists
cat services/api/todo_management.py | head -50
cat services/todo/todo_knowledge_service.py | head -50
python -c "from services.api.todo_management import router; print(router.routes)"

# Check if tests pass
pytest tests/api/test_todo_management_api.py -v
```

#### Step 2: Create Web Routes (1 hour)
```python
# Create web/api/routes/todos.py
from fastapi import APIRouter, Depends
from web.middleware.auth import get_current_user
from services.api.todo_management import (
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoResponse,
    # Import existing models
)
from services.todo.todo_knowledge_service import TodoKnowledgeService

router = APIRouter(prefix="/todos", tags=["todos"])

# Wire up existing service to web endpoints
@router.post("/", response_model=TodoResponse)
async def create_todo(
    request: TodoCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    service = TodoKnowledgeService()
    # Use existing service methods
    return await service.create_todo(current_user['user_id'], request)

# Similar for other CRUD operations...
```

Mount in web/app.py:
```python
from web.api.routes import todos
app.include_router(todos.router)
```

#### Step 3: Connect Intent Handlers (1-2 hours)
```python
# services/intent_service/todo_handlers.py (new file)
from services.todo.todo_knowledge_service import TodoKnowledgeService

class TodoIntentHandlers:
    def __init__(self):
        self.service = TodoKnowledgeService()

    async def handle_create_todo(self, intent, session_id, user_id):
        """Wire existing service to intent"""
        text = extract_todo_text(intent.message)
        todo = await self.service.create_todo(user_id, text)
        return format_todo_response(todo)

    # Similar for list, update, delete...
```

Update classifier to recognize patterns:
```python
# Already may exist, just verify:
# "add todo:", "show todos", "mark todo X complete"
```

#### Step 4: Chat Interface Integration (1-2 hours)
```python
# Update services/intent_service/intent_service.py
from .todo_handlers import TodoIntentHandlers

# Add to intent routing
if intent.category == IntentCategory.EXECUTION and "todo" in intent.action:
    handlers = TodoIntentHandlers()
    return await handlers.route_todo_action(intent, session_id, user_id)
```

#### Step 5: End-to-End Testing (1 hour)
```bash
# Test via API
curl -X POST http://localhost:8001/todos \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"text": "Review PR #285"}'

# Test via chat
python main.py chat "add todo: Review sprint progress"
python main.py chat "show my todos"
python main.py chat "mark todo 1 as complete"

# Run existing tests
pytest tests/api/test_todo_management_api.py -v
```

### Evidence Requirements [UPDATED]
- Existing service methods working (test output)
- Routes mounted and accessible (curl tests)
- Chat commands working (screenshots)
- Existing tests still passing
- No duplicate implementation (verify using existing services)

### STOP Conditions [UPDATED]
- Existing implementation incompatible with current architecture
- Tests reveal major bugs in existing code
- Would require rewriting repository/service layers

### Key Success Factor
**DO NOT REBUILD** - Use the existing infrastructure:
- TodoKnowledgeService for business logic
- TodoRepository for database access
- Existing API models for requests/responses
- Just add the connection layer!

---

## Phase Z: Final Bookending & Handoff

### Completion Checklist

#### 1. Issue Updates
- [ ] #283 description updated with solution
- [ ] #284 description updated with mappings found
- [ ] #285 description updated with implementation
- [ ] All checkboxes marked complete
- [ ] Evidence linked/attached

#### 2. Documentation Updates
- [ ] API documentation for todo endpoints
- [ ] Error message patterns documented
- [ ] Action mappings documented
- [ ] Update architecture.md if needed

#### 3. Evidence Compilation
- [ ] All test outputs in session logs
- [ ] Before/after comparisons
- [ ] Performance metrics (if relevant)
- [ ] No regressions confirmed

#### 4. Handoff Preparation
- [ ] Any discovered issues documented
- [ ] Technical debt noted
- [ ] Follow-up work identified
- [ ] Ready for PM testing

#### 5. PM Approval Request
```markdown
@PM - Phase 3 P1 Issues complete and ready for review:

Issue #283 (Error Messages):
- All 5 error types now conversational ✓
- Technical details still logged ✓
- Evidence: [screenshots/tests]

Issue #284 (Action Mapping):
- ActionMapper created with X mappings ✓
- create_github_issue now works ✓
- Evidence: [test output]

Issue #285 (Todo System):
- Full CRUD operations working ✓
- Chat commands operational ✓
- API endpoints tested ✓
- Evidence: [integration tests]

Please review and close if satisfied.
```

### Session Log Requirements
- Complete session log with all phases
- Evidence collected at each checkpoint
- Cross-validation notes (for #285)
- Session satisfaction assessment

---

## CRITICAL REMINDERS

### Methodology Enforcement
- **Inchworm Protocol**: Complete each issue 100% before moving
- **Evidence Required**: No claims without proof
- **75% Pattern**: Found that todo tables exist - wire them, don't rebuild
- **Anti-80%**: All acceptance criteria must be met
- **GitHub First**: Update issues throughout, not just at end

### Multi-Agent Coordination (for #285)
- Deploy both agents with clear task division
- Cross-validation checkpoints every 2 hours
- Shared evidence in session logs
- No duplicate work

### STOP Conditions (Apply Throughout)
Stop immediately and escalate if:
- Infrastructure doesn't match Phase -1 findings
- Critical features break (auth, upload)
- Performance degrades significantly
- Security issues discovered
- Assumptions prove wrong

### Success Metrics
- All error messages conversational
- All known action mismatches fixed
- Todo system fully operational
- Zero regressions
- PM satisfaction achieved

---

## Dependencies and Sequencing

### Recommended Execution Order

**Option A: Sequential (Safe)**
1. #283 Error Messages (4h)
2. #284 Action Mapping (2h)
3. #285 Todo System (8-12h)
Total: 14-18 hours

**Option B: Parallel (Faster)**
- Cursor: #283 Error Messages (4h)
- Code: #284 Action Mapping (2h) then start #285 Backend (6h)
- Both: Complete #285 together (2-4h)
Total: 10-12 hours

**Recommendation**: Option B if both agents available, Option A if resource constrained

---

## Risk Assessment

### Issue #283 (Error Messages)
- **Risk**: Low - Straightforward string replacements
- **Mitigation**: Keep technical logging intact

### Issue #284 (Action Mapping)
- **Risk**: Medium - May discover many mismatches
- **Mitigation**: Log unmapped for future work

### Issue #285 (Todo System)
- **Risk**: High - Large scope, multiple components
- **Mitigation**: Start with backend, add features incrementally

---

## Questions for PM Before Starting

2. **Todo UI**: Chat-only or also need web interface?
3. **Error Style**: Any specific tone/personality for error messages?
4. **Testing**: Manual testing in parallel or after completion?

---

*This gameplan follows gameplan-template.md v9.0 faithfully with all required elements*
*STOP at Phase -1 verification before proceeding*
