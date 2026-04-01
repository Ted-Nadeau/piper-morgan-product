# Memo: Chief Architect Workstream Report — Mar 13-19, 2026

**From**: Chief Architect
**To**: PM (xian), Chief of Staff (exec)
**Date**: March 21, 2026
**Re**: Engineering Beat — Week of Mar 13-19, 2026
**Coverage**: Ship #035 window (if applicable)

---

## Week Arc: "Invert the Floor"

The week began with a tactical fix (workflow hijack) and ended with a structural rethinking of how Piper responds to users. The governing insight — Piper should always be at least as good as a well-prompted LLM — reframed the entire M1 approach. By week's end, the floor-first routing architecture was formalized, Phase 1 was implemented, and the workflow dispatch system was rebuilt from scratch.

Underneath the headline, the engineering infrastructure matured significantly: Mailbox v3, the Agent 360 exercise, 3 ADRs (059, 060, and amendments to 039/049), and the first day with all 9 agent roles active.

---

## Day-by-Day Engineering Activity

| Day | Type | Sessions | Engineering Focus |
|-----|------|----------|-------------------|
| Fri Mar 13 | HIGH-COMPLEXITY | 12 | #888/#889 hijack closed, 80+ tests, spec pipeline same-day (CXO→PPM→Arch→impl), 3 chat handoffs |
| Sat Mar 14 | STANDARD | 8 | "Are we doing it backwards?" roundtable, E2E infrastructure (#352), MUX discovery (#706), floor #907, todo completion #904 |
| Sun Mar 15 | STANDARD | 5 | Floor inversion investigation, Phase 1 GUIDANCE routing, CIO methodology audit (10 recommendations), IAC presentation |
| Mon Mar 16 | HIGH-COMPLEXITY | 8 | Leadership floor synthesis, "extend without verifying" systemic discovery, action registry (34 pairs), 9 issues closed |
| Tue Mar 17 | STANDARD | 2 | Briefing audit (8/12 fixed), Medium repatriation 100%, #922 conversation continuity bug filed |
| Wed Mar 18 | MINIMAL | 1 | dev/active/ sort (80→12 files), blog image matching (134/168) |
| Thu Mar 19 | HIGH-COMPLEXITY | 9 | ALL 9 ROLES ACTIVE (first). ADR-059 drafted/reviewed/implemented same morning. ADR-060 created. Mailbox v3 built. Agent 360: 9/9 response |

---

## Key Engineering Events

### Floor Inversion (#911, ADR-060)

The week's defining architectural arc. On Saturday, PM asked "why is Piper worse than a ChatGPT wrapper at basic conversation?" Four leadership roles independently converged on the same diagnosis: the LLM is used to classify but never to respond. The structured dispatch system is a ceiling without a floor.

| Stage | Date | What Happened |
|-------|------|---------------|
| Question raised | Mar 14 | PM screenshot: "I don't have that capability yet" for a reasonable PM query |
| Diagnosis | Mar 14 | 4/4 roundtable consensus — architectural inversion, not a feature gap |
| Investigation | Mar 15 | Lead Dev confirms: canonical handlers are default, floor is last resort |
| Phase 1 | Mar 15 | GUIDANCE category routed to floor with context, 19 new tests |
| Leadership synthesis | Mar 16 | Action Gate concept approved, voice guidance defined, failure gap reassessed |
| Systemic fix | Mar 16 | Action registry (34 pairs), stub-to-floor routing, multi-intent subsumption |
| Formalized | Mar 19 | ADR-060 created. ADR-039 annotated (routing superseded, infrastructure retained) |

The most significant downstream effect: **classifier accuracy matters most for routing actions, not conversations.** Under floor-first routing, 4 of 5 keyword collision failures produce acceptable floor responses. The projected canonical pass rate is ~90%+ from floor routing alone, without classifier changes.

### Workflow Dispatch Consolidation (ADR-059)

The week's second major architectural arc, growing from a different root. #922 (conversation continuity bug: "Sure" → dead end) traced to three independent offer/acceptance systems racing for control of user affirmations. Six bugs from the same structural cause.

PM directed: remove onboarding (Gall's Law), add a thin registry-based dispatcher, consolidate. ADR-059 went from audit to architect review to implementation in one morning (March 19). Onboarding disabled (228 tests skipped), `workflow_dispatcher.py` created with registry-based dispatch, soft offer acceptance refactored.

This supersedes part of the #888 hijack fix work — the onboarding workflow is removed entirely rather than fixed. The escape command infrastructure (registry-level, from the March 13 architectural review) remains needed for standup (#889) and future workflows.

### "Extension Without Integration" Pattern

The week's recurring structural discovery. PM's QA testing on March 16 exposed five bugs sharing one root cause: classification extended independently of handling, stubs absorbed the gap silently. The Lead Dev's Five Whys elevated this from individual bugs to systemic analysis.

This pattern appeared in the workflow dispatch race (#922/ADR-059) and multiple stub-to-floor routing issues. Proposed as Pattern-063. Six bugs, one cause.

---

## Engineering Metrics

| Metric | Value |
|--------|-------|
| Issues created | ~20 (#905-#922) |
| Issues closed | ~20 (many same-day) |
| ADRs | 2 new (059, 060) + 2 annotated (039, 049) |
| Test suite (Mar 13 start) | 6,047 |
| Test suite (Mar 19 end) | 6,190 (+143, plus 228 skipped for onboarding) |
| E2E tests added | 16 (infrastructure + first tests, #352) |
| Canonical impl pass rate | 81.1% → projected ~90%+ (pending retest) |
| Agent roles active (peak) | 9/9 (first time, Mar 19) |
| Agent 360 response rate | 9/9 (100%) |
| Sessions (week total) | ~45 across 7 days |

---

## Architectural Decisions This Week

| Decision | Status | Date | Notes |
|----------|--------|------|-------|
| Floor-first routing (ADR-060) | APPROVED | Mar 14-19 | 4/4 roundtable consensus, formalized as ADR |
| Action Gate criterion | APPROVED | Mar 16 | "Operation the LLM cannot perform?" |
| Workflow dispatcher (ADR-059) | APPROVED + IMPLEMENTED | Mar 19 | Registry-based, thin routing |
| Onboarding removal | IMPLEMENTED | Mar 19 | Per ADR-059, Gall's Law |
| ADR-039 status | Annotated | Mar 19 | Routing superseded by 060, infrastructure retained |
| ADR-049 status | Annotated | Mar 19 | Pending review, onboarding patterns on hold |
| #888/#889 hijack fixes | Partially superseded | Mar 13/19 | Escape infrastructure still needed for #889 |

---

## Observations

### What Worked Well

**Spec pipeline velocity.** The CXO→PPM→Architect→Lead Dev pipeline operated at peak efficiency twice: the March 13 hijack design sprint (question to implementation in one day) and the March 14 floor roundtable (question to unanimous consensus in five hours). The parallel-independent-then-synthesize pattern (CIO's recommendation) produced genuine convergence without anchoring.

**PM QA as architecture probe.** Both the floor inversion discovery (March 14 screenshot) and the "extend without verifying" pattern (March 16 QA) came from PM manually testing the product. Automated tests passed in both cases. Pattern-045 (Green Tests, Red User) continues to be the single most reliable discovery mechanism.

**Same-day audit-to-implementation.** ADR-059 went from audit cascade to architect review to implementation in one morning. The mailbox query mechanism (pre-v3) enabled fast architect turnaround despite no direct inter-role channel.

### What Needs Attention

**Briefing staleness is systemic.** All 9 Agent 360 respondents cited it. Five of nine said handoff memos were more useful than briefings. The March 17 briefing audit fixed the worst cases, but the root cause (time-sensitive info embedded in role briefings instead of deferred to CURRENT-STATE) will recur without structural prevention.

**Post-migration canonical retest needed.** The ~90%+ pass rate projection from floor routing is promising but unverified. A full retest after Phase 2-3 migration is the required next step — measurement over projection.

**Floor Phases 3-4 not yet scheduled.** Phases 1-2 cover the worst offenders (GUIDANCE and the low-risk categories). Phases 3-4 (STATUS, PRIORITY, TEMPORAL-calendar, CONVERSATION) remain in the migration plan but are not yet scheduled within M1.

**M1 gate approaching.** The remaining work is primarily wiring verification, floor quality confirmation, and the canonical retest. The gate should be data-driven (retest results), not calendar-driven.

### Theme Candidate for Ship #035

"Invert the Floor" — the week's arc from tactical hijack fix to strategic routing rethink, culminating in a formal architectural decision that the LLM is the default, not the last resort.

---

*Chief Architect Workstream Report — Mar 13-19, 2026*
