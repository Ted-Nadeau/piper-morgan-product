# Memo: CXO Input — Conversation Lifecycle UX (#858 / #715)

**From**: Chief Experience Officer
**To**: Lead Developer, Principal Product Manager
**Date**: February 28, 2026
**Re**: UX guidance for Conversation Lifecycle Specification (#858)
**Context**: Feeds into #715 (MUX-HOME-CONVERSATIONS-LIFECYCLE)

---

## Summary

This memo provides CXO input on the user-facing aspects of conversation lifecycle. The goal is to ensure the technical specification (#858) produces UX that matches user mental models while preserving compatibility with the MUX vision (entity surfacing, multi-participant evolution, graph model).

---

## Core UX Principle

**Users don't think about conversation "lifecycle."** They think:
- "That time I talked to Piper about X"
- "What we discussed last week"
- "My old conversations"

Our UX should meet users where they are. Internal lifecycle states (RATIFIED, ARCHIVED, COMPOSTED) inform Piper's behavior but don't need to be visible to users.

---

## Section 1: Lifecycle States — User-Visible vs. Internal

### Recommendation: Simpler User-Facing States

| Internal State | User-Visible? | User Sees As |
|----------------|---------------|--------------|
| RATIFIED | No | (just "there") |
| ARCHIVED | Indirectly | "Older conversations" |
| COMPOSTED | No | "Piper remembers things" |

### User-Visible States (What Shows in UI)

| State | Meaning | Visual Treatment |
|-------|---------|------------------|
| **Active** | Recent, easily accessible | Normal appearance, in left sidebar |
| **Archived** | Older, searchable | Grouped separately or dimmed; in right sidebar |
| **Gone** | Deleted by user | Simply disappears (no "deleted" label) |

### The Colleague Test

A human colleague doesn't say "our ratified conversations" — they say "what we talked about last week." Our UI language should match natural speech.

---

## Section 2: Sidebar Identity — Navigation vs. Retrieval

### The Two Sidebars Serve Different Purposes

| Sidebar | Purpose | Mental Model | Shows |
|---------|---------|--------------|-------|
| **Left** | Navigation | "Switch to that other thing" | Recent active conversations |
| **Right** | Retrieval | "Find something from before" | Searchable archive + entities |

### Critical Clarification: Right Sidebar Is the Entity Surface

**The right sidebar is NOT "the conversation archive."** It is the **entity surface** — the place where hardened entities become visible to users.

Conversations appear there first because they are the first entity type users form through work with Piper. But the right sidebar will eventually surface:
- WorkItems with lifecycle states
- Features and domain objects
- Cross-channel activity
- Searchable history across entity types

This maps to the Three-Layer Context Persistence Model:
- Left sidebar = Layer 1 (Conversational Memory, 24-hour window, active)
- Right sidebar = Layer 2 (User History, all time, searchable, entities with state)
- Layer 3 (Composted Learning) is implicit in Piper's behavior, not directly surfaced

### Anti-Flattening Warning

Do not flatten the right sidebar to "conversation list with search." Its architectural intent is broader — it's the window into the user's work objects. The current implementation (conversations only) is a starting point, not the destination.

---

## Section 3: Conversation Naming

### Recommendation: Piper Names Conversations by Topic, Not State

**Naming triggers**:
- When topic becomes clear → Piper suggests or applies a name
- User can always override
- Fallback: Date-based ("Feb 28 chat"), not numbered ("Chat #47")

**State is visual, not nominal**:
- ❌ "Archived: M0 Planning" (state in name)
- ✅ "M0 Planning" with dimmed/grouped visual treatment (state in presentation)

The name stays stable across lifecycle transitions. The *presentation* changes.

---

## Section 4: Conversation Boundaries

### When Does a Conversation Start?

- User sends first message, or
- Piper initiates proactively ("Good morning, here's what's happening")

### When Does a Conversation End?

This is the hardest UX question. Users don't "end" conversations — they drift away.

### Recommendation: Soft Close via Inactivity, Hard Close via User Action

| Mechanism | Behavior |
|-----------|----------|
| **Soft close** | After 24-48 hours of inactivity, conversation is "soft archived" — still accessible, but new message starts a new conversation |
| **Hard close** | User explicitly archives or deletes from UI |
| **Piper suggestion** | "We covered a lot yesterday — want to start fresh or continue?" |

### The Colleague Model

You don't formally "end" a conversation with a colleague. But when you see them the next day, it's a new conversation — even if you reference yesterday's. Piper should behave similarly.

### New Day = New Conversation (Default)

After overnight inactivity, the default behavior should be to start a new conversation. Users who want to continue yesterday's can do so explicitly.

---

## Section 5: Multi-Entity Compatibility

### Language Recommendations

The spec should use language that doesn't preclude multi-participant conversations (per PDR-101, MultiChat PRD):

| Current Language | Future-Compatible Language |
|------------------|---------------------------|
| "My chat with Piper" | "Conversation about X" |
| "User's conversation" | "Conversation owner" or "created_by" |
| "Piper and I discussed" | "This conversation covered" |

### Branching and Forking

The spec should acknowledge that conversations may eventually branch or fork, even if the answer for now is "not yet." This ensures the boundary definition is extensible.

---

## Section 6: Auth Failures

### UX Principle: No Silent Failures

When auth expires during a session:
- User must be informed (not silent redirect)
- Clear action path: "Your session expired — please log in to continue"
- Conversation state should be preserved (no lost work)

---

## Section 7: Recommendations Summary

| Spec Section | CXO Recommendation |
|--------------|-------------------|
| **1. State Machine** | User-visible states (Active, Archived) simpler than internal states |
| **2. Creation Invariants** | Technical — no CXO input needed |
| **3. Auth Contract** | Surface failures to user; no silent failures |
| **4. Sidebar Identity** | Left = navigation, Right = entity surface (not just conversations) |
| **5. Representations** | Technical — no CXO input needed |
| **6. Scope & Boundary** | Soft close via inactivity; new day = new conversation by default |
| **7. Tests** | Include UX test: user can find old conversation via right sidebar search |

---

## On #715 Timing

**Recommendation: Keep #715 in M2 for now.**

The M0 testing revealed significant bugs (calendar queries, soft invocation, intent classification). Users aren't currently confused about conversation state — they're confused about whether Piper can hear them.

**Fix what's broken before adding what's missing.**

Once M0 fixes are stable and verified, #715 becomes a strong candidate for promotion. The spec work (#858) should proceed regardless — it informs the implementation whenever it happens.

---

## Anti-Flattening Checklist

Before finalizing #858 spec, verify these concepts are preserved:

- [ ] Right sidebar is "entity surface," not "conversation archive"
- [ ] Internal lifecycle states (RATIFIED, ARCHIVED, COMPOSTED) are distinct from user-visible states
- [ ] Conversation naming is by topic, not by state
- [ ] Language supports future multi-participant model
- [ ] Boundary definition allows for branching/forking evolution

---

*CXO input for Conversation Lifecycle Specification — February 28, 2026*
