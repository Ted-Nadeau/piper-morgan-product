# Gameplan: Issue #322 - ARCH-FIX-SINGLETON

**Issue:** [#322 ARCH-FIX-SINGLETON: Replace ServiceContainer singleton to enable horizontal scaling](https://github.com/mediajunkie/piper-morgan-product/issues/322)
**Created:** 2026-01-04
**Sprint:** A12
**Estimated Effort:** 18-24 hours (revised with full validation suite)

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: **FastAPI** (verified in web/app.py)
- [x] CLI structure: **Click** (verified in cli/main.py)
- [x] Database: **PostgreSQL** on port 5433 (verified in docker-compose.yml)
- [x] Testing framework: **pytest** (verified in pytest.ini)
- [x] Existing endpoints: Multiple routers mounted via `web/startup.py` and `web/router_initializer.py`
- [x] Missing features: **Dependency injection for ServiceContainer** - routes currently don't receive container via DI

**My understanding of the task**:
- I believe we need to: Remove the singleton pattern from `ServiceContainer` to allow multiple instances across uvicorn workers
- I think this involves: Modifying 9 production files + 15+ test files that call `ServiceContainer()` directly
- I assume the current state is: `web/startup.py` already stores container in `app.state.service_container` but services bypass this and instantiate directly

**Current ServiceContainer implementation** (`services/container/service_container.py:29-35`):
```python
def __new__(cls):
    """Enforce singleton pattern."""
    if cls._instance is None:
        logger.info("Creating ServiceContainer instance")
        cls._instance = super().__new__(cls)
        cls._instance._registry = ServiceRegistry()
    return cls._instance
```

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [x] Multiple agents will work in parallel on different files/features
- [x] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [x] Exploratory/risky changes where easy rollback is valuable
- [ ] Coordination queue prompt being claimed

Worktrees ADD overhead when:
- [ ] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [ ] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment:**
- [x] **USE WORKTREE** - 3 parallel criteria checked (multi-agent parallel, >30min, risky changes)

**Rationale**: This is a 16-20 hour refactoring effort touching core infrastructure. Main branch will likely advance during implementation. Changes are risky and benefit from easy rollback capability.

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What actually exists in the filesystem?**
   ```bash
   # Verified locations of ServiceContainer() calls:
   main.py                                        # 2 calls
   web/startup.py                                 # 1 call (already stores in app.state)
   services/container/__init__.py                 # 1 call (convenience export)
   services/integrations/github/issue_analyzer.py # 1 call
   services/intent_service/classifier.py          # 1 call
   services/intent_service/llm_classifier.py      # 1 call
   services/knowledge_graph/ingestion.py          # 1 call
   services/orchestration/engine.py               # 1 call
   ```

2. **Recent work in this area?**
   - Last changes to ServiceContainer: Unknown
   - Known issues/quirks: `reset()` classmethod used extensively in tests for cleanup
   - Previous attempts: None known

3. **Actual task needed?**
   - [ ] Create new feature from scratch
   - [ ] Add to existing application
   - [ ] Fix broken functionality
   - [x] Refactor existing code
   - [ ] Other: ____________

4. **Critical context I'm missing?**
   - Is horizontal scaling actually needed for Alpha? (This enables multi-worker deployment)
   - Are there Redis/shared-state considerations for multi-instance deployment?
   - Should we also prepare for multi-tenancy (per-request containers)?

### Part C: Proceed/Revise Decision

After PM verification:
- [x] **PROCEED** - Understanding is correct, gameplan appropriate
- [ ] **REVISE** - Major assumptions wrong, need different approach
- [ ] **CLARIFY** - Need more context on: Alpha vs. production scaling requirements

**✅ PM APPROVED: 2026-01-04 11:07**

PM Decisions:
1. **Priority**: Do it now (Alpha) - architectural debt spreads, we have time
2. **Scope**: Application-scoped only (no multi-tenant prep)
3. **Testing**: All 6 validation scenarios required
4. **Timeline**: 18-24 hours approved, "spend all week if necessary"

PM Guidance: "Thoroughness over speed! Verification over completion claims! Rigor over performance."

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 322
   # ✓ Verified: Issue exists, OPEN, labels: enhancement, priority: high
   ```

2. **Codebase Investigation**
   ```bash
   # Find existing patterns
   grep -r "ServiceContainer()" . --include="*.py"
   # ✓ Found 9 production files, 15+ test files

   # Check current app.state usage
   grep -r "app.state.service_container" . --include="*.py"
   # ✓ Found in web/startup.py (already implemented)

   # Verify test reset pattern
   grep -r "ServiceContainer.reset()" . --include="*.py"
   # ✓ Found in conftest.py and multiple test files
   ```

3. **Update GitHub Issue**
   - [ ] Add investigation findings
   - [ ] Add link to this gameplan
   - [ ] Update status to "In Progress"

### STOP Conditions for Phase 0
- Issue doesn't exist or is wrong number
- Singleton pattern already removed (feature implemented)
- Different problem than described (e.g., not actually blocking scaling)

---

## Phase 1: Foundation - Create Dependency Injection Helper (Non-Breaking)

**Goal**: Create infrastructure for retrieving container from request/app state without breaking existing code.

### Deliverables

1. **Create `web/dependencies.py`** (new file)
   ```python
   from fastapi import Request, Depends
   from services.container import ServiceContainer

   async def get_container(request: Request) -> ServiceContainer:
       """Get ServiceContainer from application state.

       This is the proper dependency injection path for routes.
       Falls back to singleton for backward compatibility during migration.
       """
       if hasattr(request.app.state, 'service_container'):
           return request.app.state.service_container
       # Fallback for backward compatibility (remove after Phase 3)
       return ServiceContainer()
   ```

2. **Create ADR for Container Lifecycle Decision**
   - File: `docs/internal/architecture/current/adrs/adr-XXX-service-container-lifecycle.md`
   - Document: Why application-scoped over per-request
   - Document: Migration path
   - Document: Testing implications

### Acceptance Criteria
- [ ] `web/dependencies.py` created with `get_container()` function
- [ ] ADR written and approved by PM
- [ ] No existing tests broken (backward compatibility maintained)
- [ ] Unit tests for `get_container()`: 3+ tests covering app.state present, fallback, and error cases
- [ ] Integration test: route can retrieve container from DI and access services

### Test Scope
- **Unit tests**: `get_container()` function behavior (3+ tests)
- **Integration tests**: Route-level container access (1+ test)
- **Regression tests**: Existing tests still pass

### Evidence Required
- Terminal output: `pytest tests/unit/web/test_dependencies.py -v`
- Terminal output: `pytest tests/integration/ -v -k container` (if applicable)
- ADR file location and summary

---

## Phase 2: Migrate Production Callers (File-by-File)

**Goal**: Update each production file to receive container via dependency injection or constructor.

### Phase 2A: Update Route-Adjacent Services

These services are called from routes and can easily receive container from request context.

| File | Current | Target | Complexity |
|------|---------|--------|------------|
| `services/intent_service/classifier.py` | `ServiceContainer()` | Constructor injection | Medium |
| `services/intent_service/llm_classifier.py` | `ServiceContainer()` | Constructor injection | Medium |

### Phase 2B: Update Integration Services

| File | Current | Target | Complexity |
|------|---------|--------|------------|
| `services/integrations/github/issue_analyzer.py` | `ServiceContainer()` | Constructor injection | Low |
| `services/knowledge_graph/ingestion.py` | `ServiceContainer()` | Constructor injection | Low |
| `services/orchestration/engine.py` | `ServiceContainer()` | Constructor injection | Medium |

### Phase 2C: Update Entry Points

| File | Current | Target | Complexity |
|------|---------|--------|------------|
| `main.py` | `ServiceContainer()` x2 | App-scoped creation | High |
| `web/startup.py` | `ServiceContainer()` | Already stores in app.state | None |
| `services/container/__init__.py` | Convenience export | Deprecation warning | Low |

### Acceptance Criteria Per File
- [ ] File no longer imports or calls `ServiceContainer()` directly
- [ ] Container received via constructor or function parameter
- [ ] Existing unit tests still pass
- [ ] Integration tests still pass

### Acceptance Criteria Phase 2 Overall
- [ ] All 8 production files migrated
- [ ] No `ServiceContainer()` calls in production code (except container module itself)
- [ ] All existing tests pass
- [ ] New integration test: service wiring with DI container

### Evidence Required
- `grep -r "ServiceContainer()" services/ web/ main.py` returns only container module
- `pytest tests/ -v` full pass

---

## Phase 3: Remove Singleton Pattern

**Goal**: Remove the `__new__` singleton enforcement from ServiceContainer.

### Deliverables

1. **Modify `services/container/service_container.py`**
   - Remove `_instance` class variable
   - Remove `_initialized` class variable
   - Remove `__new__` method
   - Move registry creation to `__init__`
   - Update `reset()` for test compatibility (or deprecate)

2. **Update test fixtures**
   - Modify `conftest.py` to create fresh containers
   - Update any tests using `ServiceContainer.reset()`

### Target Implementation
```python
class ServiceContainer:
    """
    Application-scoped container for service lifecycle management.

    NOT a singleton - one instance per application via FastAPI lifespan.
    For tests, create fresh instances directly.
    """

    def __init__(self):
        """Initialize container with fresh registry."""
        self._registry = ServiceRegistry()
        self._initialized = False  # Instance variable, not class variable

    # ... rest of methods unchanged except reset() ...

    @classmethod
    def reset(cls) -> None:
        """DEPRECATED: For test compatibility only.

        In new tests, create fresh ServiceContainer() instances instead.
        """
        warnings.warn(
            "ServiceContainer.reset() is deprecated. "
            "Create fresh instances in tests instead.",
            DeprecationWarning
        )
```

### Acceptance Criteria
- [ ] `__new__` method removed
- [ ] `_instance` class variable removed
- [ ] Container creates fresh registry in `__init__`
- [ ] `reset()` deprecated but functional for backward compatibility
- [ ] All unit tests pass
- [ ] All integration tests pass

### Evidence Required
- Before/after diff of `service_container.py`
- `pytest tests/ -v` full pass
- `grep "_instance" services/container/service_container.py` returns nothing

---

## Phase 4: Validation - Multi-Worker Testing

**Goal**: Verify the refactoring enables horizontal scaling.

### Deliverables

1. **Multi-worker test script**
   ```bash
   # Start with 4 workers
   uvicorn web.app:app --workers 4 --port 8001

   # Verify each worker has isolated container
   curl http://localhost:8001/api/v1/health  # Multiple times, check logs
   ```

2. **Verification tests**
   - Each worker initializes its own container
   - No shared state between workers
   - Service registry isolated per worker

3. **Update deployment documentation**
   - `docs/operations/deployment.md` (or create if needed)
   - Document multi-worker configuration
   - Document container lifecycle expectations

### Acceptance Criteria - Core
- [ ] App runs successfully with `--workers 4`
- [ ] Each worker logs separate "Creating ServiceContainer" message
- [ ] No cross-worker state pollution
- [ ] Health endpoint works correctly from all workers
- [ ] Documentation updated

### Acceptance Criteria - Full Validation Suite (6 Scenarios)

**Scenario 1: Concurrent Request Test**
- [ ] 10 simultaneous requests to `/api/v1/health`
- [ ] All requests return successfully
- [ ] No state bleeding between requests
- [ ] Responses logged from multiple workers

**Scenario 2: Database Connection Pool**
- [ ] Each worker manages its own connection pool
- [ ] Transaction works correctly with per-worker containers
- [ ] No connection pool exhaustion under load

**Scenario 3: Service Initialization Idempotency**
- [ ] Multiple `initialize()` calls don't corrupt state
- [ ] Services remain functional after repeated initialization
- [ ] No duplicate service registrations

**Scenario 4: Worker Restart Recovery**
- [ ] Kill one worker while others running
- [ ] Remaining workers continue serving requests
- [ ] New worker spawns and initializes correctly
- [ ] No service interruption for users

**Scenario 5: Memory Leak Detection**
- [ ] Run for 10 minutes under continuous load
- [ ] Memory usage remains stable (no unbounded growth)
- [ ] Before/after memory metrics documented

**Scenario 6: Graceful Shutdown**
- [ ] Send SIGTERM to master process
- [ ] All workers clean up properly
- [ ] No orphaned connections or resources
- [ ] Clean shutdown logs from all workers

### Evidence Required
- Terminal output from multi-worker startup showing 4 container initializations
- Scenario 1: `curl` output for 10 concurrent requests + worker PID logs
- Scenario 2: Database transaction test output
- Scenario 3: Repeated initialization test output
- Scenario 4: Worker kill/recovery terminal session
- Scenario 5: Memory metrics (before/after 10 minutes)
- Scenario 6: Graceful shutdown logs
- Documentation file location

---

## Phase Z: Final Bookending & Handoff

### GitHub Final Update
```bash
gh issue edit 322 --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] Phase 1: DI helper created, ADR written
- [x] Phase 2: All 8 production files migrated
- [x] Phase 3: Singleton pattern removed
- [x] Phase 4: Multi-worker deployment verified

