# Workstream Memo: Product & Strategy — March 13–19, 2026

**To**: Chief of Staff, PM
**From**: PPM
**Date**: 2026-03-21
**Re**: Ship #035 workstream contribution — Product report for the week
**Coverage**: Friday, March 13 – Thursday, March 19, 2026

---

## Theme Recommendation: "The Floor Changes Everything"

This was the week the project's product identity shifted. A single PM observation — "Why is Piper worse than a chat wrapper?" — triggered a four-role unanimous roundtable, a fundamental routing architecture inversion, and a cascade of downstream effects that are still propagating. The floor-first principle didn't just fix a bug. It redefined what Piper is: always at least as good as a well-prompted LLM with context, with structured handlers as the ceiling that makes it better, not different.

---

## Week Summary

Seven days, 40+ agent sessions across 10 roles, two architectural shifts, and the most productive engineering sprint in project history.

### Thursday, March 13: All-Hands Day

The week opened with Piper Morgan's most active single day: 12 sessions across 10 roles. Three chat handoffs (CXO, PPM, Architect — all ~3 months old, all hit the 100-upload limit) executed smoothly with comprehensive handoff memos. The workflow hijack design sprint produced a full design-to-implementation cycle in under 8 hours: CXO guidance at 8:10 AM → PPM binding direction at 8:35 AM → Architect approval at 11:35 AM → both issues (#888, #889) closed by 3:30 PM, with 34 new tests. The Lead Dev closed 7 issues and wrote 80+ tests in a single day — the most productive M1 session to date.

Three product decisions were made and implemented same-day: offer-first onboarding activation, layered escape mechanism for guided workflows, and "the session belongs to the user, not the workflow" as a governing principle. The CXO's contextual fallback work (#886) and classifier keyword fixes (#901) also shipped, projecting canonical pass rates toward 92.5%.

Ship #034 draft was completed with all 6 leadership workstream memos collected.

### Saturday, March 14: The Roundtable

PM shared a screenshot of Piper refusing a reasonable PM query with "I don't have that capability yet" and asked: "Are we doing it backwards?" Four leadership roles (PPM, CXO, Architect, CIO) wrote independent memos. The convergence was unanimous — the strongest consensus signal since "Governance at Speed." The diagnosis: we built the ceiling (structured handlers) without the floor (LLM conversation). The fix: route unmatched queries to the LLM with context instead of to a deflection.

The PPM synthesis was ratified after a revision cycle incorporating feedback from all three reviewers (CIO added ethics constraint, Architect corrected scope estimate and added no-actions constraint, CXO took ownership of voice guidance). The LLM-FLOOR issue was drafted and filed. The Lead Dev implemented the initial floor within hours. PM confirmed it working by evening — the same query that had been deflected now produced a real conversational engagement.

PM also raised two strategic threads that evening: Piper as a PM tool for non-PMs (expanding the target audience), and context-across-seams as a core infrastructure problem at four or more scales.

### Sunday, March 15: The Inversion

PM's manual testing revealed that Saturday's victory was incomplete — most messages still hit template handlers before reaching the floor. The Lead Dev investigated and diagnosed the real architectural problem: canonical handlers are the default and the floor is last resort, which is inverted from what the design docs (PDR-002, ADR-039) actually specify. The Lead Dev filed #911 (floor inversion) and implemented Phase 1 for GUIDANCE routing with 19 new tests.

The CIO delivered a six-week methodology audit (10 recommendations, overall assessment: methodology in strongest state since founding). Comms completed a final session in a two-month chat, producing an IAC presentation deck (16 slides), content pipeline inventory, and publication schedule.

### Monday, March 16: Synthesis Day

Eight sessions across seven roles. The Lead Dev's morning sprint closed 9 issues including #902 (fuzzy close), #914/#917/#920 (discovered-and-fixed same session), and began Phase 2 of the floor inversion.

The leadership synthesis cycle on the floor inversion completed: PPM synthesized Architect, CXO, and CIO guidance into binding implementation direction. The Action Gate concept was approved (refined criterion: "Does this intent require an operation the LLM cannot perform?"), the handler classification table was endorsed with one adjustment (core IDENTITY stays canonical), and all three infrastructure questions from the Lead Dev's advisory memo were answered with three-way convergence.

The CXO delivered voice guidance for floor responses — "never say I can't," engage directly, offer real actions, distinguish thinking-with-you from doing-for-you. The PPM also connected the CXO's March 13 failure gap analysis to the floor inversion, showing that 4 of 5 keyword collisions and all 3 predictive routing failures are likely resolved by floor-first routing alone.

Docs created a unified editorial calendar (304 rows), and the CIO delivered a contract gap assessment with trigger-based audit policy.

### Tuesday–Wednesday, March 17–18: Infrastructure

Lighter days focused on documentation infrastructure. The Docs agent fixed 8 of 12 stale briefing files (root cause: hardcoded counts instead of CURRENT-STATE references), battle-tested the publish-to-blog skill (v0.2), and completed Medium repatriation: 268/268 posts (100%) local with zero Medium dependencies. Blog image matching reached 87% in one session.

