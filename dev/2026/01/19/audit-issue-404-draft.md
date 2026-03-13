# Issue #404 Draft Audit vs Template

**Draft**: `issue-404-draft.md`
**Template**: `.github/ISSUE_TEMPLATE/feature.md` (283 lines)
**Audit Date**: 2026-01-19

---

## Template Coverage Matrix

| Template Section | Lines | Present in Draft | Compliant | Gap/Notes |
|-----------------|-------|------------------|-----------|-----------|
| Header (Priority, Labels, Milestone, Epic) | 10-16 | ❌ Missing | ❌ | Need to add |
| Problem Statement | 19-31 | ✅ | ✅ | Good |
| Goal | 34-45 | ✅ | ✅ | Has Example UX |
| What Already Exists | 49-55 | ✅ | ✅ | Good |
| Requirements (Phases) | 59-85 | ✅ | ⚠️ | Missing Phase 0 |
| Acceptance Criteria | 88-110 | ✅ | ✅ | Has 4 categories |
| Completion Matrix | 114-139 | ✅ | ⚠️ | Missing Evidence Link column |
| Testing Strategy | 143-162 | ✅ | ⚠️ | Missing Manual Testing Checklist |
| Success Metrics | 165-175 | ✅ | ✅ | Good |
| STOP Conditions | 178-190 | ✅ | ⚠️ | Missing some standard conditions |
| Effort Estimate | 194-205 | ✅ | ✅ | Good breakdown |
| Dependencies | 209-217 | ✅ | ⚠️ | Missing "Optional" section |
| Related Documentation | 220-224 | ✅ | ✅ | Good |
| Evidence Section | 228-246 | ❌ Missing | ❌ | Template placeholder needed |
| Completion Checklist | 250-262 | ❌ Missing | ❌ | Need to add |
| Notes for Implementation | 267-269 | ❌ Missing | ❌ | Need to add |
| Footer reminder | 273-282 | ❌ Missing | ❌ | Need to add |

---

## Required Fixes

### 1. Add Header Section
```markdown
**Priority**: P1
**Labels**: `MUX`, `foundation`, `documentation`
**Milestone**: MVP
**Epic**: MUX-VISION (#401)
**Related**: #399, #400, #612, #613, ADR-045
```

### 2. Add Phase 0: Investigation & Setup
Currently starts at Phase 1. Template requires Phase 0 if investigation needed.

```markdown
### Phase 0: Setup & Context (1 hour)

**Objective**: Verify infrastructure and gather context

**Tasks**:
- [ ] Verify #613 (P1) complete and infrastructure available
- [ ] Review P0 analysis documents
- [ ] Identify list of major features to audit

**Deliverables**:
- Feature list for audit scope
- Confirmed access to P1 infrastructure
```

### 3. Update Completion Matrix Format
Add Evidence Link column per template:

```markdown
| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Grammar compliance audit | ❌ | [pending] |
| Application patterns (5+) | ❌ | [pending] |
| Transformation guide | ❌ | [pending] |
| Worked example | ❌ | [pending] |
| Anti-flattening tests (10+) | ❌ | [pending] |
| Test fixtures (2) | ❌ | [pending] |
| Developer guide | ❌ | [pending] |
```

### 4. Add Manual Testing Checklist
Template requires explicit manual testing scenarios:

```markdown
### Manual Testing Checklist

**Scenario 1**: Pattern Application
1. [ ] Developer reads transformation guide
2. [ ] Developer applies pattern to sample feature without asking questions
3. [ ] Result expresses grammar correctly

**Scenario 2**: Anti-Flattening Detection
1. [ ] Run anti-flattening tests against Morning Standup
2. [ ] All tests pass
3. [ ] Run against intentionally flattened fixture
4. [ ] Tests correctly fail
```

### 5. Expand STOP Conditions
Template has 8 standard conditions; draft has 4 custom ones. Merge:

```markdown
## STOP Conditions

**Standard STOP conditions**:
- Infrastructure doesn't match assumptions
- Tests fail for any reason
- Pattern might already exist elsewhere
- Can't provide verification evidence
- Completion bias detected

**Domain-specific STOP conditions**:
- #399 P1 infrastructure doesn't support pattern needs
- Anti-flattening criteria conflict with existing features
- Morning Standup patterns can't be generalized
- Guide becomes too abstract (no practical examples)
```

### 6. Add Evidence Section (Template)
```markdown
## Evidence Section

[This section is filled in during/after implementation]

### Implementation Evidence
```bash
[Terminal output showing tests passing]
[Commit hashes with descriptions]
```

### Cross-Validation (if applicable)
**Verified By**: [Agent name]
**Date**: [Date]
```

### 7. Add Completion Checklist
```markdown
## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met
- [ ] Completion matrix 100%
- [ ] Evidence provided for each criterion
- [ ] Tests passing with output
- [ ] Documentation updated
- [ ] No regressions confirmed
- [ ] STOP conditions all clear
- [ ] Session log complete
```

### 8. Add Notes for Implementation
```markdown
## Notes for Implementation

- This is documentation/pattern-heavy work, not primarily coding
- Morning Standup is the reference implementation - study it deeply
- Anti-flattening tests should be aspirational, catching obvious violations
- Transformation example should be realistic but not overly complex
```

### 9. Add Footer
```markdown
---

**Remember**:
- Quality over speed (Time Lord philosophy)
- Evidence required for all claims
- No 80% completions
- PM closes issues after approval

---

_Issue created: 2026-01-19_
_Last updated: 2026-01-19_
```

---

## Recommendations Summary

| Priority | Fix | Effort |
|----------|-----|--------|
| Must | Add Header | 1 min |
| Must | Add Phase 0 | 2 min |
| Must | Fix Completion Matrix format | 1 min |
| Must | Add Evidence Section | 1 min |
| Must | Add Completion Checklist | 1 min |
| Should | Add Manual Testing Checklist | 2 min |
| Should | Expand STOP Conditions | 2 min |
| Should | Add Notes for Implementation | 1 min |
| Should | Add Footer | 1 min |

**Total effort**: ~12 minutes to fully comply with template

---

## Audit Result

**Current Compliance**: ~70%
**After Fixes**: 100%

**Recommendation**: Apply all fixes before pushing to GitHub.
