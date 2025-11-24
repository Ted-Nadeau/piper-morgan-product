# SCHEMA-PREFIXED-PK - Adopt Prefixed Primary Key Naming Convention

**Priority**: P3 (Design convention, Post-MVP)
**Labels**: `enhancement`, `documentation`, `database`, `style`, `priority: low`
**Milestone**: Post-MVP
**Epic**: Architecture & Design
**Related**: Ted Nadeau recommendation (database design best practices), Issue #337 (singular table naming)

---

## Problem Statement

### Current State
Current primary keys use generic `id` name (not table-prefixed). This causes confusion in code and queries:

**Ambiguity in JOINs**:
```sql
-- Current: Which id is which?
SELECT u.id, c.id, l.id
FROM users u
JOIN conversations c ON c.user_id = u.id
JOIN lists l ON l.owner_id = u.id
WHERE u.id = 123;  -- Have to alias everything
```

**Self-documentation**:
```python
# Current: What's this id?
conversation_id = conversation.id  # Is it user_id? conversation_id?

# Clearer:
conversation_id = conversation.conversation_id  # Obviously conversation!
```

**Inconsistency**:
- Foreign keys ARE prefixed: `conversation.user_id`, `list.owner_id`
- Primary keys are NOT: `users.id`, `conversations.id`, `lists.id`
- Creates inconsistency in schema naming

**New developer onboarding**:
- "What does this `id` refer to?" (common question in code reviews)
- Have to trace back to understand context
- Takes longer to understand database relationships

### Current Implementation
**All PKs use unprefixed `id`** (verified from database schema):

```sql
lists.id                 -- NOT lists.list_id
intents.id              -- NOT intents.intent_id
users.id                -- NOT users.user_id
workflows.id            -- NOT workflows.workflow_id
conversations.id        -- NOT conversations.conversation_id
```

**Foreign keys ARE prefixed** (creates inconsistency):
```sql
list_items.list_id     → lists.id        ✅ FK prefixed, but PK not
list_items.item_id     → (polymorphic)   ✅ FK prefixed
intents.workflow_id    → workflows.id    ✅ FK prefixed, but PK not
```

### Impact
- **Code clarity**: Ambiguous `id` attributes require context to understand
- **Onboarding friction**: Developers confused by inconsistent naming
- **Query readability**: Complex JOINs harder to read without clear PK names
- **Database design**: Inconsistent convention (FKs prefixed, PKs not)

### Ted Nadeau's Recommendation
> "Are the primary keys just 'id' or are they prefixed with table name e.g. user_id (probably preferred as less confusing)"

**Preference**: Prefixed PKs recommended for clarity and consistency

---

## Goal

**Primary Objective**: Establish and document prefixed primary key naming convention for all NEW tables, while maintaining existing unprefixed PKs (breaking change deferred to post-MVP).

**Expected Outcome**:
```
For new tables:
- user_id (not id)
- conversation_id (not id)
- organization_id (not id)
✅ Self-documenting, consistent with FKs

For existing tables (keep as-is):
- Avoid renaming (breaking change, 40-60 hour migration)
- Document in Post-MVP migration plan
```

**Not In Scope** (explicitly):
- ❌ Renaming existing table PKs (too risky for MVP)
- ❌ Updating all 27+ existing tables (deferred to post-MVP)
- ❌ Migrating all FK references (part of post-MVP if PK migration done)
- ❌ Abbreviated prefixes (use full names: `organization_id` not `org_id`)

---

## What Already Exists

### Documentation ✅
- Database schema documented (shows current unprefixed PKs)
- SQLAlchemy models in place
- Alembic migrations framework operational

### What's Missing ❌
- Named convention documentation for NEW tables
- ADR documenting PK naming decision
- Updated code generation templates for new tables
- Code review checklist for PK naming
- Post-MVP migration plan for existing tables

---

## Requirements

### Phase 1: Documentation & ADR (MVP)
**Objective**: Document convention for NEW tables and create ADR

