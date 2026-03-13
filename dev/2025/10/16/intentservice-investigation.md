# IntentService Initialization Investigation

**Date**: October 16, 2025, 8:26-8:50 AM
**Investigator**: Code Agent (Claude Code)
**Duration**: 24 minutes (target: 30 minutes)

---

## Summary

**Issue**: Valid intent returns HTTP 422 instead of 200
**Error**: "IntentService couldn't initialize properly (LLM service not registered)"
**Root Cause**: Architectural gap - web/app.py depends on ServiceRegistry but can't initialize it independently
**Pre-existing**: YES - Since October 10, 2025 (5 days before Phase 1)

---

## Test Results

### Current State (with Phase 1 changes - commit 0d195d56)
```bash
$ curl -X POST /api/v1/intent -d '{"message": "show me the standup"}'
HTTP Status: 422
Response: {"status":"error","code":"VALIDATION_ERROR","message":"Failed to process intent","details":{"error_type":"ServiceUnavailable"}}
```

### Previous State (before Phase 1 - commit 02ceaf06)
```bash
$ curl -X POST /api/v1/intent -d '{"message": "show me the standup"}'
HTTP Status: 200  ← Old incorrect behavior!
Response: {"status":"error","error":"Failed to process intent","error_type":"ServiceUnavailable"}
```

**Conclusion**: **PRE-EXISTING ISSUE**
- Same error in both versions ("ServiceUnavailable")
- Phase 1 correctly converted HTTP 200 → 422 (REST-compliant)
- Phase 1 made the error more visible, did NOT cause it

---

## Service Initialization

### ServiceRegistry Location
**File**: `services/service_registry.py`

**Implementation**: Global singleton using class variables
```python
class ServiceRegistry:
    _services: Dict[str, Any] = {}
    _initialized: bool = False

    @classmethod
    def register(cls, name: str, service: Any) -> None:
        cls._services[name] = service

    @classmethod
    def get(cls, name: str) -> Any:
        if name not in cls._services:
            raise RuntimeError(
                f"Service '{name}' not registered. "
                f"Available services: {list(cls._services.keys())}"
            )
        return cls._services[name]
```

### OrchestrationEngine Initialization
**File**: `services/orchestration/engine.py:70-77`

```python
def __init__(self, llm_client: Optional[LLMClient] = None):
    # Use ServiceRegistry if none provided
    if llm_client is None:
        from services.service_registry import ServiceRegistry
        llm_client = ServiceRegistry.get_llm()  # ← Throws error if registry empty!

    self.llm_client = llm_client
```

### main.py Service Registration
**File**: `main.py:96-118`

```python
async def initialize_domain_services():
    """Initialize domain services at application startup"""
    from services.domain.llm_domain_service import LLMDomainService
    from services.service_registry import ServiceRegistry

    # Initialize LLM service
    llm_service = LLMDomainService()
    await llm_service.initialize()

    # Register in global registry
    ServiceRegistry.register("llm", llm_service)  # ← Populates registry

    # Mark registry as initialized
    ServiceRegistry.mark_initialized()
```

**But**: main.py never starts web server! (lines 121-151 just sleep forever)

---

## Server Logs

### Startup Errors (uvicorn direct)
```
🔧 Phase 3A: Initializing OrchestrationEngine with dependency injection...
❌ Phase 3A: OrchestrationEngine initialization failed: Service 'llm' not registered. Available services: []
🔧 Phase 2B: Initializing IntentService with dependency injection...
✅ Phase 2B: IntentService initialized successfully
```

**Analysis**:
- web/app.py lifespan tries to initialize OrchestrationEngine
- OrchestrationEngine tries to get LLM service from ServiceRegistry
- ServiceRegistry is empty (no services registered)
- OrchestrationEngine initialization fails
- IntentService initializes with `orchestration_engine=None`
- When processing intent, detects missing dependency → returns "ServiceUnavailable"

### Startup Success (main.py)
```
2025-10-16 08:28:02 [info     ] LLM providers validated: 4/4
2025-10-16 08:28:02 [info     ] LLM client initialized
2025-10-16 08:28:02 [info     ] LLM domain service initialized successfully
2025-10-16 08:28:02 [info     ] Service registered: llm        service_type=LLMDomainService
2025-10-16 08:28:02,313 - __main__ - INFO - Domain services initialized successfully
[then just sleeps forever - never starts web server]
```

