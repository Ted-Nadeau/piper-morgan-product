# Prompt for Claude Code: Action Mapping (#284) + Todo System (#285)

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims. You have access to Serena MCP for semantic code navigation.

## Essential Context (Read First)
Read these briefing documents in project knowledge:
- BRIEFING-ESSENTIAL-AGENT.md - Your role requirements
- BRIEFING-CURRENT-STATE.md - Sprint A8 Phase 3 focus
- piper-style-guide.md - Piper's voice/tone for all communications

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Gameplan Assumptions FIRST
**Before doing ANYTHING else, verify infrastructure matches gameplan**:

```bash
# Gameplan assumes:
# - IntentService exists with action routing
# - TodoKnowledgeService exists (~75% complete)
# - Database tables: todos, todo_lists (exist)
# - Classifier outputs action names
# - Handlers expect method names

# Verify reality:
ls -la services/intent_service/
ls -la services/todo/
ls -la services/api/todo_management.py

# Find action handling patterns
serena.find_symbol(name_path="IntentService")
serena.find_symbol(name_path="TodoKnowledgeService")

# Check if ActionMapper or similar already exists (75% pattern)
find . -name "*action*mapper*" -o -name "*humanize*" -type f
grep -r "ActionMapper\|action_mapping\|humanize" services/ --include="*.py"
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

---

## 🛡️ ANTI-80% COMPLETION SAFEGUARDS (CRITICAL)

### MANDATORY Method Enumeration
When implementing ANY interface or mapping:

1. **Create comparison table FIRST**:
```
Classifier Actions | Mapped Handler | Status
------------------ | -------------- | ------
create_github_issue | create_issue  | ✓ Mapped
list_github_issues  | list_issues   | ✓ Mapped
[action_3]          | [handler_3]   | ✗ MISSING
TOTAL: 2/3 = 67% INCOMPLETE - CANNOT PROCEED
```

2. **100% = ALL methods mapped, not "most methods"**
3. **Evidence = Show the complete mapping dictionary**

### No Claiming "Core Works"
❌ BAD: "Core functionality works, just missing 2 actions"
✅ GOOD: "Mapping: 8/10 actions complete. Cannot proceed until 10/10."

---

## Mission

**Objective**: Fix action routing and wire up todo system

**Two Issues in Sequence**:
1. **#284** (2h): Create ActionMapper to fix classifier→handler mismatch
2. **#285** (4-6h): Wire existing TodoKnowledgeService to web routes + chat

**Scope Boundaries**:
- This prompt covers: Backend integration only
- NOT in scope: Web UI design (minimal API only)
- Cursor handles: Error messages (#283), documentation

---

## Context

**GitHub Issues**:
- #284: CORE-ALPHA-ACTION-MAPPING
- #285: CORE-ALPHA-TODO-INCOMPLETE

**Current State** (from P0 sprint Nov 1):
- ✅ Auth working (JWT + bcrypt)
- ✅ Intent classification working (98.62% accuracy)
- ✅ Some handlers working (documents, file upload)
- ❌ Some classifier actions have no matching handlers
- ❌ Todo system exists in database but not exposed

**Target State**:
- ✅ All classifier actions map to handlers
- ✅ Todo CRUD via web API
- ✅ Todo operations via chat commands
- ✅ 100% of discovered actions mapped
- ✅ 100% of todo service methods exposed

**Dependencies**:
- Requires auth system (complete from Nov 1)
- Parallel to Cursor's error message work (#283)
- Blocks beta release (todo system required)

**Infrastructure Verified**: After Phase -1 investigation above

---

## 🔍 PHASE -1 CRITICAL DISCOVERIES (MUST INVESTIGATE)

### Discovery 1: Existing Humanization Work
**PM Statement**: "We made a whole effort to humanize error messages in the past. Doesn't seem to be fully engaged."

**Your Task**:
```bash
# Find existing humanization/mapping work
find . -name "*humanize*" -o -name "*action*map*" -o -name "*translator*" -type f
grep -r "humanize\|action.map\|friendly.error" services/ --include="*.py"

