The Bug That Made Us Smarter
christian crumlish
christian crumlish
4 min read
·
3 days ago





Press enter or click to view image in full size
A robot insect teaches physics to two students, a person and a robot
“Now pay close attention”
July 9, midday

Picture this: A user types “Users are complaining that the mobile app crashes” and your AI-powered PM assistant responds with… a friendly greeting.

Not “I’ll create a bug ticket for that.” Not “Let me analyze the crash reports.” Just a cheerful “Hello! How can I help you today?”

This is the story of how fixing a simple bug taught us something profound about building AI systems: sometimes being too helpful is the problem.

The mystery of the overly friendly bug reports
It started innocently enough. We were testing PM-011 (GitHub integration, because everything eventually becomes a GitHub integration), and something was… off.

Test Case 1: “We need to add dark mode support”
Result: Creates feature ticket ✅

Test Case 2: “Users are complaining that the mobile app crashes”
Result: “Hello there! How can I assist you today?” ❌

Test Case 3: “The login page is too slow”
Result: TASK_FAILED ❌

One of these things is not like the others. Actually, none of these things were like the others.

Following the breadcrumbs
When your bug classification system classifies bug reports as small talk, you know you’ve got a problem. But where?

Time to channel my inner detective. Or more accurately, time to ask Claude Code to channel its inner detective while I provided coffee and encouragement.

The intent classification pipeline looked like this:

Pre-classifier: Quick pattern matching
LLM classification: The smart analysis
Fallback classifier: When all else fails
Confidence check: The safety net
Somewhere in that chain, “mobile app crashes” was becoming “friendly conversation.”

The plot thickens
Here’s where it gets interesting. The pre-classifier worked perfectly. It correctly identified the bug report. The LLM classification? Also correct when it ran. The fallback classifier? Spot on.

So why were we getting greetings?

The answer was hiding in lines 76–86 of classifier.py. A confidence threshold of 0.7 meant that ANY classification with confidence below 70% got overridden as "CONVERSATION/clarification_needed."

But wait, there’s more.

The road to hell is paved with good intentions
The real culprit was the _seems_vague method. In an attempt to catch truly unclear requests, we'd created a list of "vague" words:

vague_words = ["problem", "issue", "bug", "fix", "improve", "change", "update", "do"]
You see the problem, right? We were literally flagging the words “problem,” “issue,” and “bug” as too vague for our bug tracking system.

It’s like building a fire alarm that ignores any mention of “fire,” “smoke,” or “burning.”

The human moment
At 2:47 PM Pacific (I checked the logs), I had one of those moments. You know the ones. Where you stare at the code and think, “We did this to ourselves.”

The AI wasn’t broken. It was doing exactly what we told it to do. We told it that bug reports were too vague to be bug reports.

We’d been so worried about handling edge cases that we broke the main case.

The fix that taught us
The solution was embarrassingly simple:

Lower the confidence threshold from 0.7 to 0.3
Remove actual bug-related words from the “vague” list
Add word boundary detection (so “it” doesn’t match in “create_item”)
Twenty minutes of changes. Three hours of learning.

What this means for AI development
Building with AI isn’t like traditional programming. When you write a function that adds two numbers, it adds two numbers. When you build an AI classifier, you’re creating something that tries to understand meaning. And meaning is contextual.

Our classifier was technically correct. Bug reports often ARE vague. Users saying “it’s broken” without specifics IS a problem. But in trying to push users toward specificity, we’d made the system unable to recognize when they were being specific about having a problem.

The bigger pattern
This bug exemplifies something I’m seeing throughout Piper Morgan’s development:

Over-engineering the edge cases breaks the common cases.

We see this pattern everywhere:

Markdown formatters that make markdown worse
Test suites that test mocks instead of code
Validation so strict it rejects valid input
Safety checks that make the system unsafe
The test matrix of humility
After the fix, we ran a comprehensive test matrix. Every single test passed. Bug reports were classified as bug reports. Feature requests as feature requests. Even “App crashes” (just two words!) was correctly identified.

The system wasn’t just fixed. It was simpler. More robust. More… intelligent.

By making it less clever.

Lessons for fellow builders
If you’re building AI systems, especially classification systems, here’s what our bug taught us:

Test the obvious cases — We had edge case tests but missed “user reports a bug”
Beware helpful abstractions — Vague detection sounded good in theory
Low confidence doesn’t mean wrong — Sometimes 50% confidence is enough
Domain language matters — “Bug” and “issue” aren’t vague in a bug tracker
Simplicity scales — Fewer rules often means better classification
The philosophy of it all
There’s something beautifully humbling about spending three hours debugging why your bug tracker doesn’t recognize bugs. It’s like Alanis Morissette’s “Ironic,” but actually ironic.

But it also captures why I love building Piper Morgan. Every bug teaches us something. Every fix makes us smarter. Every face-palm moment becomes a blog post. Look, ma, I’m learning in public!

Where we are now
Bug reports are classified as bugs. Feature requests as features. The intent classification pipeline is humming along. And we have a new entry in our “Lessons Learned” document:

“Before adding intelligence, make sure you’re not removing common sense.”

Next week we’ll probably discover our task prioritization system doesn’t recognize the word “urgent.” But that’s next week’s blog post.

Next in Building Piper Morgan: When Your Tests Pass But Your App Fails (or: How we learned to stop mocking and love integration tests)

Ever built a feature that was too smart for its own good? What obvious thing did your clever solution miss? Drop a comment — I’m collecting stories for our hall of fame.
