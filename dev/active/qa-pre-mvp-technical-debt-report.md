# QA Pre-MVP Technical Debt Report

**Prepared for**: Lead QA Engineer
**Prepared by**: Research Code (Claude Code)
**Date**: 2025-11-19
**Purpose**: Document known issues requiring fixes before E2E testing
**Context**: Ted Nadeau architecture review uncovered technical debt

---

## Executive Summary

During architectural review for Ted Nadeau (computer scientist advisor), discovered **10 areas of technical debt** that should be addressed before comprehensive E2E testing. These range from **critical security gaps** to **post-MVP architectural improvements**.

**Critical for MVP** (7 issues): #319, #320, #321, #322, #323, #324, #325
**Post-MVP** (3 issues): #326, #327, #328

---

## Critical Issues (Must Fix Before MVP)

### 1. Windows Compatibility Bug (#319)
**Priority**: High
**Component**: Platform Compatibility
**Status**: Open

**Problem**: Filename contains illegal character (colon) on Windows, breaking `git clone`.

**File**: `archive/piper-morgan-0.1.1/docs/claude docs 5:30/conversational_refactor.md`

**Impact on Testing**:
- QA engineers on Windows cannot clone repository
- Blocks Windows-based E2E testing
- Violates cross-platform support goal

**Fix Required**:
1. Rename file (remove colon)
2. Add pre-commit hook to prevent future illegal characters
3. Test `git clone` on Windows

**Estimated Effort**: 2-3 hours
**Blocking**: Windows E2E test setup

---

### 2. Missing Database Indexes (#320)
**Priority**: Medium
**Component**: Database Performance
**Status**: Open

**Problem**: No composite indexes for common query patterns. Performance degrades as data scales.

**Missing Indexes**:
1. `conversations(user_id, created_at)` - Conversation history
2. `conversation_turns(conversation_id, turn_number)` - Turn retrieval
3. `uploaded_files(user_id, upload_date)` - File browsing
4. `patterns(user_id, category)` - Pattern learning

**Impact on Testing**:
- Performance tests will fail at scale (>1K records)
- Current: ~200ms for 1K records (table scan)
- With indexes: ~20ms (index lookup)
- At 100K records: 20+ second queries without indexes

**Fix Required**:
1. Create Alembic migration adding 4 composite indexes
2. Benchmark before/after performance
3. Update query patterns if needed

**Estimated Effort**: 4-6 hours
**Blocking**: Performance/load testing

---

### 3. Audit Field Standardization (#321)
**Priority**: High
**Component**: Data Integrity
**Status**: Open

**Problem**: Inconsistent audit trail across domain models.

**Current State**:
- Some models: only `created_at`
- Others: `created_at` + `updated_at`
- None: `created_by`, `updated_by`, `deleted_at` (soft delete)

**Impact on Testing**:
- Cannot test audit trail compliance
- Cannot test "who changed what" scenarios
- Cannot test soft delete functionality
- Blocks SOC2/GDPR compliance testing

**Fix Required**:
1. Create `AuditedModel` base class
2. Migration to add missing fields to all 36 domain models
3. Backfill existing data with system user ID
4. Update repository pattern for soft delete

**Estimated Effort**: 12-16 hours
**Blocking**: Compliance testing, audit trail validation

---

### 4. ServiceContainer Singleton (#322)
**Priority**: High
**Component**: Architecture/Scalability
**Status**: Open

**Problem**: Singleton pattern blocks horizontal scaling (multiple instances).

**Current Implementation**: `services/container/service_container.py` uses `__new__` singleton

**Impact on Testing**:
- Cannot test multi-worker deployment
- Cannot test load balancer scenarios
- Cannot test horizontal scaling
- Blocks cloud-native deployment testing

**Fix Required**:
1. Remove singleton pattern
2. Refactor to application-scoped container (FastAPI lifespan)
3. Test with multiple uvicorn workers
4. Validate no shared state between instances

**Estimated Effort**: 16-20 hours
**Blocking**: Load testing, deployment validation

---

### 5. No RBAC Implementation (#323)
**Priority**: Critical
**Component**: Security/Authorization
**Status**: Open

