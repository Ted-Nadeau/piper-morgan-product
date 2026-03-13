# Chief Architect Briefing: Ted Nadeau's Micro-Format Architecture Input

**Date**: December 1, 2025
**From**: Executive Assistant (Claude Code)
**To**: Chief Architect
**Re**: Advisor input on ADR-046 Micro-Format Agent Architecture

---

## Executive Summary

Ted Nadeau has provided substantive architectural feedback on the micro-format concept introduced in ADR-046. His input validates the approach while offering specific implementation suggestions worth considering.

---

## Key Architectural Contributions

### 1. Naming Concern

Ted notes that "Microformat" is an established HTML term (W3C spec, see [Wikipedia](https://en.wikipedia.org/wiki/Microformat)). He suggests alternatives:
- `Moment.type` (aligns with our grammar)
- Conversational Insights
- Structures
- Reactions

**Recommendation**: Consider "Conversational Structures" or simply keep using `Moment.type` to stay aligned with ADR-045's "Entities experience Moments in Places" grammar.

### 2. Template Proposals for Core Types

Ted proposes concrete templates for three micro-formats:

| Type | Template | Example |
|------|----------|---------|
| Capability/Feature | `App/Site [User-Type] Has the ability to [do\|see\|change] <X>` | "A user can see the history of their conversations" |
| Question-Answer | Explicit Q with draft/best answer + related Q&As | Q: "How do agreements become real?" A: [draft] |
| Issue/Trouble | `As <user> within <context> I experienced <X> but expected <Y>` | Trouble report format |

He notes that capabilities/features are not immediately correlated to personas - they are capabilities that can then be enabled to specific personae.

### 3. Event Notation Suggestion

```
ON <event-type> DO <set of actions>
```

This aligns with skills/workflow patterns already in our orchestration layer. Ted frames this as "drafting 'skills' associated with each microformat & a 'programming language' of agentic-ai."

### 4. GraphQL SDL as Notation Candidate

Ted suggests Schema Definition Language (GraphQL) as a candidate notation system for defining micro-formats formally. Reference: [Apollo GraphQL SDL Tutorial](https://www.apollographql.com/tutorials/lift-off-part1/03-schema-definition-language-sdl)

Worth exploring for the formalization phase.

### 5. Meta-Observation: ADRs ARE Micro-Formats

Ted observes that ADRs themselves fit the micro-format pattern:

> "Note that this is a 'microformat'... It has a 'structure', it initiates and is part of a workflow, it relates to other ADRs."

This validates the recursive/self-hosting nature of the architecture.

### 6. Relationship Types

Ted emphasizes the need to enumerate relationship types between micro-formats:
- blocks
- enables
- depends-on
- supports
- is-a-counter-example-of

He also notes that "relationship-types themselves have relationship-types to each other" (meta-relationships). This connects to thought relationships in argumentation systems.

---

## Questions Ted Raised (Needing Response)

### 1. How to address roles
> "Is it 'Chief Architect'?"

We should clarify naming conventions for advisor communications. Options:
- Use role titles (Chief Architect, PM)
- Use names (xian, Claude)
- Use both contextually

### 2. How agreements become real
> "Is it just part of the text context stream? Or is there some other representation of agreements, next steps, features, etc?"

This is a fundamental question about our tracking/reification of decisions. Current answer: Agreements are captured in:
- ADRs (architectural decisions)
- GitHub issues (actionable work)
- Roadmap documents (strategic direction)
- Session logs (context and attribution)

But Ted's question suggests we may need a more explicit "agreement register" or decision-tracking mechanism.

---

## Recommended Actions

1. **For ADR-046**: Incorporate Ted's template proposals as examples in the ADR

2. **For Tomorrow's Pairing**: Help Ted push his `ted-branch-01` branch containing glossary edits

3. **For Naming**: Decide whether "micro-format" stays or gets renamed to avoid confusion with HTML microformats

4. **For Glossary**: Review Ted's edits when his branch arrives

5. **For Process**: Answer Ted's two questions in next communication

---

## Ted's Work Status

| Contribution | Format | Status |
|--------------|--------|--------|
| Email reply on micro-formats | HTML email in outbox | Available (markdown conversion in progress) |
| Glossary edits + outbox folder | Git branch `ted-branch-01` | On Ted's local machine, not yet pushed |

---

## Process Note

Ted is engaging enthusiastically despite Git workflow friction. Tomorrow's pairing session should unblock his contributions. His willingness to work around obstacles while learning the system is valuable - he's simultaneously user-testing the advisor mailbox workflow.

**Observations for process improvement**:
- Manifest staying out of sync creates friction
- Email-as-workaround works but creates large HTML blobs needing conversion
- Agent trigger is just a briefing instruction - no enforcement mechanism
- Consider: exec assistant daily check of advisor mailbox

---

## Source Materials

- Email reply: `advisors/ted-nadeau/outbox/002-ted-reply-via-xian-email-with-full-thread.md`
- Inbox message Ted responded to: `advisors/ted-nadeau/inbox/002-micro-formats.md`
- Related ADR: `docs/internal/architecture/current/adrs/adr-046-micro-format-agent-architecture.md`

---

*Prepared by Executive Assistant (Claude Code Opus) - Session 2025-12-01-1746*
