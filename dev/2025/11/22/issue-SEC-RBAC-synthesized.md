# SEC-RBAC - Implement Role-Based Access Control

**Priority**: P0 (CRITICAL - Security showstopper)
**Labels**: `security`, `p0-critical`, `alpha-blocking`, `compliance`
**Milestone**: Sprint S1
**Epic**: Security Foundation
**Related**: ADR-012 (JWT Authentication), #358 (Encryption at Rest)

---

## Problem Statement

### Current State
**CRITICAL SECURITY GAP**: Any authenticated user can access ANY resource. No authorization checks exist.

- ✅ JWT authentication works (who you are)
- ❌ NO authorization (what you can do)
- ❌ User A can read User B's conversations
- ❌ User A can delete User B's data
- ❌ No admin vs user distinction
- ❌ No resource ownership checks

### Impact
- **Blocks**: Multi-user testing, alpha launch with external users, any production deployment
- **User Impact**: Complete privacy violation - any user can access/delete any data
- **Technical Debt**: Adding RBAC later means retrofitting every endpoint and service

### Strategic Context
Ted Nadeau's architectural review identified this as the #1 security blocker. Without RBAC, we literally cannot have multiple users safely. This must be completed before any external alpha testing.

---

## Goal

**Primary Objective**: Implement secure role-based access control with ownership verification for all resources

**Example User Experience**:
```
BEFORE: User A can DELETE User B's conversations
AFTER: User A gets 403 Forbidden when accessing User B's resources
```

**Not In Scope**:
- ❌ Complex permission hierarchies (keep it simple: admin/user/viewer)
- ❌ Dynamic permission creation (roles are fixed for MVP)
- ❌ Team-based permissions (post-MVP)
- ❌ Granular field-level permissions

---

## What Already Exists

### Infrastructure ✅
- JWT authentication system (ADR-012)
- User model with authentication
- Middleware pattern for request processing
- Domain models for all resources

### What's Missing ❌
- Role and Permission models
- Resource ownership tracking (`owner_id` fields)
- Authorization decorators/middleware
- Permission enforcement at API and service layers

---

## Requirements

### Phase 1: Database Schema
**Objective**: Create RBAC data models and migrations

**Tasks**:
- [ ] Create Role model (id, name, permissions JSON)
- [ ] Create UserRole junction table
- [ ] Add `owner_id` to all resource tables
- [ ] Create Alembic migration
- [ ] Backfill existing data with owner_id

**Deliverables**:
- Migration file with RBAC schema
- Updated domain models

### Phase 2: Authorization Middleware
**Objective**: Build authorization enforcement layer

**Tasks**:
- [ ] Create `@require_permission` decorator
- [ ] Create `@require_ownership` decorator
- [ ] Implement permission checking logic
- [ ] Add role checking utilities
- [ ] Create authorization middleware

**Deliverables**:
- `web/middleware/authorization.py`
- Authorization decorators
- Role/permission utilities

### Phase 3: Endpoint Protection
**Objective**: Apply authorization to all API endpoints

**Tasks**:
- [ ] Audit all API endpoints
- [ ] Apply authorization decorators to each endpoint
- [ ] Verify no unprotected endpoints remain
- [ ] Update service layer with ownership checks
- [ ] Add admin bypass logic

**Deliverables**:
- All endpoints protected
- Service layer authorization

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met
- [ ] Security scan passes
- [ ] Documentation updated
- [ ] ADR for RBAC design created
- [ ] 100% test coverage on authorization

---

## Acceptance Criteria

### Functionality
- [ ] Three roles implemented: Admin, User, Viewer
- [ ] Permission model supports CRUD operations
- [ ] Resource ownership enforced for all user data
- [ ] Admin can access all resources
- [ ] Users can only access own resources
- [ ] Viewers have read-only access

### Testing
- [ ] User cannot access other user's conversations
- [ ] User cannot modify other user's lists
- [ ] Admin can access all resources
- [ ] 100% test coverage on authorization
- [ ] Security scan passes (no auth bypasses)
- [ ] Integration tests for multi-user scenarios

### Quality
- [ ] No performance degradation from auth checks
- [ ] Clear 403 Forbidden messages
- [ ] Audit trail for permission denials
- [ ] No security vulnerabilities

### Documentation
- [ ] ADR documenting RBAC design decisions
- [ ] Updated API documentation with permissions
- [ ] Admin guide for role management

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Role Model | ❌ | [pending] |
| UserRole Table | ❌ | [pending] |
| Owner ID Migration | ❌ | [pending] |
| Permission Decorators | ❌ | [pending] |
| Endpoint Protection | ❌ | [pending] |
| Service Layer Auth | ❌ | [pending] |
| Test Coverage | ❌ | [pending] |
| Security Scan | ❌ | [pending] |

