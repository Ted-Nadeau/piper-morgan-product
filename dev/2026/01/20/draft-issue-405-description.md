# Draft Issue Description: #405 MUX-VISION-METAPHORS

**To**: PM for Review
**From**: Lead Developer (Claude Code Opus)
**Date**: 2026-01-20
**Re**: Issue #405 Description Draft

---

## Research Summary

### What Already Exists

**Code Implementation (Complete - from #399 P2)**:
- `services/mux/ownership.py` - Full ownership model with Mind/Senses/Understanding
- 25 ownership tests in `tests/unit/services/mux/test_ownership.py`
- `OwnershipCategory` enum: NATIVE, FEDERATED, SYNTHETIC
- `OwnershipResolver` class with confidence tracking

**Documentation References (Scattered)**:
- ADR-045: Brief table mapping categories to metaphors (3 lines)
- ADR-055: References ownership model
- Implementation Guide: Import examples, brief descriptions
- Experience Tests: Test criteria mentioning metaphors
- Onboarding Checklist: One checkbox about 3 categories

**Gap Analysis**:
- No dedicated metaphor documentation explaining WHY these metaphors
- No developer guide for choosing between categories
- No examples showing metaphors in action
- No decision tree for ownership classification
- Tech Phase 3 spec lists VISION-METAPHORS as dependency but spec doesn't exist

---

## Proposed Issue Description

### Title (Existing)
MUX-VISION-METAPHORS: Formalize ownership metaphors (Mind/Senses/Understanding)

### Description

**Context**

The ownership model code exists (from #399 P2) but the philosophical framing behind the metaphors is undocumented. Developers can USE the ownership system but don't understand WHY we chose Mind/Senses/Understanding or HOW to think about information through this lens.

**Problem**

1. **Metaphor meaning is tribal knowledge**: Why "Mind" and not "Memory"? Why "Senses" and not "Inputs"?
2. **Decision guidance missing**: When should a developer classify something as Synthetic vs Federated?
3. **Philosophy disconnected from code**: ADR-045 has a table but no narrative
4. **TECH-PHASE3-OWNERSHIP blocked**: Tech spec lists VISION-METAPHORS as dependency

**Deliverables**

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Ownership metaphor philosophy doc | Why Mind/Senses/Understanding (not Memory/Inputs/Inference) |
| 2 | Decision guide | When to use each category with examples |
| 3 | Worked examples | 3+ examples showing classification reasoning |
| 4 | ADR-045/055 updates | Cross-reference new documentation |
| 5 | Experience tests update | Add metaphor-specific test criteria |

**Acceptance Criteria**

- [ ] Philosophy document at `docs/internal/architecture/current/ownership-metaphors.md`
- [ ] Document explains WHY these specific metaphors (Mind/Senses/Understanding)
- [ ] Decision tree for ownership classification
- [ ] At least 3 worked examples with reasoning
- [ ] Cross-references added to ADR-045, ADR-055
- [ ] Experience tests updated with metaphor criteria
- [ ] Passes self-check: Developer can read doc and correctly classify new entity

**Dependencies**

- **Requires (Complete)**: #399 MUX-VISION-OBJECT-MODEL (ownership code exists)
- **Required By**: TECH-PHASE3-OWNERSHIP (tech spec lists this as dependency)

**Related Issues**

- #399 MUX-VISION-OBJECT-MODEL (implementation - complete)
- #400 MUX-VISION-CONSCIOUSNESS (philosophy - complete)
- #404 MUX-VISION-GRAMMAR-CORE (grammar application - complete)
- #401 MUX-VISION Epic

**Scope Boundaries**

- **In Scope**: Philosophy and decision guidance for ownership metaphors
- **NOT in Scope**: Code changes (ownership code already complete)
- **NOT in Scope**: Test changes beyond documentation references

---

## Audit Notes (For Next Step)

This description:
1. Identifies clear gap (philosophy vs code)
2. Lists concrete deliverables
3. Has measurable acceptance criteria
4. Links to existing infrastructure
5. Scopes appropriately (documentation, not code)

**Similar to #400**: Both are philosophy/documentation issues that formalize concepts already in code.

---

*Draft created: 2026-01-20*
*Ready for PM review*
