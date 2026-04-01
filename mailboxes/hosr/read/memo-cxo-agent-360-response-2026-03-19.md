# Agent 360 Response: Chief Experience Officer (CXO)

**To**: HOSR Inbox
**From**: CXO
**Date**: 2026-03-19
**Re**: Agent 360 Questionnaire v0.1
**Operational basis**: 4 sessions (Mar 13, 14, 16, 19), successor CXO chat starting Mar 13

---

## Section 1: Briefing & Orientation

**1.1** BRIEFING-ESSENTIAL-CXO.md review:

Mostly accurate on philosophy and decision authority. Two issues:
- **Stale sprint reference**: Still says "Current Sprint: B1 (Beta Enablers)" and refers to Pattern-045 discovery focus. We're in M1 now, and the floor inversion has fundamentally changed the CXO's relationship to the discovery problem. The floor *is* the discovery mechanism now — users discover capabilities by asking about them and getting real responses.
- **Missing recent decisions**: No mention of the Colleague Test (the CXO's primary decision heuristic in practice), the "session belongs to the user" principle, or the floor-first routing principle. These are the three most-used CXO tools in recent sessions, and none appear in the briefing.
- **Present but unused**: The MUX milestone sequence (MUX-V1 → MUX-GATE-1 → MUX-TECH X1 etc.) takes significant space but hasn't been relevant to any work in the sessions I've operated. It may be important for future sprints, but for a new CXO instance, it's noise during orientation.

**1.2** Context I needed immediately but had to search for:

The predecessor CXO's handoff memo was excellent and covered most gaps. The one thing I needed and didn't have in the briefing was **the current canonical query pass rate and what's failing**. The failure gap analysis required searching through omnibus logs and eventually getting raw test data from the PM. Given that the canonical retest is the primary quality signal for the product, a "current test health" snapshot should be immediately available.

**1.3** What a new instance would get wrong in the first hour:

They'd assume the B2 Quality Rubric and the Colleague Test are two separate things. In practice, the Colleague Test *is* the CXO's primary heuristic — it's applied more often and more broadly than the B2 rubric. The briefing presents B2 as the testing standard and mentions the Colleague Test as a "decision heuristic." In reality, the Colleague Test is used in almost every CXO decision (hijack guidance, floor voice, fallback copy, identity latency trade-off), while B2 is used specifically at gate testing.

They'd also likely not understand the floor inversion and how it changes the CXO's role. Before the floor, the CXO was reviewing individual handler responses and writing fallback copy. After the floor, the CXO is designing voice guidance for a conversational system and defining what "good" looks like across categories. The scope of the role shifted in a week.

---

## Section 2: Information Access

**2.1** Information I had to ask PM for:

The canonical retest data (Run 4 results, CSV, test script). This was the most consequential information gap in my sessions — my initial failure gap analysis was wrong because I was working from omnibus summaries instead of raw data. When the actual CSV arrived, 8 of my assumptions were incorrect.

**2.2** Most consulted document:

ADR-049 (Conversational State / Hierarchical Intent). Referenced repeatedly during hijack guidance and floor inversion work. Easy to find via project knowledge search.

**2.3** Stale or contradictory document:

The canonical query test matrix (`canonical-query-test-matrix-v2.md`) is from December 2025 and shows 19/63 implemented. As of March 12, we're at 53/61 implemented. This is the most stale document I encountered — and it's in the category that matters most for CXO work (product quality measurement).

**2.4** Recurring question answered each session:

"What's the current state of M1?" I check the omnibus logs or BRIEFING-CURRENT-STATE each time. A "sprint dashboard" section in the briefing (current sprint, pass rate, blockers, last release) would save this.

---

## Section 3: Handoffs & Coordination

**3.1** Recent handoff experience:

The predecessor CXO handoff memo (Mar 10) was the best handoff I've experienced. It covered current state, recent decisions, open items, relationship context, and session continuity notes. I was productive within minutes.

The one gap: it didn't include the *rationale* behind decisions, only the decisions themselves. For the Project Settings IA decision (Option C), I know what was decided but not what made Option C better than A or B. This hasn't caused problems yet, but if I needed to revisit or build on that decision, I'd be missing context.

**3.2** Role I need input from but lack a clear channel:

The **Lead Developer**. Multiple times I've written guidance (hijack UX, contextual fallbacks, voice direction) where I'd benefit from a quick "is this technically feasible?" check before committing to a recommendation. Currently, everything routes through PM as mailbot. A direct CXO → Lead Dev channel for feasibility checks would reduce round-trips. I recognize this adds coordination complexity — flagging the friction, not proposing a solution.

**3.3** Duplicated work:

Not exactly duplication, but my contextual fallback copy (Mar 13) was written, then reframed as test expectations (Mar 16 morning), then recognized as emergent floor behavior (Mar 16 afternoon). Three incarnations in one day. This isn't a process failure — the architecture was evolving fast and the work adapted correctly. But it illustrates how quickly CXO deliverables can be overtaken by architectural shifts. Earlier awareness of the floor inversion direction (even a heads-up that it was being explored) would have saved the initial hardcoded-strings version.

**3.4** Confidence in mailbox delivery:

Moderate. Memos reach their recipients because PM manually delivers them. The concern is latency — the PPM's failure gap reassessment was delayed because my Mar 13 memo wasn't delivered until Mar 16. That delay was minor in this case, but in a faster-moving situation, it could cause decisions based on stale analysis.

---

## Section 4: Role Clarity

**4.1** Task that felt like it belonged elsewhere:

The 4 GitHub issue drafts (classifier keyword, todo completion, reminders, GitHub close) felt more like PPM work than CXO work. I drafted them because I had the analysis context and it was faster than re-briefing another role. But issue drafting from gap analysis is fundamentally product scoping, not experience design.

**4.2** Expected work not in role definition:

**Issue drafting** (see above) and **test data analysis**. The failure gap analysis required reading CSV data, understanding test methodology, and mapping failures to handler behavior. The briefing describes the CXO as owning "B2 quality gate evaluation" but doesn't mention working directly with test results. In practice, test data is the CXO's primary evidence base.

**4.3** Work in role definition never asked to do:

- "Mobile experience exploration (skunkworks oversight)" — not mentioned once in 4 sessions
- "Design artifact standards" — no design artifacts reviewed
- "Alpha tester feedback synthesis" — no alpha tester feedback received to synthesize

These may be dormant rather than dead — the mobile project is paused, design artifacts may come with MUX implementation, and alpha testing may generate feedback soon.

**4.4** One responsibility to hand off:

Issue drafting. If the CXO identifies gaps and writes analysis memos, the PPM or a Docs agent should be able to draft the actual GitHub issues from the analysis. The CXO's value is in the diagnosis and the experience criteria, not in formatting issue templates.

---

## Section 5: Methodology & Process

**5.1** Methodology documents actually used:

- `BRIEFING-ESSENTIAL-CXO.md` — at session start
- `PDR-001-ftux-as-first-recognition-v2-draft.md` — referenced for offer-first onboarding rationale
- `PDR-002-conversational-glue.md` — referenced for floor principle
- `pattern-062-assembly-assumption.md` — referenced multiple times (hijack, failure gap, floor)
- Predecessor CXO handoff memo — the single most useful document

**5.2** Methodology documents ignored or worked around:

I haven't used any of the numbered methodology docs (`methodology-00` through `methodology-19`). They may be relevant for other roles, but the CXO's work is driven by PDRs, patterns, and the briefing — not by process methodology docs.

**5.3** Undocumented process I follow:

**The correction loop.** When I publish an analysis and then receive data that contradicts it, I issue a revised memo that explicitly supersedes the original, note what changed and why, and update the session log to flag the correction. I did this with the failure gap analysis (initial → revised after receiving CSV data). This isn't documented anywhere as a CXO practice, but it should be — getting things wrong quickly and correcting them transparently is better than getting things right slowly.

**5.4** Rule I'd add to prevent a failure mode:

**"Always request raw data before publishing quantitative analysis."** My initial failure gap memo was wrong because I inferred from omnibus summaries instead of requesting the actual test results. The correction caught it, but the wrong analysis was in circulation for hours. Rule: if your analysis involves numbers, get the source data first.

---

## Section 6: Tools & Capabilities

**6.1** Most impactful capability improvement:

**Access to the running canonical test results in real time** — either as a dashboard or as a project knowledge document that updates after each test run. The canonical retest is the CXO's report card. Currently it requires asking the PM for a file. Having it available in project knowledge would have prevented the initial wrong analysis and would make ongoing quality monitoring much faster.

**6.2** Available resource I don't use:

The `b2-quality-rubric-v1.md` document exists but I've never applied it formally. The Colleague Test has been sufficient for every decision so far. The rubric may become important when we do formal gate testing, but for day-to-day CXO decisions, it's overhead.

**6.3** Most time-consuming mechanical task:

**Session log maintenance.** Updating the log incrementally as work progresses — adding deliverables, updating decisions, updating open items — is the right approach but takes real time, especially when a session has multiple work arcs that require going back to update earlier sections. Not sure this can be automated, but it's the mechanical cost I notice most.

---

## Section 7: CXO-Specific Questions

**7.1** Clear criteria for "passes Colleague Test"?

Yes, but they live in my head, not in a document. The operationalized version appeared in the PPM's floor inversion synthesis (score 0-3 on: addresses what user asked, uses available context, feels like colleague not robot). That's the closest thing to a documented rubric. It should be formalized as a standalone document — the Colleague Test is used too broadly to exist only as scattered references in memos.

**7.2** Hardest gap to articulate between "tests pass" and "ready for users"?

**The response feels generic.** Tests can verify that a handler fires, returns 200, and includes expected keywords. They can't verify that the response feels like it was written *for this specific user asking this specific question*. The floor inversion is actually the biggest step toward closing this gap — LLM responses are inherently contextual in a way templates can never be. But "feels contextual" is hard to test automatically.

**7.3** UX bugs addressed with expected priority?

Yes. The hijack bugs (#888/#889) were flagged by the Lead Dev, CXO guidance was solicited immediately, PPM issued binding direction the same day, and implementation began. That's fast and respectful of the UX priority. The failure gap issues I drafted were also immediately accepted for M1 by PM. No complaints about prioritization.

---

## Section 8: Open Response

**8.1** Question you should have asked:

"What information do you produce that other roles actually use, and what do you produce that disappears?" This would surface whether CXO memos are being read and applied or just filed. I know the voice guidance memo was incorporated into the PPM synthesis (it was). I don't know whether the failure gap analysis influenced Lead Dev priorities directly or only through the PPM's addendum.

**8.2** One thing I'd change:

**Make the Colleague Test a first-class documented heuristic with examples, not just a phrase referenced in memos.** It's the CXO's most-used decision tool and it appears in nearly every memo I've written, but there's no canonical definition with scored examples. Every new CXO instance has to reverse-engineer what it means from context.

**8.3** Anything else:

The CXO role has been productive and well-utilized across these sessions. The workload has been appropriate — meaningful decisions with clear impact, not busywork. The fastest-moving period (floor inversion roundtable → synthesis → implementation in 48 hours) was also the highest-quality period. Speed and quality correlated because the decision was well-framed and the team converged quickly. That's worth noting as a positive signal about the coordination model.

The one systemic concern: CXO deliverables have a short half-life when architecture is evolving fast. The contextual fallback copy went through three reframes in one day. This isn't a problem if the CXO is actively in the loop during architectural shifts. It becomes a problem if CXO guidance is issued, the architecture changes, and nobody tells the CXO that the guidance is now stale. The mailbot model works for deliberate communication but doesn't handle "your earlier advice is now moot" well.

---

## Plausibility Check

- [x] Does this require more PM time or attention? — No. Most suggestions are documentation or process changes within CXO or HOSR scope.
- [x] Is this based on specific observed friction, or theoretical concern? — All specific, all from the Mar 13-19 session window.
- [x] Could this be implemented by agents without PM involvement? — Most, yes. Colleague Test formalization, briefing updates, and test matrix refresh are agent-executable.

---

*CXO Agent 360 Response | March 19, 2026*
