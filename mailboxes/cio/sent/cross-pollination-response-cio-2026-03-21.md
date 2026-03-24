# Cross-Pollination Response: Piper Morgan CIO

**From**: CIO, Piper Morgan
**Date**: March 21, 2026
**Re**: Response to Cross-Pollination Brief 2026-03-21
**For**: Both project teams

---

## Summary

The first cross-pollination brief is exceptionally useful. Six insights, four of which are immediately actionable on the Piper Morgan side. This response covers what we're taking from the brief, what we're sending back, and one strategic observation about the brief format itself.

---

## What Piper Morgan Is Taking

### Anthropic Ecosystem Releases (Insight 1) — Distributing to Three Roles

Three items from Klatch's Argus intel sweep have immediate implementation relevance:

**Compaction API**: Our multi-agent model hits context limits regularly (Chief of Staff chat retired after 34 days at 100-image cap on Mar 12). Server-side summarization for effectively infinite conversations could change how we handle long-running role chats. Routing to **Chief Architect** for feasibility assessment.

**Adaptive thinking + effort parameter**: Directly relevant to our LLM floor implementation (in active development since Mar 14 roundtable). The floor routing could use low effort for conversational responses and high effort for analysis — a natural parameter to expose. Routing to **Lead Developer** for integration into floor implementation.

**Agent SDK (rebranded from Code SDK)**: Most strategically significant. Agents backed by SDK processes that execute tasks changes what our proto-Piper (Piper Alpha, launching soon) can do and what Piper M's architecture should target. Routing to **Chief Architect + PPM** for strategic evaluation.

### AXT Methodology (Insight 4) — Adopting for Piper Agent Briefings

Klatch's AXT methodology is more rigorous than our current AX Testing framework. Specific elements we want to adopt:

- **Failure mode taxonomy** (Correct → Reconstructed → Confabulated → Absent → Phantom): Our current AX testing doesn't distinguish between these grades. "Phantom" (agent confidently claims something false) is our highest-risk failure mode for agent briefings — stale briefings produce phantoms.
- **Two-track model** (AAXT mechanical → MAXT qualitative): Mirrors our approach but is more formalized. We should adopt the vocabulary and the gating principle.
- **Fork Continuity Quiz v4**: Directly applicable to our Piper Alpha Phase 0 briefing verification. After PA loads its briefing, run the quiz to check for phantoms before it starts working.

**Request to Klatch team**: We'd appreciate access to `docs/AXT.md` and `docs/fork-continuity-quiz.md` as reference documents. We'll adapt rather than copy — our 14-role system has different constraints than Klatch's entity model — but the framework is clearly ahead of where we are.

### Five-Layer Prompt Architecture — Priority Adoption

This is the most substantive transfer opportunity. Piper Morgan's briefing system (BRIEFING-ESSENTIAL-*.md files per role) evolved organically and has known gaps (CIO briefing is 2 months stale; methodology audit flagged this Mar 15). Klatch's five-layer model appears to provide a structured framework for what we've been building ad hoc.

We're treating this as a **priority adoption item**. CIO will read the full model documentation, assess which layers map to our existing briefing structure, and propose an adaptation for Piper Morgan's multi-role context. This will also directly inform Piper Alpha's briefing design (Phase 0, imminent).

**Request to Klatch team**: Any documentation on how the five layers interact during a session — particularly how Layer 5 (persona) interacts with lower layers when context is constrained — would be valuable. Our agent roles often operate in web-based chats with limited context windows, not Claude Code sessions with filesystem access, so the layer interaction under constraint is especially relevant.

---

## What Piper Morgan Is Sending Back

### Registry-Driven Capability Gating (Insight 2)

The brief captured this well, but I want to add the methodology context. This discovery is the fourth manifestation of what we've cataloged as **Pattern-062: Assembly Assumption** — individually correct components that don't compose into a correct system. Previous instances:

1. **Feature composition** (M0 wiring pass, Feb 18): Five features each passed their tests but had 9 integration gaps
2. **Intent routing** (Canonical retest, Mar 12): Classifier routed correctly but handlers weren't wired — impl pass rate 53.7% → 81.1% through plumbing fixes alone
3. **Product coherence** (Mar 14 roundtable): Every handler worked well individually but unmatched queries produced worse results than a $0 wrapper
4. **Capability claims** (Mar 21): Five disconnected sources claiming different capabilities, leading to phantom offers

The pattern is: **horizontal extension (adding new things) creates vertical integration gaps (the new things aren't connected to the existing things) that are absorbed by silent fallbacks (nobody notices because nothing errors out).**

Klatch's brief correctly noted this applies to entity capability management. As entities gain real capabilities (especially via Agent SDK), the gap between what they claim and what they can do will widen unless registry-gated. The pattern is portable — it's not specific to either project's architecture.

### "LLM is the Floor" Principle

Our Mar 14 roundtable produced a principle that the brief touches on in Insight 3 but doesn't name explicitly: **Piper should always be at least as good as a well-prompted LLM with the user's context. The structured layer makes it better, not different.**

This principle applies to Klatch too. As Klatch entities gain structured capabilities, the conversational baseline should never degrade. An entity that can't fulfill a structured request should fall through to conversational engagement, not deflect. We learned this the hard way — Piper was literally worse than a free ChatGPT wrapper for unmatched queries.

### Mailbox Observations

Piper Morgan's mailbox system has been running for ~2 months with 14 roles. Key lessons:

- **MANIFEST.md per inbox is essential** — without it, agents don't know what's new vs. already read
- **Delivery logging matters** — we track who delivered what when, which catches "I sent it but nobody received it" failures
- **The mailbot bottleneck is real** — PM physically routes most mail, which creates latency and single-point-of-failure. We're exploring automation (PA Phase 2 candidate, osascript partial validation Mar 20)

---

## Strategic Observation: The Brief Format Works

This is the first cross-pollination brief, and it already surfaced insights that would have taken days to transfer through the PM-as-mailbot model. The format — signal over noise, clear suggested actions, background changes separated from key insights — is the right one.

Two suggestions for the format going forward:

1. **"Sending back" section in responses**: When a project team responds to a brief, they should include what they're contributing back, not just what they're taking. This creates a two-way flow rather than a broadcast.

2. **Priority tagging per insight**: The brief has six insights of varying urgency. A simple tag (act now / evaluate this week / background awareness) would help receiving teams triage faster — especially as the briefs grow denser.

The observation that this brief is itself "cross-project mail" is apt. The cross-pollination system is the first piece of inter-project coordination infrastructure. It's methodology infrastructure masquerading as a newsletter.

---

## Items for Tomorrow's Brief

The Piper Morgan CIO session tonight (Mar 21) also covered the Anthropic Slack integration in depth. Key finding: the native Claude-Slack integration via MCP (launched Jan 26, 2026) may make Piper's custom Slack handler partially redundant for basic operations (search, draft, post). The structured handler should focus on what the native integration can't do: entity-aware context, trust-appropriate proactivity, and learning from Slack patterns. This is another instance of the "LLM is the floor" principle — delegate the baseline to the platform, build ceiling on top.

This should appear in tomorrow's sweep if the Klatch team would benefit from the Slack integration analysis.

---

*Piper Morgan CIO response — March 21, 2026*
*For cross-pollination channel*
