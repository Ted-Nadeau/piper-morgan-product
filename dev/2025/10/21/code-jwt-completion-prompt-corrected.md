# Implementation Prompt: CORE-USERS-JWT - Completion (Corrected)

**Agent**: Claude Code (Programmer)
**Task**: Complete JWT token blacklist implementation
**Issue**: #227 CORE-USERS-JWT
**Date**: October 21, 2025, 4:24 PM
**Current Status**: 5 of 9 phases complete (60%)

---

## CRITICAL: What Just Happened

**You completed**:
- ✅ Phase 1: TokenBlacklist Class (services/auth/token_blacklist.py)
- ✅ Phase 2: Database Model (TokenBlacklist model added)
- ✅ Phase 3: JWT Service Integration (blacklist checks added)
- ✅ Phase 5: Middleware Verification (TokenRevoked handling confirmed)
- ✅ Phase 7: Testing (17 tests passing)

**You need to complete**:
- ❌ Phase 4: Logout Endpoint Integration
- ❌ Phase 6: Background Cleanup Task
- ❌ Phase 8: Performance Testing
- ❌ Phase 9: Database Migration (blocked by Docker)

**You were correct**: PostgreSQL should be on port 5433.

**Investigation revealed**: Docker Desktop is not running. PostgreSQL container unavailable.

**Solution**: Start Docker, then complete remaining phases.

---

## PostgreSQL Investigation Results

**From Cursor's investigation** (`postgresql-configuration-investigation.md`):

**Configuration Status**: ✅ PERFECT
- Port 5433 everywhere (.env, docker-compose.yml, alembic.ini)
- All config files consistent
- 13 existing Alembic migrations
- Database models complete

**Infrastructure Status**: ❌ NOT RUNNING
- Docker daemon not running
- No PostgreSQL on any port
- Container not started

**Solution**:
```bash
# Start Docker Desktop
open -a Docker

# Wait for Docker to initialize
sleep 30

# Start PostgreSQL container
docker-compose up -d postgres

# Verify running
docker ps | grep postgres
# Should show: piper-postgres   postgres:15   Up X minutes (healthy)
```

---

## MANDATORY: Process Corrections

### 1. You Do NOT Have Time Constraints

**The original 2.5 hour estimate was NOT a deadline.**

- ❌ Do NOT rush to finish
- ❌ Do NOT skip phases to save time
- ❌ Do NOT make "time-based" decisions
- ✅ Work systematically through ALL phases
- ✅ Ask PM if blocked
- ✅ Complete 100% of work

### 2. To-Do List is a Contract

**You CANNOT unilaterally remove items from your to-do list.**

**What happened**: You removed phases 4, 6, 8 from your list without approval.

**What should happen**:
- Keep ALL phases on list
- If blocked, STOP and ask PM
- If need to skip, STOP and ask PM
- Only remove with explicit PM approval

### 3. Phases Must Be 100% Complete

**"60% done" is NOT "done".**

**Before claiming ANY phase complete**:

1. **Check for gaps**:
   - Any tests skipped? → STOP, ask PM
   - Any dependencies missing? → STOP, ask PM
   - Any infrastructure unavailable? → STOP, ask PM
   - Any work items incomplete? → STOP, ask PM

2. **If ANY gap exists**:
   - Document the gap clearly
   - List options to resolve
   - **ASK PM for decision**
   - **WAIT for PM response**
   - Do NOT proceed until resolved

3. **Only after gap resolved**:
   - Complete the work 100%
   - Verify with tests/evidence
   - THEN mark phase complete

---

## Your Mission: Complete Remaining 4 Phases

### Phase 0: Start Docker and PostgreSQL

**Do this FIRST**:

```bash
# Start Docker Desktop
echo "Starting Docker Desktop..."
open -a Docker

# Wait for Docker to initialize
echo "Waiting 30 seconds for Docker to start..."
sleep 30

# Start PostgreSQL container
echo "Starting PostgreSQL container..."
docker-compose up -d postgres

# Verify PostgreSQL is running
echo "Verifying PostgreSQL..."
docker ps | grep postgres

# Test connection
nc -zv localhost 5433
```

**Success criteria**:
- Docker running: ✅
- PostgreSQL container up: ✅
- Port 5433 responding: ✅

**If ANY check fails**:
1. STOP immediately
2. Show me the exact error output
3. Ask: "What should I do?"
4. Wait for my response

