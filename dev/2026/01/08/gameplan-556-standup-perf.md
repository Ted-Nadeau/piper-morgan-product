# Gameplan: #556 STANDUP-PERF - Performance & Reliability

**Issue**: #556
**Epic**: #242 (CONV-MCP-STANDUP-INTERACTIVE)
**Priority**: P1
**Created**: 2026-01-08
**Template Version**: 9.2

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (verified)
- [x] Database: PostgreSQL on 5433 (verified)
- [x] Testing framework: pytest (verified)
- [x] Existing standup services: `services/standup/` with conversation_handler, conversation_manager, preference_* modules
- [x] Performance test infrastructure: `tests/performance/`, `tests/integration/test_performance_baseline.py`
- [x] Logging: structlog used throughout codebase (verified in standup modules)
- [x] Health monitoring: ADR-009 defines comprehensive health monitoring with Prometheus integration

**Monitoring Infrastructure Investigation** (Phase -1 due diligence):
- **ADR-009**: Health Monitoring System - defines `/health/*` endpoints, Prometheus metrics
- **Existing logging**: `services/standup/` already uses structlog with structured events:
  - `conversation_manager.py`: `standup_conversation_expired`, state transitions
  - `conversation_handler.py`: `standup_generation_failed`
  - `preference_*.py`: preference extraction, correction, save events
- **Prometheus integration**: Available per ADR-009, can add standup-specific metrics
- **No dedicated standup performance metrics yet** - this is the gap to fill

**My understanding of the task**:
- Profile current standup conversation response times
- Optimize to meet <500ms per turn target
- Ensure no memory leaks in 20+ turn conversations
- Implement error recovery for network/service failures
- Add monitoring/logging for production observability (extend existing structlog pattern)
- Validate with load testing (minimal concurrent load for alpha)

**Dependencies verified**:
- [x] #552 (State Management) - **CLOSED** (verified in #555 session)
- [x] #553 (Conversation Flow) - **CLOSED** (verified in #555 session)
- [x] #554 (Chat Widget) - **CLOSED** (verified)
- [x] #555 (Learning) - **CLOSED** (just completed 2026-01-08)

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel - **Not applicable**
- [x] Task duration >30 minutes - **Yes**
- [ ] Multi-component work - **No (backend only)**
- [x] Exploratory/risky changes - **Profiling may reveal unexpected issues**

Worktrees ADD overhead when:
- [x] Single agent, sequential work - **Yes**
- [ ] Small fixes (<15 min) - **No**
- [ ] Tightly coupled files - **No**
- [ ] Time-critical - **No**

**Assessment**:
- [ ] **USE WORKTREE**
- [x] **SKIP WORKTREE** - Single agent, sequential phases, exploratory but not high-risk

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What actually exists in the filesystem?**
   ```bash
   ls -la services/standup/
   ls -la tests/performance/
   ls -la tests/integration/test_performance*.py
   ```

2. **Recent work in this area?**
   - Last changes: #555 (Learning) just completed
   - Known issues/quirks: None identified yet
   - Previous attempts: Performance baseline tests exist but may need updating

3. **Actual task needed?**
   - [ ] Create new feature from scratch
   - [x] Add to existing application (optimization/reliability layer)
   - [ ] Fix broken functionality
   - [ ] Refactor existing code

4. **Critical context I'm missing?**
   - ~~Acceptable load profile for testing (concurrent users?)~~ **PM answered: Alpha rarely >1 concurrent user, minimal load needed**
   - ~~Existing monitoring/alerting infrastructure~~ **Investigated: ADR-009 + structlog in place, extend existing patterns**
   - Any known performance bottlenecks? **TBD in Phase 0 profiling**

### Part B: PM Decisions (Received 2026-01-08 5:02 PM)

1. **Load profile**: Alpha testers rarely have >1 concurrent user. Minimal load testing sufficient.
   - Adjusted Phase 5 scope: Single-user baseline, optional 2-3 concurrent test

