# Project Decision Log 001

**Start Date**: August 6, 2025
**Status**: Active
**Line Count Limit**: 6,000-7,000 lines

## Purpose

This log captures significant project decisions that affect scope, implementation approach, or resource allocation but don't require full Architecture Decision Records (ADRs).

## Decision Severity Guidelines

### ADR Required (Create separate ADR document)

- Technology/framework selection
- Major architectural patterns
- Security/privacy approaches
- Breaking changes
- Multi-sprint impact

### Decision Log Entry (Record here)

- Feature postponements
- Scope adjustments
- Sprint trade-offs
- Resource allocations
- Single sprint impact

### GitHub Comment Only (No log entry needed)

- Implementation details
- Minor adjustments
- Bug workarounds
- Test skips
- Session-level choices

## Entry Template

Each entry MUST follow this exact format:

```markdown
## [DECISION-XXX] Title of Decision

**Date**: YYYY-MM-DD HH:MM AM/PM PT
**Author**: [Name/Role]
**GitHub Issue**: #[number] (link)
**Severity**: Log-Level
**Status**: Active|Superseded|Implemented

### Context

[What situation required a decision?]

### Decision

[What was decided?]

### Rationale

- [Reason 1]
- [Reason 2]
- [Supporting evidence]

### Consequences

**Positive**:

- [Good outcome expected]

**Negative**:

- [Trade-off accepted]

**Risks**:

- [Potential issues to monitor]

### Review Date

[When should this be revisited? Use YYYY-MM-DD or "After X milestone"]

### Change Log

- YYYY-MM-DD: Initial decision documented - [Author]
- [Future updates listed here]

---
```

## Change Log

Document-level changes to track modifications:

- 2025-08-06: Initial creation - Chief Architect/PM

---

## Decision Entries Start Below This Line

============================================

## [DECISION-001] Knowledge Graph Visualization Postponement

**Date**: 2025-08-04 16:45 PM PT
**Author**: Product Manager
**GitHub Issue**: #79 (https://github.com/mediajunkie/piper-morgan-product/issues/79)
**Severity**: Log-Level
**Status**: Active

### Context

During PM-040 implementation, Cursor agent was struggling with D3.js visualization component implementation. The feature was marked as an acceptance criterion but proved complex relative to its immediate value.

### Decision

Postpone Knowledge Graph visualization feature to focus on core graph functionality.

### Rationale

- Visualization is nice-to-have, not core requirement for graph operations
- Cursor showing signs of complexity overload with D3.js integration
- Core graph operations (CRUD, traversal, pattern detection) more critical for immediate value
- Can add visualization in separate focused session with fresh agent context
- Time saved can be invested in more critical features

### Consequences

**Positive**:

- Faster delivery of core PM-040 functionality
- Reduced complexity in initial implementation
- Cleaner separation of concerns

**Negative**:

- No immediate visual representation of knowledge graph
- Acceptance criteria technically incomplete

**Risks**:

- Users may expect visualization based on issue description
- May need to update stakeholder expectations

### Review Date

After PM-040 production deployment

### Change Log

- 2025-08-06: Initial decision documented retroactively - Chief Architect

---

## [DECISION-002] PM-058 AsyncPG Connection Pool Fix - Approach Selection

**Date**: 2025-08-06 12:52 PM PT
**Author**: Code Agent (Claude Sonnet 4)
**GitHub Issue**: #38 (https://github.com/mediajunkie/piper-morgan-product/issues/38)
**Severity**: Log-Level
**Status**: Active

### Context

PM-058 AsyncPG connection pool concurrency issue blocking all testing. 4 test files fail in batch execution due to `cannot perform operation: another operation is in progress` error. Issue specifically affects `async_transaction` fixture in `conftest.py` causing contention when multiple async operations access same connection pool.

Affected files:

- `test_file_repository_migration.py` - 6/8 tests fail in batch
- `test_file_resolver_edge_cases.py` - 4/5 tests fail in batch
- `test_file_scoring_weights.py` - Status unknown
- `test_workflow_repository_migration.py` - Status unknown

### Decision

**Selected Option 1: Connection Pool Strategy Changes**

- Implement per-test connection isolation
- Increase pool size with proper async coordination
- Use connection-per-fixture approach with lifecycle management

### Rationale

- **Least Disruptive**: Works with existing AsyncSessionFactory patterns established in PM-015
- **Targeted Fix**: Addresses specific async_transaction fixture contention without major architectural changes
- **Maintains Architecture**: Preserves current database and testing patterns
- **Quick Implementation**: Can be completed within 2-hour Spring Cleaning sprint window
- **Evidence-Based**: Individual tests pass, only batch execution fails - indicating pool contention not logic errors

### Consequences

**Positive**:

