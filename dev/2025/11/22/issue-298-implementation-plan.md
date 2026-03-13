# Issue #298 Implementation Plan
**Date**: November 22, 2025, 12:22 PM
**Issue**: AUTH-PASSWORD-CHANGE - Implement Password Change Endpoint + Integration Test
**Effort**: 2-3 hours
**Status**: Planning complete

---

## Current Infrastructure Assessment ✅

**What Already Exists**:
- ✅ `PasswordService` - password hashing & verification (bcrypt, 12 rounds)
- ✅ `TokenBlacklist` - secure token revocation with Redis fallback
- ✅ Auth routes in `web/api/routes/auth.py` (login, logout, /me)
- ✅ Pydantic models in `services/auth/models.py` (LoginRequest, LoginResponse)
- ✅ JWTService for token management
- ✅ Database session management and User model
- ✅ `get_current_user` dependency for authentication checks

**What We Need to Add**:
1. PasswordValidator service (password strength requirements)
2. PasswordChangeRequest Pydantic model
3. PasswordChangeResponse Pydantic model
4. change_password method in auth service
5. /auth/change-password endpoint
6. Integration test
7. API documentation

---

## Implementation Steps (5 Phases)

### Phase 1: Create PasswordValidator Service (30 min)
**File**: `services/auth/password_validator.py` (NEW)

Requirements:
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character

```python
class PasswordValidator:
    MIN_LENGTH = 8
    SPECIAL_CHARS = "!@#$%^&*()"

    @classmethod
    def validate(password: str) -> tuple[bool, Optional[str]]:
        """Returns (is_valid, error_message)"""
        # Validation logic...
```

---

### Phase 2: Create Pydantic Models (15 min)
**File**: `services/auth/models.py` (UPDATE)

Add two models:
```python
class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str

class PasswordChangeResponse(BaseModel):
    success: bool
    message: str
```

---

### Phase 3: Add change_password Service Method (45 min)
**File**: `services/auth/jwt_service.py` (UPDATE)

Logic:
1. Get user by user_id
2. Verify current password using PasswordService.verify_password()
3. Validate new password using PasswordValidator.validate()
4. Hash new password using PasswordService.hash_password()
5. Update user.password_hash in database
6. Blacklist current token using TokenBlacklist.add()
7. Return success response

Dependencies to inject:
- session: AsyncSession
- token_id: str (from JWT token)
- user_id: UUID (from JWT claims)

---

### Phase 4: Create API Endpoint (30 min)
**File**: `web/api/routes/auth.py` (UPDATE)

New endpoint: `POST /auth/change-password`

```python
@router.post("/change-password", response_model=PasswordChangeResponse)
async def change_password(
    request: Request,
    data: PasswordChangeRequest,
    current_user: JWTClaims = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """Change user password and invalidate current token"""
    # Get token ID from JWT
    # Call jwt_service.change_password()
    # Handle errors: 400 (validation), 401 (wrong password)
    # Return success response
```

Error handling:
- `400`: Password validation fails (specific requirement)
- `400`: Passwords don't match
- `401`: Current password incorrect
- `401`: Token invalid/expired

---

### Phase 5: Integration Test (30 min)
**File**: `tests/integration/auth/test_auth_integration.py` (UPDATE)

Test: `test_password_change_invalidates_tokens`

Scenario:
1. Create test user with password "OldPass123!"
2. Login and get token
3. Verify old token works (GET /auth/me)
4. Change password to "NewPass456!"
5. Verify old token now fails (401)
6. Verify new password enables login
7. Verify new token works

---

## Execution Order

1. **Phase 1**: Create PasswordValidator (30 min)
2. **Phase 2**: Create Pydantic models (15 min)
3. **Phase 3**: Add service method (45 min)
4. **Phase 4**: Create endpoint (30 min)
5. **Phase 5**: Write test (30 min)

**Total**: ~2.5 hours

---

## Key Implementation Details

### PasswordValidator Design
- Static methods, no state
- Returns tuple: (is_valid, error_message)
- Error messages specific (not generic "invalid password")
- Can be unit tested independently

### Security Considerations
- ✅ Bcrypt handles timing-safe comparison (no timing attacks)
- ✅ Generic error messages at API level (prevent user enumeration)
- ✅ Token invalidation immediate (no delayed revocation)
- ✅ Current password verification required
- ✅ Password hashing with 12 rounds (OWASP standard)

### Token Invalidation Flow
1. User submits old password + new password
2. Verify old password is correct
3. If valid: change password in DB
4. Then: add current token to blacklist
5. User must login again with new password

**Important**: User is logged out after password change (intentional)

### Testing Strategy
- Integration test only (not unit tests)
- Tests real database and auth flow
- Uses test database with rollback
- No mocking of auth services

---

## Files to Modify

| File | Action | Details |
|------|--------|---------|
| `services/auth/password_validator.py` | CREATE | New password validation service |
| `services/auth/models.py` | UPDATE | Add PasswordChangeRequest, PasswordChangeResponse |
| `services/auth/jwt_service.py` | UPDATE | Add change_password method |
| `web/api/routes/auth.py` | UPDATE | Add /auth/change-password endpoint |
| `tests/integration/auth/test_auth_integration.py` | UPDATE | Add integration test |
| `docs/api/auth-api.md` | UPDATE | Document new endpoint |

---

## Dependencies & Order

No circular dependencies. Can implement in this order:
1. PasswordValidator (standalone)
2. Pydantic models (standalone)
3. Service method (depends on 1, 2)
4. Endpoint (depends on 3)
5. Test (depends on 4)

---

## Success Criteria

- [ ] PasswordValidator created with all requirements
- [ ] Pydantic models added
- [ ] change_password method works (verified in logs)
- [ ] Endpoint returns 200 on success
- [ ] Endpoint returns 400 on validation failure
- [ ] Endpoint returns 401 on wrong password
- [ ] Old token blocked after change
- [ ] New password works for login
- [ ] Integration test passes
- [ ] All pre-commit hooks pass

---

## Estimated Time

- Planning: ✅ Complete
- Phase 1: 30 min
- Phase 2: 15 min
- Phase 3: 45 min
- Phase 4: 30 min
- Phase 5: 30 min
- **Total**: ~2.5 hours

---

## Risk Assessment

**Low Risk**:
- All infrastructure exists
- Clear requirements in issue
- Simple linear flow
- No complex dependencies

**Potential Gotchas**:
- JWT token format (extracting token_id/JTI from token)
- Database session management (same pattern as login)
- Timing of token blacklist (must be after password update)

---

**Ready to implement?** Start with Phase 1 (PasswordValidator)
