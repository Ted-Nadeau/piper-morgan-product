# Discovery Prompt: CORE-USERS-JWT (#227)

**Agent**: Cursor (Chief Architect)
**Task**: Architectural discovery for JWT token blacklist storage
**Issue**: #227 CORE-USERS-JWT
**Duration**: 10-15 minutes
**Date**: October 21, 2025

---

## Mission

Discover what authentication and JWT infrastructure currently exists in the Piper Morgan codebase, assess token blacklist requirements, and determine implementation path for secure token invalidation (logout, security revocation).

**Key Questions**:
1. Does JWT authentication infrastructure exist?
2. Is there a token blacklist mechanism?
3. Is Redis available for blacklist storage?
4. What database fallback options exist?
5. Where are the integration points (logout, middleware)?

---

## Phase 1: Search for Auth & JWT Infrastructure (5 min)

### Serena Symbolic Queries

Run these searches to find authentication code:

```bash
# Search for JWT services
mcp__serena__search_project("JWT|jwt|token", file_pattern="services/**/*.py")

# Search for authentication services
mcp__serena__search_project("auth|authentication|AuthService", file_pattern="services/**/*.py")

# Search for Redis infrastructure
mcp__serena__search_project("redis|Redis|RedisClient", file_pattern="**/*.py")

# Search for token blacklist mentions
mcp__serena__search_project("blacklist|revoke|invalidate.*token", file_pattern="**/*.py")

# Search for logout endpoints
mcp__serena__search_project("logout|signout", file_pattern="**/*.py")

# Search for middleware
mcp__serena__search_project("middleware|auth.*middleware", file_pattern="**/*.py")
```

### Verification Commands

```bash
# Check for services/auth directory
ls -la services/auth/ 2>/dev/null || echo "services/auth/ does not exist"

# Search for JWT library usage
grep -r "import jwt\|from jwt import\|PyJWT" services/ --include="*.py"

# Search for Redis client
grep -r "redis.Redis\|aioredis\|redis.asyncio" services/ --include="*.py"

# Check for existing TODO comments about blacklist
grep -r "TODO.*blacklist\|TODO.*token.*invalidat" services/ --include="*.py"

# Search for token storage
find services/ -name "*token*" -type f

# Search for session management
find services/ -name "*session*" -type f
```

---

## Phase 2: Document Current JWT Infrastructure (5 min)

### For Each Component Found

Document:
- **File**: Path to file
- **Class/Function**: What handles JWT operations
- **Functionality**: Token creation, validation, refresh, etc
- **Storage**: Where tokens are stored (if anywhere)
- **Dependencies**: Libraries used (PyJWT, python-jose, etc)

### Expected Components

Search these areas specifically:

1. **JWT Service**
   - File: `services/auth/jwt_service.py` or similar
   - Purpose: Token creation, validation, signing
   - Check for TODO comments about blacklist

2. **Auth Middleware**
   - File: `web/middleware/` or similar
   - Purpose: Request authentication
   - Check token validation logic

3. **Login/Logout Endpoints**
   - File: `web/routes/` or `web/app.py`
   - Purpose: User authentication flows
   - Check if logout exists

4. **Redis Client**
   - File: `services/database/redis.py` or similar
   - Purpose: Cache, session storage
   - Check if Redis is configured

5. **Database Session Management**
   - File: `services/database/` or similar
   - Purpose: Persistent storage
   - Check for session tables

---

## Phase 3: Assess Blacklist Requirements (3 min)

### Current Token Validation Pattern

Find and document:

```python
# How are tokens currently validated?
# Example pattern to look for:

async def validate_token(token: str) -> User:
    # 1. Decode JWT
    payload = decode_jwt(token)

    # 2. Check expiration
    if expired(payload):
        raise TokenExpired

    # 3. TODO: Check blacklist? (look for this!)

    # 4. Load user
    return get_user(payload['user_id'])
```

### Logout Pattern

Find and document:

```python
# How is logout currently handled?
# Example pattern to look for:

@app.post("/logout")
async def logout(token: str):
    # TODO: Add token to blacklist? (look for this!)
    return {"message": "Logged out"}
```

### Assessment Questions

1. **JWT Service Exists**:
   - [ ] Token creation implemented?
   - [ ] Token validation implemented?
   - [ ] Token refresh implemented?
   - [ ] TODO comments about blacklist?

2. **Redis Available**:
   - [ ] Redis client configured?
   - [ ] Redis connection tested?
   - [ ] Used for other features (cache, sessions)?

3. **Database Available**:
   - [ ] PostgreSQL connection exists?
   - [ ] Session/token tables exist?
   - [ ] Async database access configured?

4. **Integration Points**:
   - [ ] Logout endpoint exists?
   - [ ] Auth middleware validates tokens?
   - [ ] Admin revocation capability?

---

## Phase 4: Gap Analysis (2 min)

### Infrastructure Assessment

Create inventory:

**EXISTS** (List with file paths):
- JWT service components
- Redis client (if any)
- Database connections
- Auth middleware
- Logout endpoints

**MISSING** (List what needs to be built):
- Token blacklist storage
- Blacklist operations (add, check, cleanup)
- Logout integration
- Middleware enforcement
- Admin revocation tools

