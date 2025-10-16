# Gameplan: DDD Service Container Refactor + Error Standards Completion

**Date**: October 16, 2025, 10:25 AM  
**Sprint**: A2 - Notion & Errors (Day 2)  
**Issues**: Foundation work + #215 completion  
**Epic**: Proper DDD Architecture + REST Compliance  
**Estimated Duration**: 3-5 hours total  
**Chief Architect**: Lead Developer Sonnet

---

## Executive Summary

**The Cathedral View**: Fix foundational service layer architecture, then complete error standardization properly.

**Why This Order**:
1. **Foundation first** - Service layer is broken (Oct 10 gap)
2. **Testing requires it** - Can't validate #215 without working services
3. **DDD principle** - Get layers right before presentation concerns
4. **Sprint theme** - Infrastructure + quality work

**What We're Building**:
- Proper DDD service container pattern
- Clean service lifecycle management  
- Working intent endpoint (validates DDD fix)
- Complete REST-compliant error handling (validates #215)

---

## Phase -1: Infrastructure Verification ✅ COMPLETE

**Completed**: 8:27-8:50 AM (24 minutes)

**What We Learned**:
- ✅ Phase 1 error handling working correctly
- ✅ Issue is pre-existing (from Oct 10, commit d6b8aa09)
- ✅ ServiceRegistry introduced but startup paths broken
- ✅ main.py registers services, never starts server
- ✅ uvicorn starts server, never registers services

**Investigation Report**: `dev/2025/10/16/intentservice-investigation.md`

**Decision**: Fix properly with DDD (not quick hack)

---

## Phase 1.5: DDD Service Container Implementation

### Duration: 1.5-2 hours

### Objectives

Build proper service container following DDD principles:
1. **Single responsibility** - Container manages service lifecycle
2. **Singleton pattern** - One container instance
3. **Dependency injection** - Services get dependencies cleanly
4. **Initialization order** - Services init in correct sequence
5. **Error handling** - Clear errors for missing services

---

### Architecture Overview

```
services/
├── container/
│   ├── __init__.py                    # Public API exports
│   ├── service_container.py           # Main container (singleton)
│   ├── service_registry.py            # Registry interface
│   ├── initialization.py              # Service initialization logic
│   └── exceptions.py                  # Container-specific exceptions
├── domain/
│   └── llm/
│       └── llm_domain_service.py      # Existing LLM service
└── integrations/
    └── intent/
        └── intent_service.py          # Existing Intent service
```

---

### Key Components

#### 1. ServiceContainer (Singleton)

**File**: `services/container/service_container.py`

**Responsibilities**:
- Maintain single instance (singleton pattern)
- Initialize services in correct order
- Provide service access
- Track initialization state
- Handle errors gracefully

**Key Methods**:
```python
class ServiceContainer:
    def __new__(cls):
        """Enforce singleton pattern"""
        
    def initialize(self):
        """Initialize all services in correct order"""
        
    def get_service(self, name: str):
        """Get service by name"""
        
    def is_initialized(self) -> bool:
        """Check if container is initialized"""
        
    def shutdown(self):
        """Clean shutdown of all services"""
```

---

#### 2. ServiceRegistry (Interface)

**File**: `services/container/service_registry.py`

**Responsibilities**:
- Define service registry interface
- Type safety for service access
- Service metadata management

**Key Features**:
```python
class ServiceRegistry:
    def register(self, name: str, service: Any, metadata: Dict = None):
        """Register service with optional metadata"""
        
    def get(self, name: str) -> Any:
        """Get service by name"""
        
    def has(self, name: str) -> bool:
        """Check if service exists"""
        
    def list_services(self) -> List[str]:
        """List all registered services"""
```

---

#### 3. ServiceInitializer

**File**: `services/container/initialization.py`

**Responsibilities**:
- Service initialization logic
- Dependency resolution
- Initialization order management
- Configuration loading

**Key Features**:
```python
class ServiceInitializer:
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
        
    def initialize_llm_service(self, config: Config):
        """Initialize LLM service"""
        
    def initialize_intent_service(self, llm_service):
        """Initialize intent service with dependencies"""
        
    def initialize_all(self, config: Config):
        """Initialize all services in correct order"""
```

---

#### 4. Container Exceptions

**File**: `services/container/exceptions.py`

**Purpose**: Clear error messages for container issues

```python
class ServiceNotFoundError(Exception):
    """Service not found in container"""
    
class ContainerNotInitializedError(Exception):
    """Container not initialized"""
    
class ServiceInitializationError(Exception):
    """Service failed to initialize"""
    
class CircularDependencyError(Exception):
    """Circular dependency detected"""
```

---

### Integration Points

#### main.py (Startup)

```python
from services.container import ServiceContainer

def main():
    # Initialize container
    container = ServiceContainer()
    container.initialize()
    
    # Start web server
    import uvicorn
    uvicorn.run(
        "web.app:app",
        host="127.0.0.1",
        port=8001,
        reload=False
    )
```

#### web/app.py (Lifespan)

```python
from contextlib import asynccontextmanager
from services.container import ServiceContainer

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Get or initialize container
    container = ServiceContainer()
    if not container.is_initialized():
        container.initialize()
    
    yield
    
    # Shutdown: Clean up
    container.shutdown()

app = FastAPI(lifespan=lifespan)
```

#### Service Usage (Anywhere)

```python
from services.container import ServiceContainer

# Get service
container = ServiceContainer()
llm_service = container.get_service('llm')

# Or with error handling
try:
    intent_service = container.get_service('intent')
except ServiceNotFoundError:
    # Handle missing service
    pass
```

---

### Testing Strategy

#### Unit Tests

**File**: `tests/services/container/test_service_container.py`

**Tests**:
- Singleton pattern enforcement
- Service registration
- Service retrieval
- Initialization order
- Error handling
- Shutdown cleanup

#### Integration Tests

**File**: `tests/integration/test_service_container_integration.py`

**Tests**:
- Full initialization sequence
- Service dependencies
- Intent endpoint with real services
- Error propagation

---

### Acceptance Criteria

**Phase 1.5 complete when**:

- [ ] ServiceContainer implemented (singleton)
- [ ] ServiceRegistry implemented
- [ ] ServiceInitializer implemented
- [ ] Container exceptions defined
- [ ] main.py updated to use container
- [ ] web/app.py updated with lifespan
- [ ] Unit tests written (15+ tests)
- [ ] Integration tests written (5+ tests)
- [ ] All tests passing
- [ ] Intent endpoint working (validation!)
- [ ] Documentation updated

---

### Success Validation

```bash
# Start with main.py
python main.py

# Test valid intent
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": "show me the standup"}' \
  -w "\nHTTP: %{http_code}\n"

# Expected: HTTP 200 with success response (not 422!)

# Test invalid intent
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": ""}' \
  -w "\nHTTP: %{http_code}\n"

# Expected: HTTP 422 with validation error

# Both working = DDD fix validated!
```

---

## Phase 2: Complete Remaining Endpoints (#215)

### Duration: 1.5-2 hours

### Now With Working System!

**Can actually test error handling!**

### Objectives

Apply error standards to remaining endpoints:
- workflow endpoint
- personality endpoints (3)
- admin endpoints (8)

### Task Breakdown

#### Task 1: Identify Remaining Endpoints (15 min)

From Phase 0 audit:
- GET /api/v1/workflows/{workflow_id}
- GET /api/personality/profile/{user_id}
- PUT /api/personality/profile/{user_id}
- POST /api/personality/enhance
- 8 admin endpoints

**Total**: 12 endpoints (intent already done)

#### Task 2: Update Each Endpoint (60 min)

**Pattern**:
```python
# Before
except Exception as e:
    return {"status": "error", "error": str(e)}

# After
except ValueError as e:
    return validation_error(str(e))
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return internal_error()
```

**Systematic approach**:
- Update 2-3 endpoints at a time
- Test after each batch
- Verify no regressions

#### Task 3: Test Each Endpoint (30 min)

**Manual testing**:
```bash
# For each endpoint, test:
# 1. Invalid input → 422
# 2. Valid input → 200
# 3. Server error → 500
```

**Document results** in `dev/active/phase-2-endpoint-testing.md`

### Acceptance Criteria

- [ ] All 12 endpoints updated
- [ ] Error utilities used consistently
- [ ] Manual testing complete
- [ ] No regressions detected
- [ ] Changes committed

---

## Phase 3: Update Tests (#215)

### Duration: 45-60 minutes

### Objectives

Update test expectations for new error codes

### Task Breakdown

#### Task 1: Find Tests Needing Updates (15 min)

```bash
# Find tests checking error responses
grep -r "status_code.*200.*error\|assert.*error" tests/ --include="*.py"

# Find tests for specific endpoints
find tests/ -name "*workflow*" -o -name "*personality*" -o -name "*admin*"
```

#### Task 2: Update Test Assertions (30 min)

**Old pattern**:
```python
assert response.status_code == 200
assert response.json()["status"] == "error"
```

**New pattern**:
```python
assert response.status_code == 422
assert response.json()["code"] == "VALIDATION_ERROR"
```

#### Task 3: Run Test Suite (15 min)

```bash
# Run all tests
pytest tests/ -v

# Verify pass rate
pytest tests/ --tb=line -q
```

### Acceptance Criteria

- [ ] All test expectations updated
- [ ] New error format validated in tests
- [ ] Full test suite passing
- [ ] No skipped tests due to errors

---

## Phase 4: Documentation (#215)

### Duration: 30-45 minutes

### Objectives

Complete error handling documentation

### Task Breakdown

#### Task 1: Update API Docs (15 min)

**File**: `docs/public/api/error-handling.md`

**Content**:
- Error response format
- HTTP status code meanings
- Examples for each error type
- Client implementation guide

#### Task 2: Update Migration Guide (15 min)

**File**: `docs/public/migration/error-handling-migration.md`

**Content**:
- Breaking changes explanation
- Before/after examples
- Client code updates needed
- Timeline and rollout

#### Task 3: Update README (15 min)

**File**: `README.md`

**Updates**:
- Startup instructions (python main.py)
- Error handling overview
- Link to API docs

### Acceptance Criteria

- [ ] API documentation complete
- [ ] Migration guide clear
- [ ] README updated
- [ ] All links working

---

## Phase Z: Final Validation & Handoff

### Duration: 30 minutes

### Objectives

Ensure both DDD refactor and #215 are complete and validated

### Validation Checklist

#### DDD Service Container

- [ ] Intent endpoint returns 200 for valid requests
- [ ] Intent endpoint returns 422 for invalid requests
- [ ] Services initialize in correct order
- [ ] Container singleton working
- [ ] Unit tests passing (15+)
- [ ] Integration tests passing (5+)

#### #215 Error Standards

- [ ] All 20 endpoints following Pattern 034
- [ ] All error responses have proper HTTP codes
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Migration guide clear

#### Final Integration Test

```bash
# Full system test
python main.py &
sleep 5

# Test all endpoint types
./scripts/test-all-endpoints.sh

# Expected: All returning proper status codes
```

### GitHub Issue Updates

#### Update #215 Description

**Mark complete**:
- [x] Phase 0: Audit + standards
- [x] Phase 1: Intent endpoint  
- [x] Phase 1.5: DDD service container (added!)
- [x] Phase 2: All endpoints
- [x] Phase 3: Tests updated
- [x] Phase 4: Documentation

**Add Phase 1.5 section**:
```markdown
### Phase 1.5: DDD Service Container (ADDED)

**Why Added**: Investigation revealed architectural gap from Oct 10
**What**: Proper DDD service container pattern
**Duration**: 1.5-2 hours
**Result**: Foundation fixed, services working properly

**Deliverables**:
- ServiceContainer implementation
- Service lifecycle management
- Intent endpoint now functional
- Enables proper error handling validation
```

### Session Log Completion

**Final entries**:
- DDD refactor complete with evidence
- #215 phases 2-4 complete with evidence
- Sprint A2 status: 5/5 = 100%
- Lessons learned
- Next session recommendations

---

## Timeline Summary

**Morning** (8:17 AM - 12:00 PM):
- ✅ Investigation (24 min) - DONE
- ✅ Gameplan creation (30 min) - DONE  
- 🔜 Phase 1.5: DDD refactor (1.5-2 hours)

**Afternoon** (1:00 PM - 4:00 PM):
- Phase 2: Remaining endpoints (1.5-2 hours)
- Phase 3: Test updates (45-60 min)

**Late Afternoon** (4:00 PM - 5:00 PM):
- Phase 4: Documentation (30-45 min)
- Phase Z: Final validation (30 min)

**Total**: 5-6 hours of work
**Sprint A2 Result**: 100% COMPLETE! 🎉

---

## Risk Management

### Known Risks

1. **Service dependencies complex**
   - Mitigation: Start with simple services (LLM), add intent later
   - Time buffer: 30 min extra

2. **Tests may need more updates**
   - Mitigation: Update in batches, test frequently
   - Time buffer: 30 min extra

3. **Documentation scope creep**
   - Mitigation: Focus on essentials, link to Pattern 034
   - Time buffer: None needed

### STOP Conditions

Stop and reassess if:
- DDD implementation taking > 3 hours
- Can't get intent endpoint working
- Tests failing catastrophically
- Breaking other systems

---

## Success Metrics

### Technical

- ✅ All services initialize properly
- ✅ Intent endpoint functional (200 for valid, 422 for invalid)
- ✅ All 20 endpoints REST-compliant
- ✅ Test suite passing (100+ tests)
- ✅ No regressions introduced

### Process

- ✅ Proper DDD architecture implemented
- ✅ Foundation fixed before presentation layer
- ✅ Testing validates both fixes
- ✅ Documentation complete
- ✅ Clean handoff

### Sprint

- ✅ Sprint A2: 5/5 issues complete
- ✅ Both verification and action work done
- ✅ Quality maintained throughout
- ✅ Methodology improvements captured

---

## Lessons Learned (Preemptive)

**What we expect to learn**:

1. **DDD pays off** - Fixing foundation enables everything else
2. **Investigation matters** - 24 min investigation saved days of wrong fixes
3. **Order matters** - Service layer before presentation layer
4. **Testing validates** - Can't test error handling without working services

**Document these** in session log after completion!

---

**Gameplan Status**: Ready for execution  
**PM Approval**: Pending  
**Agent Assignment**: Claude Code (full ownership)

---

*"Build the foundation right, then build upon it."*  
*- DDD Philosophy*
