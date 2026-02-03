# PDR-002: Conversational Glue

**Status**: Draft v3.1
**Date**: February 1, 2026
**Author**: Principal Product Manager
**Stakeholders**: PM (xian), CXO, Chief Architect
**Review Status**: ✅ CXO Approved | ✅ Architect Approved

---

## Decision

Conversational continuity is a **first-class product feature**, not an infrastructure detail. The connective tissue between Piper's capabilities—how conversations flow, how context persists, how discovery happens—is as important as the capabilities themselves.

Piper's value proposition depends on this glue working seamlessly. A feature that exists but cannot be discovered, or that breaks conversational flow to be invoked, fails the colleague test.

**Core Vision** (v3): Users should be able to start a chat with Piper and converse naturally. Piper should carry on a general conversation—especially one relevant to product management—and workflows should emerge naturally from that conversation. Commands and skill invocations are shortcuts, not requirements.

---

## Context

The CXO UX Strategy work (Nov 2025 - Jan 2026) revealed a critical insight: Piper's features are largely built, but users struggle to discover and use them naturally. The gap isn't capability—it's continuity.

This manifests as:
- Users don't know what Piper can do until they ask the right question
- Transitions between tasks feel abrupt rather than conversational
- Context from previous interactions doesn't inform current ones
- Proactive suggestions feel random rather than situationally appropriate

Traditional product thinking treats these as UX polish—nice to have after core features work. This PDR establishes the opposite: **conversational glue is core functionality**.

**February 2026 Update**: External research validates this positioning. Modern conversational AI best practices emphasize "conversation as collaboration, not interface" — the paradigm shift from command-driven to LLM-native dialogue patterns. See `conversational-glue-implementation-guide.md` for comprehensive research findings and implementation guidance.

---

## The Problem

### Capability Without Discovery is Invisible Capability

Piper can perform standup synthesis, issue triage, calendar analysis, document intelligence, and more. But if a user doesn't know to ask, these capabilities might as well not exist.

The blank prompt pattern ("What can I help you with?") places full articulation burden on users. Research shows ~50% of users struggle to articulate what they need from AI systems (Nielsen, 2024). These users will never discover Piper's value—not because Piper can't help, but because they can't ask.

### Context Loss Breaks the Colleague Metaphor

A colleague remembers what you discussed yesterday. A colleague notices patterns in your work. A colleague offers relevant help without being asked.

If Piper forgets context between sessions, treats each conversation as isolated, and only helps when explicitly requested—Piper isn't a colleague. Piper is a tool with a chat interface.

### Proactive Help Without Trust is Annoyance

Unsolicited suggestions can be helpful or annoying depending on:
- Whether the suggestion is relevant
- Whether the timing is appropriate
- Whether the user trusts the suggester's judgment

Piper must earn the right to be proactive. This requires a trust model that governs when and how suggestions surface.

### Scripted Interactions Break the Illusion (v3)

Research confirms that users are "conditioned to expect human-like interaction" from conversational systems. When assistants violate conversational norms—parrot confirmations, interrogation-style slot filling, rigid scripted sequences—users notice immediately and "the illusion is broken by a faulty script."

