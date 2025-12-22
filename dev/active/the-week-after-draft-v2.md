# The Week After

*December 5-9, 2025*

The crisis resolved Thursday night at 10:19 PM. [PLACEHOLDER: Your experience watching that final verification - what it felt like to see the list actually appear after three days of debugging]. By the time we closed our laptops, all four entity pages worked for actual users.

Friday morning brought something different. Not crisis, not urgency, just seven agents working in parallel on what comes next.

## Consolidation as strategy

The Weekly Ship went out first thing. [PLACEHOLDER: Specific details about Weekly Ship #020 "Convergence" - what made that synthesis meaningful to you, what patterns you saw crystallizing].

Then came the backlog. Twenty-two open beads—small tracked tasks that accumulate during sprint work—sat in the system waiting for attention. Not bugs exactly, not features exactly, just the organizational debris that builds up when you're moving fast. The kind of thing that feels low-priority until you realize you're spending mental energy remembering them all.

The solution wasn't to grind through twenty-two items. It was to recognize patterns and consolidate. Four GitHub epics emerged from the chaos: SEC-RBAC work, infrastructure improvements, Slack TDD gaps, and test debt. Twenty-two scattered items became four coherent initiatives. The backlog went from "things we should probably do sometime" to "here are four clear next steps when we're ready."

That consolidation took maybe an hour. But it freed up cognitive space that had been holding all those individual items. Sometimes the most productive work is deciding what *not* to do right now, and putting everything else into a structure that doesn't require constant remembering.

Meanwhile, the mobile track continued. [PLACEHOLDER: Mobile gesture PoC completion - what that felt like in the moment, testing it in Expo Go, your reaction to the entity-based gesture semantics]. The skunkworks model was proving itself—give clear constraints, autonomous execution, focus on "how does it feel" feedback rather than production-ready code.

By lunchtime Friday, four parallel tracks had completed their work without a single coordination issue. Seven agents, four subagents, zero conflicts. Not because we'd built elaborate coordination systems, but because each track had clear boundaries and everyone stayed in their lane.

## The database layer

Sunday morning brought a different kind of problem. CRUD operations were failing again—different symptoms than Thursday's integration gaps, but same result: users couldn't create todos, couldn't upload files, couldn't add projects. The mobile testing revealed something broken deeper in the stack.

Twenty-four hours later, we'd discovered six root causes. Each one seemed like *the* problem until fixing it revealed the next layer. Wrong repository type in dependency injection. Method name mismatches in the Projects routes. BaseRepository expecting kwargs but receiving domain objects. Silent database errors in Files that swallowed exceptions and lied about success. Missing eager loading causing "detached instance" errors.

But the breakthrough came at 6:48 AM Monday morning—technically early Tuesday by the clock—when we finally understood what had been hiding under all five symptom fixes.

The database schema defined `owner_id` columns as UUID type. The SQLAlchemy models defined them as String. PostgreSQL, being strict about types, rejected operations with a type mismatch error at SQL execution time. Every CRUD operation failed at the moment it tried to touch the database, but all the code before that point—including all the unit tests with mocks—passed perfectly.

Schema/model type drift. It explained everything. The previous five "fixes" had been addressing symptoms of this single root cause. We changed five models from `String` to `postgresql.UUID(as_uuid=False)`, and suddenly all four entity pages worked.

Why had this escaped detection so long? Unit tests with mocks bypass database type checking. The migrations changed the schema but nobody updated the models. PostgreSQL is strict about types in ways that auto-casting ORMs hide. We'd been working with a foundational mismatch that only manifested at SQL execution time with a real database.

Integration testing isn't about running more tests. It's about running tests that touch the actual integration points—real databases, real type systems, real constraints. The tests pass when they mock away the very things that break in production.

## Velocity through systematic work

Monday morning, with CRUD operations finally working, we moved to cleanup. Six open issues, ranging from hamburger menu breakpoints to dialog styling problems. The kind of UI polish work that accumulates during alpha testing.

We fixed all six in a few hours. But more interesting was what happened next.

Issue #439 had been sitting in the backlog for weeks: refactor the setup wizard. The main function was 267 lines. Four separate API key sections each duplicated ~100 lines of nearly identical code. This wasn't elegant, but it worked, and we'd been focused on more pressing problems.

Except now we had time to do it right. We extracted a single helper function that handled API key collection generically—keychain check, environment variable check, manual entry, validation. One 148-line function replaced ~400 lines of duplication.

The results: 82% reduction in the API key collection code, 71% reduction in the main wizard function. From 267 lines down to 76 lines for the orchestrator. No functions over 50 lines except justified complex helpers. Zero duplicate code blocks over 10 lines.

The refactoring took about two hours of focused work. But we'd done something important beforehand: we'd created a plan. Forty-five minutes analyzing the problem, identifying the patterns, designing the solution. That analysis meant the implementation went smoothly, with no surprises and no need to backtrack.

Analysis as valuable work—not delay, but acceleration. The hour spent planning saved hours of implementation thrashing.

## Two epics in one day

Tuesday was different. Not debugging, not cleanup, but completion.

The T2 Sprint—test infrastructure improvements—had been building for weeks. We needed smoke tests, the fast subset that could run in CI/CD gates. The goal: mark ~25% of the test suite as smoke tests, target 5 seconds or less execution time.

By noon, we'd profiled 705 tests, identified 656 fast candidates, marked 602 tests as smoke, and validated the suite. Execution time: 2-3 seconds, 40-60% faster than the target. Phantom test rate: less than 1%, excellent test hygiene. Six GitHub issues closed.

The morning's work was complete, comprehensive, and production-ready.

Then came the afternoon. The S2 Sprint—encryption at rest—needed preparation before implementation. Sensitive user data required proper cryptographic protection. But this wasn't the kind of work you just start coding. It needed careful design, compliance mapping, architectural review.

We created a comprehensive review package for Ted Nadeau, our cryptographic advisor. Thirteen specific questions about the architectural approach. Five Whys analysis for every decision. GDPR and SOC2 compliance mapping. A 42-hour implementation gameplan broken into six phases with daily breakdown. Four GitHub issue templates for deferred S3 work.

By evening, the S2 preparation was complete. Not implemented, but ready *to* implement—with all the architectural thinking done, all the questions identified, all the compliance requirements mapped.

Two epics in one day. Not through heroic effort or cutting corners, but through systematic work. The T2 Sprint moved fast because the infrastructure already existed and the scope was clear. The S2 Sprint prep moved fast because we focused on the right question: "What decisions need to be made before we write any code?"

Preparatory work as valuable work. The five hours creating that crypto review package and implementation gameplan would save *days* when Code agents actually implemented the encryption. Every question answered upfront is a question that doesn't derail implementation later.

## What systematic looks like

The week after the crisis looks different than the crisis itself. Thursday night's integration marathon had dramatic tension—users blocked, bugs layered, debugging until past 10 PM. The following week had none of that drama but equal value.

Consolidation work that freed up cognitive space. Database debugging that found root causes instead of applying symptom fixes. Refactoring that eliminated technical debt. Analysis that accelerated future implementation. Epic completion that finished entire initiatives in single days.

This is what systematic building looks like. Not reacting to crises, but working through backlogs methodically. Not rushing fixes, but investigating thoroughly. Not just shipping code, but eliminating duplication. Not just starting work, but preparing properly.

The rhythm matters as much as the outcomes. Friday's seven-agent orchestration showed we could coordinate at scale without coordination overhead. Monday's six-hour refactoring session showed we could do careful work without deadline pressure. Tuesday's two-epic day showed that preparatory work creates velocity, not drag.

By Tuesday evening, we had:
- Clean backlog (22 items → 4 clear epics)
- Working CRUD operations (six-layer root cause resolved)
- Drastically simpler codebase (71-82% reduction in key areas)
- Complete test infrastructure (T2 Sprint done)
- Ready encryption implementation (S2 Sprint prep done)
- Zero open P0 or P1 bugs

None of this made for dramatic storytelling in the moment. There was no 10 PM breakthrough, no crisis resolution, no "it finally works" catharsis. Just five days of systematic execution, each building on the previous day's work.

But that's the point. After you resolve the crisis and fix the integration gaps, the work doesn't stop—it changes character. From reactive to systematic. From urgent to deliberate. From "make it work" to "make it right."

The crisis teaches you what's broken. The week after teaches you how to build sustainably.

---

*Next on Building Piper Morgan: The Milestone Pause, where v0.8.2 reaches production and I take the first real break since May.*

*Have you experienced the shift from crisis mode to systematic building? How did your work rhythm change once the urgent fires were out?*
