# Sprint A5 Gameplan: CORE-LEARN-A - Learning Infrastructure Foundation

**Sprint**: A5
**Issue**: #221 CORE-LEARN-A
**Duration**: 2-3 days estimated (likely <1 day actual based on velocity)
**Context**: Foundation for all learning capabilities

---

## Executive Summary

CORE-LEARN-A establishes the foundational learning infrastructure for Piper Morgan. This creates the base service framework, storage layer, and observation capabilities that all future learning features will build upon.

---

## Phase 0: Discovery & Assessment (30-45 minutes)

**Objective**: Identify existing learning infrastructure

**Investigation Areas**:
```python
# Check for existing learning components
mcp__serena__search_project("learning|pattern|preference", file_pattern="services/**/*.py")
mcp__serena__search_project("UserPattern|WorkflowPattern", file_pattern="models/**/*.py")
mcp__serena__find_symbol("PatternRecognizer|PreferenceTracker", scope="services")

# Check for existing storage patterns
mcp__serena__search_project("pattern.*storage|preference.*persist", file_pattern="**/*.py")

# Look for privacy/compliance code
mcp__serena__search_project("privacy|compliant|anonymize", file_pattern="services/**/*.py")
```

**Expected Findings**:
- Pattern recognition handler (94 lines mentioned in A4)
- UserPreferenceManager (extended in A4)
- Possible learning fragments from earlier work
- Privacy utilities from ethics implementation

**Deliverables**:
- Assessment of existing infrastructure
- Gap analysis for required components
- Revised time estimate

---

## Phase 1: Core Service Framework (2-3 hours)

**Objective**: Establish learning service structure

### 1.1 Create Learning Service (1 hour)

```python
# services/learning/learning_service.py
class LearningService:
    def __init__(self,
                 pattern_recognizer: PatternRecognizer,
                 preference_tracker: PreferenceTracker,
                 workflow_optimizer: WorkflowOptimizer,
                 storage: LearningStorage):
        self.pattern_recognizer = pattern_recognizer
        self.preference_tracker = preference_tracker
        self.workflow_optimizer = workflow_optimizer
        self.storage = storage

    async def observe_action(self, action: UserAction) -> None:
        """Log user action for pattern detection"""
        # Privacy-compliant logging
        # No automation, just observation

    async def get_patterns(self, user_id: str) -> List[Pattern]:
        """Retrieve learned patterns for user"""
```

### 1.2 Pattern Recognition Component (1 hour)

```python
# services/learning/pattern_recognizer.py
class PatternRecognizer:
    def detect_patterns(self, actions: List[UserAction]) -> List[Pattern]:
        """Detect patterns from user actions"""
        # Temporal patterns (time of day, day of week)
        # Workflow patterns (action sequences)
        # Communication patterns (preferences)
```

### 1.3 Preference Tracker (30 minutes)

```python
# services/learning/preference_tracker.py
class PreferenceTracker:
    def __init__(self, user_preference_manager: UserPreferenceManager):
        self.pref_manager = user_preference_manager  # Reuse from A4

    def track_preference(self, preference: UserPreference) -> None:
        """Track implicit and explicit preferences"""
```

### 1.4 Workflow Optimizer Stub (30 minutes)

```python
# services/learning/workflow_optimizer.py
class WorkflowOptimizer:
    def analyze_workflow(self, workflow: Workflow) -> OptimizationSuggestions:
        """Analyze workflow for optimization opportunities"""
        # Stub for now, full implementation in CORE-LEARN-D
```

---

## Phase 2: Storage Layer (2 hours)

**Objective**: Implement privacy-compliant storage

### 2.1 Storage Design (30 minutes)

```python
# services/learning/storage/learning_storage.py
class LearningStorage:
    """
    Privacy-compliant storage for learning data
    - Patterns stored without PII
    - Aggregated insights only
    - User control over data
    """

    async def store_pattern(self, pattern: Pattern) -> None:
        """Store anonymized pattern"""

    async def get_user_patterns(self, user_id: str) -> List[Pattern]:
        """Retrieve patterns for user"""
```

### 2.2 Data Models (30 minutes)

```python
# services/learning/models/user_pattern.py
@dataclass
class UserPattern:
    pattern_id: str
    pattern_type: PatternType
    confidence: float
    detected_at: datetime
    metadata: Dict[str, Any]  # No PII

# services/learning/models/workflow_pattern.py
@dataclass
class WorkflowPattern:
    pattern_id: str
    action_sequence: List[str]  # Anonymized actions
    frequency: int
    avg_duration: float
```

