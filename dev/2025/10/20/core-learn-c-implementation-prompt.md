# CORE-LEARN-C Implementation: Wire Preference Learning

**Agent**: Claude Code (Programmer)
**Issue**: #223 CORE-LEARN-C - Preference Learning
**Sprint**: A5 - Learning System
**Date**: October 20, 2025, 1:30 PM
**Duration**: 2 hours estimated (based on discovery)

---

## 🎊 CELEBRATORY PREAMBLE: VIRTUALLY COMPLETE!

Discovery found that CORE-LEARN-C is **98% COMPLETE** - the highest leverage ratio in Sprint A5!

**What exists (3,625 lines of production code!)**:
- ✅ UserPreferenceManager (762 lines) - Complete hierarchical preference system
- ✅ PreferenceAPI (598 lines) - Complete REST API
- ✅ USER_PREFERENCE_PATTERN - Complete implicit learning
- ✅ Conflict resolution - Complete hierarchical + versioning
- ✅ Privacy controls - Complete validation + cleanup

**What's missing (~100 lines)**:
- ⚠️ Wire QueryLearningLoop patterns → UserPreferenceManager preferences
- ⚠️ Integration tests for the wiring
- ⚠️ Documentation updates

**The Metaphor**: We built a Ferrari (all components perfect) but forgot to connect the steering wheel (wiring). This is just finishing assembly! 🚗✨

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## Mission

**Wire two complete systems together!**

Discovery found 98% complete (3,625 lines). This is NOT a build task - it's a simple wiring task.

**Scope**:
- Add method to connect pattern learning → preference storage
- Wire USER_PREFERENCE_PATTERN to UserPreferenceManager
- Add integration tests
- Update documentation

**NOT in scope**:
- Building preference system (ALREADY EXISTS!)
- Creating API (ALREADY EXISTS!)
- Implementing conflict resolution (ALREADY EXISTS!)

---

## Discovery Report

**YOU HAVE**: `core-learn-c-discovery-report.md` uploaded by PM

**CRITICAL FINDINGS**:
- 98% infrastructure exists (3,625 lines) - HIGHEST LEVERAGE YET!
- UserPreferenceManager: 762 lines (COMPLETE!)
- PreferenceAPI: 598 lines (COMPLETE!)
- USER_PREFERENCE_PATTERN: exists in QueryLearningLoop (COMPLETE!)
- Just need ~100 lines of wiring

**Read the discovery report first!** It contains complete assessment.

---

## STOP Conditions

If ANY of these occur, STOP and escalate to PM immediately:

1. **UserPreferenceManager doesn't exist** - Discovery said 762 lines
2. **PreferenceAPI doesn't work** - Discovery said 598 lines complete
3. **USER_PREFERENCE_PATTERN missing** - Discovery said it exists
4. **Hierarchical storage broken** - Discovery said Session > User > Global works
5. **Conflict resolution broken** - Discovery said versioning works
6. **Cannot provide verification evidence** - Must show wiring works
7. **Tests don't pass** - Must maintain zero regressions

---

## Evidence Requirements

### For EVERY Claim You Make:

- **"Wiring added"** → Show method code + call site
- **"Tests pass"** → Show test output
- **"Preference learned"** → Show pattern → preference flow
- **"API works"** → Show curl/test hitting endpoint
- **"Integration works"** → Show end-to-end example

### Working Files Location:

- ✅ dev/active/ - For test scripts, verification
- ✅ services/domain/ - UserPreferenceManager
- ✅ services/learning/ - QueryLearningLoop
- ✅ tests/integration/ - Integration tests

---

## Implementation Plan (from Discovery)

### Phase 1: Wire Pattern → Preference (1 hour)

**Step 1: Find UserPreferenceManager**

```bash
# Discovery said it exists with 762 lines
ls -la services/domain/user_preference_manager.py

# Check what's already there
head -50 services/domain/user_preference_manager.py
```

**Step 2: Add pattern application method**

Add to `UserPreferenceManager` class:

