# Gameplan: CORE-INTENT-QUALITY Layer 4 Investigation
*Issue #179 - Intent responses generic or undefined*

## 🛑 INFRASTRUCTURE VERIFICATION CHECKPOINT (MANDATORY) 🛑

### Part A: Chief Architect's Current Understanding

Based on Lead Developer report and error patterns:

**Infrastructure Status**:
- [ ] Web framework: FastAPI on ports 8001/8081 (I think: VERIFIED)
- [ ] Orchestration service: Located at `services/orchestration/` (I think: EXISTS)
- [ ] Intent service: Located at `services/intent_service/` (I think: EXISTS)
- [ ] Error type: `'NoneType' object has no attribute 'create_workflow_from_intent'`
- [ ] Pattern: CONVERSATION intents work, EXECUTION/ANALYSIS/QUERY fail

**My understanding of the task**:
- Orchestration engine is returning None/null
- Intent classifier may work but orchestration layer fails
- Query actions like `show_standup` are unknown to the system

### Part B: PM Verification Required

**PM, please run these commands to verify**:

```bash
# 1. Check orchestration service initialization
grep -n "OrchestrationEngine" services/orchestration/engine.py | head -5
grep -n "__init__" services/orchestration/engine.py

# 2. Check for workflow factory patterns
grep -n "create_workflow_from_intent" services/orchestration/*.py

# 3. Look for query action definitions
grep -r "show_standup\|query_action" services/ --include="*.py"

# 4. Check if orchestration service is running
ps aux | grep -E "orchestration|engine" | grep -v grep

# 5. Find intent to workflow mapping
find services/ -name "*.json" -o -name "*.yaml" | xargs grep -l "intent\|workflow" 2>/dev/null
```

### Part C: Proceed/Revise Decision
- [ ] PROCEED if orchestration engine exists at expected location
- [ ] REVISE if architecture different than expected
- [ ] CLARIFY if workflow factory pattern not found

---

