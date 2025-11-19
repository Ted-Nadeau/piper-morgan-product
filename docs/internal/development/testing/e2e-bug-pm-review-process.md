# E2E Bug PM Review Process (Phase 3)

## Overview

After all Phase 2 investigation reports are complete, the PM reviews them to identify patterns, group related bugs, and determine strategic fix approaches.

---

## Step 1: Pattern Recognition

### Group Bugs By:

#### Same Root Cause

- Multiple bugs with identical root cause hypothesis
- Same code path or component failing
- **Action**: Batch into single fix epic

#### Same Component/Domain

- Bugs affecting same domain concept or component
- May indicate design issue in that area
- **Action**: Consider refactoring if multiple bugs

#### Same Integration Boundary

- Bugs occurring at same integration point
- Component works in isolation, fails at boundaries
- **Action**: May require integration pattern review

#### Same Architectural Pattern

- Bugs revealing pattern failure
- Pattern not working as designed
- **Action**: May require architectural change (ADR)

---

## Step 2: Fix Strategy Decision

### Decision Matrix

| Bug Pattern                    | Fix Strategy         | Rationale                               |
| ------------------------------ | -------------------- | --------------------------------------- |
| Single isolated bug            | Isolated Fix         | No systemic impact, straightforward fix |
| Multiple bugs, same root cause | Batch Fix            | Fix root cause once, resolves all       |
| Multiple bugs, same component  | Refactoring Batch    | Design issue in component               |
| Bugs violate domain rules      | Domain Model Update  | Domain understanding gap                |
| Bugs reveal pattern failure    | Architectural Change | Pattern needs redesign (ADR required)   |

### Fix Strategy Types

#### Isolated Fixes

- **When**: Single bug, no systemic impact, clear root cause
- **Approach**: Direct fix following TDD
- **Requirements**: Test first, verify domain model, lock with regression tests

#### Refactoring Batch

- **When**: Multiple bugs indicate design issue in component
- **Approach**: Refactor component to eliminate bug class
- **Requirements**:
  - Create epic for refactoring
  - Write tests for all affected bugs
  - Refactor to eliminate root cause
  - Verify all bugs fixed

#### Domain Model Update

- **When**: Bugs reveal domain understanding gap
- **Approach**: Update domain model, then fix implementations
- **Requirements**:
  - Document domain model change
  - Update `services/domain/models.py`
  - Fix implementations to match new model
  - Update tests to reflect domain changes

#### Architectural Change

- **When**: Bugs indicate pattern failure
- **Approach**: Redesign pattern, document in ADR
- **Requirements**:
  - Create ADR documenting decision
  - Redesign pattern
  - Implement new pattern
  - Migrate affected code
  - Verify all bugs fixed

---

## Step 3: Fix Assignment

### Create Epic/Issue for Fix Batch

**Epic Template**:

- Title: `[Fix Batch] [Component/Pattern] - [Brief description]`
- Description: List all bugs included, root cause summary
- Acceptance Criteria:
  - All bugs in batch fixed
  - Tests prove fixes work
  - Regression tests prevent recurrence
  - Domain model respected
  - Documentation updated

### Assign to Agent

**Agent Selection**:

- **Claude Code**: Multi-file fixes, refactoring, domain model changes
- **Cursor**: UI fixes, isolated component fixes
- **Multi-Agent**: Architectural changes requiring coordination

### Requirements for Fix Assignment

**MANDATORY**:

- TDD approach (test first)
- Excellence Flywheel verification (check existing patterns first)
- Domain model compliance check
- Inchworm Protocol (complete 100% before moving on)

---

## Step 4: Review Fix Execution

### Verify Fix Protocol Followed

Check that agent followed:

1. ✅ Write Failing Test (TDD)
2. ✅ Verify Domain Model (DDD - check `services/domain/models.py`)
3. ✅ Find Existing Patterns (Excellence Flywheel - verification first)
4. ✅ Implement Minimal Fix (Inchworm - complete 100%)
5. ✅ Lock with Regression Tests
6. ✅ Document Decision (ADR if architectural change)
7. ✅ Verify with E2E Test (original bug scenario)

### Completion Criteria

- ✅ Original bug fixed
- ✅ Test proves fix works
- ✅ Regression tests prevent recurrence
- ✅ Domain model respected
- ✅ Documentation updated
- ✅ No workarounds introduced

---

## Decision Log

**Date**: YYYY-MM-DD
**Bugs Reviewed**: #[N], #[N], #[N]

**Patterns Identified**:

- [Pattern 1]: [Bugs included]
- [Pattern 2]: [Bugs included]

**Fix Strategy Decisions**:

- Bug #[N]: [Strategy] - [Rationale]
- Bug #[N]: [Strategy] - [Rationale]

**Epics Created**:

- Epic #[N]: [Title] - [Bugs included]

**Status**: [ ] Review complete, [ ] Fixes assigned, [ ] Fixes verified