- Preserves existing AsyncSessionFactory migration work from PM-015
- Maintains current testing patterns and infrastructure
- Targeted fix reduces risk of introducing new issues

**Negative**:

- May require increased connection pool resources
- Could have minor performance impact on test execution

**Risks**:

- Connection pool configuration may need environment-specific tuning
- Performance impact must stay within <2x slower acceptance criteria

### Review Date

After PM-058 completion and batch test verification

### Change Log

- 2025-08-06: Initial decision documented - Code Agent

---

## [DECISION-003] PM-080 Schema Fix Strategy - Add Missing Column vs Consolidation

**Date**: 2025-08-06 13:15 PM PT
**Author**: Cursor Agent (Claude Sonnet 4)
**GitHub Issue**: #81 (https://github.com/mediajunkie/piper-morgan-product/issues/81)
**Severity**: Log-Level
**Status**: Active

### Context

PM-080 schema inconsistency analysis revealed 3 specific issues with UploadedFile/UploadedFileDB:

1. Missing 'metadata' field in database model
2. Type mismatch on last_referenced (Optional[datetime] vs datetime annotation)
3. Type annotation inconsistency for file_metadata (Dict[str, Any] vs dict)

Two strategic approaches identified for the missing metadata field issue.

### Decision

**Selected: Option 1 - Add Missing Column**

- Add `metadata` column to `uploaded_files` table via migration
- Keep both `metadata` and `file_metadata` fields for semantic clarity
- Update type annotations to match existing schema
- Minimal disruption approach

### Rationale

- **Minimal Risk**: No breaking changes to existing data or code
- **Semantic Clarity**: Domain model clearly separates `metadata` (general) vs `file_metadata` (file-specific)
- **Migration Safety**: Simple column addition is low-risk database operation
- **Existing Pattern**: Current `to_domain()` already maps `file_metadata` to both fields, indicating intentional separation
- **Spring Cleaning Scope**: Fits 2-hour sprint window with minimal complexity

### Consequences

**Positive**:

- Zero breaking changes to existing functionality
- Clear semantic separation maintained between metadata types
- Simple migration with rollback capability
- Schema validator will pass with 0 errors

**Negative**:

- Slight storage overhead from duplicate metadata concept
- Two JSON columns instead of one consolidated field

**Risks**:

- Developers might confuse which metadata field to use
- Potential data synchronization issues between metadata fields

### Review Date

After PM-080 completion and schema validator success

### Change Log

- 2025-08-06: Initial decision documented - Cursor Agent

---

## [DECISION-004] PM-080 SQLAlchemy Metadata Conflict - Column Name Resolution

**Date**: 2025-08-06 13:35 PM PT
**Author**: Cursor Agent (Claude Sonnet 4)
**GitHub Issue**: #81 (https://github.com/mediajunkie/piper-morgan-product/issues/81)
**Severity**: Log-Level
**Status**: Active

### Context

During PM-080 implementation, discovered SQLAlchemy Declarative API reserves 'metadata' attribute name. When attempting to add `metadata = Column(JSON, default=dict)` to UploadedFileDB model, SQLAlchemy raised:

```
sqlalchemy.exc.InvalidRequestError: Attribute name 'metadata' is reserved when using the Declarative API.
```

This conflicts with DECISION-003 strategy to add missing metadata column directly.

### Decision

**Use `item_metadata` as column name instead of `metadata`**

- Database column: `item_metadata` (avoids SQLAlchemy conflict)
- Domain mapping: Map `item_metadata` column to domain `metadata` field
- Maintain semantic separation from `file_metadata`

### Rationale

- **Technical Constraint**: SQLAlchemy reserves 'metadata' attribute name
- **Minimal Impact**: Domain model unchanged, only database column name differs
- **Clear Semantics**: `item_metadata` distinguishes from `file_metadata`
- **Consistent Pattern**: Similar to existing `item_metadata` fields in other models
- **Migration Safety**: Column name change is low-risk operation

### Consequences

**Positive**:

- Resolves SQLAlchemy conflict immediately
- Maintains domain model structure unchanged
- Clear semantic distinction between metadata types
- Follows existing naming patterns in codebase

**Negative**:

- Column name doesn't exactly match domain field name
- Slight cognitive overhead mapping between names

**Risks**:

- Developers might confuse item_metadata vs metadata vs file_metadata
- Need to ensure mapping consistency in to_domain/from_domain methods

### Review Date

After PM-080 completion and schema validator success

### Change Log

- 2025-08-06: Initial decision documented - Cursor Agent

---

## [DECISION-005] SQLAlchemy Metadata Cache Synchronization Fix - Nuclear Option Implementation

**Date**: 2025-08-06 16:10 PM PT
**Author**: Code Agent (Claude Opus 4)
**GitHub Issue**: N/A (Infrastructure fix)
**Severity**: Log-Level
**Status**: Implemented

