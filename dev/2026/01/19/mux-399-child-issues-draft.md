# MUX-VISION-OBJECT-MODEL (#399) Child Issues Draft

**Parent**: #399 MUX-VISION-OBJECT-MODEL
**Total Estimated Effort**: 35-38 hours (revised from 31-32 based on infrastructure findings)

---

## Issue Structure

```
#399 MUX-VISION-OBJECT-MODEL (Parent Epic)
├── #xxx Phase 0: Investigation & Pattern Discovery
├── #xxx Phase 1: Core Grammar & Lens Infrastructure
├── #xxx Phase 2: Ownership Model (Native/Federated/Synthetic)
├── #xxx Phase 3: Lifecycle State Machine with Composting
├── #xxx Phase 4: Metadata Schema & Journal Extensions
├── #xxx Phase 4.5: Canonical Query Tagging
└── #xxx Phase Z: Verification & Anti-Flattening Tests
```

---

## Child Issue 1: Phase 0 - Investigation & Pattern Discovery

**Title**: `MUX-399-P0: Investigation & Pattern Discovery`

**Description**:

### Overview

Investigation phase for MUX-VISION-OBJECT-MODEL. Must complete before any implementation begins.

**Cathedral Context**: Understanding the existing consciousness patterns before formalizing them.

### Deliverables

1. **Morning Standup Pattern Analysis**
   - Document how standup embodies "Entities experience Moments in Places"
   - Extract consciousness patterns that should be replicated
   - Identify what makes standup feel "present" vs mechanical

2. **Existing Spatial Infrastructure Audit**
   - Map current 8D dimension implementations across integrations
   - Document `NotionSpatialIntelligence.dimensions` pattern
   - Document Slack's `spatial_*.py` granular pattern
   - Identify common interfaces vs integration-specific implementations

3. **B1 FTUX Spec Review** (PPM addition)
   - Review `empty-state-voice-guide-v1.md`
   - Review `cross-session-greeting` specs
   - Review `contextual-hint-ux-spec-v1.md`
   - Document how these implicitly use Entity/Moment/Place thinking

4. **ADR Review**
   - ADR-038: Spatial Intelligence Patterns
   - ADR-045: Object Model (original)
   - ADR-050: Conversation-as-Graph
   - Document connections and gaps

### Acceptance Criteria

- [ ] Morning Standup analysis document (1-2 pages)
- [ ] Spatial infrastructure audit with file paths and patterns
- [ ] B1 FTUX implicit grammar mapping
- [ ] ADR connection map
- [ ] **Experience Checkpoint**: One paragraph explaining how this investigation honors "Entities experience Moments in Places"

### Estimated Effort

5 hours (was 4, +1 for B1 FTUX review)

### Dependencies

None - this is the starting point.

### Notes

- Do NOT touch code in this phase
- This is research and documentation only
- If findings significantly change the approach, escalate to PM before proceeding

---

## Child Issue 2: Phase 1 - Core Grammar & Lens Infrastructure

**Title**: `MUX-399-P1: Core Grammar Implementation & Lens Infrastructure`

**Description**:

### Overview

Implement the core grammar "Entities experience Moments in Places" with Protocol-based definitions and create the lens infrastructure.

**Cathedral Context**: Building the foundation that all future features will express.

### Deliverables

1. **Protocol Definitions**
   ```python
   EntityProtocol    # Actors with identity and agency
   MomentProtocol    # Bounded significant occurrences
   PlaceProtocol     # Contexts with atmosphere
   ```
   - Use `@runtime_checkable` Protocols (not inheritance)
   - Support grammatical role fluidity (Project can be Entity OR Place)

2. **Situation Context Manager**
   - Implement Situation as context manager (frame, not substrate)
   - Include dramatic tension capture
   - Support learning extraction on exit

3. **Lens Infrastructure** (NEW - based on investigation findings)
   - Create base `Lens` class with perception modes (noticing, remembering, anticipating)
   - Create 8 lens implementations wrapping/unifying existing dimension patterns
   - Create `LensSet` for compound perception
   - Define `Perception` result type with experience framing

4. **Visual Diagram**
   - Combine hand sketches with formal model
   - Show substrate relationships
   - Show lens application flow

5. **ADR-055 Draft**
   - "Object Model Implementation Specification"
   - Building on ADR-045
   - Include all technical decisions

### Acceptance Criteria

- [ ] Protocol definitions in `services/domain/` or new `services/mux/` module
- [ ] Situation context manager with tests
- [ ] Lens base class and 8 implementations with tests
- [ ] LensSet compound perception with tests
- [ ] Visual diagram (can be markdown/mermaid)
- [ ] ADR-055 draft complete
- [ ] **Experience Checkpoint**: One paragraph on how implementation honors the grammar

### Estimated Effort

10-12 hours (was 8, increased for lens infrastructure creation)

### Dependencies

- #xxx Phase 0 complete

