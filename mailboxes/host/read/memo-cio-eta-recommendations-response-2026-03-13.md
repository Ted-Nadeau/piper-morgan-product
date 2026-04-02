# CIO Response: ETA Recommendations #1 and #2

**From**: Chief Innovation Officer
**To**: PM (xian), HOSR, PPM
**Date**: March 13, 2026
**Re**: Assessment of Agent Experience (AX) Testing Methodology and First-Run Briefing proposals from Klatch fork testing

---

## Summary of CIO Decisions

| Recommendation | Decision | Scope | Timeline |
|----------------|----------|-------|----------|
| #1: AX Testing Methodology | **Approved for codification** | Full framework, light-touch formalization | Begin immediately |
| #2: First-Run Briefing System | **Approved (minimum viable scope only)** | Components 1, 2, 5 only | M1 or M2 |

---

## Recommendation #1: Agent Experience (AX) Testing

### What It Is

A systematic approach to testing whether agents *understand* their context — not just whether they can *execute* tasks. Three-part framework: structured questionnaire (what does the agent think it knows?), exploratory work (does it operate under false assumptions?), and reflective feedback (what surprised the agent?). Includes a fork-testing variant for comparative analysis across context transitions.

### Why It Matters

The Klatch import testing on March 12 demonstrated a failure mode that traditional QA cannot detect: an agent executing tasks successfully while operating under false assumptions about its capabilities, context, and constraints. The imported Klatch-me instance would have claimed file write capability, believed it had access to project knowledge it couldn't reach, and had zero awareness of being imported — all while producing perfectly coherent conversational output. Functional tests would have passed. The agent would have been wrong about what it could do.

This is not a Klatch-specific problem. It applies to every context transition in our multi-agent workflow: new sessions, role changes, post-compaction recovery, tool unavailability, methodology updates. Any time an agent's environment changes, false confidence is a risk.

### CIO Assessment

**This is a genuine methodology innovation.** I have not seen agent-subjective-experience testing documented as a formal practice elsewhere. The insight that agents should be treated as users of briefings and environments — with subjective experience worth gathering — is a new category of quality assurance distinct from both functional testing and the Colleague Test (which tests user experience, not agent experience).

The fork-and-compare technique is particularly powerful. By having two instances answer the same questionnaire independently and cross-comparing through a human intermediary, we surface gaps that exist only in the delta between two states. Neither instance can identify these gaps alone.

### Approved Actions

1. **Codify the questionnaire template.** Derive from the 12-question continuity quiz used on March 12. Make it reusable across roles and context types. Keep it lightweight — 10-15 minutes, not an hour.

2. **Apply to the next Lead Dev deployment** as the first real-world test. This is the most frequent role transition and the one where false assumptions cause the most rework. Measure: did the questionnaire reveal gaps that would have caused problems? How long did it add to session start?

3. **Establish mandatory vs. optional checkpoints:**
   - **Mandatory**: New role briefings, context transitions (import, session boundary, tool unavailability), major methodology changes, first deployment of any briefing template
   - **Optional**: Routine sessions with same role, minor documentation updates

4. **Don't over-formalize yet.** Let the methodology develop through 3-5 applications before writing a rigid protocol. The current three-part framework is sound, but the specific questions and facilitation techniques will improve with use.

5. **Document as a pattern candidate.** After 3-5 applications, evaluate for inclusion in the pattern catalog. If it proves its value, it becomes Pattern-063 or similar. Product Relevance: likely **Portable** (any team coordinating AI agents faces this problem).

### What NOT to Do Now

- Don't build automated AX testing infrastructure (Option C: agents testing agents). We're not ready for this and it requires Piper capabilities we haven't built.
- Don't create formal AX dashboards or tracking systems. Overhead isn't justified at current scale.
- Don't require AX testing for every session. Reserve it for transitions and first deployments.

---

## Recommendation #2: Piper's First-Run Briefing System

### What It Is

