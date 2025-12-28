# Piper Morgan UX Strategy: A Synthesis

**Document Type**: Strategic UX Recommendations
**Date**: November 26, 2025
**Author**: CXO Session (Opus)
**Inputs**:
- "Piper Morgan: UX Foundations and Open Questions" (Internal)
- "UX Patterns and Design Challenges for LLM and AI Interfaces" (Research Synthesis)

---

## Executive Summary

This document synthesizes Piper Morgan's philosophical foundations and existing architecture with current industry research on AI/LLM interface design. The goal is to produce actionable recommendations: what Piper must do, should avoid, and where opportunities exist.

**Core finding**: Piper's existing commitments—the colleague metaphor, systematic kindness, 8-dimensional spatial intelligence, ethical boundary layer—position it to address many of the challenges the industry is still grappling with. The research validates our philosophical direction while surfacing specific implementation patterns and cautionary findings.

**Strategic posture**: Piper should be **opinionated by default, transparent on request, and progressively autonomous as trust is earned.** This maps to the research finding that hybrid approaches (not pure automation, not pure manual control) consistently outperform extremes.

---

## Part I: Trust and Calibration

### Industry Insight

The research reveals a fundamental tension: transparency helps trust calibration but doesn't necessarily improve decision outcomes. Users oscillate between automation bias (over-reliance) and algorithm aversion (under-reliance), often triggered by observing AI errors. The ideal—"algorithmic vigilance"—remains largely unrealized.

Key patterns:
- Confidence displays help calibration (numeric, categorical, visual, linguistic)
- Explanations should be user-centric, not completeness-oriented
- Users need consistent visual indicators of AI presence
- Efficient correction mechanisms matter more than perfect initial output

### Application to Piper

Piper's **apprentice progression model** directly addresses the automation bias → disappointment → aversion cycle. By starting humble and earning trust gradually, Piper avoids the "I can do ANYTHING!" trap that leads to acute disappointment.

The **ethical boundary layer** with multi-agent consensus provides natural explanation infrastructure—when Piper declines or constraints something, the reasoning is already captured.

### Recommendations

| Category | Recommendation | Rationale |
|----------|---------------|-----------|
| **MUST DO** | Implement trust levels visible to user | Users need to know where they are in the relationship |
| **MUST DO** | Provide reasoning on request (not by default) | Research shows transparency helps but creates cognitive load; make it available without forcing it |
| **SHOULD DO** | Use linguistic hedging over numeric confidence | "I think" and "This might be" feel natural for colleague metaphor; numeric probabilities feel robotic |
| **SHOULD AVOID** | Claiming capabilities Piper hasn't demonstrated | The trust gradient requires demonstrated competence before expanded autonomy |
| **OPPORTUNITY** | "Show your work" expandable sections | Like Claude's extended thinking—available for users who want it, collapsed for those who don't |

### Open Questions Resolved

**Q: How much should be visible by default vs. on request?**
**A**: Default to confident-but-hedged output. Offer "show reasoning" on request. This maps to the colleague metaphor—a good colleague shares conclusions, explains if asked, doesn't preface everything with methodology.

---

## Part II: Conversation vs. Artifact

### Industry Insight

The field is converging on separating artifacts from conversation while maintaining iterative refinement through dialogue. Key patterns:
- Threshold-based triggering (substantial, self-contained, likely-to-be-edited)
- Universal version control
- Artifacts as separate processing from chat

But approaches diverge on:
- Auto-generate vs. model-decides vs. manual trigger
- Predefined types vs. any interface
- Standalone structure vs. gradual enrichment (Ink & Switch)

### Application to Piper

Piper's commitment to **"outputs to elsewhere"** is validated—no major system tries to trap artifacts inside the AI. Claude Artifacts, Canvas, and Generative UI all produce things that can be exported/used elsewhere.

The **"generative not consumptive"** principle aligns with Ink & Switch's research: documents evolving into interactive software, gradual enrichment, notes becoming apps.

Piper's **plugin architecture** for specialized tools (ChatPRD for PRDs, etc.) is strategically sound—the research shows no single system tries to do everything.

### Recommendations

