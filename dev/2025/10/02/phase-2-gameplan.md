# GREAT-3A Phase 2 Gameplan: web/app.py Refactoring

**Date**: October 2, 2025 - 4:57 PM PT
**Lead Developer**: Claude Sonnet 4.5
**GitHub Issue**: GREAT-3A (Plugin Architecture Foundation)

---

## Executive Summary

**Mission**: Refactor web/app.py (1,052 lines) to support plugin architecture by extracting business logic, moving templates, and organizing routes into logical groups.

**Approach**: Methodical, low-risk-first ordering
1. Template extraction (simple, immediate wins)
2. Intent service extraction (complex, requires careful design)
3. Route organization (final cleanup)

**Estimated Duration**: ~2 mangos total

---

## Phase 1 Completion Status

**Achieved**: 100% config pattern compliance (4 of 4 integrations)
- ✅ Slack: Standard interface
- ✅ Notion: Standard interface
- ✅ GitHub: Standard interface + extensions
- ✅ Calendar: Standard interface

**Foundation**: All integrations now use consistent service injection pattern, ready for plugin architecture.

---

## Phase 2 Context

### Current web/app.py State

**File Stats**:
- Total lines: 1,052
- Total routes: 11
- Largest routes (65% of complexity):
  - `/api/v1/intent` (226 lines) - OrchestrationEngine coupling
  - `/` home page (332 lines) - Embedded HTML
  - `/standup` UI (132 lines) - Embedded HTML

**Problems**:
1. **Business logic in routes**: Intent processing tightly coupled to route handler
2. **Embedded templates**: 464 lines of HTML in route functions
3. **Monolithic file**: 1,052 lines violates <200 line guideline
4. **No plugin mounting**: No clear place for plugins to register routes

### Why This Matters for Plugin Architecture

**Plugin Route Registration Requires**:
- Clean separation of concerns (business logic vs routing)
- Predictable mount points for plugin routes
- Modular route groups that plugins can extend
- Service layer abstraction (not direct OrchestrationEngine calls)

**Current web/app.py blocks plugin work** - must be refactored first.

---

## Phase 2A: Template Extraction

**Duration**: ~30 minutes
**Complexity**: Low (straightforward extraction)
**Risk**: Very low (no logic changes)

### Objective

Extract 464 lines of embedded HTML from routes into proper template files.

### Target Routes

1. **Home page (`/`)**: 332 lines of HTML
   - Current: Embedded in route function
   - Target: `templates/home.html`
   - Benefit: Route reduces from 332 → ~20 lines

2. **Standup UI (`/standup`)**: 132 lines of HTML
   - Current: Embedded in route function
   - Target: `templates/standup.html`
   - Benefit: Route reduces from 132 → ~20 lines

### Template Structure

```
templates/
├── base.html              # Base template (if needed)
├── home.html              # Home page template
└── standup.html           # Standup UI template
```

### Route Changes (Example)

**Before**:
```python
@app.get("/")
async def home():
    html = """
    <!DOCTYPE html>
    <html>
    ... 332 lines of HTML ...
    </html>
    """
    return HTMLResponse(html)
```

**After**:
```python
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
```

### Agent Assignment

**Cursor Agent** (template expert):
- Create templates/ directory
- Extract HTML to template files
- Update routes to use Jinja2Templates
- Test template rendering
- Verify no functionality changes

### Success Criteria

- [ ] templates/ directory created
- [ ] home.html template working
- [ ] standup.html template working
- [ ] Routes reduced to ~20 lines each
- [ ] All functionality preserved
- [ ] web/app.py reduced by ~464 lines

### Deliverable

`dev/2025/10/02/phase-2a-cursor-template-extraction.md`

---

## Phase 2B: Intent Service Extraction

**Duration**: ~1 mango
**Complexity**: Medium-High (OrchestrationEngine coupling)
**Risk**: Medium (business logic changes)

### Objective

Extract intent processing business logic from `/api/v1/intent` route (226 lines) into dedicated service layer.

### Current Route Structure

```python
@app.post("/api/v1/intent")
async def process_intent(intent: IntentRequest, ...):
    # 226 lines of:
    # - Intent parsing
    # - OrchestrationEngine calls
    # - Response formatting
    # - Error handling
    # All tightly coupled to route handler
```

### Service Layer Design

**New Service**: `services/intent/intent_service.py`

```python
class IntentService:
    """
    Service for processing user intents.

    Handles intent parsing, orchestration, and response formatting.
    Decouples business logic from route handlers.
    """

    def __init__(self, orchestration_engine: OrchestrationEngine):
        self.engine = orchestration_engine

    async def process_intent(
        self,
        intent: IntentRequest,
        user_id: str
    ) -> IntentResponse:
        """Process user intent and return formatted response"""
        # Intent processing logic moves here
        pass
```

**Route After Extraction**:
```python
@app.post("/api/v1/intent")
async def process_intent(
    intent: IntentRequest,
    request: Request
):
    """Process user intent via intent service"""
    intent_service = request.app.state.intent_service
    return await intent_service.process_intent(intent, user_id)
```

