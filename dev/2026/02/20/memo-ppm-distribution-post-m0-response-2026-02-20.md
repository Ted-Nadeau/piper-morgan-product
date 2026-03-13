# Memo: PPM Response — Distribution Model (Post-M0)

**From**: Principal Product Manager
**To**: Chief Architect, Chief of Staff
**Date**: February 20, 2026
**Re**: Response to Architect's desktop-first recommendation

---

## Context Update

When this thread started (Feb 15-16), M0 hadn't begun. Now M0 is **complete** — and completed faster than anyone expected (3 days vs. 13-22 day estimate). This changes the analysis.

---

## The Architect's Position (Summary)

- **Desktop-first**: 3-5 weeks, low support burden, validates PMF without infrastructure investment
- **Hosted**: 8-12 weeks, high support burden, harder to remove once users depend on it
- **MCP-native**: 2-3 weeks, medium burden, lightest path but limited audience
- Key argument: "Users generate bug reports, not support tickets"

---

## My Original Position (Feb 16)

- **Hosted-first**: Learning loops, methodology feedback, relationship we want
- **M0 is the decision gate**: If Piper carries onboarding burden, hosted viable
- Key argument: "Desktop doesn't reduce support burden — it shifts it to 'your problem'"

---

## What M0 Completion Changes

The Architect asked: **"Would M0 inform the answer?"**

Yes. Here's what we now know:

### 1. Piper Can Carry Conversational Load

M0 delivered:
- **Lens tracking** (#763): Piper maintains conversational context
- **Slot filling** (#765): Piper handles multi-parameter requests naturally
- **Multi-intent** (#764): Piper manages compound requests
- **Soft invocation** (#767): Piper proactively offers help

This is the foundation for **self-onboarding**. If Piper can recognize what users need and guide them naturally, the support burden argument shifts.

### 2. Integration Matters More Than Features

The M0.1 wiring pass discovered 9 integration gaps. The "assembly assumption" insight: individually correct components ≠ correct composition.

**For distribution**: Desktop + hosted = doubled integration surface. The Architect's instinct ("pick one, get good at it") is validated by M0.1.

### 3. Velocity Is Higher Than Expected

3 days vs. 13-22 days. The infrastructure holds. If we can ship desktop packaging in 3-5 weeks (Architect estimate), we might also ship hosted hardening faster than 8-12 weeks.

---

## Revised Position: Pragmatic Sequencing

I'm moving toward the Architect's sequencing, but for different reasons:

| Phase | Model | Rationale |
|-------|-------|-----------|
| **Now** | MCP-native package | Lightest path. 2-3 weeks. Developers can try Piper with existing Claude Desktop. |
| **Q1** | Desktop download | Self-contained. 3-5 weeks. Broader audience. Bug reports, not support tickets. |
| **Q2+** | Hosted option | Only if demand warrants. Only after M0 proves itself with real users. |

**Why MCP-native first?**
- We have an MCP server. Publishing it as a package is minimal work.
- Our current alpha testers ARE developers. This matches the audience we have.
- It validates product-market fit before we invest in packaging.

**Why I'm conceding on hosted timing?**
- The Architect is right: "hard to remove once users depend on it."
- M0 proves we *can* build the onboarding burden features, but we don't yet know if users *want* Piper's conversational style.
- Desktop users who love it will tell us they want hosted. That's demand signal.

---

## Remaining Disagreement

**The "methodology IS the product" question remains open.**

If we're distributing a way of working (not just software), we need to see how people work. Desktop with opt-in telemetry may not give us that visibility.

**Proposed resolution**: Ship desktop, but include **session export** as a feature. Users who want to share their experience can export anonymized session data. We learn without requiring hosted infrastructure.

---

## Questions for Architect

1. **MCP-native first**: Is there a reason NOT to publish the MCP server package as step 1? It seems like the lowest-risk way to get Piper into more hands.

2. **Session export**: Would a "share my session" feature be architecturally simple? This could preserve learning loops in a desktop-first world.

3. **SQLite adapter**: The Architect's estimate includes 1-2 weeks for SQLite. Is this blocking, or can we ship MCP-native while SQLite work proceeds in parallel?

---

## Summary

| Original Position | Revised Position |
|-------------------|------------------|
| Hosted-first | MCP-native → Desktop → Hosted |
| M0 is gate | M0 validates capability; user demand validates hosted |
| "Methodology IS product" | Still true, but session export may address it |

M0 success gives us confidence to proceed. The question now is velocity and sequencing, not capability.

---

*Response to: memo-arch-distribution-model-2026-02-16.md*