**Analysis**:
- main.py successfully registers LLM service
- But doesn't start web server on port 8001
- So can't be used for testing intent endpoints

---

## Git History

### Recent Changes to Service Architecture

**Commit d6b8aa09 - October 10, 2025 (5 days BEFORE Phase 1)**
```
refactor(llm): implement proper DDD architecture for LLM configuration

Domain Layer:
- Add LLMDomainService as proper domain service mediator
- Add ServiceRegistry for global service access pattern  ← Introduced dependency!
- Implement proper domain service initialization

Consumer Migration:
- Migrate 8 consumers to use ServiceRegistry.get_llm()
- OrchestrationEngine now depends on ServiceRegistry
```

**Impact**: This commit created the architectural gap:
1. OrchestrationEngine now requires ServiceRegistry to be populated
2. main.py initializes ServiceRegistry but doesn't start web server
3. uvicorn starts web server but doesn't populate ServiceRegistry
4. Result: No way to start system properly

**Commit 0d195d56 - October 15, 2025 (Phase 1)**
```
feat(api): Fix intent endpoint to return proper HTTP status codes

Changes:
- web/app.py only (14 insertions, 22 deletions)
- Added error utility imports
- Updated 3 error patterns to use proper HTTP codes
```

**Impact**:
- Did NOT touch service initialization
- Only changed error response format
- Made pre-existing "ServiceUnavailable" error return 422 instead of 200

**Verification**: Tested at commit 02ceaf06 (before Phase 1):
- Same "ServiceUnavailable" error occurs
- But returns HTTP 200 instead of 422
- Proves issue is pre-existing

---

## Root Cause Analysis

### Why It's Failing

**Architectural Gap Created October 10**:

1. **ServiceRegistry Pattern Introduced**
   - OrchestrationEngine depends on ServiceRegistry.get_llm()
   - Raises RuntimeError if service not registered

2. **main.py Incomplete**
   - Initializes and registers LLM service ✅
   - But never starts web server ❌
   - Just sleeps forever after service init

3. **web/app.py Can't Work Independently**
   - Expects ServiceRegistry to be pre-populated
   - Has no mechanism to initialize services itself
   - Fails when started directly via uvicorn

4. **No Working Startup Path**
   - main.py: Registers services but doesn't start server
   - uvicorn: Starts server but doesn't register services
   - Result: Can't test intent endpoints

### Why It Worked Before October 10

Before ServiceRegistry was introduced:
- OrchestrationEngine could be initialized without dependencies
- web/app.py could start independently
- No global service registration required

### Impact of Phase 1 Changes

**Phase 1 Impact: ZERO (on the bug itself)**
- Only changed HTTP status codes
- Did NOT touch service initialization
- Made error more visible (422 vs 200)
- Actually improved REST compliance

**Evidence**:
- Same error before Phase 1: "ServiceUnavailable" + HTTP 200
- Same error after Phase 1: "ServiceUnavailable" + HTTP 422
- The 422 is correct behavior per Pattern 034

---

## Recommendations

### Option 1: Make web/app.py Self-Sufficient
**Approach**: Initialize LLM service in web/app.py lifespan

**Pros**:
- web server can start independently
- Proper separation of concerns
- Works with uvicorn for development

**Cons**:
- Duplicates initialization logic from main.py
- Two different startup paths to maintain

**Effort**: 30-45 minutes

**Implementation**:
```python
# In web/app.py lifespan, before OrchestrationEngine init:
if not ServiceRegistry.is_registered("llm"):
    from services.domain.llm_domain_service import LLMDomainService
    llm_service = LLMDomainService()
    await llm_service.initialize()
    ServiceRegistry.register("llm", llm_service)
```

---

### Option 2: Complete main.py Startup
**Approach**: Make main.py actually start the web server

**Pros**:
- Single source of truth for startup
- Clear separation: main.py orchestrates everything
- Follows original architectural intent

**Cons**:
- Can't use `uvicorn` command directly for development
- More complex startup sequence

**Effort**: 45-60 minutes

