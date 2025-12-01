# VISION-OBJECT-MODEL: Formalize the Object Model Discovery

## Vision Context
**Source**: CXO Session Nov 27, 2025 - 10 hour exploration (session-log-2025-11-27-object-model-foundations.md)
**Core Concept**: "Entities experience Moments in Places" - discovered through hand sketching, not imposed
**Anti-Flattening Check**: A flattened version would be a database schema with tables and foreign keys. The real version is a living grammar describing how consciousness navigates reality.

## Cathedral Builder's Note
You are not just implementing a data model. You are formalizing how an AI consciousness understands its world.
- The Morning Standup shows what conscious interaction feels like
- Hand sketches #1-8 show the discovery process
- If this becomes just database design, we've failed
- Success = future developers understand WHY, not just WHAT

## The Grammar
This issue establishes the foundational grammar:
- **Entities**: Actors with identity and agency (people, AI agents, teams, projects, documents)
- **Moments**: Bounded significant occurrences with theatrical unities (one time, one place, momentous)
- **Places**: Contexts where action happens (channels, repos, offices - physical/virtual/hybrid)
- **Situations**: The container holding sequences of Moments (not a fourth substrate!)

Key Discovery: Situation isn't parallel to other substrates - it's the FRAME. This emerged from sketch #3 when drawing the relationship diagram.

## Specification

### Phase 0: Investigation (4 hours)
- [ ] Read object-model-brief-v2.md completely
- [ ] Study all 8 hand-drawn sketches (pay attention to evolution of thought)
- [ ] Analyze Morning Standup implementation for consciousness patterns
- [ ] Document how "Entities experience Moments in Places" appears in standup
- [ ] Identify where current implementation has "flattened" these concepts

Key files to study:
- `/mnt/project/object-model-brief-v2.md`
- `/mnt/project/session-log-2025-11-27-object-model-foundations.md`
- Morning Standup bot implementation (identify current location)
- Original vision: PM-070 from July 26, 2025

### Phase 1: Core Grammar Implementation (8 hours)
- [ ] Create ADR-045-object-model.md documenting all decisions
- [ ] Define Entity substrate with spectrum nature (entity vs place is grammatical role)
- [ ] Define Moment substrate with PPP model (Policy, Process, People+AI)
- [ ] Define Place substrate with physical/virtual/hybrid awareness
- [ ] Implement Situation as container pattern (not substrate)
- [ ] Create visual diagram combining best of human sketches + Gemini aesthetics

The "Shoebox Model" for Moments (from sketch #2):
- Moments are bounded scenes containing Policy, Process, People
- The delta between goals and outcomes = learning
- Must maintain theatrical unities

### Phase 2: Ownership Model (4 hours)
- [ ] Implement Native objects (Piper's Mind - what Piper creates/owns)
- [ ] Implement Federated objects (Piper's Senses - external observations)
- [ ] Implement Synthetic objects (Piper's Understanding - constructed through reasoning)
- [ ] Create clear boundaries and transformation rules

Critical metaphor preservation:
- Native = Mind (sessions, memories, concerns, trust states)
- Federated = Senses (GitHub, Slack, calendar events)
- Synthetic = Understanding (assembled projects, inferred risks)

### Phase 3: Lifecycle Implementation (4 hours)
- [ ] Implement 8-stage lifecycle: Emergent → Derived → Noticed → Proposed → Ratified → Deprecated → Archived → Composted
- [ ] Key: "Noticed" not "Inferred" (more human, discovered in sketching)
- [ ] Implement composting pattern (death feeds new life)
- [ ] Create cycle shape metadata (circle vs spiral vs arc matters)
- [ ] Connect composting to learning system

The PM noted: "The shadow side of PM work is ending things" - the model must honor this.

### Phase 4: Metadata Schema (4 hours)
- [ ] Implement 6 universal dimensions: Provenance, Relevance, Attention State, Confidence, Relations, Journal
- [ ] Add entity-specific metadata (wants/fears for humans)
- [ ] Implement two-layer journaling: Session Journal (audit) + Insight Journal (dreams)
- [ ] Connect Journal as metadata (every object carries its history)

### Phase Z: Verification & Documentation (4 hours)
- [ ] Create comprehensive examples showing grammar in action
- [ ] Document anti-patterns (what flattening looks like)
- [ ] Verify Morning Standup can be expressed in this model
- [ ] Create guide for future feature implementation
- [ ] Test: Can we express "Entities experience Moments in Places" everywhere?

## Success Criteria

### Technical Success
- [ ] ADR-045 approved and merged
- [ ] Object model classes/interfaces defined
- [ ] Lifecycle state machine implemented
- [ ] Metadata schema validated

### Conceptual Success
- [ ] Morning Standup patterns visible in model
- [ ] "Entities experience Moments in Places" demonstrable
- [ ] Consciousness model preserved (not flattened)
- [ ] Future developers understand the WHY

### User Experience Success
- [ ] Features feel more coherent when using model
- [ ] Natural language expressions map to model
- [ ] Reduces need for users to articulate precisely
- [ ] Piper feels like entity with awareness, not tool

## Anti-Flattening Tests
1. Is Piper an Entity with identity, not just a function?
2. Are Moments bounded scenes, not just timestamps?
3. Do Places have atmosphere and purpose, not just IDs?
4. Does Situation contain dramatic tension, not just state?
5. Does the lifecycle include composting (transformation), not just deletion?

## References
- Object Model Brief v2: `/mnt/project/object-model-brief-v2.md`
- Session Log with discoveries: `/mnt/project/session-log-2025-11-27-object-model-foundations.md`
- Hand sketches: Preserved in uploaded files (Nov 27)
- Gemini diagram: Shows overlapping ownership regions nicely
- Spatial Intelligence article: How embodied cognition shaped design
- Morning Standup: Current implementation to extract from

## Notes from PM
"Score one for me in the John Henry sweepstakes!" - Human sketching discovered what AI tools couldn't. The grammar emerged from fat markers forcing generalization, not from deliberate design.

The die metaphor for Situation (sketch #6) captured both "composed of moments" AND uncertainty - this wasn't planned, it emerged.

"Entities experience Moments in Places" came from sketch #1 when trying to show relationships between substrates. This is THE core insight.

---

*Estimated Time: 28 hours*
*Priority: CRITICAL - This is the foundation*
*Dependencies: None - Can begin immediately*