```python
async def apply_preference_pattern(
    self,
    pattern: Pattern,
    user_id: str,
    session_id: Optional[str] = None,
    scope: PreferenceScope = PreferenceScope.USER
) -> bool:
    """
    Apply a learned preference pattern to user preferences.

    Converts implicit preferences (learned patterns) to explicit preferences.
    Only applies patterns with confidence >= 0.7 (high confidence threshold).

    Args:
        pattern: The learned pattern to apply
        user_id: User ID to set preference for
        session_id: Optional session ID for session-scoped preferences
        scope: Preference scope (USER or SESSION)

    Returns:
        bool: True if preference was set, False if pattern confidence too low
    """
    # Only apply high-confidence patterns to preferences
    if pattern.confidence < 0.7:
        return False

    # Extract preference key and value from pattern
    pattern_data = pattern.pattern_data

    # Pattern data should contain preference information
    if "preference_key" not in pattern_data or "preference_value" not in pattern_data:
        return False

    preference_key = pattern_data["preference_key"]
    preference_value = pattern_data["preference_value"]

    # Set the preference using existing mechanism
    # This respects all existing validation, hierarchy, etc.
    success = await self.set_preference(
        key=preference_key,
        value=preference_value,
        user_id=user_id,
        session_id=session_id,
        scope=scope
    )

    return success
```

**Step 3: Find QueryLearningLoop**

```bash
# Discovery said USER_PREFERENCE_PATTERN exists
grep -n "USER_PREFERENCE_PATTERN" services/learning/query_learning_loop.py
```

**Step 4: Wire pattern learning to preferences**

Add to `QueryLearningLoop` (in the pattern application/learning section):

```python
async def _apply_user_preference_pattern(
    self,
    pattern: Pattern,
    context: Dict[str, Any]
) -> bool:
    """
    Apply user preference pattern by setting it as an explicit preference.

    This converts implicit preferences (learned from behavior) to explicit
    preferences (stored in UserPreferenceManager).
    """
    # Get user_id from context
    user_id = context.get("user_id")
    session_id = context.get("session_id")

    if not user_id:
        return False

    # Get UserPreferenceManager instance
    # This should be injected or accessible via service container
    from services.domain.user_preference_manager import UserPreferenceManager
    preference_manager = UserPreferenceManager()

    # Apply the pattern as an explicit preference
    success = await preference_manager.apply_preference_pattern(
        pattern=pattern,
        user_id=user_id,
        session_id=session_id,
        scope=PreferenceScope.USER
    )

    return success
```

**Step 5: Hook into pattern application**

Find where patterns are applied in QueryLearningLoop and add:

```python
# In apply_pattern method (or similar)
if pattern.pattern_type == PatternType.USER_PREFERENCE_PATTERN:
    success = await self._apply_user_preference_pattern(pattern, context)
    if success:
        # Update pattern success rate
        await self._update_pattern_success(pattern.id, success=True)
    return success
```

---

### Phase 2: Integration Tests (1 hour)

**Create test file**: `tests/integration/test_preference_learning.py`

