When Multiple AIs Drift Together
Christian Crumlish
Christian Crumlish
Kind Director of Product, 18F alum, Product Management for UX People author, Piper Morgan (AI product assistant) maker, Design in Product curator, Layers of Meta bandleader


July 23, 2025
June 15, 2025

There I was, feeling pretty confident about our multi-AI development process. Claude Opus handling architecture reviews, Claude Sonnet doing detailed implementation planning, Cursor providing code execution support. Three different AI perspectives, multiple layers of review, comprehensive test-driven development approach.

And we still managed to create duplicate domain models without anyone catching it.

This is the story of how even systematic AI collaboration can drift into architectural anti-patterns, and why human oversight remains the critical factor in maintaining architectural discipline.

The setup: confidence in systematic process
We’d been developing Piper Morgan with what felt like a bulletproof process. Every major feature went through multiple review stages:

Architecture review (Claude Opus) — High-level design and pattern consistency
Implementation planning (Claude Sonnet) — Detailed step-by-step approach
Code execution (Cursor) — Syntax assistance and local development support
Test-first discipline — Comprehensive test suite before any implementation

For tickets PM-001 through PM-008, this process had worked beautifully. Clean implementations, passing tests, architectural consistency maintained.

Those first few issues flew by so fast I barely remember executing them.

Then came PM-009: multi-project support. And everything that could go wrong with our process… did.

The architectural drift discovery
The first sign of trouble came during implementation. Cursor was trying to import the Project class and kept getting confused about which one to use:

# This should have been obvious, but wasn't:
from services.domain.models import Project       # Business logic model
from services.database.models import Project     # SQLAlchemy model
Two Project classes. Same name, different purposes, different locations. Both created by our systematic multi-AI process. Both reviewed and approved.

None of us — human or AI — had caught the fundamental naming collision.

The example code trap
How did three AI systems and a human miss something so fundamental? The answer was hiding in the architectural examples we’d been following.

The example code showed the structure of domain and database separation:

# Domain layer - pure business logic
class Project:
    def __init__(self, id: str, name: str):
        # Domain logic here

# Database layer - persistence
class Project(Base):  # SQLAlchemy model
    id = Column(String, primary_key=True)
    # Database fields here
The structure was correct. The separation was proper. But the example didn’t specify the naming convention for avoiding collisions.

We all saw “domain model + database model” and correctly implemented the separation. None of us saw “same name in different modules = import collision” until we tried to use both classes in the same scope.

The multi-AI blind spot
What’s fascinating about this failure is how each AI system made the same logical assumption:

Claude Opus (Architecture): “Domain and database layers should be separate” ✅
Claude Sonnet (Implementation): “Create Project models in both layers” ✅
Cursor (Execution): “Import Project class as needed” ❌ Which one?

Each step was individually correct. The compound result was architectural confusion.

By the way, every time I say “we missed” or “we realized” here, I should clarify that this was happening across multiple AI collaboration sessions. But the moment of recognizing the naming collision — and realizing it represented a fundamental process gap — that came from stepping back and asking “why is this so confusing?”

The key thing is a third (really fourth) point of view entered the project and immediately found a flaw none of the rest of us had seen yet.

The systematic review illusion
Here’s what was most humbling about the experience: we’d had comprehensive reviews. Opus had specifically called out concerns about “type safety regression” and “responsibility diffusion.” Sonnet had created detailed implementation plans with step-by-step verification.

But none of our systematic reviews had caught the basic naming collision.

Our review caught complex architectural interactions, business logic edge cases, integration patterns, but they missed things like simple naming conventions and import practicalities

This is like having a thorough structural engineering review that catches load-bearing calculations but misses that two different beams have the same catalog number.

The test-driven development assumption
We’d been following test-driven development religiously: write comprehensive tests first, then implement to satisfy the tests. The tests were thorough, covering business logic, error cases, integration scenarios.

But the tests assumed the implementation would follow naming conventions that we’d never explicitly established.

# Test assumed this would work:
from services.domain.models import Project
from services.database.models import ProjectDB  # We never created ProjectDB!
The tests were architecturally correct. Our implementation didn’t match the architectural assumptions the tests were making. We were using TDD (test-driven development) and forgetting to keep employing DDD (domain-driven design) as we did o, which to the basic PM in me means “check the stuff we already did and use that before making up new stuff.”

This taught me that test-driven development requires explicit architectural conventions, not just business logic specifications.

The “STOP — Architectural Decision Required!” moment
The turning point came when Cursor started suggesting breaking our domain-first architecture principles to work around the import collision. When I brought back the proposal with my concerns it set off Claude’s architectural alarm:

STOP — Architectural Decision Required! 🚨 Your copilot is suggesting breaking our core domain-first architecture principle.
The collision wasn’t a problem to solve with clever imports — it was a signal that our architectural implementation had drifted from our architectural intentions.

The TDD discipline check
Another humbling discovery was realizing we’d even violated our own TDD discipline without noticing. We’d written comprehensive tests, then implemented based on our understanding rather than implementing to satisfy the tests.

TDD principle: Let tests drive implementation decisions

What we did: Implement based on architectural assumptions, then debug why tests failed

