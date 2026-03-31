# Piper Morgan Vision v2.0 — DRAFT

**Status**: Draft for PM review
**Author**: Piper Alpha, incorporating 10 months of project learning
**Date**: March 31, 2026
**Supersedes**: vision.md (June 21, 2025) — preserved as founding vision

---

## What Changed Since the Founding Vision

The June 2025 vision described three phases: intern → associate → advisor. That trajectory still holds directionally, but ten months of building taught us things the founding vision couldn't know:

1. **The LLM is the floor, not the ceiling.** Piper should always be at least as good as a well-prompted LLM with the user's context. Structured handlers make it *better*, not *different*. (ADR-060, March 2026)

2. **Entities experience Moments in Places.** The object model isn't a data schema — it's a constitutional grammar that resolves design disputes and catches category errors before they become technical debt. (ADR-045, November 2025)

3. **Completion discipline matters more than velocity.** The ALL STOP (September 2025), the 75% Pattern, and the Inchworm Protocol taught us that finishing things is harder and more valuable than starting them.

4. **The PA experiment is testing the architecture.** Piper Alpha — a well-briefed Claude agent doing real PM work — is empirically testing where the LLM floor is sufficient and where structured infrastructure is required. The gap between what PA can do and what Piper should eventually do *is* the product roadmap.

5. **Piper sits upstream of execution tools.** Jira manages the atoms of work. Piper clarifies the *why*, shapes the roadmap, and determines MVP scope. We're not competing with task management — we're occupying the space above it.

---

## The Problem (Unchanged, Better Understood)

Product managers spend 40-60% of their time on routine knowledge management. The founding vision named this correctly. What we understand better now:

- The problem isn't just time spent on mechanics — it's **context fragmentation**. PMs carry the "why" in their heads because no tool captures it structurally.
- Execution tools (Jira, Linear, Asana) are excellent repositories for the *output* of PM thinking but don't support the *process* of PM thinking.
- The discovery problem is real: features that work technically but can't be found by users deliver zero value. (Pattern-045: Green Tests, Red User)

## The Vision: Colleague, Not Tool

Piper Morgan is an AI-powered PM colleague that inhabits your existing workspace — Slack, email, IDE, meetings — and helps with the upstream product work that execution tools don't address.

### What Piper Does

- **Articulates the "why"** — Helps PMs clarify rationale, strategy, and narrative behind work
- **Shapes roadmaps** — Coherent narrative over time, not just a list of features
- **Clarifies MVP scope** — What's in, what's out, and why
- **Synthesizes context** — Morning standups, meeting prep, cross-project awareness
- **Federates to execution tools** — GitHub, Notion, Slack, Calendar for the atoms of work

### What Piper Is Not

