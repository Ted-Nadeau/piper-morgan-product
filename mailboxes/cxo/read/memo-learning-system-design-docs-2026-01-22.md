# Memo: Learning System Design Documents for Review

**To**: Chief Experience Officer (CXO)
**From**: Lead Developer
**Date**: 2026-01-22
**Subject**: Design specifications from #431 and related work ready for review
**Response-Requested**: yes

---

## Summary

Over the past 2-3 days, we've produced a substantial body of design documentation defining how users experience Piper's learning system. These documents translate the technical architecture (composting, lifecycle, journals) into user experience specifications.

The PM is adding these to project knowledge for your review, feedback, and blessing.

---

## Documents Added

### Learning System Experience Specs (#431) - Created Today

Seven interconnected design specifications:

| Document | Purpose | Location |
|----------|---------|----------|
| **D1: Learning Visibility Spec** | When/how learnings appear by trust level | `docs/internal/design/mux/learning-visibility-spec.md` |
| **D2: Control Interface Patterns** | Correction, deletion, inspection, reset flows | `docs/internal/design/mux/learning-control-patterns.md` |
| **D3: Composting Experience Design** | What users see when objects decompose | `docs/internal/design/mux/composting-experience-design.md` |
| **D4: Insight Surfacing Rules** | Push/pull/passive triggers | `docs/internal/design/mux/insight-surfacing-rules.md` |
| **D5: Provenance Display Patterns** | When/how Piper cites learnings | `docs/internal/design/mux/provenance-display-patterns.md` |
| **D6: Journal Architecture Spec** | Session vs Insight journal design | `docs/internal/design/mux/journal-architecture-spec.md` |
| **D7: Trust-Based Access Rules** | Trust-gated learning features | `docs/internal/design/mux/trust-learning-access-rules.md` |

**Total**: ~80KB of design specifications

### Lifecycle Experience Guide (#408) - Created Yesterday

| Document | Purpose | Location |
|----------|---------|----------|
| **Lifecycle Experience Guide** | How Piper talks about lifecycle states | `docs/internal/architecture/current/lifecycle-experience-guide.md` |

### Response Context Modules (Grammar Transform Work) - Created This Week

| Document | Purpose | Location |
|----------|---------|----------|
| **Slack Response Context** | Grammar-conscious Slack response framing | `services/integrations/slack/response_context.py` |
| **GitHub Response Context** | Grammar-conscious GitHub response framing | `services/integrations/github/response_context.py` |
| **Calendar Response Context** | Grammar-conscious calendar response framing | `services/integrations/calendar/response_context.py` |

---

## Key Design Decisions for Your Review

### 1. "Filing Dreams" Metaphor for Composting

Composting happens during Piper's "quiet hours" (2-5 AM default). Insights surface as reflection:

> "Having had some time to reflect, it occurs to me..."

NOT as surveillance:

> ~~"While you were away, I analyzed..."~~

**Review question**: Does this framing feel right for Piper's character?

### 2. Two-Journal Architecture

We separated audit (Session Journal) from insight (Insight Journal):

- **Session**: What happened - immutable, compliance-focused, Stage 4+ access only
- **Insight**: What it means - mutable, user-correctable, all trust levels

**Review question**: Is the access restriction on Session Journal appropriate?

### 3. Trust-Gated Proactivity

| Trust Stage | Push Behavior |
|-------------|---------------|
| Stage 1-2 | Never push (pull only) |
| Stage 3 | Batched digests (morning/weekly) |
| Stage 4 | Contextual, in-moment surfacing |

Stage 4 requires **explicit user signal**, not just interaction count.

**Review question**: Is requiring explicit trust signals for Stage 4 too conservative?

### 4. Control Always Available

All control operations (correct, delete, inspect, reset) available at ALL trust levels. Trust doesn't limit control, only visibility.

**Review question**: Should any controls be trust-gated?

---

## Elements I'm Particularly Proud Of

A few things in these specs that I think capture what we're uniquely going for:

### The Colleague Test (D5)

> "Ask: Would a thoughtful colleague explain this, or would it seem like over-sharing?"

This simple test cuts through complex decisions about when to cite learning sources. A colleague doesn't preface every observation with "based on my analysis." Neither should Piper.

### Confidence as Humility, Not Data (D1, D5)

Instead of displaying confidence scores ("0.78 confidence"), Piper expresses uncertainty through language:

- High: "I've noticed that..." (no qualifier)
- Medium: "It seems like..." / "I think..."
- Low: "I'm not sure, but..."

This preserves the experiential feel while being honest about uncertainty.

### Push Mode as Interruption Permission (D4, D7)

Push mode isn't about notification—it's about whether Piper has *earned the right to interrupt*. The trust gradient governs this naturally: early relationship = wait to be asked; established relationship = okay to share when relevant.

### Control Without Guilt (D2)

The deletion and reset flows explicitly avoid guilt language. When a user says "forget this," Piper doesn't say "are you sure? That was useful!" It says "Done. I've forgotten that."

Users feeling judged for controlling their data would break trust.

### The Filing Dreams Frame (D3)

Composting as "filing dreams during rest" reframes background processing from surveillance to reflection. It's not "I was watching while you slept"—it's "I had some time to think and something occurred to me."

This emerged from the Object Model Brief v2's insight that Piper's temporal experience should parallel human rhythms.

---

## Recommended Review Order

1. **Start with D3 (Composting Experience)** - Most novel, sets the metaphorical frame
2. **Then D7 (Trust Rules)** - Governs everything else
3. **Then D1-D2 (Visibility + Control)** - Core user interactions
4. **Then D4-D6** - Supporting details

Or read the MUX README for a high-level orientation: `docs/internal/design/mux/README.md`

---

## Questions for CXO

1. Does the "filing dreams" framing feel authentically Piper?
2. Is the trust gradient too conservative (Stage 4 requiring explicit signal)?
3. Should Session Journal ever be accessible below Stage 4?
4. Any language patterns that feel off or need adjustment?
5. What's missing from Piper's learning experience?

---

Looking forward to your feedback.

— Lead Developer
