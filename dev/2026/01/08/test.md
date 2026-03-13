# UX Onboarding Guide for Ted Nadeau

**Date:** January 8, 2026
**From:** CXO
**Re:** How to align your multi-entity chat work with Piper Morgan's UX approach

---

## TL;DR

You have repo access. The design system lives at `docs/internal/design/`. Start with the README there—it's the front door to everything UX.

---

## What You're Working With

Piper Morgan has accumulated UX specifications, design briefs, and strategic documents over the past few months. They've recently been reorganized into a coherent structure with a clear hierarchy.

**The key insight:** We've made decisions. Some things are settled and shouldn't be re-litigated. Other things are exploratory and open for input. The docs distinguish between these.

---

## Your Reading Path

### Phase 1: Orientation (Do This First)

| Document | Location | Time | Why |
|----------|----------|------|-----|
| **Design System README** | `docs/internal/design/README.md` | 10 min | The front door. Philosophy, hierarchy, what's settled. |
| **PDR-101: Multi-Entity Conversation** | `docs/internal/pdr/PDR-101-multi-entity-conversation.md` | 15 min | The strategic decision for YOUR work. Your PRD became this. |
| **PDR-002: Conversational Glue** | `docs/internal/pdr/PDR-002-conversational-glue.md` | 10 min | How all Piper conversations should feel. Applies to your work. |

After Phase 1, you'll understand:
- What Piper's UX philosophy is (colleague, not tool)
- What's been decided about conversation UX (trust gradient, proactivity rules)
- How your multi-entity work fits into the product vision

### Phase 2: Voice & Tone (Before Writing Any Copy)

| Document | Location | Time | Why |
|----------|----------|------|-----|
| **Empty State Voice Guide** | `docs/internal/design/specs/empty-state-voice-guide-v1.md` | 10 min | How Piper sounds. Templates for different contexts. |

This matters because your UI will have text—empty states, prompts, labels. They need to sound like Piper.

### Phase 3: Interaction Patterns (As You Design)

| Document | Location | Consult When... |
|----------|----------|-----------------|
| **Contextual Hint UX Spec** | `docs/internal/design/specs/contextual-hint-ux-spec-v1.md` | Adding proactive suggestions |
| **Cross-Session Greeting Spec** | `docs/internal/design/specs/cross-session-greeting-ux-spec-v1.md` | Handling "welcome back" states |
| **Canonical Queries v2** | `docs/internal/design/specs/canonical-queries-v2.md` | Implementing user query patterns |

### Phase 4: Quality Gate (Before Claiming Done)

| Document | Location | Why |
|----------|----------|-----|
| **B1 Quality Rubric** | `docs/internal/design/specs/b1-quality-rubric-v1.md` | Defines what "feels like a colleague" means in evaluable terms |

---

## Key Concepts to Internalize

### The Five Principles

1. **Colleague, Not Tool** — Piper is a professional colleague, not a chatbot
2. **Trust Gradient** — Behavior adapts based on relationship maturity
3. **Discovery Through Use** — Users learn by doing, not reading
4. **Context-Aware, Not Creepy** — Use context helpfully, respect boundaries
5. **Always Useful, Never Stuck** — No dead ends without a path forward

### The Contractor Test

When designing interactions or writing copy, ask: *"Would this feel appropriate from a contractor you hired last month?"*

If it feels too familiar → dial back
If it feels too cold → warm up

### What's Settled (Don't Re-Litigate)

These decisions are in PDR-002 and are final unless new evidence emerges:

- **Proactivity:** Trust-graduated (Stages 1-4), not a user toggle
- **Context Persistence:** Three layers (24hr memory / user history / composted learning)
- **Suggestions:** Max 2 per 5 interactions, stop after 2 ignored
- **Voice:** Professional colleague

### What's Open (Your Input Welcome)

From MUX 2.0 work—these are exploratory:

- Specific lens definitions (the 8 spatial dimensions)
- Perception/Orientation/Judgment cognitive boundaries
- Advanced trust features (premonitions)
- Multi-entity specific patterns (this is where you come in!)

---

## For Your AI Tools

I've prepared a context document you can give to ChatGPT, Cursor, or other AI coding assistants. It establishes the constraints and philosophy so they don't accidentally diverge from our approach.

See: `docs/internal/design/ai-context-piper-ux.md`

Paste it as system context or project instructions before doing UX work.

---

## Your Workflow Integration

Based on your email thread, your process is:

```
UI/UX Spec → State Diagrams → Figma → React → DSL → Demo → MVP
```

Here's how to align each stage:

| Your Stage | Alignment Check |
|------------|-----------------|
| UI/UX Spec | Does it follow the 5 principles? Does copy match voice guide? |
| State Diagrams | Do states respect trust gradient? |
| Figma | Does visual design feel "colleague"? (We don't have visual specs yet—flag gaps) |
| React | Are components consistent with existing patterns? |
| Demo | Does it pass B1 quality rubric? |
| MVP | PR review will validate alignment |

---

## When You Find Gaps

If you need UX guidance that doesn't exist in the specs, use this format:

```
⚠️ UX GAP DETECTED

Domain: [what you're implementing]
Searched: [which specs you checked]
Gap: [what's missing]

Options:
1. Proceed with pattern from [similar spec]
2. Flag for CXO/PM review
3. [your recommendation]

Awaiting guidance.
```

Post this in Slack, email, or a GitHub issue. CXO or PM will respond.

---

## Questions?

Reach out to xian. The design system is new (reorganized this week), so your experience using it will help us refine it.

---

*Welcome aboard. Looking forward to seeing multi-entity chat come to life.*

— CXO
