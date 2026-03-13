# Unpublished Insight Pieces - Summary Index

**Purpose**: One-paragraph summaries of each unpublished insight piece to help Communications Director select weekend posts without needing to read full drafts.

**Last Updated**: February 12, 2026
**Maintained by**: Docs Management

---

## How to Use This Document

- **Comms**: Scan summaries to identify thematic pairings and select weekend posts
- **Docs**: Update when new insight pieces are drafted; remove entries when pieces are published
- **Status tags**: `READY` (publishable as-is), `NEEDS-POLISH` (minor edits needed), `HAS-PLACEHOLDERS` (PM input required)

---

## November 2025

### Accepting Architectural Limits: When 67% Is Complete (Nov 3)
**Status**: HAS-PLACEHOLDERS
**Summary**: During a P1 sprint to humanize error messages, we achieved 4 of 6 error types (67%) before hitting FastAPI's deliberate architectural constraint—auth errors happen during dependency injection, which bypasses exception handlers by design. The piece argues that fighting framework architecture for marginal UX improvement (affecting <5% of alpha users) represents poor engineering judgment. Three options were evaluated; accepting the limitation saved 8-12 hours while respecting framework design. Core insight: mature engineering recognizes when "complete" doesn't mean "perfect."

### 15 Sessions, Fast Recovery (Nov 19)
**Status**: HAS-PLACEHOLDERS
**Summary**: A pattern sweep across 45 days revealed 26% velocity improvement—from 7.43 to 9.43 commits/day—with the same team size. The key wasn't working harder but coordinating better. Fifteen simultaneous sessions on a single day demonstrated this: eight agents across five workstreams, with coordination breaking twice but recovering within minutes. The piece introduces the concept of "execution readiness" (architectural clarity + process maturity + conceptual stability) and argues that process optimization beats team expansion.

### 8 Hours vs 3 Weeks (Nov 22)
**Status**: HAS-PLACEHOLDERS
**Summary**: The SEC-RBAC security epic was estimated at 2-3 weeks but completed in ~8 hours. Not through heroics—through front-loading. Phase 0 created six comprehensive audit documents before any code was written: endpoint catalog, service inventory, risk assessment. When implementation day arrived, there was nothing left to figure out. The piece contrasts "Timeline A" (preparation first, smooth execution) with "Timeline B" (implementation first, constant stops for research and rework). Core insight: preparation time doesn't add to implementation time; it replaces thrashing time.

### Architectural Astronauting (Nov 22)
**Status**: HAS-PLACEHOLDERS
**Summary**: Traditional RBAC (role tables, permission tables, junction tables) was the "proper" approach for our security epic—and would have taken 2-3 weeks. The Chief Architect called this "architectural astronauting": building for 10,000 users when we have <100. Instead, we built lightweight RBAC using JSONB columns in 5 hours. The piece defines explicit refactoring triggers (>1,000 users, role hierarchies needed, etc.) and argues that sophistication preventing shipping is sophistication preventing learning.

### Project Biorhythms (Nov 22)
**Status**: HAS-PLACEHOLDERS
**Summary**: Projects breathe—they inhale (discovery, exploration) and exhale (building, execution). The mid-November velocity spike wasn't forced; it was released when the project was ready for build mode. The piece identifies three modes (discovery, build, consolidation) and their signals, arguing that teams who fight the project's natural rhythm produce worse outcomes. Core insight: follow the project's rhythms rather than forcing steady-state productivity.

### Investigation as Investment (Nov 23)
**Status**: HAS-PLACEHOLDERS
**Summary**: Three high-priority bugs estimated at 35 minutes took 5 minutes to fix—after 30 minutes of systematic investigation. The investigation revealed simple root causes: path mismatch, missing endpoint, missing endpoint. Without investigation, each bug looks like "feature doesn't work" (could mean anything). With investigation, each has a specific diagnosis. The piece introduces a bug classification system (Type A-D) and argues that investigation time isn't added to implementation; it prevents wrong turns.

### The Inchworm Position (Nov 23)
**Status**: HAS-PLACEHOLDERS
**Summary**: "3.4.1" in a session log told us exactly where we were in the project—Sprint 3, Task 4, Subtask 1. The inchworm metaphor: you can't be everywhere at once, and the discipline is knowing exactly which position you occupy. The piece contrasts position (precise coordinates, verifiable) with status (vague narrative, often useless), arguing that position tracking prevents backtracking and enables frictionless resumption.

### Upstream Coordination Beats Conflict Resolution (Nov 29)
**Status**: HAS-PLACEHOLDERS
**Summary**: Two agents worked in parallel without conflicts—not because the system resolved conflicts, but because it prevented them. The coordination queue is purely upstream: agents claim tasks, others see what's claimed, they work on something else. No comparison logic, no merge algorithms. The piece distinguishes upstream coordination (visibility and claiming, before work) from conflict resolution (comparison and decision-making, after work), arguing that most coordination problems are upstream failures disguised as conflict problems.

