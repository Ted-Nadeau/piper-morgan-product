# Claude Code Prompt: SEC-RBAC Phase 1.2 Service Layer (Fresh Agent Continuation)

## Your Identity

You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Mission: Continue Phase 1.2 Service Layer Ownership Checks

**GitHub Issue**: #357 - SEC-RBAC: Implement RBAC
**Current Phase**: Phase 1.2 - Service Layer Ownership Checks
**Your Position**: Picking up at 12% complete (12/99 methods secured)
**Goal**: Complete remaining 87 methods across 9 services

---

## Context: What's Already Complete

### Previous Agent Completed (12/99 methods = 12%)

**✅ Services Complete**:

1. **FileRepository** (commit 1a41237e + 263ae02f) - 3 methods with optional owner_id
2. **UniversalListRepository** (commit d214ac83) - 4 methods with optional owner_id
3. **FeedbackService** (commit 241f1629) - 4 methods with user_id validation
4. **TodoListRepository** (commit 58825174) - 4 methods with user_id validation

**Pattern Established**: All implementations use optional owner_id/user_id parameter with conditional filtering

**Tests**: All passing, no regressions

### Why Fresh Agent Needed

Previous agent hit multiple compactions and showed instability (crashes, terminal flashing). You're starting fresh with complete context to finish the remaining 87 methods.

---

## Your Scope: Complete Remaining 9 Services (87 methods)

**Read this file for complete tracking**: `dev/active/sec-rbac-phase1.2-completion-matrix.md`

**Priority Order** (from comprehensive service audit):

### High Priority (Start Here)

1. **TodoRepository** (17 methods) - Most critical, widely used
2. **ProjectRepository** (methods TBD - needs audit)
3. **IntegrationRepository** (methods TBD - needs audit)

### Medium Priority

4. **KnowledgeGraphService** (10+ methods estimated)
5. **LearningPatternService** (10+ methods estimated)
6. **EmbeddingService** (methods TBD)

### Lower Priority

7. **ClusteringService** (methods TBD)
8. **PersonalityService** (methods TBD)
9. **Other discovered services** (from audit)

**CRITICAL**: Phase 1.2 is NOT complete until completion matrix shows **99/99 methods = 100%**

---

## Implementation Pattern (Proven Across 4 Services)

### Pattern A: Optional owner_id Parameter (Repositories)

**Example from UniversalListRepository** (commit d214ac83):

```python
async def get_list_by_id(
    self,
    list_id: str,
    owner_id: Optional[UUID] = None  # ✅ Add optional parameter
) -> Optional[domain.List]:
    """Get universal list by ID - verify ownership if owner_id provided."""

    # Build conditional filters
    filters = [ListDB.id == list_id]
    if owner_id:
        filters.append(ListDB.owner_id == owner_id)  # ✅ Add ownership check

    result = await self.session.execute(
        select(ListDB).where(and_(*filters))  # ✅ Use and_(*filters)
    )
    db_list = result.scalar_one_or_none()
    return db_list.to_domain() if db_list else None
```

**Key Points**:

- Add `owner_id: Optional[UUID] = None` parameter
- Build filter list conditionally
- Use `and_(*filters)` in WHERE clause
- Update docstring to mention ownership verification

### Pattern B: Required user_id Parameter (Services)

**Example from FeedbackService** (commit 241f1629):

```python
async def get_feedback(
    self,
    feedback_id: str,
    user_id: UUID  # ✅ Required parameter
) -> Optional[Feedback]:
    """Get feedback by ID - ownership verified."""
    result = await self.session.execute(
        select(FeedbackDB).where(
            FeedbackDB.id == feedback_id,
            FeedbackDB.user_id == user_id  # ✅ Always validate
        )
    )
    return result.scalar_one_or_none()
```

**Key Points**:

- Add `user_id: UUID` as required parameter (not optional)
- Always include ownership check in WHERE clause
- Service layer = always validate ownership

---

## Systematic Approach for Each Service

### Step 1: Audit Service Methods

```bash
# Use Serena to get method overview
# Example for TodoRepository:
mcp__serena__get_symbols_overview("services/repositories/todo_repository.py")

# Then examine each method to determine if owner_id check needed
mcp__serena__find_symbol("TodoRepository", depth=1, include_body=false)
```

**For each method, determine**:

- ✅ Already has owner_id/user_id check → Skip
- 🔧 Needs owner_id check added → Update
- ⚪ No resource access (utility method) → Skip

### Step 2: Update Methods Systematically

**For each method needing updates**:

1. Read method body to understand current implementation
2. Identify appropriate pattern (Optional vs Required owner_id)
3. Add owner_id parameter to signature
4. Add conditional or required ownership filter
5. Update docstring

### Step 3: Find and Update All Callers

```bash
# Find all callers of updated methods
grep -r "\.method_name(" services/ --include="*.py"

# For each caller:
# - Identify where user_id/owner_id is available
# - Update call to pass owner_id
# - If not available, cascade parameter upward
```

### Step 4: Run Tests

