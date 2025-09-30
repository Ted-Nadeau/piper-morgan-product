# Spatial Intelligence Architecture Patterns

**Document Status**: Operational Guide
**Last Updated**: September 30, 2025
**Source**: CORE-GREAT-2C Verification (Phases 1-2)

## Overview

Piper Morgan implements **domain-optimized spatial intelligence patterns** to provide spatial coordination capabilities across different integration types. This document describes the two validated patterns and guidance for choosing between them.

Based on comprehensive verification work in CORE-GREAT-2C, we discovered that Piper Morgan successfully operates two fundamentally different spatial architecture patterns simultaneously, each optimized for its specific domain.

## Pattern 1: Granular Adapter Pattern

### Used By: Slack Integration

**Architecture:**
- **Files**: 11 total (6 core implementations + 5 test files)
- **Location**: `services/integrations/slack/spatial_*.py`
- **Access Pattern**: `Router → get_spatial_adapter() → SlackSpatialAdapter`
- **Inheritance**: Extends `BaseSpatialAdapter`

**Components**:
1. `spatial_types.py` - 14 classes (Territory, Room, Path types)
2. `spatial_adapter.py` - SlackSpatialAdapter with 9 async methods
3. `spatial_agent.py` - 6 classes for navigation and awareness
4. `spatial_intent_classifier.py` - 3 classes for intent classification
5. `spatial_mapper.py` - 30 functions for workspace/channel/message mapping
6. `spatial_memory.py` - 4 classes for spatial memory storage/retrieval

**Test Coverage**: 5 comprehensive test files with 66 test functions

**Characteristics:**
- Fine-grained component separation (types, adapter, agent, classifier, mapper, memory)
- Extensive test coverage validates each component independently
- Async/await patterns for I/O performance (15 async methods)
- Type-safe with enums and dataclasses
- Composition-based architecture (router has spatial adapter)
- Inherits from `BaseSpatialAdapter` for standardization

**When To Use:**
- Complex coordination scenarios with multiple interaction points
- Real-time messaging and event-driven architectures
- Multi-faceted spatial requirements that may evolve
- Need for extensive customization and extension
- Requirements likely to change or expand over time
- Multiple developers working on different spatial aspects

**Example Implementation:**
```python
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

# Router provides access to spatial capabilities
router = SlackIntegrationRouter()
spatial_adapter = router.get_spatial_adapter()

if spatial_adapter:
    # Access any of 9 spatial methods
    spatial_event = await spatial_adapter.create_spatial_event_from_slack(event_data)
    spatial_object = await spatial_adapter.create_spatial_object_from_slack(object_data)
    position = await spatial_adapter.map_to_position(context)
    context = await spatial_adapter.get_context(position)

    # Additional capabilities
    stats = await spatial_adapter.get_mapping_stats()
    await spatial_adapter.cleanup_old_mappings()
```

**Performance Profile:**
- Excellent for complex coordination
- Async/await optimizes I/O operations
- Component separation enables parallel testing
- Overhead justified by flexibility and maintainability

---

## Pattern 2: Embedded Intelligence Pattern

### Used By: Notion Integration

**Architecture:**
- **Files**: 1 comprehensive file (632 lines)
- **Location**: `services/intelligence/spatial/notion_spatial.py`
- **Access Pattern**: Separate `NotionSpatialIntelligence` class that uses router internally
- **Inheritance**: Standalone class (does not inherit BaseSpatialAdapter)

**Components**:
- `NotionSpatialIntelligence` - Single comprehensive class
- 8-dimensional spatial analysis (HIERARCHY, TEMPORAL, PRIORITY, COLLABORATIVE, FLOW, QUANTITATIVE, CAUSAL, CONTEXTUAL)
- 22 methods for spatial intelligence (8 analyzers + 14 support methods)
- Built-in analytics tracking
- Internal caching (workspace, database, page caches)

**Test Coverage**: 1 feature-level integration test file

**Characteristics:**
- Consolidated intelligence class design
- Intelligence layer abstraction (not integration layer)
- Analytical focus over reactive coordination
- Streamlined for knowledge management use cases
- Direct access to router capabilities
- Reversed composition (spatial intelligence has router)

**When To Use:**
- Knowledge management and semantic analysis scenarios
- Content processing and analytical workloads
- Streamlined spatial requirements with stable domain
- Well-defined, mature problem space
- Performance-critical applications requiring minimal overhead
- Single-purpose spatial intelligence needs

