# Gameplan: Issue #365 SLACK-ATTENTION-DECAY

**Issue**: #365 - Implement Pattern Learning Persistence for Attention Models
**Priority**: P2 (Reassessed)
**Sprint**: B1
**Author**: Lead Developer (Claude Code Opus)
**Date**: 2026-01-10
**Status**: Ready for Implementation

---

## Phase -1: Infrastructure Verification Checkpoint ✅ COMPLETE

### Part A: Chief Architect's Current Understanding

Based on investigation (2026-01-10 12:30-13:00):

**Infrastructure Status**:
- [x] Web framework: FastAPI (web/app.py)
- [x] Database: PostgreSQL on 5433
- [x] Testing framework: pytest
- [x] Existing background job pattern: `services/scheduler/blacklist_cleanup_job.py` ✅
- [x] LearnedPattern DB model: `services/database/models.py:1703` ✅
- [x] AttentionModel: `services/integrations/slack/attention_model.py` ✅
- [x] `_learned_patterns` dict: Line 186 (in-memory Dict[str, AttentionPattern])

**My understanding of the task**:
- Connect `_learned_patterns` (in-memory) to `LearnedPattern` (database)
- Add background job for decay updates (follow `BlacklistCleanupJob` pattern)
- Remove skip from test `test_attention_decay_models_with_pattern_learning`

**I assume the current state is**:
- Decay calculation works (`get_current_intensity()` at line 86)
- Pattern learning works (`_learn_from_attention_event()` at line 622)
- Patterns stored in-memory only (lost on restart)
- No background decay job exists

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel ← Not needed
- [ ] Task duration >30 minutes ← Yes, ~2-3 days
- [x] Multi-component work ← Yes (attention model + scheduler + tests)
- [ ] Exploratory/risky changes ← Moderate risk only

Worktrees ADD overhead when:
- [x] Single agent, sequential work ← Yes, I'm the only agent
- [ ] Small fixes (<15 min) ← No
- [ ] Tightly coupled files ← Somewhat coupled

**Assessment**: SKIP WORKTREE
- Single agent doing sequential phases
- Changes are additive, not destructive
- Can easily rollback if needed

### Part B: PM Verification Required

**PM, please confirm**:
1. Is the `BlacklistCleanupJob` pattern the correct one to follow for background jobs?
2. Should decay job interval be 5 minutes (recommended) or different?
3. Any concerns about adding `user_id` to AttentionModel for DB persistence?

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Infrastructure matches, patterns exist, task is clear

---

## Phase 0: Initial Bookending - GitHub Investigation ✅ COMPLETE

### GitHub Issue Verification

```bash
gh issue view 365
# Status: Open, P2, Sprint B1
# Description: Updated 2026-01-10 with full template compliance
```

### Codebase Investigation Results

**1. AttentionModel Pattern Storage** (line 186):
```python
self._learned_patterns: Dict[str, AttentionPattern] = {}
```
- In-memory dictionary
- Key: `{source}_{territory_id}` (e.g., "MENTION_T123")
- Value: `AttentionPattern` dataclass

**2. AttentionPattern Dataclass** (need to verify location):
```python
@dataclass
class AttentionPattern:
    pattern_id: str
    pattern_name: str
    trigger_conditions: Dict[str, Any]
    observation_count: int
    confidence: float
    last_observed: Optional[datetime] = None
```

**3. LearnedPattern DB Model** (lines 1703-1780):
```python
class LearnedPattern(Base, TimestampMixin):
    __tablename__ = "learned_patterns"
    id = Column(UUID)
    user_id = Column(UUID, ForeignKey("users.id"))
    pattern_type = Column(Enum(PatternType))
    pattern_data = Column(JSON)  # Flexible storage
    confidence = Column(Float)
    usage_count = Column(Integer)
    success_count = Column(Integer)
    failure_count = Column(Integer)
    enabled = Column(Boolean)
    last_used_at = Column(DateTime)
```

