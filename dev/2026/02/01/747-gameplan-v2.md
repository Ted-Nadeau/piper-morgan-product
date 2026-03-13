# Gameplan v2: #747 - Timezone-Aware DateTime Implementation

**Issue**: #747 (Parent) with children #750-#755
**Created**: 2026-02-01 12:15
**Priority**: P2
**Total Estimate**: 4-6 hours with parallel execution

---

## Phase -1: Infrastructure Verification

**Work Characteristics Assessment**:
- [x] Multiple agents will work in parallel on different files/features
- [x] Task duration >30 minutes
- [x] Multi-component work

**Assessment**: Multi-agent deployment appropriate. Children can run in parallel after Phase 1.

**Infrastructure Verified**:
- Database: PostgreSQL on port 5433 with timestamptz
- ORM: SQLAlchemy with DateTime(timezone=True) support
- Schema validation exists (#484)
- Some models already fixed (ConversationalMemoryEntryDB)
- 47 DateTime columns need fixing
- 239 utcnow() calls need replacing

---

## Child Issue Structure

| Issue | Phase | Agent | Scope | Blocks |
|-------|-------|-------|-------|--------|
| #750 | 1 | Agent A | datetime_utils module | #751-754 |
| #751 | 2 | Agent B | Model columns (47) | #755 |
| #752 | 3A | Agent C | services/database/ | #755 |
| #753 | 3B | Agent D | services/ (excl. database/) | #755 |
| #754 | 3C | Agent E | web/, tests/ | #755 |
| #755 | 4 | Validator | Cross-validation | Closes #747 |

---

## Execution Flow

```
                    ┌──────────────┐
                    │    #750      │
                    │ datetime_utils│
                    │   (Phase 1)   │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │    #751      │ │    #752      │ │    #753      │
    │Model Columns │ │ database/    │ │ services/    │
    │  (Phase 2)   │ │ (Phase 3A)   │ │ (Phase 3B)   │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │               │               │
           │               │        ┌──────────────┐
           │               │        │    #754      │
           │               │        │ web/tests/   │
           │               │        │ (Phase 3C)   │
           │               │        └──────┬───────┘
           │               │               │
           └───────────────┴───────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    #755      │
                    │  Validation  │
                    │  (Phase 4)   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Close #747  │
                    └──────────────┘
```

---

## Phase 1: datetime_utils Module (#750)

**Agent**: Code Agent A
**Log**: `dev/2026/02/01/HHMM-747-utils-log.md`
**Blocks**: All other phases

### Agent Instructions

```markdown
You are Code Agent A working on Piper Morgan.

**Task**: Create datetime_utils module for #750 (child of #747)
**GitHub Issue**: #750

**TDD Protocol**:
1. Write failing tests first in tests/unit/services/utils/test_datetime_utils.py
2. Implement services/utils/datetime_utils.py to make tests pass
3. Achieve 100% coverage

**Required Functions**:
- utc_now() → datetime.now(timezone.utc)
- ensure_utc(dt) → converts naive to UTC-aware, passes through aware
- is_timezone_aware(dt) → returns bool

**Evidence Required**:
- Test output showing all pass
- Coverage report showing 100%

**Session Log**: Create dev/2026/02/01/HHMM-747-utils-log.md

**When Complete**: Comment on #750 with evidence, mark ready for review.
```

---

## Phase 2: Model DateTime Columns (#751)

**Agent**: Code Agent B
**Log**: `dev/2026/02/01/HHMM-747-models-log.md`
**Depends On**: #750

### Agent Instructions

```markdown
You are Code Agent B working on Piper Morgan.

**Task**: Fix DateTime model columns for #751 (child of #747)
**GitHub Issue**: #751
**Depends On**: #750 must be complete (datetime_utils available)

**TDD Protocol**:
1. Write test that verifies all DateTime columns have timezone=True
2. Update services/database/models.py (47 columns)
3. Verify schema validation passes

**Pattern**:
Column(DateTime, default=datetime.utcnow)
→ Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

**Evidence Required**:
- Grep showing 0 DateTime columns without timezone=True
- Schema validation output
- Test results

**Session Log**: Create dev/2026/02/01/HHMM-747-models-log.md

**When Complete**: Comment on #751 with evidence, mark ready for review.
```

---

## Phase 3A-C: Replace utcnow() (#752, #753, #754)

**Agents**: Code Agents C, D, E (parallel)
**Depends On**: #750

### Agent C Instructions (#752 - services/database/)

```markdown
You are Code Agent C working on Piper Morgan.

**Task**: Replace utcnow() in services/database/ for #752
**GitHub Issue**: #752
**Depends On**: #750 must be complete

**Scope**: services/database/ only

**Pattern**:
datetime.utcnow() → datetime.now(timezone.utc)

**Evidence Required**:
- Grep showing 0 utcnow() in services/database/
- Test results for services/database/

**Session Log**: Create dev/2026/02/01/HHMM-747-group-a-log.md

**When Complete**: Comment on #752 with evidence.
```

### Agent D Instructions (#753 - services/ excluding database/)

```markdown
You are Code Agent D working on Piper Morgan.

**Task**: Replace utcnow() in services/ (excluding database/) for #753
**GitHub Issue**: #753
**Depends On**: #750 must be complete

**Scope**: services/ excluding services/database/

**Pattern**:
datetime.utcnow() → datetime.now(timezone.utc)

**Evidence Required**:
- Grep showing 0 utcnow() in scope
- Test results

**Session Log**: Create dev/2026/02/01/HHMM-747-group-b-log.md

**When Complete**: Comment on #753 with evidence.
```

### Agent E Instructions (#754 - web/ and tests/)

```markdown
You are Code Agent E working on Piper Morgan.

**Task**: Replace utcnow() in web/ and tests/ for #754
**GitHub Issue**: #754
**Depends On**: #750 must be complete

**Scope**: web/ and tests/

**Special Note**: For test files, verify mocks still work correctly.

**Pattern**:
datetime.utcnow() → datetime.now(timezone.utc)

**Evidence Required**:
- Grep showing 0 utcnow() in scope
- Full test suite passes

**Session Log**: Create dev/2026/02/01/HHMM-747-group-c-log.md

**When Complete**: Comment on #754 with evidence.
```

---

## Phase 4: Cross-Validation (#755)

**Agent**: Validation Agent
**Log**: `dev/2026/02/01/HHMM-747-validation-log.md`
**Depends On**: #750-754 all complete

### Validator Instructions

```markdown
You are the Validation Agent for #747 timezone support.

**Task**: Cross-validate all changes for #755
**GitHub Issue**: #755
**Depends On**: #750, #751, #752, #753, #754 must all be complete

**Adversarial Checks**:
1. grep -rn "datetime.utcnow" services/ web/ tests/ --include="*.py" | wc -l → must be 0
2. grep -n "Column(DateTime," services/database/models.py | grep -v "timezone=True" | wc -l → must be 0
3. Full test suite passes with 0 deprecation warnings about utcnow
4. Schema validation shows 0 mismatches (or 1 documented for embedding_vector)

**Cross-Validation Report**: Use template in #755 issue

**Session Log**: Create dev/2026/02/01/HHMM-747-validation-log.md

**When Complete**:
- If APPROVE: Comment on #755 and #747 with final evidence
- If REVISE: Comment on relevant child issue with findings
```

---

## Phase Z: Completion

### When All Children Complete

1. Validation Agent confirms all checks pass (#755)
2. Lead Developer reviews all session logs
3. Update #747 completion matrix with evidence links
4. Close child issues #750-755
5. Close parent #747 with summary

### Final Evidence for #747

```bash
# Zero utcnow()
grep -rn "datetime.utcnow" services/ web/ tests/ --include="*.py" | wc -l

# Zero DateTime without timezone
grep -n "Column(DateTime," services/database/models.py | grep -v "timezone=True" | wc -l

# Tests pass
PYTHONPATH=. python -m pytest tests/unit/ -v --tb=short 2>&1 | tail -5

# No deprecation warnings
PYTHONPATH=. python -m pytest tests/unit/ 2>&1 | grep -c "utcnow"
```

---

## STOP Conditions

- Tests fail after changes → investigate, don't proceed
- Schema validation shows new errors → investigate
- API datetime format changes → may need serialization fix
- Performance degradation → profile and assess
- Need data migration → out of scope, escalate

---

## Session Log Requirements

Each agent MUST maintain their own session log:

```markdown
# Session Log: YYYY-MM-DD-HHMM-747-[component]-log.md

**Role**: [Agent role]
**Issue**: #[number]
**Date**: [date]

## Work Log

### [time] - Started
- Read issue #[number]
- Verified dependencies complete

### [time] - TDD Phase
- Wrote tests: [test file]
- Tests failing as expected: [output]

### [time] - Implementation
- Modified: [files]
- Evidence: [grep/test output]

### [time] - Verification
- All tests pass: [output]
- Grep verification: [output]

## Evidence Summary
[Consolidated evidence for issue closure]
```

---

## Gameplan Audit Checklist

- [x] Phase -1 infrastructure verified
- [x] Child issues created (#750-755)
- [x] Dependency graph documented
- [x] Agent instructions prepared
- [x] TDD protocol specified
- [x] Evidence requirements defined
- [x] Session log requirements defined
- [x] STOP conditions listed
- [x] Phase Z completion criteria defined

**Gameplan Status**: READY FOR EXECUTION