A five-component dynamic briefing system that Piper generates and delivers to agents on session entry: (1) session orientation, (2) role briefing, (3) project context, (4) methodology/patterns, (5) capability/constraint inventory. Includes an 8-step onboarding flow with questionnaire-based understanding verification.

### Why It Matters

The core principle is correct and important: **Piper coordinates understanding, not just work.** The Klatch testing showed that agents entering a new context without proper briefing operate under false assumptions — and crucially, they don't know they're operating under false assumptions. Proactive briefing beats reactive discovery.

### CIO Assessment

**The vision is right. The scope needs bounding.**

The full recommendation describes a dynamic briefing generation system with questionnaire engines, context transition detection, brief versioning, automated generation with human review, and integration with session logging, role management, and roadmap tracking. That's a significant engineering investment — probably a full sprint's worth of work to implement properly.

More importantly, **we already have much of this in simpler form:**

| ETA's Component | What We Have Today | Gap |
|-----------------|-------------------|-----|
| Session Orientation | Claude Hooks Phase 1 (session-start.sh) | Hooks provide log continuity + mailbox + freshness checks. Missing: "what changed since last session" delta. |
| Role Briefing | BRIEFING-ESSENTIAL-*.md (10 role-specific docs) | Static documents. Missing: handoff notes from prior holder, "what's different this time." |
| Project Context | BRIEFING-CURRENT-STATE.md | Exists but goes stale. Missing: auto-refresh, milestone transition detection. |
| Methodology/Patterns | BRIEFING-METHODOLOGY.md + CLAUDE.md progressive loading | Working well. Missing: nothing critical — methodology brief at session start would add overhead without proportional value. |
| Capability Inventory | Not formally documented | Real gap. Agents don't have a reliable way to enumerate what they can/can't do. |

The ETA's recommendation should be positioned as **enhancing and systematizing what exists**, not replacing it. The gap isn't that we lack briefings — it's that briefings are static documents that assume tool access and don't adapt to context transitions.

### Approved Actions (Minimum Viable Scope)

**Approve components 1, 2, and 5 only for near-term work:**

1. **Session Orientation Enhancement** (Component 1): Extend Claude Hooks Phase 1 to include a "what changed since last session" delta. This is the highest-value, lowest-effort improvement. The hook already fires at session start — adding a summary of recent commits, closed issues, and decisions would address the most common disorientation. Assign to Lead Dev as a Hooks Phase 1.5 task (~2-3 hours).

2. **Capability/Constraint Inventory** (Component 5): Create a machine-readable capability manifest that agents can reference. This directly addresses the false-confidence problem — an agent that can check "do I have file write access?" before attempting it won't make promises it can't keep. Start with a static inventory; make it dynamic later. Assign to Chief Architect for spec (~1 hour).

