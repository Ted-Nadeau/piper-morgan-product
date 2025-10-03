# Claude Code Agent Prompt: GREAT-3A Phase 2B - Intent Service Extraction

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase 2B work.

## Mission
**Extract Intent Service**: Move business logic from `/api/v1/intent` route (226 lines) into dedicated service layer.

## Context

**Phase 2A Complete**: Templates extracted, web/app.py reduced from 1,052 → 603 lines
**Phase 2B Goal**: Extract complex business logic from intent route into service layer
**Why**: Route handlers should be thin HTTP adapters, not contain business logic

**Current Problem**: `/api/v1/intent` route has 226 lines of:
- Intent parsing
- OrchestrationEngine calls
- Response formatting
- Error handling
- All tightly coupled to route handler

## Your Tasks

### Task 1: Analyze Current Intent Route

```bash
cd ~/Development/piper-morgan

# Find the intent route
grep -n '@app.post("/api/v1/intent")' web/app.py

# Extract the full route (should be ~226 lines)
# Use line numbers from grep to extract
sed -n '<start_line>,<end_line>p' web/app.py > /tmp/intent_route.txt

# Review the route structure
cat /tmp/intent_route.txt
```

**Document**:
- What does the route actually do?
- How does it use OrchestrationEngine?
- What business logic is embedded?
- What can be extracted vs what stays in route?

### Task 2: Design IntentService Interface

**Service Location**: `services/intent/intent_service.py`

**Interface Design Principles**:
- Service handles ALL business logic
- Route handles ONLY HTTP concerns
- Service is testable without HTTP layer
- Service coordinates with OrchestrationEngine

**Proposed Interface**:
```python
class IntentService:
    """
    Service for processing user intents.

    Handles intent parsing, orchestration coordination, and response formatting.
    Decouples business logic from HTTP route handlers.
    """

    def __init__(self, orchestration_engine: OrchestrationEngine):
        """Initialize service with orchestration engine"""
        self.engine = orchestration_engine
        self.logger = logging.getLogger(__name__)

    async def process_intent(
        self,
        intent_text: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> IntentResponse:
        """
        Process user intent and return formatted response.

        Args:
            intent_text: The user's intent text
            user_id: User identifier
            context: Optional context dictionary

        Returns:
            IntentResponse with results

        Raises:
            IntentProcessingError: If processing fails
        """
        # Business logic goes here
        pass
```

**Consider**:
- Should service handle streaming responses?
- How should errors be handled?
- What models/types are needed?

### Task 3: Create Service Directory Structure

```bash
# Create directory
mkdir -p services/intent

# Create files
touch services/intent/__init__.py
touch services/intent/intent_service.py

# Verify
ls -la services/intent/
```

### Task 4: Implement IntentService

**File**: `services/intent/intent_service.py`

**Implementation Steps**:
1. Extract business logic from route
2. Move OrchestrationEngine calls to service
3. Move response formatting to service
4. Move error handling to service
5. Keep route as thin HTTP adapter

**What to Extract**:
- Intent validation logic
- OrchestrationEngine coordination
- Response construction
- Error handling (business errors, not HTTP)

**What Stays in Route**:
- HTTP request parsing
- FastAPI model validation
- HTTP response formatting
- HTTP error codes

**Example Implementation**:
```python
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

from services.orchestration.engine import OrchestrationEngine


@dataclass
class IntentResponse:
    """Response from intent processing"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class IntentProcessingError(Exception):
    """Raised when intent processing fails"""
    pass


class IntentService:
    """Service for processing user intents"""

    def __init__(self, orchestration_engine: OrchestrationEngine):
        self.engine = orchestration_engine
        self.logger = logging.getLogger(__name__)

    async def process_intent(
        self,
        intent_text: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> IntentResponse:
        """Process user intent"""
        try:
            # Extract business logic from route here
            # 1. Validate intent
            # 2. Call orchestration engine
            # 3. Format response
            # 4. Return result

            self.logger.info(f"Processing intent for user {user_id}")

            # Placeholder - implement actual logic
            result = await self.engine.process_intent(intent_text, context)

            return IntentResponse(
                success=True,
                message="Intent processed successfully",
                data=result
            )

        except Exception as e:
            self.logger.error(f"Intent processing failed: {e}")
            raise IntentProcessingError(f"Failed to process intent: {e}")
```

### Task 5: Update web/app.py Route

**Current Route** (~226 lines):
```python
@app.post("/api/v1/intent")
async def process_intent(request: Request, intent: IntentRequest):
    # ... 226 lines of business logic ...
    pass
```

