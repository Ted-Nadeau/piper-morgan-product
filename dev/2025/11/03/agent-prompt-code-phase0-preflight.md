# Code Agent: Phase 0 - Pre-Flight Checklist for Domain Model Refactoring

## Your Identity
You are Code Agent (Claude Code with Sonnet 4.5), a specialized development agent with broad codebase investigation capabilities. You will be leading Phase 0 of a multi-phase domain model refactoring.

## Session Log Management

**Continue your existing session log**: `dev/2025/11/03/2025-11-03-0615-prog-code-log.md`

Add a new major section for this refactoring work:
```markdown
---

## Domain Model Foundation Repair - Phase 0: Pre-Flight (4:11 PM)

**Mission**: Document complete current state before refactoring begins
**Gameplan**: `gameplan-domain-model-refactoring.md`
**Estimated Time**: 2 hours
```

---

## Mission

**Understand exactly what we're refactoring before touching anything.**

This is Phase 0 of a 5-phase domain model refactoring. Your job is to create a comprehensive snapshot of the current todo implementation so we know exactly what we're changing and can verify nothing breaks.

**Core Principle**: "Measure twice, cut once" - thorough documentation now prevents mistakes later.

---

## Context

**The Big Picture**:
We're implementing PM's original architectural vision where **Item and List are cognitive primitives**, with todos being one specialization. This enables future shopping lists, reading lists, etc.

**The Refactoring**:
- Todo will extend Item (base class)
- `todo.title` → `todo.text` (Item property)
- Database schema: polymorphic table structure
- Service layer: ItemService base, TodoService extends it

**Why Phase 0 Matters**:
- We're changing foundational architecture
- Need safety nets before touching anything
- Must document baseline for comparison
- Sets up branch structure for all future phases

**Your Role**: Create the complete map of current state

**Gameplan Reference**: See `gameplan-domain-model-refactoring.md` Phase 0 section

---

## Phase 0 Tasks (2 hours)

### Task 1: Document Current Todo Implementation (45 min)

**Create `docs/refactor/` directory structure**:
```bash
mkdir -p docs/refactor
cd docs/refactor
```

**Document all todo-related code**:

1. **Find all Todo classes**:
```bash
# Find every class definition
grep -r "class Todo" . --include="*.py" -n > current-todo-classes.txt

# Also check for TodoDB, TodoRepository, TodoService, etc.
grep -r "class Todo[A-Z]" . --include="*.py" -n >> current-todo-classes.txt
```

2. **Find all todo property usage**:
```bash
# Critical: Find all uses of todo.title (will become todo.text)
grep -r "\.title" . --include="*.py" | grep -i todo > current-todo-title-usage.txt

# Find all Todo instantiations
grep -r "Todo(" . --include="*.py" -n > current-todo-instantiations.txt

# Find all todo repository calls
grep -r "TodoRepository" . --include="*.py" -n > current-todo-repository-usage.txt
```

3. **Document database schema**:
```bash
# Find all migrations mentioning todos
grep -r "todos" alembic/ --include="*.py" -n > current-migrations.txt

# Look at database models
grep -A 50 "class TodoDB" services/database/models.py > current-todo-db-model.txt
```

4. **Document API surface**:
```bash
# Find all API endpoints
grep -r "@router" services/api/todo_management.py -A 5 > current-todo-api.txt

# Find all request/response models
grep -r "class Todo.*Request\|class Todo.*Response" . --include="*.py" -n > current-todo-api-models.txt
```

**Create summary document**: `docs/refactor/CURRENT-STATE-SUMMARY.md`
```markdown
# Todo Implementation - Current State

**Date**: [timestamp]
**Purpose**: Baseline documentation before domain model refactoring

## Key Files
- Domain Model: [path]
- Database Model: [path]
- Repository: [path]
- API: [path]
- Handlers: [path]

## Critical Properties
- Todo uses `.title` for text content
- Database table: `todos`
- [List other critical facts]

## Statistics
- Total todo-related classes: [count from grep]
- Uses of .title: [count]
- Repository methods: [count]
- API endpoints: [count]

## Dependencies
[List what depends on todos]
```

### Task 2: Document Current Test Coverage (30 min)

