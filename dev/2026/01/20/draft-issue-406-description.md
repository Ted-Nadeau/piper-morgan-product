# Draft Issue Description: #406 MUX-VISION-FEATURE-MAP

**To**: PM for Review
**From**: Lead Developer (Claude Code Opus)
**Date**: 2026-01-20
**Re**: Issue #406 Description Draft

---

## Research Summary

### What Already Exists

**Grammar Compliance Audit (#404)**:
- Audited 16 features for grammar compliance
- Distribution: 1 Conscious, 6 Partial, 9 Flattened
- Created transformation priority list

**Related Documentation**:
- Grammar Application Patterns (pattern-050 through 054)
- Grammar Transformation Guide
- MUX Implementation Guide
- Ownership Metaphors document (#405)

**Gap Analysis**:
- Audit tells us compliance LEVEL but not HOW to map
- No document shows the STRUCTURE of each feature's mapping
- MUX-GATE-3 requires "Existing features mapped to object model"
- Need reference for developers implementing grammar transformations

---

## Proposed Issue Description

### Title (Existing)
MUX-VISION-FEATURE-MAP: Map existing features to object model

### Description

**Context**

The grammar compliance audit (#404) assessed 16 features for Entity/Moment/Place/Lenses/Situation compliance. Now we need a formal mapping document that shows HOW each feature maps (or should map) to the object model - not just whether it passes, but what the mapping actually looks like.

**Problem**

1. **Transformation guidance is abstract**: The transformation guide explains HOW to transform but not WHAT each feature's transformation should look like
2. **Reference missing**: Developers transforming features (#619-627) need target state examples
3. **Gate requirement**: MUX-GATE-3 requires "Existing features mapped to object model"
4. **Discovery support**: CXO memo requests "explicit lens/substrate tagging for existing canonical queries"

**Deliverables**

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Feature mapping document | `feature-object-model-map.md` with all 16 features |
| 2 | Per-feature mapping template | Reusable format for each feature |
| 3 | Entity/Moment/Place identification | What is the Entity, Moment, Place for each feature |
| 4 | Lens annotations | Which lenses apply to each feature |
| 5 | Ownership classification | Native/Federated/Synthetic for key objects |
| 6 | Canonical query tagging | Per CXO request: lens/substrate for each query |

**Acceptance Criteria**

- [ ] Feature mapping document at `docs/internal/architecture/current/feature-object-model-map.md`
- [ ] All 16 features from grammar compliance audit mapped
- [ ] Each feature has: Entity, Moment, Place, Lenses, Ownership identification
- [ ] Canonical queries tagged with lens/substrate (per CXO request)
- [ ] Cross-reference to transformation guide for partial/flattened features
- [ ] Passes self-check: Developer can use map to understand target state

**Dependencies**

- **Requires (Complete)**:
  - #404 MUX-VISION-GRAMMAR-CORE (compliance audit exists)
  - #405 MUX-VISION-METAPHORS (ownership metaphors documented)
- **Required By**:
  - MUX-GATE-3 ("Existing features mapped to object model")
  - #619-627 Grammar transformation issues (need target state reference)

**Related Issues**

- #399 MUX-VISION-OBJECT-MODEL (grammar foundation - complete)
- #400 MUX-VISION-CONSCIOUSNESS (philosophy - complete)
- #404 MUX-VISION-GRAMMAR-CORE (compliance audit - complete)
- #405 MUX-VISION-METAPHORS (ownership metaphors - complete)
- #401 MUX-VISION Epic
- #531 MUX-GATE-1

**Scope Boundaries**

- **In Scope**: Mapping document showing target state for each feature
- **NOT in Scope**: Actually transforming features (separate issues #619-627)
- **NOT in Scope**: Code changes (this is documentation)

---

## Key Content for Mapping Document

Per feature, the mapping should include:

```markdown
## Feature: [Name]

**Compliance**: [Conscious/Partial/Flattened]
**Priority**: [Reference/High/Medium/Low]

### Object Model Mapping

| Element | Current | Target |
|---------|---------|--------|
| Entity | [who/what] | [who/what] |
| Moment | [what occurrence] | [what occurrence] |
| Place | [where/context] | [where/context] |
| Lenses | [which apply] | [which should apply] |
| Ownership | [Native/Federated/Synthetic] | [expected] |

### Canonical Queries (per CXO request)

| Query | Substrate | Lenses | Ownership |
|-------|-----------|--------|-----------|
| [example query] | Entity/Moment/Place | [which] | [category] |

### Transformation Notes
- [what needs to change for grammar compliance]
- [reference to transformation guide section]
```

---

## Audit Notes (For Next Step)

This description:
1. Builds on #404 audit (compliance assessed)
2. Addresses CXO request (canonical query tagging)
3. Supports MUX-GATE-3 requirement
4. Provides reference for #619-627 transformations
5. Documentation only (no code changes)

---

*Draft created: 2026-01-20*
*Ready for PM review*
