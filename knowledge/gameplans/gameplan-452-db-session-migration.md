# Gameplan: Issue #452 - Systematic db.get_session() Migration
*Created: December 2, 2025*
*Status: Audited and Ready for Execution*

---

## Phase -1: Infrastructure Verification ✅ COMPLETED

### Verified Facts (December 2, 2025)
- **Root cause confirmed**: Global `db` singleton at `services/database/connection.py:136`
- **Fix pattern validated**: `session_scope_fresh()` tested successfully on `/setup/create-user`
- **Instance count audited**: 15 HIGH RISK instances in production HTTP code

### Evidence
```bash
# Successful test output:
{"success":true,"user_id":"e2123a66-dcb5-4649-970e-860b1ad14ab5","message":"Account created: testuser_fresh"}
```

---

## Phase 0: Issue Verification ✅ COMPLETED

- Issue #452 created with full audit
- Labels: `bug`, `component: database`, `priority: high`
- Related to: #390 (ALPHA-SETUP-UI), #442 (original bug)

---

## Phase 1: Migrate auth.py (4 instances)

### Files to Modify
- `web/api/routes/auth.py` - Lines 119, 271, 330, 422

### Claude Code Prompt
```
Issue #452: Migrate auth.py from db.get_session() to session_scope_fresh()

CONTEXT:
- The global db singleton causes "Future attached to different loop" errors
- Fix pattern: Replace `async with await db.get_session() as session:` with
  `async with AsyncSessionFactory.session_scope_fresh() as session:`
- This file has 4 instances at lines 119, 271, 330, 422

TASK:
1. Read web/api/routes/auth.py
2. Replace all 4 instances of `async with await db.get_session() as session:`
   with `async with AsyncSessionFactory.session_scope_fresh() as session:`
3. Update import: ensure `from services.database.session_factory import AsyncSessionFactory` exists
4. Remove unused import: `from services.database.connection import db` if no longer needed
5. Test: curl -s -X POST http://localhost:8001/auth/login (verify no 500 errors)

DO NOT:
- Change any other code
- Add new features
- Refactor beyond the session changes
```

### Acceptance Criteria
- [ ] 4 instances migrated
- [ ] Import updated
- [ ] Server starts without errors
- [ ] Login endpoint returns expected response (not 500)

---

## Phase 2: Migrate files.py (5 instances)

### Files to Modify
- `web/api/routes/files.py` - Lines 167, 262, 335, 409, 514

### Claude Code Prompt
```
Issue #452: Migrate files.py from db.get_session() to session_scope_fresh()

CONTEXT:
- The global db singleton causes "Future attached to different loop" errors
- Fix pattern: Replace `async with await db.get_session() as session:` with
  `async with AsyncSessionFactory.session_scope_fresh() as session:`
- This file has 5 instances at lines 167, 262, 335, 409, 514

TASK:
1. Read web/api/routes/files.py
2. Replace all 5 instances of `async with await db.get_session() as session:`
   with `async with AsyncSessionFactory.session_scope_fresh() as session:`
3. Update import: ensure `from services.database.session_factory import AsyncSessionFactory` exists
4. Remove unused import: `from services.database.connection import db` if no longer needed
5. Test: curl -s http://localhost:8001/api/v1/files (verify no 500 errors)

DO NOT:
- Change any other code
- Add new features
- Refactor beyond the session changes
```

### Acceptance Criteria
- [ ] 5 instances migrated
- [ ] Import updated
- [ ] Server starts without errors
- [ ] Files endpoint returns expected response (not 500)

---

## Phase 3: Migrate document_handlers.py (5 instances)

### Files to Modify
- `services/intent_service/document_handlers.py` - Lines 79, 126, 244, 368, 393

### Claude Code Prompt
```
Issue #452: Migrate document_handlers.py from db.get_session() to session_scope_fresh()

CONTEXT:
- The global db singleton causes "Future attached to different loop" errors
- Fix pattern: Replace `async with await db.get_session() as session:` with
  `async with AsyncSessionFactory.session_scope_fresh() as session:`
- This file has 5 instances at lines 79, 126, 244, 368, 393

TASK:
1. Read services/intent_service/document_handlers.py
2. Replace all 5 instances of `async with await db.get_session() as session:`
   with `async with AsyncSessionFactory.session_scope_fresh() as session:`
3. Update import: ensure `from services.database.session_factory import AsyncSessionFactory` exists
4. Remove unused import: `from services.database.connection import db` if no longer needed
5. Run: python -m pytest tests/unit/services/intent_service/ -v

DO NOT:
- Change any other code
- Add new features
- Refactor beyond the session changes
```

### Acceptance Criteria
- [ ] 5 instances migrated
- [ ] Import updated
- [ ] Related unit tests pass

---

## Phase 4: Migrate user_context_service.py (1 instance)

### Files to Modify
- `services/user_context_service.py` - Line 176

### Claude Code Prompt
```
Issue #452: Migrate user_context_service.py from db.get_session() to session_scope_fresh()

CONTEXT:
- The global db singleton causes "Future attached to different loop" errors
- Fix pattern: Replace `async with await db.get_session() as session:` with
  `async with AsyncSessionFactory.session_scope_fresh() as session:`
- This file has 1 instance at line 176

TASK:
1. Read services/user_context_service.py
2. Replace the instance of `async with await db.get_session() as session:`
   with `async with AsyncSessionFactory.session_scope_fresh() as session:`
3. Update import: ensure `from services.database.session_factory import AsyncSessionFactory` exists
4. Remove unused import: `from services.database.connection import db` if no longer needed

DO NOT:
- Change any other code
- Add new features
- Refactor beyond the session changes
```

### Acceptance Criteria
- [ ] 1 instance migrated
- [ ] Import updated
- [ ] Server starts without errors

---

## Phase Z: Final Verification

### Full Test Suite
```bash
# Unit tests
python -m pytest tests/unit/ -v

# Integration tests (if applicable)
python -m pytest tests/integration/ -v -m "not slow"

# Manual endpoint verification
curl -s -X POST http://localhost:8001/auth/login -H "Content-Type: application/json" -d '{"username":"test","password":"test"}'
curl -s http://localhost:8001/api/v1/files
```

### Final Audit
```bash
# Verify no remaining direct db.get_session() in HTTP code
grep -n "db\.get_session()" web/api/routes/*.py services/intent_service/*.py services/user_context_service.py

# Expected: 0 results (only scripts/tests should remain)
```

### Acceptance Criteria
- [ ] All 15 instances migrated
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] No regressions in existing functionality (PM validates)
- [ ] Audit shows 0 remaining instances in HTTP code

---

## Notes

### Why Not Fix at Middleware Level?
Creating a fresh engine per-request has a small performance cost. A more efficient architectural fix would be to ensure the database engine is created/re-bound per-request at the middleware level. However:
1. The current fix is safe and well-tested
2. The performance impact is minimal for our scale
3. A middleware fix requires deeper architectural changes
4. This can be revisited if performance becomes a concern

### Scripts Are Excluded
The 8 instances in `scripts/` run their own event loops and don't have this problem. They're excluded from migration.

### Tests Are Excluded
The 8 instances in `tests/` use overridden sessions via fixtures. They're excluded from migration.
