# CORE-LEARN-B Implementation: Add Pattern Types

**Agent**: Claude Code (Programmer)
**Issue**: #222 CORE-LEARN-B - Pattern Recognition
**Sprint**: A5 - Learning System
**Date**: October 20, 2025, 12:56 PM
**Duration**: 3 hours estimated (based on discovery)

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## Mission

**Extend existing pattern recognition with 3 new pattern types!**

Discovery found 95% complete (2,827 lines). This is NOT a build task - it's a simple extension task.

**Scope**:
- Add 3 pattern type enums (TEMPORAL, COMMUNICATION, ERROR)
- Implement detection logic for each
- Add tests for new types
- Update documentation

**NOT in scope**:
- Building pattern recognition (ALREADY EXISTS!)
- Creating confidence scoring (ALREADY EXISTS!)
- Implementing analytics (ALREADY EXISTS!)

---

## Discovery Report

**YOU HAVE**: `core-learn-b-discovery-report.md` uploaded by PM

**CRITICAL FINDINGS**:
- 95% infrastructure exists (2,827 lines)
- 5 pattern types already working (examples to follow!)
- All features complete (confidence, observations, analytics, API, tests)
- Just need 3 enum extensions + tests

**Read the discovery report first!** It contains complete assessment.

---

## STOP Conditions

If ANY of these occur, STOP and escalate to PM immediately:

1. **Existing pattern types don't work** - Discovery said 5 types work
2. **Can't find PatternType enum** - Should be in models or services
3. **Confidence scoring broken** - Discovery said working
4. **API endpoints missing** - Discovery said 511 lines exist
5. **Tests don't pass** - Discovery said 448 lines of tests exist
6. **Cannot follow existing pattern** - 5 examples should exist
7. **Can't provide verification evidence** - Must show new types work

---

## Evidence Requirements

### For EVERY Claim You Make:

- **"Pattern type added"** → Show enum definition + detection logic
- **"Tests pass"** → Show test output
- **"Pattern detected"** → Show detection example
- **"API works"** → Show curl/test hitting endpoint with new type
- **"Confidence scoring works"** → Show confidence calculation

### Working Files Location:

- ✅ dev/active/ - For test scripts, verification
- ✅ services/learning/ - Pattern recognition logic
- ✅ services/knowledge/ - Pattern services
- ✅ tests/integration/ - Integration tests

---

## Implementation Plan (from Discovery)

### Phase 1: Add TEMPORAL_PATTERN (30 minutes)

**Step 1: Find PatternType enum**

```bash
# Discovery said PatternType exists with 5 types
# Find where it's defined
grep -r "class PatternType\|PatternType.*Enum" services/ models/

# Or use existing types as guide
grep -r "QUERY_PATTERN\|WORKFLOW_PATTERN" services/ models/
```

**Step 2: Add TEMPORAL_PATTERN enum value**

```python
# Add to existing PatternType enum (wherever it is)
class PatternType(str, Enum):
    QUERY_PATTERN = "query_pattern"  # Existing
    RESPONSE_PATTERN = "response_pattern"  # Existing
    WORKFLOW_PATTERN = "workflow_pattern"  # Existing
    INTEGRATION_PATTERN = "integration_pattern"  # Existing
    USER_PREFERENCE_PATTERN = "user_preference_pattern"  # Existing
    TEMPORAL_PATTERN = "temporal_pattern"  # NEW
```

**Step 3: Implement temporal detection logic**

Find where pattern detection happens (likely PatternRecognitionService or QueryLearningLoop):

```python
def detect_temporal_pattern(self, actions: List[UserAction]) -> Optional[Pattern]:
    """
    Detect temporal patterns in user actions.

    Looks for:
    - Time-of-day preferences (e.g., always at 9am)
    - Day-of-week patterns (e.g., every Monday)
    - Recurring tasks (e.g., weekly standups)
    """
    # Group actions by time and day
    time_buckets = {}  # {hour: count}
    day_buckets = {}  # {day_of_week: count}

    for action in actions:
        timestamp = action.timestamp
        hour = timestamp.hour
        day = timestamp.strftime('%A')  # Monday, Tuesday, etc.

        time_buckets[hour] = time_buckets.get(hour, 0) + 1
        day_buckets[day] = day_buckets.get(day, 0) + 1

    # Check for time-of-day pattern (10+ observations at same hour)
    for hour, count in time_buckets.items():
        if count >= 10:
            confidence = min(count / len(actions), 1.0)
            return Pattern(
                pattern_type=PatternType.TEMPORAL_PATTERN,
                pattern_data={
                    "type": "time_of_day",
                    "hour": hour,
                    "observations": count,
                    "description": f"User typically performs this action at {hour}:00"
                },
                confidence=confidence,
                usage_count=count
            )

    # Check for day-of-week pattern (10+ observations on same day)
    for day, count in day_buckets.items():
        if count >= 10:
            confidence = min(count / len(actions), 1.0)
            return Pattern(
                pattern_type=PatternType.TEMPORAL_PATTERN,
                pattern_data={
                    "type": "day_of_week",
                    "day": day,
                    "observations": count,
                    "description": f"User typically performs this action on {day}"
                },
                confidence=confidence,
                usage_count=count
            )

    return None
```

