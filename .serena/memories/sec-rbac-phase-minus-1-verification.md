# SEC-RBAC Phase -1: Infrastructure Verification (COMPLETED)

**Date**: 2025-11-21 (4:16 PM)
**Status**: ✅ VERIFIED - All Phase -1 questions answered
**Method**: Serena symbolic tools + codebase inspection

---

## Phase -1 Question 1: Which resource tables need owner_id?

### ANSWER: 12 tables need owner_id

**Already HAVE owner_id** (3 tables):
1. `todo_lists` - TodoListDB
2. `lists` - ListDB
3. `todo_items` - TodoDB

**NEED owner_id ADDED** (9 tables):
1. `projects` - ProjectDB
2. `project_integrations` - ProjectIntegrationDB
3. `uploaded_files` - UploadedFileDB
4. `knowledge_nodes` - KnowledgeNodeDB
5. `knowledge_edges` - KnowledgeEdgeDB
6. `list_memberships` - ListMembershipDB
7. `list_items` - ListItemDB
8. `feedback` - FeedbackDB
9. `personality_profiles` - PersonalityProfileModel

**ALSO CONSIDER**:
10. `learned_patterns` - LearnedPattern (user-specific patterns)
11. `learning_settings` - LearningSettings (user-specific settings)
12. `items` - ItemDB (parent class, may not need direct owner_id if items are polymorphic)

**Key Finding**: Owner_id is currently String type, not UUID. Need consistency check with User.id (which is UUID).

**Location**: `/services/database/models.py`

---

## Phase -1 Question 2: Where are the API endpoints defined?

### ANSWER: `/web/api/routes/` with router pattern

**Primary Location**: `/Users/xian/Development/piper-morgan/web/api/routes/`

**Route Files Found**:
- `auth.py` - Authentication endpoints
- `files.py` - File management endpoints
- `health.py` - Health check endpoint
- `learning.py` - Learning system endpoints (52KB - large)
- `documents.py` - Document endpoints
- `standup.py` - Standup endpoints (24KB)
- `api_keys.py` - API key management
- `conversation_context_demo.py` - Demo endpoints
- `loading_demo.py` - Demo endpoints

**Framework**: FastAPI (confirmed in `/web/app.py`)

**Pattern**: Uses FastAPI APIRouter pattern to define routes

**Key Finding**: Multiple route files means need to catalog all @app and @router decorators across all files.

---

## Phase -1 Question 3: Verify User model exists with ID field

### ANSWER: ✅ YES - User model fully verified

**Location**: `/services/database/models.py:54-118`

**Key Fields**:
```python
class User(Base):
    __tablename__ = "users"

    # PRIMARY KEY - UUID
    id = Column(postgresql.UUID(as_uuid=True),
               primary_key=True,
               default=uuid.uuid4)  # ✅ UUID type

    # ALREADY HAS ROLE FIELD
    role = Column(String(50), default="user", nullable=False)  # ✅

    # STATUS FLAGS
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_alpha = Column(Boolean, default=False)

    # RELATIONSHIPS
    personality_profiles = relationship(...)
    api_keys = relationship(...)
    blacklisted_tokens = relationship(...)
    feedback = relationship(...)
    learned_patterns = relationship(...)
    learning_settings = relationship(...)
```

**Important Notes**:
- User.id is UUID type (not String) - owner_id fields should match this type
- User already has `role` field with "user" default
- Has relationships to multiple tables for cascading deletes
- AuditLog relationship is currently disabled (no FK constraint)

---

## Phase -1 Question 4: Identify service methods needing protection

### ANSWER: Multiple service layers identified

**Service Files Found**:
1. `/services/auth/user_service.py` - User authentication
2. `/services/auth/jwt_service.py` - JWT token management
3. `/services/feedback/feedback_service.py` - Feedback handling
4. `/services/todo/todo_management_service.py` - Todo operations
5. `/services/todo/todo_knowledge_service.py` - Todo knowledge
6. `/services/item_service.py` - Item operations
7. `/services/user_context_service.py` - User context handling
8. `/services/knowledge_graph/document_service.py` - Document management
9. `/services/security/user_api_key_service.py` - API key management
10. `/services/security/key_audit_service.py` - Security audit
11. Various integration services (Slack, GitHub, Notion, Calendar, etc.)

**Repository Layer** (data access):
1. `/services/repositories/file_repository.py`
2. `/services/repositories/todo_repository.py`
3. `/services/repositories/universal_list_repository.py`

**Key Finding**: Service methods typically receive parameters but don't currently validate ownership. Need to add authorization checks to all CRUD operations.

---

## Phase -1 Question 5: Understand JWT implementation details

### ANSWER: ✅ Sophisticated JWT system in place

