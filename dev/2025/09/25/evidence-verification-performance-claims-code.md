# Agent Prompt: Evidence Verification - Performance Measurement Claims

**Agent**: Code
**Mission**: Provide actual terminal output evidence for all performance claims made in Phase 1A, with specific focus on what was actually measured.

## Critical Verification Required

### PM's Evidence Challenge
**Inconsistency identified**: Yesterday's 2041ms LLM calls vs today's 0.1ms QueryRouter claims
**Concern**: "0.1ms sounds like a mock and not a real LLM round trip to me"
**Standard**: Hard evidence with terminal output, not assertions

## Specific Evidence Requirements

### 1. Show Actual Test Execution
```bash
# Provide the EXACT terminal output from your Phase 1A measurements
echo "=== ACTUAL TERMINAL OUTPUT FROM PHASE 1A ==="
echo "Providing complete, unedited terminal output from performance measurements:"

# Re-run the exact QueryRouter measurement that produced 0.1ms claim
PYTHONPATH=. python3 -c "
import asyncio
import time
from services.orchestration.engine import OrchestrationEngine
from database.session import get_async_session

async def show_actual_measurement():
    print('=== DETAILED QueryRouter MEASUREMENT ===')

    for i in range(3):
        print(f'\\n--- Run {i+1} ---')

        async with get_async_session() as session:
            print('Starting timer...')
            start = time.time()

            print('Creating OrchestrationEngine...')
            engine = OrchestrationEngine(session)

            print('Checking if QueryRouter exists...')
            if hasattr(engine, 'query_router'):
                print(f'QueryRouter found: {type(engine.query_router)}')
            else:
                print('No query_router attribute found')

            end = time.time()
            duration_ms = (end - start) * 1000

            print(f'Total time for object creation: {duration_ms:.3f}ms')
            print(f'This measures: Object instantiation ONLY')
            print(f'This does NOT measure: Actual query processing')

    print('\\n=== WHAT THIS MEASUREMENT ACTUALLY REPRESENTS ===')
    print('✅ Measures: Python object creation')
    print('✅ Measures: Database session setup')
    print('❌ Does NOT measure: LLM API calls')
    print('❌ Does NOT measure: Actual query processing')
    print('❌ Does NOT measure: QueryRouter.route() execution')

asyncio.run(show_actual_measurement())
"
```

### 2. Test Actual Query Processing Performance
```bash
# Now measure what we ACTUALLY care about - query processing with LLM
echo ""
echo "=== ACTUAL QUERY PROCESSING MEASUREMENT ==="
PYTHONPATH=. python3 -c "
import asyncio
import time
from services.orchestration.engine import OrchestrationEngine
from database.session import get_async_session

async def measure_real_query_processing():
    print('=== REAL QUERY PROCESSING TEST ===')

    async with get_async_session() as session:
        engine = OrchestrationEngine(session)
        test_query = 'Create a GitHub issue about performance testing'

        print(f'Testing with query: \"{test_query}\"')
        print('This should involve LLM classification + routing...')

        try:
            start = time.time()
            result = await engine.process_request(test_query)
            end = time.time()

            duration_ms = (end - start) * 1000
            print(f'\\nACTUAL query processing time: {duration_ms:.0f}ms')
            print(f'Result type: {type(result)}')
            print('This INCLUDES: LLM classification, routing, processing')

        except Exception as e:
            print(f'Query processing FAILED: {e}')
            print('This means we cannot measure actual performance!')

asyncio.run(measure_real_query_processing())
"
```

### 3. Compare with Yesterday's LLM Classification
```bash
# Test LLM classification directly to compare with yesterday's findings
echo ""
echo "=== LLM CLASSIFICATION COMPARISON WITH YESTERDAY ==="
PYTHONPATH=. python3 -c "
import asyncio
import time
from services.intent_service.llm_classifier import LLMClassifier

async def verify_llm_performance():
    print('=== LLM CLASSIFICATION VERIFICATION ===')
    print('Comparing with yesterday\\'s 2041ms finding...')

    classifier = LLMClassifier()
    test_message = 'Create a GitHub issue about the login bug'

    for i in range(3):
        try:
            print(f'\\n--- LLM Test {i+1} ---')
            start = time.time()
            result = await classifier.classify(test_message)
            end = time.time()

            duration_ms = (end - start) * 1000
            print(f'LLM classification time: {duration_ms:.0f}ms')
            print(f'Result: {result.category if hasattr(result, \"category\") else \"N/A\"}')

            if duration_ms > 2000:
                print('✅ CONSISTENT with yesterday\\'s 2041ms finding')
            else:
                print('❌ INCONSISTENT - much faster than yesterday')

        except Exception as e:
            print(f'LLM classification FAILED: {e}')
            print('This could explain performance discrepancies')

    print('\\n=== REALITY CHECK ===')
    print('Yesterday: Real LLM API calls took 2041ms average')
    print('Question: Are we using real API calls or mocks today?')

asyncio.run(verify_llm_performance())
"
```