### 2.3 Privacy Utilities (30 minutes)

```python
# services/learning/privacy/anonymizer.py
class ActionAnonymizer:
    def anonymize_action(self, action: UserAction) -> AnonymizedAction:
        """Remove PII from user action"""
        # Strip sensitive data
        # Preserve patterns
        # Maintain utility
```

### 2.4 Database Schema (30 minutes)

```sql
-- SQLite schema for learning storage
CREATE TABLE user_patterns (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,  -- Hashed
    pattern_type TEXT NOT NULL,
    pattern_data TEXT NOT NULL,  -- JSON, no PII
    confidence REAL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE workflow_patterns (
    id INTEGER PRIMARY KEY,
    pattern_hash TEXT UNIQUE,
    action_sequence TEXT,  -- JSON array
    frequency INTEGER,
    avg_duration_ms INTEGER
);
```

---

## Phase 3: Basic Learning Loop (2 hours)

**Objective**: Implement observation and pattern detection

### 3.1 Action Observer (45 minutes)

```python
# services/learning/observer.py
class ActionObserver:
    def __init__(self, learning_service: LearningService):
        self.learning_service = learning_service

    async def observe(self, action: UserAction) -> None:
        """Observe and log user action"""
        # Anonymize action
        # Queue for pattern detection
        # Store for analysis
        # No automation triggered
```

### 3.2 Pattern Detection Pipeline (45 minutes)

```python
# services/learning/pipeline.py
class LearningPipeline:
    async def process_actions(self, actions: List[UserAction]) -> List[Pattern]:
        """Process actions through learning pipeline"""
        # 1. Anonymize
        # 2. Detect patterns
        # 3. Store patterns
        # 4. Update preferences
        # Return patterns (no automation)
```

### 3.3 API Endpoints (30 minutes)

```python
# web/api/learning.py
@router.get("/api/v1/learning/patterns")
async def get_patterns(user_id: str = Depends(get_current_user)):
    """Get learned patterns for user"""
    patterns = await learning_service.get_patterns(user_id)
    return {"patterns": patterns}

@router.post("/api/v1/learning/observe")
async def observe_action(action: UserAction):
    """Log user action for learning"""
    await learning_service.observe_action(action)
    return {"status": "observed"}
```

---

## Phase 4: Testing & Integration (1.5 hours)

**Objective**: Ensure quality and integration

### 4.1 Unit Tests (45 minutes)

```python
# tests/learning/test_pattern_recognizer.py
def test_temporal_pattern_detection():
    """Test time-based pattern detection"""

def test_workflow_pattern_detection():
    """Test action sequence pattern detection"""

def test_preference_tracking():
    """Test preference observation"""
```

### 4.2 Integration Tests (30 minutes)

```python
# tests/integration/test_learning_pipeline.py
def test_end_to_end_learning():
    """Test full learning pipeline"""
    # Submit actions
    # Verify patterns detected
    # Check storage
    # Validate privacy
```

### 4.3 Privacy Compliance Tests (15 minutes)

```python
# tests/learning/test_privacy.py
def test_no_pii_storage():
    """Verify no PII in stored patterns"""

def test_anonymization():
    """Test action anonymization"""
```

---

## Success Criteria

- [ ] Learning service starts with application
- [ ] User actions can be observed (API endpoint working)
- [ ] Patterns detected and stored
- [ ] Patterns queryable via API
- [ ] No PII in stored data
- [ ] All tests passing
- [ ] Documentation complete

---

## Risk Mitigation

### Low Risk
- Reusing UserPreferenceManager
- Following established service patterns
- SQLite for simple storage start

### Medium Risk
- Privacy compliance complexity
- Pattern detection accuracy
- Performance with many actions

### Mitigation
- Start simple, iterate
- Use existing privacy utilities
- Background processing for patterns

---

## Definition of Done

1. All code implemented and tested
2. API endpoints functional
3. Privacy compliance verified
4. Documentation complete
5. Ready for CORE-LEARN-B to build upon

---

## Time Estimate

**Original**: 2-3 days
**Revised based on velocity**: 4-8 hours
**Confidence**: High (based on A4 pattern)

The discovery phase will likely reveal 50-75% already exists, compressing this to half a day of work.

---

*Ready for execution!*