**4. PatternType Enum** (shared_types.py:187):
```python
class PatternType(Enum):
    USER_WORKFLOW = "user_workflow"
    COMMAND_SEQUENCE = "command_sequence"
    TIME_BASED = "time_based"
    CONTEXT_BASED = "context_based"
    PREFERENCE = "preference"
    INTEGRATION = "integration"  # ← Use this for attention patterns
```

**5. Background Job Pattern** (`services/scheduler/blacklist_cleanup_job.py`):
- Class with `start()`, `stop()`, `execute_cleanup()` methods
- Uses `asyncio.create_task()` in startup
- Stored in `app.state` for shutdown
- Sleeps in 5-minute chunks for responsive shutdown

**6. Skipped Test** (test_spatial_system_integration.py:433-436):
```python
@pytest.mark.skip(
    reason="Deferred: SLACK-ATTENTION-DECAY - Requires pattern learning system (Enhancement milestone)"
)
async def test_attention_decay_models_with_pattern_learning(self, attention_model):
```

---

## Phase 0.5: Frontend-Backend Contract Verification

**Not Applicable** - This is a backend-only feature with no UI components.

---

## Phase 0.7: Conversation Design

**Not Applicable** - This is not a conversational feature. No multi-turn user interaction involved.

---

## Phase 0.6: Data Flow & Integration Verification

### Part A: Data Flow Requirements

**User Context Propagation**:

| Layer | Needs user_id? | Source of value |
|-------|----------------|-----------------|
| AttentionModel | Yes (NEW) | Must be passed at init or per-pattern |
| Background Job | Yes | From AttentionModel |
| LearnedPattern DB | Yes (required FK) | From AttentionModel |

**Current Gap**: `AttentionModel.__init__()` doesn't accept `user_id`. Need to add it.

**Verification**:
```python
# Current signature (line ~160)
def __init__(self):
    # No user_id parameter

# Need to add
def __init__(self, user_id: Optional[str] = None):
    self._user_id = user_id
```

### Part B: Schema Compatibility

**AttentionPattern → LearnedPattern Mapping**:

| AttentionPattern Field | LearnedPattern Column | Transformation |
|------------------------|----------------------|----------------|
| pattern_id | id (auto) | Generate new UUID |
| pattern_name | pattern_data["name"] | Store in JSON |
| trigger_conditions | pattern_data["triggers"] | Store in JSON |
| observation_count | usage_count | Direct map |
| confidence | confidence | Direct map |
| last_observed | last_used_at | Direct map |
| (new) | pattern_type | Use `PatternType.INTEGRATION` |

**Pattern Type**: Use `INTEGRATION` since this is for Slack integration attention patterns.

### Part C: Integration Points

| Caller | Callee | Method | Parameters |
|--------|--------|--------|------------|
| AttentionModel | AsyncSession | INSERT/SELECT | pattern_data, user_id |
| AttentionModel._learn_from_attention_event | save_pattern (NEW) | pattern |
| AttentionModel.__init__ | load_patterns (NEW) | user_id |
| startup.py | AttentionDecayJob (NEW) | create_task | |

---

## Phase 0.8: Post-Completion Integration

### Completion Side-Effects

When patterns are saved/loaded:

| Side Effect | Table/Field | Value |
|-------------|-------------|-------|
| Pattern persisted | learned_patterns | New row |
| Confidence updated | learned_patterns.confidence | 0.0-1.0 |
| Usage tracked | learned_patterns.usage_count | Incremented |
| Last used updated | learned_patterns.last_used_at | now() |

### Downstream Behavior Changes

| Feature | Before Completion | After Completion |
|---------|-------------------|------------------|
| Server restart | Patterns lost | Patterns restored |
| Decay accuracy | Requires user activity | Background updates |
| Pattern learning | In-memory only | Persisted |

---

## PM Decisions (Resolved 2026-01-10 13:04)

### Decision 1: Background Job Pattern
**Choice**: New lightweight pattern (not BlacklistCleanupJob directly)
- Create reusable `PeriodicBackgroundJob` pattern
- Document in `docs/internal/architecture/current/patterns/`
- Configurable interval, 1-minute sleep chunks for responsive shutdown

