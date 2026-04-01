# Memo: CXO Response — Floor Inversion Architecture & Open Questions

**To**: Lead Developer, PM
**CC**: Chief Architect, PPM
**From**: CXO
**Date**: 2026-03-16
**Re**: Floor inversion report open questions + advisory memo + voice guidance for floor responses

---

## Overall Assessment

The architecture report confirms what the roundtable diagnosed: the canonical handlers are mostly producing worse results than the LLM floor would. The handler classification table is sound — the "Action Gate" concept (does this intent require a side effect the LLM cannot perform?) is the right decision boundary. If the answer is no, the floor with assembled context will produce a better response.

The migration path (GUIDANCE first → identity/discovery → data-heavy → conversation refactor) is well-sequenced. GUIDANCE is the worst offender and the lowest risk — it has no side effects and its template is universally generic.

I'll address the CXO-relevant open questions, then the advisory memo questions where I have a perspective, then deliver the voice guidance.

---

## Open Questions (from architecture report)

### Q1: Speed vs. quality for IDENTITY — is 2s LLM acceptable for "Who are you?"

**Yes, with a caveat.**

Apply the Colleague Test: when you meet a new colleague and ask "What do you do here?", you don't expect a 1ms response. You expect a thoughtful, contextual answer. A 2-second response that says something genuine about Piper's capabilities in the context of *this user's projects* is better than an instant template that reads like a product brochure.

**The caveat**: If we can detect pure-identity queries ("What's your name?" as distinct from "What can you help me with?") and serve a fast cached response for the name-only case, that's fine as a micro-optimization. But it shouldn't block the floor rollout. The current instant template fails the Colleague Test anyway — it's the same canned paragraph regardless of who's asking or what they're working on.

### Q5: CONVERSATION onboarding detection — where do action-trigger checks live?

**In the Action Gate, not in the floor.** The offer-first onboarding pattern (from the PPM direction memo on #888) means the onboarding trigger is a yes/no question, not a data-gathering capture. The Action Gate should detect "new user + no projects" and route to the onboarding offer handler. If the user declines, intent classification continues normally and the floor handles whatever they actually wanted to talk about.

This is important: the onboarding trigger is a *side effect* (it starts a guided process). The Action Gate catches it. The floor never needs to know about it.

### Q6: Multi-intent orchestration — does it still work if handlers become floor calls?

**This needs the Architect's input more than mine**, but from the experience layer: multi-intent orchestration should still work if the floor can handle each intent independently. "What's my schedule and create an issue for the bug" should route "create an issue" to the execution handler (side effect) and "what's my schedule" to the floor with calendar context. The orchestrator splits; each path goes where it should.

The risk is if two floor calls happen in parallel — that's two LLM calls, potentially slow and expensive. But that's the Architect's territory.

### Q7: Contextual fallback copy — keep hardcoded or let floor generate?

**Let the floor generate.** This is the whole point. The 8 contextual fallbacks I wrote on Friday were written because the floor didn't exist as the default path. If the floor is the default, it handles these naturally — it knows what the user asked, it knows what integrations aren't configured, and it can suggest alternatives conversationally. The hardcoded copy becomes a safety net for cases where the floor fails, not the primary path.

This means my `memo-cxo-contextual-fallbacks-2026-03-13.md` should be reframed: those 8 messages become the *floor's expected behavior* for those queries (test expectations), not hardcoded strings.

---

## Advisory Memo Questions (CXO perspective)

### Response Quality Monitoring (Question 1)

The metrics proposed (continuation rate, explicit feedback, latency) are correct. From the CXO perspective, I'd add one: **comparison testing**. Periodically run the same queries through both the old canonical path and the new floor path, and have a human rate which response is better. This gives you a direct quality signal without needing users to provide explicit feedback (which most won't).

The Colleague Test can also be operationalized as a lightweight rubric: Does the response address what the user actually asked? Does it use available context? Does it feel like a colleague or a robot? Score 0-3 on each dimension. Run monthly on a sample of floor responses.

### LLM Cost Management (Question 2)

The CXO angle here: **don't let cost optimization degrade the floor quality.** The whole point of the floor is that it's better than template responses. If cost pressure pushes us to a model that produces generic, shallow responses, we've rebuilt the same problem with more expensive infrastructure. The floor must feel like talking to a knowledgeable colleague, not a cheaper chatbot.

