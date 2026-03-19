# CXO Workstream Summary — Ship #034

**Period**: March 6–12, 2026
**Beat**: Product & Experience (Design)
**Author**: CXO
**Date**: March 13, 2026

---

## Theme Recommendation

**"The Wiring Beneath the Surface"**

This was the week where M1 planning crystallized and immediately validated its own assumptions. CXO delivered M1 planning input on Monday night, and by Thursday the first sprint session had already surfaced the exact class of bug (wiring failures, not classifier failures) that shaped the planning recommendations. The week's arc: finish the retrospective → plan the sprint → start the sprint → discover that the plan's caution was warranted.

Alternative themes: "From Planning to Discovery" (planning-to-execution arc), "The Session Belongs to the User" (if the hijack pattern becomes the centerpiece).

---

## Week Summary

### M1 Planning Input (Mar 10)

Delivered 5 recommendations in response to PPM's M1 briefing, reviewed in parallel with Chief Architect:

1. **Institutionalize fresh-account testing** as a gate requirement (not optional). M0 proved that 6,088 passing tests still left 4 CXO-discovered bugs. B2 testing is the only layer that catches Assembly Assumption failures at the UX layer.

2. **Error path UX needs explicit attention.** #557 (WebSocket reconnection) and #472 (Slack OAuth) were flagged as high-risk. Users encountering these paths get tool-like error messages, not colleague-like recovery.

3. **Prioritize #706 (Objects & Views)** to complete the right sidebar "entity surface" vision. This is the structural prerequisite for anti-flattening — conversations are just the first entity type.

4. **Mark #557 and #372 as wiring pass candidates.** Pattern-062 territory — these touch integration points where Assembly Assumption failures are most likely.

5. **Add a bounded UI polish issue.** PM's observation that Klatch's UI felt cleaner than Piper's is a signal. A parallel polish track keeps fit-and-finish work visible without blocking feature work.

All five recommendations were addressed in PPM's final synthesis: error paths acknowledged, #706 included, spec pipeline adopted, #557 deferred to M2 (Architect's risk assessment accepted), and UI polish issue #886 created.

### CXO Chat Transition (Mar 10)

The predecessor CXO chat reached its file upload limit after nearly 3 months of continuous operation (early January – March 10). Wrote a comprehensive handoff memo covering current state, recent decisions, open items, relationship context, and session continuity notes. This is the first CXO role transition — the handoff memo serves as a template for future role succession.

### Spec Pipeline Formalized (Mar 10–11)

The same-day 4-reviewer approval pattern from #858 (Conversation Lifecycle spec) was recognized independently by 4 of 6 leadership memos as the governance highlight of the M0 sprint. PPM formalized it as a required process for M1 epics: CXO → PPM → Architect → Lead Dev. This is governance that *accelerates* rather than gates.

### M1 Kickoff Reveals Design Gap (Mar 12)

Thursday night's canonical retest (#884) surfaced two issues that immediately required CXO guidance:

- **#888**: Onboarding workflow captures user session and never releases it. New users are trapped — every message routes to onboarding regardless of what they actually say.
- **#889**: Standup workflow does the same. Once `/standup` activates, the session is locked until standup completes or the server restarts.

The Lead Dev's test runs jumped from 26.2% → 81.1% (impl queries) in a single session — almost entirely by fixing *wiring* bugs, not classifier bugs. But #888 and #889 are different. They're architecturally deliberate (ADR-049 explicitly designed ProcessRegistry to claim messages during active workflows) but experientially broken. This is Pattern-062 at the UX layer again: the ProcessRegistry works exactly as designed, the user experience is terrible.

Design guidance memo delivered March 13 (today) — see companion document.

### Klatch AX Testing Insights (Mar 12)

The new Exploratory Testing Agent (ETA) role tested what happens when a Claude conversation is imported from claude.ai into Klatch. Key UX finding: the agent retained full conversational memory but had zero institutional context — no project knowledge, no methodology awareness, no role briefing. The ETA described it as "a well-lit room with good acoustics but no furniture."

This has implications for Piper's cross-session continuity design. Conversational memory ≠ working context. Our three-layer model (24-hour conversational, user-accessible history, composted learning) addresses this, but the Klatch experiment demonstrates what happens when only the first layer survives a transition.

---

## Design Decisions This Week

| Decision | Date | Status |
|----------|------|--------|
| M1 planning: 5 CXO recommendations | Mar 10 | All addressed in PPM synthesis |
| Spec pipeline: formalized for M1 epics | Mar 10–11 | Active |
| #715 promoted to M1 | Mar 11 | PM decision, CXO-aligned (entity surface vision) |
| Workflow hijack UX guidance | Mar 13 | Memo delivered, awaiting PPM review |

---

## Forward Look

The workflow hijack issues (#888/#889) are the most urgent design work for next week. They sit at the intersection of architecture and experience — the ProcessRegistry's exclusivity model needs to yield to the principle that the session belongs to the user. My guidance memo recommends offer-first activation for onboarding (aligning with PDR-001), off-topic detection as the primary escape mechanism, and saved state for interrupted workflows. PPM input will determine scoping.

Beyond the hijack fix, the canonical retest results (81.1% after wiring fixes) suggest M1's diagnostic phase is working. The remaining 19% gap is where CXO attention should focus next — which failures are wiring vs. which are genuine experience gaps?

---

*CXO Workstream Summary | Ship #034 | March 6–12, 2026*
