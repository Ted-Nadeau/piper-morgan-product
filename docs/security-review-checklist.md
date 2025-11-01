# Security Review Checklist - P0 Alpha Blockers

**Sprint**: A8 Phase 2.5
**Date**: November 1, 2025
**Issues**: #280 (Data Leak), #281 (Auth), #282 (File Upload)
**Reviewer**: Cursor Agent (Test Validation)
**Purpose**: Manual security verification before marking sprint complete

---

## Issue #280: CORE-ALPHA-DATA-LEAK

### File Security

- [ ] PIPER.md contains zero personal data
  - [ ] No mentions of: Q4, VA, DRAGONS, Kind Systems, Christian, xian
  - [ ] No specific project names
  - [ ] No team structures or company info
  - [ ] No individual preferences or examples

- [ ] Backup created before modifications
  - [ ] Backup file exists: `config/PIPER.md.backup-YYYYMMDD`
  - [ ] Backup contains original content

- [ ] No hardcoded personal data anywhere in codebase
  - [ ] Searched services/ for personal data patterns
  - [ ] Searched web/ for personal data patterns
  - [ ] No personal data in test files

### Database Security

- [ ] Personal data properly stored in JSONB field
  - [ ] xian's preferences populated in `alpha_users.preferences`
  - [ ] Data structure is valid JSON
  - [ ] Contains expected keys: projects, q4_goals, team, etc.

- [ ] Database queries parameterized (no SQL injection)
  - [ ] ConfigService uses parameterized queries
  - [ ] No string concatenation in SQL

- [ ] User data properly isolated by user_id
  - [ ] ConfigService loads user-specific data by user_id
  - [ ] No cross-user data leakage possible

### Code Review

- [ ] No personal data in logs
  - [ ] Searched for `print()` statements with personal data
  - [ ] Searched for `logger.info()` with personal data

- [ ] No personal data in error messages
  - [ ] Exception messages don't include user data
  - [ ] Stack traces filtered appropriately

- [ ] ConfigService properly merges user + generic config
  - [ ] Generic config loaded from PIPER.md
  - [ ] User config loaded from database
  - [ ] Merge logic preserves both sources
  - [ ] User data doesn't pollute generic config

### Testing

- [ ] Multi-user isolation tested
  - [ ] User A sees only User A's data
  - [ ] User B sees only User B's data
  - [ ] No data leakage confirmed

- [ ] Generic config tested
  - [ ] load_config() without user_id returns generic only
  - [ ] No personal data in generic response

---

## Issue #281: CORE-ALPHA-WEB-AUTH

### Password Security

- [ ] Bcrypt hashing implemented (not plain text)
  - [ ] `PasswordService.hash_password()` uses bcrypt
  - [ ] No MD5/SHA1/SHA256 for passwords

- [ ] Bcrypt rounds >= 12
  - [ ] Verified in PasswordService implementation
  - [ ] Hash strings show correct rounds

- [ ] No passwords in logs
  - [ ] Searched for password logging
  - [ ] Login endpoint doesn't log passwords

- [ ] No passwords in error messages
  - [ ] Validation errors don't echo passwords
  - [ ] Stack traces don't include passwords

- [ ] No passwords in git history
  - [ ] `git log -S "password.*=.*['\"]"` shows no results
  - [ ] No hardcoded test passwords in committed code

- [ ] Password strength validation (if applicable)
  - [ ] Minimum length enforced (if required)
  - [ ] Character diversity checked (if required)

### JWT Security

- [ ] JWT secret from environment variable
  - [ ] `JWT_SECRET_KEY` environment variable used
  - [ ] Falls back to reasonable default for alpha only

- [ ] JWT secret not hardcoded
  - [ ] No "secret", "password", "test" as secret
  - [ ] Secret length >= 16 characters

- [ ] JWT tokens not logged
  - [ ] Searched for token logging statements
  - [ ] Debug output doesn't include tokens

- [ ] Token expiration set (24h for alpha)
  - [ ] Tokens expire after 24 hours
  - [ ] Expiration enforced by validation

