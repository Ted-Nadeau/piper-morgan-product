# Bug #[N] Investigation Report

**Bug Title**: [From GitHub issue]
**GitHub Issue**: #[issue-number]
**Investigator**: [Agent name]
**Date**: YYYY-MM-DD
**Investigation Duration**: [Time spent]

---

## Root Cause Hypothesis

[Single clear statement of what you believe is causing the bug]

**Confidence Level**: [High/Medium/Low]

---

## Evidence

### Code References

- `path/to/file.py:line-number` - [What this shows]
- `path/to/file.py:line-number` - [What this shows]

### Logs/Errors

```
[Paste relevant log entries or error messages]
```

### Test Results

- [Test name]: [Pass/Fail] - [What this indicates]
- [Test name]: [Pass/Fail] - [What this indicates]

### Reproduction Steps Verified

- [ ] Can reproduce consistently
- [ ] Reproduction steps match issue description
- [ ] Additional reproduction paths discovered: [List any]

---

## Domain Impact

**Domain Model Check**:

- Checked `services/domain/models.py`: [What domain rules apply]
- Domain Invariant Violation: [Yes/No] - [If yes, explain]

**Business Rule Impact**:

- [Does this bug violate any business rules?]

**Domain Model Compliance**:

- [ ] Bug fix can respect existing domain model
- [ ] Bug fix requires domain model change (explain why)
- [ ] Domain model unclear (what needs clarification)

---

## Pattern Analysis

### Working Examples Found

- `path/to/working-example.py` - [How this is similar/different]
- Pattern: [Pattern name] - [How it's used correctly elsewhere]

### Reference Implementations

- ADR: [ADR number] - [Relevant architectural decision]
- Pattern: [Pattern name] - [How it should be implemented]

### Differences Identified

- [What's different between working and broken code]
- [Why the difference causes the bug]

### Dependencies

- **Upstream**: [Components that feed into this]
- **Downstream**: [Components that depend on this]
- **Integration Points**: [Where this crosses boundaries]

---

## Integration Points

**Boundaries Crossed**:

- [Component A] → [Component B] - [What happens at this boundary]
- [Layer X] → [Layer Y] - [What happens at this layer transition]

**Integration Failure Analysis**:

- [Does this work in isolation but fail at integration?]
- [What breaks at the integration point?]

---

## Recommendation

**Fix Strategy**:

- [ ] **Isolated Fix Sufficient** - Single bug, no systemic impact
  - Reasoning: [Why isolated fix is appropriate]
- [ ] **Requires Refactoring** - Multiple bugs indicate design issue
  - Reasoning: [Why refactoring is needed]
  - Scope: [What needs refactoring]
- [ ] **Requires Domain Model Change** - Bugs reveal domain understanding gap
  - Reasoning: [Why domain model change is needed]
  - Impact: [What domain concepts need updating]
- [ ] **Requires Architectural Change** - Bugs indicate pattern failure
  - Reasoning: [Why architectural change is needed]
  - ADR Required: [Yes/No] - [If yes, what decision needs documenting]
- [ ] **Needs More Investigation** - Missing information
  - What's Missing: [What information is needed]
  - Next Steps: [How to gather missing information]

**Estimated Fix Complexity**: [Low/Medium/High]

**Risk Assessment**:

- [What could break if we fix this?]
- [What tests need to be added/updated?]
- [What documentation needs updating?]

---

## Related Bugs

**Similar Bugs**:

- Bug #[N] - [How it's related]
- Bug #[N] - [How it's related]

**Pattern Group**: [If this bug is part of a pattern group]

---

## Additional Notes

[Any other observations, questions, or concerns]
