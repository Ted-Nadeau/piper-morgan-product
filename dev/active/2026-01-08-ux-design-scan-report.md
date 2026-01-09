# UX/Design Files Comprehensive Scan Report

**Date**: 2026-01-08
**Prepared by**: Documentation Manager (Haiku)
**Purpose**: Exhaustive inventory of UX/design documents for consolidation

---

## Summary

Found **50+ UX/design-related files** across the project tree. The bulk of the work happened in two periods:
1. **Nov 13-17, 2025**: Major UX Audit (15+ files)
2. **Nov 26 - Dec 1, 2025**: MUX (Modeled UX) 2.0 work (12+ files)

---

## Category 1: UX Audit Files (Nov 2025)

These form a comprehensive UX audit. **Likely candidates for docs/internal/design/audits/**

| File | Location | Content |
|------|----------|---------|
| ux-audit-phase1-interaction-patterns.md | dev/2025/11/13/ | Interaction pattern inventory |
| ux-audit-phase1-touchpoint-inventory.md | dev/2025/11/13/ | User touchpoint mapping |
| ux-audit-phase1-visual-design-tokens.md | dev/2025/11/13/ | Design token documentation |
| ux-audit-phase1-technical-constraints.md | dev/2025/11/14/ | Technical constraint analysis |
| ux-audit-phase2-journey-mapping.md | dev/2025/11/14/ | User journey maps |
| ux-audit-phase3-design-system-implementation.md | dev/2025/11/14/ | Design system spec |
| ux-audit-phase4-gap-analysis.md | dev/2025/11/14/ | Gap analysis |
| ux-audit-phase4-addendum-document-management.md | dev/2025/11/14/ | Document management UX |
| ux-audit-phase5-strategic-recommendations.md | dev/2025/11/14/ | Strategic recommendations |
| ux-audit-comprehensive-report.md | dev/2025/11/14/ | **Master audit report** |
| ux-audit-roadmap-synthesis.md | dev/2025/11/14/ | Roadmap synthesis |
| ux-synthesis-phase3-decisions.md | dev/2025/11/13/ | Phase 3 decisions |
| phase-3-suggestions-ux-design-proposal.md | dev/2025/11/13/ | Design proposals |
| ux-deployment-package.md | dev/2025/11/13/ | Deployment artifacts |
| holistic-ux-investigation-brief.md | dev/2025/11/13/ | Investigation brief |

---

## Category 2: MUX (Modeled UX) 2.0 Files

Core MUX strategic and vision documents. **High priority for consolidation.**

| File | Location | Content |
|------|----------|---------|
| MUX-VISION-LEARNING-UX-updated.md | dev/2025/11/29/ | MUX vision for learning UX |
| MUX-VISION-LEARNING-UX-updated.md | dev/2025/12/01/ | (duplicate/update?) |
| issue-MUX-VISION-LEARNING-UX.md | dev/2025/11/29/ | Issue spec |
| issue-MUX-VISION-LEARNING-UX.md | dev/2025/12/01/ | (duplicate/update?) |
| issue-MUX-TECH-PHASE1-GRAMMAR.md | dev/2025/11/29/ | Tech phase 1: Grammar |
| issue-MUX-TECH-PHASE2-ENTITY.md | dev/2025/11/29/ | Tech phase 2: Entity |
| issue-MUX-TECH-PHASE3-OWNERSHIP.md | dev/2025/11/29/ | Tech phase 3: Ownership |
| issue-MUX-TECH-PHASE4-COMPOSTING.md | dev/2025/11/29/ | Tech phase 4: Composting |
| issue-generation-strategy-ux-20.md | dev/2025/11/29/ | UX 2.0 issue generation |
| issue-generation-strategy-ux-20.md | dev/2025/12/01/ | (duplicate?) |
| alpha-setup-and-mux-gate-issues.md | dev/2025/12/28/ | MUX gate issues |

---

## Category 3: UX Strategy Documents

Strategic synthesis and direction documents.

| File | Location | Content |
|------|----------|---------|
| piper-morgan-ux-foundations-and-open-questions.md | dev/2025/11/29/ | UX foundations |
| piper-morgan-ux-strategy-synthesis.md | dev/2025/11/29/ | Strategy synthesis |
| 2025-11-26-ux-strategy-synthesis.md | dev/2025/11/26/ | Earlier synthesis |
| ux-strategic-brief-chief-architect-chief-of-staff.md | dev/2025/11/17/ | Executive brief |

---

## Category 4: INTERACT Files

Interaction-specific design work.

| File | Location | Content |
|------|----------|---------|
| issue-INTERACT-RECOGNITION.md | dev/2025/11/29/ | Recognition interaction |
| issue-INTERACT-RECOGNITION.md | dev/2025/12/01/ | (duplicate?) |

---

## Category 5: Active UX Specs (dev/active/)

**Already identified for move to docs/internal/design/specs/**

| File | Domain |
|------|--------|
| cross-session-greeting-ux-spec-v1.md | Greetings |
| contextual-hint-ux-spec-v1.md | Hints/suggestions |
| multi-entry-ftux-exploration-v1.md | Onboarding |
| empty-state-voice-guide-v1.md | Empty states |
| b1-quality-rubric-v1.md | Quality measurement |
| conversational-glue-design-brief.md | Conversation design |
| cxo-brief-discovery-ux-strategy.md | Discovery UX |
| canonical-queries-v2.md | Query patterns (UX doc) |

---

## Category 6: Already in docs/

| File | Location |
|------|----------|
| vision.md | docs/internal/planning/current/ |
| ux-piper-105-phase0-gameplan.md | docs/internal/development/planning/plans/ |

---

## Category 7: Voice/Tone Guides

| File | Location |
|------|----------|
| xian-voice-tone-guide.md | docs/assets/images/blog/comms/ |
| 2025-06-30-voice-guide-session-log.md | archive/session-logs/2025/06/ |

---

## Category 8: Historical/Archive

Already in archive - no action needed.

| File | Location |
|------|----------|
| ux-quick-win-test-report-2025-08-11.md | archive/artifacts/ |
| ux-quick-win-handoff-2025-08-11.md | archive/docs-handoffs-2025/legacy-prompts/ |
| 2025-08-01-00-UX-web-designer-sonnet-log.md | archive/session-logs/2025/08/ |

---

## PM Decision Points

### 1. UX Audit Collection (15 files)
- **Option A**: Move to `docs/internal/design/audits/2025-11-ux-audit/`
- **Option B**: Keep in dev/2025/11/ as historical working docs
- **Option C**: Extract key findings to a summary doc, archive the rest

### 2. MUX Files (12 files)
- **Option A**: Create `docs/internal/design/mux/` as dedicated MUX home
- **Option B**: Integrate into general design specs
- **Concern**: Some are "issue-" files (working docs for GitHub issues)

### 3. Duplicates Detected
Several files appear in both Nov 29 and Dec 1:
- MUX-VISION-LEARNING-UX-updated.md
- issue-MUX-VISION-LEARNING-UX.md
- issue-generation-strategy-ux-20.md
- issue-INTERACT-RECOGNITION.md

**Need to determine**: Which is canonical? Should duplicates be cleaned up?

### 4. UX Strategy Documents
Should these be in:
- `docs/internal/design/strategy/`?
- Merged into the Design System README?
- Kept as reference in dev/ tree?

### 5. Voice/Tone Guide Location
Currently in `docs/assets/images/blog/comms/` (odd location). Should move to:
- `docs/internal/design/voice/`?
- `knowledge/`?

---

## Recommended Directory Structure

```
docs/internal/design/
├── README.md                    # Front door (proposed)
├── specs/                       # Individual UX specs
│   ├── cross-session-greeting-ux-spec-v1.md
│   ├── contextual-hint-ux-spec-v1.md
│   ├── empty-state-voice-guide-v1.md
│   └── ...
├── briefs/                      # Design briefs
│   ├── conversational-glue.md
│   └── discovery-ux-strategy.md
├── strategy/                    # Strategic documents
│   ├── ux-foundations.md
│   └── ux-strategy-synthesis.md
├── mux/                         # MUX 2.0 collection
│   ├── README.md
│   ├── vision-learning-ux.md
│   └── tech-phases/
├── audits/                      # Historical audits
│   └── 2025-11-ux-audit/
└── voice/                       # Voice and tone
    └── voice-tone-guide.md
```

---

## Files Requiring PM Review

These need human judgment on whether they're:
- Reference docs (→ docs/)
- Working docs (→ stay in dev/)
- Obsolete (→ archive/)

1. All MUX issue-* files
2. UX audit collection (15 files)
3. Duplicate files across Nov 29/Dec 1
4. Voice guide location

---

**Next Steps**:
1. PM reviews and decides on MUX and audit handling
2. CXO reviews proposed directory structure
3. Execute moves for clear-cut cases
4. Resolve duplicates

---

*End of Report*