| Category | Recommendation | Rationale |
|----------|---------------|-----------|
| **MUST DO** | Maintain clear separation between conversation and artifacts | Industry consensus; mixing them creates confusion |
| **MUST DO** | Artifacts output to user's ecosystem (GitHub, Notion, Slack, etc.) | Radar O'Reilly principle—meet users where they are |
| **SHOULD DO** | Implement working drafts (scratchpad space) | Users need temporary space; not everything is permanent artifact |
| **SHOULD DO** | Version control for significant artifacts | Universal pattern; essential for iteration |
| **SHOULD AVOID** | Creating Piper-specific artifact storage that competes with user's tools | Violates ubiquity principle; creates migration friction |
| **OPPORTUNITY** | "Gradual enrichment" pattern from Ink & Switch | Documents that evolve from notes → structured → interactive |

### Open Questions Resolved

**Q: What does Piper produce? What are the artifacts of PM work?**
**A**: Roadmaps, user stories, decision logs, status updates, retrospectives, stakeholder communications, requirement specs, sprint plans. Piper helps create these but outputs to user's existing systems. Piper's internal objects are working drafts, not final destinations.

---

## Part III: Agency and Control

### Industry Insight

Victor Dibia's four principles provide a strong framework:
1. **Capability discovery**: Users need to know what's possible
2. **Observability**: Users need to see what's happening
3. **Interruptibility**: Users need to stop/redirect actions
4. **Cost-aware delegation**: Risk classification for automatic vs. approval-required

The Knight First Amendment five-level autonomy model (Operator → Collaborator → Consultant → Approver → Observer) maps well to the apprentice progression.

Critical finding: System-initiated delegation increases perceived self-threat and decreases willingness to accept delegation. The effect amplifies when users perceive less control.

### Application to Piper

The **apprentice progression** (responds when asked → anticipates and asks → offers to automate → proposes improvements) maps directly to the five-level autonomy model, run in reverse: Piper starts at Operator (user controls) and can progress toward Observer (Piper has autonomy) as trust is earned.

The research finding about system-initiated delegation validates the distinction we drew:
- "I noticed your standup is in 10 minutes" (observation) ✓
- "Want me to prepare your standup?" (offer) ✓
- "I prepared your standup for you" (action) ✗ (without earned trust)

### Recommendations

| Category | Recommendation | Rationale |
|----------|---------------|-----------|
| **MUST DO** | Implement all four Dibia principles | Capability discovery, observability, interruptibility, cost-aware delegation are baseline |
| **MUST DO** | Default to observation + offer, not action | Research shows unsolicited action creates self-threat |
| **MUST DO** | Make trust level explicit and user-controllable | Users need agency over the autonomy gradient |
| **SHOULD DO** | Risk-classify actions (low/medium/high) | Automatic for low-risk, approval for medium, explicit authorization for high |
| **SHOULD AVOID** | Jumping trust levels based on single successes | Trust builds slowly, erodes quickly |
| **OPPORTUNITY** | "Teach me to do this" mode | User can explicitly grant trust for specific patterns |

### Open Questions Resolved

**Q: Where on the proactive/reactive spectrum does Piper sit by default?**
**A**: Observe and offer. Never act without explicit authorization until trust is earned for that specific action type. The colleague who keeps offering to take over is annoying; the colleague who notices and mentions is helpful.

**Q: Can trust be explicitly granted/revoked?**
**A**: Yes. Trust should be visible ("Piper currently at Level 2 for standup tasks") and user-controllable ("Grant Level 3 for this" or "Reset to Level 1").

---

## Part IV: Memory and Continuity

### Industry Insight

Memory systems remain immature. Key findings:
- Users have incomplete mental models of how AI remembers
- Users conceptualize memory hierarchically (general → specific)
- Users desire "cleanly organized by categories"
- ChatGPT's February 2025 catastrophic memory failures (83% failure rate) show infrastructure fragility
- Claude uses file-based markdown (not vector databases), trained not to proactively remember sensitive info

The Letta/MemGPT approach offers interesting patterns:
- Two-tier memory (in-context editable + out-of-context archival)
- Self-editing memory via tools
- "Heartbeat" mechanisms and "sleep-time agents"

### Application to Piper

The **dreaming model** (filing dreams for cross-referencing, anxiety dreams for risk simulation) aligns with research directions but goes further than current implementations. Most systems only add to memory; the research identifies forgetting as an underdeveloped area.

**Session logging** as standard practice maps to the need for auditable, retrievable work records.

The **trust gradient** interacts with memory: early Piper has little material for pattern recognition; later Piper has rich history for cross-referencing and simulation.

### Recommendations

