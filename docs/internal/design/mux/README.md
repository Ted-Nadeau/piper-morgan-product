# MUX Design Documents

**Track**: MUX (Embodied UX)
**Purpose**: Design specifications for Piper Morgan's user experience

---

## Overview

This directory contains design documents for the MUX track, which focuses on how users *experience* Piper Morgan—not just what Piper does, but how it feels to work with Piper.

The MUX track implements the foundational grammar from ADR-045: **"Entities experience Moments in Places."**

---

## Document Index

### Learning System Experience (#431)

Design specifications for how users experience Piper's learning system.

| Document | Purpose |
|----------|---------|
| [learning-visibility-spec.md](learning-visibility-spec.md) | When and how learnings appear to users |
| [learning-control-patterns.md](learning-control-patterns.md) | Correction, deletion, inspection, reset flows |
| [composting-experience-design.md](composting-experience-design.md) | What users see when objects decompose |
| [insight-surfacing-rules.md](insight-surfacing-rules.md) | Push/pull/passive surfacing triggers |
| [provenance-display-patterns.md](provenance-display-patterns.md) | When and how Piper cites learnings |
| [journal-architecture-spec.md](journal-architecture-spec.md) | Session vs Insight journal design |
| [trust-learning-access-rules.md](trust-learning-access-rules.md) | Trust-gated access to learning features |

**Source Issue**: [MUX-VISION-LEARNING-UX-updated.md](MUX-VISION-LEARNING-UX-updated.md)

### Strategic Foundation

| Document | Purpose |
|----------|---------|
| [ux-strategic-brief-chief-architect-chief-of-staff.md](ux-strategic-brief-chief-architect-chief-of-staff.md) | Comprehensive UX strategy (37KB) |
| [piper-morgan-ux-strategy-synthesis.md](piper-morgan-ux-strategy-synthesis.md) | Strategy synthesis (25KB) |
| [piper-morgan-ux-foundations-and-open-questions.md](piper-morgan-ux-foundations-and-open-questions.md) | Foundational questions (22KB) |

### Implementation Planning

| Document | Purpose |
|----------|---------|
| [issue-MUX-TECH-PHASE1-GRAMMAR.md](issue-MUX-TECH-PHASE1-GRAMMAR.md) | Phase 1: Grammar implementation |
| [issue-MUX-TECH-PHASE2-ENTITY.md](issue-MUX-TECH-PHASE2-ENTITY.md) | Phase 2: Entity model |
| [issue-MUX-TECH-PHASE3-OWNERSHIP.md](issue-MUX-TECH-PHASE3-OWNERSHIP.md) | Phase 3: Ownership model |
| [issue-MUX-TECH-PHASE4-COMPOSTING.md](issue-MUX-TECH-PHASE4-COMPOSTING.md) | Phase 4: Composting lifecycle |
| [issue-MUX-VISION-LEARNING-UX.md](issue-MUX-VISION-LEARNING-UX.md) | Learning UX issue spec |
| [issue-generation-strategy-ux-20.md](issue-generation-strategy-ux-20.md) | UX issue generation strategy |
| [alpha-setup-and-mux-gate-issues.md](alpha-setup-and-mux-gate-issues.md) | Alpha testing gates |

---

## Key Concepts

### Trust Gradient

Piper's behavior adapts based on trust level:

| Stage | Name | Learning Behavior |
|-------|------|-------------------|
| 1 | New | Pull-only, minimal visibility |
| 2 | Building | On-request summaries |
| 3 | Established | Proactive sharing (batched) |
| 4 | Trusted | Full access, contextual surfacing |

### Two-Journal Architecture

- **Session Journal**: Audit trail (what happened) - immutable, Stage 4+ access
- **Insight Journal**: Learnings (what it means) - mutable, user-correctable

### Composting

When objects reach lifecycle stage 8 (COMPOSTED), they decompose into learnings. This happens during "quiet hours" and surfaces as reflection, not surveillance.

**Framing**: "Filing dreams" - Piper processes during rest, surfaces as "Having reflected..."

---

## Design Principles

1. **Colleague Test**: Would a thoughtful colleague do/say this?
2. **Reflection, Not Surveillance**: Frame learning as thinking back, not watching
3. **Control Always Available**: Users can correct, delete, inspect, reset
4. **Trust Governs Visibility**: More trust = more proactive sharing
5. **Honest Uncertainty**: Express confidence levels naturally

---

## Related Documentation

- **ADR-045**: Object Model (foundational grammar)
- **ADR-053**: Trust Computation Architecture
- **ADR-055**: Object Model Implementation
- `docs/internal/architecture/current/composting-learning-architecture.md`
- `docs/internal/architecture/current/lifecycle-experience-guide.md`

---

*Last updated: 2026-01-22*