**Collect all todo tests**:
```bash
# Find all test files
find tests/ -name "*todo*.py" -type f > docs/refactor/current-test-files.txt

# Collect all test names
pytest tests/ -k "todo" --collect-only > docs/refactor/current-todo-tests.txt

# Get test count
pytest tests/ -k "todo" --collect-only | grep "test session starts" >> docs/refactor/current-test-count.txt
```

**Run baseline tests**:
```bash
# Run all todo tests and save output
pytest tests/ -k "todo" -v > docs/refactor/baseline-test-output.txt 2>&1

# Save pass/fail summary
pytest tests/ -k "todo" --tb=no > docs/refactor/baseline-test-summary.txt 2>&1
```

**Document in**: `docs/refactor/TEST-BASELINE.md`
```markdown
# Test Baseline - Before Refactoring

**Date**: [timestamp]
**Total Tests**: [count]
**Status**: [all passing? any failures?]

## Test Files
[List from current-test-files.txt]

## Test Coverage
- Unit tests: [count]
- Integration tests: [count]
- API tests: [count]

## Baseline Results
[Summary from pytest run]

## Critical Tests to Watch
[List tests that must still pass after refactoring]
```

### Task 3: Create Refactoring Branch (10 min)

**Git workflow**:
```bash
# Ensure we're on main and up to date
git checkout main
git pull

# Create feature branch
git checkout -b foundation/item-list-primitives

# Create empty commit to mark start
git commit --allow-empty -m "feat(domain): Begin domain model foundation repair

Starting multi-phase refactoring to implement Item/List primitives.
Todo will extend Item base class per original architectural vision.

Phase 0: Pre-flight checklist and documentation
Phases 1-4: Implementation
Phase 5: Validation

Ref: gameplan-domain-model-refactoring.md"

# Show we're on new branch
git log --oneline -1
git branch --show-current
```

### Task 4: Create Safety Net Configuration (15 min)

**Create rollback script**: `docs/refactor/ROLLBACK.md`
```markdown
# Rollback Procedures

## Quick Rollback
```bash
git checkout main
git branch -D foundation/item-list-primitives
```

## Per-Phase Rollback
- Phase 1: Revert primitives addition
- Phase 2: Revert Todo refactoring
- Phase 3: Revert service layer changes
- Phase 4: Revert integration

## Database Rollback
```bash
alembic downgrade -1  # Undo last migration
```

## Recovery Plan
[Steps to restore from backup if needed]
```

**Document backup locations**: `docs/refactor/BACKUPS.md`
```markdown
# Backup Information

**Pre-refactoring state**:
- Branch: main (before creating foundation/item-list-primitives)
- Commit: [git rev-parse HEAD]
- Date: [timestamp]

**Baseline Artifacts**:
- Test output: docs/refactor/baseline-test-output.txt
- Current state: docs/refactor/CURRENT-STATE-SUMMARY.md
- Database schema: [if applicable]

**To restore baseline**:
```bash
git checkout [commit hash]
```
```

### Task 5: Document API Contracts (20 min)

**Critical for backward compatibility**:

**Create**: `docs/refactor/API-CONTRACTS.md`
```markdown
# API Contracts - Must Maintain

## Todo Creation
**Endpoint**: POST /todos
**Request**:
```json
{
  "title": "string",  // WILL BECOME "text"
  "priority": "string"
}
```
**Response**: [document current response structure]

## Todo Retrieval
**Endpoint**: GET /todos/{id}
**Response**: [document current structure]

## Todo Update
[Document all endpoints]

## Breaking Changes to Manage
1. Request field rename: title → text
2. Response field rename: title → text
3. [Others]

## Backward Compatibility Strategy
[How we'll handle the title→text transition]
```

---

## Evidence Requirements

### Documentation Files Created:
- [ ] `docs/refactor/current-todo-classes.txt` (all class definitions)
- [ ] `docs/refactor/current-todo-title-usage.txt` (all .title references)
- [ ] `docs/refactor/current-todo-instantiations.txt` (all Todo() calls)
- [ ] `docs/refactor/current-todo-repository-usage.txt` (repository usage)
- [ ] `docs/refactor/current-migrations.txt` (database migrations)
- [ ] `docs/refactor/current-todo-db-model.txt` (DB model structure)
- [ ] `docs/refactor/current-todo-api.txt` (API endpoints)
- [ ] `docs/refactor/current-todo-api-models.txt` (request/response models)
- [ ] `docs/refactor/CURRENT-STATE-SUMMARY.md` (executive summary)

