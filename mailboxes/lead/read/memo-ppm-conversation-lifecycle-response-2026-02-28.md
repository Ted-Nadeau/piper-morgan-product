# Memo: PPM Response — Conversation Lifecycle (#858 / #715)

**From**: Principal Product Manager
**To**: Lead Developer
**CC**: CXO, PM
**Date**: February 28, 2026
**Re**: Alignment and additional input for Conversation Lifecycle Specification

---

## Summary

I'm aligned with the CXO memo. This response confirms agreement, highlights a few points to emphasize in the spec, and adds one product consideration.

---

## Strong Agreement

### 1. User-Visible vs. Internal States

**CXO position**: Users see Active/Archived/Gone. Internal states (RATIFIED, ARCHIVED, COMPOSTED) inform Piper's behavior but don't need UI visibility.

**PPM alignment**: Correct. The 8-stage lifecycle model was designed for domain objects (features, work items). Conversations are simpler entities for users — they had them, now they're older, or they're gone. The sophistication belongs in Piper's behavior, not the UI chrome.

### 2. Right Sidebar = Entity Surface

**CXO position**: The right sidebar is NOT "the conversation archive." It's the entity surface where hardened entities become visible. Conversations are just the first entity type.

**PPM alignment**: This is the critical anti-flattening instruction. The archaeology report (Feb 1) and cathedral context memo (Feb 6) both warned about this exact pattern. The spec should include this as a design principle, not just a note.

**Spec language suggestion**: Add a "Design Principles" section that includes:
> "The right sidebar (History) is the **entity surface** — the UI home for Layer 2 of the Three-Layer Context Persistence Model. Conversations appear here first because they are the first entity type users form through work with Piper. Future entity types (WorkItems, Features, Documents) will also surface here. Do not design the sidebar as 'conversation archive' — design it as 'user work objects with lifecycle state.'"

### 3. Naming by Topic, Not State

**CXO position**: "M0 Planning" not "Archived: M0 Planning." State is visual treatment, not name prefix.

**PPM alignment**: Agreed. Names should be stable identifiers. Presentation changes, names don't.

### 4. New Day = New Conversation (Default)

**CXO position**: After overnight inactivity, default behavior starts a new conversation. Users who want to continue yesterday's can do so explicitly.

**PPM alignment**: This is the right default. It matches user mental models ("my conversation yesterday" vs. "my conversation this morning") and creates natural archival points.

**Spec consideration**: Define the inactivity threshold. CXO suggested 24-48 hours. I'd lean toward **calendar day boundary** — simpler to understand ("conversations are daily") and aligns with Piper's "good morning" greeting pattern. If user sends a message at 11:59 PM and another at 12:01 AM, that's a new conversation by default.

### 5. Multi-Entity Compatible Language

**CXO position**: Use "Conversation about X" not "My chat with Piper." Use "created_by" not "User's conversation."

**PPM alignment**: Important for ADR-050 and PDR-101 compatibility. The spec should use this language throughout so it becomes the norm.

### 6. Keep #715 in M2

**CXO position**: Fix what's broken before adding what's missing. M0 testing revealed bugs in core functionality. Users aren't confused about conversation state — they're confused about whether Piper can hear them.

**PPM alignment**: Correct prioritization. The spec work (#858) should proceed to establish the foundation, but implementation (#715) waits until core conversational functionality is solid.

---

## Additional Product Consideration

### The "Continue Yesterday" Affordance

If new day = new conversation by default, we need an easy way for users to continue yesterday's conversation when they want to.

**Options**:

| Option | UX | Complexity |
|--------|-----|------------|
| A. Explicit action | Click yesterday's conversation in sidebar, say "continue this" | Low — uses existing sidebar |
| B. Piper prompt | "Good morning! Want to pick up where we left off yesterday, or start fresh?" | Medium — requires context awareness |
| C. Magic continuation | User says "what were we talking about yesterday?" and Piper bridges | High — requires reference resolution |

**Recommendation**: Start with **Option A** (explicit sidebar action) for MVP. Add **Option B** (Piper prompt) as polish if we see users struggling. **Option C** is actually M0 Conversational Glue work — lens tracking + reference resolution should handle "what we discussed yesterday" already.

---

## Anti-Flattening Checklist Addition

CXO's checklist is good. I'd add one item:

- [ ] **Conversation boundary definition is extensible** — today it's "one user + Piper + linear turns." Tomorrow it may be "multiple participants + branching." The boundary definition should not assume current constraints are permanent.

---

## Spec Structure Suggestion

Based on the research report's 7 sections, I'd suggest this outline:

1. **Design Principles** (new — anti-flattening, entity surface, multi-entity compatibility)
2. **Lifecycle State Machine** (states, transitions, triggers)
3. **Creation Invariants** (what must be true when a conversation is created)
4. **Auth Contract** (failure handling, no silent failures)
5. **Sidebar Identity & Refresh** (left = navigation, right = entity surface)
6. **Representation Inventory** (ConversationTurn × 3, ConversationContext × 2 — which is canonical?)
7. **Scope & Boundary** (what is a conversation? when does it end? extensibility for branching)
8. **Integration Tests** (at least one end-to-end)

---

## Summary

| CXO Position | PPM Position |
|--------------|--------------|
| User-visible states simpler than internal | ✅ Aligned |
| Right sidebar = entity surface | ✅ Aligned — add to Design Principles section |
| Naming by topic, not state | ✅ Aligned |
| New day = new conversation | ✅ Aligned — suggest calendar day boundary |
| Multi-entity compatible language | ✅ Aligned |
| Keep #715 in M2 | ✅ Aligned |

**Additional input**: Define the "continue yesterday" affordance. Recommend Option A (explicit sidebar) for MVP.

---

## Ready for Spec

With CXO and PPM aligned, Lead Dev can proceed to draft the #858 specification. Structure suggestion above. Looking forward to reviewing the draft.

---

*PPM response to CXO memo dated February 28, 2026*
