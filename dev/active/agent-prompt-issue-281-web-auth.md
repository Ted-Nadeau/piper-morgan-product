# Claude Code Prompt: CORE-ALPHA-WEB-AUTH (#281) - Option B

**Date**: November 1, 2025, 7:00 AM PT
**Mission**: Implement alpha-ready authentication (bcrypt + JWT, defer email)
**Effort**: Medium (6-8 hours) - Option B approach
**GitHub Issue**: #281

---

## Your Identity

You are Claude Code, implementing authentication infrastructure for multi-user alpha testing. Follow systematic methodology and provide evidence at each checkpoint.

---

## CRITICAL CONTEXT: Option B Approach

**PM has chosen Option B - Alpha-Ready Auth**:

**Included** ✅:
- Bcrypt password hashing
- JWT token generation/validation
- Login/logout endpoints
- Auth middleware
- Session management
- Admin password setup script

**Deferred to MVP** ⏭️:
- Password reset flow
- Email service integration
- "Forgot password" feature

**Rationale**: Alpha testers (5-10 people) are trusted. Manual password assistance acceptable. Email system can wait until MVP.

---

## CRITICAL FIRST ACTION: Use Serena MCP

**Verify infrastructure with Serena**:

```python
# Check alpha_users table
serena.find_symbol("AlphaUser")
serena.find_symbol("password_hash")

# Look for any existing auth code
serena.find_symbol("JWT")
serena.find_symbol("authenticate")
serena.find_referencing_symbols("password")

# Check if dependencies exist
# (look for bcrypt or jwt imports)
```

**Report findings** before starting implementation.

---

## Cathedral Context

