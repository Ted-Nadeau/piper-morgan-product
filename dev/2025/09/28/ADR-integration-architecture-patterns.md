# ADR-038: Integration Architecture Patterns and Selection Criteria

**Status**: Proposed
**Date**: September 28, 2025
**Decision Makers**: PM, Chief Architect

## Context

During CORE-QUERY-1 implementation, we discovered three different integration patterns across our services:
- Slack uses direct spatial intelligence (6-file system)
- Calendar and Notion use MCP (Model Context Protocol) adapters
- GitHub uses a deprecation router pattern

Additionally, we received expert feedback from Sam Zimmerman (Anthropic) recommending dependency graphs over 8-dimensional spatial models, and research showing production systems favor hierarchical/dependency-based orchestration over spatial approaches.

## Decision

We adopt a **decision tree approach** for selecting integration architecture patterns based on the specific characteristics and requirements of each integration.

## Integration Pattern Decision Tree

```
START: New Integration Needed
    ↓
1. Is the problem domain inherently spatial/dimensional?
   (e.g., physical locations, workspace relationships, time-based events)
    ├─ YES → Consider Spatial Pattern (go to 2)
    └─ NO → Use Standard Pattern (go to 3)

2. SPATIAL EVALUATION:
   Does the integration benefit from dimensional analysis?
    ├─ YES → Implement domain-specific spatial (like Slack)
    │        Use BaseSpatialAdapter with relevant dimensions
    │        Document which dimensions and why
    └─ NO → Reconsider - use Standard Pattern (go to 3)

3. STANDARD PATTERN SELECTION:
   Does the integration need model context management?
    ├─ YES → Use MCP Adapter Pattern
    │        (Calendar, Notion approach)
    └─ NO → Does it need version migration?
            ├─ YES → Use Deprecation Router Pattern
            │        (GitHub approach)
            └─ NO → Use Simple Service Pattern
                    (Direct implementation)

4. ALL PATTERNS:
   Wrap with Integration Router for QueryRouter access
```

## Pattern Descriptions

### 1. Domain-Specific Spatial Pattern
**When to use**: Problem naturally maps to dimensions (workspace hierarchy, geographic data, temporal relationships)
**Implementation**: Direct `BaseSpatialAdapter` inheritance with domain-relevant dimensions
**Example**: Slack's 6-file spatial system for workspace analysis
**Key principle**: Spatial dimensions must map to actual problem structure, not imposed arbitrarily

### 2. MCP Adapter Pattern
**When to use**: Integration needs AI model context management, tool descriptions, or LLM interaction protocols
**Implementation**: Create adapter implementing MCP protocol
**Example**: Calendar, Notion adapters
**Key principle**: Provides standardized AI model interaction

### 3. Deprecation Router Pattern
**When to use**: Migrating between implementation versions, A/B testing features, gradual rollout
**Implementation**: Router with feature flags controlling backend selection
**Example**: GitHub's spatial/legacy migration router
**Key principle**: Enables safe transitions without breaking changes

### 4. Simple Service Pattern
**When to use**: Straightforward API integration without special requirements
**Implementation**: Direct client implementation
**Example**: Basic REST API clients
**Key principle**: Don't over-engineer when simple suffices

## Orchestration Layer Principles

Above all integration patterns, orchestration follows these principles:

1. **Use dependency graphs** for task orchestration (per Sam Zimmerman's guidance)
2. **Information flow tracking** for debugging and observability
3. **Deterministic paths** where possible for reliability
4. **Router wrappers** provide uniform QueryRouter interface regardless of backend pattern

## Selection Criteria Checklist

When choosing a pattern, evaluate:

- [ ] **Natural Structure**: Does the problem have inherent dimensions/relationships?
- [ ] **Model Interaction**: Will AI models need to interact with this integration?
- [ ] **Evolution Path**: Will we need to migrate between implementations?
- [ ] **Complexity Justified**: Does added complexity provide measurable value?
- [ ] **Debugging Needs**: Can we trace operations through the pattern?
- [ ] **Performance**: Does the pattern meet latency/throughput requirements?

## Migration Strategy

For existing integrations:
1. **Keep working patterns** - Don't refactor functioning systems without clear benefit
2. **Wrap with routers** - Add router layer for uniform access
3. **Document rationale** - Explain why each integration uses its pattern
4. **Measure before changing** - Collect metrics before proposing pattern changes

## Anti-Patterns to Avoid

1. **Forced Uniformity**: Don't retrofit patterns for consistency alone
2. **Premature Spatial**: Don't add spatial dimensions without clear mapping to problem domain
3. **Over-Engineering**: Start simple, enhance based on measured need
4. **Pattern Mixing**: Don't combine patterns within single integration (choose one)

## Consequences

### Positive
- Clear decision framework for new integrations
- Preserves working patterns (Slack spatial, GitHub router)
- Allows pattern diversity where beneficial
- Provides migration path through router abstraction

### Negative
- Multiple patterns increase maintenance complexity
- Team must understand all patterns
- Documentation burden for pattern rationale

### Mitigations
- Router layer provides uniform interface regardless of backend
- This ADR documents selection criteria
- Pattern templates reduce implementation variance

## Validation Metrics

Track these to validate pattern choices:

| Integration | Pattern | Key Metric | Target | Actual |
|------------|---------|------------|---------|--------|
| Slack | Spatial | Query accuracy | >90% | TBD |
| GitHub | Router | Migration success | 100% | 100% |
| Calendar | MCP | Context preservation | >95% | TBD |
| Notion | MCP | API reliability | >99% | TBD |

## Future Considerations

1. **Plugin Architecture**: This decision tree extends naturally to plugin selection
2. **Performance Optimization**: May need caching/batching patterns later
3. **Multi-Region**: May need geographic distribution patterns
4. **Real-time**: May need event-driven patterns for live updates

## References

- Sam Zimmerman feedback on spatial models (September 2025)
- "Recent Developments in AI Spatial Intelligence" research (2024-2025)
- GREAT-2B GitHub router implementation (September 2025)
- Phase -1B discovery of integration patterns (September 28, 2025)

---

**Decision**: Integration architecture follows decision tree based on problem characteristics rather than forcing uniformity.
