# Piper Morgan Pattern Index
*Last Updated: August 11, 2025*
*Total Patterns: 25+*

## Architectural Patterns

### Repository Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/repositories/`, `services/database/repositories.py`
- **Description**: Encapsulate data access logic with clean interface between domain models and database implementation
- **Usage Example**: BaseRepository, ProjectRepository, WorkflowRepository
- **Related ADR**: ADR-005 (repository pattern consistency)

### Service Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/*/service.py`
- **Description**: Business logic encapsulation in dedicated service classes
- **Usage Example**: IntentService, WorkflowService, AuthService
- **Related ADR**: None (core architectural principle)

### Factory Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/orchestration/workflow_factory.py`
- **Description**: Stateless object creation for concurrency safety
- **Usage Example**: WorkflowFactory.create_from_intent()
- **Related ADR**: None (core architectural principle)

### CQRS-lite Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/queries/`, `services/orchestration/`
- **Description**: Separation of read operations (queries) from write operations (commands)
- **Usage Example**: QueryRouter for reads, WorkflowEngine for writes
- **Related ADR**: None (core architectural principle)

### Universal Composition Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/domain/models.py`, `services/database/models.py`
- **Description**: Single universal class with discriminator field instead of specialized classes
- **Usage Example**: List(item_type='todo') vs separate TodoList class
- **Related ADR**: Universal List Architecture Guide

### Backward Compatibility Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/domain/models.py`
- **Description**: Compatibility layer that delegates to new architecture
- **Usage Example**: TodoList alias that delegates to universal List
- **Related ADR**: Universal List Architecture Guide

### Performance Optimization Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/database/`
- **Description**: Strategic indexing and caching for new patterns
- **Usage Example**: Indexes on item_type for universal List queries
- **Related ADR**: Universal List Architecture Guide

### Integration Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/integrations/`
- **Description**: Clear integration points and validation
- **Usage Example**: Slack integration, GitHub integration
- **Related ADR**: ADR-008 (MCP connection pooling)

## Implementation Patterns

### AsyncSession Constructor Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/database/`
- **Description**: AsyncSession constructor for automatic resource lifecycle management
- **Usage Example**: Database session management in repositories
- **Related ADR**: ADR-005 (repository pattern consistency)

### Context Manager Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/database/repositories.py`
- **Description**: Context manager approach for automatic resource lifecycle
- **Usage Example**: `async with self.session.begin():` for transactions
- **Related ADR**: ADR-008 (MCP connection pooling)

### Feature Flag Safety Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/infrastructure/feature_flags/`
- **Description**: Always test both old and new code paths during integration
- **Usage Example**: Feature flag testing in integration tests
- **Related ADR**: ADR-010 (configuration management)

### Transaction Management Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/database/repositories.py`
- **Description**: Consistent transaction handling with automatic commit/rollback
- **Usage Example**: Repository create/update operations
- **Related ADR**: ADR-005 (repository pattern consistency)

### Error Handling Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/`
- **Description**: Graceful degradation with specific error types
- **Usage Example**: Domain exceptions, HTTP status codes
- **Related ADR**: Error handling framework

### Configuration Management Pattern
- **Status**: ✅ **Proven**
- **Location**: `services/infrastructure/config/`
- **Description**: Hybrid configuration access with clean abstractions
- **Usage Example**: ConfigService for application/domain layers
- **Related ADR**: ADR-010 (configuration management)

## Testing Patterns

### Test-First Development Pattern
- **Status**: ✅ **Proven**
- **Location**: `tests/`, methodology documentation
- **Description**: Write tests before implementation to drive design
- **Usage Example**: All new features start with failing tests
- **Related ADR**: TDD Requirements methodology

### Integration Testing Pattern
- **Status**: ✅ **Proven**
- **Location**: `tests/integration/`
- **Description**: Component interactions with real dependencies
- **Usage Example**: End-to-end workflow testing
- **Related ADR**: Test Strategy document

### Unit Testing Pattern
- **Status**: ✅ **Proven**
- **Location**: `tests/unit/`
- **Description**: Isolated component testing with mocked dependencies
- **Usage Example**: Service method testing
- **Related ADR**: Test Strategy document

### End-to-End Testing Pattern
- **Status**: ✅ **Proven**
- **Location**: `tests/`
- **Description**: Full workflow testing with real services
- **Usage Example**: Complete user scenario testing
- **Related ADR**: Test Strategy document

### Test Reliability Pattern
- **Status**: ✅ **Proven**
- **Location**: `tests/`
- **Description**: Deterministic test execution with proper isolation
- **Usage Example**: Test database cleanup, mock external services
- **Related ADR**: Test Strategy document

## Decision Patterns

### Verification-First Pattern
- **Status**: ✅ **Proven** (Critical Strength: 15/16)
- **Location**: `docs/piper-education/decision-patterns/emergent/verification-first-pattern.md`
- **Description**: Ensure reliability by systematically verifying AI-generated solutions
- **Usage Example**: PM-055, PM-012, PM-021 implementations
- **Related ADR**: Excellence Flywheel methodology

### Incremental Refactoring Pattern
- **Status**: ✅ **Proven**
- **Location**: `docs/development/universal-list-architecture-guide.md`
- **Description**: Systematic transformation without compromising quality
- **Usage Example**: Universal List architecture refactoring
- **Related ADR**: Universal List Architecture Guide

