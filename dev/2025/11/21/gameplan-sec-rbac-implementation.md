# Gameplan: SEC-RBAC - Implement Role-Based Access Control

**Issue**: #357 - SEC-RBAC: Implement RBAC
**Priority**: P0 (CRITICAL - Security Showstopper)
**Sprint**: S1 (Security)
**Milestone**: MVP
**Discovered By**: Ted Nadeau (architectural review)
**Date**: November 21, 2025, 3:35 PM PT

---

## Executive Summary

**What**: Implement proper Role-Based Access Control (RBAC) system
**Why**: Currently ANY authenticated user can access ANY resource - critical security gap
**Blocks**: Multi-user testing, alpha launch, security audit, compliance
**Risk**: Data breach liability, cannot have external users
**Estimated Effort**: Large (2-3 weeks)

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### STOP! Complete This Section WITH PM Before Writing Rest of Gameplan

### Part A: Chief Architect's Current Understanding

Based on available context, I believe:

**Infrastructure Status**:
- [x] Web framework: **FastAPI** (I think: based on web/app.py references)
- [x] CLI structure: **Click** (I think: based on cli/ directory)
- [x] Database: **PostgreSQL** (I think: mentioned in test failures)
- [x] Testing framework: **pytest** (I think: confirmed from test reports)
- [ ] Auth system: **JWT-based** (I think: JWT authentication works per issue)
- [ ] User model exists: **Yes** (I think: "User A can read User B's conversations")
- [ ] Resource tables: **Unknown** (need to discover which tables need owner_id)

**My understanding of the task**:
- I believe we need to: Create complete RBAC system from scratch
- I think this involves: Database models + migrations + decorators + endpoint protection
- I assume the current state is: JWT auth exists but zero authorization checks

**Critical Questions**:
1. Which resource tables need `owner_id` field?
2. Where are the API endpoints defined?
3. Is there an existing User model with ID field?
4. Are there existing service methods that need protection?
5. How is JWT currently implemented?

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What actually exists in the filesystem?**
   ```bash
   # Check web framework
   ls -la web/
   cat web/app.py | head -20  # Verify FastAPI

   # Check database models
   ls -la services/*/models.py
   find . -name "models.py" -type f

   # Check existing auth
   find . -name "*auth*" -type f
   grep -r "JWT\|jwt" services/ --include="*.py"

   # Find resource tables
   find . -name "*.py" -exec grep -l "class.*Model\|Table" {} \;

   # Check for existing decorators
   grep -r "@require\|@auth" services/ --include="*.py"
   ```

2. **Critical infrastructure details** (per PROJECT.md):
   - Database port: ____________ (PROJECT.md should have this)
   - API port: ____________ (PROJECT.md should have this)
   - User table name/location: ____________
   - Current auth mechanism details: ____________

3. **Recent work in this area?**
   - Last changes to auth system: ____________
   - Known issues/quirks: ____________
   - Previous security attempts: ____________

4. **Actual task needed?**
   - [x] Create new feature from scratch (RBAC system)
   - [ ] Add to existing partial RBAC
   - [ ] Fix broken authorization
   - [ ] Other: ____________

5. **Resource tables requiring owner_id** (CRITICAL):
   - conversations table: Yes/No/Location?
   - lists table: Yes/No/Location?
   - tasks table: Yes/No/Location?
   - Other tables: ____________

6. **Security scan requirements**:
   - Tool to use: ____________ (Bandit? Safety? Custom?)
   - Standards to meet: ____________
   - Who validates scan: ____________

### Part C: Proceed/Revise Decision

After PM verification:
- [ ] **PROCEED** - Understanding is correct, gameplan appropriate
- [ ] **REVISE** - Major assumptions wrong, need different approach
- [ ] **CLARIFY** - Need more context on: ____________

**If REVISE or CLARIFY checked, STOP and create new gameplan**

---

## Phase 0: Initial Bookending - Security Audit & Investigation

### Purpose
**BEFORE implementing anything**: Understand current security posture, identify all unprotected resources, document risk

### Required Actions