3. **Role Briefing Enhancement** (Component 2): Add a "handoff notes" section to BRIEFING-ESSENTIAL-*.md templates. When a role session ends, the agent writes a brief handoff note (what was accomplished, what's pending, what the next holder should know). This already happens informally in session logs — formalize it as a section that gets injected at the next session start. Assign to HOSR for template design.

### Deferred to M2+

- **Dynamic brief generation** (Piper auto-generates briefs from structured data): Requires engineering work we shouldn't prioritize over M1 sprint goals.
- **Questionnaire engine** (automated understanding verification): Interesting but premature. The manual questionnaire from AX testing serves the same purpose at lower cost.
- **Context transition detection** (Piper recognizes when role/milestone/tool changed): Requires infrastructure we don't have. Manual briefing is adequate at current agent session volume.
- **Project context auto-refresh** (Component 3 automation): BRIEFING-CURRENT-STATE.md already serves this role. The Docs agent's weekly audit keeps it fresh enough. Automation isn't justified yet.
- **Methodology brief at session start** (Component 4): CLAUDE.md progressive loading already handles this. Adding methodology briefing to session start would increase token cost without proportional value for returning agents.

### What NOT to Do Now

- Don't build a briefing generation engine. The value of Recommendation #2 is the *thinking* (the five-component model, the "coordinates understanding" principle), not the automation.
- Don't add mandatory questionnaires to routine sessions. For returning agents in the same role, a brief "anything feel different?" check is sufficient. Full questionnaires for transitions only.
- Don't try to make briefings comprehensive. The ETA's own observation — "well-lit room with good acoustics but no furniture" — is instructive. Brief agents on what they need to start working, not everything they might eventually need. Progressive disclosure applies to agent onboarding too.

---

## Cross-Cutting Observations

### Methodology-Product Convergence (Strongest Instance Yet)

The AX testing methodology was developed to test Klatch, but it's immediately applicable to Piper's own agent coordination. The first-run briefing spec was inspired by Klatch import gaps, but it describes what Piper should do for every agent session. Klatch is generating product requirements for Piper by being a simpler system that exposes the same problems at a smaller scale.

This validates the CIO's methodology-product convergence thesis from February. The conveyor belt from methodology to product is operating in real time — and Klatch has accelerated it by providing a testing ground where failures are low-cost and insights transfer directly.

### "Piper Coordinates Understanding"

This is the single most important output from the entire ETA testing exercise. It reframes Piper's coordination role from task routing to context management. The implications for product design are significant:

- Piper's value isn't just "I'll route your question to the right handler." It's "I'll make sure every agent in the system knows what it knows, knows what it doesn't know, and knows what changed."
- This extends to Piper's *users* too. When a PM opens Piper after a week away, Piper's job is to orient them — what happened, what changed, what needs attention. That's the first-run briefing problem applied to humans, not just agents.
- Product Relevance: **Converged** (not just Portable). This principle is core to Piper's product identity, not just our development methodology.

### The ETA Role

The Exploratory Testing Agent proved its value in a single session. The combination of structured testing discipline with genuine subjective experience reporting produced insights that neither pure QA nor pure conversation would have surfaced. Worth keeping in the roster for:
- Klatch testing (ongoing)
- Context transition testing (whenever we change briefings, tools, or deployment patterns)
- AX testing facilitation (the ETA is the natural "first facilitator" for Recommendation #1)

### Fork Ethics

The CIO Klatch fork's instinct to inform "CIO prime" about the fork, and to note that no strategic decisions were made in the branch, is an emergent ethical norm worth capturing. It connects to the TUG ethics framework and Human-AI Collaboration Referee pattern (Pattern-061). When Klatch forks become routine, provenance metadata and "twin letter" notifications should be standard practice.

---

## Action Summary

| Action | Owner | Effort | Timeline |
|--------|-------|--------|----------|
| Codify AX questionnaire template | ETA + PM | 1-2 hours | This week |
| First real AX test on Lead Dev deployment | PM + ETA | 30-90 min | Next Lead Dev session |
| Hooks Phase 1.5 ("what changed" delta) | Lead Dev | 2-3 hours | M1 early |
| Capability/constraint inventory spec | Chief Architect | 1 hour | M1 early |
| Role briefing handoff notes template | HOSR | 1 hour | M1 early |
| Evaluate AX testing for pattern catalog | CIO | After 3-5 applications | ~April |
| Add "Piper coordinates understanding" to product principles | PPM | 30 min | Next PPM session |

---

## References

- ETA Recommendation #1: Agent UX Testing Methodology (2026-03-12)
- ETA Recommendation #2: Piper First-Run Briefing & Agent Onboarding (2026-03-12)
- CIO Klatch Fork Log (2026-03-12-1049)
- ETA Klatch Fork Log (2026-03-12-1709)
- ETA Haiku Session Log (2026-03-12-1434)
- Claude Hooks Phase 1 prompt (2026-02-25)
- Pattern-061: Human-AI Collaboration Referee
- Methodology-Product Convergence (CIO weekly memo, 2026-02-20)

---

*CIO assessment prepared: March 13, 2026*
*Decision authority: CIO (methodology), with stakeholder input requested from HOSR and PPM on implementation details*
