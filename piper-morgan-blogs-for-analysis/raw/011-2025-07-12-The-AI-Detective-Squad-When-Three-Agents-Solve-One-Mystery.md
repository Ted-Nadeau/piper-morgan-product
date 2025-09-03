The AI Detective Squad: When Three Agents Solve One Mystery
christian crumlish
christian crumlish
5 min read
·
Aug 1, 2025
7






Press enter or click to view image in full size
Three robot detectives work on a mystery
July 12

Sometimes the most interesting bugs aren’t bugs at all — they’re architectural mysteries that reveal how well (or poorly) you’ve designed your system. Yesterday’s “orchestration false positive” investigation turned into a masterclass in domain-driven design, solved by deploying three different AI agents like a detective squad.

The mystery: Why was the UI reporting success when workflows were clearly failing?

The false positive that wasn’t
The problem seemed straightforward. Users would submit requests like “Users are complaining that the mobile app crashes when they upload large photos” and the UI would respond:

“I understand you want to investigate this issue. I’ve started a workflow to handle this.” ✓
[Long pause]
“I’ve completed the analysis but couldn’t generate a summary.” ✗
This looked like a classic orchestration failure. The system was marking workflows complete despite task failures, creating false positives that would erode user trust.

Or so we thought.

Deploying the detective squad
Rather than diving in myself, I decided to try something different: deploy multiple AI agents with different investigation approaches and see what each discovered.

Opus (Principal Technical Architect): Strategic oversight and hypothesis formation

Claude Code: Rapid file navigation and pattern matching

Cursor Assistant: Systematic analysis and architectural investigation

Each got different instructions based on their strengths. Think of it like assigning a tech lead, a senior engineer, and a platform architect to the same bug.

The investigation unfolds
Claude Code’s discovery (the fast tracker)
Claude Code immediately started grep-ing through the codebase looking for success/failure propagation patterns. Within minutes, it found something interesting:

The SUMMARIZE task handler was storing results differently than other analysis tasks:

SUMMARIZE: output_data={"message": response, ...}
ANALYZE_FILE: output_data={"analysis": {"summary": "...", ...}}
But this felt like a symptom, not a root cause.

Cursor Assistant’s systematic analysis (the methodical one)
Cursor took a different approach: mapping the entire workflow state machine and tracing how task failures should propagate to workflow status. The investigation revealed:

Workflow status management was working correctly
Task failure propagation was implemented properly
The UI polling logic was sound
So if everything was architected correctly, why the false positive?

The breakthrough moment
Then we tried actually testing the bug scenario again. And something unexpected happened:

The workflow completed successfully.

No rate limits. No failures. A complete 2,429-character analysis generated and stored properly. The “couldn’t generate a summary” message was… wrong.

That’s when Opus had the insight: this wasn’t an orchestration problem. This was a domain model‒consistency violation.

The domain-driven design revelation
Here’s what we discovered: The UI was correctly expecting analysis results to be structured as workflow.result.data["analysis"]["summary"]. This was the established domain contract, followed consistently by the ANALYZE_FILE handler.

But the SUMMARIZE handler was violating this contract by storing results as {"message": response} instead of following the established pattern.

The “bug” wasn’t that the system was reporting false positives. The bug was that one task handler wasn’t following the domain model that all the others used.

This is exactly why domain-driven design matters. When you have clear, consistent contracts, violations become obvious and easy to fix.

The fix and the victory
The architecturally correct solution was simple: update the SUMMARIZE handler to follow the established domain pattern:

output_data = {
    "analysis": {
        "summary": response,
        "analysis_type": "general_analysis",
        "original_request": original_message,
    }
}
Instead of the contract-violating:

output_data = {"message": response}
Suddenly the UI could find the summary where it expected it, and the mysterious “couldn’t generate a summary” message disappeared.

What this taught us about AI collaboration
The three-AI approach revealed something important about different types of intelligence:

Pattern matching (Claude Code) found the immediate discrepancy quickly but couldn’t assess architectural significance.

Systematic analysis (Cursor) validated that the architecture was sound but couldn’t identify the specific violation.

Strategic reasoning (Opus) connected the technical details to architectural principles and recognized the domain model violation.

Each AI brought different cognitive strengths to the same problem. The combination was more powerful than any individual approach.

Not to anthropomorphize, but this is eerily similar to working with real people with their own panoply of strengths, growth areas, and stuff they really just hate doing or aren’t good at.

The meta-lesson about debugging complex systems
This investigation reinforced something I’ve learned over years of building systems: the most interesting problems aren’t usually what they appear to be.

What looked like an orchestration failure was actually a domain-modeling inconsistency. What seemed like a technical bug was actually an architectural-pattern violation. What appeared to be AI coordination failure was actually a successful discovery of emergent system behavior.

The debugging process was as valuable as the fix. We validated that:

✅ The orchestration engine correctly propagates failures
✅ The workflow state management is sound
✅ The UI polling and status interpretation work properly
✅ The domain model contracts are being followed (mostly)
✅ The architectural patterns catch violations when you look for them
The broader implications
This investigation revealed that Piper Morgan’s architecture is more robust than I thought. The domain-driven design principles we built in are working — they made the contract violation obvious and the fix straightforward.

But it also highlighted the importance of consistency reviews. When you’re building with multiple AI assistants, each implementing different components, it’s easy for domain model violations to creep in. Regular architectural review sessions are essential.

The AI debugging workflow that emerged
The July 12 investigation suggests a pattern for complex debugging with AI assistance:

Strategic AI (Opus) formulates hypotheses and provides architectural context
Tactical AIs (Code, Cursor) execute different investigation approaches in parallel
Human synthesizes findings and makes architectural decisions
All parties collaborate on fixes that maintain domain consistency
This is different from traditional pair programming or even AI-assisted coding. It’s more like having a entire debugging team available instantly.

Looking forward
The “orchestration false positive” turned out to be a domain model consistency check in disguise. The investigation validated our architectural choices while revealing areas for improvement.

More importantly, it demonstrated that debugging complex systems with AI assistance isn’t just about fixing bugs — it’s about validating architectural decisions and discovering emergent system behaviors.

The detective squad approach is now part of our toolkit for investigating complex issues. Different AIs, different perspectives, better solutions.

Next in Building Piper Morgan: How we went from 98% test failures to 87% success (and why breaking tests can be a good thing).

Also, why are the most frustrating bugs always in the last place you look? Just asking.
