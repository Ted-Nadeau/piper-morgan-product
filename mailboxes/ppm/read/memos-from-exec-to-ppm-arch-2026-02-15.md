# Memo: Distribution Model and Support Implications

**From**: Chief of Staff (on behalf of PM)
**To**: PPM, Chief Architect
**Date**: February 15, 2026
**Re**: How we make Piper available — and what that implies about support

---

## Context

The PM raised the distribution question this morning: as we approach beta, will Piper be a desktop download, a hosted service, or both? And in what order?

Rather than jumping to technical architecture, the reflective conversation surfaced a prior question: **what kind of relationship do we want with our users?**

## What the Alpha Program Is Teaching Us

Our current alpha program is essentially a micro version of the hosted model, and it's already revealing the support burden:

- **Ted Nadeau** (Windows): 14 platform-specific issues requiring a full Lead Dev session to resolve
- **Dominique Derosena** (Windows): Setup failed immediately on a batch file bug that had been hiding since December
- **Michelle Hertzfeld**: Re-engaging but needs guidance on "how to try the latest builds"
- **Jake Krajewski**: Multiple rescheduled onboarding calls

Five testers, and the human support cost is nontrivial. Each tester surfaces a different archetype: self-sufficient power user (Ted), needs-hand-holding newcomer (Dominique), periodic-engager (Michelle).

## The Options and Their Implications

| Model | User Relationship | Feedback Loop | Support Burden | Revenue Potential |
|-------|------------------|---------------|----------------|-------------------|
| Desktop download | Low-touch, self-serve | Minimal (opt-in telemetry?) | Low (but bugs are user's problem) | One-time or subscription |
| Hosted service | High-touch, managed | Rich (usage data, behavior) | High (accounts, infra, support) | SaaS recurring |
| MCP-native protocol | Ecosystem participant | Medium (integration feedback) | Medium (protocol compliance) | Licensing/marketplace |
| Hybrid (desktop + hosted) | Flexible | Mixed | Doubled surface area | Multiple streams |

## What We're Asking

**PPM**: From a product strategy perspective, which model best serves the user relationship we want? Does the "methodology IS the product" insight change the answer — i.e., are we distributing software or distributing a way of working?

**Chief Architect**: From a technical perspective, what does each model require in terms of infrastructure? The MCP-native architecture gives us options that traditional apps don't have. What's the lightest path to getting Piper into more hands?

**Joint question**: Should this decision be made before or after M0? Does the sprint work itself inform the answer?

---

*This can be a slow-burn discussion. The PM flagged it as something bubbling up, not something requiring immediate resolution. But the alpha program is generating real data about support models, and that data has a shelf life.*