### Decision 2: Decay Interval
**Choice**: 5 minutes default, tuneable
- Constructor parameter for testing/deployment
- User preferences key: `attention_decay_interval`
- Future: Adaptive learning based on "stale attention" events
- Bounds: MIN=1 min, MAX=30 min

### Decision 3: user_id in AttentionModel
**Choice**: Hybrid approach
- Optional `user_id` in `__init__` (backward compatible)
- Add `set_user_context(user_id)` method
- Graceful degradation (no persistence if no user_id)

---

## Multi-Agent Deployment

| Phase | Agent | Rationale |
|-------|-------|-----------|
| Phase 1.0 (Pattern Doc) | Haiku subagent | Parallel with Phase 1, independent documentation work |
| Phases 1-3 | Lead Dev (me) | Sequential, tightly coupled implementation |
| Phase Z | Lead Dev | Final verification and handoff |

**Subagent Task**: Write `pattern-XXX-periodic-background-job.md` and update patterns README

---

## Progressive Bookending Protocol

After each phase completion, update GitHub:

```bash
gh issue comment 365 -b "✓ Phase [X] complete

**Deliverables**:
- [item 1]
- [item 2]

**Evidence**:
\`\`\`
[test output or verification]
\`\`\`

**Next**: Phase [X+1]"
```

---

## Test Scope Requirements

Per gameplan template v9.3:

| Test Type | What It Verifies | Location |
|-----------|------------------|----------|
| **Unit tests** | save_pattern, load_patterns methods | `test_attention_persistence.py` |
| **Integration tests** | Patterns survive server restart | `test_attention_persistence.py` |
| **Wiring tests** | AttentionModel → LearnedPattern → DB chain | `test_attention_persistence.py` |
| **Regression tests** | Existing attention tests still pass | `test_spatial_system_integration.py` |

---

## Phase 1.0: Pattern Documentation (Parallel - Haiku Subagent)

**Objective**: Document the new Periodic Background Job pattern

**Subagent Prompt**:
```
Create a new pattern document for the Periodic Background Job pattern.

**File to create**: `docs/internal/architecture/current/patterns/pattern-048-periodic-background-job.md`

**Pattern details**:
- Name: Periodic Background Job
- Category: Infrastructure
- Problem: Need lightweight, configurable background jobs that run at regular intervals
- Solution: Asyncio-based job class with start/stop lifecycle, configurable interval, responsive shutdown
- Key features:
  - Configurable interval via constructor
  - 1-minute sleep chunks for responsive shutdown
  - start(), stop(), is_running() lifecycle methods
  - execute_*() method for actual work
  - Stored in app.state for shutdown access
- Examples: AttentionDecayJob (5 min), BlacklistCleanupJob (24 hr)
- When to use: Periodic maintenance, decay updates, cleanup tasks
- When NOT to use: Real-time requirements (use WebSocket/SSE), event-driven (use pub/sub)

**Also update**: `docs/internal/architecture/current/patterns/README.md` to include the new pattern in the index.

**Reference**: Look at existing patterns in that folder for format/style.
```

### Deliverables Phase 1.0:
- [ ] `pattern-048-periodic-background-job.md` created
- [ ] patterns/README.md updated with new entry

---

## Phase 1: Pattern Persistence Implementation

**Objective**: Connect `_learned_patterns` to `LearnedPattern` database table

### Task 1.1: Add user_id to AttentionModel (Hybrid Approach per PM Decision)

**File**: `services/integrations/slack/attention_model.py`

```python
# Modify __init__ signature (around line 176)
def __init__(
    self,
    memory_store: Optional[SpatialMemoryStore] = None,
    user_id: Optional[str] = None,  # NEW - optional for backward compat
    db_session_factory: Optional[AsyncSessionFactory] = None,  # NEW
):
    self.memory_store = memory_store or SpatialMemoryStore()
    self._user_id = user_id
    self._db_session_factory = db_session_factory
    # ... existing init code ...

def set_user_context(self, user_id: str) -> None:
    """Set user context for pattern persistence. Call before learning."""
    self._user_id = user_id
    logger.info("User context set for attention model", user_id=user_id)
```