# Check for ActionHumanizer, ActionMapper, ErrorTranslator classes
serena.find_symbol(name_path="ActionHumanizer")
serena.find_symbol(name_path="ActionMapper")
serena.find_symbol(name_path="ErrorTranslator")
```

**If you find existing work**:
1. ✅ Document what exists and why not working
2. ✅ Extend it, don't rebuild it
3. ✅ Report findings before implementing

### Discovery 2: Todo Infrastructure (75% Pattern Expected)
**PM Statement**: "Todo system ~75% complete - just needs wiring"

**Your Task**:
```bash
# Verify what exists
cat services/api/todo_management.py | head -100
cat services/todo/todo_knowledge_service.py | head -100
grep -r "class Todo" services/database/models.py

# Check existing tests
ls -la tests/api/test_todo_management_api.py
pytest tests/api/test_todo_management_api.py -v --collect-only

# Find what's NOT wired
curl http://localhost:8001/todos  # Likely 404
grep -r "todos" web/app.py  # Check if mounted
```

**If infrastructure exists**:
1. ✅ Use it, don't rebuild it
2. ✅ Just create the wiring layer
3. ✅ Report what % is actually complete

---

## Evidence Requirements (CRITICAL)

### For EVERY Claim You Make:
- **"Created ActionMapper"** → Show `cat services/intent_service/action_mapper.py`
- **"All actions mapped"** → Show complete mapping dictionary with X/X = 100%
- **"Todo routes working"** → Show `curl` test with actual response
- **"Chat integration works"** → Show CLI test with actual output
- **"Tests pass"** → Show `pytest` output with pass counts
- **"Committed changes"** → Show `git log --oneline -1` output

### Completion Bias Prevention:
- **NO "should work"** - only "here's proof it works"
- **NO "core done"** - only "X/X = 100% complete"
- **NO assumptions** - only verified facts
- **NO rushing** - evidence first, claims second

### Git Workflow Discipline:
After code changes:
```bash
git status
git add [files]
git commit -m "fix: Map actions to handlers (#284)"
git log --oneline -1  # SHOW THIS OUTPUT
```

---

## ISSUE #284: Action Mapping (2 hours - DO THIS FIRST)

### Objectives
1. Find ALL action/handler mismatches systematically
2. Create ActionMapper class (or extend existing)
3. Integrate into IntentService routing
4. Log unmapped actions for future work
5. Test that `create_github_issue` now works

### Step-by-Step Implementation

**Step 1: Systematic Investigation** (30 min)
```bash
# Find all classifier action outputs
serena.find_referencing_symbols("intent.action")
grep -r "action=" services/intent_service/classifier.py

# Find all handler methods
serena.find_symbol(name_path="IntentService", include_body=true)
grep -r "async def.*handle_" services/ --include="*.py"

# Create exhaustive list of mismatches
# Document in investigation-action-mappings.md
```

**Evidence Required**:
- Complete list of all classifier actions found
- Complete list of all handler methods found
- Documented mismatches with line numbers

**Step 2: Create or Extend ActionMapper** (30 min)
```python
# services/intent_service/action_mapper.py
class ActionMapper:
    """
    Maps classifier action names to handler method names.

    Classifier outputs: snake_case with context
    Handlers expect: snake_case without redundant prefix

    Example:
      Classifier: "create_github_issue"
      Handler: "_handle_create_issue"
    """

    ACTION_MAPPING = {
        # Based on Step 1 investigation
        "create_github_issue": "create_issue",
        "list_github_issues": "list_issues",
        # ... ALL discovered mappings (must be 100%)
    }

    @classmethod
    def map_action(cls, classifier_action: str) -> str:
        """Map classifier action to handler method name."""
        mapped = cls.ACTION_MAPPING.get(classifier_action)

        if mapped:
            return mapped

        # Log unmapped for future work
        logger.warning(f"Unmapped action: {classifier_action}")

        # Try fallback: use action as-is
        return classifier_action

    @classmethod
    def get_unmapped_count(cls, all_actions: list[str]) -> int:
        """Return count of unmapped actions for metrics."""
        return sum(1 for a in all_actions if a not in cls.ACTION_MAPPING)
