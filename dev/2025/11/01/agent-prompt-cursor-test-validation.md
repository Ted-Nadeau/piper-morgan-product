# Cursor Agent Prompt: Test Scaffold & Cross-Validation - P0 Blockers

**Date**: November 1, 2025, 7:16 AM PT
**Mission**: Create test scaffolds and cross-validate Code agent's implementations
**Role**: Test Engineer & Independent Verifier
**Duration**: Parallel with Code's work + validation checkpoints

---

## Your Identity

You are Cursor Agent, serving as test engineer and independent verifier for the P0 Alpha Blockers sprint. Your job is to create test infrastructure BEFORE implementation exists, then rigorously verify Code's work after each issue.

---

## Cathedral Context

**Sprint Overview**: Three P0 blockers preventing external alpha testing:
1. Issue #280: CORE-ALPHA-DATA-LEAK (2-3h)
2. Issue #282: CORE-ALPHA-FILE-UPLOAD (2-4h)
3. Issue #281: CORE-ALPHA-WEB-AUTH (6-8h)

**Code Agent**: Implementing the features
**Your Role**: Verify quality, security, completeness

**Read for context**:
- `/dev/active/gameplan-p0-alpha-blockers-v2.md` (full sprint plan)
- `/dev/active/uploads/email-service-research-mvp.md` (future work context)

---

## Mission

Create test scaffolds for all three issues to define success criteria, then independently verify Code's implementations with focus on security, edge cases, and the "anti-80%" completion standard.

---

## Phase 1: Test Scaffold Creation (1 hour)

**Objective**: Create test files that define what "done" looks like for each issue.

### Scaffold 1: Data Isolation Tests

**Create `tests/config/test_data_isolation.py`**:

```python
"""
Test suite for Issue #280: CORE-ALPHA-DATA-LEAK
Verify personal data isolation between users
"""
import pytest
from services.config.config_service import ConfigService

class TestDataIsolation:
    """Verify PIPER.md has no personal data and user data is isolated"""

    @pytest.mark.asyncio
    async def test_piper_md_has_no_personal_data(self):
        """
        Verify PIPER.md contains zero personal/company information.

        Success Criteria:
        - No mentions of: Q4, VA, DRAGONS, Kind Systems, Christian, xian
        - Only generic capabilities and personality
        - No specific project names or team structures
        """
        # TODO: Read PIPER.md
        # TODO: Check for personal data patterns
        # TODO: Assert no matches found
        pass

    @pytest.mark.asyncio
    async def test_xian_personal_data_in_database(self, db_session):
        """
        Verify xian's personal data moved to alpha_users.preferences.

        Success Criteria:
        - User 'xian' exists in alpha_users
        - preferences field is populated
        - Contains projects, q4_goals, team info
        """
        # TODO: Query alpha_users for xian
        # TODO: Verify preferences field exists
        # TODO: Assert expected keys present
        pass

    @pytest.mark.asyncio
    async def test_config_service_generic_load(self, db_session):
        """
        Verify ConfigService returns only generic config when no user_id.

        Success Criteria:
        - load_config() with no user_id returns generic only
        - No personal data in generic config
        """
        # TODO: Call ConfigService.load_config()
        # TODO: Verify only generic capabilities
        pass

    @pytest.mark.asyncio
    async def test_config_service_user_overlay(self, db_session):
        """
        Verify ConfigService merges user preferences over base config.

        Success Criteria:
        - load_config(user_id) includes user's personal data
        - Generic config preserved
        - User data overlays correctly
        """
        # TODO: Get xian's user_id
        # TODO: Call load_config(user_id)
        # TODO: Verify personal data present
        # TODO: Verify generic config still there
        pass

    @pytest.mark.asyncio
    async def test_multi_user_isolation(self, db_session):
        """
        Verify different users get different configs.

        Success Criteria:
        - User A's config has User A's data only
        - User B's config has User B's data only
        - No data leakage between users
        """
        # TODO: Create test user A and B
        # TODO: Load configs for both
        # TODO: Assert no overlap in personal data
        pass
```

