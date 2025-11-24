# Chief Architect Report: Alpha Testing Blockers

**Date**: October 30, 2025 (5:41 PM PT)
**Reporter**: Claude Code (Programmer Agent)
**Session**: Alpha Testing - First User Session
**Status**: 🔴 **CRITICAL BLOCKERS IDENTIFIED**
**Tester**: alpha-one (xian's test laptop)

---

## Executive Summary

**Achievement**: ✅ First alpha user successfully onboarded and running Piper
**Blocker**: ❌ Web application has zero user identity/authentication architecture
**Impact**: No personalized features work; production data leaks to all users
**Root Cause**: 75% complete pattern - alpha_users table exists but web app doesn't use it

**Recommendation**: Halt alpha testing until CORE-ALPHA-AUTH issues resolved (~4-8 hours of focused architectural work)

---

## What Works ✅

1. **Alpha User Onboarding** - E2E test passing
   - Setup wizard creates alpha_users records
   - Preferences stored in alpha_users.preferences JSONB
   - API keys stored with UUID→String compatibility
   - Database isolation working (alpha_users vs users tables)

2. **Basic Web UI** - Loads and accepts input
   - React frontend renders
   - Can send messages to `/api/v1/intent`
   - Generic responses work (CONVERSATION intent)

3. **Infrastructure** - All services running
   - PostgreSQL (port 5433)
   - FastAPI web server (port 8001)
   - Service container initialized
   - No crashes or startup failures

---

## Critical Blockers 🔴

### BLOCKER #1: No User Identity in HTTP Layer

**Severity**: CRITICAL - Security & Privacy Issue
**Impact**: Production data leaks to all users

**Technical Details**:
```python
# Current: web/app.py line 579-628
@app.post("/api/v1/intent")
async def process_intent(request: Request):
    request_data = await request.json()
    message = request_data.get("message", "")
    session_id = request_data.get("session_id", "default_session")
    # ❌ NO USER CONTEXT EXTRACTED

    result = await intent_service.process_intent(
        message=message,
        session_id=session_id
        # ❌ NO USER_ID PASSED
    )
```

**What's Missing**:
- No JWT/session token validation
- No user_id extraction from request
- No authentication middleware
- No way to identify which alpha user is making request

**Evidence**:
- Screenshot #1: "What tasks do I have?" returns PM's production projects
- Screenshot #3: "What's my current status?" shows PM's Q4 goals
- Data matches `config/PIPER.md` exactly (VA/Decision Reviews, DRAGONS team, Kind Systems)

**Files Affected**:
- `web/app.py` - HTTP endpoint (line 579-628)
- `services/intent/intent_service.py` - Service signature (line 94-275)
- All downstream intent handlers

---

### BLOCKER #2: Global Config Fallback Leaks Production Data

**Severity**: CRITICAL - Data Privacy Violation
**Impact**: All users see PM's personal/confidential projects

**Technical Details**:
```python
# services/user_context_service.py line 31-61
async def get_user_context(self, session_id: str) -> UserContext:
    # Loads from config/PIPER.md for ALL sessions
    context = await self._load_context_from_config(session_id)
    # ❌ Same config file for every user
    return context
```

**Data Leakage Source**: `config/PIPER.md` contains:
```markdown
## 👤 **User Context**
**Name**: Christian
**Role**: Product Manager / Developer

## 🎯 **Current Focus (Q4 2025)**
**Primary Objective**: VA/Decision Reviews Q4 Onramp implementation

## 📊 **Project Portfolio**
**VA/Decision Reviews Q4 Onramp (70%)** - Primary project
- Company Context: Kind Systems company initiative
- Team Context: DRAGONS team collaboration
```

**Evidence**:
- Alpha user queries return Christian's projects verbatim
- No per-user configuration isolation
- No database-backed user context

**Files Affected**:
- `config/PIPER.md` - Hardcoded production data
- `services/user_context_service.py` - Loads same config for all
- `services/configuration/piper_config_loader.py` - File-based only

---

### BLOCKER #3: Intent Handlers Cannot Access User Data

**Severity**: HIGH - Core Feature Broken
**Impact**: No personalization, preferences, or user-specific queries work

**Technical Details**:
```python
# services/intent_service/canonical_handlers.py
async def handle(self, intent: Intent, session_id: str):
    # ❌ No user_id parameter
    # Cannot query alpha_users table
    # Cannot retrieve preferences
    # Cannot identify user
```

**What Cannot Work**:
- "Who am I?" - No user_id to query alpha_users
- "What are my preferences?" - No user_id to query alpha_users.preferences
- "What are my tasks?" - No user_id to filter by
- Any personalized response

**Evidence**:
- Screenshot #2: "Who am I?" returns generic intro
- Screenshot #2: "What are my preferences?" returns generic intro
- No user recognition in any response

**Files Affected**:
- `services/intent_service/canonical_handlers.py` - All handlers
- `services/intent/intent_service.py` - All query handlers
- Any service expecting user context

---

## High Priority Issues 🟡

### Issue #4: File Upload Endpoint Missing

**Severity**: HIGH - Feature Completely Broken
**Impact**: Cannot test file summarization, document analysis

**Evidence**:
- Screenshot #2: "Upload Failed: Not Found"
- No `/api/upload` or `/api/v1/upload` endpoint found in codebase
- File upload UI exists but backend missing

**Files Affected**:
- `web/app.py` - No upload route defined
- Frontend expects upload capability

---

### Issue #5: Todo Creation API Error

**Severity**: HIGH - Core Feature Broken
**Impact**: Cannot create todos/tasks

**Evidence**:
- Screenshot #1: "An API error occurred" when creating todo
- Likely FK constraint or missing user_id

**Probable Causes**:
1. Todo endpoint requires user_id (doesn't have it)
2. Database FK constraint to users table (alpha user has UUID)
3. Missing error handling

**Files Affected**:
- Unknown - needs server log investigation
- Likely todo creation endpoint

---

### Issue #6: Feature Discovery Broken

**Severity**: MEDIUM - UX/Discoverability
**Impact**: Users don't know what Piper can do

**Evidence**:
- Screenshot #3: "What can you help me with?" returns generic intro
- No comprehensive feature menu
- No guided onboarding

**Files Affected**:
- `services/intent_service/canonical_handlers.py` - GUIDANCE handler

---

## Architectural Analysis

### The 75% Complete Pattern

**What Exists**:
```
✅ alpha_users table (UUID PKs)
✅ alpha_users.preferences (JSONB column)
✅ Setup wizard (creates alpha users)
✅ Preferences questionnaire (stores to alpha_users)
✅ E2E tests (all passing)
```

**What's Missing**:
```
❌ Web app authentication/authorization
❌ User session management (JWT/cookies)
❌ User context in HTTP requests
❌ User context in service layer
❌ Per-user data isolation
```

**Current Architecture**:
```
[Web UI] → [HTTP /api/v1/intent] → [IntentService] → [Handlers]
            ↓                        ↓                  ↓
         session_id only       No user context    Falls back to
         No user_id           No database access   PIPER.md config
```

**Required Architecture**:
```
[Web UI + Auth] → [HTTP /api/v1/intent + user] → [IntentService + user] → [Handlers + user]
     ↓                      ↓                           ↓                        ↓
  JWT token          Extract user_id             Query alpha_users       User-specific data
  in cookie          from session                Load preferences        Filter by user_id
```

---

## Proposed GitHub Issues

### Issue #1: CORE-ALPHA-AUTH-SESSION (BLOCKER)

**Title**: Implement user authentication and session management for alpha users

**Priority**: 🔴 P0 - BLOCKER
**Estimate**: 3-4 hours
**Dependencies**: None

**Description**:

Web application has no user authentication or session management. All requests are anonymous, making it impossible to:
- Identify which alpha user is making a request
- Retrieve user-specific data from alpha_users table
- Apply user preferences
- Isolate user data

**Acceptance Criteria**:
- [ ] User login flow (username/password or simple auth)
- [ ] JWT token generation and validation
- [ ] Session middleware extracts user_id from token
- [ ] `/api/v1/intent` endpoint receives user_id
- [ ] User session persisted across page reloads

**Technical Approach**:
1. Add `/api/v1/auth/login` endpoint
2. Query alpha_users table by username
3. Generate JWT with user_id (UUID)
4. Store JWT in HTTP-only cookie
5. Add auth middleware to extract user from JWT
6. Pass user_id to all intent handlers

**Files to Modify**:
- `web/app.py` - Add auth routes and middleware
- `web/api/routes/auth.py` - Already exists, needs integration
- `services/intent/intent_service.py` - Add user_id parameter

**Evidence**: Screenshots #1, #2, #3 all show zero user recognition

---

### Issue #2: CORE-ALPHA-USER-CONTEXT (BLOCKER)

**Title**: Pass user context through intent processing pipeline

**Priority**: 🔴 P0 - BLOCKER
**Estimate**: 2-3 hours
**Dependencies**: #1 (CORE-ALPHA-AUTH-SESSION)

**Description**:

IntentService and all intent handlers receive only `session_id`, not `user_id`. This prevents:
- Querying alpha_users table
- Retrieving user preferences
- Personalizing responses
- Filtering data by user

**Acceptance Criteria**:
- [ ] `IntentService.process_intent()` accepts `user_id` parameter
- [ ] All canonical handlers receive user context
- [ ] All query handlers receive user context
- [ ] User context includes alpha_users record and preferences
- [ ] "Who am I?" returns actual user info from alpha_users table

**Technical Approach**:
1. Update `process_intent(message, session_id, user_id)` signature
2. Create `UserContext` object from alpha_users query
3. Pass user context to all handlers
4. Update canonical handlers to use user context
5. Update query handlers to filter by user_id

**Files to Modify**:
- `services/intent/intent_service.py` (line 94-275)
- `services/intent_service/canonical_handlers.py` (all handlers)
- `web/app.py` (line 579-628) - Pass user_id from auth

**Evidence**: Screenshot #2 shows "Who am I?" cannot identify user

---

### Issue #3: CORE-ALPHA-DATA-ISOLATION (BLOCKER)

**Title**: Remove production data leakage via PIPER.md fallback

**Priority**: 🔴 P0 - BLOCKER (Security/Privacy)
**Estimate**: 1-2 hours
**Dependencies**: #2 (CORE-ALPHA-USER-CONTEXT)

**Description**:

All users see PM's production projects because `UserContextService` loads from `config/PIPER.md` for everyone. This leaks:
- PM's personal projects (VA/Decision Reviews, DRAGONS team, Kind Systems)
- PM's working hours, timezone, calendar
- PM's strategic goals and priorities
- Confidential company information

**Acceptance Criteria**:
- [ ] Alpha users see ONLY their own data (no PIPER.md fallback)
- [ ] User context loaded from alpha_users table, not file
- [ ] Projects/tasks filtered by user_id
- [ ] "What's my status?" shows user's actual status, not PM's
- [ ] Config file clearly marked as DEV-ONLY with warning

**Technical Approach**:
1. Create database-backed UserContextService
2. Load user info from alpha_users table
3. Load preferences from alpha_users.preferences JSONB
4. Remove or disable PIPER.md for alpha environment
5. Add clear warning to PIPER.md about production data

**Files to Modify**:
- `services/user_context_service.py` - Query database instead of file
- `config/PIPER.md` - Add DEV-ONLY warning or move to .gitignore
- Any query handler using UserContextService

**Evidence**: Screenshots #1, #3 show PM's production projects to alpha user

---

### Issue #4: CORE-ALPHA-FILE-UPLOAD (HIGH)

**Title**: Implement file upload endpoint for alpha testing

**Priority**: 🟡 P1 - HIGH
**Estimate**: 2-3 hours
**Dependencies**: #1 (for user_id to track uploads)

**Description**:

File upload UI exists but backend endpoint missing. Upload fails with "Not Found" error.

**Acceptance Criteria**:
- [ ] `/api/v1/upload` endpoint accepts file uploads
- [ ] Files stored in user-specific directory structure
- [ ] uploaded_files table records metadata (with user_id FK)
- [ ] Returns upload success with file_id
- [ ] File summarization flow works end-to-end

**Technical Approach**:
1. Create `/api/v1/upload` POST endpoint
2. Use FastAPI UploadFile handling
3. Store files in `uploads/{user_id}/{file_id}`
4. Record metadata in uploaded_files table
5. Return file_id for subsequent queries

**Files to Create**:
- `web/api/routes/upload.py` - Upload endpoint
- File storage service (if doesn't exist)

**Files to Modify**:
- `web/app.py` - Include upload router

**Evidence**: Screenshot #2 shows "Upload Failed: Not Found"

---

### Issue #5: CORE-ALPHA-TODO-API (HIGH)

**Title**: Fix todo creation API error for alpha users

**Priority**: 🟡 P1 - HIGH
**Estimate**: 1-2 hours
**Dependencies**: #1 (for user_id), investigate server logs

**Description**:

Creating todos fails with "An API error occurred". Likely causes:
- Missing user_id in request
- FK constraint violation (alpha UUID vs users String)
- Endpoint expects different payload

**Acceptance Criteria**:
- [ ] Server logs reviewed to identify exact error
- [ ] Todo creation works for alpha users
- [ ] Todos stored with alpha_users.id (UUID)
- [ ] "Add a todo" flow completes successfully

**Technical Approach**:
1. Review server logs for actual error
2. Fix root cause (likely user_id or FK issue)
3. Ensure todos table supports alpha_users UUIDs
4. Add error handling and user feedback

**Files to Investigate**:
- Server logs from 1:37 PM PT session
- Todo creation endpoint
- Database schema (todos table)

**Evidence**: Screenshot #1 shows "An API error occurred"

---

### Issue #6: CORE-ALPHA-FEATURE-MENU (MEDIUM)

**Title**: Add comprehensive feature menu to GUIDANCE intent

**Priority**: 🟢 P2 - MEDIUM
**Estimate**: 1 hour
**Dependencies**: None (can be done independently)

**Description**:

"What can you help me with?" returns generic intro instead of feature list. Users don't know what Piper can do.

**Acceptance Criteria**:
- [ ] GUIDANCE handler returns comprehensive feature menu
- [ ] Menu includes all supported intent categories
- [ ] Examples provided for each feature
- [ ] Menu personalized by user role/preferences (future)

**Technical Approach**:
1. Update GUIDANCE canonical handler
2. Return markdown list of features
3. Group by intent category (QUERY, EXECUTION, etc.)
4. Add examples for each

**Files to Modify**:
- `services/intent_service/canonical_handlers.py` - GUIDANCE handler

**Evidence**: Screenshot #3 shows generic intro instead of feature list

---

## Testing Readiness Assessment

### Flows That Can Be Tested NOW (No Fixes Needed):
- ✅ Basic conversation (works)
- ✅ Generic help (works but not useful)

### Flows Blocked by Issue #1 (Auth/Session):
- ❌ All personalized features
- ❌ User identity queries
- ❌ User-specific data

### Flows Blocked by Issue #2 (User Context):
- ❌ Preferences queries
- ❌ Status queries
- ❌ Any database lookups by user

### Flows Blocked by Issue #3 (Data Isolation):
- ❌ Project queries (shows wrong data)
- ❌ Task queries (shows wrong data)
- ❌ Status queries (shows wrong data)

### Flows Blocked by Issue #4 (File Upload):
- ❌ File summarization
- ❌ Document analysis

### Flows Blocked by Issue #5 (Todo API):
- ❌ Todo/task creation
- ❌ Any EXECUTION intents

**Estimated Alpha-Ready**: After Issues #1, #2, #3 resolved (6-9 hours)

---

## Recommended Approach

### Phase 1: Auth & Context (BLOCKERS - 6-9 hours)

**Sprint Goal**: Alpha users can be identified and see their own data

**Issues**:
1. CORE-ALPHA-AUTH-SESSION (3-4h)
2. CORE-ALPHA-USER-CONTEXT (2-3h)
3. CORE-ALPHA-DATA-ISOLATION (1-2h)

**Outcome**:
- Alpha users log in
- System knows who they are
- They see their own data, not PM's

**Test Plan**:
- Login as alpha-one
- "Who am I?" returns "alpha-one"
- "What's my status?" shows empty (no projects yet)
- No production data visible

### Phase 2: Core Features (HIGH - 3-5 hours)

**Sprint Goal**: File upload and todo creation work

**Issues**:
4. CORE-ALPHA-FILE-UPLOAD (2-3h)
5. CORE-ALPHA-TODO-API (1-2h)

**Outcome**:
- Can upload files
- Can create todos
- Basic EXECUTION intents work

### Phase 3: UX Polish (MEDIUM - 1 hour)

**Sprint Goal**: Better onboarding/discovery

**Issues**:
6. CORE-ALPHA-FEATURE-MENU (1h)

**Outcome**:
- Users know what Piper can do
- Better first-use experience

---

## Risk Assessment

### If We Don't Fix Blockers:

**Security Risks**:
- ❌ Production data leaked to all alpha users
- ❌ No user isolation
- ❌ Confidential company info exposed

**Testing Risks**:
- ❌ Cannot test ANY personalized features
- ❌ Cannot test user preferences
- ❌ Cannot validate alpha_users architecture
- ❌ Most flows will fail with same root cause

**Timeline Risks**:
- ❌ Repeated bug reports for same issue
- ❌ Alpha testers frustrated by non-functional app
- ❌ Cannot invite additional alpha users safely

### If We Fix Blockers First:

**Benefits**:
- ✅ Proper foundation for all future features
- ✅ Safe to invite more alpha users
- ✅ Can test real user flows
- ✅ Validates entire alpha architecture end-to-end

**Estimated Timeline**:
- **Phase 1**: 6-9 hours → Ready for basic testing
- **Phase 2**: +3-5 hours → Ready for full alpha testing
- **Total**: 1-2 days of focused work

---

## Conclusion

**Current State**:
- Infrastructure: ✅ Working
- Onboarding: ✅ Working
- Web App: ❌ No user architecture

**Blocker Summary**:
- 3 critical blockers (auth, context, isolation)
- 2 high priority issues (upload, todos)
- 1 medium priority issue (feature menu)

**Recommendation**:
Execute Phase 1 (Issues #1-3) before resuming alpha testing. This builds the foundation that ALL other features depend on.

**Next Steps**:
1. Chief Architect reviews this report
2. Decide: Build auth now, or pivot to different architecture?
3. Create GitHub issues for approved work
4. Execute Phase 1 sprint
5. Resume alpha testing with proper user architecture

---

**Report Compiled**: October 30, 2025 5:41 PM PT
**Investigation Method**: Serena MCP symbolic code analysis
**Files Analyzed**: 15+ source files across web, services, and configuration
**Evidence**: 3 screenshots from alpha-one test session
**Session Duration**: 6 hours (onboarding + testing + investigation)

🎂 **Happy Birthday Achievement**: First alpha user onboarded successfully! Foundation is solid, just needs the user layer.