**Implementation**:
```python
# In main.py start_services():
def start_services():
    print("🚀 Starting Piper Morgan services...")

    # Start web server
    import uvicorn
    from web.app import app

    port_config = get_port_configuration()
    uvicorn.run(
        app,
        host=port_config.web_host,
        port=port_config.web_port
    )
```

---

### Option 3: Make ServiceRegistry Optional
**Approach**: Allow OrchestrationEngine to initialize without ServiceRegistry

**Pros**:
- Backward compatible
- Graceful degradation
- Works in both scenarios

**Cons**:
- May hide configuration issues
- Less strict dependency management

**Effort**: 15-20 minutes

**Implementation**:
```python
# In OrchestrationEngine.__init__:
def __init__(self, llm_client: Optional[LLMClient] = None):
    if llm_client is None:
        try:
            from services.service_registry import ServiceRegistry
            llm_client = ServiceRegistry.get_llm()
        except RuntimeError:
            # ServiceRegistry not initialized - degrade gracefully
            self.llm_client = None
            return

    self.llm_client = llm_client
```

---

### Recommended Approach: Option 1

**Why Option 1**:
- ✅ Fastest to implement (30-45 min)
- ✅ Allows independent web server testing
- ✅ Follows FastAPI lifespan pattern
- ✅ No breaking changes to existing code
- ✅ Works with uvicorn for development

**Implementation Strategy**:
1. Add LLM service initialization to web/app.py lifespan (before Phase 3A)
2. Check if ServiceRegistry already has LLM service (idempotent)
3. Initialize only if missing
4. Continue with existing OrchestrationEngine init

**Next Steps**:
1. Implement Option 1 in web/app.py
2. Test valid intent endpoint (should return 200)
3. Verify empty/missing intents still return 422
4. Update Phase 1 completion status

---

## Impact on #215

**Blocks #215**: NO

**Reasoning**:
- Phase 1 code changes are complete and working correctly
- The "ServiceUnavailable" issue is separate from #215
- #215 is about error handling standards, not service initialization
- Error handling is working: 422/500 codes are correct per Pattern 034

**Recommendation**:
1. **Complete #215 Phase 1** as-is (error handling working)
2. **Create separate issue** for service initialization gap
3. **Document** that valid endpoint testing requires Option 1 fix
4. **Continue** with #215 remaining phases (other endpoints)

**If separating issues**:
- Create: "web/app.py can't start independently - ServiceRegistry dependency"
- Link to: Commit d6b8aa09 (October 10) that introduced gap
- Priority: Medium (blocks local testing, not production)
- Estimated fix: 30-45 minutes (Option 1)

---

## Next Steps

### Immediate (Today)
1. ✅ Investigation complete - root cause identified
2. Decide: Fix now or create separate issue?
3. If fixing now: Implement Option 1 (30-45 min)
4. If deferring: Create GitHub issue with full context
5. Update session log with findings

### Follow-up (This Week)
1. Implement chosen fix (Option 1, 2, or 3)
2. Test all three scenarios:
   - Empty intent → 422
   - Missing intent → 422
   - Valid intent → 200
3. Continue #215 Phase 2 (remaining endpoints)
4. Update tests to expect new status codes

### Documentation Needed
1. Update web/app.py startup documentation
2. Document proper development server startup method
3. Add troubleshooting guide for "ServiceUnavailable" errors
4. Update ADR if architectural decision changes

---

## Deliverables

- [x] Issue reproduced and documented
- [x] Server logs analyzed
- [x] Service registration code located
- [x] Git history checked
- [x] Pre-existing vs new determined (PRE-EXISTING)
- [x] Investigation report written (this document)
- [x] Clear recommendation provided (Option 1)

---

## Success Criteria

**Investigation Complete**:
- ✅ Root cause identified (ServiceRegistry dependency gap)
- ✅ Pre-existing vs new determined (Pre-existing since Oct 10)
- ✅ Impact on #215 assessed (Does not block #215)
- ✅ Clear path forward recommended (Option 1 - 30-45 min)
- ✅ Report written with evidence

---

**Investigation Complete**: 8:50 AM
**Confidence Level**: HIGH

**Key Finding**: Phase 1 changes are working correctly - they made a pre-existing error visible by using proper HTTP status codes. The actual bug (ServiceRegistry dependency) predates Phase 1 by 5 days and is a separate architectural issue.

---

*"Investigate systematically, document thoroughly, recommend clearly."*