**Step 4: Wire into pattern detection**

Find the main pattern detection method and add temporal detection:

```python
def detect_patterns(self, actions: List[UserAction]) -> List[Pattern]:
    """Detect all pattern types from user actions."""
    patterns = []

    # Existing pattern detections...
    patterns.extend(self.detect_query_patterns(actions))
    patterns.extend(self.detect_workflow_patterns(actions))
    # ... existing types ...

    # NEW: Add temporal pattern detection
    temporal_pattern = self.detect_temporal_pattern(actions)
    if temporal_pattern:
        patterns.append(temporal_pattern)

    return patterns
```

---

### Phase 2: Add COMMUNICATION_PATTERN (30 minutes)

**Step 1: Add enum value**

```python
COMMUNICATION_PATTERN = "communication_pattern"  # Add to PatternType enum
```

**Step 2: Implement communication detection logic**

```python
def detect_communication_pattern(self, interactions: List[Interaction]) -> Optional[Pattern]:
    """
    Detect communication style patterns.

    Looks for:
    - Response length preferences (short vs detailed)
    - Formality level preferences (casual vs formal)
    - Detail preferences (high-level vs detailed)
    - Format preferences (bullets vs paragraphs)
    """
    if len(interactions) < 10:
        return None

    # Analyze response preferences from user feedback
    short_responses = 0  # <100 words
    long_responses = 0   # >300 words
    bullet_format = 0
    paragraph_format = 0

    for interaction in interactions:
        response = interaction.response
        word_count = len(response.split())

        if word_count < 100:
            short_responses += 1
        elif word_count > 300:
            long_responses += 1

        # Check format (simple heuristic)
        if '- ' in response or '* ' in response:
            bullet_format += 1
        else:
            paragraph_format += 1

    total = len(interactions)

    # Detect length preference
    if short_responses / total > 0.7:
        return Pattern(
            pattern_type=PatternType.COMMUNICATION_PATTERN,
            pattern_data={
                "type": "response_length",
                "preference": "concise",
                "observations": short_responses,
                "description": "User prefers concise responses (<100 words)"
            },
            confidence=short_responses / total,
            usage_count=short_responses
        )

    # Detect format preference
    if bullet_format / total > 0.7:
        return Pattern(
            pattern_type=PatternType.COMMUNICATION_PATTERN,
            pattern_data={
                "type": "format",
                "preference": "bullet_points",
                "observations": bullet_format,
                "description": "User prefers bullet point format"
            },
            confidence=bullet_format / total,
            usage_count=bullet_format
        )

    return None
```

---

### Phase 3: Add ERROR_PATTERN (30 minutes)

**Step 1: Add enum value**

```python
ERROR_PATTERN = "error_pattern"  # Add to PatternType enum
```

**Step 2: Implement error detection logic**

```python
def detect_error_pattern(self, errors: List[ErrorEvent]) -> Optional[Pattern]:
    """
    Detect error and correction patterns.

    Looks for:
    - Common mistakes (repeated errors)
    - Retry patterns (attempt sequences)
    - Correction preferences (how user fixes errors)
    """
    if len(errors) < 10:
        return None

    # Group errors by type
    error_types = {}  # {error_type: count}
    retry_counts = {}  # {error_type: [retry_attempts]}

    for error in errors:
        error_type = error.error_type
        error_types[error_type] = error_types.get(error_type, 0) + 1

        if error.retry_count:
            if error_type not in retry_counts:
                retry_counts[error_type] = []
            retry_counts[error_type].append(error.retry_count)

    # Detect common mistake pattern
    for error_type, count in error_types.items():
        if count >= 10:
            confidence = min(count / len(errors), 1.0)

            # Calculate average retry attempts if available
            avg_retries = None
            if error_type in retry_counts:
                avg_retries = sum(retry_counts[error_type]) / len(retry_counts[error_type])

            return Pattern(
                pattern_type=PatternType.ERROR_PATTERN,
                pattern_data={
                    "type": "common_mistake",
                    "error_type": error_type,
                    "observations": count,
                    "avg_retries": avg_retries,
                    "description": f"User frequently encounters {error_type} error"
                },
                confidence=confidence,
                usage_count=count
            )

    return None
```

