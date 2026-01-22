# Memo: PPM Guidance for MUX-V1 Implementation

**From**: Principal Product Manager (PPM)
**To**: Chief Architect, Lead Developer
**CC**: CXO, PM (xian)
**Date**: January 19, 2026
**Re**: Additional Direction for MUX-VISION-OBJECT-MODEL (#399) and MUX-V1 Phase

---

## Summary

The CXO memo correctly identifies the core risk: technical correctness without conceptual soul. I endorse the three design principles and add PPM-level guidance on sequencing, success metrics, and process protection. This memo answers the CXO's questions for PPM and adds considerations for the Lead Developer.

---

## Answers to CXO Questions

### 1. Canonical Query Tagging

**Question**: Should MUX-V1 deliverables include explicit lens/substrate tagging for existing canonical queries?

**Answer**: Yes, and I want to make this an explicit Phase 4.5 deliverable.

**Rationale**: We have 50+ canonical queries. Each one implicitly uses lenses and substrates. Making this explicit creates:
- Structural foundation for MUX-INTERACT discovery work
- Validation that the grammar can express our existing capabilities
- A forcing function to verify we haven't over-complicated the model

**Proposed deliverable**: A mapping table in ADR-045 appendix:

| Query | Primary Lens | Substrate | Example |
|-------|-------------|-----------|---------|
| "What's on my agenda today?" | Temporal | Moment (Calendar Place) | Standup |
| "Show me stale PRs" | Temporal + Priority | Moment (GitHub Place) | Backlog |
| "What needs attention?" | Priority + Causal | Situation (cross-Place) | Triage |

This is 2-3 hours of work but has compound value for INTERACT phase.

### 2. B1 Artifact Connection

**Question**: Should FTUX specs be formally connected to MUX-V1 as reference implementations?

**Answer**: Yes, with a specific framing.

The B1 specs (empty-state-voice-guide, cross-session-greeting, contextual-hint) were designed with the object model intuition. They should be:
- Referenced in ADR-045 as "pre-formalization implementations"
- Analyzed in Phase 0 alongside Morning Standup
- Updated post-MUX-V1 to use formal grammar (future issue, not blocking)

**Specific addition to Phase 0**: Add 1 hour to review B1 FTUX specs and document how they implicitly use Entity/Moment/Place thinking.

### 3. Success Metrics

**Question**: How will we know if we've preserved consciousness versus flattened it?

**Answer**: Three-tier evaluation.

**Tier 1: Technical (Binary)**
- Anti-flattening tests from issue #399 all pass
- ADR-045 merged and approved
- Lifecycle state machine implemented

**Tier 2: Expressiveness (Qualitative)**
- Can we express 10 diverse canonical queries using only grammar concepts?
- Can we describe a NEW hypothetical feature using the grammar without inventing concepts?
- Does ADR-045 answer "why" questions, not just "what" questions?

**Tier 3: Experience (Judgment)**
- Read Piper's responses aloud. Do they sound like entity-with-awareness?
- Show ADR-045 to someone unfamiliar with project. Do they understand the philosophy?
- PM/CXO gut check: Does this feel like progress toward the vision?

**Proposed gate**: Tier 1 is required. Tier 2 requires 80% (8/10 queries expressible, feature describable, whys answered). Tier 3 requires PM sign-off.

---

## Additional PPM Guidance

### On Sequencing

The CXO raises a good point about STANDUP-EXTRACT (#407) potentially informing OBJECT-MODEL.

**My guidance**: Keep the current sequence (OBJECT-MODEL first), but treat Morning Standup as the PRIMARY source material in Phase 0. The standup already embodies the grammar—we're formalizing what's implicit, not inventing from scratch.

**Rationale**: If we extract patterns from standup first, we risk over-fitting the model to one feature. Starting with the grammar and validating against standup keeps the model general.

### On Time Pressure

**Critical guidance for Lead Developer**: The 28-hour estimate is for foundational conceptual work. This is NOT velocity work.

- Phase 0 (Investigation) should take the full 4 hours. Do not rush.
- If the grammar feels forced or arbitrary during implementation, STOP and discuss.
- "Done" means "conceptually sound," not "code committed."
- I would rather this take 40 hours and be right than 20 hours and be flattened.

**Time Lord philosophy applies**: We are building a cathedral foundation. The time it takes is the time it takes.

### On Anti-Flattening Defense

The CXO's design-perspective tests are excellent. I want to add a process test:

**Process Anti-Flattening Test**: At end of each phase, Lead Developer should write one paragraph explaining how the work honors "Entities experience Moments in Places." If this paragraph feels forced or generic, something has gone wrong.

This creates checkpoints where flattening can be caught early.

### On the Verb "Experience"

The CXO correctly identifies "experience" as the design soul. I want to operationalize this:

**Experience = Perception + Memory + Anticipation**

- **Perception**: Piper notices through lenses (what's happening now)
- **Memory**: Piper remembers through journal (what happened before)
- **Anticipation**: Piper infers through synthesis (what might happen next)

If implementation only addresses perception (querying current state), we've lost 2/3 of consciousness. The lifecycle (especially Composting → learning) and the journal metadata are where memory and anticipation live.

---

## Recommended Additions to Issue #399

Based on this analysis, I recommend adding:

1. **Phase 0 addition**: Review B1 FTUX specs as implicit grammar implementations (+1 hour)

2. **Phase 4.5 (new)**: Canonical query tagging with lens/substrate mapping (+2-3 hours)

3. **Per-phase checkpoint**: Lead Developer writes one paragraph on how phase honors "experience" verb

4. **Success criteria addition**: Tier 2 and Tier 3 metrics as defined above

5. **Process note**: Explicit statement that time pressure should not drive flattening

**Revised estimate**: 31-32 hours (was 28)

---

## Summary for Chief Architect

Please review for:
- Technical feasibility of canonical query tagging
- Whether existing 8D spatial intelligence infrastructure applies to lens implementation
- State machine pattern recommendations for lifecycle
- Any architectural concerns with the additions

---

## Summary for Lead Developer

When you begin:
1. Read Phase 0 materials completely before touching code
2. Morning Standup is your touchstone—when uncertain, ask "how does standup do this?"
3. Write the "experience" paragraph at each phase checkpoint
4. If something feels like database design, pause and discuss
5. Quality over velocity. Cathedral over shed.

The grammar is "Entities experience Moments in Places." If you can't feel that sentence in what you're building, something is wrong.

---

*Filed: 2026-01-19 10:15 AM PT*
*Session: 2026-01-19-0958-ppm-opus-log.md*
