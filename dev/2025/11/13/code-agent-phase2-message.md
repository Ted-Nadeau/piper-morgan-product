# Message to Code Agent: Phase 2 Implementation (Supersession Approach)

**Date**: November 13, 2025, 7:47 AM PT
**From**: Lead Developer + PM
**To**: Code Agent
**Re**: Proceed with Phase 2 - Clean Supersession of Sprint A5

---

## ✅ Architectural Decision Made: SUPERSEDE Sprint A5

After proper analysis, we've decided to **supersede Sprint A5 endpoints entirely** rather than coexist with them.

**Why**:
- Sprint A5 was exploratory/prototype (2 days, file-based)
- Phase 1/2 is production implementation (database-backed)
- No users = no backward compatibility needed
- Pre-launch = best time for clean architecture
- Sequential versions, not parallel systems

**Decision Doc**: See `/Users/xian/Development/piper-morgan/dev/active/sprint-a5-vs-phase2-analysis.md`

---

## 🎯 Your Task: Implement Phase 2 with Clean Supersession

### Phase 2.0: Deprecate Sprint A5 (15 minutes)

**Step 1: Comment Out Router Registration** (5 min)

File: `web/app.py`

Find and comment out:
```python
app.include_router(learning_router)
```

Change to:
```python
# DEPRECATED: Sprint A5 learning endpoints (Oct 20-21, 2025)
# Superseded by Issue #300 database-backed learning system
# See: dev/active/sprint-a5-vs-phase2-analysis.md
# app.include_router(learning_router)
```

**Step 2: Add Deprecation Notice** (10 min)

File: `web/api/routes/learning.py`

Add at the **very top** of the file (after imports):

```python
"""
================================================================================
SPRINT A5 ENDPOINTS (Oct 20-21, 2025) - DEPRECATED AS OF NOV 13, 2025
================================================================================

These endpoints were a prototype/exploration of learning concepts using
file-based storage. They served their purpose (proved learning value) and
are now superseded by Issue #300's database-backed production system.

STATUS: DEPRECATED - Kept for reference only
REPLACEMENT: Issue #300 endpoints (below)
DEPRECATION DATE: November 13, 2025
REMOVAL PLANNED: After MVP launch

Sprint A5 provided these valuable insights:
- Learning system is valuable to users
- Pattern-based approach works
- Need for multi-user support (database required)
- Analytics and collaborative features desired
- Automatic capture > manual teaching

Future roadmap from Sprint A5 learnings:
- Collaborative learning → Level 3 (if >50 users)
- Analytics → Post-MVP enhancement
- Export/import → Data portability feature
- Manual override → Phase 3-4 explicit feedback

DO NOT USE SPRINT A5 ENDPOINTS IN NEW CODE

================================================================================
ISSUE #300 ENDPOINTS (Nov 12-13, 2025) - PRODUCTION IMPLEMENTATION
================================================================================

Database-backed learning system with automatic real-time capture.
See: gameplan-300-learning-basic-revised.md for architecture.
"""

# ============================================
# Sprint A5 Endpoints (DEPRECATED - Keep for reference)
# ============================================

[existing 15 endpoints stay here - don't modify them]

# ============================================
# Issue #300 Phase 2 - Database-backed Pattern Management (PRODUCTION)
# ============================================

[NEW Phase 2 endpoints go below here]
```

**Evidence Required**:
```bash
# Show router commented out
grep "learning_router" web/app.py

# Show deprecation notice added
head -50 web/api/routes/learning.py | grep -A5 "DEPRECATED"
```

---

### Phase 2.1-2.4: Implement 7 New Endpoints (2-3 hours)

**Follow your original Phase 2 prompt**: `dev/active/agent-prompt-300-phase-2.md`

**With these modifications**:

1. **Router is STILL registered** ✅
   - Don't register a new router
   - The learning_router is commented out, but you'll uncomment it after adding new endpoints
   - Add your 7 new endpoints to the SAME file below Sprint A5 code

2. **After implementing all 7 endpoints**:
   - Uncomment the learning_router line in web/app.py
   - Now it routes to Issue #300 endpoints (not Sprint A5)

3. **Paths remain the same**:
   - `@router.get("/patterns")` - List patterns (database)
   - `@router.get("/patterns/{pattern_id}")` - Get pattern
   - `@router.delete("/patterns/{pattern_id}")` - Delete pattern
   - `@router.post("/patterns/{pattern_id}/enable")` - Enable
   - `@router.post("/patterns/{pattern_id}/disable")` - Disable
   - `@router.get("/settings")` - Get settings
   - `@router.put("/settings")` - Update settings

4. **Add imports at top** (after deprecation notice):
   ```python
   from services.learning.learning_handler import LearningHandler
   from services.database.models import LearnedPattern, LearningSettings
   from services.database.session import get_db
   from sqlalchemy.ext.asyncio import AsyncSession
   from uuid import UUID
   ```

5. **Use TEST_USER_ID** (hardcoded for Phase 2):
   ```python
   TEST_USER_ID = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")
   ```

---

## 📋 Implementation Checklist

