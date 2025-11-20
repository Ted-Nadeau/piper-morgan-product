# Claude Code Agent Prompt: User Controls API - Phase 2 (#300)

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- BRIEFING-ESSENTIAL-AGENT.md - Your role requirements
- BRIEFING-CURRENT-STATE.md - Current epic and focus
- BRIEFING-METHODOLOGY.md - Inchworm Protocol

---

## 🏛️ STRATEGIC CONTEXT: Building on Foundation Stone #1

### Phase 1 Complete ✅
- Database infrastructure operational
- Learning Handler wired to orchestration
- Real-time pattern capture working
- Confidence calculation validated
- Performance targets exceeded

### Phase 2: User Controls (THIS PROMPT) 🎯
**Goal**: Give users control over their learning patterns

**Philosophy**:
- **User Control First** - Before automation (Phase 4)
- **Transparency** - Users see what's learned
- **API Foundation** - Build API before frontend (Phase 3)
- **Manual Testing** - Automated tests in Phase 5

**This is not automation** - it's **user empowerment**

---

## 🛠️ INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Verify Phase 1 Deliverables FIRST

**Before doing ANYTHING else, verify these exist**:

```bash
# Check Learning Handler exists
ls -la services/learning/learning_handler.py
# Expected: 397 lines, 5 methods

# Check database model
grep -A20 "class LearnedPattern" services/database/models.py
# Expected: Model with confidence, usage_count, etc.

# Check integration
grep -A10 "learning_handler.capture_action" services/intent/intent_service.py
# Expected: Integration hooks present

# Check database table
# Note: May need to check via actual DB connection or migration files
ls -la alembic/versions/*learned_patterns*
# Expected: Migration file exists

# Check current state
ps aux | grep python
# Check if server is running
```

**Expected Phase 1 State**:
- ✅ `services/learning/learning_handler.py` exists (397 lines)
- ✅ `LearnedPattern` model in database/models.py
- ✅ Integration in IntentService (capture_action + record_outcome)
- ✅ Alembic migration for learned_patterns table
- ✅ Manual tests in tests/manual/test_learning_handler_phase1.py

**STOP Conditions**:
- ❌ Phase 1 deliverables missing
- ❌ Learning Handler not found
- ❌ Database model missing
- ❌ Integration not wired

**If Phase 1 incomplete**:
1. **STOP immediately**
2. **Report what's missing** with evidence
3. **Wait for Phase 1 completion**

**Evidence Required**: Provide terminal outputs showing all Phase 1 components present

---

## Session Log Management

**IMPORTANT**: Check for existing log before creating new one!

```bash
# Check if you already have a log today
ls -la dev/$(date +%Y/%m/%d)/$(date +%Y-%m-%d)-*-code-*-log.md
```

**If NO log exists**: Create new log:
- Format: `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-code-agent-log.md`

**If log EXISTS**: DO NOT create new log!
- Append new section to existing log
- Format: `## Session [N]: Issue #300 Phase 2 ([Time])`
- Include `---` between sessions

---

## Mission

**Implement User Controls API for Issue #300 Phase 2**: REST API for pattern management and learning settings.

**Scope for This Prompt**: Phase 2 ONLY
- Pattern Management API
- Learning Settings API
- Pattern Inspection endpoints
- **NOT in scope**: Frontend UI, automation, auth integration, comprehensive testing

**Success Target**: Users can view, enable, disable, and delete their learned patterns via API. Users can configure learning settings.

---

## Context

### GitHub Issue
- **Issue**: #300 - CORE-ALPHA-LEARNING-BASIC
- **Phase**: 2 of 6 (User Controls API)
- **Priority**: P2 (Alpha Feature)
- **Prerequisites**: Phase 1 complete ✅

### Current State (Phase 1 Complete)
- Learning Handler operational
- Patterns captured in database
- Confidence calculation working
- IntentService integration complete
- **Gap**: No user-facing API to manage patterns

### Target State (Phase 2)
- REST API for pattern management
- API for learning settings
- Users can view patterns with full details
- Users can enable/disable/delete patterns
- Users can configure learning behavior
- All endpoints tested manually with evidence

### Dependencies
- Phase 1 complete (verified in infrastructure check)
- FastAPI web framework (already in use)
- SQLAlchemy async (already configured)
- Database session management (already present)

### User Data Risk
- **MEDIUM** - Modifying/deleting user patterns
- Must verify pattern ownership (user_id check)
- Must handle concurrent modifications (SELECT FOR UPDATE)
- Must preserve data integrity (transactions)

---

## 📋 PHASE 2 SCOPE DEFINITION

### What IS In Scope ✅

**1. Pattern Management API**:
- `GET /api/learning/patterns` - List user's patterns
- `GET /api/learning/patterns/{pattern_id}` - Get specific pattern details
- `DELETE /api/learning/patterns/{pattern_id}` - Remove pattern
- `POST /api/learning/patterns/{pattern_id}/enable` - Enable pattern
- `POST /api/learning/patterns/{pattern_id}/disable` - Disable pattern

