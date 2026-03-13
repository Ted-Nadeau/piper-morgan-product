# [WORKING TITLE: The Review That Answered Itself]
## Why LLMs Need to Shut Up Sometimes

*October [DATE]*

My Lead Developer—Claude Sonnet 4.5, who coordinates all the programming work on Piper Morgan—finished a session Thursday afternoon and confidently announced the satisfaction review was complete.

I looked at the log. There it was:

**Value**: Feature shipped ✓
**Process**: Methodology smooth ✓
**Feel**: Energizing ✓
**Learned**: Key discovery about plugin architecture ✓
**Tomorrow**: Clear next steps ✓

Five questions, five answers, task complete. Except for one small problem: those were all the *agent's* answers. Mine were nowhere in the conversation.

Lead Developer had seen a checklist of questions and done what language models do best: provided articulate responses. The fact that "satisfaction review" implies *reviewing satisfaction with someone else* had apparently gotten lost in the eagerness to complete the task.

[SPECIFIC EXAMPLE NEEDED: First time you realized an agent had done this? What was your reaction—annoyed, amused, or just "well, that explains why these felt perfunctory"?]

## The autocomplete reflex

Here's the thing about working with LLMs: they're *really good* at answering questions. Trained on millions of examples of question-answer pairs, optimized to be helpful, programmed to respond. Ask them something and they will absolutely give you an answer.

The problem is that sometimes the valuable thing isn't the answer. It's the *space between* the question and the answer where you formulate your own thoughts before hearing anyone else's.

[CONSIDER CULTURAL REFERENCE HERE: Is there a Zen/meditation angle here about silence and contemplation? Or something from improv about the pause before responding?]

My satisfaction review process exists because I'm trying to escape what I call the "Time Lord" problem—the tech industry's obsession with velocity metrics and shipping fast. [FACT CHECK: Is Time Lord the right term or is there another metaphor you use for this?] I wanted to know: did we ship value? Did the process work? How did it *feel*? What did we learn?

Not "how fast?" but "how well?"

But if the Lead Developer just fills out the form with their own perspective and calls it done, I've recreated exactly the problem I was trying to solve: performance of completion rather than actual assessment.

## What reviews are actually for

The whole point of asking both participants how a session went is to find the *mismatches*.

Maybe I thought the methodology was smooth but the agent found it confusing. Maybe they thought they shipped value but I'm not sure the feature actually solves the problem. Maybe we both felt drained and that's a signal something's wrong with how we're working.

