# Request for Chief Architect Gameplan: Issue #292

**Date**: November 11, 2025, 9:45 PM
**Requested By**: Lead Developer
**For**: Chief Architect
**Issue**: #292 - CORE-ALPHA-AUTH-INTEGRATION-TESTS

---

## Issue Summary

**Title**: Add Integration Tests for Auth (Reduce Mocking)
**Priority**: P3 (Quality Improvement)
**Type**: Testing Infrastructure + Implementation
**Estimated Effort**: 3 hours (implementation once architecture decided)

**Current Problem**: Auth tests (15/15 passing) heavily rely on mocks, particularly for database operations and token blacklist checking. While unit tests are valuable, they don't catch integration issues.

**Recent Evidence**: During Issue #281 (JWT Auth), manual testing revealed:
1. Token blacklist FK constraint violation (not caught by tests)
2. Logout not actually blacklisting tokens (tests mocked it)
3. Async session conflicts (hidden by mocks)

**PM's Quote**:
> "I don't love that a lot of these tests use mocks. I know mocks are needed in unit tests but we also need integration testing... the truth will out!"

---

## Why Requesting Gameplan

### Architectural Decisions Needed

This isn't just "write more tests" - it requires architectural decisions about testing infrastructure:

**1. Test Isolation Strategy**
- How do we use a real database without tests affecting each other?
- Fixture-based cleanup? Transaction rollback? Separate test DB?
- What's the right balance between isolation and real behavior?

**2. Database Fixture Architecture**
- Do we override `get_db_session()` or use real sessions?
- How do we avoid the "mocking trap" while maintaining test speed?
- What cleanup strategy prevents test pollution?

**3. Integration vs Unit Test Boundaries**
- What should be integration tested vs unit tested?
- How many integration tests is the right number? (5? 10? 20?)
- What's our testing pyramid strategy?

**4. Performance Considerations**
- Integration tests are slower - what's acceptable? (30s? 60s? 120s?)
- Should they run on every commit or just pre-deploy?
- How do we keep them fast enough to be useful?

**5. CI/CD Integration**
- How do integration tests fit into the pipeline?
- Different environments for unit vs integration?
- When do they block merges?

### Why Chief Architect Should Decide

**Lead Dev Perspective**: I can write tests, but architectural decisions about testing infrastructure should be intentional and systematic.

**Chief Architect Expertise**:
- Overall system architecture vision
- Testing strategy across the project
- Performance trade-off decisions
- Long-term maintenance considerations

**Better Outcome**: A gameplan from Chief Architect will result in:
- Cleaner testing architecture
- Better integration with existing patterns
- Decisions documented in ADR format
- Testing strategy that scales

---

## What's Already Known

### Current Test Architecture

**Unit Tests** (Fast, Mocked):
```python
# tests/conftest.py - Global mock
@pytest.fixture(autouse=True)
async def mock_token_blacklist():
    """Mocks TokenBlacklist.is_blacklisted() for ALL tests"""
    with patch("services.auth.models.TokenBlacklist.is_blacklisted", return_value=False):
        yield

# Tests override database
async def test_login_success(async_client, db_session):
    # db_session overrides real database
```

**Current Strengths**:
- Fast (tests run in ~3 seconds)
- Isolated (no database dependency)
- Good for TDD

**Current Weaknesses**:
- Mocks hide integration bugs
- Can't test real FK constraints
- Can't test actual transaction behavior
- False confidence (tests pass, but real system broken)

### What Integration Tests Should Cover