**2. Learning Settings API**:
- `GET /api/learning/settings` - Get user's learning settings
- `PUT /api/learning/settings` - Update learning settings
- Settings fields:
  - `learning_enabled`: bool (global on/off)
  - `suggestion_threshold`: float (default: 0.7)
  - `automation_threshold`: float (default: 0.9)

**3. Pattern Inspection**:
- Full pattern details in responses:
  - pattern_id, pattern_type, confidence
  - usage_count, success_count, failure_count
  - pattern_data (full JSON)
  - enabled, created_at, last_used_at

**4. Security**:
- Pattern ownership verification (user_id check)
- 403 Forbidden for unauthorized access
- 404 Not Found for missing patterns

**5. Manual Testing**:
- curl/Postman commands for each endpoint
- Test with actual database
- Verify ownership checks
- Document test results

### What is NOT In Scope ❌

**DO NOT IMPLEMENT**:
- ❌ Frontend UI (Phase 3)
- ❌ Pattern automation (Phase 4)
- ❌ Pattern suggestions in responses (Phase 3)
- ❌ Auth integration (continue with test user)
- ❌ Enhanced similarity matching (Phase 3-4)
- ❌ Automated unit tests (Phase 5)
- ❌ Automated integration tests (Phase 5)
- ❌ Pattern analytics/statistics (future)
- ❌ Pattern export/import (future)
- ❌ Batch operations (future)

**If you're tempted to add these**: STOP and stick to scope!

---

## Evidence Requirements (CRITICAL)

### For EVERY Claim You Make:

**"API endpoint created"** → Show code + curl test:
```bash
$ grep -A20 "@router.get.*patterns" web/api/routes/learning.py
[show actual code]

$ curl -X GET http://localhost:8001/api/learning/patterns
[show actual response]
```

**"Pattern ownership verified"** → Show test:
```bash
$ # Try to delete another user's pattern (should fail)
$ curl -X DELETE http://localhost:8001/api/learning/patterns/{other-user-pattern}
{"detail": "Pattern not found"}  # 404 or 403

$ # Delete own pattern (should succeed)
$ curl -X DELETE http://localhost:8001/api/learning/patterns/{my-pattern}
{"success": true}
```

**"Settings API working"** → Show GET/PUT cycle:
```bash
$ curl -X GET http://localhost:8001/api/learning/settings
{"learning_enabled": true, "suggestion_threshold": 0.7, ...}

$ curl -X PUT http://localhost:8001/api/learning/settings \
  -H "Content-Type: application/json" \
  -d '{"learning_enabled": false}'
{"learning_enabled": false, ...}

$ curl -X GET http://localhost:8001/api/learning/settings
{"learning_enabled": false, ...}  # Verify persisted
```

**"All endpoints tested"** → Show test results for EACH endpoint

**"Committed changes"** → Show git log:
```bash
$ git log --oneline -1
abc1234 feat(#300): Phase 2 - User Controls API
```

### Completion Bias Prevention:
- **Never guess! Always verify first!**
- **NO "should work"** - only "here's proof it works"
- Show actual curl outputs, not expected outputs
- Test each endpoint before claiming complete

---

## Implementation Phases

### Phase 2.0: Create API Structure (30 minutes)

**Goal**: Set up FastAPI route structure for learning endpoints

**Tasks**:

**Step 2.0.1: Create Route File** (15 min):
```bash
# Check if routes structure exists
ls -la web/api/routes/

# If learning.py doesn't exist, create it
touch web/api/routes/learning.py
```

**File**: `web/api/routes/learning.py`
```python
"""
Learning API endpoints for pattern management and settings.
Issue #300 Phase 2 - User Controls API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from services.database.session import get_db
from services.database.models import LearnedPattern
from services.learning.learning_handler import LearningHandler
# Import other dependencies as needed

router = APIRouter(prefix="/api/learning", tags=["learning"])

# TODO: Get user_id from auth - using test user for Phase 2
TEST_USER_ID = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")


# Endpoints will be added in Phase 2.1-2.3
```

**Step 2.0.2: Register Router** (15 min):

Check main app file:
```bash
# Find main app
grep -r "FastAPI()" web/ --include="*.py"
```

Add router to main app (likely `web/app.py` or similar):
```python
from web.api.routes import learning

app.include_router(learning.router)
```

**Verification**:
```bash
# Start server (if not running)
cd /path/to/project
uvicorn web.app:app --port 8001 --reload &

# Check routes registered
curl http://localhost:8001/docs
# Should see /api/learning in OpenAPI docs
```

**STOP Conditions**:
- FastAPI not found
- Can't locate main app file
- Router registration fails

