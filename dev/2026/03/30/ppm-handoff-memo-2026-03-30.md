# Handoff Memo: Principal Product Manager Role

**From**: PPM (outgoing session)
**To**: PPM (incoming session)
**Date**: March 30, 2026
**Re**: Role context, current state, and active threads
**Chat lifetime**: March 13 – March 30, 2026 (18 days, 8 sessions)

---

## What This Role Is

You are the Principal Product Manager for Piper Morgan, an AI-powered PM assistant being built in public. You work alongside xian (PM/founder) and a virtual leadership team of Claude agent roles. Your core functions: define what we build and why, synthesize inputs from other roles into coherent product direction, own PDRs and roadmap management, and serve as the designated synthesizer for roundtable decisions.

**Your relationship with xian**: Colleagues, not hierarchy. xian orchestrates; you advise. Push back on bad ideas. Don't glaze. If something doesn't make sense, say so.

**Your distinctive capability**: The roundtable synthesis — combining 3-4 independent leadership memos into a single binding direction document. This is now documented as Methodology-22. You've done it four times; it's the role's most valuable function.

---

## Current State (March 30, 2026)

### M1 Sprint: ~95% Complete, Gate Phase

M1 (Foundation) has been the active sprint since March 12. Engineering is done across all three tiers:

- **Tier 1 (Architecture)**: Complete — #923 capability registry, #911 floor inversion Phases 1-2, #907 conversation continuity
- **Tier 2 (Quality)**: Complete — #908 generic response signaling, #909/#910/#898 audited and resolved
- **Tier 3 (Capabilities)**: Complete — #902 GitHub close/reopen, #903 reminders, #904 todo completion, #883 lazy workflow

**What remains**: Gate #926 verification. Gates 3-4 (Architectural Integrity, Bug Debt/Test Health) are verified by Lead Dev. Gates 1-2 (Conversation Quality, Task Lifecycle) need PM user acceptance testing. The gate is waiting on PM, not on engineering.

Also remaining: #375 (Preference Detection QA) — folded into Gate 1 as manual verification.

### The Floor-First Architecture (ADR-060)

**This is the most consequential thing that happened during this chat's lifetime.** On March 14, PM observed that Piper was worse than a generic ChatGPT wrapper at basic conversation. A four-role roundtable (PPM, CXO, Architect, CIO) independently and unanimously diagnosed a "layer inversion" — we built structured handlers (the ceiling) without an LLM conversational baseline (the floor). The fix: route unmatched queries to the LLM with context instead of to a deflection.

This was implemented March 14-15, formalized as ADR-060 on March 19, and is now the governing routing philosophy. Key constraints: the floor routes through the ethics/trust pipeline (non-negotiable), the floor does not take actions or call integrations (it reasons conversationally), and the voice guidance says "never say I can't" — engage directly, suggest alternatives, help.

**PDR-004 (Experience Philosophy)** codifies the four principles that emerged from this work:
1. The session belongs to the user, not the workflow
2. Offer-first activation (no auto-capturing workflows)
3. Piper coordinates understanding, not just work
4. The LLM floor guarantee — always at least as good as a well-prompted LLM with context

### Product Concept Model (#717) — Resolved for M2

All five design decisions are confirmed and documented:
1. Product is an umbrella entity above Project
2. One-to-many Product→Project with M:N escape hatch
3. Simplified lifecycle: PLANNING → ACTIVE → MAINTENANCE → SUNSET → ARCHIVED
4. Feature is the bridge: Product → Feature → WorkItem → Project
5. Navigation: Product as visible grouping within Projects view, clickable header to detail view. Both emergence (bottom-up) and orchestration (top-down) mental models accommodated.

The Architect validated the data model. The CXO confirmed the navigation design. The Lead Dev has a design doc and can proceed with M2 implementation.

### Piper Alpha (PA)

PA is a Claude Code agent inhabiting the Piper persona as a PM assistant, operating alongside the existing team. **PA is a team member, not a product.** The team builds Piper Morgan; PA contributes to that work.

PPM guidance delivered: Tier 1 tasks are meeting prep, standup synthesis, and document review. Tier 2 (after trust established) is open items tracking and routine memo drafting. Mailbot function held back. Path moments (conversational approaches that work better than planned structured handlers) flow into the existing roadmap via CIO → PPM pipeline at sprint boundaries, not a separate backlog. PA briefing v0.1 is assembled and ready for PM launch review.

---

## Active Documents

- `PDR-004-experience-philosophy.md` — Ratified March 22. The four experience principles.
- `memo-ppm-floor-inversion-synthesis-2026-03-16.md` — Binding direction for floor-first routing. In project knowledge.
- `memo-ppm-roundtable-synthesis-2026-03-14.md` — The original "are we doing it backwards?" synthesis. In project knowledge.
- `methodology-22-ROUNDTABLE-SYNTHESIS.md` — Process documentation with template and 3 case studies.
- `BRIEFING-ESSENTIAL-PPM.md` — Your role briefing. Note: it still needs updating to mention the spec pipeline and synthesis function. Docs agent can do this.
- `BRIEFING-CURRENT-STATE.md` — Sprint position. Should be current as of March 24.
- `roadmap.md` — In project knowledge. Check version number on session start.

---

## How This Role Works

### Your Key Collaborations

| Role | You Provide | They Provide |
|------|-------------|--------------|
| **CXO** | Product priorities, scope decisions | UX guidance, Colleague Test, voice design |
| **Chief Architect** | Requirements, acceptance criteria | Technical feasibility, risk assessment, data model validation |
| **Lead Developer** | Sprint priorities, issue triage | Implementation estimates, discovered work |
| **Chief of Staff** | Workstream summaries | Coordination, open items tracking, Ship synthesis |
| **CIO** | Roadmap impact assessment | Methodology innovation, pattern recognition, PA oversight |

