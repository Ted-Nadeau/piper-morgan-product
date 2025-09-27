# Phase 1: CORE-GREAT-1B Integration Implementation & Testing

## Mission
Coordinate implementation of the three identified connection points and validate end-to-end orchestration pipeline works. Focus on integration testing and Bug #166 resolution verification.

## Prerequisites
- Phase 0 complete: Integration gaps identified with exact line numbers
- Ready: 3 surgical fixes needed in web/app.py and engine.py
- Goal: End-to-end Intent → QueryRouter → Response flow working

## GitHub Progress Tracking
**Update issue #186 checkboxes as you validate (PM will validate completion):**

```markdown
## Implementation Phase
- [ ] Cursor's QueryRouter integration completed
- [ ] OrchestrationEngine bridge method verified
- [ ] Bug #166 timeout fix validated
- [ ] Integration testing passed
- [ ] End-to-end flow demonstrated
```

## Your Role: Implementation Validation & Integration Testing

### Step 1: Verify Cursor's Implementation
```bash
# Check QueryRouter integration in web/app.py
grep -n -A 5 -B 5 "query_router" web/app.py

# Verify handle_query_intent method exists
grep -n -A 10 "handle_query_intent" services/orchestration/engine.py

# Check Bug #166 timeout fix
grep -n -A 5 "asyncio.wait_for\|timeout" web/app.py
```

### Step 2: Integration Testing
```bash
# Test QUERY intent handling
python3 -c "
import asyncio
from services.orchestration.engine import OrchestrationEngine
from services.domain.models import Intent, IntentCategory

async def test_query_integration():
    engine = OrchestrationEngine()
    intent = Intent(
        action='search_projects',
        category=IntentCategory.QUERY,
        confidence=0.95,
        context={'query': 'Find all Python projects'}
    )

    # Test new handle_query_intent method
    if hasattr(engine, 'handle_query_intent'):
        result = await engine.handle_query_intent(intent)
        print(f'Query handled: {result is not None}')
        return True
    else:
        print('handle_query_intent method missing')
        return False

success = asyncio.run(test_query_integration())
print(f'Integration test: {success}')
"
```

### Step 3: End-to-End Flow Test
```bash
# Test complete orchestration pipeline
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find all projects related to machine learning",
    "context": {"user_id": "test"}
  }' | python -m json.tool
```

### Step 4: Bug #166 Concurrent Request Test
```bash
# Test multiple concurrent requests don't hang
for i in {1..3}; do
  curl -X POST http://localhost:8001/api/v1/intent \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Test concurrent request $i\"}" &
done
wait
echo "All concurrent requests completed"
```

## Evidence Required
- QueryRouter integration confirmed working
- handle_query_intent method tested successfully
- Timeout prevention verified for Bug #166
- End-to-end flow demonstration

## Test Scope Specification
**Unit tests**: Individual method functionality
**Integration tests**: Component interaction verification
**Concurrency tests**: Bug #166 resolution validation

## Success Criteria
Complete Intent → OrchestrationEngine → QueryRouter → Response pipeline working without UI hangs.

## Coordination
Validate Cursor's surgical implementations and provide integration test results.