**Evidence Required**:
```bash
# Show router file created
$ ls -la web/api/routes/learning.py

# Show router registered
$ grep "learning.router" web/app.py  # or wherever app is

# Show docs accessible
$ curl http://localhost:8001/docs | grep learning
```

---

### Phase 2.1: Pattern Management Endpoints (1 hour)

**Goal**: Implement GET, DELETE, enable, disable endpoints

**Step 2.1.1: List Patterns Endpoint** (15 min):

```python
@router.get("/patterns")
async def list_patterns(
    db: AsyncSession = Depends(get_db)
) -> List[dict]:
    """List all patterns for current user"""

    # Query user's patterns
    result = await db.execute(
        select(LearnedPattern)
        .where(LearnedPattern.user_id == TEST_USER_ID)
        .order_by(LearnedPattern.last_used_at.desc())
    )
    patterns = result.scalars().all()

    # Format response
    return [
        {
            "pattern_id": str(pattern.pattern_id),
            "pattern_type": pattern.pattern_type.value,
            "confidence": pattern.confidence,
            "usage_count": pattern.usage_count,
            "success_count": pattern.success_count,
            "failure_count": pattern.failure_count,
            "pattern_data": pattern.pattern_data,
            "enabled": pattern.enabled,
            "created_at": pattern.created_at.isoformat(),
            "last_used_at": pattern.last_used_at.isoformat() if pattern.last_used_at else None,
        }
        for pattern in patterns
    ]
```

**Test**:
```bash
curl -X GET http://localhost:8001/api/learning/patterns | jq '.'
```

**Step 2.1.2: Get Pattern Details Endpoint** (10 min):

```python
@router.get("/patterns/{pattern_id}")
async def get_pattern(
    pattern_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Get detailed information about a specific pattern"""

    # Query pattern
    result = await db.execute(
        select(LearnedPattern)
        .where(
            LearnedPattern.pattern_id == pattern_id,
            LearnedPattern.user_id == TEST_USER_ID  # Ownership check
        )
    )
    pattern = result.scalar_one_or_none()

    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    # Return detailed info
    return {
        "pattern_id": str(pattern.pattern_id),
        "pattern_type": pattern.pattern_type.value,
        "confidence": pattern.confidence,
        "usage_count": pattern.usage_count,
        "success_count": pattern.success_count,
        "failure_count": pattern.failure_count,
        "pattern_data": pattern.pattern_data,
        "enabled": pattern.enabled,
        "created_at": pattern.created_at.isoformat(),
        "last_used_at": pattern.last_used_at.isoformat() if pattern.last_used_at else None,
        "last_updated_at": pattern.last_updated_at.isoformat() if pattern.last_updated_at else None,
    }
```

**Test**:
```bash
# First, get a pattern_id from list
PATTERN_ID=$(curl -s http://localhost:8001/api/learning/patterns | jq -r '.[0].pattern_id')

# Then get details
curl -X GET http://localhost:8001/api/learning/patterns/$PATTERN_ID | jq '.'
```

**Step 2.1.3: Delete Pattern Endpoint** (15 min):

```python
@router.delete("/patterns/{pattern_id}")
async def delete_pattern(
    pattern_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Delete a learned pattern"""

    # Query pattern with FOR UPDATE (lock for deletion)
    result = await db.execute(
        select(LearnedPattern)
        .where(
            LearnedPattern.pattern_id == pattern_id,
            LearnedPattern.user_id == TEST_USER_ID  # Ownership check
        )
        .with_for_update()
    )
    pattern = result.scalar_one_or_none()

    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    # Delete pattern
    await db.delete(pattern)
    await db.commit()

    return {"success": True, "pattern_id": str(pattern_id)}
```

**Test**:
```bash
# Delete a pattern
curl -X DELETE http://localhost:8001/api/learning/patterns/$PATTERN_ID

# Verify deleted (should return 404)
curl -X GET http://localhost:8001/api/learning/patterns/$PATTERN_ID
```

**Step 2.1.4: Enable/Disable Endpoints** (20 min):

```python
@router.post("/patterns/{pattern_id}/enable")
async def enable_pattern(
    pattern_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Enable a pattern"""

    # Query pattern
    result = await db.execute(
        select(LearnedPattern)
        .where(
            LearnedPattern.pattern_id == pattern_id,
            LearnedPattern.user_id == TEST_USER_ID
        )
        .with_for_update()
    )
    pattern = result.scalar_one_or_none()

    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    # Enable pattern
    pattern.enabled = True
    await db.commit()

    return {
        "success": True,
        "pattern_id": str(pattern_id),
        "enabled": True
    }


@router.post("/patterns/{pattern_id}/disable")
async def disable_pattern(
    pattern_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Disable a pattern"""

    # Query pattern
    result = await db.execute(
        select(LearnedPattern)
        .where(
            LearnedPattern.pattern_id == pattern_id,
            LearnedPattern.user_id == TEST_USER_ID
        )
        .with_for_update()
    )
    pattern = result.scalar_one_or_none()

    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    # Disable pattern
    pattern.enabled = False
    await db.commit()

    return {
        "success": True,
        "pattern_id": str(pattern_id),
        "enabled": False
    }
```

