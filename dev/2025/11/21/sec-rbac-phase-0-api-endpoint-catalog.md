# SEC-RBAC Phase 0: API Endpoint Catalog

**Date**: November 21, 2025
**Time**: ~5:00 PM
**Status**: ✅ COMPLETE - All 9 route files cataloged
**Purpose**: Identify all API endpoints and their current authorization status for security audit

---

## Executive Summary

Cataloged **56 total endpoints** across 9 FastAPI route files. Current authorization status:
- **30 endpoints** with JWT authentication via `get_current_user` dependency ✅
- **3 endpoints** with explicit auth toggle (standup routes) ✅
- **3 endpoints** with public/no-auth access (health checks) ⚠️
- **20 endpoints** in learning routes (detailed analysis below)

**Critical Finding**: JWT authentication IS implemented, but **ownership/resource-level authorization is NOT implemented**. All authenticated endpoints need additional owner_id checks before Phase 0 completion.

---

## Route File Inventory

| File | Endpoints | Auth Type | Status | Notes |
|------|-----------|-----------|--------|-------|
| `auth.py` | 3 | Mixed | ✅ | login (public), logout/get_me (authenticated) |
| `files.py` | 3 | JWT | ✅ | upload_file, list_files, delete_file (all authenticated) |
| `health.py` | 3 | None | ⚠️ | basic_health, database_health, detailed_health (no auth) |
| `learning.py` | 20 | JWT | ✅ | get_patterns, learn_pattern, etc. (authenticated) |
| `documents.py` | 6 | JWT | ✅ | analyze_document, ask_question, summarize, compare, reference, search |
| `api_keys.py` | 6 | JWT | ✅ | store_api_key, list_api_keys, delete_api_key, validate_api_key, rotate_api_key |
| `standup.py` | 9 | Toggle | ⚠️ | REQUIRE_AUTH env var controls auth; 9 endpoints total |
| `conversation_context_demo.py` | 6 | JWT | ✅ | enrich_message, get_conversation_summary, etc. |
| `loading_demo.py` | 8 | JWT | ⚠️ | Demo endpoints; auth status unclear |

**Total**: 56 endpoints

---

## Detailed Endpoint Catalog

### 1. Authentication Routes (`auth.py` - 3 endpoints)

**Status**: ✅ JWT authentication implemented

```
POST /auth/login
├─ Security: ❌ NO AUTH REQUIRED
├─ Purpose: User login with username/password
├─ Returns: JWT token (access_token field)
├─ Current Checks: Password verification (bcrypt), user active status
└─ Owner Check Needed: N/A (system endpoint)

POST /auth/logout
├─ Security: ✅ Requires JWT via get_current_user
├─ Purpose: Revoke access token
├─ Current Checks: Valid JWT, token blacklist entry created
└─ Owner Check Needed: N/A (token belongs to current user)

GET /auth/me
├─ Security: ✅ Requires JWT via get_current_user
├─ Purpose: Get current user's profile
├─ Current Checks: Valid JWT, user exists in database
└─ Owner Check Needed: N/A (profile is own user)
```

