# ADR-038: Spatial Intelligence Architecture Patterns

**Date**: September 30, 2025
**Status**: Accepted
**Context**: CORE-GREAT-2C Verification Work (GitHub Issue #194)
**Supersedes**: None
**Superseded by**: None

---

## Decision

Piper Morgan will support **two distinct spatial intelligence patterns** optimized for different integration domains:

1. **Granular Adapter Pattern** for complex coordination scenarios
2. **Embedded Intelligence Pattern** for streamlined knowledge management

Both patterns are considered first-class architectural approaches, and new integrations should choose the pattern most appropriate for their domain.

---

## Context

During CORE-GREAT-2C verification work (Phases 1-2, September 30, 2025), we discovered that Slack and Notion integrations implement fundamentally different but equally valid spatial architecture approaches.

### Slack Implementation (Granular Adapter Pattern)
- **Structure**: 11 files (6 core + 5 tests)
- **Location**: `services/integrations/slack/spatial_*.py`
- **Access**: `router.get_spatial_adapter() → SlackSpatialAdapter`
- **Inheritance**: Extends `BaseSpatialAdapter`
- **Components**: Types, Adapter, Agent, Classifier, Mapper, Memory
- **Use Case**: Real-time messaging coordination

### Notion Implementation (Embedded Intelligence Pattern)
- **Structure**: 1 comprehensive file (632 lines)
- **Location**: `services/intelligence/spatial/notion_spatial.py`
- **Access**: Separate `NotionSpatialIntelligence` class using router internally
- **Inheritance**: Standalone class (no base adapter)
- **Components**: Single comprehensive intelligence class
- **Use Case**: Knowledge management and semantic analysis

### Verification Results
- ✅ Slack spatial: 11 files, 100% operational, 66 test functions passing
- ✅ Notion spatial: 1 file, 100% operational, 8-dimensional analysis working
- ✅ Both patterns: Support 8-dimensional spatial metaphor
- ✅ Zero conflicts: Patterns coexist successfully
- ✅ Feature flags: Both support USE_SPATIAL_* control
- ✅ Production-proven: Both operational in production codebase

---

## Options Considered

### Option 1: Standardize on Single Pattern (REJECTED)
Force all integrations to use the same architectural approach.

**Advantages**:
- Single pattern to learn and maintain
- Consistent codebase structure
- Easier onboarding for new developers

**Disadvantages**:
- Wrong tool for some domains (over-engineering or under-engineering)
- Performance penalties for mismatched patterns
- Maintenance burden (either too complex or too inflexible)
- Discards validated, working implementations
- **Rejected**: Both patterns are production-proven and domain-optimized

### Option 2: Support Multiple Patterns (CHOSEN)
Allow domain-optimized architectures based on integration characteristics.

**Advantages**:
- Optimal performance for each domain
- Appropriate complexity levels
- Proven operational in production
- Clear selection criteria
- Flexibility for future integrations

**Disadvantages**:
- Multiple patterns to maintain
- Documentation overhead
- Training requirement for developers

**Decision**: CHOSEN - Benefits outweigh costs

### Option 3: Hybrid Approach (REJECTED)
Combine both patterns in single implementation (e.g., granular components with embedded access).

**Advantages**:
- Theoretically "best of both worlds"
- Single architectural style

**Disadvantages**:
- Complexity without clear benefit
- Unclear which pattern to follow
- No production validation
- Maintenance burden of both approaches
- **Rejected**: Adds complexity without solving real problems

---

## Decision Rationale

### Core Principle: Domain-Optimized Architecture

**Key Insight**: Domain-specific optimization outweighs standardization for standardization's sake.

Different integration domains have fundamentally different spatial requirements:

**Reactive Coordination (Slack)**:
- Real-time event processing
- Multiple interaction types (messages, threads, reactions, etc.)
- Complex state management across channels/workspaces
- Need for fine-grained component testing
- **Solution**: Granular Adapter Pattern (11 files, component-based)

**Analytical Intelligence (Notion)**:
- Batch processing of knowledge structures
- Single comprehensive analytical model
- Stable domain with clear requirements
- Performance-critical operations
- **Solution**: Embedded Intelligence Pattern (1 file, consolidated)

### Evidence-Based Decision

**Production Validation**:
- Both patterns verified operational (GREAT-2C Phases 1-2)
- Zero conflicts between patterns
- 100% feature parity (8-dimensional spatial metaphor)
- Complete test coverage (66 tests Slack, integration tests Notion)

**Architectural Quality**:
- Slack: Clean component separation, extensive test coverage
- Notion: Consolidated design, lower overhead, direct access
- Both: Feature flag control, async/await patterns, observability

**Developer Experience**:
- Clear selection criteria documented
- Pattern choice based on objective factors
- Both patterns have proven track record

---

## Implementation

### Pattern Selection Criteria

New spatial integrations must choose pattern based on:

1. **Domain Complexity**:
   - Many distinct capabilities (>5) → Granular
   - Few focused capabilities (≤5) → Embedded

2. **Requirement Stability**:
   - Evolving requirements → Granular (easier to extend)
   - Stable requirements → Embedded (lower overhead)

3. **Performance Criticality**:
   - Performance critical → Embedded (minimal overhead)
   - Performance adequate → Either pattern

4. **Testing Requirements**:
   - Component-level isolation needed → Granular
   - Integration-level testing sufficient → Embedded

5. **Team Structure**:
   - Multiple developers on feature → Granular (parallel work)
   - Single developer or small team → Embedded (simpler)

6. **Domain Nature**:
   - Reactive coordination → Granular
   - Analytical intelligence → Embedded

### Pattern Descriptions

#### Granular Adapter Pattern

**When to Use**:
- Complex coordination scenarios
- Real-time messaging and events
- Multi-faceted spatial requirements
- Requirements likely to evolve
- Multiple developers working on spatial features

**Structure**:
```
services/integrations/{integration}/
  spatial_types.py          # Domain types and primitives
  spatial_adapter.py        # Main adapter (inherits BaseSpatialAdapter)
  spatial_agent.py          # Navigation and awareness
  spatial_intent_classifier.py  # Intent classification
  spatial_mapper.py         # Domain-specific mapping
  spatial_memory.py         # Memory storage/retrieval
  tests/
    test_spatial_*.py       # Component-level tests
```

**Access Pattern**:
```python
router = IntegrationRouter()
adapter = router.get_spatial_adapter()
result = await adapter.map_to_position(context)
```

#### Embedded Intelligence Pattern

**When to Use**:
- Knowledge management scenarios
- Semantic analysis and content processing
- Streamlined spatial requirements
- Stable, well-defined domain
- Performance-critical applications
- Single comprehensive model fits domain

**Structure**:
```
services/intelligence/spatial/{integration}_spatial.py
  # Single comprehensive class
  # 8-dimensional analysis methods
  # Built-in analytics tracking
  # Internal router usage
```

**Access Pattern**:
```python
spatial = IntegrationSpatialIntelligence()
await spatial.connect()
analysis = await spatial.get_comprehensive_spatial_analysis(item_id)
```

### Common Requirements

All spatial patterns **must**:

1. **Router Integration**:
   - Use IntegrationRouter (directly or indirectly)
   - Support feature flag control (USE_SPATIAL_*)
   - Provide health check capabilities

2. **8-Dimensional Spatial Metaphor**:
   - Implement relevant dimensions for domain
   - Use consistent naming (HIERARCHY, TEMPORAL, PRIORITY, COLLABORATIVE, FLOW, QUANTITATIVE, CAUSAL, CONTEXTUAL)
   - Document which dimensions supported

3. **Backward Compatibility**:
   - Graceful degradation when spatial disabled
   - Don't break existing functionality
   - Support legacy mode via feature flags

4. **Async Patterns**:
   - Use async/await for I/O operations
   - Support concurrent operations where appropriate
   - Handle cleanup properly

5. **Observability**:
   - Log spatial operations appropriately
   - Track analytics/metrics
   - Support debugging and troubleshooting

---

## Consequences

### Positive Consequences

1. **Optimal Performance**: Each integration uses pattern suited to its needs
2. **Appropriate Complexity**: No over-engineering or under-engineering
3. **Production-Proven**: Both patterns validated and operational
4. **Clear Guidance**: Selection criteria documented
5. **Flexibility**: Future integrations can choose appropriate pattern
6. **No Breaking Changes**: Both existing patterns continue working

### Negative Consequences

1. **Multiple Patterns**: Two patterns to maintain instead of one
2. **Documentation Overhead**: Must document both patterns
3. **Training**: Developers need to understand pattern selection
4. **Consistency Risk**: Must ensure both patterns follow core requirements

### Mitigation Strategies

**For Multiple Patterns**:
- Clear documentation of both patterns
- Decision framework for pattern selection
- Common requirements enforced across patterns

**For Documentation Overhead**:
- Comprehensive pattern guide created (`docs/architecture/spatial-intelligence-patterns.md`)
- Pattern comparison table
- Usage examples for both patterns

**For Training**:
- Selection criteria clearly documented
- Decision framework provides objective guidance
- Examples from production code (Slack, Notion)

**For Consistency**:
- Common requirements documented (router integration, 8-dimensional metaphor, etc.)
- Feature flag system consistent across patterns
- Observability standards apply to both

---

## Compliance Requirements

### For Existing Implementations

**Slack (Granular Adapter Pattern)**:
- ✅ Compliant: Follows all pattern requirements
- ✅ Production operational
- ✅ Feature flag control working
- ✅ 8-dimensional metaphor supported
- ✅ Comprehensive test coverage

**Notion (Embedded Intelligence Pattern)**:
- ✅ Compliant: Follows all pattern requirements
- ✅ Production operational
- ✅ Feature flag control working
- ✅ 8-dimensional analysis implemented
- ✅ Integration test coverage

### For New Implementations

New spatial integrations must:

1. **Choose Pattern**: Use decision framework to select appropriate pattern
2. **Document Choice**: Create brief rationale document explaining pattern choice
3. **Follow Requirements**: Implement all common requirements
4. **Feature Flags**: Support USE_SPATIAL_{INTEGRATION}=true/false
5. **Router Integration**: Integrate with IntegrationRouter infrastructure
6. **Dimensions**: Implement relevant 8-dimensional analysis
7. **Testing**: Provide appropriate test coverage (component or integration)
8. **Documentation**: Update spatial pattern guide with integration

### Review Process

Pattern selection should be reviewed during:
- Initial design phase
- Architecture review
- Code review (ensure pattern followed correctly)

---

## References

### Documentation
- [Spatial Intelligence Patterns Guide](../../../../architecture/spatial-intelligence-patterns.md) - Comprehensive pattern documentation
- [Operational Guide](../../../../operations/operational-guide.md) - Feature flag usage and troubleshooting

### Source Code
- Granular Pattern: `services/integrations/slack/spatial_*.py` (11 files)
- Embedded Pattern: `services/intelligence/spatial/notion_spatial.py` (1 file)
- Base Adapter: `services/integrations/spatial_adapter.py`

### Verification
- GitHub Issue #194: CORE-GREAT-2C verification work
- Session Log: `dev/2025/09/30/2025-09-30-1025-prog-code-log.md`
- Phase 1: Slack spatial investigation (11 files analyzed)
- Phase 2: Notion spatial investigation (consolidated architecture discovered)

---

## Version History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2025-09-30 | 1.0 | Claude Code | Initial ADR creation based on GREAT-2C verification |

---

## Approval

**Approved by**: CORE-GREAT-2C Verification Work (Phases 1-4)
**Implementation Status**: Complete and Operational
**Production Status**: Both patterns deployed and validated

---

**Next Review**: After next spatial integration implementation
**Related ADRs**: None (first spatial architecture ADR)
**Supersedes**: None
**Superseded by**: None (active)

---

*This ADR documents the discovery and validation of two production spatial patterns during GREAT-2C verification work (September 30, 2025).*
