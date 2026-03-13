# Anti-Pattern Index: Design Document

**Date**: 2026-01-21
**Author**: Docs Management Agent (Haiku)
**Status**: Draft - Awaiting PM Audit

---

## Purpose

Create a periodically-updated index that cross-references anti-patterns found throughout the documentation without duplicating the pattern/anti-pattern details themselves. The index serves as a navigation aid, connecting dots bidirectionally between:
- Where anti-patterns are documented
- What recommended patterns address them
- Which categories of anti-patterns exist

---

## Design Principles

1. **Index, Don't Duplicate**: Link to source documents; don't copy content
2. **Bidirectional Navigation**: From anti-pattern → pattern AND pattern → anti-pattern
3. **Categorization**: Group anti-patterns by domain (Testing, Grammar, Architecture, Process)
4. **Periodic Updates**: Design for easy re-scanning; include "Last Scanned" date
5. **Lightweight**: Keep the index itself scannable (~200-400 lines max)

---

## Proposed Structure

```markdown
# Anti-Pattern Index

**Last Scan**: [DATE]
**Documents Scanned**: [COUNT] patterns, [COUNT] ADRs, [COUNT] design docs

## Quick Reference by Category

| Category | Anti-Patterns | Key Patterns |
|----------|---------------|--------------|
| Grammar/Consciousness | 7 | Pattern-050–054, consciousness-philosophy.md |
| Testing | 3 | Pattern-045, Pattern-049 |
| Architecture | 5 | ADR-006, ADR-010, Pattern-003 |
| Process/Methodology | 4 | Pattern-046, Pattern-047 |

---

## Anti-Pattern Catalog

### Grammar & Consciousness Anti-Patterns

| ID | Anti-Pattern | Source Location | Recommended Pattern |
|----|--------------|-----------------|---------------------|
| G-01 | Query language in responses | grammar-transformation-guide.md:318 | Pattern-052 (Personality Bridge) |
| G-02 | Timestamps without context | grammar-transformation-guide.md:330 | Pattern-053 (Warmth Calibration) |
| ... | ... | ... | ... |

### Testing Anti-Patterns

| ID | Anti-Pattern | Source Location | Recommended Pattern |
|----|--------------|-----------------|---------------------|
| T-01 | Mocked dependencies hiding integration issues | pattern-045:19-25 | Pattern-045 (Green Tests, Red User) |
| ... | ... | ... | ... |

### Architecture Anti-Patterns

| ID | Anti-Pattern | Source Location | Recommended Pattern |
|----|--------------|-----------------|---------------------|
| A-01 | Dual repository implementations | adr-005 | ADR-005 decision |
| ... | ... | ... | ... |

### Process Anti-Patterns

| ID | Anti-Pattern | Source Location | Recommended Pattern |
|----|--------------|-----------------|---------------------|
| P-01 | Premature closure (75% complete) | pattern-046 | Pattern-046 (Beads Discipline) |
| P-02 | Proceeding with uncertainty | pattern-047 | Pattern-047 (Time Lord Alert) |
| ... | ... | ... | ... |

---

## Reverse Index: Pattern → Anti-Patterns Addressed

| Pattern | Anti-Patterns Addressed |
|---------|------------------------|
| Pattern-045 | T-01, T-02, T-03 |
| Pattern-050 | G-03 |
| Pattern-052 | G-01, G-05 |
| ... | ... |

---

## Scan Methodology

Documents scanned in this pass:
- [ ] All pattern-*.md files (57 patterns)
- [ ] All adr-*.md files (55 ADRs)
- [ ] MUX design docs (5 files)
- [ ] Methodology docs (key files)
- [ ] Transformation guides

Keywords searched: `anti-pattern`, `Anti-Pattern`, `don't`, `avoid`, `❌`, `Bad:`, `Flattened`
```

---

## File Location

**Proposed**: `docs/internal/architecture/current/anti-pattern-index.md`

**Rationale**:
- Lives alongside patterns (which it indexes)
- Architecture section is appropriate for cross-cutting reference
- `current/` indicates it's actively maintained

---

## Scan Scope for Pilot

**Primary targets** (high anti-pattern density):
1. `docs/internal/architecture/current/patterns/` - 57 patterns
2. `docs/internal/architecture/current/adrs/` - 55 ADRs
3. `docs/internal/architecture/current/consciousness-philosophy.md`
4. `docs/internal/architecture/current/ownership-metaphors.md`
5. `docs/internal/development/grammar-transformation-guide.md`
6. `docs/internal/development/grammar-onboarding-checklist.md`

**Excluded from pilot** (lower priority, can add later):
- Omnibus logs (historical)
- Session logs (transient)
- Knowledge/ symlinks (duplicate of docs/)
- Trash/ (deprecated)

---

## ID Scheme

Category prefixes:
- **G-##**: Grammar/Consciousness anti-patterns
- **T-##**: Testing anti-patterns
- **A-##**: Architecture anti-patterns
- **P-##**: Process/Methodology anti-patterns
- **I-##**: Integration anti-patterns

IDs are stable across scans (assigned once, not renumbered).

---

## Update Workflow

**Trigger**: Part of weekly docs audit (FLY-AUDIT) OR on-demand after major documentation sprints

**Process**:
1. Run scan against target directories
2. Compare to existing index
3. Add new anti-patterns with IDs
4. Update "Last Scan" date
5. Mark any patterns that have been removed/superseded

---

## Questions for PM

1. **File location**: Is `docs/internal/architecture/current/anti-pattern-index.md` appropriate?
2. **Category scheme**: G/T/A/P/I - are these the right categories?
3. **Scope**: Should the pilot include any other documents?
4. **Weekly audit integration**: Add to FLY-AUDIT checklist?
5. **Line number references**: Include line numbers (e.g., `:318`) or just file names?

---

## Implementation Plan

1. **Phase 1**: Scan grammar-transformation-guide.md and consciousness-philosophy.md (highest density)
2. **Phase 2**: Scan all 57 patterns
3. **Phase 3**: Scan all 55 ADRs
4. **Phase 4**: Scan remaining MUX docs
5. **Phase 5**: Create index document

Estimated pilot time: ~1-2 hours

---

## Success Criteria

- [ ] Index created at agreed location
- [ ] All anti-patterns from pilot scope captured
- [ ] Bidirectional navigation working (anti-pattern → pattern, pattern → anti-patterns)
- [ ] Categories feel natural and complete
- [ ] Index is scannable (<400 lines)
- [ ] Update workflow documented

---

*Design complete. Awaiting PM audit before implementation.*
