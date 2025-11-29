# INFRA-MIGRATION-ROLLBACK - Comprehensive Database Migration Rollback Testing

**Priority**: P1 (Safety critical)
**Labels**: `infrastructure`, `database`, `testing`, `priority: high`
**Milestone**: MVP
**Epic**: Infrastructure & Reliability
**Related**: #320 (indexes), #321 (audit fields), #336 (soft delete) - all require migrations

---

## Problem Statement

### Current State
Database migrations are written but not systematically tested for rollback safety. This creates critical production risks:

**Production Incidents**:
- Migration fails halfway → database in inconsistent state
- Rollback attempt fails → manual recovery required
- Downtime extends from minutes to hours
- Data corruption if rollback logic is incorrect

**Deployment Fear**:
- Team afraid to run migrations in production
- Migrations delayed, technical debt accumulates
- Manual testing required for each migration (slow, error-prone)
- Can't confidently deploy schema changes

**Lack of Confidence**:
- Don't know if rollback works until production failure
- No automated verification of rollback safety
- Can't practice disaster recovery
- 30+ migration files with unknown rollback status

### Current Implementation
**Migration files exist** (`alembic/versions/`):
- 30+ migration files with `upgrade()` and `downgrade()` functions
- No systematic testing of `downgrade()` functions
- No CI/CD validation of rollback safety
- Manual testing only (inconsistent, error-prone)
- No data integrity checks after migration/rollback

### Impact
- **Blocks**: Cannot confidently deploy large migrations (indexes, soft delete, audit fields)
- **Risk**: Production failures without practiced recovery procedures
- **Velocity**: Fear of migrations slows development pace
- **Compliance**: SOC2 requires rollback capability - not currently tested/documented

---

## Goal

**Primary Objective**: Create comprehensive migration testing framework that validates all migrations can upgrade and safely rollback with zero data loss, plus documented procedures for production deployment.

**Expected Outcome**:
```
When deploying migration:
- Automated tests verify rollback works ✅
- Data integrity validated after migration/rollback ✅
- Performance measured on realistic data ✅
- CI/CD prevents broken migrations from merging ✅
- Team confident in rollback capability ✅
```

**Not In Scope** (explicitly):
- ❌ Optimizing existing slow migrations (address in separate issue)
- ❌ Full-table reorganization strategies (future enhancement)
- ❌ Zero-downtime migration techniques (post-MVP optimization)
- ❌ Database version upgrades (separate infrastructure task)

---

## What Already Exists

### Infrastructure ✅
- Alembic migration framework operational
- PostgreSQL 15 with full DDL transaction support
- 30+ migration files with upgrade/downgrade implementations
- pytest testing framework already in place
- GitHub Actions CI/CD pipeline

### What's Missing ❌
- Systematic rollback testing framework
- Data validation after migration/rollback
- Performance benchmarking for migrations
- CI/CD automation for migration validation
- Migration safety checklist and best practices
- Production migration runbook
- Documented rollback procedures

---

## Requirements

### Phase 1: Migration Testing Framework
**Objective**: Create automated testing suite for all migrations

**Tasks**:
- [ ] Create `tests/infrastructure/` directory with `__init__.py`
- [ ] Implement `MigrationTester` base class in `tests/infrastructure/test_migrations.py`:
  - `test_migration_cycle(revision)` - Full upgrade → downgrade cycle
  - `snapshot_schema()` - Capture database schema (tables, columns, indexes, constraints)
  - `snapshot_data()` - Capture row counts + checksums for data integrity
  - `validate_upgrade(before, after, revision)` - Verify expected schema changes
  - `validate_downgrade(before, after)` - Verify schema restoration
- [ ] Create parametrized tests for all existing migrations
- [ ] Test each migration individually (isolated, not cumulative)
- [ ] Test data preservation during migration/rollback cycles
- [ ] Test idempotency (migrations can run multiple times safely)

**Deliverables**:
- Test framework implementation
- All 30+ migrations with passing rollback tests
- Schema snapshot comparison working
- Data integrity validation functional

### Phase 2: Data Validation Framework
**Objective**: Verify data integrity after migrations

**Tasks**:
- [ ] Create `tests/infrastructure/validators.py` with `MigrationDataValidator` class
- [ ] Implement validation checks:
  - Foreign key integrity (no orphaned records)
  - NOT NULL constraint validation
  - Unique constraint validation
  - Index existence and usability (via EXPLAIN ANALYZE)
  - Domain-specific consistency checks (turn_number sequences, position gaps, etc.)