### Phase 2.0: Deprecation ✓
- [ ] Comment out learning_router in web/app.py
- [ ] Add deprecation notice to learning.py
- [ ] Evidence: grep outputs showing changes

### Phase 2.1: Pattern Management
- [ ] GET /patterns (list)
- [ ] GET /patterns/{id} (details)
- [ ] DELETE /patterns/{id}
- [ ] POST /patterns/{id}/enable
- [ ] POST /patterns/{id}/disable
- [ ] Test each with curl

### Phase 2.2: Settings API
- [ ] Create LearningSettings model
- [ ] Create alembic migration
- [ ] GET /settings
- [ ] PUT /settings
- [ ] Test GET/PUT cycle

### Phase 2.3: Security
- [ ] Pattern ownership checks (user_id filter)
- [ ] Error handling (404, 400, 422)
- [ ] Security test script created
- [ ] All security tests pass

### Phase 2.4: Documentation
- [ ] API documentation (docs/api/learning-api.md)
- [ ] Test guide (tests/manual/PHASE2-TEST-GUIDE.md)
- [ ] Evidence package compiled

### Phase 2.Z: Re-enable Router
- [ ] Uncomment learning_router in web/app.py
- [ ] Verify endpoints accessible
- [ ] Run full test suite

---

## 🚨 CRITICAL: Use Serena First!

**Before doing ANYTHING**:

```python
# Check current file structure
mcp__serena__list_dir("web/api/routes", recursive=true)

# Check learning.py symbols (see what exists)
mcp__serena__get_symbols_overview("web/api/routes/learning.py")

# Check LearningHandler interface
mcp__serena__get_symbols_overview("services/learning/learning_handler.py")

# Check database models
mcp__serena__find_symbol("LearnedPattern", "services/database/models.py")
```

**Then** proceed with implementation.

---

## 📊 Success Criteria

### Functionality ✅
- [ ] Sprint A5 properly deprecated (router commented, notice added)
- [ ] All 7 Phase 2 endpoints working
- [ ] Database persistence (LearnedPattern + LearningSettings)
- [ ] Pattern ownership verified
- [ ] Error handling working

### Code Quality ✅
- [ ] Clear deprecation notice for Sprint A5
- [ ] Clean separation between old/new code
- [ ] Uses existing LearningHandler from Phase 1
- [ ] No duplication of logic

### Testing ✅
- [ ] All 10 manual tests pass
- [ ] Security tests pass
- [ ] curl outputs for each endpoint
- [ ] No 500 errors

### Documentation ✅
- [ ] API documentation complete
- [ ] Test guide created
- [ ] Evidence provided
- [ ] Git commits clean

---

## 📦 Expected Deliverables

**Modified Files**:
1. `web/app.py` - Router commented/uncommented
2. `web/api/routes/learning.py` - Deprecation notice + 7 new endpoints
3. `services/database/models.py` - LearningSettings model
4. New alembic migration for learning_settings

**New Files**:
1. `tests/manual/test_phase2_security.py`
2. `tests/manual/PHASE2-TEST-GUIDE.md`
3. `docs/api/learning-api.md`

**Evidence Package**:
- Deprecation notice in place
- curl outputs for all 7 endpoints
- Database verification
- Security test results
- Git commits

---

## ⏱️ Estimated Effort

- **Phase 2.0** (Deprecation): 15 minutes
- **Phase 2.1** (Pattern APIs): 1 hour
- **Phase 2.2** (Settings): 45 minutes
- **Phase 2.3** (Security): 30 minutes
- **Phase 2.4** (Documentation): 30 minutes
- **Total**: ~2.5-3 hours

---

## 🎯 Key Points

1. **Sprint A5 stays in file** - Don't delete, just deprecate
2. **Same file** - Add Phase 2 endpoints to web/api/routes/learning.py
3. **Router commented** - Until Phase 2 endpoints ready
4. **Then uncomment** - Router now serves Phase 2 endpoints
5. **Use Serena first** - Always verify before building
6. **Evidence required** - For every claim

---

## 📞 When to Escalate

**Stop and ask if**:
- Serena shows unexpected structure
- LearningHandler interface different than expected
- Database models don't match
- Any architectural questions
- Scope ambiguity

**Don't stop for**:
- Standard implementation questions
- Testing approaches (follow manual strategy)
- Evidence format (follow examples)

---

## 🏗️ Remember

**Sprint A5 served its purpose** - Proved learning is valuable
**Phase 2 is production** - Build it right, build it clean
**Pre-launch elegance** - No technical debt at launch
**One learning system** - Clear, clean, professional

---

**Status**: Ready for implementation
**Approach**: Supersession (clean replacement)
**Priority**: P2 (Alpha Feature)
**Go/No-Go**: ✅ GO

---

_"Part of a cathedral, not just a random brick shed"_
_"Sprint A5 taught us what to build - now build it right"_
_"Always use Serena first"_

---

**Original Phase 2 Prompt**: dev/active/agent-prompt-300-phase-2.md (still valid for Phases 2.1-2.4)
**Architectural Decision**: dev/active/sprint-a5-vs-phase2-analysis.md
**This Message**: Add-on with supersession instructions