### Technical Notes

- Location TBD: `services/mux/` (new) vs extending `services/domain/`
- Protocols go in `services/mux/protocols.py` or similar
- Lenses should unify existing patterns, not replace integration-specific implementations
- Morning Standup should be expressible using these constructs

---

## Child Issue 3: Phase 2 - Ownership Model

**Title**: `MUX-399-P2: Ownership Model (Native/Federated/Synthetic)`

**Description**:

### Overview

Implement the three-category ownership model that describes Piper's relationship to objects.

**Cathedral Context**: Distinguishing what Piper owns, observes, and constructs.

### Deliverables

1. **Ownership Categories**
   | Category | Metaphor | Examples |
   |----------|----------|----------|
   | Native | Piper's Mind | Sessions, memories, trust states |
   | Federated | Piper's Senses | GitHub issues, Slack messages, calendar events |
   | Synthetic | Piper's Understanding | Inferred project status, assembled risk picture |

2. **Ownership Protocol/Mixin**
   - `HasOwnership` protocol or mixin
   - Ownership determination rules
   - Transformation rules between categories

3. **Integration with Existing Models**
   - Map existing domain models to ownership categories
   - Document which entities fall into which category

### Acceptance Criteria

- [ ] Ownership enum/types defined
- [ ] `HasOwnership` protocol with category determination
- [ ] Transformation rules documented and implemented
- [ ] Existing domain models categorized
- [ ] Tests for ownership assignment and transformation
- [ ] **Experience Checkpoint**: One paragraph on ownership honoring the grammar

### Estimated Effort

4 hours

### Dependencies

- #xxx Phase 1 complete (Protocols defined)

---

## Child Issue 4: Phase 3 - Lifecycle State Machine

**Title**: `MUX-399-P3: Lifecycle State Machine with Composting`

**Description**:

### Overview

Implement the 8-stage lifecycle with composting feedback to the learning system.

**Cathedral Context**: "Nothing disappears, it transforms." Death feeds new life.

### Deliverables

1. **Lifecycle States**
   ```
   Emergent → Derived → Noticed → Proposed → Ratified → Deprecated → Archived → Composted
   ```

2. **State Machine**
   - Valid transition map
   - Transition validation
   - Transition history tracking

3. **Composting Feedback Loop**
   - Learning extraction on COMPOSTED transition
   - Integration with existing learning system
   - "The shadow side of PM work is ending things" - honor this

4. **HasLifecycle Protocol**
   - Mixin/protocol for objects with lifecycle
   - State property and history

### Acceptance Criteria

- [ ] `LifecycleState` enum with 8 states
- [ ] `LifecycleManager` with valid transitions
- [ ] Composting extracts learnings (integration with learning service)
- [ ] `HasLifecycle` protocol/mixin
- [ ] Transition history tracking
- [ ] Tests for all transitions including composting
- [ ] **Experience Checkpoint**: One paragraph on lifecycle honoring the grammar

### Estimated Effort

4 hours

### Dependencies

- #xxx Phase 1 complete (Protocols defined)
- Can potentially parallel with Phase 2

---

## Child Issue 5: Phase 4 - Metadata Schema & Journal Extensions

**Title**: `MUX-399-P4: Metadata Schema & Journal Extensions`

**Description**:

### Overview

Implement the 6 universal metadata dimensions and extend journal infrastructure.

**Cathedral Context**: What Piper knows about what it perceives.

### Deliverables

1. **Six Metadata Dimensions**
   - Provenance (source, confidence, timestamp)
   - Relevance (score, factors, decay)
   - Attention State (noticed by whom, when)
   - Confidence (score, basis, last validated)
   - Relations (typed links to other objects)
   - Journal (session + insight history)

2. **Two-Layer Journal**
   - Session Journal: Audit trail (extend existing session logs)
   - Insight Journal: What it meant (extend learning system)

3. **HasMetadata Protocol**
   - Universal metadata interface
   - Optional dimensions (not all objects need all metadata)

### Acceptance Criteria

- [ ] Metadata dimension types defined
- [ ] `HasMetadata` protocol
- [ ] Session journal extension (or documentation of existing)
- [ ] Insight journal extension (or documentation of existing)
- [ ] Tests for metadata assignment and retrieval
- [ ] **Experience Checkpoint**: One paragraph on metadata honoring the grammar

### Estimated Effort

4 hours

### Dependencies

- #xxx Phase 1 complete
- Can potentially parallel with Phases 2 and 3

---

## Child Issue 6: Phase 4.5 - Canonical Query Tagging

**Title**: `MUX-399-P4.5: Canonical Query Lens/Substrate Tagging`

**Description**:

### Overview

Map existing canonical queries to lenses and substrates, validating the grammar's expressiveness.

**Cathedral Context**: If we can't express what we already do, we've over-complicated.

### Deliverables

