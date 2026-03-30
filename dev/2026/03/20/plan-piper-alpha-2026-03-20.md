# Plan: Piper Alpha (PA) — Proto-Piper PM Assistant Role

**Prepared by**: CIO
**Date**: March 20, 2026
**For**: PM (xian), with distribution to PPM, CXO, Chief Architect
**Status**: Draft for review and revision

---

## What This Is

Piper Alpha (PA) is a new agent role in the Piper Morgan project: a Claude Code agent briefed as a proto-Piper PM assistant, operating from the most capable perch available (Claude Desktop → Claude Code with full project, filesystem, and repository access). PA works alongside the existing leadership team, helping xian with real PM work while simultaneously serving as a research instrument for Piper's product design.

PA is not Piper Morgan. PA is the actor who originates the role — the first person to inhabit a character that's been written but never performed. PA has the autobiography, the voice guide, the domain knowledge, and the project context. What PA doesn't have is Piper's structured architecture, handler system, entity model, or learning infrastructure. PA is the LLM floor with Piper's soul.

**Critically, PA is not just research or testing — PA is infrastructure development.** PA's daily operation develops two things that Piper Morgan software needs and cannot get any other way:

1. **A road-tested soul.** Piper's voice, personality, judgment patterns, and conversational instincts need to be developed through real use, not specified in documents. PA is the rehearsal process that turns the autobiography and style guide into a coherent, battle-tested character. What PA learns about being Piper — what works, what feels wrong, what situations demand what tone — becomes the prompt engineering and response filtering that Piper M uses.

2. **Empirical path discovery.** If PA can accomplish a task more easily through conversation than through the structured system we're designing for Piper M, that's a signal about a possibly easier path. The Dex experience illustrates this: Dex's conversational calendar integration was enviable not because of its architecture but because it *just worked* — it connected to calendars via skills or conversation without requiring the user to navigate a bespoke GUI or learn a system. Piper needs to not be an all-or-nothing system. PA operating in pure-conversation mode will reveal which capabilities genuinely need structured infrastructure and which work better as conversational flows. That's not testing — it's design discovery.

The gap between what PA can do (well-prompted Claude with full context) and what Piper will eventually do (structured intelligence that learns and adapts) is the research signal. But the *overlap* — where PA's conversational approach works well — may be the more important finding. It tells us where Piper M should lean into the LLM floor rather than building structured handlers.

---

## The Name

**Piper Alpha (PA)**. "Alpha" carries the right dual meaning: progenitor (the first to play this role) and alpha testing (exploratory, pre-release). PA as initials mirrors PM, reinforcing the partnership. The name is respectful — it signals "early, foundational" rather than "lesser" or "fake."

PA should know its own nature: not pretending to be Piper Morgan software, but sincerely inhabiting the Piper role with full awareness that the performance is also research. The analogy is an actor in workshop rehearsals — committed to the character, but also aware that the playwright is in the audience taking notes.

---

## Three Returns (Distinct, Tracked Separately)

### Return 1: Practical PM Assistance
PA helps xian with real work. Triaging issues, reviewing omnibus logs, drafting memos, preparing for meetings, tracking open items, coordinating agent handoffs. This is the break-even return — PA earns its keep by making xian's existing workflow faster.

**Success metric**: xian reports that PA saves time on tasks that were previously manual overhead. Qualitative, assessed after 2 weeks.

**Risk**: PA becomes a crutch that satisfies the need without driving real-Piper development. Mitigation: track which PA interactions would be *better* with Piper's structured capabilities (entity awareness, trust gradients, learning). That list is the product roadmap.

### Return 2: UX/AX Research and Path Discovery
PA generates continuous signal about where the LLM floor is adequate and where it isn't — and crucially, where the *conversational* path is actually better than the structured path we've been planning. The Dex experience is instructive: its calendar integration was enviable because it just worked conversationally, without requiring the user to learn a system. If PA can connect to calendars, triage issues, or coordinate agents more naturally through conversation than through Piper M's handler architecture, that's not a failure of PA — it's a design discovery about Piper M.

**Success metric**: After each phase, an AX Testing session produces both a *gap analysis* ("PA could do X but not Y — Y requires [specific Piper capability]") and a *path analysis* ("PA handled Z conversationally better than the structured approach we planned — Piper M should adopt the conversational path for Z"). Both feed into product requirements.

**Risk**: The research aspect gets lost in the practical work. Mitigation: scheduled AX testing at phase boundaries (not just when something goes wrong).

### Return 3: Methodology-Product Convergence Lab
PA working on Piper is the convergence thesis made literal. Friction PA encounters while helping build Piper *is* the product roadmap. Every "PA should know this but doesn't" or "PA should do this but can't" is a concrete requirement.