- [ ] Signature validation working
  - [ ] Tampered tokens rejected
  - [ ] Wrong secret tokens rejected
  - [ ] Expired tokens rejected

- [ ] No sensitive data in JWT payload
  - [ ] No password_hash in token
  - [ ] No API keys in token
  - [ ] Only user_id, username, basic claims

### Endpoint Security

- [ ] All sensitive endpoints require authentication
  - [ ] `/chat` requires auth
  - [ ] `/upload` requires auth
  - [ ] `/status` requires auth (or not, depending on design)
  - [ ] Other user-specific endpoints require auth

- [ ] Login endpoint returns generic errors (no user enumeration)
  - [ ] Invalid username: "Invalid username or password"
  - [ ] Invalid password: "Invalid username or password"
  - [ ] Same error message for both cases

- [ ] Logout properly clears tokens
  - [ ] Cookie deleted on logout
  - [ ] Token invalidation (if implemented)

- [ ] HTTP-only cookies used for web UI
  - [ ] `httponly=True` in cookie settings
  - [ ] `secure=False` for alpha (dev), `True` for production
  - [ ] `samesite="lax"` set appropriately

- [ ] No CSRF vulnerabilities
  - [ ] CORS configured correctly
  - [ ] SameSite cookie policy set

- [ ] Rate limiting considered (optional for alpha)
  - [ ] Not required for alpha
  - [ ] Note added for production

### Code Security

- [ ] No hardcoded credentials
  - [ ] Searched entire codebase
  - [ ] No test credentials in production code

- [ ] No test credentials in production code
  - [ ] No "admin/admin" pairs
  - [ ] No default passwords

- [ ] SQL injection prevention
  - [ ] All queries parameterized
  - [ ] No string concatenation in SQL

- [ ] XSS prevention in responses
  - [ ] User input properly escaped
  - [ ] JSON responses properly encoded

- [ ] Proper error handling (no stack traces to users)
  - [ ] 500 errors don't show stack traces
  - [ ] Debug info not leaked to clients

### Testing

- [ ] Password hashing tested
  - [ ] Tests verify bcrypt format
  - [ ] Tests verify rounds >= 12
  - [ ] Tests verify salt uniqueness

- [ ] JWT generation tested
  - [ ] Tests verify token format
  - [ ] Tests verify claims present
  - [ ] Tests verify expiration

- [ ] JWT validation tested
  - [ ] Valid tokens pass
  - [ ] Expired tokens fail
  - [ ] Tampered tokens fail

- [ ] Login flow tested
  - [ ] Valid credentials succeed
  - [ ] Invalid credentials fail
  - [ ] Missing password fails

- [ ] Protected endpoints tested
  - [ ] Without auth returns 401
  - [ ] With valid auth succeeds
  - [ ] With invalid auth returns 401

- [ ] Multi-user isolation tested
  - [ ] User A can't access User B's data
  - [ ] Sessions properly isolated

---

## Issue #282: CORE-ALPHA-FILE-UPLOAD

### File Validation

- [ ] File size limit enforced (10MB)
  - [ ] Files <= 10MB accepted
  - [ ] Files > 10MB rejected with 413
  - [ ] Boundary case tested (exactly 10MB)

- [ ] File type validation implemented
  - [ ] Content-Type header checked
  - [ ] File extension validated

- [ ] Allowed types: text, PDF, Word, Markdown, JSON only
  - [ ] text/plain accepted
  - [ ] application/pdf accepted
  - [ ] application/vnd.openxmlformats-officedocument.wordprocessingml.document accepted
  - [ ] text/markdown accepted
  - [ ] application/json accepted

- [ ] Rejected types: executables, scripts, binaries
  - [ ] .exe rejected with 415
  - [ ] .sh rejected with 415
  - [ ] .dll rejected with 415
  - [ ] .bat rejected with 415
  - [ ] Other dangerous types rejected

### Path Security

- [ ] No path traversal vulnerabilities (../)
  - [ ] `../../../etc/passwd` rejected or sanitized
  - [ ] `..\\..\\..\\windows\\system32` rejected or sanitized
  - [ ] Path traversal patterns blocked