2. **Monitoring infrastructure**: Warrants investigation (completed above)
   - ADR-009 health monitoring exists
   - structlog already used in standup modules
   - Extend existing patterns, no new infrastructure needed

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - All dependencies satisfied, infrastructure understood, PM questions answered
- [ ] **BLOCKED** - Dependencies incomplete
- [ ] **CLARIFY** - Need more context

---

## Phase 0: Initial Bookending - Profiling & Baseline

### Purpose
Establish current performance baseline before optimization.

### Required Actions

1. **Verify dependencies complete**
   ```bash
   gh issue view 555 --json state -q '.state'
   # Must return "CLOSED"
   ```

2. **Profile current conversation response times**
   ```python
   # Create profiling script
   import time
   import asyncio
   from services.standup.conversation_handler import StandupConversationHandler

   async def profile_conversation():
       handler = StandupConversationHandler(...)
       times = []

       # Simulate 10-turn conversation
       for i in range(10):
           start = time.time()
           response = await handler.handle_turn(user_id, f"Turn {i}")
           elapsed = time.time() - start
           times.append(elapsed)
           print(f"Turn {i}: {elapsed:.3f}s")

       print(f"P50: {sorted(times)[len(times)//2]:.3f}s")
       print(f"P95: {sorted(times)[int(len(times)*0.95)]:.3f}s")
   ```

3. **Profile memory usage**
   ```python
   import tracemalloc

   tracemalloc.start()
   # Run 20-turn conversation
   snapshot = tracemalloc.take_snapshot()
   # Analyze memory growth
   ```

4. **Update GitHub Issue**
   ```bash
   gh issue comment 556 -b "## Phase 0: Profiling Started
   - [ ] Response time baseline established
   - [ ] Memory usage baseline established
   - [ ] Bottlenecks identified"
   ```

### Deliverables
- Baseline metrics documented
- Bottleneck analysis
- Optimization targets identified

### STOP Conditions
- Current performance already meets <500ms target → Skip Phase 1, proceed to Phase 2
- Memory usage shows no growth → Skip Phase 2, proceed to Phase 3
- Infrastructure issues prevent profiling → Escalate

---

## Phase 0.5: Frontend-Backend Contract Verification

**SKIP** - This issue is backend-only performance work. No new UI or API endpoints.

---

## Phase 1: Performance Optimization

**Deploy**: Lead Developer (Opus) - judgment needed for optimization strategies

### Objective
Meet <500ms response time target (p95).

### Tasks

1. **Address identified bottlenecks**
   - Analyze profiling data from Phase 0
   - Common suspects:
     - LLM API calls (if any)
     - Database queries
     - JSON serialization/deserialization
     - File I/O (preference storage)

2. **Implement caching where appropriate**
   ```python
   # Example: Cache frequently accessed preferences
   from functools import lru_cache

   @lru_cache(maxsize=100)
   def get_cached_preferences(user_id: str) -> Dict:
       # Expire cache after session ends
   ```

3. **Optimize hot paths**
   - Reduce unnecessary computations
   - Batch database operations if applicable
   - Consider async parallelization

4. **Measure improvement**
   ```bash
   # Before/after comparison
   python -m pytest tests/performance/test_standup_*.py -v
   ```

### Deliverables
- Optimized code with before/after metrics
- Response time <500ms at p95

### Evidence Required
- Profiling output showing improvement
- Test showing response time meets target

### Progressive Bookending
```bash
gh issue comment 556 -b "✓ Phase 1 complete: Performance optimization
- Before: [X]ms p95
- After: [Y]ms p95
- Optimization: [what was done]
Next: Phase 2 (memory)"
```

---

## Phase 2: Memory Optimization

**Deploy**: Lead Developer (Opus)

### Objective
No memory leaks in long conversations (20+ turns).

### Tasks

1. **Test 20+ turn conversation memory**
   ```python
   # tests/performance/test_standup_memory.py
   @pytest.mark.performance
   async def test_memory_stable_20_turns():
       import tracemalloc

       tracemalloc.start()
       handler = StandupConversationHandler(...)

       # Initial snapshot
       initial = tracemalloc.take_snapshot()

       # Run 20 turns
       for i in range(20):
           await handler.handle_turn(user_id, f"Turn {i}")

       # Final snapshot
       final = tracemalloc.take_snapshot()

       # Compare
       diff = final.compare_to(initial, 'lineno')
       growth = sum(stat.size_diff for stat in diff if stat.size_diff > 0)

       # Assert no significant growth (allow 1MB max)
       assert growth < 1_000_000, f"Memory grew by {growth} bytes"
   ```