```

**Evidence Required**:
- File created: `cat services/intent_service/action_mapper.py`
- Mapping count: "ACTION_MAPPING contains X entries"
- Coverage metric: "X/Y actions mapped = Z%"

**Step 3: Integrate into IntentService** (45 min)
```python
# services/intent_service/intent_service.py

from .action_mapper import ActionMapper

class IntentService:
    async def route_action(self, intent: Intent, session_id: str, user_id: str):
        """Route intent to appropriate handler."""

        # NEW: Map classifier action to handler method
        mapped_action = ActionMapper.map_action(intent.action)

        # Get handler (with mapped name)
        handler_name = f"_handle_{mapped_action}"
        handler = getattr(self, handler_name, None)

        if not handler:
            # Friendly fallback (coordinates with Cursor's #283 work)
            logger.error(f"No handler for mapped action: {mapped_action} (original: {intent.action})")
            return self._handle_unknown_action(intent)

        return await handler(intent, session_id, user_id)
```

**Evidence Required**:
- Modified file: `git diff services/intent_service/intent_service.py`
- Integration point clear: Show exact lines changed

**Step 4: Test Known Failure Case** (15 min)
```bash
# Test the example from issue description
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "create a github issue for tracking this bug"}'

# Should now work (not "No handler" error)

# Also test via CLI
python main.py chat "create a github issue"
```

**Evidence Required**:
- Before: Screenshot/output showing "No handler" error
- After: Output showing action successfully mapped
- Test output proving it works

### #284 Acceptance Criteria Checklist
- [ ] All classifier actions discovered (used Serena)
- [ ] ActionMapper created with 100% of known actions
- [ ] Integrated into IntentService routing
- [ ] create_github_issue example working
- [ ] Unmapped actions logged (not errored)
- [ ] Tests show before/after behavior
- [ ] Changes committed with evidence

---

## ISSUE #285: Todo System (4-6 hours - DO THIS SECOND)

### Objectives
1. Verify existing infrastructure (repository, service, models)
2. Create web routes → TodoKnowledgeService
3. Add chat handlers → TodoKnowledgeService
4. Test full CRUD via API and chat
5. **DO NOT REBUILD** - wire existing services only

### Step-by-Step Implementation

**Step 1: Verify Existing Infrastructure** (30 min)
```bash
# Check what exists (75% pattern expected)
cat services/api/todo_management.py | head -100
cat services/todo/todo_knowledge_service.py | head -100
cat services/database/models.py | grep -A 30 "class Todo"

# Check existing tests
pytest tests/api/test_todo_management_api.py -v

# Document findings
ls -la services/todo/
ls -la services/api/todo_management.py
```

**Evidence Required**:
- Existing service methods documented
- Existing API models documented
- Test status (pass/fail counts)
- Actual completion %: "Found X/Y components = Z% complete"

**STOP Condition**: If <50% exists, escalate for new gameplan

**Step 2: Create Web Routes** (1-1.5h)
```python
# web/api/routes/todos.py (NEW FILE)
from fastapi import APIRouter, Depends, HTTPException
from web.middleware.auth import get_current_user
from services.api.todo_management import (
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoResponse,
    TodoListResponse,
)
from services.todo.todo_knowledge_service import TodoKnowledgeService

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])
service = TodoKnowledgeService()