**Problem**: Only JWT authentication exists. No role-based access control.

**Security Gap**: Any authenticated user can access any resource.

**Impact on Testing**:
- Cannot test authorization scenarios
- Cannot test admin vs user permissions
- Cannot test resource ownership
- Blocks multi-user testing scenarios

**Fix Required**:
1. Create Role and Permission models
2. Migration to add RBAC tables
3. Authorization middleware/decorators
4. Ownership checks for all resources
5. Tests for permission enforcement

**Estimated Effort**: 20-24 hours
**Blocking**: Security testing, multi-user scenarios

---

### 6. No Encryption at Rest (#324)
**Priority**: High
**Component**: Security/Compliance
**Status**: Open

**Problem**: Sensitive data stored unencrypted in PostgreSQL.

**Unencrypted**:
- Conversation content
- Uploaded file content
- Pattern data
- User PII (email, metadata)

**Impact on Testing**:
- Cannot test SOC2 compliance
- Cannot test GDPR data protection
- Cannot test encryption key rotation
- Security audit will fail

**Fix Required**:
1. Implement field-level encryption service
2. Encrypt sensitive fields (conversation_content, file_content)
3. Key management strategy (env var for alpha, AWS KMS later)
4. Migration to encrypt existing data
5. Benchmark performance (<5% overhead target)

**Estimated Effort**: 24-30 hours
**Blocking**: Compliance testing, security audits

---

### 7. OS Detection in Scripts (#325)
**Priority**: Medium
**Component**: Developer Experience
**Status**: Open

**Problem**: Shell scripts assume Unix/macOS, break on Windows.

**Affected Scripts**:
- `scripts/start-piper.sh`
- `scripts/stop-piper.sh`
- `scripts/run_tests.sh`
- Pre-commit hooks

**Impact on Testing**:
- Windows QA engineers cannot run scripts
- Cannot automate Windows E2E tests
- Manual workarounds required

**Fix Required**:
1. Create `scripts/lib/os-detect.sh` library
2. Update all scripts with OS detection
3. Add Windows-specific logic (where feasible)
4. Warn for unsupported operations
5. Test on macOS, Linux, Git Bash

**Estimated Effort**: 6-8 hours
**Blocking**: Windows automation

---

## Post-MVP Issues (Track but Not Blocking)

### 8. Multi-Organization Support (#326)
**Priority**: Medium
**Component**: Architecture
**Status**: Open (Post-MVP)

**Problem**: Single-tenant only, cannot support multiple organizations (B2B SaaS).

**Impact**: Does not block MVP testing, but needed for B2B scenarios.

**Estimated Effort**: 40-60 hours (design + implementation)

---

### 9. AI Agent GitHub Accounts (#327)
**Priority**: Low
**Component**: Process
**Status**: Open (Post-MVP)

**Problem**: AI agents commit using PM's account, hard to distinguish human vs AI.

**Impact**: Process improvement, not blocking testing.

**Estimated Effort**: 4-6 hours (account setup + docs)

---

### 10. Centralized Observability (#328)
**Priority**: Medium
**Component**: Infrastructure
**Status**: Open (Post-MVP)

**Problem**: No centralized logging, metrics, or monitoring.

**Impact**: Makes debugging hard, but not blocking MVP functional testing.

**Estimated Effort**: 30-40 hours (logging + metrics + dashboards)

---

## Testing Recommendations

### Phase 1: Fix Blockers (Before E2E Testing Begins)
**Must complete**: #319, #323 (RBAC), #324 (Encryption)

**Why**: Security and platform compatibility are foundational.

**Timeline**: ~50 hours (2 weeks for one developer)

---

### Phase 2: Performance & Scale (During E2E Testing)
**Should complete**: #320 (Indexes), #321 (Audit fields), #322 (Singleton)

**Why**: Performance issues will surface during E2E, easier to fix proactively.

**Timeline**: ~35 hours (1.5 weeks)

---

### Phase 3: Developer Experience (Parallel)
**Nice to have**: #325 (OS detection)

**Why**: Improves QA team productivity, can run in parallel.

**Timeline**: ~8 hours (1 day)

---

## Test Coverage Gaps

### Cannot Test Until Fixed

