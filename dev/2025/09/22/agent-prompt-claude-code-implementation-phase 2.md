# Claude Code Agent Prompt: QueryRouter Implementation & Integration Testing

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You excel at broad implementation, integration testing, and end-to-end verification. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first:
- BRIEFING-CURRENT-STATE - Current epic and focus
- BRIEFING-ROLE-PROGRAMMER - Your role requirements
- BRIEFING-METHODOLOGY - Inchworm Protocol
- BRIEFING-PROJECT - What Piper Morgan is

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Implementation Readiness FIRST
**Before doing ANYTHING else, verify Phase 1 findings are accurate**:

```bash
# Verify Phase 1 investigation results:
# - QueryRouter exists and imports successfully
# - AsyncSessionFactory pattern exists in engine.py
# - Commented code is at expected lines (85-107)

# Verify reality:
python3 -c "from services.queries.query_router import QueryRouter; print('✓ QueryRouter imports')"
grep -n "AsyncSessionFactory" services/orchestration/engine.py
sed -n '85,107p' services/orchestration/engine.py | head -10
```

**If reality doesn't match Phase 1 findings**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

## Session Log Management
Continue existing log at: `dev/2025/09/22/2025-09-22-1204-claude-code-queryrouter-log.md`

## GitHub Progress Discipline (MANDATORY)

### Checkbox Updates Required
**You MUST update GitHub issue #185 DESCRIPTION (not comments) as you complete each task:**

```markdown
## Implementation Phase
- [x] Phase 1 findings verified (AsyncSessionFactory pattern confirmed)
- [x] QueryRouter initialization implemented (using async session pattern)
- [ ] Integration testing completed
- [ ] End-to-end GitHub issue creation tested
- [ ] All existing tests still pass
```

### Update Process:
1. **Complete an implementation step** with evidence
2. **Immediately update GitHub issue** with checkbox ✓
3. **Include technical evidence** in parentheses
4. **Use issue DESCRIPTION, never just comments**

**This maintains implementation accountability and progress visibility!**

## Mission
Implement QueryRouter re-enablement with comprehensive integration testing and end-to-end verification. Focus on broad testing across the codebase, integration validation, and ensuring the North Star test (GitHub issue creation) works perfectly.

**Scope Boundaries**:
- This prompt covers: Implementation oversight, integration testing, end-to-end validation
- NOT in scope: Surgical engine.py edits (that's Cursor's job)
- Cursor handles: Precise AsyncSession code implementation in engine.py

## Context
- **GitHub Issue**: #185 - CORE-GREAT-1A: QueryRouter Investigation & Fix
- **Current State**: Root cause identified - database session management issue
- **Target State**: QueryRouter enabled and working, GitHub issue creation functional
- **Phase 1 Complete**: Both agents confirmed AsyncSession pattern solution
- **Implementation Ready**: Straightforward fix using existing patterns

## Evidence Requirements

### For EVERY Claim You Make:
- **"QueryRouter initializes"** → Show startup log with no errors
- **"Integration tests pass"** → Show pytest output with specific test results
- **"GitHub issue creation works"** → Show end-to-end test with actual issue URL
- **"No regressions"** → Show full test suite results
- **"Performance targets met"** → Show timing evidence <500ms

### Completion Bias Prevention:
- **Never guess! Always verify first!**
- **NO "should work now"** - only "test results show"
- **NO "probably fixed"** - only "evidence demonstrates"
- **NO assumptions** - only verified outcomes

### Critical Anti-Pattern Prevention:
**NEVER disable functionality when encountering complexity!**
- **DO**: Report blockers with evidence and request guidance
- **DON'T**: Comment out code or add workarounds
- **DO**: Create GitHub issues for any unexpected complexity
- **DON'T**: Assume temporary fixes will be addressed later

## Constraints & Requirements

### For Claude Code (Implementation Oversight)
1. **Phase 1 verified**: Confirm investigation findings before proceeding
2. **Integration focus**: Test QueryRouter across entire orchestration flow
3. **End-to-end validation**: Ensure North Star test works (GitHub issue creation)
4. **Performance verification**: Confirm <500ms target is met
5. **Regression prevention**: Verify all existing functionality still works
6. **Report complexities**: Don't disable, seek guidance for unexpected issues
7. **Session log**: Continue existing queryrouter investigation log

## Multi-Agent Coordination

You are working alongside Cursor Agent who is implementing the surgical fix.

### Your Focus (Claude Code):
- **Implementation oversight** and coordination
- **Integration testing** across orchestration pipeline
- **End-to-end validation** of complete flow
- **Performance verification** and benchmarking
- **Regression testing** to ensure no breakage
- **Update GitHub issue** with implementation progress

### Cursor Agent's Focus:
- Surgical implementation in services/orchestration/engine.py
- Precise AsyncSession pattern implementation
- Constructor parameter fixes

### Coordination:
- Let Cursor implement the engine.py fix first
- Then proceed with integration testing
- Update GitHub issue #185 with test results
- Coordinate on any unexpected complexity

## Phase 0: Mandatory Verification

```bash
# 1. Verify Phase 1 findings
python3 -c "from services.queries.query_router import QueryRouter; print('✓ QueryRouter ready')"
grep -A 5 -B 5 "AsyncSessionFactory" services/orchestration/engine.py

# 2. Check current system state
ps aux | grep python
python main.py --version 2>/dev/null || echo "Check startup method"

# 3. Baseline test current functionality
PYTHONPATH=. python -m pytest tests/ -x --tb=short -q | head -10

# 4. Verify GitHub issue tracking
gh issue view 185
```

