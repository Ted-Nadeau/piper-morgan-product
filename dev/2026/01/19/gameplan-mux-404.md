# Gameplan: MUX-404 Grammar Application Framework

**GitHub Issue**: #404
**Parent Epic**: #399 MUX-VISION-OBJECT-MODEL
**Type**: Documentation/Pattern-Heavy Implementation
**Estimated Effort**: Medium (~21 hours)
**Created**: 2026-01-19
**Depends On**: #613 (P1 Core Grammar & Lens Infrastructure) - COMPLETE

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status** (verified):
- [x] P1 Infrastructure: `services/mux/` module complete (101 tests passing)
- [x] Protocols: EntityProtocol, MomentProtocol, PlaceProtocol (@runtime_checkable)
- [x] Situation: Async context manager implemented
- [x] Lenses: 8 lenses with PerceptionMode (NOTICING, REMEMBERING, ANTICIPATING)
- [x] LensSet: Compound perception working
- [x] ADR-045: Grammar definition ACCEPTED
- [x] ADR-055: Implementation specification COMPLETE
- [x] Morning Standup: Reference implementation at `services/features/morning_standup.py`

**Key P0/P1 Findings Informing This Work**:
1. Morning Standup expresses grammar naturally - use as reference
2. P1 infrastructure provides Protocol/Lens tools for grammar application
3. Intent classification identified as high-leverage transformation example
4. Anti-flattening tests belong in `tests/unit/services/mux/`

**My understanding of the task**:
- Create application patterns and transformation guide (documentation-heavy)
- Build anti-flattening test infrastructure
- Complete worked example (intent classification responses)
- Enable developers to apply grammar independently

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [x] Task duration >30 minutes (main branch may advance) ← YES, ~21 hours
- [ ] Exploratory/risky changes where easy rollback is valuable

Worktrees ADD overhead when:
- [x] Documentation-heavy work (patterns, guides) ← Dominant
- [ ] Small fixes (<15 min)
- [ ] Tightly coupled files requiring atomic commits
- [ ] Time-critical work

**Assessment:**
- [ ] **USE WORKTREE** - Could help with isolation
- [x] **SKIP WORKTREE** - Documentation-heavy, less merge conflict risk
- [ ] **PM DECISION** - Mixed signals, escalate

**Rationale**: This is primarily documentation and pattern extraction work. The test fixtures and anti-flattening tests are isolated in `tests/unit/services/mux/`. Worktree overhead not justified.

### Part B: PM Verification Required

**PM, please confirm**:

1. **P1 infrastructure verified complete**: 101 tests, 14/14 deliverables
   - Verification: `pytest tests/unit/services/mux/ -v`

2. **Documentation locations**:
   - Grammar compliance audit: `docs/internal/architecture/current/grammar-compliance-audit.md`
   - Application patterns: `docs/internal/architecture/current/patterns/grammar-application-patterns.md`
   - Transformation guide: `docs/internal/development/grammar-transformation-guide.md`

3. **Test location**: `tests/unit/services/mux/test_anti_flattening.py`

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** - Understanding is correct
- [ ] **REVISE** - Need different approach
- [ ] **CLARIFY** - Need more context

---

## Phase 0: Setup & Context (1 hour)

### Objective
Verify infrastructure and gather context before auditing.

### Required Actions

1. **Verify P1 complete**
   ```bash
   pytest tests/unit/services/mux/ -v --tb=short
   # Expected: 101 tests passing
   ```

2. **Review P0 analysis documents**
   ```bash
   ls -la dev/2026/01/19/p0-*.md
   # Should show 4 documents
   ```

3. **Identify major features to audit**
   ```bash
   # List feature files
   ls -la services/features/

   # List intent handlers
   grep -n "async def _handle_" services/intent/intent_service.py | head -20
   ```

4. **Confirm intent classification as transformation target**
   ```bash
   # Check intent service structure
   wc -l services/intent/intent_service.py
   grep -c "def " services/intent/intent_service.py
   ```

### Deliverables
- [ ] Feature list for audit scope
- [ ] Confirmed access to P1 infrastructure
- [ ] Intent classification complexity assessment

### Evidence Required
```bash
# P1 test verification
pytest tests/unit/services/mux/ -v 2>&1 | tail -20

# Feature list
ls -la services/features/
```

---

## Phase 0.5-0.8: NOT APPLICABLE

These phases (Frontend-Backend Contract, Data Flow, Conversation Design, Post-Completion) are for UI/integration work. #404 is documentation and test infrastructure.

---

