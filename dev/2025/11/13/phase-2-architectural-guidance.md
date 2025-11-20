# Architectural Guidance: Phase 2 Implementation
## Issue #300 - User Controls API

**Date**: November 13, 2025, 7:25 AM PT
**From**: Lead Developer
**To**: Code Agent
**Re**: Sprint A5 vs Phase 2 Architecture

---

## 🎯 Architectural Decision: Coexist with Clear Separation

### The Situation

**What Code Agent Discovered** (using Serena - excellent!):
- `web/api/routes/learning.py` already exists from Sprint A5
- Contains 15 file-based learning endpoints
- Phase 2 needs to add 7 database-backed endpoints
- Potential architectural conflict

**Options Considered**:
1. Replace Sprint A5 endpoints → Loses work
2. Coexist at same level → Confusing
3. Refactor Sprint A5 → Too much scope
4. Separate paths → Clean separation

---

## ✅ Decision: Option D+ (Hybrid with Pragmatism)

### Implementation Strategy

**Sprint A5 Endpoints** (Ignore for Now):
- **Path**: `/api/v1/learning/*` (root level)
- **Backend**: QueryLearningLoop (file-based)
- **Status**: Legacy/experimental from Sprint A5
- **Action**: **Leave as-is, don't modify**
- **Future**: May deprecate later if not used

**Phase 2 Endpoints** (Your Focus):
- **Path**: `/api/v1/learning/patterns/*` (subpath)
- **Path**: `/api/v1/learning/settings` (subpath)
- **Backend**: LearningHandler + LearnedPattern (database)
- **Status**: Production implementation
- **Action**: **Add these to same file**

### Why This Works

✅ **Clean Separation**: Different subpaths (`patterns/*` vs root `/*`)
✅ **No Conflicts**: Sprint A5 endpoints won't interfere
✅ **Focus**: Phase 2 stays focused on new system
✅ **Pragmatic**: Don't waste time refactoring legacy code
✅ **Future-Proof**: Can remove Sprint A5 endpoints later if needed

---

## 🛠️ Implementation Instructions

### Phase 2.0: Add Endpoints to Existing File

**File**: `web/api/routes/learning.py` (already exists)

**Steps**:

1. **Read existing file with Serena**:
   ```python
   mcp__serena__get_symbols_overview("web/api/routes/learning.py")
   ```

2. **Add clear separation comment**:
   ```python
   # ============================================
   # Sprint A5 Endpoints (File-based - Legacy)
   # Status: Experimental, may be deprecated
   # ============================================

   [existing 15 endpoints stay here - DON'T MODIFY]

   # ============================================
   # Issue #300 Phase 2 - Database-backed Pattern Management
   # Status: Production implementation
   # Backend: LearningHandler + LearnedPattern model
   # ============================================

   [NEW Phase 2 endpoints go here]
   ```

3. **Add imports at top**:
   ```python
   from services.learning.learning_handler import LearningHandler
   from services.database.models import LearnedPattern, LearningSettings
   from services.database.session import get_db
   from sqlalchemy.ext.asyncio import AsyncSession
   ```

4. **Add 7 new endpoints** (below existing ones):
   ```python
   # Pattern Management
   @router.get("/patterns")
   @router.get("/patterns/{pattern_id}")
   @router.delete("/patterns/{pattern_id}")
   @router.post("/patterns/{pattern_id}/enable")
   @router.post("/patterns/{pattern_id}/disable")

   # Settings
   @router.get("/settings")
   @router.put("/settings")
   ```

5. **Router already registered** ✅:
   - The `learning_router` is already imported in `web/app.py`
   - No need to modify app.py
   - Just add endpoints to the file

---

## 📝 Phase 2 Scope (Reminder)

### DO Implement ✅

1. **7 Database-backed Endpoints**:
   - Pattern list, get, delete, enable, disable
   - Settings get, put

2. **Use Phase 1 Infrastructure**:
   - LearningHandler (from Phase 1)
   - LearnedPattern model (from Phase 1)
   - Database session management (existing)

3. **Create Settings Infrastructure**:
   - LearningSettings model (new)
   - Alembic migration (new)

4. **Security**:
   - Pattern ownership checks (user_id filter)
   - Error handling (404, 400, 422)
   - SELECT FOR UPDATE for modifications

5. **Testing**:
   - Manual testing with curl
   - Security test script
   - Test guide documentation

6. **Documentation**:
   - API documentation
   - Test guide
   - Evidence for all claims

### DO NOT Do ❌

1. **Don't touch Sprint A5 endpoints** - Leave them alone
2. **Don't create new file** - Add to existing web/api/routes/learning.py
3. **Don't refactor Sprint A5 code** - Out of scope
4. **Don't create frontend** - Phase 3
5. **Don't add auth** - Use TEST_USER_ID for Phase 2
6. **Don't add automation** - Phase 4

