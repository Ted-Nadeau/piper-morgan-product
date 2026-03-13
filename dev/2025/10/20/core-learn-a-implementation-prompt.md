# CORE-LEARN-A Implementation: Wire Learning System

**Agent**: Claude Code (Programmer)
**Issue**: #221 CORE-LEARN-A - Learning Infrastructure Foundation
**Sprint**: A5 - Learning System
**Date**: October 20, 2025, 11:01 AM
**Duration**: 6 hours estimated (based on discovery)

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## Mission

**Wire the existing learning system!** Discovery found 90% (4,252 lines) of production-ready code that just needs integration. This is NOT a build task - it's a 6-hour wiring task.

**Scope**:
- Create API endpoints (2h)
- Wire to main application (2h)
- Extend user preferences (0.5h)
- Integration testing (1.5h)

**NOT in scope**:
- Building learning services (ALREADY EXIST!)
- Refactoring architecture (ALREADY DDD-COMPLIANT!)
- Creating storage layer (ALREADY EXISTS!)

---

## Discovery Report

**YOU HAVE**: `core-learn-a-discovery-report.md` uploaded by PM

**CRITICAL FINDINGS**:
- QueryLearningLoop (610 lines) - Complete, just needs wiring
- CrossFeatureKnowledgeService (601 lines) - Complete, just needs wiring
- PatternRecognitionService (543 lines) - Complete, ready
- Knowledge Infrastructure (2,994 lines) - Complete and integrated
- DDD compliant - No architectural changes needed
- Privacy compliant - Built-in from day one

**Read the discovery report first!** It contains:
- Component locations
- Integration points
- Revised estimates
- Implementation plan

---

## STOP Conditions

If ANY of these occur, STOP and escalate to PM immediately:

1. **Existing services don't work** - Discovery said they're production-ready
2. **Architecture mismatch** - Discovery said DDD-compliant
3. **Missing dependencies** - Should all be in place
4. **Tests fail** - Existing tests should pass
5. **Cannot find services** - Check discovery report locations
6. **Privacy issues** - Discovery said privacy-compliant
7. **Storage doesn't work** - JSON storage should be ready
8. **Can't provide verification evidence** - Must show wiring works

---

## Evidence Requirements

### For EVERY Claim You Make:

- **"Service wired"** → Show initialization in main.py
- **"API endpoints work"** → Show curl/test hitting endpoints
- **"Preferences extended"** → Show new preference keys
- **"Tests pass"** → Show test output
- **"Integration complete"** → Show end-to-end flow

### Working Files Location:

- ✅ dev/active/ - For test scripts, verification
- ✅ web/api/routes/ - For API endpoints
- ✅ main.py - For service initialization
- ✅ services/orchestration/ - For learning integration

---

## Implementation Plan (from Discovery)

### Phase 1: API Layer (2 hours)

**File**: `web/api/routes/learning.py` (NEW)

**Create REST endpoints**:

