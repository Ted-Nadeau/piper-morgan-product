# Phase 2: QueryRouter Integration Testing & Validation

## Mission
Re-enable QueryRouter and validate it works end-to-end. Focus on integration testing, performance verification, and ensuring the North Star test (GitHub issue creation) passes.

## Prerequisites 
- Phase 1 complete: Root cause identified (database session management)
- Solution confirmed: Use AsyncSessionFactory pattern from engine.py lines 135-138
- Ready for implementation with Cursor handling surgical fix

## GitHub Progress Tracking
**Update issue #185 checkboxes as you complete each step:**

```markdown
## Phase 2: Implementation & Testing
- [ ] Cursor surgical fix completed
- [ ] QueryRouter initialization verified  
- [ ] Integration testing passed
- [ ] North Star test passed (GitHub issue creation <500ms)
- [ ] Regression testing completed
- [ ] Performance targets met
```

## Your Role: Integration Testing & Validation

**Cursor implements** → **You validate**

### Step 1: Verify Cursor's Implementation
```bash
# Confirm QueryRouter is no longer None
python3 -c "
from services.orchestration.engine import OrchestrationEngine
engine = OrchestrationEngine()
print(f'QueryRouter initialized: {engine.query_router is not None}')
print(f'Type: {type(engine.query_router)}')
"
```

### Step 2: Integration Testing
```bash
# Test orchestration pipeline works
PYTHONPATH=. python -c "
import asyncio
from services.orchestration.engine import OrchestrationEngine
from services.domain.models import Intent, IntentCategory

async def test_integration():
    engine = OrchestrationEngine()
    intent = Intent(
        action='create_github_issue',
        category=IntentCategory.GITHUB_OPERATION,
        confidence=0.95,
        context={'title': 'Test', 'body': 'Test body'}
    )
    workflow = await engine.create_workflow_from_intent(intent)
    return workflow is not None

result = asyncio.run(test_integration())
print(f'Integration test: {result}')
"
```

### Step 3: North Star Test (GitHub Issue Creation)
```bash
# The key test from CORE-GREAT-1 acceptance criteria
PYTHONPATH=. python -c "
import asyncio
import time
from services.orchestration.engine import OrchestrationEngine
from services.domain.models import Intent, IntentCategory

async def north_star_test():
    start_time = time.time()
    engine = OrchestrationEngine()
    
    intent = Intent(
        action='create_github_issue',
        category=IntentCategory.GITHUB_OPERATION,
        confidence=0.95,
        context={
            'title': 'CORE-GREAT-1A Success Test',
            'body': 'QueryRouter is working!',
            'labels': ['queryrouter', 'success']
        }
    )
    
    workflow = await engine.create_workflow_from_intent(intent)
    if workflow:
        result = await engine.execute_workflow(workflow)
        execution_time = time.time() - start_time
        print(f'Status: {result.status}')
        print(f'Time: {execution_time:.3f}s (target: <0.5s)')
        return execution_time < 0.5 and result.status.name == 'COMPLETED'
    return False

success = asyncio.run(north_star_test())
print(f'North Star test passed: {success}')
"
```

### Step 4: Regression Testing
```bash
# Ensure nothing broke
PYTHONPATH=. python -m pytest tests/ -x --tb=short
```

## Evidence Required
- Terminal output showing QueryRouter initialization
- Integration test results
- North Star test timing and success
- Full test suite results

## Success: North Star Working
When "Create GitHub issue about X" works end-to-end in <500ms, CORE-GREAT-1A is complete.

## Coordination
Work with Cursor on any issues. Report complexity immediately - never disable functionality.