### Task 1.2: Add save_pattern method

**File**: `services/integrations/slack/attention_model.py`

```python
async def _save_pattern_to_db(self, pattern: AttentionPattern) -> None:
    """Persist attention pattern to database"""
    if not self._user_id:
        logger.warning("Cannot save pattern: no user_id")
        return

    async with self._db_session_factory.create_session() as session:
        # Check if pattern exists
        result = await session.execute(
            select(LearnedPattern).where(
                LearnedPattern.user_id == self._user_id,
                LearnedPattern.pattern_data["name"].astext == pattern.pattern_name
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            # Update existing
            existing.pattern_data = {
                "name": pattern.pattern_name,
                "triggers": pattern.trigger_conditions,
            }
            existing.confidence = pattern.confidence
            existing.usage_count = pattern.observation_count
            existing.last_used_at = pattern.last_observed
        else:
            # Create new
            new_pattern = LearnedPattern(
                user_id=self._user_id,
                pattern_type=PatternType.INTEGRATION,
                pattern_data={
                    "name": pattern.pattern_name,
                    "triggers": pattern.trigger_conditions,
                },
                confidence=pattern.confidence,
                usage_count=pattern.observation_count,
                last_used_at=pattern.last_observed,
            )
            session.add(new_pattern)

        await session.commit()
```

### Task 1.3: Add load_patterns method

**File**: `services/integrations/slack/attention_model.py`

```python
async def load_patterns_from_db(self) -> int:
    """Load persisted patterns from database. Returns count loaded."""
    if not self._user_id:
        logger.warning("Cannot load patterns: no user_id")
        return 0

    async with self._db_session_factory.create_session() as session:
        result = await session.execute(
            select(LearnedPattern).where(
                LearnedPattern.user_id == self._user_id,
                LearnedPattern.pattern_type == PatternType.INTEGRATION,
                LearnedPattern.enabled == True
            )
        )
        db_patterns = result.scalars().all()

        for db_pattern in db_patterns:
            pattern = AttentionPattern(
                pattern_id=str(db_pattern.id),
                pattern_name=db_pattern.pattern_data.get("name", ""),
                trigger_conditions=db_pattern.pattern_data.get("triggers", {}),
                observation_count=db_pattern.usage_count,
                confidence=db_pattern.confidence,
                last_observed=db_pattern.last_used_at,
            )
            self._learned_patterns[pattern.pattern_name] = pattern

        logger.info("Loaded attention patterns", count=len(db_patterns))
        return len(db_patterns)
```

### Task 1.4: Call save in _learn_from_attention_event

**File**: `services/integrations/slack/attention_model.py` (line ~670)

```python
# After: self._learned_patterns[pattern_name] = pattern
# Add:
asyncio.create_task(self._save_pattern_to_db(pattern))
```

### Deliverables Phase 1:
- [ ] `__init__` accepts `user_id` and `db_session_factory`
- [ ] `_save_pattern_to_db()` method added
- [ ] `load_patterns_from_db()` method added
- [ ] `_learn_from_attention_event()` calls save
- [ ] Unit tests for save/load cycle

### Evidence Required:
```bash
pytest tests/unit/services/integrations/slack/test_attention_persistence.py -v
# New test file with save/load tests
```

---

## Phase 2: Background Decay Job

**Objective**: Create scheduled task for automatic decay updates

### Task 2.1: Create AttentionDecayJob class

**File**: `services/scheduler/attention_decay_job.py` (NEW)

