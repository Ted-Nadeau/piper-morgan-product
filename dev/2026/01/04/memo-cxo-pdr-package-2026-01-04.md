# Memo: Product Strategy Update for CXO

**To**: Chief Experience Officer
**From**: Principal Product Manager
**Date**: January 4, 2026
**Re**: PDR Package, UX Work Validation, and Next Steps

---

## Summary

Three Product Decision Records have been drafted today, heavily informed by your UX Strategy Synthesis work. This memo shares those PDRs, validates your contributions, and requests specific UX deliverables for next steps.

---

## Your Work Has Been Foundational

The UX Strategy Synthesis (Nov 26, 2025) and UX Summary Report (Jan 3, 2026) provided critical inputs that shaped all three PDRs:

| Your Contribution | Where It Landed |
|-------------------|-----------------|
| Recognition interface pattern | Core principle in PDR-001 |
| Trust gradient model (4 stages) | Proactivity governance in PDR-002 |
| 10%/90% discovery insight | FTUX success criteria reframing |
| B2 quality gate concept | Release criterion in PDR-002 |
| Articulation barrier research | User need framing in PDR-001 |
| Proactivity throttling rules | Explicit in PDR-002 (2/5 max, stop after 2 ignores) |
| Contextual capability hints | Discovery glue mechanism |

**The insight that proved most generative**: Your 10%/90% framing (users discover ~10% during onboarding, ~90% through use) completely reoriented how we think about FTUX success. We're not measuring "did they learn our features?" but "can they discover features naturally going forward?"

---

## PDR Package

Three PDRs are attached for your review:

### PDR-001: First Contact is First Recognition (Draft v2)

**Decision**: FTUX embodies the recognition interface pattern from moment zero—not a wizard that precedes the "real" experience.

**Key insight from today**: "Onboarding IS the primer." The preferences questionnaire itself demonstrates conversational interaction. Users learn how to talk to Piper by talking to Piper during setup. No separate demo artifact needed.

**Your input incorporated**:
- Trust gradient initialization at Stage 1
- Progressive reveal over feature tours
- Contextual capability response design

**Open design work**: Cross-session greeting patterns (context-aware, not scripted)

### PDR-002: Conversational Glue (Draft v1)

**Decision**: Conversational continuity is a first-class product feature, not infrastructure. The glue between capabilities is as important as the capabilities themselves.

**Three components**:
1. Discovery Glue — Recognition interface, contextual hints, dead-end recovery
2. Context Glue — Session persistence, cross-session memory, entity resolution
3. Proactivity Glue — Trust gradient governs when/how Piper offers unsolicited help

**B2 as release criterion**: Features that work technically but fail the B2 conversational test are not ready for users.

### PDR-101: Multi-Entity Conversation Support (Draft v1)

**Decision**: Piper supports multi-entity conversations in two modalities:
1. Host Mode: Piper hosts conversations with multiple humans/agents
2. Participant Mode: Piper joins externally-hosted contexts (e.g., Slack)

**Key insight**: Our development methodology IS the prototype. The async multi-agent coordination we do daily (Chief Architect ↔ Lead Developer ↔ PPM handoffs) is multi-entity conversation, just human-mediated.

**Source**: Ted Nadeau's "NewApp" PRD v0.3, which provides substantial architectural thinking we're translating into our vernacular.

---

## Requests for CXO

### Immediate (This Week)

1. **PDR Review**: Read attached PDRs, note any UX concerns or gaps
2. **Cross-Session Greeting Patterns**: PDR-001 establishes context-aware greeting as the approach. Need UX specification for:
   - Visual treatment of "continue or start fresh?" option
   - How to surface "last session context" without overwhelming
   - Edge cases: trivial sessions, long gaps, abandoned conversations

### Near-Term (Next 2 Weeks)

3. **B2 Quality Rubric**: PDR-002 defines B2 as "conversation feels natural." Need evaluable criteria:
   - What specific qualities constitute "natural"?
   - How do we assess this during development?
   - Who evaluates? (Alpha testers? Internal review?)

4. **Contextual Hint UX**: PDR-002 specifies throttling rules (2/5 max, stop after 2 ignores). Need:
   - Visual design for capability hints
   - Placement and timing patterns
   - Dismissal interaction (and "don't show again" option)

5. **Empty State Voice Guide**: PDR-001 requires "empty states are oriented." Need:
   - Voice/tone guidance for empty state Piper messages
   - Examples across key views (standup, issues, calendar)

### As Capacity Allows

6. **Multi-Entry Point FTUX Exploration**: PDR-001 establishes multiple entry points over linear wizard. Sketch or wireframe exploration of how this might look?

---

## Feedback Loop

Your UX work has been essential. The pattern we're establishing:

```
CXO Research/Synthesis → PPM translates to PDRs → PDRs inform implementation
                    ↑                                        ↓
                    └──────── Validation/Iteration ──────────┘
```

If this flow works for you, we can continue refining it. If you see friction points or want to adjust the handoff, let's discuss.

---

## Attachments

- PDR-001-ftux-as-first-recognition-v2-draft.md
- PDR-002-conversational-glue.md
- PDR-101-multi-entity-conversation.md

---

*Looking forward to your review. The work you've done has given us a strong foundation—now we're making it actionable.*

— PPM