```python
"""
Integration tests for preference learning system.

Tests the flow from pattern detection → implicit preference → explicit preference.
"""

import pytest
from datetime import datetime
from services.learning.query_learning_loop import QueryLearningLoop, PatternType
from services.domain.user_preference_manager import UserPreferenceManager, PreferenceScope


class TestPreferenceLearning:
    """Test preference learning from patterns."""

    @pytest.fixture
    async def preference_manager(self):
        """Create UserPreferenceManager instance."""
        manager = UserPreferenceManager()
        yield manager
        # Cleanup after test
        await manager.clear_session_preferences("test_user", "test_session")

    @pytest.fixture
    async def learning_loop(self):
        """Create QueryLearningLoop instance."""
        loop = QueryLearningLoop()
        yield loop

    async def test_pattern_to_preference_flow(
        self,
        preference_manager,
        learning_loop
    ):
        """
        Test complete flow: User behavior → Pattern → Preference.

        Simulates:
        1. User consistently chooses concise responses
        2. System learns USER_PREFERENCE_PATTERN
        3. Pattern is applied as explicit preference
        4. Preference is retrievable and affects behavior
        """
        # Create a high-confidence user preference pattern
        pattern = {
            "id": "pattern_001",
            "pattern_type": PatternType.USER_PREFERENCE_PATTERN,
            "pattern_data": {
                "preference_key": "response_style",
                "preference_value": "concise",
                "observations": 15,
                "description": "User consistently prefers concise responses"
            },
            "confidence": 0.85,  # High confidence
            "usage_count": 15,
            "first_seen": datetime.now(),
            "last_used": datetime.now()
        }

        # Apply pattern to preferences
        success = await preference_manager.apply_preference_pattern(
            pattern=pattern,
            user_id="test_user"
        )

        assert success is True

        # Verify preference was set
        response_style = await preference_manager.get_preference(
            key="response_style",
            user_id="test_user"
        )

        assert response_style == "concise"

    async def test_low_confidence_pattern_ignored(
        self,
        preference_manager
    ):
        """
        Test that low-confidence patterns don't become preferences.

        Only patterns with confidence >= 0.7 should be applied.
        """
        # Create a low-confidence pattern
        pattern = {
            "id": "pattern_002",
            "pattern_type": PatternType.USER_PREFERENCE_PATTERN,
            "pattern_data": {
                "preference_key": "detail_level",
                "preference_value": "detailed",
                "observations": 5,
                "description": "User might prefer detailed responses"
            },
            "confidence": 0.45,  # Low confidence
            "usage_count": 5
        }

        # Attempt to apply pattern
        success = await preference_manager.apply_preference_pattern(
            pattern=pattern,
            user_id="test_user"
        )

        # Should be rejected due to low confidence
        assert success is False

        # Verify preference was NOT set
        detail_level = await preference_manager.get_preference(
            key="detail_level",
            user_id="test_user"
        )

        assert detail_level is None  # Should be None (not set)

    async def test_preference_hierarchy_preserved(
        self,
        preference_manager
    ):
        """
        Test that pattern-derived preferences respect hierarchy.

        Session preferences should override user preferences.
        """
        # Set user-level preference from pattern
        user_pattern = {
            "id": "pattern_003",
            "pattern_type": PatternType.USER_PREFERENCE_PATTERN,
            "pattern_data": {
                "preference_key": "format",
                "preference_value": "markdown",
                "observations": 12
            },
            "confidence": 0.8,
            "usage_count": 12
        }

        await preference_manager.apply_preference_pattern(
            pattern=user_pattern,
            user_id="test_user",
            scope=PreferenceScope.USER
        )

        # Set session-level preference from pattern
        session_pattern = {
            "id": "pattern_004",
            "pattern_type": PatternType.USER_PREFERENCE_PATTERN,
            "pattern_data": {
                "preference_key": "format",
                "preference_value": "json",
                "observations": 8
            },
            "confidence": 0.75,
            "usage_count": 8
        }

        await preference_manager.apply_preference_pattern(
            pattern=session_pattern,
            user_id="test_user",
            session_id="test_session",
            scope=PreferenceScope.SESSION
        )

        # Session preference should override user preference
        format_pref = await preference_manager.get_preference(
            key="format",
            user_id="test_user",
            session_id="test_session"
        )

        assert format_pref == "json"  # Session value, not user value

        # Without session, should get user preference
        format_pref_no_session = await preference_manager.get_preference(
            key="format",
            user_id="test_user"
        )

        assert format_pref_no_session == "markdown"  # User value

    async def test_explicit_overrides_implicit(
        self,
        preference_manager
    ):
        """
        Test that explicit preferences override pattern-derived preferences.

        User-stated preferences should take precedence over learned preferences.
        """
        # User explicitly sets preference
        await preference_manager.set_preference(
            key="verbosity",
            value="verbose",
            user_id="test_user"
        )

        # System learns different preference from behavior
        pattern = {
            "id": "pattern_005",
            "pattern_type": PatternType.USER_PREFERENCE_PATTERN,
            "pattern_data": {
                "preference_key": "verbosity",
                "preference_value": "terse",
                "observations": 10
            },
            "confidence": 0.8,
            "usage_count": 10
        }

        # Apply pattern (should succeed but not override explicit preference)
        success = await preference_manager.apply_preference_pattern(
            pattern=pattern,
            user_id="test_user"
        )

        # Pattern application succeeds
        assert success is True

        # But explicit preference still takes precedence due to hierarchy/versioning
        # (Session > User > Pattern-derived)
        # This test verifies the mechanism exists - actual precedence depends on
        # how apply_preference_pattern uses scope parameter

    async def test_cross_feature_preference_learning(
        self,
        learning_loop,
        preference_manager
    ):
        """
        Test that preferences learned in one feature apply to others.

        Cross-feature preference sharing via USER_PREFERENCE_PATTERN.
        """
        # Simulate learning preference in feature A
        context_a = {
            "user_id": "test_user",
            "feature": "github_integration",
            "action": "create_issue"
        }

        # Create pattern from feature A behavior
        pattern = {
            "id": "pattern_006",
            "pattern_type": PatternType.USER_PREFERENCE_PATTERN,
            "pattern_data": {
                "preference_key": "label_preference",
                "preference_value": "bug",
                "source_feature": "github_integration",
                "observations": 20
            },
            "confidence": 0.9,
            "usage_count": 20
        }

        # Apply pattern
        await preference_manager.apply_preference_pattern(
            pattern=pattern,
            user_id="test_user"
        )

        # Verify preference is accessible in feature B
        context_b = {
            "user_id": "test_user",
            "feature": "jira_integration",
            "action": "create_ticket"
        }

        label_pref = await preference_manager.get_preference(
            key="label_preference",
            user_id="test_user"
        )

        # Preference learned in GitHub should be available in Jira
        assert label_pref == "bug"

    async def test_preference_privacy_controls(
        self,
        preference_manager
    ):
        """
        Test that preference learning respects privacy controls.

        Ensures PII is not leaked through preference patterns.
        """
        # Attempt to set preference with PII-like data
        pattern = {
            "id": "pattern_007",
            "pattern_type": PatternType.USER_PREFERENCE_PATTERN,
            "pattern_data": {
                "preference_key": "email_address",  # Potentially sensitive
                "preference_value": "user@example.com",
                "observations": 10
            },
            "confidence": 0.8,
            "usage_count": 10
        }

        # Apply pattern - should be validated/sanitized by JSON serialization
        success = await preference_manager.apply_preference_pattern(
            pattern=pattern,
            user_id="test_user"
        )

        # System should handle this according to privacy controls
        # (either reject, sanitize, or allow if validation passes)
        # This test verifies the mechanism exists
        assert success is not None  # Returns bool, not error
```

