# SCHEMA-SINGULAR-TABLES - Adopt Singular Table Naming Convention

**Priority**: P3 (Design convention, Post-MVP)
**Labels**: `enhancement`, `documentation`, `database`, `style`, `priority: low`
**Milestone**: Post-MVP
**Epic**: Architecture & Design
**Related**: Ted Nadeau recommendation (database design best practices), Issue #335 (prefixed PK naming)

---

## Problem Statement

### Current State
Current tables use predominantly plural names (26 of 27 tables). This causes confusion and edge cases:

**Plural edge cases** (English is inconsistent):
```
category → categories  ❌ (not categorys)
person → people        ❌ (not persons)
index → indices        ❌ (not indexes)
child → children       ❌ (not childs)
```

**ORM mapping confusion**:
```python
# Model is singular, table is plural (mismatch)
class User(Base):
    __tablename__ = "users"  # Singular model, plural table (confusing)

# vs clearer:
class User(Base):
    __tablename__ = "user"  # Matches model name
```

**Foreign key readability**:
```sql
-- Current (plural):
lists.owner_id → users.id     # "lists owner_id"? Grammatically awkward

-- Singular (clearer):
list.owner_id → user.user_id  # "list owner_id" (singular-to-singular)
```

### Current Implementation
**26 of 27 tables use plural naming** (verified from database schema):

**Plural tables**:
- `users`, `lists`, `list_items`, `list_memberships`
- `intents`, `workflows`, `tasks`, `features`, `products`
- `stakeholders`, `work_items`, `projects`, `project_integrations`
- `todo_items`, `todo_lists`, `uploaded_files`, `user_api_keys`
- `audit_logs`, `learned_patterns`, `learning_settings`
- `knowledge_nodes`, `knowledge_edges`
- `personality_profiles`, `feedback`, `items`

**Singular tables** (framework-controlled, not our choice):
- `alembic_version` (Alembic migration framework)

### Impact
- **Code clarity**: Plural suffixes add noise and confusion
- **Edge cases**: Developers must remember plural rules (categories not categorys)
- **ORM confusion**: Model names don't match table names
- **FK readability**: Awkward grammar in foreign key relationships
- **Onboarding**: New developers confused by plural naming convention

### Ted Nadeau's Recommendation
> "Suggest table names be singular 'user' not plural 'users' (annoying plural suffixes 'ies' in english) (even though table is collection of elements & therefore 'plural' (a 'murder' of users))"

**Preference**: Singular table names recommended for simplicity and clarity

---

## Goal

**Primary Objective**: Establish and document singular table naming convention for all NEW tables, while maintaining existing plural tables (breaking change deferred to post-MVP).

**Expected Outcome**:
```
For new tables:
- user (not users)
- organization (not organizations)
- conversation (not conversations)
✅ Simpler naming, matches ORM models, avoids edge cases

For existing tables (keep as-is):
- Avoid renaming (breaking change, 30-50 hour migration)
- Document in Post-MVP decision plan
```

**Not In Scope** (explicitly):
- ❌ Renaming existing plural tables (too risky for MVP)
- ❌ Updating all 26 existing tables (deferred to post-MVP)
- ❌ Abbreviated names (use full singular: `category` not `cat`)
- ❌ Framework tables (leave `alembic_version` as-is)

---

## What Already Exists

### Documentation ✅
- Database schema documented (shows current plural naming)
- SQLAlchemy models in place
- Alembic migrations framework operational

### What's Missing ❌
- Naming convention documentation for NEW tables
- ADR documenting singular table naming decision
- Code generation templates for new tables
- (Optional) Linter rule for enforcing new convention
- Post-MVP migration plan for existing tables

---

## Requirements

### Phase 1: Documentation & ADR (MVP)
**Objective**: Document convention for NEW tables and create ADR

