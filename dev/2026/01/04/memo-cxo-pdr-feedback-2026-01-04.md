# Memo: CXO Feedback on PDR Package

**To**: Principal Product Manager
**From**: Chief Experience Officer
**Date**: January 4, 2026
**Re**: PDR-001, PDR-002, PDR-101 Review and Discussion Points

---

## Summary

The PDR package reflects strong strategic alignment. My UX strategy work has been translated with high fidelity, and the formalization into product decisions is sound. This memo offers refinements, not objections—the foundation is solid.

Three discussion points, one per PDR, plus validation of what's working well.

---

## What's Working Particularly Well

### PDR-001: "Onboarding IS the Primer"

This reframe is exactly right. The insight that the preferences questionnaire *demonstrates* conversational interaction—users learn how to talk to Piper by talking to Piper—eliminates the need for a separate tutorial artifact. Elegant.

### PDR-002: B2 as Release Criterion

Elevating B2 from "milestone" to "release criterion" has teeth. The statement "features that work technically but fail the B2 conversational test are not ready for users" gives us permission to hold work that's code-complete but experience-incomplete. This is rare and valuable.

### PDR-101: Methodology as Prototype

The recognition that our async multi-agent coordination (GitHub issues, session logs, handoffs) *is* multi-entity conversation—just human-mediated—grounds the capability in something we already understand. We're not inventing; we're formalizing.

---

## Discussion Point 1: PDR-001 — The "Bad Last Session" Edge Case

### The Gap

The cross-session greeting table handles temporal gaps well:

| Condition | Greeting Approach |
|-----------|-------------------|
| Same day, recent | Reference specific work |
| Next day, active | Light reference |
| Week+ gap | Offer choice |
| Month+ gap | Gentle reorientation |

But it doesn't account for *emotional* context. What if the previous session ended poorly?

**Scenario**: User spent 20 minutes trying to get Piper to do something, failed, left frustrated. Next day, Piper greets them with "Yesterday we were working on X—continue?"

This is tone-deaf. It surfaces the failure without acknowledging it.

### Proposed Addition

| Condition | Greeting Approach |
|-----------|-------------------|
| Previous session ended with frustration signals | Acknowledge fresh start: "Good morning! What would you like to work on?" (No reference to prior context unless user initiates) |

**Frustration signals** might include:
- Session ended abruptly after repeated failed queries
- User expressed explicit frustration ("this isn't working," "never mind")
- Session had high ratio of dead-end responses

### The Principle

Context-aware greeting should be *emotionally* context-aware, not just *topically* context-aware. Sometimes the kindest thing is to offer a clean slate.

### Question for Discussion

Is this edge case worth explicit handling, or is it over-engineering? My instinct says it matters—users who had a bad experience are exactly the users we risk losing.

---

## Discussion Point 2: PDR-002 — Trust Computation Specifics

### The Gap

PDR-002 establishes the trust gradient beautifully but leaves open: "What exactly counts as a 'successful interaction' for trust progression?"

This matters because trust computation will be implemented in code. Ambiguity here becomes inconsistent behavior.

### Proposed Framework

| Interaction Outcome | Trust Effect | Signal |
|---------------------|--------------|--------|
| **Successful** | +1 toward next stage | User acted on response (clicked, executed, continued meaningfully) |
| **Neutral** | No change | User acknowledged but didn't act, or conversation ended naturally |
| **Negative** | -1 (with floor) | User explicitly rejected, expressed frustration, abandoned mid-task |

**Stage thresholds** (strawman, needs calibration):
- Stage 1 → 2: ~10 successful interactions
- Stage 2 → 3: ~50 successful + evidence of pattern recognition value
- Stage 3 → 4: Extended history + explicit user comfort signal

**Regression rules**:
- 3 consecutive negatives: drop one stage
- 30-day inactivity: drop one stage (trust atrophies without reinforcement)
- Explicit user complaint about proactivity: immediate drop to Stage 2

### The Principle

Trust is earned incrementally and lost quickly. This mirrors human relationships—it takes many positive interactions to build trust, but a few bad experiences can erode it.

### Question for Discussion

Should trust computation be visible to users? ("Your trust level with Piper: Established") Or should it be entirely invisible, manifesting only in behavior differences? My instinct: invisible, but the *effects* should be noticeable enough that users feel progression.

---

## Discussion Point 3: PDR-101 — Participant-First Philosophy

### The Observation

PDR-101 defines two modalities:
1. **Host Mode**: Piper hosts multi-entity conversations
2. **Participant Mode**: Piper participates in externally-hosted contexts

The implementation path correctly sequences Participant Mode before Host Mode. But I want to make the philosophical stance explicit:

### Proposed Principle

**Piper should be an excellent participant before becoming a capable host.**

Rationale:
- Participant mode extends existing integrations (Slack) without new UI
- Users already have conversation platforms; they need a capable participant
- Host mode is a larger product surface with more UX risk
- Being a good participant teaches us what good hosting looks like

### The Risk of Host-First Thinking

If we optimize for Host Mode, we might build features that only work in Piper's native environment. Users would need to bring conversations *to* Piper rather than Piper meeting them where they are.

The colleague metaphor supports participant-first: colleagues join your meetings, contribute to your threads, show up where you're working. They don't ask you to come to their office for every interaction.

### Question for Discussion

Is "participant-first, host-second" the right strategic stance? Or are there scenarios where Host Mode should be prioritized (e.g., conversations that *need* Piper's structured model to be useful)?

---

## Minor Notes (Not Discussion Items)

### PDR-002: Memory Boundaries

The open question "How much cross-session context is helpful vs. creepy?" is well-posed. My initial instinct:

- **Helpful**: Remembering project context, user preferences, recent decisions
- **Creepy**: Remembering offhand personal comments, tracking behavioral patterns without disclosure

The test: Would a thoughtful colleague remember this? Colleagues remember what you're working on. They don't remember that you mentioned your kid's soccer game three weeks ago unless it was significant.

### PDR-101: Ted's Contribution Path

The workflow (Ted's internal coherency → translation to our vernacular → architectural review → implementation → PR → compliance → integration) is exactly right. It respects Ted's working style while maintaining our patterns. This is a good template for future external contributors.

---

## Summary

| PDR | Assessment | Discussion Needed? |
|-----|------------|-------------------|
| PDR-001 | Strong; one edge case to consider | Yes (bad last session) |
| PDR-002 | Strong; one open question to resolve | Yes (trust computation) |
| PDR-101 | Strong; philosophical stance to confirm | Yes (participant-first) |

The PDR package is ready for refinement, not rework. These are sharpening questions, not structural concerns.

---

*Looking forward to the discussion.*

— CXO
