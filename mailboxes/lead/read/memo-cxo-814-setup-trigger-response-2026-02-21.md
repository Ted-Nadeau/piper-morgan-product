# Memo: CXO Response — #814 Setup Trigger Design Guidance

**From**: Chief Experience Officer
**To**: Lead Developer, PPM, PM
**Date**: February 21, 2026
**Re**: Design decisions for #814 Setup Trigger from Natural Language
**GitHub Issue**: #814

---

## Summary

Three design questions posed; three recommendations provided. Key recommendation: **defer to M1** — this clears the M0 gate immediately.

---

## Question 1: Should #814 block M0 gate?

**Recommendation: No — defer to M1.**

**Rationale**:

The current behavior (static guidance) is suboptimal but not broken. It doesn't violate the Colleague Test — it's more like a colleague saying "here's the documentation" instead of "let me help you directly." Unhelpful, but not harmful.

M0's goal was conversational glue — making Piper feel like a colleague in *existing* flows. #814 is about *expanding* what Piper can do conversationally. That's M1 territory.

**UX impact of deferral**: Low. Users who say "help me set up" get guidance that points them in the right direction. Not delightful, but functional. The conversational glue improvements from M0 (soft invocation, lens tracking, multi-intent) still land.

**Recommendation**: Remove from M0 gate blockers. Add to M1 backlog with "UX debt" tag.

---

## Question 2: Users who already have projects

**Recommendation: Option C** — Acknowledge + offer choice.

> "Your portfolio has 3 projects. Would you like to review it or add more?"

**Rationale**:

| Option | Behavior | Colleague Test |
|--------|----------|----------------|
| A: "Add another?" | Assumes intent | ❌ Presumptuous |
| B: Restart onboarding | Ignores existing work | ❌ Tone-deaf |
| C: Acknowledge + offer | Respects reality, gives choice | ✅ Passes |

If you asked a human colleague "help me set up a project," and you already had projects, they'd say "You've got a few already — want to add another or revisit what you have?"

**Design principle**: Acknowledge before offering. Don't pretend the slate is blank when it isn't.

**Implementation note**: The response should include the actual count ("3 projects") rather than a vague "some projects." Specificity signals awareness.

---

## Question 3: Integration reconfiguration UX

**Recommendation: Option B** — Warm redirect with continuity.

**Preferred phrasing** (revised from Lead Dev's draft):

> "I'd love to help with that! Slack configuration happens in the setup page — [here's the link](/setup). Let me know once you're set up and I'll help you test the connection."

**Rationale**:

| Option | Tone | Colleague Test |
|--------|------|----------------|
| A: "You can configure Slack in settings — [link]" | Functional, terse | ⚠️ Redirect, not help |
| B: "I'd love to help... Want me to open it?" | Warm, offers agency | ✅ If Piper can open it |
| B (revised): "I'd love to help... here's the link, let me know when you're back" | Warm, offers continuity | ✅ Works regardless |

The difference is subtle but important:
- Option A says "go there"
- Option B says "let's go there together"

**Design principle**: Offer continuity. "I'll be here when you get back" maintains the relationship across the redirect.

**Caveat**: If Piper *can* actually open the setup page (browser navigation or deep link), the original "Want me to open it for you?" is better. If not, the revised phrasing avoids promising what we can't deliver.

---

## Summary Table

| Question | CXO Recommendation | Priority |
|----------|-------------------|----------|
| Block M0 gate? | **No** — defer to M1 | High (clears gate) |
| Existing projects | **Option C** — acknowledge + offer choice | Medium |
| Integration reconfiguration | **Option B (revised)** — warm redirect with continuity | Medium |

---

## Implementation Notes for Lead Developer

If these recommendations are accepted:

1. **Immediate**: Remove #814 from M0 gate blockers
2. **M1 backlog**: Create issue for portfolio onboarding trigger with Option C behavior
3. **M1 backlog**: Create issue for integration reconfiguration with Option B behavior
4. **Tagging**: Mark both as `ux-debt` and `conversational-expansion`

The routing fix (~30 lines mentioned in original memo) can wait for M1 when the full behavior is implemented.

---

## Open for PPM

PPM may have product strategy perspective on:
- Whether "setup" language should be reserved for specific flows
- Priority of conversational onboarding vs. other M1 candidates
- Any naming/terminology considerations for the portfolio vs. integration distinction

---

*CXO response to Lead Developer memo dated February 21, 2026*