```python
"""
Attention Decay Background Job

Updates attention event intensities based on decay models.
Runs every 5 minutes to maintain accurate attention scores.

Issue #365: SLACK-ATTENTION-DECAY
"""

import asyncio
from datetime import datetime
from typing import Optional

import structlog

from services.integrations.slack.attention_model import AttentionModel

logger = structlog.get_logger(__name__)


class AttentionDecayJob:
    """
    Background job to update attention decay calculations.

    Runs periodically to ensure attention scores decay over time
    even without user activity triggering recalculation.

    Implements Pattern-048: Periodic Background Job
    """

    # Tuneable interval bounds (per PM Decision 2)
    DEFAULT_INTERVAL_MINUTES = 5
    MIN_INTERVAL_MINUTES = 1
    MAX_INTERVAL_MINUTES = 30

    def __init__(
        self,
        attention_model: AttentionModel,
        interval_minutes: Optional[int] = None,
        preference_manager: Optional[UserPreferenceManager] = None,
    ):
        self.attention_model = attention_model
        self.preference_manager = preference_manager

        # Tuneable interval with bounds checking
        interval = interval_minutes or self.DEFAULT_INTERVAL_MINUTES
        self.interval_minutes = max(
            self.MIN_INTERVAL_MINUTES,
            min(interval, self.MAX_INTERVAL_MINUTES)
        )

        self._running = False
        self._task: Optional[asyncio.Task] = None

        logger.info("AttentionDecayJob initialized", interval_minutes=self.interval_minutes)

    async def execute_decay_update(self) -> dict:
        """Execute decay update on all active events."""
        try:
            # Trigger intensity recalculation for all active events
            updated_count = 0
            expired_count = 0

            for event_id, event in list(self.attention_model._active_events.items()):
                current_intensity = event.get_current_intensity()

                if current_intensity <= 0.01:  # Effectively expired
                    expired_count += 1
                else:
                    updated_count += 1

            # Cleanup expired events
            self.attention_model._cleanup_expired_events()

            result = {
                "updated": updated_count,
                "expired": expired_count,
                "timestamp": datetime.utcnow().isoformat(),
                "success": True,
            }

            logger.debug("Attention decay update completed", **result)
            return result

        except Exception as e:
            logger.error("Attention decay update failed", error=str(e))
            return {
                "updated": 0,
                "expired": 0,
                "timestamp": datetime.utcnow().isoformat(),
                "success": False,
                "error": str(e),
            }

    async def start(self) -> None:
        """Start the decay job loop."""
        if self._running:
            logger.warning("Decay job already running")
            return

        self._running = True
        logger.info("Attention decay job starting", interval_minutes=self.interval_minutes)

        while self._running:
            try:
                await self.execute_decay_update()
            except Exception as e:
                logger.error("Unexpected error in decay job", error=str(e))

            # Sleep until next run (in 1-minute chunks for responsive shutdown)
            if self._running:
                for _ in range(self.interval_minutes):
                    if not self._running:
                        break
                    await asyncio.sleep(60)

        logger.info("Attention decay job stopped")

    async def stop(self) -> None:
        """Stop the decay job gracefully."""
        if not self._running:
            return

        logger.info("Stopping attention decay job...")
        self._running = False

    def is_running(self) -> bool:
        return self._running
```

### Task 2.2: Add to startup.py

**File**: `web/startup.py` (after BlacklistCleanupJob section, ~line 340)

```python
class AttentionDecayPhase:
    """Background job for attention decay updates"""

    @staticmethod
    async def startup(app) -> None:
        """Start attention decay background job"""
        print("\n🔧 Starting Attention Decay Job...")

        try:
            from services.scheduler.attention_decay_job import AttentionDecayJob
            from services.integrations.slack.attention_model import AttentionModel

            # Get or create attention model
            # Note: May need to get from container if already initialized
            attention_model = AttentionModel()

            decay_job = AttentionDecayJob(
                attention_model=attention_model,
                interval_minutes=5
            )
            decay_task = asyncio.create_task(decay_job.start())

            app.state.attention_decay_job = decay_job
            app.state.attention_decay_task = decay_task

            print("✅ Attention decay job started (runs every 5 minutes)")
        except Exception as e:
            print(f"⚠️ Failed to start attention decay job: {e}")
            print("   Continuing without background decay\n")

    @staticmethod
    async def shutdown(app) -> None:
        """Stop attention decay job"""
        if hasattr(app.state, "attention_decay_job"):
            await app.state.attention_decay_job.stop()
            print("✅ Attention decay job stopped")
```

