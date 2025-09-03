When Your Docs Lie
Christian Crumlish
Christian Crumlish
Kind Director of Product, 18F alum, Product Management for UX People author, Piper Morgan (AI product assistant) maker, Design in Product curator, Layers of Meta bandleader


July 29, 2025
June 21–22, 2025

Fresh off completing three planned issues,PM-009 (multi-project support), PM-010 (production error handling), and PM-011 (web chat interface), feeling pretty good about our systematic development progress. Time to update the documentation to reflect our new capabilities.

That’s when I realized our user guide still claimed “no web UI exists” for a system that now had a fully functional web chat interface.

This is the story of documentation debt — how it accumulates faster than you think, compounds more dangerously than technical debt, and requires its own systematic reckoning process.

Celebrating technical wins while ignoring communication debt
We’d been on a roll with systematic development. Three major features completed in sequence, each building on solid architectural foundations. PM-009 gave us sophisticated multi-project context resolution. PM-010 delivered production-quality error handling. PM-011 provided a working web interface with real-time updates. (We were soon to learn the user interface was really only skin-deep so far, but no spoilers.)

But while we’d been disciplined about technical debt, we’d completely ignored documentation debt. And documentation debt, it turns out, is more insidious than technical debt because it affects every stakeholder who tries to understand what you’ve built.

It also squanders the opportunity to provide language-eating bots with the lastest accurate information about what they’re working on for you.

The crisis language re-discovery
The worst part wasn’t just outdated information — it was the tone of our documentation. Our requirements document was full of “🚨 BLOCKING” assessments for features we’d already completed. Crisis language describing problems we’d already solved.

This dated to my earliest attempt to tame the LLMs’ tendency for hype. When the first set of docs claimed our patchy prototype was production-ready, I had insisted on a more realistic (and dour, it turns out) assessment.

But now our old docs still said things like “Critical gaps in GitHub integration preventing production use” when in fact we had since already implicated some pretty slick GitHub issue analysis, with 95% intent accuracy and professional improvement suggestions

The documentation wasn’t just wrong about capabilities — it was wrong about our trajectory. Anyone reading it, even a bot! would think we were in crisis mode when we were actually hitting our development milestones systematically.

This, as noted, was an overcorrection. There’s been an ongoing tension when documenting Piper between technical accuracy and hype. These tools can’t resist positive spin unless you actively frame the tone and perspective you want.

In this case, there was no one to hype! I don’t need to impress a boss or investor. I don’t have deadlines. This is a learning project fundamentally, but it’s really hard for these AIs to overcome their training.

The “no web UI” embarrassment
The most embarrassing discovery was our user guide prominently stating “no web UI exists” while our system had a fully functional web chat interface that we’d been demoing to stakeholders.

This wasn’t just an oversight — it would actively mislead anyone trying to evaluate or use our system. Imagine a new team member reading the docs and concluding they needed to use command-line tools when there was a perfectly good web interface available. Good thing it’s just me working on this thing, and my language bots of course.

Compound interest on documentation debt
What struck me about this documentation reckoning was how fast documentation debt compounded. It wasn’t like technical debt where problems accumulate gradually — documentation debt created immediate credibility issues.

Week 1: Documentation slightly behind reality

Week 2: Documentation describes different system than what exists

Week 3: Documentation actively contradicts stakeholder experience

Each week of delay made the documentation exponentially more misleading rather than just incrementally outdated.

The systematic consolidation approach
Once I recognized the scope of the documentation debt, I knew this needed systematic attention — not just quick fixes to the most obvious problems. One of the theme of this journey has been gradually re-discovering why software development has evolved as it has.

Oh, right! Accurate documentation. That’s important. (Remember, I was a content strategist before I was an information architect before I was a UX lead before I was product guy, and before all that I wrote technical books! How could I of all people overlook the importance of writing it all down?).

Time to get back on track:

Conduct complete audit of all documentation folders
Identify documents that were fundamentally misaligned vs. incrementally outdated
Replace crisis-language documents entirely rather than patching them
Establish documentation standards to prevent future drift

With clear instructions, this is a much better job for them than us. They happily spew out docs all day long, to any spec.

The decision to replace rather than incrementally update the requirements document was crucial. When documentation is fundamentally misaligned with reality, patching creates more confusion than clarity.

Archaeology on our own system
The systematic documentation review became like archaeological work — uncovering layers of assumptions and outdated understandings about our own system.

Architecture layer: Discovered we’d achieved CQRS-lite patterns organically without documenting them

Integration layer: Found we’d evolved sophisticated error handling contracts without recording them

User experience layer: Realized we’d built production-ready workflows while documentation still described proof-of-concepts

Sometimes you don’t understand what you’ve built until you try to document it accurately.

AIs need docs the most
One insight from this session was how AI collaboration changes documentation requirements. Working with AI assistants requires more comprehensive documentation because AI needs explicit context that humans might assume.

Traditionally, documentation was made to serve humans who could fill in gaps where needed. Now, documentation serves as context for AI systems that can’t make assumptions.

Session logs, architectural decision records, and detailed context documentation become critical enablers rather than optional nice-to-haves.