| Category | Recommendation | Rationale |
|----------|---------------|-----------|
| **MUST DO** | Visible memory with user control | Users need to see what Piper remembers and edit/delete |
| **MUST DO** | Session logging as core infrastructure | Auditability, handoff, and dreaming substrate |
| **MUST DO** | Project-scoped memory isolation | Research validates this (Claude does it); prevents context bleed |
| **SHOULD DO** | "Dreaming" as background cross-referencing | Filing dreams: connect today's work to historical patterns |
| **SHOULD DO** | "Dreaming" as risk simulation | Anxiety dreams: game out potential problems |
| **SHOULD AVOID** | Proactive memory without consent | Claude trained not to remember sensitive info unless asked |
| **OPPORTUNITY** | "Forget this" and temporary modes | Research identifies forgetting as gap; users need scratch space |
| **OPPORTUNITY** | Memory decay for stale patterns | Most systems only add; pruning outdated patterns could improve quality |

### Open Questions Resolved

**Q: When does Piper "sleep"?**
**A**: Between sessions and/or on schedule. "Sleep" is when background processing happens—not real-time with user, but before next session.

**Q: Are dream outputs visible?**
**A**: The *results* are visible (improved pattern recognition, proactive observations). The *process* is available on request ("Why did you connect these?") but not forced on user.

**Q: How does dreaming relate to trust gradient?**
**A**: Early Piper has limited dreaming material. As history accumulates, dreaming becomes more valuable. This is natural—an apprentice on day 1 has little to cross-reference; after 6 months, they have rich pattern material.

---

## Part V: Articulation Barrier

### Industry Insight

Nielsen's finding is stark: ~50% of adults in advanced countries qualify as low-literacy users. "Low-articulation users" exceed that number. Prompt engineering as a profession signals interface failure.

Patterns that help:
- Style galleries (recognition over recall)
- Prompt rewrite (editing easier than creation)
- Related prompts / follow-up suggestions
- Prompt builders (structured templates)
- Hybrid interfaces (text + GUI)
- Voice mode (captures nuance, but interruption issues)

Key tension: Hiding complexity (accommodation) vs. building capability (teaching).

### Application to Piper

The **canonical queries as recognition interface** directly addresses this. Piper demonstrates what it understands; user recognizes and selects. This inverts the traditional pattern where user must articulate and AI responds.

**"Piper articulates, user recognizes"** maps to the style gallery pattern—showing options rather than requiring specification.

The **trust gradient** interacts here: early Piper offers more explicit options; later Piper can operate on briefer cues because shared vocabulary is established.

### Recommendations

| Category | Recommendation | Rationale |
|----------|---------------|-----------|
| **MUST DO** | Canonical queries as primary interface | Piper presents what it can do; user selects. Recognition > articulation |
| **MUST DO** | "What can you help with?" produces actionable list | Core capability discovery; addresses Nielsen's concern |
| **SHOULD DO** | Related/follow-up suggestions after each interaction | Research shows doubled engagement (Perplexity pattern) |
| **SHOULD DO** | Hybrid interface (conversational + structured when helpful) | Text preserves flexibility; GUI shows what's possible |
| **SHOULD AVOID** | Requiring precise commands or syntax | Prompt engineering = interface failure |
| **OPPORTUNITY** | Voice mode for lower articulation barrier | Speaking is easier than writing for many users |
| **OPPORTUNITY** | Progressive vocabulary building | As trust builds, Piper can respond to shorter cues; shared vocabulary develops |

### Open Questions Resolved

**Q: Is Piper a teaching tool or a doing tool?**
**A**: Both, at different stages. Early Piper teaches by demonstrating (canonical queries, capability discovery). As shared vocabulary builds, Piper becomes more doing-focused because user knows how to direct it efficiently. The trust gradient IS the teaching → doing progression.

---

## Part VI: Agent Interfaces and Ubiquity

### Industry Insight

Agent UX is rapidly evolving. Key patterns:
- Supervisor/worker architecture dominates (orchestrator + specialized workers)
- Visual feedback loops for real-time agent actions
- Pause/resume/cancel capabilities
- Event-driven asynchronous processing
- Durable execution (crash recovery)

Challenges:
- Cost communication UX underdeveloped
- Multi-agent debugging difficult
- Cross-platform handoffs (MCP helping here)
- Long-running state (days/weeks) largely unsolved

### Application to Piper

Piper's **MCP federation** positions it well for cross-platform presence. The architecture already assumes Piper can manifest in multiple contexts (Slack, CLI, Web, email).

The **Radar O'Reilly principle** (presence, not destination) aligns with emerging agent patterns where AI appears in context rather than requiring dedicated interfaces.

