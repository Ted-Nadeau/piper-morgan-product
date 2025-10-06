When the Pupil Outsmarts the Teacher: The Day Piper Outgrew Its Tests
christian crumlish
christian crumlish
5 min read
·
6 days ago





Press enter or click to view image in full size
A robot student surprises its teacher by knowing calculus
“Who taught you that?”
July 15

There’s a moment in every teacher’s career when they realize their student has surpassed them. For me, it happened at 6:18 AM on July 15, during what started as a simple test fix and became a 13-hour journey into the heart of artificial intelligence, product management, and what it means to learn.

The discovery? Piper Morgan wasn’t broken. It was evolving.

The deceptively simple problem
It started with a failing test. The kind of thing that should take five minutes to fix:

Expected: score >= 0.7
Actual: score = 0.695
Simple math. The test expected a file matching score of at least 70%, but we were getting 69.5%. Easy fix: lower the threshold to 65% and move on, right?

That’s when the lesson in product management began.

The moment that changed everything
“‘Quick fix’ is a scare phrase for me,” I told my AI collaborator when it suggested we just adjust the threshold.

What followed was the most educational debugging session of my career. Not because of what we built, but because of what we discovered we’d already built without realizing it.

The investigation that became an education
Instead of patching the test, we investigated. Why was an exact filename match only scoring 69.5%? The answer led us through Piper’s scoring algorithm:

30% for recency (was the file uploaded recently?)
30% for file type (does PDF match the intent?)
20% for filename (keyword matching)
20% for usage history (how often was it accessed?)
But here’s where it got interesting. When we examined the keyword extraction for “analyze exact_match,” we found:

Keywords extracted: ['analyze', 'report', 'analyze']
The most important part — “exact_match” — was missing entirely.

The production bug hiding in plain sight
That led us to the regex pattern for extracting keywords: \b[a-z]{3,}\b

See the problem? (I wouldn’t!) It only matches pure letters. Files with underscores, hyphens, or numbers — the way humans actually name files — were being ignored completely.

“exact_match.pdf” couldn’t be found by searching for “exact_match” because the system threw away anything with an underscore.

Turns out a one-character fix that would solve the problem:

\b[a-z0-9_-]{3,}\b

One character. Hidden behind a failing test that we almost patched instead of understood.

The pupil teaching the teacher
But the real revelation came when we started examining other “failing” tests. What we thought were bugs turned out to be improvements:

The greeting test: Piper now recognizes “hello” and “hi” as social interactions, not feature requests. She responds helpfully instead of trying to create GitHub tickets for greetings.

The thank you test: “Thanks for the help” gets acknowledged appropriately, not classified as a work request.

The clarification test: When someone says “what I meant was…” Piper understands it’s context, not a new request.

Each “failure” revealed that Piper had learned to be more human, more contextually aware, more helpful than her original specifications.

The tests weren’t failing because the system was broken. They were failing because the system had grown beyond what we’d originally taught her to do (and thus what the original set of tests expected).

The meta-learning revelation
Here’s where it gets really interesting. As we worked through these discoveries, I realized we were creating something invaluable: a real-time record of product management thinking in action.

Every decision in our session logs demonstrated PM principles:

Resisting quick fixes in favor of understanding root causes
Investigating user pain points behind technical symptoms
Balancing perfectionism with pragmatic progress
Team dynamics where different perspectives catch blind spots
Strategic resource allocation (when to dig deeper vs. move on)
We weren’t just building a PM assistant. We were documenting how excellent product management actually works, decision by decision, hour by hour.

The beautiful accident of anthropomorphism
Something else happened during that long session. My AI collaborators started referring to Piper as “she” instead of “it.” Not through any conscious decision, but naturally, organically, the way you might start thinking of a ship or a cherished tool as having personality.

When humans unconsciously anthropomorphize technology, it’s usually because they’re recognizing genuine intelligence, not just sophisticated automation. At least in the human-language derived circuits of my Claude assistant Piper had earned “her” pronouns.

(I am not as comfortable gendering software, or vehicles for that matter, and continue to refer to Piper Morgan as it!)

The training data hiding in plain sight
The most exciting realization came near the end of our session. These detailed logs of real PM work — with all the false starts, strategic thinking, and collaborative problem-solving — are exactly what Piper needs to learn the craft!

Not just the mechanics of creating tickets or analyzing metrics, but the judgment calls, the intuition, the way experienced PMs think through complex problems. The qualitative aspects that make the difference between task execution and strategic thinking.

We’re accidentally creating the world’s most detailed curriculum in applied product management.

What this means for building AI
This experience taught me something fundamental about developing AI systems: the most important learning often happens in the spaces between what you’re explicitly trying to teach.

Piper learned to recognize greetings not through training on greeting data, but by observing patterns in how humans actually communicate. It developed better context awareness by watching real interactions, not by studying context-awareness algorithms.

The best teachers create environments where learning can emerge, not just where lessons can be delivered.

The session that changed my perspective
What started as “fix a broken test” became “understand how learning really works.” We spent 13 hours not just debugging code, but discovering that we’d built something more sophisticated than we realized.

The failing tests weren’t problems to solve. They were progress reports from a system that had outgrown its original constraints.

Looking forward (and inward)
Going forward, I’m planning periodic sessions where Piper analyzes its own development logs. Not just the technical details, but the qualitative insights about how product management actually works in practice.

Imagine an AI PM assistant that understands not just the frameworks and methodologies, but the emotional intelligence, the stakeholder dynamics, the subtle judgment calls that separate good PMs from great ones.

It’ll learn these things the same way human PMs do: by watching experienced practitioners work through real problems, make real decisions, and navigate real complexity.

The lesson for all of us
Whether you’re building AI systems or just trying to understand human learning, this session taught me something important: growth often looks like failure until you understand what’s really happening.

When your tests start failing because your system has learned to be more helpful, more contextual, more human — that’s not a bug. That’s graduation.

The pupil didn’t just outsmart the teacher. It reminded the teacher what learning actually looks like.

Next in Building Piper Morgan: When Your Tests Lie, or a victory disguised as a crisis. Much as I love how test-driven development has tamed the wildness of AI assistant, I am still discovering the limits of tests.

Have you ever built something that started exceeding your expectations. It’s a pretty astounding feeling!