**New Route** (~20-30 lines):
```python
@app.post("/api/v1/intent")
async def process_intent(
    request: Request,
    intent: IntentRequest
) -> IntentResponseModel:
    """
    Process user intent via intent service.

    Route handler delegates all business logic to IntentService.
    """
    try:
        # Get service from app state
        intent_service: IntentService = request.app.state.intent_service

        # Call service (business logic)
        result = await intent_service.process_intent(
            intent_text=intent.text,
            user_id=intent.user_id,
            context=intent.context
        )

        # Return HTTP response
        return IntentResponseModel(
            success=result.success,
            message=result.message,
            data=result.data
        )

    except IntentProcessingError as e:
        # Business error → 400
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Unexpected error → 500
        raise HTTPException(status_code=500, detail="Internal server error")
```

**Key Changes**:
- Route becomes thin HTTP adapter
- Business logic moved to service
- Service retrieved from app.state
- HTTP concerns (status codes) stay in route
- Business errors converted to HTTP errors

### Task 6: Update Startup (web/app.py lifespan)

**Add IntentService to app state**:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan with service initialization"""

    # ... existing initialization ...

    # Initialize IntentService
    from services.intent.intent_service import IntentService

    intent_service = IntentService(
        orchestration_engine=app.state.orchestration_engine
    )
    app.state.intent_service = intent_service

    print("✅ IntentService initialized")

    yield

    # Cleanup
    print("🛑 Services shutdown complete")
```

### Task 7: Handle Streaming Responses (If Needed)

**Check if intent route uses streaming**:
```bash
grep -i "stream\|sse\|event" /tmp/intent_route.txt
```

**If streaming is used**:
- Service needs to support streaming pattern
- Consider using async generator
- Route still handles SSE/streaming HTTP details

**Example Streaming Support**:
```python
class IntentService:
    async def process_intent_stream(
        self,
        intent_text: str,
        user_id: str
    ):
        """Process intent with streaming response"""
        async for chunk in self.engine.process_stream(intent_text):
            yield chunk
```

### Task 8: Test Service Integration

```bash
# Test 1: Service imports
python -c "from services.intent.intent_service import IntentService; print('Import OK')"

# Test 2: Service instantiation
python -c "from services.intent.intent_service import IntentService; from services.orchestration.engine import OrchestrationEngine; e = OrchestrationEngine(None); s = IntentService(e); print('Service OK')"

# Test 3: App startup
python -c "import sys; sys.path.insert(0, '.'); from web.app import app; print('App loads OK')"

# Test 4: Manual test - start server
# uvicorn web.app:app --reload --port 8001
# Test /api/v1/intent endpoint
```

### Task 9: Verify Line Count Reduction

```bash
# Count lines after extraction
wc -l web/app.py

# Expected: ~603 → ~377 (reduction of ~226 lines)
# Intent route: 226 → ~20-30 lines
```

### Task 10: Check OrchestrationEngine Integration

**Critical**: Ensure service properly coordinates with OrchestrationEngine

**Verify**:
- How does current route call engine?
- What parameters does engine need?
- Does engine support the service pattern?
- Are there any breaking changes?

**Test engine integration**:
```python
# In service method
result = await self.engine.process_intent(
    intent_text=intent_text,
    context=context
)
```

## Deliverable

Create: `dev/2025/10/02/phase-2b-code-intent-extraction.md`

Include:
1. **Current Route Analysis**: What the route currently does
2. **Service Design**: IntentService interface and implementation
3. **Route Simplification**: Before/after comparison with diffs
4. **Startup Integration**: How service is initialized
5. **Streaming Support**: If implemented
6. **Test Results**: All test commands passing
7. **Line Count Reduction**: Verification of ~226 line reduction
8. **OrchestrationEngine Integration**: How service coordinates with engine

## Critical Requirements

- **DO extract** ALL business logic to service
- **DO keep** route as thin HTTP adapter
- **DO preserve** all functionality
- **DO handle** errors appropriately (business vs HTTP)
- **DON'T break** existing API contract
- **DON'T change** OrchestrationEngine interface

## Time Estimate
60 minutes (1 mango)

## Success Criteria
- [ ] IntentService created in services/intent/
- [ ] Service handles all business logic
- [ ] Route reduced from ~226 → ~20-30 lines
- [ ] Service added to app.state
- [ ] All existing functionality preserved
- [ ] OrchestrationEngine integration working
- [ ] Streaming support (if needed)
- [ ] All test commands pass

---

**Deploy at 5:10 PM**
**Complex phase - careful extraction of business logic**
