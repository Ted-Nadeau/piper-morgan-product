# Memo: "Green Tests, Red User" Pattern and Prevention Strategies

**To**: Chief Architect
**From**: Chief of Staff (for PM)
**Date**: December 11, 2025
**Re**: Integration Testing Quality Gates - Operationalizing Alpha Testing Insights

---

## Context

During Dec 7's alpha testing session, Michelle encountered complete CRUD failures across all entity pages (Todos, Projects, Files, Lists) despite passing unit tests. Lead Developer conducted systematic debugging that revealed **6 sequential root causes**, culminating in the discovery of a schema/model UUID type mismatch that was the underlying failure for all operations.

This incident revealed a critical pattern worth operationalizing into our quality gates and methodology.

---

## The "Green Tests, Red User" Pattern

**Definition**: Unit tests with mocks pass cleanly, but real user testing against actual database reveals systematic failures.

**What Happened Dec 7**:
- ✅ All unit tests passing (705 tests, 100% success)
- ✅ Individual components working in isolation
- ❌ All CRUD operations failing for real users
- ❌ Integration between components breaking at SQL execution

**Root Cause**: Database schema defined `owner_id` columns as `uuid` type, but SQLAlchemy models defined them as `String`. PostgreSQL rejected type mismatch at SQL execution time. This affected 5 models: ProjectDB, KnowledgeNodeDB, KnowledgeEdgeDB, ListMembershipDB, ListItemDB.

**Why It Escaped Detection**:
1. Unit tests with mocks bypass actual database type checking
2. Schema migrations changed types but models weren't updated
3. PostgreSQL is strict about types (no auto-casting)
4. Previous fixes addressed symptoms but not root cause
5. No integration tests hitting real PostgreSQL database

---

## Prevention Strategies Documented

From Dec 7 Lead Developer session, these strategies were identified:

### 1. Integration Tests Must Hit Real PostgreSQL
- Unit tests catch logic errors
- Integration tests catch schema/model drift
- Both are necessary, neither sufficient alone

### 2. Schema Validation Check on Startup
- Automated validation that SQLAlchemy models match database schema
- Fail fast if type mismatches detected
- Prevents deployment with drift

### 3. Post-Migration Model Audit
- After any migration adding `owner_id` or similar columns
- Systematic audit of affected models
- Pattern: All `owner_id` refs to `users.id` → `postgresql.UUID(as_uuid=False)`

### 4. Real Database in CI/CD
- T2 Sprint now provides this foundation
- 602 smoke tests marked (<3 seconds execution)
- Can run against actual PostgreSQL in CI pipeline

---

## Proposed Quality Gates

### For Lead Developer Sessions
**Gate 1**: "Done" now means "user can use it" not "code complete"
- Before closing issues, verify with real database
- Test CRUD operations through full stack
- Catch integration gaps before PM testing

### For Test Infrastructure
**Gate 2**: Integration test coverage for core flows
- Alpha user journey smoke tests
- Real database, real auth, real sessions
- Complement unit test suite (not replace)

### For Architecture Reviews
**Gate 3**: Schema/model drift detection
- Automated startup validation
- Post-migration audit checklist
- Type consistency enforcement

---

## Methodology Insights

### Pattern Recognition
This incident demonstrates why "test-driven development" requires **integration-driven testing** not just unit-driven testing. The Swiss cheese model: each layer (DI, routes, repositories, models, schema) worked individually but alignment between layers failed.

### Verification Theater vs. Real Verification
- Unit tests provided false confidence
- Real user testing revealed truth
- Our "inchworm protocol" (100% complete before moving forward) caught this because Michelle's testing was thorough

### Time Lord Doctrine Application
PM's insight during this debugging: "Priority ≠ rush. Priority signals what to work on next. Pace should remain deliberate, craft-focused."

The 24-hour debugging session (7:06 AM Dec 7 → 6:48 AM Dec 8) was thorough, systematic, and ultimately successful because we didn't rush to "fix" symptoms without finding root cause.

---

## Recommended Actions

### Immediate (This Week)
1. Document "Green Tests, Red User" pattern in methodology handbook
2. Add to Excellence Flywheel as integration testing discipline
3. Update session templates to include integration verification checklist

### Short-term (Next Sprint)
1. Create schema validation startup check (Issue scope: 4-6 hours)
2. Expand smoke tests to include CRUD operations (T2 foundation exists)
3. Add post-migration audit to gameplan template

### Long-term (Post-Alpha)
1. Automate schema/model drift detection in CI/CD
2. Expand integration test coverage to all alpha user journeys
3. Consider contract testing for API/database boundaries

---

## Connection to Existing Methodology

This pattern reinforces several existing principles:

**Verification First** (Pattern-006): "Concrete evidence of completion before moving forward"
- Integration testing provides that evidence
- Unit tests alone are insufficient evidence

**Excellence Flywheel** (Methodology-00): "TDD requirements → Multi-agent coordination → Systematic breakthroughs"
- This debugging session was systematic breakthrough
- Now we operationalize learning into TDD requirements

**Cross-Validation Protocol** (Pattern-010): "Multiple perspectives catch what single view misses"
- Unit tests = developer perspective
- Integration tests = system perspective
- User testing = reality perspective

---

## Questions for Chief Architect

1. **Priority**: Should schema validation startup check be added to S2 Sprint or deferred to post-alpha?

2. **Scope**: Should we scope integration test expansion as separate epic, or fold into existing test infrastructure work?

3. **Automation**: At what point do we invest in automated schema/model drift detection? (Current manual audit works for alpha)

4. **Documentation**: Where should "Green Tests, Red User" pattern live? New ADR? Pattern catalog? Methodology doc?

---

## Success Metrics

We'll know this is operationalized when:

- ✅ No CRUD operation ships without integration test against real database
- ✅ Schema/model drift caught before deployment
- ✅ "Done" means verified by user, not just passing tests
- ✅ CI/CD includes integration smoke tests
- ✅ Pattern recognized and named in team vocabulary

---

**Next Steps**: Awaiting Chief Architect's guidance on priority, scope, and documentation location for operationalizing these insights.

---

*Filed: December 11, 2025*
*Source: Dec 7 omnibus log analysis + Dec 9 T2 Sprint completion*
*Related: Methodology Excellence Flywheel, Pattern-006 Verification First, T2 Sprint completion*
