# Issue: Implement Web UI Authentication and Session Management

**Priority**: HIGH
**Milestone**: MVP (Blocks Multi-User Deployment)
**Labels**: `security`, `authentication`, `web-ui`, `mvp-blocker`, `multi-user`
**Estimated Effort**: 8-12 hours

---

## Problem

The current web UI has **no authentication mechanism**, making it suitable only for:
- ✅ Alpha testers on their own laptops
- ✅ Local development with single repository
- ❌ Any deployment with multiple users
- ❌ Shared backend services
- ❌ Production environments

**Current Risks**:
- Any user can access any session
- No user identity verification
- Sessions not isolated by user
- Data privacy concerns
- Security vulnerabilities

**When This Blocks**:
- ✅ Alpha testing (local repos): No blocker
- ❌ MVP deployment (shared backend): Critical blocker
- ❌ Production (multi-user): Security issue

---

## Current State

**Web UI** (`web/app.py`):
```python
@app.post("/chat")
async def chat_endpoint(request: Request):
    # NO authentication check
    # NO user verification
    # Anyone can send messages

    data = await request.json()
    message = data.get("message", "")
    session_id = data.get("session_id", "default_session")  # Predictable!

    # Process message...
```

**Problems**:
1. No login/logout mechanism
2. No user identity attached to sessions
3. Predictable session IDs (can be guessed)
4. No session isolation between users
5. No access control

---

## Requirements

### 1. User Authentication

**Must Have**:
- [ ] Login page/flow
- [ ] User credential verification
- [ ] Session token generation
- [ ] Token validation on each request
- [ ] Logout functionality
- [ ] Session expiration

**Nice to Have**:
- Password reset flow
- Remember me option
- OAuth integration (GitHub, Google)
- Multi-factor authentication

---

### 2. Session Management

**Must Have**:
- [ ] User-specific session IDs (not guessable)
- [ ] Session isolation (user A can't access user B's sessions)
- [ ] Session persistence across page refreshes
- [ ] Secure session storage (httpOnly cookies)
- [ ] Session cleanup on logout

**Nice to Have**:
- Multiple concurrent sessions per user
- Session activity tracking
- Session history/management UI

---

### 3. User Database Integration

**Must Have**:
- [ ] Link web sessions to user records
- [ ] Use existing `users` table (already has auth fields)
- [ ] Store session tokens securely
- [ ] Track last login
- [ ] User activity logging

**Schema** (Already Exists):
```sql
-- Table: users (already in database)
id              varchar(255) PRIMARY KEY
username        varchar(255) UNIQUE NOT NULL
email           varchar(255) UNIQUE NOT NULL
password_hash   varchar(500)
is_active       boolean DEFAULT true
is_verified     boolean DEFAULT false
created_at      timestamp DEFAULT now()
updated_at      timestamp DEFAULT now()
last_login_at   timestamp
role            varchar(50) DEFAULT 'user'  -- Added in A7
```

---

### 4. API Security

**Must Have**:
- [ ] Require authentication token on all endpoints
- [ ] Validate token on each request
- [ ] Return 401 for unauthenticated requests
- [ ] Rate limiting per user
- [ ] CSRF protection

**Nice to Have**:
- API key support (for CLI/integrations)
- JWT tokens
- Token refresh mechanism
- IP-based restrictions

---

## Implementation Approaches

### Option 1: Simple Session-Based Auth (Recommended for MVP)

**Pros**:
- Simple to implement
- Works with existing tech stack
- Good for web UI
- Fast development time

**Cons**:
- Requires server-side session storage
- Not suitable for distributed systems (yet)
- Requires sticky sessions for load balancing

**Implementation**:
```python
# web/auth.py (NEW FILE)
from fastapi import Depends, HTTPException, Cookie
from services.user.user_service import UserService

async def get_current_user(session_token: str = Cookie(None)):
    """Dependency to get current authenticated user"""
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = await UserService.get_user_by_session(session_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    return user

# web/app.py - Protect endpoints
@app.post("/chat")
async def chat_endpoint(
    request: Request,
    current_user: User = Depends(get_current_user)  # Require auth
):
    data = await request.json()
    message = data.get("message", "")

    # Use user-specific session ID
    session_id = f"{current_user.id}_{uuid.uuid4()}"

    # Process with user context
    result = await intent_service.process_intent(
        message,
        session_id=session_id,
        user_id=current_user.id  # Track user
    )
```

**Timeline**: 8 hours
- 2 hours: Auth endpoints (login, logout)
- 2 hours: Session management
- 2 hours: Protect existing endpoints
- 2 hours: Testing and polish

---

### Option 2: JWT Token-Based Auth

**Pros**:
- Stateless (no server session storage)
- Works with distributed systems
- Industry standard
- Suitable for API and web UI

**Cons**:
- More complex to implement
- Token management complexity
- Refresh token handling
- Longer development time

**Timeline**: 12 hours
- 3 hours: JWT implementation
- 2 hours: Login/logout endpoints
- 3 hours: Token validation middleware
- 2 hours: Refresh token logic
- 2 hours: Testing

---

### Option 3: OAuth Integration (Future Enhancement)