- [ ] Filenames sanitized
  - [ ] Special characters handled
  - [ ] Unicode filenames handled
  - [ ] Long filenames handled

- [ ] Files stored in user-isolated directories
  - [ ] Pattern: `uploads/{user_id}/{filename}`
  - [ ] User A's files in separate directory from User B

- [ ] Upload directory outside web root
  - [ ] Not in `web/static/`
  - [ ] Not publicly accessible via URL
  - [ ] Files only accessible through authenticated endpoints

### Storage Security

- [ ] User isolation enforced (User A can't access User B's files)
  - [ ] Directory permissions correct
  - [ ] File access checks in place
  - [ ] No direct file path access

- [ ] Proper file permissions
  - [ ] Files not executable (0644 or similar)
  - [ ] Directories have correct permissions (0755 or similar)

- [ ] Uploaded files not executable
  - [ ] Execute bit not set
  - [ ] Files stored in non-executable partition (if applicable)

- [ ] Metadata stored securely in database
  - [ ] User ID associated with file
  - [ ] File path not directly exposed to users
  - [ ] Metadata includes: filename, size, content_type, upload_time

### Code Security

- [ ] Authentication required for upload
  - [ ] `/upload` endpoint requires auth
  - [ ] No anonymous uploads

- [ ] User context properly validated
  - [ ] User ID from authenticated session
  - [ ] Not from user input
  - [ ] Can't upload as different user

- [ ] No arbitrary file write
  - [ ] Destination path controlled by server
  - [ ] User can't specify upload directory

- [ ] Proper error handling
  - [ ] File errors don't crash server
  - [ ] Disk full handled gracefully
  - [ ] Permission errors handled

- [ ] Content-type validation
  - [ ] Header checked against allowed types
  - [ ] MIME type validated
  - [ ] File extension matches content-type

### Testing

- [ ] Upload success tested
  - [ ] Text file uploads successfully
  - [ ] Response includes file_id, filename, size

- [ ] File size limits tested
  - [ ] 10MB+ file rejected
  - [ ] Clear error message

- [ ] File type validation tested
  - [ ] Allowed types accepted
  - [ ] Dangerous types rejected

- [ ] Path traversal tested
  - [ ] `../` patterns blocked
  - [ ] No files written outside uploads directory

- [ ] User isolation tested
  - [ ] User A can't access User B's files
  - [ ] File lists filtered by user

---

## General Security

### Environment Variables

- [ ] All secrets in environment variables
  - [ ] `JWT_SECRET_KEY`
  - [ ] `DATABASE_URL`
  - [ ] API keys (if any)

- [ ] .env file in .gitignore
  - [ ] Verified in `.gitignore`
  - [ ] `.env` not in git

- [ ] No secrets in git history
  - [ ] `git log -S "secret_key"` checked
  - [ ] `git log -S "password"` checked

- [ ] Environment variables documented
  - [ ] README or docs include env var list
  - [ ] Example values provided

### Database

- [ ] All queries parameterized
  - [ ] No f-strings with user input in SQL
  - [ ] No string concatenation in queries

- [ ] No SQL injection vectors
  - [ ] Manual review of all SQL queries
  - [ ] Dynamic queries use safe methods

- [ ] Proper connection handling
  - [ ] Connections closed properly
  - [ ] Connection pooling configured

- [ ] Sensitive fields encrypted (if applicable)
  - [ ] Not required for alpha
  - [ ] password_hash is already bcrypt (sufficient)

### Logging

- [ ] No passwords logged
  - [ ] Login attempts don't log passwords
  - [ ] Error logs don't include passwords

- [ ] No tokens logged
  - [ ] JWT tokens not logged
  - [ ] API keys not logged

- [ ] No PII in logs (unless necessary)
  - [ ] User emails not logged unnecessarily
  - [ ] Personal data not in debug logs

- [ ] Error logs don't reveal system internals
  - [ ] Stack traces filtered for production
  - [ ] Database schema not exposed

### Dependencies

- [ ] bcrypt >= 4.1.1
  - [ ] Checked in `requirements.txt`
  - [ ] No known vulnerabilities

