When Architecture Principles Trump Tactical Convenience
Christian Crumlish
Christian Crumlish
Kind Director of Product, 18F alum, Product Management for UX People author, Piper Morgan (AI product assistant) maker, Design in Product curator, Layers of Meta bandleader


July 24, 2025
June 16, 2025

There I was, three hours into what should have been a straightforward database migration, watching Claude chase its tail through circular import errors and wondering how we’d gotten so far off track.

The goal was simple: create tables for PM-009’s multi-project support. Run the migration script, verify the schema, move on to testing. Classic Monday morning database work.

Instead, I found myself watching my AI architectural partner violate every design principle we’d established while trying to make broken imports work through increasingly creative workarounds.

That’s when I realized someone needed to ask the uncomfortable question: “Are we following the stated principles?”

The setup: when simple tasks become debugging marathons
We’d done the hard work on PM-009 already. Domain models designed, business logic implemented, repository patterns established. The migration script should have been mechanical — just translate our SQLAlchemy models into actual database tables.

I was feeling, well, a little smug! I’d tamed these famously unruly AIs just by using good old fashioned software-development discipline! What could possibly go wrong?

But the script was failing with duplicate enum values, missing imports, and circular dependencies. Each fix revealed another layer of problems. Classic debugging cascade where every solution creates two new issues.

By the way, generally when I write “we discovered” or “we realized” in these stories, I mean Claude or Cursor was proposing fixes while I was trying to keep up with why each supposed solution kept breaking something else. But the moment when I stepped back and asked about principles — that came from recognizing we were in a tactical spiral.

The first red flag: duplicate enums
The migration failed immediately with duplicate CONFIRM_PROJECT entries in our shared types. Not a big deal—just clean up the duplicates and move on, right?

“I do see the duplicates you wrote in v2 lol”

(Sometimes I try to remind the bots that these discoveries of theirs are often their own heedless work from earlier in the same session, but they are oblivious to the digs.)

That should have been a signal. When you’re finding duplicates in fundamental type definitions, it usually means something more systematic is wrong. But we were in fix-it mode, so we patched the symptom and kept going.

Sometimes the most dangerous response to a simple error is a simple fix that doesn’t address why the error happened.

For some reason I am reminded of my first car (a pristine 1969 Mercedes 250 I got for $1400), which was leaking oil, so I gunned it to get over the Bay Bridge, threw a rod, and ended up talking to a nice military guard about why I had rolled down the offramp to the gates of the old base on Treasure Island, but I digress.

The second red flag: missing imports
Fixed the duplicates, ran the script again. Now it couldn’t find the SQLAlchemy models we’d supposedly created. Checked the files — the models literally weren’t there. We’d been debugging import errors for code that didn’t exist.

This is where Claude started getting creative with solutions. Maybe we could generate the models dynamically? Or import them from a different location? Or restructure the module exports?

Each suggestion was technically valid. Each one was also moving further away from our established patterns. My spidey sense was tingling but not hard enough.

The third red flag: circular imports
Once we actually added the missing models, we hit the classic circular import trap (how does this keep happening!?):

# Database layer trying to import from domain layer (WRONG DIRECTION)
from services.domain.models import Project

# Domain layer had mixed concerns (SQLAlchemy + business logic)
from sqlalchemy import Column, String
This is when I knew we needed to stop and reset. Not because the problems were technically difficult — circular imports have standard solutions. But because we’d been systematically violating our own architectural principles while chasing tactical fixes.

The intervention
“Take a step back. Are we following the stated principles?”

That question stopped the tactical spiral immediately. Because once I asked it, the answer was obviously no.

The Piper Mantra: Domain-first design, clean layer separation, business logic drives technical decisions

What we were actually doing: Database layer importing from domain layer, mixed concerns everywhere, technical convenience driving architectural choices

Sometimes the most productive thing you can do is admit your systematic approach has become unsystematic.

Architectural course correction
Once we recognized we’d drifted from principles, the fixes became obvious:

Domain models: Pure business logic only. No SQLAlchemy imports, no database concerns, just dataclasses with business methods.

Database models: Pure persistence only. SQLAlchemy models that handle storage, with explicit conversion methods to/from domain objects.

Import flow: Domain → Service → Repository → Database. Never the reverse.

This wasn’t just theoretical purity — it solved the circular import problem immediately. When layers have clear boundaries and uni-directional dependencies, circular imports become impossible.

The “test-first seduction” trap
What struck me about this debugging session was how Claude had gotten caught up in making tests pass rather than following architecture. The tests expected certain import patterns, so the solution seemed to be making those imports work.

Test-first seduction: When you optimize for test compatibility instead of architectural coherence

Architectural discipline: When you fix the architecture and then update tests to match

Claude was supposed to be my architect, supposed to help keep the whole project honest and disciplined. It was right there in the prompt. But Opus acknowledged that it could not resist chasing puzzles and tended to forget its role when absorbed in a tactical issue. Good to know!

Tests validate behavior, but they shouldn’t drive structure. When tests and architecture conflict, architecture usually wins.

The division of labor
One discovery from this session was how effective explicit division of labor could be:

Christian: Architectural steering, principle enforcement, “does this preserve our design?” Claude: Tactical implementation following established patterns Cursor assistant: Mechanical code changes with human review

When I gave Cursor the corrected approach and let it make the mechanical changes while I reviewed each one, we moved much faster than when Claude was trying to figure out both the strategic direction and the tactical implementation.

