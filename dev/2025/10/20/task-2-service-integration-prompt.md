# Task 2: Service Integration - Standup API

**Agent**: Claude Code (Programmer)
**Issue**: #162 (CORE-STAND-MODES-API)
**Task**: 2 of 7 - Service Integration
**Sprint**: A4 "Standup Epic"
**Date**: October 19, 2025
**Estimated Effort**: Medium (2 hours)

---

## Mission

Integrate the new REST API endpoints with the existing StandupOrchestrationService, ensuring all 5 generation modes are accessible via API with proper dependency injection and error handling.

**Scope**:
- Connect API routes to StandupOrchestrationService
- Implement proper dependency injection
- Add error handling for service failures
- Format responses for each output type (json, slack, markdown, text)

**NOT in scope**:
- Authentication (Task 3)
- OpenAPI docs (Task 4)
- Testing (Task 6)

---

## Context

- **GitHub Issue**: #162 (CORE-STAND-MODES-API) - Multi-modal API
- **Current State**:
  - ✅ API endpoints created (Task 1 complete)
  - ✅ 5 generation modes working (from #119)
  - ✅ StandupOrchestrationService exists (services/domain/standup_orchestration_service.py)
  - ✅ JWT authentication system found (services/auth/)
- **Target State**: API endpoints connected to orchestration service
- **Dependencies**:
  - StandupOrchestrationService (domain service)
  - Services it depends on (GitHub, Calendar, etc.)
  - JWT authentication (for next task)
- **User Data Risk**: None - read-only operations
- **Infrastructure Verified**: Yes - all services exist from Phase 1

---

## STOP Conditions (EXPANDED TO 17)

If ANY of these occur, STOP and escalate to PM immediately:

1. **Infrastructure doesn't match gameplan** - Service locations different than expected
2. **Method implementation <100% complete** - All 5 modes must be integrated
3. **Pattern already exists in catalog** - Check before creating new patterns
4. **Tests fail for any reason** - Even if "expected" or "minor"
5. **Configuration assumptions needed** - Don't guess service config
6. **GitHub issue missing or unassigned** - Verify #162 still assigned to you
7. **Can't provide verification evidence** - Must show it working with real data
8. **ADR conflicts with approach** - Check ADR-029 for domain service patterns
9. **Resource not found after searching** - If service doesn't exist, STOP
10. **User data at risk** - Though none expected here
11. **Completion bias detected** - Don't claim done without proof
12. **Rationalizing gaps as "minor"** - No placeholders, no "good enough"
13. **GitHub tracking not working** - Issue updates must work
14. **Single agent seems sufficient** - This IS single agent task
15. **Git operations failing** - All commits must work
16. **Server state unexpected** - Verify services are running
17. **UI behavior can't be visually confirmed** - Use curl to test API

**Remember**: STOP means STOP. Don't try to work around it. Ask PM.

---

## Evidence Requirements (CRITICAL - EXPANDED)

### For EVERY Claim You Make:

- **"Integrated with service"** → Show curl output with real generated standup
- **"All 5 modes work"** → Show curl test for each mode
- **"Error handling works"** → Show failure case handling gracefully
- **"Response formatting works"** → Show json, slack, markdown, text outputs
- **"Dependencies injected"** → Show service initialization code
- **"Performance targets met"** → Show generation times <2s

### Completion Bias Prevention (CRITICAL):

- **Never guess! Always verify first!**
- **NO "should work"** - only "here's proof it works"
- **NO "probably fixed"** - only "here's evidence it's fixed"
- **NO assumptions** - only verified facts with terminal output
- **NO rushing to claim done** - evidence first, claims second

### Git Workflow Discipline:

After ANY code changes:
```bash
# Always verify commits
git status
git add [files]
git commit -m "[descriptive message]"
git log --oneline -1  # MANDATORY - show this output
```

### Server State Awareness:

Before claiming integration works:
```bash
# Check what's running
ps aux | grep python
ps aux | grep piper
lsof -i :8001  # Verify port is available or in use correctly

# Test the actual API
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "trifecta", "format": "json"}' | jq '.'
```

---

## Related Documentation

- **resource-map.md** - ALWAYS CHECK FIRST for service locations
- **stop-conditions.md** - When to stop and ask for help
- **anti-80-pattern.md** - Understanding completion bias prevention
- **ADR-029** - Domain Service Mediation Architecture
- **Pattern-014** - Error Handling Pattern (API Contract)
- **Phase 1 work** - Issue #119 for service details

---

## REMINDER: Methodology Cascade

This prompt carries our methodology forward. You are responsible for:

1. **Verifying infrastructure FIRST** (no wrong assumptions)
2. **Ensuring 100% completeness** (no 80% pattern)
3. **Checking what exists NEXT** (no reinventing)
4. **Preserving user data ALWAYS** (though none at risk here)
5. **Checking resource-map.md FIRST** (for service locations)
6. **Following ALL verification requirements**
7. **Providing evidence for EVERY claim**
8. **Creating method enumeration tables** (5 modes = 100%)
9. **Stopping when assumptions are needed**
10. **Maintaining architectural integrity**
11. **Updating GitHub with progress** (in descriptions!)
12. **Creating session logs in .md format**
13. **Verifying git commits with log output**
14. **Checking server state before/after changes**
15. **Providing visual proof for API claims** (curl outputs)
16. **Never guessing - always verifying first!**
17. **Never rationalizing incompleteness!**

**Infrastructure mismatches and completion bias are session failures. Evidence is mandatory.**

---

## Task Requirements

### 1. Verify Infrastructure (BEFORE Implementation)

**Location Verification**:
```bash
# Check service exists
ls -la services/domain/standup_orchestration_service.py
cat services/domain/standup_orchestration_service.py | head -20

# Check what methods it has
grep "async def" services/domain/standup_orchestration_service.py

# Check API routes file
ls -la web/api/routes/standup.py
cat web/api/routes/standup.py | head -50
```

**Expected Services**:
- StandupOrchestrationService (from #119)
- Methods: generate_standup, generate_with_documents, generate_with_issues, generate_with_calendar, generate_with_trifecta

**If NOT found**: STOP (condition #1 or #9)

---

### 2. Understand Service Dependencies

**Investigation Required**:
```bash
# What does StandupOrchestrationService need?
grep "__init__" services/domain/standup_orchestration_service.py -A 10

# What services does it depend on?
grep "self\." services/domain/standup_orchestration_service.py | head -20
```

**Document findings**:
- What parameters does __init__ take?
- Which services are required vs optional?
- How are they currently instantiated?

**If unclear**: STOP (condition #5 - configuration assumptions)

---

### 3. Implement Dependency Injection

**In web/api/routes/standup.py**:

```python
from fastapi import APIRouter, Depends, HTTPException
from services.domain.standup_orchestration_service import StandupOrchestrationService
from services.infrastructure.config.config_service import ConfigService

# Dependency injection pattern
async def get_orchestration_service() -> StandupOrchestrationService:
    """
    Provide orchestration service with all dependencies.

    This follows ADR-029 domain service mediation pattern.
    """
    # Get config service
    config = ConfigService()

    # Initialize all required services
    # (Based on what you found in step 2)
    github_service = ...  # As needed
    calendar_service = ...  # As needed
    # etc.

    return StandupOrchestrationService(
        # Pass required dependencies
    )

# Use in endpoint
@router.post("/generate")
async def generate_standup(
    request: StandupRequest,
    orchestration: StandupOrchestrationService = Depends(get_orchestration_service)
):
    """Generate standup with injected service"""
    # Implementation here
```

**Evidence Required**:
- Show the __init__ signature
- Show your dependency injection code
- Show it compiles without errors

---

### 4. Connect API Routes to Service Methods

**For each mode, call appropriate service method**:

```python
@router.post("/generate", response_model=StandupResponse)
async def generate_standup(
    request: StandupRequest,
    orchestration: StandupOrchestrationService = Depends(get_orchestration_service)
):
    """Generate standup in requested mode"""

    try:
        # Route to appropriate generation method based on mode
        if request.mode == "standard":
            result = await orchestration.generate_standup(
                user_id=request.user_id or "default"
            )
        elif request.mode == "documents":
            result = await orchestration.generate_with_documents(
                user_id=request.user_id or "default"
            )
        elif request.mode == "issues":
            result = await orchestration.generate_with_issues(
                user_id=request.user_id or "default"
            )
        elif request.mode == "calendar":
            result = await orchestration.generate_with_calendar(
                user_id=request.user_id or "default"
            )
        elif request.mode == "trifecta":
            result = await orchestration.generate_with_trifecta(
                user_id=request.user_id or "default"
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid mode")

        # Format response
        formatted = await format_standup_content(result, request.format)

        return StandupResponse(
            success=True,
            standup={
                "content": formatted,
                "format": request.format,
                "mode": request.mode
            },
            metadata={
                "generated_at": time.time(),
                # ... other metadata
            },
            performance_metrics={
                "generation_time_ms": calculate_time(),
                # ... other metrics
            }
        )

    except Exception as e:
        logger.error(f"Standup generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Standup generation failed: {str(e)}"
        )
```

**Method Enumeration Table** (REQUIRED):

| Mode | Service Method | Status |
|------|----------------|--------|
| standard | generate_standup() | ☐ |
| documents | generate_with_documents() | ☐ |
| issues | generate_with_issues() | ☐ |
| calendar | generate_with_calendar() | ☐ |
| trifecta | generate_with_trifecta() | ☐ |

**Target**: 5/5 = 100% ✅

**If <100%**: STOP (condition #2)

---

### 5. Implement Response Formatting

**Create format helper function**:

```python
async def format_standup_content(
    result: dict,
    format_type: str
) -> Union[str, dict]:
    """
    Format standup content based on requested format.

    Args:
        result: Raw standup data from orchestration service
        format_type: One of: json, slack, markdown, text

    Returns:
        Formatted content in requested type
    """
    if format_type == "json":
        # Return structured dict
        return result

    elif format_type == "slack":
        # Format for Slack (from CLI if exists)
        return format_as_slack(result)

    elif format_type == "markdown":
        # Format as markdown
        return format_as_markdown(result)

    elif format_type == "text":
        # Format as plain text
        return format_as_text(result)

    else:
        raise ValueError(f"Unknown format: {format_type}")
```

**Format Helper Functions**:

```python
def format_as_slack(result: dict) -> str:
    """Format standup for Slack"""
    # Check if CLI has this already
    # Look in cli/commands/standup.py for existing formatting
    # Reuse if possible, don't duplicate
    pass

def format_as_markdown(result: dict) -> str:
    """Format standup as markdown"""
    # Create clean markdown output
    pass

def format_as_text(result: dict) -> str:
    """Format standup as plain text"""
    # Create plain text output
    pass
```

**Evidence Required**:
- Show example output for each format
- Show it renders correctly

---

### 6. Add Error Handling

**Follow Pattern-014** (Error Handling Pattern):

```python
# Service failures
try:
    result = await orchestration.generate_with_trifecta(user_id)
except ServiceUnavailableError as e:
    raise HTTPException(
        status_code=503,
        detail={
            "error": "Service temporarily unavailable",
            "message": "Standup generation is temporarily unavailable. Please try again in a moment.",
            "technical_details": str(e) if DEBUG else None
        }
    )
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise HTTPException(
        status_code=500,
        detail={
            "error": "Generation failed",
            "message": "Unable to generate standup. Please try again.",
            "technical_details": str(e) if DEBUG else None
        }
    )
```

**Error Scenarios to Handle**:
- Invalid mode (400)
- Service unavailable (503)
- Unexpected errors (500)
- User-friendly messages for all

---

## Verification Steps

### Step 1: Start the API Server

```bash
# Make sure no other instance running
lsof -i :8001

# If something is running, stop it first
# Then start the API
uvicorn main:app --reload --port 8001

# Verify it started
curl http://localhost:8001/api/standup/health
```

**Expected**: `{"status": "healthy"}`

**If fails**: STOP (condition #16 - server state)

---

### Step 2: Test Each Mode

```bash
# Test standard mode
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "standard", "format": "json"}' | jq '.'

# Test documents mode
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "documents", "format": "json"}' | jq '.'

# Test issues mode
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "issues", "format": "json"}' | jq '.'

# Test calendar mode
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "calendar", "format": "json"}' | jq '.'

# Test trifecta mode
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "trifecta", "format": "json"}' | jq '.'
```

**Evidence Required**: Show curl output for ALL 5 modes

**Expected**:
- All return 200 OK
- All return valid JSON
- All contain standup content
- Generation time <2s each

**If any fail**: STOP and investigate (condition #4 or #7)

---

### Step 3: Test Each Format

```bash
# JSON format
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "trifecta", "format": "json"}' | jq '.'

# Slack format
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "trifecta", "format": "slack"}'

# Markdown format
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "trifecta", "format": "markdown"}'

# Text format
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "trifecta", "format": "text"}'
```

**Evidence Required**: Show output for ALL 4 formats

**Expected**: Different formatting for each type

---

### Step 4: Test Error Handling

```bash
# Invalid mode
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "invalid", "format": "json"}' -v

# Invalid format
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "standard", "format": "invalid"}' -v
```

**Evidence Required**: Show error responses

**Expected**:
- 400 or 422 status codes
- User-friendly error messages
- No stack traces exposed

---

### Step 5: Performance Verification

```bash
# Time the generation
time curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "trifecta", "format": "json"}' | jq '.performance_metrics'
```

**Evidence Required**: Show generation times

**Expected**: All modes <2s (target from #119)

**If slower**: Document but don't block (optimization for later)

---

## Success Criteria

Task 2 is complete when:

- [ ] StandupOrchestrationService location verified
- [ ] Service dependencies understood and documented
- [ ] Dependency injection implemented correctly
- [ ] All 5 modes integrated (5/5 = 100%)
- [ ] All 4 formats working correctly
- [ ] Error handling implemented (Pattern-014)
- [ ] All 5 modes tested with curl (evidence provided)
- [ ] All 4 formats tested (evidence provided)
- [ ] Error cases tested (evidence provided)
- [ ] Performance <2s verified (evidence provided)
- [ ] Code committed with git log output shown
- [ ] Session log updated in .md format
- [ ] Method enumeration table shows 100%
- [ ] No placeholders or "TODO" markers
- [ ] No assumptions made without verification

---

## Self-Check Before Claiming Complete

### Ask Yourself:

1. **Does infrastructure match what Phase 1 established?** (StandupOrchestrationService exists where expected)
2. **Is my implementation 100% complete?** (5/5 modes = 100%)
3. **Did I provide terminal evidence for every claim?** (curl outputs for all modes/formats)
4. **Can another agent verify my work independently?** (Clear evidence trail)
5. **Did I preserve all user configuration?** (Not applicable - no user config)
6. **Am I claiming work done that I didn't actually do?** (All modes actually tested)
7. **Is there a gap between my claims and reality?** (Evidence matches claims)
8. **Did I verify git commits with log output?** (Shown `git log --oneline -1`)
9. **Did I check server state after changes?** (Shown API actually running)
10. **For API claims, do I have curl proof?** (All endpoints tested)
11. **Am I rationalizing gaps as "minor" or "optional"?** (No gaps exist)
12. **Do I have objective metrics or subjective impressions?** (Actual curl outputs)
13. **Am I guessing or do I have evidence?** (Evidence for everything)

### If Uncertain About Anything:

- Run verification commands yourself
- Show actual output, not expected output
- Create method enumeration table (5/5)
- Acknowledge what's not done yet
- Ask for help if stuck
- **Never guess - always verify!**

---

## Files to Modify

### Primary File

- `web/api/routes/standup.py` - Add service integration

### Supporting Code (If Needed)

- May need format helpers (could be in utils)
- Error handling utilities (use Pattern-014)

### Session Log

- `dev/2025/10/19/HHMM-prog-code-log.md` - Your session log

---

## Deliverables

### 1. Code Changes

**Modified**:
- web/api/routes/standup.py (service integration + formatting)

**Evidence**:
```bash
git diff web/api/routes/standup.py
git log --oneline -1
```

### 2. Method Completeness

**Enumeration Table**:

| Mode | Integrated | Tested | Evidence |
|------|-----------|--------|----------|
| standard | ✅ | ✅ | curl output shown |
| documents | ✅ | ✅ | curl output shown |
| issues | ✅ | ✅ | curl output shown |
| calendar | ✅ | ✅ | curl output shown |
| trifecta | ✅ | ✅ | curl output shown |

**Target**: 5/5 = 100% ✅

### 3. Evidence Report

**Terminal outputs showing**:
- Service integration working
- All 5 modes tested
- All 4 formats tested
- Error handling tested
- Performance verified
- Git commit confirmed

### 4. Session Log

**In dev/2025/10/19/HHMM-prog-code-log.md**:
- Infrastructure findings
- Service dependencies discovered
- Integration approach
- All test outputs
- Performance results
- Any issues encountered
- Time spent

---

## Constraints & Requirements

### For Claude Code:

1. **Infrastructure verified**: Confirm service exists before coding
2. **100% method compatibility**: All 5 modes integrated (5/5)
3. **Check existing first**: Look for existing format helpers in CLI
4. **Evidence Required**: Every claim needs terminal output proof
5. **Verification First**: Check service signature before implementing
6. **Stop Conditions**: Stop immediately if any of 17 triggers occurs
7. **Session Log Format**: Must be .md not .txt
8. **Git Discipline**: Verify all commits with log output
9. **Server Awareness**: Test with actual running API
10. **Objective metrics**: 5/5 modes = 100% (not "mostly done")

---

## Cross-Validation Preparation

Leave clear markers for verification (Task 6 will test this):

**What to document**:
- Service location and signature
- Dependency injection approach
- Method enumeration table (5/5 = 100%)
- Test commands used (curl commands)
- Expected outputs for each mode/format
- Performance metrics observed
- Any edge cases found

**Evidence format**:
```bash
# Mode: standard, Format: json
$ curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "standard", "format": "json"}' | jq '.'
{
  "success": true,
  "standup": { ... },
  "metadata": { ... },
  "performance_metrics": {
    "generation_time_ms": 892
  }
}
```

---

## Example Evidence Format

```bash
# Show service exists
$ ls -la services/domain/standup_orchestration_service.py
-rw-r--r-- 1 user group 4821 Oct 19 15:00 services/domain/standup_orchestration_service.py

# Show methods available
$ grep "async def" services/domain/standup_orchestration_service.py
async def generate_standup(self, user_id: str) -> dict:
async def generate_with_documents(self, user_id: str) -> dict:
async def generate_with_issues(self, user_id: str) -> dict:
async def generate_with_calendar(self, user_id: str) -> dict:
async def generate_with_trifecta(self, user_id: str) -> dict

# Show integration works
$ curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "trifecta", "format": "json"}' | jq '.performance_metrics'
{
  "generation_time_ms": 1047,
  "target_time_ms": 2000,
  "time_saved_minutes": 15
}

# Show git commit
$ git log --oneline -1
abc1234 feat(standup-api): integrate with StandupOrchestrationService

# Show method completeness
5 modes integrated / 5 modes total = 100% COMPLETE ✅
```

---

## Remember

- **This is about getting a WIN** - You can do this!
- **Evidence = confidence** - Show your work, feel proud
- **STOP conditions protect you** - Use them without hesitation
- **100% means 100%** - But you're integrating 5 things that already work!
- **PM is rooting for you** - We all want you to succeed

**You've got this!** The hard work is done (Phase 1). Now we're just wiring it up properly. 🎯

---

*Template Version: 8.0*
*Based on: agent-prompt-template.md*
*All methodology sections included*
*Task-specific sections customized*
*Ready for deployment*
