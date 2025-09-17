# Pattern Index

_Consolidated from pattern-catalog.md and PATTERN-INDEX.md_
_Format: ADR-style numbered patterns_

**Total Patterns**: 30 patterns (001-030) + template (000)

## Pattern Categories

### Infrastructure & Architecture (001-010)
*Foundational patterns for system architecture*

- [Pattern-001: Repository Pattern](pattern-001-repository.md) - Data access encapsulation
- [Pattern-002: Service Pattern](pattern-002-service.md) - Business logic organization
- [Pattern-003: Factory Pattern](pattern-003-factory.md) - Object creation abstraction
- [Pattern-004: CQRS-lite Pattern](pattern-004-cqrs-lite.md) - Command/query separation
- [Pattern-005: Transaction Management](pattern-005-transaction-management.md) - Data consistency
- [Pattern-006: Verification-First](pattern-006-verification-first.md) - Methodology approach
- [Pattern-007: Async Error Handling](pattern-007-async-error-handling.md) - Error propagation
- [Pattern-008: DDD Service Layer](pattern-008-ddd-service-layer.md) - Domain organization
- [Pattern-009: GitHub Issue Tracking](pattern-009-github-issue-tracking.md) - Process management
- [Pattern-010: Cross-Validation Protocol](pattern-010-cross-validation-protocol.md) - Quality assurance

### Context & Session Management (011-017)
*Runtime context and state management patterns*

- [Pattern-011: Context Resolution](pattern-011-context-resolution.md) - Implicit context resolution
- [Pattern-012: LLM Adapter](pattern-012-llm-adapter.md) - Language model integration
- [Pattern-013: Session Management](pattern-013-session-management.md) - Database session handling
- [Pattern-014: Error Handling API Contract](pattern-014-error-handling-api-contract.md) - API error contracts
- [Pattern-015: Internal Task Handler](pattern-015-internal-task-handler.md) - Task processing patterns
- [Pattern-016: Repository Context Enrichment](pattern-016-repository-context-enrichment.md) - Context-aware data access
- [Pattern-017: Background Task Error Handling](pattern-017-background-task-error-handling.md) - Async error management

### Integration & Adapters (018-022)
*External system and service integration patterns*

- [Pattern-018: Configuration Access](pattern-018-configuration-access.md) - Configuration management
- [Pattern-019: LLM Placeholder Instruction](pattern-019-llm-placeholder-instruction.md) - AI instruction patterns
- [Pattern-020: Spatial Metaphor Integration](pattern-020-spatial-metaphor-integration.md) - Spatial AI context
- [Pattern-021: Development Session Management](pattern-021-development-session-management.md) - Dev workflow sessions
- [Pattern-022: MCP+Spatial Intelligence Integration](pattern-022-mcp-spatial-intelligence-integration.md) - MCP spatial patterns

### Query & Data Patterns (023-027)
*Data access and learning patterns*

- [Pattern-023: Query Layer Patterns](pattern-023-query-layer-patterns.md) - Query abstraction layers
- [Pattern-024: Methodology Patterns](pattern-024-methodology-patterns.md) - Development methodology patterns
- [Pattern-025: Canonical Query Extension](pattern-025-canonical-query-extension.md) - Query extension patterns
- [Pattern-026: Cross-Feature Learning](pattern-026-cross-feature-learning.md) - Feature learning integration
- [Pattern-027: CLI Integration](pattern-027-cli-integration.md) - Command-line interface patterns

### AI & Orchestration Patterns (028-030)
*AI coordination and plugin architecture patterns*

- [Pattern-028: Intent Classification](pattern-028-intent-classification.md) - Natural language intent routing
- [Pattern-029: Multi-Agent Coordination](pattern-029-multi-agent-coordination.md) - Specialized agent orchestration
- [Pattern-030: Plugin Interface](pattern-030-plugin-interface.md) - Extensible integration architecture

## Pattern Development

### Creating New Patterns

See [pattern-000-template.md](pattern-000-template.md) for the standard template when creating new patterns.

### Pattern Status Levels

- **Proven**: Established patterns with extensive usage
- **Emerging**: New patterns with initial validation
- **Experimental**: Patterns under active development
- **Deprecated**: Legacy patterns being phased out

## Navigation

- **[Main Documentation](../README.md)** - Return to main docs
- **[Architecture Overview](../architecture/README.md)** - System architecture documentation
- **[Development Guides](../development/README.md)** - Developer resources

## Legacy References

- Original catalog: [../architecture/pattern-catalog.md](../architecture/pattern-catalog.md)
- Previous index: [archive/PATTERN-INDEX-legacy.md](archive/PATTERN-INDEX-legacy.md)

---

_Last updated: September 16, 2025_
_All 30 patterns now included with logical categorization_