- [ ] pyjwt >= 2.8.0
  - [ ] Checked in `requirements.txt`
  - [ ] No known vulnerabilities

- [ ] No known vulnerabilities in dependencies
  - [ ] `pip list` checked
  - [ ] Major packages verified

---

## Testing

### Test Coverage

- [ ] All security features have tests
  - [ ] Password hashing tested
  - [ ] JWT generation/validation tested
  - [ ] Auth endpoints tested
  - [ ] File upload security tested
  - [ ] Data isolation tested

- [ ] Edge cases tested
  - [ ] Empty inputs
  - [ ] Very long inputs
  - [ ] Special characters
  - [ ] Unicode handling

- [ ] Negative tests (wrong password, etc.)
  - [ ] Invalid credentials tested
  - [ ] Expired tokens tested
  - [ ] Malformed requests tested

- [ ] Multi-user isolation tested
  - [ ] At least 2 users tested
  - [ ] No data leakage confirmed

### Manual Testing

- [ ] Attempted SQL injection
  - [ ] Tried in username field
  - [ ] Tried in other user inputs
  - [ ] No vulnerabilities found

- [ ] Attempted path traversal
  - [ ] Tried `../../../etc/passwd`
  - [ ] Tried other traversal patterns
  - [ ] All blocked or sanitized

- [ ] Attempted XSS
  - [ ] Tried `<script>alert('xss')</script>`
  - [ ] Tried other XSS payloads
  - [ ] All properly escaped

- [ ] Attempted unauthorized access
  - [ ] Tried accessing without token
  - [ ] Tried accessing other user's data
  - [ ] All blocked with 401/403

- [ ] Token tampering tested
  - [ ] Modified token payload
  - [ ] Modified token signature
  - [ ] All rejected

---

## Documentation

- [ ] Security considerations documented
  - [ ] README includes security notes
  - [ ] Setup guide mentions security steps

- [ ] Environment variables documented
  - [ ] List of required variables
  - [ ] Example values provided
  - [ ] Security implications explained

- [ ] Setup instructions include security steps
  - [ ] Password setup explained
  - [ ] JWT secret generation explained

- [ ] Known limitations documented
  - [ ] Alpha limitations noted
  - [ ] Features deferred to MVP listed
  - [ ] Manual password reset process documented

---

## Final Verification

### Pre-Approval Checks

- [ ] All automated tests pass
  - [ ] `pytest tests/config/test_data_isolation.py`
  - [ ] `pytest tests/auth/test_password_service.py`
  - [ ] `pytest tests/auth/test_jwt_service.py`
  - [ ] `pytest tests/auth/test_auth_endpoints.py`
  - [ ] `pytest tests/web/test_file_upload.py`

- [ ] Manual testing complete
  - [ ] Worked through all manual test scenarios
  - [ ] No security issues found

- [ ] Code review complete
  - [ ] All modified files reviewed
  - [ ] No obvious security issues

- [ ] Multi-user testing complete
  - [ ] Tested with 2+ different user accounts
  - [ ] No data leakage observed

### Evidence Collection

- [ ] Test output captured
  - [ ] Screenshots or terminal output saved
  - [ ] All tests passing

- [ ] Security scan results
  - [ ] No critical vulnerabilities
  - [ ] Known issues documented

- [ ] Code audit notes
  - [ ] Review findings documented
  - [ ] Issues tracked in GitHub

---

## Sign-Off

**Reviewer**: Cursor Agent (Test Validation)
**Date**: _________________
**Result**: ☐ PASS   ☐ FAIL   ☐ NEEDS WORK

**Overall Assessment**:

_[Summary of security posture, major findings, recommendations]_

**Blockers** (if any):

_[List any security issues that must be fixed before approval]_

**Recommendations for MVP**:

_[Security improvements to add before wider release]_

**Notes**:

_[Additional context, concerns, or observations]_

---

**Approval Required From**:
- [ ] Product Manager (xian/Christian)
- [ ] Code Agent (implementation verification)
- [ ] Cursor Agent (security verification)

**Ready for External Alpha**: ☐ YES   ☐ NO

---

*This checklist must be completed and signed off before inviting external alpha testers.*