```python
"""
Learning API Routes

Endpoints for pattern management, feedback, and analytics.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from services.learning.query_learning_loop import get_learning_loop
from services.learning.cross_feature_knowledge import get_cross_feature_service

router = APIRouter(prefix="/api/v1/learning", tags=["learning"])


@router.get("/patterns")
async def get_patterns(
    query_id: str = None,
    feature: str = None,
    min_confidence: float = 0.5
) -> Dict[str, Any]:
    """
    Get learned patterns.

    Query params:
    - query_id: Filter by query
    - feature: Filter by feature
    - min_confidence: Minimum confidence threshold
    """
    learning_loop = get_learning_loop()

    if query_id:
        pattern = learning_loop.get_learned_pattern(query_id)
        return {"patterns": [pattern] if pattern else []}

    # Get all patterns (implement filtering)
    patterns = learning_loop.get_all_patterns()

    # Filter by confidence
    if min_confidence:
        patterns = [p for p in patterns if p.get('confidence', 0) >= min_confidence]

    # Filter by feature
    if feature:
        patterns = [p for p in patterns if p.get('feature') == feature]

    return {"patterns": patterns}


@router.post("/feedback")
async def submit_feedback(
    query_id: str,
    success: bool,
    feedback: str = None
) -> Dict[str, Any]:
    """
    Submit feedback on a pattern application.

    Body:
    - query_id: Query identifier
    - success: Was pattern application successful?
    - feedback: Optional feedback text
    """
    learning_loop = get_learning_loop()

    await learning_loop.record_feedback(
        query_id=query_id,
        success=success,
        feedback=feedback
    )

    return {
        "status": "feedback_recorded",
        "query_id": query_id,
        "success": success
    }


@router.get("/analytics")
async def get_analytics() -> Dict[str, Any]:
    """
    Get learning system analytics.

    Returns:
    - total_patterns: Total learned patterns
    - success_rate: Overall success rate
    - patterns_by_feature: Breakdown by feature
    """
    learning_loop = get_learning_loop()

    patterns = learning_loop.get_all_patterns()

    # Calculate analytics
    total = len(patterns)
    successful = sum(1 for p in patterns if p.get('success_rate', 0) > 0.5)

    analytics = {
        "total_patterns": total,
        "successful_patterns": successful,
        "success_rate": successful / total if total > 0 else 0,
        "patterns_by_feature": {}
    }

    return analytics


@router.post("/patterns/{pattern_id}/apply")
async def apply_pattern(
    pattern_id: str,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Apply a learned pattern to new context.

    Path params:
    - pattern_id: Pattern identifier

    Body:
    - context: Contextual information for pattern application
    """
    learning_loop = get_learning_loop()

    result = await learning_loop.apply_pattern(
        pattern_id=pattern_id,
        context=context
    )

    return {
        "status": "pattern_applied",
        "pattern_id": pattern_id,
        "result": result
    }


@router.get("/knowledge/shared")
async def get_shared_knowledge(
    source_feature: str = None,
    target_feature: str = None
) -> Dict[str, Any]:
    """
    Get cross-feature shared knowledge.

    Query params:
    - source_feature: Filter by source feature
    - target_feature: Filter by target feature
    """
    cross_feature_service = get_cross_feature_service()

    knowledge = await cross_feature_service.get_shared_knowledge(
        source_feature=source_feature,
        target_feature=target_feature
    )

    return {"knowledge": knowledge}


@router.delete("/patterns/{pattern_id}")
async def delete_pattern(pattern_id: str) -> Dict[str, Any]:
    """
    Delete a learned pattern.

    Path params:
    - pattern_id: Pattern identifier
    """
    learning_loop = get_learning_loop()

    await learning_loop.delete_pattern(pattern_id)

    return {
        "status": "pattern_deleted",
        "pattern_id": pattern_id
    }
```

**Register router in main.py**:

```python
# In main.py, add to API router registration
from web.api.routes import learning

app.include_router(learning.router)
```

---

### Phase 2: Application Integration (2 hours)

#### 2.1 Service Initialization (1 hour)

**File**: `main.py` (MODIFY)

**Add to service initialization**:

```python
# Add imports
from services.learning.query_learning_loop import get_learning_loop
from services.learning.cross_feature_knowledge import get_cross_feature_service

# Add to startup
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Piper Morgan...")

    # Existing service initialization...

    # Initialize learning services
    logger.info("Initializing learning services...")
    learning_loop = get_learning_loop()
    cross_feature_service = get_cross_feature_service()
    logger.info("Learning services initialized")

    logger.info("Piper Morgan started successfully")
```

#### 2.2 Orchestration Integration (1 hour)

**File**: `services/orchestration/engine.py` (MODIFY)

**Add learning integration to orchestration**:

```python
# Add import
from services.learning.query_learning_loop import get_learning_loop

class OrchestrationEngine:
    def __init__(self, ...):
        # Existing initialization...
        self.learning_loop = get_learning_loop()

    async def process_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process query with learning integration."""

        # Check for learned patterns
        learned_pattern = self.learning_loop.get_learned_pattern(query)
        if learned_pattern and learned_pattern.get('confidence', 0) > 0.7:
            logger.info(f"Found learned pattern for query: {query}")
            # Consider using learned pattern

        # Existing orchestration logic...
        result = await self._execute_orchestration(query, context)

        # Record pattern for learning
        await self.learning_loop.learn_pattern(
            query=query,
            intent=result.get('intent'),
            context=context,
            success=result.get('success', True)
        )

        return result
```

---

### Phase 3: User Preferences (0.5 hours)

**File**: `services/domain/user_preference_manager.py` (EXTEND)

**Add learning preference keys**:

