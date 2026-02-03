# Memo: Weekly Communications Briefing for Weekly Ship #028

**From**: Communications Director
**To**: Chief of Staff, PM
**Date**: January 30, 2026
**Re**: Week of January 23-29, 2026 Summary for Weekly Ship Preparation

---

## Week at a Glance

| Day | Rating | Issues Closed | Tests Added | Theme |
|-----|--------|---------------|-------------|-------|
| Fri 23 | HIGH-COMPLEXITY | 18+ | ~636 | TRUST-LEVELS epic complete + Jan 22 forensic recovery |
| Sat 24 | HIGH-COMPLEXITY | 22+ | ~915 | 6-hour logging incident + Mobile PoC breakthrough |
| Sun 25 | HIGH-VELOCITY | 21 | 1000+ | MUX-IMPLEMENT P1-P3 sprint |
| Mon 26 | HIGH-ALIGNMENT | 5 | ~80 | Multi-advisor coordination + ADR-049 implementation |
| Tue 27 | HIGH-VELOCITY | 10 | ~50 | v0.8.5 release + MUX-IMPLEMENT complete |
| Wed 28 | MIXED-DAY | 8 | — | Alpha docs polish + P0 bug discovery (11 bugs) |
| Thu 29 | LIGHT-DAY | 0 | — | Bug triage + root causes found + multi-tenancy gap |

**Week totals (Jan 23-29)**: ~84 issues closed, ~2,680+ tests added

---

## Headline Candidates

1. **"From Sprint to Ship: v0.8.5 and the MUX-IMPLEMENT Marathon"** — 10-day sprint culminating in release
2. **"The P0 That Never Worked"** — Portfolio onboarding discovered to have NEVER persisted projects
3. **"Alpha Testing Reveals the 75% Pattern"** — 11 bugs in one afternoon, real users find what tests miss
4. **"Six Hours in the Dark"** — The logging incident and the fix that followed
5. **"Mobile Comes Alive"** — PoC goes from "broken" to tactile validation in one day
6. **"Multi-Tenancy Reality Check"** — Calendar tokens stored globally; one user saw another's events

**My recommendation**: Lead with **v0.8.5 and the MUX-IMPLEMENT completion** as the positive frame, with the **P0 discovery** and **multi-tenancy gap** as the honest "what alpha testing revealed" story. The narrative arc: we shipped → we tested for real → we found deep bugs → we fixed them → we found MORE bugs. That's the system working.

---

## Workstream Summaries

### 1. Product/Experience

**MUX-IMPLEMENT Super Epic**: COMPLETE ✅
- P1 (Navigation): Home state, utility layer, command palette, place windows — 185 tests
- P2 (Documentation): Document access, lifecycle indicators, composting views — 302 tests
- P3 (Conversation): Memory sync, channel consistency, follow-up detection — 407 tests
- P4 (Accessibility): WCAG 2.1 AA compliance, design tokens enforced, contrast testing — 638 template validations

**ADR-049 ProcessRegistry**: Implemented and accepted
- Guided process architecture generalized (onboarding, standup, future process types)
- Unified `_check_active_guided_process()` in intent_service.py

**Insight Lifecycle Decision**: Insights are NOT entities — grammar test revealed category error ("What would BLOCKED insight mean?"). Principled deferral.

### 2. Engineering/Architecture

**v0.8.5 Released** (Jan 27):
- Final test suite: 5253 passed, 24 skipped
- Lifecycle indicators on Todos, Projects, Work Items
- New views: Work Items, Project Detail
- Three alpha testers unblocked (Jake, Rebecca, Dominique)