**Read this gameplan section for FULL implementation details**:
- `/mnt/user-data/uploads/gameplan-p0-alpha-blockers-v2.md` (Issue #3 section)

This prompt is a condensed execution guide. The gameplan has complete code examples.

---

## Mission

Implement complete authentication system with bcrypt password hashing, JWT tokens, login/logout endpoints, auth middleware, and admin password management - WITHOUT email/password reset (deferred to MVP).

---

## Phase -1: Verify Infrastructure (20 minutes)

**Critical Questions**:

1. **Does alpha_users.password_hash field exist?**
   ```python
   serena.find_symbol("AlphaUser")
   # Look for password_hash field
   ```

2. **Is bcrypt installed?**
   ```bash
   pip list | grep bcrypt
   ```

3. **Any existing auth code to build on?**
   ```python
   serena.find_symbol("JWT")
   serena.list_dir("services/auth")
   ```

**Report findings with evidence**. If infrastructure doesn't match expectations, STOP and report.

---

## Implementation Checkpoints

### Checkpoint 1: Dependencies (15 minutes)

**Add to requirements.txt**:
```
bcrypt==4.1.1
pyjwt==2.8.0
python-multipart==0.0.6
```

**Install**:
```bash
pip install bcrypt pyjwt python-multipart --break-system-packages
```

**Verify**:
```bash
python -c "import bcrypt; print('bcrypt OK')"
python -c "import jwt; print('jwt OK')"
```

**Evidence**: Show installation output and verification.

---

### Checkpoint 2: Password Service (1 hour)

**Create `services/auth/password_service.py`**:

```python
"""Password hashing and verification using bcrypt."""
import bcrypt

class PasswordService:
    """Handles password hashing and verification"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password with bcrypt (12 rounds)"""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed.encode('utf-8')
            )
        except Exception:
            return False

    @staticmethod
    def generate_temp_password(length: int = 16) -> str:
        """Generate secure temporary password"""
        import secrets
        import string
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
        return ''.join(secrets.choice(alphabet) for _ in range(length))

# Test if run directly
if __name__ == "__main__":
    ps = PasswordService()
    password = "test_password_123"
    hashed = ps.hash_password(password)
    print(f"Hash: {hashed}")
    print(f"Verify correct: {ps.verify_password(password, hashed)}")
    print(f"Verify wrong: {ps.verify_password('wrong', hashed)}")
```

**Test**:
```bash
python services/auth/password_service.py
```

**Evidence**: Show test output proving hash/verify works.

---

### Checkpoint 3: JWT Service (1 hour)

**Create `services/auth/jwt_service.py`**:

```python
"""JWT token generation and validation."""
import jwt
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class JWTService:
    """Handles JWT token generation/validation"""

    def __init__(self):
        self.secret_key = os.getenv(
            'JWT_SECRET_KEY',
            'alpha-jwt-secret-CHANGE-IN-PRODUCTION'
        )
        self.algorithm = 'HS256'
        self.expire_hours = 24  # 24 hours for alpha

    def generate_token(
        self,
        user_id: str,
        username: str
    ) -> str:
        """Generate JWT access token"""
        expire = datetime.utcnow() + timedelta(hours=self.expire_hours)

        payload = {
            'user_id': user_id,
            'username': username,
            'exp': expire,
            'iat': datetime.utcnow(),
            'type': 'access'
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate token and return payload"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

# Test if run directly
if __name__ == "__main__":
    jwt_svc = JWTService()
    token = jwt_svc.generate_token("user-123", "test")
    print(f"Token: {token}")
    payload = jwt_svc.validate_token(token)
    print(f"Payload: {payload}")
```

**Test**:
```bash
python services/auth/jwt_service.py
```

**Evidence**: Show token generation and validation working.

---

### Checkpoint 4: Auth Endpoints (1.5 hours)

**Create `web/routes/auth.py`**:

See gameplan for complete implementation. Key endpoints:

1. `POST /auth/login` - Authenticate user, return JWT
2. `POST /auth/logout` - Clear auth cookie
3. `GET /auth/me` - Get current user info

**Register in `web/app.py`**:
```python
from web.routes.auth import router as auth_router
app.include_router(auth_router)
```

**Test**:
```bash
# Test login (after setting password - see Checkpoint 6)
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test_password"}'

# Should return: {"token": "...", "user_id": "...", ...}
```

**Evidence**: Show endpoint registration and curl test output.

---

### Checkpoint 5: Auth Middleware (1 hour)

**Create `web/middleware/auth.py`**:

```python
"""Authentication middleware for protected endpoints."""
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any

from services.auth.jwt_service import JWTService

jwt_service = JWTService()
security = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """Get current authenticated user from token"""
    token = None

    # Try Authorization header
    if credentials:
        token = credentials.credentials

    # Try cookie
    if not token:
        token = request.cookies.get("auth_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Validate
    payload = jwt_service.validate_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload

async def require_auth(
    current_user: Dict = Depends(get_current_user)
) -> Dict:
    """Require authentication - use as dependency"""
    return current_user
```

**Protect existing endpoints in `web/app.py`**:
```python
from web.middleware.auth import require_auth

@app.post("/chat")
async def chat_endpoint(
    request: Request,
    current_user: Dict = Depends(require_auth)  # ← ADD THIS
):
    data = await request.json()
    message = data.get("message", "")

    # Use user context
    user_id = current_user['user_id']
    session_id = f"{user_id}:{data.get('session_id', 'default')}"

    result = await intent_service.process_intent(
        message,
        session_id,
        user_id=user_id
    )
    return {"response": result.message}
```

**Evidence**: Show middleware created and endpoints protected.

---

### Checkpoint 6: Admin Password Script (45 minutes)

**Create `scripts/setup_alpha_passwords.py`**:

```python
"""Admin script to set passwords for alpha users."""
import asyncio
import argparse
from sqlalchemy import select

# Adapt imports based on your structure
from database import get_db_session
from models.user import AlphaUser
from services.auth.password_service import PasswordService

ps = PasswordService()

async def set_user_password(username: str, password: str = None):
    """Set password for specific user"""
    async with get_db_session() as db:
        result = await db.execute(
            select(AlphaUser).where(AlphaUser.username == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            print(f"❌ User '{username}' not found")
            return False

        # Generate if not provided
        if not password:
            password = ps.generate_temp_password()
            print(f"Generated password: {password}")

        # Hash and store
        hashed = ps.hash_password(password)
        user.password_hash = hashed
        await db.commit()

        print(f"✅ Password set for '{username}' (ID: {user.id})")
        return True

async def set_all_passwords():
    """Set passwords for all users without passwords"""
    async with get_db_session() as db:
        result = await db.execute(
            select(AlphaUser).where(
                (AlphaUser.password_hash == None) |
                (AlphaUser.password_hash == '')
            )
        )
        users = result.scalars().all()

        if not users:
            print("✅ All users have passwords")
            return

        print(f"Found {len(users)} users without passwords:\n")

        for user in users:
            password = ps.generate_temp_password()
            hashed = ps.hash_password(password)
            user.password_hash = hashed
            print(f"  {user.username}: {password}")

        await db.commit()
        print("\n✅ Passwords set. SAVE THESE CREDENTIALS!")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('username', nargs='?', help='Username')
    parser.add_argument('--all', action='store_true', help='Set all passwords')
    parser.add_argument('--password', help='Specific password')

    args = parser.parse_args()

    if args.all:
        await set_all_passwords()
    elif args.username:
        await set_user_password(args.username, args.password)
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())
```

**Test**:
```bash
# Set password for xian
python scripts/setup_alpha_passwords.py xian --password "test123"

# Or set passwords for all users
python scripts/setup_alpha_passwords.py --all
```

**Evidence**: Show script output setting passwords successfully.

---

### Checkpoint 7: Login UI (1 hour)

**Create `web/static/login.html`** - see gameplan for complete HTML/CSS/JS.

Key features:
- Clean, professional login form
- Username/password inputs
- Error message display
- JWT token storage in localStorage
- Redirect to main app after login
- Check if already logged in

**Update `web/app.py`** to serve login:
```python
from fastapi.responses import FileResponse, RedirectResponse

@app.get("/login")
async def login_page():
    return FileResponse("web/static/login.html")

@app.get("/")
async def root(auth_token: str = Cookie(None)):
    """Redirect to login if not authenticated"""
    if not auth_token:
        return RedirectResponse(url="/login")

    # Validate token
    from services.auth.jwt_service import JWTService
    jwt_svc = JWTService()
    payload = jwt_svc.validate_token(auth_token)

    if not payload:
        return RedirectResponse(url="/login")

    return FileResponse("web/static/index.html")
```

**Evidence**: Show login page created and routing configured.

---

## Testing & Verification (1 hour)

### Test 1: Password Hashing
```python
python -c "
from services.auth.password_service import PasswordService
ps = PasswordService()
h = ps.hash_password('test123')
print('Hash:', h)
print('Valid:', ps.verify_password('test123', h))
print('Invalid:', ps.verify_password('wrong', h))
"
# Expected: Hash string, True, False
```

### Test 2: JWT Tokens
```python
python -c "
from services.auth.jwt_service import JWTService
js = JWTService()
token = js.generate_token('user-1', 'test')
print('Token:', token[:50] + '...')
payload = js.validate_token(token)
print('Valid:', payload is not None)
print('User:', payload.get('username'))
"
# Expected: Token string, True, 'test'
```

### Test 3: Login Endpoint
```bash
# Set password first
python scripts/setup_alpha_passwords.py xian --password "test123"

# Test login
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "test123"}'

# Expected: {"token": "...", "user_id": "...", "username": "xian"}
```

### Test 4: Protected Endpoint
```bash
# Without auth (should fail)
curl http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
# Expected: 401 Not authenticated

# With auth (should work)
TOKEN="[paste token from Test 3]"
curl http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "hello"}'
# Expected: Success response
```

### Test 5: Web UI Login
```
1. Open browser to http://localhost:8001
2. Should redirect to /login
3. Enter username: xian
4. Enter password: test123
5. Click Sign In
6. Should redirect to main app (/)
7. Check console for auth_token in localStorage
8. Navigate to /login again - should redirect to /
```

### Test 6: Multi-User Isolation
```
1. Login as xian in Chrome
2. Login as another user in Incognito
3. Send messages as both
4. Verify sessions are separate
5. Logout from one - other should stay logged in
```

---

## Success Criteria

**Verify ALL before claiming complete**:
- [ ] bcrypt installed and working
- [ ] pyjwt installed and working
- [ ] Password service hashes/verifies correctly
- [ ] JWT service generates/validates tokens
- [ ] Login endpoint works
- [ ] Logout endpoint clears cookies
- [ ] Auth middleware protects endpoints
- [ ] Admin script sets passwords
- [ ] Login UI functional
- [ ] Multi-user sessions isolated
- [ ] All tests pass
- [ ] No passwords in logs or errors
- [ ] Changes committed to git

---

## Evidence Format

**Provide complete proof**:

1. **Files Created/Modified**:
   ```
   services/auth/password_service.py: Created (X lines)
   services/auth/jwt_service.py: Created (Y lines)
   web/routes/auth.py: Created (Z lines)
   web/middleware/auth.py: Created (A lines)
   scripts/setup_alpha_passwords.py: Created (B lines)
   web/static/login.html: Created (C lines)
   web/app.py: Modified (+D lines for routing)
   requirements.txt: Modified (+3 lines)
   ```

2. **All Test Outputs**:
   - All 6 tests with full terminal output
   - Screenshots optional but appreciated

3. **Git Status**:
   ```bash
   git status
   git log --oneline -5
   git diff --stat main
   ```

4. **Security Verification**:
   ```bash
   # Verify no passwords in code
   grep -r "password.*=.*['\"]" services/ web/ --include="*.py"
   # Expected: Only PasswordService methods, no hardcoded passwords
   ```

---

## Security Checklist

Before claiming complete, verify:
- [ ] Passwords hashed with bcrypt (12+ rounds)
- [ ] JWT secret key from environment variable
- [ ] No passwords hardcoded anywhere
- [ ] No tokens logged
- [ ] HTTP-only cookies for web UI
- [ ] Authorization header support for API
- [ ] Token expiration working (24h)
- [ ] Failed login doesn't leak user existence
- [ ] Rate limiting (nice-to-have, optional for alpha)

---

## Time Lord Reminder

This is 6-8 hours of solid work. Don't rush. Each checkpoint should be fully working before moving to next.

If you hit issues or unknowns, STOP and report. Don't guess.

Take breaks between checkpoints. Fresh eyes catch bugs.

---

## Questions for PM (if needed)

- If alpha_users structure is different than expected
- If database session management is different
- If there's existing auth code that conflicts
- If JWT secret should be set differently
- If session timeout should be different

**Always ask rather than assume!**

---

## What's Deferred (NOT in scope)

Remember, you're NOT implementing:
- ❌ Password reset flow
- ❌ Email service
- ❌ "Forgot password" UI
- ❌ OAuth (Google, GitHub)
- ❌ Two-factor authentication

Those are MVP features. For alpha, manual password assistance is fine.

---

Good luck! This is the biggest piece, but it's well-scoped and you have complete examples in the gameplan. Take it checkpoint by checkpoint and you'll get there! 🔐🏰
