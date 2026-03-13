# Weekly Ship #028: The Alpha Reality Check

**Period**: January 23-29, 2026
**Theme**: Sprint → Ship → Reality Check

---

## The Week in One Sentence

We completed a 10-day sprint, shipped v0.8.5, and alpha testing immediately revealed what 5,253 unit tests couldn't find.

---

## By the Numbers

| Metric | Value |
|--------|-------|
| Issues closed | ~80 |
| Tests added | ~2,700 |
| Final test suite | 5,253 |
| Bugs discovered | 18 |
| P0 bugs found | 2 |
| Epics completed | 3 |
| Version released | v0.8.5 |
| Alpha testers unblocked | 3 |

---

## The Arc

This week had a clear narrative: **build fast → ship → discover what's broken → find root causes**.

**Thursday-Sunday (Jan 23-26)**: Extraordinary velocity. TRUST-LEVELS epic complete with 453 tests. MUX-IMPLEMENT sprints P1-P3 done. Mobile PoC breakthrough. ProcessRegistry architecture (ADR-049) implemented through multi-advisor coordination.

**Monday (Jan 27)**: v0.8.5 released. MUX-IMPLEMENT super epic complete after 10 days. Three alpha testers unblocked.

**Tuesday (Jan 28)**: Reality check. 11 bugs found in a single afternoon of testing, including a P0: portfolio onboarding has *never* actually saved projects to the database.

**Wednesday (Jan 29)**: Root cause investigation. The P0 wasn't a simple bug - it traced to a global unique constraint that should have been per-user. And deeper: calendar tokens stored globally without user scoping. One tester could see another's calendar events.

---

## The Milestone: MUX-IMPLEMENT Complete

The 10-day sprint (Jan 18-27) delivered the MUX foundation:

| Sprint | Focus | Delivered |
|--------|-------|-----------|
| P1 | Navigation & Settings | Home state, utility layer, command palette |
| P2 | Documentation Access | Lifecycle indicators, composting views |
| P3 | Conversation Model | Memory sync, channel consistency |
| P4 | Accessibility | WCAG 2.1 AA compliance, design tokens |

The grammar "Entities experience Moments in Places" moved from documentation to running code. The design principles established in December are now testable in production.

---

## The Reality Check

Then we tested for real.

**The P0 that never worked (#728)**: Portfolio onboarding captures project names. Piper says "I've added them to your portfolio." User goes to Projects page. Nothing there.

Root cause: The conversation *said* things happened. The database told a different story. No code ever wrote the projects.

**The deeper discovery (#734)**: Calendar and integration tokens were stored globally without user_id prefixes. One alpha tester saw another's calendar events.

Root cause: The Oct 2025 multi-user implementation was incomplete. Some storage paths use user scoping. Others don't.

**The pattern**: This is the 75% Pattern we documented months ago - infrastructure exists, wiring doesn't. We named it, and now we caught it. The methodology is working.

---

## The Lesson

> "Conversation says X happened" ≠ "X actually happened in database"

Unit tests passed. The conversation flowed smoothly. Success messages displayed. But the database was empty.

This is what alpha testing is for. Real users doing real workflows expose what mocked tests cannot.

---

## Methodology Wins

### Leadership Caucus (Pattern-059)

When PPM and Chief Architect disagreed on #427 closure criteria, the escalation worked:
- PPM said close with 2/4 criteria met
- Architect said the user would notice the gap
- Lead Dev synthesized and escalated
- Team converged on the better answer

Formalized as Pattern-059: sync coordination that complements async mailboxes.

### Simple Trigger Architecture

The logging incidents (Jan 22-25) revealed that verbose 30-line protocols fail post-compaction. Simple 6-line triggers survive.

New principle: **Protocols that must survive cognitive boundaries need simple triggers, not comprehensive procedures.**

### 60 Patterns

The pattern catalog reached 60 entries. A shared vocabulary for problems accelerates diagnosis and documentation.

---

## Mobile Update

The Mobile 2.0 PoC went from "broken" to "tactile validation" in one session (Jan 24).

Root cause found: Reanimated animation version mismatch - JS 0.7.1 vs native 0.5.1. Toast rendered invisibly.

Fix: Bypassed Reanimated, used simple setTimeout. All components now verified: gestures, intent callbacks, toast, haptics, card spring-back.

---

## What's Next

1. **Bug stabilization**: 10 of 18 bugs fixed within scope; remaining in progress
2. **Multi-tenancy audit**: Systematic review of all user-scoped data before expanding alpha
3. **E2E test coverage**: Tests that verify database state, not just conversation flow
4. **Continue alpha testing**: Gradual onboarding continues as bugs get fixed

---

## The Honest Assessment

**The good news**: We found these issues during alpha, not after launch. Root causes are being identified, not just symptoms patched. The methodology is working.

**The sobering news**: Oct 2025 multi-user implementation was incomplete. Some paths use user scoping, others don't. This has been lurking for months.

**The work ahead**: Foundation fixes before feature expansion. That's the right call.

---

## Previous Ship

[Ship #027: The Grammar of Experience](https://www.linkedin.com/posts/xian_weeklyship027-the-grammar-of-experience-activity-7289748028050173952-cYpZ)

---

*Ship #028 | January 23-29, 2026*
*Building Piper Morgan in public*