### Scaffold 2: File Upload Tests

**Create `tests/web/test_file_upload.py`**:

```python
"""
Test suite for Issue #282: CORE-ALPHA-FILE-UPLOAD
Verify file upload security and functionality
"""
import pytest
from fastapi.testclient import TestClient

class TestFileUpload:
    """Verify file upload works with proper security"""

    def test_upload_requires_authentication(self, client: TestClient):
        """
        Verify upload endpoint requires authentication.

        Success Criteria:
        - Upload without token returns 401
        - Upload with invalid token returns 401
        """
        # TODO: Attempt upload without auth
        # TODO: Assert 401 status
        pass

    def test_upload_text_file_success(self, authenticated_client: TestClient):
        """
        Verify text file uploads successfully.

        Success Criteria:
        - Returns 200 with file_id
        - File saved in user's directory
        - Metadata stored in database
        """
        # TODO: Create test.txt
        # TODO: Upload file
        # TODO: Verify response
        # TODO: Verify file on disk
        pass

    def test_upload_file_size_limit(self, authenticated_client: TestClient):
        """
        Verify file size limit enforced (10MB).

        Success Criteria:
        - Files <= 10MB accepted
        - Files > 10MB rejected with 413
        """
        # TODO: Create 11MB file
        # TODO: Attempt upload
        # TODO: Assert 413 status
        # TODO: Verify error message
        pass

    def test_upload_file_type_validation(self, authenticated_client: TestClient):
        """
        Verify only allowed file types accepted.

        Success Criteria:
        - .txt, .pdf, .docx, .md, .json accepted
        - .exe, .sh, .dll rejected with 415
        """
        # TODO: Create test.sh file
        # TODO: Attempt upload
        # TODO: Assert 415 status
        pass

    def test_upload_user_isolation(self, db_session):
        """
        Verify files stored in user-isolated directories.

        Success Criteria:
        - User A's files in uploads/user_a/
        - User B's files in uploads/user_b/
        - User A cannot access User B's files
        """
        # TODO: Create two users
        # TODO: Upload files as each
        # TODO: Verify directory isolation
        pass

    def test_upload_special_characters_filename(self, authenticated_client):
        """
        Verify filenames with special characters handled safely.

        Success Criteria:
        - Filenames sanitized or rejected
        - No path traversal possible
        - Files saved with safe names
        """
        # TODO: Create file with ../../../etc/passwd name
        # TODO: Attempt upload
        # TODO: Verify no path traversal
        pass
```

### Scaffold 3: Password Service Tests

**Create `tests/auth/test_password_service.py`**:

```python
"""
Test suite for password hashing (Issue #281)
"""
import pytest
from services.auth.password_service import PasswordService

class TestPasswordService:
    """Verify password hashing security"""

    def test_hash_password_creates_bcrypt_hash(self):
        """
        Verify passwords hashed with bcrypt.

        Success Criteria:
        - Hash starts with $2b$ (bcrypt identifier)
        - Hash is 60 characters
        - Same password produces different hashes (salt)
        """
        # TODO: Hash password
        # TODO: Verify bcrypt format
        # TODO: Verify uniqueness with salt
        pass

    def test_verify_password_correct(self):
        """
        Verify correct password validates successfully.

        Success Criteria:
        - verify_password returns True for correct password
        """
        # TODO: Hash password
        # TODO: Verify with same password
        # TODO: Assert True
        pass

    def test_verify_password_incorrect(self):
        """
        Verify incorrect password rejected.

        Success Criteria:
        - verify_password returns False for wrong password
        - No exception raised
        """
        # TODO: Hash password
        # TODO: Verify with wrong password
        # TODO: Assert False
        pass

    def test_hash_rounds_sufficient(self):
        """
        Verify bcrypt rounds >= 12 for security.

        Success Criteria:
        - Bcrypt rounds set to 12 or higher
        - Verified in hash string
        """
        # TODO: Hash password
        # TODO: Extract rounds from hash
        # TODO: Assert >= 12
        pass

    def test_generate_temp_password_strength(self):
        """
        Verify generated passwords are strong.

        Success Criteria:
        - Length >= 16 characters
        - Contains letters, numbers, symbols
        - Cryptographically random
        """
        # TODO: Generate password
        # TODO: Verify length
        # TODO: Verify character diversity
        pass
```