2. **Implement conversation cleanup**
   - Clear completed conversation state
   - Release temporary resources
   - Garbage collect if needed

3. **Add memory monitoring**
   ```python
   # In conversation handler
   import structlog

   logger = structlog.get_logger()

   async def handle_turn(self, ...):
       # Log memory periodically
       if turn_number % 5 == 0:
           import tracemalloc
           current, peak = tracemalloc.get_traced_memory()
           logger.info("memory_status", current_mb=current/1e6, peak_mb=peak/1e6)
   ```

### Deliverables
- Memory stability test passing
- Conversation cleanup implemented
- Memory monitoring in place

### Evidence Required
- Test output showing stable memory over 20 turns
- Cleanup verification

### Progressive Bookending
```bash
gh issue comment 556 -b "✓ Phase 2 complete: Memory optimization
- Memory stable over 20 turns
- Growth: <1MB
- Cleanup implemented
Next: Phase 3 (error recovery)"
```

---

## Phase 3: Error Recovery

**Deploy**: Lead Developer (Opus)

### Objective
Graceful handling of failures with context preservation.

### Tasks

1. **Handle network interruption mid-conversation**
   ```python
   # Implement retry logic
   from tenacity import retry, stop_after_attempt, wait_exponential

   @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
   async def _call_external_service(self, ...):
       # Network-dependent calls
   ```

2. **Handle service errors (calendar down, etc.)**
   ```python
   async def _handle_gathering(self, context):
       try:
           calendar_data = await self._get_calendar_events()
       except CalendarServiceError as e:
           logger.warning("calendar_unavailable", error=str(e))
           # Continue with degraded mode
           calendar_data = {"status": "unavailable", "message": "Calendar temporarily unavailable"}
   ```

3. **Preserve conversation context on recovery**
   - State saved before risky operations
   - Restore point after recovery
   - User notified of recovery

4. **User-friendly error messages**
   ```python
   ERROR_MESSAGES = {
       "network": "I'm having trouble connecting. Give me a moment...",
       "calendar": "Calendar is temporarily unavailable. I'll include what I can.",
       "github": "Couldn't reach GitHub. Proceeding with other information.",
   }
   ```

### Deliverables
- Retry logic for network calls
- Graceful degradation for service failures
- Context preservation on recovery
- Clear user messaging

### Evidence Required
- Test showing recovery from network drop
- Test showing degraded mode works
- Test showing context preserved

### Progressive Bookending
```bash
gh issue comment 556 -b "✓ Phase 3 complete: Error recovery
- Retry logic implemented
- Graceful degradation for [list services]
- Context preservation verified
Next: Phase 4 (monitoring)"
```

---

## Phase 4: Monitoring Integration

**Deploy**: Lead Developer (Opus)

### Objective
Production observability for standup conversations (extending existing structlog infrastructure).

### Context (from Phase -1 investigation)
- ADR-009 health monitoring system exists with Prometheus integration
- Standup modules already use structlog with structured events
- **Gap**: No dedicated standup conversation performance metrics
- **Approach**: Extend existing patterns, add conversation lifecycle events

### Tasks

1. **Extend existing structlog patterns for conversation lifecycle**
   ```python
   # services/standup/conversation_handler.py (already imports structlog)
   logger.info("standup_conversation_started", user_id=user_id, session_id=session_id)
   logger.info("standup_turn_completed", turn_number=n, duration_ms=duration)
   logger.info("standup_conversation_completed",
               total_turns=n,
               total_duration_ms=total,
               success=True)
   ```

2. **Add performance timing logs** (follow existing pattern in preference_*.py)
   ```python
   import time

   async def handle_turn(self, ...):
       start = time.time()
       # ... work ...
       duration_ms = (time.time() - start) * 1000

       logger.info("standup_turn_performance",
                   duration_ms=duration_ms,
                   p95_target_ms=500,
                   meets_target=duration_ms < 500)
   ```