1. **Canonical Query Mapping Table**
   | Query | Primary Lens | Secondary Lens(es) | Substrate | Example |
   |-------|-------------|-------------------|-----------|---------|
   | "What's on my agenda today?" | Temporal | Contextual | Moment (Calendar Place) | Standup |
   | "Show me stale PRs" | Flow | Temporal, Priority | Moment (GitHub Place) | Backlog |
   | "What needs attention?" | Priority | Collaborative, Temporal | Situation | Triage |

2. **Coverage Analysis**
   - How many of 50+ canonical queries are expressible?
   - Which queries require concepts not in the grammar?
   - Refinement recommendations if gaps found

3. **ADR-055 Appendix**
   - Full mapping table
   - Analysis notes

### Acceptance Criteria

- [ ] Mapping table for 50+ canonical queries
- [ ] Coverage percentage documented
- [ ] Any grammar gaps identified with recommendations
- [ ] ADR-055 appendix updated
- [ ] **Experience Checkpoint**: One paragraph on how tagging validates the grammar

### Estimated Effort

3 hours

### Dependencies

- #xxx Phase 1 complete (Lenses defined)
- Should come after lenses exist to validate against

### Notes

This is a PPM-requested addition. It's validation, not implementation.
80% coverage (40/50 queries expressible) is the Tier 2 success threshold.

---

## Child Issue 7: Phase Z - Verification & Anti-Flattening Tests

**Title**: `MUX-399-PZ: Verification & Anti-Flattening Tests`

**Description**:

### Overview

Final verification that the implementation preserves consciousness and doesn't flatten to mere database schema.

**Cathedral Context**: Ensuring we built a cathedral, not a shed.

### Deliverables

1. **Anti-Flattening Test Suite**

   **Technical Tests**:
   - [ ] Piper is Entity with identity, not just function
   - [ ] Moments are bounded scenes, not timestamps
   - [ ] Places have atmosphere and purpose, not just IDs
   - [ ] Situations contain dramatic tension, not just state
   - [ ] Lifecycle includes composting (transformation), not just deletion

   **Design Tests** (from CXO):
   - [ ] Response framing: "I notice..." not "Found 3 results"
   - [ ] Empty states: "Nothing here yet..." not "No data"
   - [ ] Error handling: "I couldn't reach..." not "Operation failed"
   - [ ] History display: Moments by significance, not timestamp list
   - [ ] Entity references: Names and relationships, not IDs and labels

2. **Experience Tests**
   Can we describe Piper's behavior using:
   - "Piper noticed that..."
   - "Piper remembers when..."
   - "Piper anticipates..."

   Rather than:
   - "The system returned..."
   - "The query matched..."

3. **Implementation Guide**
   - How future features should use the grammar
   - Common patterns and anti-patterns
   - Morning Standup as reference implementation

4. **ADR-055 Finalization**
   - Status: Accepted
   - All sections complete
   - Ready for move to `docs/internal/architecture/current/adrs/`

### Acceptance Criteria

- [ ] Anti-flattening test suite passes (all checkboxes)
- [ ] Experience tests documented with examples
- [ ] Implementation guide for future developers
- [ ] ADR-055 finalized and ready for merge
- [ ] PM/CXO sign-off on consciousness preservation
- [ ] **Final Experience Checkpoint**: Summary of how the full implementation honors "Entities experience Moments in Places"

### Estimated Effort

4 hours

### Dependencies

- All previous phases complete

### Success Metrics (from PPM)

**Tier 1 (Required)**:
- Anti-flattening tests pass
- ADR-055 merged
- Lifecycle state machine implemented

**Tier 2 (80% threshold)**:
- 8/10 diverse canonical queries expressible using grammar
- Can describe NEW hypothetical feature using grammar without inventing concepts
- ADR answers "why" questions, not just "what"

**Tier 3 (Judgment)**:
- PM/CXO gut check: Does this feel like progress toward the vision?

---

## Summary

| Issue | Title | Hours | Dependencies |
|-------|-------|-------|--------------|
| P0 | Investigation & Pattern Discovery | 5 | None |
| P1 | Core Grammar & Lens Infrastructure | 10-12 | P0 |
| P2 | Ownership Model | 4 | P1 |
| P3 | Lifecycle State Machine | 4 | P1 |
| P4 | Metadata Schema & Journals | 4 | P1 |
| P4.5 | Canonical Query Tagging | 3 | P1 |
| PZ | Verification & Anti-Flattening | 4 | All |

**Total: 34-38 hours**

### Parallelization Opportunities

After P0 and P1 complete:
- P2, P3, P4 can potentially run in parallel (independent concepts)
- P4.5 needs P1 complete (validates lenses)
- PZ must be last

### TDD Approach

Each phase should follow:
1. Write tests first based on acceptance criteria
2. Implement to pass tests
3. Verify experience checkpoint
4. Independent agent can verify claims

---

*Draft created: January 19, 2026*
*For review before GitHub issue creation*