### Scaffold 4: JWT Service Tests

**Create `tests/auth/test_jwt_service.py`**:

```python
"""
Test suite for JWT tokens (Issue #281)
"""
import pytest
import time
from services.auth.jwt_service import JWTService

class TestJWTService:
    """Verify JWT token security"""

    def test_generate_token_format(self):
        """
        Verify JWT tokens properly formatted.

        Success Criteria:
        - Token has 3 parts separated by dots
        - Contains user_id and username claims
        - Has expiration claim
        """
        # TODO: Generate token
        # TODO: Decode (unsafe) to check claims
        # TODO: Verify format
        pass

    def test_validate_token_success(self):
        """
        Verify valid tokens validate successfully.

        Success Criteria:
        - Fresh token validates
        - Returns payload with claims
        """
        # TODO: Generate token
        # TODO: Validate immediately
        # TODO: Assert payload matches
        pass

    def test_validate_token_expired(self):
        """
        Verify expired tokens rejected.

        Success Criteria:
        - Token with past expiration returns None
        - No exception raised
        """
        # TODO: Create token with 0 second expiry
        # TODO: Wait 1 second
        # TODO: Validate
        # TODO: Assert None
        pass

    def test_validate_token_tampered(self):
        """
        Verify tampered tokens rejected.

        Success Criteria:
        - Modified token returns None
        - Signature validation catches tampering
        """
        # TODO: Generate valid token
        # TODO: Modify payload
        # TODO: Validate
        # TODO: Assert None
        pass

    def test_secret_key_from_environment(self):
        """
        Verify JWT secret comes from environment variable.

        Success Criteria:
        - JWT_SECRET_KEY env var used if set
        - Falls back to default for alpha
        """
        # TODO: Check JWTService initialization
        # TODO: Verify env var usage
        pass
```

### Scaffold 5: Auth Endpoints Tests

**Create `tests/auth/test_auth_endpoints.py`**:

```python
"""
Test suite for auth endpoints (Issue #281)
"""
import pytest
from fastapi.testclient import TestClient

class TestAuthEndpoints:
    """Verify authentication endpoints"""

    def test_login_success(self, client: TestClient, db_session):
        """
        Verify successful login flow.

        Success Criteria:
        - POST /auth/login with valid credentials returns 200
        - Response includes token, user_id, username
        - Cookie set with auth_token
        """
        # TODO: Create test user with password
        # TODO: Login with credentials
        # TODO: Verify response
        # TODO: Verify cookie
        pass

    def test_login_invalid_username(self, client: TestClient):
        """
        Verify login fails for non-existent user.

        Success Criteria:
        - Returns 401
        - Generic error message (don't leak user existence)
        """
        # TODO: Login with fake username
        # TODO: Assert 401
        # TODO: Verify error message
        pass

    def test_login_invalid_password(self, client: TestClient, db_session):
        """
        Verify login fails for wrong password.

        Success Criteria:
        - Returns 401
        - Generic error message
        """
        # TODO: Create test user
        # TODO: Login with wrong password
        # TODO: Assert 401
        pass

    def test_logout_clears_cookie(self, authenticated_client: TestClient):
        """
        Verify logout clears authentication.

        Success Criteria:
        - POST /auth/logout returns 200
        - Cookie deleted
        - Subsequent requests fail auth
        """
        # TODO: Login first
        # TODO: Call logout
        # TODO: Verify cookie cleared
        # TODO: Try authenticated endpoint
        # TODO: Assert 401
        pass

    def test_get_current_user(self, authenticated_client: TestClient):
        """
        Verify GET /auth/me returns user info.

        Success Criteria:
        - Returns user_id, username, email
        - Requires authentication
        """
        # TODO: Login first
        # TODO: Call /auth/me
        # TODO: Verify user info returned
        pass

    def test_protected_endpoint_without_auth(self, client: TestClient):
        """
        Verify protected endpoints require auth.

        Success Criteria:
        - /chat endpoint returns 401 without token
        """
        # TODO: Call /chat without auth
        # TODO: Assert 401
        pass

    def test_protected_endpoint_with_auth(self, authenticated_client: TestClient):
        """
        Verify authenticated requests work.

        Success Criteria:
        - /chat endpoint works with valid token
        - User context available
        """
        # TODO: Login first
        # TODO: Call /chat
        # TODO: Verify 200 response
        pass
```