### Risk-Based Decision Pattern
- **Status**: ✅ **Proven**
- **Location**: `docs/development/methodology-04-ARCHITECTURAL-AGILITY.md`
- **Description**: Evaluate technical, performance, maintenance, and integration risks
- **Usage Example**: Architectural decision framework
- **Related ADR**: Architectural Agility methodology

### Context-Driven Decision Pattern
- **Status**: ✅ **Proven**
- **Location**: `docs/piper-education/decision-patterns/`
- **Description**: Decisions based on specific context and requirements
- **Usage Example**: Multi-project configuration management
- **Related ADR**: Context management framework

### AI-Assisted Decision Pattern
- **Status**: ✅ **Proven**
- **Location**: `docs/development/human-ai-architectural-collaboration.md`
- **Description**: Human strategic vision + AI systematic execution
- **Usage Example**: Multi-agent coordination for complex projects
- **Related ADR**: Human-AI collaboration framework

## Quality Assurance Patterns

### Excellence Flywheel Methodology
- **Status**: ✅ **Proven**
- **Location**: `docs/development/methodology-core/`
- **Description**: Systematic approach to development quality and velocity
- **Usage Example**: All development work follows this methodology
- **Related ADR**: Core methodology documents

### Systematic Verification Pattern
- **Status**: ✅ **Proven**
- **Location**: `CLAUDE.md`, methodology documentation
- **Description**: Verify requirements and existing state before implementation
- **Usage Example**: Pattern discovery before implementation
- **Related ADR**: Excellence Flywheel methodology

### Quality Gate Enforcement Pattern
- **Status**: ✅ **Proven**
- **Location**: `tests/`, CI/CD pipeline
- **Description**: Automated validation prevents testing regressions
- **Usage Example**: Test coverage requirements, build validation
- **Related ADR**: Test Strategy document

### Regression Prevention Pattern
- **Status**: ✅ **Proven**
- **Location**: `tests/`, automation tools
- **Description**: Prevent over-mocking and testing regressions
- **Usage Example**: Reality testing, health monitoring
- **Related ADR**: Test Strategy document

## Process Patterns

### Multi-Agent Coordination Pattern
- **Status**: ✅ **Proven**
- **Location**: `docs/development/methodology-core/methodology-02-AGENT-COORDINATION.md`
- **Description**: Strategic deployment of multiple AI agents for parallel work
- **Usage Example**: Claude Code + Cursor Agent coordination
- **Related ADR**: Agent coordination methodology

### Handoff Protocol Pattern
- **Status**: ✅ **Proven**
- **Location**: `docs/development/prompts/`
- **Description**: Systematic context transfer between agent sessions
- **Usage Example**: Session handoff documentation and verification
- **Related ADR**: Session management framework

### Session Management Pattern
- **Status**: ✅ **Proven**
- **Location**: `docs/development/session-logs/`
- **Description**: Structured session logging and progress tracking
- **Usage Example**: Daily session logs with mission tracking
- **Related ADR**: Session logging framework

### Documentation Pattern
- **Status**: ✅ **Proven**
- **Location**: `docs/`
- **Description**: Comprehensive documentation with cross-references
- **Usage Example**: ADRs, implementation guides, session logs
- **Related ADR**: Documentation standards

## Discovered Patterns (Not Yet Documented)

### MCP Integration Patterns
- **Pattern**: MCP connection pooling and circuit breaker patterns
- **Found in**: `docs/architecture/adr-008-mcp-connection-pooling-production.md`
- **Needs documentation**: Detailed MCP integration pattern guide

### Slack Integration Patterns
- **Pattern**: Slack spatial metaphors and integration architecture
- **Found in**: `services/integrations/slack/`
- **Needs documentation**: Slack integration pattern catalog

### Workflow Orchestration Patterns
- **Pattern**: Complex workflow coordination and state management
- **Found in**: `services/orchestration/`
- **Needs documentation**: Workflow orchestration pattern guide

### Knowledge Graph Patterns
- **Pattern**: Semantic knowledge representation and querying
- **Found in**: `services/knowledge_graph/`
- **Needs documentation**: Knowledge graph pattern catalog

---

## Pattern Usage Guidelines

### Before Implementing New Features
1. **Check Pattern Index**: Look for existing patterns that apply
2. **Verify Implementation**: Use established patterns rather than creating new ones
3. **Follow Conventions**: Maintain consistency with existing pattern usage
4. **Document Deviations**: Explain why new patterns are needed

### Pattern Evolution
1. **Proven Patterns**: Use as-is, maintain consistency
2. **Experimental Patterns**: Test thoroughly, document learnings
3. **Deprecated Patterns**: Avoid in new code, plan migration
4. **New Patterns**: Document thoroughly, validate with team

### Quality Standards
1. **Architectural Consistency**: All patterns must align with domain models
2. **Test Coverage**: All patterns must have comprehensive test coverage
3. **Documentation**: All patterns must be documented with examples
4. **Performance**: All patterns must meet performance requirements

---

*Pattern Index maintained by Cursor Agent - Last updated August 11, 2025*
*Total patterns documented: 25+ architectural and implementation patterns*
*Strategic value: Comprehensive pattern understanding for MCP Monday development*
