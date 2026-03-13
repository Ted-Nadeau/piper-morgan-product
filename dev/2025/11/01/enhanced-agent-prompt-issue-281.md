# Enhanced Claude Code Prompt: CORE-ALPHA-WEB-AUTH (#281)

**Date**: November 1, 2025, 9:13 AM PT (Enhanced)
**Original**: 7:00 AM PT
**Updates**: Aligned with #280 (data isolation) and #282 (file upload auth patterns)

---

## CRITICAL UPDATES FROM MORNING WORK

### Context from Issue #280 (Data Isolation)
**Completed 8:45 AM** - Alpha database architecture clarified:

- ✅ `alpha_users` table exists and working
- ✅ User preferences in `alpha_users.preferences` (JSONB)
- ✅ Each user isolated by `user_id`
- ✅ UserContextService loads user-specific data
- ✅ See: ADR-040 for architecture decisions

**Important**: Your auth system will follow this same isolation pattern.

### Context from Issue #282 (File Upload)
**Completed 8:50 AM** - File upload uses this auth pattern:

```python
# This is the pattern YOU will implement
from fastapi import Depends

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """Get current authenticated user from JWT token"""
    # Your implementation here
```

**Files already using this dependency**:
- `web/api/routes/files.py` line 42: `current_user: dict = Depends(get_current_user)`
- Pattern: User-isolated storage in `uploads/{user_id}/`

**Critical**: Issue #282 is BLOCKED waiting for your auth implementation. File upload works but can't be tested until JWT auth is ready.

---

## Updated Phase -1: Verify Infrastructure

**Additional checks based on morning work**:

```python
# 1. Verify alpha_users table (from #280)
serena.view_file("services/database/models.py")
# Look for: AlphaUser class with password_hash field

# 2. Check existing file upload auth pattern (from #282)
serena.view_file("web/api/routes/files.py", view_range=[1, 50])
# See how get_current_user is referenced (YOU will implement this)

# 3. Verify user isolation patterns
serena.find_referencing_symbols("user_id")
# Should find: uploads/{user_id}/, alpha_users.preferences, etc.
```

---

## Updated Security Checklist

**Align with existing user isolation**:

- [ ] JWT `user_id` matches `alpha_users.id` (UUID format)
- [ ] Session isolation follows #282 pattern (user-scoped resources)
- [ ] UserContextService integration (optional, can defer)
- [ ] File upload routes work with your auth (verify #282 tests)

---

## Updated Testing Section

### Additional Test 7: Verify File Upload Auth Integration

After completing #281, verify #282 can be tested:

```bash
# 1. Login and get token
TOKEN=$(curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "test123"}' \
  | jq -r '.token')

# 2. Test file upload (from #282)
curl -X POST http://localhost:8001/api/v1/files/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.txt"

# Expected: File uploads successfully, stored in uploads/xian/

# 3. Verify user isolation
curl -X GET http://localhost:8001/api/v1/files/list \
  -H "Authorization: Bearer $TOKEN"

# Expected: Only xian's files returned
```

**Why this matters**: Issue #282 is complete but blocked on your auth. This test proves the integration works.

---

## Updated Success Criteria

**Add these to original checklist**:

- [ ] `get_current_user` dependency works with file upload routes
- [ ] JWT payload includes `user_id` (matches alpha_users.id)
- [ ] User isolation verified (uploads, preferences, sessions)
- [ ] File upload tests passing (from #282)
- [ ] UserContextService can use JWT user_id (if integrated)

---

## Architecture Alignment Notes

### From ADR-040 (Database Architecture)

Your auth system fits into this pattern:

```
Login Request
    ↓
JWT Token Generated (with user_id)
    ↓
Protected Endpoint Called
    ↓
get_current_user() validates token
    ↓
Extract user_id from JWT payload
    ↓
Query alpha_users table (your database)
    ↓
User-specific resources loaded
```

**Database Sessions**: Use existing async database session pattern:
```python
from services.database.connection import get_db_session

async with get_db_session() as db:
    result = await db.execute(
        select(AlphaUser).where(AlphaUser.username == username)
    )
    user = result.scalar_one_or_none()
```

### From #282 (File Upload Pattern)

Your `get_current_user` will be used like this:

```python
# Pattern used in web/api/routes/files.py
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)  # YOUR CODE
) -> dict:
    user_id = current_user["user_id"]
    # Use user_id for isolation
```

**Return format from get_current_user should be**:
```python
{
    "user_id": "uuid-string",  # From alpha_users.id
    "username": "xian",        # From alpha_users.username
    # Optional: "preferences": {...}
}
```

---

## Files That Will Use Your Auth

**Already waiting for your implementation**:
1. `web/api/routes/files.py` (Issue #282) ✅ Ready
2. `web/app.py` (main app routing)
3. Future: Document processing routes (post-#281)

**Pattern they expect**:
```python
from web.middleware.auth import get_current_user

@router.post("/some-endpoint")
async def endpoint(
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]
    username = current_user["username"]
    # Your user-isolated logic here
```

---

## Questions Answered from Morning Work

**Q: Does alpha_users.password_hash exist?**
A: YES - field exists, currently NULL for all users except xian (who was manually set)

**Q: What user isolation pattern?**
A: user_id-based - see `uploads/{user_id}/` pattern from #282

**Q: Database session management?**
A: Use `get_db_session()` async context manager - proven pattern

**Q: Any existing auth to build on?**
A: NO - you're implementing from scratch, but #282 shows expected pattern

---

## Evidence Updates

**Additional evidence to provide**:

1. **Integration with #282**:
   ```bash
   # After implementing auth, test file upload
   python -m pytest tests/api/test_files_integration.py
   # Expected: All tests pass with auth
   ```

2. **User Isolation Proof**:
   ```bash
   # Login as two different users
   # Upload files as each
   # Verify: ls uploads/ shows separate user directories
   # Verify: Each user sees only their files via API
   ```

---

## Original Prompt Sections

**Everything below this line is from your original prompt** and remains valid. The updates above enhance it with context from #280 and #282.

---

[... rest of original prompt follows unchanged ...]

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

[Continue with all original prompt sections from line 59 onwards...]

---

## Summary of Enhancements

**What's new**:
1. ✅ Context from #280 (alpha_users, user isolation, ADR-040)
2. ✅ Context from #282 (file upload auth dependency pattern)
3. ✅ Test 7 added (verify file upload integration)
4. ✅ Architecture alignment notes
5. ✅ User isolation verification steps
6. ✅ get_current_user return format specified

**What's unchanged**:
- All original implementation steps (Checkpoints 1-7)
- All original tests (1-6)
- Security checklist
- Time estimates (6-8 hours)
- Evidence requirements

**Net result**: Same great prompt, now aligned with morning's architectural decisions and ready to unblock #282 testing!

---

**Ready to deploy with Sonnet 4.5!** 🔐🏰