- [ ] Create test cases for common patterns:
  - Adding columns with defaults
  - Renaming columns
  - Creating indexes
  - Data transformations (splitting columns, merging data, etc.)
- [ ] Test data transformation reversibility (downgrade restores original data)

**Deliverables**:
- Data validation framework
- Test cases for common migration patterns
- Evidence of zero data loss during migration/rollback

### Phase 3: Performance Benchmarking
**Objective**: Measure migration performance on realistic data scales

**Tasks**:
- [ ] Create `tests/infrastructure/performance.py` with `MigrationPerformanceTester` class
- [ ] Implement benchmarking for different data volumes:
  - Small: 1K records
  - Medium: 10K records
  - Large: 100K records
- [ ] Measure both upgrade and downgrade times
- [ ] Define performance thresholds:
  - MVP: <1 minute for any migration on 10K records
  - Production: <30 seconds on production-sized data (100K+ records)
- [ ] Create performance regression detection (fail if slower than baseline)
- [ ] Generate performance benchmark report

**Deliverables**:
- Performance benchmark tests for all migrations
- Baseline measurements documented
- Performance regression detection implemented

### Phase 4: CI/CD Integration
**Objective**: Automate migration testing in GitHub Actions

**Tasks**:
- [ ] Create `.github/workflows/test-migrations.yml`:
  - Runs on: every PR modifying `alembic/versions/`
  - Test PostgreSQL service (postgres:15)
  - Run migration rollback tests
  - Run data validation tests
  - Run performance benchmarks
  - Fail PR if any test fails
- [ ] Add migration test results to PR status checks
- [ ] Ensure CI runs before any migration merge

**Deliverables**:
- GitHub Actions workflow for migration testing
- Automated testing on every PR
- CI prevents broken migrations from merging

### Phase 5: Safety Checklist & Best Practices
**Objective**: Document migration best practices and safety requirements

**Tasks**:
- [ ] Create `docs/internal/development/database/migration-safety-checklist.md`:
  - Pre-migration checklist (downgrade logic, idempotency, test coverage)
  - Data safety checks (preservation, transformation reversibility, defaults)
  - Performance checks (<30 seconds on realistic data)
  - Rollback testing requirements
  - Production readiness (backup, documentation, downtime estimate)
- [ ] Document best practices for common patterns:
  - Adding columns (nullable, server defaults)
  - Renaming columns (reversible transformation)
  - Creating indexes (CONCURRENTLY for zero locks)
  - Data transformations (batch updates, reversible logic)
- [ ] Create examples of good vs bad migrations
- [ ] Update PR template to require migration checklist

**Deliverables**:
- Migration safety checklist
- Best practices guide with examples
- PR template updates

### Phase 6: Production Migration Runbook
**Objective**: Document procedures for safe production migrations

**Tasks**:
- [ ] Create `docs/operations/migration-runbook.md`:
  - Pre-migration checklist (backup, testing, team notification)
  - Migration execution steps with verification
  - Post-migration validation (smoke tests, query verification)
  - Rollback procedure (when/how to rollback)
  - Emergency recovery (restore from backup)
- [ ] Create `scripts/migrate-production.sh`:
  - Verify backup taken
  - Verify rollback tested
  - Record downtime estimate
  - Apply migration with logging
  - Verify migration succeeded
  - Run smoke tests
- [ ] Create smoke test suite (`scripts/smoke-test.sh`)
- [ ] Document monitoring during migration (log tailing, error checking)

**Deliverables**:
- Production migration runbook
- Migration execution script
- Smoke test suite
- Monitoring guidance

### Phase Z: Completion & Validation
- [ ] All 30+ migrations have passing rollback tests
- [ ] Data validation framework verified working
- [ ] Performance benchmarks established
- [ ] CI/CD automation functional
- [ ] Safety checklist implemented
- [ ] Production runbook tested in staging
- [ ] Team trained on new procedures
- [ ] GitHub issue fully updated with evidence

---

## Acceptance Criteria

### Phase 1: Testing Framework
- [ ] `MigrationTester` class created with all methods
- [ ] Full cycle test (upgrade → downgrade) passing
- [ ] Individual migration tests for all 30+ migrations
- [ ] Data preservation tests working
- [ ] Idempotency tests passing
- [ ] All existing migrations have passing rollback tests

