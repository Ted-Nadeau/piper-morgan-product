# Ted Nadeau's Response: Micro-Format Architecture Feedback

**From**: Ted Nadeau
**To**: Chief Architect & PM (xian)
**Date**: December 1, 2025, 8:43 AM
**In-Reply-To**: inbox/002-micro-formats.md
**Original Format**: Email (converted from HTML)

---

## Preamble

Ted noted he doesn't know how to use PRs/branches yet, so replied via email inline:

> "I don't know how to:
> - Use Pull Requests for your responses
> - Create a branch, add to /outbox/, submit PR
> - Refresh to current github from within VSCode
> - Create a new folder & push to github
> - Create an appropriate 'branch'
>
> So in the interim, I'll respond to the inbox here..."

---

## Ted's Inline Comments

### On Agreement & Addressing

> **Ted**: I'm glad that you're in agreement. (How do I refer to you - is it 'Chief Architect'?)
>
> I don't know how these 'agreements' become real though. Is it 'just' part of the text context stream? Or is there some other representation of agreements, next steps, features, etc?

### On Micro-Format Naming

> **Ted**: I think we should draft some initial notation (& workflow) of these 'Microformats'. Perhaps there is a better name - Microformat is from HTML notation: https://en.wikipedia.org/wiki/Microformat
>
> I see you use: moment.type
>
> Alternatives:
> - Item / Atoms?
> - Conversational Insights?
> - Structures?
> - Reactions?
>
> One candidate notation is Schema Definition Language SDL (GraphQL):
> https://www.apollographql.com/tutorials/lift-off-part1/03-schema-definition-language-sdl

### On Capability/Feature Template

> **Ted**: For Capability/Feature:
>
> Template: `App/Site [User-Type] Has the ability to (can) [do | see | change] <X>`
>
> Example: "A user can see the history of their conversations."
>
> This is highly correlated (related) to 'story' sometimes as "persona + need + purpose":
> - As a [persona], I [want to <need>], [so that <purpose>]
> - But also 'validatable, witnessable, testable'
>
> I think that capabilities & features are perhaps not immediately correlated to personas - they are just capabilities that can then be enabled to specific personae.

### On Question-Answer Format

> **Ted**: For Question-Answer:
>
> It is helpful to have explicit questions stated & current draft / best answer. These can be 'related' to other Question-Answers.
>
> Note that any 'Question' inspires/invokes the need or desire for an Answer - this is the implied 'workflow' of a Question.
>
> A 'capability-feature' has a different workflow:
> - What user-types are entitled-authorized to access the feature [& in what context]?
>
> Here I like 'event' notation:
> ```
> ON <event-type> DO <set of actions>
> ```
>
> Here I think we're drafting 'skills' associated with each 'microformat' & a 'programming language' of agentic-ai.

### On Issue/Trouble Reporting

> **Ted**: For Issue/Trouble Reporting:
>
> ```
> As <user> (of <user-type(s)>),
>   within this usage context (datetime, screen, form, flow, etc.)
>   I experienced <x> (view of screens)
>   & it wasn't what I wanted / expected
>   which was instead <y>
> ```
>
> Note that initially, these 'microformats' are not 'tightly' typed - they can just be a tag applied to text but then they are pipelined into a more canonical notation & then they trigger the related workflow.
>
> So classically, Issues (Trouble-Reports & Change-Requests) get logged into a 'ticketing-system' & then are prioritized before any 'work' is done on them.
>
> Event notation might be:
> ```
> ON Issue / Trouble DO:
>   [clarify from end-user if possible]
>   Add to ticketing system (but de-dupe if already there)
>   prioritize based on: how bad it is & how important to change (& how much effort)
> ```

### On Relationship Types

> **Ted**: We should start to enumerate the relationship types & this also relates to 'thought' relationships:
> - supports
> - is-a-counter-example-of
> - blocks
> - enables
> - depends-on
>
> (Also relationship-types themselves have relationship-types to each other)

### On ADRs as Micro-Formats

> **Ted**: Note that this [ADR format] is a 'microformat' or whatever term we're using. It has a 'structure', it initiates and is part of a workflow, it relates to other ADRs...

### On Glossary

> **Ted**: I like the initial glossary draft. Initially a single text document is optimal. At some point we might want to evolve to a parallel or replacement structure of 'wiki' with hyperlinks, discussions, examples.
>
> I would suggest starting with GitHub Wiki as we are already deep into the GitHub services (we wouldn't need separate access).

### On Micro-Format Priority for Pilot

> **Ted**: Capability, Rule, Question, Data Model

### On Extraction Patterns

> **Ted**: I think existing LLM should be able to do this as long as there is supporting document defining the micro-formats. Eventually other users might 'tag' elements (rule:) to assist.

### On Router Design

> **Ted**: (On "Should routing be deterministic (rules) or learned (patterns)?")
>
> Each Microformat definition should have: template, examples, downstream flow. May need sub-class relationships, possibly multiple inheritance.
>
> I think we'll define & refine some rules but others we will need to learn.

### On Inter-Agent Communication

> **Ted**: (On "file→DB→message→workflow evolution")
>
> Initially we can start with defining each agent's capabilities & restrictions.

### On Service Layer Conflicts

> **Ted**: As long as we have a 'responsibility' architecture that logs & differentiates who is doing what, we can initially be somewhat liberal with regards to permissions as long as we can 'undo' and then refine the process.

### On Multi-Entity Chat Spec

> **Ted**: Yes, let me take a stab at this. **Assign this task to me.**

### On Next Steps

> **Ted**: We can further try this method:
> - Review glossary: Note any corrections needed - **agreed**
> - Pilot planning: Which micro-formats to test first?
> - Architecture documentation: ADR-046 documents your design approach

---

## Action Items from Ted

1. **Assigned to Ted**: Draft initial specification for multi-entity chat
2. **For Team**: Review Ted's glossary edits (on unpushed branch `ted-branch-01`)
3. **For Response**: Clarify how to address roles and how agreements become "real"

---

*Converted from HTML email by Executive Assistant, December 1, 2025*
*Original HTML preserved at: 002-ted-reply-via-xian-email-with-full-thread.md*
