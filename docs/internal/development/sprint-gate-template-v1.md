# Sprint Completion Gate Template

**Issue Type**: Sprint Gate
**Parent**: [Sprint Epic, e.g., M0-GLUE]
**Labels**: `gate`, `process`, `required-for-close`

---

## Purpose

This gate ensures the sprint cannot close without verification that implementation is complete—not just "appears complete." It operationalizes lessons from the 75% Pattern (Aug 2025 stubs, Jan 2026 #728/#734).

**This issue blocks sprint closure until all criteria have explicit sign-off.**

---

## Gate 1: Persistence Layer Audit

**Purpose**: Verify that user-facing "success" messages correspond to actual database writes.

### Criteria

- [ ] **Success-to-DB Mapping**: Each user-visible success message traced to specific DB write
- [ ] **E2E Test Coverage**: Critical user flows have E2E tests that verify DB state (not mocked)
- [ ] **No Mock-Only Coverage**: Any flow with only mocked tests flagged for E2E addition

### Evidence Required

| Flow | Success Message | DB Table | E2E Test Name | Verified By |
|------|-----------------|----------|---------------|-------------|
| _example: Project creation_ | _"Added to portfolio"_ | _projects_ | _test_project_creation_persists_ | _[initials]_ |
| | | | | |
| | | | | |

### Sign-off

- [ ] **Persistence Audit Complete** — Signed: __________ Date: __________

---

## Gate 2: Anti-Flattening Verification

**Purpose**: Ensure implementation matches design intent and conversational quality standards.

### Criteria

- [ ] **Design Intent Check**: Implementation reviewed against source design doc (PDR, spec, or implementation guide)
- [ ] **No Parrot Confirmations**: Zero instances of repeating user input verbatim as confirmation
- [ ] **Colleague Test Applied**: New conversational flows reviewed with question "Would a human colleague respond this way?"
- [ ] **Forward Momentum**: Every response offers a path forward (no dead ends)

### Evidence Required

**Design Document Reference**: ___________________________

**Parrot Confirmation Audit**:
- Files reviewed: ___________________________
- Instances found: ___ (must be 0 to pass)
- If any found, fix PR: ___________________________

**Colleague Test Log**:
| Flow | Tested Phrase | Pass/Fail | Notes |
|------|---------------|-----------|-------|
| | | | |
| | | | |

### Sign-off

- [ ] **Anti-Flattening Verification Complete** — Signed: __________ Date: __________

---

## Gate 3: Multi-Tenancy Sanity Check

**Purpose**: Verify user-scoped data is actually user-scoped with no cross-user leakage.

*Skip if sprint has no user-data features. Mark N/A with justification.*

### Criteria

- [ ] **User Scoping Verified**: All new data storage includes `user_id` or `owner_id` in queries
- [ ] **No Default User Patterns**: Grep for `user_id="default"`, `owner_id=None`, hardcoded user references
- [ ] **Cross-User Test**: Explicit test that User A cannot see User B's data
- [ ] **RequestContext Threading**: New endpoints receive and use `RequestContext.user_id`

### Evidence Required

**Grep Results** (must be empty or justified):
```
grep -r "user_id=\"default\"" --include="*.py" services/ web/
grep -r "owner_id=None" --include="*.py" services/ web/
```
Result: ___________________________

**Cross-User Test Name**: ___________________________

**New Endpoints Audit**:
| Endpoint | Has RequestContext | Uses user_id | Verified |
|----------|-------------------|--------------|----------|
| | | | |

### Sign-off

- [ ] **Multi-Tenancy Check Complete** — Signed: __________ Date: __________
- [ ] **N/A** — Justification: ___________________________

---

## Final Sprint Closure

### All Gates Must Pass

- [ ] Gate 1: Persistence Layer Audit — PASSED
- [ ] Gate 2: Anti-Flattening Verification — PASSED
- [ ] Gate 3: Multi-Tenancy Sanity Check — PASSED or N/A

### Sprint Closure Authorization

**Sprint**: ___________________________
**Closure Date**: ___________________________
**Authorized By**: ___________________________

---

## Usage Notes

1. **Create this issue** when sprint epic is created
2. **Link as blocker** to sprint epic closure
3. **Fill in evidence** as work progresses (don't batch at end)
4. **Require sign-off** from someone other than primary implementer where possible
5. **Archive completed gates** in sprint retrospective

---

*Template Version: 1.0*
*Created: February 3, 2026*
*Origin: Ship #028 "Conversation ≠ Reality" learning*