## Context
- **Issue**: #179 (child of #166)
- **Previous Fix**: Layer 3 proxy routing (#172) ✅ COMPLETE
- **Current Problem**: Layer 4 response quality - orchestration failures
- **Complexity**: Medium-High (null pointer suggests initialization issue)
- **Agents**: Claude Code + Cursor (multi-agent default)

## Phase 0: Investigation & Pattern Analysis (30 minutes)

### Investigation Focus: Orchestration Initialization

**Code Agent - Backend Investigation**:
```python
# 1. Trace orchestration engine initialization
# Check services/orchestration/engine.py
# Look for: __init__, setup, initialize methods
# Find: Where OrchestrationEngine gets created

# 2. Identify workflow factory registration
# Check workflow_factory.py
# Look for: register_workflow, add_handler patterns

# 3. Find intent→workflow mapping
# Check for configuration files
# Look in: config/, services/orchestration/
```

**Cursor Agent - Error Pattern Documentation**:
```javascript
// 1. Document all error responses
// Test different intent types:
// - "hello" (CONVERSATION) - works?
// - "show standup" (QUERY) - fails?
// - "analyze project" (ANALYSIS) - fails?
// - "create task" (EXECUTION) - fails?

// 2. Capture exact error messages
// Look for patterns in console/network responses
```

### Phase 0 Checkpoint (30 min) 🚦
- Code: Report orchestration initialization findings
- Cursor: Report error pattern matrix
- Both: Identify if it's initialization vs registration issue
- **Decision Gate**: Root cause identified? Continue. Unclear? Escalate.

### GitHub Bookending - Start
```bash
gh issue comment 179 --body "
## Investigation Starting
- [ ] Orchestration engine initialization check
- [ ] Workflow factory registration audit
- [ ] Intent→workflow mapping discovery
- [ ] Error pattern documentation

Started: $(date)
Agents: Code + Cursor
"
```

---

## Phase 1: Root Cause Diagnosis (45 minutes)

### Likely Causes to Investigate

**1. Orchestration Engine Not Initialized**
```python
# Check main.py or app.py for:
orchestration_engine = OrchestrationEngine()
# OR it might be None/never created
```

**2. Workflow Factory Missing Registrations**
```python
# Check for registration code like:
factory.register("show_standup", ShowStandupWorkflow)
factory.register("query", QueryWorkflow)
```

**3. Intent Category Mapping Broken**
```python
# Check for mapping like:
INTENT_TO_WORKFLOW = {
    IntentCategory.QUERY: QueryWorkflow,
    IntentCategory.EXECUTION: ExecutionWorkflow,
}
```

### Validation Tests
```bash
# Direct orchestration test (if possible)
curl -X POST http://localhost:8001/api/orchestrate \
  -d '{"intent": {"category": "QUERY", "action": "show_standup"}}' \
  -H "Content-Type: application/json"
```

### Phase 1 Checkpoint (45 min) 🚦
- Code: Root cause confirmed with code evidence
- Cursor: Reproduction steps documented
- Both: Agreement on fix approach
- **Decision Gate**: Clear fix? Proceed. Multiple issues? Prioritize.

---

## Phase 2: Implementation (60 minutes)

### Fix Patterns Based on Root Cause

**If Orchestration Not Initialized**:
```python
# In main.py or initialization:
from services.orchestration.engine import OrchestrationEngine

# Add initialization
orchestration_engine = OrchestrationEngine()
app.state.orchestration_engine = orchestration_engine
```

**If Workflow Registration Missing**:
```python
# In workflow_factory.py or initialization:
def register_workflows(factory):
    factory.register("show_standup", ShowStandupWorkflow)
    factory.register("analyze", AnalysisWorkflow)
    # etc.
```

**If Intent Mapping Broken**:
```python
# In orchestration/engine.py:
def create_workflow_from_intent(self, intent):
    if not self.workflow_factory:
        raise ValueError("Workflow factory not initialized")

    workflow_class = self.get_workflow_for_intent(intent)
    if not workflow_class:
        raise ValueError(f"No workflow for intent: {intent.category}")

    return workflow_class(intent)
```

### Implementation Requirements
- [ ] Fix initialization/registration issue
- [ ] Add error handling for None cases
- [ ] Add logging for debugging
- [ ] Create unit tests for the fix

### Phase 2 Checkpoint (60 min) 🚦
- Code: Fix implemented with tests
- Cursor: Ready to validate UI behavior
- Both: No regressions introduced
- **Decision Gate**: Tests pass? Continue. Failures? Debug.

---

## Phase 3: Validation & Testing (45 minutes)

### Comprehensive Testing Matrix

**Intent Categories to Test**:
```bash
# CONVERSATION (should work already)
curl -X POST http://localhost:8081/api/v1/intent \
  -d '{"message": "hello"}' \
  -H "Content-Type: application/json"

# QUERY (currently broken)
curl -X POST http://localhost:8081/api/v1/intent \
  -d '{"message": "show standup"}' \
  -H "Content-Type: application/json"

# EXECUTION (currently broken)
curl -X POST http://localhost:8081/api/v1/intent \
  -d '{"message": "create task: fix bugs"}' \
  -H "Content-Type: application/json"

# ANALYSIS (currently broken)
curl -X POST http://localhost:8081/api/v1/intent \
  -d '{"message": "analyze my project"}' \
  -H "Content-Type: application/json"
```

### Success Criteria
- [ ] All intent categories return appropriate responses
- [ ] No more "NoneType" errors
- [ ] No more "Unknown query action" errors
- [ ] Response quality contextually appropriate
- [ ] Performance still <100ms

### Evidence Collection
- Terminal output showing successful responses
- Browser screenshots of working UI
- Test results showing all categories work
- Performance metrics for each category

---

## Phase Z: Bookending & Documentation (30 minutes)

### GitHub Closure
```bash
gh issue comment 179 --body "
## Resolution Complete ✅

### Root Cause
[Specify: initialization/registration/mapping]

### Fix Applied
[Code changes with file:line references]

### Validation Results
- CONVERSATION: ✅ Working
- QUERY: ✅ Fixed (show_standup works)
- EXECUTION: ✅ Fixed (task creation works)
- ANALYSIS: ✅ Fixed (analysis works)

### Performance
[Metrics for each category]

### Next Steps
Ready for comprehensive intent pattern review
"

gh issue close 179 --comment "Layer 4 orchestration issue resolved"
```

### Git Discipline
```bash
git add -A
git commit -m "fix(orchestration): Initialize engine and register query workflows

- Fixed OrchestrationEngine null initialization
- Added workflow registration for QUERY/EXECUTION/ANALYSIS
- Added error handling for missing workflows
- All intent categories now properly handled

Fixes #179, Related to #166"

git log --oneline -1
git push origin main
```

### Documentation Updates
- [ ] Update ADR if new pattern discovered
- [ ] Document workflow registration pattern
- [ ] Update domain-models.md if relevant
- [ ] Create orchestration-guide.md if needed

---

## STOP Conditions
1. ❌ Orchestration service doesn't exist where expected
2. ❌ Workflow factory pattern completely different
3. ❌ Multiple initialization points conflicting
4. ❌ Database dependencies discovered
5. ❌ Authentication layer interfering
6. ❌ Tests revealing deeper issues
7. ❌ Performance degradation with fix
8. ❌ Configuration files missing
9. ❌ Circular dependencies found
10. ❌ Memory leaks detected

---

## Time Estimate
- Phase 0: 30 minutes (investigation)
- Phase 1: 45 minutes (diagnosis)
- Phase 2: 60 minutes (implementation)
- Phase 3: 45 minutes (validation)
- Phase Z: 30 minutes (bookending)
- **Total**: ~3.5 hours

---

## Notes for Agents

### Known Context
- CONVERSATION intents work (basic responses)
- QUERY/EXECUTION/ANALYSIS fail at orchestration
- Error: 'NoneType' suggests initialization issue
- Previous Layer 3 proxy fix successful

### Investigation Priority
1. Check initialization first (most likely)
2. Then registration/mapping
3. Finally configuration

### Cross-Agent Coordination
- Code focuses on backend initialization
- Cursor documents UI error patterns
- Both validate the fix works end-to-end

---

*Gameplan Version: 1.0*
*Issue: #179 CORE-INTENT-QUALITY*
*Created: September 17, 2025*
*Priority: High - Blocking all non-conversation intents*
