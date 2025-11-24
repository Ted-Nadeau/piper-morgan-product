---
name: Feature/Fix Implementation
about: Standard issue template for implementations (features, fixes, refactors)
title: '[LABEL] Brief Title'
labels: ''
assignees: ''
---

# [LABEL]-[SHORT-NAME] - [Full Title]

**Priority**: P0/P1/P2/P3
**Labels**: `[primary-label]`, `[secondary-label]`
**Milestone**: Sprint AX
**Epic**: [Epic Name if applicable]
**Related**: [Related issues, patterns, ADRs]

---

## Problem Statement

### Current State
[What's broken, missing, or suboptimal? Be specific.]

### Impact
- **Blocks**: [What can't be done without this?]
- **User Impact**: [How does this affect users/alpha testers?]
- **Technical Debt**: [What gets worse if we don't fix this?]

### Strategic Context
[Why now? How does this fit into larger goals?]

---

## Goal

**Primary Objective**: [One-sentence description of what success looks like]

**Example User Experience** (if applicable):
```
[Before/after scenario or user story]
```

**Not In Scope** (explicitly):
- ❌ [Thing that might seem related but isn't part of this]
- ❌ [Future enhancement that should wait]

---

## What Already Exists

### Infrastructure âœ… (if any)
[List components, patterns, or code that already exists and works]

### What's Missing ❌
[List specific gaps that need to be filled]

---

## Requirements

### Phase 0: Investigation & Setup (if needed)
[What needs to be verified before implementation starts?]

### Phase 1: [First Phase Name]
**Objective**: [What this phase accomplishes]

**Tasks**:
- [ ] [Specific task with clear completion criteria]
- [ ] [Another task]

**Deliverables**:
- [File or artifact created]
- [Evidence required]

### Phase 2: [Second Phase Name]
[Continue for each phase...]

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] Documentation updated
- [ ] GitHub issue fully updated
- [ ] Session log completed
- [ ] Cross-validation complete (if multi-agent)

---

## Acceptance Criteria

### Functionality
- [ ] [Specific feature works as described]
- [ ] [Another feature or behavior verified]
- [ ] [Edge case handled correctly]

### Testing
- [ ] Unit tests written and passing
- [ ] Integration tests passing (if applicable)
- [ ] Manual testing scenarios verified

### Quality
- [ ] No regressions introduced
- [ ] Performance meets requirements ([specific metric])
- [ ] Error handling implemented
- [ ] Security requirements met (if applicable)

### Documentation
- [ ] User-facing docs updated (if needed)
- [ ] Code documentation complete
- [ ] ADR created/updated (if architectural decision)
- [ ] Session log completed

---

## Completion Matrix

**Use this to verify 100% completion before declaring "done"**

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| [Feature/file 1] | âœ…/⏸️/❌ | [commit/test output] |
| [Feature/file 2] | âœ…/⏸️/❌ | [commit/test output] |
| [Feature/file 3] | âœ…/⏸️/❌ | [commit/test output] |

**Legend**:
- âœ… = Complete with evidence
- ⏸️ = In progress
- ❌ = Not started / Blocked

**Definition of COMPLETE**:
- âœ… ALL acceptance criteria checked
- âœ… Evidence provided (test outputs, commits, screenshots)
- âœ… No known issues remaining
- âœ… Cross-validation passed (if multi-agent)

**NOT complete means**:
- âŒ "Works but Test X has issue"
- âŒ "N-1 tests passing"
- âŒ "Core done, extras optional"
- âŒ Any rationalization of incompleteness

---

## Testing Strategy

### Unit Tests
```
[Key test scenarios]
```

### Integration Tests (if applicable)
```
[End-to-end workflows to verify]
```

### Manual Testing Checklist
**Scenario 1**: [Test name]
1. [ ] [Step with expected result]
2. [ ] [Step with expected result]

**Scenario 2**: [Test name]
1. [ ] [Step with expected result]

---

## Success Metrics

### Quantitative
- [Specific measurable outcome]
- [Performance target]
- [Coverage percentage]

### Qualitative
- [User satisfaction criterion]
- [Code quality indicator]

---

## STOP Conditions

**STOP immediately and escalate if**:
- Infrastructure doesn't match assumptions
- Tests fail for any reason (don't rationalize!)
- Performance degrades unacceptably
- Security concerns discovered
- Pattern might already exist elsewhere
- User data at risk
- Completion bias detected (claiming without proof)
- Can't provide verification evidence

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Large / Medium / Small

**Breakdown by Phase**:
- Phase 0: [size]
- Phase 1: [size]
- Phase 2: [size]
- Testing: [size]
- Documentation: [size]

**Complexity Notes**: [Technical challenges, unknowns, or dependencies that affect size]

---

## Dependencies

### Required (Must be complete first)
- [ ] #[issue-number] - [Title]
- [ ] [Service/component] operational

### Optional (Nice to have)
- [ ] [Enhancement that could help]

---

## Related Documentation

- **Architecture**: [Relevant ADRs, patterns]
- **Methodology**: [Which methodology docs apply]
- **Strategic**: [Related planning docs]

---

## Evidence Section

[This section is filled in during/after implementation]

### Implementation Evidence
```bash
[Terminal output showing tests passing]
[Commit hashes with descriptions]
[Performance metrics]
```

### Cross-Validation (if applicable)
**Verified By**: [Agent name]
**Date**: [Date]
**Report**: [Link to verification report]

**Verification Results**:
- âœ…/❌ [Criterion verified]
- âœ…/❌ [Another criterion]

---

## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met âœ…
- [ ] Completion matrix 100% âœ…
- [ ] Evidence provided for each criterion âœ…
- [ ] Tests passing with output âœ…
- [ ] Documentation updated âœ…
- [ ] No regressions confirmed âœ…
- [ ] STOP conditions all clear âœ…
- [ ] Session log complete âœ…
- [ ] Cross-validation complete (if multi-agent) âœ…

**Status**: [In Progress / Ready for Review / Complete]

---

## Notes for Implementation

[PM or architect can add specific guidance here]

---

**Remember**:
- Quality over speed (Time Lord philosophy)
- Evidence required for all claims
- No 80% completions
- PM closes issues after approval

---

_Issue created: [Date]_
_Last updated: [Date]_
