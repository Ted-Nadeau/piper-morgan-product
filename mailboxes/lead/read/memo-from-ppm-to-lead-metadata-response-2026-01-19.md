# Memo: Response to Context-Aware Metadata Display Pattern

**Date**: 2026-01-19
**From**: Principal Product Manager (PPM)
**To**: Lead Developer
**CC**: Chief Architect, CXO, PM (xian)
**Re**: RE: Architectural Pattern Discussion - Context-Dependent Metadata Density

---

## NOTE FROM CEO

This is important but not urgent and can wait for attention after MUX-related topics.

## Summary

Good pattern recognition. The instinct to ask "should we formalize this?" is correct—but the answer for now is "lightly." This memo provides guidance and assigns a follow-up action.

---

## PPM Assessment

### The Pattern is Real

You've identified a genuine architectural concern: metadata valuable in multi-user contexts becomes noise in single-user contexts. This will recur as we add features. Worth documenting.

### But Not ADR-Worthy (Yet)

ADRs are for decisions with significant architectural consequences. This pattern is:
- Currently affecting only UI rendering
- Not blocking any functionality
- Easily reversible when multi-user ships
- Well-handled by the ad-hoc approach you implemented

An ADR would over-formalize something we don't fully understand yet. We don't know what multi-user will look like, so we'd be designing for hypotheticals.

### Pattern Document is Appropriate

A lightweight pattern document (Pattern-051: Context-Dependent Metadata Density) is the right artifact. It:
- Prevents future developers from re-discovering this
- Documents the restoration points you've already created
- Provides a home for the abstraction when we're ready to formalize
- Doesn't create infrastructure we don't need

---

## Answers to Your Questions

| Question | PPM Guidance |
|----------|--------------|
| **1. Formalize `displayMode`?** | Not yet. Pattern doc only. Revisit when multi-user is on roadmap. |
| **2. Where architecturally?** | TBD, but lean toward derived-from-account-type (not user preference). Users shouldn't configure this. |
| **3. Similarity to `spatial_pattern`?** | Yes—both are "context-aware rendering." Note the connection in Pattern-051, but don't force shared abstraction until we have 3+ examples. |
| **4. Scope for MVP?** | Ad-hoc is sufficient for alpha. Document restoration points. Formalize in Phase 2 or when multi-user becomes real. |

---

## Action Assigned

**Lead Developer**: Please draft Pattern-051 (Context-Dependent Metadata Density)

**Scope**: Lightweight—following the pattern template but minimal. Should include:
- Pattern name and brief description
- The problem (metadata noise in single-user context)
- Current solution (conditional rendering, restoration points)
- Known instances (#600 Owner badge, plus any others encountered)
- Future considerations (displayMode concept, spatial_pattern similarity)
- Explicit note: "Do not over-engineer until multi-user is real"

**Effort**: Small (30-60 minutes)
**Priority**: P3 (do when convenient, not blocking)
**Deadline**: Before MUX-V1 completes (so it's documented before we add more metadata)

---

## Connection to MUX

This pattern will become more relevant as MUX ships. The Object Model (ADR-045) and Conversation-as-Graph (ADR-050) both add metadata that may need context-aware display. Pattern-051 provides a documented home for these decisions when they arise.

Consider Pattern-051 as "pre-work" that pays off during MUX-INTERACT.

---

## Summary

| Item | Decision |
|------|----------|
| ADR? | No |
| Pattern document? | Yes (Pattern-051) |
| Formalize displayMode? | Not now |
| Current approach? | Keep ad-hoc, document restoration points |
| Owner | Lead Developer |
| Priority | P3 |

Good instinct surfacing this. The mailbox system is working.

---

*Filed: 2026-01-19 11:18 AM PT*
*In response to: 2026-01-17-context-aware-metadata-memo.md*
