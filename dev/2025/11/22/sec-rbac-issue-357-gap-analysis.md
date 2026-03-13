# SEC-RBAC Issue #357: Gap Analysis

**Date**: November 22, 2025, 11:50 AM
**Purpose**: Compare what we've built vs what Issue #357 requires

---

## Issue #357 Requirements

### Core Implementation (from acceptance criteria)
- [ ] Create Role model and migration
- [ ] Create Permission model and migration
- [ ] Create RolePermission junction table
- [ ] Create UserRole junction table
- [ ] Add `owner_id` to all resource tables
- [ ] Backfill existing data with owner_id

### Authorization Enforcement
- [ ] Create `@require_permission` decorator
- [ ] Create `@require_ownership` decorator
- [ ] Apply to ALL API endpoints
- [ ] Apply to ALL service methods
- [ ] No unprotected endpoints remain

### Role Definitions
- [ ] **Admin**: All permissions on all resources
- [ ] **User**: CRUD own resources only
- [ ] **Viewer**: Read-only access to shared resources

### Testing
- [ ] User cannot access other user's conversations
- [ ] User cannot modify other user's lists
- [ ] Admin can access all resources
- [ ] 100% test coverage on authorization
- [ ] Security scan passes (no auth bypasses)

---

## What We've Actually Built (Phases 1-2)

### ✅ Completed

**Database Schema**:
- ✅ Added `owner_id` to 9 resource tables (Phase 1.1)
- ✅ Backfilled existing data with xian's account (Phase 1.1)
- ✅ Added `shared_with` JSONB columns to lists/todos (existing)

**Service Layer**:
- ✅ 9 services secured with owner_id validation (Phase 1.2)
- ✅ 67+ methods enforce ownership checks (Phase 1.2)

**API Endpoints**:
- ✅ 26 endpoints protected with owner_id checks (Phase 1.3)
- ✅ 6 sharing endpoints for lists (Phase 1.4)
- ✅ 6 role-based endpoints for lists/todos (Phase 2)

**Role-Based Sharing**:
- ✅ ShareRole enum (VIEWER, EDITOR, ADMIN) (Phase 2)
- ✅ SharePermission dataclass (Phase 2)
- ✅ Permission matrix implemented (Phase 2)
- ✅ Read-only sharing (Phase 1.4)
- ✅ Role-based modify/share permissions (Phase 2)

**Testing**:
- ✅ Manual test script (24 test cases) (Phase 2)
- ✅ Access control matrix validated (Phase 2)

### ❌ Not Completed (vs Issue #357)

**Missing from Issue Requirements**:
- ❌ No Role model/table (we used enum instead)
- ❌ No Permission model/table (we used JSONB)
- ❌ No RolePermission junction table (we used JSONB)
- ❌ No UserRole junction table (we used JSONB)
- ❌ No `@require_permission` decorator (we used dependency injection)
- ❌ No `@require_ownership` decorator (we used dependency injection)
- ❌ No cross-user access tests (manual script, not automated)
- ❌ No security scan (Bandit, Safety)
- ❌ No admin role enforcement (system-wide admin)

**Missing Coverage**:
- ❌ Projects don't have role-based sharing yet
- ❌ Files don't have role-based sharing yet
- ❌ Conversations don't have role-based sharing yet
- ❌ System-wide admin role (bypass all ownership checks)

---

## Approach Comparison

### Issue #357 Approach (Original Gameplan)
**Architecture**: Traditional RBAC with relational tables
- Separate `roles` table
- Separate `permissions` table
- Junction tables for relationships
- Decorator-based enforcement
- Centralized AuthorizationService

**Pros**:
- Enterprise-standard approach
- Fine-grained permission control
- Easy to add new permissions
- Clear audit trail
- Familiar to security auditors

**Cons**:
- More complex implementation (2-3 weeks)
- More database tables/joins
- Potentially slower queries
- Overkill for current needs?

### Our Approach (Phases 1-2)
**Architecture**: Lightweight RBAC with JSONB
- owner_id columns for ownership
- JSONB `shared_with` for collaboration
- ShareRole enum (VIEWER/EDITOR/ADMIN)
- Repository-level enforcement
- Dependency injection pattern

**Pros**:
- Fast implementation (5 hours)
- Simple schema (fewer tables)
- Fast queries (GIN indexes on JSONB)
- Sufficient for current needs
- Production-ready

