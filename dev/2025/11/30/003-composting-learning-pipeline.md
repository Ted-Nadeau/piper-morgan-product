# Document Composting to Learning Pipeline

## Context
The Object Model includes an 8-stage lifecycle ending in "Composting" - where deprecated objects decompose into learnings that feed new emergent objects. This connects to the Learning System and Insight Journal, but the architectural connection isn't documented. We need to define how this actually works.

## Scope
**In Scope:**
- Define trigger mechanisms for composting
- Document decomposition process
- Map connection to Learning System
- Specify Insight Journal integration
- Create architectural diagrams

**Out of Scope:**
- Implementation code
- Database schema changes
- UI/UX design (covered by CXO)
- Performance optimization

## Acceptance Criteria
- [ ] Clear triggers defined (time-based? event-based? user-initiated?)
- [ ] Decomposition algorithm documented (what gets extracted?)
- [ ] Learning storage mechanism specified
- [ ] Feedback loop to Emergent stage mapped
- [ ] Insight Journal connection documented
- [ ] Architectural diagram created
- [ ] Integration points with existing systems identified

## Deliverables
Create `/mnt/user-data/outputs/composting-learning-architecture.md` containing:
1. Conceptual Overview (what composting means)
2. Technical Architecture (how it works)
3. Trigger Mechanisms (when it happens)
4. Decomposition Process (what gets extracted)
5. Learning Storage (where insights go)
6. Feedback Loops (how learnings create new Emergent)
7. Integration Points (Morning Standup example)

## Resources
- ADR-045 Object Model: `/mnt/user-data/outputs/ADR-045-object-model.md`
- Object Model Brief v2: `/mnt/project/object-model-brief-v2.md`
- Learning System docs (if they exist - find them)
- Insight Journal concept from UX sessions

## Verification
- Architecture is technically sound
- Connects cleanly to existing systems
- Morning Standup could use this pattern
- No hand-waving - concrete mechanisms
- Diagram clearly shows the flow

## Notes
This is connecting two powerful concepts:
1. The object lifecycle with composting
2. The learning system that makes Piper smarter

Think about this like a composter in a garden - organic matter breaks down into nutrients that feed new growth. What are the "nutrients" in Piper's context? Patterns? Preferences? Corrections?

The Morning Standup might already do some of this implicitly - look for examples there.

## Dependencies
Should review the models.py audit (prompt 001) first to understand current state.