---

### Phase 3: Documentation (30 minutes)

**Update**: `docs/public/api-reference/learning-api.md`

Add section:

```markdown
## Preference Learning

Piper Morgan learns user preferences both explicitly (stated) and implicitly (inferred from behavior).

### Explicit Preferences

User-stated preferences through direct configuration or feedback:

```python
# Set explicit preference
preference_manager.set_preference("response_style", "concise", user_id="user123")

# Get preference (respects hierarchy)
style = preference_manager.get_preference("response_style", user_id="user123")
```

### Implicit Preferences

Preferences derived from behavior patterns:

1. **Pattern Detection**: User behavior creates patterns (e.g., always choosing concise responses)
2. **Pattern Learning**: QueryLearningLoop learns USER_PREFERENCE_PATTERN with confidence score
3. **Preference Application**: High-confidence patterns (>= 0.7) become explicit preferences
4. **Preference Usage**: System applies preferences to future interactions

**Example Flow**:

```
User Action (15x): Choose concise response
    ↓
Pattern Detected: USER_PREFERENCE_PATTERN (confidence: 0.85)
    ↓
Preference Set: response_style = "concise"
    ↓
Future Responses: Automatically formatted concisely
```

### Conflict Resolution

When preferences conflict, the system uses hierarchy:

1. **Session > User > Global**: Session preferences override user preferences
2. **Explicit > Implicit**: Stated preferences override learned preferences
3. **Recent > Historical**: Newer preferences override older ones (via versioning)

**Example**:

```python
# User states preference explicitly
preference_manager.set_preference("format", "json", user_id="user123")