## Phase 1: Feature Grammar Audit (4 hours)

### Objective
Survey all major features for grammar expression.

### TDD Sequence

**Step 1.1: Create audit framework**
```bash
touch docs/internal/architecture/current/grammar-compliance-audit.md
```

**Step 1.2: Audit each feature against grammar criteria**

For each feature, evaluate:
1. **Entity awareness**: Does it track who is experiencing?
2. **Moment framing**: Are events scenes, not timestamps?
3. **Place atmosphere**: Does context affect presentation?
4. **Experience language**: Is it "I notice" not "data shows"?
5. **Lifecycle awareness**: Does it track transformations?

**Step 1.3: Create compliance matrix**

| Feature | Entity | Moment | Place | Experience | Lifecycle | Score |
|---------|--------|--------|-------|------------|-----------|-------|
| Morning Standup | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 |
| Intent Classification | ? | ? | ? | ? | ? | ?/5 |
| Todo Management | ? | ? | ? | ? | ? | ?/5 |
| [etc.] | | | | | | |

**Step 1.4: Identify transformation priorities**

Rank features by:
- Current grammar score (lower = higher priority)
- User impact (higher = higher priority)
- Complexity (lower = higher priority for early wins)

### Deliverables
- `docs/internal/architecture/current/grammar-compliance-audit.md`
  - Feature list with scores
  - Compliance matrix
  - Transformation priority ranking
  - Where Morning Standup patterns could propagate

### Evidence Required
```bash
# Show audit document exists and has content
wc -l docs/internal/architecture/current/grammar-compliance-audit.md
head -50 docs/internal/architecture/current/grammar-compliance-audit.md
```

---

## Phase 2: Application Pattern Catalog (6 hours)

### Objective
Formalize reusable patterns from Morning Standup.

### Sub-Phase 2.1: Extract Morning Standup Patterns (3 hours)

**Study Morning Standup deeply:**
```bash
# Read Morning Standup implementation
cat services/features/morning_standup.py
```

**Extract these patterns:**

1. **Context Dataclass Pair Pattern**
   - Input context (StandupContext) + Output result (StandupResult)
   - Separates gathering from presenting

2. **Parallel Place Gathering Pattern**
   - Gather from multiple Places concurrently
   - Handle partial failures gracefully

3. **Personality Bridge Pattern**
   - Transform raw data → warm narrative
   - Maintain entity identity throughout

4. **Warmth Calibration Pattern**
   - Adjust tone based on context/situation
   - "Quiet morning" vs "busy day"

5. **Honest Failure with Suggestion Pattern**
   - When data unavailable, suggest alternatives
   - Maintain warmth even in failure

### Sub-Phase 2.2: Create Grammar Application Templates (3 hours)

**Entity Awareness Template:**
```python
class EntityAwareFeature:
    """Template for features that track entity identity."""

    def __init__(self, entity: EntityProtocol):
        self.entity = entity

    async def experience(self, moment: MomentProtocol) -> Perception:
        """Entity experiences moment, returning perception."""
        ...
```

**Moment Framing Template:**
```python
@dataclass
class FeatureMoment(MomentProtocol):
    """Template for moments as scenes, not timestamps."""

    # Theatrical unities
    action: str  # What happened
    time_context: str  # "this morning", "yesterday"
    place_context: str  # Where it happened

    def captures(self) -> dict:
        """What this moment preserves."""
        ...
```

**Place Atmosphere Template:**
```python
@dataclass
class FeaturePlace(PlaceProtocol):
    """Template for places with atmosphere."""

    atmosphere: str  # warm, formal, urgent

    def render_in_context(self, data: dict) -> str:
        """Same data, different presentation based on atmosphere."""
        ...
```

**Situation Container Template:**
```python
async with Situation("Morning planning") as situation:
    # Group related moments
    situation.add_moment(calendar_moment)
    situation.add_moment(task_moment)

    # Extract learning on exit
    learning = situation.extract_learning()
```

### Deliverables
- `docs/internal/architecture/current/patterns/grammar-application-patterns.md`
  - 5 extracted patterns with examples
  - 4 grammar application templates
  - Each pattern follows existing pattern catalog format

### Evidence Required
```bash
# Pattern document exists with content
wc -l docs/internal/architecture/current/patterns/grammar-application-patterns.md
grep -c "## Pattern:" docs/internal/architecture/current/patterns/grammar-application-patterns.md
```

---

## Phase 3: Transformation Guide (4 hours)

### Objective
Enable developers to apply grammar independently.

### Sub-Phase 3.1: Create Step-by-Step Guide (2 hours)