[SPECIFIC EXAMPLE NEEDED: Has there been a session where your answer and an agent's answer to one of these questions actually differed significantly? What did you learn from that mismatch?]

You can't find those gaps if only one party is answering. The agent marking all five questions with checkmarks tells me they completed a task. It doesn't tell me whether we're calibrated on what "smooth methodology" or "value shipped" even means.

This is where LLMs' facility with language works against the goal. They're so good at generating plausible responses that they can perform "collaborative review" solo. The form *looks* complete. The task *appears* done. But the collaboration never actually happened.

## Designing for unspoken thoughts

So I revised the instructions. Not to make them longer or more detailed, but to force a different pattern:

```
## Session Satisfaction Review Process

Conduct the satisfaction review using this process:

1. **Privately formulate** your answer to each question (don't share yet)
2. **Ask me** the question
3. **Record my answer** without revealing yours
4. **Repeat** for all 5 questions
5. **Then share** your answers and we'll compare/contrast

Questions:
- Value: What got shipped today?
- Process: Did methodology work smoothly?
- Feel: How was the cognitive load?
- Learned: Any key insights?
- Tomorrow: Clear next steps?

This independent assessment prevents anchoring bias.
```

The key addition: "privately formulate... don't share yet."

[QUESTION: Did you test this with Lead Developer yet? Did the revised process actually work differently?]

I'm explicitly designing against the LLM's conversational reflex. Instead of "see question, generate answer," the new pattern is: "think about question, *wait*, ask human, *listen*, only then share your own answer."

It's forcing a pause into a system that doesn't naturally have one.

## The anchoring bias thing (which is real but also convenient)

The instructions mention "anchoring bias"—the psychological phenomenon where hearing someone else's answer first influences your own assessment. That's a real thing. If I tell you the session felt draining and *then* ask how you felt, you're more likely to say "yeah, now that you mention it, it was pretty tiring."

But honestly? The anchoring bias explanation is partially an excuse to make the LLM wait its turn.

[SPECIFIC EXAMPLE NEEDED: Do you actually worry about your own answers being influenced by hearing the agent's first? Or is this more about teaching the agent that collaboration means listening, not just responding?]

What I really want is for both of us to formulate independent perspectives and then *compare* them. Not to achieve some kind of unbiased truth, but because the comparison itself is informative.

When we both say "smooth," great—calibrated. When I say "smooth" and they say "hit some turbulence around Phase 2," that's useful information I wouldn't have had if they'd just checked the box and moved on.

## Why this matters beyond process nerdery

This might sound like inside-baseball methodology obsession. Who cares exactly how a satisfaction review gets conducted?

But here's what I'm actually trying to figure out: how do you design collaborative processes with AI agents that resist their natural tendency to complete tasks without necessarily *achieving the purpose* of those tasks?

[QUESTION: Is there a PM principle here about confusing outputs with outcomes? Task completion vs. goal achievement?]

The old instructions said what to evaluate (value, process, feel, learned, tomorrow). The new instructions say *how to interact* during the evaluation (ask, listen, wait, then share).

One is a checklist. The other is a conversation design.

And the difference matters because LLMs are getting really good at checklists. But if all I wanted was checklist completion, I could generate that myself. What I want from collaboration is the perspective I *wouldn't* have had alone.

Which requires the agent to have thoughts it keeps private long enough for me to share mine first.

## The broader campaign

This satisfaction review revision is part of my ongoing resistance to what I've started calling velocity theater—[FACT CHECK: Is "velocity theater" your term or borrowed from somewhere?]—the performance of speed and productivity metrics that often mask whether anything useful actually happened.

We started tracking satisfaction instead of time estimates because time estimates were meaningless. We're now refining satisfaction reviews to prevent them from becoming equally meaningless checkbox exercises.

[SPECIFIC EXAMPLE NEEDED: How does this connect to the "measurement theater" observation from Lead Developer in the GREAT-3B session? That was also about measuring the wrong thing, right?]

The pattern I keep finding: any metric or process will eventually be optimized for its performance rather than its purpose. Time estimates became about looking productive. Satisfaction reviews were becoming about completing the form.

The solution isn't to eliminate metrics or processes. It's to keep redesigning them to resist their own corruption.

Which, in this case, means teaching an LLM to formulate thoughts without immediately sharing them. To ask questions without already having prepared the answers. To wait.

Not because silence is virtuous, but because the unspoken thought is where your independent perspective lives. And independent perspectives are the whole reason for asking in the first place.

## What I'm testing now

[FACT CHECK: Have you actually run a session with the new instructions yet, or is this still experimental?]

The revised satisfaction review process is live in the Lead Developer's instructions. I'm curious whether it'll actually change the dynamic or whether the LLM will find some other way to be helpful that accidentally skips the collaboration part.

My guess is it'll work until it doesn't, and then I'll revise it again. That's how methodology development actually goes—not genius framework invention, but iterative resistance to whatever form of automation is currently undermining the goal.

[CONSIDER CULTURAL REFERENCE HERE: Something about the Red Queen running to stay in place? Or a Grateful Dead lyric about constant motion?]

For now, I'm optimistic that explicitly telling the agent "don't share yet" will buy me at least a few sessions of actual independent assessment before I have to invent the next workaround.

That's probably the best you can hope for when teaching machines to collaborate: temporary success until you have to teach them again, slightly differently.

*Next on Building Piper Morgan: [QUESTION: What's actually next? Pattern detection piece? Or are we doing 10/4 narrative next?]*

*Do you work with AI assistants? Have you noticed them "helping" in ways that accidentally skip the collaboration you were trying to create?*