### Phase 2: Data Validation
- [ ] `MigrationDataValidator` class created
- [ ] FK validation checks implemented
- [ ] NOT NULL constraint validation working
- [ ] Index existence/usability verification working
- [ ] Domain-specific consistency checks implemented
- [ ] Test cases for common patterns passing
- [ ] Zero data loss verified during migration/rollback

### Phase 3: Performance Benchmarking
- [ ] Performance tests for all migrations
- [ ] Measurements at 1K, 10K, 100K record scales
- [ ] Baseline measurements documented
- [ ] All migrations complete in <1 minute at 10K records
- [ ] Regression detection implemented
- [ ] Performance report generated

### Phase 4: CI/CD Integration
- [ ] `.github/workflows/test-migrations.yml` created
- [ ] Tests run on every migration-related PR
- [ ] PR fails if migration tests fail
- [ ] Performance benchmarks in CI output
- [ ] Data validation results visible in CI

### Phase 5: Safety Documentation
- [ ] Migration safety checklist created
- [ ] Best practices guide with examples
- [ ] Good vs bad migration examples documented
- [ ] PR template includes migration checklist
- [ ] All checklist items verified for existing migrations

### Phase 6: Production Runbook
- [ ] Migration runbook created and tested in staging
- [ ] `migrate-production.sh` script working
- [ ] Smoke test suite functional
- [ ] Backup verification working
- [ ] Rollback procedure tested successfully
- [ ] Team trained and confident with procedures

### Testing & Validation
- [ ] All tests passing (100% success rate)
- [ ] Migration tests run in <10 minutes total
- [ ] No false positives in rollback detection
- [ ] Production runbook tested on staging environment
- [ ] Rollback successfully tested in staging

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Testing framework created | ❌ | [test_migrations.py] |
| All migrations tested | ❌ | [test results] |
| Data validation working | ❌ | [validator tests] |
| Performance benchmarks | ❌ | [performance report] |
| CI/CD integrated | ❌ | [workflow file] |
| Safety checklist | ❌ | [checklist doc] |
| Production runbook | ❌ | [runbook doc] |
| Team training complete | ❌ | [training log] |

**Definition of COMPLETE**:
- ✅ All 30+ migrations pass rollback tests
- ✅ Data validation framework verified
- ✅ Performance thresholds met
- ✅ CI/CD automation working
- ✅ Safety checklist implemented
- ✅ Production procedures tested and documented

---

## Testing Strategy

### Unit Tests: Migration Framework
```python
# tests/infrastructure/test_migrations.py
@pytest.mark.asyncio
async def test_migration_full_cycle(fresh_database):
    """Test: upgrade → validate → downgrade → validate"""
    # 1. Snapshot schema before
    schema_before = await snapshot_schema()

    # 2. Apply migration
    command.upgrade(alembic_cfg, target_revision)
    schema_after = await snapshot_schema()

    # 3. Validate expected changes
    await validate_upgrade(schema_before, schema_after)

    # 4. Rollback
    command.downgrade(alembic_cfg, f"{target_revision}^")
    schema_restored = await snapshot_schema()

    # 5. Verify restoration
    assert schema_restored == schema_before
```

### Integration Tests: Data Validation
```python
@pytest.mark.asyncio
async def test_migration_with_data(fresh_database):
    """Test: data preserved during upgrade/downgrade"""
    # 1. Insert test data before migration
    await insert_test_data()
    data_before = await fetch_all_data()

    # 2. Apply migration
    command.upgrade(alembic_cfg, revision)

    # 3. Verify data unchanged
    data_after = await fetch_all_data()
    assert data_after == data_before

    # 4. Rollback
    command.downgrade(alembic_cfg, f"{revision}^")

    # 5. Verify data preserved
    data_restored = await fetch_all_data()
    assert data_restored == data_before
```

### Performance Tests
```python
@pytest.mark.asyncio
@pytest.mark.parametrize("scale", ["1k", "10k", "100k"])
async def test_migration_performance(scale):
    """Test: measure migration time on different scales"""
    # 1. Seed database with test data
    await seed_database(scale)

    # 2. Benchmark upgrade
    start = time.time()
    command.upgrade(alembic_cfg, revision)
    upgrade_time = time.time() - start

    # 3. Benchmark downgrade
    start = time.time()
    command.downgrade(alembic_cfg, f"{revision}^")
    downgrade_time = time.time() - start

    # 4. Assert thresholds
    assert upgrade_time < 60, f"Upgrade took {upgrade_time}s (threshold: 60s)"
    assert downgrade_time < 60, f"Downgrade took {downgrade_time}s (threshold: 60s)"
```