### Service Boundaries

**IntentService Responsibilities**:
- Parse and validate intents
- Coordinate with OrchestrationEngine
- Format responses
- Handle intent-specific errors

**Route Handler Responsibilities**:
- HTTP request/response handling
- Authentication/authorization
- Input validation (FastAPI models)
- Dependency injection (get service from app.state)

### OrchestrationEngine Integration

**Current Pattern** (in route):
```python
# Direct engine access in route
engine = request.app.state.orchestration_engine
result = await engine.process(...)
```

**New Pattern** (via service):
```python
# Service handles engine coordination
class IntentService:
    def __init__(self, engine: OrchestrationEngine):
        self.engine = engine

    async def process_intent(self, ...):
        result = await self.engine.process(...)
        return self._format_response(result)
```

### Startup Integration

**Update web/app.py lifespan**:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ... existing setup ...

    # Initialize intent service
    from services.intent.intent_service import IntentService

    intent_service = IntentService(
        orchestration_engine=app.state.orchestration_engine
    )
    app.state.intent_service = intent_service

    yield
    # ... cleanup ...
```

### Agent Assignment

**Code Agent** (service extraction expert):
- Create IntentService class
- Extract business logic from route
- Design service interface
- Update route to use service
- Add service to app.state
- Test intent processing flow

### Architectural Questions (if needed)

**Question 1**: Should IntentService live in `services/intent/` or `services/orchestration/`?
- Pro intent/: Separate concern from orchestration
- Pro orchestration/: Tightly coupled to OrchestrationEngine

**Question 2**: How should service handle streaming responses?
- Current route uses streaming for some intents
- Service needs to support streaming pattern

**Question 3**: Should service handle all OrchestrationEngine interaction?
- Or just intent-specific logic?
- Where does general orchestration fit?

**Recommendation**: Start with `services/intent/` and keep streaming support. Can refactor later if orchestration/ makes more sense.

### Success Criteria

- [ ] IntentService created
- [ ] Route reduced from 226 → ~30 lines
- [ ] Business logic moved to service
- [ ] OrchestrationEngine integration working
- [ ] All intent types still processed correctly
- [ ] Streaming responses still work
- [ ] Error handling preserved

### Deliverable

`dev/2025/10/02/phase-2b-code-intent-extraction.md`

---

## Phase 2C: Route Organization

**Duration**: ~30 minutes
**Complexity**: Low (file organization)
**Risk**: Low (no logic changes)

### Objective

Split remaining web/app.py routes into logical groups, each <200 lines.

### Current Route Inventory (After 2A + 2B)

**Simplified Routes** (after template + intent extraction):
```
web/app.py (now ~358 lines, down from 1,052)

Core API Routes:
- POST /api/v1/intent (~30 lines, simplified)
- POST /api/v1/workflows/execute (~30 lines)
- GET /api/v1/workflows (~20 lines)

Personality Routes:
- GET /api/v1/personality (~25 lines)
- POST /api/v1/personality/ephemeral (~30 lines)

Standup Routes:
- GET /standup (~20 lines, template only)
- POST /api/v1/standup/execute (~25 lines)

UI Routes:
- GET / (~20 lines, template only)

Utility Routes:
- GET /health (~10 lines)
- GET /api/v1/config (~15 lines)
- WebSocket /ws (~30 lines)
```

### Proposed Route Groups

**Group A: Core API** (`web/routes/core_api.py` ~80 lines)
- POST /api/v1/intent
- POST /api/v1/workflows/execute
- GET /api/v1/workflows

**Group B: Personality API** (`web/routes/personality_api.py` ~55 lines)
- GET /api/v1/personality
- POST /api/v1/personality/ephemeral

**Group C: Standup Features** (`web/routes/standup.py` ~45 lines)
- GET /standup (UI)
- POST /api/v1/standup/execute

**Group D: UI Pages** (`web/routes/ui.py` ~20 lines)
- GET / (home page)

**Group E: Utilities** (`web/routes/utils.py` ~55 lines)
- GET /health
- GET /api/v1/config
- WebSocket /ws

### New Directory Structure

```
web/
├── app.py                 (~100 lines: FastAPI setup, lifespan, router mounting)
├── routes/
│   ├── __init__.py
│   ├── core_api.py       (~80 lines)
│   ├── personality_api.py (~55 lines)
│   ├── standup.py        (~45 lines)
│   ├── ui.py             (~20 lines)
│   └── utils.py          (~55 lines)
└── templates/
    ├── home.html
    └── standup.html
```

### Router Mounting Pattern

**web/app.py (simplified)**:
```python
from fastapi import FastAPI
from web.routes import core_api, personality_api, standup, ui, utils

app = FastAPI(lifespan=lifespan)

