The 40-minute miracle: how two AI agents achieved 642x performance in one session
christian crumlish
christian crumlish
5 min read
·
5 days ago





Press enter or click to view image in full size
A robot passes the baton to another in a relay race
“We’re breaking the record!”
July 18

Here’s how you know your development process is getting weird: you deploy two AI agents in parallel, step away for 40 minutes, and come back to a 642ｘ performance improvement with comprehensive documentation.

I mean, I was present for those 40 minutes. Providing strategic direction, breaking down complex tasks, catching the occasional infinite loop. But the actual coding? That was Claude Code and Cursor Assistant working in perfect coordination while I tried to keep up with their status updates.

Connection-leak detective work
Yesterday we’d built domain models for content search in five minutes using TDD. Today’s mission: fix the connection leak from our proof-of-concept that was creating a new connection for every single request.

The numbers were damning: 103ms overhead per request just for connection creation. Multiply that by 100 requests and you’re looking at 10+ seconds of pure connection waste.

The parallel deployment
Instead of sequential work, I tried something different: deploy both agents simultaneously with clear, non-overlapping assignments.

Claude Code: Build the connection pool with singleton pattern, circuit breaker, and TDD discipline.

Cursor Assistant: Create performance benchmarks to quantify the problem and validate the solution.

The theory was that Code would build the fix while Cursor measured the improvement. In practice, it was like watching a perfectly choreographed dance between two systems that had never worked together before.

Thesmoking gun
Cursor delivered the bad news first: baseline benchmarks showing exactly how broken our POC was.

Connection creation: 103.08ms per request
Memory: 18KB per connection
Reuse rate: 0% (new connection every time)
Every single request was paying that 103ms tax for the privilege of creating a connection that got thrown away immediately. It was like paying setup fees for every transaction instead of maintaining an account, like getting a new library card every time you want to check out a book.

Meanwhile, the async deadlock drama
While Cursor was quantifying our connection leak, Code hit a classic async programming challenge: tests hanging on semaphore acquisition. (Yes, I stopped and asked Claude to explain to me what semaphore means in this context — it’s an asyncio concept that allows you to limit the number of simultaneous operations in a section of code).

The debugging process was fascinating to watch unfold in real-time:

Test hangs during pool initialization
Investigation reveals lock held during I/O operation
Breakthrough insight: “Never hold async locks during I/O operations”
Refactor to separate state checking from connection creation
All tests pass
That’s the kind of low-level async pattern that can eat hours of debugging time. Code identified and fixed it in about 10 minutes.

The integration moment
By 4:50 PM, both agents had completed their assignments:

Code: ✅ Connection pool with 17 comprehensive tests passing
Cursor: ✅ Performance benchmarks ready to run
But there was a gap: the pool wasn’t connected to the benchmarks yet. Code had built beautiful infrastructure, Cursor had perfect measurement tools, but they weren’t talking to each other.

This is where AI coordination gets interesting. Code quickly added a feature flag (USE_MCP_POOL=true/false) for zero-breaking-change integration. Cursor updated the benchmarks to support dual-mode testing. Perfect handoff.

I think I first encountered feature flags at CloudOn, where it was critical to be able to ship a feature to the app store turned off, and then turn it on when ready to launch. (We also hid some of our payment features from Apple athat way at 7 Cups but that’s another story.)

The numbers that changed everything
USE_MCP_POOL=false (baseline):

Connection creation: 102.79ms
Memory per operation: 17.57KB
Connections for 100 requests: 100
USE_MCP_POOL=true (with connection pool):

Connection creation: 0.16ms
Memory per operation: 0.58KB
Connections for 100 requests: 1 (reused!)
642x faster connection creation. 97% memory reduction. 99% fewer connections.

Those aren’t typos. Those are the kind of improvements that change how you think about system architecture. I’ve gotten used to these bots hyping me up. They unintentionally sandbag their estimates by pegging them to human norms, then celebrate when they blow through the estimates, but this is real before-and-after math, a massive reduction in waste.

The PM moment
Halfway through the session, Cursor hit a complexity wall trying to create visualization charts for the performance data. The task was getting unwieldy, and I could see the agent starting to struggle.

This is where the human-in-the-loop pattern becomes crucial: “This assignment may be too challenging. Can we isolate the difficult part?”

We broke it down: essential documentation (easy), fancy visualizations (nice-to-have). Cursor focused on what mattered, delivered the critical updates, and the session stayed on track.

The 40-minute reality check
At 5:00 PM I looked at the clock and realized something surreal: we’d been actively working for less than 40 minutes.

In those 40 minutes:

Identified and quantified a major performance bottleneck
Built production-ready connection pool infrastructure
Implemented comprehensive error handling and circuit breaker patterns
Achieved 642x performance improvement
Created complete technical documentation
Updated all project tracking
The kind of work that would normally take days, compressed into a single focused session.

What multi-agent coordination teaches us
Clear division of labor prevents conflicts. Code focused on infrastructure, Cursor on measurement. No overlap, no confusion about responsibilities.

Parallel execution multiplies throughput. Instead of sequential implementation → testing, both happened simultaneously with perfect integration at the end.

Feature flags enable safe integration. Code’s USE_MCP_POOL flag meant zero risk deployment with easy rollback if needed.

Human coordination amplifies AI capabilities. The agents were incredibly productive, but needed strategic direction and complexity management to stay effective.

The deeper insight about performance
The 642x improvement wasn’t just about connection pooling — it was about understanding where the real bottlenecks hide. The actual file operations were fast (0.01ms). The content processing was reasonable. But that hidden 103ms connection overhead was eating everything.

Performance optimization isn’t about making fast things faster. It’s about finding the thing that’s secretly slow and fixing that first.

What’s next
With connection pooling solved, we’re ready for Day 3: real content search. No more fake filename matching — time to implement actual content extraction and TF-IDF relevance scoring using the domain models we built.

The infrastructure foundation is now rock-solid. 642x performance improvement means we can afford to do more sophisticated content analysis without worrying about connection overhead.

Plus we’ve proven that multi-agent coordination can work beautifully when the division of labor is clear and the integration points are well-defined.

Next on Building Piper Morgan: When Your Infrastructure Gets Smarter Than Your Tests — building content search with MCP and finding out that some test failures are failures of the tests.

Ever managed parallel work streams that needed to integrate perfectly at the end? I’m curious how others approach coordination challenges, whether with AI agents or human teams.
