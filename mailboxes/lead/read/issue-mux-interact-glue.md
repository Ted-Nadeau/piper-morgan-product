# MUX-INTERACT-GLUE: Conversational Glue Design Brief

## Summary

Design the interaction patterns that create natural conversational flow—the connective tissue that makes conversations feel coherent rather than transactional.

## Problem Statement

Current state: Piper can classify intents and respond to individual requests. But conversations feel like discrete transactions rather than flowing dialogue.

**What's missing**: The "glue" between turns—context carry-over, natural follow-ups, topic transitions, acknowledgment patterns.

**Example of the gap**:
```
User: "What's on my agenda tomorrow?"
Piper: [responds with tomorrow's agenda]
User: "How about today?"
Piper: [should understand this is same query, different day]
        [currently may not handle this naturally]
```

## Scope

### In Scope

| Component | Description | Example |
|-----------|-------------|---------|
| Context carry-over | Maintaining relevant context between turns | "How about today?" understands previous query |
| Natural follow-ups | Recognizing continuation vs new topic | "And what about Friday?" |
| Topic transitions | Graceful handling of topic changes | "Actually, let me ask about something else" |
| Acknowledgment patterns | Confirming understanding before proceeding | "Got it, updating that now..." |
| Clarification flows | Asking for missing info naturally | "Which project did you mean?" |
| Conversational repair | Recovering from misunderstandings | "Sorry, I thought you meant X. Let me try again." |

### Out of Scope (Handled Elsewhere)

| Component | Where Handled |
|-----------|---------------|
| Intent classification | #619 (Grammar Transform) |
| Multi-intent parsing | #595, #427 |
| Process-level context | ADR-049 (Two-Tier Intent) |
| Conversation structure | ADR-050 (Conversation-as-Graph) |
| Memory persistence | ADR-054 (Cross-Session Memory) |

## Infrastructure Available

We have significant infrastructure that this work should build on:

| ADR | What It Provides |
|-----|------------------|
| ADR-024 (Persistent Context) | Preference hierarchy, context persistence |
| ADR-049 (Two-Tier Intent) | Process-level vs turn-level classification |
| ADR-050 (Conversation-as-Graph) | Node types, conversation structure |
| ADR-054 (Cross-Session Memory) | Three-layer memory model |
| ADR-055 (Object Model) | "Entities experience Moments in Places" grammar |

**Gap**: These ADRs provide infrastructure. This issue provides **interaction design**—how that infrastructure manifests in user experience.

## Design Questions to Answer

1. **What triggers context carry-over?**
   - Pronouns ("it", "that", "those")?
   - Temporal references ("today" after "tomorrow")?
   - Implicit topic continuation?

2. **How long does context persist?**
   - Within turn? Within session? Across sessions?
   - What causes context to "expire"?

3. **What acknowledgment patterns feel natural?**
   - When should Piper confirm before acting?
   - When should Piper just act?
   - How verbose should confirmations be?

4. **How does Piper handle ambiguity?**
   - Ask for clarification?
   - Make best guess and confirm?
   - Present options?

5. **What does conversational repair look like?**
   - How does Piper recognize it misunderstood?
   - How does it recover without being awkward?

## Deliverables

1. **Conversational Glue Pattern Catalog**
   - Named patterns for each glue type
   - When to use each pattern
   - Example dialogues

2. **ADR Update or New ADR**
   - Document decisions on above questions
   - May extend ADR-049 or create new

3. **Implementation Guidance**
   - How patterns map to existing infrastructure
   - Where new infrastructure is needed

## Related Issues

| Issue | Relationship |
|-------|--------------|
| #427 | MUX-IMPLEMENT-CONVERSE-MODEL - will implement these patterns |
| #595 | MUX-INTENT-MULTI - multi-intent is one aspect of glue |
| #625 | GRAMMAR-TRANSFORM: Conversation Handler - grammar alignment |
| #488 | MUX-INTERACT-DISCOVERY - discovery relates to follow-up suggestions |

## Success Criteria

After this work:
- [ ] Each glue component has a named pattern with examples
- [ ] Design decisions documented in ADR format
- [ ] #427 has clear specification to implement
- [ ] Alpha testers can have multi-turn conversations that feel natural

## Anti-Pattern Warning

**Do not**: Design glue patterns in isolation from the object model grammar.

Conversational glue should feel like Piper **experiencing** the conversation as a Moment, not processing a transaction queue. The grammar "Entities experience Moments in Places" applies here too.

## Placement

**Phase**: MUX-INTERACT (4.4)
**Sequence**: Should complete before #427 (MUX-IMPLEMENT-CONVERSE-MODEL) begins
**Dependencies**: MUX-V1 complete (✅), MUX-TECH in progress

## Labels

`mux`, `interaction-design`, `planning`, `mux-interact`

## Milestone

MUX-INTERACT

---

*Planning issue created per Chief Architect guidance, January 21, 2026*
*Gap identified in Lead Developer memo analysis*
