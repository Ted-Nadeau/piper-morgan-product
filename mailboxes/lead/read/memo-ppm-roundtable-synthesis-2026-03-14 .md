# Roundtable Synthesis: "Are We Doing It Backwards?"

**To**: PM (xian)
**From**: PPM (synthesizer)
**Date**: 2026-03-14
**Re**: Synthesis of four leadership memos on conversational floor problem
**Input memos**: PPM, CXO, Chief Architect, CIO — all dated 2026-03-14

---

## Consensus: Unanimous on Diagnosis and Immediate Action

All four memos independently arrived at the same conclusion. I'm not going to soften this: that level of convergence on an uncoordinated question is the strongest signal we've produced since "Governance at Speed" appeared in 4 of 6 Ship #033 memos.

### The Diagnosis (4/4 agree)

Piper's structured routing system treats unmatched queries as dead ends rather than routing them to the LLM for conversational engagement. This makes Piper *worse* than a generic wrapper for any request that doesn't match a pre-built handler — which is the majority of things a PM might ask about.

Each memo frames this slightly differently, and the framings are complementary:

| Role | Framing | Key Phrase |
|------|---------|------------|
| PPM | Layer inversion — we built Layer 1 (handlers) without Layer 0 (conversation) | "We built the flying buttresses while the floor doesn't exist" |
| CXO | Bouncer vs. concierge — classifier acts as gatekeeper instead of router | "The floor must always be 'at least as good as an LLM with context'" |
| Architect | Architectural inversion — LLM used to classify but not to respond | "We spent LLM tokens deciding we can't help, then don't use the LLM to actually help" |
| CIO | Cliff at the boundary — structured side is excellent, unstructured side is worse than nothing | "The LLM is the floor, not the ceiling" |

