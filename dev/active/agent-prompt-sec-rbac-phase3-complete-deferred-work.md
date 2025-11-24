# SEC-RBAC Phase 3: Complete All Deferred Work

**Date**: November 22, 2025, 1:03 PM
**From**: Lead Developer (PM Decision: Option B)
**To**: Code Agent
**Priority**: P0 (Complete Issue #357)
**Estimated Time**: 4 hours total

---

## Mission

Complete ALL deferred work items to fully close Issue #357 with no remaining tasks.

**PM Decision**: Option B - Complete everything now for comprehensive RBAC implementation.

---

## Context

You've completed Phase 3 Steps 1-3:
- ✅ System-wide admin role (users.is_admin)
- ✅ 16/20 automated cross-user access tests
- ✅ Security scanning (Bandit + Safety)
- ✅ 3/9 critical repositories updated (Lists, Todos, Files)

**Now**: Complete the 3 deferred work items to achieve 100% RBAC coverage.

---

## Deferred Work Items (All Required)

### Item 1: Projects Role-Based Sharing (90 min)

**Goal**: Add role-based sharing to Projects (same JSONB pattern as Lists/Todos)

**Steps**:

1. **Database Migration** (15 min)
   - Check if `projects` table has `shared_with` JSONB column
   - If not: Create migration to add it
   - Pattern: `shared_with JSONB DEFAULT '[]'::jsonb`
   - Add GIN index: `CREATE INDEX idx_projects_shared_with ON projects USING GIN (shared_with);`

2. **Domain Model** (10 min)
   - File: `services/domain/models.py`
   - Add `shared_with: List[SharePermission] = field(default_factory=list)` to Project class
   - Verify SharePermission and ShareRole already exist (from Phase 2)

3. **ProjectRepository Methods** (30 min)
   - File: `services/repositories/project_repository.py`
   - Add 4 methods (follow UniversalListRepository pattern):

   ```python
   async def share_project(
       self,
       project_id: UUID,
       owner_id: str,
       user_to_share_with: str,
       role: ShareRole
   ) -> bool:
       """Share project with another user with specified role"""
       # Verify ownership
       # Add user to shared_with JSONB array
       # Return success/failure

   async def unshare_project(
       self,
       project_id: UUID,
       owner_id: str,
       user_to_unshare: str
   ) -> bool:
       """Remove user from project sharing"""
       # Verify ownership
       # Remove user from shared_with

   async def update_share_role(
       self,
       project_id: UUID,
       owner_id: str,
       target_user_id: str,
       new_role: ShareRole
   ) -> bool:
       """Update sharing role for a user"""
       # Verify ownership
       # Update role in shared_with array

   async def get_user_role(
       self,
       project_id: UUID,
       user_id: str
   ) -> Optional[ShareRole]:
       """Get user's role for a project (owner/viewer/editor/admin)"""
       # Check if owner
       # Check shared_with
       # Return role or None
   ```

4. **API Endpoints** (25 min)
   - File: `web/api/routes/projects.py`
   - Add 4 endpoints:

   ```python
   @router.post("/api/v1/projects/{project_id}/share")
   async def share_project(
       project_id: str,
       request: ShareProjectRequest,
       current_user: User = Depends(get_current_user)
   ):
       """Share project with user"""
       # Validate role (VIEWER/EDITOR/ADMIN)
       # Call repository.share_project()

   @router.delete("/api/v1/projects/{project_id}/share/{user_id}")
   async def unshare_project(
       project_id: str,
       user_id: str,
       current_user: User = Depends(get_current_user)
   ):
       """Remove user from project sharing"""

   @router.put("/api/v1/projects/{project_id}/share/{user_id}")
   async def update_project_share(
       project_id: str,
       user_id: str,
       request: UpdateShareRoleRequest,
       current_user: User = Depends(get_current_user)
   ):
       """Update user's sharing role"""

   @router.get("/api/v1/projects/{project_id}/my-role")
   async def get_my_project_role(
       project_id: str,
       current_user: User = Depends(get_current_user)
   ):
       """Get current user's role for project"""
   ```

5. **Manual Testing** (10 min)
   - Create test project as User A
   - Share with User B as VIEWER
   - Verify User B can read but not edit
   - Update to EDITOR role
   - Verify User B can now edit
   - Document results

**Acceptance Criteria**:
- ✅ Migration adds shared_with to projects (if needed)
- ✅ 4 repository methods implemented
- ✅ 4 API endpoints functional
- ✅ Manual testing shows roles work correctly

---

### Item 2: Extended Repository Coverage (120 min)

**Goal**: Add admin bypass to 6 remaining repositories

**Repositories to Update**:

1. **ProjectRepository** (20 min - 5 methods)
   - File: `services/repositories/project_repository.py`
   - Methods: `get_project_by_id()`, `update_project()`, `delete_project()`, `get_projects()`, `add_project_member()`
   - Pattern: Add `is_admin: bool = False` parameter
   - Logic: `if owner_id and not is_admin: filters.append(owner_id == ...)`

2. **ConversationRepository** (15 min - 3 methods)
   - File: `services/repositories/conversation_repository.py`
   - Methods: `get_conversation()`, `update_conversation()`, `delete_conversation()`
   - Pattern: Same admin bypass pattern
   - Note: Already has user_id validation (verify if owner_id exists)

3. **KnowledgeGraphService** (25 min - 8 methods)
   - File: `services/knowledge/knowledge_graph_service.py`
   - Methods: All CRUD methods for nodes/edges
   - Pattern: Admin bypass for ownership checks
   - Test: Run existing 40 KG tests to verify no regressions

4. **FeedbackService** (15 min - 3 methods)
   - File: `services/learning/feedback_service.py`
   - Methods: `get_feedback()`, `update_feedback()`, `delete_feedback()`
   - Pattern: Admin can access any user's feedback

5. **PersonalityProfileRepository** (15 min - 3 methods)
   - File: `services/personality/personality_profile_repository.py`
   - Methods: `get_profile()`, `update_profile()`, `delete_profile()`
   - Note: User-scoped (user owns their profile), admin bypass for support

6. **TodoListRepository** (10 min - inherited)
   - File: `services/repositories/todo_list_repository.py`
   - Check: Does this inherit from UniversalListRepository?
   - If yes: Already has admin bypass (no work needed)
   - If no: Add admin bypass to CRUD methods

**For Each Repository**:
1. Read current implementation
2. Identify methods with owner_id/user_id checks
3. Add `is_admin: bool = False` parameter
4. Update ownership logic: `if owner_id and not is_admin:`
5. Run tests to verify no regressions
6. Document changes

**Acceptance Criteria**:
- ✅ All 6 repositories have admin bypass
- ✅ Consistent pattern across all repos
- ✅ All existing tests still pass
- ✅ No new security vulnerabilities introduced

---

### Item 3: Files Ownership Support (45 min)

**Goal**: Add owner_id to UploadedFile domain model and verify database migration

**Issue**: FileRepository has owner_id checks but UploadedFile domain model doesn't have owner_id field

**Steps**:

1. **Verify Database Schema** (5 min)
   - Check if `files` table has `owner_id` column (migration 4d1e2c3b5f7a should have added it)
   - Run: `docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d files"`
   - Verify: Column exists and is indexed

2. **Update Domain Model** (10 min)
   - File: `services/domain/models.py`
   - Add `owner_id: str` field to UploadedFile class
   - Ensure it's required (not Optional)
   - Match database schema exactly

3. **Update FileRepository** (15 min)
   - File: `services/repositories/file_repository.py`
   - Verify all CRUD methods use owner_id correctly
   - Check that domain model ↔ database model mapping includes owner_id
   - Fix any mapping issues

4. **Test File Ownership** (10 min)
   - Create file as User A
   - Try to access as User B (should fail)
   - Access as admin (should succeed)
   - Verify owner_id is saved correctly in database

5. **Update File Tests** (5 min)
   - File: `tests/integration/test_cross_user_access.py`
   - Uncomment the 4 deferred file tests
   - Verify they now pass with owner_id field present
   - Total file tests should be 4/4 passing

**Acceptance Criteria**:
- ✅ UploadedFile domain model has owner_id field
- ✅ Database schema matches domain model
- ✅ FileRepository correctly maps owner_id
- ✅ 4/4 file cross-user access tests pass
- ✅ Manual testing confirms ownership works

---

## Execution Plan

**Total Time**: ~4 hours (255 minutes)

**Recommended Order**:
1. Item 3: Files ownership (45 min) - Fixes domain model inconsistency first
2. Item 1: Projects sharing (90 min) - Extends proven pattern
3. Item 2: Extended repos (120 min) - Most time-consuming, do last

**STOP Conditions**:
- Any migration fails
- Any test suite fails
- Domain model conflicts discovered
- Security scan shows new vulnerabilities
- Manual testing reveals bugs

If you hit a STOP condition, document it and wait for PM guidance.

---

## Deliverables

When all 3 items are complete, create:

1. **Final Completion Report**: `dev/2025/11/22/sec-rbac-phase3-full-completion-report.md`
   - All work completed (Steps 1-3 + deferred items 1-3)
   - Test results (all 20 tests should pass)
   - Manual testing evidence
   - Security scan results
   - Commits made

2. **GitHub Issue Update**: Update Issue #357
   - Change status to completed
   - Add comment with final completion report link
   - List all deliverables with evidence

3. **Close Issue #357**:
   ```bash
   gh issue comment 357 -b "✅ SEC-RBAC fully complete. All work finished including previously deferred items. See final completion report for evidence."
   gh issue close 357
   ```

---

## Success Criteria

Issue #357 can be closed when:

- ✅ All 9 repositories have owner_id + admin bypass
- ✅ Projects have role-based sharing (4 methods + 4 endpoints)
- ✅ Files have owner_id in domain model
- ✅ All 20 cross-user access tests pass
- ✅ Security scan shows 0 new issues
- ✅ Manual testing validates all features
- ✅ Documentation complete
- ✅ No deferred work remaining

---

## Notes

- **Code Quality**: All pre-commit hooks must pass
- **Testing**: Run full test suite before closing issue
- **Documentation**: Be thorough - this is the final state
- **Commits**: Clear commit messages referencing Issue #357
- **Time Tracking**: Document actual vs estimated time

---

**PM Approval**: Option B - Complete all deferred work
**Authorization**: Proceed immediately
**Expected Completion**: ~4 hours from start

Good luck! This is the final push to fully close Issue #357.
