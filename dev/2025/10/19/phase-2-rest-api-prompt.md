# Phase 2: REST API for Multi-Modal Standup Generation

**Agent**: Claude Code (Programmer)
**Issue**: #162 (CORE-STAND-MODES-API)
**Sprint**: A4 "Standup Epic"
**Phase**: 2 - REST API Implementation
**Date**: October 19, 2025, 4:00 PM
**Duration**: 1.5 days estimated
**Dependencies**: #119 (CORE-STAND-FOUND) ✅ COMPLETE

---

## Mission

Expose the 5 existing standup generation modes via REST API endpoints, enabling programmatic access with proper authentication, error handling, and OpenAPI documentation.

**Foundation Complete**: Issue #119 verified all 5 generation modes working with real data (800-1000ms performance).

---

## Current Implementation Status (90%+ Complete!)

**From Phase 1 Discovery**:

✅ **5 Generation Modes Implemented** (services/features/morning_standup.py):
1. `generate_standup()` - Standard mode with session context
2. `generate_with_documents()` - Document-focused standup
3. `generate_with_issues()` - Issue Intelligence integration
4. `generate_with_calendar()` - Calendar-aware standup
5. `generate_with_trifecta()` - All integrations combined

✅ **StandupOrchestrationService** (services/domain/standup_orchestration_service.py):
- DDD-compliant domain service
- All integrations working with real data
- Performance: 800-1000ms (beats <2s target)

✅ **CLI Implementation** (cli/commands/standup.py - 372 lines):
- Beautiful colored terminal output
- Performance tracking
- Time savings calculation
- Multiple format options (text, slack)

**What's Missing**: REST API endpoints to expose this functionality

---

## Work Required

### Task 1: API Endpoint Design (2 hours)

**Create**: `web/api/routes/standup.py` (new file)

**Endpoint Structure**:

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, Literal
from services.domain.standup_orchestration_service import StandupOrchestrationService
from services.auth import get_current_user  # Existing auth pattern

router = APIRouter(prefix="/api/standup", tags=["standup"])

# Request/Response Models
class StandupRequest(BaseModel):
    """Request model for standup generation"""
    mode: Literal["standard", "documents", "issues", "calendar", "trifecta"] = Field(
        default="standard",
        description="Generation mode to use"
    )
    format: Literal["json", "slack", "markdown", "text"] = Field(
        default="json",
        description="Output format"
    )
    user_id: Optional[str] = Field(
        default=None,
        description="User ID (from auth if not provided)"
    )

class StandupResponse(BaseModel):
    """Response model for standup generation"""
    success: bool
    standup: dict
    metadata: dict
    performance_metrics: dict

# Endpoints
@router.post("/generate", response_model=StandupResponse)
async def generate_standup(
    request: StandupRequest,
    current_user = Depends(get_current_user)
):
    """
    Generate a standup report in the specified mode and format.

    Modes:
    - standard: Basic standup with session context
    - documents: Document-focused standup
    - issues: Issue Intelligence integration
    - calendar: Calendar-aware standup
    - trifecta: All integrations combined

    Formats:
    - json: Structured JSON response
    - slack: Slack-formatted text
    - markdown: Markdown formatted text
    - text: Plain text format
    """
    # Implementation here
    pass

@router.get("/modes", response_model=list[str])
async def list_available_modes():
    """List all available generation modes"""
    return ["standard", "documents", "issues", "calendar", "trifecta"]

@router.get("/formats", response_model=list[str])
async def list_available_formats():
    """List all available output formats"""
    return ["json", "slack", "markdown", "text"]

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "standup-api"}
```

**Key Patterns to Follow** (from Pattern-014):
- Centralized error handling
- Proper HTTP status codes
- User-friendly error messages
- Technical details for debugging
- Consistent response format

---

### Task 2: Service Integration (2 hours)

**Integrate with StandupOrchestrationService**:

```python
# In generate_standup endpoint
from services.domain.standup_orchestration_service import StandupOrchestrationService
import time

