# Gameplan: #647 TRUST-LEVELS-1 Core Infrastructure

**Issue**: #647 (TRUST-LEVELS-1: Core Infrastructure)
**Date**: 2026-01-23
**Author**: Lead Developer
**Template Version**: 9.3 (streamlined for infrastructure work)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (verified)
- [x] Database: PostgreSQL on port 5433 (verified)
- [x] Testing framework: pytest (verified)
- [x] ORM: SQLAlchemy with Alembic migrations (verified)
- [x] Domain models: `services/domain/models.py` (verified)
- [x] Shared types: `services/shared_types.py` (verified)
- [x] Repository pattern: `services/repositories/` (verified)

**My understanding of the task**:
- Create TrustStage enum, TrustEvent and UserTrustProfile domain models
- Create UserTrustProfileDB SQLAlchemy model and migration
- Create UserTrustProfileRepository for persistence
- Create TrustComputationService with stage transition logic
- Write comprehensive unit tests

**Current state**:
- No trust infrastructure exists (verified via grep)
- ADR-053 provides complete code specifications
- Existing patterns in codebase to follow

### Part A.2: Work Characteristics Assessment

**Worktree Assessment**:
- [ ] Multiple agents in parallel - NO (single agent)
- [ ] Task duration >30 minutes - YES
- [ ] Multi-component work - NO (backend only)
- [x] Single agent, sequential work - YES
- [x] Tightly coupled files requiring atomic commits - YES

**Assessment**: **SKIP WORKTREE** - Single agent, sequential phases, tightly coupled domain/DB models.

### Part B: PM Verification (Pre-filled from audit)

**Actual task**: Create new infrastructure from scratch following ADR-053.

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding is correct, gameplan appropriate

---

## Phase 0: Initial Bookending - GitHub Investigation

### Skipped Phases