### Implementation Complexity

For each missing component:
- **Simple** (<1 hour): Redis SET operations, basic CRUD
- **Moderate** (1-2 hours): Fallback logic, integration
- **Complex** (2+ hours): New infrastructure, migration

---

## Discovery Report Format

Create: `dev/2025/10/21/core-users-jwt-discovery-report.md`

### Report Structure

```markdown
# CORE-USERS-JWT Discovery Report

**Date**: October 21, 2025
**Agent**: Cursor (Chief Architect)
**Duration**: [X] minutes
**Issue**: #227 CORE-USERS-JWT

---

## Executive Summary

**Key Finding**: [One sentence: Does JWT + Redis infrastructure exist?]

**Current State**:
- JWT service: [EXISTS / PARTIAL / MISSING]
- Redis client: [EXISTS / MISSING]
- Token blacklist: [EXISTS / MISSING]
- Logout integration: [EXISTS / PARTIAL / MISSING]

**Work Required**: [X-Y hours based on gap analysis]

---

## Current Authentication Infrastructure

### Directory Structure

```
services/
├── auth/                [EXISTS / MISSING]
│   ├── jwt_service.py   [EXISTS / MISSING]
│   └── __init__.py      [EXISTS / MISSING]
├── database/
│   ├── redis.py         [EXISTS / MISSING]
│   └── session.py       [EXISTS / MISSING]
```

### JWT Service Status

**File**: [path or N/A]
**Functionality**:
- Token creation: [YES/NO]
- Token validation: [YES/NO]
- Token refresh: [YES/NO]
- Blacklist check: [YES/NO]

**TODO Comments Found**:
```python
[paste any TODO comments about blacklist]
```

### Redis Infrastructure Status

**File**: [path or N/A]
**Status**: [CONFIGURED / NOT CONFIGURED]
**Usage**: [cache, sessions, other features]

**Connection Details**:
```python
[paste Redis client configuration if found]
```

### Authentication Flow

**Login Endpoint**: [path or N/A]
**Logout Endpoint**: [path or N/A]
**Middleware**: [path or N/A]

**Current Token Validation**:
```python
[paste current validation logic]
```

---

## Gap Analysis

### What Exists

[List with file paths and line counts]

### What's Missing

**1. Token Blacklist Storage**
- Redis-based blacklist implementation
- Database fallback mechanism
- TTL management

**2. Blacklist Operations**
```python
class TokenBlacklist:
    async def add(token, reason, expires_at)
    async def is_blacklisted(token)
    async def remove_expired()
```

**3. Integration Points**
- Logout endpoint blacklist integration
- Middleware blacklist enforcement
- Admin revocation capability

**4. Background Tasks**
- Expired token cleanup
- Monitoring and metrics

---

## Implementation Estimate

### Phase 1: Token Blacklist Storage
- Redis client setup (if needed): [X hours]
- TokenBlacklist class implementation: [X hours]
- Database fallback: [X hours]
- **Subtotal**: [X-Y hours]

### Phase 2: Integration
- Logout endpoint integration: [X hours]
- Middleware enforcement: [X hours]
- Admin revocation: [X hours]
- **Subtotal**: [X-Y hours]

### Phase 3: Background Tasks
- Cleanup task: [X hours]
- Monitoring: [X hours]
- **Subtotal**: [X-Y hours]

### Phase 4: Testing
- Unit tests: [X hours]
- Integration tests: [X hours]
- Performance tests: [X hours]
- **Subtotal**: [X-Y hours]

**TOTAL ESTIMATE**: [X-Y hours]

---

## Recommendations

### Option 1: [Title]
- **Time**: [X hours]
- **Scope**: [description]
- **Benefits**: [list]
- **Risks**: [list]

### Option 2: [Title]
- ...

### Recommended Approach: [Option X]
- **Rationale**: [why]

---

## Technical Considerations

### Redis Advantages
- O(1) blacklist lookups
- Automatic expiration via TTL
- High performance (<10ms)
- Minimal storage overhead

### Database Fallback
- Reliability if Redis down
- Persistent audit trail
- Query capabilities

### Security Considerations
- Token ID vs full token storage
- Audit logging for revocations
- Admin access controls

---

## Files Examined

**Authentication**:
- services/auth/[...]

**Database**:
- services/database/[...]

**Web/API**:
- web/routes/[...]
- web/middleware/[...]

**Configuration**:
- [config files found]

---

## Next Steps

1. [Action 1]
2. [Action 2]
3. [Action 3]

---

*Discovery complete. Ready for implementation planning.*
```

---

## Success Criteria

Discovery is complete when:

- [x] All Serena queries executed
- [x] All verification commands run
- [x] JWT service status documented
- [x] Redis infrastructure assessed
- [x] Integration points identified
- [x] Gap analysis complete
- [x] Effort estimate provided
- [x] Discovery report written
- [x] Recommendations clear

---

## Notes for Cursor

- Check for TODO comments explicitly
- Document current token validation flow
- Assess Redis availability carefully
- Identify all integration points
- Consider security implications
- Provide realistic effort estimates

---

**Ready to discover!** Use this prompt to investigate JWT token blacklist requirements.