#### 1. GitHub Issue Verification & Bookending
```bash
# Verify issue exists
gh issue view 357

# Initial bookending
gh issue edit 357 --body "
## Status: Security Investigation Started

### Phase 0: Security Audit
- [ ] Current auth mechanism documented
- [ ] All resource tables identified
- [ ] All API endpoints catalogued
- [ ] Unprotected endpoints listed
- [ ] Risk assessment complete

**Agent**: Claude Code
**Started**: $(date)
"
```

#### 2. Comprehensive Security Audit

**Task 0.1**: Document Current Auth Mechanism (30 min)
```bash
# Find JWT implementation
find . -name "*.py" -exec grep -l "JWT\|jwt\|token" {} \;

# Document findings in audit report
echo "# Current Auth Audit" > /tmp/sec-rbac-audit.md
echo "## JWT Implementation" >> /tmp/sec-rbac-audit.md
# ... detailed investigation
```

**Task 0.2**: Identify ALL Resource Tables (45 min)
```bash
# Find all database models
find services/ -name "models.py" -o -name "*_model.py"

# For each model, document:
# - Table name
# - Current fields
# - Whether it has owner_id
# - What data it contains

# Create inventory
echo "## Resource Tables Inventory" >> /tmp/sec-rbac-audit.md
# List all tables with security implications
```

**Task 0.3**: Catalogue ALL API Endpoints (60 min)
```bash
# Find all FastAPI route definitions
grep -r "@app\.\|@router\.\|@api\." web/ --include="*.py"

# For each endpoint, document:
# - Route path
# - HTTP method
# - What resource it accesses
# - Current auth/authz status

# Create endpoint inventory
echo "## API Endpoints Inventory" >> /tmp/sec-rbac-audit.md
# List all endpoints with protection status
```

**Task 0.4**: Identify Service Methods Needing Protection (45 min)
```bash
# Find all service layer methods
find services/ -name "*_service.py" -o -name "service.py"

# Document methods that:
# - Access user data
# - Modify resources
# - Need ownership checks

# Create service method inventory
echo "## Service Methods Requiring Authorization" >> /tmp/sec-rbac-audit.md
```

**Task 0.5**: Create Risk Assessment (30 min)
```markdown
# Risk Assessment Template

## Current Vulnerabilities
1. **Cross-User Data Access**
   - Endpoint: /conversations/{id}
   - Risk: User A can read User B's conversations
   - Severity: CRITICAL
   - Data at risk: [describe]

2. **Unauthorized Modification**
   - Endpoint: /lists/{id}/delete
   - Risk: User A can delete User B's lists
   - Severity: CRITICAL
   - Data at risk: [describe]

[Continue for all discovered vulnerabilities]

## Attack Scenarios
1. Scenario: Malicious user enumerates IDs
2. Scenario: User modifies admin-only settings
[Continue for all scenarios]

## Compliance Impact
- SOC2: [impact]
- GDPR: [impact]
- HIPAA (if applicable): [impact]
```

#### 3. Update GitHub with Audit Results
```bash
gh issue comment 357 -b "
## Phase 0 Complete: Security Audit Results

### Findings
- **Unprotected Endpoints**: [count]
- **Resource Tables**: [count] require owner_id
- **Service Methods**: [count] need authorization
- **Risk Level**: CRITICAL

### Audit Report
See: /dev/2025/11/21/sec-rbac-security-audit.md

### Ready for Implementation Planning
"
```

### Deliverables
- [ ] Complete security audit report (moved to persistent storage)
- [ ] Resource tables inventory
- [ ] API endpoints inventory
- [ ] Service methods inventory
- [ ] Risk assessment document
- [ ] GitHub issue updated with findings

### STOP Conditions
- ❌ Cannot find User model (blocks everything)
- ❌ Auth system more complex than JWT (need different approach)
- ❌ Database not PostgreSQL (need different migrations)
- ❌ No FastAPI framework (need different decorators)

---

## Phase 1: Database Schema - RBAC Models & Migrations

**Duration**: 2-3 days
**Deploy**: Claude Code (single agent - schema design critical)