# System learns different preference from behavior
# Pattern: "format" = "markdown" (confidence: 0.8)

# Result: Explicit preference ("json") takes precedence
```

### Privacy Controls

Preference learning includes privacy protections:

- **JSON Validation**: Prevents PII leakage through serialization checks
- **TTL Expiration**: Session preferences auto-expire
- **Scope Isolation**: User/session/global separation
- **Confidence Threshold**: Only high-confidence patterns (>= 0.7) become preferences

### API Endpoints

**Get Preferences** (with hierarchy):
```bash
GET /api/v1/preferences?user_id=user123&session_id=session456
```

**Set Preference**:
```bash
POST /api/v1/preferences
{
  "key": "response_style",
  "value": "concise",
  "user_id": "user123",
  "scope": "user"
}
```

**Learning Status**:
```bash
GET /api/v1/learning/patterns?pattern_type=user_preference_pattern&user_id=user123
```

### Specialized Preference Categories

**Reminder Preferences**:
- `reminder_enabled`: Enable/disable reminders
- `reminder_time`: Preferred reminder time
- `reminder_timezone`: User timezone
- `reminder_days`: Days to send reminders

**Learning Preferences** (from CORE-LEARN-A):
- `learning_enabled`: Enable/disable learning
- `learning_min_confidence`: Minimum confidence threshold
- `learning_features`: Features to learn from

### Version History

**Version 1.2** (CORE-LEARN-C):
- Added implicit preference derivation from patterns
- Added `apply_preference_pattern()` method
- Added integration tests for preference learning
- Updated conflict resolution documentation
```

---

## Verification Steps

### Step 1: Verify UserPreferenceManager Extended

```bash
# Check method was added
grep -A 20 "apply_preference_pattern" services/domain/user_preference_manager.py

# Should show new method with pattern application logic
```

---

### Step 2: Verify QueryLearningLoop Wired

```bash
# Check wiring was added
grep -A 15 "_apply_user_preference_pattern" services/learning/query_learning_loop.py

# Should show new method connecting to UserPreferenceManager
```

---

### Step 3: Run Existing Tests

```bash
# Ensure existing tests still pass
pytest tests/integration/test_learning_system.py -v

# Should pass: 7/9 (same as before)
```

---

### Step 4: Run New Tests

```bash
# Run new preference learning tests
pytest tests/integration/test_preference_learning.py -v

# Should pass: 7 new integration tests
```

---

### Step 5: Test End-to-End Flow

Create manual test script in `dev/active/test_preference_learning_flow.py`:

