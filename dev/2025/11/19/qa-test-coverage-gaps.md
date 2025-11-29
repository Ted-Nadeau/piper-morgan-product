# Test Coverage Gaps Analysis

**For**: Lead QA Engineer
**From**: Research Code (Claude Code)
**Date**: 2025-11-19 17:00 PM PT
**Context**: Pre-MVP testing preparation, technical debt from architecture review

---

## Executive Summary

During Ted Nadeau's architecture review, we discovered **10 areas of technical debt** that block comprehensive testing. This document analyzes:
- **What cannot be tested** until issues are fixed
- **What test types are needed** (unit, integration, E2E, security, performance)
- **Test data requirements** for realistic scenarios
- **Automation gaps** in CI/CD pipeline
- **Recommended testing strategy** for MVP

**Bottom line**: **Fix critical blockers first** (#323 RBAC, #324 Encryption), then start E2E testing while fixing others in parallel.

---

## 1. Test Coverage Gaps by Issue

### Issue #319: Windows Compatibility

**What Can't Be Tested**:
- ❌ Windows E2E testing (git clone fails)
- ❌ Cross-platform CI/CD (Windows runners blocked)
- ❌ Windows developer onboarding
- ❌ Windows-specific bugs (path separators, line endings)

**Required Test Coverage**:
- **Platform compatibility tests**: Clone, install, run on Windows/macOS/Linux
- **File path tests**: Verify no illegal characters in filenames
- **Line ending tests**: CRLF vs LF handling

**Blocked Scenarios**:
- QA engineer on Windows cannot set up environment
- CI/CD cannot run Windows test matrix
- Production deployment to Windows servers (if ever needed)

**Priority**: Medium (workaround: Use WSL or macOS for testing)

---

### Issue #320: Missing Database Indexes

**What Can't Be Tested**:
- ❌ Performance testing at scale (>1K records)
- ❌ Load testing (concurrent users)
- ❌ Query performance benchmarks
- ❌ Scalability testing

**Required Test Coverage**:
- **Performance tests**: Query time < 100ms for common operations
- **Load tests**: 10 concurrent users, 100 requests/sec
- **Scalability tests**: 10K, 100K, 1M records

**Blocked Scenarios**:
```python
# Test: Conversation history performance
def test_conversation_history_performance():
    # Seed 10,000 conversations for user
    seed_conversations(user_id, count=10000)

    # Query should be <100ms (currently ~200ms without index)
    start_time = time.time()
    conversations = await get_user_conversations(user_id, limit=50)
    duration = time.time() - start_time

    assert duration < 0.1, f"Query took {duration}s (expected <0.1s)"
    # ❌ FAILS without index on (user_id, created_at)
```

**Performance baselines** (cannot establish until indexes added):
- Conversation history: Target <50ms (currently ~200ms)
- Pattern learning queries: Target <100ms (currently unknown)
- File browsing: Target <50ms (currently unknown)

**Priority**: Medium (Performance testing can wait until MVP+1)

---

### Issue #321: Audit Field Standardization

**What Can't Be Tested**:
- ❌ Audit trail compliance (SOC2, GDPR)
- ❌ Change tracking ("who modified what and when")
- ❌ Data lineage testing
- ❌ Soft delete scenarios (no deleted_at field yet)

**Required Test Coverage**:
- **Audit tests**: Verify all changes captured (created_by, updated_by)
- **Compliance tests**: GDPR right to audit, SOC2 change tracking
- **Data integrity tests**: Ensure audit fields populated correctly

**Blocked Scenarios**:
```python
# Test: Audit trail for list modification
def test_list_modification_audit_trail():
    # User A creates list
    list = await create_list(user_a, name="Test List")
    assert list.created_by == user_a.id  # ❌ Field doesn't exist

    # User B modifies list
    await update_list(list.id, user_b, name="Modified List")
    assert list.updated_by == user_b.id  # ❌ Field doesn't exist
    assert list.updated_at > list.created_at  # ✅ This exists

    # Audit log should show both changes
    audit_log = await get_audit_log(resource_id=list.id)
    assert len(audit_log) == 2  # ❌ Can't fully test without audit fields
```

**Compliance gaps**:
- Cannot prove "who deleted this record" (no deleted_by)
- Cannot audit "who created vs who last modified"
- Cannot track change history for compliance

**Priority**: High (Blocks compliance testing)

---

### Issue #322: ServiceContainer Singleton

**What Can't Be Tested**:
- ❌ Multi-worker deployment (horizontal scaling)
- ❌ Load balancer scenarios
- ❌ Concurrent request handling (multiple instances)
- ❌ Kubernetes pod autoscaling

**Required Test Coverage**:
- **Deployment tests**: Multiple uvicorn workers
- **Concurrency tests**: Shared state isolation
- **Load balancer tests**: Round-robin distribution

**Blocked Scenarios**:
```bash
# Test: Run with multiple workers
uvicorn web.app:app --workers 4

# ❌ FAILS: ServiceContainer singleton shared across workers
# Results in shared state, race conditions
```

**Current limitation**: Can only test single-worker deployment

**Priority**: Medium (Single-worker sufficient for alpha, scale later)

---

### Issue #323: No RBAC Implementation ⚠️ CRITICAL

**What Can't Be Tested**:
- ❌ **Security testing** (unauthorized access scenarios)
- ❌ **Multi-user testing** (user A can't access user B's data)
- ❌ **Admin vs user permissions**
- ❌ **Resource ownership** (conversation belongs to user)
- ❌ **Role-based access control**

**Required Test Coverage**:
- **Authorization tests**: User can only access own resources
- **Privilege escalation tests**: Regular user cannot access admin functions
- **Resource ownership tests**: Cross-user data access blocked

**Blocked Scenarios**:
```python
# Test: User cannot access other user's conversations
async def test_conversation_access_control():
    # User A creates conversation
    conversation_a = await create_conversation(user_a)

    # User B tries to access User A's conversation
    with pytest.raises(Forbidden):
        await get_conversation(conversation_a.id, user=user_b)
        # ❌ CURRENTLY NO ERROR - any auth'd user can access any resource!
```

**Security gaps** (CANNOT TEST):
1. User enumeration (can user B list all users?)
2. Horizontal privilege escalation (user B accesses user A's data)
3. Vertical privilege escalation (user promotes self to admin)
4. API endpoint authorization (all endpoints return data regardless of owner)

**Current state**: **ANY authenticated user can access ANY resource**

**Priority**: **CRITICAL** - Blocks ALL security testing

---

### Issue #324: No Encryption at Rest ⚠️ CRITICAL

**What Can't Be Tested**:
- ❌ **Compliance testing** (SOC2, GDPR, HIPAA)
- ❌ **Data protection testing**
- ❌ **Encryption key rotation**
- ❌ **Security audit** (data at rest security)

**Required Test Coverage**:
- **Encryption tests**: Verify sensitive data encrypted in DB
- **Decryption tests**: Ensure encrypted data readable by application
- **Key rotation tests**: Verify old data readable after key rotation
- **Performance tests**: Encryption overhead < 5%

**Blocked Scenarios**:
```python
# Test: Conversation content encrypted at rest
async def test_conversation_encryption_at_rest():
    conversation = await create_conversation(
        user_id=user.id,
        content="Sensitive strategy discussion"
    )

    # Check database directly - content should be encrypted
    raw_db_content = await db.execute(
        "SELECT content FROM conversations WHERE id = $1",
        conversation.id
    )

    # ❌ CURRENTLY: Content stored as plaintext
    assert raw_db_content != "Sensitive strategy discussion"
    assert is_encrypted(raw_db_content)  # Should be encrypted blob
```

**Compliance gaps** (CANNOT CERTIFY):
- SOC2: Encryption at rest requirement
- GDPR: Data protection requirement
- HIPAA: PHI encryption (if handling health data)

**Current state**: **Sensitive data (conversations, files, patterns) stored UNENCRYPTED**

**Priority**: **CRITICAL** - Blocks compliance certification

---

### Issue #325: No OS Detection in Scripts

**What Can't Be Tested**:
- ❌ Automated testing on Windows (scripts fail)
- ❌ Cross-platform CI/CD matrix
- ❌ Developer onboarding (Windows devs can't run scripts)

**Required Test Coverage**:
- **Platform tests**: Scripts run on macOS, Linux, Git Bash
- **Graceful degradation tests**: Scripts warn on unsupported operations

**Blocked Scenarios**:
- Automated test runs on Windows CI/CD runners
- QA engineer on Windows cannot run `./scripts/run_tests.sh`

**Priority**: Medium (Manual workarounds available)

---

### Issue #336: Soft Delete Strategy

**What Can't Be Tested**:
- ❌ Soft delete / restore workflows
- ❌ Data recovery scenarios
- ❌ Permanent deletion after retention period
- ❌ GDPR "right to be forgotten" compliance

**Required Test Coverage**:
- **Soft delete tests**: Record marked deleted, not actually removed
- **Restore tests**: Soft-deleted record can be restored
- **Query filtering tests**: Deleted records hidden by default
- **Permanent deletion tests**: Cleanup job after 90 days

**Blocked Scenarios**:
```python
# Test: Soft delete and restore
async def test_soft_delete_restore():
    list = await create_list(user, name="Test List")

    # Soft delete
    await delete_list(list.id, user, permanent=False)
    assert list.deleted_at is not None  # ❌ Field doesn't exist
    assert list.deleted_by == user.id   # ❌ Field doesn't exist

    # Verify hidden from normal queries
    lists = await get_user_lists(user)
    assert list.id not in [l.id for l in lists]  # ❌ Still returns deleted

    # Restore
    await restore_list(list.id, user)
    assert list.deleted_at is None  # ❌ Restore method doesn't exist

    # Verify visible again
    lists = await get_user_lists(user)
    assert list.id in [l.id for l in lists]
```

**Priority**: Medium (Nice to have, not MVP blocker)

---

### Issue #338: Migration Rollback Testing

**What Can't Be Tested**:
- ❌ Migration rollback success
- ❌ Data integrity after rollback
- ❌ Migration performance on large datasets
- ❌ Partial migration failure recovery

**Required Test Coverage**:
- **Rollback tests**: Migration upgrade → downgrade restores original state
- **Data validation tests**: No data loss/corruption during migration
- **Performance tests**: Migration completes in <1 minute on 10K records

**Blocked Scenarios**:
- Cannot confidently deploy database migrations to production
- No automated rollback testing in CI/CD
- Unknown migration duration on production data volumes

**Priority**: High (De-risks database changes)

---

## 2. Test Type Coverage Matrix

| Test Type | Current Coverage | Gaps | Blocking Issues |
|-----------|------------------|------|-----------------|
| **Unit Tests** | Partial | Missing authorization, encryption, soft delete logic | #323, #324, #336 |
| **Integration Tests** | Limited | Missing multi-user scenarios, compliance workflows | #321, #323, #324 |
| **E2E Tests** | None | Can't test end-to-end user workflows (no RBAC) | #323 |
| **Security Tests** | None | Can't test authorization, encryption, audit trails | #323, #324, #321 |
| **Performance Tests** | None | Can't benchmark (no indexes, no scale data) | #320 |
| **Compliance Tests** | None | Can't verify SOC2/GDPR requirements | #321, #324 |
| **Platform Tests** | macOS only | No Windows/Linux automated testing | #319, #325 |
| **Load Tests** | None | Can't test concurrent users (singleton) | #322 |
| **Migration Tests** | Manual only | No automated rollback testing | #338 |

---

## 3. Test Data Requirements

### Current Limitations

**Single-user testing only**: Without RBAC (#323), can't create realistic multi-user scenarios.

**Test data needs** (BLOCKED until RBAC):
- 10+ test users with different roles (admin, user, guest)
- 100+ conversations across multiple users
- User A cannot see User B's data scenarios
- Cross-user collaboration scenarios (shared lists)

### Required Test Data Sets

**Small** (Alpha testing):
- 5 users
- 50 conversations
- 200 patterns
- 100 uploaded files

**Medium** (MVP testing):
- 20 users
- 1,000 conversations
- 5,000 patterns
- 500 uploaded files

**Large** (Performance testing):
- 100 users
- 10,000 conversations
- 50,000 patterns
- 5,000 uploaded files

**XL** (Scalability testing):
- 1,000 users
- 100,000 conversations
- 500,000 patterns
- 50,000 uploaded files

**Cannot create realistic test data until**:
- RBAC implemented (#323) - for multi-user scenarios
- Soft delete (#336) - for deletion/restore scenarios
- Audit fields (#321) - for change tracking scenarios

---

## 4. Automation Gaps in CI/CD

### Current State

**Existing automation** (from `.pre-commit-config.yaml`):
- ✅ Smoke tests (<1s basic functionality)
- ✅ Code quality (isort, flake8, black)
- ✅ GitHub architecture enforcement
- ✅ Documentation checks

**Missing automation**:
- ❌ Integration tests in CI/CD
- ❌ Security tests (authorization, encryption)
- ❌ Performance benchmarks
- ❌ Migration rollback tests (Issue #338)
- ❌ Multi-platform testing (Windows, Linux)
- ❌ Load testing

### Recommended CI/CD Pipeline

```yaml
# .github/workflows/test-suite.yml
name: Comprehensive Test Suite

on: [pull_request, push]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run unit tests
        run: pytest tests/unit/ -v --cov=services
      - name: Coverage report
        run: coverage report --fail-under=80

  integration-tests:  # ❌ BLOCKED by #323, #324
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
    steps:
      - name: Run integration tests
        run: pytest tests/integration/ -v

  security-tests:  # ❌ BLOCKED by #323, #324
    runs-on: ubuntu-latest
    steps:
      - name: Run security tests
        run: pytest tests/security/ -v
      - name: OWASP dependency check
        run: safety check

  performance-tests:  # ❌ BLOCKED by #320
    runs-on: ubuntu-latest
    steps:
      - name: Seed database (10K records)
        run: python scripts/seed_large_dataset.py
      - name: Run performance benchmarks
        run: pytest tests/performance/ -v

  migration-tests:  # ❌ BLOCKED by #338
    runs-on: ubuntu-latest
    steps:
      - name: Test migration rollback
        run: pytest tests/migrations/ -v

  platform-tests:  # ❌ BLOCKED by #319, #325
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - name: Test on ${{ matrix.os }}
        run: pytest tests/platform/ -v
```

**All blocked jobs** can be enabled after fixing critical issues.

---

## 5. Recommended Testing Strategy

### Phase 1: Fix Critical Blockers (Week 1-2)

**Must fix BEFORE E2E testing**:
1. **#323: RBAC** (20-24 hours) - **CRITICAL**
   - Enables: Security testing, multi-user scenarios
   - Unblocks: 80% of integration/E2E tests

2. **#324: Encryption at Rest** (24-30 hours) - **CRITICAL**
   - Enables: Compliance testing, security audits
   - Unblocks: SOC2/GDPR certification path

**Rationale**: These block MOST testing scenarios.

### Phase 2: Start E2E Testing (Week 3-4)

**Can test with basic RBAC + Encryption**:
- ✅ User registration & login
- ✅ Create/read/update/delete conversations (own only)
- ✅ Upload files
- ✅ Pattern learning
- ✅ Basic workflows

**Still cannot test** (but OK for MVP):
- Performance at scale (no indexes yet)
- Soft delete/restore (not implemented)
- Multi-worker deployment (singleton)

### Phase 3: Fix Performance & Data Integrity (Week 5-6)

**Fix in parallel with E2E testing**:
1. **#320: Database Indexes** (4-6 hours)
   - Enables: Performance testing

2. **#321: Audit Fields** (12-16 hours)
   - Enables: Compliance testing

3. **#338: Migration Rollback Testing** (30-40 hours)
   - Enables: Safer deployments

### Phase 4: Platform & Scalability (Week 7-8)

**Nice-to-have for MVP**:
1. **#319: Windows Compatibility** (2-3 hours)
2. **#325: OS Detection** (6-8 hours)
3. **#322: ServiceContainer Singleton** (16-20 hours) - if scaling needed
4. **#336: Soft Delete** (34-48 hours) - if data recovery critical

---

## 6. Test Coverage Goals

### MVP Targets

**Unit Test Coverage**: 80% (currently unknown)
- Focus on critical paths: authentication, authorization, data access

**Integration Test Coverage**: 60%
- Multi-user scenarios
- API endpoint authorization
- Database transactions

**E2E Test Coverage**: 40%
- Critical user workflows (register, login, create conversation, upload file)
- Admin workflows (if RBAC has admin role)

**Security Test Coverage**: 100% of critical scenarios
- Unauthorized access blocked
- Encryption verified
- Audit trail complete

**Performance Test Coverage**: Key operations benchmarked
- Conversation history < 100ms
- Pattern queries < 100ms
- File upload < 5s

### Post-MVP Targets

**Unit Test Coverage**: 90%
**Integration Test Coverage**: 80%
**E2E Test Coverage**: 70%
**Load Test Coverage**: 10 concurrent users, 100 req/sec
**Platform Test Coverage**: macOS, Linux, Windows (Git Bash)

---

## 7. Recommended Test Tools

**Unit Testing**:
- ✅ pytest (already using)
- ✅ pytest-cov (coverage reporting)
- ✅ pytest-asyncio (async test support)

**Integration Testing**:
- ✅ pytest + PostgreSQL fixtures
- ✅ TestClient (FastAPI test client)
- Consider: testcontainers (isolated test databases)

**Security Testing**:
- **OWASP ZAP** (security scanning)
- **safety** (dependency vulnerability checking)
- **bandit** (Python security linter)

**Performance Testing**:
- **locust** (load testing)
- **pytest-benchmark** (microbenchmarks)
- **pgbench** (PostgreSQL performance)

**E2E Testing**:
- **Playwright** or **Selenium** (UI testing)
- **API testing**: requests library + pytest

**CI/CD**:
- ✅ GitHub Actions (already using)
- **Codecov** (coverage reporting)
- **SonarQube** (code quality)

---

## 8. Risk Assessment

### High Risk (Will Cause Test Failures)

**#323 (RBAC)**:
- **Risk**: ANY authenticated user can access ANY resource
- **Impact**: Security tests will fail, multi-user scenarios broken
- **Mitigation**: Fix IMMEDIATELY

**#324 (Encryption)**:
- **Risk**: Sensitive data stored unencrypted
- **Impact**: Compliance tests will fail, security audit fails
- **Mitigation**: Fix IMMEDIATELY

### Medium Risk (May Cause Issues)

**#321 (Audit Fields)**:
- **Risk**: Cannot track "who changed what"
- **Impact**: Compliance tests incomplete
- **Mitigation**: Fix in Phase 2 (parallel with E2E)

**#320 (Indexes)**:
- **Risk**: Performance tests will fail at scale
- **Impact**: Can't certify performance SLAs
- **Mitigation**: Fix before performance testing (Phase 3)

### Low Risk (Workarounds Available)

**#319 (Windows)**:
- **Risk**: QA can't test on Windows
- **Mitigation**: Use WSL or macOS temporarily

**#325 (OS Detection)**:
- **Risk**: Scripts fail on Windows
- **Mitigation**: Manual testing possible

---

## 9. Success Metrics

**Phase 1 (Fix Blockers)**:
- ✅ RBAC tests passing (100% authorization scenarios)
- ✅ Encryption tests passing (all sensitive data encrypted)
- ✅ Security scan clean (no critical vulnerabilities)

**Phase 2 (E2E Testing)**:
- ✅ Critical user workflows tested (5+ scenarios)
- ✅ Multi-user scenarios tested (user A vs user B)
- ✅ Regression test suite established (30+ tests)

**Phase 3 (Performance & Data)**:
- ✅ Performance baselines established
- ✅ Audit trail complete (all changes tracked)
- ✅ Migration rollback tested successfully

**Phase 4 (Platform & Scale)**:
- ✅ Windows testing automated
- ✅ Load tests passing (10 concurrent users)
- ✅ Soft delete/restore workflows tested

---

## 10. Summary & Next Actions

**Critical Path** (DO FIRST):
1. Fix #323 (RBAC) - **BLOCKS 80% of testing**
2. Fix #324 (Encryption) - **BLOCKS compliance**
3. Start E2E testing with multi-user scenarios

**Parallel Work** (WHILE E2E testing):
1. Fix #320 (Indexes) - Enable performance testing
2. Fix #321 (Audit Fields) - Enable compliance testing
3. Set up #338 (Migration Testing) - De-risk deployments

**Defer to MVP+1**:
1. #336 (Soft Delete) - Nice to have
2. #322 (Singleton) - Not blocking alpha
3. #319/#325 (Windows) - Workarounds available

**Test Automation Priority**:
1. Security tests (authorization, encryption) - **Week 1-2**
2. Integration tests (multi-user scenarios) - **Week 3-4**
3. Performance tests (query benchmarks) - **Week 5-6**
4. Platform tests (Windows/Linux) - **Week 7-8**

---

**Prepared by**: Research Code (Claude Code)
**Date**: 2025-11-19 17:00 PM PT
**Related Reports**: `qa-pre-mvp-technical-debt-report.md` (detailed issue breakdown)
**GitHub Issues**: #319-#328, #329-#331, #336, #338-#340