**Test**:
```bash
# Disable pattern
curl -X POST http://localhost:8001/api/learning/patterns/$PATTERN_ID/disable

# Verify disabled
curl -X GET http://localhost:8001/api/learning/patterns/$PATTERN_ID | jq '.enabled'
# Should show: false

# Enable pattern
curl -X POST http://localhost:8001/api/learning/patterns/$PATTERN_ID/enable

# Verify enabled
curl -X GET http://localhost:8001/api/learning/patterns/$PATTERN_ID | jq '.enabled'
# Should show: true
```

**Phase 2.1 Evidence Required**:
```bash
# Show all endpoints implemented
$ grep "@router\." web/api/routes/learning.py

# Test each endpoint
$ curl -X GET http://localhost:8001/api/learning/patterns
$ curl -X GET http://localhost:8001/api/learning/patterns/{id}
$ curl -X POST http://localhost:8001/api/learning/patterns/{id}/disable
$ curl -X POST http://localhost:8001/api/learning/patterns/{id}/enable
$ curl -X DELETE http://localhost:8001/api/learning/patterns/{id}

# All should return successful responses (not 500 errors)
```

---

### Phase 2.2: Learning Settings API (45 minutes)

**Goal**: Implement settings GET/PUT endpoints

**Step 2.2.1: Create Settings Model** (15 min):

First, check if settings model exists:
```bash
grep -r "LearningSettings\|learning_settings" services/database/models.py
```

If not, add to `services/database/models.py`:

```python
class LearningSettings(Base):
    """User learning preferences and configuration"""
    __tablename__ = "learning_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True  # One settings per user
    )

    learning_enabled = Column(Boolean, default=True, nullable=False)
    suggestion_threshold = Column(Float, default=0.7, nullable=False)
    automation_threshold = Column(Float, default=0.9, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    user = relationship("User", back_populates="learning_settings")
```

Add to User model:
```python
# In User class
learning_settings = relationship(
    "LearningSettings",
    back_populates="user",
    uselist=False,  # One-to-one
    cascade="all, delete-orphan"
)
```

**Create migration**:
```bash
cd /path/to/project
alembic revision -m "add_learning_settings_table_issue_300"
```

Edit migration file to add table creation.

**Run migration**:
```bash
alembic upgrade head
```

**Step 2.2.2: Get Settings Endpoint** (15 min):

```python
from pydantic import BaseModel

class LearningSettingsResponse(BaseModel):
    learning_enabled: bool
    suggestion_threshold: float
    automation_threshold: float
    updated_at: str


@router.get("/settings")
async def get_settings(
    db: AsyncSession = Depends(get_db)
) -> LearningSettingsResponse:
    """Get user's learning settings"""

    # Query settings
    result = await db.execute(
        select(LearningSettings)
        .where(LearningSettings.user_id == TEST_USER_ID)
    )
    settings = result.scalar_one_or_none()

    # If no settings exist, create defaults
    if not settings:
        settings = LearningSettings(
            user_id=TEST_USER_ID,
            learning_enabled=True,
            suggestion_threshold=0.7,
            automation_threshold=0.9
        )
        db.add(settings)
        await db.commit()
        await db.refresh(settings)

    return LearningSettingsResponse(
        learning_enabled=settings.learning_enabled,
        suggestion_threshold=settings.suggestion_threshold,
        automation_threshold=settings.automation_threshold,
        updated_at=settings.updated_at.isoformat()
    )
```

**Test**:
```bash
curl -X GET http://localhost:8001/api/learning/settings | jq '.'
```

**Step 2.2.3: Update Settings Endpoint** (15 min):

