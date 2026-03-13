The Technical Debt Reckoning
Christian Crumlish
Christian Crumlish
Kind Director of Product, 18F alum, Product Management for UX People author, Piper Morgan (AI product assistant) maker, Design in Product curator, Layers of Meta bandleader


August 5, 2025
June 26

So there I was, supposedly at the end of a successful integration sprint, staring at what should have been a celebration moment, and instead discovering I’d accidentally built two orchestration systems.

And only one of them actually worked.

This is the kind of discovery that makes you question everything you thought you knew about your own codebase. Like finding out you’ve been wearing mismatched socks for a week, except instead of socks, it’s fundamental architecture, and instead of a week, it’s… well, however long it takes to accidentally build duplicate systems without noticing.

Welcome to the technical debt reckoning.

Success with a side of confusion
We’d just completed a major integration milestone. File analysis was working end-to-end. The tests were passing. Users could upload files, get intelligent analysis, and everything flowed through our task-based architecture beautifully.

But as I started preparing for the next integration (GitHub functionality), I kept running into this nagging confusion about which orchestration system I was supposed to use (without really understanding what was going on).

There was OrchestrationEngine — the newer, cleaner task-based architecture that aligned perfectly with our domain models. And there was WorkflowExecutor — the older system that had grown organically from our early GitHub proof-of-concept work.

Both worked. Both had tests. Both were actively maintained. And I had no clear memory of making a conscious decision to keep both. This is a side effect of working with AIs that “know” a lot more about programming than I do. They suggest things, I say “that sounds good,” and the implications escape me. (I try to ask for tradeoffs and pros and cons these days!)

The detective work begins
When you suspect architectural confusion, you start with the basics: grep for usage patterns and see what’s actually running in production.

grep -r "OrchestrationEngine" services/
grep -r "WorkflowExecutor" services/
What I found was… interesting.

OrchestrationEngine was everywhere the application was actually working. The main API used it exclusively. File analysis flowed through it. The domain models were designed around its task-based approach.

WorkflowExecutor was… well, it was thoroughly tested, had its own handlers, and was definitely being maintained. But it wasn’t being used by anything that mattered.

It was like discovering you’ve been paying rent on two apartments but only sleeping in one.

The “why did this happen?” moment
Here’s the thing about technical debt: it doesn’t usually happen because you make bad decisions. It happens because you make reasonable decisions that become less reasonable over time, and then you keep making more reasonable decisions on top of them.

WorkflowExecutor started as a perfectly sensible solution for GitHub integration. Quick, focused, got the job done. When we needed file analysis, OrchestrationEngine emerged as a better architectural approach — more extensible, better separation of concerns, aligned with our evolving domain models.

But instead of migrating WorkflowExecutor’s functionality to the new system, we just… kept both. Because WorkflowExecutor was working, and who has time to fix something that isn’t broken when you’re trying to ship features? And, well, I didn’t ask and nobody suggested it.

I was starting to understand how AOL Instant Messenger had gotten into the spaghettified state it was in when I was director of product in its final years.

Classic technical debt formation: each individual decision makes sense, but the accumulated result is architectural confusion.

The testing gap that should have been a red flag
Here’s what really should have tipped me off: OrchestrationEngine — the system that was actually running our application — had zero tests.

Zero.

WorkflowExecutor, the legacy system that nothing was using? Comprehensive test coverage.

This is like having a perfectly maintained spare car while your daily driver has no brakes. It works right up until you need to stop.

The test coverage gap existed because OrchestrationEngine had evolved organically from real usage patterns, while WorkflowExecutor had been built with proper TDD discipline from the start. Good process applied to the wrong system.

It’s like we had built a bicycle with state-of-the-art precision and were running our errands in a go-kart.

The hard decision
When you discover architectural debt like this, you’ve got three options:

Ignore it: Keep both systems, accept the confusion, hope future developers figure it out
Merge: Try to combine the best of both systems into some hybrid approach
Choose: Pick the right system and migrate everything to it

Option 1 is what got us here in the first place. Option 2 is how you end up with three systems instead of two. That left Option 3.

But choosing means admitting that time and effort spent on one system was essentially waste. It means having uncomfortable conversations about sunk costs and technical priorities.

Sometimes the kindest thing you can do for your codebase is stop maintaining the parts that don’t serve it anymore.

The OrchestrationEngine decision
So why OrchestrationEngine over WorkflowExecutor?

Domain alignment: OrchestrationEngine’s task-based approach matched how our business logic actually worked. Tasks could be composed, reused, and tested independently.

Production reality: It was already handling our most complex workflows successfully. File analysis, user interactions, the stuff that actually mattered — all flowing through OrchestrationEngine.

Extension patterns: Adding new functionality (like GitHub integration) fit naturally into the task handler pattern.

Future flexibility: The architecture anticipated growth in ways WorkflowExecutor didn’t.

WorkflowExecutor wasn’t bad — it was just optimized for a different phase of the project. Early exploration versus systematic growth.

The cleanup discipline
Once you make the architectural decision, the cleanup work is mostly mechanical. But it requires discipline.

Step 1: Ensure the chosen system has proper test coverage (we wrote 11 comprehensive tests for OrchestrationEngine)

Step 2: Extract any unique functionality from the deprecated system (WorkflowExecutor had some GitHub handlers we needed to preserve)

Step 3: Update all documentation to reflect the single-system approach

Step 4: Actually delete the deprecated code (the hardest step psychologically)

