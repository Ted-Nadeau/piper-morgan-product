# UX Summary Report: Discovery & Conversational Glue

**To**: Principal Product Manager
**From**: Chief Experience Officer
**Date**: January 3, 2026
**Re**: Design Guidance for B2 Sprint and MUX-INTERACT Implementation

---

## Executive Summary

Pattern-045 ("Green Tests, Red User") identified a critical gap: we have 35 working canonical queries (56% of target), but users can't discover them. This report provides UX design decisions and interaction patterns to guide B2 implementation and subsequent MUX-INTERACT work.

**Core insight**: The problem isn't capability—it's discoverability. The solution is "conversational glue": the connective tissue that transforms isolated interactions into flowing dialogue.

---

## Part 1: Design Decisions

### 1.1 Proactivity Level

**Decision**: Assistant mode, with trust-gradient modulation toward Colleague

| Trust Stage | Proactivity Behavior |
|-------------|---------------------|
| Stage 1 (New) | Respond to queries; minimal unsolicited help |
| Stage 2 (Building) | Offer related capabilities after task completion |
| Stage 3 (Established) | Proactive suggestions based on context |
| Stage 4 (Trusted) | Anticipate needs; "I'll do X unless you stop me" |

**Rationale**: Users earn more proactive Piper through demonstrated value, not settings toggles. This prevents the "self-threat" dynamic where AI that assumes too much authority creates resistance.

**Implementation note**: Trust stage should be computed from interaction history, not user preference. The user doesn't choose their trust level—they develop it.

---

### 1.2 Context Persistence

**Decision**: Three-layer model

| Layer | Scope | Purpose |
|-------|-------|---------|
| **Conversational Memory** | 24-hour window | Natural continuity ("yesterday we discussed...") |
| **User History** | All past conversations | User-accessible archive (Claude-style chat list) |
| **Composted Learning** | Extracted patterns | Informs behavior without explicit recall |

**Rationale**: These serve different needs:
- Memory is about *flow*
- History is about *control* (user data ownership)
- Learning is about *value* (Piper improves over time)

**Implementation note**: When Piper references past context, it must be explicit:
> "Yesterday you asked about the Q1 roadmap—shall I pick up where we left off?"

Never implicit (which feels surveilled).

---

### 1.3 Suggestion Frequency

**Decision**: Context-dependent with throttling

| Trigger | Behavior |
|---------|----------|
| Dead-end response | Always offer next steps |
| Successful task completion | Offer one logical next action |
| Mid-conversation | Rarely interrupt |
| Session start | Proactive orientation based on context |
| User ignores 2 suggestions | Stop suggesting for that session |

**Throttle rule**: Maximum 2 proactive suggestions per 5 interactions.

**Rationale**: Piper surfaces capabilities when they're *relevant*, not when they're impressive.

---

## Part 2: Discovery Patterns

### 2.1 Recommended Patterns

**A. Contextual Command Palette**
- Triggered by `/` or `?` in input field
- Shows capabilities filtered by current context
- Example: In GitHub conversation, `/` surfaces GitHub commands first

**B. Proactive Capability Hints**
- After successful task: "Standup generated. *I can also post this to Slack.*"
- Throttled, never repeat same hint twice
- One hint per completion, max

**C. Empty State Education**
- Empty screens teach, not just display emptiness
- "No todos yet. *Say 'add a todo' or 'show my GitHub issues' to get started.*"
- Include conversational example + direct command

**D. "Did You Mean" Recovery**
- On uncertain intent: "Did you want to: (a) see calendar, (b) check GitHub, or (c) something else?"
- Failed interactions become discovery moments

### 2.2 Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| Feature tours | Users skip them |
| Capability lists | Overwhelming, not contextual |
| Badges for unused features | Feels like nagging |
| "Did you know..." unprompted | Interrupts flow |

---

## Part 3: Conversational Design Philosophy

### 3.1 Core Principle

**Professional colleague, not friend.**

Piper should feel like a competent team member you've worked with for a few months—helpful, proactive, occasionally anticipating needs, but not presumptuous about the relationship.

### 3.2 Voice Guidelines

| Do | Don't |
|----|-------|
| "I noticed you have a standup in an hour" | "I've been thinking about you!" |
| "Based on yesterday's chat..." | "I remember everything we've discussed" |
| "Would you like me to..." | "I'll go ahead and..." (without permission) |
| "I'm not sure—could you clarify?" | Pretend to know when uncertain |
| Use "I" sparingly | Overuse "I feel" or "I think" |

### 3.3 The Contractor Test

> Would this feel appropriate from a contractor you hired last month?

If yes, proceed. If it would feel too familiar or too cold from that person, adjust.

### 3.4 Avoiding Uncanny Valley

1. **Acknowledge limitations honestly** — "I can't access that yet" beats creative workarounds that fail
2. **Don't simulate emotions** — No "I'm excited to help!" Just help.
3. **Maintain consistent voice** — Same personality across Slack, web, CLI
4. **Let silence exist** — Not every response needs a follow-up question