- **Phase 0.5** (Frontend-Backend Contract): N/A - No UI work
- **Phase 0.6** (Data Flow): N/A - Single-layer infrastructure (will be needed in #648)
- **Phase 0.7** (Conversation Design): N/A - No conversational features
- **Phase 0.8** (Post-Completion): N/A - Infrastructure doesn't change user state directly

### Required Actions

1. **Verify ADR-053 is accessible and complete**
   ```bash
   cat docs/internal/architecture/current/adrs/adr-053-trust-computation-architecture.md | head -20
   ```

2. **Verify existing patterns to follow**
   ```bash
   # Enum pattern
   grep -A 5 "class.*Enum" services/shared_types.py | head -20

   # Dataclass pattern
   grep -A 10 "@dataclass" services/domain/models.py | head -30

   # SQLAlchemy pattern
   grep -A 10 "class.*Base" services/database/models.py | head -30

   # Repository pattern
   ls services/repositories/
   ```

3. **Update GitHub Issue**
   ```bash
   gh issue edit 647 --add-label "in-progress"
   ```

### STOP Conditions
- ADR-053 missing or incomplete → STOP
- Existing patterns unclear → STOP

---

## Phase 1: Domain Models

**Objective**: Create domain layer types in shared_types.py and domain/models.py

### Tasks

1. **Add TrustStage enum to shared_types.py**
   ```python
   class TrustStage(IntEnum):
       """Trust stages per PDR-002 and ADR-053"""
       NEW = 1           # Respond to queries; no unsolicited help
       BUILDING = 2      # Offer related capabilities after task completion
       ESTABLISHED = 3   # Proactive suggestions based on observed context
       TRUSTED = 4       # Anticipate needs; "I'll do X unless you stop me"
   ```

2. **Add TrustEvent dataclass to domain/models.py**
   ```python
   @dataclass
   class TrustEvent:
       """Individual interaction that affects trust"""
       event_id: UUID
       timestamp: datetime
       outcome: Literal["successful", "neutral", "negative"]
       context: str  # Brief description for discussability
       stage_at_time: TrustStage
   ```

3. **Add UserTrustProfile dataclass to domain/models.py**
   - Full specification from ADR-053
   - Include all counters, history, timestamps

### Evidence Required
- grep showing TrustStage in shared_types.py
- grep showing TrustEvent and UserTrustProfile in domain/models.py
- Python import test: `python -c "from services.shared_types import TrustStage; print(TrustStage.NEW)"`

### STOP Conditions
- Import conflicts with existing code → STOP
- Enum value collision → STOP

---

## Phase 2: Database Layer

**Objective**: Create persistence infrastructure

### Tasks

1. **Add UserTrustProfileDB to database/models.py**
   ```python
   class UserTrustProfileDB(Base):
       __tablename__ = "user_trust_profiles"

       id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
       user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, index=True)
       current_stage = Column(Integer, default=1)
       # ... full spec from ADR-053
   ```

2. **Create Alembic migration**
   ```bash
   alembic revision --autogenerate -m "add_user_trust_profiles"
   ```

3. **Run migration**
   ```bash
   alembic upgrade head
   ```

4. **Verify table creation**
   ```bash
   docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d user_trust_profiles"
   ```

### Evidence Required
- Migration file created
- `alembic upgrade head` succeeds
- Table exists with correct columns

### STOP Conditions
- Migration fails → STOP
- Foreign key to users table fails → STOP (verify users table exists)

---

## Phase 3: Repository

**Objective**: Create data access layer

### Tasks

1. **Create services/repositories/trust_repository.py**
   - Follow existing repository patterns
   - Implement: get(user_id), get_or_create(user_id), save(profile)
   - Domain ↔ DB model mapping methods

2. **Create tests/unit/services/repositories/test_trust_repository.py**
   - test_get_returns_none_for_missing
   - test_get_or_create_creates_new
   - test_get_or_create_returns_existing
   - test_save_persists_changes
   - test_domain_db_mapping_roundtrip

3. **Run tests**
   ```bash
   python -m pytest tests/unit/services/repositories/test_trust_repository.py -v
   ```

### Evidence Required
- All 5 repository tests passing
- Test output shown

### STOP Conditions
- Repository pattern unclear → STOP
- Database session management unclear → STOP

---

## Phase 4: Core Service

**Objective**: Create trust computation logic

### Tasks

1. **Create services/trust/ directory**
   ```bash
   mkdir -p services/trust
   touch services/trust/__init__.py
   ```

2. **Create services/trust/trust_service.py**
   - TrustComputationService class
   - All methods from ADR-053:
     - record_interaction(user_id, outcome, context) → TrustStage
     - _compute_stage(profile) → TrustStage
     - _get_floor(profile) → TrustStage
     - handle_explicit_complaint(user_id, complaint) → TrustStage
     - explicit_trust_upgrade(user_id, signal) → TrustStage
   - Add calibration comments to thresholds

3. **Create tests/unit/services/trust/test_trust_service.py**
   - test_new_user_starts_at_stage_1
   - test_stage_1_to_2_after_10_successful
   - test_stage_2_to_3_after_50_successful
   - test_stage_3_to_4_requires_explicit_signal
   - test_consecutive_negatives_drop_stage
   - test_floor_prevents_drop_below_stage_2
   - test_explicit_complaint_drops_to_stage_2
   - test_stage_4_to_3_regression_path
   - test_event_history_bounded_to_50
   - test_neutral_outcome_no_stage_change

4. **Run tests**
   ```bash
   python -m pytest tests/unit/services/trust/test_trust_service.py -v
   ```

### Evidence Required
- All 10 service tests passing
- Test output shown
- Calibration comments visible in code

### STOP Conditions
- Stage transition logic unclear → STOP
- Test coverage insufficient → STOP

---

## Phase Z: Final Bookending & Handoff

### Tasks

1. **Run full test suite to check for regressions**
   ```bash
   python -m pytest tests/unit/ -v --tb=short
   ```

2. **Update Completion Matrix in #647**
   - All components marked ✅
   - Evidence links provided

3. **Update session log with implementation notes**

4. **Request PM approval**

### Evidence Required
- All unit tests passing (new + existing)
- Completion matrix 100%
- Session log complete

---

## Verification Gates

- [ ] Phase 1: Domain models importable
- [ ] Phase 2: Migration runs, table exists
- [ ] Phase 3: Repository tests passing (5 tests)
- [ ] Phase 4: Service tests passing (10 tests)
- [ ] Phase Z: No regressions, ready for PM review

---

## Agent Deployment

**Single Agent**: Lead Developer (Claude Code with Opus)
**Rationale**: Sequential phases, tightly coupled code, straightforward implementation following ADR-053 specs.

---

## STOP Conditions (Apply Throughout)

- ADR-053 code examples inconsistent → STOP
- Existing patterns conflict with ADR-053 → STOP
- Migration fails → STOP
- Any test fails → STOP
- Import errors → STOP

---

## Success Criteria

- [ ] TrustStage enum in shared_types.py
- [ ] TrustEvent and UserTrustProfile in domain/models.py
- [ ] UserTrustProfileDB in database/models.py
- [ ] Migration runs successfully
- [ ] UserTrustProfileRepository with 5 passing tests
- [ ] TrustComputationService with 10 passing tests
- [ ] No regressions in existing tests
- [ ] Stage 4→3 regression path verified

---

_Gameplan created: 2026-01-23_
_Ready for audit against gameplan-template.md_