### Purpose
Create database foundation for RBAC: roles, permissions, junction tables, owner_id fields

### Tasks

#### Task 1.1: Create Role Model (2 hours)

**Create**: `services/auth/models/role.py`

```python
# Expected structure (verify against existing patterns)
class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    is_system = Column(Boolean, default=False)  # System roles can't be deleted
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
```

**Tests Required**:
- [ ] Role creation with valid data
- [ ] Unique name constraint enforced
- [ ] System role cannot be deleted
- [ ] Role updates tracked with timestamp

#### Task 1.2: Create Permission Model (2 hours)

**Create**: `services/auth/models/permission.py`

```python
# Expected structure
class Permission(Base):
    __tablename__ = "permissions"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    resource = Column(String(50), nullable=False)  # e.g., "conversation", "list"
    action = Column(String(50), nullable=False)  # e.g., "read", "write", "delete"
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Unique constraint on resource + action
    __table_args__ = (
        UniqueConstraint('resource', 'action', name='uq_resource_action'),
    )
```

**Tests Required**:
- [ ] Permission creation with resource + action
- [ ] Unique resource+action constraint enforced
- [ ] Valid permission combinations only

#### Task 1.3: Create RolePermission Junction Table (1 hour)

**Create**: `services/auth/models/role_permission.py`

```python
class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(UUID, ForeignKey('roles.id'), primary_key=True)
    permission_id = Column(UUID, ForeignKey('permissions.id'), primary_key=True)
    granted_at = Column(DateTime, default=datetime.utcnow)
```

**Tests Required**:
- [ ] Role-permission association created
- [ ] Foreign key constraints enforced
- [ ] Duplicate associations prevented

#### Task 1.4: Create UserRole Junction Table (1 hour)

**Create**: `services/auth/models/user_role.py`

```python
class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(UUID, ForeignKey('users.id'), primary_key=True)
    role_id = Column(UUID, ForeignKey('roles.id'), primary_key=True)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    assigned_by = Column(UUID, ForeignKey('users.id'))  # Audit trail
```

**Tests Required**:
- [ ] User-role association created
- [ ] Foreign key constraints enforced
- [ ] Assignment audit trail captured

#### Task 1.5: Add owner_id to Resource Tables (4-6 hours)

**CRITICAL**: Must identify ALL resource tables requiring owner_id

**For each resource table**:
1. Add migration to add `owner_id` column
2. Create foreign key to users table
3. Add index on owner_id
4. Backfill existing data (assign to admin or mark)

**Example Migration Pattern**:
```python
# Migration: add_owner_id_to_conversations
def upgrade():
    # Add column
    op.add_column('conversations',
        sa.Column('owner_id', UUID, nullable=True))

    # Add foreign key
    op.create_foreign_key(
        'fk_conversations_owner',
        'conversations', 'users',
        ['owner_id'], ['id']
    )

    # Add index
    op.create_index('ix_conversations_owner_id',
        'conversations', ['owner_id'])

    # Backfill existing data (assign to first admin user)
    # Note: Requires data migration strategy from PM
```

**Tables requiring owner_id** (verify with PM in Phase -1):
- [ ] conversations
- [ ] lists
- [ ] tasks
- [ ] notes
- [ ] [other tables identified in Phase 0]

**Tests Required** (per table):
- [ ] owner_id foreign key enforced
- [ ] Cannot set invalid owner_id
- [ ] Index improves query performance
- [ ] Backfill completed successfully

#### Task 1.6: Seed Initial Roles & Permissions (2 hours)

**Create**: `services/auth/seeds/rbac_seed.py`

