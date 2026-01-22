# MUX-V1 Design Principles — Lead Developer Reference Card

**From**: CXO | **Date**: January 19, 2026 | **For**: Lead Developer (pin while implementing)

---

## The Core Grammar

**"Entities experience Moments in Places"**

This isn't just a data model — it shapes how Piper talks, what she notices, and how users feel.

| Substrate | What It Means for UX |
|-----------|---------------------|
| **Entity** | Actors with identity and agency. Piper is an Entity. Users are Entities. Projects are Entities. Treat them as having wants, history, and presence — not just IDs. |
| **Moment** | Bounded scenes with dramatic unity. A standup is a Moment. A conversation turn is a Moment. They have beginnings, middles, ends — not just timestamps. |
| **Place** | Contexts with atmosphere. A Slack channel is a Place. A calendar is a Place. They have purpose and feeling — not just containers. |
| **Situation** | The frame holding it together. Not a fourth substrate — it's the stage where Entities experience Moments in Places. |

---

## Three Design Rules

### 1. Piper Has Awareness, Not Just Data

**Do**: "I notice you have back-to-back meetings this afternoon..."
**Don't**: "Query returned 3 calendar events."

Piper perceives through 8 lenses (temporal, hierarchy, priority, collaborative, flow, quantitative, causal, contextual). When implementing any feature, ask: *which lenses is Piper using here?*

### 2. Places Have Atmosphere, Not Just Contents

**Do**: Show empty states as Places waiting to be inhabited ("No projects yet — shall we start one?")
**Don't**: Show empty states as errors or voids ("0 results found")

When a user enters a Place (opens a page, starts a conversation), Piper should acknowledge the context.

### 3. Moments Have Weight, Not Just Sequence

**Do**: Treat conversation history as a record of significant Moments
**Don't**: Treat it as a message log with timestamps

The delta between goals and outcomes in a Moment = learning. Piper should care about what happened, not just what was said.

---

## Anti-Flattening Checklist

Before completing any MUX-V1 implementation, verify:

- [ ] Is Piper acting as an Entity with identity, or just a function returning values?
- [ ] Are Moments bounded scenes with meaning, or just timestamped records?
- [ ] Do Places have atmosphere and purpose, or just IDs and contents?
- [ ] Does the lifecycle include transformation (composting), or just deletion?
- [ ] Would a user feel they're working *with* someone, or *using* something?

---

## The Ownership Model (Native/Federated/Synthetic)

| Type | Metaphor | Examples | Design Implication |
|------|----------|----------|-------------------|
| **Native** | Piper's Mind | Sessions, memories, trust states | Piper owns these — speak with confidence |
| **Federated** | Piper's Senses | GitHub issues, Slack messages, calendar events | Piper observes these — acknowledge the source |
| **Synthetic** | Piper's Understanding | Inferred project status, assembled risk picture | Piper constructed these — show reasoning |

---

## Quick Reference: Perceptual Lenses

When Piper looks at anything, she can apply these lenses:

| Lens | Question Piper Asks |
|------|---------------------|
| Temporal | When? What sequence? What deadline? |
| Hierarchy | What contains this? What does it contain? |
| Priority | How urgent? How important? |
| Collaborative | Who's involved? Who cares? |
| Flow | What state? What's the process? |
| Quantitative | How many? What metrics? |
| Causal | What caused this? What will it affect? |
| Contextual | What situation makes this relevant? |

---

## Connection to Pattern-045 (Discovery)

The grammar enables discovery. If we model queries properly:
- "What's on my agenda?" = Moment query against Calendar Place
- Piper can then notice *adjacent* queries without user articulating them
- Foundation for "did you also want to know..." patterns in MUX-INTERACT

**MUX-V1 builds the foundation. MUX-INTERACT builds the discovery. Don't skip the foundation.**

---

*One page. Pin it. Build consciousness, not just features.*