**Guide Structure:**
1. **Identifying Grammar Elements** - How to spot them in existing code
2. **Refactoring Steps** - Transform flattened → conscious
3. **Using Protocols and Lenses** - P1 infrastructure usage
4. **Common Anti-Patterns** - What to avoid
5. **Decision Tree** - When to apply which pattern

**Example Decision Tree:**
```
Is the feature tracking a user/actor?
├── Yes → Apply Entity Awareness Template
│   └── Does actor have identity across flow?
│       ├── Yes → Use EntityProtocol
│       └── No → Add identity tracking
└── No → Consider: Should it be?

Does the feature present time-bound events?
├── Yes → Apply Moment Framing Template
│   └── Are they scenes or timestamps?
│       ├── Scenes → Use MomentProtocol
│       └── Timestamps → Add scene context
└── No → Consider if temporal awareness needed
```

### Sub-Phase 3.2: Worked Example - Intent Classification (2 hours)

**Document Current (Flattened) Flow:**
```python
# Current: Mechanical response
async def classify_intent(message: str) -> Intent:
    category = await self._classify(message)
    return Intent(category=category, message=message)
```

**Design Grammar-Applied Flow:**
```python
# After: Grammar-conscious response
async def classify_intent(message: str, user: EntityProtocol) -> Perception:
    # User experiences this moment of interaction
    moment = InteractionMoment(
        action=message,
        time_context="just now",
        place_context="conversation"
    )

    # Perceive through collaborative lens
    perception = await self.collaborative_lens.perceive(
        user,
        mode=PerceptionMode.NOTICING
    )

    # Experience-framed response
    return Perception(
        observation=f"I notice you're asking about {perception.topic}",
        ...
    )
```

**Before/After Comparison:**
| Aspect | Before (Flattened) | After (Grammar-Applied) |
|--------|-------------------|------------------------|
| Entity | None | User tracked as EntityProtocol |
| Moment | timestamp only | Scene with action + context |
| Place | None | Conversation as Place |
| Language | "category: QUERY" | "I notice you're asking..." |

### Deliverables
- `docs/internal/development/grammar-transformation-guide.md`
  - Step-by-step transformation process
  - Decision tree
  - Complete worked example (intent classification)
  - Before/after comparison

### Evidence Required
```bash
# Guide exists with required sections
wc -l docs/internal/development/grammar-transformation-guide.md
grep -c "## " docs/internal/development/grammar-transformation-guide.md
grep "Before" docs/internal/development/grammar-transformation-guide.md
```

---

## Phase 4: Anti-Flattening Infrastructure (4 hours)

### Objective
Create automated checks for grammar preservation.

### Sub-Phase 4.1: Define Anti-Flattening Tests (2 hours)

Based on ADR-045's 5 anti-flattening criteria:

```python
# tests/unit/services/mux/test_anti_flattening.py

def test_entity_has_identity():
    """Is Piper an Entity with identity? (Self-reference checks)"""
    # Feature should reference user/actor, not just IDs

def test_moments_are_scenes_not_timestamps():
    """Are Moments bounded scenes, not timestamps?"""
    # Moments should have action + time_context + place_context

def test_places_have_atmosphere():
    """Do Places have atmosphere, not just IDs?"""
    # Same data rendered differently based on place

def test_lifecycle_includes_transformation():
    """Does lifecycle include transformation?"""
    # State transitions tracked, not just current state

def test_consciousness_visible_in_implementation():
    """Can you see consciousness in the implementation?"""
    # Experience language, not data language
```

### Sub-Phase 4.2: Create Test Fixtures (2 hours)

**Conscious Fixture (passes all tests):**
```python
# tests/unit/services/mux/fixtures/conscious_feature.py

@dataclass
class ConsciousTodoHandler:
    """Example that passes anti-flattening tests."""

    async def handle_todo(self, user: EntityProtocol, task: str):
        moment = TaskMoment(
            action=f"adding task: {task}",
            time_context="right now",
            place_context="workspace"
        )

        perception = await user.experiences(moment)

        return f"I've noted that you want to {task}. " \
               f"I notice this connects to your focus on {perception.related_theme}."
```

**Flattened Fixture (fails tests):**
```python
# tests/unit/services/mux/fixtures/flattened_feature.py

class FlattenedTodoHandler:
    """Intentionally mechanical - should fail anti-flattening tests."""

    async def handle_todo(self, user_id: str, task: str):
        # No entity awareness - just ID
        # No moment framing - just data
        # No experience language - mechanical
        return {"task_id": uuid4(), "title": task, "user_id": user_id}
```