```python
# Seed data for initial RBAC setup
ROLES = [
    {"name": "admin", "description": "Full system access", "is_system": True},
    {"name": "user", "description": "Standard user access", "is_system": True},
    {"name": "viewer", "description": "Read-only access", "is_system": True},
]

PERMISSIONS = [
    # Conversation permissions
    {"resource": "conversation", "action": "read"},
    {"resource": "conversation", "action": "write"},
    {"resource": "conversation", "action": "delete"},

    # List permissions
    {"resource": "list", "action": "read"},
    {"resource": "list", "action": "write"},
    {"resource": "list", "action": "delete"},

    # [Add all resource types from Phase 0 audit]
]

ROLE_PERMISSIONS = {
    "admin": ["*:*"],  # All permissions
    "user": [
        "conversation:read", "conversation:write", "conversation:delete",
        "list:read", "list:write", "list:delete",
        # [Own resources only - enforced by decorators]
    ],
    "viewer": [
        "conversation:read",
        "list:read",
        # [Shared resources only]
    ]
}
```

**Tests Required**:
- [ ] Seed data creates all roles
- [ ] Seed data creates all permissions
- [ ] Role-permission associations correct
- [ ] Idempotent (can run multiple times)

### Phase 1 Deliverables
- [ ] 4 new models created with tests
- [ ] owner_id added to all resource tables
- [ ] Migrations tested (up and down)
- [ ] Seed data creates initial RBAC setup
- [ ] All tests passing (100% coverage on models)
- [ ] GitHub issue updated with progress

### Phase 1 STOP Conditions
- ❌ Migration fails on any table
- ❌ Foreign key constraints break existing queries
- ❌ Cannot backfill owner_id data (need PM strategy)
- ❌ Performance degradation on large tables

---

## Phase 2: Authorization Service - Permission Checking Logic

**Duration**: 2-3 days
**Deploy**: Claude Code (single agent - security logic critical)

### Purpose
Create service layer for checking permissions and ownership

### Tasks

#### Task 2.1: Create AuthorizationService (3 hours)

**Create**: `services/auth/authorization_service.py`

```python
class AuthorizationService:
    """Centralized authorization logic"""

    def __init__(self, db_session):
        self.db = db_session

    def check_permission(self, user_id: UUID, resource: str, action: str) -> bool:
        """Check if user has permission for resource:action"""
        # 1. Get user's roles
        # 2. Get permissions for those roles
        # 3. Check if permission exists
        # 4. Cache result for performance
        pass

    def check_ownership(self, user_id: UUID, resource_type: str,
                       resource_id: UUID) -> bool:
        """Check if user owns the resource"""
        # 1. Query resource table for owner_id
        # 2. Compare with user_id
        # 3. Cache result for performance
        pass

    def is_admin(self, user_id: UUID) -> bool:
        """Check if user has admin role"""
        # Quick check for admin bypass
        pass

    def get_user_permissions(self, user_id: UUID) -> List[str]:
        """Get all permissions for user (for debugging/UI)"""
        # Return list like ["conversation:read", "list:write"]
        pass
```

**Tests Required**:
- [ ] User with permission returns True
- [ ] User without permission returns False
- [ ] Admin bypasses all checks
- [ ] Ownership check validates owner_id
- [ ] Non-owner returns False
- [ ] Permission check caches results
- [ ] Invalid resource/action handled gracefully

#### Task 2.2: Create Permission Checker Utilities (2 hours)

**Create**: `services/auth/permission_utils.py`

```python
def require_permission(resource: str, action: str):
    """Utility for checking permissions in service methods"""
    # Can be used without decorators
    pass

def require_ownership(resource_type: str, resource_id: UUID):
    """Utility for checking ownership in service methods"""
    pass

def get_accessible_resources(user_id: UUID, resource_type: str):
    """Get all resources user can access (for queries)"""
    # Returns query filter for owner_id
    pass
```

**Tests Required**:
- [ ] Utilities work without HTTP context
- [ ] Can be used in background jobs
- [ ] Proper error messages on failure

#### Task 2.3: Integration with Existing Auth (2 hours)

**Modify**: Current JWT/auth implementation

```python
# Add authorization service to auth flow
# After JWT validation, inject authorization service
# Make user_id and auth service available to endpoints
```

**Tests Required**:
- [ ] JWT still works as before
- [ ] Authorization service available in requests
- [ ] No performance degradation