@router.post("/", response_model=TodoResponse)
async def create_todo(
    request: TodoCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new todo for current user."""
    user_id = current_user["user_id"]
    todo = await service.create_todo(user_id, request)
    return TodoResponse.from_domain(todo)

@router.get("/", response_model=TodoListResponse)
async def list_todos(
    status: str = None,
    current_user: dict = Depends(get_current_user)
):
    """List user's todos, optionally filtered by status."""
    user_id = current_user["user_id"]
    todos = await service.list_todos(user_id, status=status)
    return TodoListResponse(todos=[TodoResponse.from_domain(t) for t in todos])

@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: str,
    request: TodoUpdateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update a todo (mark complete, change priority, etc)."""
    user_id = current_user["user_id"]
    todo = await service.update_todo(user_id, todo_id, request)
    if not todo:
        raise HTTPException(404, "Todo not found")
    return TodoResponse.from_domain(todo)

@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a todo."""
    user_id = current_user["user_id"]
    deleted = await service.delete_todo(user_id, todo_id)
    if not deleted:
        raise HTTPException(404, "Todo not found")
    return {"status": "deleted"}

# Mount in web/app.py
from web.api.routes import todos
app.include_router(todos.router)
```

**Evidence Required**:
- File created: `cat web/api/routes/todos.py`
- Routes mounted: `grep "todos" web/app.py`
- Server shows routes: `curl http://localhost:8001/openapi.json | jq '.paths | keys | .[] | select(contains("todo"))'`

**Step 3: Create Chat Handlers** (1.5-2h)
```python
# services/intent_service/todo_handlers.py (NEW FILE)
from services.todo.todo_knowledge_service import TodoKnowledgeService
from services.shared_types import Intent
import re

class TodoIntentHandlers:
    """
    Chat integration for todo operations.
    Wires natural language commands to TodoKnowledgeService.
    """

    def __init__(self):
        self.service = TodoKnowledgeService()

    async def handle_create_todo(self, intent: Intent, session_id: str, user_id: str) -> str:
        """
        Handle: "add todo: Review PR #285"
        Extract text, call service, format response.
        """
        text = self._extract_todo_text(intent.message)
        if not text:
            return "I didn't catch what you'd like me to add. Could you try: 'add todo: [description]'?"

        todo = await self.service.create_todo(user_id, text)
        return f"✓ Added: {todo.text} (id: {todo.id[:8]}...)"

    async def handle_list_todos(self, intent: Intent, session_id: str, user_id: str) -> str:
        """Handle: "show my todos" or "list todos"""
        status = self._extract_status_filter(intent.message)
        todos = await self.service.list_todos(user_id, status=status)

        if not todos:
            return "You don't have any todos yet. Try: 'add todo: [description]'"

        # Format for conversational display
        lines = [f"Your todos ({len(todos)}):"]
        for i, todo in enumerate(todos, 1):
            status_icon = "✓" if todo.completed else "○"
            lines.append(f"{i}. {status_icon} {todo.text}")

        return "\n".join(lines)

    async def handle_complete_todo(self, intent: Intent, session_id: str, user_id: str) -> str:
        """Handle: "mark todo 1 as complete" or "complete todo about PR"""
        todo_id = self._extract_todo_id(intent.message)
        if not todo_id:
            return "Which todo? Try: 'mark todo [id or keyword] as complete'"

        todo = await self.service.complete_todo(user_id, todo_id)
        if not todo:
            return "I couldn't find that todo. Try 'list todos' to see your current items."

        return f"✓ Completed: {todo.text}"

    async def handle_delete_todo(self, intent: Intent, session_id: str, user_id: str) -> str:
        """Handle: "delete todo 3" or "remove todo about meeting"""
        todo_id = self._extract_todo_id(intent.message)
        if not todo_id:
            return "Which todo should I remove? Try: 'delete todo [id or keyword]'"

        deleted = await self.service.delete_todo(user_id, todo_id)
        if not deleted:
            return "I couldn't find that todo. Try 'list todos' to see what's available."

        return "✓ Todo removed"

    def _extract_todo_text(self, message: str) -> str:
        """Extract todo text from 'add todo: TEXT' pattern."""
        match = re.search(r'add todo:?\s+(.+)', message, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def _extract_status_filter(self, message: str) -> str:
        """Extract status filter if present."""
        if 'complete' in message.lower():
            return 'completed'
        elif 'active' in message.lower() or 'pending' in message.lower():
            return 'active'
        return None

    def _extract_todo_id(self, message: str) -> str:
        """Extract todo ID from message (by number or keyword)."""
        # Try numeric ID first
        match = re.search(r'todo\s+(\d+)', message, re.IGNORECASE)
        if match:
            return match.group(1)

        # Try keyword match (simple version)
        match = re.search(r'todo\s+about\s+(.+)', message, re.IGNORECASE)
        if match:
            keyword = match.group(1).strip()
            # Service can search by keyword
            return f"keyword:{keyword}"

        return None

# Integration into IntentService
# services/intent_service/intent_service.py

from .todo_handlers import TodoIntentHandlers

class IntentService:
    def __init__(self):
        # ... existing init
        self.todo_handlers = TodoIntentHandlers()

    async def route_action(self, intent, session_id, user_id):
        # ... existing routing

        # Add todo routing
        if "todo" in intent.action.lower():
            return await self._route_todo_action(intent, session_id, user_id)

        # ... rest of routing

    async def _route_todo_action(self, intent, session_id, user_id):
        """Route todo-related actions."""
        action_map = {
            "create_todo": self.todo_handlers.handle_create_todo,
            "add_todo": self.todo_handlers.handle_create_todo,
            "list_todos": self.todo_handlers.handle_list_todos,
            "show_todos": self.todo_handlers.handle_list_todos,
            "complete_todo": self.todo_handlers.handle_complete_todo,
            "mark_complete": self.todo_handlers.handle_complete_todo,
            "delete_todo": self.todo_handlers.handle_delete_todo,
            "remove_todo": self.todo_handlers.handle_delete_todo,
        }

        handler = action_map.get(intent.action)
        if not handler:
            return f"I'm not sure how to help with that todo action. Try: add todo, list todos, complete todo, or delete todo."

        return await handler(intent, session_id, user_id)
```

**Evidence Required**:
- File created: `cat services/intent_service/todo_handlers.py`
- Integration point: `git diff services/intent_service/intent_service.py`
- All handler methods present: Show method enumeration table

**Step 4: Update Intent Classifier** (30 min)
```python
# Add todo patterns to classifier if not present
# Check existing patterns first:
grep -r "todo" services/intent_service/classifier.py

# If needed, add patterns:
TODO_PATTERNS = [
    r'add\s+todo',
    r'create\s+todo',
    r'list\s+todos',
    r'show\s+(my\s+)?todos',
    r'mark\s+todo.*complete',
    r'complete\s+todo',
    r'delete\s+todo',
    r'remove\s+todo',
]
```

**Evidence Required**:
- Pattern verification: Show existing or added patterns
- Classification test: Show classifier recognizing "add todo: test" correctly

**Step 5: End-to-End Testing** (1h)
```bash
# Test via API
TOKEN=$(curl -s -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"xian","password":"test123456"}' \
  | jq -r '.token')

# Create todo
curl -X POST http://localhost:8001/api/v1/todos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Review sprint progress"}'

# List todos
curl -X GET http://localhost:8001/api/v1/todos \
  -H "Authorization: Bearer $TOKEN"

# Test via chat
python main.py chat "add todo: Test the new todo system"
python main.py chat "show my todos"
python main.py chat "mark todo 1 as complete"
python main.py chat "delete todo 2"

# Run existing tests
pytest tests/api/test_todo_management_api.py -v

# Run new integration tests (if time)
pytest tests/integration/test_todo_workflows.py -v
```

**Evidence Required**:
- API tests: All curl commands with actual responses
- Chat tests: All CLI outputs showing responses
- Test suite: pytest output showing pass counts
- Manual verification: PM can test and confirm working

### #285 Acceptance Criteria Checklist
- [ ] Existing infrastructure verified and documented
- [ ] Web routes created and mounted
- [ ] All CRUD operations working via API
- [ ] Chat handlers created and integrated
- [ ] Intent classifier recognizes todo patterns
- [ ] End-to-end tests passing
- [ ] Manual testing successful
- [ ] Zero existing service code rebuilt
- [ ] Changes committed with evidence

---

## Multi-Agent Coordination

**You are working in parallel with Cursor Agent**:
- **Cursor**: #283 (Error Messages) - different files, no conflicts
- **You**: #284 + #285 - backend integration

**Coordination Points**:
- After #284 complete: Report to PM, check if Cursor needs anything
- After #285 backend: Check if Cursor starting documentation
- No direct dependencies, both can work simultaneously

**Share via GitHub**:
- Update issue descriptions with checkboxes as you progress
- Commit frequently with issue references
- Comment in issues if discoveries affect other agent's work

---

## STOP Conditions (17 Total)
Stop immediately and escalate if:
1. Infrastructure doesn't match gameplan (verify first!)
2. ActionMapper or similar already exists (extend it, don't rebuild)
3. Todo infrastructure <50% complete (gameplan assumes 75%)
4. Method implementation <100% complete (anti-80%)
5. Tests fail for any reason (report, don't decide if critical)
6. Can't provide verification evidence (no guessing)
7. User data at risk (todos are user data)
8. Server state unexpected (check what's running)
9. Existing patterns conflict with approach (find pattern first)
10. Git operations failing (show error, don't proceed)
11. Auth endpoints broken (dependency on Nov 1 work)
12. PM preferences in PIPER.user.md could be affected
13. Completion bias detected (claiming without proof)
14. Rationalizing gaps as "minor" (all gaps matter)
15. GitHub tracking not working (issue updates failing)
16. Performance degrades significantly (check before/after)
17. Discovery proves gameplan assumptions wrong

---

## When Tests Fail (CRITICAL)

**If ANY test fails**:
1. **STOP immediately** - Do NOT continue
2. **Do NOT decide** if failure is "critical"
3. **Report with evidence**:

```
⚠️ STOP - Tests Failing

Failing: [X] tests
Passing: [Y] tests

Exact errors:
[paste pytest output]

Root cause (if known):
[your diagnosis]

Options:
1. [fix approach]
2. [alternative approach]
3. [skip with PM approval]

Awaiting PM decision.
```

**PM decides what's critical, not you.**

---

## Success Metrics

**Issue #284** (Action Mapping):
- X/X actions mapped = 100%
- create_github_issue example working
- Zero "No handler" errors for known actions
- All unmapped actions logged

**Issue #285** (Todo System):
- 100% of existing service methods exposed
- CRUD working via both API and chat
- All tests passing (existing + new)
- Manual testing successful
- Zero existing code rebuilt

**Overall**:
- All evidence provided
- All git commits shown
- All acceptance criteria met
- PM can test and verify
- Ready for beta deployment

---

## Final Reminders

1. **Phase -1 Investigation FIRST** - Use Serena to find existing work
2. **75% Pattern Expected** - Extend, don't rebuild
3. **100% Completion Required** - X/X = 100% for all mappings/methods
4. **Evidence for Every Claim** - Show terminal output
5. **Stop on Test Failures** - Report, don't decide
6. **Reference piper-style-guide.md** - For any user-facing text
7. **Update Session Log** - Track progress throughout
8. **Coordinate with Cursor** - Update issues, share discoveries
9. **No Time Pressure** - Quality over speed (Time Lord principle)
10. **PM Approval Required** - Before claiming "complete"

---

**Ready to begin Phase -1 investigation. Report findings before implementing anything.**
