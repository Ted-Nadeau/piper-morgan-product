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
## [DECISION-005] PM-034 Foundation Repair Before Phase 3
**Date**: 2025-08-07 10:44 AM PT
**Author**: Lead Developer/Chief Architect
**GitHub Issue**: # PM-034.1
**Severity**: Log-Level
**Status**: Active

### Context
PM-034 Phase 2 validation revealed 50% system functionality due to architectural conflicts.

### Decision
Repair foundation issues before proceeding to Phase 3 ConversationManager. Note this decision is thoroughly documented in  ADR-012.

### Rationale
- Database session conflicts will compound with new features
- Global state in Slack integration creates race conditions
- Building Phase 3 on broken foundation multiplies technical debt

### Review Date
After foundation repair completion.