### Phase 2 Deliverables
- [ ] AuthorizationService implemented and tested
- [ ] Permission utilities created
- [ ] Integration with existing auth complete
- [ ] 100% test coverage on service
- [ ] Performance benchmarks met (<50ms for checks)
- [ ] GitHub issue updated

### Phase 2 STOP Conditions
- ❌ Performance too slow (>100ms per check)
- ❌ Cannot integrate with existing auth
- ❌ Cache invalidation issues

---

## Phase 3: API Protection - Decorators & Middleware

**Duration**: 3-4 days
**Deploy**: Claude Code (single agent - security critical)

### Purpose
Create decorators/middleware to protect ALL endpoints and service methods

### Tasks

#### Task 3.1: Create Permission Decorator (3 hours)

**Create**: `services/auth/decorators.py`

```python
from functools import wraps
from fastapi import HTTPException, Depends

def require_permission(resource: str, action: str):
    """Decorator to require specific permission"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 1. Get current user from JWT
            # 2. Check permission via AuthorizationService
            # 3. Raise 403 if not authorized
            # 4. Continue if authorized
            pass
        return wrapper
    return decorator

def require_ownership(resource_type: str,
                     id_param: str = "id"):
    """Decorator to require resource ownership"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 1. Get current user
            # 2. Extract resource_id from kwargs[id_param]
            # 3. Check ownership via AuthorizationService
            # 4. Raise 403 if not owner and not admin
            pass
        return wrapper
    return decorator

def require_admin():
    """Decorator to require admin role"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Quick admin check
            pass
        return wrapper
    return decorator
```

**Tests Required**:
- [ ] Decorator blocks unauthorized users
- [ ] Decorator allows authorized users
- [ ] Ownership decorator validates owner_id
- [ ] Admin bypass works
- [ ] Proper 403 errors returned
- [ ] Error messages are clear

#### Task 3.2: Apply Decorators to ALL Endpoints (6-8 hours)

**CRITICAL**: Must protect EVERY endpoint identified in Phase 0

**For each endpoint**:
1. Add appropriate decorator (@require_permission or @require_ownership)
2. Add test to verify protection
3. Document in code which permission is required

**Example**:
```python
# Before
@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: UUID):
    return conversation_service.get(conversation_id)

# After
@app.get("/conversations/{conversation_id}")
@require_ownership("conversation", "conversation_id")
async def get_conversation(conversation_id: UUID):
    return conversation_service.get(conversation_id)
```

**Tracking**:
- [ ] Endpoint 1: /conversations - protected
- [ ] Endpoint 2: /lists - protected
- [ ] [Continue for ALL endpoints from Phase 0]

**Tests Required** (per endpoint):
- [ ] User can access own resource
- [ ] User cannot access other's resource
- [ ] Admin can access any resource
- [ ] 403 returned for unauthorized

#### Task 3.3: Apply Protection to Service Methods (4-6 hours)

**For each service method identified in Phase 0**:
1. Add permission/ownership checks
2. Ensure service layer enforces authorization
3. Add comprehensive tests

**Example**:
```python
# In ConversationService
def get_conversation(self, conversation_id: UUID, user_id: UUID):
    # Check ownership
    if not self.auth_service.check_ownership(
        user_id, "conversation", conversation_id
    ):
        raise PermissionError("Not authorized")

    return self.db.query(Conversation).get(conversation_id)
```

**Tests Required**:
- [ ] Service method enforces authorization
- [ ] Cannot bypass via direct service call
- [ ] Proper error on unauthorized access

#### Task 3.4: Create Authorization Middleware (Optional) (2 hours)

**If beneficial**: Create FastAPI middleware for blanket protection

```python
@app.middleware("http")
async def authorization_middleware(request: Request, call_next):
    # Log all authorization attempts
    # Add request-level authorization context
    pass
```

### Phase 3 Deliverables
- [ ] Decorators created and tested
- [ ] ALL endpoints protected (100%)
- [ ] ALL service methods protected (100%)
- [ ] Comprehensive test suite (100% coverage)
- [ ] No unprotected code paths remain
- [ ] GitHub issue updated