```python
# Add to existing preference keys
LEARNING_ENABLED = "learning_enabled"  # bool
LEARNING_MIN_CONFIDENCE = "learning_min_confidence"  # float (0.0-1.0)
LEARNING_FEATURES = "learning_features"  # List[str] - features to learn from

# Add helper methods (following A4 pattern)
async def get_learning_enabled(self, user_id: str) -> bool:
    """Get learning enabled preference."""
    return await self.get_preference(user_id, LEARNING_ENABLED, default=True)

async def set_learning_enabled(self, user_id: str, enabled: bool) -> None:
    """Set learning enabled preference."""
    await self.set_preference(user_id, LEARNING_ENABLED, enabled)

async def get_learning_min_confidence(self, user_id: str) -> float:
    """Get minimum confidence threshold."""
    return await self.get_preference(user_id, LEARNING_MIN_CONFIDENCE, default=0.5)

async def set_learning_min_confidence(self, user_id: str, confidence: float) -> None:
    """Set minimum confidence threshold."""
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("Confidence must be between 0.0 and 1.0")
    await self.set_preference(user_id, LEARNING_MIN_CONFIDENCE, confidence)

async def get_learning_features(self, user_id: str) -> List[str]:
    """Get features enabled for learning."""
    return await self.get_preference(user_id, LEARNING_FEATURES, default=[])

async def set_learning_features(self, user_id: str, features: List[str]) -> None:
    """Set features enabled for learning."""
    await self.set_preference(user_id, LEARNING_FEATURES, features)
```

---

### Phase 4: Testing & Documentation (1.5 hours)

#### 4.1 Integration Tests (1 hour)

**File**: `tests/integration/test_learning_system.py` (NEW)

```python
"""
Integration tests for learning system.

Tests end-to-end learning flow including API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_patterns_endpoint():
    """Test GET /api/v1/learning/patterns"""
    response = client.get("/api/v1/learning/patterns")
    assert response.status_code == 200
    assert "patterns" in response.json()


def test_submit_feedback_endpoint():
    """Test POST /api/v1/learning/feedback"""
    response = client.post(
        "/api/v1/learning/feedback",
        json={
            "query_id": "test_query_123",
            "success": True,
            "feedback": "Worked great!"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "feedback_recorded"


def test_get_analytics_endpoint():
    """Test GET /api/v1/learning/analytics"""
    response = client.get("/api/v1/learning/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_patterns" in data
    assert "success_rate" in data


def test_shared_knowledge_endpoint():
    """Test GET /api/v1/learning/knowledge/shared"""
    response = client.get("/api/v1/learning/knowledge/shared")
    assert response.status_code == 200
    assert "knowledge" in response.json()


def test_learning_preferences():
    """Test learning preference management"""
    from services.domain.user_preference_manager import UserPreferenceManager

    pref_manager = UserPreferenceManager()
    user_id = "test_user_learning"

    # Test learning enabled
    await pref_manager.set_learning_enabled(user_id, True)
    enabled = await pref_manager.get_learning_enabled(user_id)
    assert enabled is True

    # Test confidence threshold
    await pref_manager.set_learning_min_confidence(user_id, 0.7)
    confidence = await pref_manager.get_learning_min_confidence(user_id)
    assert confidence == 0.7

    # Test features
    features = ["intent", "knowledge"]
    await pref_manager.set_learning_features(user_id, features)
    stored = await pref_manager.get_learning_features(user_id)
    assert stored == features


def test_end_to_end_learning_flow():
    """Test complete learning flow from query to feedback"""
    # 1. Submit query (triggers learning)
    query = "test learning query"

    # 2. Check for learned pattern
    response = client.get(
        "/api/v1/learning/patterns",
        params={"query_id": query}
    )
    assert response.status_code == 200

    # 3. Submit feedback
    response = client.post(
        "/api/v1/learning/feedback",
        json={
            "query_id": query,
            "success": True,
            "feedback": "Great result!"
        }
    )
    assert response.status_code == 200

    # 4. Verify analytics updated
    response = client.get("/api/v1/learning/analytics")
    assert response.status_code == 200
```

#### 4.2 Documentation (30 minutes)

**File**: `docs/api/learning.md` (NEW)

