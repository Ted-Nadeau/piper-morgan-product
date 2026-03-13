# ADR Connection Map

**Investigation Phase**: P0 - Investigation & Pattern Discovery
**Parent Issue**: #612 (MUX-399-P0)
**Date**: 2026-01-19
**Investigator**: Claude Code (Lead Developer role)

---

## Executive Summary

Three ADRs form the architectural foundation for the object model:
- **ADR-038** (Accepted): Spatial patterns provide the 8D infrastructure that becomes lenses
- **ADR-045** (Accepted): The object model grammar defines Entities/Moments/Places
- **ADR-050** (Proposed): Conversation-as-graph provides journal/metadata structure

**Key finding**: ADR-045 was designed to integrate with the other two. The 8 perceptual lenses explicitly map to ADR-038's spatial dimensions. ADR-050's ConversationGraph is how Moments are structured and navigated.

**Gap for ADR-055**: Implementation specification needed—how to actually code the grammar.

---

## ADR Summaries

### ADR-038: Spatial Intelligence Architecture Patterns

**Location**: `docs/internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md`
**Status**: Accepted (September 30, 2025, updated October 1, 2025)

**Key Points**:

1. **Three spatial patterns** for different integration domains:
   - Granular Adapter Pattern (Slack) - Multiple files, component-based
   - Embedded Intelligence Pattern (Notion) - Single file, consolidated
   - Delegated MCP Pattern (Calendar) - Router + MCP adapter

2. **8-dimensional spatial metaphor** is REQUIRED across all patterns:
   - HIERARCHY, TEMPORAL, PRIORITY, COLLABORATIVE
   - FLOW, QUANTITATIVE, CAUSAL, CONTEXTUAL

3. **Pattern selection criteria** (6 factors):
   - Domain complexity, requirement stability, performance
   - Testing needs, team structure, domain nature

4. **All patterns** must support:
   - Router integration
   - Feature flag control (`USE_SPATIAL_*`)
   - Backward compatibility
   - Async patterns
   - Observability

**What's Already Decided**:
- The 8 dimensions ARE the standard
- Multiple implementation patterns are valid
- Each integration chooses appropriate pattern
- `self.dimensions` dict pattern is canonical

**Relation to Object Model**:
> "The 8 perceptual lenses map to the existing 8-dimensional spatial intelligence work." (ADR-045, line 60)

The spatial dimensions **ARE** the lenses. ADR-038 defined the technical infrastructure; ADR-045 reframes it as "perception."

---

### ADR-045: Object Model - "Entities Experience Moments in Places"

**Location**: `docs/internal/architecture/current/adrs/adr-045-object-model.md`
**Status**: Accepted (November 28, 2025)

**Key Points**:

1. **Core Grammar**: "Entities experience Moments in Places"
   - Substrates: Entities, Places, Moments
   - Situations: Container holding sequences of Moments (NOT a fourth substrate)