**Example Implementation:**
```python
from services.intelligence.spatial.notion_spatial import NotionSpatialIntelligence

# Create spatial intelligence instance
spatial = NotionSpatialIntelligence()

# Connect to workspace
await spatial.connect()

# Perform 8-dimensional analysis
analysis = await spatial.get_comprehensive_spatial_analysis(page_id)

# Access individual dimensions
hierarchy = await spatial.analyze_page_structure(page_id)      # HIERARCHY
temporal = await spatial.analyze_timestamps(page_id)            # TEMPORAL
priority = await spatial.analyze_tags_status(page_id)           # PRIORITY
collaborative = await spatial.analyze_authors(page_id)          # COLLABORATIVE
flow = await spatial.analyze_workflow_props(page_id)           # FLOW
quantitative = await spatial.analyze_metrics(page_id)          # QUANTITATIVE
causal = await spatial.analyze_relations(page_id)              # CAUSAL
contextual = await spatial.analyze_workspace(workspace_id)     # CONTEXTUAL

# Get analytics
analytics = spatial.get_spatial_analytics()
# Returns: workspaces_analyzed, databases_mapped, pages_processed, etc.

# Cleanup when done
await spatial.close()
```

**Performance Profile:**
- Excellent for analytical workloads
- Minimal overhead (single class)
- Direct method calls (no adapter indirection)
- Built-in caching optimizes repeated operations
- Lower memory footprint than granular pattern

---

## Pattern Comparison

| Aspect | Granular Adapter Pattern | Embedded Intelligence Pattern |
|--------|--------------------------|-------------------------------|
| **Complexity** | High (11 files, 6 components) | Low (1 file, 1 class) |
| **Lines of Code** | ~81 functions across 6 files | 632 lines, 22 methods |
| **Flexibility** | Very High (component-based) | Moderate (monolithic) |
| **Performance** | Good (async I/O optimized) | Excellent (direct access) |
| **Testability** | Excellent (66 test functions) | Good (integration tests) |
| **Maintenance** | Higher overhead (11 files) | Lower overhead (1 file) |
| **Use Case** | Coordination/Messaging | Knowledge/Semantic Analysis |
| **Location** | `services/integrations/` | `services/intelligence/` |
| **Base Class** | Inherits BaseSpatialAdapter | Standalone class |
| **Access** | `router.get_spatial_adapter()` | Separate class instantiation |
| **Composition** | Router has adapter | Intelligence has router |
| **Focus** | Reactive coordination | Analytical intelligence |

---

## 8-Dimensional Spatial Metaphor

Both patterns support the same **8-dimensional spatial analysis framework**:

1. **HIERARCHY** - Structural relationships (nested pages, parent-child)
2. **TEMPORAL** - Time-based patterns (creation, modification, sequences)
3. **PRIORITY** - Importance and urgency (tags, status, rankings)
4. **COLLABORATIVE** - Team dynamics (authors, editors, participants)
5. **FLOW** - State transitions (workflows, status changes)
6. **QUANTITATIVE** - Metrics and measurements (counts, durations, sizes)
7. **CAUSAL** - Dependencies and relationships (linked items, references)
8. **CONTEXTUAL** - Surrounding environment (workspace, domain, scope)

This consistent metaphor enables interoperability between different spatial systems while allowing implementation flexibility.

---

## Implementation Guidelines

### Feature Flag Integration

Both patterns support feature flag control for graceful enablement/disablement:

**Slack (Granular Pattern)**:
```python
from services.infrastructure.config.feature_flags import FeatureFlags

# Check if spatial should be used
if FeatureFlags.should_use_spatial_slack():
    # Use SlackSpatialAdapter
    spatial_adapter = router.get_spatial_adapter()
else:
    # Use legacy mode or basic functionality
    pass
```

**Notion (Embedded Pattern)**:
```python
from services.infrastructure.config.feature_flags import FeatureFlags

# Check if spatial should be used
if FeatureFlags.should_use_spatial_notion():
    # Use NotionSpatialIntelligence
    spatial = NotionSpatialIntelligence()
    await spatial.connect()
else:
    # Use basic Notion router without spatial intelligence
    pass
```

**Environment Variables**:
```bash
# Enable spatial systems (default: true)
export USE_SPATIAL_SLACK=true
export USE_SPATIAL_NOTION=true

# Disable for legacy mode
export USE_SPATIAL_SLACK=false
export USE_SPATIAL_NOTION=false
```

### Router Integration Requirements

All spatial patterns must:

1. **Integrate through Router Infrastructure**
   - Use IntegrationRouter base class or standalone with router access
   - Support feature flag control
   - Provide health check capabilities

2. **Support 8-Dimensional Spatial Metaphor**
   - Implement appropriate dimensions for domain
   - Use consistent dimension naming (HIERARCHY, TEMPORAL, etc.)
   - Document which dimensions are supported

3. **Maintain Backward Compatibility**
   - Gracefully degrade when spatial disabled
   - Don't break existing functionality
   - Support legacy mode via feature flags

4. **Follow Async Patterns**
   - Use async/await for I/O operations
   - Support concurrent operations where appropriate
   - Handle cleanup properly (context managers, destructors)

5. **Provide Observability**
   - Log spatial operations appropriately
   - Track analytics/metrics
   - Support debugging and troubleshooting