Specific anti-patterns identified in current Piper implementation:
- "Is that your main project?" asked repeatedly during setup (they can't all be "main")
- Explicit confirmation dialogs for low-stakes actions
- Sequential slot-filling that ignores information already provided

---

## Decision Rationale

### Conversational Glue Has Three Components

**1. Discovery Glue**: How users learn what Piper can do
**2. Context Glue**: How information persists and connects across interactions
**3. Proactivity Glue**: How Piper offers help without being asked

Each component requires explicit product design, not just technical implementation.

### Five Foundational Principles (v3)

Based on research synthesis, all conversational design should follow these principles:

| Principle | What It Means | What It Forbids |
|-----------|---------------|-----------------|
| **Conversation as Collaboration** | Piper is a colleague, not a command line | "I don't understand" without alternatives |
| **Implicit Over Explicit** | Default to implicit confirmation | Parrot confirmations, multi-step dialogs |
| **Information Flows Forward** | Never ask for already-provided info | Re-asking for project name mid-workflow |
| **Graceful Over Rigid** | Handle the unexpected gracefully | "Complete current workflow first" |
| **Trust Governs Autonomy** | Proactivity increases with demonstrated competence | Maximum proactivity from day one |

---

## Component 1: Discovery Glue

### The Recognition Interface Pattern

Piper articulates the situation first, then offers relevant actions. This inverts the typical AI pattern where users must know what to ask.

**Instead of**: Blank prompt waiting for user input

**Do this**: Piper observes context and offers:
> "You have 3 GitHub issues that changed overnight and a standup in 2 hours. Want me to summarize the issues, or help you prep for standup?"

### Contextual Capability Hints

After successful task completion, Piper may surface one related capability the user hasn't used.

**Throttling rules** (prevent annoyance):
- Maximum 2 suggestions per 5 successful interactions
- Stop suggesting if user ignores 2 suggestions in a session
- Never interrupt flow—only suggest at natural pause points
- Respect "don't show me this again" for specific capabilities

**Example**:
> User completes issue triage
> Piper: "Nice work. By the way, I can also generate release notes from closed issues if that's ever useful."

### "What Can You Help With?" Response Quality

When users explicitly ask what Piper can do, the response must be:
- **Contextual**: Based on connected integrations and current project state
- **Prioritized**: Most relevant capabilities first, not alphabetical feature list
- **Actionable**: Each capability includes "want to try it?" option

**Anti-pattern**: Generic feature list that reads like marketing copy

**Implementation status**: #488 MUX-INTERACT-DISCOVERY implemented explicit "what can you do?" handling. Gap remains in contextual capability surfacing based on conversation state.

### Dead-End Recovery

When Piper can't help with a request, the response includes alternative paths:

**Instead of**: "I can't do that."

**Do this**: "I can't access your email directly, but I could help you draft a response if you paste the thread, or summarize your calendar to help you find time to respond."

---

## Component 2: Context Glue

### Session Context Persistence

Within a session, Piper maintains full context:
- What the user asked
- What Piper provided
- What decisions were made
- What tasks remain

This is table stakes—most chat interfaces do this.

### Cross-Session Memory

Between sessions, Piper maintains relevant context:
- User preferences (communication style, technical depth, etc.)
- Project state (active integrations, recent activity)
- Conversation history (what was discussed, what was decided)
- Trust level (earned through interaction history)

**Cross-session greeting** follows context-aware pattern (per PDR-001):

| Condition | Greeting Approach |
|-----------|-------------------|
| Same day, recent session | Reference specific work: "Back already! We were working on [X]—continue?" |
| Next day, active project | Light reference: "Yesterday we discussed [X]. Continue, or different focus?" |
| Week+ gap | Offer choice: "It's been a bit! Want to pick up where we left off, or start fresh?" |
| Month+ gap | Gentle reorientation: "Welcome back! Want me to catch you up, or start fresh?" |
| Previous session trivial | No reference: "What can I help with?" |

**Key principle**: Always offer the pivot. Never trap users in previous context.

**Implementation status**: #102 CONV-UX-GREET implemented calendar-aware greetings. ADR-054 designed cross-session memory architecture. Gap remains in full ADR-054 implementation.

### Entity Continuity

When users reference entities (projects, issues, people, documents), Piper resolves references across the conversation:

- "The issue we discussed" → resolves to specific GitHub issue
- "My standup" → resolves to user's recurring standup
- "That document" → resolves to most recently referenced document

This requires anaphoric reference resolution—understanding what "it," "that," and "the thing" refer to.

### Follow-Up Recognition (v3)

Beyond simple reference resolution, Piper must handle:
- **Lens inheritance**: "What about Thursday?" inherits the calendar lens from previous query
- **Elliptical phrases**: "And Sarah?" expands to "What about Sarah's availability?"
- **Comparative queries**: "How about tomorrow instead?" compares to previously discussed time

**Implementation status**: Pattern-011 (Context Resolution) provides foundation. Gap remains in lens tracking and ellipsis expansion.

---

## Component 3: Proactivity Glue

### The Trust Gradient Model

Piper's proactivity is governed by earned trust, not user preference. Users cannot simply enable "maximum proactivity"—trust must be demonstrated through competent behavior over time.

| Trust Stage | Piper Behavior | How Earned |
|-------------|----------------|------------|
| Stage 1 (New) | Responds to queries; no unsolicited help | Default for new users |
| Stage 2 (Building) | Offers related capabilities after task completion | ~10 successful interactions |
| Stage 3 (Established) | Proactive suggestions based on observed context | ~50 interactions + pattern recognition |
| Stage 4 (Trusted) | Anticipates needs; "I'll do X unless you stop me" | Extended history + explicit user comfort |

**Trust can decrease**: If Piper makes poor suggestions, misunderstands context repeatedly, or causes user to lose trust, proactivity level regresses.

### Trust Computation Framework

**Implementation status**: ADR-053 implemented trust computation (453 tests). Gap remains in wiring trust level to response generation.

**Interaction Outcomes**:

| Outcome | Trust Effect | Signal |
|---------|--------------|--------|
| **Successful** | +1 toward next stage | User acted on response (clicked, executed, continued meaningfully) |
| **Neutral** | No change | User acknowledged but didn't act, or conversation ended naturally |
| **Negative** | -1 (with floor) | User explicitly rejected, expressed frustration, abandoned mid-task |

**Stage Thresholds** (calibration needed—starting point):
- Stage 1 → 2: ~10 successful interactions
- Stage 2 → 3: ~50 successful + evidence of pattern recognition value
- Stage 3 → 4: Extended history + explicit user comfort signal

**Regression Rules**:
- 3 consecutive negative interactions: drop one stage
- 90-day inactivity: drop one stage (Stage 4→3 or 3→2 only; never below Stage 2 once earned)
- Explicit user complaint about proactivity: immediate drop to Stage 2

**Visibility Decision**: Trust level is invisible—no "Your trust level: Established" display. But effects should be noticeable enough that users feel progression. If user asks "Why did you just do that without asking?", Piper can explain: "Based on our history, I thought this was something you'd want me to handle. Should I check first next time?"

### Proactivity Triggers

At Trust Stage 3+, Piper may initiate based on:

| Trigger | Example Proactive Behavior |
|---------|---------------------------|
| Calendar event approaching | "Your standup is in 30 minutes. Want me to prep your notes?" |
| GitHub activity spike | "12 new comments on issues you own overnight. Summary?" |
| Document staleness | "Your roadmap doc hasn't been updated in 2 weeks. Review time?" |
| Pattern recognition | "You usually check PRs on Monday mornings. 3 await your review." |

### Proactivity Guardrails

**Never proactive about**:
- Sensitive personal information
- Actions that can't be undone
- Anything the user has dismissed twice

**Always ask before**:
- Taking action on behalf of user (until Trust Stage 4)
- Sharing information with others
- Modifying external systems

---

## Success Criteria

### Discovery Glue Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| Unprompted capability discovery (30-day) | ≥3 features per user | Users finding capabilities without explicit instruction |
| "What can you help with?" satisfaction | >4/5 rating | Response quality when explicitly asked |
| Dead-end recovery success | >60% continue conversation | Users don't abandon after hitting limits |
| Feature tour skip rate | N/A | No feature tour exists; discovery is conversational |

### Context Glue Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| Cross-session reference accuracy | >90% | When user references "what we discussed," Piper resolves correctly |
| Anaphoric resolution success | >85% | "It," "that," "the thing" resolved correctly |
| Context-aware greeting relevance | >80% user acceptance | Users don't immediately redirect after greeting |
| **Follow-up resolution accuracy (v3)** | >90% | "What about Thursday?" type queries resolve correctly |

### Proactivity Glue Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| Proactive suggestion acceptance | >30% at Stage 2, >50% at Stage 3 | Suggestions are relevant enough to act on |
| Proactive suggestion annoyance | <10% "don't show again" | Not annoying users |
| Trust progression | 50% reach Stage 2 within 30 days | Users earning trust through natural use |

### Dialogue Quality Metrics (v3)

| Metric | Target | Rationale |
|--------|--------|-----------|
| Multi-intent handling | >85% | Compound queries get coherent single response |
| Parrot confirmation rate | 0% | No verbatim repeating of user input |
| Explicit confirmation rate | <20% | Most interactions use implicit confirmation |
| Dead-end rate | <5% | Conversations rarely end in confusion |

---

## The B2 Quality Gate

From the CXO UX synthesis: **"B2" represents the threshold where conversational glue works well enough that users experience Piper as a colleague, not a chatbot.**

B2 is not a feature checklist. B2 is a qualitative assessment:
- Does conversation feel natural or stilted?
- Does Piper remember what matters?
- Are proactive suggestions helpful or annoying?
- Can users discover capabilities without reading documentation?

**B2 is a release criterion**: Features that work technically but fail the B2 conversational test are not ready for users.

### B2 Assessment Criteria (v3.1)

| Criterion | Test | Pass Condition |
|-----------|------|----------------|
| **Naturalness** | "Does this feel like talking to a colleague?" | Alpha testers agree ≥4/5 |
| **Memory** | "Does Piper remember what matters?" | Context references resolve >85% |
| **Proactivity** | "Are suggestions helpful or annoying?" | Acceptance >30%, annoyance <10% |
| **Discovery** | "Can I discover capabilities without docs?" | ≥3 features discovered/30 days |
| **Recovery** | "When I hit a wall, does Piper help me get unstuck?" | >60% continue after failure |
| **Flow** | "Can I accomplish goals naturally?" | No explicit command required for core tasks |

*Note: Recovery added per CXO feedback (Feb 1, 2026) — this is where colleague and chatbot most visibly diverge.*

### The Colleague Test (v3)

For any conversational interaction, ask:

> "If a human colleague responded this way, would it feel natural or weird?"

If weird, redesign.

### The Assistant Persona (v3.1)

*Added per CXO feedback — critical framing for voice design.*

**Piper is an assistant proving themselves — a junior peer earning expanded responsibility.**

This isn't a statement about capability; it's about role. An assistant:
- **Suggests**, doesn't instruct
- **Observes**, doesn't evaluate
- **Supports decisions**, doesn't make them
- Is appropriately **deferential** to the user they assist

| Manager Voice (wrong) | Assistant Voice (right) |
|----------------------|------------------------|
| "You should prioritize the API work." | "The API work blocks three other items — want me to move it up?" |
| "That's not the best approach." | "That could work. I noticed another option that might be simpler..." |
| "Remember to update the stakeholders." | "Should I draft a stakeholder update for you to review?" |

**The longer-term vision**: Piper aspires to be "promoted" to full product manager — given more responsibility and strategic work. But like any human assistant, that comes with time, proven expertise, and trust earned through consistent good judgment.

---

## Alternatives Rejected

### Explicit Feature Discovery (Tours, Tips, Badges)
**Rejected because**: Foreign to colleague metaphor. Colleagues don't give you achievement badges for discovering they can help with spreadsheets.

### User-Controlled Proactivity Settings
**Rejected because**: Users don't know what proactivity level is appropriate until they experience it. Trust-based progression is more natural than preference toggles.

### Session Isolation (Fresh Start Each Time)
**Rejected because**: Destroys the colleague relationship. Valuable for privacy-conscious users as an option, but not the default.

### Maximum Context Retention (Remember Everything)
**Rejected because**: Creepy. Users should feel Piper remembers what's relevant, not that Piper is surveillance. Selective memory is more human.

### Confidence Thresholds Without Tiering (v3)
**Rejected because**: Binary "understood/not understood" creates either over-confirmation or over-assumption. Tiered confidence (reject/explicit/implicit/proceed) matches natural conversation better.

---

## Implementation Requirements (v3)

Based on gap analysis against implementation guide, the following work is required:

### P0 — MVP Critical

| Requirement | Gap | Effort | Issue |
|-------------|-----|--------|-------|
| Follow-up recognition (lens inheritance) | Major | 3-5d | #427 Phase 2 |
| Multi-intent handling | Major | 5-8d | #595 |
| Natural slot filling | Moderate | 3-5d | TBD |
| "Main project" fix | Major | 1-2d | TBD |
| Soft workflow invocation | Moderate | 3-5d | TBD |

### P1 — MVP Important

| Requirement | Gap | Effort | Issue |
|-------------|-----|--------|-------|
| Confidence-tiered responses | Major | 3-5d | TBD |
| Repair strategy hierarchy | Major | 5-8d | TBD |
| Error-specific recovery | Major | 5-8d | TBD |
| Anti-parrot audit + fixes | Audit needed | 2-3d | TBD |
| Acknowledgment variation | Moderate | 2-3d | TBD |

### P2 — MVP Nice to Have

| Requirement | Gap | Effort | Issue |
|-------------|-----|--------|-------|
| Trust-proactivity wiring | Major | 3-5d | TBD |
| Context-aware tool surfacing | Major | 5-8d | TBD |
| Progressive disclosure | Major | 5-8d/workflow | TBD |

See `conversational-glue-implementation-guide.md` for complete requirements and `conversational-glue-gap-analysis.md` for detailed gap mapping.

---

## Implications

**For CXO**:
- Design recognition interface patterns for each major capability
- Specify contextual capability hint UX (when, where, how to dismiss)
- Design cross-session greeting variations
- Define "B2 quality" assessment criteria
- **Review implementation guide for UX requirements (v3)**

**For Chief Architect**:
- Cross-session memory architecture (what persists, how long, how retrieved) — ADR-054
- Trust level computation and persistence — ADR-053 ✓
- Anaphoric reference resolution system — Pattern-011
- Proactivity trigger infrastructure
- **Review implementation guide for architecture requirements (v3)**
- **Confidence scoring integration into intent classification (v3)**

**For Implementation**:
- Discovery glue is not separate from features—each feature needs discovery design
- Context glue requires UserContextService enhancements
- Proactivity glue requires trust computation (may be new system)
- **See M0 (Glue Sprint) for prioritized implementation plan (v3)**

---

## Relationship to Other PDRs

**PDR-001 (First Contact is First Recognition)**: FTUX is the first expression of conversational glue. The principles established there (Piper speaks first, multiple entry points, onboarding as primer) are specific applications of the glue patterns defined here.

**PDR-003 (Multi-Entity Chat)** [Pending]: Multi-entity conversations will require extended glue—how context persists when multiple participants are involved, how proactivity works in group settings.

---

## Open Questions

1. **Memory boundaries**: How much cross-session context is helpful vs. creepy? What's the retention policy? CXO "thoughtful colleague" test: remember work context and stated preferences; don't remember casual asides or inferred personal details.

2. ~~**Trust computation specifics**~~: **Resolved v2** — Framework established above (interaction outcomes, stage thresholds, regression rules). ADR-053 implemented.

3. **Privacy mode**: Should there be an explicit "don't remember this session" option? How does it interact with trust levels?

4. **Multi-device continuity**: If a user switches from desktop to mobile mid-task, how does context transfer?

5. ~~**Natural conversation patterns**~~: **Resolved v3** — External research conducted; implementation guide created with specific patterns for dialogue management, state architecture, workflow transitions, and anti-robotics.

---

## References

- CXO UX Strategy Synthesis (Nov 26, 2025) — Recognition interface, trust gradient origins
- CXO UX Summary Report (Jan 3, 2026) — B2 quality gate, discovery patterns, proactivity rules
- PDR-001: First Contact is First Recognition — FTUX as glue expression
- Nielsen research on articulation barrier (2024)
- Ethics-First Architecture — Trust gradient foundations
- Personalization Technical Assessment (Jan 4, 2026) — Adaptive detection infrastructure
- **Conversational Glue Implementation Guide (Feb 1, 2026)** — Research synthesis and implementation patterns (v3)
- **Conversational Glue Gap Analysis (Feb 1, 2026)** — Current state mapping and prioritization (v3)
- **External research sources** (v3): Stanford SLP, Google Conversation Design, Amazon Alexa, Microsoft Copilot Studio, Rasa CALM, CHI 2019/2025 papers

---

## Changelog

**v3.1 (February 1, 2026 — CXO/Architect Review)**:
- Added "Recovery" dimension to B2 Assessment Criteria (CXO feedback)
- Added "The Assistant Persona" section with role framing (CXO feedback)
- Clarified B2 Recovery test language
- Architect review confirmed architectural soundness

**v3 (February 1, 2026)**:
- Added "Core Vision" statement emphasizing natural conversation
- Added Five Foundational Principles section
- Added Follow-Up Recognition requirements (lens inheritance, ellipsis)
- Added Dialogue Quality Metrics (multi-intent, parrot rate, confirmation rate)
- Added B2 Assessment Criteria table with testable conditions
- Added "The Colleague Test" heuristic
- Added Implementation Requirements section with P0/P1/P2 prioritization
- Added references to implementation guide and gap analysis
- Resolved "natural conversation patterns" open question via external research
- Updated implementation status notes throughout
- Added "Scripted Interactions Break the Illusion" to problem statement

**v2 (January 4, 2026)**:
- Added Trust Computation Framework (CXO feedback)
- Added interaction outcomes table (+1 successful, 0 neutral, -1 negative)
- Added stage thresholds and regression rules
- Established visibility decision: invisible computation, visible effects, discussable on request
- Modified inactivity regression: 90 days (gentler than 30), never below Stage 2 once earned
- Added memory boundaries guidance ("thoughtful colleague" test)
- Flagged trust computation for Chief Architect ADR

**v1 (January 4, 2026)**:
- Initial draft establishing conversational glue as first-class product concern
- Defined three glue components: Discovery, Context, Proactivity
- Established trust gradient as proactivity governor
- Defined B2 quality gate
- Connected to PDR-001 and upcoming PDR-003

---

*PDR-002 | Draft v3.1 | February 1, 2026 | CXO ✅ Architect ✅*