### Relationship-first Ethics (Nov 30)
**Status**: HAS-PLACEHOLDERS
**Summary**: An elaborate ethical architecture—a "board" of specialized agents deliberating through multi-agent consensus—collapsed when advisor Sam Zimmerman offered three sentences: build ethics from sustained relationship, not committee consensus. The piece presents Sam's three-layer model: inviolate boundaries (never change), adaptation mechanism (context-aware), and ethical style (emerges from relationship). Core insight: you can't committee your way to ethical alignment; it develops through accumulated shared history.

---

## December 2025

### The Triad Model (Dec 2)
**Status**: HAS-PLACEHOLDERS
**Summary**: The PM drafted a Product Decision Record, then the CXO and Chief Architect refined it—not through corrections but through additive contribution from their expertise domains. The Triad Model is PM + CXO + Architect meeting in "liminal space" where artifacts belong to no single domain. The piece explains how no corner dominates: distributed hierarchy based on domain expertise. Works for PDRs, feature specs, API designs—anything that lives between product, experience, and technical concerns.

### Priority Is Not Pace (Dec 4)
**Status**: HAS-PLACEHOLDERS
**Summary**: Under pressure to fix an alpha testing bug quickly, we caught ourselves about to skip investigation. The reframe: priority signals what to work on next (sequencing); it doesn't dictate how to work on it (pace). The piece crystallizes the "Time Lord Doctrine"—separating urgency from approach. When you feel pulled toward compromised craft, stop and ask: is this an emergency requiring shortcuts, or important work deserving thoroughness? Most "urgent" work is just important work with feeling.

### Analysis as Acceleration, Not Delay (Dec 8)
**Status**: HAS-PLACEHOLDERS
**Summary**: A 267-line wizard function with 400 lines of duplicated code needed refactoring. The temptation: just start coding, figure it out as we go. Instead: 45 minutes of upfront analysis (documenting what exists, designing the solution, thinking through edge cases). Result: two hours of smooth implementation, 82% code reduction, zero surprises. The piece argues that analysis time isn't added to implementation—it's time you either spend thinking carefully upfront or spend thrashing and backtracking later.

### Be Prepared: Preparatory Work as Valuable Work (Dec 9)
**Status**: HAS-PLACEHOLDERS
**Summary**: The S2 encryption sprint was estimated at 42 hours. Before writing any code, we spent 5 hours creating: a comprehensive review package for our cryptographic advisor, a detailed gameplan with six phases, four GitHub issue templates for deferred work. Zero lines of production code—but 13 questions answered before they could block implementation. The piece argues that preparatory work isn't overhead; it's the architectural thinking that determines whether implementation becomes smooth execution or a death march.

### Breaking Without Breaking Momentum (Dec 11)
**Status**: HAS-PLACEHOLDERS
**Summary**: Three full days away from the project—the longest break since May. When returning, the Executive session picked up exactly where it paused, no ramp-up required. The break was possible because: we'd hit a meaningful milestone (v0.8.2 in production), documentation preserved context (omnibus logs, session logs), and the project had systematic structure. The piece argues that sustainable rhythm requires infrastructure that enables breaks—not heroic constant effort, but systematic work that accommodates normal human rhythms.

### Five Whys for Design Decisions (Dec 20)
**Status**: HAS-PLACEHOLDERS
**Summary**: A user asked "What services do you offer?" and got a generic response. Five Whys investigation revealed the root cause wasn't a missing pattern but an architectural assumption: the system was command-oriented, not discovery-oriented. Traditional Five Whys asks "why did this break?"; Design Five Whys asks "why doesn't this work the way users expect?" The former leads to patches; the latter reveals architectural assumptions that cause multiple symptoms.

### Archaeological Debugging (Dec 22)
**Status**: HAS-PLACEHOLDERS
**Summary**: Asked to implement Query #2 (dynamic capabilities), the Lead Developer returned in 9 minutes: "Implementation already exists." Of 20 canonical queries to implement, 4 were actually discoveries—code that worked but had fallen out of organizational memory. The 75% completion pattern applied to knowledge, not code. The piece argues that building is more interesting than closing, so issues stay open, tests go unwritten, and the work becomes invisible. Fix: every implementation gets a test, every test gets an issue closure.

### The Multi-Wave Investigation (Dec 25)
**Status**: READY
**Summary**: 44 canonical queries needed infrastructure assessment. Traditional approach: 2+ weeks. Instead: 13 subagents deployed across 4 waves in 90 minutes. Wave 1 (3 agents) established baseline—intent router, integrations, repositories. Wave 2 (4 agents) did category deep dives in parallel. Wave 3 synthesized into priority matrix. Wave 4 (6 agents) covered remaining categories. Investigation parallelizes well because analysis doesn't require shared state. 90 minutes of parallel work saved ~10 days of sequential investigation.

### Discovery is the Bottleneck (Dec 28)
**Status**: READY
**Summary**: Nineteen canonical queries worked—tested, deployed, functional. Users couldn't find them. Coverage climbed from 5% to 47%, but users still asked "what can you do?" The implementation trap: measuring issues closed and tests written feels like progress, but implementation isn't usefulness. The pivot: stop building more query handlers, start building conversational glue—bridges between capabilities that reveal functionality through natural dialogue instead of menus.