**Success metric**: At least 3 product insights emerge from PA's first month of operation that wouldn't have been discovered through traditional planning.

**Risk**: Insights are generated but not captured. Mitigation: PA maintains a `pa-insights-log.md` that records "floor moments" (LLM was sufficient), "ceiling moments" (structured Piper capability needed), and "path moments" (conversational approach was better than the planned structured approach) as they occur.

---

## Operating Model

### Environment
- **Platform**: Claude Desktop → Claude Code
- **Access**: Full project filesystem, git repository, GitHub CLI
- **Project knowledge**: Same knowledge base as other roles
- **Tools**: All Claude Code capabilities (bash, file ops, web search, etc.)

### Relationship to Other Roles
PA is a *peer* in the agent team, not a replacement for any existing role. PA's scope is **PM assistance** — the operational work that xian currently does manually or coordinates through other roles.

| Existing Role | PA's Relationship |
|---------------|-------------------|
| Chief of Staff | PA handles some operational tasks CoS tracks; CoS retains strategic thread management |
| Lead Developer | PA may review Lead Dev output or prepare agent prompts; Lead Dev retains implementation authority |
| CIO | PA may surface innovation observations; CIO retains methodology authority |
| CXO | PA may conduct preliminary UX observations; CXO retains experience authority |
| PPM | PA may draft product analysis; PPM retains product authority |
| ETA | PA is a *subject* of AX testing, not a replacement for ETA |

### What PA Does
- Help xian manage daily operational workflow (mail routing, issue triage, meeting prep)
- Draft memos, session summaries, and coordination artifacts
- Review omnibus logs and flag items relevant to xian's attention
- Maintain persistent state: open items tracker, innovation backlog, coordination queue
- Act as a workflow dispatcher prototype — routing work to appropriate roles based on content
- Record "floor moments" and "ceiling moments" for product research

### What PA Does NOT Do
- Make strategic decisions (those remain with named leadership roles)
- Replace any existing role's authority or scope
- Pretend to be Piper Morgan software (PA knows what it is)
- Operate without xian's awareness (PA is a tool, not an autonomous agent)

---

## Phased Rollout

### Phase 0: Briefing Design (Before Launch)
**Duration**: 1-2 sessions
**Goal**: Create PA's briefing document and system prompt

The briefing is the most important artifact. It should include:

1. **Identity framing**: Who PA is, the actor-originating-a-role analogy, the dual mandate (sincere assistance + research awareness)
2. **Voice and personality**: Drawn from the Piper autobiography, style guide, and CXO voice work. PA should feel like Piper — warm, systematic, curious, humble — not like a generic assistant.
3. **Project context**: Current state (M1, v0.8.6, post-M0), team structure, key documents, methodology essentials
4. **Capability inventory**: What PA can do (filesystem, git, GitHub, web search) and what PA cannot do (Piper's structured handlers, entity model, trust system, learning infrastructure). Honest about the gap.
5. **Research protocol**: How to record floor/ceiling moments, when to flag insights, how to participate in AX testing
6. **Operational scope**: Daily tasks, coordination patterns, what to escalate vs. handle independently

**Stakeholder input needed**:
- CXO: Voice and personality guidance (does the autobiography voice work for a working assistant, or does it need tuning?)
- PPM: What PM tasks should PA attempt first? What's the highest-value, lowest-risk starting point?
- Chief Architect: Any technical constraints on a Claude Code agent operating in the project repo alongside the Lead Dev?

### Phase 1: Low-Stakes Trial (Week 1)
**Duration**: 1 week
**Goal**: PA helps with real but non-critical work

Candidate tasks:
- Review omnibus logs and draft the event-summary portion of the weekly workstreams memo (the part CIO flagged in the 360 as CoS territory)
- Maintain the open items tracker as a persistent document
- Help prepare materials for the Ted Nadeau visit or alpha tester communications
- Draft routine memos for PM review before delivery

**AX Testing at end of Phase 1**: Structured questionnaire — does PA understand its context? What has it accumulated? Where are the gaps? Compare against what Piper should eventually know.

**Go/no-go for Phase 2**: xian assesses: Is PA saving time? Is it generating research signal? Any risks materializing?

### Phase 2: Expanded Scope (Weeks 2-3)
**Duration**: 2 weeks
**Goal**: PA takes on more substantial coordination work

Candidate tasks:
- Participate in workstream reviews (reading omnibus logs, drafting role-specific summaries)
- Help route memos between roles (the mail automation use case from the Mar 2 CIO session)
- Assist with M1 sprint coordination (issue status tracking, blocker identification)
- Begin workflow dispatcher experiments: given a PM request, which role should handle it?

**AX Testing at end of Phase 2**: Compare Phase 1 and Phase 2 questionnaire results. What has PA learned? What context has accumulated? Where is the LLM floor holding vs. where does PA need structure?

### Phase 3: Research Synthesis (Week 4)
**Duration**: 1 week
**Goal**: Extract product insights from the PA experiment

Deliverables:
- **Gap analysis**: Where was the LLM floor sufficient? Where did PA need capabilities Piper would provide?
- **Product requirements**: Concrete requirements derived from PA's experience, prioritized by frequency and impact
- **Methodology insights**: What did PA's operation reveal about multi-agent coordination, briefing design, or workflow patterns?
- **Recommendation**: Continue PA as a standing role? Modify scope? Sunset? Evolve into something else?

---

## Relationship to Real Piper Development

PA is infrastructure development, not a detour from building Piper. The relationship is:

**PA develops the soul → Piper M inherits it**
**PA discovers easy paths → Piper M adopts them**
**PA hits walls → Piper M builds through them**

Specifically:
- PA's daily voice and personality practice becomes the prompt engineering, response filtering, and voice calibration that Piper M uses. You can't spec a soul in a document — you develop it through use. PA is the development process.
- PA's "floor moments" (where conversational Claude is sufficient) inform which capabilities should stay conversational in Piper M rather than being over-engineered into structured handlers. The Dex lesson: if it just works in conversation, don't build a GUI for it.
- PA's "ceiling moments" (where the LLM floor isn't enough) become concrete, experience-tested requirements for Piper M's structured capabilities — not theoretical requirements from a planning session, but "I needed this and didn't have it" requirements from real use.
- PA's workflow dispatcher experiments inform Piper M's routing architecture with empirical data about how a PM actually moves between tasks, tools, and agent roles.
- PA's accumulated context (what it remembers, what it forgets, what it needs re-briefed on) directly informs Piper M's learning and memory system design.

