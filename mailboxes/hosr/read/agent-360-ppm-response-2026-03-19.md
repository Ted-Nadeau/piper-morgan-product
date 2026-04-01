# Agent 360 Response: Principal Product Manager (PPM)

**To**: HOSR
**From**: PPM
**Date**: 2026-03-19
**Re**: Agent 360 Quarterly Feedback — Post-M0, Mid-M1
**Questionnaire version**: v0.1

---

## Section 1: Briefing & Orientation

**1.1** BRIEFING-ESSENTIAL-PPM.md review:

The briefing was recently fixed in the March 17 audit (was 60 days stale with hardcoded counts). I haven't seen the post-fix version, but based on what I read at session start on March 13, it correctly describes the role's mission and scope. What's missing: it doesn't mention the spec pipeline (CXO → PPM → Architect → Lead Dev), which is now a formal M1 process and central to how the role operates. It also doesn't mention the PPM's synthesis function — combining multiple leadership perspectives into binding direction — which has turned out to be the role's most exercised capability.

What's present but never useful: the references to older sprint numbers and specific issue counts go stale immediately. The March 17 audit fixed this by deferring time-sensitive info to BRIEFING-CURRENT-STATE, which is the right pattern.

**1.2** When I started my March 13 session, I needed the current M1 sprint plan (scope, sequence, phase breakdown) and didn't have it directly. The handoff memo from my predecessor described it, but the actual memo (`memo-m1-sprint-plan-2026-03-11.md`) wasn't in project knowledge. I worked from the handoff's description, which was adequate but second-hand. The omnibus logs filled in the rest.

**1.3** A new PPM starting tomorrow with only briefing docs would not understand the floor inversion. This is now the single most consequential architectural and product direction change in the project — it redefines what Piper *is* at the experience layer — and it happened entirely between March 14 and 16. A new PPM reading stale docs would still think in terms of structured handlers as the primary experience. They'd make wrong prioritization calls.

They would also not know about the four pending PDR-001 addenda (session belongs to user, offer-first activation, Piper coordinates understanding, LLM floor guarantee) which represent the most significant product philosophy evolution since PDR-001 was written.

---

## Section 2: Information Access