The **multi-agent ethical board** is itself an agent coordination pattern—Piper already orchestrates internal agents.

### Recommendations

| Category | Recommendation | Rationale |
|----------|---------------|-----------|
| **MUST DO** | Consistent identity across channels | User interacts with Piper in Slack, CLI, Web—should feel like same colleague |
| **MUST DO** | Context handoff between channels | Start conversation in Slack, continue in web—Piper remembers |
| **MUST DO** | Interruptibility across all contexts | User can pause/stop Piper regardless of where initiated |
| **SHOULD DO** | Channel-appropriate interaction modes | Slack = brief and immediate; Web = deeper exploration; CLI = power user |
| **SHOULD AVOID** | Channel lock-in | Don't force users to specific channel for specific capabilities |
| **OPPORTUNITY** | Progressive channel expansion | Start with core channels, add more as Piper matures |
| **OPPORTUNITY** | MCP as ubiquity substrate | Other tools calling Piper (not just Piper calling tools) |

### Open Questions Resolved

**Q: Does Piper need its own interface?**
**A**: Yes, but not as primary. Piper's web interface is for deeper exploration, configuration, and direct engagement—when user *chooses* to go to Piper. But primary use is Piper manifesting in user's existing contexts.

---

## Part VII: Non-Determinism and Reliability

### Industry Insight

Genuinely novel challenge: LLMs are non-deterministic even at temperature=0. Research found up to 15% accuracy variation across runs, with best/worst gaps up to 70%. Root cause: batch variance in GPU processing, not just floating point.

Tensions:
- Creative applications benefit from variability
- Critical applications demand reproducibility
- Audit trails require traceable decisions
- User mental models assume determinism

### Application to Piper

Piper's commitment to **transparency, auditability, legibility** creates tension with inherent non-determinism. The **ethical boundary layer** requires traceable decisions.

The **session logging** practice helps—even if outputs vary, the reasoning and process are captured.

### Recommendations

| Category | Recommendation | Rationale |
|----------|---------------|-----------|
| **MUST DO** | Log all decisions with reasoning | Auditability requires traceability even when outputs vary |
| **MUST DO** | Ethical boundary decisions must be reproducible | Non-negotiable for trust; may require deterministic override layer |
| **SHOULD DO** | Default to lower temperature for PM tasks | Consistency matters more than creativity for professional work |
| **SHOULD DO** | "Regenerate" option when output unsatisfactory | Variability as feature, not bug, for optional retries |
| **SHOULD AVOID** | Promising exact reproducibility | Can't guarantee; don't overpromise |
| **OPPORTUNITY** | "Creative mode" toggle for ideation tasks | Higher temperature for brainstorming, lower for execution |

### Open Questions Resolved

**Q: How does non-determinism affect auditability?**
**A**: Log inputs, reasoning, and outputs—all three. Even if running same input twice produces different output, the reasoning chain is captured. For ethical boundaries, implement deterministic enforcement layer that doesn't depend on LLM output.

---

## Part VIII: Multi-Modal Integration

### Industry Insight

The field is moving toward integrated multi-modal experiences:
- ChatGPT Advanced Voice Mode: natively multimodal, captures emotional nuance
- Google Nest Hub: eight ML models simultaneously, no wake words needed
- BMW: "Act, Locate, Inform" principle across displays

Challenges:
- Context retention across modalities
- Discoverability (voice lacks visible affordances)
- Error recovery when modalities conflict
- Privacy concerns (always-listening)

### Application to Piper

Piper's **ubiquity aspiration** implies multi-modal presence eventually. If Piper is in Slack (text), meetings (voice), and documents (embedded), modality integration matters.

The **Radar O'Reilly pattern** is inherently multi-modal—Radar appears however is appropriate to context.

### Recommendations

| Category | Recommendation | Rationale |
|----------|---------------|-----------|
| **MUST DO** | Text-first, other modalities as enhancement | Text is most accessible, most controllable, most auditable |
| **SHOULD DO** | Explore voice for input (lower articulation barrier) | Speaking easier than writing for many users |
| **SHOULD AVOID** | Voice-only interactions for important decisions | Need text record; voice ephemeral |
| **SHOULD AVOID** | Always-listening without explicit consent | Privacy and trust concerns |
| **OPPORTUNITY** | Meeting presence (listen and summarize with permission) | Natural extension of Radar O'Reilly pattern |
| **FUTURE** | Visual interface for complex spatial displays | 8D intelligence might benefit from visualization |

### Open Questions Resolved