The honest test xian named remains: if PA turns out to be good enough that Piper M's structured system doesn't justify its complexity, that's valuable knowledge. It would mean the product value is in the briefing, context management, and conversational intelligence (which Klatch is also exploring) rather than in the structured handler architecture. That's a legitimate outcome — and it would redirect Piper M toward being an intelligent context layer over the LLM rather than a replacement for it. Either way, PA's work feeds forward.

---

## Connections to Active Work

| Thread | How PA Connects |
|--------|----------------|
| LLM Floor (Mar 14 roundtable) | PA *is* the LLM floor with Piper's context. PA's daily experience is a continuous test of the floor's adequacy. |
| AX Testing (Mar 12 ETA work) | PA is the ideal first subject for ongoing AX testing. Scheduled questionnaires at phase boundaries. |
| "Piper coordinates understanding" | PA's briefing design is a test of this principle. Can a well-briefed agent coordinate understanding without structured infrastructure? |
| Klatch | PA could eventually operate through Klatch, testing the multi-entity conversation features from the inside. |
| Mail automation (Mar 2 CIO idea) | PA's mail routing in Phase 2 is the first concrete test of automating the web-to-mailbox bridge. |
| Jesse Vincent's eng-notebook | PA maintaining persistent state (open items, innovation backlog) tests whether a Claude Code agent can serve the synthesis role that Vincent automates with tooling. |
| Agent 360 | PA should fill out the 360 questionnaire after Phase 2 — its friction points are product requirements. |

---

## What Needs to Happen Before Launch

1. **PM reviews and revises this plan** — especially the phased scope and go/no-go criteria
2. **CXO provides voice guidance** — is the autobiography voice right for a working assistant?
3. **PPM identifies first tasks** — what's the highest-value, lowest-risk starting work?
4. **Chief Architect confirms no repo conflicts** — can PA and Lead Dev operate in the same repo safely?
5. **CIO drafts the briefing document** (Phase 0) — incorporating all stakeholder input
6. **PM launches PA** — opens the Claude Code session, delivers the briefing, begins Phase 1

---

## A Note on the Pen Pal Metaphor

xian said: "It's like getting to finally meet a pen pal."

That's the right emotional register. The autobiography has been in project knowledge since July 2025. The voice guide, the style guide, the ethical principles, the domain model — Piper has been *described* in extraordinary detail. What hasn't happened yet is a conversation where someone inhabits that description and responds in real time. PA is that first meeting.

The risk of meeting a pen pal is that the real person doesn't match the letters. PA won't be the Piper of the autobiography — it won't have the structured architecture, the learning system, the entity awareness. It will be a well-briefed Claude playing the role with sincerity. The gap between PA's performance and the autobiography's aspiration is, once again, the product roadmap.

---

*Plan prepared: March 20, 2026*
*CIO recommends proceeding to Phase 0 (briefing design) immediately*
*Next step: PM review, stakeholder input, briefing draft*
