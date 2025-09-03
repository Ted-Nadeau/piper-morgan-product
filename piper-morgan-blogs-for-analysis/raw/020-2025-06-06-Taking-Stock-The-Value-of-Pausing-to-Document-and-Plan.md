Taking Stock: The Value of Pausing to Document and Plan
Christian Crumlish
Christian Crumlish
Kind Director of Product, 18F alum, Product Management for UX People author, Piper Morgan (AI product assistant) maker, Design in Product curator, Layers of Meta bandleader


July 7, 2025
June 6, 2025

Sometimes the most productive thing you can do is stop being productive.

A week or so into my first attempt at building Piper Morgan, I had that special kind of mess that only happens when you’re building something while figuring out what you’re building. Working code that didn’t quite work. Clear vision that wasn’t quite clear. You know the feeling.

So I did something radical: I stopped coding and started documentint what I’d actually built versus what I thought I’d built.

Turns out, those are very different things.

The documentation exercise that became an intervention
The plan was simple, ask for a whole slew of standard technical docs based on our current codebase: Architecture doc, technical spec, requirements, one pager, roadmap, backlog, report to the team, one-pager, presentation. Anything I could think of I asked for.

Sonnet wrote me some enthusiastic first drafts:

“Piper Morgan seamlessly integrates organizational knowledge across multiple context levels, enabling sophisticated multi-modal product management workflows…”
I read that three times and still wasn’t sure what it meant. And I built the thing. I was pretty sure it was wrong though.

Don’t believe the hype
I took the whole slew of documents and showed them to Opus. I told it “You are distinguished principal architect and an enthusiastic PM and developer have built a prototype that they are presenting to the team as production ready.” I asked it to rewrite the docs to more realistic.

That lens changed everything:

“Working system” → “Basic implementation with significant gaps”
“Production-ready architecture” → “Services deployed locally, not production-hardened”
“Advanced AI reasoning” → “Template responses with some LLM calls”
“Learning system” → “Stores feedback (learning TBD)”

Was this depressing? Nah. It was liberating. Finally, I could see what I’d actually built.

You can’t steer based on hype
The revised documentation definitely backed off on the wild claims:

“Reduces PM work by 50%” → “Potential 30–50% reduction (unproven assumption)”
“Intelligent issue creation” → “Basic GitHub integration, intelligence varies”
“Knowledge-aware responses” → “Search works, relevance inconsistent”

But here’s the thing: honest documentation enables honest planning. When you know where you really are, you can figure out where to go next.

The planning paradox
There’s always this tension: time spent documenting feels like time not spent coding. Especially when you’re a team of one (plus AI assistants who never sleep but also never quite understand context).

But that June 6th pause taught me something. Comprehensive planning accelerates development by:

Forcing honest assessment — Can’t fix what you won’t acknowledge
Identifying critical blockers — That workflow persistence bug I’d been ignoring? Yeah, that was blocking everything
Setting realistic timelines — Based on actual capacity, not caffeinated optimism
Creating accountability — Even if just to future me
Enabling better decisions — Clear priorities beat fuzzy good intentions

What actually got clarified
AI development has unique challenges: It’s not just API calls. It’s prompt engineering, output validation, and handling the fact that LLMs sometimes just make stuff up. The timeline estimates were all over the map. In some ways way conservative because based on language about unaugmented human developers. In other way ambitious because of the hours spent fixing LLM-powered mistakes.

Single developer risk is real: Without documentation, this whole project was just in my head. There was no way to even see the whole shebang, let alone show it to anyone else. Someday I’d love to have others adding to this codebase, but that won’t happen if it’s a black box.

Integration complexity compounds: GitHub + Claude + OpenAI + ChromaDB + PostgreSQL = five potential failure points. When I started this project I knew it was ambitious but I had underestimated the level of complexity and the endless combinations of glitch that can bring the whole house down.

It’s not quite the complex-stakeholder complexity I dealt with at big companies like Yahoo and even bigger enterprises like California and the U.S. Federal government, but it has that same quality of you can get almost everything aligned when suddenly one of your mainstays goes out of true and you’re b0rked again.

The meta-documentation bonus
Writing docs about building an AI system with AI assistance got weird fast. The session log my bot wrote was more optimistic than my mental state. Had to keep editing:

Bot: “Successfully implemented sophisticated orchestration engine!” Me: “Fixed basic workflow execution. Mostly.”

Bot: “Learning system captures valuable signals!” Me: “Redis stores some JSON. Learning part TODO.”

Realistic next steps, or…
Armed with more honest documentation, it seemed the priorities became crystal clear:

Fix workflow persistence — Currently broken, blocking everything
Get ONE integration working end-to-end — GitHub first, fantasies later
Improve search quality — Current results are… creative
Build basic UI — API-only testing getting old

The documentation exercise also generated two useful scripts: one to populate GitHub with all the docs, another to create issues from the backlog. At least the automation to document my struggles was working!

Over time we outgrew those scripts but the concept of maintaining docs automatically and iterating them over time stays with me.

What I didn’t see yet was that we needed to stop and start over, as recounted in “The Great Rebuild: Starting Over When Starting Over Is the Only Option,” so for the moment I just kept plowing ahead thinking my taking-stock pause was enough.

Getting the balance right
Building complex systems requires alternating between execution and reflection. Pure execution without planning leads to beautiful messes (hi, current state!). Pure planning without execution leads to beautiful fiction (hi, first draft docs!).

The sweet spot? Periodic reality checks like this one. Comprehensive enough to hurt a little, focused enough to actually help. Even as we outgrew the prototype and started on the MVP, I have continued to alternate between periods of developing and periods of taking stock and reviewing where we are.

The actual learning
That day of documentation taught me more about Piper Morgan than the previous week of coding. Not because writing is magic, but because writing honestly about what you’ve built forces you to see it clearly.

With what we learned from generating these docs, reviewing them, and asking for expert advice was that even with some basic capabilities working and the possibility of adding more, we lacked a solid architectural foundation, would likely never be able to build the more sophisticated features I’d imagined, and that it was time to rethink.

That alone probably saved me weeks of sunk-cost work on a dead-end approach. I didn’t mind learning this! I learned so much in the first nine or ten days and none of it went to waste in the rebuild. I’m just glad we stopped and checked the map before driving further into the desert.

Next up in Building Piper Morgan: Back to coding with clearer priorities and expectations so realistic they hurt.

(Ever documented your way to clarity? When did you realize what you’d actually built versus what you thought you built? Share your documentation reality checks — I’m collecting stories of honesty-driven development.)