---

## Pattern Selection Guide

### Choose Granular Adapter Pattern When:

✅ Domain is complex with multiple interaction types
✅ Requirements are evolving or uncertain
✅ Need extensive customization and extension points
✅ Multiple developers working on spatial features
✅ Comprehensive test coverage is critical
✅ Real-time coordination is primary use case
✅ Component-based architecture preferred

**Examples**: Messaging platforms, real-time collaboration tools, event-driven systems

### Choose Embedded Intelligence Pattern When:

✅ Domain is well-defined and stable
✅ Analytical processing is primary use case
✅ Performance optimization is critical
✅ Single comprehensive class provides sufficient structure
✅ Lower maintenance overhead preferred
✅ Knowledge management is primary focus
✅ Monolithic design acceptable for domain

**Examples**: Knowledge bases, content management systems, semantic analysis tools

### Decision Framework

Ask these questions:

1. **Complexity**: How many distinct spatial capabilities are needed?
   - Many (>5) → Granular
   - Few (≤5) → Embedded

2. **Stability**: How likely are requirements to change?
   - Evolving → Granular
   - Stable → Embedded

3. **Performance**: Is minimal overhead critical?
   - Yes → Embedded
   - No → Either pattern

4. **Testing**: Need component-level test isolation?
   - Yes → Granular
   - No → Embedded

5. **Team Size**: Multiple developers on spatial features?
   - Yes → Granular
   - No → Embedded

6. **Domain Nature**: Reactive coordination or analytical intelligence?
   - Reactive → Granular
   - Analytical → Embedded

---

## Migration Between Patterns

If you need to migrate from one pattern to another:

### Embedded → Granular (Complexity Increasing)

1. Create separate component files (types, adapter, etc.)
2. Extract dimensions into specialized classes
3. Implement `BaseSpatialAdapter` interface
4. Add `get_spatial_adapter()` to router
5. Migrate tests to component-level
6. Update feature flag checks
7. Deprecate embedded implementation gradually

### Granular → Embedded (Simplification)

1. Consolidate components into single class
2. Merge related functionality
3. Remove adapter indirection layer
4. Update router to remove `get_spatial_adapter()`
5. Consolidate tests to integration level
6. Simplify feature flag checks
7. Archive granular components

**Note**: Migration is a significant undertaking. Choose the right pattern initially based on expected long-term needs.

---

## Future Pattern Development

When implementing spatial intelligence for new integrations:

### Step 1: Domain Analysis
- Understand the integration's primary use case
- Identify spatial dimensions relevant to domain
- Assess complexity and evolution likelihood
- Determine performance requirements

### Step 2: Pattern Selection
- Use decision framework above
- Consider team capabilities and resources
- Evaluate maintenance implications
- Choose appropriate pattern

### Step 3: Implementation
- Follow pattern guidelines strictly
- Implement feature flag control
- Support 8-dimensional metaphor (where applicable)
- Add comprehensive tests

### Step 4: Documentation
- Document pattern choice rationale
- Explain dimension implementations
- Provide usage examples
- Update this guide with lessons learned

---

## Validation Evidence

Both patterns are **production-proven and fully operational**:

**Slack (Granular)**:
- ✅ 11 files verified operational (GREAT-2C Phase 1)
- ✅ 66 test functions passing
- ✅ SlackSpatialAdapter with 9 methods working
- ✅ Feature flag control verified (USE_SPATIAL_SLACK)
- ✅ Router integration confirmed (get_spatial_adapter())

**Notion (Embedded)**:
- ✅ 1 file (632 lines) verified operational (GREAT-2C Phase 2)
- ✅ NotionSpatialIntelligence with 22 methods working
- ✅ 8 dimensional analyzers confirmed functional
- ✅ Feature flag control verified (USE_SPATIAL_NOTION)
- ✅ Router integration confirmed (internal usage)

Both patterns coexist successfully with **zero conflicts** and **100% compatibility**.

---

## Conclusion

Piper Morgan's dual spatial intelligence patterns represent a **mature architectural approach** that optimizes for different domains rather than forcing a one-size-fits-all solution.

**Key Insights**:
- Domain-specific optimization outweighs standardization for standardization's sake
- Both patterns support the same 8-dimensional spatial metaphor
- Feature flag control enables graceful degradation
- Production validation confirms both patterns are viable long-term

**Choose wisely**: The right pattern makes development easier, maintenance simpler, and performance better. The wrong pattern creates unnecessary complexity or insufficient flexibility.

---

**See Also**:
- [Router Patterns](router-patterns.md) - General router architecture
- [ADR-038: Spatial Intelligence Patterns](../internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md) - Architectural decision record
- [Webhook Security Design](webhook-security-design.md) - Security architecture

**Maintained by**: Piper Morgan Core Team
**Questions**: Create a GitHub issue with label `architecture`