Six test failures, all from method signature mismatches. The tests expected llm.complete() calls; our implementation used llm.infer_project_id(). The tests were right. Our implementation was guessing.

Complex features don’t excuse abandoning good process — they require more discipline, not less.

The architectural anti-pattern recognition
Once we recognized the naming collision, we could see the broader anti-pattern:

Anti-pattern: Same entity name in multiple layers

Correct pattern: Layer-specific naming with explicit mapping

# Anti-pattern (what we built):
services.domain.models.Project
services.database.models.Project

# Correct pattern (what we should have built):
services.domain.models.Project       # Business logic
services.database.models.ProjectDB   # Persistence + mapping methods
The fix required systematic refactoring, but once we made the change, everything else became obvious.

The human oversight revelation
The most important insight from this experience was about the irreplaceable role of human oversight in AI collaboration.

AIs are excellent at following patterns, implementing specifications, and maintaining consistency within established frameworks. But they can collectively drift when the framework itself has gaps.

AIs caught complex logic errors, business rule violations, integration issues, but my human oversight became essential for recognizing when systematic process had systematic blind spots

The human role isn’t just coordinating AI systems — it’s maintaining architectural vigilance that spans multiple AI perspectives.

The discipline to stop and fix root causes
When we discovered the architectural anti-pattern, we had a choice:

Patch it: Use import aliases and namespaces to work around the collision
Fix it: Rename one class and establish proper naming conventions

Patching always feels faster. Fixing can feel like “going backwards” but architectural problems that get patched instead of fixed tend to compound. We chose systematic repair over tactical workarounds.

Collaboration pattern insights
The experience taught me several things about effective AI collaboration:

Multiple perspectives help but don’t guarantee correctness: Each AI system brought valuable insights, but they could all miss the same fundamental issue.

Reviews need explicit checklists: “Does this follow our patterns?” isn’t enough. “Are there naming collisions?” needs to be a specific check.

Implementation-time validation matters: Even with thorough planning, drift happens during execution. Regular “does this match our intentions?” checks are essential.

Human pattern recognition is different: AIs excel at consistency within established patterns. Humans are better at recognizing when patterns themselves need revision.

A test-first architecture lesson
One outcome of the debugging session was establishing “test-first architecture” as a discipline:

Test-first development: Write tests before implementation Test-first architecture: Make architectural assumptions explicit in test structure

Our tests assumed ProjectDB naming but we'd never explicitly documented that convention. The tests were more architecturally correct than our implementation.

Sometimes your tests know more about good architecture than your implementation does.

A systematic recovery template
The process we used to recover from the architectural drift became a template for future issues:

Stop adding complexity — No more patches or workarounds
Identify the root pattern violation — Naming collision, not import issue
Fix systematically — Rename + establish conventions, don’t just patch
Verify architectural alignment — Make sure fix matches intended patterns
Document the lesson — Update process to prevent recurrence

This systematic approach to architectural problems became part of our standard toolkit.

Recalibrating my confidence in these assistants
Perhaps the most valuable outcome was recalibrating confidence in our systematic process. Multiple AI perspectives are incredibly valuable, but they’re not infallible.

Less “We have systematic reviews, so architectural drift won’t happen” and more “We have systematic reviews, so architectural drift will be caught quickly.”

The difference is subtle but important. Good process doesn’t prevent all problems — it makes problems visible and recoverable.

The importance of architectural examples
This experience also taught me about the responsibility of creating architectural examples. Examples that show structure without naming conventions can mislead even systematic implementors.

Good examples need:

structure + naming + boundaries + common pitfalls

(Incomplete examples create correct understanding of relationships but incorrect implementation details.)

Example creators bear responsibility for the blind spots their examples might create.

Insight about compound AI wisdom
What I learned about AI collaboration is that compound AI wisdom isn’t just additive — it’s multiplicative when working well, but it can also multiply blind spots when all systems make the same assumption.

Different perspectives catch different issues and shared assumptions can hide fundamental problems

The solution isn’t “fewer AI perspectives” — it’s better coordination and explicit human oversight of the coordination process.

Practicing architectural vigilance
The most practical outcome was establishing “architectural vigilance” as an explicit practice:

Regular questions: Are we following our own patterns? Do our implementations match our intentions? Are we creating accidental complexity?

Explicit checks: Naming consistency, import cleanliness, layer separation, pattern adherence

Human responsibility: Maintaining architectural perspective that spans multiple AI contributions. What I like to call :the primate in the loop.”

Vigilance isn’t (just) about not trusting AI systems — it’s about taking responsibility for the overall architectural coherence they help create.

The foreshadowing…
Looking back, this architectural drift experience set up everything that followed. The systematic recovery approach we developed here became the foundation for handling the complexity accumulation that built up through PM-009.

Learning to catch and fix architectural drift quickly made it possible to manage the technical debt that accumulated during more complex implementations.

Next on Building Piper Morgan: more tales of white-knuckle architectural rigor when we are getting tired and just wanna go home!

What’s your experience with AI collaboration and architectural oversight? Have you seen systematic processes miss fundamental issues? I’d love to hear about your own experiences with multiple AI perspectives and the human oversight that makes them effective.
