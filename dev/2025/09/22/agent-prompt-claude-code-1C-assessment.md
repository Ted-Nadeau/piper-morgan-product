# Phase 0: CORE-GREAT-1C Testing & Locking Assessment

## Mission
Assess current test coverage for QueryRouter infrastructure and design regression prevention mechanisms to lock in GREAT-1A & 1B achievements. Focus on preventing the 75% pattern from recurring.

## Prerequisites
- GREAT-1A & 1B complete: QueryRouter enabled and integrated
- Chief Architect Decision: Testing/Locking/Documentation ONLY (NO QUERY processing)
- Goal: Lock QueryRouter against future accidental disabling

## GitHub Progress Tracking
**Update issue #188 checkboxes as you assess (PM will validate completion):**

```markdown
## Assessment Phase
- [ ] Current test coverage for orchestration analyzed
- [ ] Regression prevention points identified
- [ ] Performance baseline requirements mapped
- [ ] Lock mechanism designs proposed
- [ ] Documentation gap assessment completed
```

## Your Role: Test Coverage & Regression Prevention Design

### Step 1: Current Test Infrastructure Assessment
```bash
# Find existing orchestration/QueryRouter tests
find tests/ -name "*.py" | grep -E "(orchestrat|query|engine)"
find . -name "*test*.py" -exec grep -l "QueryRouter\|OrchestrationEngine" {} \;

# Check test patterns and coverage approach
ls -la tests/
PYTHONPATH=. python -m pytest tests/ --collect-only | grep -E "(orchestrat|query)" | head -10
```

### Step 2: Identify Critical Regression Points
```bash
# Find places where QueryRouter could be accidentally disabled again
grep -r "query_router.*None" services/ --include="*.py"
grep -r "get_query_router" services/orchestration/engine.py
grep -n "TODO.*QueryRouter" services/ --include="*.py"

# Check for patterns that enabled the 75% problem originally
grep -r "#.*QueryRouter" services/ --include="*.py"
grep -r "temporarily.*disabled" services/ --include="*.py"
```

### Step 3: Performance Baseline Establishment
```bash
# Test current QueryRouter initialization performance
time python3 -c "
import asyncio
from services.orchestration.engine import OrchestrationEngine

async def baseline_test():
    engine = OrchestrationEngine()
    query_router = await engine.get_query_router()
    return query_router is not None

result = asyncio.run(baseline_test())
print(f'QueryRouter baseline: {result}')
"

# Test handle_query_intent performance
time python3 -c "
import asyncio
from services.orchestration.engine import OrchestrationEngine
from services.domain.models import Intent, IntentCategory

async def performance_test():
    engine = OrchestrationEngine()
    intent = Intent(
        action='test_query',
        category=IntentCategory.QUERY,
        confidence=0.95,
        context={'test': True}
    )

    result = await engine.handle_query_intent(intent)
    return result is not None

result = asyncio.run(performance_test())
print(f'Query handling performance test: {result}')
"
```

### Step 4: Lock Mechanism Design
```bash
# Analyze what specific tests would prevent regression
grep -A 10 -B 5 "__init__" services/orchestration/engine.py
grep -A 5 "get_query_router" services/orchestration/engine.py

# Check existing test patterns to follow
find tests/ -name "*.py" -exec grep -l "assert.*not.*None" {} \; | head -5
```

## Evidence Required
- Complete test inventory with coverage gaps identified
- Specific regression prevention opportunities with line numbers
- Performance timing baselines for <500ms validation
- Lock mechanism specifications (test designs that prevent disabling)

## Test Categories to Design
**Initialization Lock**: Test fails if QueryRouter is None
**Method Lock**: Test fails if get_query_router method missing
**Performance Lock**: Test fails if operations exceed 500ms
**Integration Lock**: Test fails if handle_query_intent broken
**Import Lock**: Test fails if QueryRouter can't be imported

## Success Criteria
Comprehensive regression prevention strategy that makes QueryRouter disabling impossible without test failure.

## Scope Boundaries (Critical)
- Focus ONLY on QueryRouter/OrchestrationEngine infrastructure
- NO investigation of QUERY processing issues (separate CORE-QUERY epic)
- Lock existing working functionality, don't expand scope

## Coordination
Working with Cursor on documentation assessment and specific lock implementation requirements.

## GitHub Progress Tracking
**Update issue #188 checkboxes as you assess (PM will validate completion):**

```markdown
## Assessment Phase
- [ ] Current test coverage analyzed
- [ ] Regression prevention opportunities identified
- [ ] Documentation gaps mapped
- [ ] Performance baseline requirements defined
- [ ] Lock mechanism designs proposed
```

## Your Role: Test Coverage & Lock Design Assessment

### Step 1: Analyze Current Test Coverage
```bash
# Find existing tests for orchestration/QueryRouter
find tests/ -name "*.py" | grep -E "(orchestrat|query)" | head -10
find . -name "*test*.py" -exec grep -l "QueryRouter\|OrchestrationEngine" {} \;

# Check overall test coverage
PYTHONPATH=. python -m pytest tests/ --collect-only | head -20
```

### Step 2: Assess QueryRouter Testing Gaps
```bash
# Look for existing QueryRouter tests
grep -r "QueryRouter" tests/ --include="*.py"
grep -r "handle_query_intent" tests/ --include="*.py"
grep -r "get_query_router" tests/ --include="*.py"

# Check for orchestration integration tests
grep -r "orchestration" tests/ --include="*.py" | head -10
```

### Step 3: Identify Regression Prevention Points
```bash
# Find places where QueryRouter could be accidentally disabled
grep -r "query_router.*None" services/ --include="*.py"
grep -r "#.*QueryRouter" services/ --include="*.py"
grep -r "TODO.*QueryRouter" services/ --include="*.py"

# Check for initialization patterns that could break
grep -A 5 -B 5 "get_query_router" services/orchestration/engine.py
```

### Step 4: Performance Baseline Analysis
```bash
# Test current QueryRouter performance
time python3 -c "
import asyncio
from services.orchestration.engine import OrchestrationEngine

async def test_performance():
    engine = OrchestrationEngine()
    query_router = await engine.get_query_router()
    return query_router is not None

result = asyncio.run(test_performance())
print(f'QueryRouter initialization: {result}')
"
```

## Evidence Required
- Current test file inventory with coverage gaps
- Specific regression prevention opportunities
- Performance timing baselines
- Documentation audit results

## Test Scope Categories
**Unit tests**: QueryRouter initialization, method functionality
**Integration tests**: Orchestration pipeline end-to-end
**Performance tests**: <500ms initialization and operation
**Regression tests**: Prevent accidental disabling
**Lock tests**: Fail if QueryRouter becomes None

## Success: Comprehensive Test & Lock Strategy
Clear plan for preventing QueryRouter from ever being disabled again.

## Coordination
Working with Cursor on focused test implementation requirements.
