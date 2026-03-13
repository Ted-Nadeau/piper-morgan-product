# Gameplan: Issue #286 - CONVERSATION Handler Architecture Fix

**Date**: November 6, 2025
**Issue**: #286 - CORE-ALPHA-CONVERSATION-PLACEMENT
**Priority**: P2 - Important (Architecture)
**Estimated Effort**: 2 hours
**Agent**: Code (systematic refactor)

---

## Context

The CONVERSATION handler is architecturally misplaced in IntentService. It's currently at line 199 (after orchestration check) but should be with other canonical handlers at lines 123-136.

**Current Problem**:
- Handler in wrong section of code
- Uses string comparison instead of enum
- Breaks architectural pattern

---

## Phase -1: Verification (15 minutes)

### Verify Current State

```bash
# Check current handler location
grep -n "conversation" services/intent_service/intent_service.py | head -10

# Verify canonical handler section
sed -n '123,136p' services/intent_service/intent_service.py

# Check line 199 area
sed -n '195,205p' services/intent_service/intent_service.py
```

### Expected Findings
- Line 199: `if intent.category.value == "conversation":`
- Lines 123-136: Other canonical handlers (GREETING, QUERY, etc.)
- Inconsistent comparison pattern (string vs enum)

### STOP if
- Handler already moved
- Different line numbers (update accordingly)
- Major architectural changes detected

---

## Phase 0: Setup (10 minutes)

### Create Issue Branch

```bash
git checkout main
git pull
git checkout -b fix/286-conversation-handler-placement
```

### Run Baseline Tests

```bash
# Ensure tests pass before changes
pytest tests/intent_service/ -v -k "conversation"
pytest tests/integration/ -v -k "conversation"

# Save baseline
pytest tests/ --json-report --json-report-file=baseline-286.json
```

---

## Phase 1: Move Handler (30 minutes)

### Step 1: Copy Handler Method

First, understand what we're moving:
```python
# Current (around line 199)
if intent.category.value == "conversation":
    return await self._handle_conversation_intent(intent, session_id)
```

### Step 2: Add to Canonical Section

```python
# services/intent_service/intent_service.py
# Around lines 123-136, add with other handlers:

if intent.category == IntentCategory.GREETING:
    return await self._handle_greeting_intent(intent, session_id)

if intent.category == IntentCategory.QUERY:
    return await self._handle_query_intent(intent, session_id)

# ADD HERE:
if intent.category == IntentCategory.CONVERSATION:
    return await self._handle_conversation_intent(intent, session_id)

if intent.category == IntentCategory.ANALYSIS:
    return await self._handle_analysis_intent(intent, session_id)
```

### Step 3: Remove Old Location

```python
# Remove from line 199
# DELETE these lines:
if intent.category.value == "conversation":
    return await self._handle_conversation_intent(intent, session_id)
```

### Step 4: Fix Enum Usage

Ensure using enum comparison (not string):
```python
# Correct:
if intent.category == IntentCategory.CONVERSATION:

# Wrong:
if intent.category.value == "conversation":
```

---

## Phase 2: Test Impact (45 minutes)

### Unit Tests

```bash
# Run conversation-specific tests
pytest tests/intent_service/test_intent_service.py -v -k "conversation"

# Run handler tests
pytest tests/intent_service/test_canonical_handlers.py -v
```

### Integration Tests

```bash
# Test conversation flow end-to-end
pytest tests/integration/ -v -k "conversation"

# Test routing logic
pytest tests/integration/test_intent_routing.py -v
```

### Performance Check

```python
# Add timing test if not exists
async def test_conversation_handler_performance():
    """Verify handler responds in <100ms"""
    start = time.time()

    intent = Intent(
        category=IntentCategory.CONVERSATION,
        action="continue",
        original_message="Let's continue our discussion"
    )

    response = await intent_service.process_intent(
        intent, session_id="test"
    )

    elapsed = time.time() - start
    assert elapsed < 0.1  # 100ms
    assert response is not None
```

---

## Phase 3: Verify Architecture (20 minutes)

### Check Handler Order

```python
# Verify canonical handlers are in logical order:
# 1. GREETING (hello)
# 2. QUERY (questions)
# 3. CONVERSATION (dialogue)  # <- NEW POSITION
# 4. ANALYSIS (analysis)
# 5. SYNTHESIS (generation)
# 6. STRATEGY (planning)
# 7. EXECUTION (actions)
```

### Verify No Duplicates

```bash
# Ensure handler not called twice
grep -n "_handle_conversation_intent" services/intent_service/intent_service.py

# Should only see:
# - Method definition
# - Single call in canonical section
```

### Check Coverage

```bash
# Run with coverage
pytest tests/intent_service/ --cov=services.intent_service --cov-report=term-missing

# Verify conversation path covered
```

---

## Phase 4: Documentation (10 minutes)

### Update Code Comments

```python
# services/intent_service/intent_service.py

# Canonical handler routing (lines ~120)
"""
Route intents to canonical handlers based on category.
Order matters for performance - most common first:
1. GREETING - Quick welcome responses
2. QUERY - Information requests
3. CONVERSATION - Dialogue continuity
4. ANALYSIS - Data analysis
...
"""
```

### Update Architecture Docs

If exists, update:
- `docs/architecture/intent-routing.md`
- `docs/patterns/canonical-handlers.md`

---

## Phase Z: Final Validation (15 minutes)

### Checklist

- [ ] Handler moved to lines 123-136 area
- [ ] Old location (line 199) removed
- [ ] Using enum comparison (not string)
- [ ] All tests pass
- [ ] Performance <100ms verified
- [ ] No duplicate handler calls
- [ ] Code comments updated

### Run Full Test Suite

```bash
# Final comprehensive test
pytest tests/ -v

# Compare with baseline
pytest tests/ --json-report --json-report-file=after-286.json
diff baseline-286.json after-286.json
```

### Create PR

```bash
git add -A
git commit -m "fix(#286): Move CONVERSATION handler to canonical section

- Moved handler from line 199 to canonical section (lines 123-136)
- Changed from string to enum comparison
- Maintains same functionality with better architecture
- All tests passing"

git push origin fix/286-conversation-handler-placement
```

---

## Success Criteria

- ✅ Handler in canonical section with other category handlers
- ✅ Uses `IntentCategory.CONVERSATION` enum (not string)
- ✅ Line 199 area no longer has conversation check
- ✅ All existing tests pass
- ✅ Performance maintained (<100ms)
- ✅ Architecture pattern consistent

---

## Risk Assessment

**Low Risk** ✅
- Simple code move
- No logic changes
- Well-tested area
- Easy to revert

**Mitigation**:
- Run tests at each step
- Keep changes minimal
- Single purpose commit

---

*Estimated: 2 hours*
*Actual: _____ (fill in after completion)*