```python
class LearningSettingsUpdate(BaseModel):
    learning_enabled: bool | None = None
    suggestion_threshold: float | None = None
    automation_threshold: float | None = None


@router.put("/settings")
async def update_settings(
    updates: LearningSettingsUpdate,
    db: AsyncSession = Depends(get_db)
) -> LearningSettingsResponse:
    """Update user's learning settings"""

    # Query settings with lock
    result = await db.execute(
        select(LearningSettings)
        .where(LearningSettings.user_id == TEST_USER_ID)
        .with_for_update()
    )
    settings = result.scalar_one_or_none()

    # Create if doesn't exist
    if not settings:
        settings = LearningSettings(
            user_id=TEST_USER_ID,
            learning_enabled=True,
            suggestion_threshold=0.7,
            automation_threshold=0.9
        )
        db.add(settings)

    # Update fields if provided
    if updates.learning_enabled is not None:
        settings.learning_enabled = updates.learning_enabled
    if updates.suggestion_threshold is not None:
        # Validate threshold (0.0 - 1.0)
        if not 0.0 <= updates.suggestion_threshold <= 1.0:
            raise HTTPException(400, "suggestion_threshold must be between 0.0 and 1.0")
        settings.suggestion_threshold = updates.suggestion_threshold
    if updates.automation_threshold is not None:
        # Validate threshold (0.0 - 1.0)
        if not 0.0 <= updates.automation_threshold <= 1.0:
            raise HTTPException(400, "automation_threshold must be between 0.0 and 1.0")
        settings.automation_threshold = updates.automation_threshold

    settings.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(settings)

    return LearningSettingsResponse(
        learning_enabled=settings.learning_enabled,
        suggestion_threshold=settings.suggestion_threshold,
        automation_threshold=settings.automation_threshold,
        updated_at=settings.updated_at.isoformat()
    )
```

**Test**:
```bash
# Get current settings
curl -X GET http://localhost:8001/api/learning/settings | jq '.'

# Update learning_enabled
curl -X PUT http://localhost:8001/api/learning/settings \
  -H "Content-Type: application/json" \
  -d '{"learning_enabled": false}' | jq '.'

# Verify updated
curl -X GET http://localhost:8001/api/learning/settings | jq '.learning_enabled'
# Should show: false

# Update thresholds
curl -X PUT http://localhost:8001/api/learning/settings \
  -H "Content-Type: application/json" \
  -d '{"suggestion_threshold": 0.8, "automation_threshold": 0.95}' | jq '.'

# Verify
curl -X GET http://localhost:8001/api/learning/settings | jq '.'
```

**Phase 2.2 Evidence Required**:
```bash
# Show settings model added
$ grep -A15 "class LearningSettings" services/database/models.py

# Show migration created
$ ls -la alembic/versions/*learning_settings*

# Test GET
$ curl -X GET http://localhost:8001/api/learning/settings

# Test PUT (disable learning)
$ curl -X PUT http://localhost:8001/api/learning/settings \
  -H "Content-Type: application/json" \
  -d '{"learning_enabled": false}'

# Verify persisted
$ curl -X GET http://localhost:8001/api/learning/settings | jq '.learning_enabled'
```

---

### Phase 2.3: Security & Error Handling (30 minutes)

**Goal**: Verify ownership checks, handle errors properly

**Step 2.3.1: Ownership Verification Test** (15 min):

Create test script `tests/manual/test_phase2_security.py`:

```python
"""
Manual security tests for Phase 2 User Controls API
Tests pattern ownership and authorization
"""
import requests
from uuid import uuid4

BASE_URL = "http://localhost:8001/api/learning"

# Test user (from Phase 1)
TEST_USER_ID = "3f4593ae-5bc9-468d-b08d-8c4c02a5b963"

def test_ownership():
    """Test that users can only access their own patterns"""

    print("\n=== Testing Pattern Ownership ===\n")

    # Get patterns for test user
    response = requests.get(f"{BASE_URL}/patterns")
    assert response.status_code == 200
    patterns = response.json()

    if not patterns:
        print("⚠️  No patterns exist for test - create some first")
        return

    # Try to access existing pattern (should work)
    pattern_id = patterns[0]["pattern_id"]
    response = requests.get(f"{BASE_URL}/patterns/{pattern_id}")
    assert response.status_code == 200
    print(f"✓ Can access own pattern: {pattern_id[:8]}...")

    # Try to access non-existent pattern (should 404)
    fake_id = str(uuid4())
    response = requests.get(f"{BASE_URL}/patterns/{fake_id}")
    assert response.status_code == 404
    print(f"✓ Cannot access non-existent pattern (404)")

    # Try to delete non-existent pattern (should 404)
    response = requests.delete(f"{BASE_URL}/patterns/{fake_id}")
    assert response.status_code == 404
    print(f"✓ Cannot delete non-existent pattern (404)")

    # Try to disable non-existent pattern (should 404)
    response = requests.post(f"{BASE_URL}/patterns/{fake_id}/disable")
    assert response.status_code == 404
    print(f"✓ Cannot disable non-existent pattern (404)")

    print("\n✅ All ownership tests passed!\n")


def test_settings_validation():
    """Test settings validation"""

    print("\n=== Testing Settings Validation ===\n")

    # Try invalid threshold (too high)
    response = requests.put(
        f"{BASE_URL}/settings",
        json={"suggestion_threshold": 1.5}
    )
    assert response.status_code == 400
    print("✓ Rejects threshold > 1.0 (400)")

    # Try invalid threshold (negative)
    response = requests.put(
        f"{BASE_URL}/settings",
        json={"automation_threshold": -0.1}
    )
    assert response.status_code == 400
    print("✓ Rejects threshold < 0.0 (400)")

    # Try valid threshold
    response = requests.put(
        f"{BASE_URL}/settings",
        json={"suggestion_threshold": 0.75}
    )
    assert response.status_code == 200
    print("✓ Accepts valid threshold (200)")

    print("\n✅ All validation tests passed!\n")


if __name__ == "__main__":
    try:
        test_ownership()
        test_settings_validation()
        print("\n🎉 All security tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
```

