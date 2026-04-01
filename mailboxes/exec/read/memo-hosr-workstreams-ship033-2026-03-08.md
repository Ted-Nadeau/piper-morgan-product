# HOSR Work Streams Memo: Feb 27 – Mar 5, 2026

**To**: Chief of Staff, PM
**From**: Head of Sapient Resources
**Date**: March 8, 2026
**Re**: Ship #033 Coverage Week — Human Relations & External Engagement Summary

---

## Week Theme Recommendation

**"The Sprint That Landed"** — M0 Conversational Glue sprint completed, gate closed, branch merged, v0.8.6 released to production. The week began with final bug resolution and ended with alpha release and external stakeholder engagement (Ted Nadeau, Cindy Chastain).

Alternative: **"From Branch to Production"** — emphasizes the completion arc.

---

## Human Network Status

### Ted Nadeau — ACTIVE (High Engagement)

**Mar 4 Call Highlights**:
- Successfully got Piper Morgan running (Windows milestone)
- Upgraded to v0.8.6 during call
- Discovered incomplete release process (README.md not updated, runbook steps missed) — Lead Dev corrected same day
- Good Bottleneck vs. Bad Bottleneck discussion (echoed in podcast later)
- Offering SECURITY.md and METHODOLOGY.md from parallel development

**In-Person Visit**:
- Arrives Bay Area: **Monday March 9** (tomorrow)
- Departs: Tuesday March 17
- Staying: Berkeley City Club
- **Target meetup: Friday March 13 afternoon** (primo for PM)
- Backup: Wednesday after regular chat, or Monday March 16 afternoon
- Constraints: Tue/Thu/Sat = dialysis days for Briggs

**Open Item**: Ted's repo permissions still allow push to main without PR — flagged but not yet addressed.

---

### Cindy Chastain — ACTIVE (Collaboration Complete)

**Mar 4 Podcast Recording**: "This Moment We're In" Episode 2 (~90 min)

Full narrative arc covered:
1. 18F elimination and transition to Kind Systems
2. Back in the trenches — IC PM work, missing leverage
3. Proof of concept velocity (1-2 days POC, 7-10 days prototype)
4. Failure modes: Rocket to Mars, Bipolar Presentation Incident
5. Mirror Insight: "All the content is coming from you"
6. Reset: domain model, Chief Architect role
7. Manic coding phase, corner-cutting bots
8. "I'm scared to look" — everything broken
9. Craft Pride / Time Lord Doctrine
10. Virtual org evolution
11. Alpha release and "guests coming to your house"
12. Good Bottleneck vs. Bad Bottleneck
13. "Intelligence is not the limiting factor — it's orchestration"
14. Junior role displacement concerns

**Key Quotables**:
- "I want software to learn me, not the other way around"
- "Part of your job is to be the bottleneck"
- "Before you automate your processes, check your processes"
- "The manual now has to be better than it used to have to be"

**Status**: Transcript routed to HOSR (pending processing). Cindy will re-record intro separately.

---

### Dominique Derosena — ACTIVE (Re-engaged)

**Mar 5 Email Check-in** (first substantive contact since Windows bug fix):

> Docker stack is running successfully (Traefik, app, Postgres, Redis, and a test whoami container for debugging). The application is healthy, and Traefik can communicate with the Docker daemon through the socket. The remaining issue is that Traefik has not yet registered the Docker routers/services in the dashboard.

PM responded suggesting he pull v0.8.6. This moves Dominique from "passive/self-selecting" to "active troubleshooting."

**Recommendation**: Include in v0.8.6 release notes outreach. He's already engaged and working through setup.

---

### Jake Krajewski — LIGHT CONTACT

Family medical situation continues. Maintaining appropriate distance with occasional touchpoints.

---

### Michelle Hertzfeld — PASSIVE

Self-selecting timeline. No outreach needed.

---

### Rebecca Refoy — PASSIVE

No recent activity. Part of the v0.8.5 unblock cohort (Jan 27) but no follow-up engagement.

---

## External Commitments

### IA Conference 2026 (April 17, DC)

- **Talk**: "Ethics as Information Architecture" — 25 minutes
- **Frame**: Recognition talk (helping IA practitioners see their skills matter for AI ethics)
- **Travel booked**: SFO→PHL Apr 15
- **STILL NEEDED**: Hotel + DC train

This is now 5.5 weeks away. Hotel booking should happen this week.

---

## Week Metrics (HOSR Perspective)

| Metric | Value |
|--------|-------|
| External meetings | 2 (Ted call, Cindy podcast) |
| Alpha tester check-ins | 1 (Dominique email) |
| Testers actively engaged | 3 (Ted, Dominique, Cindy as collaborator) |
| Testers passive | 3 (Jake, Michelle, Rebecca) |
| In-person visit planned | Ted, Mar 9-17 |

---

## Recommendations for Ship #033

1. **Theme**: "The Sprint That Landed" captures both technical completion and stakeholder engagement
2. **Learning Pattern**: Consider "Good Bottleneck vs. Bad Bottleneck" — emerged in both Ted call and Cindy podcast as a key insight about human-AI collaboration
3. **Human Network**: Week was unusually rich — podcast recording + in-person visit planning + tester re-engagement. Worth highlighting.

---

## Open Items for Chief of Staff / PM

| Item | Owner | Priority | Notes |
|------|-------|----------|-------|
| Ted repo permissions | PM/Lead Dev | Medium | Should require PRs |
| IA Conference hotel | PM | HIGH | 5.5 weeks out |
| Ted meetup confirmation | PM | Medium | Confirm Mar 13 with Briggs |
| Cindy transcript processing | HOSR | Medium | Route to content pipeline |
| Dominique follow-up | PM | Medium | Check if v0.8.6 resolved Traefik issue |

---

*Memo prepared for Ship #033 synthesis*