**Q: What multi-modal patterns matter for ubiquity?**
**A**: Context handoff across modalities (start in voice, continue in text). Channel-appropriate interaction (brief in Slack, deeper in web). Text as anchor with other modalities as enhancement.

---

## Part IX: Strategic Synthesis

### Piper's Competitive Positioning

The research reveals that no existing product fully embodies the "colleague who inhabits your workspace" vision:
- ChatGPT/Claude: Destination, not presence
- Copilots (GitHub, Microsoft): Present in context but narrowly scoped
- Agent frameworks: Technical infrastructure, not colleague experience
- PM tools: Traditional software, not AI colleagues

**Piper's differentiation**: Combining spatial intelligence (understands context across 8 dimensions), ethical boundaries (trustworthy by architecture), colleague metaphor (earns autonomy over time), and ubiquitous presence (manifests where user works).

### Priority Sequence

Based on research findings and Piper's foundations, recommended implementation sequence:

**Phase 1: Trust Foundation**
1. Visible trust levels with user control
2. Canonical queries as recognition interface
3. Session logging infrastructure
4. Consistent identity across current channels (Slack, CLI, Web)

**Phase 2: Memory and Continuity**
5. Project-scoped memory with user visibility
6. Context handoff between channels
7. Working drafts / scratchpad functionality
8. Basic dreaming (filing-type cross-referencing)

**Phase 3: Autonomy Progression**
9. Risk classification for actions
10. "Teach me to do this" trust granting
11. Scheduled/automated pattern execution (with earned trust)
12. Anxiety-type dreaming (risk simulation)

**Phase 4: Ubiquity Expansion**
13. Additional channel integrations
14. Voice input exploration
15. Meeting presence (with permission)
16. MCP server mode (other tools consuming Piper)

### Success Metrics

| Dimension | Metric | Target |
|-----------|--------|--------|
| Trust | Users grant Level 3+ trust within 30 days | 60% |
| Articulation | Users successfully complete tasks without syntax errors | 95% |
| Ubiquity | Users engage via 2+ channels | 70% |
| Retention | Users return within 7 days of first session | 80% |
| Satisfaction | "Feels like a colleague" rating | 4.5/5 |

---

## Part X: What This Means for Immediate Work

### UX Design Implications

1. **Onboarding**: Demonstrate canonical queries; let user recognize what Piper can do rather than requiring articulation
2. **First Interaction**: Piper orients itself ("Here's what I notice..."), not user orienting Piper
3. **Trust Display**: Visible indicator of current trust level and what would unlock next level
4. **Memory Transparency**: "What do you remember about me?" produces clear, editable list
5. **Channel Consistency**: Same personality, adapted expression across Slack/Web/CLI

### Architecture Implications

1. **Trust Level Storage**: Per-user, per-action-type trust levels with history
2. **Canonical Query Handlers**: Complete implementation across all 5 categories
3. **Memory Architecture**: Session logs + project memory + cross-referencing infrastructure
4. **Channel Adapters**: Unified Piper identity with channel-appropriate expression

### Interaction Design Implications

1. **Default Posture**: Observe → Offer → (wait for acceptance) → Act
2. **Error Handling**: Intent recovery, not error messages
3. **Explanation**: Available on request, not forced
4. **Interruption**: Always possible, always graceful

---

## Appendix: Research-to-Piper Mapping

| Research Finding | Piper Application |
|-----------------|-------------------|
| Automation bias → disappointment → aversion cycle | Apprentice progression prevents initial over-promise |
| System-initiated delegation creates self-threat | Observe + offer, not unsolicited action |
| ~50% users have articulation difficulty | Canonical queries as recognition interface |
| Transparency helps calibration but adds cognitive load | Available on request, not forced |
| Artifacts should be separate from conversation | Outputs to elsewhere principle validated |
| Users want "cleanly organized" memory | Hierarchical project-scoped memory |
| Forgetting is underdeveloped area | "Forget this" and memory decay as opportunity |
| Consistent visual indicators of AI presence | Same Piper identity across channels |
| Non-determinism at temperature=0 | Deterministic ethical layer + reasoning logs |
| Voice lowers articulation barrier | Future opportunity for input mode |

---

*This synthesis provides the strategic foundation for Piper Morgan's UX development. Individual features will require detailed design, but the philosophical and architectural direction is now grounded in both internal commitments and industry learning.*

---

**Document Status**: Complete
**Next Steps**:
1. Review with PM for alignment
2. Identify immediate implementation priorities
3. Create detailed design briefs for Phase 1 features