@router.post("/generate", response_model=StandupResponse)
async def generate_standup(
    request: StandupRequest,
    current_user = Depends(get_current_user)
):
    """Generate standup report"""
    start_time = time.time()

    try:
        # Get user_id from auth or request
        user_id = request.user_id or current_user.id

        # Initialize orchestration service
        orchestration = StandupOrchestrationService(
            github_domain_service=...,  # From dependencies
            calendar_domain_service=...,
            # ... other services
        )

        # Route to appropriate generation method
        if request.mode == "standard":
            result = await orchestration.generate_standup(user_id)
        elif request.mode == "documents":
            result = await orchestration.generate_with_documents(user_id)
        elif request.mode == "issues":
            result = await orchestration.generate_with_issues(user_id)
        elif request.mode == "calendar":
            result = await orchestration.generate_with_calendar(user_id)
        elif request.mode == "trifecta":
            result = await orchestration.generate_with_trifecta(user_id)

        # Format response based on request.format
        formatted_content = format_standup_content(result, request.format)

        # Calculate performance metrics
        generation_time = (time.time() - start_time) * 1000  # ms

        return StandupResponse(
            success=True,
            standup={
                "content": formatted_content,
                "format": request.format,
                "mode": request.mode
            },
            metadata={
                "user_id": user_id,
                "generated_at": time.time(),
                "services_used": result.get("services_used", [])
            },
            performance_metrics={
                "generation_time_ms": generation_time,
                "target_time_ms": 2000,
                "time_saved_minutes": 15
            }
        )

    except Exception as e:
        # Follow Pattern-014 error handling
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Standup generation failed",
                "message": "Unable to generate standup. Please try again.",
                "technical_details": str(e) if DEBUG else None
            }
        )

def format_standup_content(result: dict, format_type: str) -> str:
    """Format standup content based on requested format"""
    if format_type == "json":
        return result  # Already structured
    elif format_type == "slack":
        # Use existing Slack formatting from CLI
        return format_for_slack(result)
    elif format_type == "markdown":
        return format_as_markdown(result)
    elif format_type == "text":
        return format_as_text(result)
```

---

### Task 3: Authentication Integration (1 hour)

**Use Existing Auth Patterns**:

```python
# Assuming auth pattern exists in services/auth.py or similar
from services.auth import get_current_user, UserContext

@router.post("/generate", response_model=StandupResponse)
async def generate_standup(
    request: StandupRequest,
    current_user: UserContext = Depends(get_current_user)
):
    """
    Generate standup with authentication.

    Authentication via:
    - Bearer token in Authorization header
    - API key in X-API-Key header
    - Session cookie
    """
    # User is already authenticated via Depends(get_current_user)
    user_id = request.user_id or current_user.id

    # Proceed with generation...
```

**Error Handling for Auth**:

```python
# 401 Unauthorized
if not current_user:
    raise HTTPException(
        status_code=401,
        detail={
            "error": "Authentication required",
            "message": "Please provide valid authentication credentials."
        }
    )

# 403 Forbidden
if not current_user.has_permission("standup:generate"):
    raise HTTPException(
        status_code=403,
        detail={
            "error": "Insufficient permissions",
            "message": "You don't have permission to generate standups."
        }
    )
```

---

### Task 4: OpenAPI Documentation (1 hour)

**Add to main.py** (or wherever FastAPI app is initialized):

```python
from fastapi import FastAPI
from web.api.routes import standup

app = FastAPI(
    title="Piper Morgan API",
    description="AI-Powered PM Assistant",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Include standup router
app.include_router(standup.router)
```

**Document Request/Response Examples**:

```python
class StandupRequest(BaseModel):
    """Request model for standup generation"""
    mode: Literal["standard", "documents", "issues", "calendar", "trifecta"] = Field(
        default="standard",
        description="Generation mode",
        examples=["trifecta"]
    )
    format: Literal["json", "slack", "markdown", "text"] = Field(
        default="json",
        description="Output format",
        examples=["slack"]
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "mode": "trifecta",
                    "format": "slack",
                    "user_id": "user-123"
                }
            ]
        }
```

---

### Task 5: Error Handling (1 hour)

**Follow Pattern-014** (Error Handling Pattern):

```python
from fastapi import HTTPException, status
from typing import Dict, Any

class StandupAPIError(Exception):
    """Base exception for standup API errors"""
    pass

class InvalidModeError(StandupAPIError):
    """Invalid generation mode"""
    pass

class GenerationFailedError(StandupAPIError):
    """Standup generation failed"""
    pass