**Security scenarios** (#323, #324):
- User cannot access other user's conversations ❌
- Admin can access all resources ❌
- Encrypted data at rest ❌
- Audit trail for changes ❌

**Performance scenarios** (#320, #322):
- 10K conversation load test ❌
- Multi-worker deployment ❌
- Concurrent user testing ❌

**Platform compatibility** (#319, #325):
- Windows E2E tests ❌
- Cross-platform automation ❌

---

## Risk Assessment

### High Risk (Likely to cause test failures)
- **#323 (RBAC)**: Security tests will fail, multi-user scenarios broken
- **#324 (Encryption)**: Compliance tests will fail
- **#320 (Indexes)**: Performance tests will fail at scale

### Medium Risk (May cause issues)
- **#321 (Audit fields)**: Data integrity tests incomplete
- **#322 (Singleton)**: Deployment tests will fail

### Low Risk (Workarounds available)
- **#319 (Windows)**: QA can use WSL temporarily
- **#325 (OS detection)**: Manual testing possible

---

## Recommended Fix Order

1. **#323 (RBAC)** - 20-24 hours - Blocks most security testing
2. **#324 (Encryption)** - 24-30 hours - Blocks compliance testing
3. **#320 (Indexes)** - 4-6 hours - Quick win, prevents performance issues
4. **#319 (Windows)** - 2-3 hours - Quick win, enables Windows testing
5. **#321 (Audit fields)** - 12-16 hours - Data integrity
6. **#322 (Singleton)** - 16-20 hours - Deployment testing
7. **#325 (OS detection)** - 6-8 hours - Developer experience

**Total**: ~85-107 hours (~2.5-3 weeks for one developer)

---

## Testing Strategy Recommendation

### Option A: Waterfall (Fix Everything First)
- **Pros**: Clean slate, no known blockers
- **Cons**: 3-week delay before E2E testing starts
- **Recommendation**: Use for critical issues only (#323, #324)

### Option B: Parallel (Fix + Test)
- **Pros**: Find more issues sooner, faster feedback
- **Cons**: Some tests will fail initially
- **Recommendation**: Start E2E after Phase 1 fixes (#323, #324, #319)

### Option C: Risk-Based (Prioritize by Impact)
- **Pros**: Focus on highest-value testing first
- **Cons**: Lower-priority bugs may surface late
- **Recommendation**: **BEST APPROACH** - Fix critical issues (#323, #324), start testing, fix others as blockers discovered

---

## Questions for QA Lead

1. **Timeline**: When do you need to start E2E testing?
2. **Platform**: Will QA team test on Windows, or macOS/Linux only?
3. **Scope**: Which scenarios are MVP-critical vs nice-to-have?
4. **Resources**: How many developers available to fix these issues?
5. **Risk tolerance**: Okay with some test failures initially (parallel approach)?

---

## References

- **Research session log**: `dev/active/2025-11-19-1259-research-code-log.md`
- **Ted Nadeau reply draft**: `dev/active/ted-nadeau-reply-draft.md`
- **GitHub issues**: #319-#328
- **Source code**:
  - `services/container/service_container.py` (singleton)
  - `services/domain/models.py` (36 domain models)
  - ADR-012: Protocol-Ready JWT Authentication

---

## Appendix: Issue Quick Reference

| # | Title | Priority | Effort | Blocks Testing |
|---|-------|----------|--------|----------------|
| #319 | Windows compatibility | High | 2-3h | Windows E2E |
| #320 | Database indexes | Medium | 4-6h | Performance |
| #321 | Audit fields | High | 12-16h | Compliance |
| #322 | Singleton pattern | High | 16-20h | Scaling |
| #323 | RBAC | Critical | 20-24h | Security |
| #324 | Encryption at rest | High | 24-30h | Compliance |
| #325 | OS detection | Medium | 6-8h | Windows automation |
| #326 | Multi-org | Medium | 40-60h | No (Post-MVP) |
| #327 | AI accounts | Low | 4-6h | No (Post-MVP) |
| #328 | Observability | Medium | 30-40h | No (Post-MVP) |

**Total MVP effort**: 85-107 hours
**Total Post-MVP effort**: 74-106 hours