### Phase 3 STOP Conditions
- ❌ Cannot find all endpoints (Phase 0 audit incomplete)
- ❌ Decorator breaks existing functionality
- ❌ Performance degradation unacceptable

---

## Phase 4: Comprehensive Testing & Security Scan

**Duration**: 2-3 days
**Deploy**: Claude Code (single agent - testing critical)

### Purpose
Verify RBAC works correctly and no security holes remain

### Tasks

#### Task 4.1: Cross-User Access Tests (4 hours)

**Create**: `tests/security/test_cross_user_access.py`

```python
def test_user_cannot_read_other_conversation():
    """User A cannot read User B's conversation"""
    # 1. Create User A with conversation
    # 2. Login as User B
    # 3. Try to access User A's conversation
    # 4. Assert 403 Forbidden
    pass

def test_user_cannot_modify_other_list():
    """User A cannot modify User B's list"""
    # Similar pattern for all resources
    pass

# [Add tests for ALL resource types]
```

**Tests Required**:
- [ ] Read protection works (all resources)
- [ ] Write protection works (all resources)
- [ ] Delete protection works (all resources)
- [ ] Admin bypass works correctly
- [ ] Viewer role restrictions work

#### Task 4.2: Permission Matrix Tests (3 hours)

**Create**: `tests/security/test_permission_matrix.py`

```python
# Test all role-permission combinations
PERMISSION_MATRIX = {
    "admin": {
        "conversation": ["read", "write", "delete"],
        "list": ["read", "write", "delete"],
        # All permissions
    },
    "user": {
        "conversation": ["read", "write", "delete"],  # Own only
        "list": ["read", "write", "delete"],  # Own only
    },
    "viewer": {
        "conversation": ["read"],  # Shared only
        "list": ["read"],  # Shared only
    }
}

# Generate tests from matrix
```

**Tests Required**:
- [ ] Admin can do everything
- [ ] User can CRUD own resources
- [ ] User cannot access other resources
- [ ] Viewer can only read shared resources

#### Task 4.3: Security Scan (2 hours)

**Run Security Tools**:
```bash
# Static analysis
bandit -r services/ -ll

# Dependency vulnerabilities
safety check

# SQL injection check
# Manual review of query construction

# Authorization bypass attempts
# Penetration testing checklist
```

**Checks Required**:
- [ ] No SQL injection vulnerabilities
- [ ] No hard-coded credentials
- [ ] No authorization bypass paths
- [ ] All inputs validated
- [ ] Proper error handling (no info leakage)

#### Task 4.4: Performance Testing (2 hours)

```python
def test_authorization_performance():
    """Authorization checks don't degrade performance"""
    # 1. Measure endpoint response time before RBAC
    # 2. Measure endpoint response time after RBAC
    # 3. Assert degradation < 50ms
    pass
```

**Tests Required**:
- [ ] Authorization checks < 50ms
- [ ] Cache improves repeated checks
- [ ] No N+1 query problems

#### Task 4.5: Documentation & Audit Trail (2 hours)

**Create**: `docs/security/rbac-implementation.md`

```markdown
# RBAC Implementation Documentation

## Security Model
- Roles: admin, user, viewer
- Permissions: [list all]
- Protected resources: [list all]

## Usage Guide
- How to check permissions in code
- How to add new permissions
- How to assign roles

## Security Audit Results
- Scan date: [date]
- Tools used: [list]
- Vulnerabilities found: [list]
- Mitigation steps: [list]

## Testing Coverage
- Cross-user access tests: [count]
- Permission matrix tests: [count]
- Total authorization tests: [count]
```

### Phase 4 Deliverables
- [ ] Cross-user access tests passing
- [ ] Permission matrix tests passing
- [ ] Security scan clean
- [ ] Performance requirements met
- [ ] Documentation complete
- [ ] 100% test coverage on authorization
- [ ] GitHub issue updated

### Phase 4 STOP Conditions
- ❌ Security scan finds vulnerabilities
- ❌ Tests reveal authorization bypass
- ❌ Performance unacceptable

---

## Phase Z: Final Bookending & Security Sign-Off

### Purpose
Complete final verification, get security approval, prepare for deployment

