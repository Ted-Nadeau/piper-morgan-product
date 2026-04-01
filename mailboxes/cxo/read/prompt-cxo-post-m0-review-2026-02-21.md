# Prompt: Post-M0 CXO Review — Vision Survival Assessment

**For**: Chief Experience Officer
**Session Type**: Review / Assessment
**Participants**: CXO, PM (xian), optionally PPM
**Duration**: 1-2 hours
**Timing**: Before declaring B2 quality gate achieved

---

## Context

M0 (Conversational Glue) sprint is complete. Five features implemented:

| Issue | Feature | Tests |
|-------|---------|-------|
| #766 | GLUE-MAINPROJ: Fixed repeated "main project" question | 11 |
| #763 | GLUE-FOLLOWUP: Lens tracking with inheritance | 152 |
| #765 | GLUE-SLOTFILL: Natural slot filling framework | 124 |
| #764 | GLUE-MULTIINTENT: Intent orchestration | 47 |
| #767 | GLUE-SOFTINVOKE: Soft workflow invocation | 79 |

Additionally, M0.1 wiring pass fixed 9 integration gaps (#819-#827).

The sprint gate (#779) verified technical completion. This review verifies **vision survival** — did the implementation match the design intent, or did it get "flattened" into something technically working but experientially broken?

---

## Your Mission

Assess whether the M0 implementation matches the PDR-002 vision and the conversational-glue-implementation-guide.md specifications.

**Key question**: Would a user experience this as "conversational colleague" or "chatbot with features"?

---

## Preparation (Before Session)

Please review:

1. **`knowledge/PDR-002-conversational-glue-v3.md`** — The product vision
   - Five Foundational Principles (Section "Five Foundational Principles")
   - B2 Quality Gate criteria (Section "Success Criteria")
   - The Colleague Test

2. **`knowledge/conversational-glue-implementation-guide.md`** — The design specification
   - Section 5: Anti-Robotics Patterns
   - Section 12: Success Criteria
   - Section 13: Anti-Flattening Safeguards

3. **`knowledge/b2-quality-rubric-v1.md`** — The assessment rubric

---

## Session Agenda

### 1. Feature Walkthrough (30-45 min)

For each M0 feature, review sample interactions:

**#766 GLUE-MAINPROJ**
- Old: "Is that your main project?" asked repeatedly
- New: Primary designation asked once at end, easy to decline
- Test: Add 3 projects, observe flow

**#763 GLUE-FOLLOWUP**
- Test: "What's on my calendar tomorrow?" → "What about Thursday?"
- Should inherit calendar lens, not ask "Thursday... what?"
- Test: Several follow-up patterns (pronouns, elliptical, comparative)

**#765 GLUE-SLOTFILL**
- Test: "Schedule a meeting with Sarah Tuesday at 2pm about Q3"
- Should NOT ask for attendee, time, or day (already provided)
- Should only ask for genuinely missing slots

**#764 GLUE-MULTIINTENT**
- Test: "What's on my calendar and what are my top priorities?"
- Should address both, not drop the second
- Response should be coherent, not sequential dumps

**#767 GLUE-SOFTINVOKE**
- Test: "I need to get the team together next week"
- Should offer to help with meeting, not ignore the implied need
- Offer should be declinable without awkwardness

### 2. Colleague Test Application (15-20 min)

For each feature, explicitly ask:

> "If a human colleague responded this way, would it feel natural or weird?"

Document any "weird" responses with specifics.

### 3. B2 Criteria Scoring (15-20 min)

Score against B2 quality gate:

| Criterion | Target | Assessment |
|-----------|--------|------------|
| Naturalness | ≥4/5 | "Does this feel like talking to a colleague?" |
| Memory | >85% resolution | "Does Piper remember what matters?" |
| Proactivity | >30% acceptance, <10% annoyance | "Are suggestions helpful or annoying?" |
| Discovery | ≥3 features/30 days | "Can I discover capabilities without docs?" |
| Recovery | >60% continue | "When things go wrong, does Piper help?" |

### 4. Vision Erosion Check (10-15 min)

Review the anti-flattening table from the implementation guide:

| Vision | Flattened Version | Check |
|--------|-------------------|-------|
| Natural workflow invocation | Explicit command required | |
| Implicit confirmation | Confirm dialog for everything | |
| Multi-intent handling | "One thing at a time please" | |
| Contextual proactivity | Random suggestions | |
| Graceful topic shifts | "Complete current workflow first" | |

Flag any instances where implementation matches the "flattened" column.

---

## Output

After the session, produce a memo with:

1. **Verdict**: "B2 Ready" or "Revisions Needed"

2. **Feature-by-feature assessment**:
   - Colleague Test: Pass/Fail
   - Notable observations
   - Any flattening detected

3. **B2 scores** (even if subjective from limited testing)

4. **Revision list** (if any):
   - Specific issues to address
   - Priority (blocking vs. polish)

5. **Recommendation** for alpha tester feedback collection:
   - What specific questions to ask testers
   - What interactions to observe

---

## Sample Conversation Transcripts

PM to provide before session:
- [ ] 2-3 transcripts showing lens tracking (#763)
- [ ] 1-2 transcripts showing slot filling (#765)
- [ ] 1-2 transcripts showing multi-intent (#764)
- [ ] 1-2 transcripts showing soft invocation (#767)

If transcripts not available, session will include live testing with PM.

---

## Scheduling

Recommend scheduling within 1 week of M0 completion (i.e., by Feb 25).

Session can be asynchronous (CXO reviews independently, then discusses findings with PM) or synchronous (joint review session).

---

*This review is the qualitative check that sprint gates can't capture. The goal is catching vision erosion before we declare success.*