**Pros**:
- No password management
- Trusted providers (GitHub, Google)
- Better UX (one-click login)

**Cons**:
- Requires external dependencies
- More complex setup
- Not suitable for MVP

**Recommendation**: Phase 2 enhancement after MVP

---

## Recommended Approach for MVP: Option 1 (Session-Based)

**Why**:
- Fastest to implement (8 hours)
- Sufficient for MVP with single server
- Uses existing infrastructure
- Clear upgrade path to JWT later
- Blocks Alpha → MVP transition soonest

---

## Implementation Plan

### Phase 1: Auth Infrastructure (2 hours)

**Create**:
- `web/auth.py` - Authentication utilities
- `services/user/session_service.py` - Session management
- Database: `user_sessions` table (or use existing token_blacklist)

**Add**:
- Login endpoint: `POST /auth/login`
- Logout endpoint: `POST /auth/logout`
- Session validation dependency: `get_current_user()`

---

### Phase 2: Protect Endpoints (2 hours)

**Update**:
- `/chat` - Require authentication
- `/status` - Require authentication (or make public?)
- `/history` - Require authentication
- All API endpoints - Add auth dependency

**Add**:
- 401 error responses
- Login redirect for web UI
- Token validation on each request

---

### Phase 3: Web UI Updates (2 hours)

**Create**:
- Login page (`web/static/login.html`)
- Login form with username/password
- Session cookie management
- Redirect to login when unauthenticated

**Update**:
- Main chat UI to check authentication
- Store session token in cookie
- Handle 401 responses (redirect to login)
- Add logout button

---

### Phase 4: Testing & Polish (2 hours)

**Test**:
- [ ] Login with valid credentials → success
- [ ] Login with invalid credentials → error
- [ ] Access chat without login → redirect
- [ ] Logout clears session
- [ ] Session persists across page refresh
- [ ] Multiple users can't access each other's sessions

**Polish**:
- Error messages
- Loading states
- Session expiration handling
- Remember me option (nice to have)

---

## Testing Requirements

### Unit Tests
- [ ] Session creation
- [ ] Session validation
- [ ] Session expiration
- [ ] User authentication
- [ ] Password verification

### Integration Tests
- [ ] Login flow (end-to-end)
- [ ] Protected endpoint access
- [ ] Logout flow
- [ ] Session persistence
- [ ] Cross-user isolation

### Security Tests
- [ ] Cannot guess session tokens
- [ ] Cannot access other users' sessions
- [ ] Expired sessions rejected
- [ ] Invalid tokens rejected
- [ ] Password hashing verified

### Manual Testing
- [ ] Complete login/logout cycle
- [ ] Session persists across browser tabs
- [ ] Session expires after timeout
- [ ] Multiple users simultaneously
- [ ] Cannot access chat without login

---

## Acceptance Criteria

- [ ] Login page implemented
- [ ] User credentials verified against database
- [ ] Session tokens generated securely
- [ ] All API endpoints require authentication
- [ ] Sessions isolated by user
- [ ] Logout clears session
- [ ] Session persists across page refreshes
- [ ] 401 responses trigger login redirect
- [ ] All tests pass
- [ ] Manual testing confirms multi-user isolation
- [ ] No security vulnerabilities in auth flow

---

## Security Considerations

### Must Address:
- [ ] Password hashing (bcrypt/argon2)
- [ ] Secure session token generation (cryptographically random)
- [ ] HttpOnly cookies (prevent XSS)
- [ ] HTTPS enforcement (production)
- [ ] CSRF protection
- [ ] Rate limiting (login attempts)
- [ ] Session expiration
- [ ] Secure token storage

### Nice to Have:
- Password complexity requirements
- Account lockout after failed attempts
- Audit logging
- IP tracking
- Session activity monitoring

---

## Migration Path

### Current (Alpha):
- Single user per local repo
- No authentication needed
- Works as-is

### MVP (This Issue):
- Multiple users on shared backend
- Session-based authentication
- User isolation enforced

### Future (Post-MVP):
- JWT tokens for distributed systems
- OAuth integration
- SSO support
- Advanced session management

---

## Related Issues

- #228: User model implementation (COMPLETED - A7)
- #227: Token blacklist (COMPLETED - A7)
- #249: Audit logging (COMPLETED - A7)
- #XXX: Rate limiting per user (future)
- #XXX: OAuth integration (future)

---

## References

- **Database Schema**: Users table exists (`services/user/models.py`)
- **Auth Service**: `services/user/auth_service.py` (may exist)
- **Session Management**: Need to implement
- **Security Best Practices**: OWASP Authentication Cheat Sheet

---

## Notes

**Why This is MVP Blocker**:
- Cannot deploy shared backend without authentication
- Security risk for production
- Required for multi-user scenarios

**Why Not Alpha Blocker**:
- Alpha testers use local repos
- Single user per instance
- No shared backend yet

**Recommended Timeline**:
- Start: After Phase 2 testing complete
- Complete: Before MVP release
- Estimated: 8 hours for session-based auth

---

**Created**: October 27, 2025, 12:30 PM
**Reporter**: Lead Developer (Sonnet 4.5)
**Priority**: MVP blocker (not Alpha blocker)