### Required Actions

#### 1. Final Security Verification
```bash
# Run complete test suite
pytest tests/security/ -v

# Run security scan
bandit -r services/ -ll

# Manual security checklist
[ ] No unprotected endpoints
[ ] All resources have owner_id
[ ] Cross-user access blocked
[ ] Admin permissions working
[ ] Viewer restrictions working
[ ] Performance acceptable
```

#### 2. GitHub Final Update
```bash
gh issue edit 357 --body "
## Status: Complete - Awaiting Security Sign-Off

### Implementation Complete
- [x] RBAC models and migrations deployed
- [x] Authorization service implemented
- [x] ALL endpoints protected (100%)
- [x] ALL service methods protected (100%)
- [x] Comprehensive tests passing
- [x] Security scan clean

### Evidence
- Test results: [link]
- Security scan: [link]
- Performance metrics: [link]
- Documentation: [link]

### Ready for Security Review
**Reviewer**: Ted Nadeau (discovered issue)
**PM**: [name] (final approval)
"
```

#### 3. Documentation Updates
- [ ] Update architecture.md with RBAC system
- [ ] Create security ADR documenting decisions
- [ ] Update API documentation with authorization requirements
- [ ] Create runbook for role/permission management

#### 4. Evidence Compilation
- [ ] All test outputs in session log
- [ ] Security scan reports
- [ ] Performance benchmarks
- [ ] Before/after comparison (no authz → full RBAC)

#### 5. Deployment Preparation
- [ ] Migration scripts tested on staging
- [ ] Rollback plan documented
- [ ] Seed data ready for production
- [ ] Monitoring alerts configured

#### 6. Security Sign-Off Request
```markdown
@Ted Nadeau - SEC-RBAC implementation complete and ready for security review:
- All acceptance criteria met ✅
- No unprotected endpoints remain ✅
- Cross-user access blocked ✅
- Security scan clean ✅
- 100% test coverage ✅

Please review and approve for alpha deployment.

@PM - After security sign-off, ready for final approval and closure.
```

### CRITICAL: Agents Do NOT Close Security Issues
**Requires**: Security expert approval + PM approval

---

## STOP Conditions (Throughout Implementation)

**STOP immediately and escalate if**:

### Security Issues
- ❌ Authorization bypass discovered
- ❌ Data leak possible
- ❌ SQL injection vulnerability found
- ❌ Cannot protect all endpoints

### Implementation Issues
- ❌ Migrations break existing data
- ❌ Performance degradation >100ms
- ❌ Cannot integrate with existing auth
- ❌ JWT system incompatible

### Testing Issues
- ❌ Tests reveal security holes
- ❌ Cannot achieve 100% coverage
- ❌ Permission checks can be bypassed

**When stopped**: Document the issue with evidence, provide options, wait for PM/security review.

---

## Evidence Requirements

### What Counts as Evidence

**Security Testing**:
✅ Test output showing 403 for unauthorized access
✅ Test output showing 200 for authorized access
✅ Security scan reports (Bandit, Safety)
✅ Manual penetration test results

**Implementation**:
✅ Database migrations applied successfully
✅ All endpoints have decorators (code review)
✅ Service methods enforce authorization
✅ Seed data creates proper roles/permissions

**Performance**:
✅ Benchmark showing <50ms authorization overhead
✅ Cache hit rates for repeated checks
✅ Query performance with owner_id indexes

❌ "Should be secure"
❌ "Tests pass" without showing authorization tests
❌ "Protected" without showing decorator usage

---

## Success Criteria

### Issue Completion Requires

**Functionality**:
- [x] Role model created and seeded
- [x] Permission model created and seeded
- [x] Junction tables created
- [x] owner_id added to ALL resource tables
- [x] Decorators protect ALL endpoints
- [x] Service methods enforce authorization

**Testing**:
- [x] User cannot access other user's data (proven)
- [x] Admin can access all resources (proven)
- [x] Viewer restrictions work (proven)
- [x] 100% test coverage on authorization
- [x] Security scan passes

