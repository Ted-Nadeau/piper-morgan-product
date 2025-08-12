When Claude Took a Break (And Gemini Stepped In)
christian crumlish
christian crumlish
2 min read
·
Aug 2, 2025





Time for one more flashback to the “lost weekend” two days into this project, reconstructed after the fact from a Gemini log so long I couldn’t get back to the head of it without crashing my browser. Part 1 of 4.

Press enter or click to view image in full size
A robot understudy steps in for a frozen robot actor
“I’m ready to take over”
May 30, early

Saturday morning. I’ve got a prototype with bugs, and Claude’s exhausted from a documentation marathon (that is, I am now locked out for hours from my free Claude account). Time to test whether all that “vendor independence” architecture talk was just talk, or if it could survive real-world constraints.

“Can you help me patch a few bugs in a Python prototype?”

That simple question to Gemini started one of the most educational debugging sessions I’ve had. Not because the bugs were complex, but because it proved something crucial: good development methodology transfers across AI providers seamlessly.

The handoff
I handed over the same files, the same context, the same systematic approach I had been using with Claude. Gemini picked up the debugging thread without missing a beat. No special adaptation needed. No workflow changes required.

This wasn’t theoretical anymore. My initial approach to coding an idea with LLM support was being stress-tested under real constraints.

Seven bugs, one mystery
What followed was methodical, collaborative debugging:

Critical Bug #1: Milestone assertion error in PyGithub (thanks to [ADD DETAIL: external contributor who spotted this])
Critical Bug #2: Repository configuration pointing to wrong repo
Critical Bug #3: Knowledge base context retrieval returning empty results
Plus four more: Dependency conflicts, JSON parsing brittleness, error message improvements, label handling
Seven bugs fixed systematically while chasing one complete mystery — a PyGithub AssertionError that made zero technical sense.

The real lesson
This wasn’t just about debugging Python. It was about discovering that vendor independence isn’t just good architecture — it’s operational resilience.

When your primary tool fails (and they all fail eventually), you need systems that survive the transition. Clean interfaces. Well-documented state. Methodical processes that work regardless of which AI is helping you think through the problem.

I had… some of that in place?

Build for when things break
We love to talk about the AI revolution, but Saturday morning taught me something simpler: build your systems to survive your tools failing. Because they will.

Whether it’s API limits, service outages, or just needing a fresh perspective, the projects that survive are the ones designed for tool independence from day one.

Bugs got fixed. The mystery got strategically abandoned. And the principle got proven under fire.

Sometimes the best validation comes when everything else is breaking.

Next on Building Piper Morgan: Part 2 of the Lost Weekend, “The Demo That Needed Documentation.”

Technical debt is like Saturday morning debugging — it accumulates quietly until you’re forced to deal with it systematically.