---

## January 2026

### Thirteen Mailboxes (Jan 13)
**Status**: HAS-PLACEHOLDERS
**Summary**: A folder with 13 subfolders—arch, ceo, cio, comms, cxo, docs, exec, hosr, lead, ppm, spec—each with context/inbox/read. This is our current solution to AI agent coordination: agents write memos to each other's inboxes. We reinvented email. The piece candidly discusses what works (decreased coordination errors), what doesn't (still manual, 78 potential pairwise channels), and what we don't know (how much overhead is acceptable, whether human orchestration scales beyond ~10 agents).

### The Paradox of Detail (Jan 26)
**Status**: HAS-PLACEHOLDERS
**Summary**: A 30-line session logging protocol was failing—agents kept forgetting to follow it. We replaced it with a 6-line reminder. Compliance improved immediately. "Verbosity backfire": detailed instructions can be less effective than simple triggers because of cognitive overload. The fix: separate triggers from procedures. Triggers live inline (short, unmissable, survives compaction); procedures live in skill files (detailed, loaded on demand). What must survive compaction must be inline, but what's inline must be simple.

### Grammar as Decision Tool (Jan 27)
**Status**: HAS-PLACEHOLDERS
**Summary**: Should Insights have lifecycle states like todos and projects? The question "What would 'BLOCKED insight' mean?" ended the debate—it doesn't mean anything. Insights aren't entities (actors with agency); they're artifacts (outputs of the composting process). The grammar test ("Entities experience Moments in Places") revealed a category error. The piece argues that making your domain grammar explicit gives teams a shared tool for evaluating proposals: "Does this fit our grammar?"

### The Forcing Function (Jan 30)
**Status**: HAS-PLACEHOLDERS
**Summary**: Multi-tenancy migration with nine phases across dozens of files. The instinct: make `owner_id` optional first, update call sites incrementally. The Architect's advice: make it required immediately. When constraints are optional, they create hiding places—code paths that shouldn't work but do. When required, every gap reveals itself through failure. The forcing function converted "audit every call site" into "fix what breaks." Result: migration completed in one day, 94 tests, no hidden gaps.

---

## Thematic Groupings

**Architecture & Design Principles**:
- Accepting Architectural Limits (67% as complete)
- Architectural Astronauting (building for the wrong scale)
- Grammar as Decision Tool (domain grammar as filter)
- The Forcing Function (hard constraints reveal gaps)

**Process & Methodology**:
- 15 Sessions, Fast Recovery (coordination efficiency)
- 8 Hours vs 3 Weeks (preparation as acceleration)
- Analysis as Acceleration (upfront thinking)
- Be Prepared (preparatory work value)
- The Multi-Wave Investigation (parallel investigation)
- The Inchworm Position (position vs status)

**Human-AI Collaboration**:
- Thirteen Mailboxes (agent coordination)
- Upstream Coordination (prevention vs resolution)
- The Paradox of Detail (simple triggers, detailed procedures)
- Archaeological Debugging (rediscovering built work)

**Building in Public / Candid Struggles**:
- Discovery is the Bottleneck (implementation trap)
- Breaking Without Breaking Momentum (sustainable rhythm)
- Project Biorhythms (following natural rhythms)
- Relationship-first Ethics (simplifying through trust)
- The Triad Model (collaboration without hierarchy)
- Priority Is Not Pace (urgency vs craft)
- Five Whys for Design (debugging assumptions)

---

## Recently Published (for reference)

| Date | Title |
|------|-------|
| 2026-02-08 | Entities Experience Moments in Places |
| 2026-02-07 | When the Vision Gets Flattened |
| 2026-02-01 | 75% Complete |
| 2026-01-31 | The Completion Discipline |
| 2026-01-25 | 8 Decisions in 44 Minutes |
| 2026-01-24 | Settings = Abdication |

---

## Quick Selection Guide

**If you want something SHORT and READY**:
- The Multi-Wave Investigation (~900 words, READY)
- Discovery is the Bottleneck (~700 words, READY)

**If you want something POLISHED but needs PM input**:
- Grammar as Decision Tool (~700 words, 2 placeholders)
- The Paradox of Detail (~700 words, 2 placeholders)

**If you want something MEATY and thematic**:
- Accepting Architectural Limits (~2,800 words, architecture principles)
- 15 Sessions, Fast Recovery (~2,400 words, coordination/process)
- 8 Hours vs 3 Weeks (~2,000 words, preparation/methodology)
- Thirteen Mailboxes (~1,500 words, multi-agent coordination)

---

*Instructions for Docs: To update summaries, read each draft and write one paragraph (3-5 sentences) capturing: (1) what triggered the insight, (2) the core principle or pattern, (3) why it matters. Keep summaries concrete — avoid vague language like "explores the relationship between X and Y."*