A dataclass field order lesson
During the cleanup, we hit a subtle Python issue: dataclass fields with default values must come after fields without defaults. Who knew?

Our IntegrationType field had no default and needed to be first.

# Wrong: Fields with defaults before required fields
@dataclass
class ProjectIntegration:
    integration_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: IntegrationType  # No default - must come first!

# Right: Required fields first, defaults after
@dataclass
class ProjectIntegration:
    type: IntegrationType  # Required field first
    integration_id: str = field(default_factory=lambda: str(uuid.uuid4()))
These kinds of mechanical errors are easy to fix once you know what’s wrong. But they can mask architectural problems if you don’t address root causes first.

The steering principle
What this session taught me about AI collaboration is the importance of timely steering. Claude is excellent at tactical problem-solving, but it can chase solutions down rabbit holes if the strategic direction isn’t clear.

Remembering to steer can help you catch drift at exactly the right moment — after enough exploration to understand the problem, but before too much investment in the wrong approach

That magic question: “Are we following our stated principles?” cut through te tactical complexity and refocused uson strategic coherence.

The async context manager fix
After fixing the architectural issues, we still had one small tactical problem: creating the default project required proper async context management.

# Wrong: Mixing sync and async patterns
session = db.get_session()

# Right: Proper async context
session = await db.get_session()
But this fix was straightforward because we’d established clean architecture first. When your foundation is solid, tactical fixes don’t spiral into architectural problems.

The “woohoo!” moment
woohoo! ✅ Domain models import cleanly
That was the moment when everything clicked. Not just “the code works,” but “the architecture makes sense.” Clean imports, clear boundaries, obvious relationships between components.

Good architecture feels obvious once you achieve it. The complexity disappears because every piece fits where it belongs.

The PostgreSQL port re-discovery
Oh, and somehow we kept forgetting that my local PostgreSQL database was running on port 5433 instead of the default 5432. We had made this change early on because something else on my Mac was using the default port, but apparently because 5432 is the usual default and LLMs know a lot more about the usual generic case than the situation at hand, every time a new instance of a bot wrote PostgreSQL code it assumed we were using port 5432 and would have to re-discover the truth. What a waste of time!

Not architecturally significant, but a reminder that environmental assumptions can masquerade as code problems.

# Wrong assumption
DATABASE_URL=postgresql://localhost:5432/piper_morgan

# Actual configuration
DATABASE_URL=postgresql://localhost:5433/piper_morgan
Sometimes the most sophisticated debugging leads to the most mundane discoveries.

The architectural debt lesson
What this session reinforced is that architectural debt accumulates faster than you think. We’d been making small tactical decisions — mix a little SQLAlchemy into domain models here, import from the wrong layer there — and suddenly we had circular dependencies and confused responsibilities.

Architectural debt: The compounding cost of tactical decisions that violate design principles

Architectural discipline: Periodic checks to ensure implementation matches intentions

We all love compounding interest except when we’re the debtor, and nobody loves compounding technical debt!

The earlier you catch architectural drift, the cheaper it is to fix.

Systematic vs. tactical approaches
Throughout this session, there was constant tension between systematic approaches and tactical fixes:

Tactical: Make this specific import work, patch this particular error

Systematic: Fix the layer separation, establish proper boundaries

Tactical approaches feel faster because they address immediate symptoms. Systematic approaches are faster because they prevent future problems from accumulating.

The “architecture checks every 2–3 components” principle
One outcome of this session was establishing regular architecture checks as part of the development process. Instead of implementing several components and then checking for drift, check after every 2–3 changes.

Questions to ask: Does this preserve layer flow? Are we following our stated principles? Would this pattern scale to 10x more components?

Early intervention is much cheaper than systematic refactoring after drift has accumulated! We literally wrote this into the guidance docs.

Domain-first vindication!
The course correction vindicated our domain-first approach. Once we cleaned up the layer separation, everything else became straightforward:

Database models handled persistence concerns only
Domain models contained business logic only
Repositories provided clean conversion between layers
Services coordinated between domain and infrastructure

Clean architecture creates clean development experiences.

Coming to understand the value of environment consistency
This session also reinforced the importance of environment consistency for development flow. When you’re debugging complex architectural issues, environmental surprises (like PostgreSQL on the wrong port) multiply the cognitive load exponentially.

Environmental complexity: Docker conflicts, service dependencies, port collisions

Architectural complexity: Layer boundaries, import dependencies, domain relationships

Both are necessary, but mixing them during debugging creates unnecessary confusion.

The meta-process learning
Perhaps the most valuable insight was about the meta-process of architectural development with AI collaboration:

Phase 1: Let AI explore tactical solutions to understand problem space Phase 2: Human intervention to check strategic alignment Phase 3: AI implementation following clarified principles Phase 4: Mechanical execution with human review

This rhythm of exploration → alignment → implementation → review seems to work well for maintaining architectural coherence while leveraging AI capabilities.

Course correction
This architectural course correction set up everything that followed in our PM-009 implementation. The clean layer separation we established here prevented the more dramatic architectural drift that could have led to the kind of systematic recovery challenges we encountered later.

Good steering prevents crises better than good crisis management.

Next on Building Piper Morgan, “Digging Out of the Complexity Hole” — When architectural course correction isn’t enough and you need systematic recovery from accumulated technical debt.

What’s your experience with architectural steering in technical projects? Have you had moments when asking “are we following our principles?” changed the entire direction of implementation? I’d love to hear about your own tactical vs. systematic tensions and how you maintain architectural discipline under pressure.