### Test Documentation:
- [ ] `docs/refactor/current-test-files.txt` (all test files)
- [ ] `docs/refactor/current-todo-tests.txt` (collected test names)
- [ ] `docs/refactor/current-test-count.txt` (test statistics)
- [ ] `docs/refactor/baseline-test-output.txt` (full test run)
- [ ] `docs/refactor/baseline-test-summary.txt` (pass/fail summary)
- [ ] `docs/refactor/TEST-BASELINE.md` (baseline documentation)

### Branch & Safety:
- [ ] Feature branch created: `foundation/item-list-primitives`
- [ ] Empty commit marking start
- [ ] On correct branch (git branch --show-current)
- [ ] `docs/refactor/ROLLBACK.md` (rollback procedures)
- [ ] `docs/refactor/BACKUPS.md` (backup information)
- [ ] `docs/refactor/API-CONTRACTS.md` (contracts to maintain)

### Summary Statistics (Required in Final Report):
- [ ] Total Todo-related classes found: [number]
- [ ] Total uses of `.title` property: [number]
- [ ] Total repository methods: [number]
- [ ] Total API endpoints: [number]
- [ ] Total tests found: [number]
- [ ] Baseline test pass rate: [percentage]
- [ ] Files that will need updating: [list of critical files]

---

## STOP Conditions

**STOP immediately and report if**:
- Any tests are currently failing (baseline broken)
- Cannot create refactoring branch (git issues)
- Missing critical todo functionality in codebase
- Unclear about current architecture
- Cannot find todo-related code where expected

**DO NOT**:
- Make ANY code changes (Phase 0 is documentation only)
- Modify any files (except creating docs/refactor/)
- Run migrations
- Touch database
- Implement anything (that's Phase 1+)

---

## Completion Criteria

**Must have ALL of these**:
1. ✅ Complete documentation in `docs/refactor/` directory
2. ✅ All grep outputs saved to files (evidence of investigation)
3. ✅ Test baseline established (pytest output saved)
4. ✅ Feature branch created and active
5. ✅ Rollback procedures documented
6. ✅ API contracts documented
7. ✅ Summary statistics in final report
8. ✅ CURRENT-STATE-SUMMARY.md completed
9. ✅ Zero code changes (documentation phase only)

**Final Report Format**:
```markdown
# Phase 0 Complete: Pre-Flight Checklist

**Duration**: [actual time]
**Files Created**: [count]
**Documentation Pages**: [count]

## Summary Statistics
- Todo classes found: [X]
- .title references: [X]
- Tests in baseline: [X] (all passing)
- Critical files to update: [list]

## Key Findings
1. [Important discovery 1]
2. [Important discovery 2]

## Ready for Phase 1
✅ Baseline documented
✅ Branch created
✅ Safety nets in place
✅ No blockers identified

**Next Phase**: Phase 1 - Create the Primitives
```

---

## Time Budget

- Task 1 (Document Implementation): 45 minutes
- Task 2 (Document Tests): 30 minutes
- Task 3 (Create Branch): 10 minutes
- Task 4 (Safety Nets): 15 minutes
- Task 5 (API Contracts): 20 minutes

**Total**: 2 hours

---

## Critical Reminders

1. **This is documentation only** - No code changes in Phase 0
2. **Thoroughness over speed** - We need complete baseline
3. **Evidence-based** - Every claim backed by grep output
4. **Safety first** - Branch isolation, rollback plans
5. **Think like an archaeologist** - Map everything before digging

**The goal**: When Phase 1 starts, we have a complete map of what we're changing

**Success metric**: Another developer could understand current todo implementation by reading your docs

---

## After Completion

**Report back with**:
1. Link to completed `docs/refactor/CURRENT-STATE-SUMMARY.md`
2. Summary statistics
3. Any surprises or concerns discovered
4. Confirmation all tests pass in baseline
5. Confirmation branch created successfully

Then we proceed to Phase 1: Create the Primitives.

Good luck! This documentation will be our roadmap for the entire refactoring. 🏰