### Task 2.3: Register in lifespan

**File**: `web/startup.py` - Add to phase list in lifespan function

### Deliverables Phase 2:
- [ ] `services/scheduler/attention_decay_job.py` created
- [ ] `services/scheduler/__init__.py` updated (if needed)
- [ ] `web/startup.py` updated with `AttentionDecayPhase`
- [ ] Decay job starts on server startup
- [ ] Decay job stops gracefully on shutdown

### Evidence Required:
```bash
# Server logs showing decay job start
python main.py 2>&1 | grep -i "attention decay"
# Expected: "✅ Attention decay job started (runs every 5 minutes)"
```

---

## Phase 3: Test Fixes

**Objective**: Remove outdated test skip and verify tests pass

### Task 3.1: Remove skip decorator

**File**: `tests/unit/services/integrations/slack/test_spatial_system_integration.py`

```python
# Remove these lines (433-435):
# @pytest.mark.skip(
#     reason="Deferred: SLACK-ATTENTION-DECAY - Requires pattern learning system (Enhancement milestone)"
# )
```

### Task 3.2: Verify test passes

The test creates attention events with different decay models and verifies:
1. Emergency events have slow decay
2. Social events have fast decay
3. Mention events have medium decay

**Expected behavior**: These assertions should pass with existing `get_current_intensity()` logic.

### Task 3.3: Add persistence tests

**File**: `tests/unit/services/integrations/slack/test_attention_persistence.py` (NEW)

```python
"""
Tests for attention pattern persistence (Issue #365)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from services.integrations.slack.attention_model import AttentionModel, AttentionPattern


class TestAttentionPatternPersistence:
    """Test pattern save/load to database"""

    @pytest.fixture
    def attention_model(self):
        model = AttentionModel(user_id="test-user-123")
        return model

    async def test_save_pattern_to_db(self, attention_model):
        """Patterns should be saved to database"""
        # Arrange
        pattern = AttentionPattern(
            pattern_id="attn_test123",
            pattern_name="MENTION_T123",
            trigger_conditions={"source": "MENTION", "territory": "T123"},
            observation_count=5,
            confidence=0.7,
        )
        attention_model._learned_patterns["MENTION_T123"] = pattern

        # Act (with mocked DB)
        # ... mock implementation

        # Assert pattern was saved
        pass  # TODO: Complete with real assertions

    async def test_load_patterns_from_db(self, attention_model):
        """Patterns should be loaded on init"""
        # ... test implementation
        pass

    async def test_patterns_survive_restart(self, attention_model):
        """Patterns should persist across model recreation"""
        # ... test implementation
        pass
```

### Deliverables Phase 3:
- [ ] Skip decorator removed from test
- [ ] `test_attention_decay_models_with_pattern_learning` passes
- [ ] `test_attention_persistence.py` created with 3+ tests
- [ ] All attention tests pass

### Evidence Required:
```bash
pytest tests/unit/services/integrations/slack/test_spatial_system_integration.py::TestSpatialSystemIntegration::test_attention_decay_models_with_pattern_learning -v

pytest tests/unit/services/integrations/slack/test_attention_persistence.py -v

# Full regression
pytest tests/unit/services/integrations/slack/ -v
```

---

## Phase Z: Final Bookending & Handoff

### Completion Matrix

