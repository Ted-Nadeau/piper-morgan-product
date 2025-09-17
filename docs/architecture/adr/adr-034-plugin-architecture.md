# ADR-034: Plugin Architecture Implementation

## Status
Accepted

## Context
The June 3, 2025 architectural decision established plugin architecture from day one, but it was only partially implemented. Currently, GitHub integration is hardcoded rather than pluggable. With spatial intelligence patterns already in our MCP integrations and the need for Notion, Slack, and future PM tool integrations, implementing the plugin architecture is critical for extensibility.

## Decision
We will implement a plugin architecture where all external integrations (GitHub, Notion, Slack, Jira, etc.) are pluggable components implementing a common interface. The architecture will be domain-driven, with PM concepts defining the interface rather than tool-specific features.

### Plugin Architecture Principles
1. **Domain-first**: PM concepts (WorkItem, TeamMember) drive the interface
2. **Tool-agnostic**: No tool-specific logic in core
3. **Event-driven**: Every plugin interaction emits learnable events
4. **Capability-based**: Plugins declare their capabilities
5. **Spatial-aware**: Leverage MCP spatial intelligence patterns

### Core Components
```
Core System
    ↓
Plugin Interface (PiperPlugin)
    ↓
Plugin Registry
    ↓
Individual Plugins (GitHub, Notion, Slack, etc.)
```

## Consequences

### Positive
- **Vendor independence**: Not locked to any PM tool ecosystem
- **Infinite extensibility**: New tools added without core changes
- **Learning amplification**: Every plugin feeds the learning system
- **Cross-tool intelligence**: Spatial queries across all plugins
- **Market differentiation**: Works with any PM stack

### Negative
- **Abstraction complexity**: Mapping diverse tools to common model
- **Feature parity challenges**: Lowest common denominator risk
- **Testing burden**: Each plugin needs comprehensive tests
- **Initial overhead**: Extracting GitHub to plugin takes effort
- **API stability requirement**: Plugin interface becomes critical contract

### Neutral
- **Configuration complexity**: Plugin selection and configuration
- **Documentation needs**: Plugin development guide required
- **Version management**: Plugin compatibility tracking

## Implementation

### Phase 1: Extract GitHub (Week 1)
```python
# Current: services/integrations/github/
# Target: plugins/github/
class GitHubPlugin(PiperPlugin):
    """GitHub as first plugin implementation"""
```

### Phase 2: Plugin Infrastructure (Week 2)
- Plugin registry implementation
- Discovery mechanism
- Configuration system
- Lifecycle management

### Phase 3: Second Plugin (Week 3)
- Implement Notion plugin (high user value)
- Validate interface completeness
- Refine based on learnings

### Phase 4: Spatial Integration (Week 4)
- Connect to MCP spatial patterns
- Enable cross-plugin queries
- Implement unified search

## Migration Strategy
1. Create plugin interface (Pattern-030)
2. Wrap existing GitHub integration
3. Test extensively with no functional changes
4. Move GitHub code to plugin structure
5. Add second plugin to validate architecture

## Success Metrics
- Plugin development time (target: <1 week per plugin)
- Cross-plugin query success rate
- Learning events generated per plugin
- User satisfaction with multi-tool support

## References
- Original vision: June 3, 2025 (Clean slate, plugin from day one)
- Pattern-030: Plugin Interface
- MCP spatial patterns: services/mcp/
- Related issues: Multiple integration requests across tracks
