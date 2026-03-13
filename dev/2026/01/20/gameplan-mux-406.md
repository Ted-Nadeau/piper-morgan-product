# Gameplan: #406 MUX-VISION-FEATURE-MAP

**Issue**: #406 MUX-VISION-FEATURE-MAP: Map existing features to object model
**Epic**: MUX-VISION (#401)
**Type**: Documentation
**Created**: 2026-01-20

---

## Overview

Create a comprehensive feature-to-object-model mapping document that shows how each of the 16 features maps (or should map) to Entity/Moment/Place/Lenses/Ownership. This provides the target state reference for grammar transformation work.

---

## Infrastructure Prerequisites

### Phase -1: Infrastructure Verification

| Check | Command | Expected Result |
|-------|---------|-----------------|
| Grammar compliance audit exists | `ls -la docs/internal/architecture/current/grammar-compliance-audit.md` | File exists |
| Ownership metaphors exists | `ls -la docs/internal/architecture/current/ownership-metaphors.md` | File exists |
| MUX implementation guide exists | `ls -la docs/internal/development/mux-implementation-guide.md` | File exists |
| #404 complete | `gh issue view 404 --json state -q '.state'` | CLOSED |
| #405 complete | `gh issue view 405 --json state -q '.state'` | CLOSED |

**If ANY verification fails**: STOP and escalate to PM.

---

## Phase Breakdown

### Phase 0: Setup & Template Creation

**Agent**: Haiku
**Purpose**: Create mapping template and gather feature list

**Tasks**:
- 0.1: Read grammar compliance audit for feature list (16 features)
- 0.2: Read MUX implementation guide for grammar elements
- 0.3: Create per-feature mapping template
- 0.4: Create document structure

**Deliverables**:
- Feature list extracted
- Mapping template ready

**Phase 0.5-0.8**: N/A (documentation work)

---

### Phase 1: Reference Implementation Mapping

**Agent**: Sonnet
**Purpose**: Map Morning Standup (the reference implementation) in full detail

**Tasks**:
- 1.1: Read `services/features/morning_standup.py`
- 1.2: Identify Entity, Moment, Place for Morning Standup
- 1.3: Annotate lenses used
- 1.4: Classify ownership for key objects
- 1.5: Document canonical queries with lens/substrate

**Deliverables**:
- Complete Morning Standup mapping (reference)

---

### Phase 2: Partial/Flattened Feature Mappings

**Agent**: Sonnet
**Purpose**: Map remaining 15 features (6 Partial + 9 Flattened)

**Tasks**:
- 2.1: Map 6 Partial features (Intent, Slack, GitHub, Calendar, Conversation, Onboarding, Personality)
- 2.2: Map 9 Flattened features (Todo, Notion, Auth, List, Project, File, Feedback, MCP)
- 2.3: For each feature:
  - Current state mapping
  - Target state mapping (what it SHOULD look like)
  - Transformation notes
- 2.4: Tag canonical queries per CXO request

**Deliverables**:
- All 16 features mapped
- Current vs target state documented
- Canonical query tagging complete

---

### Phase Z: Integration & Cross-References

**Agent**: Default
**Purpose**: Connect to existing documentation

**Tasks**:
- Z.1: Add cross-references to transformation guide
- Z.2: Add cross-references to grammar compliance audit
- Z.3: Update ADR-055 Developer Resources section
- Z.4: Verify document completeness (16/16 features)
- Z.5: Completion matrix verification

**Deliverables**:
- All cross-references added
- Document complete
- Ready for MUX-GATE-3

---

## Completion Matrix

| # | Deliverable | Phase | Acceptance Criteria |
|---|-------------|-------|---------------------|
| 1 | Feature mapping document | 1-2 | File exists at specified path |
| 2 | Per-feature template | 0 | Template used for all features |
| 3 | Entity/Moment/Place IDs | 1-2 | All 16 features have mapping |
| 4 | Lens annotations | 1-2 | Lenses listed per feature |
| 5 | Ownership classification | 1-2 | N/F/S assigned per feature |
| 6 | Canonical query tagging | 1-2 | Queries tagged with lens/substrate |

**Target**: 6/6 = 100%

---

## Agent Strategy

**Approach**: Sequential multi-phase

**Rationale**:
- Phase 1 (Morning Standup) establishes pattern
- Phase 2 applies pattern to remaining features
- Large documentation scope benefits from dedicated phases

**Agent Assignments**:
| Phase | Agent | Reasoning |
|-------|-------|-----------|
| 0 | Haiku | Template creation |
| 1 | Sonnet | Detailed reference mapping |
| 2 | Sonnet | Bulk feature mapping |
| Z | Default | Integration |

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Feature code unclear | Reference grammar compliance audit analysis |
| Too many features | Focus on mapping structure, not deep analysis |
| Overlap with #404 | Distinct purpose: #404 = compliance, #406 = mapping |
| Document too long | Use consistent template for scanability |

---

## Related Documentation

- Grammar Compliance Audit: `docs/internal/architecture/current/grammar-compliance-audit.md`
- MUX Implementation Guide: `docs/internal/development/mux-implementation-guide.md`
- Ownership Metaphors: `docs/internal/architecture/current/ownership-metaphors.md`
- Grammar Transformation Guide: `docs/internal/development/grammar-transformation-guide.md`
- CXO Memo: `mailboxes/ppm/read/memo-ppm-ca-mux-v1-design-context-2026-01-19.md`

---

## Notes

This document serves as the target state reference for:
- Developers transforming features (#619-627)
- MUX-GATE-3 completion evidence
- Future feature implementation guidance

---

*Gameplan Version: 1.0*
*Created: 2026-01-20*
*Template: Gameplan Template v9.3*
