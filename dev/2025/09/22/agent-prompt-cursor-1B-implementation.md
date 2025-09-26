# Phase 1: CORE-GREAT-1B Surgical Connection Implementation

## Mission
Make precise surgical fixes to implement the three identified connection points: QueryRouter integration, OrchestrationEngine bridge method, and Bug #166 timeout fix.

## Prerequisites
- Phase 0 complete: Exact integration requirements identified
- Target: 3 specific connection points with exact line numbers
- Goal: Connect Intent detection to QueryRouter execution

## GitHub Progress Tracking
**Update issue #186 checkboxes as you implement (PM will validate completion):**

```markdown
## Surgical Implementation
- [ ] QueryRouter integration added (web/app.py lines 662-670)
- [ ] handle_query_intent method implemented (engine.py)
- [ ] Bug #166 timeout fix applied (web/app.py line 658)
- [ ] Local testing verified
- [ ] Import verification passed
```

## Your Role: Surgical Implementation

### Step 1: Backup and Verify Current State
```bash
# Create backups
cp web/app.py web/app.py.backup.$(date +%Y%m%d-%H%M)
cp services/orchestration/engine.py services/orchestration/engine.py.backup.$(date +%Y%m%d-%H%M)

# Verify current state matches Phase 0 findings
sed -n '662,670p' web/app.py
sed -n '97p' services/orchestration/engine.py
sed -n '658p' web/app.py
```

### Step 2: Implement QueryRouter Integration (web/app.py)
**Target: Lines 662-670**

Replace QUERY intent detection with QueryRouter execution:

**Current (broken):**
```python
if intent.category.value == "QUERY":
    print(f"🔍 Processing QUERY intent: {intent.action}")
    # ❌ QueryRouter never called
```

**Implement:**
```python
if intent.category.value == "QUERY":
    print(f"🔍 Processing QUERY intent: {intent.action}")
    result = await orchestration_engine.handle_query_intent(intent)
    return {"status": "success", "result": result}
```

### Step 3: Add OrchestrationEngine Bridge Method
**Target: services/orchestration/engine.py**

Add after line 97 (after get_query_router method):

```python
async def handle_query_intent(self, intent: Intent) -> dict:
    """Handle QUERY intents using QueryRouter"""
    query_router = await self.get_query_router()
    return await query_router.route_query(intent)
```

### Step 4: Fix Bug #166 (web/app.py line 658)
**Current (blocking):**
```python
workflow = await orchestration_engine.create_workflow_from_intent(intent)
```

**Implement (with timeout):**
```python
workflow = await asyncio.wait_for(
    orchestration_engine.create_workflow_from_intent(intent),
    timeout=30.0
)
```

Add asyncio import if needed:
```python
import asyncio
```

### Step 5: Local Verification
```bash
# Test imports work
python3 -c "
from web.app import app
from services.orchestration.engine import OrchestrationEngine
print('✓ Imports successful')
"

# Verify method exists
python3 -c "
from services.orchestration.engine import OrchestrationEngine
engine = OrchestrationEngine()
print(f'handle_query_intent exists: {hasattr(engine, \"handle_query_intent\")}')
"
```

## Evidence Required
- Before/after code with exact line numbers
- Successful import verification
- Method existence confirmation
- Backup file creation

## Success Criteria
Three surgical fixes implemented using exact specifications from Phase 0 investigation.

## Coordination
Complete implementation first, then Code will validate integration testing.