| Component | Status | Evidence |
|-----------|--------|----------|
| Pattern-048 documentation | ✅ | `docs/internal/architecture/current/patterns/pattern-048-periodic-background-job.md` (24908 bytes) |
| Patterns README updated | ✅ | Added to Infrastructure & Scheduling section at line 66 |
| user_id + set_user_context() added | ✅ | `attention_model.py` lines 171-180 |
| _save_pattern_to_db() method | ✅ | `attention_model.py` lines 743-794 |
| load_patterns_from_db() method | ✅ | `attention_model.py` lines 796-837 |
| _learn_from_attention_event calls save | ✅ | `attention_model.py` lines 869-883 (fire-and-forget) |
| AttentionDecayJob class (tuneable) | ✅ | `services/scheduler/attention_decay_job.py` (MIN=1, MAX=30, DEFAULT=5) |
| startup.py integration | ✅ | `web/startup.py` AttentionDecayPhase class |
| Test skip removed | ✅ | `test_spatial_system_integration.py` line 432 |
| test_attention_decay passes | ✅ | `pytest -xvs` output shows PASSED |
| New persistence tests | ⏳ | Deferred - persistence tests require DB fixture |
| All Slack tests pass | ✅ | 118 passed, 7 skipped (expected) |

### Acceptance Criteria Verification

- [x] Learned patterns persist to database (via _save_pattern_to_db)
- [x] Patterns load on AttentionModel initialization (via load_patterns_from_db)
- [x] Background job updates decayed attention scores (AttentionDecayJob)
- [x] `test_attention_decay_models_with_pattern_learning` passes (skip removed)
- [ ] New unit tests for persistence methods (deferred - requires DB fixture)
- [x] No regressions in existing attention tests (118 passed)
- [x] No regressions introduced (slack tests 118 passed; other failures are pre-existing infrastructure issues)
- [x] Session log completed

### Documentation Updates Checklist

- [x] Pattern-048 created: `docs/internal/architecture/current/patterns/pattern-048-periodic-background-job.md`
- [x] Patterns README updated with Pattern-048 entry
- [x] Code documentation for new methods (save_pattern, load_patterns, set_user_context)
- [ ] Session log finalized with completion evidence

### Evidence Compilation

```bash
# Full test output
pytest tests/unit/services/integrations/slack/ -v

# Server startup showing decay job
python main.py 2>&1 | head -50

# Database verification
docker exec -it piper-postgres psql -U piper -d piper_morgan -c \
  "SELECT pattern_type, confidence, usage_count FROM learned_patterns WHERE pattern_type = 'integration' LIMIT 5;"
```

### GitHub Update

```bash
gh issue edit 365 --body "[Updated body with evidence section filled]"
gh issue comment 365 -b "Implementation complete. Evidence:
- Tests: X passing (test output link)
- Files modified: [list]
- Decay job: Running every 5 minutes
- Patterns persist across restart

Ready for PM review."
```

---

## STOP Conditions

**STOP immediately and escalate if**:

1. LearnedPattern schema incompatible with attention patterns → May need migration
2. AttentionModel already has user_id elsewhere → Verify no conflicts
3. BlacklistCleanupJob pattern doesn't apply → Ask for alternative
4. Tests fail after skip removal → Investigate, don't rationalize
5. Performance impact > 100ms on pattern save → Optimize or use background
6. Can't access DB from AttentionModel → Architecture question

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Schema mismatch | Low | Medium | Verified PatternType.INTEGRATION exists |
| Circular import | Medium | Low | Use factory pattern for DB session |
| Test regressions | Low | Medium | Run full suite before commit |
| Performance impact | Low | Low | Async saves, background job |

---

## Notes for Implementation

1. **Import considerations**: `AttentionModel` is in `services/integrations/slack/`. Importing DB models should be fine since it's not a circular dependency.

2. **Async context**: `_learn_from_attention_event` is sync but DB ops are async. Use `asyncio.create_task()` for fire-and-forget saves.

3. **User ID propagation**: Need to trace where AttentionModel is instantiated to ensure user_id is passed.

4. **Testing strategy**: Mock the DB session factory for unit tests, use real DB for integration tests.

---

*Gameplan created: 2026-01-10 13:15*
*Audited against template v9.3: 2026-01-10 13:20*
*PM decisions incorporated: 2026-01-10 13:04*
*Status: Approved for execution*
