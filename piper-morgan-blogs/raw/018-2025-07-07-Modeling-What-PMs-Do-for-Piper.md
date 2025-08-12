Modeling What PMs Do for Piper
Christian Crumlish
Christian Crumlish
Kind Director of Product, 18F alum, Product Management for UX People author, Piper Morgan (AI product assistant) maker, Design in Product curator, Layers of Meta bandleader


July 19, 2025
June 7, 2025

There’s a moment in every product’s development when you realize you’re solving your own problem. For me and Piper Morgan, June 7 was that day. While manually parsing markdown files to create GitHub issues and tracking progress in a chat window, it hit me: I was doing exactly what Piper Morgan was supposed to automate.

The irony was intriguing.

The documentation reality check
The day started with a harsh truth. Reading through my documentation, it was… optimistic. Very optimistic. Like “we’ll have AGI by Tuesday” optimistic.

Sample from the original:

“Piper Morgan seamlessly orchestrates complex workflows across multiple systems while learning from every interaction to provide increasingly sophisticated insights.”
What it should have said:

“Piper Morgan has a sophisticated architecture with significant implementation gaps. Currently converts all user requests into GitHub tickets, including requests to improve itself.”
I started to wonder if these docs were being written by the PR department at Tesla.

The GitHub token dance (redux)
Creating a script to parse my backlog and generate GitHub issues should have been simple. It wasn’t.

github_token = os.getenv('GITHUB_TOKEN')
repo = g.get_repo("mediajunkie/piper-morgan-platform")
repo.create_issue(title=title, body=body, labels=labels)

Error: 403 Forbidden.
But I have a token! With permissions! Or… do I? Didn’t this happen a week ago? Can you tell I’m not a real dev?

Turns out I was somehow again using the token that only had issues:read permission. Not issues:write. Because why would you want to CREATE issues with a personal access token? That would be crazy.

Twenty minutes and three token regenerations later (each time discovering new permission requirements), I realized I already had a had a classic token with full repo scope (a two-way PAT). Sometimes the old ways are best.

A meta-learning moment
As I watched my script create 23 GitHub issues from markdown, then manually updated each one with proper formatting, then tracked progress in my session log, then updated GitHub again… the absurdity hit me.

I was:

Parsing structured data (markdown backlog)
Transforming it (GitHub issue format)
Executing API calls (creating issues)
Tracking state (progress checkpoints)
Updating multiple systems (GitHub + session logs)

This wasn’t development. This was product management. And I was doing it manually while building a tool to automate product management.

Database drama
PM-001 (the first issue on our new roadmap!) seemed simple: initialize the database schema. How hard could it be?

CREATE TABLE intents (
    id UUID PRIMARY KEY,
    message TEXT NOT NULL,
    classified_intent VARCHAR(100),
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
Run the script. Check the database. Empty. Run it again. Still empty.

The problem? My initialization script was connecting from outside the Docker network. PostgreSQL was listening on localhost inside the container, not outside. The script was successfully connecting to... nothing.

Solution: Run the script inside the Docker container. Or better yet, let the application initialize its own schema. Sometimes the best automation is no automation.

The beautiful mundane
By the end of the session, I had:

6 documentation files rewritten with honest assessments
23 GitHub issues created and properly labeled
One database schema initialized and verified
A repository pattern implemented for clean data access
Progress tracked in multiple places

None of it was exciting. All of it was necessary.

The real insight wasn’t technical. It was realizing that the manual orchestration I was doing — breaking down work, creating tickets, tracking progress, updating stakeholders — was exactly what Piper Morgan should handle.

Pattern recognition
What emerged was a clear pattern:

Parse structured information (backlog → issues)
Transform to appropriate format (markdown → GitHub API)
Execute with proper error handling (permissions, labels, state)
Track progress across systems (GitHub, logs, documentation)
Update all stakeholders (comments, documentation, status)

This is product management. Not the strategic thinking part — the execution part. The part that takes 60% of our time and could be automated.

Documentation as development
The documentation rewrite wasn’t just about honesty. It was about understanding what we were really building. Each “sophisticated architecture with implementation gaps” was a roadmap item. Each “currently converts all requests to tickets” was a feature boundary.

Good documentation doesn’t just describe what is — it clarifies what should be. Documentation often feels like a burden. Like homework. The boring part. I want to ship code, not write about it! But code is writing and documentation informs code.

We write docs for future us and for people who have to understand our work who were never us. And, increasingly, we are writing docs so AIs can understand what we are working on and help us with it.

Next steps, with clarity
With PM-001 complete and PM-002 in progress, the path was clear. But more importantly, the meta-pattern was clear. Every manual step in my development process was a feature for Piper Morgan:

Parsing backlogs → Backlog ingestion feature
Creating issues → Issue generation (already building)
Tracking progress → Workflow monitoring
Updating documentation → Automated status reports

We weren’t just building a PM assistant. We were automating ourselves out of the mundane parts of product management.

Today’s lesson
Sometimes the best requirements gathering is doing the work manually first. Every frustration, every repetitive task, every “there must be a better way” moment — those are your features.

Today I was my own user. And my own pain points became Piper Morgan’s roadmap.

The script that created 23 GitHub issues? That’s now part of Piper Morgan’s DNA. The documentation generator? Future feature. The progress tracking? Core functionality.

We’re not just eating our own dog food. We’re building the entire kitchen.

Next in Building Piper Morgan: Helping a robot know lots of little things before it can known one big thing.

Have you ever prototyped a process or workflow manually before trying to automate it? Highly recommended!