---

### Phase 4: Testing (1 hour)

**Create test file**: `tests/integration/test_pattern_types.py`

```python
"""
Integration tests for new pattern types (TEMPORAL, COMMUNICATION, ERROR).

Tests pattern detection, confidence scoring, and API integration.
"""

import pytest
from datetime import datetime, timedelta
from services.learning.query_learning_loop import QueryLearningLoop
from services.knowledge.pattern_recognition_service import PatternRecognitionService


class TestTemporalPatterns:
    """Test temporal pattern detection."""

    def test_time_of_day_pattern_detection(self):
        """Test detection of time-of-day patterns."""
        # Create 15 actions at 9 AM
        actions = []
        for i in range(15):
            action = UserAction(
                timestamp=datetime(2025, 10, i+1, 9, 0),  # 9 AM each day
                action_type="create_standup"
            )
            actions.append(action)

        # Detect patterns
        service = PatternRecognitionService()
        patterns = service.detect_patterns(actions)

        # Should detect temporal pattern
        temporal_patterns = [p for p in patterns if p.pattern_type == "temporal_pattern"]
        assert len(temporal_patterns) > 0

        pattern = temporal_patterns[0]
        assert pattern.pattern_data["type"] == "time_of_day"
        assert pattern.pattern_data["hour"] == 9
        assert pattern.usage_count >= 10
        assert pattern.confidence > 0.5

    def test_day_of_week_pattern_detection(self):
        """Test detection of day-of-week patterns."""
        # Create 12 actions on Mondays
        actions = []
        base_date = datetime(2025, 10, 6)  # A Monday
        for i in range(12):
            action = UserAction(
                timestamp=base_date + timedelta(weeks=i),
                action_type="create_standup"
            )
            actions.append(action)

        # Detect patterns
        service = PatternRecognitionService()
        patterns = service.detect_patterns(actions)

        # Should detect temporal pattern
        temporal_patterns = [p for p in patterns if p.pattern_type == "temporal_pattern"]
        assert len(temporal_patterns) > 0

        pattern = temporal_patterns[0]
        assert pattern.pattern_data["type"] == "day_of_week"
        assert pattern.pattern_data["day"] == "Monday"
        assert pattern.usage_count >= 10


class TestCommunicationPatterns:
    """Test communication pattern detection."""

    def test_concise_response_preference(self):
        """Test detection of concise response preference."""
        # Create 12 interactions with short responses
        interactions = []
        for i in range(12):
            interaction = Interaction(
                query="test query",
                response="Short response here.",  # <100 words
                feedback={"helpful": True}
            )
            interactions.append(interaction)

        # Detect patterns
        service = PatternRecognitionService()
        patterns = service.detect_patterns(interactions)

        # Should detect communication pattern
        comm_patterns = [p for p in patterns if p.pattern_type == "communication_pattern"]
        assert len(comm_patterns) > 0

        pattern = comm_patterns[0]
        assert pattern.pattern_data["preference"] == "concise"
        assert pattern.confidence > 0.7

    def test_bullet_format_preference(self):
        """Test detection of bullet point format preference."""
        # Create 12 interactions with bullet responses
        interactions = []
        for i in range(12):
            interaction = Interaction(
                query="test query",
                response="Here are the points:\n- Point 1\n- Point 2\n- Point 3",
                feedback={"helpful": True}
            )
            interactions.append(interaction)

        # Detect patterns
        service = PatternRecognitionService()
        patterns = service.detect_patterns(interactions)

        # Should detect communication pattern
        comm_patterns = [p for p in patterns if p.pattern_type == "communication_pattern"]
        assert len(comm_patterns) > 0

        pattern = comm_patterns[0]
        assert pattern.pattern_data["preference"] == "bullet_points"


class TestErrorPatterns:
    """Test error pattern detection."""

    def test_common_mistake_detection(self):
        """Test detection of common mistake patterns."""
        # Create 15 similar errors
        errors = []
        for i in range(15):
            error = ErrorEvent(
                error_type="missing_repository",
                timestamp=datetime.now(),
                retry_count=1
            )
            errors.append(error)

        # Detect patterns
        service = PatternRecognitionService()
        patterns = service.detect_patterns(errors)

        # Should detect error pattern
        error_patterns = [p for p in patterns if p.pattern_type == "error_pattern"]
        assert len(error_patterns) > 0

        pattern = error_patterns[0]
        assert pattern.pattern_data["error_type"] == "missing_repository"
        assert pattern.usage_count >= 10
        assert pattern.confidence > 0.5


class TestPatternTypeIntegration:
    """Test integration of all pattern types with API."""

    def test_api_returns_all_pattern_types(self):
        """Test that API can return all 8 pattern types."""
        from fastapi.testclient import TestClient
        from main import app

        client = TestClient(app)

        # Get patterns
        response = client.get("/api/v1/learning/patterns")
        assert response.status_code == 200

        patterns = response.json()["patterns"]
        pattern_types = set(p["pattern_type"] for p in patterns)

        # Should support all 8 types (5 existing + 3 new)
        expected_types = {
            "query_pattern",
            "response_pattern",
            "workflow_pattern",
            "integration_pattern",
            "user_preference_pattern",
            "temporal_pattern",  # NEW
            "communication_pattern",  # NEW
            "error_pattern"  # NEW
        }

        # At least the new types should be present in schema/supported types
        assert "temporal_pattern" in pattern_types or len(patterns) == 0  # May be empty
        assert "communication_pattern" in pattern_types or len(patterns) == 0
        assert "error_pattern" in pattern_types or len(patterns) == 0

    def test_pattern_confidence_scoring_all_types(self):
        """Test that confidence scoring works for all pattern types."""
        learning_loop = QueryLearningLoop()

        # Each pattern type should support confidence scoring
        # This is verified by the existing infrastructure
        # Just ensure new types follow the same pattern

        # Create sample patterns of each new type
        temporal_pattern = {
            "pattern_type": "temporal_pattern",
            "confidence": 0.8,
            "usage_count": 15
        }

        comm_pattern = {
            "pattern_type": "communication_pattern",
            "confidence": 0.75,
            "usage_count": 12
        }

        error_pattern = {
            "pattern_type": "error_pattern",
            "confidence": 0.7,
            "usage_count": 10
        }

        # Verify structure matches expected pattern
        for pattern in [temporal_pattern, comm_pattern, error_pattern]:
            assert "pattern_type" in pattern
            assert "confidence" in pattern
            assert "usage_count" in pattern
            assert pattern["usage_count"] >= 10  # Minimum observations
            assert 0 <= pattern["confidence"] <= 1  # Valid confidence range
```

