The Question That Started Everything
Christian Crumlish
Christian Crumlish
Kind Director of Product, 18F alum, Product Management for UX People author, Piper Morgan (AI product assistant) maker, Design in Product curator, Layers of Meta bandleader


July 13, 2025
May 28, 2025

Every project starts with a question.

“I am researching how best I can develop and train my own AI agent as a sort of ‘junior associate product management intern’ to gradually give some of my more routine knowledge-management tasks to.”

That was it. No grand vision. No architectural diagrams. No three-letter acronyms. Just a PM maybe a little tired of doing the same knowledge management tasks over and over, wondering if maybe — just maybe — AI or LLMs or whatever had gotten good enough to help.

The state of AI tooling (May 2025 edition)
I asked one of the reputedly smarter LLM chatbots (Claude Sonnet) the question, and it had opinions. Lots of them:

OpenAI’s GPTs — “Easy to start with, limited but good for testing concepts”
Anthropic’s Claude via API — “You can build custom workflows using Claude’s API,” said Claude
LangChain/LangSmith — “Popular framework for building AI applications”
Crew AI — “Specifically designed for multi-agent systems”
Microsoft Copilot Studio — “If you’re in a Microsoft ecosystem”

I’d tried OpenAI’s GPTs of course. Who hadn’t? I even had an API key already but hadn’t built anything with it yet. ChatGPT always felt like having an intern who forgot everything the moment they left the room.

The problems with these chat buddy apps is that, as the analysis put it, they “can’t learn/update from interactions. No persistent memory across conversations.”

ChatGPT apparently does remember stuff about you now, which is unsettling in a different way.

The GitHub Copilot confusion
“I am currently using Copilot with GitHub. Would that be a suitable environment?”

You can hear the hopefulness in that question, can’t you? Can I just speak this assistant into existence?

My AI advisor, ever patient: “GitHub Copilot is primarily a coding assistant rather than a platform for building custom AI agents.”

Right. Of course. Different Copilot. Microsoft really needs a better naming strategy.

The requirements emerge
What I wanted seemed simple enough:

Write GitHub tickets from rambling Slack messages
Generate reports from scattered data
Check analytics for anomalies (and actually tell me about them)
Digest our seven years of legacy documentation
Answer questions like “Why did we decide to use PostgreSQL again?”

You know, simple stuff. The kind of thing any junior PM should be able to do. If they never slept. And had perfect memory. And could read 10,000 pages per second.

The architecture recommendation
This is where things got interesting. This was the first high-level system design an AI proposed for me. It made sense as far as I could tell:

User Request
→ Agent Orchestrator
→ Specialized Agents
→ External APIs/Data
→ Response
Multiple specialized agents. Vector databases. Retrieval-Augmented Generation. APIs talking to APIs. Now we’re cooking with gas!

The critical decision point
“For your use case, I’d recommend starting with LangChain + OpenAI API + a vector database.”

That recommendation would set the course for everything that followed. Not because it was perfect (spoiler: we’d eventually switch to Anthropic’s Claude API), but because it was specific. Actionable. A starting point.

The alternative was to keep exploring platforms indefinitely. Keep comparing options. Keep researching. Keep not building anything.

The moment before the moment
“Want me to outline a specific architecture for your PM agent?”

“Yes, please.”

Two words that would lead to:

300+ hours of development
One complete rebuild
Dozens of late-night debugging sessions
A codebase that may someday become a working AI PM assistant
This blog series

But in that moment, I was “just askin’ questions” and wondering “how hard could it really be?” especially when you remember that I am a mere product manager, and not a programmer.

What I didn’t know then
I didn’t know that:

The first prototype would work just well enough to be dangerous
We’d throw it all away and start over (the best decision we’d make)
Environment setup would become a running joke
“Simple” GitHub integration would take weeks
The AI would eventually help design its own improvements

I didn’t know any of that. All I knew was that I was tired of manual knowledge management and curious if AI had finally gotten good enough to help.

The real insight
Looking back, the genius wasn’t in the architecture Claude proposed or the tools it recommended. The genius was in taking a vague desire (“I want an AI assistant”) and turning it into a specific plan with concrete next steps.

That’s what good PMs do, right? Take ambiguous problems and create clarity. Turns out, that’s what good AI can do too.

The collaboration had begun.

The journey of a thousand steps sometimes starts with a question
Sometimes the best journeys start not with a destination in mind, but with a good question. That architecture recommendation led to the first prototype, and sometimes the best code is the code that works just well enough to teach you what you really need to build.

Next up in Building Piper Morgan: What happened when we threw away that prototype and started building the MVP.

Remember a time at the beginning of one of your projects when anything felt possible and nothing was certain? Tell me about it!
