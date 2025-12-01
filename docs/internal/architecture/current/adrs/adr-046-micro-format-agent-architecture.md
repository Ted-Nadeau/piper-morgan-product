# ADR-046: Micro-Format Agent Architecture

**Status**: Proposed
**Date**: November 30, 2025
**Author**: Chief Architect, with architectural design by Ted Nadeau

## Context

Through using the advisor mailbox system, Ted Nadeau identified a powerful architectural pattern for agent coordination. His insight: text input should be decomposed into typed "micro-formats" that are routed to specialized agent handlers. This emerged from practical experience with async collaboration needs.

Our current architecture uses the grammar "Entities experience Moments in Places" but lacks granularity in Moment types and processing specialization. The coordination queue works but treats all prompts uniformly. We need more sophisticated routing and handling.

Ted's observation: "There should be many small agents (helps with context, security, division of labor, scaling)."

## Decision

Adopt a micro-format processing pipeline architecture where:

1. **Input text is decomposed** into typed micro-formats
2. **Each micro-format type** has a specialized listener agent
3. **Processing cascades** through a defined pipeline
4. **Service agents** handle final integration with external systems

### Micro-Format Types (Initial Set)

1. **Capability/Feature/Use Case** - What system can do
2. **Initiative/Epic/Story/Task** - Work hierarchy
3. **Rule/Requirement/Guideline/Heuristic/Algorithm** - Constraints and patterns
4. **Assertion/Statement** - Claims requiring validation
5. **Question** - Queries needing answers
6. **Issue/Change Request/Trouble Report** - Problems to resolve
7. **Permission/Security** - Access control needs
8. **Data Model/Schema** - Structure definitions
9. **Events/Workflow** - Process definitions
10. **Functions/Objects** - Code structures

(Anticipate ~2x more types through discovery)

### Relationship Model

Micro-formats relate through typed connections:
- `blocks` - Prevents progress
- `enables` - Allows capability
- `depends-on` - Requires completion
- `related-to` - Loose association
- `validates` - Confirms assertion
- `invalidates` - Contradicts claim

### Processing Architecture

```
Input Layer: Text Analysis
    ↓
Extraction Layer: Micro-format identification
    ↓
Routing Layer: Type-specific distribution
    ↓
Processing Layer: Specialized handlers (ON EVENT new-X DO)
    ↓
Service Layer: External system integration
```

### Evolution Path

1. **Phase 1**: File-based (current coordination queue)
2. **Phase 2**: Repository-backed with relationships
3. **Phase 3**: Message-based with routing
4. **Phase 4**: Workflow orchestration

## Consequences

### Positive

- **Specialization**: Each agent focuses on one concern
- **Scalability**: Add new micro-format types without disrupting existing ones
- **Security**: Agents have minimal context/permissions
- **Traceability**: Clear path from input to action
- **Composability**: Micro-formats combine into larger structures
- **Evolution**: Natural path from files to workflows

### Negative

- **Complexity**: More moving parts than monolithic processing
- **Coordination**: Inter-agent communication overhead
- **Discovery**: Need to identify micro-format types through use
- **Training**: Each agent type needs specific capabilities

### Neutral

- Changes our Moment model from generic to typed
- Requires routing layer infrastructure
- Shifts from single agent to multi-agent coordination
- Creates dependency on micro-format extraction accuracy

## Implementation Strategy

### Pilot Approach (December 2025)

1. Test 3-4 micro-format types in coordination queue
2. Measure extraction accuracy and routing effectiveness
3. Implement specialized handlers for pilot types
4. Gather metrics on processing improvement

### Full Implementation (Q1 2026)

1. Build extraction layer with LLM-based classification
2. Implement routing infrastructure
3. Create specialized agent templates
4. Connect to service layer (GitHub, Slack, etc.)

## Relationship to Existing Architecture

### Maps to Object Model
- Micro-formats are specialized **Moment** subtypes
- Listener agents are specialized **Entity** processors
- Service layer represents **Places** where actions manifest
- Relationships create **Situation** containers

### Extends Coordination Queue
- Queue evolves from generic to typed prompts
- Routing becomes intelligent rather than claimed
- Specialization improves processing quality

## Validation

Ted's architecture emerged from actual use of our systems, not theoretical design. This bottom-up discovery validates the pattern through experience.

## References

- Ted's advisor mailbox response (November 30, 2025)
- ADR-045: Object Model (Entities, Moments, Places)
- Coordination Queue pilot results
- MUX-TECH implementation phases

## Decision Outcome

**Accepted** - Will pilot with 3-4 micro-format types in December 2025, then expand based on results.

## Notes

This architecture represents a convergence between our build methodology (how we coordinate agents) and Piper's architecture (how Piper processes information). The recursive elegance is that we'll use micro-format processing to build the micro-format processor.

Ted's insight about "write-flow vs read-and-work-update flow" suggests different pipelines for different operations - creation versus modification patterns.

---

*Attribution: Core architectural design by Ted Nadeau, formalized by Chief Architect*