### Context

Tests were failing with `column "item_metadata" of relation "uploaded_files" does not exist` despite the column being properly defined in SQLAlchemy domain models. Chief Architect requested systematic 3-step approach to resolve apparent SQLAlchemy metadata cache synchronization issue.

Initial symptoms:
- SQLAlchemy model correctly defined `item_metadata` column in `UploadedFileDB`
- File repository migration tests failing on database operations
- Standard cache clearing approaches ineffective

### Decision

**Implement comprehensive database environment investigation with nuclear option cache clearing as fallback**

- Applied Chief Architect's 3-step systematic approach
- Built nuclear option SQLAlchemy metadata rebuild in `conftest.py`
- Discovered and resolved actual root cause: database environment mismatch

### Rationale

- **Systematic Investigation**: Chief Architect's 3-step approach (cache → instances → nuclear) provided methodical debugging
- **Nuclear Option Preservation**: Even though root cause was different, the nuclear option cache clearing has value for future SQLAlchemy issues
- **Evidence-Based Resolution**: Direct database investigation revealed true issue was schema mismatch, not cache
- **Environment Verification**: Database connection debugging uncovered local vs Docker PostgreSQL mismatch

### Consequences

**Positive**:

- All 9 file repository migration tests now pass (verified: 9/9 passing)
- Nuclear option methodology preserved for future SQLAlchemy cache issues
- Systematic debugging approach documented for reuse
- Database environment verification established as standard practice

**Negative**:

- Initial investigation time spent on cache issue rather than environment verification
- Required manual database schema fix outside of migration system

**Risks**:

- Multiple database environments may cause future confusion
- Local PostgreSQL schema drift from Docker container schema

### Review Date

After next migration deployment to verify schema synchronization practices

### Change Log

- 2025-08-06: Initial decision documented - Code Agent (Chief Architect DECISION-002 methodology)

---

## [DECISION-006] Foundation Repair Before Phase 3 - Database & Slack Architecture

**Date**: 2025-08-07 11:08 AM PT
**Author**: Lead Developer (Code Agent)
**GitHub Issue**: #85 (https://github.com/mediajunkie/piper-morgan-product/issues/85)
**Severity**: ADR-Level (requires ADR-007)
**Status**: Active

### Context

PM-034 Phase 3 integration work blocked by foundational architecture failures discovered through root cause analysis. System health at 50% (2/4 components working):

- ✅ Query Response Formatter: 100% accuracy, 0.002ms
- ✅ Type System: Clean domain models, zero coupling
- ❌ Database Connection: Session pattern inconsistency, transaction conflicts
- ❌ Slack Message Consolidation: Memory leaks, complex state management

Root cause analysis identified three critical architecture failures that must be resolved before Phase 3 parallel execution can succeed.

### Decision

**Mandatory foundation repair before any PM-034 Phase 3 work:**

1. **Database Session Unification** (ADR-007)
   - Standardize on AsyncSessionFactory across all services
   - Eliminate RepositoryFactory and db.get_session() competing patterns
   - Remove transaction boundary conflict logic from BaseRepository

2. **Slack Integration Simplification**
   - Replace MESSAGE_CONSOLIDATION_BUFFER global state with immediate response
   - Remove PROCESSED_EVENTS memory leak patterns
   - Implement circuit breaker at integration boundaries

3. **Integration Health Monitoring**
   - Centralized error aggregation for component health tracking
   - Graceful degradation strategies for failed components
   - Clear separation of concerns between integration layers

### Rationale

- **Phase 3 Dependency**: ConversationManager cannot be built on unreliable database layer
- **Integration Architecture**: Current 5-layer chain (SpatialEvent → SlackContext → Intent → Orchestration → Response) has silent failure modes
- **System Reliability**: 50% health indicates architectural issues, not implementation bugs
- **Evidence-Based**: Working components (Query Response Formatter, Type System) demonstrate excellence through simplicity
- **Trust Protocol**: No Phase 3 implementation without solid foundation verification

### Consequences

**Positive**:

- Database Connection component: 0% → 100% reliability target
- Eliminates session leaks and connection pool exhaustion
- Foundation stable for ConversationManager with Redis integration
- Clear migration path from complex to simple integration patterns
- Phase 3 parallel execution becomes feasible

**Negative**:

- PM-034 Phase 3 timeline delayed by foundation repair work
- Requires systematic migration of existing services
- Temporary disruption during session pattern unification

**Risks**:

- Service disruption during database session pattern migration
- Slack integration simplification might affect existing workflows
- Foundation repair scope might expand beyond initial estimates

### Review Date

After foundation repair completion and before PM-034 Phase 3 implementation

### Change Log

- 2025-08-07: Initial decision documented - Lead Developer (foundation repair mission)

---