---

## Part 4: FTUX & Discovery Relationship

### 4.1 Assessment

Discovery failure is *partially* an onboarding failure, but not entirely.

FTUX should teach three things:
1. **What Piper is** — PDR-001's "Piper speaks first" handles this ✓
2. **How to ask** — Currently weak ✗
3. **Where to start** — Currently okay ✓

### 4.2 Recommended FTUX Addition

A brief "conversation primer":

> "You can talk to me naturally. Some examples:
> - 'What's on my calendar today?'
> - 'Create a GitHub issue about the login bug'
> - 'Help me prepare for my standup'
>
> Not sure what to ask? Try 'What can you help with?'"

### 4.3 Ongoing Discovery

Users discover ~10% of capabilities in FTUX and ~90% through use. This is why contextual hints and "did you mean" patterns matter more than comprehensive onboarding.

FTUX-CONCIERGE should implement the "What can you help with?" response as a *contextual* answer:
> "Right now I can help with your calendar (connected), GitHub issues (connected), and general PM tasks. You haven't connected Slack yet—want to?"

---

## Part 5: Mental Model Formation

### 5.1 The Challenge

Users chronically underestimate *and* overestimate AI capabilities—often simultaneously.

### 5.2 Patterns That Help

| Pattern | Implementation |
|---------|----------------|
| **Capability Boundaries** | Explain limits in error states: "I can create issues, but can't merge PRs" |
| **Confidence Indicators** | "I think you mean Q1 roadmap (80% confident). Right?" |
| **Integration Visibility** | Settings dashboard shows what's connected |
| **Progressive Unlocks** | "We've worked together a week—want proactive suggestions?" |
| **Contextual "What Can You Do"** | Response varies by what's connected and recent context |

### 5.3 Target Mental Model

Users should internalize:

> "Piper knows what I've connected, remembers recent conversations, learns my patterns over time, and gets more proactive as we build trust. It won't do anything without asking first until I tell it otherwise."

---

## Part 6: B2 Implementation Guidance

### 6.1 Issue Mapping

| B2 Issue | Primary UX Pattern |
|----------|-------------------|
| MUX-INTERACT-DISCOVERY | Contextual command palette, "did you mean" recovery |
| FTUX-CONCIERGE | Empty state education, contextual capability response |
| CONV-UX-PERSIST | User history layer, explicit context referencing |
| CONV-UX-GREET | Session start proactive orientation |
| SLACK-ATTENTION-DECAY | Trust-gradient proactivity in notifications |

### 6.2 Recommended B2 Clustering

**Cluster 1: Discovery** (addresses Pattern-045 directly)
- MUX-INTERACT-DISCOVERY
- FTUX-CONCIERGE

**Cluster 2: Conversational Continuity**
- CONV-UX-PERSIST
- CONV-UX-GREET

**Cluster 3: Polish** (can run parallel)
- FTUX-QUICK-2, FTUX-QUICK-3
- SLACK-ATTENTION-DECAY

### 6.3 Success Criteria

B2 succeeds when:
- [ ] Users can discover capabilities without documentation
- [ ] "What can you help with?" returns contextual, useful response
- [ ] Dead-end interactions offer recovery paths
- [ ] Session continuity feels natural ("yesterday we discussed...")
- [ ] Proactive suggestions feel helpful, not intrusive

---

## Part 7: MUX-INTERACT Preview

The following MUX-INTERACT issues directly implement patterns from this report:

| Issue | Pattern Source |
|-------|---------------|
| INTERACT-RECOGNITION | "Did you mean" recovery (Section 2.1D) |
| INTERACT-TRUST-LEVELS | Trust gradient proactivity (Section 1.1) |
| INTERACT-DELEGATION | Professional colleague voice (Section 3.1) |
| INTERACT-PREMONITION | Proactive capability hints (Section 2.1B) |
| INTERACT-MOMENT-UI | Context persistence model (Section 1.2) |

This report serves as design foundation for that phase.

---

## Appendix: Key References

- **Pattern-045**: Green Tests, Red User (19 queries work, 0% discovery)
- **PDR-001**: FTUX as First Recognition
- **Conversational Glue Design Brief**: Chief Architect, Dec 26, 2025
- **Mobile Research Insights**: Entity-based interaction, trust through restraint
- **Learning System UX**: MUX-VISION-LEARNING-UX issue scope

---

## Summary

The path from "35 working queries that users can't find" to "conversational colleague that surfaces the right capability at the right moment" requires:

1. **Trust-graduated proactivity** — Earn the right to anticipate
2. **Three-layer persistence** — Memory, history, learning
3. **Contextual discovery** — Relevant suggestions, not feature lists
4. **Professional voice** — Contractor test, not friend test
5. **Boundary clarity** — Users know what Piper can and can't do

B2 implements the foundation. MUX-INTERACT extends it across the full interaction surface.

---

*Prepared by: Chief Experience Officer*
*Session: January 3, 2026, 6:04 PM - 7:30 PM*
*Status: Ready for PPM Review*
