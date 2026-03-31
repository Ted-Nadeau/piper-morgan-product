# Workstream Memo: Product & Strategy — March 20–26, 2026

**To**: Chief of Staff, PM
**From**: PPM
**Date**: 2026-03-30
**Re**: Ship #036 workstream contribution — Product report for the week
**Coverage**: Friday, March 20 – Thursday, March 26, 2026

---

## Theme Recommendation: "Closing the Sprint"

The week's arc was convergence: M1's open items steadily resolved until all that remained was the gate itself. Three engineering tiers completed, the Product concept model fully specified through a 4-role coordination chain, PDR-004 codified ten days of product thinking, and the M1 gate was filed with CXO and PPM refinements incorporated. The week ended with an unplanned pause — Anthropic service disruptions halted work on March 26 — but by then the sprint was ready for its final verification.

---

## Product Perspective

This was a week of decisions landing. The product work that dominated the previous two weeks (floor inversion roundtable, hijack UX design sprint, conversational floor architecture) had produced principles and direction. This week those principles became artifacts: PDR-004 ratified, #717 resolved with all five concept decisions confirmed, and the M1 gate shaped by both CXO and PPM independent reviews.

### Product Concept Model (#717) — Resolved

The week's most substantive product design work was the #717 resolution. The Lead Dev surfaced five design decisions needed for M2. Four were straightforward (Product as umbrella, one-to-many with Projects, simplified lifecycle, Feature as bridge). The fifth — where Product appears in navigation — produced a productive three-role disagreement:

PPM recommended first-class navigation. CXO recommended Product as a section within Projects, citing PDR-003's emergence model. PM challenged both by observing that the orchestration model (product-first, projects-as-execution) is equally valid. PPM revised to accommodate both mental models: Product appears as a visible grouping header within the Projects view, clickable through to a Product detail view. Neither emergence nor orchestration is privileged.

The Architect validated all schema decisions, specified cascade behavior, and confirmed the 1:N → M:N migration path is clean. CXO answered the final design question (header prominence: visible, always present, section-title typography). The Lead Dev consolidated everything into a design doc and closed #717 — a 4-role coordination chain executing in ~90 minutes.

### PDR-004: Experience Philosophy — Ratified

The four principles accumulated since March 13 were codified as a standalone PDR: session belongs to the user, offer-first activation, Piper coordinates understanding, and the LLM floor guarantee. This was the right level of artifact — the principles operate above FTUX (PDR-001) and govern every interaction, not just the first one. PDR-004 is now the authoritative reference for Piper's experience design.

### M1 Gate #926 — Shaped and Verified

The Lead Dev filed the gate with four verification areas. PPM and CXO independently reviewed and converged on shared recommendations: fresh-account smoke testing, Colleague Test rubric with scoring threshold, multi-turn integration tests, and capability registry verification. The Lead Dev incorporated all additions and verified Gates 3 and 4 (Architectural Integrity, Bug Debt/Test Health) by March 24. Gates 1 and 2 (Conversation Quality, Task Lifecycle) await PM user acceptance testing.

### Piper Alpha — Briefing Assembled

The PA briefing reached v0.1 through a five-role synthesis: CIO provided structure, CXO provided voice guidance (working register vs. autobiography register), PPM defined Tier 1 tasks and roadmap impact rules, Architect set coexistence constraints, and HOSR prepared session protocols. PA is ready for launch pending PM review.

---

## Key Metrics (Product-Relevant)

| Metric | Value |
|--------|-------|
| Product decisions resolved | 5 (#717 concept model) |
| PDRs ratified | 1 (PDR-004 Experience Philosophy) |
| M1 issues closed | ~12 (including #717, #706, #902, #903, #883, #904, #908, #898) |
| M1 gate status | Filed, CXO+PPM reviewed, Gates 3-4 verified |
| M1 completion | ~95% (Tiers 1-3 complete, Tier 4 PM-led items remaining) |
| Methodology docs created | 2 (Methodology-22 Roundtable Synthesis, Colleague Test formalization) |
| Tests passing | 6,310 (0 failures, 228 skipped for ADR-059 onboarding) |
| Agent 360 action items completed | 3 of 3 (Colleague Test, Roundtable Synthesis, CIO reassurance) |

---

## Decisions Made This Week

1. **#717 Product as umbrella entity** above Project (Mar 22, confirmed Mar 23)
2. **#717 One-to-many Product→Project** with documented M:N escape hatch (Mar 22, Architect validated Mar 23)
3. **#717 Simplified lifecycle**: PLANNING → ACTIVE → MAINTENANCE → SUNSET → ARCHIVED (Mar 22)
4. **#717 Feature as bridge**: Product → Feature → WorkItem → Project hierarchy (Mar 22, Architect validated Mar 23)
5. **#717 Navigation**: Product as visible grouping within Projects, clickable to detail view. Both emergence and orchestration models accommodated (Mar 23, CXO confirmed Mar 24)
6. **PDR-004 ratified** as standalone PDR, not PDR-001 addendum (Mar 22)
7. **Gate #926 structure**: Four gates confirmed (Conversation Quality, Task Lifecycle, Architectural Integrity, Bug Debt). Classifier accuracy gate correctly dropped (Mar 22)

---

## Risks and Concerns

**M1 gate closure depends on PM testing.** Gates 3-4 are verified. Gates 1-2 need user acceptance testing by PM — testing actual conversations, not just automated checks. This is the right dependency (the PM should verify the product feels right before closing), but it means gate closure timing is in PM's hands.

**Service disruption impact.** Anthropic service issues disrupted work on March 26-28. The Docs agent session was interrupted mid-work on March 26 with commits stranded locally. However, Comms completed a substantial session that day (13 content pieces drafted, February content gap closed, "Wiring vs. Wizardry" published). The disruption's primary impact was on March 27-28, delaying omnibus synthesis, mail delivery, and the Ship process.

**M2 scope is large.** #717 is resolved, which was the M2 blocker. But M2 (MVP Activation) includes Product implementation, security (#542 RBAC), and potentially #715 (Conversation Lifecycle). The expansion risk lessons from M0 (3.9x) and M1 apply — plan carefully.

---

## Forward Look

M1 is at ~95% and waiting for gate verification. The engineering work is complete across all three tiers. The remaining items are PM-led: user acceptance testing for Gates 1-2, and the final #375 (Preference Detection) decision. Once those clear, M1 closes and we move to M2 planning.

The Piper Alpha briefing is assembled and ready for PM review. PA launch will be a significant moment — the first time an agent inhabits the Piper persona in a working context alongside the team that's building Piper.

Ship #035 ("Pour the Floor") was drafted March 21 and should be ready for publication. Ship #036 coverage is this week.

---

*PPM Workstream Memo | March 30, 2026*