# Mount route groups
app.include_router(core_api.router, prefix="/api/v1", tags=["core"])
app.include_router(personality_api.router, prefix="/api/v1", tags=["personality"])
app.include_router(standup.router, tags=["standup"])
app.include_router(ui.router, tags=["ui"])
app.include_router(utils.router, tags=["utils"])
```

**Route Group Pattern** (example: `web/routes/core_api.py`):
```python
from fastapi import APIRouter, Request, Depends

router = APIRouter()

@router.post("/intent")
async def process_intent(intent: IntentRequest, request: Request):
    """Process user intent via intent service"""
    intent_service = request.app.state.intent_service
    return await intent_service.process_intent(intent)

@router.post("/workflows/execute")
async def execute_workflow(...):
    # Workflow execution logic
    pass

# ... other core API routes
```

### Plugin Integration Points

**After Phase 2C, plugins can mount like**:
```python
# Plugin registration (future Phase 3)
class SlackPlugin(PiperPlugin):
    def register_routes(self, app: FastAPI):
        from .routes import slack_routes
        app.include_router(
            slack_routes.router,
            prefix="/api/v1/integrations/slack",
            tags=["slack"]
        )
```

### Agent Assignment

**Both Agents** (coordinated split):

**Cursor Agent**:
- Create web/routes/ directory structure
- Split UI/Standup routes (Groups C, D)
- Create route group files
- Test route mounting

**Code Agent**:
- Split API routes (Groups A, B, E)
- Update app.py router mounting
- Verify all routes still work
- Test dependency injection still functions

### Success Criteria

- [ ] web/routes/ directory created
- [ ] All 5 route groups created
- [ ] Each group <200 lines
- [ ] app.py reduced to ~100 lines
- [ ] All routes still accessible
- [ ] All functionality preserved
- [ ] Plugin mounting pattern clear

### Deliverable

`dev/2025/10/02/phase-2c-route-organization.md`

---

## Phase 2 Summary

### Total Changes

**Before Phase 2**:
- web/app.py: 1,052 lines (monolithic)
- No templates/ directory
- Business logic in routes
- No clear plugin mounting

**After Phase 2**:
- web/app.py: ~100 lines (setup + mounting only)
- web/routes/: 5 route groups (~255 lines total)
- web/templates/: 2 template files (~464 lines)
- services/intent/: Intent service (~150 lines)
- Total: ~969 lines (well-organized, modular)

**Net Result**: Same functionality, organized for plugin architecture

### Plugin Architecture Readiness

**Phase 2 Enables**:
- ✅ Clean route mounting pattern
- ✅ Service layer abstraction
- ✅ Modular route groups
- ✅ Template organization
- ✅ Clear extension points

**Phase 3 Can Now**:
- Define PiperPlugin interface
- Implement plugin registry
- Enable plugin route mounting
- Support plugin lifecycle management

### Risk Mitigation

**Incremental Approach**:
1. Templates first (simple, low risk)
2. Service extraction second (complex, contained risk)
3. Route organization last (simple, depends on 1+2)

**Each phase**:
- Self-contained
- Testable independently
- Reversible if needed
- Builds on previous phase

### Time Estimates

- Phase 2A: 30 minutes (template extraction)
- Phase 2B: 60 minutes (intent service extraction)
- Phase 2C: 30 minutes (route organization)
- **Total**: ~2 hours (2 mangos)

### Success Criteria (Overall)

- [ ] web/app.py <200 lines
- [ ] All route groups <200 lines
- [ ] Business logic in service layer
- [ ] Templates in templates/ directory
- [ ] All existing functionality preserved
- [ ] Plugin mounting pattern established
- [ ] No breaking changes to API contracts

---

## Next Steps

**Immediate**: Execute Phase 2A (template extraction)
**Then**: Execute Phase 2B (intent service extraction)
**Finally**: Execute Phase 2C (route organization)
**After Phase 2**: Begin Phase 3 (plugin interface definition)

---

**Gameplan Status**: ✅ Ready for Execution
**Time**: 4:57 PM PT
**Estimated Completion**: ~6:57 PM PT (2 hours from start)

---

## Appendix: Architectural Notes

### Service Layer Design Philosophy

**Principle**: Routes should be thin adapters between HTTP and business logic.

**Route Responsibility**:
- Parse HTTP request
- Validate input (via FastAPI models)
- Call service layer
- Format HTTP response

**Service Responsibility**:
- Business logic
- Orchestration
- Data transformation
- Error handling (business errors, not HTTP errors)

### Template Philosophy

**Principle**: Presentation logic separate from route logic.

**Template Responsibility**:
- HTML structure
- UI components
- Client-side behavior (minimal)

**Route Responsibility**:
- Data preparation
- Template selection
- Context passing

### Route Organization Philosophy

**Principle**: Logical grouping by feature domain, not by HTTP method.

**Good Grouping** (by feature):
- core_api.py: Intent + Workflows
- personality_api.py: All personality routes
- standup.py: All standup routes

**Bad Grouping** (by method):
- get_routes.py: All GET endpoints
- post_routes.py: All POST endpoints

**Reason**: Features evolve together, plugins extend feature domains.

---

**End of Gameplan**