---

### Phase 4: Logout Endpoint Integration

**File**: `web/routes/auth.py` or `web/app.py` (find existing auth routes)

**Task**: Add token revocation to logout endpoint

**Step 1**: Find logout endpoint
```bash
# Search for existing logout endpoint
grep -r "logout\|signout" web/ --include="*.py"

# If not found, search for auth routes
find web/ -name "*auth*" -o -name "*route*"
```

**Step 2**: Add blacklist integration

**If logout endpoint exists**:
```python
@router.post("/logout")
async def logout(
    token: str = Depends(get_current_token),
    jwt_service: JWTService = Depends(get_jwt_service),
    current_user: User = Depends(get_current_user)
):
    """
    Logout user and revoke token.
    """
    try:
        # Revoke the token
        success = await jwt_service.revoke_token(
            token=token,
            reason="logout",
            user_id=current_user.id
        )

        if success:
            logger.info(f"User {current_user.id} logged out successfully")
            return {"message": "Logged out successfully"}
        else:
            logger.error(f"Failed to revoke token for user {current_user.id}")
            return {"message": "Logout completed but token revocation failed"}

    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Logout failed")
```

**If logout endpoint does NOT exist**:
1. STOP immediately
2. Tell me: "No logout endpoint found. Should I create one or skip Phase 4?"
3. Wait for my response

**Success criteria**:
- [ ] Logout endpoint calls jwt_service.revoke_token()
- [ ] Error handling implemented
- [ ] Logging added
- [ ] Manual test successful (show curl output)

**Evidence required**:
```bash
# Show the code change
git diff web/routes/auth.py  # or wherever logout is

# Show it works (manual test)
curl -X POST http://localhost:8001/auth/logout \
  -H "Authorization: Bearer test-token"
```

**STOP conditions**:
- Logout endpoint doesn't exist → Ask PM
- Can't find auth routes → Ask PM
- Test fails → Ask PM

---

### Phase 6: Background Cleanup Task

**File**: `services/background/cleanup_tasks.py` (CREATE if needed)

**Task**: Create background task to clean expired blacklist entries

**Step 1**: Check if background tasks exist
```bash
# Search for existing background task infrastructure
find . -name "*background*" -o -name "*task*" -o -name "*scheduler*" | grep -v __pycache__

# Search for asyncio task patterns
grep -r "asyncio.create_task\|background.*task" services/ --include="*.py"
```

**Step 2**: Create cleanup task

```python
"""
Background Tasks for Maintenance
"""
import asyncio
import logging
from datetime import timedelta
from services.auth.token_blacklist import TokenBlacklist

logger = logging.getLogger(__name__)


async def cleanup_expired_blacklist_tokens(
    blacklist: TokenBlacklist,
    interval_hours: int = 24
):
    """
    Background task to clean up expired blacklist entries.

    Runs every 24 hours. Redis entries expire automatically via TTL.
    This only cleans database fallback entries.
    """
    logger.info(f"Starting blacklist cleanup task (every {interval_hours}h)")

    while True:
        try:
            await asyncio.sleep(interval_hours * 3600)

            count = await blacklist.remove_expired()
            logger.info(f"Blacklist cleanup removed {count} expired entries")

        except Exception as e:
            logger.error(f"Blacklist cleanup error: {e}")
            await asyncio.sleep(300)  # 5 min before retry


async def start_background_tasks(blacklist: TokenBlacklist):
    """Start all background tasks"""
    asyncio.create_task(
        cleanup_expired_blacklist_tokens(blacklist, interval_hours=24)
    )
    logger.info("Background tasks started")
```

**Step 3**: Integrate with application startup

**Find app startup** (likely in `main.py` or `app.py`):
```bash
grep -r "@app.on_event\|lifespan\|startup" . --include="*.py" | grep -v __pycache__
```

**Add startup hook**:
```python
@app.on_event("startup")
async def startup_event():
    # ... existing startup code

    # Start background tasks
    blacklist = app.state.token_blacklist  # or however it's accessed
    await start_background_tasks(blacklist)
```

**Success criteria**:
- [ ] Cleanup task created
- [ ] Integrated with app startup
- [ ] Proper error handling
- [ ] Logging for monitoring