2. **Ownership Model** (Piper's relationship to objects):
   - Native: Creates, owns (Sessions, Memories, Concerns)
   - Federated: Observes, queries (GitHub Issues, Slack Messages)
   - Synthetic: Constructs through reasoning (Assembled Projects)

3. **Lifecycle Model** (8 stages):
   - Emergent → Derived → Noticed → Proposed → Ratified → Deprecated → Archived → Composted
   - Composting feeds new Emergent objects (circular)

4. **Perceptual Model** (8 lenses):
   - Maps 1:1 to ADR-038's spatial dimensions:

   | ADR-038 Dimension | ADR-045 Lens |
   |-------------------|--------------|
   | TEMPORAL | Temporal |
   | HIERARCHY | Hierarchy |
   | PRIORITY | Priority |
   | COLLABORATIVE | Collaborative |
   | CAUSAL | Causal |
   | CONTEXTUAL | Contextual |
   | FLOW | Flow |
   | QUANTITATIVE | Identity (implied) |

5. **Metadata Model** (6 dimensions):
   - Provenance, Relevance, Attention State
   - Confidence, Relations, Journal

6. **Anti-Flattening Tests** (5 criteria):
   - Is Piper an Entity with identity?
   - Are Moments bounded scenes, not timestamps?
   - Do Places have atmosphere, not just IDs?
   - Does lifecycle include transformation?
   - Can you see consciousness in the implementation?

**What's Already Decided**:
- The grammar is accepted
- Morning Standup is the reference implementation
- All features should express the grammar
- Consciousness preservation is required

**What Remains for ADR-055**:
- How to implement Entity/Moment/Place protocols
- How to wrap existing spatial methods as lenses
- How ownership model affects code organization
- How lifecycle states are tracked in database
- How metadata attaches to objects

---

### ADR-050: Conversation-as-Graph Model

**Location**: `docs/internal/architecture/current/adrs/adr-050-conversation-as-graph-model.md`
**Status**: Proposed (January 13, 2026)

**Key Points**:

1. **Graph-based conversation model** (not linear):
   - Nodes: Typed conversation elements (message, task, whisper, decision, question)
   - Links: Explicit relationships (reply, reference, blocking, annotates, resolves)

2. **View Projections** over same data:
   - Timeline (chronological)
   - Thread (grouped by parent_id)
   - Tasks (type = 'task')
   - Decisions (type = 'decision')
   - Questions (type = 'question')

3. **Facilitator Architecture**:
   - Orchestrator Facilitator → Domain Agents (GitHub, Calendar, Wiki)
   - Tuning: Verbosity, Stance, Alignment

4. **Explicit connection to ADR-045**:
   > "ADR-045 (Object Model): 'Entities experience Moments in Places' — a ConversationGraph is a **Place** where multiple **Entities** collaborate through typed **Moments** (Nodes)." (ADR-050, lines 170-171)

5. **Relationship to ADR-046** (Moment.type):
   > "Moment.types map to ConversationNodeTypes. The decomposition pipeline produces typed nodes that populate the graph." (ADR-050, line 169)

**What's Already Decided**:
- Conversations should be modeled as graphs
- Nodes have types (aligning with Moment.type from ADR-046)
- Links have types (extensible)
- Multiple views over same data

**Relation to Object Model**:
- ConversationGraph = Place
- ConversationNode = Moment
- Participants = Entities
- Links = Relations (metadata dimension)
- Journal = Interaction history over time

---

## Connection Map

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        ADR RELATIONSHIP MAP                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                        ┌───────────────────────┐                             │
│                        │      ADR-045          │                             │
│                        │    OBJECT MODEL       │                             │
│                        │   "Entities experience │                             │
│                        │    Moments in Places"  │                             │
│                        └───────────┬───────────┘                             │
│                                    │                                         │
│               ┌────────────────────┼────────────────────┐                    │
│               │                    │                    │                    │
│               ▼                    ▼                    ▼                    │
│     ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│     │    ADR-038      │  │   GRAMMAR       │  │    ADR-050      │           │
│     │    SPATIAL      │  │   CORE          │  │   CONVERSATION  │           │
│     │  INTELLIGENCE   │  │                 │  │    AS GRAPH     │           │
│     │                 │  │   Entity        │  │                 │           │
│     │ 8D Dimensions   │◄─│   Moment        │─►│ ConversationNode│           │
│     │ become Lenses   │  │   Place         │  │ as Moment       │           │
│     │                 │  │   Situation     │  │                 │           │
│     │ PERCEPTION      │  │                 │  │ ConversationGraph│          │
│     │ INFRASTRUCTURE  │  │   Ownership     │  │ as Place        │           │
│     │                 │  │   Lifecycle     │  │                 │           │
│     └────────┬────────┘  │   Metadata      │  │ JOURNAL         │           │
│              │           │                 │  │ INFRASTRUCTURE  │           │
│              │           └─────────────────┘  └────────┬────────┘           │
│              │                                         │                    │
│              │           ┌───────────────────┐         │                    │
│              └──────────►│     ADR-055       │◄────────┘                    │
│                          │  IMPLEMENTATION   │                              │
│                          │  SPECIFICATION    │                              │
│                          │                   │                              │
│                          │  How to code:     │                              │
│                          │  - Entity protocol│                              │
│                          │  - Lens wrappers  │                              │
│                          │  - Ownership impl │                              │
│                          │  - Lifecycle DB   │                              │
│                          │  - Metadata attach│                              │
│                          └───────────────────┘                              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Relationship Details

| From | To | Relationship | Evidence |
|------|-----|-------------|----------|
| ADR-038 | ADR-045 | 8D Dimensions = Perceptual Lenses | ADR-045 line 60: "These map to the existing 8-dimensional spatial intelligence work" |
| ADR-045 | ADR-050 | ConversationGraph = Place | ADR-050 line 171: "a ConversationGraph is a Place" |
| ADR-045 | ADR-050 | ConversationNode = Moment | ADR-050 line 171: "Entities collaborate through typed Moments (Nodes)" |
| ADR-046 | ADR-050 | Moment.type = ConversationNodeType | ADR-050 line 169: "Moment.types map to ConversationNodeTypes" |
| ADR-054 | ADR-050 | Memory persistence for graph | ADR-050 line 173: "cross-session memory handles persistence" |

---

## Gaps for ADR-055

### 1. Protocol Definitions

**What's missing**: Actual Python Protocol classes for Entity, Moment, Place

**What ADRs specify**:
- ADR-045: Conceptual definitions
- ADR-038: Implementation patterns (methods, not protocols)

**ADR-055 needs**:
```python
@runtime_checkable
class EntityProtocol(Protocol):
    """Any actor with identity and agency."""
    id: str
    ownership: OwnershipType  # Native/Federated/Synthetic
    lifecycle_state: LifecycleState
    ...
```

### 2. Lens Infrastructure

**What's missing**: Lens classes that wrap spatial dimension methods

**What ADRs specify**:
- ADR-038: `self.dimensions = {...}` pattern with 8 methods
- ADR-045: 8 perceptual lenses concept

**ADR-055 needs**:
```python
class TemporalLens:
    """Lens wrapping temporal dimension analysis."""
    def perceive(self, target: EntityProtocol, mode: PerceptionMode) -> Perception:
        # Call integration-specific dimension method
        ...
```

### 3. Ownership Model Implementation

**What's missing**: How ownership type affects code organization

**What ADRs specify**:
- ADR-045: Native/Federated/Synthetic categories

**ADR-055 needs**:
- Where Native objects are stored (internal database)
- How Federated objects are accessed (integration adapters)
- How Synthetic objects are constructed (reasoning service)

### 4. Lifecycle State Machine

**What's missing**: Database schema and state transitions

**What ADRs specify**:
- ADR-045: 8 stages with composting

**ADR-055 needs**:
- `lifecycle_state` column on domain objects
- State transition rules and validation
- Composting mechanism implementation

### 5. Metadata Attachment

**What's missing**: How 6 metadata dimensions attach to objects

**What ADRs specify**:
- ADR-045: Provenance, Relevance, Attention, Confidence, Relations, Journal
- ADR-050: Journal as interaction history in graph

**ADR-055 needs**:
- Metadata schema design
- Journal structure (link to ADR-050 ConversationLink)
- Relation graph infrastructure

### 6. Anti-Flattening Enforcement

**What's missing**: How to prevent grammar degradation

**What ADRs specify**:
- ADR-045: 5 anti-flattening tests

**ADR-055 needs**:
- Automated tests that verify grammar
- Code review checklist
- Pattern library updates

---

## Potential Conflicts

### Conflict 1: QUANTITATIVE vs Identity Lens

**Issue**: ADR-038 has QUANTITATIVE dimension, ADR-045 lists "Identity" as 8th lens

**Resolution**: They're different concerns
- QUANTITATIVE: Counts, metrics (numeric perception)
- Identity: What is this entity (type recognition)

**Recommendation**: Keep both—QUANTITATIVE becomes a lens, Identity is a separate concern (perhaps part of Entity protocol, not a lens)

### Conflict 2: Spatial as Methods vs Lenses as Classes

**Issue**: ADR-038 defines dimensions as methods in `self.dimensions` dict. ADR-045/mapping doc assumes wrappable classes.

**Resolution**: Adapter pattern (documented in spatial audit)
- Keep existing method-based implementation
- Lenses call methods based on target type
- No need to refactor existing spatial code

### Conflict 3: ADR-050 Status

**Issue**: ADR-050 is "Proposed" not "Accepted"

**Resolution**: P1 should proceed assuming ADR-050 direction is correct, but:
- Confirm with PM that graph model is accepted direction
- Keep journal implementation decoupled if needed
- Don't depend on ADR-050 features not yet implemented

---

## Recommendations for P1

### 1. Start with Protocol Definitions

Create `services/domain/protocols.py`:
- EntityProtocol
- MomentProtocol
- PlaceProtocol
- SituationProtocol

This is foundational—everything else depends on it.

### 2. Lens Infrastructure as Adapters

Don't rebuild spatial dimensions. Create:
- `services/perception/lenses/` directory
- One lens class per dimension
- Each lens calls integration-specific methods

### 3. Ownership as Marker, Not Location

Ownership (Native/Federated/Synthetic) should be:
- A field on Entity objects
- Not a directory structure
- Queryable for different treatment

### 4. Defer Full Lifecycle Until Needed

Start with:
- Emergent → Noticed → Ratified → Archived
- Add other states when features need them
- Composting is Phase 3+ concern

### 5. Journal = Conversation Links

Leverage ADR-050's link model:
- Journal entries are Links to ConversationNodes
- Relation graph uses same infrastructure
- This unifies metadata and conversation

---

## Evidence Summary

| Claim | ADR | Line Numbers |
|-------|-----|--------------|
| 8D dimensions are the standard | ADR-038 | 344-348 |
| Three spatial patterns valid | ADR-038 | 13-18 |
| Grammar is "Entities experience Moments in Places" | ADR-045 | 15 |
| Ownership: Native/Federated/Synthetic | ADR-045 | 27-33 |
| Lifecycle: 8 stages with composting | ADR-045 | 36-42 |
| 8 lenses map to 8D dimensions | ADR-045 | 60 |
| ConversationGraph is a Place | ADR-050 | 171 |
| ConversationNode is a Moment | ADR-050 | 171 |
| Moment.type = ConversationNodeType | ADR-050 | 169 |

---

*Analysis complete: 2026-01-19*
*P0 Deliverable 4 of 4*