**Alpha Testing Bug Discovery** (Jan 28):
- 11 bugs filed (#720-730)
- **P0 Critical**: #728 — Portfolio onboarding NEVER wrote projects to database
- Root cause: Conversation said "I've added them" but no persistence code existed
- 10 of 11 fixes applied same day

**Bug Root Causes Found** (Jan 29):
- **#731 Conversation persistence**: FIXED & VERIFIED — direct chat wasn't creating DB records
- **#736 Projects unique constraint**: Found REAL root cause of #728 — unique constraint was GLOBAL not per-user; different users couldn't have projects with same name
- **#734 Multi-tenancy CRITICAL**: Calendar/integration tokens stored globally without user_id prefix — alfamux user saw previous user's calendar events
- 3 parallel agents deployed for deeper investigation

**Pattern Validations**:
- "75% Pattern" confirmed again — infrastructure exists, wiring doesn't
- Multi-user isolation gaps found (#724, #728, #734, #736)

### 3. Methodology

**Logging Incident** (Jan 24):
- 6-hour gap discovered (post-compaction agents stopped logging)
- Root cause: Jan 22 CLAUDE.md refactor externalized critical protocol
- Fix: Inline mandatory verification with STOP condition
- Lesson: "Skill vs Protocol" distinction — protocols must survive context boundaries

**Leadership Caucus Pattern** (Pattern-059):
- Formalized from Jan 26 PPM/Architect disagreement
- PPM said close #427 with 2/4; Architect said can't
- Escalation → MVP Rubric emerged: "Does the user notice the gap?"

**Skills Formalized**:
- `discovered-work-capture` skill created
- Simple trigger + detailed skill architecture validated

### 4. External Relations/Communications

**Publications this week**:
- Weekly Ship #027 (LinkedIn, Jan 28)
- The Planning Caucus (Medium, Jan 28)
- The CLAUDE.md Paradox (Medium, Jan 30)

**Content pipeline loaded**:
- 3 narratives drafted (Does the User Notice?, The Cathedral Release, plus updates)
- 2 insight pieces ready for weekend (The Completion Discipline, 75% Complete)

**Alpha Tester Communications**:
- v0.8.5 release notes sent (Jan 28, 11:59 AM)
- Alpha docs audit completed (7 files fixed, 13 issue categories addressed)
- Tester roster created (7 active, 8 prospects)

### 5. Mobile

**PoC Breakthrough** (Jan 24):
- Root cause found: Reanimated animation version mismatch (JS 0.7.1 vs native 0.5.1)
- Fix: Bypassed Reanimated, simple setTimeout for auto-dismiss
- All components verified working: gestures, intent callbacks, toast, haptics, card spring-back
- Tactile validation period initiated

---

## Key Decisions Made

| Decision | Date | Outcome |
|----------|------|---------|
| ADR-049 (ProcessRegistry) | Jan 26 | APPROVED and implemented as MVP |
| ADR-050 Phases 1-3 | Jan 26 | DEFERRED to V2 (multi-party features) |
| MVP Rubric | Jan 26 | "Does the user notice?" becomes standard test |
| Insight lifecycle | Jan 27 | DEFERRED — Insights aren't entities |
| Logging protocol | Jan 24 | Inline + mandatory + STOP condition |

---

## Risks and Issues

**Active**:
- #720 Race condition on first load — partial root cause, needs more investigation
- #725 Chat refresh regression — from #583, needs verification
- #734 Multi-tenancy token storage — CRITICAL gap, requires threading user_id through ALL storage AND retrieval calls

**Resolved**:
- 6-hour logging incident — fix deployed, monitored
- Mobile PoC "broken" status — now functional
- P0 #728 (projects never save) — fix applied
- #731 Conversation persistence — FIXED & VERIFIED
- #736 Projects unique constraint — migration applied and tested

---

## Numbers for the Ship

| Metric | Value |
|--------|-------|
| Issues closed (Jan 23-29) | ~84 |
| Issues created (alpha bugs) | 17+ (#720-736) |
| Tests added | ~2,680+ |
| Final test suite | 5,253 |
| Alpha bugs found | 17 (11 on Jan 28, 6 on Jan 29) |
| Alpha bugs fixed | 12+ |
| Version released | v0.8.5 |
| Alpha testers unblocked | 3 |
| Patterns formalized | 1 (Pattern-059) |
| ADRs accepted | 1 (ADR-049) |
| Drafts created | 5 |
| Publications | 3 |

---

## Suggested Ship #028 Structure

**Theme**: "The Alpha Reality Check"

The week had a clear arc: complete a major milestone (v0.8.5, MUX-IMPLEMENT), ship it to testers, discover what real usage reveals. The P0 bug (#728) is the honest story — portfolio onboarding looked complete, felt complete, but never actually persisted anything. And Jan 29 dug deeper: the *real* root cause was a global unique constraint that should have been per-user.

**Sections**:
1. **The Release** — v0.8.5, 10-day sprint complete, 3 testers unblocked
2. **The Discovery** — 11 bugs in one afternoon, including a P0 that had NEVER worked
3. **The Deeper Dig** — Jan 29 found real root causes: global constraints, multi-tenancy gaps
4. **The Pattern** — 75% complete strikes again (infrastructure exists, wiring doesn't)
5. **The Methodology** — MVP Rubric from advisor disagreement, Leadership Caucus pattern
6. **The Fix** — 12+ bugs fixed, parallel agents deployed, systematic triage

**Tone**: Honest about what alpha testing revealed, but framed as the system working — we built, we tested for real, we found the gaps, we dug deeper, we fixed them. That's what alpha is for.

---

## Note

This briefing covers the complete week: January 23-29, 2026.

---

*Prepared by Communications Director*
*January 30, 2026, 6:15 PM (updated)*
