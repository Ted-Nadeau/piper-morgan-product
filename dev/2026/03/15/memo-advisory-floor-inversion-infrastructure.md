# Advisory Memo: Infrastructure Questions for Floor Inversion (#911)

**From**: Lead Developer (Claude) & PM (xian)
**To**: Leadership / Advisory
**Date**: 2026-03-15
**Re**: Three infrastructure decisions we'd like input on before scaling the floor-first architecture

---

## Context

We're inverting Piper's response routing so the conversational floor (LLM-generated responses) is the **default** rather than the last resort. Currently, most user messages hit template-based canonical handlers that return boilerplate regardless of what the user actually said. The floor — which reads the message and responds thoughtfully — produces better results but is only reached when everything else fails.

The architectural change is straightforward and already supported by our design docs (PDR-002, ADR-039). We're proceeding with implementation. However, three infrastructure questions sit outside our core competency and we'd value expert input before we scale beyond Phase 1.

**Attachments**: Full architecture investigation report at `dev/2026/03/15/floor-inversion-architecture-report.md`

---

## Question 1: Response Quality Monitoring

**The problem**: Once the floor generates most responses, how do we know if they're good? Template responses are predictably mediocre. LLM responses are unpredictably good-or-bad. We need a quality signal.

**Our current thinking**:
- Conversation continuation rate (user sends another message vs. abandons)
- Explicit feedback mechanism (thumbs up/down on responses)
- Floor response latency tracking (already instrumented via `floor_hit` flag)

**What we'd like input on**:
- Are there established patterns for LLM response quality monitoring in production?
- Should we build a lightweight eval framework, or is there an off-the-shelf approach worth adopting?
- What metrics actually correlate with user satisfaction in conversational AI?

**Urgency**: Low. We can ship Phase 1 without this. Becomes important as we scale to all categories.

---

## Question 2: LLM Cost Management & Caching

**The problem**: Under the old architecture, most responses were free (templates). Under floor-first, every message requires an LLM call for response generation (in addition to the existing classification call). This roughly doubles our per-message LLM cost.

**Our current thinking**:
- Context assembly results could be cached (project lists, priorities don't change per-request)
- Some responses could use a smaller/cheaper model (identity questions, simple acknowledgments)
- A locally-running LLM for routine classification could reduce API costs significantly

**What we'd like input on**:
- Is local LLM inference (e.g., Ollama, llama.cpp) mature enough for production classification workloads?
- What's the right caching layer for assembled context? Redis (already in our stack) with TTLs per data type?
- At what scale does cost optimization become urgent vs. premature?

**Urgency**: Medium. Current usage is low (alpha), but architecture decisions now affect cost trajectory.

---

## Question 3: Floor Model Selection

**The problem**: The floor currently uses whatever model the intent service is configured with. For response generation (as opposed to classification), we could potentially use a different model — faster, cheaper, or better suited for conversation.

**Our current thinking**:
- Classification needs precision (correct category/action) — may benefit from a stronger model
- Response generation needs fluency and context-awareness — could potentially use a lighter model with good prompting
- A two-model approach adds operational complexity

**What we'd like input on**:
- Is a split-model architecture (strong for classification, light for generation) common in practice?
- What are the operational gotchas (version drift, prompt compatibility, failover)?
- Any model recommendations for conversational response generation specifically?

**Urgency**: Low. Single-model works fine for now. Worth thinking about before scaling.

---

## What We're NOT Asking About

For clarity, we're confident in and proceeding with:
- The floor-first architectural approach (design docs support it)
- Quality over speed trade-off (product ethos)
- The phased migration path (GUIDANCE first, then expand)
- Handler classification (which handlers keep canonical routing vs. go to floor)

These three questions are about scaling infrastructure, not product direction.

---

_Prepared by Lead Developer, 2026-03-15. See #911 for full implementation plan._