The temptation is to just comment out the old system “in case we need it later.” But keeping dead code around is how you end up with technical debt in the first place.

By the way, this all sounds like I clean up code messes every day. A few weeks earlier I would have despaired of fixing this. I’d have — at best — been trying to follow stepwise advice, showing screens and errors to the chatbot, making typos, breaking stuff. I’d have made a bigger mess. But this far along, trusting the development process we’d, well, developed and was impressed at how smoothly the cleanup went.

So, really, my assistants fix it, but the initial recognition that we had two systems serving the same purpose — that came from forcing myself to slow down and actually understand what we’d built.

Documentation-debt déjà vu
Cleaning up the architectural confusion revealed a second layer of debt: our documentation was describing a system that didn’t match what we’d actually built.

The technical specs talked about WorkflowExecutor as the primary orchestration system. The architecture diagrams showed workflows that weren’t actually in use. The API documentation described patterns that had evolved beyond recognition.

This is how technical debt compounds: inconsistent code leads to inconsistent documentation, which leads to incorrect assumptions in future development decisions.

This happens a lot when you have AIs generate you a bunch of docs as a one-off. Who is going to maintain those docs and keep them up to date? You? Did you even read them? The bots? How will they remember to check, and when? (Over time we solved these problems, but that would be weeks later.)

And good documentation isn’t just nice to have — it’s a forcing function for architectural clarity.

What I learned about noticing debt
Technical debt isn’t always obvious. Sometimes it hides in plain sight as “working systems” that just happen to be redundant.

Signals to watch for:

Developer confusion about which pattern to follow
Multiple ways to accomplish the same fundamental task
Test coverage gaps in systems that are actually being used
Documentation that doesn’t match implementation reality
Integration work that feels harder than it should

The key insight: Technical debt isn’t just bad code. It’s confusing code. Code that makes the next developer (including future you) have to make decisions that should already be made.

The relief of clarity
There’s something deeply satisfying about resolving architectural confusion. Not just because the codebase is cleaner, but because your mental model finally matches the reality of what you’ve built. It’s like having a headache go away.

After the cleanup, adding GitHub integration became straightforward. Create a task handler, register it with OrchestrationEngine, write tests. No decisions about which system to use, no studying two different patterns to figure out which one to follow.

Clarity compounds just like debt does. Every future integration gets easier because the patterns are consistent and well-understood.

A systematic approach to debt
What turned this from a frustrating discovery into a productive session was approaching it systematically:

Assess honestly: What do we actually have, versus what we think we have?
Trace usage patterns: Which systems are actually serving users?
Evaluate architectural fit: Which approach serves our long-term goals?
Plan migration: What needs to be preserved, what can be discarded?
Execute with discipline: Follow through on the cleanup, don’t leave loose ends

You don’t have to pay off all your debt, certainly not at once. There are acceptable levels of debt at times if it is not slowing you down and not creating compound problems, but other forms of debt cannot be ignored without eventually tanking your project.

Technical debt isn’t inherently bad — it’s just the accumulation of decisions that made sense at the time. The problem comes when you stop making conscious choices about it.

More compound effects
The architectural cleanup paid dividends immediately. The next day, when we were working on domain contract enforcement, the clean single-system architecture made it easy to understand where problems were coming from and how to fix them.

Later in the week, systematic GitHub integration flowed naturally through the established patterns. No confusion, no competing approaches, just clear implementation following clear architecture.

This is what good technical debt management gets you: not perfect code, but predictable code. Code where the next step is obvious and the patterns are consistent.

When debt becomes opportunity
Here’s what I didn’t expect about the technical debt reckoning: it wasn’t just about cleaning up mistakes. It was about discovering what we’d actually learned about building this kind of system.

OrchestrationEngine emerged from real usage patterns. It had evolved to solve actual problems we’d encountered with WorkflowExecutor’s approach. The “accidental” architecture was actually better architecture — we just hadn’t recognized it yet.

Sometimes technical debt isn’t just waste to be cleaned up. It’s evidence of learning that hasn’t been systematized yet.

The ongoing discipline
Technical debt management isn’t a one-time cleanup — it’s an ongoing practice. But having gone through this systematic reckoning gave us patterns for recognizing and addressing debt before it compounds.

Regular architecture reviews: Periodic check-ins on whether our documented patterns match our implemented patterns

Usage audits: Grep for what’s actually being used versus what’s being maintained

Test coverage monitoring: Gaps in test coverage often indicate unclear architectural boundaries

Developer confusion signals: When integration work feels harder than it should, that’s usually a debt signal

The goal isn’t to eliminate all technical debt — it’s to make conscious decisions about which debt to accept and which debt to address.

Sunk costs make us feel bad
Maybe the most important lesson from the technical debt reckoning was about honest assessment. It’s easy to rationalize keeping multiple systems because “they both work” or “we might need the flexibility.”

But architectural clarity is worth more than theoretical flexibility. Having one well-understood system beats having two sort-of-understood systems, even if both work.

The hardest part wasn’t the technical cleanup — it was admitting that effort spent on WorkflowExecutor was essentially waste, even though every individual decision that led to it was reasonable.

Sometimes the most productive thing you can do is stop being productive in directions that no longer serve the project.

Next on Building Piper Morgan “When Your Tests Tell You What Your Code Should Do” — the follow-up story of how clean architecture enables learning.

What’s your experience with technical debt reckoning? Have you discovered duplicate systems, competing patterns, or architectural confusion hiding in plain sight? I’d love to hear about your own moments of “wait, why do we have two of these?” and how you resolved them.
