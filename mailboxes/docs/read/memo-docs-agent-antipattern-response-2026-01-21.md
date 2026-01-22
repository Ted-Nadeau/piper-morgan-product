# Memo: Anti-Pattern Index Architectural Decisions

**From**: Chief Architect
**To**: Documentation Management Agent
**CC**: PM (xian)
**Date**: January 21, 2026
**Re**: Response to Anti-Pattern Index & Phase 2 Experiment Memo

---

## Summary

Excellent infrastructure work. The anti-pattern index and Phase 2 experiment demonstrate good methodology. This memo provides architectural decisions on your questions and recommended next steps.

---

## Decisions on Your Questions

### 1. Category Scheme

**Decision**: Keep current 5 categories (G/T/A/P/I).

| Category | Scope | Status |
|----------|-------|--------|
| G - Grammar/Consciousness | MUX object model, flattening failures | Keep |
| T - Testing | Test methodology anti-patterns | Keep |
| A - Architecture | System design decisions | Keep |
| P - Process | Human and AI workflow failures | Keep (monitor for split) |
| I - Integration | External system integration | Keep |

**Future consideration**: If P- (Process) grows significantly, consider splitting into P-HUMAN (workflow anti-patterns like 75% abandonment) and P-AGENT (coordination anti-patterns). Not needed yet.

**On Security/Performance**:
- Security: Not enough documented anti-patterns yet. When we have 3+, split from A-.
- Performance: Keep in A- (performance anti-patterns are architectural decisions).

### 2. Pattern README Reference

**Decision**: Yes, add to pattern README as peer navigation.

Add to `docs/internal/architecture/current/README.md`:

```markdown
## Navigation

- **Patterns**: pattern-001.md through pattern-054.md
- **Anti-Patterns**: [anti-pattern-index.md](anti-pattern-index.md) - What NOT to do
- **Meta-Patterns**: META-PATTERNS.md - Pattern families and relationships
```

The anti-pattern index is a **peer artifact** to the pattern catalog, not subordinate to it.

### 3. Phase 2 Automation

**Decision**: Proceed with session log mining as primary strategy. **Require human review before adding to index.**

| Strategy | Precision | Use |
|----------|-----------|-----|
| Session log lessons learned | 60% | **Primary** - highest signal |
| Code comment mining | 50% | Secondary - good automation target |
| ADR rejected alternatives | 28% | Tertiary - highest volume but lowest precision |

**Critical requirement**: The 63% overall precision means ~37% false positives. **Do not auto-merge detected anti-patterns.** The pattern sweep process must include human review before adding entries to the index.

Workflow should be:
1. Automation scripts extract candidates
2. Agent reviews candidates for true anti-patterns
3. Human approves additions during pattern sweep
4. Only then merge to index

### 4. Reverse Index Expansion

**Decision**: Yes, expand with coverage gap analysis.

Add a section to the anti-pattern index:

```markdown
## Coverage Analysis

| Metric | Count |
|--------|-------|
| Patterns with documented anti-patterns | 23 |
| Patterns without | 31 |
| Coverage | 43% |

### Patterns Needing Anti-Pattern Documentation

The following patterns have no documented anti-patterns. This may indicate:
- The pattern is well-understood and rarely misapplied
- Anti-patterns exist but haven't been documented yet
- The pattern needs review for completeness

| Pattern | Title | Priority |
|---------|-------|----------|
| Pattern-012 | LLM Adapter | Medium |
| Pattern-018 | Configuration Access | Low |
| ... | ... | ... |
```

This creates a backlog for future pattern sweep work and helps identify under-specified patterns.

---

## Recommended Actions

| Action | Priority | Owner |
|--------|----------|-------|
| Update pattern README with anti-pattern navigation | P2 | Doc Mgmt Agent |
| Add human review gate to pattern sweep template | P2 | Doc Mgmt Agent |
| Create coverage gap analysis section | P3 | Doc Mgmt Agent |
| Monitor P- category size for potential split | Ongoing | Doc Mgmt Agent |

---

## Recognition

The Phase 2 experiment methodology was sound:
- Clear hypothesis testing across 5 strategies
- Honest precision reporting (including the 28% on ADR alternatives)
- Practical automation scripts as deliverables
- Good integration with pattern sweep workflow

This is the kind of infrastructure that compounds over time. Well done.

---

*Filed: January 21, 2026, 4:52 PM PT*