### 4. Identify What Was Actually Measured
```bash
# Clarify exactly what the 0.1ms, 2538ms, and 37ms measurements represent
echo ""
echo "=== MEASUREMENT CLARITY VERIFICATION ==="

echo "Phase 1A claimed measurements:"
echo "- QueryRouter Init: 0.1ms average"
echo "- LLM Classification: 2538ms average"
echo "- Orchestration Flow: 37ms average"
echo ""
echo "Evidence required for each:"

echo ""
echo "1. QueryRouter Init (claimed 0.1ms):"
echo "   - What exactly was timed?"
echo "   - Was this object creation or actual routing?"
echo "   - Terminal output showing measurement method?"

echo ""
echo "2. LLM Classification (claimed 2538ms):"
echo "   - Is this consistent with yesterday's 2041ms?"
echo "   - Using real API calls or mocks?"
echo "   - Terminal output showing actual API calls?"

echo ""
echo "3. Orchestration Flow (claimed 37ms):"
echo "   - How is this faster than LLM classification?"
echo "   - What components were included/excluded?"
echo "   - Does this include the 2538ms LLM call?"

echo ""
echo "LOGICAL CONSISTENCY CHECK:"
echo "If Orchestration Flow includes LLM Classification,"
echo "then Flow time should be >= LLM time"
echo "Current claim: 37ms flow includes 2538ms LLM call"
echo "This is MATHEMATICALLY IMPOSSIBLE"
```

## Evidence Collection Requirements

### Terminal Output Evidence
```
=== REQUIRED EVIDENCE ===
1. Complete terminal output from Phase 1A measurements
2. Exact commands and scripts executed
3. Clear identification of what each measurement represents
4. Logical consistency verification between measurements

Mathematical Consistency Check:
- LLM Classification: [X]ms
- Orchestration Flow: [X]ms
- Logic: Flow >= LLM if Flow includes LLM
- Current claim consistency: [PASS/FAIL]
```

### Measurement Method Verification
```
=== MEASUREMENT METHOD EVIDENCE ===
QueryRouter Init (0.1ms claim):
- Actual measurement: [object creation / routing execution]
- Terminal output: [paste actual output]
- Includes LLM calls: [YES/NO]

LLM Classification (2538ms claim):
- API calls: [REAL/MOCK]
- Consistency with yesterday: [CONSISTENT/INCONSISTENT]
- Terminal output: [paste actual output]

Orchestration Flow (37ms claim):
- Components included: [list what was measured]
- Relationship to LLM time: [explain how flow < LLM time]
- Terminal output: [paste actual output]
```

### Reality Check Assessment
```
=== REALITY CHECK RESULTS ===
Performance claims vs yesterday's findings:
- Yesterday: 2041ms LLM classification
- Today: 2538ms LLM classification
- Consistency: [CONSISTENT/INCONSISTENT]

Logic verification:
- Can orchestration flow (37ms) include LLM classification (2538ms): [IMPOSSIBLE/POSSIBLE]
- Explanation for discrepancy: [required]

Mock vs Real API verification:
- Evidence of real API calls: [YES/NO with proof]
- Mock detection indicators: [list any found]
```

## Success Criteria
- [ ] Complete terminal output from Phase 1A measurements provided
- [ ] Clear identification of what each measurement actually represents
- [ ] Mathematical consistency between measurements verified
- [ ] Comparison with yesterday's findings explained
- [ ] Mock vs real API usage definitively determined
- [ ] Any discrepancies explained with evidence

## Time Estimate
15-20 minutes for complete evidence verification

## Critical Requirements
**Terminal output**: Actual command execution output, not summaries
**Mathematical consistency**: Explain how flow time relates to component times
**Yesterday comparison**: Reconcile with 2041ms LLM findings
**Mock detection**: Verify real API calls vs mock usage

**Focus: Provide hard evidence that PM can verify, not assertions or claims**
