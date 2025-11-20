# SEC-323: Implement RBAC (Role-Based Access Control)
**Priority**: P0 (CRITICAL - Security showstopper)
**Labels**: `security`, `blocker`, `mvp-required`, `multi-user`
**Effort**: 20-24 hours
**Discovered by**: Ted Nadeau (architectural review)

---

## Problem

**CRITICAL SECURITY GAP**: Any authenticated user can access ANY resource. No authorization checks exist.

**Current state**:
- JWT authentication works (who you are)
- NO authorization (what you can do)
- User A can read User B's conversations
- User A can delete User B's data
- No admin vs user distinction

**This blocks**:
- Multi-user testing
- Alpha launch with external users
- Any production deployment
- Security audit
- Compliance certification

## Solution

Implement proper RBAC with:
1. Role model (admin, user, viewer)
2. Permission model (read, write, delete)
3. Resource ownership checks
4. Authorization decorators/middleware
5. Comprehensive test coverage

## Acceptance Criteria

### Core Implementation
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

## Implementation Design

```python
# models/auth/role.py
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)  # admin, user, viewer
    permissions = relationship('Permission', secondary='role_permissions')

# models/auth/permission.py
class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    resource = Column(String(50))  # conversation, list, pattern
    action = Column(String(50))    # create, read, update, delete

# decorators/auth.py
def require_permission(resource: str, action: str):
    """Check if user has permission for resource + action"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = get_current_user()
            if not has_permission(user, resource, action):
                raise HTTPException(403, "Permission denied")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def require_ownership(resource_param: str = 'id'):
    """Check if user owns the resource"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = get_current_user()
            resource_id = kwargs.get(resource_param)
            if not owns_resource(user, resource_id):
                raise HTTPException(403, "Not resource owner")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage example
@router.get("/conversations/{id}")
@require_permission("conversation", "read")
@require_ownership("id")
async def get_conversation(id: int):
    # User can only access their own conversations
    pass
```

## Migration Strategy

```sql
-- 1. Add owner_id to resource tables
ALTER TABLE conversations ADD COLUMN owner_id INTEGER REFERENCES users(id);
ALTER TABLE lists ADD COLUMN owner_id INTEGER REFERENCES users(id);
ALTER TABLE uploaded_files ADD COLUMN owner_id INTEGER REFERENCES users(id);

-- 2. Backfill with first/only user (for alpha)
UPDATE conversations SET owner_id = (SELECT id FROM users LIMIT 1);

-- 3. Make owner_id NOT NULL after backfill
ALTER TABLE conversations ALTER COLUMN owner_id SET NOT NULL;
```

## Security Testing

```python
# tests/test_rbac.py
async def test_user_cannot_access_other_user_conversation():
    user1 = create_test_user("user1")
    user2 = create_test_user("user2")
    conv = create_conversation(owner=user1)

    # User2 tries to access User1's conversation
    response = client.get(
        f"/conversations/{conv.id}",
        headers={"Authorization": f"Bearer {user2.token}"}
    )
    assert response.status_code == 403
    assert "Not resource owner" in response.json()["detail"]

async def test_admin_can_access_any_conversation():
    admin = create_test_user("admin", role="admin")
    user = create_test_user("user")
    conv = create_conversation(owner=user)

    # Admin accesses user's conversation
    response = client.get(
        f"/conversations/{conv.id}",
        headers={"Authorization": f"Bearer {admin.token}"}
    )
    assert response.status_code == 200
```

## Rollout Plan

1. **Phase 1**: Implement models and migrations (4 hours)
2. **Phase 2**: Create authorization decorators (4 hours)
3. **Phase 3**: Apply to all endpoints (8 hours)
4. **Phase 4**: Comprehensive testing (4 hours)
5. **Phase 5**: Security audit and fixes (4 hours)

## Risk Assessment

**Without this**:
- 🚫 Cannot have multiple users
- 🚫 Cannot pass security audit
- 🚫 Data breach liability
- 🚫 Cannot achieve SOC2 compliance

**With this**:
- ✅ Secure multi-user support
- ✅ Pass security audits
- ✅ Enterprise-ready authorization
- ✅ Compliance foundation

---

*CRITICAL: This must be completed before any external users access the system*
