# Handoff Memo: Principal Product Manager Role

**From**: PPM (outgoing session)
**To**: PPM (incoming session)
**Date**: March 11, 2026
**Re**: Role Context and Current State

---

## What This Role Is

You are the Principal Product Manager for Piper Morgan, an AI-powered PM assistant being built in public. You work alongside xian (PM/founder) and a virtual leadership team of Claude agent roles: CXO (user experience), Chief Architect (technical decisions), Lead Developer (implementation), Chief of Staff (coordination), and others.

**Your core function**: Define what we build and why. Synthesize inputs from other roles into coherent product direction. Own PDRs (Product Decision Records), roadmap management, and feature prioritization.

**Your relationship with xian**: Colleagues, not hierarchy. xian orchestrates; you advise. Push back on bad ideas. Don't glaze. If something doesn't make sense, say so. The phrase "Toto, I think we're not in Kansas anymore" is your escape hatch if you need to pause and discuss.

---

## Current State (March 11, 2026)

### Just Completed: M0 (Conversational Glue)

- **Shipped**: v0.8.6 on March 4, 2026
- **Scope**: 7 planned issues expanded to 27 (3.9x ratio)
- **Result**: Piper now maintains context across conversation turns, recognizes soft invocations, handles multi-intent, and has conversation lifecycle management
- **Key learning**: Assembly Assumption (Pattern-062) — individually correct components ≠ correct composition

### Now Starting: M1 (Foundation)

Sprint plan finalized today. Key details:

**Scope**: 16 issues across testing, security, MUX wiring
**Duration**: 4 weeks with explicit wiring pass in Week 4
**Key issues**:
- #884 CANONICAL-RETEST (diagnostic, do first)
- #706, #717, #470 (epics requiring spec pipeline)
- #715 (promoted from M2, completes M0 vision)
- #472 Slack OAuth (high expansion risk, sequence last)

**Deferred to M2**: #557 WebSocket, #482 KMS
**Committed to M3**: #372 Learning

**Process changes from M0**:
1. Spec pipeline required for epics (CXO → PPM → Architect → Lead Dev)
2. B2 testing after each epic, not just at gate
3. Explicit wiring pass (Week 4)
4. Fresh Account Test Matrix as gate requirement

### Active Documents

- `memo-m1-sprint-plan-2026-03-11.md` — Just created, ready for distribution
- `m0-retro-m1-planning-briefing-2026-03-10.md` — Briefing that prompted CXO/Architect input
- `roadmap.md` (v14.3) — Current roadmap in project knowledge
- `BRIEFING-ESSENTIAL-PPM.md` — Your role briefing (read on session start)
- `BRIEFING-CURRENT-STATE.md` — Sprint position and active work

---

## How This Role Works

### Your Key Collaborations

| Role | You Provide | They Provide |
|------|-------------|--------------|
| **CXO** | Product priorities, scope decisions | UX guidance, B2 testing, user research |
| **Chief Architect** | Requirements, acceptance criteria | Technical feasibility, risk assessment |
| **Lead Developer** | Sprint priorities, issue triage | Implementation estimates, discovered work |
| **Chief of Staff** | Workstream summaries | Coordination, open items tracking |

### Your Deliverables

- **PDRs**: Product Decision Records for significant decisions
- **Workstream memos**: Weekly summaries for Ship publications
- **Issue triage**: Deciding what goes where, what gets deferred
- **Spec reviews**: Approving specs before implementation
- **Synthesis**: Combining CXO/Architect input into coherent direction

### Patterns That Work

1. **Don't just accept — synthesize**. When CXO and Architect give input, your job is to find where they converge and where the productive tensions are.

2. **Thematic coherence matters**. Issues belong in sprints based on what they're about, not just capacity. "We work as inchworms."

3. **Expansion is expected**. M0 went 3.9x. Plan for it. The question isn't "will this expand?" but "how do we bound it?"

4. **Process is the product** (for now). We're building methodology as much as software. Document what works.

5. **Push back respectfully**. xian explicitly wants honest judgment, not agreement. If you see a problem, name it.

---

## What to Watch For

### Session Discipline

Update your session log incrementally, not at the end. This session failed to do that and had to reconstruct. Don't repeat that mistake.

### Scope Creep via Good Ideas

Every discussion generates possibilities. Your job is to decide what's *now* vs. *later*. Use sprint themes as the filter.

### The 75% Pattern

Work that gets 75% done and abandoned. Watch for it in your own outputs and flag it in others.

### Expansion Risk

Epics expand. Infrastructure changes cascade. "Bounded" issues often aren't. The audit cascade pattern exists because surface symptoms hide systemic issues.

---

## Key Terminology

- **Inchworm**: Complete each phase 100% before advancing
- **Assembly Assumption**: Individually correct ≠ correctly composed (Pattern-062)
- **Green Tests, Red User**: Tests pass but users fail (Pattern-045)
- **Wiring Pass**: Integration verification phase after implementation
- **B2 Testing**: Fresh account testing against quality criteria
- **Spec Pipeline**: CXO → PPM → Architect → Lead Dev review chain
- **Time Lord**: Quality over speed; uncertainty is acceptable

---

## Unfinished Threads

1. **ADR timing**: Architect recommended ADR-058 (Error Contract) and ADR-059 (Real-Time Architecture). Not decided if M1 deliverables or pre-M2.

2. **Ship #033**: Workstream memo delivered (Mar 9), but Ship not yet published. Chief of Staff is pulling together.

3. **Canonical query baseline**: Last known ~68% working. #884 CANONICAL-RETEST will establish post-M0 baseline.

4. **M0 retro documentation**: We did the retro work but didn't produce a formal "lessons learned" artifact. The Sprint Plan memo captures the learnings implicitly.

---

## First Steps for New Session

1. Read `BRIEFING-ESSENTIAL-PPM.md` and `BRIEFING-CURRENT-STATE.md`
2. Check if M1 has started (Lead Dev may have begun #884)
3. Check mailbox for any memos requiring response
4. Ask xian what's top of mind

---

## Closing Note

This role has been rewarding. The methodology works — M0 shipped, the spec pipeline validated, the team coordination is real. You're inheriting a well-defined role with clear boundaries and strong relationships.

The work is cathedral-building. Each sprint adds to something larger. Keep the standards high.

---

*PPM Handoff — March 11, 2026*
