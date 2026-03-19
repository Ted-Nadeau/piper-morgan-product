# Implementation Checklist: Methodology Audit Policy Enforcement

**Purpose**: Make the two approved policy changes self-enforcing, not just documented.
**Date**: March 16, 2026

---

## Policy 1: Trigger-Based Methodology Audit

### Documents to Update

| Document | Change | Owner | Enforcement Mechanism |
|----------|--------|-------|-----------------------|
| `staggered-audit-calendar-2026.md` | Replace Methodology Audit rows (Wks 7, 14, 21...) with "Trigger: sprint gate + 2 weeks. Max interval: 8 weeks." Remove fixed week assignments. | Chief of Staff | Calendar is the reference doc agents check |
| `BRIEFING-ESSENTIAL-CHIEF-STAFF.md` | Add to responsibilities: "Track sprint gate closures. When a gate closes, flag CIO for methodology audit within 2 weeks." | Docs agent | CoS reads this at session start — it becomes their job |
| `BRIEFING-ESSENTIAL-CIO.md` | Update "Methodology audit cadence (6-8 week cycles)" to "Methodology audit cadence (triggered by sprint gate closure + 2 weeks; 8-week max interval)" | Docs agent | CIO reads this at session start |
| `sprint-gate-template-v1.md` | Add checklist item at bottom: "[ ] Methodology audit window opened (CIO has 2 weeks)" | Docs agent | Gate closure physically triggers the reminder |

### How It Self-Enforces

The sprint gate template is the key. When the Lead Dev closes a gate using the template, the checklist item reminds everyone that the audit window is now open. The Chief of Staff's briefing tells them to track it. The CIO's briefing tells them to expect it. Three touchpoints, no single point of failure.

---

## Policy 2: CIO Self-Approval for Emerging Patterns

### Documents to Update

| Document | Change | Owner | Enforcement Mechanism |
|----------|--------|-------|-----------------------|
| `BRIEFING-ESSENTIAL-CIO.md` | Add to Decision Authority: "Self-approve patterns to Emerging status in pattern catalog. PM upgrades to Proven." | Docs agent | CIO knows they have the authority |
| `pattern-000-template.md` | Ensure Status field lists "Emerging" as a valid option with definition: "In catalog, findable, not yet validated through 3+ applications. Subject to revision." | Docs agent | Template enforces the status vocabulary |
| `CLAUDE.md` or project instructions | Add to pattern section: "Patterns may be committed at Emerging status by CIO without PM pre-approval. PM reviews and may upgrade to Proven." | Docs agent | All agents see this in project instructions |
| `methodology-20-OMNIBUS-SESSION-LOGS.md` (or equivalent) | Note that Emerging patterns should be referenced in session logs and omnibus entries the same way Proven patterns are | Docs agent | Agents don't treat Emerging as second-class |

### How It Self-Enforces

The pattern template is the key. When the CIO creates a new pattern doc, the template offers "Emerging" as a status with a clear definition. The CIO briefing confirms the authority. Project instructions tell all agents to treat Emerging patterns as real. No approval gate blocks catalog entry.

### What Prevents Abuse

PM retains upgrade/revision/removal authority. The "Emerging" status itself signals "this hasn't been fully validated yet." The 3-5 application threshold for promotion to "Proven" is documented in the template. If a pattern turns out to be wrong, PM or CIO can demote or remove it — the low barrier to entry is matched by a low barrier to correction.

---

## Immediate Actions for PM

1. **Deliver to Chief of Staff**: methodology-audit-policy-updates-2026-03-16.md + this checklist. CoS owns the staggered calendar and briefing updates.
2. **Deliver to Docs agent**: This checklist as a work order. Docs agent updates the 4-5 documents listed above.
3. **Deliver to Chief Architect**: memo-cio-contract-gap-response-2026-03-16.md + Lead Dev's original methodological note.
4. **CIO immediate action**: Commit Pattern-062 (Assembly Assumption) to catalog as Emerging — first use of the new policy.

---

## Verification

After Docs agent completes updates, the following should be true:
- [ ] `staggered-audit-calendar-2026.md` no longer has fixed Methodology Audit weeks
- [ ] `sprint-gate-template-v1.md` has methodology audit checkbox
- [ ] `BRIEFING-ESSENTIAL-CHIEF-STAFF.md` mentions gate-triggered audit tracking
- [ ] `BRIEFING-ESSENTIAL-CIO.md` reflects trigger-based cadence and self-approval authority
- [ ] `pattern-000-template.md` lists Emerging as a valid status with definition
- [ ] Project instructions reference CIO self-approval for Emerging patterns

Once all boxes checked, these policies are enforced by the documents agents actually read, not by a memo they'll never see again.