**Tasks**:
- [ ] Create `docs/internal/development/database/naming-conventions.md`:
  - Table naming convention: Singular noun (not plural)
  - Examples: `user`, `organization`, `conversation`, `session`
  - Non-examples: `users`, `organizations`, `categories`
  - Rationale: Simplicity, ORM matching, no edge cases, FK readability
  - Exceptions: `alembic_version` (framework-controlled, don't rename)
  - Includes plural edge case examples with singular solutions

- [ ] Create ADR: `docs/internal/architecture/current/adrs/adr-XXX-singular-table-naming.md`
  - **Status**: Accepted (for NEW tables only)
  - **Context**: Current tables 26 plural/1 singular, inconsistent with ORM models
  - **Decision**: New tables use singular names, existing tables unchanged
  - **Rationale**:
    - Simplicity (no plural rules to remember)
    - ORM consistency (model name matches table name)
    - Avoids edge cases (category not categories)
    - FK readability (singular-to-singular relationships)
    - Modern convention (Rails 5+, Domain-Driven Design)
  - **Industry context**: Rails, Django, modern ORMs favor singular
  - **Consequences**:
    - Positive: Clarity, simplicity, consistency, no edge cases
    - Negative: Transitional inconsistency (old plural, new singular), 30-50 hour cost if we migrate later
    - Mitigation: Document clearly, gradual adoption, defer migration to post-MVP
  - **When to reconsider**: Multi-org migration (good opportunity to rename all)

- [ ] Update onboarding documentation to reference table naming convention

**Deliverables**:
- Naming conventions document with examples
- ADR for table naming decision
- References in onboarding docs

### Phase 2: Code Review & Templates (Post-MVP)
**Objective**: Ensure new tables follow singular naming convention

**Tasks**:
- [ ] Update code review checklist: "New tables use singular names"
- [ ] Update PR template: "If adding database table, verify table name is singular"
- [ ] Update SQLAlchemy model template:
  ```python
  class Organization(AuditedModel):
      __tablename__ = "organization"  # ✅ Singular (matches class)
      organization_id = Column(UUID, primary_key=True)
  ```
- [ ] Update migration template:
  ```python
  def upgrade():
      op.create_table(
          'organization',  # ✅ Singular
          sa.Column('organization_id', sa.Integer(), nullable=False),
          ...
      )
  ```

**Deliverables**:
- Code review checklist updates
- PR template updates
- Updated code generation templates

### Phase 3: Linter Rule (Optional, Post-MVP)
**Objective**: Prevent accidental plural table names in new migrations

**Tasks**:
- [ ] Create `scripts/lint/check_table_names.py`:
  - Detect `CREATE TABLE` statements in migrations
  - Warn if table name ends in 's' (likely plural)
  - Allow exceptions (e.g., `alembic_version`)
  - Run on every new migration

- [ ] Integrate linter into CI/CD pipeline:
  - Run on PR if migration files modified
  - Fail PR if plural table detected (with clear error message)

**Deliverables**:
- Linter rule implementation
- CI/CD integration
- Clear error messages guiding developers

### Phase 4: Migration Plan (Post-MVP, Deferred)
**Objective**: Plan for renaming existing tables (only if we decide to migrate)

**Tasks** (Post-MVP only):
- [ ] Cost/benefit analysis: Is 30-50 hours worth it?
- [ ] Impact analysis: How many tables, FKs, indexes affected?
- [ ] Create migration script for renaming all 26 tables
- [ ] Update all FK constraints
- [ ] Update all indexes
- [ ] Test rollback on staging environment
- [ ] Update all 26 SQLAlchemy models with new table names
- [ ] Update all queries and relationships in codebase

**Deliverables** (Post-MVP):
- Migration plan document
- Migration cost/benefit analysis
- Decision: Migrate now, later, or never?

### Phase Z: Completion & Integration
- [ ] ADR created and approved by Chief Architect
- [ ] Naming conventions documented clearly
- [ ] Onboarding docs updated
- [ ] First new table uses singular naming as example
- [ ] Code review validates convention for new tables
- [ ] GitHub issue updated with evidence

---

## Acceptance Criteria

### Phase 1: Documentation
- [ ] Naming conventions document created
- [ ] Table naming rule clearly stated: "Use singular noun"
- [ ] Good examples: `user`, `organization`, `conversation`, `session`, `category`
- [ ] Bad examples: `users`, `organizations`, `categories`
- [ ] Plural edge case examples: `person/people`, `index/indices`, `child/children`
- [ ] Rationale section explaining why singular is better
- [ ] Exceptions documented (e.g., framework tables)
- [ ] ADR created: `adr-XXX-singular-table-naming.md`
- [ ] ADR includes industry context and modern convention discussion
- [ ] ADR approved by Chief Architect
- [ ] Onboarding documentation updated with reference

### Phase 2: Templates & Review (Post-MVP)
- [ ] Code review checklist includes table naming check
- [ ] PR template includes migration table naming verification
- [ ] Model template uses singular table names
- [ ] Migration template uses singular table names
- [ ] First new table created uses singular naming
- [ ] Code review validates convention followed

### Phase 3: Linter (Optional, Post-MVP)
- [ ] Linter rule detects plural table names
- [ ] CI/CD integration working
- [ ] Clear error messages guide developers
- [ ] Exception handling for framework tables

### Phase 4: Migration (Post-MVP, Optional)
- [ ] Migration plan documented (if approved)
- [ ] Cost estimate: 30-50 hours
- [ ] FK and index impact analysis completed
- [ ] Rollback tested successfully
- [ ] Decision documented: Migrate, defer, or abandon

### Testing & Validation
- [ ] First new table example follows convention
- [ ] No regressions in existing tables (unchanged)
- [ ] Documentation accurate and complete
- [ ] Onboarding doesn't reference plural tables

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Naming conventions doc | ❌ | [naming-conventions.md] |
| ADR created | ❌ | [adr-XXX-singular-table-naming.md] |
| Chief Architect review | ❌ | [approval] |
| Onboarding updated | ❌ | [onboarding doc] |
| Code review checklist | ❌ | [checklist] |
| PR template updated | ❌ | [template] |
| Templates updated | ❌ | [templates] |
| Linter rule created | ❌ | [linter.py] |
| First new table created | ❌ | [example model] |

**Definition of COMPLETE (MVP)**:
- ✅ Naming conventions documented clearly
- ✅ ADR created and approved
- ✅ Onboarding docs updated
- ✅ Code review checklist includes table naming
- ✅ First new table follows singular convention

---

## Testing Strategy

No code testing needed for MVP (documentation only). Verification:
- [ ] Naming conventions document renders correctly
- [ ] ADR follows template structure
- [ ] All internal links valid
- [ ] All examples clear and correct
- [ ] No broken references

**Validation at first new table**:
- [ ] New table uses singular name (e.g., `organization` not `organizations`)
- [ ] New table uses prefixed PK (e.g., `organization_id` per Issue #335)
- [ ] Code review verifies convention followed
- [ ] SQLAlchemy model matches: `__tablename__ = "organization"`

**Linter validation** (Phase 3):
- [ ] Linter detects plural table names in migrations
- [ ] CI/CD fails on plural tables (unless excepted)
- [ ] Error message guides developer to singular naming

---

## Success Metrics

### Quantitative
- ADR created and approved: 1/1 ✅
- Naming conventions documented: 1/1 ✅
- First new table uses singular naming: 1/1 ✅
- Code review checklist updated: 1/1 ✅
- Linter rule created (Phase 3): 1/1 ✅

### Qualitative
- Chief Architect agrees with singular convention
- Code reviews easier to conduct (clear naming rule)
- New developers understand table naming without explanation
- Developers appreciate no plural edge case confusion
- ORM models match table names (consistency appreciated)

---

## STOP Conditions

**STOP immediately and escalate if**:
- Chief Architect disagrees with singular naming (discuss alternative)
- ADR contradicts existing architectural decisions (resolve conflicts)
- Documentation unclear or incorrect (revise before approving)
- First new table created with plural naming (enforce in code review)
- Linter conflicts with existing migrations (adjust exceptions)

**When stopped**: Document objection, propose alternative, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Small

**Breakdown by Phase**:
- Phase 1 (Documentation & ADR): 4-6 hours
  - Naming conventions doc: 2 hours
  - ADR creation: 1.5 hours
  - Industry context and examples: 1-2 hours

- Phase 2 (Templates & Review): 1-2 hours (lightweight)
  - Update templates: 1 hour
  - Update checklist/PR template: 1 hour

- Phase 3 (Linter rule): 4-5 hours (optional)
  - Linter implementation: 3 hours
  - CI/CD integration: 2 hours

- Phase 4 (Migration plan): 30-50 hours (Post-MVP, deferred)
  - Rename migrations: 20 hours
  - Update FKs/indexes: 15 hours
  - Testing: 10 hours
  - Deployment: 5 hours

**Total MVP**: 4-6 hours (documentation only)
**Total if migration needed**: 34-56 hours

**Complexity Notes**:
- Low complexity for MVP (documentation only, no code changes)
- High complexity if migration needed (30-50 hours, breaking changes)
- Recommended approach: Document now, decide on migration post-MVP

---

## Dependencies

### Required (Must be complete first)
- [ ] Database schema finalized (26+ tables)
- [ ] Issue #335 (prefixed PK naming) ideally addressed in parallel

### Optional (Nice to have)
- [ ] ADR template review
- [ ] Chief Architect availability for review
- [ ] Code generation scripts (for templates)

---

## Related Documentation

- **Related Issues**:
  - #335: Prefixed PK naming (complementary convention)
  - #320, #321, #336: Migration issues (may need table renames if migration done)

- **Database Documentation**:
  - services/database/models.py (current models with plural table names)
  - alembic/versions/ (migrations)

- **References**:
  - Ted Nadeau email (2025-11-19): "suggest table names be singular"
  - Rails conventions: https://guides.rubyonrails.org/active_record_basics.html
  - Django conventions: https://docs.djangoproject.com/en/stable/topics/db/models/
  - Domain-Driven Design: https://martinfowler.com/bliki/DomainDrivenDesign.html

---

## The Great Debate: Singular vs Plural

This is one of computer science's eternal bikeshed topics. Both sides have arguments:

### Arguments for Plural (Current State)

**Pros**:
- ✅ Semantic match: Table IS a collection of rows (plural makes sense)
- ✅ SQL tradition: Most databases use plural naming
- ✅ Reads naturally: "SELECT * FROM users" (multiple users)
- ✅ English grammar: "a collection of users" sounds right

**Cons**:
- ❌ Plural edge cases: categories, people, indices, children
- ❌ ORM mismatch: `class User` vs table `users`
- ❌ FK awkwardness: `lists.owner_id → users.id` (awkward grammar)
- ❌ Must remember plural rules: Is it `persons` or `people`?

### Arguments for Singular (Ted's Recommendation)

**Pros**:
- ✅ No plural edge cases: Always use singular, simple rule
- ✅ ORM consistency: `class User` → table `user` (matches)
- ✅ FK clarity: `list.owner_id → user.user_id` (singular-to-singular)
- ✅ Domain-driven: Table represents entity TYPE, not collection
- ✅ Modern convention: Rails 5+, Django 2+, many modern ORMs favor singular

**Cons**:
- ❌ Grammatically odd: Table is a collection, should be plural
- ❌ Different from SQL tradition
- ❌ "SELECT * FROM user" sounds slightly wrong
- ❌ Migration complexity if renaming existing tables

### Our Decision: Singular

**Why**:
1. **Simplicity**: One rule to remember (always singular), no edge cases
2. **ORM consistency**: Model names match table names
3. **FK readability**: Singular-to-singular relationships are clearer
4. **Avoids confusion**: No more "is it categories or categorys?"
5. **Modern practice**: Aligns with contemporary conventions
6. **Ted's influence**: His point about "annoying plural suffixes 'ies'" resonated

---

## Examples

### Example 1: Good (Singular)
```python
# services/domain/models.py
class Organization(AuditedModel):
    __tablename__ = "organization"  # ✅ Singular (matches class)

    organization_id = Column(UUID, primary_key=True)  # ✅ Prefixed PK
    name = Column(String(255), nullable=False)
    settings = Column(JSON)
```

### Example 2: Good (Junction Table)
```python
class UserOrganization(AuditedModel):
    __tablename__ = "user_organization"  # ✅ Both singular

    user_id = Column(UUID, ForeignKey('user.user_id'))
    organization_id = Column(UUID, ForeignKey('organization.organization_id'))
```

### Example 3: FK Readability
```python
class Session(AuditedModel):
    __tablename__ = "session"  # ✅ Singular

    session_id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey('user.user_id'))  # Clear: session belongs to user
```

### Example 4: Avoids Edge Cases
```python
# No more worrying about plural forms!
class Category(AuditedModel):
    __tablename__ = "category"  # ✅ Not 'categories'

class Person(AuditedModel):
    __tablename__ = "person"  # ✅ Not 'people'

class Index(AuditedModel):
    __tablename__ = "index"  # ✅ Not 'indices'
```

### Example 5: Current (Plural - Keep as-is)
```python
# Existing tables (don't rename in MVP)
class User(AuditedModel):
    __tablename__ = "users"  # Keep plural (breaking change deferred)

    id = Column(UUID, primary_key=True)  # Unprefixed (keep as-is)
```

---

## Trade-offs

### Pros (Singular - New Convention)
- ✅ Simplicity: No plural rules to memorize
- ✅ ORM matching: Model names match table names
- ✅ No edge cases: Category, not categories; person, not people
- ✅ FK clarity: Singular-to-singular relationships
- ✅ Self-documenting: Clear what each table represents
- ✅ Modern convention: Aligns with contemporary best practices

### Cons (Singular - New Convention)
- ❌ Grammatically odd: Table is collection, should be plural (philosophical)
- ❌ Future migration: 30-50 hours if renaming all existing tables
- ❌ Transitional inconsistency: Old tables plural, new singular (confusing?)

### Pros (Plural - Current State)
- ✅ SQL tradition: Most databases use plural
- ✅ Semantic accuracy: Collection of rows = plural
- ✅ Natural reading: "SELECT * FROM users" sounds right

### Cons (Plural - Current State)
- ❌ Plural edge cases: Must know English rules (categories not categorys)
- ❌ ORM mismatch: `class User` → table `users` (different names)
- ❌ FK awkwardness: `lists.owner_id → users.id` (awkward grammar)

---

## Alternatives Considered

**Alternative 1: Keep plural everywhere**
- Pro: No changes needed, matches existing
- Con: Plural edge cases, ORM mismatch, Ted recommended against
- Decision: ❌ Rejected (Ted recommended singular)

**Alternative 2: Migrate all existing tables NOW**
- Pro: Full consistency, done early
- Con: 30-50 hours effort, high risk for alpha
- Decision: ❌ Rejected (too risky for MVP)

**Alternative 3: Singular for new tables, defer migration decision**
- Pro: Immediate clarity for new code, gradual adoption, lower risk
- Con: Transitional inconsistency (old plural, new singular)
- Decision: ✅ Chosen (MVP approach)

**Alternative 4: Linter enforcement for consistency**
- Pro: Prevent regressions, catch plural tables in CI
- Con: Additional tooling required
- Decision: ✅ Chosen for Phase 3 (optional, post-MVP)

---

## Discussion Questions

1. Should we migrate existing 26 tables to singular (high risk, 30-50 hours)?
2. If migrate, do it with multi-org feature (good opportunity) or defer indefinitely?
3. Should linter enforce singular for new migrations (prevent regressions)?
4. Exception for `alembic_version` (framework-controlled)?
5. How to handle existing code documentation that references plural tables?
6. Should we announce convention change in next development meeting?

---

## Completion Checklist

Before requesting PM review:
- [ ] Naming conventions document created ✅
- [ ] ADR created and approved ✅
- [ ] Onboarding docs updated ✅
- [ ] Code review checklist updated ✅
- [ ] PR template updated ✅
- [ ] Model template uses singular ✅
- [ ] Migration template uses singular ✅
- [ ] Linter rule created (Phase 3) ✅
- [ ] First new table uses convention ✅
- [ ] Documentation complete ✅

**Status**: Not Started

---

## Notes for Implementation

**From synthesized issues #337 + #340**:
- Both issues identified same problem: plural tables causing edge case confusion
- Both proposed same solution: singular for new tables, keep existing plural
- #337 had better industry context and explicit "Our Decision" section
- Synthesized into comprehensive documentation with ADR and linter phases

**Key Decisions**:
- MVP focuses on Phase 1: Documentation + ADR (4-6 hours)
- Phase 2 (templates): Lightweight, ready for Phase 1 approval
- Phase 3 (linter): Optional, helps prevent regressions
- Phase 4 (migration): Deferred to post-MVP, decide later if needed
- Coordinate with Issue #335 (prefixed PK naming) for consistent conventions

**Complementary to Issue #335**:
- Issue #335: PK naming convention (`organization_id`)
- This issue: Table naming convention (`organization` not `organizations`)
- Together they create consistent, self-documenting schema

---

**Remember**:
- This is a design decision, not a breaking change (yet)
- MVP: Document for new tables only
- Apply consistently to all new tables going forward
- Revisit migration decision when multi-org feature planned
- Chief Architect should approve convention

---

_Issue synthesized: November 20, 2025_
_Synthesized from: #337 + #340_
_Canonical name: SCHEMA-SINGULAR-TABLES_