---

## 🚨 Critical Path Checks

### Before Writing Any Code

**Use Serena to verify**:
```python
# 1. Check existing file structure
mcp__serena__get_symbols_overview("web/api/routes/learning.py")

# 2. Understand LearningHandler interface
mcp__serena__get_symbols_overview("services/learning/learning_handler.py")

# 3. Check LearnedPattern model
mcp__serena__find_symbol("LearnedPattern", "services/database/models.py")

# 4. Understand session management
mcp__serena__find_symbol("get_db", "services/database/session.py")
```

**Check domain architecture**:
- Read relevant patterns if needed
- Check ADRs for learning system decisions
- Understand DDD boundaries

**Then and only then**: Start implementing

---

## 📊 Expected File Changes

### Modified Files

1. **web/api/routes/learning.py**:
   - Add 7 new endpoints
   - Add imports for LearningHandler, models
   - Add separation comments

2. **services/database/models.py**:
   - Add LearningSettings model
   - Add User.learning_settings relationship

3. **New Alembic migration**:
   - Create learning_settings table

4. **New test files**:
   - `tests/manual/test_phase2_security.py`
   - `tests/manual/PHASE2-TEST-GUIDE.md`

5. **New documentation**:
   - `docs/api/learning-api.md`

### NOT Modified

- ❌ Sprint A5 endpoints in learning.py
- ❌ web/app.py (router already registered)
- ❌ QueryLearningLoop (legacy, leave alone)
- ❌ CrossFeatureKnowledgeService (legacy, leave alone)

---

## ✅ Success Criteria

### Functionality
- [ ] 7 new endpoints working (patterns + settings)
- [ ] Database persistence (LearnedPattern + LearningSettings)
- [ ] Pattern ownership verification (user_id checks)
- [ ] Error handling (404, 400, 422)

### Code Quality
- [ ] Clear separation from Sprint A5 endpoints (comments)
- [ ] Uses existing LearningHandler from Phase 1
- [ ] Follows DDD patterns
- [ ] No duplication of Phase 1 code

### Testing
- [ ] All 10 manual tests pass
- [ ] Security tests pass
- [ ] curl outputs for each endpoint
- [ ] No 500 errors

### Documentation
- [ ] API documentation complete
- [ ] Test guide created
- [ ] Evidence provided for all claims
- [ ] Git commits with clear messages

---

## 🎓 Methodology Reinforcement

### What You Did RIGHT This Morning ✅

1. **Started new session log** - Good organization
2. **Verified Phase 1 infrastructure FIRST** - Followed Phase -1 requirement
3. **Used Serena after reminder** - Quick correction
4. **Created memory** - Prevent future mistakes
5. **STOPPED and escalated** - Correct behavior when unclear!

### Continue These Practices

**Always Use Serena First**:
- File/directory structure
- Symbol finding
- Understanding existing code
- Checking what exists

**Investigation Before Implementation**:
- Check domain models
- Review relevant patterns
- Check ADRs if applicable
- Understand existing architecture

**Evidence-Based Claims**:
- Terminal outputs for every claim
- Database queries showing state
- Test results proving functionality
- No guessing!

**Escalate When Unclear**:
- Architectural decisions
- Scope questions
- Conflicting requirements
- PM is available!

---

## 🚀 Ready to Proceed

**Status**: ✅ Architectural decision made

**Your Task**: Implement Phase 2.0 through 2.4

**File to Modify**: `web/api/routes/learning.py` (add to existing)

**Backend to Use**: LearningHandler + LearnedPattern (from Phase 1)

**New Infrastructure**: LearningSettings model + migration

**Testing**: Manual with curl, security script, test guide

**Documentation**: API docs, test guide, session log

---

## 📞 When to Escalate

**Escalate to me if**:
- More architectural conflicts discovered
- Unclear how to use existing infrastructure
- Domain model questions
- Pattern/ADR interpretation needed
- Scope ambiguity

**Don't escalate for**:
- Standard implementation questions (check docs first)
- Testing approaches (follow manual testing strategy)
- Evidence format (follow examples in prompt)

---

## 🏗️ The Cathedral

**Foundation**: Phase 1 complete ✅ (10/10 rating)
**User Controls**: Phase 2 (in progress) ← YOU ARE HERE
**Suggestions UI**: Phase 3 (next)
**Automation**: Phase 4 (later)

Build solid, build once, build right.

---

**Status**: Ready for Phase 2 implementation
**Blocking Issues**: None
**Architectural Clarity**: ✅ Clear
**Go/No-Go**: ✅ GO

---

_"Part of a cathedral, not just a random brick shed"_
_"Always use Serena first"_
_"Check what exists before building"_