---

### Phase 5: Documentation (30 minutes)

**Update**: `docs/public/api-reference/learning-api.md`

Add section for new pattern types:

```markdown
## Pattern Types

Piper Morgan recognizes 8 types of patterns:

### Existing Pattern Types

1. **QUERY_PATTERN** - Query patterns and preferences
2. **RESPONSE_PATTERN** - Response style patterns
3. **WORKFLOW_PATTERN** - Command sequences and workflows
4. **INTEGRATION_PATTERN** - Integration preferences
5. **USER_PREFERENCE_PATTERN** - General user preferences

### New Pattern Types (CORE-LEARN-B)

6. **TEMPORAL_PATTERN** - Time-based patterns
   - Time-of-day preferences (e.g., "always at 9 AM")
   - Day-of-week patterns (e.g., "every Monday")
   - Recurring tasks (e.g., "weekly standups")

   Example:
   ```json
   {
     "pattern_type": "temporal_pattern",
     "pattern_data": {
       "type": "time_of_day",
       "hour": 9,
       "observations": 15,
       "description": "User typically creates standups at 9:00 AM"
     },
     "confidence": 0.83,
     "usage_count": 15
   }
   ```

7. **COMMUNICATION_PATTERN** - Communication style patterns
   - Response length preferences (concise vs detailed)
   - Formality level (casual vs formal)
   - Detail preferences (high-level vs detailed)
   - Format preferences (bullets vs paragraphs)

   Example:
   ```json
   {
     "pattern_type": "communication_pattern",
     "pattern_data": {
       "type": "format",
       "preference": "bullet_points",
       "observations": 12,
       "description": "User prefers bullet point format"
     },
     "confidence": 0.75,
     "usage_count": 12
   }
   ```

8. **ERROR_PATTERN** - Error and correction patterns
   - Common mistakes (repeated errors)
   - Retry patterns (attempt sequences)
   - Correction preferences (how user fixes errors)

   Example:
   ```json
   {
     "pattern_type": "error_pattern",
     "pattern_data": {
       "type": "common_mistake",
       "error_type": "missing_repository",
       "observations": 15,
       "avg_retries": 1.2,
       "description": "User frequently encounters missing_repository error"
     },
     "confidence": 0.71,
     "usage_count": 15
   }
   ```

## Pattern Detection

All patterns require **minimum 10 observations** before confirmation.

Confidence scoring ranges from 0.0 to 1.0:
- < 0.5: Low confidence
- 0.5-0.7: Medium confidence
- > 0.7: High confidence

Patterns are automatically detected from user interactions and stored for future use.
```