**Run tests**:
```bash
python tests/manual/test_phase2_security.py
```

**Step 2.3.2: Error Handling Review** (15 min):

Verify each endpoint handles errors:
- 404 for pattern not found
- 400 for invalid input
- 500 for server errors (should not happen!)

**Test error cases**:
```bash
# 404: Non-existent pattern
curl -X GET http://localhost:8001/api/learning/patterns/00000000-0000-0000-0000-000000000000
# Should return: {"detail": "Pattern not found"}

# 400: Invalid threshold
curl -X PUT http://localhost:8001/api/learning/settings \
  -H "Content-Type: application/json" \
  -d '{"suggestion_threshold": 2.0}'
# Should return: {"detail": "suggestion_threshold must be between 0.0 and 1.0"}

# 400: Invalid UUID format
curl -X GET http://localhost:8001/api/learning/patterns/not-a-uuid
# Should return: 422 Unprocessable Entity (FastAPI validation)
```

**Phase 2.3 Evidence Required**:
```bash
# Show security test created
$ ls -la tests/manual/test_phase2_security.py

# Run security tests
$ python tests/manual/test_phase2_security.py
[show output - all tests should pass]

# Test error handling
$ curl -X GET http://localhost:8001/api/learning/patterns/fake-id
{"detail": "Pattern not found"}
```

---

### Phase 2.4: Documentation & Testing (30 minutes)

**Goal**: Document all endpoints, create comprehensive test guide

**Step 2.4.1: Create API Documentation** (15 min):

Create `docs/api/learning-api.md`:

```markdown
# Learning API Documentation

**Issue**: #300 Phase 2 - User Controls API
**Base Path**: `/api/learning`

## Pattern Management Endpoints

### List Patterns
**GET** `/api/learning/patterns`

Returns all patterns for the current user.

**Response** (200):
```json
[
  {
    "pattern_id": "uuid",
    "pattern_type": "USER_WORKFLOW",
    "confidence": 0.75,
    "usage_count": 10,
    "success_count": 8,
    "failure_count": 2,
    "pattern_data": {...},
    "enabled": true,
    "created_at": "2025-11-12T20:00:00",
    "last_used_at": "2025-11-13T06:00:00"
  }
]
```

### Get Pattern Details
**GET** `/api/learning/patterns/{pattern_id}`

Returns detailed information about a specific pattern.

**Response** (200): Single pattern object
**Response** (404): `{"detail": "Pattern not found"}`

### Delete Pattern
**DELETE** `/api/learning/patterns/{pattern_id}`

Permanently deletes a pattern.

**Response** (200): `{"success": true, "pattern_id": "uuid"}`
**Response** (404): `{"detail": "Pattern not found"}`

### Enable Pattern
**POST** `/api/learning/patterns/{pattern_id}/enable`

Enables a disabled pattern.

**Response** (200): `{"success": true, "pattern_id": "uuid", "enabled": true}`

### Disable Pattern
**POST** `/api/learning/patterns/{pattern_id}/disable`

Disables an active pattern (prevents suggestions).

**Response** (200): `{"success": true, "pattern_id": "uuid", "enabled": false}`

## Settings Endpoints

### Get Settings
**GET** `/api/learning/settings`

Returns current learning settings for the user.

**Response** (200):
```json
{
  "learning_enabled": true,
  "suggestion_threshold": 0.7,
  "automation_threshold": 0.9,
  "updated_at": "2025-11-13T07:00:00"
}
```

### Update Settings
**PUT** `/api/learning/settings`

Updates learning settings (partial updates supported).

**Request Body**:
```json
{
  "learning_enabled": false,  // optional
  "suggestion_threshold": 0.8,  // optional (0.0 - 1.0)
  "automation_threshold": 0.95  // optional (0.0 - 1.0)
}
```

**Response** (200): Updated settings object
**Response** (400): Validation error

## Error Codes

- **200 OK**: Success
- **400 Bad Request**: Invalid input (e.g., threshold out of range)
- **404 Not Found**: Pattern doesn't exist or not owned by user
- **422 Unprocessable Entity**: Invalid request format
- **500 Internal Server Error**: Server error (should not happen!)

## Authentication

**Current (Phase 2)**: Using test user UUID
**Future (Phase 3-4)**: JWT auth with user_id from token
```

**Step 2.4.2: Create Test Guide** (15 min):

Create `tests/manual/PHASE2-TEST-GUIDE.md`:

```markdown
# Phase 2 Manual Test Guide

## Prerequisites
- Server running: `uvicorn web.app:app --port 8001 --reload`
- Phase 1 patterns exist in database

## Test Sequence

### 1. List Patterns
```bash
curl -X GET http://localhost:8001/api/learning/patterns | jq '.'
```
**Expected**: Array of patterns (may be empty)

### 2. Get Pattern Details
```bash
# Get first pattern ID
PATTERN_ID=$(curl -s http://localhost:8001/api/learning/patterns | jq -r '.[0].pattern_id')

# Get details
curl -X GET http://localhost:8001/api/learning/patterns/$PATTERN_ID | jq '.'
```
**Expected**: Full pattern object

### 3. Disable Pattern
```bash
curl -X POST http://localhost:8001/api/learning/patterns/$PATTERN_ID/disable | jq '.'
```
**Expected**: `{"success": true, "enabled": false}`

### 4. Verify Disabled
```bash
curl -X GET http://localhost:8001/api/learning/patterns/$PATTERN_ID | jq '.enabled'
```
**Expected**: `false`

### 5. Enable Pattern
```bash
curl -X POST http://localhost:8001/api/learning/patterns/$PATTERN_ID/enable | jq '.'
```
**Expected**: `{"success": true, "enabled": true}`

### 6. Get Settings
```bash
curl -X GET http://localhost:8001/api/learning/settings | jq '.'
```
**Expected**: Settings object with defaults

### 7. Update Settings
```bash
curl -X PUT http://localhost:8001/api/learning/settings \
  -H "Content-Type: application/json" \
  -d '{"learning_enabled": false}' | jq '.'
```
**Expected**: Updated settings with `learning_enabled: false`

### 8. Verify Settings Persisted
```bash
curl -X GET http://localhost:8001/api/learning/settings | jq '.learning_enabled'
```
**Expected**: `false`

### 9. Delete Pattern (DESTRUCTIVE - test last!)
```bash
curl -X DELETE http://localhost:8001/api/learning/patterns/$PATTERN_ID | jq '.'
```
**Expected**: `{"success": true}`

### 10. Verify Deleted
```bash
curl -X GET http://localhost:8001/api/learning/patterns/$PATTERN_ID
```
**Expected**: `{"detail": "Pattern not found"}` (404)

## Security Tests

### Test Ownership
```bash
# Try to access non-existent pattern
curl -X GET http://localhost:8001/api/learning/patterns/00000000-0000-0000-0000-000000000000
```
**Expected**: 404 Not Found

### Test Validation
```bash
# Try invalid threshold
curl -X PUT http://localhost:8001/api/learning/settings \
  -H "Content-Type: application/json" \
  -d '{"suggestion_threshold": 2.0}'
```
**Expected**: 400 Bad Request with error message

## Automated Test Script
```bash
python tests/manual/test_phase2_security.py
```
**Expected**: All tests pass

## Success Criteria
- ✅ All 10 manual tests pass
- ✅ Security tests pass
- ✅ No 500 errors
- ✅ Ownership properly enforced
- ✅ Settings persist across requests
```

**Phase 2.4 Evidence Required**:
```bash
# Show documentation created
$ ls -la docs/api/learning-api.md
$ ls -la tests/manual/PHASE2-TEST-GUIDE.md

# Run full test sequence from guide
[paste results of each test showing success]

# Show OpenAPI docs
$ curl http://localhost:8001/docs | grep -A5 learning
[show /api/learning endpoints in docs]
```

---

## Success Criteria (Phase 2 Complete)

### Functionality ✅
- [ ] All 5 pattern management endpoints working
- [ ] Settings GET/PUT endpoints working
- [ ] Pattern ownership verification
- [ ] Error handling (404, 400, 422)
- [ ] Database persistence

### API Quality ✅
- [ ] RESTful design
- [ ] Proper HTTP status codes
- [ ] JSON request/response bodies
- [ ] Input validation
- [ ] Clear error messages

### Security ✅
- [ ] Pattern ownership checks (user_id filter)
- [ ] 404 for unauthorized access
- [ ] SELECT FOR UPDATE for modifications
- [ ] Transaction safety

### Testing ✅
- [ ] All manual tests pass (10 tests from guide)
- [ ] Security tests pass
- [ ] Error cases tested
- [ ] No 500 errors observed

### Documentation ✅
- [ ] API documentation created
- [ ] Test guide created
- [ ] OpenAPI docs accessible
- [ ] All endpoints documented

### Evidence ✅
- [ ] curl outputs for each endpoint
- [ ] Database state verified
- [ ] Security test results
- [ ] Git commits with messages

---

## What's NOT Expected (Out of Scope)

❌ **Frontend UI** (Phase 3)
❌ **Pattern automation** (Phase 4)
❌ **Auth integration** (Phase 3-4)
❌ **Automated unit tests** (Phase 5)
❌ **Automated integration tests** (Phase 5)

If you find yourself implementing these, STOP and stick to Phase 2 scope!

---

## Deliverables

**Code**:
1. `web/api/routes/learning.py` - All endpoints
2. `services/database/models.py` - LearningSettings model (if needed)
3. Alembic migration for learning_settings table (if needed)

**Tests**:
1. `tests/manual/test_phase2_security.py` - Security tests
2. `tests/manual/PHASE2-TEST-GUIDE.md` - Manual test guide

**Documentation**:
1. `docs/api/learning-api.md` - API documentation
2. Session log with evidence
3. Git commits

**Evidence Package**:
- curl outputs for ALL endpoints
- Database verification
- Security test results
- OpenAPI docs screenshot
- Git log showing commits

---

## Estimated Effort

**Total**: 2-3 hours

- Phase 2.0 (Structure): 30 minutes
- Phase 2.1 (Pattern APIs): 1 hour
- Phase 2.2 (Settings APIs): 45 minutes
- Phase 2.3 (Security): 30 minutes
- Phase 2.4 (Documentation): 30 minutes

---

## STOP Conditions (17 Total)

If ANY occur, STOP and report:

1. Phase 1 deliverables missing
2. Learning Handler not found
3. Database model missing
4. Can't register router
5. FastAPI not working
6. Database connection fails
7. Pattern ownership check fails
8. Any endpoint returns 500
9. Settings validation broken
10. Tests fail
11. Can't create migration
12. Can't commit changes
13. Documentation can't be created
14. Tempted to add frontend UI
15. Tempted to add automation
16. Tempted to integrate auth
17. Any test in manual guide fails

---

## Cross-Validation Preparation

**For next agent (or PM) to verify**:

**What to Check**:
1. All 5 pattern endpoints exist: `grep "@router" web/api/routes/learning.py`
2. Settings endpoints exist: `grep "settings" web/api/routes/learning.py`
3. Manual tests pass: `python tests/manual/test_phase2_security.py`
4. All 10 tests from guide pass
5. OpenAPI docs show endpoints: `curl http://localhost:8001/docs`

**Commands**:
```bash
# Check endpoints
grep "@router\." web/api/routes/learning.py | wc -l
# Expected: 7 endpoints

# Test pattern list
curl -X GET http://localhost:8001/api/learning/patterns

# Test settings
curl -X GET http://localhost:8001/api/learning/settings

# Run security tests
python tests/manual/test_phase2_security.py

# Follow test guide
cat tests/manual/PHASE2-TEST-GUIDE.md
```

**Expected Results**:
- 7 endpoints registered
- All curl commands succeed
- Security tests pass
- Test guide completes successfully

---

## Self-Check Before Claiming Complete

Ask yourself:
1. ✅ Did I verify Phase 1 exists FIRST?
2. ✅ Are ALL 7 endpoints implemented?
3. ✅ Did I test EACH endpoint with curl?
4. ✅ Do pattern ownership checks work?
5. ✅ Does settings validation work?
6. ✅ Did I create security tests?
7. ✅ Did I create documentation?
8. ✅ Did I create test guide?
9. ✅ Did I run all 10 manual tests?
10. ✅ Did I provide evidence for every claim?
11. ✅ Did I stay within Phase 2 scope (no frontend, no automation)?
12. ✅ Are my git commits clean with messages?
13. ✅ Am I guessing or do I have evidence?

**If uncertain**: Run tests again, provide more evidence, never guess!

---

## Related Documentation

- `gameplan-300-learning-basic-revised.md` - Full gameplan
- `HANDOFF-LEAD-DEV-PHASE1-COMPLETE.md` - Phase 1 results
- `phase-1-review-summary.md` - Lead Dev's Phase 1 review
- `agent-prompt-template.md` - Template v10.2
- FastAPI documentation - https://fastapi.tiangolo.com/

---

## REMINDER: This Is The Cathedral

**Foundation Stone #1**: Phase 1 complete ✅
**User Controls**: Phase 2 (THIS PROMPT)
**Suggestions UI**: Phase 3 (separate prompt)
**Automation**: Phase 4 (separate prompt)

**Don't Skip Ahead**: Build one solid layer at a time

**API First**: Foundation for frontend (Phase 3)

**User Control**: Before automation (Phase 4)

**Time Lord Way**: Quality over speed, build it right

---

**Status**: Ready for Agent Deployment
**Issue**: #300 - CORE-ALPHA-LEARNING-BASIC
**Phase**: 2 of 6 (User Controls API)
**Scope**: API-only, manual testing
**Estimated Effort**: 2-3 hours
**Priority**: P2 (Alpha Feature)

---

_"Part of a cathedral, not just a random brick shed"_
_"Quality exists outside of time constraints"_
_"Never guess - always verify first!"_
_Building User Controls on Foundation Stone #1 🏗️_