These aren't four versions of the same idea. They're four perspectives on the same structural problem, each revealing a different facet. The PPM framing (layer inversion) describes the product architecture. The CXO framing (bouncer vs. concierge) describes the user experience. The Architect framing (classify but don't respond) describes the technical waste. The CIO framing (cliff at boundary) describes the strategic risk.

### The Immediate Fix (4/4 agree)

Every memo independently recommended the same one-thing-to-change-first: **route unmatched queries to the LLM with Piper's full context instead of to a deflection message.**

The Architect provided the specific routing change:

```
Current:  UNKNOWN → "I can't do that" (the wall)
Proposed: UNKNOWN → LLM Conversational Response with context (the floor)
```

The Architect also confirmed this is architecturally bounded: one new terminal node in the routing graph, no changes to the dispatch system, pre-classifier, LLM classifier, canonical handlers, or ProcessRegistry.

### The Principle (4/4 agree, slightly different formulations)

All four memos articulate the same principle. The CXO's formulation is the crispest:

**Piper should always be at least as good as a well-prompted LLM with the user's context. The structured layer makes it *better* than that, not *different* from that.**

The handlers are the ceiling. The LLM is the floor. Nothing in the structured system should lower the floor below what a context-aware LLM provides for free.

---

## Where the Memos Diverge (Productively)

### Scope of the fix

The Architect cleanly separates three layers of work:

1. **The floor** (do now): Replace UNKNOWN deflection with LLM response. Architecturally bounded scope — Lead Dev to assess actual engineering effort.
2. **The fallback policy** (define soon): When do structured handlers fall through to the floor vs. returning errors? This is a product design question. PPM and CXO should lead.
3. **The learning vision** (M3+): Piper grows new capabilities from unhandled conversations. PM's screenshot note describes this. Unbounded scope.

All four memos agree on separating these. Nobody is proposing we build the learning system tomorrow.

### Risks worth discussing

The Architect raised four honest concerns that nobody else addressed as directly:

1. **Confidence boundary.** When a handler partially matches but can't complete — does it fall through to the LLM? The fallback policy needs definition. This is the PPM/CXO question for Phase 2.

2. **Expectation management.** A conversational response to "help me manage agents" might set the expectation that Piper *can take action*, leading to frustration when the user tries and hits a wall. CXO should own the framing design — how Piper signals "I can think about this with you" vs. "I can do this for you."

3. **Context quality.** The LLM floor is only as good as the context injected. User profile, project data, conversation history, integration awareness — some exists, some doesn't. A thin-context fallback will feel hollow. This is a real constraint on how good the floor can be on day one.

4. **Slippery slope.** If the LLM floor is good enough, does it undermine the case for structured handlers? The Architect's own answer is right — handlers are *better* because they take actions, integrate tools, maintain state. But this tension is worth naming explicitly for roadmap prioritization.

### The CIO's connections

The CIO draws lines to three recent threads: Amodei's "Day 100 agent" (learning over time vs. one-shot), the AX testing "coordinates understanding" principle, and the Assembly Assumption. The Assembly Assumption connection is the most pointed: the unhandled-query path is a composition gap. Each handler works correctly for its domain. The intent classifier works correctly for known categories. The composition of "classifier + handlers + no fallback" produces a broken experience.

---

## What's Not in These Memos (and Might Matter)

**Lead Dev perspective.** The Lead Dev wasn't in this roundtable. They will need to assess: how does `_handle_generic_query` currently work? What context does it receive? How much effort to make it good vs. making it exist? The Architect's routing diagram suggests it's bounded, but the Lead Dev has ground truth.

**Alpha tester data.** We don't actually know how often users are hitting the wall today. The canonical retest tested specific queries — we know 19% of implemented queries fail. But we don't know what percentage of *real user queries* fall outside all handlers. If it's 5%, the floor matters less urgently. If it's 50%, it's an emergency. We should instrument this.

**Piper's voice in unstructured contexts.** The CXO's question from this morning's hijack memo applies here too: does Piper's personality system work well in open-ended conversation? The handlers have structured response patterns. The LLM floor would need Piper to be Piper without the scaffolding. That might need prompt work.

---

## Recommended Actions

### Immediate (this sprint)

1. **File an issue for the LLM conversational floor.** This is the routing change: UNKNOWN → LLM response with context. The Architect confirmed it's architecturally bounded. I'd recommend it enters M1 as a high-priority addition — it arguably has more user impact than any single handler fix currently in the sprint.

2. **Non-negotiable constraint: The LLM floor operates within Piper's existing ethical framework.** The fallback path must route through the same CORE ethics, trust computation, and boundary checking pipeline as structured handlers. It must not bypass these layers. This is an acceptance criterion for the implementation, not an enhancement. Without this, the conversational floor becomes a jailbreak vector — the path of least resistance for a fast implementation is a direct LLM call that skips the ethics pipeline. That must not happen.

3. **Non-negotiable constraint: The LLM floor reasons conversationally — it does not take actions or call integrations.** The floor is "Piper thinking with you." Structured handlers are "Piper doing things for you." This constraint keeps the floor's scope bounded and preserves a clear distinction between conversational reasoning and capability execution. If the floor starts calling APIs, we've introduced a different category of problem.

4. **Codify the principle.** "Piper is always at least as good as a well-prompted LLM with context. Structured handlers make it better, not different." This goes into PDR-001 alongside the other pending addenda (session ownership, offer-first, coordinates understanding). These four principles are cohering into a product philosophy update.

### Soon (this sprint or next)

5. **Define the fallback policy.** When does a structured handler fall through to the LLM floor? PPM and CXO to draft, Architect to review for feasibility. This is the Architect's "Layer 2" question and it has real design implications.

6. **CXO to draft voice guidance for conversational-floor responses.** How does Piper distinguish collaborative thinking from capability promises in unstructured contexts? This addresses the Architect's expectation management risk — without clear voice guidance, a conversational response to "help me manage agents" could set the expectation that Piper can take action, leading to frustration. CXO owns this.

7. **Instrument the wall.** How often are users hitting UNKNOWN today? What are they asking? This data should drive handler prioritization — build handlers for the things users actually ask about, not the things we imagine they'll ask about. If we add the LLM floor and instrument it, we get both the fix and the signal for what to build next — the learning loop starts operating informally even before we build it formally.

### Later (M2–M3)

8. **The learning intake loop.** PM's screenshot note vision: Piper notices capability gaps, attempts via LLM, observes what worked, drafts new skills. This is the "Day 100 agent" trajectory. It depends on the floor existing first.

---

## The Bigger Reflection

PM asked "are we doing it backwards?" All four of us said: partly yes. We built ceiling infrastructure without the floor. That's not a catastrophe — the ceiling work is real and valuable. But we need to pour the floor now, before the ceiling work matters to anyone except us.

The encouraging part: this is fixable. One routing change establishes the floor. The structured system we've built becomes the enhancement layer on top of it. Everything we've built gets *more* valuable, not less, once the floor exists — because users will actually stay long enough to encounter the structured handlers.

The CIO's connection to Pattern-062 (Assembly Assumption) is apt. We're discovering at the product level what we discovered at the technical level during M0: individually correct components don't guarantee a correct composition. The classifier is correct. The handlers are correct. The composition produces an incorrect experience for unmatched queries.

The fix follows the same pattern as M0: identify the composition gap, wire it, verify.

---

*PPM Synthesis | March 14, 2026*
*Input: 4 roundtable memos (PPM, CXO, Architect, CIO)*
*Revised: March 14, 2026 — incorporated feedback from CIO (ethics constraint), Architect (scope correction, no-actions constraint), CXO (voice guidance action, instrumentation emphasis)*
