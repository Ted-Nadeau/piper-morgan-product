# Extension Without Integration

*March 26, 2026*

[alt text: PLACEHOLDER — cartoon TBD]

*March 13–19*

Six features. Each one correct. Each one tested. Each one reviewed and approved. And together, they produced chaos.

We discovered the pattern while investigating a conversation continuity bug. A user would say "Sure" after Piper offered to help, and instead of continuing the conversation, Piper would treat it as a brand-new query. Not a hard bug to describe. But the root cause took three days to surface.

Three independent systems were each listening for user acceptance. One was built for onboarding (#824). One for workflow hijack recovery (#888). One for soft capability offers (#852). Each had its own detection logic. Each worked correctly in isolation. Each passed its tests.

When they ran simultaneously — which is to say, always — four competing detection points raced to interpret "Sure." The onboarding system thought the user was accepting onboarding. The soft offer system thought they were accepting a capability offer. The workflow system thought they were resuming a suspended session. The user just meant "yes, help me with that."

## The pattern

Our Lead Developer named it after auditing the codebase and finding six instances of the same structural flaw:

Features get extended independently. Each extension has its own issue, its own acceptance criteria, its own tests. Each one passes review. Nobody tests how they compose.

This isn't a testing failure. The tests were correct — each feature did what it said it would do. It's a *composition* failure. The acceptance criteria for each feature asked "does this feature work?" but never asked "does this feature work when the other five are also running?"

[CHRISTIAN TO POLISH: Does this resonate with your experience on other projects? The pattern seems universal — is there a way to connect it to traditional software teams, not just multi-agent development?]

## Why multi-agent development makes it worse

In a traditional team, developers share a codebase, sit in the same standup, and sometimes notice when their work overlaps. The collision is accidental but detectable through proximity.

In multi-agent development, each agent works in its own session with its own context window. Agent A builds the onboarding flow on Tuesday. Agent B builds the soft offer system on Thursday. Agent C fixes the workflow hijack the following week. None of them sees the others' work in their context. None of them knows to test the combination.

The agents aren't wrong. They're doing exactly what was asked. The gap is structural — it lives between the issue descriptions, not inside them.

[ADD PERSONAL REFLECTION: You've described the PM role as "mailbot" — routing work between agents. Does this pattern suggest the routing needs to include integration context? Or is the fix at a different layer entirely?]

## The fix has two layers

The immediate fix for our bug was architectural: consolidate the three acceptance systems into a single workflow dispatcher. One detection point, one registry, one routing decision. ADR-059, written, reviewed, and implemented in a single morning.

But the meta-fix is recognizing the pattern *before* it ships. Every feature that touches a shared pipeline — in our case, the offer/classification/handler chain — needs integration acceptance criteria. Not "does this feature work?" but "does this feature work in a multi-turn conversation where the other features are also active?"

We added two practices:

First, **composition tests**: multi-turn conversation scenarios that exercise feature combinations. Not just "start onboarding" but "start onboarding, change your mind, ask about projects, get offered a capability, accept it." The features need to share a conversation, not just share a codebase.

Second, **composition audits at milestone boundaries**: before closing a sprint gate, audit every feature that touches the pipeline and verify they've been tested together. Not a full regression — a focused check on the interaction points.

[CONSIDER: Is there a useful analogy here? Musical instruments that each play the right notes but aren't in the same key? Ingredients that are each fine but don't combine into a meal? Or is the technical description clearer without the metaphor?]

## The broader lesson

This pattern isn't specific to AI agents. It's what happens when any team builds features in parallel — microservices teams, platform teams, any organization where different people own different parts of the same user experience. The features work. The tests pass. The composition fails.

What's different in multi-agent development is the *speed* at which the pattern emerges. When you can build a complete feature in a single session, you can accumulate six independently correct but mutually incompatible features in a week. Traditional teams might take months to reach the same state. Multi-agent velocity compresses the feedback loop — which means you hit the composition wall faster.

The good news is that the detection cycle is also faster. Our audit cascade identified six instances, diagnosed the structural cause, and implemented the architectural fix in under three hours. In a traditional codebase with the same number of competing systems, the investigation alone might have taken days.

Speed creates the problem. Speed also enables the fix. The question is whether you have the diagnostic practices to notice before your users do.

[ADD PERSONAL REFLECTION: You caught this because you manually tested Piper and noticed "Sure" didn't work. Pattern-045 (Green Tests, Red User) again. Is there something to say about the role of manual testing as the last line of defense against composition failures?]

---

_Next on Building Piper Morgan: [TITLE TBD] — [teaser TBD]._

_Have you ever shipped features that each worked perfectly in isolation but fell apart when they ran together? What made you notice — a test, a user, or something else?_