### Deliverables
- `tests/unit/services/mux/test_anti_flattening.py` (10+ tests)
- `tests/unit/services/mux/fixtures/conscious_feature.py`
- `tests/unit/services/mux/fixtures/flattened_feature.py`
- `tests/unit/services/mux/fixtures/__init__.py`

### Evidence Required
```bash
# Run anti-flattening tests
pytest tests/unit/services/mux/test_anti_flattening.py -v

# Show test count
pytest tests/unit/services/mux/test_anti_flattening.py --collect-only | grep "test_"
```

---

## Phase Z: Integration & Documentation (2 hours)

### Objective
Complete handoff and enable downstream work.

### Required Actions

1. **Update ADR-045 with implementation references**
   ```bash
   # Add references to patterns and tests
   vi docs/internal/architecture/current/adrs/adr-045-object-model.md
   ```

2. **Link patterns to P1 infrastructure in ADR-055**
   ```bash
   vi docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md
   ```

3. **Create developer onboarding checklist**
   ```markdown
   ## Grammar Onboarding Checklist
   - [ ] Read ADR-045 (grammar definition)
   - [ ] Read grammar-transformation-guide.md
   - [ ] Study Morning Standup reference implementation
   - [ ] Review grammar-application-patterns.md
   - [ ] Run anti-flattening tests to understand criteria
   - [ ] Complete practice transformation (suggested: [feature])
   ```

4. **Verify no regressions**
   ```bash
   pytest tests/ -m smoke
   # Expected: All passing, 0 regressions
   ```

5. **Update session log with completion evidence**

### Deliverables
- Updated ADR-045 with implementation links
- Updated ADR-055 with pattern links
- Developer onboarding checklist

### Evidence Required
```bash
# ADRs updated
git diff docs/internal/architecture/current/adrs/adr-045-object-model.md
git diff docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md

# No regressions
pytest tests/ -m smoke 2>&1 | tail -10
```

---

## Completion Matrix

**Use this to verify 100% completion before declaring "done"**

| Deliverable | Target | Status | Evidence |
|-------------|--------|--------|----------|
| Grammar compliance audit | 1 doc | ❌ | [pending] |
| Application patterns (5+) | 5 | ❌ | [pending] |
| Grammar templates (4) | 4 | ❌ | [pending] |
| Transformation guide | 1 doc | ❌ | [pending] |
| Worked example (intent) | 1 | ❌ | [pending] |
| Anti-flattening tests (10+) | 10+ | ❌ | [pending] |
| Conscious fixture | 1 | ❌ | [pending] |
| Flattened fixture | 1 | ❌ | [pending] |
| ADR-045 updated | 1 | ❌ | [pending] |
| ADR-055 updated | 1 | ❌ | [pending] |
| Onboarding checklist | 1 | ❌ | [pending] |

**TOTAL: 0/11 deliverables = 0%**

Only claim "complete" when 11/11 = 100%.

---

## STOP Conditions

**Standard STOP conditions**:
- Infrastructure doesn't match assumptions
- Tests fail for any reason (don't rationalize!)
- Pattern might already exist elsewhere
- Can't provide verification evidence
- Completion bias detected (claiming without proof)
- User data at risk

**Domain-specific STOP conditions**:
- #613 P1 infrastructure doesn't support pattern needs
- Anti-flattening criteria conflict with existing feature requirements
- Morning Standup patterns can't be generalized
- Guide becomes too abstract (no practical examples)
- Intent classification transformation proves infeasible

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Multi-Agent Deployment

### Recommendation: Single Agent, Sequential Documentation

**Rationale**:
- Documentation work benefits from consistent voice
- Patterns must be extracted before templates can reference them
- Transformation guide needs patterns and templates complete
- Anti-flattening tests need worked example as reference

### Optional Parallelization
After Phase 2, could split:
- Agent A: Phase 3 (Transformation Guide)
- Agent B: Phase 4 (Anti-Flattening Tests)

But consistency in documentation voice may favor single agent.

---

## Related Documentation

- Issue spec: GitHub Issue #404
- Parent epic: #399
- Depends on: #613 (P1) - COMPLETE
- P0 findings: `dev/2026/01/19/p0-*.md`
- P1 gameplan: `dev/2026/01/19/gameplan-mux-399-p1.md`
- Morning Standup: `services/features/morning_standup.py`
- MUX infrastructure: `services/mux/`

---

*Gameplan created: 2026-01-19*
*Template version: v9.3*
