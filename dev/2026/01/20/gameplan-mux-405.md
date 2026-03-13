# Gameplan: #405 MUX-VISION-METAPHORS

**Issue**: #405 MUX-VISION-METAPHORS: Formalize ownership metaphors (Mind/Senses/Understanding)
**Epic**: MUX-VISION (#401)
**Type**: Documentation/Formalization
**Created**: 2026-01-20

---

## Overview

Formalize the philosophical foundation behind the ownership metaphors (Mind/Senses/Understanding) that are already implemented in code. This enables developers to understand WHY we chose these metaphors and HOW to use them correctly.

---

## Infrastructure Prerequisites

### Phase -1: Infrastructure Verification

| Check | Command | Expected Result |
|-------|---------|-----------------|
| Ownership code exists | `ls -la services/mux/ownership.py` | File exists |
| Ownership tests exist | `ls -la tests/unit/services/mux/test_ownership.py` | File exists |
| ADR-045 exists | `ls -la docs/internal/architecture/current/adrs/adr-045-*.md` | File exists |
| Experience tests exist | `ls -la docs/internal/development/mux-experience-tests.md` | File exists |
| #399 complete | `gh issue view 399` | State: CLOSED |
| #400 complete | `gh issue view 400` | State: CLOSED |
| #404 complete | `gh issue view 404` | State: CLOSED |

**If ANY verification fails**: STOP and escalate to PM.

---

## Phase Breakdown

### Phase 0: Setup & Context Gathering

**Agent**: Haiku
**Purpose**: Gather source material for philosophy document

**Tasks**:
- 0.1: Read ownership implementation (`services/mux/ownership.py`)
- 0.2: Read ownership tests for examples (`tests/unit/services/mux/test_ownership.py`)
- 0.3: Read ADR-045 ownership section (lines 29-35)
- 0.4: Read CXO sketches if available (mind/senses/understanding origin)
- 0.5: Document source materials found

**Deliverables**:
- Source material summary for Phase 1-2

**Phase 0.5-0.8**: N/A (documentation work, no new code/UI)

---

### Phase 1: Philosophy Document Core

**Agent**: Sonnet
**Purpose**: Create the philosophical foundation

**Tasks**:
- 1.1: Create `docs/internal/architecture/current/ownership-metaphors.md`
- 1.2: Write "Why These Metaphors" section explaining Mind/Senses/Understanding choice
- 1.3: Write "The Three Relationships" section with deep explanations
- 1.4: Connect metaphors to consciousness philosophy (#400)

**Deliverables**:
- Philosophy document Part 1 (Sections 1-3)

---

### Phase 2: Decision Guide & Examples

**Agent**: Sonnet
**Purpose**: Make the philosophy actionable

**Tasks**:
- 2.1: Create decision tree for ownership classification
- 2.2: Write 3+ worked examples with reasoning:
  - Example 1: Session (Native/Mind) - why and how
  - Example 2: GitHub Issue (Federated/Senses) - why and how
  - Example 3: Inferred Risk (Synthetic/Understanding) - why and how
- 2.3: Add "Common Mistakes" section
- 2.4: Add "Edge Cases" section

**Deliverables**:
- Philosophy document Part 2 (Sections 4-6)
- Decision tree diagram (ASCII or Mermaid)
- 3+ worked examples

---

### Phase Z: Integration & Cross-References

**Agent**: Default
**Purpose**: Connect to existing documentation

**Tasks**:
- Z.1: Update ADR-045 with reference to ownership-metaphors.md
- Z.2: Update ADR-055 with reference to ownership-metaphors.md
- Z.3: Update mux-experience-tests.md with metaphor-specific test criteria
- Z.4: Update grammar-onboarding-checklist.md with metaphor reading
- Z.5: Verify all cross-references work
- Z.6: Completion matrix verification

**Deliverables**:
- ADR-045 updated
- ADR-055 updated
- Experience tests updated
- Onboarding checklist updated
- Completion matrix 5/5

---

## Completion Matrix

| # | Deliverable | Phase | Acceptance Criteria |
|---|-------------|-------|---------------------|
| 1 | Ownership metaphor philosophy doc | 1-2 | File exists at specified path |
| 2 | WHY explanation | 1 | Section explains Mind/Senses/Understanding choice |
| 3 | Decision tree | 2 | Tree helps classify new entities |
| 4 | Worked examples (3+) | 2 | At least 3 examples with reasoning |
| 5 | ADR cross-references | Z | ADR-045, ADR-055 reference new doc |
| 6 | Experience tests update | Z | Metaphor criteria added |

**Target**: 6/6 = 100%

---

## Agent Strategy

**Approach**: Sequential single-agent (like #400)

**Rationale**:
- Documentation-heavy work
- Sequential dependencies (philosophy → examples → integration)
- Small scope (one document + cross-references)
- Similar to #400 pattern that worked well

**Agent Assignments**:
| Phase | Agent | Reasoning |
|-------|-------|-----------|
| 0 | Haiku | Gathering/reading work |
| 1-2 | Sonnet | Philosophy and example creation |
| Z | Default | Integration updates |

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Philosophy too abstract | Ground in code examples from ownership.py |
| Overlap with #400 | Clear scope boundaries, no consciousness discussion |
| Decision tree too complex | Keep to 3-5 questions max |
| Examples not representative | Use canonical examples from ADR-045 |

---

## Related Documentation

- ADR-045: Object Model Vision
- ADR-055: Object Model Implementation
- `services/mux/ownership.py`: Implementation reference
- `consciousness-philosophy.md`: Companion philosophy document (#400)
- `grammar-transformation-guide.md`: HOW to transform features (#404)

---

## Notes

This issue is the "ownership-specific" companion to #400 (consciousness philosophy). While #400 covers the Five Pillars broadly, #405 goes deep on the Mind/Senses/Understanding metaphor specifically.

---

*Gameplan Version: 1.0*
*Created: 2026-01-20*
*Template: Gameplan Template v9.3*