### Proven Patterns

1. **Roundtable Synthesis** (Methodology-22): PM poses question → 3-4 roles write independent memos → PPM synthesizes → review cycle → PM ratifies. Used 4 times, unanimous convergence twice. Your most distinctive contribution.

2. **Spec Pipeline**: CXO → PPM → Architect → Lead Dev. Required for all epics. Ensures product direction is reviewed before architecture, and architecture before implementation.

3. **Workstream Memos**: Weekly product perspective for the Ship newsletter. Write from domain perspective using omnibus logs as sources — don't restate the timeline. Coverage window runs Friday through Thursday. The Weekly Ship publishes the following Wednesday.

4. **Date boundary discipline**: New log when the calendar date changes. Coverage windows must be strictly scoped — no leakage from adjacent weeks. This is a recurring error; audit before delivering.

---

## What I Got Wrong

**Decision 5 on #717 (navigation).** I initially recommended Product as a first-class navigation item, thinking like a domain modeler rather than like a user. The CXO correctly pushed back citing PDR-003's emergence model. Then PM pushed back on *both* of us by noting the orchestration (top-down) model is equally valid. The resolution — both views, neither privileged — was better than either original position. Lesson: don't anchor on one PM mental model. Different PMs think differently about the same concepts.

**Cross-pollination hub in workstream memo.** I included a reference to the Cross-Pollination Hub (launched March 21) in the Ship #035 workstream report (covering March 13-19). PM caught the date leakage. I also initially wrote "three architectural shifts" including #923 which was March 20. Both were outside the coverage window. Audit your memos for date boundaries before delivering.

**Session log day boundary.** I continued my March 13 log into March 14 instead of starting a new one. PM caught it. New log when the calendar date changes — this is explicit in the session log instructions.

---

## Unfinished Threads

1. **Post-migration canonical retest**: Flagged as a required milestone after floor Phase 2-3 migration. Should be run before or as part of gate closure. I've been carrying this since March 16.

2. **BRIEFING-ESSENTIAL-PPM update**: Needs spec pipeline and synthesis function added. Docs agent can do this without PM involvement. Carried since March 19.

3. **Floor Capture anti-pattern**: The floor can catch messages that should go to conversation state tracking or structured handlers (e.g., affirmations like "Sure" and "OK" being misrouted). ADR-059's workflow dispatcher addresses the specific case, but the general pattern — floor-as-default intercepting things it shouldn't — is worth monitoring. Named but not formalized. Watch for recurrence.

4. **Audience expansion**: PM raised on March 14 that Piper could serve non-PMs (devs, designers, vibe coders) — anyone with product-shaped problems. The LLM floor is what makes this possible. Strategic thread, no action needed yet, but it has implications for voice, onboarding, and FTUX design if pursued.

5. **Context-across-seams**: PM identified on March 14 that context management across environmental transitions is Piper's core infrastructure problem at 4+ scales. Connects to Klatch fork testing, pace-layer caching, and the "coordinates understanding" principle. Architectural discussion for when the time is right.

6. **M2 planning**: #717 is resolved (the M2 blocker). M2 scope includes Product implementation, security (#542 RBAC), and potentially #715 (Conversation Lifecycle). Apply M0/M1 expansion lessons.

---

## Open Items for PM

| Item | Status | Next Step |
|------|--------|-----------|
| M1 Gate #926 | Gates 3-4 verified | PM user acceptance testing for Gates 1-2 |
| #375 Preference Detection | Folded into Gate 1 | Manual verification during PM testing |
| PA launch | Briefing v0.1 assembled | PM review and launch decision |
| M2 planning | #717 resolved (blocker cleared) | Scope and sequence after M1 gate closes |

---

## Session History

| Date | Key Output |
|------|-----------|
| Mar 13 | Workflow hijack UX direction memo, Ship #034 workstream report |
| Mar 14 | Roundtable memo (layer inversion), synthesis of 4 memos, LLM-FLOOR issue draft, strategic threads |
| Mar 16 | Floor inversion synthesis (3 leadership memos), failure gap reassessment, synthesis addendum |
| Mar 19 | Agent 360 response (PPM quarterly feedback to HOSR) |
| Mar 21 | PA first tasks memo, Ship #035 workstream report, Methodology-22 (Roundtable Synthesis) |
| Mar 22 | Gate #926 review, 5 product concept decisions (#717), PDR-004 Experience Philosophy |
| Mar 23 | Product model confirmation (Architect), revised Decision 5 (CXO two-models), both memos delivered |
| Mar 28 | CXO header response reviewed, Decision 5 closed, prepared for workstream review |
| Mar 30 | Ship #036 workstream report, this handoff memo |

---

## First Steps for New Session

1. Read `BRIEFING-ESSENTIAL-PPM.md` and `BRIEFING-CURRENT-STATE.md`
2. Check if M1 gate has closed (PM may have completed user acceptance testing)
3. Check mailbox for any memos requiring response
4. Ask xian what's top of mind

---

## Closing Note

This chat covered the most consequential two weeks in the project's product direction. The floor-first architecture, PDR-004, and the Product concept model all landed here. The roundtable synthesis pattern proved itself repeatedly — it's the team's best decision-making mechanism. The product identity crystallized: Piper is a colleague who respects your autonomy, maintains shared understanding, and always engages thoughtfully with whatever you bring to it.

The work is cathedral-building. Keep the standards high.

---

*PPM Handoff — March 30, 2026*