**Tasks**:
- [ ] Create `docs/internal/development/database/naming-conventions.md`:
  - Primary key convention: Prefix with singular table name
  - Examples: `user_id`, `conversation_id`, `organization_id`
  - Non-examples: `id`, `org_id` (abbreviated)
  - Rationale: Self-documentation, clarity, consistency with FKs
  - Exceptions: `alembic_version` (framework-controlled)
  - Singular table names (see Issue #337): `user` not `users`

- [ ] Create ADR: `docs/internal/architecture/current/adrs/adr-XXX-primary-key-naming.md`
  - **Status**: Accepted (for NEW tables only)
  - **Context**: Current tables use unprefixed `id`, inconsistent with FKs
  - **Decision**: New tables use prefixed PKs, existing tables unchanged
  - **Rationale**:
    - Self-documenting (obvious what table it belongs to)
    - Clearer JOIN queries (no aliasing needed)
    - Consistent with FK naming convention
    - Better onboarding (less confusion)
  - **Consequences**:
    - Positive: Clarity, consistency, self-documentation
    - Negative: Transitional inconsistency (old unprefixed, new prefixed), 40-60 hour cost if we migrate later
    - Mitigation: Document clearly, gradual adoption, defer migration to post-MVP
  - **When to reconsider**: Multi-org support (good time to migrate existing tables)

- [ ] Update onboarding documentation to reference PK naming convention

**Deliverables**:
- Naming conventions document
- ADR for PK naming decision
- References in onboarding docs

### Phase 2: Code Review & Enforcement (Post-MVP)
**Objective**: Ensure new tables follow prefixed PK convention

**Tasks**:
- [ ] Update code review checklist: "New tables use prefixed PKs"
- [ ] Update PR template: "If adding database table, verify PK naming follows convention"
- [ ] (Optional) Create pre-commit hook to warn on unprefixed PKs in new migrations
- [ ] Update model generation templates (if using templates)

**Deliverables**:
- Code review checklist updates
- PR template updates

### Phase 3: Migration Plan (Post-MVP, Deferred)
**Objective**: Plan for renaming existing PKs (only if we decide to migrate)

**Tasks** (Post-MVP only):
- [ ] Cost/benefit analysis: Is it worth 40-60 hours?
- [ ] Impact analysis: How many tables, FKs, and code files affected?
- [ ] Create migration script for renaming PKs
- [ ] Test rollback on staging environment
- [ ] Update all 27+ models with new PK names
- [ ] Update all queries and relationships

**Deliverables** (Post-MVP):
- Migration plan document
- Migration cost estimate
- Decision: Migrate now or never?

### Phase Z: Completion & Integration
- [ ] ADR created and approved by Chief Architect
- [ ] Naming conventions documented
- [ ] Onboarding docs updated
- [ ] Next new table uses prefixed PKs as example
- [ ] GitHub issue updated with evidence

---

## Acceptance Criteria

### Phase 1: Documentation
- [ ] Naming conventions document created (`docs/internal/development/database/naming-conventions.md`)
- [ ] PK naming rule clearly stated: "Prefix with singular table name"
- [ ] Good examples: `user_id`, `conversation_id`, `organization_id`, `session_id`
- [ ] Bad examples: `id`, `org_id`, `conversation`, `users_id`
- [ ] Rationale section explaining why prefixed is better
- [ ] Exceptions documented (e.g., framework-controlled tables)
- [ ] ADR created: `adr-XXX-primary-key-naming.md`
- [ ] ADR approved by Chief Architect
- [ ] Onboarding documentation updated with reference
- [ ] Examples show singular table names (matches Issue #337)

### Phase 2: Code Review (Post-MVP)
- [ ] Code review checklist includes PK naming check
- [ ] PR template includes migration PK naming verification
- [ ] First new table created uses prefixed PKs
- [ ] Code review validates convention followed

### Phase 3: Migration (Post-MVP, Optional)
- [ ] Migration plan documented (if approved)
- [ ] Cost estimate: 40-60 hours
- [ ] FK impact analysis: All 27+ tables with references identified
- [ ] Rollback tested successfully
- [ ] Decision documented: Migrate or keep current state

### Testing & Validation
- [ ] First new table example follows convention
- [ ] No regressions in existing tables (unchanged)
- [ ] Documentation accurate and complete

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Naming conventions doc | ❌ | [naming-conventions.md] |
| ADR created | ❌ | [adr-XXX-primary-key-naming.md] |
| Chief Architect review | ❌ | [approval] |
| Onboarding updated | ❌ | [onboarding doc] |
| Code review checklist | ❌ | [checklist] |
| PR template updated | ❌ | [template] |
| First new table created | ❌ | [example model] |

**Definition of COMPLETE (MVP)**:
- ✅ Naming conventions documented clearly
- ✅ ADR created and approved
- ✅ Onboarding docs updated
- ✅ Code review checklist includes PK naming
- ✅ First new table follows convention

---

## Testing Strategy

No code testing needed (documentation + convention). Verification:
- [ ] Naming conventions document renders correctly
- [ ] ADR follows template structure
- [ ] All internal links valid
- [ ] Examples are clear and correct
- [ ] No broken references

**Validation at first new table**:
- [ ] New table uses prefixed PK (e.g., `organization_id` not `id`)
- [ ] New table uses singular name (e.g., `organization` not `organizations`)
- [ ] Code review verifies convention followed
- [ ] SQLAlchemy model matches: `organization_id = Column(UUID, primary_key=True)`

---

## Success Metrics

### Quantitative
- ADR created and approved: 1/1 ✅
- Naming conventions documented: 1/1 ✅
- First new table follows convention: 1/1 ✅
- Code review checklist updated: 1/1 ✅

### Qualitative
- Chief Architect agrees with convention
- Code reviews easier to conduct (clear naming)
- New developers understand PK naming without explanation
- Consistency with FK naming appreciated

---

## STOP Conditions

**STOP immediately and escalate if**:
- Chief Architect disagrees with prefixed PK naming (discuss alternative)
- ADR contradicts existing architectural decisions (resolve conflicts)
- Documentation unclear or incorrect (revise, don't merge)
- First new table created without following convention (enforce in code review)

**When stopped**: Document objection, propose alternative, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Small

**Breakdown by Phase**:
- Phase 1 (Documentation & ADR): 4-6 hours
  - Naming conventions doc: 2 hours
  - ADR creation: 1.5 hours
  - Examples and review: 1-2 hours

- Phase 2 (Code Review): 1-2 hours (lightweight)
  - Update checklist: 30 minutes
  - Update PR template: 30 minutes
  - First example validation: 1 hour

- Phase 3 (Migration plan): 40-60 hours (Post-MVP, deferred)

**Total MVP**: 4-6 hours (documentation only)
**Total if migration needed**: 44-66 hours

**Complexity Notes**:
- Low complexity - documentation only, no code changes
- Deferred migration is high complexity but not needed for MVP
- Recommended approach: Document now, decide on migration post-MVP

---

## Dependencies

### Required (Must be complete first)
- [ ] Database schema finalized (27+ current tables)
- [ ] Issue #337 (singular table naming) ideally addressed first

### Optional (Nice to have)
- [ ] ADR template review
- [ ] Chief Architect availability for review

---

## Related Documentation

- **Related Issues**:
  - #337: Singular table naming (complementary convention)
  - #320, #321, #336: Migration issues (may need PK updates if migration done)

- **Database Documentation**:
  - services/database/models.py (current models with unprefixed PKs)
  - alembic/versions/ (migrations)

- **References**:
  - Ted Nadeau email (2025-11-19): "prefixed with table name e.g. user_id (probably preferred)"
  - Rails conventions: https://guides.rubyonrails.org/active_record_basics.html
  - Django conventions: https://docs.djangoproject.com/en/stable/topics/db/models/

---

## Examples

### Example 1: Good (Prefixed PK)
```python
# services/domain/models.py
class Organization(AuditedModel):
    __tablename__ = "organization"  # Singular

    organization_id = Column(UUID, primary_key=True)  # ✅ Prefixed
    name = Column(String(255), nullable=False)
    settings = Column(JSON)
```

### Example 2: Good (FK matches PK)
```python
class Session(AuditedModel):
    __tablename__ = "session"  # Singular

    session_id = Column(UUID, primary_key=True)  # ✅ Prefixed PK
    user_id = Column(UUID, ForeignKey('user.user_id'))  # ✅ FK matches PK name
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Example 3: Clear in Queries
```python
# With prefixed PKs, queries are self-documenting
# SELECT s.session_id, u.user_id FROM session s JOIN user u ...

# vs unprefixed (confusing):
# SELECT s.id, u.id FROM sessions s JOIN users u ...  # Which id is which?
```

### Example 4: Self-Join Clarity
```python
# Employee reporting structure
class Employee(AuditedModel):
    __tablename__ = "employee"

    employee_id = Column(Integer, primary_key=True)  # ✅ Clear
    manager_id = Column(Integer, ForeignKey('employee.employee_id'))  # ✅ Self-ref clear

    # With unprefixed (confusing):
    # id, manager_id → which one is the employee's ID?
```

### Example 5: Current (Unprefixed - Keep as-is)
```python
# Existing tables (don't rename in MVP)
class User(AuditedModel):
    __tablename__ = "users"  # Plural (current convention)

    id = Column(UUID, primary_key=True)  # Keep unprefixed for now
    email = Column(String(255))
```

---

## Trade-offs

### Pros (Prefixed PKs)
- ✅ Self-documenting: `user_id` obviously belongs to user
- ✅ Clearer JOINs: No need to alias in complex queries
- ✅ Consistent with FKs: Both use same naming pattern
- ✅ Prevents errors: Harder to use wrong ID
- ✅ Better onboarding: Obvious to new developers
- ✅ Industry practice: Many projects use this convention

### Cons (Prefixed PKs)
- ❌ More verbose: `user_id` vs `id` (minor)
- ❌ ORM attribute names longer: `user.user_id` vs `user.id` (minor)
- ❌ Future migration complexity: 40-60 hours if renaming existing tables

### Cons (Unprefixed PKs - current state)
- ❌ Ambiguous in JOINs: Which `id` is this?
- ❌ Not self-documenting: Need context to understand
- ❌ Inconsistent with FKs: FKs are prefixed, PKs not
- ❌ Onboarding friction: Common "what's this id?" questions

---

## Alternatives Considered

**Alternative 1: Keep unprefixed `id` forever**
- Pro: No changes needed, matches existing
- Con: Ambiguous, inconsistent with FKs, harder to read
- Decision: ❌ Rejected (Ted recommended prefixed)

**Alternative 2: Migrate all existing tables NOW**
- Pro: Full consistency, done early
- Con: 40-60 hours effort, high risk for alpha
- Decision: ❌ Rejected (too risky for MVP)

**Alternative 3: Document convention for new tables, defer migration**
- Pro: Immediate clarity for new code, gradual adoption, lower risk
- Con: Transitional inconsistency (old unprefixed, new prefixed)
- Decision: ✅ Chosen (MVP approach)

**Alternative 4: Prefix only certain tables (multi-org)**
- Pro: Targeted, lower effort
- Con: Still inconsistent, harder to explain convention
- Decision: ❌ Rejected (apply to all new tables consistently)

---

## Discussion Questions

1. Should we migrate existing tables before multi-org feature (good opportunity)?
2. Should linter enforce this for new migrations (prevent regressions)?
3. Exception for framework-controlled tables (`alembic_version.id`)?
4. Abbreviated prefixes okay? (`org_id` vs `organization_id`)
5. Should ORM models alias attributes for backward compatibility?

---

## Completion Checklist

Before requesting PM review:
- [ ] Naming conventions document created ✅
- [ ] ADR created and approved ✅
- [ ] Onboarding docs updated ✅
- [ ] Code review checklist updated ✅
- [ ] PR template updated ✅
- [ ] First new table uses convention ✅
- [ ] Documentation complete ✅

**Status**: Not Started

---

## Notes for Implementation

**From synthesized issues #335 + #339**:
- Both issues identified same problem: unprefixed PKs causing ambiguity
- Both proposed same solution: prefix new tables, defer existing migration
- #335 emphasized ADR creation; #339 emphasized documentation
- Synthesized into comprehensive documentation package with ADR

**Key Decisions**:
- MVP focuses on Phase 1: Documentation + ADR (4-6 hours)
- Phase 2 (code review): Lightweight enforcement post-MVP
- Phase 3 (migration): Deferred to post-MVP, decide later if needed
- Use full names, not abbreviations: `organization_id` not `org_id`
- Coordinate with Issue #337 (singular table naming)

**Complementary to Issue #337**:
- This issue: PK naming convention (`organization_id`)
- Issue #337: Table naming convention (`organization` not `organizations`)
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
_Synthesized from: #335 + #339_
_Canonical name: SCHEMA-PREFIXED-PK_
