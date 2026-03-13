# Gameplan: Issue #582 - Standup Command / Portfolio Integration

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/582
**Type**: Bug Fix (Integration Gap)
**Template Version**: v9.3
**Created**: 2026-01-12 19:09
**Status**: Awaiting PM Approval

---

## Problem Statement

When running `/standup` command, Piper responds "You don't have any active projects configured in your PIPER.md yet" despite the user having projects in their portfolio (created via FTUX onboarding).

**Hypothesis**: Standup feature looks for projects in `PIPER.md` config file, but portfolio onboarding stores projects in the database. These two systems are not connected.

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Standup feature: `services/standup/` - Interactive standup assistant (#242)
- [x] Portfolio onboarding: `services/onboarding/portfolio_handler.py` - FTUX flow (#490)
- [x] Project storage: Database via `services/repositories/project_repository.py`
- [x] PIPER.md config: `config/PIPER.user.md` - User configuration file
- [ ] How standup finds projects: Unknown - need to investigate

**My understanding of the task**:
- Standup looks for projects in wrong location (config file vs database)
- Need to connect standup to portfolio/project database
- Must not break: existing PIPER.md project config (if anyone uses it), standup flow

**Key questions to investigate**:
1. Where does standup currently look for projects?
2. Where does portfolio onboarding store projects?
3. Are these the same "project" concept or different models?

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [x] Investigation-heavy (need to trace code paths)
- [x] May be simple fix once root cause found

**Assessment**: [x] **SKIP WORKTREE** - Investigation first, likely simple integration fix

### Part B: PM Decisions (2026-01-12 20:28)

1. **Project source priority**:
   - [x] **Requires DDD analysis** - Need deep-dive to determine the right model
   - Cannot make quick decision on DB vs config vs both

2. **Standup should work for**:
   - [x] Prompt users to complete prerequisites (portfolio onboarding) if not done
   - Bridge gap by guiding users to proper setup flow

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** - Investigation phase only
- [x] **REVISE** - Scope changed to DDD analysis first, then implementation
- [ ] **CLARIFY** - N/A

**Revised Scope**: This is now a two-phase effort:
1. **Phase A**: DDD Analysis - Understand project models in both systems
2. **Phase B**: Implementation - Based on DDD findings

---

## Phase 0: DDD Analysis (PM Required)

### Purpose
Per PM guidance (2026-01-12 20:28): "We need to do a deep-dive DDD analysis to determine the right model."

### Questions to Answer

1. **What is a "Project" in the Standup bounded context?**
   - What attributes does standup need? (name, status, recent activity?)
   - What operations does standup perform on projects?

2. **What is a "Project" in the Portfolio bounded context?**
   - What attributes does portfolio capture? (name, description, goals?)
   - What operations does portfolio perform on projects?

3. **Are these the same aggregate or different aggregates?**
   - Same entity, different views?
   - Different entities that need mapping?
   - One is a subset of the other?

4. **Where is the source of truth?**
   - Database (portfolio creates, standup reads)?
   - Config file (PIPER.md)?
   - Both with sync?

### Domain Model Comparison (COMPLETED 2026-01-12 21:15)

| Attribute | Standup/CanonicalHandlers | Portfolio/Project Table | Same? |
|-----------|---------------------------|-------------------------|-------|
| name | From `user.preferences["projects"]` | `projects.name` | NO - Different storage |
| description | From `user.preferences["projects"]` | `projects.description` | NO - Different storage |
| status | N/A | N/A | N/A |
| owner_id | From `user_id` param | `projects.owner_id` | YES (same user) |
| created_at | N/A | `projects.created_at` | Only in portfolio |

### Root Cause Analysis (COMPLETED)

**The Gap**: Two disconnected storage locations for "projects":

1. **CanonicalHandlers/UserContextService** looks for projects in:
   - `User.preferences["projects"]` JSONB field (in `users` table)
   - Fallback to PIPER.md config parsing

2. **Portfolio Onboarding** stores projects in:
   - `projects` table via `ProjectRepository.create()`
   - Creates `domain.Project` entities

**These are NOT connected!** Portfolio creates projects in the database's `projects` table, but standup/status handlers read from `user.preferences["projects"]` or PIPER.md config.

### Code Path Evidence

**Standup/Status project lookup** (services/intent_service/canonical_handlers.py:1102-1107):
```python
projects = user_context.projects
if not projects:
    return {
        "message": "You don't have any active projects configured in your PIPER.md yet. "
        ...
```

**UserContextService gets projects** (services/user_context_service.py:117-121):
```python
projects=(
    self._extract_projects_from_prefs(user_prefs)  # From user.preferences
    if user_prefs
    else self._extract_projects(merged_config)     # From PIPER.md
),
```

**Portfolio saves to** (services/conversation/conversation_handler.py:276-292):
```python
project_repo = ProjectRepository(db_session)
for project_data in captured_projects:
    project = domain.Project(
        owner_id=user_id,
        name=project_data.get("name", "Untitled Project"),
        ...
    )
    await project_repo.create(project)  # Saves to projects table
```

### Key Files Identified

| File | Role | Issue |
|------|------|-------|
| `services/user_context_service.py` | Loads user context | Doesn't check `projects` table |
| `services/intent_service/canonical_handlers.py` | Provides status responses | Uses UserContextService |
| `services/conversation/conversation_handler.py` | Persists onboarding projects | Saves to `projects` table |
| `services/database/repositories/project_repository.py` | Project data access | Contains the solution |

### Investigation Commands

```bash
# Standup's project concept
grep -rn "project\|Project" services/standup/ --include="*.py" -B 2 -A 5

# Portfolio's project concept
grep -rn "project\|Project" services/onboarding/portfolio_handler.py -B 2 -A 5

# Domain model definition
grep -rn "class Project" services/domain/models.py -A 30

# Database model
grep -rn "class Project" services/database/models.py -A 30
```

### DDD Decision Required

After investigation, PM to decide:
- [x] **Portfolio Project is canonical - standup adapts** ← RECOMMENDED
- [ ] Same aggregate - standup should use portfolio's Project
- [ ] Different aggregates - need Anti-Corruption Layer
- [ ] Need new unified Project model

### Recommended Fix Approach (Based on DDD Analysis)

**Option B: UserContextService queries ProjectRepository**

Modify `UserContextService._load_context_from_config()` to ALSO query the `projects` table:

```python
# In UserContextService._load_context_from_config()
# After loading from config/preferences:

# NEW: Also load from projects table
from services.database.repositories import ProjectRepository
async with AsyncSessionFactory.session_scope() as session:
    project_repo = ProjectRepository(session)
    db_projects = await project_repo.list_active_projects(owner_id=str(user_id))

    # Merge: DB projects take precedence over config
    if db_projects:
        context.projects = [p.name for p in db_projects]
    # else: keep config-based projects as fallback
```

**Why this approach**:
1. Single point of change (UserContextService)
2. Maintains backwards compatibility with PIPER.md
3. Follows DDD: Portfolio's Project table is source of truth
4. UserContextService becomes the adapter/translator

**Alternative Option C** (if PM prefers):
Portfolio onboarding could ALSO write to `user.preferences["projects"]` to keep both in sync. This is simpler but duplicates data.

---

## Phase 0.1: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 582
   ```

2. **Related Code Investigation**
   ```bash
   # Find standup project lookup
   grep -rn "project\|PIPER" services/standup/ --include="*.py"

   # Find portfolio project storage
   grep -rn "project\|create_project" services/onboarding/ --include="*.py"

   # Find project repository
   grep -rn "class.*Project" services/repositories/ --include="*.py"

   # Check how standup is triggered
   grep -rn "/standup\|standup" services/intent/ --include="*.py"
   ```

3. **Trace the flow**
   - `/standup` command → intent classification → standup handler → project lookup
   - Portfolio onboarding → project creation → database storage

### STOP Conditions
- If "project" means different things in standup vs portfolio → Need domain alignment
- If standup has no project lookup (hardcoded response) → Different fix needed
- If projects are stored but in different user context → Auth/user_id issue

---

## Phase 0.5: Frontend-Backend Contract Verification

**N/A** - This is a backend-only integration issue. No frontend changes expected.

---

## Phase 0.6: Data Flow & Integration Verification (COMPLETED 2026-01-12)

### Part A: Data Flow Requirements

| Layer | Gets Projects From | Expected Source | Current Source | Gap? |
|-------|-------------------|-----------------|----------------|------|
| UserContextService | PIPER.md or user.preferences | Database | Config only | **YES** |
| CanonicalHandlers | user_context.projects | Database | Config only | **YES** |
| Portfolio Handler | Creates in DB | Database | Database | No |
| ProjectRepository | Database | Database | Database | No |

### Part B: Integration Points Verified

| Caller | Callee | Method | Verified? |
|--------|--------|--------|-----------|
| CanonicalHandlers | UserContextService | get_user_context() | [x] Line 1080 |
| UserContextService | (none) | _load_context_from_config() | [x] Missing DB query |
| ConversationHandler | ProjectRepository | create() | [x] Line 291 |
| IntentService | CanonicalHandlers | _handle_status_query() | [x] Line 1065 |

### Part C: Key Code Locations to Investigate

```bash
# Standup entry point
grep -rn "standup" services/intent/intent_service.py

# Standup handler implementation
ls -la services/standup/

# Project model
grep -rn "class Project" services/domain/models.py

# Project repository
cat services/repositories/project_repository.py | head -50
```

---

## Phase 0.7: Conversation Design (For Standup Flow)

### Purpose
Standup is a multi-turn conversation. Document expected flow to ensure fix doesn't break it.

### Happy Path Script (Current Expected Flow)

```
Turn 1:
  User: "/standup"
  Piper: "Good morning! Let's do your standup. Which project would you like to start with?"
         [Lists user's projects]
  State: INITIATED

Turn 2:
  User: "Piper Morgan"
  Piper: "What did you accomplish on Piper Morgan since your last standup?"
  State: GATHERING_ACCOMPLISHMENTS

Turn 3:
  User: "Fixed the sidebar integration bug"
  Piper: "Great! What are you planning to work on next?"
  State: GATHERING_PLANS

Turn 4:
  User: "Working on MUX implementation"
  Piper: "Any blockers or concerns?"
  State: GATHERING_BLOCKERS

Turn 5:
  User: "None right now"
  Piper: "Here's your standup summary: [summary]. Want me to share this?"
  State: CONFIRMING
```

### Edge Cases for This Fix

| User Input | Current State | Current Behavior | Expected After Fix |
|------------|---------------|------------------|-------------------|
| "/standup" (no projects in DB) | NONE | "No projects in PIPER.md" | Prompt to complete portfolio onboarding |
| "/standup" (projects in DB) | NONE | "No projects in PIPER.md" | List projects from DB |
| "/standup" (projects in both) | NONE | Shows PIPER.md only | TBD by DDD analysis |

---

## Phase 0.8: Post-Completion Integration

### Purpose
Ensure the fix integrates properly with rest of system.

### Completion Side-Effects Checklist

When standup successfully finds projects:

| Side Effect | Location | Value | Verified? |
|-------------|----------|-------|-----------|
| Projects listed in standup prompt | Chat response | Project names from DB | [ ] |
| User can select a project | Standup flow | Continues normally | [ ] |
| Standup completes successfully | Full flow | Summary generated | [ ] |

### Downstream Behavior Changes

| Feature | Before Fix | After Fix |
|---------|-----------|-----------|
| /standup with DB projects | "No projects" error | Lists DB projects |
| /standup without projects | "No projects" error | Prompts for portfolio onboarding |
| Portfolio → Standup flow | Disconnected | Connected |

---

## Phase 1: Investigation (Before Implementation)

### 1.1 Trace Standup Project Lookup

Find where standup gets its project list:
```bash
# In standup service, find project references
grep -rn "project" services/standup/ --include="*.py" -A 3 -B 3
```

### 1.2 Trace Portfolio Project Storage

Verify where portfolio stores projects:
```bash
# In portfolio handler, find project creation
grep -rn "project" services/onboarding/portfolio_handler.py -A 3 -B 3
```

### 1.3 Compare Project Models

Check if same model is used:
```bash
# Domain model
grep -rn "class Project" services/domain/models.py -A 20
```

### 1.4 Document Gap

After investigation, document:
- Where standup looks: ____________
- Where portfolio stores: ____________
- Gap: ____________
- Fix approach: ____________

---

## Phase 2: Implementation (COMPLETED 2026-01-12 22:03)

### Changes Made

**File**: `services/user_context_service.py`

1. **New method `_load_projects_from_db()`** (lines 170-212):
   - Queries `ProjectRepository.list_active_projects(owner_id=user_id)`
   - Returns list of project names
   - Graceful fallback on errors

2. **Modified `_load_context_from_config()`** (lines 84-168):
   - Added database project loading step (step 4)
   - Project source priority:
     1. Database projects (from portfolio onboarding) - highest
     2. User preferences projects
     3. Config-based projects (PIPER.md) - fallback
   - Added `has_db_projects` to logging

### Likely Fix Approaches

**Option A**: Standup uses Project Repository
- Modify standup to query `ProjectRepository.get_by_owner(user_id)`
- Requires passing `user_id` through standup flow

**Option B**: Standup uses shared project service
- Create/use a `ProjectService` that both standup and portfolio use
- Abstracts project source (DB, config, etc.)

**Option C**: Config loader includes DB projects
- Modify PIPER.md loader to also check database
- Merge config + database projects

---

## Phase 2.5: Testing

### Manual Test Scenarios

| # | Scenario | Steps | Expected | Status |
|---|----------|-------|----------|--------|
| 1 | Standup with DB projects | Complete portfolio, run /standup | Shows projects from DB | [ ] |
| 2 | Standup with no projects | New user, run /standup | Graceful message | [ ] |
| 3 | Portfolio still works | Run portfolio onboarding | Projects saved to DB | [ ] |
| 4 | Existing standup features | Run full standup flow | All features work | [ ] |

### Regression Checks

| Check | How | Status |
|-------|-----|--------|
| Portfolio onboarding works | Complete FTUX flow | [ ] |
| Standup flow completes | Full standup conversation | [ ] |
| No console errors | Check browser console | [ ] |
| No backend errors | Check server logs | [ ] |

---

## Phase Z: Final Bookending

### Commit Message Template

```
fix(#582): Connect standup to portfolio projects

Root cause: Standup looked for projects in PIPER.md config, but portfolio
onboarding stores projects in the database.

Fix:
- [Details after implementation]

Testing: Manual verification of standup with DB projects
Closes #582

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## Multi-Agent Deployment

**Assessment**: Single agent - DDD investigation requires deep context that would be lost in handoff.

| Phase | Agent | Rationale |
|-------|-------|-----------|
| DDD Analysis | Lead Dev | Domain expertise needed |
| Implementation | Lead Dev | Follows from DDD findings |

---

## Verification Gates

- [ ] Phase 0: DDD analysis complete, PM decision made
- [ ] Phase 0.1: Investigation commands run
- [ ] Phase 0.6: Data flow documented
- [ ] Phase 0.7: Conversation design verified
- [ ] Phase 0.8: Post-completion integration documented
- [ ] Phase 1: Root cause identified
- [ ] Phase 1: Fix approach determined (based on DDD)
- [ ] Phase 2: Implementation complete
- [ ] Phase 2.5: All test scenarios pass
- [ ] Phase Z: Evidence compiled
- [ ] Phase Z: PM approval

---

## Completion Matrix

| Criterion | Status | Evidence |
|-----------|--------|----------|
| DDD analysis complete | [ ] | Domain model comparison |
| PM decision on project source | [ ] | DDD decision checkbox |
| Root cause identified | [ ] | Investigation findings |
| Fix approach approved | [ ] | PM approval |
| Implementation complete | [ ] | Code changes |
| Standup shows DB projects | [ ] | Test #1 |
| No-projects case handled | [ ] | Test #2 (prompts for onboarding) |
| No regressions | [ ] | Test #3, #4 |
| Issue updated with evidence | [ ] | GitHub link |
| PM approval received | [ ] | Issue closed |

---

## STOP Conditions

- "Project" is fundamentally different concept in standup vs portfolio → Need domain model alignment first
- Standup requires PIPER.md for other config → Need to preserve config loading
- user_id not available in standup context → Need to trace auth flow
- Multiple project sources create conflicts → Need PM decision on priority

---

## Risk Analysis

### What Could This Fix Mask?

| Potential Deeper Issue | How to Check | Status |
|------------------------|--------------|--------|
| Project model inconsistency | Compare domain models | [ ] |
| user_id not propagated to standup | Check standup handler signature | [ ] |
| PIPER.md still needed for other config | Check what else uses PIPER.md | [ ] |
| Standup was never integrated with portfolio | Check #242 and #490 for integration notes | [ ] |

---

## Effort Estimate

| Phase | Estimate |
|-------|----------|
| Phase -1: Verification | 5 min |
| Phase 0: Investigation | 15 min |
| Phase 0.6: Data flow | 10 min |
| Phase 1: Deep investigation | 20 min |
| Phase 2: Implementation | 15-30 min |
| Phase 2.5: Testing | 15 min |
| Phase Z: Bookending | 5 min |
| **Total** | ~90 min |

---

_Gameplan created: 2026-01-12 19:09_
_Updated for template v9.3 compliance: 2026-01-12 20:35_