# Error handler
@router.exception_handler(StandupAPIError)
async def handle_standup_error(request, exc):
    """Centralized standup error handling"""

    error_messages = {
        InvalidModeError: {
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Invalid generation mode",
            "message": "Please use one of: standard, documents, issues, calendar, trifecta"
        },
        GenerationFailedError: {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "error": "Generation failed",
            "message": "Unable to generate standup. Please try again in a moment."
        }
    }

    error_info = error_messages.get(type(exc), {
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "error": "Unknown error",
        "message": "An unexpected error occurred."
    })

    return JSONResponse(
        status_code=error_info["status"],
        content={
            "error": error_info["error"],
            "message": error_info["message"],
            "technical_details": str(exc) if DEBUG else None
        }
    )
```

**Common Error Scenarios**:

```python
# 400 Bad Request - Invalid mode
if mode not in ["standard", "documents", "issues", "calendar", "trifecta"]:
    raise HTTPException(
        status_code=400,
        detail="Invalid mode. Use one of: standard, documents, issues, calendar, trifecta"
    )

# 422 Unprocessable Entity - Validation error
# (Handled automatically by FastAPI/Pydantic)

# 500 Internal Server Error - Generation failure
try:
    result = await orchestration.generate_with_trifecta(user_id)
except Exception as e:
    raise HTTPException(
        status_code=500,
        detail="Standup generation failed. Please try again."
    )

# 503 Service Unavailable - Service degraded
if not orchestration.is_healthy():
    raise HTTPException(
        status_code=503,
        detail="Standup service temporarily unavailable. Please try again in a moment."
    )
```

---

### Task 6: Testing (3 hours)

**Create**: `tests/api/test_standup_api.py`

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_standup_standard_mode():
    """Test standard mode generation"""
    response = client.post(
        "/api/standup/generate",
        json={"mode": "standard", "format": "json"},
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "standup" in data
    assert data["standup"]["mode"] == "standard"

def test_generate_standup_trifecta_mode():
    """Test trifecta mode with all integrations"""
    response = client.post(
        "/api/standup/generate",
        json={"mode": "trifecta", "format": "slack"},
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["standup"]["mode"] == "trifecta"
    assert data["standup"]["format"] == "slack"

def test_generate_standup_invalid_mode():
    """Test error handling for invalid mode"""
    response = client.post(
        "/api/standup/generate",
        json={"mode": "invalid", "format": "json"},
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 422  # Pydantic validation

def test_generate_standup_unauthorized():
    """Test authentication requirement"""
    response = client.post(
        "/api/standup/generate",
        json={"mode": "standard", "format": "json"}
        # No auth header
    )
    assert response.status_code == 401

def test_list_available_modes():
    """Test modes listing endpoint"""
    response = client.get("/api/standup/modes")
    assert response.status_code == 200
    modes = response.json()
    assert "trifecta" in modes
    assert len(modes) == 5

def test_performance_metrics():
    """Test performance tracking"""
    response = client.post(
        "/api/standup/generate",
        json={"mode": "standard", "format": "json"},
        headers={"Authorization": "Bearer test-token"}
    )
    data = response.json()
    assert "performance_metrics" in data
    assert data["performance_metrics"]["generation_time_ms"] < 2000
    assert "time_saved_minutes" in data["performance_metrics"]

def test_health_check():
    """Test health endpoint"""
    response = client.get("/api/standup/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

---

### Task 7: Integration Testing (2 hours)

**Test with Real Services**:

```bash
# Start the API server
uvicorn main:app --reload --port 8001

# Test all endpoints
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "mode": "trifecta",
    "format": "slack"
  }'

# Test modes listing
curl http://localhost:8001/api/standup/modes

# Test formats listing
curl http://localhost:8001/api/standup/formats

# Test health
curl http://localhost:8001/api/standup/health