---

## Testing Strategy

### Unit Tests
```python
# Test permission enforcement
async def test_user_cannot_access_other_conversations():
    user1 = create_user()
    user2 = create_user()
    conv = create_conversation(owner=user1)

    # User2 tries to access user1's conversation
    with pytest.raises(PermissionDenied):
        await get_conversation(conv.id, user=user2)

# Test admin bypass
async def test_admin_can_access_any_resource():
    admin = create_user(role="admin")
    user = create_user(role="user")
    conv = create_conversation(owner=user)

    # Admin should succeed
    result = await get_conversation(conv.id, user=admin)
    assert result.id == conv.id
```

### Integration Tests
```python
# Multi-user scenario
async def test_multi_user_isolation():
    # Create multiple users with data
    # Verify complete isolation
    # Test admin access to all
```

### Manual Testing Checklist
**Scenario 1**: User isolation
1. [ ] Create User A with conversations
2. [ ] Create User B
3. [ ] User B cannot see User A's conversations
4. [ ] User B cannot modify User A's data

**Scenario 2**: Admin access
1. [ ] Create admin user
2. [ ] Admin can view all user data
3. [ ] Admin can modify all user data

---

## Success Metrics

### Quantitative
- 0 unauthorized access incidents
- 100% test coverage on auth code
- <10ms overhead for permission checks

### Qualitative
- Clear permission denial messages
- No user confusion about access rights
- Passes security audit

---

## STOP Conditions

**STOP immediately and escalate if**:
- Existing authentication breaks
- Performance overhead >50ms
- Circular dependency in permission checks
- Cannot distinguish user resources
- Admin lockout scenario possible

---

## Effort Estimate

**Overall Size**: Large (20-24 hours)

**Breakdown by Phase**:
- Phase 1 (Schema): 4 hours
- Phase 2 (Middleware): 8 hours
- Phase 3 (Endpoints): 6 hours
- Testing: 4 hours
- Documentation: 2 hours

**Complexity Notes**:
- Must retrofit all existing endpoints
- Careful migration to avoid locking out users
- Performance impact must be minimal

---

## Dependencies

### Required (Must be complete first)
- [ ] JWT Authentication (ADR-012) - ✅ Already complete

### Optional (Nice to have)
- [ ] #358 - Encryption at Rest (can be parallel)
- [ ] Audit logging system

---

## Related Documentation

- **Architecture**: ADR-012 (JWT Authentication), upcoming ADR-XXX (RBAC Design)
- **Code**: `services/domain/models.py`, `web/middleware/`
- **Security**: OWASP Authorization guidelines

---

## Risk Assessment

**Without RBAC**:
- 🚫 Cannot have multiple users
- 🚫 Cannot pass security audit
- 🚫 Data breach liability
- 🚫 Cannot achieve SOC2 compliance
- 🚫 Complete privacy violation

**With RBAC**:
- ✅ Secure multi-user support
- ✅ Pass security audits
- ✅ Enterprise-ready authorization
- ✅ Compliance foundation
- ✅ User data isolation

---

## Implementation Example

```python
# services/domain/models.py
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    permissions = Column(JSON)  # {"resource": ["create", "read", "update", "delete"]}

class UserRole(Base):
    __tablename__ = 'user_roles'
    user_id = Column(Integer, ForeignKey('users.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))

# web/middleware/authorization.py
from functools import wraps

def require_permission(resource: str, action: str):
    """Decorator to enforce permission checks"""
    def decorator(func):
        @wraps(func)
        async def wrapper(request, *args, **kwargs):
            user = request.state.user

            # Check if user has permission
            if not await has_permission(user, resource, action):
                raise HTTPException(403, "Permission denied")

            # Check ownership if not admin
            if user.role != "admin" and resource != "public":
                if not await owns_resource(user, resource, kwargs.get('resource_id')):
                    raise HTTPException(403, "Not owner of resource")

            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

# Usage in endpoints
@app.get("/conversations/{conversation_id}")
@require_permission("conversations", "read")
async def get_conversation(conversation_id: int, request: Request):
    # Implementation
    pass
```

---

**CRITICAL**: This must be completed before any external users access the system

---

_Issue created from synthesis of #323 and #357_
_Priority: P0 - Absolute blocker for multi-user operation_
