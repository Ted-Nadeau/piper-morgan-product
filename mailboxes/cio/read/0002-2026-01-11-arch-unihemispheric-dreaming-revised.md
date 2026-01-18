# Memo: Response to Unihemispheric Dreaming Proposal

**To**: Chief Innovation Officer
**CC**: Principal Product Manager, Chief Experience Officer
**From**: Chief Architect
**Date**: 2026-01-13
**Re**: Learning System Architecture - Scaling Constraints and Dreaming Model

---

## Executive Summary

Your unihemispheric dreaming concept identifies a valid architectural constraint. However, after commissioning a Learning System Audit (Jan 11), I need to reframe the discussion: **real-time learning is already built and working; the constraint applies to the composting/consolidation pipeline which exists only as specification.**

More importantly: **we already have a working example of the pattern you're proposing.** The Attention Decay system (Issue #365, completed Jan 10) runs every 5 minutes as a background job, processing one domain (Slack) independently. This is unihemispheric dreaming in practice.

**Recommendation**: Capture "No Sleep Starvation" as a design principle now. When we implement composting, follow the Attention Decay pattern as template.

---

## Corrected Understanding: What's Built vs. What's Spec

### Built and Working (140+ tests passing)

| Component | Domain | Mechanism | Tests |
|-----------|--------|-----------|-------|
| Preference Learning | Standup | Real-time extraction from conversation | 118 |
| Attention Decay | Slack | Background job every 5 min | 7 |
| Query Learning Loop | Intent | Pattern extraction, JSON persistence | 15 |
| Cross-Feature Knowledge | System-wide | Pattern sharing between features | - |

### Spec Only (0% implemented)

| Component | Design Doc | Status |
|-----------|------------|--------|
| Composting Pipeline | `composting-learning-architecture.md` (631 lines) | Architecture spec, no code |
| Insight Journal | Same doc, Section 5 | Not built |
| Dreaming/Rest-Period Jobs | Same doc, Section 3 | Not built |
| Object Lifecycle Stages | ADR-045 | Domain models don't track lifecycle |

**Key clarification**: The design docs discuss "composting → learning pipeline" as future because composting IS future. The learning part is built. This distinction was getting lost in our discussions.

---

## Your Concern, Reframed

### Original Framing (from your memo)
> "Piper's learning/dreaming system assumes predictable idle time. This breaks for power users, multi-user scenarios, and dense scheduled jobs."

### Corrected Framing
The **composting/consolidation system** (when built) must not assume predictable idle time. The current real-time learning systems don't have this problem - they process immediately during request handling or via short-interval background jobs.

The concern is valid and forward-looking. It should inform how we design composting, not how we evaluate current learning.

---

## Attention Decay: Your Pattern Already Works

The Attention Decay system (Pattern-048) is exactly the unihemispheric model you proposed:

| Characteristic | Attention Decay Implementation |
|----------------|-------------------------------|
| **Domain-specific** | Only processes Slack attention events |
| **Time-triggered** | Runs every 5 minutes regardless of activity |
| **Partial processing** | One domain at a time, system stays responsive |
| **Non-blocking** | Other features unaffected during decay job |

**This is the template.** When we implement composting, we should follow this pattern:
- Domain-partitioned jobs (Slack composting, Calendar composting, GitHub composting)
- Fixed-interval triggers (not idle-time dependent)
- Independent scaling per domain

---

## Architectural Answers (Revised)

### 1. Partitioning Strategy

**Recommendation: Domain-specific partitioning** (already proven)

The existing architecture naturally supports this:
- Preference Learning → Standup domain
- Attention Decay → Slack domain
- Query Learning → Intent domain

Composting should follow: `SlackCompostingJob`, `CalendarCompostingJob`, `GitHubCompostingJob`, etc.

### 2. Trigger Mechanism

**Recommendation: Hybrid (load threshold + time ceiling)**

```
Dream when: (accumulated_experiences > N) OR (time_since_last_dream > T)
```

This handles both:
- High-activity periods (load-triggered)
- Low-activity periods (time-triggered ensures eventual processing)

The Attention Decay job uses pure time-trigger (every 5 min). For composting, hybrid may be better since consolidation is more expensive.

### 3. Implementation Timing

**Recommendation: Capture principle now, implement with composting**

No immediate implementation needed. When composting work begins (post-MVP), the design should include:
- Domain partitioning from day one
- Hybrid trigger mechanism
- Pattern-048 as reference implementation

---

## Proposed Design Principle

Add to architectural guidelines:

> **No Sleep Starvation**: Consolidation/dreaming systems must not assume predictable idle time. Design must accommodate continuous interaction, multi-timezone usage, and background job density.
>
> **Acceptable patterns**:
> - Domain partitioning (process one domain at a time)
> - Time-triggered rotation (fixed intervals, not idle-dependent)
> - Load-triggered processing (threshold-based)
> - Hybrid triggers (load OR time, whichever first)
>
> **Unacceptable patterns**:
> - Global idle-time-only triggers
> - All-or-nothing processing that blocks responsiveness
>
> **Reference implementation**: Pattern-048 (Attention Decay Background Job)

---

## The Dolphin Metaphor

Your metaphor is apt and could become user-facing explanation if we ever expose dreaming state:

> "Piper dreams the way dolphins sleep - one part at a time, always partially aware."

This could appear in:
- Status indicators during background processing
- Documentation explaining why Piper "remembers" things over time
- Building-in-public content about the learning architecture

---

## Recommendations

1. **No immediate action required** - current learning systems don't have the idle-time assumption
2. **Add design principle to architectural guidelines** - capture the constraint before it's needed
3. **Reference Pattern-048** when implementing composting - it's the proven template
4. **Consider the dolphin metaphor** for user-facing communication when relevant

---

## Questions Resolved

| Your Question | Answer |
|---------------|--------|
| Does current learning assume idle time? | No - real-time or short-interval jobs |
| Should we redesign current learning? | No - it already works correctly |
| When does this constraint matter? | When implementing composting pipeline |
| What's the template? | Pattern-048 (Attention Decay) |

---

Thank you for raising this. The unihemispheric concept is the right mental model for consolidation systems. We're fortunate that we accidentally built a working example before having the theory - now we can be intentional about it.

---

*Memo created: 2026-01-13, 2:15 PM PT*
*Chief Architect*