**Location**: `/services/auth/jwt_service.py`

**JWT Implementation Details**:

**Standard Claims** (RFC 7519):
- `iss` (Issuer): "piper-morgan"
- `aud` (Audience): "piper-morgan-api" or specific service
- `sub` (Subject): User ID
- `exp` (Expiration): Unix timestamp
- `iat` (Issued At): Unix timestamp
- `jti` (JWT ID): Unique token identifier

**Custom Piper Morgan Claims**:
- `user_id` - UUID of user
- `user_email` - User email
- `scopes` - List of permission strings
- `token_type` - TokenType enum (ACCESS, REFRESH, API, FEDERATION)
- `session_id` - Optional session tracking
- `workspace_id` - Optional multi-tenant support
- `mcp_compatible` - Boolean flag for MCP protocol compatibility

**Token Types Supported**:
- ACCESS - For API access
- REFRESH - For refreshing access tokens
- API - For API key tokens
- FEDERATION - For OAuth federation

**Token Blacklist System**:
- Implemented in `/services/auth/token_blacklist.py`
- Uses Redis with database fallback
- Stores token ID (JTI claim), not full token
- Used for logout/revocation

**Auth Middleware**:
- Location: `/services/auth/auth_middleware.py`
- Uses HTTPBearer security scheme
- Extracts "Bearer <token>" from Authorization header
- Already validates JWT signature

**Key Finding**: JWT system is production-ready with proper separation of concerns. Authorization layer can be cleanly added on top without modifying JWT structure.

---

## Summary Table: Phase -1 Verification

| Question | Status | Answer |
|----------|--------|--------|
| Resource tables needing owner_id | ✅ ANSWERED | 12 tables: 3 already have it, 9 need it |
| API endpoint locations | ✅ ANSWERED | `/web/api/routes/` - 9 route files found |
| User model with ID | ✅ CONFIRMED | UUID type, has role field already |
| Service methods | ✅ IDENTIFIED | 11+ service files, 3 repository files |
| JWT implementation | ✅ VERIFIED | Sophisticated system with standard + custom claims |

---

## Remaining Gaps / Clarifications Needed

### Gap 1: owner_id Type Mismatch ⚠️
- **Issue**: Existing owner_id fields are String type
- **User.id**: UUID type
- **Decision Needed**: Should new owner_id be String (consistent with existing) or UUID (consistent with User.id)?
- **Recommendation**: Use UUID for new tables, consider migration for existing

### Gap 2: Exact Resource Scope ⚠️
- **Issue**: 9+ tables need owner_id, but PM should confirm priority order
- **Decision Needed**: Which tables are in scope for Phase 1 vs post-alpha?
- **Question for PM**: Are all 12 tables required for alpha, or just critical ones?

### Gap 3: Service Method Catalog ⚠️
- **Issue**: Found 11+ service files, but not exhaustively cataloged every method
- **Decision**: Phase 0 (Security Audit) will systematically catalog all service methods
- **Not blocking**: Can proceed with Phase 0 audit to discover exact counts

### Gap 4: Data Backfill Strategy ⚠️
- **Issue**: Existing data in 3 tables that already have owner_id - how was it backfilled?
- **Decision Needed**: What strategy for backfilling owner_id on 9 new tables?
- **Options**:
  1. Assign all existing data to first admin user
  2. Assign all existing data to system user
  3. Mark as null (allow null migration, then enforce non-null later)
  4. Manual PM decision per table

### Gap 5: Shared Resources ⚠️
- **Issue**: Some resources might be shared between users (e.g., list_memberships)
- **Decision Needed**: How to handle resources with multiple users?
- **Example**: A todo list shared with multiple users - who is owner_id?

---

## Recommendations for Proceeding

### ✅ CLEAR TO PROCEED TO PHASE 0 (Security Audit)
- Infrastructure is compatible
- User model exists with proper ID
- JWT system is sophisticated but non-blocking
- Can do comprehensive security audit now

### BEFORE PHASE 1 (Database Schema):
1. **PM Clarifies**:
   - Which 12 tables are in scope (all or subset)?
   - owner_id type: String or UUID?
   - Backfill strategy for existing data
   - Handling of shared resources

2. **Code Review**: Validate which tables actually hold user-owned data

---

## Infrastructure Readiness: ✅ APPROVED FOR PHASE 0

All Phase -1 infrastructure questions answered. No blockers found.

**Next Step**: Proceed to Phase 0 (Security Audit) to:
- Enumerate ALL API endpoints with protection status
- Identify ALL service methods accessing user data
- Document current auth/authz gaps
- Create comprehensive risk assessment

---

**Verified By**: Claude Code (Programmer Agent)
**Method**: Serena symbolic tools + direct codebase inspection
**Confidence**: High - source verified