**Evidence required**:
```bash
# Show the file was created
ls -la services/background/cleanup_tasks.py

# Show startup integration
grep -A 5 "start_background_tasks" main.py  # or app.py

# Show it doesn't crash on startup
python -c "from services.background.cleanup_tasks import cleanup_expired_blacklist_tokens; print('OK')"
```

**STOP conditions**:
- Can't find app startup → Ask PM
- Background task patterns unclear → Ask PM
- Integration point not obvious → Ask PM

---

### Phase 8: Performance Testing

**File**: `tests/performance/test_blacklist_performance.py` (CREATE)

**Task**: Verify blacklist checks meet <5ms target

**Create performance test**:

```python
"""
Performance tests for JWT token blacklist
Target: <5ms average for blacklist checks
"""
import pytest
import time
from statistics import mean
from datetime import datetime, timedelta
from services.auth.token_blacklist import TokenBlacklist


@pytest.mark.asyncio
@pytest.mark.performance
async def test_blacklist_check_performance(blacklist):
    """Should check blacklist in <5ms average"""
    token_id = "perf-test-token"

    # Add to blacklist
    await blacklist.add(
        token_id=token_id,
        reason="test",
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )

    # Measure 100 lookups
    times = []
    for _ in range(100):
        start = time.perf_counter()
        await blacklist.is_blacklisted(token_id)
        elapsed = (time.perf_counter() - start) * 1000  # Convert to ms
        times.append(elapsed)

    avg_time = mean(times)
    max_time = max(times)
    min_time = min(times)

    print(f"\nBlacklist Check Performance:")
    print(f"  Average: {avg_time:.2f}ms")
    print(f"  Min: {min_time:.2f}ms")
    print(f"  Max: {max_time:.2f}ms")
    print(f"  Target: <5.00ms")

    # Assert performance target
    assert avg_time < 5.0, f"Average time {avg_time:.2f}ms exceeds 5ms target"

    # Also check max time isn't too bad
    assert max_time < 10.0, f"Max time {max_time:.2f}ms exceeds 10ms threshold"


@pytest.mark.asyncio
@pytest.mark.performance
async def test_blacklist_add_performance(blacklist):
    """Should add tokens to blacklist quickly"""
    times = []

    for i in range(50):
        token_id = f"perf-add-test-{i}"

        start = time.perf_counter()
        await blacklist.add(
            token_id=token_id,
            reason="test",
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)

    avg_time = mean(times)

    print(f"\nBlacklist Add Performance:")
    print(f"  Average: {avg_time:.2f}ms")
    print(f"  Target: <10.00ms")

    assert avg_time < 10.0, f"Average add time {avg_time:.2f}ms too slow"
```

**Run performance tests**:
```bash
# Ensure directory exists
mkdir -p tests/performance

# Run performance tests
pytest tests/performance/test_blacklist_performance.py -v -m performance
```

**Success criteria**:
- [ ] Performance tests created
- [ ] Tests pass
- [ ] Average lookup time <5ms
- [ ] Average add time <10ms

**Evidence required**:
```bash
# Show test output with timing
pytest tests/performance/test_blacklist_performance.py -v -s -m performance
```

**STOP conditions**:
- Performance tests fail → Show me results, ask what to do
- Can't achieve <5ms → Show me results, ask what to do
- Redis unavailable for testing → Ask PM

---

### Phase 9: Database Migration

**Task**: Create and apply Alembic migration for token_blacklist table

**Now that Docker is running**:

```bash
# Generate migration
cd /Users/xian/Development/piper-morgan
alembic revision --autogenerate -m "Add token_blacklist table for CORE-USERS-JWT"

# Review the generated migration
cat alembic/versions/*_add_token_blacklist_table*.py

# Apply migration
alembic upgrade head

# Verify table exists
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d token_blacklist"
```

**Success criteria**:
- [ ] Migration file generated
- [ ] Migration applied successfully
- [ ] Table exists in database
- [ ] Indexes created

**Evidence required**:
```bash
# Show migration was created
ls -la alembic/versions/*token_blacklist*

# Show migration applied
alembic current

# Show table exists
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d token_blacklist"
```

**STOP conditions**:
- Docker/PostgreSQL won't start → Show me error, ask what to do
- Migration generation fails → Show me error, ask what to do
- Migration apply fails → Show me error, ask what to do

---

## Phase Completion Checklist

**After completing each phase**, verify:

1. **Work is 100% done**:
   - [ ] All code written
   - [ ] All tests passing (NO skips)
   - [ ] All files created/modified
   - [ ] All evidence captured

2. **No gaps exist**:
   - [ ] No missing dependencies
   - [ ] No configuration issues
   - [ ] No infrastructure problems
   - [ ] No test failures

3. **Evidence provided**:
   - [ ] Terminal output for all commands
   - [ ] Git diffs for code changes
   - [ ] Test results showing pass
   - [ ] Manual test results if applicable

**If ANY item unchecked**: STOP and ask PM before proceeding to next phase.

---

## Final Deliverable: Complete Evidence Document

**After ALL 9 phases complete**, create:

`dev/2025/10/21/core-users-jwt-implementation-evidence-final.md`

**Include**:

### Files Created
```
services/auth/token_blacklist.py (X lines)
services/background/cleanup_tasks.py (X lines)
tests/performance/test_blacklist_performance.py (X lines)
Total new: X lines
```

### Files Modified
```
services/database/models.py (+X lines)
services/auth/jwt_service.py (+X lines)
web/routes/auth.py (+X lines)
Total modified: X lines
```

### Database Migration
```
alembic revision: [hash] - "Add token_blacklist table"
alembic upgrade head - SUCCESS
Table 'token_blacklist' exists with indexes
```

### Test Results
```
[paste complete pytest output showing ALL tests passing]
```

### Performance Results
```
Blacklist check: X.XXms average (target <5ms)
Blacklist add: X.XXms average (target <10ms)
✅ Performance targets met
```

### Manual Testing
```
[paste curl output showing logout works]
[paste evidence that token is revoked]
```

---

## Critical Reminders

### 1. No Time Pressure
- Work is complete when it's 100% done
- NOT when 2.5 hours have passed
- Take the time needed to do it right

### 2. Ask When Blocked
- Docker won't start? → Ask PM
- Endpoint doesn't exist? → Ask PM
- Tests fail? → Ask PM
- Configuration unclear? → Ask PM

### 3. Do NOT Skip Phases
- ALL 4 remaining phases are required
- Do NOT remove from to-do list
- Do NOT mark complete without evidence
- Do NOT rationalize gaps

### 4. Provide Evidence
- Show terminal output for everything
- Prove tests pass (no "should work")
- Prove files exist (ls -la)
- Prove code works (manual tests)

### 5. 100% Means 100%
- 9/9 phases = complete
- 8/9 phases = NOT complete
- 60% = NOT complete
- Only 100% is acceptable

---

## Communication Protocol

**When blocked**:
```
⚠️ BLOCKED - Phase X

Problem: [Describe issue]
What I tried: [Commands run]
Error output: [Paste exact error]

Options:
1. [Option to resolve]
2. [Option to resolve]
3. [Option to resolve]

Waiting for PM guidance.
```

**When phase complete**:
```
✅ Phase X Complete

Evidence:
[Terminal output]
[Test results]
[Git diff]

Ready to proceed to Phase Y.
```

**When all phases complete**:
```
✅ ALL 9 PHASES COMPLETE

Summary:
- Phase 1: ✅ TokenBlacklist class
- Phase 2: ✅ Database model
- Phase 3: ✅ JWT integration
- Phase 4: ✅ Logout endpoint
- Phase 5: ✅ Middleware verification
- Phase 6: ✅ Background cleanup
- Phase 7: ✅ Testing (X tests passing)
- Phase 8: ✅ Performance (X.XXms)
- Phase 9: ✅ Migration applied

Evidence document: dev/2025/10/21/core-users-jwt-implementation-evidence-final.md

Ready for PM review and issue closure.
```

---

## Success Criteria for Completion

Implementation is complete when:

- [x] Docker started successfully
- [x] PostgreSQL running on port 5433
- [x] Phase 4: Logout endpoint integrated
- [x] Phase 6: Background cleanup task created
- [x] Phase 8: Performance tests passing (<5ms)
- [x] Phase 9: Database migration applied
- [x] ALL tests passing (NO skipped tests)
- [x] Evidence document complete
- [x] Manual testing successful
- [x] NO breaking changes

**Remember**: Only claim complete when ALL boxes checked!

---

**You've got this! Start with Phase 0 (Docker), then systematically complete phases 4, 6, 8, 9. Ask if blocked. Provide evidence for everything. 100% completion required.**

**Good luck! 🚀**