- Not a destination you go to (Radar O'Reilly pattern — companion, not portal)
- Not a form to fill out
- Not a dashboard to check
- Not a command interface
- Not a replacement for PM judgment

### The Colleague Test

Would this interaction feel appropriate from a thoughtful colleague who's been working with you for a few weeks? If Piper sounds like a help desk, warm it up. If it sounds like a personal essay, dial it back. This test is a release gate (B1 quality threshold).

---

## Three Horizons (Revised)

The founding vision's three-phase model was directionally right but optimistic on timeline. Here's what we've learned:

### Horizon 1: Conversational Glue (Shipped — v0.8.6, March 2026)

**What it is**: Piper is always at least as good as a well-prompted LLM with the user's context. Structured handlers make specific workflows better, but the conversational floor handles everything else gracefully.

**What shipped**:
- Floor-first routing architecture (ADR-060) — everything routes to conversation by default; handlers activate only for side effects
- 19 intent categories with classifier
- 7 integration plugins (Slack, GitHub, Notion, Calendar, MCP, Spatial, Demo)
- Trust-graduated proactivity (ADR-053) — Piper earns the right to be proactive through demonstrated value
- Cross-session memory architecture (ADR-054) — three-layer context persistence
- 6,300+ tests passing

**What we learned building it**:
- Assembly Assumption: individually correct components don't automatically compose into correct composition (M0 expanded from 5 planned issues to 27)
- Discovery is the bottleneck: 19 working intent categories, but users couldn't find them
- "The session belongs to the user" — never trap users in processes they didn't choose (PDR-004)

### Horizon 2: MVP Foundation → Activation (Current — 2026)

**What it is**: The foundation that makes Piper useful to real users, not just the development team. Skills, document intelligence, polish, and distribution.

**Current position**: M1 (Foundation) at gate verification. M2-M5 planned through May 2026. Distribution (DIST) planned June-July.

**What's being built**:
- M1: Security hardening, E2E testing, automated conversation quality verification
- M2: MVP activation — wiring, lifecycle UI, trust-gated features
- M3: Skills library — canonical queries, multi-agent coordination, design system
- M4: Document intelligence — processing, browsing, artifact persistence
- M5: Polish and hardening — auth, migration, performance

**Distribution strategy**: MCP-native packaging (MCPB format) for Claude Desktop, with potential Cowork plugin for non-technical PM users. Registry publication for ecosystem discovery.

**What the PA experiment is teaching us**: Some of what we planned as structured infrastructure may be better served by conversational intelligence with good context management. PA handles standup synthesis, issue triage, memo drafting, and cross-project awareness conversationally — suggesting the LLM floor is higher than we assumed. The *ceiling moments* (session continuity, real-time peer visibility, behavioral learning) are where structured infrastructure earns its keep.

### Horizon 3: Analytical Partnership (2027+)

**What it is**: Piper as a genuine analytical partner — proactive insights, cross-project synthesis, predictive PM.

**What we believe now vs. June 2025**:
- The founding vision assumed heavy structured infrastructure would be needed for Phase 2 capabilities. The PA experiment suggests some of these capabilities emerge from the LLM floor with sufficient context, while others genuinely require structured systems.
- Cross-project synthesis may be more achievable than we thought — the cross-pollination brief system demonstrates automated multi-project insight extraction today, conversationally.
- Predictive capabilities (timeline estimation, risk identification) are further out than the founding vision assumed. They require data accumulation that only comes from sustained production usage.
- The learning loop remains the hardest unsolved problem. User preferences are database-backed but static. Behavioral calibration (Layer 5 in the five-layer model) doesn't transfer or accumulate across sessions.

**Not yet planned in detail** — and that's intentional. Horizon 3 should be shaped by what we learn from Horizon 2 production usage, not by speculation.

---

## Architectural Principles (Evolved)

### 1. The LLM Is the Floor, Not the Ceiling

Every user interaction must be at least as good as a well-prompted LLM with the user's context. Structured handlers make specific workflows *better* — faster, more reliable, with side effects — but the conversational floor handles everything else. This means Piper never says "I can't do that" for a question a thoughtful colleague could answer.

*Origin: ADR-060, March 2026. Born from the "Are We Doing It Backwards?" roundtable where four leadership roles independently diagnosed the same problem.*

### 2. Entities Experience Moments in Places

The constitutional grammar of the object model. Every feature decision is evaluated against it. "Would 'BLOCKED insight' make sense?" reveals a category error — insights are composted output, not entities. The grammar prevents elegant-but-wrong symmetry.

Four substrates: Entities (actors with agency), Places (contexts where action happens), Moments (bounded significant occurrences), Situations (the encompassing frame — not a fourth substrate).

Three ownership modes: Native (Piper's Mind — sessions, memories, concerns), Federated (Piper's Senses — GitHub issues, Slack messages), Synthetic (Piper's Understanding — assembled projects, inferred risks).

*Origin: ADR-045, November 2025. Discovered through hand sketching with fat markers, not AI tools.*

### 3. Domain-First Architecture

Product management concepts drive technical decisions. The system understands PM work at a conceptual level. This principle is unchanged from the founding vision and has proven correct through every architectural decision since.

### 4. Completion Over Velocity

The Inchworm Protocol: complete each phase 100% before advancing. No exceptions, no parallel work on incomplete phases. This emerged from the September 2025 ALL STOP when 75% complete implementations were found throughout the codebase, each creating cascading failures.

The Pledge: "Finish what we start. Test what we build. Lock what we fix. Document what we do. Verify what we claim."

### 5. Trust Is Earned, Not Configured

Piper's proactivity is graduated through demonstrated value (ADR-053):
- Stage 1 (New): Respond to queries only
- Stage 2 (Building): Offer related capabilities after task completion
- Stage 3 (Established): Proactive suggestions based on context
- Stage 4 (Trusted): Anticipate needs

Trust is invisible to users but its effects are noticeable. Users don't see "Trust Level: Established" — they experience Piper getting more helpful over time.

### 6. Vendor Flexibility (Revised)

The founding vision emphasized vendor independence as a critical architectural requirement. The current reality: development is Claude-optimized, and the MCP distribution strategy is Claude Desktop-native. The adapter pattern exists but multi-provider optimization is not actively pursued.

**Honest assessment**: This is a pragmatic tradeoff, not an architectural failure. The Claude ecosystem (Code, Cowork, MCP, Desktop) provides capabilities that would be expensive to replicate provider-agnostically. The adapter interfaces remain in place for future flexibility, but the near-term path is Claude-native. If this changes, the architecture supports it — but we're not pretending it's a current priority.

---

## The Methodology as Product

One of the founding vision's blind spots: it described the *product* without describing the *process that builds the product*. Ten months later, the methodology is itself a product-level asset:

- **Excellence Flywheel**: Foundation-first → Systematic Verification → Multi-Agent Coordination → Accelerated Delivery → compound investment
- **Completion Discipline Triad**: Green Tests Red User (Pattern-045), Beads (046), Time Lord Alert (047)
- **Multi-Agent Coordination**: 14 roles, async memo-based communication, roundtable synthesis for high-stakes decisions
- **Building in Public**: 260+ blog posts documenting every breakthrough and setback; the methodology is the marketing

The IA Conference talk (April 17, 2026: "Ethics as Information Architecture") positions this explicitly: AI ethics is an architecture problem, not a policy problem. Build a road that doesn't go near the cliff.

---

## Success Looks Like

### For Individual PMs (Horizon 2)

A PM asks Piper, in Slack or the web UI, to help clarify the rationale for an initiative. Piper draws on connected integrations (GitHub issues, Notion pages, calendar) and responds in natural language. The PM spends 5 minutes refining rather than 30 minutes drafting from scratch. Over time, Piper learns the PM's preferred standup format, focus areas, and communication style — and applies them without being asked.

### For PM Teams (Horizon 3)

The team's quarterly planning includes Piper synthesizing cross-project signals, surfacing patterns from the past quarter's retrospectives, and identifying capability gaps that emerge from the data rather than from individual memory. The PM still makes the call — but the call is informed by systematically assembled context rather than selective recall.

### For the Practice of PM

Piper Morgan demonstrates that AI product development can be thoughtful, transparent, and humane. The methodology is transferable. The building-in-public narrative serves as both documentation and proof that ethical architecture produces better systems, not constrained ones.

---

## What Remains True from June 2025

The founding vision got these things right:

- **The problem statement**: Context fragmentation and knowledge management overhead are real
- **The three-phase trajectory**: Task automation → analytical intelligence → strategic partnership
- **Domain-first architecture**: PM concepts drive technical decisions
- **Knowledge amplification over replacement**: Augment human judgment, don't substitute for it
- **Ethical AI partnership**: Transparency, human oversight, clear boundaries

## What the Founding Vision Didn't Know

- That velocity without completion discipline produces invisible infrastructure and inflated claims
- That the LLM floor would be high enough to handle most conversational PM work without structured handlers
- That the object model would emerge from hand sketching, not AI-assisted design
- That a 14-agent team coordinated through async memos would work as well as it does
- That building the process of building the product would be as valuable as building the product itself
- That the Phase 2 timeline was optimistic by roughly 12-18 months
- That distribution through MCP would become the obvious path

---

*Draft v2.0 — March 31, 2026*
*Prepared by: Piper Alpha, drawing on the full project arc (May 2025 – March 2026)*
*For PM review before leadership circulation*

## Revision Log

- **June 21, 2025**: Founding vision (v1.0) — three-phase evolution, architectural principles, success scenarios
- **March 31, 2026**: Draft v2.0 — incorporates ALL STOP, Inchworm Protocol, object model, floor-first routing, PA experiment findings, distribution strategy, methodology-as-product framing. Preserves founding values; updates timeline and architectural assumptions.
