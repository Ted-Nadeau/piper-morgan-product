# Prompt for Code Agent: GREAT-4C Phase -1 Investigation

## Context

GREAT-4C gameplan assumed 219 handlers exist. Discovery found only 5 handlers in canonical_handlers.py:
- `_handle_identity_query`
- `_handle_temporal_query`
- `_handle_status_query`
- `_handle_priority_query`
- `_handle_guidance_query`

Meanwhile, GREAT-4A established 44 intent patterns that classify actions like:
- `create_issue` (CREATE category)
- `update_status` (UPDATE category)
- `search_docs` (SEARCH category)

**Critical Gap**: Test showed `create_issue` classifies correctly but has no handler.

## Mission

Investigate the intent classification → handler routing system to determine:
1. How does a classified intent get routed to a handler?
2. Where are CREATE/UPDATE/SEARCH actions handled (if anywhere)?
3. What happens when no handler exists for an action?
4. Is handler coverage complete or are there gaps?

## Investigation Steps

### Step 1: Find the Routing Logic

Search for where classified intents get dispatched to handlers:

```bash
# Look for the orchestration/routing code
grep -r "canonical_handlers\|CanonicalHandlers" services/intent_service/ --include="*.py" -A 5

# Find where Intent objects are processed
grep -r "def execute\|def process\|def handle" services/intent_service/ --include="*.py" -A 10

# Look for handler registry or mapping
grep -r "handler.*map\|_handlers\|HANDLERS" services/intent_service/ --include="*.py"
```

### Step 2: Trace a Classification End-to-End

```bash
# Start from the API endpoint
grep -r "/api/v1/intent" web/ --include="*.py" -A 20

# Or from Slack integration
grep -r "classify.*message\|intent.*classify" services/integrations/slack/ --include="*.py" | head -20
```

### Step 3: Check for Additional Handler Files

```bash
# Are there other handler files besides canonical_handlers.py?
find services/intent_service -name "*handler*" -type f

# Check for action handlers
find services -name "*action*" -type f | grep -v __pycache__

# Look for execute/process modules
find services -name "*execute*" -o -name "*process*" | grep -v __pycache__
```

### Step 4: Test What Actually Happens

Create test script: `dev/2025/10/05/test_unhandled_intent.py`

```python
"""Test what happens with unhandled intent actions."""
import asyncio
from services.intent_service import classifier

async def test_routing():
    """Test intents that should have no handler."""

    test_cases = [
        ("create an issue about login", "Should have CREATE handler?"),
        ("update the status of issue 123", "Should have UPDATE handler?"),
        ("search for architecture docs", "Should have SEARCH handler?"),
        ("what day is it", "HAS handler - temporal"),
    ]

    for text, expected in test_cases:
        print(f"\nTest: {text}")
        print(f"Expected: {expected}")

        try:
            result = await classifier.classify(text)
            print(f"Category: {result.category}")
            print(f"Action: {result.action}")
            print(f"Confidence: {result.confidence}")

            # Does it execute?
            # Look for execute/process method
            if hasattr(result, 'execute'):
                exec_result = await result.execute()
                print(f"Execution: {exec_result}")
            else:
                print("No execute method found")

        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_routing())
```

Run it:
```bash
python3 dev/2025/10/05/test_unhandled_intent.py
```

### Step 5: Document Handler Registry

Create: `dev/2025/10/05/handler-coverage-analysis.md`

```markdown
# Handler Coverage Analysis

## Classified Intent Categories (from GREAT-4A)
- TEMPORAL: 17 patterns → ✅ `_handle_temporal_query`
- STATUS: 14 patterns → ✅ `_handle_status_query`
- PRIORITY: 13 patterns → ✅ `_handle_priority_query`
- IDENTITY: patterns → ✅ `_handle_identity_query`
- GUIDANCE: patterns → ✅ `_handle_guidance_query`
- CREATE: patterns → ❌ NO HANDLER
- UPDATE: patterns → ❌ NO HANDLER
- SEARCH: patterns → ❌ NO HANDLER

## Routing Mechanism
[Document how intents → handlers based on investigation]

## Gaps Found
[List unhandled actions/categories]

## Recommendations
[Should GREAT-4C add missing handlers? Or are they handled elsewhere?]
```

---

## Expected Findings

**Scenario A: Handlers Exist Elsewhere**
- CREATE/UPDATE/SEARCH handled by different services
- canonical_handlers.py is just for query-type intents
- Routing logic dispatches to appropriate service

**Scenario B: Genuine Gaps**
- Only 5 categories have handlers
- CREATE/UPDATE/SEARCH fall through to errors/defaults
- GREAT-4C should add missing handlers

**Scenario C: Different Architecture**
- Handlers aren't needed - intents route directly to services
- canonical_handlers.py is legacy or specialized
- Current architecture doesn't match assumptions

---

## Deliverables

- [ ] Routing logic documented
- [ ] Handler coverage mapped
- [ ] Test script run with results
- [ ] Handler coverage analysis created
- [ ] Recommendation for GREAT-4C scope

---

**Session Log**: `dev/2025/10/05/2025-10-05-1540-prog-code-log.md`

**Effort**: Small (investigation only, no implementation)

**Time Estimate**: 20-30 minutes

---

## Success Criteria

You should be able to answer:
1. How does `create_issue` intent get handled (or not)?
2. Are there 5 handlers or more (just not in canonical_handlers.py)?
3. What should GREAT-4C actually focus on?

Report findings back to Lead Developer for Chief Architect consultation.