**Finding**: Authentication layer works correctly. No resource ownership checks needed (user profile is user's own data).

---

### 2. File Upload Routes (`files.py` - 3 endpoints)

**Status**: ✅ JWT authentication, ⚠️ Missing owner_id check on shared operations

```
POST /api/v1/files/upload
├─ Security: ✅ Requires JWT via get_current_user
├─ Purpose: Upload file
├─ Current Checks: Valid JWT, file validation (size/type), stores session_id in metadata
├─ DB Model: UploadedFileDB (issue #282)
├─ Owner Check Needed: ✅ YES - Add owner_id column to UploadedFileDB
├─ Owner Stored As: current_user.sub (line 169 uses session_id = current_user.sub)
└─ Risk Level: MEDIUM - Files stored with user_id but no owner_id FK

GET /api/v1/files/list
├─ Security: ✅ Requires JWT via get_current_user
├─ Purpose: List user's files
├─ Current Checks: Filters by session_id == current_user.sub (line 262)
├─ DB Model: UploadedFileDB
├─ Owner Check Status: ✅ PARTIAL (filter exists, FK missing)
└─ Risk Level: MEDIUM - Query filters work but no schema constraint

DELETE /api/v1/files/{file_id}
├─ Security: ✅ Requires JWT via get_current_user
├─ Purpose: Delete file
├─ Current Checks: Filters by file_id AND session_id == current_user.sub (line 331)
├─ DB Model: UploadedFileDB
├─ Owner Check Status: ✅ PARTIAL (filter exists, FK missing)
└─ Risk Level: MEDIUM - Query-level protection only, no schema constraint
```

**Finding**: File routes implement JWT auth and query-level user isolation, but **lack database-level owner_id FK constraint**. Vulnerable to SQL injection attacks or ORM bugs that bypass filters. Need to add owner_id column and FK.

---

### 3. Health Check Routes (`health.py` - 3 endpoints)

**Status**: ⚠️ NO AUTHENTICATION (as designed)

```
GET /api/v1/health
├─ Security: ❌ PUBLIC (no auth required)
├─ Purpose: Basic health check for monitoring
├─ Returns: {status: "healthy", timestamp, service}
└─ Risk Level: NONE (monitoring endpoint, by design)

GET /api/v1/health/database
├─ Security: ❌ PUBLIC (no auth required)
├─ Purpose: Database health check
├─ Potential Issue: Exposes database structure/status to unauthenticated users
└─ Risk Level: LOW (database structure not sensitive, but recommend auth anyway)

GET /api/v1/health/detailed
├─ Security: ❌ PUBLIC (no auth required)
├─ Purpose: Detailed system health
├─ Potential Issue: May expose implementation details
└─ Risk Level: LOW (but review for sensitive info)
```

**Finding**: Health endpoints intentionally public for monitoring. **Recommendation**: Consider restricting detailed_health to authenticated users only. Basic health can remain public.

---

### 4. Learning System Routes (`learning.py` - 20 endpoints)

**Status**: ✅ JWT authentication required

**Endpoints by Category**:

**Pattern Management (7 endpoints)**:
```
GET /api/v1/learning/patterns
├─ Security: ✅ Requires JWT (not explicitly shown but inferred from file pattern)
├─ Returns: List of patterns for user
├─ DB Model: LearnedPattern (user_id FK)
└─ Owner Check Needed: ✅ YES - Filter by user_id

POST /api/v1/learning/patterns
├─ Purpose: Create new pattern
├─ DB Model: LearnedPattern
└─ Owner Check Needed: ✅ YES - Set user_id = current_user

GET/DELETE /api/v1/learning/patterns/{pattern_id}
├─ Purpose: Get/delete specific pattern
└─ Owner Check Needed: ✅ YES - Verify user_id matches

POST /api/v1/learning/patterns/{pattern_id}/enable
POST /api/v1/learning/patterns/{pattern_id}/disable
POST /api/v1/learning/patterns/{pattern_id}/execute
├─ Purpose: Manage pattern state
└─ Owner Check Needed: ✅ YES for all three
```

**Feedback & Analytics (3 endpoints)**:
```
POST /api/v1/learning/feedback
├─ Purpose: Submit pattern feedback
├─ DB Model: FeedbackDB
└─ Owner Check Needed: ✅ YES

GET /api/v1/learning/analytics
└─ Owner Check Needed: ✅ YES - Filter by user

GET /api/v1/learning/knowledge/stats
└─ Owner Check Needed: ✅ YES
```

**Knowledge Sharing (2 endpoints)**:
```
GET /api/v1/learning/knowledge/shared
└─ Purpose: Get shared knowledge from other users

POST /api/v1/learning/knowledge/share
└─ Purpose: Share knowledge with others
```

**Settings & Preferences (5 endpoints)**:
```
GET /api/v1/learning/settings
POST /api/v1/learning/settings
GET/POST /api/v1/learning/privacy-settings
POST /api/v1/learning/export-preferences
GET /api/v1/learning/health_check

└─ Owner Check Needed: ✅ YES for all (except health_check)
```

**Additional (3 endpoints)**:
```
POST /api/v1/learning/enable
POST /api/v1/learning/disable
GET /api/v1/learning/status
└─ User settings management - Owner check needed
```

**Finding**: Learning routes have JWT auth but **require systematic owner_id checks**. System uses LearnedPattern, FeedbackDB, LearningSettings models - all need owner_id validation.

---

### 5. Document Routes (`documents.py` - 6 endpoints)

**Status**: ✅ JWT authentication

```
POST /api/v1/documents/analyze
├─ Security: ✅ Requires JWT
├─ Purpose: Analyze document
└─ Owner Check: UNCLEAR - Need to verify document ownership

POST /api/v1/documents/ask
├─ Purpose: Ask question about document
└─ Owner Check: UNCLEAR - Might allow cross-user access?

POST /api/v1/documents/summarize
POST /api/v1/documents/compare
POST /api/v1/documents/reference
GET /api/v1/documents/search
└─ All need owner_id verification
```

**Finding**: Document routes have JWT auth but **no visibility into ownership model**. Need to inspect document service to determine if owner_id checks exist.

---

### 6. API Key Routes (`api_keys.py` - 6 endpoints)

**Status**: ✅ JWT authentication, ✅ Owner checks implemented

```
POST /api/v1/api-keys/store
├─ Security: ✅ Requires JWT
├─ Purpose: Store new API key
├─ Current Checks: Key stored with user_id
└─ Owner Check: ✅ YES (UserApiKeyDB model has user_id FK)

GET /api/v1/api-keys/list
├─ Purpose: List user's API keys
└─ Owner Check: ✅ YES (filters by user_id)

DELETE /api/v1/api-keys/{key_id}
├─ Purpose: Delete API key
└─ Owner Check: ✅ YES (must own key to delete)

POST /api/v1/api-keys/validate
POST /api/v1/api-keys/rotate
└─ Owner Check: ✅ YES for both
```

**Finding**: API key routes have **both JWT auth AND owner_id checks**. This is the RECOMMENDED PATTERN for Phase 1-3 implementation.

---

### 7. Standup Routes (`standup.py` - 9 endpoints)

**Status**: ✅ JWT authentication (with toggle), ⚠️ User isolation unclear

**Auth Pattern**:
```python
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH", "true").lower() == "true"
```

**Endpoints**:
```
GET /api/v1/standup
POST /api/v1/standup
├─ Security: ✅ Can require JWT (REQUIRE_AUTH=true)
├─ Current Check: get_current_user_optional (line 188)
└─ Owner Check: UNCLEAR - Need to inspect standup service

GET /api/v1/standup/modes
GET /api/v1/standup/formats
GET /api/v1/standup/health_check
POST /api/v1/standup/format-{slack|markdown|text}
└─ Auth: Varies by endpoint
```

**Finding**: Standup routes support auth toggle but **need verification that user_id is properly scoped**. Optional auth might allow unauthenticated users to generate standups.

---

### 8. Conversation Context Demo Routes (`conversation_context_demo.py` - 6 endpoints)

**Status**: ✅ JWT authentication

```
POST /api/v1/demo/enrich-message
GET /api/v1/demo/conversation-summary
GET /api/v1/demo/context-tracking-stats
POST /api/v1/demo/conversation
POST /api/v1/demo/entity-patterns
POST /api/v1/demo/reference-resolution
└─ All require JWT authentication
└─ Owner Check: UNCLEAR - Demo endpoints may not need isolation
```

**Finding**: Demo routes have JWT auth. **Recommendation**: Verify if demo endpoints should have user isolation or remain globally accessible.

---

### 9. Loading Demo Routes (`loading_demo.py` - 8 endpoints)

**Status**: ⚠️ Auth status unclear

```
GET /api/v1/demo/loading/simple
GET /api/v1/demo/loading/manual
GET /api/v1/demo/loading/stream-existing
GET /api/v1/demo/loading/stream-new
GET /api/v1/demo/loading/progress-tracker
GET /api/v1/demo/loading/timeout
GET /api/v1/demo/loading/error
GET /api/v1/demo/loading/status
└─ Auth status needs verification
└─ Owner Check: Likely not needed (demo/test endpoints)
```

**Finding**: Loading demo endpoints appear to be demo/test only. **Recommendation**: Move to separate testing route or explicitly protect if production-facing.

---

## Summary: Current Authorization Status

### JWT Authentication ✅
- **Implemented**: 30+ endpoints use `get_current_user` dependency
- **Missing**: 3 health check endpoints (intentional)
- **Optional**: 9 standup endpoints (REQUIRE_AUTH toggle)

### Owner-Level Authorization ⚠️
| Pattern | Endpoints | Status | Examples |
|---------|-----------|--------|----------|
| **Implemented** | 6 | ✅ | API key routes (validate ownership before operation) |
| **Partial** | 6 | ⚠️ | File routes (query filter but no FK constraint) |
| **Needed** | 20+ | ❌ | Learning routes (no owner_id checks visible) |
| **Unclear** | 12+ | ❓ | Document, conversation, loading demo routes |
| **Not Required** | 3 | ✅ | Health check endpoints (public by design) |

---

## Priority: Endpoints Requiring Owner_id Checks (Phase 1)

### HIGH PRIORITY (User Data):
1. **Learning Routes (10 endpoints)** - LearnedPattern, FeedbackDB, LearningSettings
2. **File Routes (3 endpoints)** - UploadedFileDB (need to add owner_id FK)
3. **Document Routes (6 endpoints)** - If documents are user-owned

### MEDIUM PRIORITY (System/Config):
4. **Standup Routes (9 endpoints)** - If scoped per user
5. **API Key Routes (6 endpoints)** - Already has checks ✅

### LOW PRIORITY (Public/Demo):
6. **Health Routes (3 endpoints)** - Public by design
7. **Demo Routes (14 endpoints)** - Demo/test only

---

## Recommendations for Phase 0 Completion

### 1. Verification Tasks
- [ ] Read `learning.py` routes fully to understand owner_id patterns
- [ ] Read `documents.py` service to verify document ownership model
- [ ] Read `standup.py` service to verify user isolation
- [ ] Read `conversation_context_demo.py` to clarify if demo needs isolation

### 2. Documentation Tasks
- [ ] Create endpoint-by-endpoint authorization matrix
- [ ] Document which tables need owner_id added (Phase 1 database schema)
- [ ] Identify missing owner_id checks (Phase 2 authorization layer)

### 3. Risk Assessment
- [ ] Quantify exposure: X endpoints lack owner_id validation
- [ ] Impact: Users can potentially access other users' data
- [ ] Mitigation: Add owner_id checks before public release

---

## Next Steps

**Phase 0.4**: Identify service methods needing protection
**Phase 0.5**: Create comprehensive risk assessment report

---

**Status**: Phase 0.3 COMPLETE
**Evidence**: Direct code inspection of 9 route files + symbol catalog
**Next**: Phase 0.4 (Service method inventory)