3. **Enhance existing error logging** (already has `standup_generation_failed`)
   ```python
   # Extend with recovery context
   logger.error("standup_error",
                error_type=type(e).__name__,
                recoverable=True,
                action="retry",
                turn_number=n)
   ```

4. **Document metrics for dashboards** (per ADR-009 pattern)
   - Conversation start/end/duration
   - Turn count and timing
   - Error rates and types
   - Can be queried via structlog output

### Deliverables
- Structured logging for all conversation events (extending existing)
- Performance timing in logs
- Error tracking with recovery context
- Brief metrics documentation

### Evidence Required
- Log output showing conversation lifecycle
- Performance metrics visible in logs

### Progressive Bookending
```bash
gh issue comment 556 -b "✓ Phase 4 complete: Monitoring integration
- Extended existing structlog patterns
- Conversation lifecycle logged (start, turn, end)
- Performance timing in place (duration_ms, meets_target)
- Error tracking with recovery context
Next: Phase 5 (load testing)"
```

---

## Phase 5: Load Testing

**Deploy**: Lead Developer (Opus)

### Objective
Validate performance under realistic alpha load (minimal per PM guidance).

### Context (PM Decision 2026-01-08)
- Alpha testers rarely have >1 concurrent user
- Minimal load testing sufficient
- Focus on single-user baseline, optional light concurrency test

### Tasks

1. **Define alpha-realistic load profile**
   - Primary: Single user, 10-turn conversation
   - Secondary (optional): 2-3 concurrent conversations
   - Turns per conversation: 5-10

2. **Create baseline performance test** (primary)
   ```python
   # tests/performance/test_standup_performance.py
   @pytest.mark.performance
   async def test_standup_single_user_performance():
       """Test single-user conversation meets p95 target."""
       handler = StandupConversationHandler(...)
       times = []

       for i in range(10):
           start = time.time()
           await handler.handle_turn(user_id, f"Turn {i}")
           times.append(time.time() - start)

       p95 = sorted(times)[int(len(times) * 0.95)]
       assert p95 < 0.5, f"P95: {p95:.3f}s (target: 0.5s)"
   ```

3. **Create optional light concurrency test** (if time permits)
   ```python
   @pytest.mark.performance
   async def test_standup_light_concurrency():
       """Test 2-3 concurrent conversations (alpha realistic max)."""
       import asyncio

       async def run_conversation(user_id):
           handler = StandupConversationHandler(...)
           times = []
           for i in range(5):
               start = time.time()
               await handler.handle_turn(user_id, f"Turn {i}")
               times.append(time.time() - start)
           return times

       # Run 3 concurrent conversations (alpha max realistic)
       results = await asyncio.gather(*[
           run_conversation(f"user-{i}") for i in range(3)
       ])

       all_times = [t for r in results for t in r]
       p95 = sorted(all_times)[int(len(all_times) * 0.95)]
       assert p95 < 0.5, f"P95 under load: {p95:.3f}s (target: 0.5s)"
   ```