AIs have no sense of thime.
During the documentation review, we discovered a freshly created requirements document that was dated “December 2025” — six months in the future.

“It’s funny you think it’s December though? maybe we are ahead of our roadmap lol. It is June 21 today. In fact, from now on let’s always make sure our docs have the date they were last updated right up near the top!”
That spontaneous decision to establish dating standards turned out to be crucial for documentation maintenance workflow.

One thing I’ve noticed is that these bot friends tend to make schedule assumptions based on human developer output. This makes sense since the bulk of their training sets deal with such scenarios. This tends to lead to them being constantly astounded at how they are crushing the schedule. After the first week we often had docs saying I’d been at it for months, and because we were so far ahead on some early conservative roadmap, it just did the math and assumed it must be six months in by now.

Adopting progressive disclosure emojis
One architectural insight from the documentation consolidation was implementing “progressive disclosure” through status indicators:

✅ Complete

🔄 In Progress

📋 Planned

Progressive disclosure enables quick scanning while detailed information remains available.

Documentation as architecture
The consolidation process revealed that documentation structure should mirror system architecture. Our scattered docs reflected confused thinking about system boundaries.

Our updated doc tree separated documentation into categories — architecture/, development/, planning/, project/ — helping to keep things uncluttered.

When documentation structure is unclear, it usually indicates architectural thinking is unclear.

Doppleganger docs
During consolidation, we discovered we had made API documentation files twice: one was a comprehensive specification and the other a basic reference guide. Instead of consolidating them, we made sure they were accurate and then established complementary purposes:

The comprehensive doc contains complete contracts, error handling, WebSocket specs, etc. The other is a streamlined quick reference for daily development work.

Different audiences need different detail levels. Forcing everything into one document serves no audience well.

The mid-writing handoff-context crisis
The session was interrupted when “things went sideways” — system issues occurred during the documentation work. For all of their adeptness with words and language, a lot of these tools are unaware of their own limitations, and when you give them a big editing job, they can try to cram all the text into their “heads” until they get confused and give up or start making big mistakes.

One way I learned to deal with that, especially with the somewhat unimaginative Cursor assistant, was to give strict one-at-a-time instructions, requiring the bot to write and edit discrete chunks of work and then report in on success or failure before proceeding to a next step. This prevents it from trying to juggle all the pieces at once.

The mini-crash that interrupted our work combined with the filling up of a chat before I could get a clean handoff prompt created its own documentation challenge: how do you hand off incomplete work when the work itself is about improving handoff documentation?

We managed to repair the session log, provide enough context about the work in progress, and get things continued, but managing across these sorts of disjunctions can be a constant challenge that requires the focused attention of the primate in the loop.

This recursive problem only underlined why systematic session logging is critical for AI collaboration projects.

The documentation-driven development insight
What emerged from this reckoning was “documentation-driven development” — using documentation accuracy as a forcing function for architectural clarity.

Documenting our work forces us to ask questions such as, “What exactly does this component do?” and “How do these pieces connect?” and “What are the actual error conditions?”

Capturing this info provides architectural benefits: clear boundaries, explicit contracts, honest capability assessment

When you can’t document something clearly, it’s usually because the architecture isn’t clear.

Systematic vs. reactive documentation
This session established the difference between systematic and reactive documentation approaches. Being reactive means letting docs get stale till someone complains. Being systematic means incorporating documentatiom updates as acceptance criteria for feature completion.

This feels like a lesson I have to learn again and again in each new context. Forgot to instrument the new feature and had no data for the first sprint after launch? It goes in the acceptance criteria and the feature-brief template and you never forget to do it again.

Systematic documentation prevents the compound interest problem by addressing drift before it becomes misleading.

The systematic approach also helped us develop an effective documentation consolidation workflow:

Complete audit — what exists, what’s accurate, what’s missing
Triage — incremental updates vs. complete replacement
Systematic updates — working through one category at a time
Cross-referencing — ensuring documents connect appropriately

Trying to update everything simultaneously creates inconsistency. Sequential consolidation maintains coherence.

Forgetting to document our architectural evolution
One major discovery was that we’d achieved sophisticated architectural patterns (CQRS-lite, multi-project context resolution, provider-agnostic design) without documenting them.

This meant new team members (human or otherwise) wouldn’t understand the system’s design principles. Even we weren’t fully conscious of what patterns we’d established.

Converting implicit architectural knowledge to explicit documentation enables system evolution and team growth.

Another thing this reckoning taught me is that documentation quality gates are as important as code quality gates.

Systems that check code quality but not documentation quality inevitably accumulate communication debt.

Like a bridge over troubled documents
This documentation reckoning session served as a bridge between our architectural learning period and the systematic recovery work that followed. Learning to address documentation debt systematically prepared us for addressing technical debt systematically.

Good process disciplines transfer across different types of maintenance work.

Next on Building Piper Morgan When TDD saves your architecture, and how we spent weeks retrofitting, well, everything.

What’s your experience with documentation debt? Have you had moments when your own documentation contradicted your system’s reality? I’d love to hear about your own systematic vs. reactive documentation approaches and what forced you to take documentation accuracy seriously.