---

## Phase 2: Security Review Checklist (15 minutes)

**Create `docs/security-review-checklist.md`**:

```markdown
# Security Review Checklist - P0 Alpha Blockers

**Sprint**: A8 Phase 2.5
**Date**: November 1, 2025
**Issues**: #280, #281, #282

---

## Issue #280: Data Leak Prevention

### File Security
- [ ] PIPER.md contains zero personal data
- [ ] Backup created before modifications
- [ ] No hardcoded personal data anywhere in codebase

### Database Security
- [ ] Personal data properly stored in JSONB field
- [ ] Database queries parameterized (no SQL injection)
- [ ] User data properly isolated by user_id

### Code Review
- [ ] No personal data in logs
- [ ] No personal data in error messages
- [ ] ConfigService properly merges user + generic config

---

## Issue #281: Authentication Security

### Password Security
- [ ] Bcrypt hashing implemented (not plain text)
- [ ] Bcrypt rounds >= 12
- [ ] No passwords in logs
- [ ] No passwords in error messages
- [ ] No passwords in git history
- [ ] Password strength validation (if applicable)

### JWT Security
- [ ] JWT secret from environment variable
- [ ] JWT secret not hardcoded
- [ ] JWT tokens not logged
- [ ] Token expiration set (24h for alpha)
- [ ] Signature validation working
- [ ] No sensitive data in JWT payload

### Endpoint Security
- [ ] All sensitive endpoints require authentication
- [ ] Login endpoint returns generic errors (no user enumeration)
- [ ] Logout properly clears tokens
- [ ] HTTP-only cookies used for web UI
- [ ] No CSRF vulnerabilities
- [ ] Rate limiting considered (optional for alpha)

### Code Security
- [ ] No hardcoded credentials
- [ ] No test credentials in production code
- [ ] SQL injection prevention
- [ ] XSS prevention in responses
- [ ] Proper error handling (no stack traces to users)

---

## Issue #282: File Upload Security

### File Validation
- [ ] File size limit enforced (10MB)
- [ ] File type validation implemented
- [ ] Allowed types: text, PDF, Word, Markdown, JSON only
- [ ] Rejected types: executables, scripts, binaries

### Path Security
- [ ] No path traversal vulnerabilities (../../../etc/passwd)
- [ ] Filenames sanitized
- [ ] Files stored in user-isolated directories
- [ ] Upload directory outside web root

### Storage Security
- [ ] User isolation enforced (User A can't access User B's files)
- [ ] Proper file permissions
- [ ] Uploaded files not executable
- [ ] Metadata stored securely in database

### Code Security
- [ ] Authentication required for upload
- [ ] User context properly validated
- [ ] No arbitrary file write
- [ ] Proper error handling
- [ ] Content-type validation

---

## General Security

### Environment Variables
- [ ] All secrets in environment variables
- [ ] .env file in .gitignore
- [ ] No secrets in git history
- [ ] Environment variables documented

### Database
- [ ] All queries parameterized
- [ ] No SQL injection vectors
- [ ] Proper connection handling
- [ ] Sensitive fields encrypted (if applicable)

### Logging
- [ ] No passwords logged
- [ ] No tokens logged
- [ ] No PII in logs (unless necessary)
- [ ] Error logs don't reveal system internals

### Dependencies
- [ ] bcrypt >= 4.1.1
- [ ] pyjwt >= 2.8.0
- [ ] No known vulnerabilities in dependencies

---

## Testing

### Test Coverage
- [ ] All security features have tests
- [ ] Edge cases tested
- [ ] Negative tests (wrong password, etc.)
- [ ] Multi-user isolation tested

### Manual Testing
- [ ] Attempted SQL injection
- [ ] Attempted path traversal
- [ ] Attempted XSS
- [ ] Attempted unauthorized access
- [ ] Token tampering tested

---

## Documentation

- [ ] Security considerations documented
- [ ] Environment variables documented
- [ ] Setup instructions include security steps
- [ ] Known limitations documented

---

**Reviewer**: [Name]
**Date**: [Date]
**Result**: PASS / FAIL / NEEDS WORK
**Notes**:
[Add any findings, concerns, or recommendations]
```