### CI/CD Tests
```yaml
# .github/workflows/test-migrations.yml
- name: Run migration rollback tests
  run: pytest tests/infrastructure/test_migrations.py -v

- name: Run data validation
  run: pytest tests/infrastructure/test_data_validation.py -v

- name: Run performance benchmarks
  run: pytest tests/infrastructure/test_performance.py -v --tb=short
```

---

## Success Metrics

### Quantitative
- **100% rollback test coverage**: All 30+ migrations have passing tests
- **Zero data loss**: 100% of migrations preserve data during rollback cycles
- **Performance targets**: All migrations <1 min at 10K, <30s at 100K records
- **CI/CD pass rate**: 100% of migrations pass CI/CD before merge
- **Test execution time**: Migration tests complete in <10 minutes

### Qualitative
- Team confident in migration safety
- No fear of production deployments
- Rollback procedures practiced and documented
- CI/CD catches issues before production
- SOC2 rollback capability requirement met

---

## STOP Conditions

**STOP immediately and escalate if**:
- Rollback test fails for any migration (verify downgrade logic, don't skip test)
- Data loss detected during migration/rollback (investigate, don't ignore)
- Performance exceeds thresholds (optimize migration, don't lower threshold)
- CI/CD tests can't run due to infrastructure (fix test environment)
- Migration framework incompatible with existing migrations (investigate root cause)

**When stopped**: Document the issue, investigate root cause, propose fix, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown by Phase**:
- Phase 1 (Testing Framework): 10-15 hours
- Phase 2 (Data Validation): 6-8 hours
- Phase 3 (Performance Benchmarking): 6-8 hours
- Phase 4 (CI/CD Integration): 4-6 hours
- Phase 5 (Safety Checklist): 6-8 hours
- Phase 6 (Production Runbook): 6-8 hours

**Total**: 38-53 hours (~1 week for single developer)

**Complexity Notes**:
- Medium complexity - requires understanding of Alembic, testing patterns, and CI/CD
- Risk: Some existing migrations may have incomplete downgrade logic (fix required)
- Safety critical - must be thorough, no shortcuts
- Benefits: Blocks future high-confidence migration deployments

---

## Dependencies

### Required (Must be complete first)
- [ ] Alembic migrations framework operational
- [ ] PostgreSQL 15+ (atomic DDL support)
- [ ] pytest and testing infrastructure working
- [ ] GitHub Actions CI/CD pipeline configured

### Optional (Nice to have)
- [ ] Database performance monitoring tools
- [ ] Staging environment for testing production procedures
- [ ] Load testing environment

---

## Related Documentation

- **Related Issues**:
  - #320: Database indexes (requires migration testing)
  - #321: Audit fields (requires migration testing)
  - #336: Soft delete (requires migration testing)

- **Database Documentation**:
  - Alembic docs: https://alembic.sqlalchemy.org/
  - PostgreSQL DDL transactions: https://www.postgresql.org/docs/current/ddl.html
  - alembic/versions/ (existing migrations)

- **Project Documentation**:
  - docs/internal/development/database/ (to be created)
  - docs/operations/ (to be created)

---

## Common Migration Patterns & Tests

### Pattern 1: Adding Column
```python
# Migration
def upgrade():
    op.add_column('users', sa.Column('email_verified', sa.Boolean(),
                                      server_default='false', nullable=False))

def downgrade():
    op.drop_column('users', 'email_verified')

# Test: Data preservation, default application
```

### Pattern 2: Renaming Column
```python
# Migration
def upgrade():
    op.alter_column('users', 'name', new_column_name='full_name')

def downgrade():
    op.alter_column('users', 'full_name', new_column_name='name')

# Test: Data values intact after rename, reversible
```

### Pattern 3: Creating Index
```python
# Migration
def upgrade():
    op.create_index('ix_users_email_created', 'users', ['email', 'created_at'])

def downgrade():
    op.drop_index('ix_users_email_created')

# Test: Index exists after upgrade, gone after downgrade
```

### Pattern 4: Data Transformation (Complex)
```python
# Migration: Split 'name' into 'first_name' and 'last_name'
def upgrade():
    # Add new columns
    op.add_column('users', sa.Column('first_name', sa.String(100)))
    op.add_column('users', sa.Column('last_name', sa.String(100)))

    # Migrate data
    connection = op.get_bind()
    connection.execute("""
        UPDATE users
        SET first_name = split_part(name, ' ', 1),
            last_name = split_part(name, ' ', 2)
    """)

    # Drop old column
    op.drop_column('users', 'name')

def downgrade():
    # Add old column back
    op.add_column('users', sa.Column('name', sa.String(200)))

    # Restore data
    connection = op.get_bind()
    connection.execute("""
        UPDATE users
        SET name = COALESCE(first_name, '') || ' ' || COALESCE(last_name, '')
    """)

    # Drop new columns
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')

# Test: Data reversibility - 'John Doe' → {'John', 'Doe'} → 'John Doe'
```

---

## Rollback Scenarios

**Scenario 1: Migration fails halfway**
```
1. Migration starts
2. Error occurs (constraint violation, syntax error)
3. PostgreSQL transaction rolls back automatically
4. Database unchanged (PostgreSQL atomic DDL)
5. Fix migration, retry
✅ No manual intervention needed
```

**Scenario 2: Migration succeeds but breaks application**
```
1. Migration completes successfully
2. Application deployment fails (code incompatible)
3. Run: alembic downgrade -1
4. Verify rollback succeeded: alembic current
5. Redeploy old application version
✅ Service restored quickly with tested rollback
```

**Scenario 3: Rollback fails**
```
1. Attempt rollback: alembic downgrade -1
2. Downgrade fails (bad downgrade logic)
3. Database in partially rolled-back state
4. Manual recovery:
   - Run: alembic current (verify state)
   - Restore from backup: psql < backup.sql
   - Fix downgrade migration
   - Complete rollback manually with corrected migration
✅ Runbook procedures enable recovery
```

---

## Evidence Section

[This section is filled in during/after implementation]

### Test Results
```
Phase 1 - Testing Framework:
- 30+ migrations tested for rollback safety
- All tests passing: 100/100 ✅

Phase 2 - Data Validation:
- FK integrity checks: PASS
- NOT NULL validation: PASS
- Index validation: PASS
- Data transformation reversibility: PASS

Phase 3 - Performance:
- 1K records: <500ms for all migrations
- 10K records: <2s for all migrations
- 100K records: <30s for all migrations

Phase 4 - CI/CD:
- GitHub Actions workflow operational
- Tests run on every migration-related PR
- 0 false positives, 100% test accuracy

Phase 5 - Safety:
- Safety checklist implemented
- All existing migrations verified against checklist
- PR template updated

Phase 6 - Production:
- Runbook tested in staging environment
- Rollback successfully executed
- Team trained and confident
```

---

## Completion Checklist

Before requesting PM review:
- [ ] All migration tests implemented ✅
- [ ] Data validation framework working ✅
- [ ] Performance benchmarks established ✅
- [ ] CI/CD automation functional ✅
- [ ] Safety checklist implemented ✅
- [ ] Production runbook created/tested ✅
- [ ] All tests passing ✅
- [ ] Documentation complete ✅
- [ ] Team training completed ✅

**Status**: Not Started

---

## Notes for Implementation

**From synthesized issues #334 + #338**:
- Both issues identified same problem: migrations not tested for rollback
- #338 had better phase organization; #334 had additional safety checklist focus
- Synthesized into comprehensive framework covering testing, validation, performance, CI/CD, safety, and production procedures

**Key Decisions**:
- MVP focuses on Phases 1-5 (testing + safety)
- Phase 6 (production runbook) can be refined post-MVP with real production experience
- Safety checklist as separate deliverable (easier to maintain)
- Performance benchmarks at 3 scales (1K, 10K, 100K)

**Rollback Procedure Critical**:
- This blocks confidence on #320, #321, #336 migrations
- Should be completed BEFORE large migrations deployed
- Team needs to practice procedures (recommend staging environment runs)

---

**Remember**:
- Migrations are HIGH-RISK operations - must be thorough
- Rollback safety > features (never ship untested downgrade)
- Performance must be measured, not guessed
- Team confidence is the real success metric

---

_Issue synthesized: November 20, 2025_
_Synthesized from: #334 + #338_
_Canonical name: INFRA-MIGRATION-ROLLBACK_