### Files Modified
- web/dependencies.py (new)
- services/container/service_container.py
- main.py
- services/intent_service/classifier.py
- services/intent_service/llm_classifier.py
- services/integrations/github/issue_analyzer.py
- services/knowledge_graph/ingestion.py
- services/orchestration/engine.py
- services/container/__init__.py
- tests/conftest.py
- docs/internal/architecture/current/adrs/adr-XXX-*.md (new)

### Test Results
- Unit tests: XXX passed
- Integration tests: XXX passed
- Multi-worker: Verified with 4 workers

### Ready for PM Review
"
```

### Documentation Updates
- [ ] ADR created for container lifecycle decision
- [ ] Deployment docs updated for multi-worker
- [ ] CLAUDE.md updated if container access pattern changes

### Success Criteria Template

### Issue Completion Requires
- [ ] All acceptance criteria met (all phases)
- [ ] Evidence provided for each criterion
- [ ] Tests passing (with output)
- [ ] No regressions introduced
- [ ] Documentation updated
- [ ] GitHub issue fully updated
- [ ] PM approval received

---

## Multi-Agent Coordination Plan

### Agent Deployment Map
| Phase | Agent Type | Focus | Evidence Required | Handoff |
|-------|------------|-------|------------------|---------|
| 1 | Code Agent | DI helper + ADR | 3+ unit tests, ADR file | Test locations, ADR path |
| 2A-2C | Code Agent | File migrations | grep output, test results | Modified file list |
| 3 | Code Agent | Singleton removal | Diff, test pass | Container code |
| 4 | Lead Dev | Multi-worker validation | Terminal logs, curl results | Deployment doc |

### Verification Gates
- [ ] Phase 1: DI helper tests passing
- [ ] Phase 2: No direct `ServiceContainer()` calls in production
- [ ] Phase 3: Unit + integration tests passing
- [ ] Phase 4: Multi-worker deployment verified

### Evidence Collection Points
1. **After each subagent returns**: Collect evidence immediately
2. **Before phase transition**: Verify accumulated evidence
3. **Before issue closure**: Compile all evidence into GitHub issue
4. **At session end**: Update session log and omnibus log

### Handoff Quality Checklist
Before accepting handoff from any agent:
- [ ] All acceptance criteria checkboxes addressed
- [ ] Test output provided (not just "tests pass")
- [ ] Files modified list included
- [ ] User verification steps documented
- [ ] Blockers explicitly stated (if any)

---

## Discovered Work Protocol

During this 16-20 hour refactoring, additional issues WILL be discovered. Follow Beads discipline:

1. Discover work mid-implementation → `bd create "Title"`
2. Link to parent → `bd dep add <new> 322 --type discovered-from`
3. Continue current phase unless PM redirects
4. PM decides priority of discovered work

**Anti-pattern**: Do NOT rationalize discovered work as "part of #322" without tracking.

---

## STOP Conditions

Stop immediately and escalate if:
- Tests fail after any phase
- Services can't retrieve container via DI
- Multi-worker startup fails
- Unexpected state sharing detected between workers
- Performance degradation >10% on startup

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Tests break during migration | Medium | High | Phase-by-phase with full test suite runs |
| Service wiring breaks | Medium | High | Backward-compatible fallback in Phase 1 |
| Performance regression | Low | Medium | Benchmark startup time before/after |
| Multi-worker issues | Low | High | Explicit Phase 4 validation |
| Database sessions behave differently | Low | Medium | Phase 4 includes DB transaction test |

---

## What Counts as Evidence

**Valid Evidence:**
- Terminal output showing success (paste actual output)
- Test results with full output (not just "tests pass")
- Performance metrics (before/after numbers)
- Git commits/diffs (actual hashes)
- `curl` responses (actual output)

**Invalid Evidence:**
- "Should work"
- "Tests pass" without output
- "Fixed" without proof
- Assumptions about behavior

---

## Open Questions for PM

~~1. **Priority**: Is horizontal scaling needed for Alpha, or is this post-Alpha work?~~
~~2. **Scope**: Should we also prepare for per-request containers (multi-tenant)?~~
~~3. **Testing**: Any specific scenarios to validate beyond multi-worker?~~
~~4. **Timeline**: Is 16-20 hours acceptable for Sprint A12?~~

**All questions resolved - see Phase -1 Part C for PM decisions**

---

*Gameplan created by Lead Developer (Claude Code Opus), 2026-01-04*
*Phase -1 approved by PM: 2026-01-04 11:07*
*Execution begun: 2026-01-04 11:07*