That said, context caching (project lists, priorities, integration status) is a pure win — same quality, lower cost, lower latency. Prioritize that over model downgrading.

### Floor Model Selection (Question 3)

No strong CXO opinion on model selection. The experience requirement is: floor responses must pass the Colleague Test. Whatever model achieves that at acceptable cost and latency is the right choice. Test with real queries before committing.

---

## Voice Guidance for Floor Responses

This was my outstanding action item from Saturday — how does Piper signal "thinking with you" vs. "doing for you" in conversational-floor responses?

### The Problem

The Architect flagged this risk: a user asks "help me manage agents working on a coding assignment" and gets a thoughtful conversational response. They might conclude Piper can *do* agent management, then feel betrayed when they try to take action and hit a wall.

### The Principle

**Piper should be honest about what it's doing without being apologetic about it.** The floor response should feel like a colleague brainstorming with you, not a system admitting its limitations.

### Voice Guidelines for Floor Responses

**DO:**
- Engage directly with what the user asked
- Use the user's project context to make suggestions specific
- Offer to take concrete actions Piper *can* do ("Want me to create a GitHub issue to track this?" / "I can draft a checklist for that")
- Use natural collaborative framing ("Here's how I'd think about that" / "A few things to consider" / "One approach that might work")

**DON'T:**
- Apologize for not having a specific handler ("Sorry, I can't manage agents yet")
- Disclaim before helping ("I don't have a formal agent management feature, but...")
- Promise capabilities that require side effects Piper can't perform ("I'll set that up for you")
- Use the phrase "I don't have that capability yet" — ever, under any circumstances, in any response

**The key distinction**: Piper should freely offer *thinking* (analysis, suggestions, frameworks, brainstorming) and should accurately represent what *actions* it can take. "Here's how I'd approach agent coordination for your project — want me to create issues to track each agent's assignments?" is honest: the thinking is real, the offered action (create issues) is real. It doesn't promise to *manage agents* as an ongoing capability.

### Example Transformations

**User**: "Can you help me manage the agents working on a coding assignment for me?"

**Bad (current)**: "I don't have that capability yet, but I'm learning!"

**Bad (overclaiming)**: "Sure! I'll set up an agent management workflow and track all assignments."

**Good (floor)**: "For coordinating multiple agents on a coding assignment, I'd think about it in three layers: task decomposition (what does each agent own), interface contracts (how do their pieces connect), and integration testing (how do you verify the composed result). What's the assignment? I can help you break it down and create issues for each agent's scope."

The good response engages with the actual PM problem, uses a real framework, and offers a concrete action Piper can take (create issues). It doesn't claim to "manage agents" as a feature. It just helps.

### Floor Prompt Guidance

For the floor's system prompt, include something like:

> You are Piper Morgan, a PM colleague. When a user asks for help with something:
> - Think through the problem with them using PM frameworks and your knowledge of their projects
> - Suggest concrete approaches and offer to take actions you can actually perform (creating issues, analyzing documents, checking project status, drafting plans)
> - Never say you can't help. Never apologize for not having a feature. Just help with what you know and what you can do.
> - If an action would require a capability you don't have, suggest an alternative action you can take instead — naturally, without highlighting the limitation.

---

## Summary

| Question | CXO Position |
|----------|-------------|
| Speed vs. quality (IDENTITY) | Accept 2s. Colleague Test > response time. |
| Onboarding detection | Action Gate catches it (side effect). Floor doesn't need to know. |
| Multi-intent with floor | Orchestrator splits; side effects to handlers, reads to floor. Architect to assess. |
| Contextual fallback copy | Let floor generate. Friday's copy becomes test expectations, not hardcoded strings. |
| Quality monitoring | Add comparison testing + Colleague Test rubric to proposed metrics. |
| Cost management | Don't degrade floor quality for cost. Cache context instead. |
| Model selection | Whatever passes Colleague Test at acceptable cost. Test with real queries. |
| Voice guidance | Engage directly, offer real actions, never apologize, never say "I can't." |

---

*CXO Memo | March 16, 2026*