**Cons**:
- Less flexible for future complex permissions
- No system-wide admin role
- Not the "textbook" RBAC approach
- May need refactor for enterprise features

---

## Gap Between What We Built vs Issue #357

### Critical Gaps

1. **No System-Wide Admin Role**
   - Issue requires: Admin can access ALL resources
   - We have: Only owner or shared users can access
   - Impact: Support team can't help users, no admin override

2. **No Decorators**
   - Issue requires: `@require_permission`, `@require_ownership`
   - We have: Dependency injection with owner_id checks
   - Impact: Different pattern, but functionally equivalent

3. **No Cross-User Access Tests**
   - Issue requires: Automated tests proving User A can't access User B's data
   - We have: Manual test script (not automated)
   - Impact: Can't run in CI/CD, manual validation only

4. **No Security Scan**
   - Issue requires: Security scan passes (Bandit, Safety)
   - We have: No scan run yet
   - Impact: Unknown if vulnerabilities exist

### Minor Gaps

5. **Partial Resource Coverage**
   - We have: Lists, Todos with role-based sharing
   - Missing: Projects, Files, Conversations with role-based sharing
   - Impact: Inconsistent collaboration features

6. **No Permission Tables**
   - Issue requires: Role/Permission models
   - We have: Enum + JSONB
   - Impact: Less flexible, but sufficient for current needs

---

## Recommendation: Phase 3 Options

### Option A: Fill Critical Gaps (Pragmatic) ⭐ **RECOMMENDED**

**Scope**: Add missing features to meet Issue #357 requirements
1. System-wide admin role enforcement
2. Cross-user access automated tests
3. Security scan (Bandit, Safety)
4. Extend to Projects/Files/Conversations

**Estimated**: 3-4 hours
**Risk**: Low (builds on working system)
**Closes Issue #357**: Yes (with lightweight approach)

### Option B: Refactor to Traditional RBAC (Purist)

**Scope**: Rebuild with relational Role/Permission tables
1. Create Role/Permission/junction tables
2. Migrate JSONB to relational model
3. Create AuthorizationService
4. Add decorators
5. Re-test everything

**Estimated**: 2-3 days (significant refactor)
**Risk**: Medium (changes working system)
**Closes Issue #357**: Yes (exact match to requirements)

### Option C: Hybrid Approach

**Scope**: Keep JSONB for sharing, add system admin role
1. Add User.is_admin boolean flag
2. Repository methods check is_admin for bypass
3. Add cross-user tests
4. Security scan
5. Extend to more resources

**Estimated**: 2-3 hours
**Risk**: Low (minimal changes)
**Closes Issue #357**: Partially (meets spirit, not letter)

---

## My Recommendation

**Option A** (Fill Critical Gaps with pragmatic approach)

**Rationale**:
1. Our lightweight RBAC **meets the security goals** of Issue #357
2. System-wide admin + tests + scan = production-ready
3. Can always refactor to traditional RBAC later if needed
4. 3-4 hours vs 2-3 days is significant time savings
5. Current approach is working well

**What Phase 3 Should Include**:
1. ✅ System-wide admin role (User.is_admin flag + bypass logic)
2. ✅ Cross-user access automated tests (pytest)
3. ✅ Security scan (Bandit, Safety)
4. ✅ Extend to Projects/Files (same JSONB pattern)
5. ✅ Update Issue #357 with completion evidence

**After Phase 3**: Issue #357 can be closed with evidence that security goals are met, even if implementation differs from original spec.

---

## Questions for PM

1. **Is the lightweight JSONB approach acceptable** for Issue #357, or do you require traditional Role/Permission tables?

2. **What level of admin role** do we need?
   - Simple: `User.is_admin` boolean (bypasses all ownership checks)
   - Complex: Separate admin permission table with granular controls

3. **Which resources need role-based sharing** in Phase 3?
   - Projects? Files? Conversations? All of them?

4. **Are automated cross-user tests required**, or is manual test script sufficient for alpha?

5. **Should we close Issue #357 after Phase 3**, or keep it open for future refactor to traditional RBAC?

---

_Gap Analysis Prepared By: Lead Developer (Claude Sonnet)_
_Date: November 22, 2025, 11:50 AM_
_Purpose: Align Phase 3 scope with Issue #357 requirements_