**Critical Flows** (from PM's observation):
1. Full auth lifecycle (login → use → logout → verify blacklisted)
2. Multi-user isolation (users can't access each other's data)
3. Token expiration (tokens actually expire)
4. Concurrent operations (race conditions)
5. Password change invalidation (old tokens stop working)

**Additional Scenarios** (if time permits):
6. FK cascade behavior (user deletion cascades to tokens)
7. Session management (multiple sessions per user)
8. Rate limiting (if implemented)
9. API key rotation impact
10. Cross-environment behavior

### Known Constraints

**Database**: PostgreSQL via Docker (port 5432 or 5433)
**Framework**: FastAPI with SQLAlchemy async
**Test Framework**: pytest with pytest-asyncio
**Current Coverage**: 100% pass rate for unit tests (250+ tests)

**Performance Target**: Integration tests should complete in < 60 seconds total

---

## Questions for Chief Architect

### 1. Test Isolation Strategy

**Question**: How should integration tests achieve database isolation?

**Options**:
- **Option A**: Transaction rollback after each test
  - Pros: Fast, clean
  - Cons: Doesn't test actual commit behavior

- **Option B**: Truncate tables after each test
  - Pros: Tests real commits
  - Cons: Slower, potential for conflicts

- **Option C**: Separate test database per test
  - Pros: Maximum isolation
  - Cons: Very slow, complex setup

**Your Recommendation**: _______________

**Rationale**: _______________

---

### 2. Database Fixture Design

**Question**: Should integration tests use real `get_db_session()` or a test fixture?

**Options**:
- **Option A**: Use real `get_db_session()`, just with test database
  - Pros: Tests exact production code path
  - Cons: Harder to clean up

- **Option B**: Test-specific fixture that mimics production
  - Pros: Easier cleanup
  - Cons: Slight deviation from production

- **Option C**: Hybrid - real sessions with cleanup hooks
  - Pros: Balance of both
  - Cons: More complex

**Your Recommendation**: _______________

**Rationale**: _______________

---

### 3. Testing Pyramid Balance

**Question**: What's the right ratio of unit to integration tests?

**Current**: 15 unit tests, 0 integration tests

**Options**:
- **Option A**: Heavy unit, light integration (15:5 ratio)
  - 15 unit tests (keep current)
  - 5 integration tests (critical flows only)

- **Option B**: Balanced (15:10 ratio)
  - 15 unit tests (keep current)
  - 10 integration tests (comprehensive coverage)

- **Option C**: Integration-heavy (15:15 ratio)
  - 15 unit tests (keep current)
  - 15 integration tests (duplicate some unit tests)

**Your Recommendation**: _______________

**Rationale**: _______________

---

### 4. Performance Budget

**Question**: What's acceptable for integration test runtime?

**Current**: Unit tests run in ~3 seconds

**Options**:
- **Option A**: < 30 seconds (can run frequently)
- **Option B**: < 60 seconds (run before deploy)
- **Option C**: < 120 seconds (comprehensive but slower)

**Your Recommendation**: _______________

**Trade-offs you're optimizing for**: _______________

---

### 5. CI/CD Strategy

**Question**: How should integration tests fit into CI/CD?

**Options**:
- **Option A**: Run on every commit (alongside unit tests)
  - Pros: Catch issues immediately
  - Cons: Slower feedback loop

- **Option B**: Run on PR only (not every commit)
  - Pros: Faster local development
  - Cons: Integration issues discovered later

- **Option C**: Run on PR + manual trigger
  - Pros: Flexible, faster default path
  - Cons: Manual step might be forgotten

**Your Recommendation**: _______________

**Rationale**: _______________

---

### 6. Scope Definition

**Question**: What should be integration tested vs left to manual testing?

**Must Have** (everyone agrees):
- [ ] Full auth lifecycle
- [ ] Token blacklist verification
- [ ] Multi-user isolation

**Nice to Have** (if time permits):
- [ ] Token expiration
- [ ] Concurrent operations
- [ ] Password change flows
- [ ] FK cascade behavior

**Out of Scope** (manual only):
- [ ] Browser-based UI testing
- [ ] Performance benchmarking
- [ ] Load testing
- [ ] Security penetration testing

**Your Recommendations**:
- Must have: _______________
- Nice to have: _______________
- Out of scope: _______________

---

## Gameplan Request

### What We Need from Chief Architect

**Gameplan Document** (similar to UUID migration gameplan):

1. **Architecture Decision Record** (or equivalent)
   - Testing infrastructure architecture
   - Database isolation strategy
   - Fixture design pattern
   - Performance targets
   - CI/CD integration strategy

2. **Phased Implementation Plan**
   - Phase 1: Infrastructure setup
   - Phase 2: Critical tests (5 tests)
   - Phase 3: Additional tests (if time)
   - Phase 4: Documentation

3. **Test Scenarios Specification**
   - Which 5-10 tests to implement
   - What each test should verify
   - Expected behavior for each
   - Pass/fail criteria

4. **Success Criteria**
   - What makes this complete?
   - How do we measure success?
   - What's the acceptance criteria?

### Format

**Deliverable**: `gameplan-292-auth-integration-tests.md`

**Similar to**: UUID migration gameplan (which worked excellently)

**Level of Detail**: Enough for Code Agent to implement without ambiguity

**Timeline**: Tomorrow morning preferred (so agents can work tomorrow)

---

## Benefits of Gameplan Approach

**For Chief Architect**:
- Opportunity to set testing architecture standards
- Document testing strategy decisions
- Create reusable patterns for other features

**For Lead Dev**:
- Clear architectural decisions to follow
- Less guesswork on trade-offs
- Better prompt to give Code Agent

**For Code Agent**:
- Unambiguous implementation plan
- Clear success criteria
- Architectural context for decisions

**For PM**:
- Confidence in testing strategy
- Systematic approach
- Reusable pattern for future

**For Project**:
- Testing architecture documented
- Decisions captured in ADR
- Scalable approach for other areas

---

## Alternative: Lead Dev Makes Decisions

If Chief Architect is unavailable or prefers Lead Dev to proceed:

**Lead Dev can create prompt** making these assumptions:
- Transaction rollback isolation (Option 1A)
- Real `get_db_session()` with cleanup (Option 2C)
- Light integration tests (Option 3A - 5 tests)
- 60 second budget (Option 4B)
- Run on PR (Option 5B)
- Focus on critical flows only

**Trade-off**: Faster to implement, but may not match Chief Architect's vision

---

## Recommendation

**Preferred**: Chief Architect gameplan
- Testing infrastructure is architectural
- Benefits from systematic decisions
- Creates reusable pattern

**Acceptable**: Lead Dev prompt with assumptions
- Can proceed immediately
- May need refactoring later

**Your call**: What works best for tomorrow's schedule?

---

## Timeline

**If Chief Architect creates gameplan**:
- Tonight/tomorrow morning: Chief creates gameplan (1 hour)
- Tomorrow: Code Agent implements (3 hours)
- Total: 4 hours

**If Lead Dev creates prompt**:
- Tonight: Lead Dev creates prompt (2 hours)
- Tomorrow: Code Agent implements (3 hours)
- Later: Potential refactor if needed (1-2 hours)
- Total: 5-7 hours

**Verdict**: Chief Architect gameplan is more efficient long-term

---

## Summary

**Issue**: #292 - Add integration tests for auth (reduce mocking)
**Why Gameplan**: Architectural decisions about testing infrastructure
**Key Questions**: Isolation strategy, fixture design, test scope, performance, CI/CD
**Request**: Gameplan document from Chief Architect
**Timeline**: Tomorrow morning (so agents can work tomorrow)
**Alternative**: Lead Dev can proceed with reasonable assumptions

**What Chief Architect brings**: Testing architecture expertise, systematic decisions, documented strategy, reusable patterns

---

**Awaiting Chief Architect's gameplan or direction to proceed with Lead Dev assumptions.**

---

_Requested: November 11, 2025, 9:45 PM_
_Priority: P3 (but needed for tomorrow's work)_
_Issue: #292 - CORE-ALPHA-AUTH-INTEGRATION-TESTS_