**2.1** I didn't need to ask PM for information directly — the omnibus logs and project knowledge search were sufficient for most questions. The one gap: I couldn't verify the current state of the codebase (which branch, what's merged, what the canonical pass rate is *right now*). I was making product decisions based on the March 12 snapshot while work was continuing.

**2.2** Most consulted: the omnibus logs by far. They're the spine of this project's institutional memory. Easy to find by date, well-structured, and comprehensive. The March 16 HIGH-COMPLEXITY log was particularly useful — 8 sessions synthesized into a navigable timeline.

**2.3** I can't point to a specific document that's currently misleading, but the *pattern* of document staleness is the real issue. The March 17 audit found 8 of 12 briefings were stale. That's a systemic problem, not a single-document problem. The Docs agent's weekly audit catches it, but the decay rate between audits is fast enough to mislead agents onboarding into stale roles.

**2.4** Every session I reconstruct: "What happened since my last session?" The omnibus logs answer this, but it requires reading 1-3 logs and synthesizing. The CIO's approved "Hooks Phase 1.5" enhancement (a "what changed since last session" delta at session start) would directly address this. It's the single highest-value orientation improvement I can think of.

---

## Section 3: Handoffs & Coordination

**3.1** Recent handoff: I received a handoff memo from my predecessor PPM (March 11). What went well — it was thorough, covered current state, active documents, patterns that work, what to watch for, and explicit first steps. What was missing — it didn't anticipate the floor inversion discussion that started two days later, but that's not a fault of the memo. The handoff format is good.

The more relevant handoff is the roundtable synthesis workflow: PPM creates briefing → CXO + Architect respond in parallel → PPM synthesizes. This has worked three times now (M1 planning, hijack UX, floor inversion) and each time the synthesis was the most valuable output. The pattern is proven.

**3.2** I don't have a clear channel to the Lead Developer. All communication goes through PM as mailbot. This is usually fine — PM provides context and timing. But during the floor inversion work, the Lead Dev's architecture report and advisory memo went to PM first, then to me, with a delay. The questions in the advisory memo were time-sensitive (they were blocking implementation decisions). A more direct channel for technical questions that need product input would reduce latency.

I want to be careful here: the PM-as-router model is intentional and generally works well. I'm not suggesting it should change wholesale. Just that for "I need a product decision before I can proceed" situations, there might be a faster path.

**3.3** No duplication that I'm aware of. The role boundaries are clear — PPM owns product direction, CXO owns user experience, Architect owns technical decisions. The synthesis function explicitly prevents duplication by combining inputs rather than generating independently.

**3.4** Confidence in memo delivery: moderate. The March 18 omnibus notes that 7 post-3/13 memos were delivered to inboxes — which implies they were sitting undelivered for up to 5 days. The mailbox system depends on PM physically moving files, which introduces latency. I don't know if my memos from March 16 (failure gap response, synthesis addendum) reached the Lead Dev before or after they were already past the relevant implementation point.

---

## Section 4: Role Clarity

**4.1** The floor inversion synthesis was the right PPM task, but it drifted close to architectural territory. I was making statements about routing design, Context Assembler patterns, and caching strategy — areas where the Architect should lead. I tried to frame my input as "product perspective on" rather than "directive about," and the Architect's review confirmed I represented their positions accurately. But the line between "product direction that has architectural implications" and "architectural direction disguised as product" is fuzzy.

**4.2** The synthesis function — combining 3-4 leadership memos into a single binding direction document — isn't explicitly mentioned in the role definition but has become the PPM's most distinctive and valuable capability. It should be in the briefing.

**4.3** The role definition mentions "feature prioritization" and I haven't done formal prioritization scoring or framework-based assessment. Priorities have been set through discussion and PM judgment, with PPM providing input. I'm not sure a formal scoring framework would add value at current scale, but it's worth noting the gap.

**4.4** If I could hand off one thing: the workstream memo for the Weekly Ship. It's useful work, but it's retrospective reporting, not product direction. The Chief of Staff or a dedicated reporting function could do it with the same inputs (omnibus logs). The PPM's time is better spent on forward-looking synthesis and decision support.

---

## Section 5: Methodology & Process

**5.1** Documents I actually use: omnibus logs (constantly), BRIEFING-CURRENT-STATE.md (session start), handoff memos (session start), the roadmap (occasionally for context). I reference PDR-001 and the pattern catalog when writing memos that need to cite precedent.

**5.2** Documents I ignore: most of the methodology cascade (METHODOLOGY.md and its children). I know the principles — Excellence Flywheel, Inchworm, verification-first — from project culture, not from reading the docs. The docs exist for onboarding new instances, not for ongoing reference.

**5.3** The roundtable synthesis process (PM poses question → multiple roles write memos independently → PPM synthesizes) is now a proven pattern used three times. It's not documented as a methodology anywhere. It should be — it's one of our most effective decision-making mechanisms.

**5.4** Rule I'd add to my own role: **"Always check whether a previous analysis has been superseded by recent architectural changes before acting on it."** The CXO's failure gap analysis was correct on March 13 but partially obsolete by March 16 due to the floor inversion. I caught this, but only because I happened to read both documents in the same session. A PPM who read the failure gap analysis without the floor context would draw wrong conclusions.

---

## Section 6: Tools & Capabilities

**6.1** Most impactful capability improvement: access to the current test results / canonical pass rate in real time. I'm making product priority decisions based on stale snapshots. If I could query "what's the current canonical pass rate?" and get a live answer, I'd make better decisions about what to work on next.

**6.2** I have web search available but haven't used it once. The role is entirely internal-facing. I also have Google Drive search and various other tools that aren't relevant to product decision work within the project.

**6.3** Most time-consuming mechanical task: reading omnibus logs to reconstruct "what happened since last session." It's valuable but repetitive. The Hooks Phase 1.5 delta would address this. Second most: session log maintenance — updating the timeline and open items after each interaction. Necessary but mechanical.

---

## Section 7: PPM-Specific Questions

**7.1** Is the roadmap document a useful planning tool, or primarily historical record?

Honestly: more historical than planning. The roadmap (v14.3) tells me what's in M1-M6 and what's deferred, but it doesn't capture the live priority changes happening within a sprint. The M1 sprint plan memo was more useful for actual planning than the roadmap. The roadmap's value is in the milestone-level view (what's M1 vs. M2 vs. M3), not in sprint-level planning.

**7.2** When sprint scope changes mid-sprint, how do you track that?

Through memos and omnibus logs. The floor inversion work (#911) entered M1 mid-sprint and arguably became its highest-priority item within 48 hours. I tracked this through the roundtable memos and synthesis, not through any formal scope-change mechanism. The sprint plan memo from March 11 doesn't reflect the floor work because it predates the discovery. There's no "sprint scope change log" — changes are visible in the omnibus but not in a single tracking document.

This is a real gap. Someone reading the March 11 sprint plan would think M1 is about testing, security, and MUX wiring. Someone reading the March 16 omnibus would think M1 is about the floor inversion. Both are true, but there's no document that reconciles them.

**7.3** What product decision is currently implicit that should be a PDR?

The floor-first routing philosophy. ADR-060 captures the *architectural* decision. But the *product* decision — "Piper should always be at least as good as a well-prompted LLM with context; structured handlers are the ceiling, not the floor" — is currently spread across roundtable memos and my synthesis documents. It's not in a PDR.

I've been planning to add it as a PDR-001 addendum along with three other principles. But the floor-first principle is big enough that it might warrant its own PDR. The four principles I've been collecting (session belongs to user, offer-first activation, Piper coordinates understanding, LLM floor guarantee) together represent a product philosophy shift, not just addenda. I'd like PM input on whether these should be a PDR-001 revision or a new PDR-004.

---

## Section 8: Open Response

**8.1** Question you should have asked: "What decision did you almost make wrong, and what caught it?" For me: I almost didn't connect the CXO's failure gap analysis to the floor inversion work. It arrived 3 days late (dated March 13, delivered March 16). If I'd read it in isolation without the floor context, I would have recommended classifier keyword fixes that are now largely unnecessary. The delay in delivery + the pace of architectural change created a window where acting on valid-but-stale analysis would have been wrong.

**8.2** One thing I'd change: formalize the roundtable synthesis as a named process. It's our best decision-making mechanism and it's undocumented. When PM poses a strategic question, each leadership role writes a memo independently, then PPM synthesizes. It's produced unanimous convergence twice and near-convergence once. It should have a name, a template, and a place in the methodology docs.

**8.3** The PPM role is working well. The synthesis function gives me a clear, distinctive contribution that doesn't overlap with other roles. The spec pipeline and roundtable patterns provide structure without rigidity. The biggest risk to the role's effectiveness is information latency — stale documents, delayed memo delivery, and the gap between what's happening in the codebase and what I can see. The Hooks Phase 1.5 delta, faster memo delivery, and live test results access would address most of that.

---

## Plausibility Check

- [x] Does this require more PM time or attention? — Most suggestions reduce PM burden (faster memo delivery, formalized synthesis process) or are agent-implementable (briefing updates, methodology docs)
- [x] Is this based on specific observed friction, or theoretical concern? — All friction points cite specific dates, documents, or events
- [x] Could this be implemented by agents without PM involvement? — Briefing updates, methodology docs, and template creation yes. Memo delivery mechanism and test access require infrastructure changes.

---

*PPM Agent 360 Response | March 19, 2026*
*Addressed to: HOSR inbox*