---

## Phase 3: Cross-Validation Protocol (After Each Issue)

### When Code Completes Issue #280

**Evidence Verification** (15 minutes):

1. **Verify Files Exist**:
   ```bash
   # Check Code's claimed modifications
   ls -la config/PIPER.md
   ls -la config/PIPER.md.backup-*
   ls -la scripts/migrate_personal_data_to_xian.py

   # Use Serena to verify ConfigService changes
   serena.view_file("services/config/config_service.py")
   ```

2. **Verify Git Commits**:
   ```bash
   git log --oneline -5
   git diff main --stat
   ```

3. **Test Personal Data Removal**:
   ```bash
   grep -i "Q4\|VA\|DRAGONS\|Kind Systems\|christian\|xian" config/PIPER.md
   # Expected: No matches
   ```

4. **Test Database Migration**:
   ```python
   # Run migration script
   python scripts/migrate_personal_data_to_xian.py

   # Verify data in database
   python -c "
   import asyncio
   from sqlalchemy import select
   from database import get_db_session
   from models.user import AlphaUser

   async def check():
       async with get_db_session() as db:
           result = await db.execute(
               select(AlphaUser).where(AlphaUser.username == 'xian')
           )
           user = result.scalar_one()
           print(f'Preferences: {user.preferences}')

   asyncio.run(check())
   "
   ```

5. **Run Your Tests**:
   ```bash
   python -m pytest tests/config/test_data_isolation.py -v
   ```

**Report findings**: If issues found, report to PM. If clean, mark #280 verified.

---

### When Code Completes Issue #282

**Evidence Verification** (15 minutes):

1. **Verify Endpoint Exists**:
   ```python
   serena.view_file("web/app.py")
   # Look for @app.post("/upload")
   ```

2. **Test Upload Functionality**:
   ```bash
   # Create test file
   echo "Test content" > test.txt

   # Upload (get token from login first)
   curl -X POST http://localhost:8001/upload \
     -H "Authorization: Bearer TOKEN" \
     -F "file=@test.txt"
   ```

3. **Test Security Validations**:
   ```bash
   # Test file size limit
   dd if=/dev/zero of=large.txt bs=1M count=20
   curl -X POST http://localhost:8001/upload \
     -H "Authorization: Bearer TOKEN" \
     -F "file=@large.txt"
   # Expected: 413

   # Test file type validation
   echo "#!/bin/bash" > test.sh
   curl -X POST http://localhost:8001/upload \
     -H "Authorization: Bearer TOKEN" \
     -F "file=@test.sh"
   # Expected: 415
   ```

4. **Verify User Isolation**:
   ```bash
   ls -R uploads/
   # Should show separate user directories
   ```

5. **Run Your Tests**:
   ```bash
   python -m pytest tests/web/test_file_upload.py -v
   ```

**Report findings**: Security issues are blockers. Don't pass until secure.

---

### When Code Completes Issue #281 (Most Critical)