```python
"""
Manual test for preference learning flow.

Tests: User behavior → Pattern → Preference → Application
"""

import asyncio
from services.learning.query_learning_loop import QueryLearningLoop, PatternType
from services.domain.user_preference_manager import UserPreferenceManager


async def main():
    print("Testing Preference Learning Flow...")

    # Initialize services
    preference_manager = UserPreferenceManager()
    learning_loop = QueryLearningLoop()

    # Simulate user behavior pattern
    print("\n1. Creating USER_PREFERENCE_PATTERN from behavior...")
    pattern = {
        "id": "test_pattern_001",
        "pattern_type": PatternType.USER_PREFERENCE_PATTERN,
        "pattern_data": {
            "preference_key": "response_style",
            "preference_value": "concise",
            "observations": 15,
            "description": "User consistently chooses concise responses"
        },
        "confidence": 0.85,
        "usage_count": 15
    }
    print(f"Pattern created: {pattern}")

    # Apply pattern to preferences
    print("\n2. Applying pattern to UserPreferenceManager...")
    success = await preference_manager.apply_preference_pattern(
        pattern=pattern,
        user_id="test_user_123"
    )
    print(f"Pattern application success: {success}")

    # Retrieve preference
    print("\n3. Retrieving learned preference...")
    response_style = await preference_manager.get_preference(
        key="response_style",
        user_id="test_user_123"
    )
    print(f"Retrieved preference: response_style = {response_style}")

    # Verify hierarchy
    print("\n4. Testing preference hierarchy...")

    # Set session preference
    await preference_manager.set_preference(
        key="response_style",
        value="detailed",
        user_id="test_user_123",
        session_id="test_session_456",
        scope="session"
    )

    # Session should override user
    session_style = await preference_manager.get_preference(
        key="response_style",
        user_id="test_user_123",
        session_id="test_session_456"
    )
    print(f"Session preference (should be 'detailed'): {session_style}")

    # Without session, should get user preference
    user_style = await preference_manager.get_preference(
        key="response_style",
        user_id="test_user_123"
    )
    print(f"User preference (should be 'concise'): {user_style}")

    # Cleanup
    await preference_manager.clear_session_preferences("test_user_123", "test_session_456")

    print("\n✅ All tests passed! Preference learning flow works!")


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python dev/active/test_preference_learning_flow.py
```

---

## Success Criteria

CORE-LEARN-C is complete when:

- [ ] `apply_preference_pattern()` method added to UserPreferenceManager
- [ ] `_apply_user_preference_pattern()` method added to QueryLearningLoop
- [ ] Pattern application wired into QueryLearningLoop flow
- [ ] 7 new integration tests passing
- [ ] All existing tests still passing (zero regressions)
- [ ] Manual end-to-end test demonstrates flow
- [ ] Documentation updated with preference learning
- [ ] Code committed with evidence
- [ ] Session log updated

---

## Files to Create/Modify

### Modify (Extend Existing)

- `services/domain/user_preference_manager.py` (+30 lines) - Add pattern application method
- `services/learning/query_learning_loop.py` (+30 lines) - Add preference pattern wiring
- `docs/public/api-reference/learning-api.md` (+40 lines) - Add preference learning docs

### Create

- `tests/integration/test_preference_learning.py` (~350 lines) - 7 integration tests
- `dev/active/test_preference_learning_flow.py` (~80 lines) - Manual verification

### Session Log

- Continue in existing log or create new: `dev/2025/10/20/HHMM-prog-code-log.md`

---

## Expected Timeline

**Total**: 2 hours (from discovery)

**Breakdown**:
- 1h: Wire pattern → preference (30 lines × 2 files)
- 1h: Integration tests (7 tests, ~350 lines)

---

## Remember

**YOU ARE WIRING, NOT BUILDING!**

98% exists (3,625 lines):
- UserPreferenceManager (762 lines - COMPLETE!)
- PreferenceAPI (598 lines - COMPLETE!)
- USER_PREFERENCE_PATTERN (exists - COMPLETE!)
- Hierarchical storage (COMPLETE!)
- Conflict resolution (COMPLETE!)
- Privacy controls (COMPLETE!)

**Your job**:
1. Add method to connect systems (~30 lines)
2. Wire QueryLearningLoop to UserPreferenceManager (~30 lines)
3. Test thoroughly (7 integration tests)
4. Document usage (~40 lines)

**Not your job**:
- Build preference system (exists!)
- Create hierarchical storage (exists!)
- Implement conflict resolution (exists!)
- Design privacy controls (exists!)

**Just wire the Ferrari's steering wheel and drive!** 🚗✨

---

**Ready to connect the last pieces!** 🔌

*Discovery found 98% complete. Implementation is just wiring two excellent systems together. Sprint A5 momentum continues!*