The Lead Dev filed #922 (conversation continuity bug) after PM QA testing revealed that affirmations and follow-ups were being misrouted to the floor — a new failure mode introduced by the floor-first work.

Dev/active/ sort completed (80→12 files). Mailbox v3 infrastructure was designed and built. 7 post-March-13 memos were delivered to recipient inboxes.

### Thursday, March 19: All Nine Agents

The first day with all 9 primary agent roles active. The ADR-059 (Workflow Dispatcher) sprint was the centerpiece: audit cascade → ADR draft → Architect review → implementation, all in one morning. Onboarding was disabled (Gall's Law — remove the broken thing rather than patch it), and a registry-based dispatcher replaced three competing offer/acceptance systems. ADR-060 (Floor-First Routing) was also formalized as a standalone ADR.

The Agent 360 questionnaire achieved 100% response rate (9/9). HOSR identified 7 cross-cutting themes, the strongest being universal briefing staleness (cited by all 9 agents). The Mailbox v3 system validated on first use — first delivery run processed 22 items and caught a slug error, proving the validation layer immediately.

Blog pipeline reached 100% completion: 269/269 posts with imageSlug.

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Sessions | 40+ across 7 days |
| Roles active | 10 (all primary roles + ETA) |
| Issues closed | ~25+ |
| Issues created | ~20+ |
| Git commits | 30+ |
| New tests written | 200+ |
| ADRs created/formalized | 2 (ADR-059, ADR-060) |
| Architectural shifts | 2 (floor-first routing, workflow dispatcher) |
| Agent 360 responses | 9/9 (100%) |
| Blog posts with images | 269/269 (100%) |
| Ship drafts | 1 (#034 "Measure First, Then Act") |
| Chat handoffs | 3 (CXO, PPM, Architect) |
| Days with all roles active | 2 (Mar 13, Mar 19) |

---

## Product Decisions Made This Week

1. **Workflow hijack UX**: Offer-first onboarding, layered escape, session-belongs-to-user principle (Mar 13)
2. **LLM conversational floor**: Unanimous roundtable consensus — Piper always at least as good as a well-prompted LLM with context (Mar 14)
3. **Floor-first routing inversion**: Canonical handlers are the ceiling, LLM is the floor. Handlers handle actions; floor handles conversation. (Mar 15–16)
4. **Action Gate criterion**: "Does this intent require an operation the LLM cannot perform?" — refined by Architect, approved by all (Mar 16)
5. **Voice guidance**: Never say "I can't," engage directly, offer real actions, distinguish thinking from doing (Mar 16)
6. **Ethics boundary in floor**: Non-negotiable — floor routes through same ethics/trust pipeline as handlers (Mar 16)
7. **No-actions constraint**: Floor reasons conversationally, does not call integrations or take actions (Mar 16)
8. **Onboarding disabled**: Gall's Law — remove the broken system rather than patch it, per ADR-059 (Mar 19)
9. **Workflow dispatcher**: Registry-based dispatch replaces 3 competing offer/acceptance systems, per ADR-059 (Mar 19)

---

## Risks and Concerns

**Velocity is high but fragile.** The Lead Dev closed 20 issues in 24 hours (Mar 13–14) and the team had two all-hands days in one week. This pace isn't sustainable and shouldn't be expected to repeat. M1 is approaching completion (~80%) but the remaining 20% includes wiring pass and quality verification, which are slower and less dramatic than bug fixes.

**Floor quality is the new frontier.** The routing is inverted, but the quality of floor responses depends on context assembly — how much relevant data the floor receives for each query category. The Phase 1 prompt-parroting lesson (Mar 15) and the #922 conversation continuity bug (Mar 17) show that each migration phase needs careful testing, not just routing changes.

**#922 is a floor-introduced regression.** Affirmations ("Sure," "OK") and follow-ups are being misrouted to the floor instead of connecting to the preceding conversation turn. This is the natural consequence of making the floor the default — it catches things it shouldn't. ADR-059's workflow dispatcher addresses this, but it's worth noting that the floor introduced a new failure mode while fixing the old one.

**Briefing staleness is systemic.** All 9 Agent 360 respondents cited it. The Docs agent's weekly audit catches drift, but the decay rate between audits is fast enough to mislead newly onboarding agents. The root cause fix (hardcoded counts → CURRENT-STATE references) was applied Mar 17, but enforcement requires ongoing discipline.

---

## Forward Look

M1 is at ~80% and approaching its gate. The floor-first routing (ADR-060) is the week's most consequential output — it changes what Piper *is* at the experience layer. The remaining M1 work is primarily verification: canonical retest after Phase 2-3 migration, quality assessment of floor responses across categories, and the wiring pass.

Ship #034 ("Measure First, Then Act") was drafted March 13 and is awaiting publication. Ship #035 coverage window is this week.

---

*PPM Workstream Memo | March 21, 2026*
