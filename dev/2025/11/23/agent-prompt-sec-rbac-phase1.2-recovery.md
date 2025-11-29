# Claude Code Prompt: SEC-RBAC Phase 1.2 Recovery and Completion

## Critical Context: What Just Happened

**You made two serious errors that resulted in commits being reverted:**

1. **Commit 9f1e6f97 (PersonalityProfileRepository)** - REVERTED

   - **Error**: You added a service that was NOT in the completion matrix scope
   - **Why this matters**: PM defines scope, not you. You cannot add services without PM approval.

2. **Commit e3e40103 (ConversationRepository)** - REVERTED
   - **Error**: You referenced `ConversationTurnDB` which DOESN'T EXIST in the codebase
   - **Why this matters**: This is broken code that would fail immediately with NameError
   - **How it happened**: You assumed the ORM model existed without verifying

**Both commits have been reverted. The codebase is back to 7 services complete.**

---

## Current Status (ACTUAL)

**Services Complete**: 7/8+ services (52 methods total)

✅ **COMPLETE**:

1. FileRepository (14 methods) - Commits 1a41237e + 263ae02f
2. UniversalListRepository (11 methods) - Commit d214ac83
3. TodoManagementService (7 methods) - Verified secure
4. FeedbackService (4 methods) - Commit 241f1629
5. TodoListRepository (4 methods) - Commit 58825174
6. KnowledgeGraphService (12 methods) - Commit 720d39ce
7. ProjectRepository (7 methods) - Commit fd245dbc

🔲 **PENDING**:

- Section 6: Learning Services (needs discovery and audit)

---

## THE COMPLETION MATRIX IS LAW

**Read this file NOW**: `dev/active/sec-rbac-phase1.2-completion-matrix.md`

**CRITICAL RULES**:

1. **The matrix defines scope** - If a service is NOT explicitly listed in sections 1-8, you CANNOT work on it
2. **You cannot modify the matrix scope** - You can only check off items, not add new ones
3. **PM approval required** - If you discover work that seems needed but isn't in the matrix, STOP and ask PM
4. **Evidence required** - "Tests pass" is not enough. You must verify code actually runs.

---

## What "Complete" Actually Means

**Phase 1.2 is NOT complete until**:

- Section 6 (Learning Services) is discovered, audited, and either completed OR marked as blocked with evidence
- ALL services in the matrix are either ✅ COMPLETE or have documented blockers
- NO services have been added to scope without PM approval
- ALL code actually runs (no references to non-existent classes)

---

## Mandatory Verification Protocol (BEFORE ANY COMMIT)

**Step 1: Scope Check**

```bash
# Before touching ANY service, verify it's in the matrix
grep -A 5 "ServiceName" dev/active/sec-rbac-phase1.2-completion-matrix.md
# If grep returns nothing → STOP, ask PM
```

**Step 2: ORM Verification (CRITICAL)**

```bash
# Before referencing ANY ORM model, verify it exists
grep "class ORM ModelNameDB" services/database/models.py
# If grep returns nothing → STOP, the model doesn't exist
```

**Step 3: Test Verification**

```bash
# Tests must actually import and run your code
pytest tests/path/to/test.py -xvs
# If import fails → your code is broken, fix it before claiming "tests pass"
```

---

## Your Mission: Complete Section 6 (Learning Services)

**Current Status**: Section 6 is listed as "PENDING" with estimated 10+ methods

**Your Tasks**:

### Task 1: Discovery

Use Serena to discover what Learning Services actually exist:

```bash
# Find all learning-related services
mcp__serena__list_dir("services/learning", recursive=false)

# For each service file found, get overview
mcp__serena__get_symbols_overview("services/learning/[filename].py")

# Check if owner_id column exists in relevant tables
grep -r "learning" alembic/versions/4d1e2c3b5f7a*.py
```

### Task 2: Report Findings

Create a discovery report showing:

- What services exist in `services/learning/`
- Which ones have CRUD methods that need owner_id validation
- Which tables have owner_id column support (check migration 4d1e2c3b5f7a)
- Estimated method count

### Task 3: Implementation (ONLY if tables have owner_id)

- Follow the proven pattern from completed services
- Add optional `owner_id: Optional[UUID] = None` parameter
- Verify ORM models exist BEFORE using them
- Run actual tests that import your code
- Commit with evidence

### Task 4: Update Matrix

- Mark Section 6 as either:
  - ✅ COMPLETE (with commit hash and method count)
  - ⚠️ BLOCKED (with explanation why - e.g., "No owner_id in tables")

---

## If You're Blocked

**Acceptable Blockers**:

- Tables don't have owner_id column (check migration 4d1e2c3b5f7a)
- ORM models don't exist for the service
- Service doesn't have exposed CRUD methods

**When Blocked**:

1. Document the blocker in Section 6 of the matrix
2. Provide evidence (grep results, file listings)
3. Mark Section 6 as complete with note "No owner_id schema support found"
4. Report to PM

---

## If Section 6 is Actually Empty or Blocked

If you discover that Learning Services genuinely don't need owner_id validation (no CRUD methods, no owner_id in tables, etc.), then:

1. Update Section 6 status with evidence
2. Mark Phase 1.2 as COMPLETE
3. Report final status to PM

**Phase 1.2 completion criteria**:

- All 8 sections processed (either complete or blocked with evidence)
- NO services added to scope without PM approval
- ALL code runs successfully
- ALL tests pass

---

## Red Flags That Should Make You STOP

- ❌ You're about to add a service not in sections 1-8
- ❌ You're referencing a class you haven't verified exists
- ❌ You're claiming "tests pass" without running pytest on your changed code
- ❌ You're marking the matrix COMPLETE without processing Section 6
- ❌ You're assuming an ORM model exists based on the domain model

---

## Expected Outcome

**Best Case**: Learning Services have owner_id tables, you complete Section 6, Phase 1.2 is 100% done

**Also Acceptable**: Learning Services don't need owner_id (no CRUD/no schema), you document this with evidence, Phase 1.2 is complete

**NOT Acceptable**:

- Claiming Phase 1.2 is complete without processing Section 6
- Adding services not in the matrix
- Writing code that references non-existent classes
- Claiming tests pass when code doesn't import

---

## Start Here

1. Read the completion matrix: `dev/active/sec-rbac-phase1.2-completion-matrix.md`
2. Discover what Learning Services exist
3. Report findings
4. Proceed based on what you find

**Remember**: PM defines scope. You execute within scope. Evidence required for all claims.

---

_Prompt created by: Lead Developer_
_Date: November 22, 2025, 10:05 AM_
_Context: Recovery after scope violations and breaking changes_
_Status: 7/8 sections complete, Section 6 pending discovery_