# View OpenAPI docs
open http://localhost:8001/docs
```

**Verify**:
- All 5 modes work
- All 4 formats work
- Authentication required
- Error handling graceful
- Performance <2s
- OpenAPI docs accurate

---

## Success Criteria

Phase 2 is complete when:

- [ ] REST endpoints for all 5 generation modes functional
- [ ] Query parameters for mode and format selection working
- [ ] Proper HTTP status codes and error responses (Pattern-014)
- [ ] OpenAPI documentation complete and accessible
- [ ] Integration with existing auth patterns
- [ ] Performance maintained (<2s response time)
- [ ] All existing functionality preserved (CLI still works)
- [ ] Comprehensive test suite (pytest tests passing)
- [ ] Integration testing complete with real services
- [ ] Documentation updated

---

## Files to Create/Modify

### New Files
1. `web/api/routes/standup.py` - Main API endpoints (~200 lines)
2. `tests/api/test_standup_api.py` - Test suite (~300 lines)
3. `docs/api/standup-endpoints.md` - API documentation

### Modified Files
1. `main.py` - Include standup router
2. `web/app.py` - Register API routes (if needed)
3. `requirements.txt` - Add any missing dependencies

---

## Architecture Notes

**Follow Established Patterns**:
1. **Pattern-014**: Error handling with user-friendly messages
2. **ADR-029**: Domain service mediation (use StandupOrchestrationService)
3. **Existing auth**: Don't reinvent authentication
4. **FastAPI patterns**: Async endpoints, dependency injection, response models

**Layer Separation**:
```
API Layer (web/api/routes/standup.py)
    ↓ delegates to
Domain Service (services/domain/standup_orchestration_service.py)
    ↓ uses
Feature Layer (services/features/morning_standup.py)
    ↓ uses
Integration Layer (services/integrations/...)
```

---

## Performance Targets

**From Issue #119 Results**:
- Standard mode: <1s ✅
- With issues: 948ms ✅
- With documents: 919ms ✅
- With calendar: 805ms ✅
- Trifecta: <1000ms ✅

**API Overhead Target**: +50-100ms (HTTP/JSON processing)

**Total Target**: <2s end-to-end (plenty of headroom!)

---

## Testing Strategy

1. **Unit Tests** (pytest):
   - Each endpoint
   - Each mode
   - Each format
   - Error scenarios
   - Auth scenarios

2. **Integration Tests**:
   - Real service calls
   - End-to-end flow
   - Performance validation
   - Multi-user scenarios

3. **Manual Testing**:
   - OpenAPI UI (Swagger)
   - curl commands
   - Postman collection (optional)

---

## Timeline

**Day 1** (8 hours):
- Task 1: Endpoint design (2h)
- Task 2: Service integration (2h)
- Task 3: Auth integration (1h)
- Task 4: OpenAPI docs (1h)
- Task 5: Error handling (1h)
- Task 6: Testing start (1h)

**Day 2** (4 hours):
- Task 6: Testing complete (2h)
- Task 7: Integration testing (2h)
- Documentation and cleanup

**Total**: 1.5 days (12 hours)

---

## Important Notes

### Don't Reinvent

**Reuse existing code**:
- StandupOrchestrationService (working!)
- MorningStandupWorkflow (working!)
- Authentication patterns (existing!)
- Error handling patterns (Pattern-014)
- Format converters from CLI

### Maintain Existing Functionality

**CLI must still work**:
- Don't break existing CLI commands
- Don't change service interfaces
- Only ADD new API layer on top

### Follow Time Lords Principles

- **Complete means complete**: All 10 success criteria
- **No scope reduction**: All 5 modes, all 4 formats
- **Test everything**: Unit + integration tests
- **Document properly**: OpenAPI + written docs

---

## Completion Report Template

**Create**: `dev/2025/10/[date]/phase-2-rest-api-complete.md`

```markdown
# Phase 2: REST API Implementation - Complete

**Date**: [date]
**Duration**: [actual time]
**Status**: COMPLETE ✅

## Deliverables
- [ ] API endpoints created
- [ ] All 5 modes functional via API
- [ ] All 4 formats working
- [ ] Authentication integrated
- [ ] Error handling implemented
- [ ] OpenAPI docs complete
- [ ] Test suite passing
- [ ] Integration testing complete
- [ ] Performance validated
- [ ] Documentation updated

## Test Results
- Unit tests: X/X passing
- Integration tests: X/X passing
- Performance: All modes <2s
- Error scenarios: All handled gracefully

## API Endpoints
- POST /api/standup/generate ✅
- GET /api/standup/modes ✅
- GET /api/standup/formats ✅
- GET /api/standup/health ✅

## Performance
- Standard: Xms
- Documents: Xms
- Issues: Xms
- Calendar: Xms
- Trifecta: Xms

## Next Steps
- Issue #162 ready to close
- Ready for Phase 3: Slack reminder integration
```

---

**Let's build this API!** 🚀

Foundation is solid, integrations working, now we just expose it via REST.

**Remember**:
- Reuse existing code
- Follow established patterns
- Test comprehensively
- Document properly
- Complete means complete