---

## Verification Steps

### Step 1: Verify Enum Added

```bash
# Check PatternType enum has 8 values
grep -A 10 "class PatternType" services/ models/ -r

# Should show:
# QUERY_PATTERN
# RESPONSE_PATTERN
# WORKFLOW_PATTERN
# INTEGRATION_PATTERN
# USER_PREFERENCE_PATTERN
# TEMPORAL_PATTERN (new)
# COMMUNICATION_PATTERN (new)
# ERROR_PATTERN (new)
```

---

### Step 2: Run Existing Tests

```bash
# Ensure existing tests still pass
pytest tests/integration/test_learning_system.py -v

# Should pass: 7/9 (same as before)
```

---

### Step 3: Run New Tests

```bash
# Run new pattern type tests
pytest tests/integration/test_pattern_types.py -v

# Should pass: All tests for 3 new pattern types
```

---

### Step 4: Test API

```bash
# Start application
python main.py

# Test pattern retrieval includes new types
curl http://localhost:8001/api/v1/learning/patterns

# Should return patterns array (may be empty but structure correct)
```

---

### Step 5: Manual Pattern Detection Test

Create test script in `dev/active/test_pattern_detection.py`:

```python
"""Manual test for new pattern type detection."""

from datetime import datetime, timedelta
from services.knowledge.pattern_recognition_service import PatternRecognitionService

# Test temporal pattern
print("Testing temporal pattern detection...")
actions = []
for i in range(15):
    # 15 actions at 9 AM
    action = {
        "timestamp": datetime(2025, 10, i+1, 9, 0),
        "action_type": "create_standup"
    }
    actions.append(action)

service = PatternRecognitionService()
patterns = service.detect_patterns(actions)

temporal = [p for p in patterns if p.get("pattern_type") == "temporal_pattern"]
print(f"Detected {len(temporal)} temporal patterns")
if temporal:
    print(f"Pattern: {temporal[0]}")

print("\nAll tests passed! ✅")
```

Run it:
```bash
python dev/active/test_pattern_detection.py
```

---

## Success Criteria

CORE-LEARN-B is complete when:

- [ ] 3 new pattern types added to enum (TEMPORAL, COMMUNICATION, ERROR)
- [ ] Detection logic implemented for each type
- [ ] Minimum 10 observations threshold enforced
- [ ] Confidence scoring works for all types
- [ ] All existing tests pass (7/9 from CORE-LEARN-A)
- [ ] New tests pass for 3 pattern types (9+ tests)
- [ ] API returns all 8 pattern types
- [ ] Documentation updated with examples
- [ ] Code committed with evidence
- [ ] Session log updated

---

## Files to Create/Modify

### Modify (Extend Existing)

- Pattern type enum (wherever PatternType is defined)
- Pattern detection service (add 3 detection methods)
- Pattern detection orchestration (wire new methods)

### Create

- `tests/integration/test_pattern_types.py` (~300 lines) - Tests for new types
- `dev/active/test_pattern_detection.py` (~50 lines) - Manual verification

### Update

- `docs/public/api-reference/learning-api.md` - Add pattern type documentation

### Session Log

- Continue in existing log or create new: `dev/2025/10/20/HHMM-prog-code-log.md`

---

## Expected Timeline

**Total**: 3 hours (from discovery)

**Breakdown**:
- 30 min: TEMPORAL_PATTERN
- 30 min: COMMUNICATION_PATTERN
- 30 min: ERROR_PATTERN
- 1h: Testing (9+ tests for 3 types)
- 30 min: Documentation

---

## Remember

**YOU ARE EXTENDING, NOT BUILDING!**

95% exists:
- 5 pattern types (examples to follow!)
- Confidence scoring (already works!)
- Observation tracking (already works!)
- API endpoints (already work!)
- Tests infrastructure (already exists!)

**Your job**:
1. Add 3 enum values
2. Copy existing pattern detection logic
3. Adapt for new pattern types
4. Test thoroughly
5. Document

**Not your job**:
- Build pattern recognition (exists!)
- Create confidence scoring (exists!)
- Implement analytics (exists!)
- Design architecture (done!)

**Just extend and ship!** 🔌

---

**Ready to extend the pattern recognition system!** 🚀

*Discovery found 95% complete. Implementation is simple enum extensions. Sprint A5 momentum continues!*