**Evidence Verification** (30 minutes):

1. **Verify Dependencies Installed**:
   ```bash
   pip list | grep bcrypt
   pip list | grep pyjwt
   ```

2. **Test Password Hashing**:
   ```bash
   python -c "
   from services.auth.password_service import PasswordService
   ps = PasswordService()
   h = ps.hash_password('test123')
   print(f'Hash: {h}')
   print(f'Bcrypt: {h.startswith(\"$2b$\")}')
   print(f'Verify: {ps.verify_password(\"test123\", h)}')
   "
   ```

3. **Test JWT Tokens**:
   ```bash
   python -c "
   from services.auth.jwt_service import JWTService
   js = JWTService()
   token = js.generate_token('user-1', 'test')
   print(f'Token: {token[:50]}...')
   payload = js.validate_token(token)
   print(f'Valid: {payload is not None}')
   "
   ```

4. **Test Login Flow**:
   ```bash
   # Set password first
   python scripts/setup_alpha_passwords.py xian --password "test123"

   # Test login
   curl -X POST http://localhost:8001/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "xian", "password": "test123"}'
   ```

5. **Test Protected Endpoints**:
   ```bash
   # Without auth (should fail)
   curl http://localhost:8001/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "hello"}'
   # Expected: 401

   # With auth (should work)
   curl http://localhost:8001/chat \
     -H "Authorization: Bearer TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"message": "hello"}'
   # Expected: 200
   ```

6. **Run Security Checklist**:
   ```bash
   # Work through security-review-checklist.md
   # Check each item manually

   # Search for security issues
   grep -r "password.*=.*['\"]" services/ web/ --include="*.py"
   # Should only find PasswordService methods, no hardcoded passwords
   ```

7. **Run Your Tests**:
   ```bash
   python -m pytest tests/auth/ -v
   ```

**Report findings**: Auth is security-critical. Be thorough. Flag any concerns.

---

## Success Criteria

**Before marking sprint complete, verify**:

- [ ] All Code's claimed files actually exist
- [ ] All Code's claimed tests actually pass
- [ ] All YOUR tests pass (ones you created)
- [ ] Security checklist 100% verified
- [ ] No hardcoded secrets found
- [ ] Multi-user isolation confirmed
- [ ] Edge cases tested
- [ ] Documentation updated
- [ ] GitHub issues updated with evidence

---

## Coordination with PM

**Report Format**:

```markdown
## Cross-Validation Report: Issue #XXX

**Date**: [timestamp]
**Code Agent Claims**: [Summary of what Code said it did]
**Verification Results**:

✅ **Passed Checks**:
- File X exists at claimed location
- Tests pass as claimed
- Feature works as described

⚠️ **Issues Found**:
- Security concern: [describe]
- Missing edge case: [describe]
- Test gap: [describe]

🔍 **Recommendations**:
- [What should be fixed/improved]

**Verdict**: VERIFIED / NEEDS WORK / BLOCKED
```

---

## Time Management

**Estimate**:
- Test scaffolds: 1 hour
- Security checklist: 15 minutes
- Cross-validation #280: 15 minutes
- Cross-validation #282: 15 minutes
- Cross-validation #281: 30 minutes (critical)

**Total**: ~2.25 hours

This runs **parallel** with Code's 10-15 hours, so doesn't extend timeline.

---

## Questions for PM (if needed)

- If test infrastructure doesn't exist yet
- If you find security vulnerabilities
- If Code's evidence doesn't match reality
- If you need clarification on security standards

**Always escalate security concerns immediately.**

---

## Anti-80% Reminder

Your job is to be the **independent verifier**. Don't just rubber-stamp Code's work. Actually run the tests, check the evidence, find the edge cases.

If Code claims "tests pass" but you find failures, that's a BLOCK.

Quality gate enforcement is your superpower. Use it!

---

Good luck! Your systematic verification prevents the "looks done but broken" scenario that often happens with AI agents. 🔍🏰
