The Coordination Tax: When Copy-Paste Becomes Your Biggest Bottleneck
christian crumlish
christian crumlish
5 min read
·
Jul 31, 2025
8






Press enter or click to view image in full size
A robot and a person do their taxes
“We should have kept receipts.”
Jul 8, 2025

Monday morning, and we’re down to what should have been the simplest possible fix: “The UI shows ‘Workflow completed successfully!’ instead of the actual document summary. Should be a quick fix.”

You know where this is going, right?

Two hours later, I’d discovered six sequential bugs, each one hiding behind the previous fix like Russian nesting dolls. But the real revelation wasn’t about the bugs themselves — it was about the coordination tax I was paying with every copy-paste, every context switch, every “let me check the logs” round trip.

By the end, I had a working document summarizer and a visceral understanding of why developer tools that reduce coordination overhead aren’t just nice-to-have — they’re essential for maintaining both development velocity and developer sanity.

I maybe should have picked up on this earlier. I’m a product manager. It’s glue work. Coordination work and the people (or, I guess, entities) doing it is my bread and butter. OK, sometimes I am slow.

The cascade resumes
What followed was a perfect demonstration of how integration bugs cascade through a system, each fix revealing the next issue lurking beneath like sedimentary layers of technical debt:

Bug 1: The UI display illusion
Symptom: Generic success message instead of summary
Assumed fix: Update JavaScript to show response.message
Reality: The data structure was fundamentally wrong
Coordination cost: 5 copy-paste cycles to discover this
Bug 2: Data structure mismatch
Symptom: workflow.result.data was completely empty
Discovery: Backend stored unwrapped data, frontend expected wrapped
Fix applied: Wrap the data properly in the result envelope
New problem: “No file ID found in workflow context”
Coordination cost: Another 3 round trips through logs and database queries
Bug 3: File ID resolution chaos
Symptom: File analyzer couldn’t find the file to analyze
Root cause: Intent enricher used probable_file_id, engine looked for file_id
Fix applied: Support both field names with fallback logic
New problem: Still getting basic statistics, not actual summaries
Coordination cost: Grep commands through multiple services, more log diving
Bug 4: The missing LLM client
Symptom: TextAnalyzer only returned “115 lines, 559 words”
Investigation: TextAnalyzer HAD summarization code but llm_client was None
Root cause: AnalyzerFactory() called without passing the LLM client
Fix applied: AnalyzerFactory(llm_client=self.llm_client)
New problem: ‘LLMClient’ object has no attribute ‘summarize’
Bug 5: The method that never was
Symptom: AttributeError on llm_client.summarize()
Investigation: TextAnalyzer calling non-existent method
Worse discovery: DocumentAnalyzer ALSO calling non-existent methods
Reality check: Nobody had ever successfully called the LLM for document analysis
Bug 6: The final fix (finally!)
Correct pattern: await self.llm_client.complete(task_type="analyze_file", prompt=...)
Applied to: Both TextAnalyzer AND DocumentAnalyzer
Result: Finally, actual LLM-powered summaries!
Each fix felt like victory until the next problem revealed itself. It’s like debugging whack-a-mole, but the moles are architectural assumptions you didn’t know you were making.

The real cost of coordination
This session perfectly illustrated why coordination overhead is the hidden killer of development productivity:

What actually happened:

2 hours of debugging time
15–20 copy-paste cycles between logs, UI, and code
Multiple context switches as each fix revealed the next problem
6 sequential bugs discovered one at a time
Growing frustration with each “one small fix”
What could have happened with better tooling:

Direct navigation: “Show me how DocumentAnalyzer calls the LLM”
Instant verification: “Does LLMClient have a summarize method?”
Dependency tracing: “Where is AnalyzerFactory instantiated?”
Estimated time: 30 minutes with high confidence
The difference isn’t just about speed — it’s about maintaining context and flow. Every copy-paste cycle is a mini context switch that forces you to rebuild your mental model of the system.

Imagine if you had to drive a car with someone else looking of the windshield and telling you what’s coming? That’s what it felt like.

Architectural lessons from the trenches
My pain is your education, though. I’m sharing my adventures in part to save other people the time of making my mistakes.

1. Integration points are where bugs hide
Every component boundary in our system had a hidden mismatch:

API → UI: Data structure assumptions
Orchestrator → Analyzer: Missing dependencies
Analyzer → LLM: Wrong method names
The individual components all worked perfectly. The bugs lived entirely in the handshakes between them.

2. Assumptions are expensive
We assumed:

The UI was the only problem
Data structures matched across layers
LLM methods existed because code called them
One component working meant the pipeline worked
Each assumption cost 15–30 minutes of debugging time. And each one felt reasonable until it wasn’t.

3. Simple verification is powerful
One command could have prevented each bug:

grep -n "message" web/app.py
grep -n "to_domain" repositories/
grep -n "llm_client" services/analysis/
grep -n "summarize" services/llm/
But without direct file access, each verification required a copy-paste round trip through a human intermediary (me). The friction compounds quickly.

The beautiful irony
Want to know the best part? The first document our finally-working summarizer processed was an Architecture Decision Record about adopting Claude Code to reduce coordination overhead.

(I was starting to twig to the value of letting Claude see my code directly, so I asked my chief architect bot to propose a plan for adopting Code and gave it the data from these sessions to make the case.)

The AI understood the assignment perfectly, summarizing how Claude Code “promises complete implementation traces, self-directed task completion, architectural rule enforcement, and reduced context switching.”

We had just spent two hours proving exactly why we need better tooling. The universe has a sense of humor about these things.

The coordination tax is real
This debugging session wasn’t a failure — it was data. Real, visceral data about the hidden costs of coordination overhead in modern development.

Every copy-paste operation is a tax on your cognitive resources. Every context switch between logs and code breaks your mental model. Every “let me check that” conversation is a tiny friction that seems harmless in isolation but compounds into hours of lost productivity.

When you’re building complex systems with multiple AI agents or even just working with traditional tools, the coordination tax can easily become your biggest bottleneck. Not the complexity of the problems, not the technical challenges, but the simple friction of moving information between contexts.

Moving forward with systematic approaches
The document summarization feature works now, and it works well. But more importantly, we have a perfect case study for why systematic approaches to reducing coordination overhead aren’t just productivity improvements — they’re essential for maintaining development sanity.

Sometimes you have to experience the pain to truly appreciate the solution. Two hours of copy-paste debugging has a way of crystallizing exactly what needs to be fixed in your development workflow.

Next on Building Piper Morgan: Two-Fisted Coding: Wrangling Robot Programmers When You’re Just a PM, or mo’ robots, mo’ problems.

Have you experienced your own coordination tax episodes? When has the friction of moving information between tools or contexts become your biggest development bottleneck? I’d love to hear your stories of debugging sessions that revealed more about tooling needs than about the actual bugs.