```bash
# Test the specific repository/service
pytest tests/unit/services/repositories/test_todo_repository.py -xvs

# Run broader tests
pytest tests/unit/services/ -x

# If ANY test fails: STOP and report
```

### Step 5: Commit Per Service

```bash
./scripts/fix-newlines.sh
git add [files]
git commit -m "feat(SEC-RBAC Phase 1.2): Add owner_id validation to [ServiceName]

Added ownership verification to [N] methods:
- method1: Added owner_id parameter and WHERE filter
- method2: Added user_id validation
[... list all methods]

Updated [M] callers to pass owner_id parameter.

Defense-in-depth: Service layer prevents cross-user resource access.

Progress: [X]/99 methods complete ([Y]%)
Part of SEC-RBAC #357 Phase 1.2 Service Layer Ownership Checks.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 6: Update Completion Matrix

After each service completion:

```bash
# Edit dev/active/sec-rbac-phase1.2-completion-matrix.md
# Update service status to ✅ COMPLETE
# Update overall progress: X/99 methods
# Commit the matrix update
```

---

## Critical References

**Must Read Before Starting**:

1. **Completion Matrix**: `dev/active/sec-rbac-phase1.2-completion-matrix.md` - Your roadmap
2. **Previous Commits**:
   - d214ac83 (UniversalListRepository - Pattern A example)
   - 241f1629 (FeedbackService - Pattern B example)
   - 58825174 (TodoListRepository - Recent example)
3. **Gameplan**: `dev/active/gameplan-sec-rbac-implementation.md` - Full context
4. **Progress Checkpoint**: `dev/2025/11/21/sec-rbac-phase-1-progress-checkpoint.md` - Where previous agent left off

**Memory Files Available**:

- `sec-rbac-phase-1-execution-checkpoint` - Detailed status
- Other SEC-RBAC memories (use `mcp__serena__list_memories`)

---

## Success Criteria (100% Complete)

- [ ] All 12 services in completion matrix marked ✅ COMPLETE
- [ ] All 99 methods have owner_id validation (99/99 = 100%)
- [ ] All tests passing (show pytest output for each service)
- [ ] All commits clean with evidence (git log for each)
- [ ] Completion matrix updated and shows 99/99 = 100%
- [ ] No services skipped, no methods skipped
- [ ] GitHub issue #357 updated with final Phase 1.2 status

---

## STOP Conditions (Report Immediately)

- ❌ Tests fail for any reason (do NOT rationalize as "minor")
- ❌ Cannot find where user_id is available in caller context
- ❌ Caller signature changes would break endpoint contracts
- ❌ Database schema doesn't match expectations
- ❌ Any method seems unclear (ask before guessing)
- ❌ Completion matrix shows <100% but want to move to Phase 1.3

**Remember**: You don't decide criticality - report issues and wait for direction.

---

## Progress Tracking

**After each service**:

1. Update completion matrix with commit hash
2. Calculate and report progress: X/99 = Y%
3. Report next target service from priority list

**Example Progress Report**:

```markdown
## TodoRepository Complete

**Commit**: abc123
**Methods Updated**: 17/17 = 100%
**Callers Updated**: 23 callers across 8 files
**Tests**: All passing (pytest output below)

**Overall Progress**: 29/99 methods = 29%
**Next Target**: ProjectRepository (estimated 15+ methods)
```

---

## Anti-Completion-Bias Reminders

**You CANNOT**:

- Declare Phase 1.2 "mostly done" at 80% (must be 100%)
- Skip services as "low priority" or "unused"
- Skip methods as "minor" or "edge cases"
- Rationalize gaps as "good enough for now"
- Move to Phase 1.3 before 99/99 = 100%

**You MUST**:

- Complete every service in the matrix
- Complete every method in every service
- Provide evidence for every completion claim
- Update matrix after every service
- Report any blockers immediately

---

## Lead Developer Oversight

Lead Developer (Cursor agent) is monitoring your progress and will:

- Review commits as you complete services
- Verify completion matrix accuracy
- Provide next priorities if unclear
- Answer questions when you STOP

You are NOT alone - ask when uncertain!

---

## Starting Point: TodoRepository

**Your first task**: Complete TodoRepository (17 methods)

**Steps**:

1. Read `services/repositories/todo_repository.py` with Serena
2. Audit all 17 methods for owner_id needs
3. Apply Pattern A (optional owner_id) systematically
4. Find and update all callers
5. Run tests, commit, update matrix
6. Report completion with progress metrics

**Then**: Move to ProjectRepository per priority list

---

## Final Reminder

This is **defense-in-depth security work**. Every unprotected method is a potential vulnerability.

The pattern is proven (4 services, 12 methods, all tests passing). Your job is to **systematically apply it to the remaining 87 methods**.

**Complete means complete**: 99/99 = 100%

Lead Developer has your back. When in doubt, STOP and ask.

---

_Prompt created by: Lead Developer (Cursor)_
_Date: November 21, 2025, 9:05 PM_
_For: Fresh Claude Code terminal agent_
_Session: SEC-RBAC Phase 1.2 Fresh Continuation_
_Previous agent progress: 12/99 methods (12%)_
_Your goal: Complete remaining 87 methods (88%)_