## Implementation Approach

### Step 1: Coordinate with Cursor Implementation
**Objective**: Ensure Cursor's engine.py fix is complete before testing
```bash
# Wait for Cursor to complete the surgical fix
# Verify the fix is in place
grep -A 10 "QueryRouter(" services/orchestration/engine.py

# Check if placeholder is removed
grep -n "self.query_router = None" services/orchestration/engine.py
```
**Evidence**: Confirmation that Cursor's implementation is complete
**Validation**: QueryRouter initialization code is uncommented and uses AsyncSession

### Step 2: Integration Testing
**Objective**: Test QueryRouter across the complete orchestration pipeline
```bash
# Test OrchestrationEngine initialization
python3 -c "
from services.orchestration.engine import OrchestrationEngine
engine = OrchestrationEngine()
print(f'QueryRouter initialized: {engine.query_router is not None}')
print(f'QueryRouter type: {type(engine.query_router)}')
"

# Test intent flow integration
PYTHONPATH=. python -c "
from services.intent_service.intent_classifier import IntentClassifier
from services.domain.models import Intent, IntentCategory
intent = Intent(
    action='create_github_issue',
    category=IntentCategory.GITHUB_OPERATION,
    confidence=0.95,
    context={'title': 'Test issue', 'body': 'Test body'}
)
print('Intent created successfully for testing')
"
```
**Evidence**: QueryRouter initializes without errors and integrates with intent system
**Validation**: No None objects, proper types, successful initialization

### Step 3: End-to-End North Star Test
**Objective**: Verify "Create GitHub issue about X" works completely
```bash
# Test the complete flow that was broken
# This is our North Star test from CORE-GREAT-1 acceptance criteria

# Method 1: Direct orchestration test
PYTHONPATH=. python -c "
import asyncio
from services.orchestration.engine import OrchestrationEngine
from services.domain.models import Intent, IntentCategory

async def test_github_creation():
    engine = OrchestrationEngine()
    intent = Intent(
        action='create_github_issue',
        category=IntentCategory.GITHUB_OPERATION,
        confidence=0.95,
        context={
            'title': 'CORE-GREAT-1A Test Issue',
            'body': 'This issue was created to test QueryRouter functionality',
            'labels': ['test', 'queryrouter']
        }
    )

    workflow = await engine.create_workflow_from_intent(intent)
    if workflow:
        result = await engine.execute_workflow(workflow)
        print(f'Workflow result: {result.status}')
        print(f'Execution time: {result.total_execution_time_seconds}s')
        return result.total_execution_time_seconds < 0.5
    return False

result = asyncio.run(test_github_creation())
print(f'North Star test passed: {result}')
"

# Method 2: CLI test if available
if [ -f "cli/commands/github.py" ]; then
    echo "Testing CLI GitHub creation..."
    PYTHONPATH=. python cli/commands/github.py create "CORE-GREAT-1A CLI Test Issue"
fi
```
**Evidence**: GitHub issue created successfully with timing <500ms
**Validation**: Complete orchestration flow works end-to-end

### Step 4: Regression Testing
**Objective**: Ensure existing functionality still works
```bash
# Run comprehensive test suite
PYTHONPATH=. python -m pytest tests/ -v --tb=short

# Test existing orchestration functionality
PYTHONPATH=. python -m pytest tests/test_orchestration.py -v

# Test intent classification still works
PYTHONPATH=. python -m pytest tests/test_intent_service.py -v

# Performance regression check
time PYTHONPATH=. python -c "
from services.orchestration.engine import OrchestrationEngine
import time
start = time.time()
engine = OrchestrationEngine()
end = time.time()
print(f'Engine initialization time: {(end-start)*1000:.1f}ms')
"
```
**Evidence**: All tests pass, no performance regression
**Validation**: Initialization time reasonable, no broken functionality

## Success Criteria (With Evidence)
- [ ] Phase 1 findings verified (AsyncSession pattern confirmed)
- [ ] Cursor implementation completed (engine.py fix in place)
- [ ] QueryRouter initializes successfully (no None objects)
- [ ] Integration tests pass (orchestration pipeline works)
- [ ] North Star test passes (GitHub issue creation <500ms)
- [ ] Regression tests pass (no existing functionality broken)
- [ ] Performance targets met (startup and execution timing)
- [ ] GitHub issue #185 updated with implementation evidence

## Deliverables
1. **Integration Test Results**: QueryRouter working in orchestration pipeline
2. **North Star Validation**: GitHub issue creation working end-to-end
3. **Regression Report**: All existing tests still passing
4. **Performance Metrics**: Timing evidence for all operations
5. **Implementation Evidence**: Terminal output showing success
6. **GitHub Update**: Issue #185 updated with implementation completion

## Cross-Validation Preparation
Coordinate with Cursor on:
- Implementation completion confirmation
- Any unexpected complexity discovered
- Test results and evidence sharing
- Performance impact assessment

## STOP Conditions
If ANY of these occur, STOP and escalate:
1. Phase 1 findings don't match current reality
2. Cursor's implementation causes errors or failures
3. Integration tests reveal architectural issues
4. Performance significantly degrades
5. Any temptation to disable or work around problems
6. North Star test fails after implementation

---

**Focus**: Integration testing, end-to-end validation, regression prevention
**Evidence**: Required for every implementation claim
**Coordination**: Support Cursor's implementation with comprehensive testing
**Goal**: Prove QueryRouter works completely in production-like conditions
**Anti-Pattern**: Never disable complexity - report and seek guidance