```markdown
# Learning API Documentation

## Overview

The Learning API provides endpoints for pattern management, feedback submission, and analytics.

## Endpoints

### GET /api/v1/learning/patterns

Get learned patterns with optional filtering.

**Query Parameters**:
- `query_id` (optional): Filter by query
- `feature` (optional): Filter by feature
- `min_confidence` (optional): Minimum confidence threshold (0.0-1.0)

**Example**:
```bash
curl http://localhost:8001/api/v1/learning/patterns?min_confidence=0.7
```

### POST /api/v1/learning/feedback

Submit feedback on pattern application.

**Request Body**:
```json
{
  "query_id": "query_123",
  "success": true,
  "feedback": "Worked perfectly!"
}
```

### GET /api/v1/learning/analytics

Get system-wide learning analytics.

**Response**:
```json
{
  "total_patterns": 42,
  "successful_patterns": 35,
  "success_rate": 0.83,
  "patterns_by_feature": {}
}
```

## User Preferences

Users can control learning behavior through preferences:

- `learning_enabled`: Enable/disable learning (default: true)
- `learning_min_confidence`: Minimum confidence threshold (default: 0.5)
- `learning_features`: List of features to learn from (default: [])

## Privacy

All learning is privacy-compliant:
- Metadata-only learning (no PII)
- User consent required
- Data anonymization built-in
```

---

## Verification Steps

### Step 1: Verify Services Exist

```bash
# Check that services exist
ls -la services/learning/query_learning_loop.py
ls -la services/learning/cross_feature_knowledge.py
ls -la services/knowledge/pattern_recognition_service.py

# Should all exist (610, 601, 543 lines respectively)
```

---

### Step 2: Run Existing Tests

```bash
# Discovery said tests exist
pytest tests/intent/test_learning_handlers.py -v

# Should pass without changes
```

---

### Step 3: Test API Endpoints

```bash
# Start application
python main.py

# In another terminal, test endpoints
curl http://localhost:8001/api/v1/learning/patterns
curl http://localhost:8001/api/v1/learning/analytics
curl -X POST http://localhost:8001/api/v1/learning/feedback \
  -H "Content-Type: application/json" \
  -d '{"query_id": "test", "success": true}'

# All should return valid JSON
```

---

### Step 4: Run Integration Tests

```bash
# Run new integration tests
pytest tests/integration/test_learning_system.py -v

# Expected: All tests passing
```

---

### Step 5: Verify Preferences

```bash
# Create test script
python3 -c "
import asyncio
from services.domain.user_preference_manager import UserPreferenceManager

async def test():
    pm = UserPreferenceManager()
    await pm.set_learning_enabled('test', True)
    enabled = await pm.get_learning_enabled('test')
    print(f'Learning enabled: {enabled}')

asyncio.run(test())
"

# Should print: Learning enabled: True
```

---

## Success Criteria

CORE-LEARN-A is complete when:

- [ ] API endpoints created (`web/api/routes/learning.py`)
- [ ] Endpoints registered in main.py
- [ ] Services initialized on startup
- [ ] Orchestration integrated with learning
- [ ] User preferences extended (3 new keys)
- [ ] All existing tests pass
- [ ] New integration tests pass (6+ tests)
- [ ] API documentation complete
- [ ] Can query patterns via API
- [ ] Can submit feedback via API
- [ ] Analytics endpoint working
- [ ] Code committed with evidence
- [ ] Session log updated

---

## Files to Create/Modify

### Create

- `web/api/routes/learning.py` (~200 lines) - API endpoints
- `tests/integration/test_learning_system.py` (~150 lines) - Integration tests
- `docs/api/learning.md` (~100 lines) - API documentation

### Modify

- `main.py` - Service initialization + router registration
- `services/orchestration/engine.py` - Learning integration
- `services/domain/user_preference_manager.py` - Learning preferences

### Session Log

- `dev/2025/10/20/HHMM-prog-code-log.md` (continue from morning)

---

## Expected Timeline

**Total**: 6 hours (from discovery)

**Breakdown**:
- 2h: API endpoints
- 2h: Application integration
- 0.5h: User preferences
- 1h: Integration tests
- 0.5h: Documentation

---

## Remember

**YOU ARE WIRING, NOT BUILDING!**

The services exist. They're production-ready. They're DDD-compliant. They're privacy-compliant.

**Your job**:
1. Create API layer (REST endpoints)
2. Wire services to main app
3. Extend preferences (like A4)
4. Test integration
5. Document

**Not your job**:
- Build learning services (exist!)
- Refactor architecture (compliant!)
- Create storage (exists!)
- Design patterns (done!)

**Just wire and ship!** 🔌

---

**Ready to wire the learning system!** 🚀

*4-minute discovery, 6-hour implementation. Sprint A5 is flying!*
