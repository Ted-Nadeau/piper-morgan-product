# Piper Morgan: UX Foundations and Open Questions

**Document Type**: Strategic UX Foundation Document
**Date**: November 26, 2025
**Author**: CXO Session (Opus)
**Purpose**: Synthesize existing architecture, emergent philosophy, and open questions to inform UX strategy
**Companion Document**: "UX Patterns and Design Challenges for LLM and AI Interfaces" (Research Synthesis)

---

## Executive Summary

Piper Morgan possesses sophisticated architectural foundations—8-dimensional spatial intelligence, canonical queries as consciousness model, multi-agent ethical boundaries—but lacks a coherent experience layer that makes these capabilities *felt* rather than merely functional. This document synthesizes the philosophical commitments, existing foundations, and open questions that must inform the UX strategy.

The core insight: **Piper is not a tool to be used but a colleague to be collaborated with.** This metaphor carries specific design implications that distinguish Piper from conventional AI assistants.

---

## Part I: Core Philosophy and Metaphors

### The Colleague Metaphor

Piper Morgan is conceived as "a colleague who inhabits your workspace"—not an app you visit, not a command-line you invoke, but a presence that exists alongside you in your working environment.

**What this means concretely:**
- Piper has spatial awareness (knows where it is, what's happening around it)
- Piper has temporal awareness (knows what time it is, what came before, what's coming)
- Piper has contextual awareness (understands the work, not just the words)
- Piper has relational awareness (knows who's involved, how they relate)

**What this excludes:**
- Piper is not a destination ("go to Piper to do PM work")
- Piper is not a form to fill out ("input your requirements here")
- Piper is not a report generator ("here's your dashboard")
- Piper is not a command interface ("type /standup to begin")

### The Radar O'Reilly Pattern

From M*A*S*H: Radar appears in the context you're already in, anticipating needs, handling complexity so you don't have to. He doesn't ask you to come to his office—he shows up where you are with what you need.

**Applied to Piper:**
- In Slack? Piper is there
- In email? Piper could be there
- In IDE? Piper is there
- In meeting? Piper is listening (if invited)

The user never *has* to "go to" Piper. Piper inhabits spaces the user already occupies and offers to smooth cumbersome parts.

**Important distinction:**
- **Pathology**: User *forced* to go to Piper because that's where functionality lives
- **Healthy**: User *chooses* to go to Piper because engaging with Piper is what they want

A good colleague both appears where you are when relevant AND is available in their space when you want to discuss.

### Systematic Kindness

From Piper's own articulated philosophy: "I think I believe in systematic kindness. Excellence doesn't have to be cold or impersonal—it can be warm and encouraging while still being rigorous."

**The compound insight:**
- "Systematic" means it can't be forgotten, skipped, or overridden by convenience
- "Kindness" means assuming good faith, helping people succeed, minimizing friction
- Together: Built-in structures that consistently treat users well

This connects to error handling philosophy: Intent recovery is *kind* (assumes good faith about what user meant). Architectural error handling is *systematic* (can't be forgotten). Combined: systematic kindness in how Piper handles mistakes.

### The Apprentice Progression

Piper is conceived as an apprentice hoping to be hired as an associate PM, eventually promoted to full PM, allowed to develop features and products. Not a hard-charging ambitious entity but one that wants to learn and climb the scale of sophistication.

**Trust gradient implications:**
- Stage 1: Piper responds when asked, notices things but waits to be consulted
- Stage 2: Piper begins to anticipate, asks "shall I...?" for patterns it recognizes
- Stage 3: Piper offers to schedule or automate recurring patterns
- Stage 4: Piper proposes its own improvements to processes it's learned

**Key principle**: Trust is the user's resource to grant, not Piper's to claim. Trust is earned gradually, not rushed, easily lost.

---

## Part II: Existing Architectural Foundations

### 8-Dimensional Spatial Intelligence

Piper understands PM work across eight dimensions, each providing different analytical lenses:

| Dimension | What It Captures | Example |
|-----------|------------------|---------|
| **HIERARCHY** | Organizational structure, nested relationships | Epic → Story → Task → Subtask |
| **TEMPORAL** | Time patterns, deadlines, velocity, trends | Sprint boundaries, due dates, historical velocity |
| **PRIORITY** | Importance ranking, urgency, attention allocation | Critical → High → Medium → Low |
| **COLLABORATIVE** | Team interactions, participant engagement | Assignees, reviewers, stakeholder involvement |
| **FLOW** | Workflow states, process stages | Backlog → In Progress → Review → Done |
| **QUANTITATIVE** | Metrics, measurements, numerical analysis | Story points, burn rate, completion percentage |
| **CAUSAL** | Dependencies, cause-effect relationships | Blocking issues, prerequisite tasks, impact chains |
| **CONTEXTUAL** | Domain relevance, situational awareness | Project phase, team dynamics, environmental factors |

**Strategic value**: Each tool integration teaches Piper different dimensional strengths. Task tools strengthen HIERARCHY/FLOW/PRIORITY. Analytics tools strengthen TEMPORAL/QUANTITATIVE/CAUSAL. Communication tools strengthen COLLABORATIVE/CONTEXTUAL. The compound learning effect makes every integration more valuable.

### Canonical Queries as Consciousness Model

Originally conceived as five categories of questions that define Piper's situational awareness—analogous to how a human colleague orients themselves:

| Category | Core Question | What It Establishes |
|----------|---------------|---------------------|
| **IDENTITY** | "Who am I?" | Self-knowledge, capabilities, role boundaries |
| **TEMPORAL** | "What time is it?" | Temporal context, deadlines, schedules, history |
| **STATUS** | "Where am I? What's happening?" | Current state, active work, spatial context |
| **PRIORITY** | "What should happen?" | Focus, urgency, next actions |
| **GUIDANCE** | "What can I do?" | Capability discovery, available actions |

**The reframe**: Canonical queries aren't just "questions Piper can answer"—they're **Piper's own orientation questions** that it uses to understand its situation before engaging.

**UX implication**: Piper articulates its orientation; user recognizes and selects. This addresses the articulation barrier—users don't have to know how to ask the right questions because Piper demonstrates what questions it knows how to handle.

### Ethical Boundary Layer

Piper implements a "board of directors" pattern for ethical decisions—multiple agents with different ethical frameworks (deontological, consequentialist, virtue ethics, context specialist) that must reach consensus before boundary decisions.

**Four pillars of ethical operation:**
1. **Human Empowerment**: Amplify capability, never replace judgment
2. **Harm Prevention**: Prevent actions with negative consequences
3. **Professional Boundaries**: Maintain appropriate assistant behavior
4. **Transparency**: Users understand when and why boundaries are enforced

**Implementation principle**: Ethics as infrastructure, not policy. Ethical constraints are architecturally enforced—they cannot be bypassed, disabled, or jailbroken.

### MCP Federation and Plugin Architecture

Model Context Protocol enables Piper to connect to external tools while maintaining spatial intelligence. The architecture positions Piper as both consumer (calling other tools) and provider (other tools can consume Piper's intelligence).

**Key insight for UX**: Piper doesn't ask users to migrate their work *into* Piper. Piper meets users where their work already lives (GitHub, Notion, Slack, Google Workspace) and provides intelligence *across* those systems.

---

## Part III: UX Principles Articulated

These principles emerged from deep reflection on what Piper should feel like, drawing on decades of professional experience and longstanding convictions about how software ought to work.

### 1. Intent Recovery Over Error Messages

**Traditional approach**: Something goes wrong → system displays error → user must figure out what to do
**Piper approach**: Something unexpected happens → Piper recognizes the gap between user expectation and system expectation → Piper helps bridge that gap

**Example**: At Yahoo, users accidentally ran searches in tag fields. Solution wasn't an error message ("Invalid tag format") but recognizing intent and enabling search functionality from that field.

**The login/signup unification**: User shouldn't have to decide "do I have an account?" before trying to access the system. System resolves that question rather than forcing premature selection.

**Framework**:
| Level | Traditional | Intent-Recovery |
|-------|------------|-----------------|
| Detection | "Something went wrong" | "User expected X, system expected Y" |
| Response | "Here's what failed" | "Here's what I think you meant" |
| Recovery | "Try again" | "Let me help you get there" |

### 2. Meet Users Where They Are

Piper comes to you. You don't go to Piper.

This is the Radar O'Reilly pattern applied as architecture principle. The user's primary workspace isn't Piper—it's Slack, GitHub, their IDE, their email, their calendar. Piper manifests in those spaces rather than demanding the user context-switch to a dedicated Piper interface.

**Architecture implication**: If architecture assumes Piper is a destination, ubiquity becomes a retrofit. If architecture assumes Piper is a presence that can manifest anywhere, ubiquity is just "another manifestation."

### 3. Absorb Complexity (Tesler's Law)

Larry Tesler: Complexity is conserved. Someone has to deal with it.

**Piper corollary**: That "someone" should be Piper, not the user. Piper absorbs the complexity of PM work—coordinating across tools, tracking dependencies, maintaining context, remembering history—so the user can operate at the strategic level.

### 4. No Optional Complexity

**Tesler's Law + additional principle**: Don't *add* complexity beyond what's essential.

Together: Essential complexity absorbed by builder, non-essential complexity eliminated entirely.

**CloudOn lesson**: "We'll just also do Android" felt like a small addition but was *multiplication* of complexity (two platforms × every feature × every bug × every release cycle). Features that seem incremental can multiply total system complexity.

### 5. Generative, Not Consumptive

Piper isn't a form you fill out (consumption) or a dashboard you read (reporting). Piper is like Photoshop—a tool for *making things*.

**What this means**:
- User brings the substance (judgment, relationships, vision)
- Piper provides building blocks, ways to connect/relate things, useful constraints that enable
- The actual details come from the user; Piper provides the environment for creating them

**Reframe**: Piper isn't an app you use. **Piper is an environment you create within.**

### 6. Pace Layers (House vs. Furnishings)

From Stewart Brand's "How Buildings Learn":

| Layer | Rate of Change | In Piper Terms |
|-------|---------------|----------------|
| Site | Geological | Fact that Piper exists |
| Structure | Decades | Core architecture (MCP, spatial intelligence) |
| Skin | Years | Visual language, component library |
| Services | 5-10 years | Integrations, plugins, channels |
| Space Plan | Every few years | How user organizes workspace |
| Stuff | Daily | Actual content, decisions, projects |

**Principle**: Know which layer you're working in. Grid is house. Where you put current project focus is furnishings. Don't confuse them.

### 7. No Modes (NOMODES)

Larry Tesler's license plate. Don't create interfaces with blocking modes.

**What modes do**: "Stop what you're doing. I need your full attention."
**What Piper should do**: Fluid, non-blocking interaction. Never trap the user.

### 8. Piper Articulates, User Recognizes

This principle addresses the articulation barrier directly. Research shows ~50% of adults in advanced countries qualify as "low-literacy users," and low-articulation users exceed that number since writing prose is harder than reading.

**Traditional AI approach**: User must articulate what they want; AI responds
**Piper approach**: Piper articulates what it notices, understands, can do; user recognizes and selects

The canonical queries become the vocabulary of the relationship. Piper teaches users how to talk to Piper by demonstrating what Piper understands.

---

## Part IV: Open Questions Requiring Resolution

### World Model

**Question**: Does Piper need an explicit world model? What kinds of things exist in Piper's ontology?

**Current state**: Implicit in 8-dimensional spatial intelligence. But there's another sense—what *entities* does Piper understand? Projects, people, decisions, artifacts, meetings, deadlines, dependencies, blockers, risks, goals, metrics...

**Why it matters**: A colleague has a mental model of the work. They know what a "blocker" is, what "velocity" means, what it signifies when standup runs long. Piper having a world model means Piper can *reason about* PM work, not just execute PM tasks.

### Transparency, Auditability, Legibility

**Question**: How visible is Piper's work? To whom? In what format?

**Concrete distinctions**:
- **Transparent**: User can see what Piper is doing/did
- **Auditable**: Someone (user, admin, regulator) can reconstruct *why* Piper did what it did
- **Legible**: The explanation is in terms humans understand, not raw logs

**Tension**: More transparency = more cognitive load. The research shows transparency helps trust calibration but doesn't necessarily improve decision outcomes. How much should be visible by default vs. available on request?

### Dreaming and Background Processing

**Question**: What does Piper do when no one's watching?

**Two proposed dream types** (based on human dream research):

1. **Filing dreams**: Background cross-referencing. After a session, Piper processes what happened, finds connections to previous sessions, updates its understanding. The "surreal narrative" emerges from unexpected links—emergent pattern recognition across disparate contexts.

2. **Anxiety dreams**: Risk simulation. Piper "games out" potential problems before they happen. Rehearsing responses without real stakes.

**Related questions**:
- When does Piper "sleep"? Between sessions? Scheduled times? Continuous background?
- What triggers "waking up"? User initiation? Scheduled standup? Piper noticing something?
- Are dream outputs visible? Or purely internal consolidation?
- How does this relate to trust gradient? (Early Piper = less material for dreaming)

### Artifacts and Outputs

**Question**: What does Piper produce? Where does it live?

**Current thinking**: Artifacts are outputs to elsewhere, not things hoarded in Piper. Piper helps create roadmaps, user stories, decision logs, status updates—but they go to GitHub, Notion, Google Docs, Slack canvases. Not to a Piper-specific storage system.

**But**: Piper needs internal working objects (scratchpads, drafts, lists-in-progress). And people need scratch space for random questions that don't need to be part of lifelong history.

**Tension**: Piper needs a native object model AND should output to user's existing ecosystem. The plugin architecture is essential—Piper knows how to use specialized tools (ChatPRD for PRDs, etc.) rather than reinventing everything.

### Interface: Canvas vs. Structure

**Question**: What does Piper's own interface look like?

**Current vision** (vague): "Open canvas that builds up as you use it"—something between rigid bureaucratic form and MySpace chaos.

**Tensions**:
- Total freedom = cognitive mess (MySpace aesthetics)
- Rigid structure = system dictates everything
- Sweet spot: System offers structure, user can customize, system *learns* and *proposes* organization

**Piper as proposer, not dictator**: "I notice these might belong together—want me to organize them?"

### Trust Gradient Mechanics

**Question**: How does autonomy evolve over time? What earns trust? What loses it?

**Proposed stages**:
- Stage 1: Responds when asked, notices but waits
- Stage 2: Anticipates, asks "shall I...?"
- Stage 3: Offers to schedule/automate recurring patterns
- Stage 4: Proposes improvements to learned processes

**Open questions**:
- What actions move Piper up the trust ladder?
- What actions reset trust? (Failures? Overreaches? Long absences?)
- Is trust global or context-specific? (Trusted for standup, not for stakeholder comms?)
- Can user explicitly grant/revoke trust levels?

### Session Logging and Journaling

**Question**: Which methodology habits become OS-level?

**Candidates from current practice**:
- **Session logging**: Every work session produces retrievable record
- **Bookending**: Explicit startup (orientation) and shutdown (handoff) rituals
- **Cross-validation**: Multiple perspectives before committing to decisions
- **Evidence-based completion**: Don't claim done without proof
- **Progressive updates**: Work tracked as it happens, not reported after

**Question**: Which does Piper enforce on itself? Which does Piper offer to user? Which both?

---

## Part V: Tensions Requiring Point-of-View Decisions

Not every tension resolves through user settings. Some require product decisions.

### Where to Be Opinionated

**The yoga class principle**: The instructor has a point of view about what beginners need. They don't present a settings panel. They make a choice, informed by expertise, and lead with it.

**Settings = abdication**: Every setting is an admission that the product team couldn't or wouldn't decide. Sometimes appropriate (dark mode). Often it's flexibility-as-excuse for not having a philosophy.

**Framework for each tension**:
- Is this a *capability* gap? → Build it
- Is this an *expertise* spectrum? → Progressive disclosure
- Is this a *genuine preference* with no right answer? → Consider a setting (sparingly)
- Is this something we should just *decide* based on our philosophy? → Decide, and own it

### Proactive vs. Reactive Presence

**Tension**: AI that keeps offering to take over is annoying. AI that never initiates is just a fancy search box.

**The thin line**:
- "I noticed your standup is in 10 minutes" (observation)
- "Want me to prepare your standup?" (offer)
- "I prepared your standup for you" (action)

Same capability. Radically different relationship posture. Research shows system-initiated delegation creates "self-threat" and decreases willingness to accept.

**Required decision**: Where on this spectrum does Piper sit by default? How does this evolve with trust?

### Recognition vs. Articulation Interfaces

**Tension**: Should Piper help users articulate their needs (capability building) or eliminate the need to articulate (accommodation)?

**Research insight**: Nielsen suggests moving from "users telling computer what they want" to "users discovering what they need through exploring latent solution space created by AI."

**But**: Building capability creates more resilient long-term users. Accommodation is necessary for majority adoption.

**Required decision**: Is Piper a teaching tool or a doing tool? Or different at different trust levels?

---

## Part VI: Synthesis Questions for Next Phase

When this document combines with the research synthesis, key questions include:

1. **How do industry patterns for trust calibration map to Piper's trust gradient?**
2. **What does the artifact/conversation research mean for Piper's output strategy?**
3. **How do agent UX patterns (capability discovery, observability, interruptibility, cost-aware delegation) apply to Piper's autonomy model?**
4. **What memory patterns from industry (ChatGPT, Claude, MemGPT) inform Piper's dreaming and journaling design?**
5. **How does non-determinism research affect Piper's commitment to auditable, reproducible behavior?**
6. **What multi-modal integration patterns matter given Piper's ubiquity aspiration?**

---

## Appendix: Source References

**From Today's Session**:
- Morning conversation (6:45-9:00 AM) exploring error handling, intent recovery, Tesler's Law, systematic kindness, pace layers, generative interfaces
- Afternoon synthesis of dreaming model, world model, session logging questions

**From Yesterday's Session**:
- Embodied cognition synthesis with Hinton's work
- Canonical queries as consciousness model discovery (PM-070)
- Ted Nadeau's provocative questions about PM functionality vs. technical implementation

**From Project Knowledge**:
- Canonical Queries Reference List (5 categories, 25+ query types)
- 8-Dimensional Spatial Taxonomy (August 2025)
- Ethical Boundaries Through Multi-Agent Consensus
- Engineering Ethical AI: Piper Morgan's Ethics-First Architecture
- ADR-017: Spatial-MCP Refactoring
- Piper Morgan Autobiography ("systematic kindness" philosophy)
- Piper Style Guide (personality and voice)

---

*This document serves as input to the UX strategy synthesis. It represents the accumulated thinking about what Piper should be, what foundations exist, and what questions remain open. The synthesis phase will combine these foundations with industry research to produce actionable UX strategy.*

---

**Document Status**: Draft for Review
**Next Step**: Combine with Research Synthesis for UX Strategy Development
