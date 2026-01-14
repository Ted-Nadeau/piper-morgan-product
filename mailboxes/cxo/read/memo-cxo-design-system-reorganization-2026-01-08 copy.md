# Memo: Design System Reorganization

**To:** CXO
**From:** Documentation Management Agent
**Date:** January 8, 2026
**Re:** Design System Front Door & UX Document Consolidation

---

## Executive Summary

We've completed a comprehensive reorganization of Piper Morgan's UX and design documentation, creating a "front door" (`docs/internal/design/README.md`) that serves as the authoritative entry point for both human designers and LLM agents. This consolidates 37 documents across 5 categories with explicit guidance on when to consult each.

**Your review is needed on:**
1. Design Philosophy statement (5 principles - draft needs validation)
2. Document Hierarchy (PDR > Brief > Spec > Voice Guide)
3. Whether the MUX 2.0 work is ready for integration or should remain exploratory

---

## What Was Done

### 1. Created Design System Front Door
**Location:** `docs/internal/design/README.md`

Key features:
- **"Consult When" guidance** - Each spec has explicit triggers for when agents should read it
- **Red Flags section** - Warning signs that an LLM is "going rogue" (creating patterns without specs, writing copy without voice guide, etc.)
- **Gap Detection Protocol** - Structured format for agents to report when they need guidance not covered by specs
- **Document Hierarchy** - Clear precedence when specs conflict

### 2. Consolidated UX Documentation (37 files total)

| Directory | Files | Contents |
|-----------|-------|----------|
| `specs/` | 6 | Greeting UX, Contextual Hints, FTUX, Empty States, B1 Rubric, Canonical Queries |
| `briefs/` | 2 | Conversational Glue, Discovery UX Strategy |
| `research/` | 2 | UX for AI Field Reconnaissance, Mobile UX Opportunity Mapping |
| `mux/` | 11 | MUX 2.0 Vision work (Nov 2025) - Grammar, Entity, Ownership, Composting phases |
| `audits/2025-11-ux-audit/` | 15 | Complete November 2025 UX Audit |

### 3. Resolved Duplicates
Four document sets existed in both `dev/2025/11/29/` and `dev/2025/12/01/`. All were verified identical via diff. Earlier date (Nov 29) designated canonical per PM decision.

### 4. PDR Directory Created
Moved PDRs to `docs/internal/pdr/` with README explaining their role as strategic intent documents.

---

## Items Requiring CXO Review

### 1. Design Philosophy (DRAFT - needs your validation)

Currently in README:
```
Piper Morgan's UX follows these core principles:

1. Conversational First: Piper is a colleague, not a tool
2. Trust Gradient: Behavior adapts based on relationship maturity
3. Discovery Over Documentation: Users learn by doing, not reading
4. Contextual Intelligence: Actions informed by what Piper knows
5. Graceful Degradation: Always provide value, even with limited context
```

**Questions:**
- Are these the right 5 principles?
- Is the ordering correct (most important first)?
- Any missing principles that should be added?

### 2. Document Hierarchy

Current precedence (higher number wins when specs conflict):
1. PDRs - Strategic intent
2. Design Briefs - Tactical direction
3. UX Specs - Implementation details
4. Voice Guides - Tone and copy

**Question:** Is this the right hierarchy for your design authority model?

### 3. MUX 2.0 Integration Status

The MUX work from November 2025 includes significant strategic vision:
- Grammar model: "Entities experience Moments in Places"
- Consciousness/embodiment principles
- Anti-flattening protocols
- Technical phase definitions (Grammar, Entity, Ownership, Composting)

**Question:** Should MUX concepts be:
- (a) Integrated into the main Design Philosophy as canonical?
- (b) Kept as exploratory work pending further development?
- (c) Merged selectively (which concepts)?

---

## Recommendations

### 1. Establish Spec Review Cadence
Many specs are marked "v1 Final" but haven't been reviewed since creation. Suggest quarterly review to ensure they reflect actual implementation.

### 2. Close Coverage Gaps
The README documents known gaps:
- Error messaging and recovery flows
- Mobile interaction patterns
- Accessibility guidelines
- Dark mode / theming
- Loading states and skeleton screens

Recommend prioritizing error messaging and accessibility as they affect all users.

### 3. Add "Interaction Playground" for Testing
Before implementing new patterns, agents should have a way to test against existing specs. The B1 Quality Rubric is a start, but a more interactive validation would help.

### 4. Consider Voice Guide Expansion
The Empty State Voice Guide is the only copy guidance. Consider whether we need:
- Error message voice guide
- Notification voice guide
- Onboarding copy standards

---

## Files for Your Direct Review

If you'd like to review the key documents:

1. **Front door (start here):** `docs/internal/design/README.md`
2. **Design Philosophy context:** `docs/internal/design/mux/piper-morgan-ux-strategy-synthesis.md`
3. **MUX Vision:** `docs/internal/design/mux/MUX-VISION-LEARNING-UX-updated.md`
4. **Issue generation strategy:** `docs/internal/design/mux/issue-generation-strategy-ux-20.md`

---

## Appendix: Full File Inventory

<details>
<summary>Click to expand full file list</summary>

**specs/**
- b1-quality-rubric-v1.md
- canonical-queries-v2.md
- contextual-hint-ux-spec-v1.md
- cross-session-greeting-ux-spec-v1.md
- empty-state-voice-guide-v1.md
- multi-entry-ftux-exploration-v1.md

**briefs/**
- conversational-glue-design-brief.md
- cxo-brief-discovery-ux-strategy.md

**research/**
- mobile-ux-opportunity-mapping.md
- ux-for-ai-research-reconnaissance.md

**mux/**
- MUX-VISION-LEARNING-UX-updated.md
- alpha-setup-and-mux-gate-issues.md
- issue-MUX-TECH-PHASE1-GRAMMAR.md
- issue-MUX-TECH-PHASE2-ENTITY.md
- issue-MUX-TECH-PHASE3-OWNERSHIP.md
- issue-MUX-TECH-PHASE4-COMPOSTING.md
- issue-generation-strategy-ux-20.md
- piper-morgan-ux-foundations-and-open-questions.md
- piper-morgan-ux-strategy-synthesis.md
- ux-strategic-brief-chief-architect-chief-of-staff.md
- object-model-brief-v2.md

**audits/2025-11-ux-audit/**
- 00-AUDIT-EXECUTIVE-SUMMARY.md
- 01-interaction-patterns-analysis.md
- 02-ftux-walkthrough.md
- 03-visual-design-review.md
- 04-user-journey-mapping.md
- 05-gap-analysis.md
- 06-design-system-foundation-analysis.md
- 07-competitive-analysis.md
- 08-voice-and-tone-analysis.md
- 09-integration-patterns-review.md
- 10-strategic-recommendations.md
- 11-research-bibliography.md
- 12-session-handoff-recommendations.md
- 13-prototype-opportunities.md
- 14-design-principles-extraction.md

</details>

---

*This memo generated as part of the Jan 8, 2026 documentation management session.*