4. **Document baseline performance**
   - Single-user p95 response time
   - Any observed bottlenecks
   - Note: Heavy load testing deferred (alpha doesn't need it)

### Deliverables
- Single-user performance test (required)
- Light concurrency test (optional)
- Baseline performance documented

### Evidence Required
- Test output showing p95 meets <500ms target
- Brief performance documentation

### Progressive Bookending
```bash
gh issue comment 556 -b "✓ Phase 5 complete: Load testing
- Single-user p95: [X]ms (target: 500ms)
- Light concurrency: [tested/skipped per scope]
- Heavy load testing: Deferred (alpha scope)
Next: Phase Z (completion)"
```

---

## Phase Z: Final Bookending & Handoff

### Final Verification Checklist

- [ ] Response time <500ms per turn (p95)
- [ ] Memory stable in 20+ turn conversations
- [ ] Error recovery preserves context
- [ ] Monitoring/logging in place (extended structlog patterns)
- [ ] Single-user performance test passed
- [ ] All tests passing
- [ ] No regressions to existing standup functionality

### Documentation Updates
- [ ] Code documentation complete
- [ ] Session log finalized
- [ ] Performance metrics documented

### Evidence Compilation
- [ ] Profiling before/after in session log
- [ ] Test output attached to issue
- [ ] Load test results documented

### GitHub Final Update
```bash
gh issue comment 556 -b "## Issue #556 Complete - Ready for PM Review

### Evidence Summary
- [x] Response time: [X]ms p95 (target: 500ms)
- [x] Memory: Stable over 20 turns (<1MB growth)
- [x] Error recovery: [scenarios covered]
- [x] Monitoring: Extended structlog with conversation lifecycle
- [x] Performance test: Single-user p95 [X]ms
- [x] All tests passing (output attached)
- [x] No regressions confirmed

### Files Created/Modified
- tests/performance/test_standup_performance.py (new)
- tests/performance/test_standup_memory.py (new)
- tests/performance/test_standup_load.py (new)
- services/standup/conversation_handler.py (modified - monitoring, error recovery)
- services/standup/preference_service.py (modified - if caching added)

### Ready for PM Review"
```

---

## Verification Gates

- [ ] **Phase 0 Gate**: Baseline metrics established (PM will validate)
- [ ] **Phase 1 Gate**: Response time <500ms p95 (PM will validate)
- [ ] **Phase 2 Gate**: Memory stable over 20 turns (PM will validate)
- [ ] **Phase 3 Gate**: Error recovery tests passing (PM will validate)
- [ ] **Phase 4 Gate**: Monitoring logging verified (PM will validate)
- [ ] **Phase 5 Gate**: Single-user performance test passing (PM will validate)
- [ ] **Phase Z Gate**: No regressions, all tests passing (PM will validate)

---

## Handoff Quality Checklist

Before accepting handoff from any agent/phase:
- [ ] All acceptance criteria checkboxes addressed
- [ ] Test output provided (not just "tests pass")
- [ ] Performance metrics included
- [ ] Files modified list included
- [ ] Blockers explicitly stated (if any)

---

## Multi-Agent Deployment Map

| Phase | Agent Type | Model | Rationale |
|-------|------------|-------|-----------|
| 0 | Lead Dev | Opus | Profiling analysis, judgment |
| 1 | Lead Dev | Opus | Optimization decisions |
| 2 | Lead Dev | Opus | Memory analysis |
| 3 | Lead Dev | Opus | Error handling design |
| 4 | Lead Dev | Opus | Monitoring strategy |
| 5 | Lead Dev | Opus | Load test design |
| Z | Lead Dev | Opus | Final verification |

**Note**: This is primarily Lead Dev work due to the judgment calls needed for optimization strategies and performance analysis.

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] Any dependency (#552-555) not complete
- [ ] Performance cannot meet <500ms without major rearchitecture
- [ ] Memory leaks unfixable without major changes
- [ ] Tests fail for any reason
- [ ] Existing standup functionality breaks

---

## Effort Estimate

**Overall Size**: Small-Medium (1-2 days)

| Phase | Estimate | Cumulative |
|-------|----------|------------|
| Phase 0 | 1-2 hours | 1-2 hours |
| Phase 1 | 1-2 hours | 2-4 hours |
| Phase 2 | 1 hour | 3-5 hours |
| Phase 3 | 1-2 hours | 4-7 hours |
| Phase 4 | 1 hour | 5-8 hours |
| Phase 5 | 1 hour | 6-9 hours |
| Phase Z | 30 min | ~1-1.5 days |

---

## Dependencies

### Required (All complete)
- [x] #552 (State Management) - **CLOSED**
- [x] #553 (Conversation Flow) - **CLOSED**
- [x] #554 (Chat Widget) - **CLOSED**
- [x] #555 (Learning) - **CLOSED**

### Enables
- #242 Epic closure (this is the final child issue)

---

## Remember

- All dependencies satisfied (#552, #553, #554, #555 all closed)
- Evidence required for all claims
- No 80% completions
- Profiling first, optimize second
- PM closes issues after approval
- This is the final issue before Epic #242 can be closed

---

*Gameplan created: 2026-01-08*
*Template version: 9.2*