**Quality**:
- [x] No authorization bypasses possible
- [x] Performance acceptable (<50ms overhead)
- [x] Documentation complete
- [x] Deployment ready

**Approval**:
- [x] Security expert sign-off (Ted Nadeau)
- [x] PM approval
- [x] Evidence provided for all criteria

---

## Risk Mitigation

### High-Risk Areas

**1. Data Backfill**
- **Risk**: Existing data has no owner_id
- **Mitigation**: Clear strategy from PM for assigning owners
- **Fallback**: Mark as system-owned, require admin review

**2. Performance Impact**
- **Risk**: Authorization adds latency
- **Mitigation**: Aggressive caching, indexes
- **Monitoring**: Alert if >50ms overhead

**3. Authorization Bypass**
- **Risk**: Forgotten endpoints or service methods
- **Mitigation**: Comprehensive Phase 0 audit, 100% testing
- **Verification**: Security scan + manual review

**4. Breaking Changes**
- **Risk**: Existing clients break with new auth requirements
- **Mitigation**: Gradual rollout, backward compatibility period
- **Testing**: Comprehensive regression testing

---

## Deployment Strategy

### Staged Rollout

**Stage 1: Staging Environment**
- Deploy RBAC system
- Run complete test suite
- Manual security testing
- Performance validation

**Stage 2: Alpha (If Approved)**
- Deploy to alpha environment
- Limited users with monitoring
- Quick rollback ability
- Gather feedback

**Stage 3: Production**
- Full deployment with monitoring
- Phased by user group
- 24/7 security monitoring

### Rollback Plan

If critical issue discovered:
1. Revert migrations (down)
2. Remove decorators (feature flag)
3. Restore previous auth behavior
4. Investigate and fix offline

---

## Estimated Effort

**Total**: 2-3 weeks (Large)

**Breakdown by Phase**:
- Phase -1: Verification with PM (1-2 hours)
- Phase 0: Security audit (1 day)
- Phase 1: Database models (2-3 days)
- Phase 2: Authorization service (2-3 days)
- Phase 3: API protection (3-4 days)
- Phase 4: Testing & scan (2-3 days)
- Phase Z: Final verification (1 day)

**Complexity**: High (security-critical, touches everything)

---

## Notes for Implementation

### Best Practices

**Security First**:
- Deny by default (explicit allow only)
- Defense in depth (decorators + service checks)
- Audit trail for all authorization decisions
- Clear error messages (but no info leakage)

**Testing Discipline**:
- Test negative cases (unauthorized access)
- Test positive cases (authorized access)
- Test edge cases (admin bypass, viewer limits)
- Performance tests for every check

**Code Quality**:
- Clear naming (require_permission, check_ownership)
- Consistent patterns across endpoints
- Comprehensive documentation
- No shortcuts or workarounds

### Common Pitfalls to Avoid

❌ Forgetting to protect a single endpoint
❌ Inconsistent permission names
❌ N+1 queries for permission checks
❌ Exposing sensitive data in error messages
❌ Assuming admin check is enough
❌ Not testing negative cases

---

## Dependencies

### Required (Must exist first)
- [x] User model with ID field
- [x] JWT authentication working
- [x] PostgreSQL database
- [x] FastAPI framework
- [x] pytest testing framework

### Blocks (Cannot proceed until complete)
- Multi-user alpha testing
- External user access
- Security audit/compliance
- Production deployment

---

## Related Documentation

**To Read Before Starting**:
- PROJECT.md - Critical ports and configuration
- Current auth implementation
- Database schema documentation
- API endpoint documentation

**To Create During Work**:
- Security audit report (Phase 0)
- RBAC implementation ADR
- Security testing documentation
- Deployment runbook

---

**Remember**:
- **Security is binary**: Either secure or not, no 80% security
- **Evidence required**: Every claim about security must be proven
- **PM + Security approval**: Both required before closure
- **Quality over speed**: Security bugs are unacceptable

---

_Gameplan created: November 21, 2025, 3:35 PM PT_
_Last updated: [date]_
_Status: Awaiting Phase -1 Verification with PM_
